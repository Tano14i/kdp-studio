# Report nicchia — Martina Riva, volume 2
01 Ricerca · aggiornato il 06/09/2026

## Indice
1. Stato del passo
2. Il blocco
3. Opzioni per sbloccare
4. Nicchie candidate da misurare
5. Cosa va misurato, quando i dati arrivano

## 1. Stato del passo

**Non eseguito.** Nessun verdetto, nessun numero. Questo file esiste per
registrare perché.

## 2. Il blocco

`ricerca-nicchia` misura una nicchia su Amazon prima di scrivere una riga:
concorrenti reali, prezzi, valutazioni, curva di declino delle vendite,
domanda vera estratta dai suggerimenti di ricerca.

Da questa sessione remota `amazon.it` è irraggiungibile: la network policy
dell'environment blocca il dominio a livello di proxy (`EGRESS_BLOCKED`).
Verificato il 06/09/2026, insieme a `tiktok.com` e alla CDN di Blotato.

Senza quei dati il passo produrrebbe un verdetto basato su impressioni. La
regia ha una regola precisa in proposito: un verdetto senza numeri accanto
non è un verdetto, e il passo 1 non è finito.

Nel dossier del metodo vale anche la regola inversa: prima di credere a uno
zero, verificare di aver interrogato la cosa giusta. Qui lo zero è dello
strumento, non del mercato.

## 3. Opzioni per sbloccare

| # | Opzione | Costo | Cosa produce |
|---|---|---|---|
| A | Allargare la network policy dell'environment ad `amazon.it` | Una modifica nelle impostazioni | Ricerca completa e automatica, ripetibile |
| B | Eseguire la ricerca da una sessione locale, senza restrizione | Tempo dell'autore | Stessa qualità, non ripetibile da qui |
| C | L'autore incolla i dati grezzi (schede, recensioni, suggerimenti) | Lavoro manuale, molto | Verdetto possibile, copertura parziale |
| D | Lanciare la ricerca dal KDP Trend Hunter già deployato su Railway | Nessuno, esiste già | Ricerca completa, con i dati che tornano all'autore |

**L'opzione D è la più promettente, ed è stata verificata in parte.**
`kdp_server.py` non interroga Amazon in modo diretto: passa da **Apify**
(`APIFY_TOKEN`, `api.apify.com`), quindi il blocco su `amazon.it` non lo
riguarda. Il token sta nelle variabili d'ambiente di Railway, non qui, e da
questa sessione anche `api.apify.com` risulta bloccato: la ricerca quindi si
lancia dall'interfaccia del Trend Hunter, non da qui. I risultati poi si
incollano in questo file.

Da verificare, prima di contarci: che il deploy Railway sia ancora attivo e che
`APIFY_TOKEN` sia ancora valido. L'endpoint diagnostico nel server riporta
entrambe le cose.

## 4. Nicchie candidate da misurare
5. Cosa va misurato, quando i dati arrivano

Da `ricerca-nicchia`, per ogni nicchia candidata:

- concorrenti diretti con ASIN, e la tabella va conservata: la riusano
  l'avatar (per sapere quali recensioni leggere) e le campagne (per il
  targeting). Non si rifà due volte.
- prezzi e formati praticati
- valutazioni medie e numero di recensioni
- curva di declino: da quanto tempo vendono i primi in classifica
- domanda reale dai suggerimenti di ricerca, non dalle idee

Il verdetto è a tre valori: SI FA, DA VERIFICARE, NON SI FA.
