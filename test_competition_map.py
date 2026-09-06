#!/usr/bin/env python3
"""Verifica che i numeri misurati sopravvivano a tutto il resto.

    python3 test_competition_map.py

/api/competition-map fa due cose molto diverse: MISURA (Apify: titolo,
recensioni, BSR, prezzo) e poi INTERPRETA (Claude). Sono state a lungo
accoppiate, con due conseguenze:

- se l'interpretazione falliva, la misura — gia' pagata ad Apify — spariva
  dentro un 500;
- anche quando riusciva, la risposta conteneva solo la riscrittura del
  modello (`reviews_est`, `price_est`) e non i numeri misurati. Il prezzo
  rilevato non veniva nemmeno passato al modello.

Questi controlli tengono separate le due cose. Non toccano la rete: Apify e
Claude sono sostituiti da funzioni finte, perche' cio' che si verifica e' la
logica di questo codice, non il comportamento di due servizi esterni.
"""
import asyncio, importlib.util, os, pathlib, sys

os.environ.setdefault("ANTHROPIC_API_KEY", "non-usata-in-questo-test")
os.environ.setdefault("KDP_API_KEY", "non-usata-in-questo-test")

_spec = importlib.util.spec_from_file_location(
    "srv", pathlib.Path(__file__).with_name("kdp_server.py"))
srv = importlib.util.module_from_spec(_spec)
sys.modules["srv"] = srv
_spec.loader.exec_module(srv)

LIBRI_APIFY = [
    {"title": "La dieta anti endometriosi", "reviewsCount": 412,
     "bestsellersRank": [{"rank": 24300}], "price": "16,90 €"},
    {"title": "Endometriosi ed alimentazione", "reviewsCount": 87,
     "bestsellersRank": [{"rank": 95200}], "price": "18,00 €"},
]

fallimenti: list[str] = []


def verifica(condizione, descrizione):
    print(f"  {'ok  ' if condizione else 'ROTTO'} {descrizione}")
    if not condizione:
        fallimenti.append(descrizione)


async def apify_riesce(actor, payload, timeout_sec=120):
    return LIBRI_APIFY


async def apify_fallisce(actor, payload, timeout_sec=120):
    raise RuntimeError("actor non raggiungibile")


async def prove():
    srv.APIFY_TOKEN = "finto-ma-presente"

    print("\n1. Apify riesce, Claude non ha credito — il caso reale del 06/09")
    srv.run_actor = apify_riesce

    async def claude_senza_credito(prompt, max_tokens=4000, allow_truncated=False):
        raise RuntimeError("Error code: 400 - credit balance is too low")
    srv.call_claude = claude_senza_credito

    r = await srv.competition_map({"niche": "endometriosi", "marketplace": "it"})
    verifica(r.get("measured") is True, "i dati misurati restano dichiarati misurati")
    verifica(len(r.get("measured_books", [])) == 2, "i due libri misurati escono comunque")
    verifica("analysis_error" in r, "il fallimento del modello viene dichiarato, non nascosto")
    verifica(r["measured_books"][0]["bsr"] == 24300, "il BSR misurato arriva intero")
    verifica(r["measured_books"][0]["price"] == "16,90 €", "il prezzo misurato arriva intero")

    print("\n2. raw:true — i numeri senza il modello")
    chiamato = {"si": False}

    async def spia(prompt, max_tokens=4000, allow_truncated=False):
        chiamato["si"] = True
        return "{}"
    srv.call_claude = spia
    r = await srv.competition_map({"niche": "endometriosi", "marketplace": "it", "raw": True})
    verifica(chiamato["si"] is False, "con raw il modello non viene chiamato affatto")
    verifica(len(r["measured_books"]) == 2, "i libri misurati ci sono lo stesso")
    verifica("books" not in r, "nessun campo di analisi in modalita' raw")

    print("\n3. Apify fallisce — non si chiede al modello di inventare")
    srv.run_actor = apify_fallisce
    chiamato["si"] = False
    r = await srv.competition_map({"niche": "endometriosi", "marketplace": "it"})
    verifica(chiamato["si"] is False, "senza misure il modello non viene interrogato")
    verifica(r.get("measured") is False, "la risposta dichiara di non avere misure")
    verifica(bool(r.get("apify_error")), "il motivo del vuoto e' scritto nella risposta")
    verifica(r.get("books") == [], "nessun libro inventato riempie il campo dei libri")

    print("\n4. Apify riesce e Claude risponde — misure e analisi convivono")
    srv.run_actor = apify_riesce

    async def claude_ok(prompt, max_tokens=4000, allow_truncated=False):
        verifica("16,90" in prompt, "il prezzo misurato viene passato al modello")
        verifica("24300" in prompt, "il BSR misurato viene passato al modello")
        return '{"books": [{"title": "La dieta anti endometriosi"}], "collective_gap": "x"}'
    srv.call_claude = claude_ok
    r = await srv.competition_map({"niche": "endometriosi", "marketplace": "it"})
    verifica(r.get("collective_gap") == "x", "l'analisi arriva")
    verifica(len(r.get("measured_books", [])) == 2,
             "le misure arrivano ACCANTO all'analisi, non al posto suo")
    verifica(r.get("measured") is True, "la risposta distingue misurato da stimato")


asyncio.run(prove())
print(f"\n{'FALLITO' if fallimenti else 'OK'} — {len(fallimenti)} controlli rotti")
for f in fallimenti:
    print(f"  ! {f}")
sys.exit(1 if fallimenti else 0)
