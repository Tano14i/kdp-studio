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

## Stato

| # | Fase | Stato | Checkpoint | Chiuso il |
|---|------|-------|-----------|-----------|
| 0 | Cartella e convenzioni | fatto | — | 06/09 |
| 1 | Nicchia e concorrenti | fatto — **NON SI FA** | — | 06/09 |
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

La fase 1 e' chiusa con verdetto **NON SI FA**: la domanda esiste, ma lo
scaffale e' occupato da dieci pen name con lo stesso posizionamento e tre
titoli con editore. Le fasi da 2 in poi restano *da fare* e non partono su
questa nicchia. Vedi `01 Ricerca/report-nicchia.md`.

## Aperto adesso

**Il progetto e' fermo per verdetto negativo.** Aspetta una decisione
dell'autore: cambiare nicchia (restano in rosa autosabotaggio, lutto, salute
cronica) oppure chiudere qui. Se si cambia nicchia si apre una cartella
nuova: questa resta com'e', con dentro il motivo dello stop.

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
3. **Decisione dell'autore: cambiare nicchia o chiudere.** Nient'altro parte
   prima di questa. Se si cambia nicchia, si apre una cartella nuova e questa
   resta com'e'.

Tutto il resto della mappa (avatar, concept, copertina, outline, DNA,
campione, manoscritto, revisione, interni, immagini, scheda) non e' «da fare
piu' avanti»: non e' da fare affatto su questa nicchia.

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
