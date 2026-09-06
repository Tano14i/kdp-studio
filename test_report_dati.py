#!/usr/bin/env python3
"""I numeri scritti nei report del passo 1b devono essere quelli dei dati.

`regia` §10: una specifica scritta a mano e un artefatto prodotto da uno
script divergono sempre, e in silenzio. I report `01b-angolo.md` citano voti e
numeri di recensioni che vengono da `dati-angolo.json`, generato da
`sonda_angolo.py`. Basta una rigenerazione — o una riga corretta a mano — e le
due cose smettono di concordare senza che nessuno se ne accorga.

Questo controllo copre TUTTE le righe di quelle tabelle, non un campione
(`regia` §11), esce con codice diverso da zero al primo disaccordo, e stampa
cosa ha controllato.

Niente rete: legge solo file del repo.

    python3 test_report_dati.py
"""
import json, pathlib, re, sys

RADICE = pathlib.Path(__file__).resolve().parent
# Riga di tabella markdown con un numero di recensioni in fondo:
#   | Wiest, *La montagna sei tu* | 4,4 | **1.204** |
# Riga di tabella markdown che cita un ASIN e un numero di recensioni:
#   | `8845410048` | Wiest, *La montagna sei tu* | 4,4 | **1204** |
# L'ASIN e' obbligatorio, e non e' pedanteria: accostare report e dati per
# somiglianza di titolo vuol dire indovinare, e due libri che contengono
# entrambi la parola «vittima» mandano l'accostamento sul libro sbagliato
# senza dirlo. Un controllo che indovina non e' un controllo.
# L'ASIN e' un ISBN-10 (i libri con editore) oppure un codice B0... (tutto il
# resto, compreso ogni titolo autopubblicato). Accettarne uno solo dei due
# lascerebbe fuori dal controllo meta' delle tabelle.
RIGA = re.compile(r"^\|\s*`(?P<asin>[0-9]{9}[0-9X]|B0[A-Z0-9]{8})`\s*\|(?P<titolo>[^|]+)\|"
                  r"(?P<voto>[^|]*)\|(?P<recensioni>[^|]*)\|\s*$")


def numero(cella: str):
    """Il numero dentro una cella markdown, senza grassetti e separatori."""
    pulita = cella.replace("*", "").replace(".", "").replace(" ", " ").strip()
    return int(pulita) if pulita.isdigit() else None


def schede_accanto(report: pathlib.Path) -> dict:
    """Tutte le schede lette dai file di dati che stanno nella stessa cartella.

    Un report puo' poggiare su piu' di un file generato — `dati-angolo.json`
    per i concorrenti del passo 1, `dati-scaffale-*.json` per la verifica
    dell'angolo. Cercarne uno solo per nome fisso lascerebbe le altre tabelle
    fuori dal controllo senza dirlo.
    """
    per_asin = {}
    for f in sorted(report.parent.glob("dati-*.json")):
        try:
            contenuto = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        # nella stessa cartella vivono anche i dati della domanda, che sono
        # liste: si ignorano invece di far esplodere il controllo.
        if not isinstance(contenuto, dict):
            continue
        schede = contenuto.get("schede", [])
        for s in schede:
            if s.get("recensioni"):
                per_asin[s["asin"]] = s
    return per_asin


def controlla(report: pathlib.Path) -> list[str]:
    per_asin = schede_accanto(report)
    guasti, controllate = [], 0
    for n, riga in enumerate(report.read_text(encoding="utf-8").splitlines(), 1):
        m = RIGA.match(riga)
        if not m:
            continue
        atteso = numero(m.group("recensioni"))
        if atteso is None:
            continue
        titolo = m.group("titolo").strip()
        asin = m.group("asin")
        scheda = per_asin.get(asin)
        if scheda is None:
            guasti.append(f"{report}:{n} — «{titolo}» cita {atteso} recensioni per "
                          f"l'ASIN {asin}, che nessun dati-*.json accanto ha letto")
            continue
        reale = int(scheda["recensioni"])
        controllate += 1
        if reale != atteso:
            guasti.append(f"{report}:{n} — «{titolo}» dice {atteso} recensioni, "
                          f"dati-angolo.json ne ha {reale} (ASIN {scheda['asin']})")
        print(f"  ok  {asin}  {atteso} recensioni  {titolo}")
    if not controllate:
        guasti.append(f"{report} — nessuna riga con ASIN e numero di recensioni: "
                      f"o la tabella e' sparita, o il formato e' cambiato e "
                      f"questo controllo non sta piu' controllando niente")
    return guasti


def controlla_trasversale(file: pathlib.Path, tutte: dict) -> list[str]:
    """Come `controlla`, ma per un file che cita libri di piu' progetti.

    `note-mercato.md` §3-bis mette in fila i numeri di entrambe le nicchie: se
    fosse controllato solo per progetto, quella tabella resterebbe l'unica a
    poter divergere in silenzio — cioe' esattamente il punto cieco che questo
    controllo esiste per chiudere.
    """
    guasti, controllate = [], 0
    for n, riga in enumerate(file.read_text(encoding="utf-8").splitlines(), 1):
        m = RIGA.match(riga)
        if not m:
            continue
        atteso = numero(m.group("recensioni"))
        if atteso is None:
            continue
        asin, titolo = m.group("asin"), m.group("titolo").strip()
        if asin not in tutte:
            guasti.append(f"{file}:{n} — «{titolo}» cita l'ASIN {asin}, che nessun "
                          f"dati-angolo.json ha letto")
            continue
        reale = int(tutte[asin]["recensioni"])
        controllate += 1
        if reale != atteso:
            guasti.append(f"{file}:{n} — «{titolo}» dice {atteso} recensioni, i dati "
                          f"ne hanno {reale} (ASIN {asin})")
        print(f"  ok  {asin}  {atteso} recensioni  {titolo}")
    if not controllate:
        guasti.append(f"{file} — nessuna riga con ASIN e recensioni: o la tabella e' "
                      f"sparita, o il formato e' cambiato e questo controllo non sta "
                      f"piu' controllando niente")
    return guasti


def main() -> int:
    report = sorted(list(RADICE.glob("progetti/*/01 Ricerca/01b-angolo.md"))
                    + list(RADICE.glob("progetti/*/01 Ricerca/scaffale-*.md")))
    if not report:
        print("Nessun 01b-angolo.md: niente da controllare.")
        return 0

    guasti = []
    tutte = {}
    for r in report:
        print(f"\n{r.relative_to(RADICE)}")
        guasti += controlla(r)
        tutte.update(schede_accanto(r))

    trasversali = [RADICE / "_profili" / "note-mercato.md"]
    for f in trasversali:
        if f.exists():
            print(f"\n{f.relative_to(RADICE)}")
            guasti += controlla_trasversale(f, tutte)

    print(f"\n{len(report) + len(trasversali)} file controllati, riga per riga.")
    if guasti:
        print("\nGUASTI — il report e i dati non concordano. Ha ragione il file "
              "dei dati:\n")
        for g in guasti:
            print(f"  {g}")
        return 1
    print("Report e dati concordano.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
