# Dossier di metodo — endometriosi
pen name da decidere · italiano (Amazon.it) · avviato il 06/09/2026

E' il registro del progetto, con il nome che la regia cerca per primo
all'avvio. Un file solo.

## Indice
1. Stato
2. Aperto adesso
3. Cosa manca, in ordine
4. Da non dimenticare
5. Errori commessi e come sono stati corretti
6. Perche' le recensioni negative non arrivano da Apify

## Stato

| # | Fase | Stato | Checkpoint | Chiuso il |
|---|------|-------|-----------|-----------|
| 0 | Cartella e convenzioni | fatto | — | 06/09 |
| 1 | Nicchia e concorrenti | **in corso — DA VERIFICARE** | — | |
| 2 | Avatar cliente | da fare | — | |
| 3 | Concept e positioning | da fare | CP1 | |
| 4 | Titolo, sottotitolo, copertina | da fare | CP2 | |
| 5 | Outline | da fare | CP3 | |
| 6 | DNA stilistico | da fare | CP4 | |
| 7 | Campione di scrittura | da fare | CP5 | |
| 8 | Manoscritto | da fare | — | |
| 9 | Revisione | da fare | — | |
| 10 | Interni impaginati | da fare | — | |
| 11 | Immagini e copertina finita | da fare | — | |
| 12 | Scheda, A+, campagne | da fare | CP7 | |
| 13 | Traduzione e mercati | da fare | CP6 | |

La fase 1 e' **in corso**, non fatta: il verdetto e' DA VERIFICARE, che non e'
un verdetto ma un compito. Vedi `01 Ricerca/report-nicchia.md`.

## Aperto adesso

Un dato, non piu' una decisione: **le recensioni a 1, 2 e 3 stelle** dei tre
libri con trazione — `8844056623`, `8858161254`, `B0G9X7BQ3T`.

**Deciso il 06/09 sera, dall'autore: si raccolgono dal browser.** Scartato il
noleggio di `neatrat` ($25/mese, non dimostrato). Link gia' filtrati e formato
in `01 Ricerca/da-raccogliere.md`.

E' l'unica cosa che manca per chiudere la fase 1. La fase 2 non parte prima,
per quanto allettante sia: e' la regola che oggi ha risparmiato due libri.

## Cosa manca, in ordine

1. ~~Cartella e convenzioni~~ — fatto il 06/09
2. **Recensioni negative dei tre libri con trazione — solo dal browser.**
   La strada automatica e' stata tentata e non funziona, vedi §5. Restano
   venti minuti con `scheda-raccolta.md`, parte B: recensioni a 1, 2 e 3
   stelle di `8844056623`, `8858161254`, `B0G9X7BQ3T`, testo intero.
3. Poi: chiudere la fase 1 con SI FA o NON SI FA, con i numeri accanto.
4. Solo dopo: avatar cliente, sulle stesse recensioni.

## Da non dimenticare

- **Sette libri su nove parlano di alimentazione.** Il vuoto, se c'e', non e'
  il tema ma l'angolo: diagnosi, lavoro, coppia, dolore quotidiano fuori dai
  pasti.
- **L'incumbent ha un seguito social** (Fasolino, 4,9 stelle su 50 recensioni).
  Non lo si batte scrivendo meglio sullo stesso terreno. Le sue recensioni
  parlano di riconoscimento, non di utilita': il terreno libero e' la pratica
  quotidiana.
- **Sei libri su nove hanno da zero a tre recensioni.** La concorrenza vera
  sono tre libri, non nove. E' il quadro piu' favorevole dei tre misurati oggi.
- **Una sola query non basta.** Una chiamata restituisce dieci risultati e ne
  tiene due o tre, e il campione cambia ogni volta. Sei query unite per ASIN.
- **`enriched: true` nelle recensioni** significa che parte vengono da
  amazon.com e non da .it. Da riguardare prima di fondarci un avatar.

## Errori commessi e come sono stati corretti

**06/09 — Detto «quattro pertinenti su dieci» a occhio.**
Guardando la prima risposta avevo contato quattro libri sul tema. Il filtro,
applicato agli stessi dieci titoli, ne ha trovati tre: avevo incluso *Il
capitale umano della vulvodinia*, che e' una patologia diversa. Contare a
occhio una lista corta sembra sicuro, e non lo e'.

**06/09 — Uno SHA git inventato.**
Nel chiudere la PR #3 avevo passato come `expectedHeadSha` uno SHA completo
ricostruito a memoria da quello breve. GitHub ha rifiutato con 409 invece di
procedere. Il guasto sarebbe stato invisibile senza quel controllo: e' lo
stesso principio degli strumenti scritti oggi, che si rifiutano di concludere
quando non sanno.

## 6. Perche' le recensioni negative non arrivano da Apify

Chiuso una prima volta il 06/09 pomeriggio, **riaperto e richiuso la sera con
la causa esatta**, dopo che il 404 e' stato reso parlante (PR #8).

La sequenza, per chi la riprendera':

1. `filterByStar` passato nell'URL a `epctex` (PR #4, #5): **non poteva
   funzionare** — quell'actor non accetta pagine `/product-reviews` ne'
   filtri, e in piu' non e' mai partito (403 `actor-is-not-rented` in ogni
   chiamata della giornata).
2. Nomi di campo corretti su `automation-lab` (PR #6): ora colpisce davvero
   amazon.it — 9 recensioni datate invece di 5 americane, 1 negativa — ma con
   **qualunque** `filterByStars` diverso da `all` restituisce **0 elementi**.
   Coerente con Amazon che mostra le recensioni filtrate e paginate solo a
   chi e' loggato. 9 su 212 e' quante ne mostra la pagina prodotto.
3. `neatrat` (PR #7), che dichiara `ratings` ad array senza login: **403
   `actor-is-not-rented`**. Non ha mai girato. Costa **$25/mese + consumo**.

Quindi la strada automatica **esiste ma non e' gratuita**, e non e' ancora
dimostrata: noleggiare `neatrat` e' l'unico modo di sapere se mantiene la
promessa. E' una decisione dell'autore, con il prezzo accanto.

Senza noleggio: recensioni negative solo dal browser, `scheda-raccolta.md`
parte B, venti minuti per i tre ASIN.

Cosa e' stato guadagnato comunque: le date delle recensioni; l'avviso che ha
impedito due volte un verdetto capovolto; il 404 che ora dice cosa ha fatto
ogni actor; e la prima negativa italiana vera su `8844056623`, seconda voce
indipendente che chiama superficiale il libro piu' venduto della nicchia.
