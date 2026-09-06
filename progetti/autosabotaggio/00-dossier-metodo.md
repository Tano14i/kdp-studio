# Dossier di metodo — autosabotaggio
pen name da decidere · italiano (Amazon.it) · avviato il 06/09/2026

E' il registro del progetto, con il nome che la regia cerca per primo
all'avvio. Un file solo: se ce ne fossero due, fra tre giorni sarebbero
diversi e nessuno saprebbe quale vale.

## Indice
1. Stato
2. Aperto adesso
3. Cosa manca, in ordine
4. Da non dimenticare
5. Errori commessi e come sono stati corretti
6. Aggiornamento del 06/09, sera
7. Il passo 1b, aperto la sera del 06/09

## Stato

| # | Fase | Stato | Checkpoint | Chiuso il |
|---|------|-------|-----------|-----------|
| 0 | Cartella e convenzioni | fatto | — | 06/09 |
| 1 | Nicchia e concorrenti | fatto — **NON SI FA** sul tema | — | 06/09 |
| 1b | Angolo (`ricerca-inversa`) | fatto — **NON SI FA** sull'angolo, definitivo | — | 06/09 |
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

Fase 1 chiusa con verdetto **NON SI FA**: quindici concorrenti su tre
sotto-temi, con tre bestseller da editore in cima. Vedi
`01 Ricerca/report-nicchia.md`.

**Quel verdetto non chiude piu' il progetto.** Riguarda il *tema*, e nella
mappa attuale un NON SI FA sul tema apre il passo **1b** invece di finire la
corsa. Il 1b e' stato eseguito il 06/09 sera: vedi §7 e
`01 Ricerca/01b-angolo.md`.

Le righe **1b** e **14** sono state aggiunte alla tabella nella stessa
occasione: questa si fermava al 13 ed era la vecchia mappa.

## Aperto adesso

**Il progetto e' chiuso su tema e su angolo, e adesso il no e' solido.** Il
passo 1b ha provato quattro pieghe; la piu' forte era l'adulto con ADHD, e la
verifica sullo scaffale l'ha smentita il 06/09 sera: quattordici titoli in
prima pagina, uno solo clinico, dieci pratici rivolti proprio a quel lettore.
Il sotto-angolo della procrastinazione ha gia' il suo libro. Vedi §7 e
`01 Ricerca/scaffale-adhd-adulti.md`.

**La condizione e' stata verificata la sera stessa, ed e' andata contro.** Era
scritta prima di conoscere i numeri per non poterla piegare dopo: sotto 30
recensioni sui tre titoli piu' recensiti l'angolo tornava in discussione, a 30
o piu' il no diventava definitivo.

I tre piu' recensiti hanno **179, 158 e 114**, con voti fra 4,0 e 4,9, e sei
titoli su dieci stanno sopra 85. Non e' uno scaffale di fantasmi: e' uno
scaffale di libri che i lettori tengono.

**Questa cartella si chiude qui** — due no, uno sul tema e uno sull'angolo,
quattro pieghe provate e il motivo di ognuna scritto. Se un giorno qualcuno la
riapre, ci trova un no molto piu' solido di quello di stamattina, che era il no
di chi non aveva provato niente.

La domanda che era aperta qui prima — «ha senso provare un'altra nicchia con
lo strumento attuale?» — ha ricevuto una risposta parziale il 06/09 sera, e
non e' quella che sembrava: **lo strumento attuale non era l'unico**. Le
schede prodotto di Amazon.it si leggono da qui, e i numeri che hanno prodotto
hanno corretto una conclusione del passo 1. Vedi §7.

## Cosa manca, in ordine

1. ~~Cartella e convenzioni~~ — fatto il 06/09
2. ~~Nicchia e concorrenti~~ — fatto il 06/09, verdetto **NON SI FA**
3. ~~Passo 1b, l'angolo~~ — fatto il 06/09 sera, `01 Ricerca/01b-angolo.md`.
4. ~~La verifica dell'angolo sullo scaffale ADHD~~ — fatta il 06/09 sera,
   `01 Ricerca/scaffale-adhd-adulti.md`. Esito: **NON SI FA sull'angolo**.
5. ~~Le recensioni dei tre titoli piu' recensiti~~ — fatte il 06/09 sera:
   179, 158, 114. La condizione non e' rispettata, il no e' definitivo.
6. **Scegliere come procurarsi i dati dei concorrenti.** Non e' piu' una
   domanda senza risposta: due strade sono pronte e descritte in
   `_profili/note-mercato.md` §5-bis — il backend su Railway (vivo, con
   APIFY_TOKEN configurato; serve prima il merge della PR #2 e il redeploy,
   poi la chiave) oppure la raccolta nel browser (`scheda-raccolta.md` +
   `analizza_concorrenti.py`, che si puo' fare adesso). Manca solo la scelta.
7. **Poi: su quale nicchia spenderla.** Non piu' «non su queste due»: il
   passo 1b ha riaperto entrambe a livello di angolo. La classifica dei temi
   in crescita resta in `_profili/note-mercato.md` §2, e da li' viene la
   piega piu' forte di questo progetto (ADHD adulti, indice 2,59 e 277.376
   visite: la miglior combinazione crescita+volume della tabella).
8. ~~`avatar-cliente`~~ — non si apre: non c'e' nessun SI FA da cui partire.

## Da non dimenticare

- **Il mercato e' Amazon.it, in italiano.** Ogni misura va presa su amazon.it:
  una presa su amazon.com non vale e non va confrontata.
- **Lo strumento va puntato sul mercato giusto.** `completion.amazon.com`
  risponde 200 con lista vuota per ogni marketplace non-US. Corretto in
  `kdp_server.py` il 06/09; `test_amazon_markets.py` lo sorveglia.
- **Su Amazon.it l'alias `stripbooks` non filtra ai soli libri.** E' la causa
  sia delle radici nominali che tornano ferramenta, sia del falso segnale
  «+libro» qui sotto. Sono lo stesso difetto visto da due lati.
- **Una query senza autore attaccato non e' una query libera.** Puo' essere un
  titolo cosi' noto da non aver bisogno del nome. Prima di chiamarla vuota, si
  cerca il titolo. Costato due volte in un giorno.
- **L'autocomplete non puo' trovare un vuoto di tema.** Mostra solo query con
  volume, e nella saggistica pratica italiana quel volume implica gia' dei
  libri sopra. Il vuoto sta nell'angolo, e si trova nelle recensioni dei
  concorrenti, non nella barra di ricerca.

## Errori commessi e come sono stati corretti

**06/09 — Il segnale «+libro» inventato e creduto.**
Avevo definito che una query col suffisso «libro» segnalasse un vuoto: chi
scrive «vittimismo libro» lo fa perche' la ricerca nuda non gli fa emergere un
libro. L'ho chiamato «il segnale di vuoto piu' pulito del raccolto» e ci ho
costruito sopra parte della rosa di nicchie presentata all'autore.

Falso. Le tre query col suffisso — `autosabotaggio libri`, `vittimismo libro`,
`procrastinazione libro` — hanno rispettivamente sei, tre e sei libri, con
bestseller in cima. La spiegazione vera era gia' nei dati dello stesso
giorno, in un'osservazione mai collegata: su Amazon.it `stripbooks` non filtra
ai soli libri, ed e' per questo che «guida per» restituiva box doccia. Chi
vuole un libro aggiunge «libro» perche' il filtro del reparto e' rotto, non
perche' il libro manchi.

Il motivo tecnico conta piu' dell'esito: avevo due osservazioni sullo stesso
difetto, prese lo stesso giorno, e le ho tenute separate. Una era il rumore
nei dati, l'altra l'avevo promossa a segnale di opportunita'.

**06/09 — La stessa trappola della query nuda, due volte.**
Nella nicchia precedente avevo letto «come non odiare tuo marito dopo i figli»
come query libera: era un titolo Sonzogno. Qui la stessa cosa sarebbe
successa con «come smettere di fare la vittima», che e' un titolo Mondadori di
Giulio Cesare Giacobbe. Stavolta ho cercato il titolo prima di concludere, e
la trappola non e' scattata. La regola scritta dopo il primo errore ha
funzionato al primo impiego.


## Aggiornamento del 06/09, sera

Questo progetto resta chiuso: il verdetto NON SI FA non cambia, e le prove
stanno in `01 Ricerca/report-nicchia.md`.

Cambia pero' il motivo per cui il **metodo** era fermo. Al momento della
chiusura mancava lo strumento per misurare l'offerta, e quella mancanza era
scritta qui come un problema aperto. Non lo e' piu'.

Cosa e' stato fatto dopo la chiusura, e dove sta scritto:

| Cosa | Dove |
|---|---|
| Le due strade per i dati dei concorrenti | `_profili/note-mercato.md` §5-bis |
| Classifica dei temi in crescita (26 misurati) | `_profili/note-mercato.md` §2 |
| Scheda per la raccolta nel browser | `scheda-raccolta.md` |
| Strumento che trasforma la raccolta in numeri | `analizza_concorrenti.py` |
| Fix del marketplace, piu' i controlli automatici | PR #2 |

Si scrive qui perche' chi riprende questo progetto legge questo file per primo,
e senza questa riga ricomincerebbe a cercare una soluzione che esiste gia'.


## 7. Il passo 1b, aperto la sera del 06/09

Il progetto era chiuso con NON SI FA. Non era sbagliato il verdetto: era
incompleta la mappa. Un NON SI FA riguarda il **tema**, e in questo mercato un
tema libero non esiste per costruzione — quindi chiudere li' vuol dire
chiudere sempre. Il documento del 1b sta in `01 Ricerca/01b-angolo.md`.

**L'angolo candidato.** Per l'adulto con ADHD — diagnosticato o che se lo
sospetta — che ha gia' provato i libri sulla procrastinazione e li ha mollati
a meta': un libro da **aprire nel momento in cui stai per mollare**, non da
leggere dall'inizio alla fine. Tre pieghe nella stessa riga: pubblico,
momento, uso. I quindici concorrenti trattano tutti l'autosabotaggio come un
problema di volonta', ed e' esattamente il motivo per cui falliscono su questo
lettore. Un percorso in ventun giorni venduto a un adulto con ADHD chiede al
lettore proprio la cosa che non riesce a fare.

**Il numero che corregge il passo 1, e va ricordato.** Le schede prodotto di
Amazon.it sono risultate leggibili da questo contenitore (circa una volta su
quattro, con `sonda_angolo.py`). I numeri che ne escono:

| Titolo | Voto | Recensioni |
|---|---:|---:|
| Wiest, *La montagna sei tu* | 4,4 | **1.204** |
| Giacobbe, *Come smettere di fare la vittima* (Mondadori) | 4,4 | 59 |
| Ramirez Basco, *Prima o poi lo faccio!* | 4,5 | 32 |
| Ho, *Basta autosabotaggio!* | 4,0 | **14** |
| Pradervand, *Mai piu' vittima* | 3,8 | **10** |

Il report del passo 1 diceva «tre bestseller da editore in cima ai tre
sotto-temi» e aggiungeva che il verdetto non dipendeva dai numeri mancanti.
I numeri dicono che c'e' **un gigante e quattro libri sottili**: sul
vittimismo l'ancora Mondadori ha 59 recensioni, su procrastinazione la
migliore ne ha 32. Non ribalta il NON SI FA sul tema — chi entra
sull'autosabotaggio generico entra contro Wiest — ma smonta il pezzo di
ragionamento che parlava di tre bestseller.

**«Ancora con editore» e' una categoria, non una misura.** E' la regola che
esce da qui, ed e' registrata in `_profili/note-mercato.md` §3-bis. Vale per
ogni nicchia futura: un editore in cima a una lista non dice quanto vende quel
libro, e in due nicchie su due i numeri veri erano molto piu' bassi di quanto
la categoria facesse pensare.


## 8. La verifica che ha chiuso l'angolo, e l'errore che l'aveva aperto

06/09 sera. Lo scaffale `adhd adulti` e' stato guardato nel browser, ed e'
`01 Ricerca/scaffale-adhd-adulti.md`. Il conteggio chiesto — quanti clinici,
quanti pratici — e' tornato **1 clinico e 10 pratici per l'adulto che ce l'ha
addosso**, su quattordici titoli in prima pagina. Dodici su quattordici
autopubblicati, otto in Kindle Unlimited.

La piega piu' forte del passo 1b poggiava su una frase di
`_profili/note-mercato.md` §3: sopra ADHD adulti c'erano «sei concorrenti, o
clinici o strategie generiche», quindi in mezzo non c'era niente. In mezzo c'e'
tutto.

**L'errore, con la causa tecnica.** Quei sei erano i titoli emersi da un paio
di ricerche, e accanto era anche scritto che l'elenco era «parziale per
difetto». Poi la frase e' stata riusata come se fosse un censimento. La regola,
ora anche in `note-mercato.md` §3:

> Un conteggio di concorrenti dichiarato parziale non puo' reggere una
> conclusione sul vuoto. Un elenco che sa di essere incompleto puo' dire
> «e' occupato», mai «e' libero».

**Cosa invece ha funzionato, e va detto insieme all'errore.** Il passo 1b non
aveva scritto SI FA: aveva scritto «in corso, manca la verifica sullo
scaffale», e messo quella verifica come punto 1. Se avesse chiuso con un SI
FA, adesso ci sarebbero un avatar e un outline costruiti su un vuoto
inesistente. Il cancello e' costato una ricerca nel browser invece di tre
settimane — ed e' esattamente il mestiere che fa.

**La chiusura, la sera stessa.** La condizione sulle recensioni e' stata
verificata recuperando gli ASIN dalle ricerche web e leggendo le schede con
`sonda_angolo.py`: dieci titoli misurati, i tre piu' recensiti a 179, 158 e
114. Tabella in `01 Ricerca/scaffale-adhd-adulti.md` §4.

Due cose imparate strada facendo, che valgono oltre questa nicchia:

- **gli ASIN si recuperano dalla ricerca web**, non solo dal browser
  dell'autore. `www.amazon.it/s` resta 503, ma cercare un titolo esatto su un
  motore di ricerca restituisce l'URL `amazon.it/dp/<ASIN>`, e da li'
  `sonda_angolo.py` legge i numeri. E' la strada che ha chiuso questo
  progetto in cinque minuti invece di rimandare a un altro giro nel browser;
- **ogni conteggio fatto finora su questa nicchia era per difetto.** I dieci
  titoli misurati sono ASIN *diversi* dai quattordici visti in prima pagina:
  lo scaffale vero ne ha almeno venti.
