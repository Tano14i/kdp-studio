# Angolo — autosabotaggio
Passo 1b · `ricerca-inversa` · Amazon.it, italiano · 06/09/2026

Il passo 1 ha chiuso con **NON SI FA** sul tema. Nella mappa attuale quel
verdetto non chiude piu' il progetto: lo manda qui. Questo file prova quattro
pieghe prima di lasciar cadere la nicchia, e dice a che punto e' la verifica.

## Indice
1. Da dove si e' partiti, e cosa non si e' potuto guardare
2. Le parole dei lettori, verbatim
3. Le quattro pieghe
4. L'angolo candidato
5. La verifica sullo scaffale
6. A che punto e' il passo 1b
7. Cosa resta da verificare, in ordine

---

## 1. Da dove si e' partiti, e cosa non si e' potuto guardare

La mossa A di `ricerca-inversa` vuole i contenuti che girano e i commenti
sotto. **Da questo contenitore quelle fonti non sono raggiungibili**, e la
prova e' stata presa prima di scrivere invece di essere data per scontata:

| Fonte | Esito, misurato il 06/09 |
|---|---|
| `reddit.com` (anche `/search.json`, `old.reddit`) | **403** |
| `it.quora.com` | **403** |
| `facebook.com` | **400** |
| commenti TikTok / Instagram / YouTube | home 200, ma i commenti arrivano via JS: niente testo |
| `goodreads.com` | **200**, pagine libro complete |
| `www.amazon.it/dp/<ASIN>` | **200** circa una volta su quattro |
| `www.amazon.it/s` (ricerca) | **503** |
| `www.amazon.it/product-reviews/...` | pagina anti-robot |

Quindi la mossa A e' stata fatta **sul sostituto raggiungibile**: le
recensioni dei lettori sotto i libri concorrenti, su Goodreads. Serve la
stessa funzione — le parole di chi ha letto, e cosa dice che mancava — ma va
detto che e' **piu' debole** della fonte prevista: chi recensisce su Goodreads
ha gia' comprato e finito il libro, mentre il commento sotto un video e' di
qualcuno che il libro non sa nemmeno che esiste. Il campione e' spostato verso
i lettori forti, non verso il mercato.

Ne segue una cosa onesta da dire subito: **il peso di questo documento sta
sulla mossa B**, il niche bending sui dati che il repo ha gia'. La mossa A qui
porta qualche parola vera, non un campione.

## 2. Le parole dei lettori, verbatim

Non si parafrasano: servono cosi' come sono anche a `avatar-cliente` e agli
hook di `promozione-social`.

Sotto **«Basta autosabotaggio!» di Judy Ho** (3,79 su Goodreads, 1.268
valutazioni; su Amazon.it 4,0 con 14 recensioni):

> «no book will do that work for you»

> «listening to the book while remodeling a house is so not the same as
> sitting down with the journal she recommends»

Un lettore lamenta inoltre che l'esempio portante e' quasi sempre la perdita
di peso.

**Il limite di queste citazioni, detto invece che nascosto:** sono in inglese,
perche' Goodreads raccoglie il pubblico dell'originale americano, non quello
dell'edizione italiana. Valgono come segnale sul *libro*, non come voce del
lettore italiano. La voce italiana sta nelle recensioni di Amazon.it, che da
qui non si leggono (§1).

Quello che le due frasi dicono, ed e' poco ma solido: il libro chiede un
lavoro — il quaderno, gli esercizi — **che il lettore non fa**. Non lamenta
che il contenuto sia sbagliato: lamenta che il formato presuppone una
costanza che non ha. Tenere a mente per la piega «uso».

## 3. Le quattro pieghe

### Piega «pubblico» — l'adulto con ADHD

*Stesso dolore, chi altro ce l'ha e nessuno serve?*

Tutti i quindici concorrenti del passo 1 trattano l'autosabotaggio e la
procrastinazione come un problema di **volonta'**: capirsi, decidersi,
resistere. Per un adulto con ADHD non e' un problema di volonta', ed e' la
ragione per cui quei libri gli falliscono addosso uno dopo l'altro.

Cosa dice il repo, senza bisogno di nuove misure:

- ADHD adulti ha **indice di crescita 2,59 con 277.376 visite in dodici mesi**
  (`_profili/note-mercato.md` §2). E' la miglior combinazione crescita+volume
  della tabella dei 26 temi, e la nota lo dice gia' a chiare lettere;
- l'offerta sopra quel tema e' **«o clinico, o strategie generiche»**
  (§3, sei concorrenti, due-tre testi clinici). Fra il manuale diagnostico e
  il libro di consigli generici non c'e' niente;
- l'autocomplete risponde `adhd adulti` e `adhd adulti libro` **per intero**,
  senza nome d'autore attaccato (`dati-angolo.json`).

Su quest'ultimo punto vale la regola gia' costata un errore in questo repo:
**una query senza autore attaccato non e' una query libera**, puo' essere un
titolo cosi' noto da non averne bisogno. Qui non e' stato possibile
controllarlo, perche' la pagina di ricerca risponde 503 — ed e' la prima voce
di §7.

L'avvertenza di `ricerca-inversa` §5 — «la piega pubblico produce spesso
pubblici che non comprano» — **non morde qui**: il pubblico non e' il partner
o il collega di chi ha il problema, e' chi ce l'ha addosso. E' proprio quello
che secondo quella nota compra.

**Regge**, ed e' la piega piu' forte.

### Piega «momento» — la ricaduta, non la partenza

*Stesso pubblico, quale fase non e' coperta?*

Tutta l'offerta vende **l'inizio**: «Liberarsi dall'Autosabotaggio in 21
Giorni», «Come Smettere di Procrastinare», «Prima o poi lo faccio!». Nessuno
dei quindici vende la terza ripartenza — quella di chi quei ventun giorni li
ha gia' cominciati due volte.

L'autocomplete non conosce questa lingua: `come ricominciare dopo aver
mollato` e' **muto a ogni lunghezza di prefisso**, e `come smettere di ri`
porta a `come smettere di rimandare`, che e' di nuovo l'inizio.

**Quello zero non e' una bocciatura, e non e' nemmeno una conferma.**
L'autocomplete indicizza solo cio' che ha volume, e un angolo sta sotto quella
soglia per costruzione (`note-mercato.md` §4). E' lo strumento che ha prodotto
cinque NON SI FA di fila: usarlo per giudicare una piega ne produrrebbe un
sesto per definizione.

**Regge, debolmente**, e da sola non basterebbe.

### Piega «uso» — da aprire, non da leggere

*Come viene usato il libro, non cosa dice.*

E' la piega che `ricerca-inversa` indica come quasi sempre la piu' forte, ed
e' l'unica delle quattro che ha una parola di lettore vera sotto (§2): il
libro chiede un quaderno e degli esercizi, e il lettore non li fa.

Tutti e quindici i concorrenti sono libri **da leggere dall'inizio alla
fine**, spesso in forma di percorso a giorni. Quello che non esiste e' il
libro **da aprire nel momento in cui stai per mollare** — consultazione a
strappo, tre pagine, nessun percorso da riprendere da dove si era interrotto.

E si incastra con la piega «pubblico» invece di sommarcisi: non finire un
percorso di ventun giorni **e' il disturbo**, non il fallimento del lettore.
Un libro in ventun giorni venduto a un adulto con ADHD e' un libro che chiede
al lettore proprio la cosa che non riesce a fare.

**Regge.**

### Piega «angolo» — l'ambiente invece del carattere

*Di cosa parlano tutti, e cosa resta fuori?*

Parlano tutti di mentalita', motivazione, credenze limitanti. Resterebbe fuori
l'autosabotaggio come problema di **progettazione della giornata** — l'ambiente
che rende il comportamento difficile, non il carattere che lo produce.

Ma il posto e' meno vuoto di quanto sembri: `Gestione Del Tempo e
Procrastinazione` di Leonardo Parodi sta gia' li', e la produttivita' in
italiano e' un reparto affollato per conto suo.

**Non regge da sola.** Resta buona come materiale di un capitolo.

## 4. L'angolo candidato

> Per l'adulto con ADHD — diagnosticato o che se lo sospetta — che ha gia'
> provato i libri sulla procrastinazione e li ha mollati a meta': un libro
> fatto per essere **aperto nel momento in cui stai per mollare**, non letto
> dall'inizio alla fine. Non ventun giorni: tre pagine, adesso.

Tre pieghe su quattro, nella stessa riga: **pubblico** (ADHD adulto),
**momento** (la ricaduta), **uso** (consultazione invece di percorso).

## 5. La verifica sullo scaffale

`ricerca-inversa` §4 dice che questa verifica non e' saltabile. E' stata fatta
**a meta'**, e la meta' che manca e' quella che conta.

### Cosa si e' potuto misurare: quanto pesa davvero lo scaffale del passo 1

Numeri nuovi, presi il 06/09 da `www.amazon.it/dp/<ASIN>` con
`sonda_angolo.py`. Il file `dati-angolo.json` e' generato: se diverge da
questa tabella, ha ragione il file.

Sono un'istantanea, non una serie: il conteggio di Wiest e' passato da 1.204 a
1.206 fra due letture della stessa sera. Servono a distinguere dieci
recensioni da milleduecento, non a seguire un andamento — per quello servirebbe
il BSR, che da qui non si legge.

| ASIN | Titolo | Voto | Recensioni su Amazon.it |
|---|---|---:|---:|
| `8845410048` | Wiest, *La montagna sei tu* | 4,4 | **1204** |
| `8804582677` | Giacobbe, *Come smettere di fare la vittima* (Mondadori) | 4,4 | 59 |
| `885901753X` | Ramirez Basco, *Prima o poi lo faccio!* | 4,5 | 32 |
| `885902420X` | Ho, *Basta autosabotaggio!* | 4,0 | **14** |
| `8880934449` | Pradervand, *Mai piu' vittima* | 3,8 | **10** |
| `8844048035` | Krech, *L'arte di passare all'azione* | — | HTTP 500 su 8 tentativi |

L'ASIN in prima colonna non e' arredamento: e' il legame con
`dati-angolo.json`, e `test_report_dati.py` lo usa per controllare a ogni push
che questi numeri siano ancora quelli dei dati.

**Questo cambia la lettura del passo 1, e va scritto.** Il report di nicchia
concludeva «quindici concorrenti, con tre bestseller da editore in cima ai tre
sotto-temi», e aggiungeva che il verdetto non dipendeva dai numeri mancanti.
I numeri adesso ci sono, e dicono una cosa diversa: **c'e' un gigante e ci
sono quattro libri sottili.** Wiest ha milleduecento recensioni; le tre ancore
editoriali restanti stanno fra dieci e cinquantanove, cioe' allo stesso
livello dei pen name KDP.

Non ribalta il NON SI FA sul tema — chi entra sull'autosabotaggio generico
entra contro Wiest. Ma smonta il «tre bestseller da editore»: sul sotto-tema
vittimismo l'ancora Mondadori ha 59 recensioni, e su procrastinazione la
migliore ne ha 32. **Era una conclusione che decideva un investimento, ed e'
stata verificata da un secondo angolo solo adesso.**

### Cosa NON si e' potuto misurare, ed e' il punto

Le tre domande di `ricerca-inversa` §4, una per una:

1. **Esiste gia' un libro su quell'angolo?** — *non si sa.* Serve cercare
   «adhd adulti», «procrastinazione adhd», «adhd donne» sulla ricerca di
   Amazon.it, che da qui risponde 503. **E' la domanda che decide, ed e'
   aperta.**
2. **Se non esiste, c'e' un motivo?** — parzialmente risposto: il tema e' in
   crescita e ha volume, quindi non e' un pubblico che non esiste. Resta da
   escludere che sia un pubblico che compra manuali clinici invece che libri
   pratici.
3. **Il pubblico regge un titolo?** — 277.376 visite in dodici mesi su
   it.wikipedia dicono di si' sul tema. Non dicono nulla sull'angolo.

Manca inoltre, per tutti: **BSR, andamento delle recensioni, prezzi.** La
pagina prodotto raggiungibile da qui e' una versione leggera che non li porta,
e `product-reviews` risponde anti-robot.

## 6. A che punto e' il passo 1b

**Chiuso il 06/09 sera con NON SI FA sull'angolo.** La verifica che mancava e'
stata fatta: `scaffale-adhd-adulti.md`, quattordici titoli dalla prima pagina
di Amazon.it.

Il conteggio che questo documento chiedeva — «quanti clinici, quanti pratici»
— e' tornato **1 clinico e 10 pratici per l'adulto che ce l'ha addosso**. La
piega «pubblico» poggiava sul fatto che fra il manuale clinico e il consiglio
generico non ci fosse niente: c'e' tutto, ed e' li' che stanno tutti. Il
sotto-angolo della procrastinazione ha gia' il suo libro, *IL METODO ADHD: 30
giorni*.

Il verdetto e' scritto per esteso in `scaffale-adhd-adulti.md` §5, con una
condizione fissata prima di conoscere i numeri delle recensioni, e in §6 c'e'
l'errore di metodo che l'ha reso possibile.

**Quello che segue e' il testo com'era prima della verifica**, e resta perche'
serve piu' cosi' che corretto: e' il ragionamento che sembrava solido e che lo
scaffale ha smentito.

### Com'era scritto qui prima del 06/09 sera

**In corso — verifica sullo scaffale mancante.** Non e' un SI FA e non e' un
NON SI FA, e la differenza non e' formale.

`regia` §3: «L'angolo trovato nei commenti resta un'ipotesi finche' non e'
verificato sullo scaffale — quella verifica e' dentro il passo 1b e non si
salta.» Qui l'ipotesi c'e' ed e' motivata su tre pieghe; la verifica no.
Scrivere SI FA adesso vorrebbe dire far partire l'avatar su un angolo di cui
nessuno ha guardato lo scaffale — cioe' esattamente l'errore che questa
disciplina esiste per evitare, un piano piu' avanti.

Il passo 2 non parte. Manca una cosa sola, e sono venti minuti.

## 7. Cosa resta da verificare

~~Lo scaffale «adhd adulti»~~ — **fatto il 06/09 sera**, ed e' quello che ha
chiuso l'angolo. Vedi `scaffale-adhd-adulti.md`.

Resta **una cosa sola**, ed e' la condizione scritta in
`scaffale-adhd-adulti.md` §5: il numero di recensioni dei tre titoli piu'
recensiti della lista. Sotto le 30 recensioni ciascuno lo scaffale e' sottile
e l'angolo torna in discussione; a 30 o piu' anche per uno solo, il NON SI FA
e' definitivo.

Non e' una scappatoia lasciata aperta: e' la stessa cautela che il 06/09 ha
corretto una conclusione gia' scritta nell'altra direzione
(`note-mercato.md` §3-bis). Finche' quel dato non c'e', l'angolo e' chiuso.

Le altre due voci che stavano qui **non hanno piu' un motivo**: se `adhd
adulti` sia un titolo non cambia niente ora che si e' visto lo scaffale, e le
recensioni negative dei concorrenti erano materia prima della fase 2, che non
parte.

---

*Dati grezzi: `dati-angolo.json`, generato da `sonda_angolo.py` — non si
modifica a mano.*
