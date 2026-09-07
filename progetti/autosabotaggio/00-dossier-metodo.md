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

## Stato

| # | Fase | Stato | Checkpoint | Chiuso il |
|---|------|-------|-----------|-----------|
| 0 | Cartella e convenzioni | fatto | — | 06/09 |
| 1 | Nicchia e concorrenti | fatto — **NON SI FA** sul tema | — | 06/09 |
| 1b | Angolo (`ricerca-inversa`) | **da fare** | verdetto | |
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

Fase 1 chiusa con verdetto **NON SI FA**: quindici concorrenti su tre
sotto-temi, con tre bestseller da editore in cima. Vedi
`01 Ricerca/report-nicchia.md`.

## Aperto adesso

**Il progetto e' fermo per verdetto negativo.** Ma la decisione che aspetta
l'autore non e' piu' «quale nicchia proviamo adesso»: e' se ha senso provarne
un'altra con lo strumento attuale. Due nicchie, due NON SI FA, stesso motivo
di fondo — vedi `01 Ricerca/report-nicchia.md` §5.

## Cosa manca, in ordine

1. ~~Cartella e convenzioni~~ — fatto il 06/09
2. ~~Nicchia e concorrenti~~ — fatto il 06/09, verdetto **NON SI FA**
3. **Passo 1b — `ricerca-inversa`, non ancora eseguito.** Questo progetto e'
   stato chiuso il 06/09 con la regia di allora, per cui un NON SI FA sul tema
   fermava tutto. La regia versionata nel repo (PR #12, stessa sera) dice
   un'altra cosa: il no riguarda il *tema*, e prima di chiudere si prova a
   piegarlo — pubblico, momento, uso, angolo. Il progetto si ferma davvero
   solo se non regge nessuna delle quattro pieghe. Quindi lo stato onesto non
   e' «chiuso» ma **«fermo al 1b»**. I dati dei concorrenti, quando serviranno
   per la verifica dell'angolo, si prendono da Railway: `competition-map` con
   `raw:true` e `amazon-reviews` senza filtro funzionano (vedi
   `_profili/note-mercato.md` §5-bis).
4. **Poi: su quale nicchia spenderla.** Non su queste due, chiuse con NON SI
   FA. La classifica dei temi in crescita e' in `_profili/note-mercato.md` §2.

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
