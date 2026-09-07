# Cancello d'ingresso di promozione-social — cosa c'e' e cosa manca
04 Mercato · aggiornato il 07/09/2026

`promozione-social` non genera un solo contenuto prima di avere questi sette
dati. Tre ci sono, quattro no. **Il lavoro e' fermo qui.**

## Indice
1. Quello che c'e'
2. Quello che manca
3. Gli interruttori da fissare

## 1. Quello che c'e'

### 1 · ASIN e link *(senza questo ci si ferma, e c'e')*

| Edizione | ASIN / ISBN | Prezzo netto | Royalty a copia |
|---|---|---:|---:|
| **Cartaceo** | B0H5W5BD5X · ISBN 9798182122399 | 14,41 EUR | **6,60 EUR** |
| Kindle | B0H62CB67K | 2,45 EUR | 1,69 EUR |

Destinazione di ogni CTA: **l'edizione cartacea**, che rende quasi quattro
volte l'ebook e vende il doppio. Il link e' verificato il 07/09/2026 — la
scheda risponde e l'URL canonico che Amazon dichiara e':

```
https://www.amazon.it/Diventa-Master-Campagna-manuale-avresti/dp/B0H5W5BD5X
```

### 2 · Titolo e sottotitolo esatti

> **Diventa Master - La Tua Prima Campagna**
> *Il manuale che avresti voluto prima di sederti al tavolo*

Il sottotitolo e' gia' un hook: nomina il momento (il primo tavolo) e il
rimpianto (avresti voluto). Non va riscritto, va usato.

### 7 · Stato di vendita — si promuove, non si ripubblica

21 copie in tre mesi (14 cartacee, 7 Kindle), 104,23 EUR, **senza nessuna
promozione**. Il 58% del fatturato del pen name. Non e' un libro da rilanciare:
e' un libro che sta gia' salendo e che nessuno ha mai spinto.

## 2. Quello che manca

| # | Dato | Dove si prende |
|---|---|---|
| 3 | Descrizione della scheda | pagina Amazon del libro, testo intero |
| 4 | Indice dei capitoli | dal manoscritto o dall'anteprima Amazon |
| 5 | Copertina, immagine | file originale, o dalla scheda |
| 6 | Recensioni ricevute, testo intero | scheda Amazon.it — **forse zero** |

**Tentato il 07/09/2026, non riuscito.** La scheda risponde e conferma titolo e
ASIN, ma Amazon serve agli agenti solo l'intestazione della pagina: descrizione,
recensioni, indice e classifica non arrivano. Non e' un problema di URL
sbagliato e non si risolve riprovando — questi quattro dati vanno presi a mano
dall'autore, o con lo strumento di raccolta che il repo usa per i concorrenti.

Sul **6**: 21 copie vendute rendono probabile che le recensioni siano zero o
una. Se e' cosi' si procede lo stesso, ma gli hook vanno ricavati dall'indice e
dalle recensioni **dei concorrenti**, e va scritto qui che sono di seconda
mano. Le recensioni dei concorrenti in questa nicchia non sono mai state
raccolte: `01 Ricerca/` e' vuota.

Il **4** e' il piu' importante dei quattro: ogni capitolo e' un filone di
contenuti per trenta giorni. Senza indice non c'e' calendario.

## 3. Gli interruttori da fissare

Decidono quali format sono ammessi, e vanno fissati **prima** di generare, non
dopo. Per il pen name Martina Riva erano `volto = no`, `voce = nessuna`, e
quella configurazione ha escluso un intero format.

| Interruttore | Valori | Per Cedric Darkstone |
|---|---|---|
| volto | si / no | **da decidere** |
| voce | mia / sintetica / nessuna | **da decidere** |

C'e' una quarta decisione che riguarda solo questo pen name e che il metodo
non prevede: **il profilo social parla di questo libro o del catalogo?**
Cedric Darkstone ha quattro titoli, due in inglese e due in italiano. Un
profilo italiano costruito su *Diventa Master* lascia fuori meta' catalogo;
uno costruito su tutti e quattro parla in due lingue a due pubblici diversi e
non ne convince nessuno. Va sciolta al checkpoint 7.
