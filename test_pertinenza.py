#!/usr/bin/env python3
"""Il filtro di pertinenza, provato sui titoli veri restituiti da Amazon.it.

    python3 test_pertinenza.py

Su Amazon.it l'alias `stripbooks` non filtra bene: una ricerca per
"endometriosi" restituisce anche romanzi rosa e manuali di pilates. Senza
filtro, la mediana dei prezzi della nicchia la decidono i libri sbagliati.

I titoli qui sotto non sono inventati: sono quelli che il servizio ha
restituito davvero il 06/09/2026 per la ricerca "endometriosi" su amazon.it.
"""
import importlib.util, os, pathlib, sys

os.environ.setdefault("ANTHROPIC_API_KEY", "non-usata-in-questo-test")
os.environ.setdefault("KDP_API_KEY", "non-usata-in-questo-test")
_spec = importlib.util.spec_from_file_location(
    "srv", pathlib.Path(__file__).with_name("kdp_server.py"))
srv = importlib.util.module_from_spec(_spec)
sys.modules["srv"] = srv
_spec.loader.exec_module(srv)

# (nicchia, titolo, atteso pertinente)
CASI = [
    # I dieci risultati reali per "endometriosi" — tre pertinenti, sette no
    ("endometriosi", "A Taste of Vanilla: An age gap, boss x employee romance", False),
    ("endometriosi", "Dalle crepe del dolore, la luce di tre miracoli", False),
    ("endometriosi", "MISS POSITIVE La tua cerca rimedi in cucina", False),
    ("endometriosi", "FIBROMIALGIA E DIETA ANTINFIAMMATORIA", False),
    ("endometriosi", "Il capitale umano della vulvodinia", False),
    ("endometriosi", "Botanica della meraviglia. Coltivare lo stupore", False),
    ("endometriosi", "La dieta anti endometriosi. L'alimentazione antinfiammatoria", True),
    ("endometriosi", "Endometriosi: Un nuovo inizio", True),
    ("endometriosi", "Pilates al Muro: Rinasci in 10 Minuti al Giorno", False),
    ("endometriosi", "Endometriosi. Microbiota e alimentazione", True),
    # Morfologia italiana: il confronto e' per prefisso
    ("endometriosi", "Convivere con l'endometriosica cronica", True),
    # Accenti e punteggiatura non devono ingannare
    ("perche", "Il perché delle cose", True),
    # Nicchie a piu' parole: servono TUTTE, non una qualsiasi
    ("adhd adulti", "ADHD negli Adulti: Tecniche ed Esercizi Pratici", True),
    ("adhd adulti", "Ricette per bambini adulti e golosi", False),
    ("gioco azzardo", "SCONFIGGI LA LUDOPATIA: uscire dal gioco d'azzardo", True),
    ("gioco azzardo", "Il gioco delle perle di vetro", False),
    ("gioco azzardo", "L'azzardo di vivere", False),
]

fallimenti = []
print(f"{'esito':<7} {'nicchia':<16} titolo")
for nicchia, titolo, atteso in CASI:
    token = srv._token_nicchia(nicchia)
    ottenuto, _ = srv._pertinenza({"title": titolo, "url": ""}, token)
    ok = ottenuto == atteso
    if not ok:
        fallimenti.append(f"[{nicchia}] {titolo}: atteso {atteso}, ottenuto {ottenuto}")
    print(f"{'ok' if ok else 'ROTTO':<7} {nicchia:<16} {titolo[:56]}")

# Senza token utilizzabili non si filtra: meglio niente filtro che uno a caso
vuoto, _ = srv._pertinenza({"title": "Qualunque cosa"}, srv._token_nicchia("di per"))
if not vuoto:
    fallimenti.append("senza token utilizzabili il filtro deve lasciar passare tutto")
print(f"{'ok' if vuoto else 'ROTTO':<7} {'(nicchia vuota)':<16} nessun token -> non si filtra")

print(f"\n{'FALLITO' if fallimenti else 'OK'} — {len(CASI) + 1} casi, {len(fallimenti)} rotti")
for f in fallimenti:
    print(f"  ! {f}")
sys.exit(1 if fallimenti else 0)
