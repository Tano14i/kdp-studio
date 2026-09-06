#!/usr/bin/env python3
"""Mappa della domanda reale su un marketplace Amazon, dai suggerimenti di ricerca.

Non parte da nicchie scelte a tavolino: parte da radici a verbo di intento
("come smettere di", "come superare") e lascia che sia l'autocomplete di Amazon
a dire cosa cercano davvero i lettori. Espande ogni radice lettera per lettera,
e approfondisce solo i prefissi che hanno dato frutto.

    python3 harvest_demand.py --market it
    python3 harvest_demand.py --market de --out domanda-de.json

Due cose imparate sul campo, che questo script rispetta:

1. L'host DEVE essere completion.amazon.<tld> del mercato interrogato. Su
   completion.amazon.com ogni marketplace non-US risponde 200 con zero
   suggerimenti: uno zero falso che si legge come "nicchia senza domanda".
   La tabella dei mercati e' quella di kdp_server.py, letta da li'.

2. Su Amazon.it l'alias stripbooks NON filtra ai soli libri: radici nominali
   ("guida per") tornano ferramenta. Le radici a verbo di intento restano
   pulite, perche' nessuno cerca una guida per cassetti scrivendo "come
   smettere di". Per questo le radici predefinite sono tutte verbali.
"""
import argparse, json, pathlib, string, sys, time, urllib.parse, urllib.request
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Radici per lingua. Verbo + preposizione: e' il linguaggio di chi ha un
# problema, non di chi cerca un argomento.
ROOTS = {
    "it": ["come smettere di ", "come superare ", "come gestire ", "come vincere ",
           "come affrontare ", "come uscire da", "come liberarsi ", "come curare ",
           "come convivere con ", "come ritrovare ", "come imparare a ", "come non "],
    "us": ["how to stop ", "how to overcome ", "how to deal with ", "how to manage ",
           "how to quit ", "how to cope with ", "how to learn to ", "how not to "],
    "uk": ["how to stop ", "how to overcome ", "how to deal with ", "how to manage ",
           "how to quit ", "how to cope with ", "how to learn to ", "how not to "],
    "de": ["wie man aufhört ", "wie überwinde ich ", "wie gehe ich um mit ",
           "wie lerne ich ", "wie werde ich "],
    "fr": ["comment arrêter de ", "comment surmonter ", "comment gérer ",
           "comment vivre avec ", "comment apprendre à "],
    "es": ["como dejar de ", "como superar ", "como gestionar ",
           "como vivir con ", "como aprender a "],
}


def load_markets(server_path: pathlib.Path) -> dict:
    """Rilegge AMAZON_MARKETS da kdp_server.py senza importarlo.

    Importare il modulo tirerebbe dentro anthropic, fastapi e la API key:
    qui serve solo la tabella, e deve restare una sola (kdp_server.py).
    """
    try:
        src = server_path.read_text(encoding="utf-8")
        inizio = src.index("AMAZON_MARKETS = {")
        fine = src.index("def amazon_market(", inizio)
    except (OSError, ValueError) as e:
        raise SystemExit(
            f"Non riesco a leggere la tabella dei marketplace da {server_path}: {e}\n"
            "Se AMAZON_MARKETS e' stata rinominata o spostata, va aggiornato anche "
            "questo script.") from e
    ns: dict = {}
    exec(src[inizio:fine], ns)
    return ns["AMAZON_MARKETS"]


def make_suggester(mk: dict, retries: int = 2):
    host = f"completion.amazon.{mk['tld']}"

    def suggest(prefix: str) -> list[str]:
        q = urllib.parse.urlencode({
            "limit": 11, "prefix": prefix, "suggestion-type": "KEYWORD",
            "page-type": "Search", "alias": "stripbooks", "site-variant": "desktop",
            "version": "3", "event": "onKeyPress", "wc": "",
            "lop": mk["lop"], "mid": mk["mid"]})
        req = urllib.request.Request(f"https://{host}/api/2017/suggestions?{q}", headers={
            "User-Agent": UA, "Accept": "application/json",
            "Accept-Language": mk["accept_language"]})
        for _ in range(retries):
            try:
                with urllib.request.urlopen(req, timeout=12) as r:
                    data = json.loads(r.read().decode("utf-8"))
                return [v for s in data.get("suggestions", [])
                        if (v := (s.get("value") or "").strip())
                        and v.lower() != prefix.strip().lower()]
            except Exception:
                time.sleep(0.6)
        return []
    return suggest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--market", default="it", help="it, de, fr, es, uk, us")
    ap.add_argument("--out", default="", help="file JSON di uscita")
    ap.add_argument("--workers", type=int, default=8)
    args = ap.parse_args()

    here = pathlib.Path(__file__).parent
    markets = load_markets(here / "kdp_server.py")
    code = args.market.strip().lower()
    if code not in markets:
        print(f"Mercato sconosciuto: {code!r}. Disponibili: {', '.join(markets)}",
              file=sys.stderr)
        return 2
    if code not in ROOTS:
        print(f"Nessuna radice di intento definita per {code!r}: aggiungila a ROOTS.",
              file=sys.stderr)
        return 2

    mk = markets[code]
    suggest = make_suggester(mk)
    print(f"Mercato: amazon.{mk['tld']} ({mk['lop']})", file=sys.stderr)

    # Prova a vuoto: se il mercato non risponde e' inutile fare 2000 chiamate
    # e concludere che la domanda non esiste.
    probe = ROOTS[code][0]
    if not suggest(probe):
        print(f"ERRORE: {probe!r} non restituisce nulla su completion.amazon.{mk['tld']}.\n"
              f"Prima di concludere che non c'e' domanda, verifica host, mid e lop.",
              file=sys.stderr)
        return 1

    results: dict[str, set] = defaultdict(set)

    def probe_one(job):
        root, pfx = job
        return root, pfx, suggest(pfx)

    jobs = [(r, r + c) for r in ROOTS[code] for c in [""] + list(string.ascii_lowercase)]
    live = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for root, pfx, sug in ex.map(probe_one, jobs):
            if sug:
                live.append((root, pfx))
                results[root].update(sug)
    print(f"livello 1: {len(jobs)} chiamate, {len(live)} prefissi vivi", file=sys.stderr)

    jobs2 = [(r, p + c) for r, p in live for c in string.ascii_lowercase]
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for root, pfx, sug in ex.map(probe_one, jobs2):
            results[root].update(sug)
    print(f"livello 2: {len(jobs2)} chiamate", file=sys.stderr)

    out = {r: sorted(v) for r, v in sorted(results.items())}
    total = sum(len(v) for v in out.values())
    dest = pathlib.Path(args.out or f"domanda-{code}.json")
    dest.write_text(json.dumps(
        {"market": code, "tld": mk["tld"], "queries": out, "total": total},
        ensure_ascii=False, indent=1), encoding="utf-8")

    for root, qs in out.items():
        print(f"\n=== {root!r} — {len(qs)} ===")
        for q in qs:
            print(f"   {q}")
    print(f"\n{total} query di intento uniche -> {dest}")
    if total == 0:
        print("Zero query: e' lo strumento, non il mercato. Controlla la tabella.",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
