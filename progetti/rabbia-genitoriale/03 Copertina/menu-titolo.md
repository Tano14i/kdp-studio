# Titolo, sottotitolo, copertina — il menu
Passo 4 · **Checkpoint 2** · 07/09/2026

Il sistema propone, l'autore sceglie. Niente e' deciso finche' non c'e' una
riga scritta con la data.

---

## 1. Cosa dice l'autocomplete, prima di inventare qualunque titolo

`pubblicazione-kdp` §1: mai a intuito. Sondate 14 frasi candidate su
`completion.amazon.it` (`dati-lingua-titolo.json`, generato).

**Tornano intere, cioe' hanno domanda indicizzata:**

| Frase | Padrone? |
|---|---|
| `mio figlio non mi ascolta` | **SI'** — e' un titolo |
| `farsi ascoltare dai figli` | **SI'** — e' il sottotitolo di Naumburg, piu' altri quattro |
| `educare senza urlare` | **SI'** — torna con «moreno marchetti» attaccato |
| `disciplina positiva` | no, ma e' il nome della categoria: lo usano tutti |
| `capricci bambini` | no |

**Non hanno domanda indicizzata** (utile saperlo, non usarle come chiave):
`genitori che urlano`, `perdere la calma`, `ho perso la pazienza`,
`crisi di rabbia bambini`, `bambini che non ubbidiscono`.

### Le due trappole scattate, ed e' la terza volta

`mio figlio non mi ascolta` sembrava perfetto: la domanda del lettore, con
volume, senza autore attaccato. **E' il titolo di Sabrina Salmaso**, *Mio Figlio
Non Mi Ascolta!: La Soluzione In 6 Semplici Mosse*, serie «Risposte
Pedagogiche». C'e' anche *Mio figlio non ascolta mai!* di BC Brain Children.

`farsi ascoltare dai figli` idem: e' Naumburg parola per parola, e sotto ci
stanno altri quattro titoli.

*Una query senza autore attaccato non e' una query libera.* La regola e' in
`note-mercato.md` §6, e oggi ha impedito di stampare in copertina il titolo di
qualcun altro.

## 2. Sei concorrenti nuovi, trovati mentre si cercava altro

| ASIN | Titolo | Voto | Recensioni |
|---|---|---:|---:|
| `8804728728` | Faber e Mazlish, *Come parlare perche' i bambini ti ascoltino* (Mondadori) | 4,6 | **1533** |
| `B0CB4WYYFY` | Mamma Sophia, *Educare Senza Urlare: Tecniche Efficaci* | 5,0 | 32 |
| `B0DM9NCJGV` | Panozzo, *ORA BASTA!* | 4,4 | 9 |

Piu' tre non misurabili da qui (HTTP 500): Salmaso *Mio Figlio Non Mi
Ascolta!*, Bacus *100 modi per farsi ascoltare senza urlare ne' minacciare*,
Poulhalec *12 strumenti per farsi ascoltare dai bambini*.

**Faber e Mazlish con 1.533 recensioni e' il vero gigante di questo scaffale**,
e nessuno dei nostri documenti lo aveva. E' il quarto conteggio di questa
nicchia che risulta per difetto. Non cambia il concept — quel libro insegna a
parlare, non dice cosa fare al decimo tentativo — ma cambia con chi ci si
confronta in copertina: **la nostra deve reggere accanto a un classico**, non
solo accanto ai pen name.

Da segnalare per il futuro: Bacus promette «le strategie e le parole che
funzionano **anche con i bambini piu' oppositivi**». E' il titolo piu' vicino
al nostro territorio fra tutti quelli visti. Va misurato prima dell'outline.

## 3. Quattro titoli, con il collaudo a 200 px

Nessuno usa `educare senza urlare`, `mio figlio non mi ascolta` o `farsi
ascoltare dai figli`: sono occupati.

### T1 — **Piano B**
> **Piano B**
> *Cosa fare con tuo figlio quando il metodo gentile non ha funzionato.
> 30 situazioni vere, dalla decima volta in poi.*

**Regge:** sei lettere. A 200 px e' l'unico dei quattro che si legge senza
sforzo. Dice il concept senza accusare nessuno — non dice che gli altri
sbagliano, dice che questo viene dopo. In questa nicchia non lo usa nessuno.
**Non regge:** «Piano B» da solo non si cerca. Tutta la scoperta la fa il
sottotitolo, e in italiano «piano» e' ambiguo (piano = lentamente, o il piano
di una casa).

### T2 — **Ho gia' provato tutto**
> **Ho gia' provato tutto**
> *Il libro per i genitori che hanno letto gli altri libri e alla decima volta
> hanno urlato lo stesso.*

**Regge:** e' la voce del lettore, in prima persona. Chi si riconosce lo compra
senza leggere altro. Ed e' l'unico che dichiara apertamente di venire **dopo**
gli altri libri — coerente con A2 stretto e con B5-a.
**Non regge:** quattro parole in copertina, e a 200 px il sottotitolo sparisce.
«Provato tutto» puo' leggersi come resa invece che come punto di partenza.

### T3 — **Alla decima volta**
> **Alla decima volta**
> *Cosa fare quando hai chiesto con calma nove volte e tuo figlio non ti
> ascolta ancora.*

**Regge:** viene dalle parole esatte di un lettore vero («Alla decima volta che
non ottieni comunque nulla cosa resta da fare?»). Specifico e memorabile. Il
sottotitolo contiene «non ti ascolta», che e' lingua indicizzata, **senza
copiare il titolo di Salmaso**.
**Non regge:** non contiene ne' «urlare» ne' «capricci», quindi la scoperta
dipende interamente dal sottotitolo e dalle sette parole chiave. Tre parole in
copertina si leggono a 200 px, ma non dicono di cosa parla il libro.

### T4 — **E adesso che ho urlato**
> **E adesso che ho urlato**
> *I dieci minuti dopo: cosa dire, cosa fare, come si rimette a posto.*

**Regge:** e' l'unico che nomina l'urlo — la lingua del reparto — senza dire
«senza urlare» o «smettere di urlare», che sono di altri. Occupa un momento
preciso e riconoscibile.
**Non regge, e va detto:** e' **fuori dal concept scelto**. A2 stretto sta al
decimo tentativo, cioe' *prima* dell'urlo; questo titolo vende il *dopo*
l'urlo, che era la formulazione superata del 06/09 pomeriggio. Restringe il
libro a un sottoinsieme di se stesso. In lista per far vedere il campo.

### Il collaudo, fatto a mente e da rifare sull'immagine vera

`pubblicazione-kdp` §4 pretende la riduzione a 200 px di altezza, e va fatta
**sul file**, non sulla descrizione. A occhio: T1 sopravvive intero, T3
sopravvive, T2 e T4 perdono il sottotitolo. Da verificare quando esiste la
copertina.

## 4. La riga dell'autore — B5-a

Confermato il 07/09: chi firma **e' un genitore** che ha attraversato quello
che il libro racconta. Quindi la riga puo' esistere ed essere vera.

Due forme, e la seconda e' piu' rischiosa e piu' forte:

**A · discreta** — solo il nome sul fronte. La dichiarazione («non sono una
psicologa, sono un genitore che quei libri li ha comprati e provati») sta in
quarta e nell'introduzione.

**B · dichiarata sul fronte** — una riga sotto il sottotitolo:
> *Scritto da un genitore, non da un esperto.*

**Perche' B potrebbe funzionare qui piu' che altrove:** e' l'esatto contrario
dell'accusa che affonda il piu' venduto della nicchia — «una certa Letizia
Merini che in pratica non esiste», «fate almeno una ricerca sulla persona che
lo ha scritto». Dichiararlo in copertina toglie la domanda prima che nasca.
**Perche' potrebbe non funzionare:** i lettori di Petrucciani comprano *la
dottoressa*. Su quello scaffale «non sono un'esperta» puo' leggersi come «non
so di cosa parlo».

**Il pen name non e' deciso** (il dossier dice «pen name da decidere») e non lo
decido io: con B5-a il nome deve essere uno dietro cui c'e' davvero qualcuno.

## 5. La copertina

### Il principio, prima delle misure

`pubblicazione-kdp` §4: si guardano le copertine dei concorrenti in una lista
di risultati, e la leggibilita' in miniatura viene prima dell'atmosfera.

**Ne ho viste tre**, dalla ricerca `senso di colpa genitori`: *Genitori liberi*
(turchese, illustrazione piatta), *La colpa non e' dei genitori* (beige e
grigio, sedia e ombra, taglio letterario), *Genitori senza sensi di colpa*
(azzurro pallido, foto di bambino). **Tre non sono un campione**, e una
scansione vera si fa dal browser dell'autore su `educare senza urlare`.

Quello che si vede gia': **il reparto e' chiaro, pastello, illustrato.** Se la
scansione lo conferma, la strada e' il contrario — fondo scuro pieno, tipografia
grande, nessuna illustrazione — e a 200 px vincerebbe da sola. Da confermare
prima di disegnare.

### Le misure, calcolate e mai stimate

Formato D2, tascabile: **12,7 × 20,32 cm** (5 × 8 pollici).

```
dorso            = pagine × 0,002252"        (carta bianca)
larghezza totale = 2 × 5" + dorso + 0,25"    (0,125" di abbondanza per lato)
altezza totale   = 8" + 0,25"
area sicura      = 0,25" dentro il rifilo
codice a barre   = 2 × 1,2" in basso a destra della quarta, lasciato vuoto
```

Con 96 pagine: dorso 0,2162" · tela **10,4662 × 8,25"**.

**Questo numero e' provvisorio e va rigenerato dal PDF vero.** `regia` §10: la
foliazione si estrae dall'artefatto con uno script, non si scrive a mano. 96
pagine e' il centro dell'intervallo D2, non un dato.

### La divisione del lavoro

Il generatore fa la texture, **lo script fa tutto cio' che ha una misura**:
titolo, dorso, aree sicure, posizioni, composti in PIL sulla tela esatta. Un
generatore di immagini non sa scrivere e non sa contare.

---

## La casella

```
Titolo:        T_
Riga autore:   A oppure B
Pen name:      ____________________
```

Dopo la scelta si scrivono `decisioni/02-copertina.md` con le alternative
scartate e il motivo, e si passa al passo 5, l'outline — checkpoint 3.

**E qui il libro puo' ancora morire a costo zero.** E' l'ultimo momento in cui
costa una giornata invece di tre mesi.
