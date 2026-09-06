# Come raccogliere i dati con il KDP Trend Hunter
01 Ricerca · aggiornato il 06/09/2026

Traccia per l'autore. Serve a raccogliere, in un giro solo, tutto quello che
`ricerca-nicchia` deve misurare per emettere un verdetto.

## Indice
1. Prima di iniziare
2. Le due nicchie e le query
3. I pannelli, in ordine
4. Cosa riportare
5. Cosa serve dopo, per l'avatar

## 1. Prima di iniziare

**Metti il marketplace su Italia.** È il punto che fa fallire tutto il resto:
lato server il default è `us` (`kdp_server.py`, `marketplace = req.get(
"marketplace", "us")`). Con quel default misuri il mercato americano su nicchie
italiane, e i numeri che tornano sono coerenti fra loro ma inutili.

Poi due controlli veloci:

- `/health/full` — il deploy Railway risponde
- `/api/debug/env` — riporta `APIFY_TOKEN_loaded`. Se è falso, i dati reali
  (classifica, recensioni, prezzi) non arrivano e restano solo i suggerimenti
  di ricerca

Se il token non c'è, fermarsi qui e reintegrarlo nelle variabili Railway. Senza
quello il giro si fa a metà e va rifatto.

## 2. Le due nicchie e le query

Scelte dall'autore il 06/09/2026.

**Alta sensibilità**
`alta sensibilità` · `persone altamente sensibili` · `ipersensibilità` ·
`essere troppo sensibili`

**Dipendenza affettiva**
`dipendenza affettiva` · `relazioni tossiche` · `amore tossico` ·
`smettere di amare chi ti fa male`

Le varianti servono: la nicchia si misura su come la cerca il lettore, non su
come la chiama l'autore.

## 3. I pannelli, in ordine

| # | Pannello | Endpoint | Cosa produce |
|---|---|---|---|
| 1 | Niche Validator | `/api/niche-validator` | Domanda, densità di concorrenza, punteggi, go/no-go. Lanciarlo su ogni query |
| 2 | Suggerimenti keyword | `/api/apify/keywords`, piattaforma `amazon` | La domanda reale: cosa scrive davvero la gente nella barra di ricerca |
| 3 | ASIN Reverse | `/api/asin-reverse` | Un concorrente alla volta. Lanciarlo sui primi 5 di ogni nicchia |

Il pannello 3 è quello che dà i numeri che qui mancano del tutto. Vale la pena
farlo su cinque titoli per nicchia, non su uno.

## 4. Cosa riportare

Per ogni concorrente, una riga:

| ASIN | Titolo | Autore | Editore | Formato | Prezzo | Pagine | Uscita | Voto | N. recensioni | Posizione in classifica |
|---|---|---|---|---|---|---|---|---|---|---|

Le tre colonne che decidono il verdetto sono **uscita**, **numero di
recensioni** e **posizione**. Insieme dicono da quanto tempo vendono i primi e
quanto è alto il muro da scavalcare partendo da zero recensioni.

Serve anche, per ogni nicchia, l'elenco grezzo dei suggerimenti di ricerca. Va
bene incollato così com'è, senza pulirlo.

Una domanda da tenere a mente mentre si guardano i risultati: **fra i primi
dieci c'è almeno un indipendente?** Se sono tutti editori con distribuzione, la
nicchia è misurabile ma probabilmente non aggredibile da un pen name a zero
recensioni.

## 5. Cosa serve dopo, per l'avatar

Il passo 2 parte dalle recensioni vere dei concorrenti, non dalle schede.
Gli ASIN raccolti qui si riusano lì: il pannello avatar del Trend Hunter
(`/api/amazon-reviews`, marketplace `it`) le scarica, poi Review Mining le
analizza.

La tabella degli ASIN non si rifà: la usano l'avatar e, più avanti, il
targeting delle campagne.
