# Dati di prova

Servono ai controlli automatici, non alla ricerca. I libri non esistono: gli
ASIN cominciano tutti con `B0TEST`.

- `concorrenti-completi.csv` — copertura sufficiente su ogni campo:
  `analizza_concorrenti.py` deve uscire con **0** e produrre il verdetto.
- `concorrenti-scarsi.csv` — troppi `?`: deve uscire con **1** e rifiutarsi di
  concludere. E' il controllo che conta di piu': uno strumento che conclude
  comunque, su meta' dato, e' peggio di uno che non risponde.
