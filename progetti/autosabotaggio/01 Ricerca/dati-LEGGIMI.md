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

## 2. Come si rigenerano

Dalla radice del repo:

```
python3 harvest_demand.py --market it --out domanda-it.json
```

Se il totale torna zero non e' il mercato vuoto, e' lo strumento puntato male.
`python3 test_amazon_markets.py` lo dice in trenta secondi ed esce con codice
diverso da zero al primo mercato che non risponde.
