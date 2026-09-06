#!/usr/bin/env python3
"""Quali temi si stanno scaldando in italiano, misurato su it.wikipedia.

    python3 trend_topics.py
    python3 trend_topics.py --temi "Menopausa,Burnout,Longevità"

PERCHE' NON BASTA GUARDARE LE VISITE
Wikipedia perde traffico su tutto — risposte AI, zero-click. Nel paniere di
controllo il calo mediano e' circa -48% in tre anni. Un tema che perde il 20%
sta quindi CRESCENDO rispetto alla piattaforma. Guardare il numero assoluto
farebbe scartare esattamente i temi che si stanno scaldando.

    indice = crescita della voce / crescita mediana del paniere di controllo

    indice > 1  regge o sale contro corrente -> tema che si scalda
    indice < 1  scende piu' della media       -> tema che si raffredda

COSA QUESTO STRUMENTO NON DICE
Dice se l'interesse sale, non se lo scaffale e' libero. Un tema in crescita
con sei libri sopra resta un tema con sei libri sopra: l'offerta va misurata
a parte, cercando i titoli.

UNO ZERO NON E' MAI UN DATO, FINCHE' NON E' CONFERMATO
Una richiesta fallita e una voce inesistente sono cose diverse, e confonderle
produce falsi zeri: e' gia' successo qui, con sei worker in parallelo che si
prendevano un 429 e diventavano "voce inesistente". Solo un 404, o la chiave
"-1" dell'API, contano come assenza. Tutto il resto e' un guasto, si ritenta,
e se resta irraggiungibile si dichiara PARZIALE la classifica.
"""
import argparse, json, statistics, sys, time, urllib.error, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

UA = "kdp-studio-research/1.0"
PAGEVIEWS = ("https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/"
             "it.wikipedia/all-access/user/{}/monthly/2021010100/2026090100")
WIKI_API = "https://it.wikipedia.org/w/api.php?action=query&redirects=1&format=json&titles={}"

# Ultimi 12 mesi completi contro gli stessi 12 mesi tre anni prima: stessi mesi
# da una parte e dall'altra, cosi' la stagionalita' si annulla da sola.
RECENTI = [f"2025{m:02d}" for m in range(9, 13)] + [f"2026{m:02d}" for m in range(1, 9)]
BASE    = [f"2022{m:02d}" for m in range(9, 13)] + [f"2023{m:02d}" for m in range(1, 9)]
BASE_MINIMA = 600   # sotto questa soglia il rapporto e' rumore, non tendenza

CONTROLLO = ["Italia", "Roma", "Acqua", "Matematica", "Storia",
             "Musica", "Cane", "Sole", "Cucina", "Automobile"]

TEMI_PREDEFINITI = [
    "Disturbo da deficit di attenzione e iperattività", "Disturbo dello spettro autistico",
    "Burnout", "Disturbo borderline di personalità", "Dislessia",
    "Disturbo post traumatico da stress", "Menopausa", "Endometriosi",
    "Sindrome dell'ovaio policistico", "Infertilità", "Dipendenza da Internet",
    "Sigaretta elettronica", "Gioco d'azzardo patologico",
    "Disturbo da alimentazione incontrollata", "Intelligenza artificiale",
    "Caregiver", "Solitudine", "Smart working", "Educazione finanziaria",
    "Longevità", "Digiuno intermittente", "Microbiota", "Disturbo del sonno",
    "Ansia", "Narcisismo", "Mindfulness", "Adolescenza", "Cambiamento climatico",
]


class Irraggiungibile(Exception):
    """La richiesta non e' riuscita. NON significa che la voce non esista."""


def get_json(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    ultimo = None
    for tentativo in range(5):
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None            # unico caso in cui l'assenza e' reale
            ultimo = e
        except Exception as e:
            ultimo = e
        time.sleep(1.5 * (tentativo + 1))
    raise Irraggiungibile(f"{type(ultimo).__name__}: {ultimo}")


def resolve(titolo: str):
    d = get_json(WIKI_API.format(urllib.parse.quote(titolo)))
    if d is None:
        return None
    for pid, p in d.get("query", {}).get("pages", {}).items():
        if pid != "-1":
            return p.get("title")
    return None


def serie(titolo: str) -> dict:
    d = get_json(PAGEVIEWS.format(urllib.parse.quote(titolo.replace(" ", "_"), safe="")))
    if not d or "items" not in d:
        return {}
    return {i["timestamp"][:6]: i["views"] for i in d["items"]}


def crescita(s: dict):
    rec = sum(s.get(m, 0) for m in RECENTI)
    bas = sum(s.get(m, 0) for m in BASE)
    return (None if bas < BASE_MINIMA else rec / bas), rec, bas


def misura(titolo: str):
    try:
        vero = resolve(titolo)
    except Irraggiungibile as e:
        return titolo, None, None, 0, 0, f"IRRAGGIUNGIBILE ({e})"
    if not vero:
        return titolo, None, None, 0, 0, "voce assente (404 confermato)"
    try:
        s = serie(vero)
    except Irraggiungibile as e:
        return titolo, vero, None, 0, 0, f"IRRAGGIUNGIBILE ({e})"
    g, rec, bas = crescita(s)
    return titolo, vero, g, rec, bas, "" if g is not None else f"base troppo magra ({bas})"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--temi", default="", help="elenco separato da virgole; vuoto = predefiniti")
    ap.add_argument("--out", default="trend-it.json")
    ap.add_argument("--workers", type=int, default=2,
                    help="tenerlo basso: sopra 2 Wikipedia risponde 429")
    args = ap.parse_args()
    temi = [t.strip() for t in args.temi.split(",") if t.strip()] or TEMI_PREDEFINITI

    print("Paniere di controllo (calo di piattaforma):", file=sys.stderr)
    ctrl = []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for t, vero, g, rec, bas, nota in ex.map(misura, CONTROLLO):
            if g:
                ctrl.append(g)
                print(f"  {t:<12} {g:.3f}", file=sys.stderr)
    if len(ctrl) < 5:
        print("Paniere di controllo incompleto: senza baseline l'indice non ha "
              "significato. Rilanciare.", file=sys.stderr)
        return 1
    baseline = statistics.median(ctrl)
    print(f"  mediana = {baseline:.3f}\n", file=sys.stderr)

    righe, irraggiungibili, scartati = [], [], []
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        for t, vero, g, rec, bas, nota in ex.map(misura, temi):
            if g is None:
                (irraggiungibili if "IRRAGGIUNGIBILE" in nota else scartati).append(f"{t}: {nota}")
                continue
            righe.append((g / baseline, g, rec, bas, vero))
    righe.sort(reverse=True)

    print(f"{'indice':>7} {'grezzo':>7} {'12m rec.':>9} {'12m base':>9}  voce")
    for idx, g, rec, bas, vero in righe:
        print(f"{idx:7.2f} {g:7.2f} {rec:9d} {bas:9d}  {vero}")
    json.dump({"baseline": round(baseline, 4),
               "righe": [{"indice": round(i, 3), "grezzo": round(g, 3),
                          "recenti": r, "base": b, "voce": v} for i, g, r, b, v in righe],
               "irraggiungibili": irraggiungibili, "scartati": scartati},
              open(args.out, "w"), ensure_ascii=False, indent=1)

    # Riepilogo finale: gli avvisi vanno letti, non sepolti a meta' output.
    print(f"\n--- {len(righe)} temi misurati, {len(scartati)} scartati, "
          f"{len(irraggiungibili)} irraggiungibili ---")
    for s in scartati:
        print(f"  scartato: {s}")
    for s in irraggiungibili:
        print(f"  ! {s}")
    if irraggiungibili:
        print("\nCLASSIFICA PARZIALE: le voci qui sopra non sono state misurate per\n"
              "guasto di rete, NON perche' assenti. Rilanciare prima di concluderne\n"
              "qualcosa.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
