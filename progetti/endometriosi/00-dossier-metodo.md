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
7. Sospeso il 06/09 sera: il tema e' troppo medico

## Stato

| # | Fase | Stato | Checkpoint | Chiuso il |
|---|------|-------|-----------|-----------|
| 0 | Cartella e convenzioni | fatto | — | 06/09 |
| 1 | Nicchia e concorrenti | **sospeso** — era DA VERIFICARE | — | |
| 1b | Angolo (`ricerca-inversa`) | non aperto | — | |
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
| 14 | Promozione social | da fare | — | |

La fase 1 non e' ne' chiusa ne' in corso: e' **sospesa**. Il verdetto era
DA VERIFICARE — un compito, non un verdetto — e quel compito non verra'
svolto, perche' il 06/09 sera l'autore ha fermato il progetto per un motivo
che sta a monte della misura. Vedi §7.

Le righe **1b** e **14** sono state aggiunte alla tabella il 06/09 sera: la
mappa di `regia` le ha, questa tabella si fermava al 13 ed era la vecchia
mappa. Su questo progetto restano non aperte.

## Aperto adesso

**Niente. Il progetto e' sospeso dal 06/09 sera, per decisione dell'autore:
il tema e' troppo medico.** Il perche' e cosa comporta stanno in §7.

Non e' un NON SI FA della fase 1 — la fase 1 non e' mai arrivata a un
verdetto. E' uno stop che arriva da sopra la misura, e va tenuto distinto:
i numeri di `01 Ricerca/report-nicchia.md` restano validi e favorevoli, e se
un giorno la decisione cambiasse si ripartirebbe da li', non da zero.

## Cosa manca, in ordine

Niente, finche' la sospensione regge. Quello che mancava resta scritto qui,
in ordine, per chi riaprisse il progetto:

1. ~~Cartella e convenzioni~~ — fatto il 06/09
2. ~~Recensioni negative dei tre libri con trazione~~ — **non piu' da fare**,
   progetto sospeso il 06/09 sera. Erano venti minuti con
   `scheda-raccolta.md` parte B sui tre ASIN `8844056623`, `8858161254`,
   `B0G9X7BQ3T`, e `01 Ricerca/da-raccogliere.md` e' pronto: se il progetto
   riparte, si riparte da li'.
3. ~~Chiudere la fase 1 con SI FA o NON SI FA~~ — sospeso insieme al resto.
4. ~~Avatar cliente~~ — sospeso.

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
7. Sospeso il 06/09 sera: il tema e' troppo medico

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


## 7. Sospeso il 06/09 sera: il tema e' troppo medico

**Decisione dell'autore, non conclusione di una misura.** Il progetto si ferma
prima che la fase 1 arrivi a un verdetto, e il motivo non e' nei numeri: e'
che l'endometriosi e' una patologia, e un libro pratico su una patologia
scritto da un pen name e' un mestiere diverso da quello che questo metodo sa
fare.

Va scritto qui perche' e' il tipo di decisione che, se non messa nero su
bianco, fra tre giorni verrebbe presa di nuovo in modo diverso — e perche'
questo tema aveva i numeri migliori dei tre misurati, quindi la tentazione di
riaprirlo tornera'.

**Cosa si perde, detto onestamente.** Era il quadro piu' favorevole del
raccolto, ed e' giusto sapere a cosa si rinuncia:

- indice di crescita 2,49 con 108.555 visite in dodici mesi
  (`_profili/note-mercato.md` §2), terzo su 26 temi misurati;
- sei libri su nove con da zero a tre recensioni: la concorrenza vera erano
  tre titoli, non nove;
- un angolo gia' visibile senza altre misure — sette libri su nove parlano di
  alimentazione, e diagnosi, lavoro, coppia e dolore quotidiano erano scoperti.

Quell'angolo, in altre parole, era gia' un passo 1b riuscito prima che il
passo 1b esistesse. La sospensione non lo smentisce: lo mette da parte.

**Cosa resta valido per gli altri progetti.** Il motivo dello stop e' il
*tipo* di tema, non il metodo, quindi due cose vanno riusate e non rifatte:

- la regola «il vuoto sta nell'angolo, non nel tema» e' nata qui, ed e' quella
  che ha fatto scrivere `ricerca-inversa`;
- il lavoro sulle recensioni via Apify, con la sua diagnosi completa in §6,
  vale per qualunque nicchia: la strada automatica resta chiusa e documentata
  come chiusa. Non si ritenta.

**Cosa lo riaprirebbe.** Solo un cambio di premessa dell'autore — un pen name
con una competenza dichiarabile sul tema, oppure un taglio che esce dal
medico (per esempio il lavoro e la coppia, senza toccare sintomi e cure). Se
succede, questo file e `01 Ricerca/` sono gia' pronti e la misura non si
rifa'.
