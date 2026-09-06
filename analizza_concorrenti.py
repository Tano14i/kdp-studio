#!/usr/bin/env python3
"""Trasforma la raccolta manuale dei concorrenti nei numeri della fase 1.

    python3 analizza_concorrenti.py "progetti/<nicchia>/01 Ricerca/concorrenti.csv"

Formato atteso (punto e virgola, una riga per libro, intestazione facoltativa):

    asin;titolo;autore;prezzo_cartaceo;prezzo_kindle;n_recensioni;stelle;bsr;data_pubblicazione;pagine

Un campo non trovato si scrive `?`. Il `?` viene contato come mancante e
dichiarato; NON viene sostituito con una stima. Un numero inventato produce un
verdetto sbagliato che sembra fondato, ed e' il modo peggiore di sbagliare.

Lo script rifiuta di concludere se manca troppo: meglio dire "non lo so" che
dare una fascia di prezzo costruita su tre libri su dieci.
"""
import csv, math, statistics, sys
from datetime import date

CAMPI = ["asin", "titolo", "autore", "prezzo_cartaceo", "prezzo_kindle",
         "n_recensioni", "stelle", "bsr", "data_pubblicazione", "pagine"]
OGGI = date(2026, 9, 6)
COPERTURA_MINIMA = 0.5      # sotto meta' dei valori presenti non si conclude


def num(v):
    """'12,90' e '12.90' -> 12.9 · '?' e vuoto -> None · '1.234' -> 1234."""
    if v is None:
        return None
    v = v.strip().replace("€", "").replace(" ", " ").strip()
    if v in ("", "?", "-", "n/d", "na"):
        return None
    v = v.replace(".", "") if v.count(".") > 1 or (v.count(".") == 1 and len(v.split(".")[-1]) == 3) else v
    v = v.replace(",", ".")
    try:
        return float(v)
    except ValueError:
        return None


def anno_mese(v):
    """Accetta 2021, 03/2021, 2021-03, marzo 2021 -> (anno, mese) o None."""
    if not v or v.strip() in ("?", "", "-"):
        return None
    s = v.strip().lower()
    MESI = {m: i + 1 for i, m in enumerate(
        "gennaio febbraio marzo aprile maggio giugno luglio agosto "
        "settembre ottobre novembre dicembre".split())}
    for nome, n in MESI.items():
        if nome in s:
            for tok in s.replace(",", " ").split():
                if tok.isdigit() and len(tok) == 4:
                    return int(tok), n
    cifre = [t for t in s.replace("/", " ").replace("-", " ").split() if t.isdigit()]
    anni = [int(t) for t in cifre if len(t) == 4]
    mesi = [int(t) for t in cifre if len(t) <= 2 and 1 <= int(t) <= 12]
    if anni:
        return anni[0], (mesi[0] if mesi else 6)
    return None


def mesi_da(am):
    a, m = am
    return max(1, (OGGI.year - a) * 12 + (OGGI.month - m))


def fascia(valori, etichetta, unita="€"):
    if not valori:
        return f"  {etichetta}: nessun dato"
    v = sorted(valori)
    mediana = statistics.median(v)
    return (f"  {etichetta}: da {v[0]:.2f}{unita} a {v[-1]:.2f}{unita}"
            f" · mediana {mediana:.2f}{unita} · su {len(v)} libri")


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    percorso = sys.argv[1]
    try:
        testo = open(percorso, encoding="utf-8").read()
    except OSError as e:
        print(f"Non riesco a leggere {percorso}: {e}", file=sys.stderr)
        return 2

    righe = []
    for r in csv.reader([l for l in testo.splitlines() if l.strip()], delimiter=";"):
        if r and r[0].strip().lower() == "asin":
            continue                       # intestazione
        r = (r + [""] * len(CAMPI))[:len(CAMPI)]
        righe.append(dict(zip(CAMPI, [c.strip() for c in r])))
    if not righe:
        print("Nessuna riga leggibile.", file=sys.stderr)
        return 2

    n = len(righe)
    print(f"\n=== {n} concorrenti — {percorso} ===\n")

    # copertura, dichiarata prima di qualunque conclusione
    print("Copertura dei dati (quanto e' stato davvero trovato):")
    copertura = {}
    for c in ["prezzo_cartaceo", "prezzo_kindle", "n_recensioni", "stelle",
              "bsr", "data_pubblicazione"]:
        presenti = sum(1 for r in righe if num(r[c]) is not None
                       or (c == "data_pubblicazione" and anno_mese(r[c])))
        copertura[c] = presenti / n
        stato = "ok" if copertura[c] >= COPERTURA_MINIMA else "INSUFFICIENTE"
        print(f"  {c:<20} {presenti:2d}/{n}  {copertura[c]*100:5.0f}%  {stato}")

    print("\nPrezzi:")
    print(fascia([num(r["prezzo_cartaceo"]) for r in righe if num(r["prezzo_cartaceo"])], "cartaceo"))
    print(fascia([num(r["prezzo_kindle"]) for r in righe if num(r["prezzo_kindle"])], "kindle"))

    rec = [num(r["n_recensioni"]) for r in righe if num(r["n_recensioni"]) is not None]
    if rec:
        rec_s = sorted(rec, reverse=True)
        print(f"\nRecensioni: totale {int(sum(rec))} · mediana {statistics.median(rec):.0f}"
              f" · massimo {int(rec_s[0])}")
        sotto50 = sum(1 for x in rec if x < 50)
        print(f"  libri sotto le 50 recensioni: {sotto50}/{len(rec)}")
        if rec_s[0] > 0 and len(rec_s) >= 4:
            quota = sum(rec_s[:3]) / sum(rec_s)
            print(f"  i primi 3 titoli tengono il {quota*100:.0f}% delle recensioni totali")
            print("  -> concentrata: pochi titoli dominano, gli altri raccolgono briciole"
                  if quota > 0.7 else
                  "  -> distribuita: nessun titolo domina, si entra piu' facilmente")
        elif rec_s[0] > 0:
            print(f"  (concentrazione non calcolata: servono almeno 4 libri, ce ne sono {len(rec_s)})")

    # curva: recensioni al mese dalla pubblicazione
    print("\nRitmo di raccolta recensioni (recensioni al mese dalla pubblicazione):")
    curva = []
    for r in righe:
        am, nr = anno_mese(r["data_pubblicazione"]), num(r["n_recensioni"])
        if am and nr is not None:
            curva.append((nr / mesi_da(am), r["titolo"][:44] or r["asin"], nr, mesi_da(am)))
    if not curva:
        print("  nessun dato: servono data di pubblicazione e numero recensioni")
    else:
        for v, t, nr, m in sorted(curva, reverse=True):
            print(f"  {v:6.2f}/mese  {t:<46} ({int(nr)} rec. in {m} mesi)")
        print(f"  mediana: {statistics.median([c[0] for c in curva]):.2f} recensioni/mese")

    # quanti sono entrati di recente
    date_ok = [d for d in (anno_mese(r["data_pubblicazione"]) for r in righe) if d]
    if date_ok:
        recenti = sum(1 for d in date_ok if mesi_da(d) <= 12)
        due_anni = sum(1 for d in date_ok if mesi_da(d) <= 24)
        print(f"\nEta' dei titoli: {recenti}/{len(date_ok)} pubblicati negli ultimi 12 mesi, "
              f"{due_anni}/{len(date_ok)} negli ultimi 24")
        # L'interpretazione esce solo se le date coprono almeno meta' dei libri:
        # dire "nessun ingresso recente" avendo la data di uno su tre e' una
        # conclusione sul campione, non sulla nicchia.
        if copertura["data_pubblicazione"] < COPERTURA_MINIMA:
            print(f"  (nessuna lettura: date note solo per {len(date_ok)}/{n} libri)")
        elif recenti / len(date_ok) > 0.4:
            print("  -> la nicchia si sta riempiendo ADESSO: molti sono entrati da poco")
        elif recenti == 0:
            print("  -> nessun ingresso recente: o e' stabile, o non interessa piu' a nessuno")

    bsr = [num(r["bsr"]) for r in righe if num(r["bsr"]) is not None]
    if bsr:
        b = sorted(bsr)
        print(f"\nBSR: migliore {int(b[0]):,} · mediana {int(statistics.median(b)):,}"
              f" · peggiore {int(b[-1]):,}".replace(",", "."))
        print(f"  libri sotto 100.000 (vendono ogni giorno): {sum(1 for x in b if x < 100000)}/{len(b)}")

    # verdetto solo se i dati bastano
    print("\n--- Cosa si puo' concludere ---")
    scarsi = [c for c, v in copertura.items() if v < COPERTURA_MINIMA]
    if scarsi:
        print(f"NON ABBASTANZA per un verdetto: sotto la meta' dei valori su {', '.join(scarsi)}.")
        print("Meglio tornare a raccogliere quei campi che concludere su meta' dato.")
        return 1
    print("Copertura sufficiente su tutti i campi: i numeri qui sopra reggono un verdetto.")
    print("Restano da leggere le recensioni negative — i numeri dicono se la nicchia e'")
    print("affollata, le recensioni se e' affollata di libri buoni.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
