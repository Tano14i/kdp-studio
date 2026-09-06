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

## 5. A che punto siamo

Il passo 1b su questo progetto resta **in corso**. Sono state chiuse due
domande e ne resta aperta una, che e' quella che decide.

**Chiuso:** il tema e' occupato da un reparto che vende davvero (§1), quindi il
NON SI FA del passo 1 e' definitivo e non si riapre.

**Chiuso:** la cornice della colpa e' occupata da tre libri deboli, due dei
quali con editore (§2). Non e' un vuoto invitante: e' un posto dove qualcuno
ha gia' provato e non ha funzionato.

**Aperto, ed e' l'unica cosa che manca:** lo scaffale della **riparazione**,
sulle due ricerche che non sono state ancora fatte —
`dopo aver urlato ai figli` e `chiedere scusa ai figli`, su Amazon.it. Servono
solo i titoli: i numeri si leggono poi a macchina.

La domanda a cui rispondono, formulata adesso per non poterla piegare dopo:

> Esiste un libro italiano per genitori che venda **cosa si fa dopo**, invece
> di come non farlo? Se esiste ed e' forte, l'angolo e' chiuso. Se esiste ed e'
> debole come i tre della colpa, vale la lettura B di §3 e l'angolo e' chiuso
> lo stesso. **Se non esiste affatto**, allora contano i contenuti di §4, e
> l'angolo passa al concept.
