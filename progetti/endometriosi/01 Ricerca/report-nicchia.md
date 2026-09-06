# Report di nicchia — endometriosi
Fase 1 · Amazon.it, italiano · aggiornato il 06/09/2026

## Indice
1. Verdetto
2. La domanda
3. L'offerta: nove libri, tre con trazione
4. Prezzi
5. La concentrazione su un angolo solo
6. L'incumbent, e perche' e' diverso dagli altri
7. Il segnale di vuoto, e quanto vale
8. Cosa manca per chiudere il verdetto
9. Come rifare questa misura

---

## 1. Verdetto

**DA VERIFICARE.** Non SI FA e non NON SI FA, e la differenza conta: si prende
il dato che manca, e basta. Non si passa all'avatar «intanto che ci siamo».

Il quadro e' il piu' promettente dei tre misurati oggi — domanda in crescita,
offerta sottile, un angolo dominante che lascia scoperto tutto il resto — ma
manca la meta' che decide: le **recensioni negative** dei tre libri con
trazione. I numeri dicono che la nicchia e' poco affollata; solo le recensioni
dicono se e' affollata di libri *buoni*.

## 2. La domanda

| Misura | Valore |
|---|---|
| Indice di crescita (it.wikipedia, contro paniere) | **2,49** |
| Visite 12 mesi | 108.555 |
| Andamento grezzo | 1,34 — cresce in assoluto mentre Wikipedia dimezza |
| Suggerimento di Amazon.it | `endometriosi dieta` |

Terzo posto nella classifica dei temi in crescita (`_profili/note-mercato.md` §2),
e il primo per rapporto fra crescita e volume: il gioco d'azzardo cresce di
piu' ma parte da una base dieci volte piu' piccola.

## 3. L'offerta: nove libri, tre con trazione

Raccolti via Apify su amazon.it con sei query diverse, uniti per ASIN, filtrati
per pertinenza. Quaranta titoli scartati perche' di altro argomento.

| ASIN | Rec. | Stelle | Prezzo | Titolo |
|---|---:|---:|---:|---|
| 8844056623 | 212 | 4,4 | 16,44 € | La dieta anti endometriosi (Signorile) |
| 8858161254 | 50 | **4,9** | 13,70 € | L'inferno invisibile. Endometriosi (Fasolino) |
| B0G9X7BQ3T | 43 | 4,8 | 33,00 € | Endometriosi: Un nuovo inizio |
| B0DXMTB7BB | 3 | 5,0 | — | Endometriosi. Microbiota e alimentazione |
| B0GT991318 | 2 | 5,0 | — | Endometriosi e Alimentazione: Metodo Endo-Fit |
| B0GPQFRXS2 | 0 | — | 10,00 € | CARA ENDOMETRIOSI - PARLIAMONE: diario emotivo |
| B0H424W6F6 | 0 | — | 25,66 € | Il ricettario completo della dieta |
| B0H9JYZR1V | 0 | — | — | Endometriosi e Alimentazione: Endo-Fit (2) |
| B0H89FTPDW | 0 | — | 14,41 € | Endometriosi e dieta antinfiammatoria |

**Sei libri su nove hanno da zero a tre recensioni.** Sono entrati di recente e
non hanno preso. E' il dato piu' incoraggiante di tutta la giornata: nelle due
nicchie precedenti i concorrenti erano dieci e quindici, quasi tutti con
trazione e con editori dietro. Qui la concorrenza vera sono **tre libri**.

## 4. Prezzi

Da 10,00 a 33,00 €, mediana **15,43 €** su sei prezzi noti su nove.

Il libro col prezzo piu' alto (33 €) ha 43 recensioni; quello a 10 € ne ha zero.
Il prezzo da solo non spiega la trazione.

## 5. La concentrazione su un angolo solo

**Sette libri su nove parlano di alimentazione**: dieta, ricette, dieta
antinfiammatoria, microbiota, «Metodo Endo-Fit» (due volte, dallo stesso
filone). E' lo stesso angolo, ripetuto.

Quello che non c'e', o c'e' una volta sola:

- il percorso diagnostico e la sua lentezza
- il lavoro: assenze, colloqui, dire o non dire
- la coppia e la sessualita'
- il dolore quotidiano fuori dai pasti
- la gestione emotiva (un solo titolo, `CARA ENDOMETRIOSI`, con zero recensioni)

## 6. L'incumbent, e perche' e' diverso dagli altri

`L'inferno invisibile` di Fasolino: **4,9 stelle su 50 recensioni**, la
valutazione piu' alta della nicchia.

Non e' un pen name KDP. Le recensioni lo dicono da sole: *«Seguo il dottor
Fasolino da tanto tempo, aspettavo con ansia un suo libro»*. Ha un seguito sui
social che porta lettori al libro, ed e' un vantaggio che non si batte
scrivendo meglio.

E le sue recensioni non parlano di utilita' ma di **riconoscimento**:

> «Ora so che qualcuno ci crede»
> «per la prima volta ho avuto la sensazione di ritrovare la mia voce»
> «ho trovato le parole che per anni ho cercato»
> «senza sentirmi piu' sola»

Un libro che compete con questo su questo terreno perde. Il terreno libero e'
un altro: **la pratica quotidiana**, che Fasolino non copre e che i sette libri
di dieta coprono solo a tavola.

## 7. Il segnale di vuoto, e quanto vale

Una recensione a quattro stelle sul libro piu' venduto della nicchia:

> «Utile se sei alle prime armi. Libro utile se non si conosce la malattia o le
> basi dell'alimentazione. **Non adatto a chi conosce la malattia** e ne
> "mastica" gia' bene cause e rimedi alimentari.»

E' la lamentela piu' preziosa raccolta oggi: dice che l'offerta si ferma al
livello principiante. Chi convive con l'endometriosi da anni compra, legge, e
non trova niente di nuovo.

**Quanto vale davvero: poco, per ora.** E' *una* recensione. La regola pagata
oggi due volte e' che una conclusione che decide un investimento va verificata
da due angoli prima di essere scritta come fatto. Se la stessa lamentela
ricorre su libri diversi, e' l'indice del libro. Se resta una, e' un'opinione.

## 8. Cosa manca per chiudere il verdetto

| Cosa | Perche' manca | Effetto |
|---|---|---|
| **Recensioni negative (1-3 stelle)** | l'endpoint restituisce quello che l'actor da', senza filtro per stelle: 10 recensioni su 60 richieste, nove a 4-5 stelle | e' il dato che decide. Senza, non si sa se i libri sono buoni |
| Date di pubblicazione | non estratte dall'actor sui risultati di ricerca | niente curva di declino |
| BSR | l'actor non lo fornisce sulla ricerca: sta sulla pagina prodotto | niente stima di vendite |

Le tre raccolte hanno anche restituito `enriched: true`, cioe' parte delle
recensioni sono state completate da amazon.com e non da .it. Vanno riguardate
prima di fondarci un avatar.

**Il passo successivo e' uno solo**: le recensioni a 1, 2 e 3 stelle dei tre
libri con trazione — 8844056623, 8858161254, B0G9X7BQ3T. Dal browser sono
venti minuti (`scheda-raccolta.md`, parte B). Via Apify servirebbe un filtro
per stelle che l'endpoint oggi non espone.

## 9. Come rifare questa misura

```
POST /api/competition-map {"niche":"endometriosi","marketplace":"it","raw":true}
POST /api/amazon-reviews  {"asins":[...],"marketplace":"it","max_reviews":60}
```

Sei query diverse unite per ASIN: una sola restituisce dieci risultati e ne
tiene due o tre, e il campione cambia a ogni chiamata. Con una sola query si
concluderebbe su un campione diverso ogni volta.

Dati grezzi: `dati-concorrenti-apify.json`, `recensioni-concorrenti.txt`.
Generati, non si modificano a mano.
