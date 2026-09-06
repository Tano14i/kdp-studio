# Scaffale dell'angolo «il dopo» — Amazon.it
Verifica del passo 1b · 06/09/2026

E' la verifica che `01b-angolo.md` §7 chiedeva. Fatta a meta': una delle
quattro ricerche e' stata portata dall'autore, e i numeri sono stati letti a
macchina recuperando gli ASIN dalla ricerca web.

## Indice
1. Lo scaffale della prevenzione: quanto e' forte davvero
2. Lo scaffale della colpa: quanto e' debole
3. La lettura, e la trappola che ci sta dentro
4. Lo scaffale della riparazione: nessun libro, ma i contenuti girano
5. A che punto siamo

---

## 1. Lo scaffale della prevenzione: quanto e' forte davvero

E' l'offerta che il passo 1 aveva contato ma non misurato: tredici titoli che
vendono tutti **come non urlare**. I numeri, presi da `www.amazon.it/dp/<ASIN>`
con `sonda_angolo.py` (dati grezzi in `dati-scaffale-urlare.json`, generato):

| ASIN | Titolo | Voto | Recensioni |
|---|---|---:|---:|
| `B0BDNFCH9N` | Merini, *Educare Senza Urlare: 4 libri in 1* | 4,3 | **211** |
| `B0CZ5P4SD5` | Petrucciani, *Educare senza perdere la calma* | 4,7 | **184** |
| `B0CK3ZZKQS` | Nunziata, *Educare senza urlare: Strategie efficaci* | 4,7 | **113** |
| `B0BTTQHCLP` | Moreno e Marchetti, *Educare Senza Urlare: 4 Libri in 1* | 4,7 | 58 |
| `880997784X` | Garcia, *Educare senza gridare* | 4,5 | 35 |
| `B0CK44F1QL` | Monte, *La Guida Definitiva per Genitori Esauriti* | 4,3 | 10 |

**Il NON SI FA del passo 1 esce rafforzato, non indebolito.** Duecentoundici
recensioni sul primo, tre titoli sopra cento: non e' uno scaffale di fantasmi,
e' un reparto che vende. Chi entra sulla prevenzione entra contro questi.

Due correzioni al report del passo 1, che li' non si potevano fare:

- **i concorrenti sono piu' di tredici.** Petrucciani, Nunziata e Garcia non
  erano nella lista, e sono stati trovati senza cercarli, mentre si cercava
  altro. Come per l'altra nicchia: ogni conteggio fatto finora era per difetto;
- **Michela Monte ha 10 recensioni.** Il report la indicava come «il colpo piu'
  duro», perche' il suo sottotitolo copriva gia' l'angolo ipotizzato. Copre
  l'angolo, ma non lo presidia: e' l'ultimo della lista.

## 2. Lo scaffale della colpa: quanto e' debole

Ricerca `senso di colpa genitori`, portata dall'autore. E' l'angolo piu'
vicino a quello candidato — «assolvere invece di correggere».

| ASIN | Titolo | Voto | Recensioni |
|---|---|---:|---:|
| `B0H2WXMKRM` | Carulli, *La colpa non e' dei genitori* | 5,0 | 4 |

Piu' due che dallo scaffale si leggono ma di cui non si e' ricavato l'ASIN
(numeri dalla pagina dei risultati, non misurati a macchina, quindi fuori dalla
tabella controllata):

- Martella, *Genitori liberi. Itinerari per educare senza sensi di colpa*,
  **Sonzogno** — 5,0 con **10** recensioni, 17,10 euro;
- Rotbart, *Genitori senza sensi di colpa*, **Vallardi** — 4,5 con **2**
  recensioni.

Tre libri sulla colpa dei genitori: **10, 4 e 2 recensioni.** Due dei tre hanno
dietro un editore vero.

## 3. La lettura, e la trappola che ci sta dentro

Uno scaffale sottile sembra un'occasione. Qui non e' detto che lo sia, e la
differenza decide il progetto.

**Lettura A — nessuno l'ha fatto bene.** Tre libri deboli su un tema con
domanda: c'e' spazio.

**Lettura B — la promessa non vende.** Gli stessi lettori sono li' e spendono:
comprano `come non urlare` a duecentoundici recensioni. Sonzogno e Vallardi
hanno entrambi provato la cornice della colpa, con distribuzione in libreria, e
hanno fatto 10 e 2. Due editori che falliscono dove i pen name fanno 211 non
sono un caso.

**La B e' pesante, e va guardata prima della A.** E' esattamente l'avvertenza
di `ricerca-inversa` §5: senza la verifica, questa skill produce entusiasmo.

C'e' pero' una distinzione che le due letture non catturano, ed e' la piu'
utile:

> I tre libri deboli vendono uno **stato** — «senza sensi di colpa», «la colpa
> non e' tua». I libri che vendono forte vendono un'**azione** — «come non
> urlare», «educare senza perdere la calma». L'angolo candidato non e' uno
> stato: e' un'azione, e per giunta a orario — *cosa fai nei dieci minuti dopo*.

Se la regola vera del reparto e' «gli stati non vendono, le azioni si'», i
10-4-2 non bocciano l'angolo candidato: bocciano una cornice diversa che gli
somiglia. Se invece la regola e' «della colpa non si vuole sentir parlare»,
l'angolo e' morto.

**Questa distinzione non e' verificata.** E' la cosa piu' importante scritta in
questo file, ed e' un'ipotesi.

## 4. Lo scaffale della riparazione: nessun libro, ma i contenuti girano

Cercando in rete un libro italiano per genitori sulla **riparazione dopo
l'urlo**, non ne esce nessuno. Escono libri illustrati per bambini che
insegnano a chiedere scusa — pubblico opposto — e poi questo:

- «**Ho urlato a mio figlio: ho rovinato tutto?** La pedagogista: *ai figli non
  servono genitori perfetti*» — nostrofiglio.it
- «**Che differenza c'e' tra scusarsi e riparare?**» — ilgenitoreconsapevole.it
- «**Riparare e chiedere scusa: non e' lo stesso**» — podcast La Tela
- «Va bene chiedere scusa ai figli?» — reel La Tela
- «Imparare a chiedere scusa. Come si puo' chiedere scusa ai propri figli in
  modo credibile?» — La Difesa del Popolo

**E' la forma esatta del segnale che `ricerca-inversa` cerca**: la domanda
esiste e viene servita da articoli, podcast e reel, cioe' da contenuti gratuiti
e brevi. Nessuno l'ha ancora messa in un libro. Il primo titolo di quella lista
e' l'angolo candidato, parola per parola, scritto da un giornale invece che da
un autore.

**Cosa questo NON dimostra.** Che una ricerca in rete non trovi un libro non
vuol dire che sullo scaffale non ci sia: la ricerca di Amazon.it da qui
risponde 503, e tutto quello che si sa dei titoli italiani passa da quello che
un motore decide di mostrare. E' un indizio forte, non una misura.

## 5. Le due ricerche mancanti: nessun risultato

Il passo 1b su questo progetto resta **in corso**. Sono state chiuse due
domande e ne resta aperta una, che e' quella che decide.

**Chiuso:** il tema e' occupato da un reparto che vende davvero (§1), quindi il
NON SI FA del passo 1 e' definitivo e non si riapre.

**Chiuso:** la cornice della colpa e' occupata da tre libri deboli, due dei
quali con editore (§2). Non e' un vuoto invitante: e' un posto dove qualcuno
ha gia' provato e non ha funzionato.

**Fatte il 06/09 sera. Esito: nessun risultato**, su entrambe.

La domanda era stata formulata prima di vederne l'esito, per non poterla
piegare dopo:

> Esiste un libro italiano per genitori che venda **cosa si fa dopo**, invece
> di come non farlo? Se esiste ed e' forte, l'angolo e' chiuso. Se esiste ed e'
> debole come i tre della colpa, vale la lettura B di §3 e l'angolo e' chiuso
> lo stesso. **Se non esiste affatto**, allora contano i contenuti di §4, e
> l'angolo passa al concept.

Il terzo caso.

### Prima di crederci: quanto vale uno zero

In questo repo uno zero ha gia' ingannato due volte, ed e' scritto in
`note-mercato.md` §6 che **prima di credere a uno zero si verifica di aver
interrogato la cosa giusta**. Un «nessun risultato» dalla ricerca di Amazon su
una frase lunga in italiano e' uno strumento debole: potrebbe essere il motore
che non regge la frase, non lo scaffale che e' vuoto. Prenderlo per buono
sarebbe la terza replica dello stesso errore — e per giunta nella direzione in
cui fa comodo, che e' la peggiore.

Per questo la conclusione poggia su **tre strade indipendenti**, non su quella:

| Strada | Esito |
|---|---|
| Ricerca Amazon.it su `dopo aver urlato ai figli` e `chiedere scusa ai figli` | nessun risultato |
| Ricerca in rete di un libro italiano sulla riparazione (tre formulazioni diverse) | nessun libro per genitori; escono articoli, podcast, e libri illustrati **per bambini** sul chiedere scusa |
| Ricerca in rete sul termine tecnico «rottura e riparazione» | un volume FrancoAngeli su separazione e divorzio (altro tema), un articolo sull'«educazione riparativa». Nessun libro pratico per genitori |

Due delle tre non passano dalla casella di ricerca di Amazon, quindi lo zero
non e' piu' un artefatto di un solo strumento. E' la regola del repo:
*una conclusione che decide un investimento va verificata due volte, da due
angoli diversi.*

### Cosa c'e' al posto del libro

L'unico titolo che esce cercando la riparazione e' *Smettere di urlare e'
facile* di Rona Renner — che e' di nuovo la **prevenzione**, tradotta. Il
resto e' contenuto gratuito, e si accumula:

- Unobravo, «Urlare ai figli: come gestire la vergogna da genitore»
- Unobravo, «Perche' urlo ai miei figli? Rabbia e vergogna genitoriale»
- Nostrofiglio, «Ho urlato a mio figlio: ho rovinato tutto?»
- ilgenitoreconsapevole.it, «Che differenza c'e' tra scusarsi e riparare?»
- La Tela, podcast «Riparare e chiedere scusa: non e' lo stesso»
- genitorisenzastress, «Perche' urlare ai tuoi figli non funziona»

Sei fonti diverse, tutte gratuite, tutte sulla stessa domanda. E' il quadro
che `ricerca-inversa` descrive: **la domanda e' servita, il libro no.**

## 6. Verdetto sull'angolo: SI FA

Primo SI FA di questo repo, dopo cinque temi misurati e due progetti chiusi.
Va scritto con dentro anche cio' che lo indebolisce, perche' il passo
successivo ci si costruisce sopra.

**Cosa lo regge:**

- nessun libro italiano sulla riparazione, verificato da tre strade (§5);
- la domanda esiste e viene servita da sei fonti gratuite diverse (§5);
- **il pubblico c'e' e spende**: lo scaffale accanto fa 211, 184 e 113
  recensioni (§1). Non e' un vuoto in una stanza vuota, e' un vuoto dentro un
  reparto affollato;
- due lettrici italiane, sotto l'incumbent, dicono con parole loro di essersi
  sentite giudicate (`01b-angolo.md` §2). E' il bisogno che nessuno raccoglie.

**Cosa lo indebolisce, e va portato al passo successivo invece che dimenticato:**

- **la cornice della colpa non vende** (§2): 10, 4 e 2 recensioni, con Sonzogno
  e Vallardi dietro. E' l'unico contro-indizio duro che abbiamo;
- l'ipotesi che spiega la differenza — *gli stati non vendono, le azioni si'*
  (§3) — **non e' verificata**, ed e' quella su cui poggia il fatto che il
  contro-indizio non colpisca questo angolo;
- che una riparazione non abbia libri potrebbe avere un motivo che non
  conosciamo. `ricerca-inversa` §4, domanda 2: un pubblico che non compra e'
  un vuoto che resta vuoto.

**La condizione che il SI FA porta con se', al checkpoint 1:**

> Il concept deve promettere un'**azione**, non uno stato. «Cosa fai nei dieci
> minuti dopo» si puo' fare; «un libro per non sentirti in colpa» e' gia' stato
> provato da due editori e ha fatto 10 e 2 recensioni. Se le opzioni di
> `concept-positioning` scivolano sulla seconda, questo verdetto non le copre.

Il passo 1b e' chiuso. Il prossimo e' il **passo 2, `avatar-cliente`**.

