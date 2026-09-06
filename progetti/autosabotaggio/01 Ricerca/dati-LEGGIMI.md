# Dati grezzi — 01 Ricerca
Fase 1 · aggiornato il 06/09/2026

## Indice
1. Cosa sono questi file
2. Come si rigenerano

## 1. Cosa sono questi file

**File generati. Non si modificano a mano.** Sono l'istantanea di cosa
suggeriva Amazon.it il 06/09/2026; se qualcuno li corregge a mano, il report
e i dati smettono di concordare e il report ha torto senza che nessuno lo veda.

| File | Cosa contiene |
|---|---|
| `dati-domanda-amazon-it.json` | 89 query di intento, mappa generale del mercato |
| `dati-nicchia-autosabotaggio.json` | 11 query, approfondimento sulla nicchia scelta |
| `dati-angolo.json` | passo 1b: lingua dell'angolo a scala di prefissi, piu' i numeri delle schede dei concorrenti gia' noti |
| `frasi-angolo.txt` | l'ingresso di `dati-angolo.json`: le frasi sondate. Questo si modifica a mano — e' la domanda, non la risposta |

## 2. Come si rigenerano

Dalla radice del repo:

```
python3 harvest_demand.py --market it --out domanda-it.json
python3 sonda_angolo.py --frasi <frasi.txt> --asin <lista> --out dati-angolo.json
```

`sonda_angolo.py` **fonde invece di sovrascrivere**: una scheda letta ieri non
si perde perche' oggi Amazon ha bloccato il tentativo, e la riga porta la data
della lettura. Serve perche' la scheda passa circa una volta su quattro: senza
la fusione, ogni rigenerazione cancellerebbe a caso qualche misura vera.

Se il totale torna zero non e' il mercato vuoto, e' lo strumento puntato male.
`python3 test_amazon_markets.py` lo dice in trenta secondi ed esce con codice
diverso da zero al primo mercato che non risponde.
