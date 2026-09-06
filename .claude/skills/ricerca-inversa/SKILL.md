---
name: ricerca-inversa
description: "Cerca l'angolo libero invece del tema libero. Parte dai contenuti che girano e dai commenti sotto, risale alla domanda che nessun libro ha ancora risposto, e piega un tema occupato su un pubblico o un momento scoperti. Usa quando ricerca-nicchia ha chiuso con NON SI FA, o prima di scegliere una nicchia da zero."
version: 0.1.0
argument-hint: "ricerca-inversa \"<tema o progetto chiuso>\" [--mercato it]"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch]
---

## Il muro che questa skill esiste per aggirare

`_profili/note-mercato.md` §1, scritto dopo cinque misurazioni:

> **Cinque temi verificati, cinque volte occupato.** Non è sfortuna nella
> scelta dei temi. È la struttura del mercato: la saggistica pratica italiana
> su Amazon è stata sistematicamente coltivata. **Un tema libero, in questo
> mercato, non esiste.** Chi lo cerca continuerà a trovare NON SI FA, al ritmo
> di una giornata per tentativo.

La conclusione è giusta e la ricerca che l'ha prodotta è fatta bene. Il
problema è la domanda: `ricerca-nicchia` chiede **«questo tema è libero?»**, e
in questo mercato la risposta è no per costruzione.

Questa skill fa una domanda diversa: **«dentro questo tema occupato, quale
angolo è scoperto?»** — che è una domanda a cui, a differenza dell'altra, si
può rispondere sì.

Non sostituisce `ricerca-nicchia`. Le cambia il punto di partenza e ne
riceve il verdetto quando è negativo.

## Usa quando

- `ricerca-nicchia` ha chiuso con **NON SI FA** — e allora questa skill è il
  passo successivo, non la fine del progetto.
- Si deve scegliere una nicchia da zero e si vuole evitare il giro di
  NON SI FA a un giorno l'uno.
- Un tema ha domanda misurata (`note-mercato.md` §2) ma scaffale pieno.

## NON per

- Confermare un'idea che l'autore ha già deciso. Questa skill cerca, non
  giustifica.
- Sostituire la misura dell'offerta. L'angolo trovato qui **va comunque
  verificato su Amazon** prima di scrivere: vedi §4.

## 1. Le due mosse

Sono due, e nell'ordine. La prima trova candidati, la seconda li rende
difendibili.

### Mossa A — la ricerca inversa

Si parte dai contenuti, non dallo scaffale.

Il ragionamento normale è: *scelgo un tema → guardo su Amazon se è libero →
scrivo.* Fallisce perché lo scaffale è pieno ovunque.

Il ragionamento inverso è: *guardo cosa sta già facendo fermare le persone →
leggo la domanda che si fanno nei commenti → verifico se quella domanda ha già
un libro.* Amazon smette di essere il punto di partenza e diventa il test
finale.

**Dove si guarda** — TikTok e Instagram per i contenuti, i commenti sotto; i
gruppi Facebook di nicchia; le discussioni Reddit italiane; le domande sotto
i video YouTube lunghi. Mai Amazon in questa fase.

**Cosa si cerca, in ordine:**

1. **I contenuti fuori scala.** Non quelli buoni: quelli che hanno numeri
   molto sopra la media dell'account che li ha pubblicati. Un creator con
   duemila follower e un video da centomila visualizzazioni ha toccato un
   nervo che lui stesso non sapeva di avere.
2. **I commenti sotto, non il contenuto.** È lì che sta il materiale. Il
   contenuto dice cosa interessa; i commenti dicono **cosa manca**.
3. **Le domande che si ripetono** sotto contenuti di autori diversi. Una
   domanda posta a tre creator diversi non è curiosità di una persona: è un
   buco.
4. **Le richieste esplicite** — «avete un libro su questo?», «dove posso
   approfondire?», «e per chi invece…». Sono la forma più diretta di domanda
   inevasa che esista, e nessuno le conta.

**Il passaggio che conta** è da «questo contenuto tira» a «questa è la
domanda». Un contenuto che va bene non è una nicchia: è un contenuto. La
nicchia è la domanda ripetuta sotto, formulata come la formulerebbe chi la
fa — con le sue parole, non con le tue.

### Mossa B — il niche bending

Si prende un tema con domanda misurata e scaffale pieno, e invece di
abbandonarlo lo si piega.

Quattro pieghe possibili, da provare tutte e quattro:

| Piega | Domanda | Esempio dal repo |
|---|---|---|
| **Pubblico** | stesso dolore, chi altro ce l'ha e nessuno serve? | endometriosi: i partner, i genitori, i datori di lavoro |
| **Momento** | stesso pubblico, quale fase non è coperta? | endometriosi: prima della diagnosi, non dopo |
| **Uso** | come viene usato il libro, non cosa dice | «da portare in visita» invece di «da leggere» |
| **Angolo** | di cosa parlano tutti, e cosa resta fuori? | endometriosi: sette su nove parlano di alimentazione |

**Il caso di scuola è già nel repo.** Da
`progetti/endometriosi/00-dossier-metodo.md`:

> Sette libri su nove parlano di alimentazione. Il vuoto, se c'è, non è il
> tema ma l'angolo: diagnosi, lavoro, coppia, dolore quotidiano fuori dai
> pasti.

Quella riga è già un niche bending completo, scritto senza sapere di farlo.
Questa skill esiste per farlo di proposito ogni volta, invece che per
intuizione una volta su cinque.

**La piega più forte è quasi sempre «uso».** Le altre tre cambiano di chi si
parla; questa cambia cosa il libro *fa* per chi lo compra, ed è la più
difficile da imitare per un concorrente che sta già vendendo — perché per
copiarla dovrebbe rifare il libro, non aggiungerci un capitolo.

## 2. Il verdetto cambia oggetto

`ricerca-nicchia` emette un verdetto sul **tema**. Questa skill lo emette
sull'**angolo**, e sono due cose diverse.

| | `ricerca-nicchia` | `ricerca-inversa` |
|---|---|---|
| domanda | il tema è libero? | quale angolo è scoperto? |
| parte da | lo scaffale Amazon | i contenuti e i commenti |
| NON SI FA vuol dire | il tema è occupato | nessuna delle quattro pieghe regge |
| Amazon serve a | trovare il vuoto | **verificare** il vuoto trovato altrove |

Un **NON SI FA sul tema non chiude più il progetto**: lo manda qui. Si chiude
solo se anche l'angolo non regge — e allora il no è molto più solido di prima,
perché sono state provate quattro pieghe invece di zero.

## 3. Il documento

`01b-angolo.md`, accanto a `01-nicchia.md`, con la data:

1. **da dove si è partiti** — contenuti visti, fonte, giorno
2. **le domande ripetute**, con le parole esatte di chi le fa
3. **le quattro pieghe provate**, ognuna con il motivo per cui regge o no
4. **l'angolo candidato**, in una riga
5. **la verifica su Amazon** — vedi §4
6. **il verdetto sull'angolo**, con i numeri accanto
7. **cosa resta da verificare**

Le parole esatte raccolte al punto 2 non servono solo qui: sono materia prima
per `avatar-cliente` e per gli hook di `promozione-social`. Non si
parafrasano mai.

## 4. La verifica, che non è saltabile

Un angolo trovato nei commenti è un'ipotesi, non un mercato. Va verificato
sullo scaffale prima di scrivere, ed è l'unico momento in cui si torna su
Amazon.

Tre domande, con i numeri:

1. Esiste già un libro **su quell'angolo**, non su quel tema?
2. Se non esiste: c'è un motivo per cui nessuno l'ha fatto? Un pubblico che
   non compra libri è un vuoto che resta vuoto.
3. Il pubblico dell'angolo è abbastanza grande da reggere un titolo?

**Da questo contenitore Amazon non è raggiungibile.** Il proxy blocca
`amazon.it` (403 sul CONNECT, verificato il 06/09/2026, anche su
`completion.amazon.it`), e prima ancora l'IP di datacenter prendeva 503 —
`scheda-raccolta.md` §1. La verifica si fa dal browser dell'autore, con quella
scheda. La strada automatica è chiusa e documentata come chiusa: non
ritentarla.

## 5. Dove questa skill sbaglia

Va letto prima di fidarsi di un risultato.

- **Un contenuto virale non è un mercato.** Le persone si fermano su cose per
  cui non pagherebbero mai. È il difetto strutturale della mossa A, e la §4
  esiste per questo: senza la verifica, questa skill produce entusiasmo.
- **I commenti sono un campione distorto.** Commenta chi ha molto da dire, non
  chi compra. Una domanda ripetuta da tre persone su un video da centomila
  visualizzazioni non è una domanda di massa.
- **La piega «pubblico» produce spesso pubblici che non comprano.** I partner,
  i genitori, i colleghi di qualcuno hanno il problema ma non lo cercano su
  Amazon: lo cerca chi ce l'ha addosso. Va verificata più delle altre tre.
- **Il metodo è ricostruito, non ricevuto.** Le due mosse sono la
  ricostruzione di due tecniche note per nome — «ricerca inversa» e «niche
  bending» — di cui questa skill non ha visto il materiale originale. Quello
  che c'è scritto qui regge o cade sui risultati che produce, non sulla
  fonte.
- **Non risolve un libro che non interessa a nessuno.** Se le quattro pieghe
  non reggono, il no va scritto e il progetto va chiuso, come faceva
  `ricerca-nicchia`. Questa skill aggiunge quattro tentativi prima del no, non
  toglie il no.

## 6. Chi la chiama

`regia`, in due punti:

- **prima del passo 1**, quando si parte da zero e si vuole scegliere il tema
  dai contenuti invece che dallo scaffale;
- **dopo un NON SI FA** del passo 1, come passo 1b, prima di chiudere il
  progetto.

Vedi `regia` §2 e §3.
