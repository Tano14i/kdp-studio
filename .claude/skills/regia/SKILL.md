---
name: regia
description: "Dirige un progetto libro dall'inizio alla promozione: legge il dossier, capisce a che punto siamo e chiama la skill giusta al momento giusto, fermandosi ai sette checkpoint. Un NON SI FA sulla nicchia apre ricerca-inversa invece di chiudere il progetto, e la pubblicazione non e' l'ultimo passo: dopo c'e' promozione-social. Usa per avviare o riprendere un libro."
---

# Regia

Questa skill non fa il lavoro: decide **chi lo fa e quando**, si ferma dove
deve decidere l'autore, e tiene il conto di cosa manca. Vale per un libro, e la
stessa disciplina regge qualunque progetto lungo.

## 1. La prima cosa, sempre

All'invocazione, prima di qualsiasi proposta:

1. cerca `00-dossier-metodo.md` nella cartella del progetto
2. **se non c'è**: è un libro nuovo → invoca `progetto-libro` per creare
   cartella, convenzioni e dossier, poi riparti da qui
3. **se c'è**: leggi la tabella di stato e l'elenco «cosa manca» in fondo
4. di' in tre righe a che punto siamo e qual è il prossimo passo
5. esegui quel passo, e uno solo

Mai proporre l'intero piano e chiedere da dove partire: il dossier lo sa già.
Mai saltare avanti perché un passo successivo sembra più interessante.

## 2. La mappa

Quattro fasi. La colonna «chi lo fa» è la skill da invocare.

| # | Passo | Chi lo fa | Checkpoint |
|---|---|---|---|
| 0 | Cartella e convenzioni | `progetto-libro` | — |
| 1 | Nicchia e concorrenti | `ricerca-nicchia` | **verdetto** |
| 1b | Angolo, se il tema è occupato | `ricerca-inversa` | **verdetto** |
| 2 | Avatar cliente | `avatar-cliente` | — |
| 3 | Concept e positioning | `concept-positioning` | **1** |
| 4 | Titolo, sottotitolo, copertina | `pubblicazione-kdp` §4 | **2** |
| 5 | Outline | `outline-libro` | **3** |
| 6 | DNA stilistico | `dna-stilistico` | **4** |
| 7 | Campione di scrittura | `dna-stilistico` | **5** |
| 8 | Manoscritto | in conversazione, sotto outline e DNA | — |
| 9 | Revisione | `revisione-manoscritto` | — |
| 10 | Interni impaginati | in conversazione (vedi §6) | — |
| 11 | Immagini, copertina finita | `higgsfield-kdp-book` | — |
| 12 | Scheda, A+, campagne | `pubblicazione-kdp` | **6** e **7** |
| 13 | Traduzione e mercati | in conversazione (vedi §6) | — |
| 14 | Promozione social | `promozione-social` | — |

**L'ordine non è un'opinione.** Due punti si sbagliano sempre:

- **la copertina viene prima della scrittura**, non dopo. È la promessa del
  libro, ed è l'ultimo momento in cui il libro può morire a costo zero.
  Bocciare un'idea in tre giorni costa meno che scoprirlo dopo tre mesi
- **il campione approvato viene prima del manoscritto.** Meglio correggere
  cinque pagine che riscriverne duecento

**Il passo 14 non è facoltativo.** Su Amazon.it la saggistica pratica è
occupata (`_profili/note-mercato.md` §1): una scheda nuova non emerge dalla
ricerca interna, e un libro pubblicato senza traffico da fuori non viene
scoperto. La mappa finiva al 13 e quello era un buco, non una scelta.

## 3. Il verdetto della nicchia è un cancello

`ricerca-nicchia` chiude con un verdetto a tre valori, e la regia lo rispetta
prima di chiamare qualunque altra skill:

- **SI FA** → si prosegue con l'avatar
- **DA VERIFICARE** → si prende il dato che manca, e basta. Non si passa
  all'avatar «intanto che ci siamo»
- **NON SI FA** → **non si chiude più qui: si passa al 1b**, `ricerca-inversa`.
  Il verdetto negativo riguarda il *tema*, e in questo mercato un tema libero
  non esiste per costruzione. Prima di chiudere si prova a piegarlo: quattro
  pieghe, e solo se non regge nessuna il progetto si ferma davvero. Allora sì
  si scrive il motivo nel dossier e si chiude — e quel no vale molto di più,
  perché sono stati provati quattro angoli invece di zero

Se il verdetto manca, o non ha numeri accanto, il passo 1 non è finito —
comunque sia scritta la riga nella tabella di stato.

**Il 1b ha il suo cancello, sullo stesso schema.** `ricerca-inversa` emette un
verdetto sull'**angolo**, non sul tema: SI FA apre l'avatar, NON SI FA chiude
il progetto per davvero. L'angolo trovato nei commenti resta però un'ipotesi
finché non è verificato sullo scaffale — quella verifica è dentro il passo 1b
e non si salta.

**Si può entrare dal 1b anche partendo da zero**, prima del passo 1, quando si
vuole scegliere il tema dai contenuti che girano invece che dallo scaffale.
In quel caso l'ordine è 1b → 1, e il passo 1 diventa la verifica dell'angolo
invece della ricerca del tema.

La tabella degli ASIN prodotta qui viene riusata due volte: da `avatar-cliente`,
per sapere quali recensioni leggere, e da `pubblicazione-kdp`, per il targeting
delle campagne. Non si rifà.

## 4. Come si chiama una skill

Una alla volta, e solo quando la sua precondizione è soddisfatta.

**Precondizione** — prima di invocare, verifica che esista il file del passo
precedente. `outline-libro` senza il documento dell'avatar produce un indice
sull'argomento invece che sul lettore, che è esattamente l'errore che quella
skill esiste per evitare. Se il file manca, non improvvisare: torna indietro di
un passo.

**Consegna** — passa alla skill solo i documenti che le servono, per nome. Per
fare la copertina non serve il manoscritto, e infatti non si apre.

**Chiusura** — un passo è finito quando ha lasciato il suo file e la riga
nella tabella di stato è aggiornata. Non quando la risposta è arrivata in chat.

## 5. I sette checkpoint

Un checkpoint è una cosa sola: **il lavoro si ferma e aspetta l'autore.** Non
può andare avanti finché non ha scelto, e la scelta resta scritta con la data.

1. **Concept e positioning** — che libro sarà, per chi, con che promessa
2. **Copertina** — titolo, sottotitolo, e come si presenta
3. **Outline** — cosa entra, cosa resta fuori, in che ordine
4. **DNA stilistico** — come deve suonare, e le parole da non usare mai
5. **Campione di scrittura** — il via libera al manoscritto
6. **Traduzione** — quali mercati, con che registro
7. **Marketing** — come si presenta al mondo il giorno del lancio

A ogni checkpoint si presentano **più opzioni, non una**, e accanto a quella
scelta restano scritte le scartate con il motivo. Quelle scelte sono il lavoro
creativo dell'autore: sono la ragione per cui il libro è suo.

Se l'autore non risponde, il progetto si ferma. Per costruzione, non per
cortesia.

## 6. I passi senza skill

Due passi non hanno ancora una skill. Vanno fatti in conversazione, con la
stessa disciplina, e ognuno lascia comunque il suo file:

- **interni impaginati** — il PDF di stampa e la sua verifica su tutte le
  pagine
- **traduzione e mercati** — la domanda non è quanto costa tradurre, ma se il
  vuoto che si sfrutta esiste anche lì

Quando uno di questi torna una seconda volta, è il momento di trasformarlo in
skill invece di rifarlo a mano. È esattamente così che sono nate
`ricerca-inversa` e `promozione-social`: erano due buchi della mappa, non due
passi in conversazione.

## 7. La finestra di contesto

Più contesto non vuol dire meglio. Troppo poco dà risposte generiche; troppo fa
dimenticare le regole di prima e comincia a inventare. La zona giusta si tiene
così:

- **ogni documento del progetto si apre con un indice**, così si leggono i
  titoli e si apre solo il pezzo che serve, come in una libreria
- **ogni passo apre solo i documenti della sua precondizione**
- **le decisioni già prese non si rispiegano**: stanno scritte, si rileggono

Una finestra pulita non è un dettaglio tecnico. È la differenza tra un libro
che sta in piedi e uno che si sfalda a metà.

## 8. Ogni passo lascia un file, numerato

`00-dossier-metodo.md`, `01-nicchia.md`, `02-avatar.md`, `03-concept.md`,
`04-copertina.md`, `05-outline.md`… Il numero è l'ordine di esecuzione, e serve
a vedere i buchi a colpo d'occhio.

Una decisione presa e non scritta è una decisione che verrà presa di nuovo, in
modo diverso, fra tre giorni. Scrivi anche quelle piccole: **perché** un numero
è cambiato vale più del numero.

## 9. Il dossier apre con una tabella di stato

| # | Passo | Stato | Dove sta |
|---|---|---|---|
| 1 | … | eseguito / **da fare** | nome del file |

Gli stati onesti sono tre: *eseguito*, *eseguito ma non scritto*, *da fare*.
Il secondo è quello che salva il progetto: è il passo che credi fatto e che
non esiste in nessun file.

In fondo, un elenco «cosa manca, in ordine», con barrate le voci chiuse. È la
prima cosa da leggere quando si riprende dopo una pausa, ed è quello che questa
skill legge per prima all'avvio.

## 10. Le specifiche si generano dal prodotto

Una specifica scritta a mano e un prodotto costruito da uno script divergono
sempre, e in silenzio. La foliazione, l'elenco dei file, le misure: si
**estraggono dall'artefatto** con uno script e si scrivono in un file marcato
come generato.

Su un libro di 154 pagine il piano diceva «indice su una pagina, schede vuote
su sei»; il PDF aveva l'indice su due e le schede su due. Il totale tornava
pari, quindi nessun controllo protestava. L'ha trovato solo la lettura del PDF
vero, pagina per pagina.

**Quando il piano e l'artefatto non concordano, ha ragione l'artefatto.** Poi
si decide: correggere l'artefatto o correggere il piano. Mai lasciarli diversi.

## 11. La verifica copre tutto, mai un campione

Controllare quattro pagine su centocinquanta e dichiarare fatto è il modo in
cui un libro intero finisce stampato con il markdown grezzo in vista. È
successo.

Ogni verifica automatica: passa su **tutti** gli elementi, esce con codice
diverso da zero se qualcosa non va, e stampa cosa ha controllato — così si
legge in tre righe invece di rileggere il prodotto.

Ogni vincolo di posizione si scrive come `assert`, non come speranza. Un assert
che scatta costa dieci secondi; lo stesso errore trovato sulla copia prova
costa una settimana.

## 12. Gli avvisi vanno letti

Se uno script stampa «attenzione: questa sezione occupa 2 pagine invece di 1»,
quell'avviso è un guasto, non rumore. Un avviso che nessuno legge è peggio di
nessun avviso, perché dà l'impressione che un controllo esista.

Regola: o l'avviso diventa un errore che ferma, o va in un riepilogo che
qualcuno guarda davvero alla fine.

## 13. Si registrano anche i propri errori

Nel dossier va una riga per ogni conclusione sbagliata e per come è stata
corretta — con il motivo tecnico, non solo l'esito. «La ricerca era partita sul
mercato sbagliato, e da uno zero avevo dedotto assenza di domanda» vale, la
prossima volta, più della conclusione giusta.

Due regole che nascono da lì:

- **prima di credere a uno zero, verifica di aver interrogato la cosa giusta.**
  Un risultato vuoto è quasi sempre uno strumento puntato male
- una conclusione che decide un investimento va verificata due volte, da due
  angoli diversi, prima di scriverla come fatto

## 14. Quando qualcosa deve restare vero per anni

Indirizzi, numeri di pagina, misure che finiscono su carta: **stanno in un
punto solo**, e tutto il resto li legge da lì. Un riferimento a «pagina 4»
dentro un colophon diventa falso alla prima riga aggiunta; un rimando alla
sezione per nome non scade mai.

Stessa regola per gli indirizzi stampati: una costante in cima allo script, e
un commento che dice che si cambia lì.