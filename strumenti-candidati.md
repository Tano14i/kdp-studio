# Strumenti esterni candidati
Aggiornato il 06/09/2026

## Indice
0. Esito delle ispezioni (06/09, sera)
1. Come leggere questo elenco
2. Il blocco di oggi: recensioni negative
3. Il buco strutturale: BSR e curva di declino
4. Il passo senza strumenti: interni impaginati
5. La strada ufficiale
6. Cosa NON risolvono

## 0. Esito delle ispezioni (06/09, sera)

Tre candidati ispezionati sul codice, non sulle descrizioni. La lezione vale
piu' dei singoli esiti: **la descrizione su GitHub e' pubblicita'**, e due su
tre non erano quello che dicevano.

| Repository | Cosa e' davvero | Esito |
|---|---|---|
| `omkarcloud/amazon-scraper` | **non uno scraper**: 344 righe che chiamano un'API RapidAPI a pagamento dello stesso autore. `grep review` nel codice: 0 occorrenze | scartato |
| `scrapehero-code/amazon-review-scraper` | scraper vero ma fermo a feb 2024, su `requests` semplice: sbatte nello stesso 503. Il suo codice lo ammette («try using better proxies») | scartato — ma il suo URL di partenza ha rivelato `filterByStar`, il parametro vero di Amazon |
| `neatrat/amazon-reviews-scraper` (Apify) | dichiara `ratings` ad array senza login. In produzione: **403 actor-is-not-rented**, $25/mese + consumo | non provato: decisione dell'autore di non noleggiare |

Cio' che ha risolto davvero il problema non era in nessun repository: era lo
**schema di input dell'actor che gia' usavamo**, letto invece che indovinato.
Tre campi su quattro avevano il nome sbagliato (`filterByStar` per
`filterByStars`, `maxReviews` per `maxReviewsPerProduct`, `countryCode` per
`marketplace`), e l'actor usava silenziosamente i default. Corretti, ha
colpito amazon.it per la prima volta. Ma con qualunque filtro per stelle
restituisce zero: Amazon mostra le recensioni filtrate solo a chi e' loggato.

Conclusione operativa: per le recensioni negative, **browser loggato**. Per
tutto il resto — domanda, offerta, prezzi, recensioni non filtrate con data —
la strada automatica c'e' e funziona.

## 1. Come leggere questo elenco

Le sezioni che seguono sono l'elenco originale, scritto PRIMA delle ispezioni.
Restano come traccia di cosa sembrava promettente e perche'; l'esito vero e'
nella sezione 0.

**Nessuno di questi e' stato provato** al momento in cui e' stato scritto. Sono stati trovati per descrizione, non
ispezionandone il codice, la licenza o lo stato di manutenzione. Metterli qui
come «soluzioni» sarebbe lo stesso errore commesso oggi tre volte: scrivere
come fatto qualcosa verificato da un angolo solo.

Prima di adottarne uno vanno guardati: ultimo commit, licenza, se il
marketplace italiano e' davvero supportato, e se funziona da un IP di
datacenter (vedi §6).

## 2. Il blocco di oggi: recensioni negative

Serve filtrare le recensioni per stelle. `/api/amazon-reviews` non lo espone e
ha restituito 10 recensioni su 60 richieste, nove a 4-5 stelle.

| Repository | Perche' interessa | Riserva |
|---|---|---|
| [omkarcloud/amazon-scraper](https://github.com/omkarcloud/amazon-scraper) | API REST propria, 24 marketplace, recensioni con ripartizione per voto. Autoospitato: niente costo Apify | da verificare se il filtro per stelle e' esposto |
| [scrapehero-code/amazon-review-scraper](https://github.com/scrapehero-code/amazon-review-scraper) | Restituisce anche la **data** della recensione, che oggi il nostro endpoint scarta | semplice, forse troppo: nessuna gestione dei blocchi |
| [philipperemy/amazon-reviews-scraper](https://github.com/philipperemy/amazon-reviews-scraper) | multilingua, pensato per mercati non-US | da verificare la manutenzione |

La data delle recensioni non serve solo alla fase 2: e' anche l'unico modo che
abbiamo di ricostruire la **curva di declino** senza il BSR.

## 3. Il buco strutturale: BSR e curva di declino

E' il dato che manca in tutte e tre le nicchie misurate. L'actor Apify non lo
fornisce sui risultati di ricerca, perche' sta sulla pagina del prodotto.

**[akaszynski/keepa](https://github.com/akaszynski/keepa)** — client Python per
l'API di Keepa. E' l'unica fonte seria di **BSR storico**: serie temporali per
ASIN, non l'istantanea di oggi. Supporta i marketplace europei, Italia compresa.

Perche' cambia le cose: con il BSR storico si smette di dedurre e si misura.
«Questa nicchia si sta scaldando o si sta spegnendo» diventa un grafico invece
di un'inferenza da Wikipedia; «questo concorrente vende» smette di essere una
supposizione dal numero di recensioni.

Riserva onesta: richiede un abbonamento a pagamento. E' l'unica voce di questo
elenco che costa, ed e' anche l'unica che risolve un problema che nessuna
alternativa gratuita risolve.

## 4. Il passo senza strumenti: interni impaginati

La fase 10 del metodo non ha ne' skill ne' strumenti: oggi si farebbe a mano.

| Repository | Cosa fa |
|---|---|
| [nikmcfly/kindle-book-skill](https://github.com/nikmcfly/kindle-book-skill) | **E' gia' una skill Claude**: da Markdown a EPUB3 + PDF di stampa, con i margini KDP giusti per il formato scelto (pandoc + XeLaTeX) |
| [rxpelle/book-formatter](https://github.com/rxpelle/book-formatter) | Alternativa libera a Vellum e Atticus: interni KDP con formati, margine interno, testatine |
| [jp-fosterson/pandoc-novel](https://github.com/jp-fosterson/pandoc-novel) | pandoc + LaTeX + Make, buon modello se si vuole controllare tutto |
| [vpuna/markdown-to-book](https://github.com/vpuna/markdown-to-book) | un comando: PDF brossura, PDF cartonato, EPUB |

Il primo e' il piu' interessante per struttura, non solo per funzione: la
regia dice che quando un passo senza skill torna una seconda volta va
trasformato in skill invece che rifatto a mano. Qui la skill esiste gia'.

Attenzione a un punto che il metodo prende sul serio: **la verifica va fatta
su tutte le pagine del PDF prodotto, non su un campione**, e la foliazione va
estratta dall'artefatto e non scritta a mano. Uno strumento che genera il PDF
non toglie quel controllo, lo rende solo piu' facile da automatizzare.

## 5. La strada ufficiale

**Product Advertising API** di Amazon: dati di prodotto leciti e stabili,
senza scraping e senza blocchi. Va verificato se l'account ha i requisiti —
Amazon chiede un account Affiliati con un minimo di vendite qualificanti — ma
se ci sono, e' la fonte piu' solida e la meno soggetta a rompersi.

Da controllare prima di investire tempo altrove.

## 6. Cosa NON risolvono

**Nessuno scraper autoospitato risolve il problema dell'IP.** Da questo
contenitore `www.amazon.it/s` risponde 503, e ha risposto 503 anche a un
browser Chromium vero: e' l'indirizzo di datacenter a essere rifiutato, non lo
strumento. Lo stesso vale su Railway.

Il valore di Apify non e' il codice — quello si riscrive in un pomeriggio — ma
i **proxy residenziali**. Uno scraper autoospitato sposta solo il problema, a
meno di aggiungerci dei proxy, che e' di nuovo un costo.

Questo non toglie valore all'elenco: Keepa passa da API e non fa scraping, gli
strumenti di impaginazione girano in locale, e la PA-API e' ufficiale. Ma va
detto prima, non dopo aver installato qualcosa.
