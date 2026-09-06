#!/usr/bin/env python3
"""Verifica che ogni marketplace della tabella risponda davvero.

Copre TUTTE le righe di AMAZON_MARKETS, non un campione, e fallisce con exit
code diverso da zero se anche una sola non risponde. Stampa cosa ha
controllato, cosi' si legge l'esito senza rileggere il codice.

    python3 test_amazon_markets.py          # tabella completa (rete)
    python3 test_amazon_markets.py --offline # solo i controlli senza rete
"""
import json, sys, urllib.parse, urllib.request, pathlib

# kdp_server importa anthropic, fastapi e httpx e pretende una API key: qui
# serve solo la tabella, quindi la si rilegge dal sorgente invece di importare
# il modulo. Cosi' il controllo gira anche dove quelle librerie non ci sono.
_sorgente = pathlib.Path(__file__).with_name("kdp_server.py")
try:
    src = _sorgente.read_text(encoding="utf-8")
    inizio = src.index("AMAZON_MARKETS = {")
    fine = src.index("def amazon_market(", inizio)
except (OSError, ValueError) as e:
    print(f"Non riesco a leggere la tabella dei marketplace da {_sorgente}: {e}\n"
          "Se AMAZON_MARKETS e' stata rinominata o spostata, va aggiornato anche "
          "questo controllo — altrimenti smette di sorvegliare senza dirlo.",
          file=sys.stderr)
    sys.exit(2)
ns: dict = {}
exec(src[inizio:fine], ns)
AMAZON_MARKETS = ns["AMAZON_MARKETS"]
LANGUAGE_TO_MARKET = ns["LANGUAGE_TO_MARKET"]
_MARKET_ALIASES = ns["_MARKET_ALIASES"]

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
PROBE = {"us": "anxiety", "uk": "anxiety", "it": "ansia",
         "de": "angst", "fr": "anxiete", "es": "ansiedad"}

failures: list[str] = []

# ── controlli senza rete ──────────────────────────────────────────────────
print("Struttura della tabella:")
for code, mk in AMAZON_MARKETS.items():
    missing = {"tld", "mid", "lop", "country", "accept_language"} - set(mk)
    if missing:
        failures.append(f"{code}: campi mancanti {missing}")
    print(f"  {code:>3}  amazon.{mk['tld']:<6} mid={mk['mid']:<15} lop={mk['lop']}")

mids = [m["mid"] for m in AMAZON_MARKETS.values()]
if len(set(mids)) != len(mids):
    failures.append("due marketplace condividono lo stesso mid")

print("\nOgni lingua mappata punta a un mercato che esiste:")
for lang, code in LANGUAGE_TO_MARKET.items():
    ok = code in AMAZON_MARKETS
    if not ok:
        failures.append(f"lingua {lang!r} -> mercato inesistente {code!r}")
    print(f"  {lang:<10} -> {code}  {'ok' if ok else 'ROTTO'}")

print("\nOgni alias punta a un mercato che esiste:")
for alias, code in _MARKET_ALIASES.items():
    ok = code in AMAZON_MARKETS
    if not ok:
        failures.append(f"alias {alias!r} -> mercato inesistente {code!r}")
    print(f"  {alias:<6} -> {code}  {'ok' if ok else 'ROTTO'}")

if "--offline" in sys.argv:
    print(f"\n{'FALLITO' if failures else 'OK'} — controlli offline "
          f"su {len(AMAZON_MARKETS)} mercati")
    for f in failures:
        print(f"  ! {f}")
    sys.exit(1 if failures else 0)

# ── controlli con rete: tutte le righe, nessun campione ───────────────────
def ask(host: str, mk: dict, prefix: str):
    q = urllib.parse.urlencode({
        "limit": 6, "prefix": prefix, "suggestion-type": "KEYWORD",
        "page-type": "Search", "alias": "stripbooks", "site-variant": "desktop",
        "version": "3", "event": "onKeyPress", "wc": "",
        "lop": mk["lop"], "mid": mk["mid"]})
    req = urllib.request.Request(f"https://{host}/api/2017/suggestions?{q}",
        headers={"User-Agent": UA, "Accept": "application/json",
                 "Accept-Language": mk["accept_language"]})
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read().decode()).get("suggestions", [])

print("\nRisposta reale di ogni marketplace (host proprio):")
for code, mk in AMAZON_MARKETS.items():
    try:
        sugg = ask(f"completion.amazon.{mk['tld']}", mk, PROBE[code])
    except Exception as e:
        failures.append(f"{code}: chiamata fallita — {e}")
        print(f"  {code:>3}  ERRORE {e}")
        continue
    if not sugg:
        failures.append(f"{code}: zero suggerimenti su completion.amazon.{mk['tld']}")
        print(f"  {code:>3}  ZERO — host o mid sbagliati")
    else:
        print(f"  {code:>3}  {len(sugg):2d} suggerimenti  es. {sugg[0].get('value')!r}")

# La regressione da cui nasce tutto: .com non deve rispondere per i non-US.
print("\nControprova — su completion.amazon.com i non-US devono dare zero\n"
      "(e' il bug che ha prodotto il falso 'nicchia senza domanda'):")
for code, mk in AMAZON_MARKETS.items():
    if code == "us":
        continue
    try:
        sugg = ask("completion.amazon.com", mk, PROBE[code])
    except Exception as e:
        print(f"  {code:>3}  chiamata fallita ({e}) — controprova saltata")
        continue
    print(f"  {code:>3}  {len(sugg)} suggerimenti su .com"
          f"{'  (come atteso: host proprio obbligatorio)' if not sugg else '  <-- .com ora risponde, la nota nel codice va aggiornata'}")

print(f"\n{'FALLITO' if failures else 'OK'} — {len(AMAZON_MARKETS)} mercati "
      f"controllati, {len(failures)} problemi")
for f in failures:
    print(f"  ! {f}")
sys.exit(1 if failures else 0)
