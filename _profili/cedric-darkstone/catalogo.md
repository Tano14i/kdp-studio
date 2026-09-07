# Catalogo Cedric Darkstone — stato al 07/09/2026

Pen name attivo, quattro titoli pubblicati, nicchia **giochi di ruolo da
tavolo (D&D / TTRPG)**, due lingue. Nessuna cartella progetto, nessun dossier,
nessuna delle sette decisioni scritta da nessuna parte: fino a oggi questo pen
name esisteva solo dentro KDP.

Fonte dei numeri: report **KDP Orders gennaio → settembre 2026**, letto da
`analisi-vendite.py`. I numeri non si scrivono a mano: stanno in
[`vendite-2026.md`](vendite-2026.md), che quello script genera. Se un numero
qui e' diverso da li', ha ragione il file generato.

## Indice
1. La conclusione che conta
2. Il catalogo, SKU per SKU
3. Dove nasce il fatturato
4. I quattro guasti trovati dai controlli
5. Cosa ha funzionato e cosa no
6. Cosa manca, in ordine
7. **Checkpoint — le tre strade**
8. Tabella di stato
9. Errori di questa analisi

## 1. La conclusione che conta

**179,91 EUR in nove mesi, e il 79% e' arrivato negli ultimi tre.**

Non e' un catalogo piatto: e' un catalogo che ha appena trovato qualcosa. Il
libro pubblicato a **luglio 2026** — *Diventa Master - La Tua Prima Campagna* —
da solo vale **104,23 EUR, il 58% del totale**, prodotti in tre mesi contro i
nove degli altri. Da luglio in poi il pen name gira a **~46 EUR/mese** contro
i ~6 EUR/mese del primo semestre.

| Periodo | Royalty | Al mese |
|---|---:|---:|
| gen → giu 2026 (6 mesi, tre titoli) | 36,94 EUR | 6,16 EUR |
| lug → set 2026 (3 mesi, quattro titoli) | 138,76 EUR* | 46,25 EUR |

*settembre e' parziale: il report si ferma al giorno 7, e ha gia' fatto 24,56 EUR.
La tabella conta le vendite (175,70 EUR); i 4,20 EUR di Kindle Unlimited stanno
fuori perche' il report non li assegna al mese. Totale con KU: 179,91 EUR.

E c'e' una cosa che questo dice al resto dello studio. Il repo ha misurato
**cinque nicchie di saggistica pratica italiana e ha chiuso cinque volte con
NON SI FA** (`_profili/note-mercato.md` §1). Intanto, in una nicchia che nessun
documento di questo repo nomina mai, un pen name gia' vivo vendeva. **Il
mercato dove Cedric Darkstone guadagna non e' mai stato misurato**, e le uniche
misure che abbiamo sono di un mercato dove non abbiamo ancora pubblicato niente.

## 2. Il catalogo, SKU per SKU

| Titolo | Lingua | ASIN eBook | ASIN cartaceo | ISBN | Uscita stimata |
|---|---|---|---|---|---|
| Diario del Dungeon Master | IT | — | B0CYCNXQS2 | *vuoto* | prima del 2026 |
| First-Time Dungeon Master | EN | B0GKYP3N7T | B0GKYTMQW6 | 9798246469538 | ~feb 2026 |
| Diventa Master - La Tua Prima Campagna | IT | B0H62CB67K | B0H5W5BD5X | 9798182122399 | ~lug 2026 |
| 500 Random Encounter Tables | EN | B0H67Q12T6 | B0H67HKDWL | 9798183536751 | ~giu 2026 |

Il *Diario* e' l'unico senza edizione digitale, l'unico senza ISBN nel report,
e l'unico a royalty 50%. Tre anomalie sullo stesso titolo: vedi §4.

## 3. Dove nasce il fatturato

**Il cartaceo e' il prodotto, l'ebook e' il volantino.** 81% delle royalty da
36 copie di carta, 17% da 14 copie digitali.

| | Copie | Royalty | Per copia |
|---|---:|---:|---:|
| Cartaceo | 36 | 145,63 EUR | **4,05 EUR** |
| eBook | 14 | 30,07 EUR | 2,15 EUR |
| Kindle Unlimited | 1.512 pagine | 4,20 EUR | — |

Sul mercato italiano lo scarto e' ancora piu' netto: *Diventa Master* rende
**6,60 EUR** a copia in carta e **1,69 EUR** in digitale. **La stessa vendita
vale quasi quattro volte tanto se il lettore compra il cartaceo**, e infatti
il cartaceo vende anche di piu' (14 copie contro 7).

Kindle Unlimited e' rumore: 1.512 pagine lette in nove mesi valgono 4,20 EUR,
il 2,3% del totale. Vale come vetrina, non come ricavo.

**Amazon.it fa il 65% di tutto** con due titoli, mentre i due titoli inglesi
messi insieme — sui mercati piu' grandi del mondo — fanno 64 EUR. Il pen name
ha un nome inglese, meta' catalogo in inglese, e guadagna in italiano.

## 4. I quattro guasti trovati dai controlli

Questi non sono opinioni: sono le quattro righe con cui `analisi-vendite.py`
esce con codice diverso da zero.

### 4.1 Il nome dell'autore e' spaccato in due

Su *500 Random Encounter Tables* — sia ebook sia cartaceo — il nome e'
registrato **`Cedric  Darkstone`, con due spazi**. Sugli altri tre titoli e'
`Cedric Darkstone`.

Per Amazon sono due autori diversi. Il libro piu' recente in inglese **non
compare nella pagina autore degli altri tre**, e il lettore che finisce di
leggerlo e clicca sul nome non trova il resto del catalogo. E' esattamente il
punto in cui un catalogo dovrebbe funzionare come catalogo, ed e' rotto per
uno spazio.

Costo della riparazione: una modifica in Bookshelf. Ritorno: il collegamento
fra il titolo che sta crescendo e gli altri tre.

### 4.2 Il *Diario* ha venduto sei copie a zero euro

Gennaio 2026, sei copie vendute a 6,00 EUR di listino con **royalty 0,00 EUR**.
Il conto e' esatto: 50% di 6,00 = 3,00, meno 3,08 di stampa = negativo, quindi
zero. **Il prezzo era sotto il costo di produzione.** Sei lettori serviti,
zero incassato.

Da febbraio il prezzo e' salito a 8,19 EUR e la royalty a 1,02 EUR: la
correzione e' gia' stata fatta, ed e' l'unica decisione di questo catalogo che
si vede nei dati. Ma resta il margine peggiore del catalogo: **12,5% del
prezzo di copertina**, contro il 46% di *Diventa Master*.

### 4.3 Il *Diario* paga il 50% dove KDP paga il 60%

Il report riporta royalty **50%** per il cartaceo del *Diario*, mentre gli
altri tre titoli sono al 60% standard. Nella stessa riga la colonna ISBN e'
vuota, dove gli altri hanno il loro.

Non ho un modo per stabilire da qui perche': va guardato nel Bookshelf. Se il
titolo puo' passare al 60%, agli attuali 8,19 EUR la royalty va da 1,02 a
**1,83 EUR, +79%**, senza toccare il prezzo.

### 4.4 Il *Diario* e' fermo da luglio

Tredici copie in nove mesi, 7,14 EUR totali, ultima vendita luglio. E' il
titolo piu' vecchio, l'unico senza ebook, l'unico senza copertina coordinata
al resto (non lo vedo, ma il prezzo di 6-8 EUR contro i 14,99 degli altri dice
che e' un prodotto di un'altra epoca del catalogo).

## 5. Cosa ha funzionato e cosa no

**Le due giornate gratis si leggono bene solo mettendole una accanto all'altra**,
perche' sono state fatte in modo opposto e hanno reso in modo opposto.

| | feb — First-Time DM | giu — 500 Encounter Tables |
|---|---:|---:|
| Copie regalate | 27 | 11 |
| Su quanti mercati | 8 | 2 (USA, India) |
| Copie vendute nel mese stesso | 4 | 0 |
| Copie vendute nei 3 mesi dopo | 2 | **6** |
| Pagine KU nel mese stesso | 206 | 4 |
| Pagine KU nei 3 mesi dopo | 261 | **557** |

**Undici copie regalate su due mercati hanno reso piu' di ventisette sparse su
otto**, e non di poco: sei vendite contro sei, ma con meno della meta' delle
copie regalate, e con il doppio delle pagine lette.

I due ritorni hanno anche forme diverse. Febbraio ha reso **subito e sul
cartaceo**: nel mese stesso della promo sono partite tre copie di carta —
Italia, Olanda, Australia — che valgono 5,92, 5,92 e 8,68 EUR, cioe' quasi
tutto il mese migliore del primo semestre. Poi si e' spento. Giugno non ha
reso niente nel mese e ha reso tutto dopo, con due mesi di ritardo: 557 pagine
lette e sei copie fra luglio e settembre.

**Tre mercati hanno ricevuto una copia gratis e non hanno mai comprato niente,
di nessun titolo, in nove mesi**: India, Brasile e Canada. Sono a zero euro
nella tabella dei mercati. Regalare li' non e' costato niente, ma non ha
comprato neanche niente.

**Il Giappone e' il contrario**: una copia regalata in febbraio, e a maggio una
copia cartacea venduta con **1.050 JPY di royalty** — la royalty per copia piu'
alta dell'intero catalogo, 6,51 EUR. Un mercato solo, una vendita sola, ed e'
il 4% del fatturato di nove mesi.

**Il libro italiano nuovo ha fatto in tre mesi il doppio di quello inglese in
otto.** *Diventa Master* e' uscito a luglio senza nessuna promo gratis e ha
venduto 21 copie per 104,23 EUR. *First-Time DM* e' uscito a febbraio con 27
copie regalate e ne ha vendute 10 in otto mesi, per 39,11 EUR.

**Nessuno di questi libri e' mai stato promosso fuori da Amazon.** Il passo 14
della regia — `promozione-social` — non e' mai stato fatto per nessun titolo.
Tutto quello che si vede in questi numeri e' traffico interno ad Amazon: chi
gia' cercava un manuale per master lo ha trovato. Nessun lettore e' mai
arrivato da fuori.

## 6. Cosa manca, in ordine

1. le quattro riparazioni del §4 — sono l'unico guadagno che non richiede di
   scrivere niente
2. il prezzo dell'ebook italiano: 2,45 EUR netti e' il fondo della fascia 70%,
   e sette copie in tre mesi non sono un volume che il prezzo stia sostenendo
3. la nicchia TTRPG non e' mai stata misurata con `ricerca-nicchia`, e questo
   e' l'unico mercato in cui questo studio ha gia' venduto qualcosa
4. `promozione-social` per *Diventa Master*, che e' il titolo che sta gia'
   crescendo da solo
5. il secondo titolo italiano — *Diventa Master* dimostra che li' c'e' domanda,
   e in questo catalogo non ha compagni
6. che fare del *Diario*: rilanciarlo o lasciarlo morire

## 7. Checkpoint — chiuso il 07/09/2026: **strada B**

**Scelto: portare fuori da Amazon il titolo che gia' cresce** — `promozione-social`
su *Diventa Master - La Tua Prima Campagna*.

Le riparazioni della strada A restano da fare comunque: costano giorni, non
settimane, e non tolgono niente alla B.

Le scartate, col motivo, perche' fra tre mesi servira' sapere perche' no:

- **C, misurare la nicchia e scrivere il quinto libro** — non scartata, rimandata.
  Aumenta il numero di libri che vendono invece del rendimento di quelli che
  ci sono, ma sono due-tre mesi prima di vedere un euro, e c'e' gia' un titolo
  che cresce da solo e che nessuno sta spingendo. Si riapre quando la B ha
  prodotto i suoi primi dati di pubblico, che alla ricerca servono.
- **B e C insieme** — scartata per la finestra di contesto (§7 del metodo) e
  perche' la B parte da un pen name social che non esiste ancora: farla a meta'
  attenzione e' il modo di non farla.
- **Solo le riparazioni** — scartata perche' non risolve il problema vero. Il
  catalogo resta invisibile fuori da Amazon anche riparato alla perfezione.

Le tre strade, come erano state presentate:

### A — Riparare quello che c'e' *(giorni, non settimane)*

Nome autore, royalty del *Diario*, prezzo dell'ebook italiano. Nessuna
scrittura, nessuna ricerca.
**Quello che rende:** il collegamento del catalogo, +79% sulla royalty del
*Diario*, e un prezzo dell'ebook italiano deciso invece che ereditato.
**Quello che non risolve:** il catalogo resta invisibile fuori da Amazon.

### B — Portare fuori da Amazon il titolo che gia' cresce *(un mese)*

`promozione-social` su *Diventa Master*, il libro che fa il 58% del fatturato
senza che nessuno lo abbia mai spinto.
**Perche' proprio questo:** e' l'unico che ha gia' dimostrato di vendere senza
aiuto, e la nicchia D&D italiana ha su TikTok e Instagram un pubblico visibile
che nessuno dei quattro libri sta intercettando.
**Quello che costa:** un pen name da costruire da zero — Cedric Darkstone non
ha profili social — e trenta giorni di pubblicazioni.

### C — Misurare la nicchia e scrivere il quinto libro *(due-tre mesi)*

`ricerca-nicchia` sul TTRPG italiano, poi la catena completa fino a
`pubblicazione-kdp`.
**Perche':** e' l'unico mercato dove questo studio ha gia' un verdetto positivo
*dal campo* invece che da una misura. Cinque NON SI FA sulla saggistica
pratica contro 179 EUR incassati qui.
**Quello che costa:** e' la strada piu' lunga, ed e' anche l'unica che aumenta
il numero di libri che vendono invece del rendimento di quelli che ci sono.

**Non sono alternative secche.** A costa giorni e va fatta comunque; il vero
bivio e' fra B e C — spingere quello che c'e', o aggiungerne uno.

## 8. Tabella di stato

Il catalogo esiste, il metodo dietro no. Questa tabella dice quali passi della
regia sono stati fatti *sul serio* per questo pen name.

| # | Passo | Stato | Dove sta |
|---|---|---|---|
| 0 | Cartella e convenzioni | **eseguito oggi** | questa cartella |
| 1 | Nicchia e concorrenti | **da fare** | — |
| 2 | Avatar cliente | **da fare** | — |
| 3 | Concept e positioning | eseguito ma non scritto | solo nei quattro libri |
| 4 | Titolo, sottotitolo, copertina | eseguito ma non scritto | solo nei quattro libri |
| 5 | Outline | eseguito ma non scritto | — |
| 6-7 | DNA stilistico e campione | eseguito ma non scritto | — |
| 8-11 | Manoscritto → copertina | eseguito | i quattro titoli pubblicati |
| 12 | Scheda, A+, campagne | parziale | schede vive, A+ e campagne ignote |
| 13 | Traduzione e mercati | eseguito ma non scritto | IT + EN, senza una regola |
| 14 | Promozione social | **da fare** | — |

Le righe «eseguito ma non scritto» sono il caso che il metodo chiama
pericoloso: quattro libri portano decisioni di concept, voce e posizionamento
che non esistono in nessun file, e che al quinto libro verranno prese di nuovo,
diverse.

## 9. Errori di questa analisi

Per il §13 del metodo — si registrano anche i propri errori, col motivo
tecnico, perche' valgono piu' della conclusione giusta.

- **Prima versione della tabella per copia: sbagliata.** Prendevo la royalty
  della riga del report senza dividerla per le copie di quella riga, e
  l'ebook italiano risultava rendere 6,76 EUR a copia — cioe' il 276% del
  prezzo. E' l'assurdo che ha fatto vedere il bug; se la riga fosse stata di
  due copie invece che di quattro, il numero sarebbe stato solo un po'
  sbagliato e sarebbe passato. **Un margine impossibile e' un controllo che si
  puo' automatizzare, e adesso lo e'.**
- **Il conteggio degli avvisi contava le occorrenze, non i guasti distinti**:
  diceva «18 da guardare» per quattro problemi. Un avviso gonfiato e' un
  avviso che si smette di leggere.
- **La prima lettura delle promo gratis era sbagliata in tre punti**, e li
  elenco perche' l'errore e' sempre lo stesso: avevo contato solo i tre mesi
  *dopo* la promo. Cosi' febbraio risultava un fallimento (2 copie), quando le
  sue tre vendite di cartaceo in Italia, Olanda e Australia erano arrivate
  *nel mese stesso*; avevo scritto che nessuno dei mercati regalati aveva poi
  comprato, e invece il Giappone ha comprato la copia piu' redditizia del
  catalogo; e avevo sommato le pagine KU sulla finestra sbagliata.
  **La finestra di misura era stata scelta prima di guardare i dati, e ha
  deciso la conclusione al posto loro.** Con la finestra giusta la conclusione
  si e' capovolta: la promo di giugno non e' andata «un po' meglio», ha reso il
  doppio con meno della meta' delle copie.
- **I cambi in euro sono indicativi**, non contabili. Per questo l'output
  generato riporta sempre la royalty per valuta non convertita accanto alla
  stima: quella e' il dato, l'euro e' la comodita'. I cambi stanno in un punto
  solo, in cima allo script.
