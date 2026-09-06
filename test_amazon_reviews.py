#!/usr/bin/env python3
"""L'endpoint delle recensioni non deve mai rispondere 500.

    python3 test_amazon_reviews.py

Nato da un guasto reale del 06/09: rimuovendo un actor e' sparita per
sbaglio la definizione di un altro, py_compile non vede i NameError, e in
produzione ogni chiamata rispondeva 500 in testo semplice. Nessun test
esercitava fetch_for_asin. Ora si': gli actor sono sostituiti da funzioni
finte (nessuna rete, nessuna chiave) e si verifica che, qualunque cosa
facciano, la risposta sia o un 200 con i dati o un 404 che dice cosa e'
successo a ogni actor — mai un'eccezione non gestita.
"""
import asyncio, importlib.util, os, pathlib, sys
os.environ.setdefault("ANTHROPIC_API_KEY", "non-usata")
os.environ.setdefault("KDP_API_KEY", "non-usata")
_spec = importlib.util.spec_from_file_location("srv", pathlib.Path(__file__).with_name("kdp_server.py"))
srv = importlib.util.module_from_spec(_spec); sys.modules["srv"] = srv; _spec.loader.exec_module(srv)
from fastapi import HTTPException

rotti = []
def verifica(c, d):
    print(f"  {'ok  ' if c else 'ROTTO'} {d}")
    if not c: rotti.append(d)

RECENSIONI = [{"asin": "B01TEST000", "rating": 2, "title": "Deludente", "text": "Superficiale e ripetitivo.",
               "date": "2025-03-01", "verified": True},
              {"asin": "B01TEST000", "rating": 5, "title": "Ottimo", "text": "Chiaro e utile.",
               "date": "2025-02-01", "verified": True}]

async def prove():
    srv.APIFY_TOKEN = "finto"
    chiamate = []

    print("\n1. Tutti gli actor falliscono (es. non noleggiati): 404 parlante, non 500")
    async def tutti_falliscono(actor, inp, timeout_sec=120):
        chiamate.append(actor); raise RuntimeError("HTTP 403 actor-is-not-rented")
    srv.run_actor = tutti_falliscono
    for filtro in ("", "critical"):
        chiamate.clear()
        try:
            await srv.fetch_amazon_reviews({"asins": ["B01TEST000"], "marketplace": "it", "filtro_stelle": filtro})
            verifica(False, f"filtro={filtro!r}: doveva alzare HTTPException")
        except HTTPException as e:
            verifica(e.status_code == 404, f"filtro={filtro!r}: e' un 404, non un'eccezione libera")
            det = e.detail if isinstance(e.detail, dict) else {}
            verifica(bool(det.get("tentativi")), f"filtro={filtro!r}: il 404 elenca i tentativi")
            verifica(all("actor-is-not-rented" in t["esito"] for t in det.get("tentativi", [])),
                     f"filtro={filtro!r}: l'esito riporta l'errore vero dell'actor")
        except Exception as e:
            verifica(False, f"filtro={filtro!r}: eccezione non gestita {type(e).__name__}: {e}")
        verifica(len(chiamate) >= 2, f"filtro={filtro!r}: ha provato piu' di un actor ({len(chiamate)})")
    ordine_con_filtro = chiamate[0]
    verifica("neatrat" in ordine_con_filtro, "con filtro il primo actor e' quello che dichiara di filtrare")

    print("\n2. Il primo actor risponde: 200 con voti, date e tentativi")
    async def primo_risponde(actor, inp, timeout_sec=120):
        return RECENSIONI
    srv.run_actor = primo_risponde
    r = await srv.fetch_amazon_reviews({"asins": ["B01TEST000"], "marketplace": "it"})
    verifica(r["count"] == 2, "due recensioni")
    verifica(r["voti"]["negative_1_3"] == 1 and r["voti"]["positive_4_5"] == 1, "i voti sono contati")
    verifica(r["date_note"] == 2, "le date sopravvivono")
    verifica("tentativi" in r, "anche il 200 dice cosa ha fatto ogni actor")

    print("\n3. Filtro chiesto ma tornano solo positive: l'avviso scatta")
    async def solo_positive(actor, inp, timeout_sec=120):
        return [RECENSIONI[1]] * 3
    srv.run_actor = solo_positive
    r = await srv.fetch_amazon_reviews({"asins": ["B01TEST000"], "marketplace": "it", "filtro_stelle": "critical"})
    verifica(bool(r.get("avviso")), "avviso presente quando il filtro non ha morso")

    print("\n4. Filtro non ammesso: 400, non silenzio")
    try:
        await srv.fetch_amazon_reviews({"asins": ["B01TEST000"], "marketplace": "it", "filtro_stelle": "boh"})
        verifica(False, "doveva rifiutare")
    except HTTPException as e:
        verifica(e.status_code == 400, "filtro non valido -> 400")

asyncio.run(prove())
print(f"\n{'FALLITO' if rotti else 'OK'} — {len(rotti)} controlli rotti")
sys.exit(1 if rotti else 0)
