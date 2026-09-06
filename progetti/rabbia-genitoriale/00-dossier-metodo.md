# Dossier di metodo — rabbia-genitoriale
pen name da decidere · italiano (Amazon.it) · avviato il 06/09/2026

E' il registro del progetto, con il nome che la regia cerca per primo
all'avvio. Un file solo: se ce ne fossero due, fra tre giorni sarebbero
diversi e nessuno saprebbe quale vale.

Titolo di lavoro, non titolo del libro: si cambia solo quando il checkpoint 2
decide il titolo vero, e questa cartella non si rinomina mai.

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
| 1b | Angolo (`ricerca-inversa`) | **in corso** — manca la verifica | — | |
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

La fase 1 e' chiusa con verdetto **NON SI FA**: la domanda esiste, ma lo
scaffale e' occupato da dieci pen name con lo stesso posizionamento e tre
titoli con editore. Vedi `01 Ricerca/report-nicchia.md`.

**Quel verdetto non chiude piu' il progetto.** Riguarda il *tema*, e nella
mappa attuale un NON SI FA sul tema apre il passo **1b** invece di finire la
corsa. Il 1b e' stato eseguito il 06/09 sera: vedi §7 e
`01 Ricerca/01b-angolo.md`.

Le righe **1b** e **14** sono state aggiunte alla tabella nella stessa
occasione: questa si fermava al 13 ed era la vecchia mappa. Il 1b mancante non
era un dettaglio di forma — era la riga che decideva se questo progetto fosse
chiuso o solo fermo.

## Aperto adesso

**Una verifica di venti minuti nel browser dell'autore, e non e' piu' una
decisione: e' un dato.** Il passo 1b ha trovato un angolo che regge su
quattro pieghe, ma un angolo trovato nelle recensioni resta un'ipotesi finche'
non e' guardato lo scaffale — e la ricerca di Amazon.it da qui risponde 503.

Da cercare, con `scheda-raccolta.md`: `dopo aver urlato ai figli`, `senso di
colpa genitori`, `chiedere scusa ai figli`, `riparare rapporto con i figli`.
La domanda e' una sola: **qualcuno vende gia' il dopo, invece del prima?**

L'elenco completo, in ordine, sta in `01 Ricerca/01b-angolo.md` §7. La fase 2
non parte prima, per quanto l'angolo sia convincente: e' la regola che oggi ha
gia' risparmiato due libri.

## Da non dimenticare

- **Il mercato e' Amazon.it, in italiano.** Scelto il 06/09. Ogni misura va
  presa su amazon.it: una presa su amazon.com non vale e non va confrontata.
- **Lo strumento va puntato sul mercato giusto.** L'autocomplete di Amazon su
  `completion.amazon.com` risponde 200 con lista vuota per ogni marketplace
  non-US. Uno zero cosi' sembra assenza di domanda e non lo e'. Corretto in
  `kdp_server.py` il 06/09; `test_amazon_markets.py` lo sorveglia.
- **Su Amazon.it l'alias `stripbooks` non filtra ai soli libri.** Le radici
  nominali ("guida per") tornano ferramenta. Solo radici a verbo di intento.
- **Il suffisso «libro» in una query e' un segnale di vuoto.** Chi scrive
  "... libro" lo fa perche' la ricerca senza quella parola non gli ha fatto
  emergere un libro.
- **C'e' un incumbent forte nella genitorialita' italiana** (Novara, «Urlare
  non serve a nulla»), con distribuzione editoriale vera. Va misurato prima
  di decidere l'angolo, non dopo. Misurato il 06/09: non era uno, erano tre
  con editore piu' dieci autopubblicati.
- **Il suffisso «+libro» in una query NON e' un segnale di vuoto.** Lo avevo
  creduto e usato per costruire la rosa delle nicchie: smentito il 06/09
  stesso, vedi `01 Ricerca/report-nicchia.md` §9. Misura il fatto che su
  Amazon.it il filtro del reparto Libri non funziona, non un buco di mercato.
- **Una query senza autore attaccato non e' una query libera.** Puo' essere
  un titolo cosi' noto da non aver bisogno del nome dell'autore: e' il caso
  di «come non odiare tuo marito dopo i figli», che e' un Sonzogno del 2017.
  Prima di chiamare vuota una query, si cerca il titolo. Errore commesso e
  corretto il 06/09, vedi `01 Ricerca/report-nicchia.md` §5.

## Cosa manca, in ordine

1. ~~Cartella e convenzioni~~ — fatto il 06/09
2. ~~Nicchia e concorrenti~~ — fatto il 06/09, verdetto **NON SI FA**
3. ~~Passo 1b, l'angolo~~ — fatto il 06/09 sera, `01 Ricerca/01b-angolo.md`.
   Tre pieghe su quattro reggono, con parole di lettori italiani sotto.
4. **La verifica dell'angolo sullo scaffale** — vedi «Aperto adesso». E' la
   sola cosa che separa questo progetto da un SI FA o da un NON SI FA
   definitivo.
5. **Scegliere come procurarsi i dati dei concorrenti.** Non e' piu' una
   domanda senza risposta: due strade sono pronte e descritte in
   `_profili/note-mercato.md` §5-bis — il backend su Railway (vivo, con
   APIFY_TOKEN configurato; serve prima il merge della PR #2 e il redeploy,
   poi la chiave) oppure la raccolta nel browser (`scheda-raccolta.md` +
   `analizza_concorrenti.py`, che si puo' fare adesso). Manca solo la scelta.
6. **Poi, e solo con un SI FA scritto:** `avatar-cliente`.

Tutto il resto della mappa (concept, copertina, outline, DNA, campione,
manoscritto, revisione, interni, immagini, scheda) resta fermo: non e' «da
fare piu' avanti», e' da non fare finche' il punto 4 non ha risposta.

## Errori commessi e come sono stati corretti

**06/09 — Lo strumento puntato sul mercato sbagliato.**
La prima misura sull'autocomplete di Amazon.it e' tornata vuota. Non era il
mercato senza domanda: era `completion.amazon.com`, che per ogni marketplace
non-US risponde HTTP 200 con lista vuota. L'host deve essere
`completion.amazon.it`. Corretto in `kdp_server.py`, sorvegliato da
`test_amazon_markets.py`. *Prima di credere a uno zero, verifica di aver
interrogato la cosa giusta.*

**06/09 — Zero uniforme scambiato per misura.**
Un test sulle «continuazioni» di una query e' tornato zero su tutte e quindici
le query provate. Uno zero cosi' uniforme e' lo strumento, non il mondo:
l'autocomplete completa per prefisso, e una frase gia' completa non ha
continuazioni per costruzione. La misura e' stata buttata invece che
riportata.

**06/09 — Una query nuda scambiata per una query libera.**
Avevo dedotto che «come non odiare tuo marito dopo i figli», arrivando senza
nome d'autore attaccato, fosse una domanda che nessun libro occupava. Era il
contrario: e' il titolo di Jancee Dunn per Sonzogno, e chi la digita cerca
quel libro per nome. La deduzione era sbagliata nel ragionamento, non solo
nell'esito, ed e' stata presentata all'autore come punto di forza prima di
essere verificata. *Una conclusione che decide un investimento va verificata
da due angoli prima di essere scritta come fatto.*


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

Il progetto era stato chiuso con NON SI FA e archiviato. Non era sbagliato il
verdetto: era incompleta la mappa. Un NON SI FA riguarda il **tema**, e in
questo mercato un tema libero non esiste per costruzione
(`_profili/note-mercato.md` §1) — quindi chiudere li' vuol dire chiudere
sempre. Il passo 1b chiede un'altra cosa: **dentro questo tema occupato, quale
angolo e' scoperto?**

Il documento sta in `01 Ricerca/01b-angolo.md`. Tre cose da tenere a mente
senza doverlo riaprire:

**L'angolo candidato.** Non un altro libro su come non urlare, ma cosa si fa
nei dieci minuti dopo — per il genitore che ha gia' urlato e lo sa. Tredici
concorrenti su tredici vendono la prevenzione; nessuno di loro puo' occupare
il dopo senza contraddire il proprio titolo.

**La prova, e il suo limite.** Due lettrici italiane diverse dicono con parole
loro che il libro dell'incumbent le ha fatte sentire in colpa — «Ottimo se
volete sapere cosa sbagliate!» e «mi sono sentita una 💩 per quasi tutto il
tempo della lettura». Quello e' un dato. Che cio' che manca sia *la
riparazione* e' invece una deduzione, dichiarata come tale nel documento: e'
il motivo per cui il 1b non chiude con un SI FA.

**Un numero che corregge il passo 1.** `Smettila di urlare` di Naumburg, una
delle tre «ancore con editore» che avevano deciso il NON SI FA, ha **14
recensioni** su Amazon.it. Il passo 1 le aveva contate come prova di
saturazione senza poterle misurare, e aveva scritto che il verdetto non
dipendeva da quei numeri. Sul progetto gemello lo stesso controllo ha trovato
la stessa cosa in modo piu' netto. La regola che ne esce, e che vale per ogni
misura futura: **«ancora con editore» e' una categoria, non una misura.**
Registrata in `_profili/note-mercato.md` §3-bis.
