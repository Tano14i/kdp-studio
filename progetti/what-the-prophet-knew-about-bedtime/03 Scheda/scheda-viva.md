# La scheda viva — letta il 07/09/2026

Fonte: stampa PDF della pagina Amazon.com fornita dall'autore, 07/09/2026
ore 09:03. Amazon non è raggiungibile da questo contenitore, quindi questo
file va rifatto a mano ogni volta che serve un dato aggiornato.

## Indice
1. I dati
2. Il numero che decide tutto
3. Lo scaffale, e dove sta il prezzo
4. Cosa manca sulla scheda, e costa zero
5. La foliazione, e cosa dice l'aritmetica

## 1. I dati

| | |
|---|---|
| ASIN | **B0H6ZCL6QC** |
| ISBN-13 | 979-8184833187 |
| Link | `amazon.com/What-Prophet-Knew-About-Bedtime/dp/B0H6ZCL6QC` |
| Pubblicato | **29 giugno 2026** — 70 giorni fa |
| Editore | Independently published |
| Formati | **solo paperback.** Nessuna edizione Kindle |
| Prezzo | **$19,99** |
| Pagine | **67** |
| Formato | 6 × 0,16 × 9 pollici |
| Età di lettura | 5-8 anni |
| Categoria | Children's Books › Literature & Fiction › **Religious Fiction** › Muslim — **una sola** |
| Posizione (BSR) | **nessuna. «No ranking yet»** |
| Vendite 30 giorni | **0-0** |
| Recensioni | **0** |
| Contenuti A+ | **assenti** |
| Video | assente |

**Il sottotitolo online è quello del frontespizio**, non quello scelto al
checkpoint 2:

> *30 Illustrated Bedtime Sunnah Rituals to Help Muslim Kids End the Day with
> Faith, Calm, and Love for the Prophet ﷺ*

La descrizione è scritta bene: apre con una domanda, elenca i tre blocchi per
notte, dichiara l'età, e chiude sulla nota che il Profeta ﷺ non è raffigurato.
Non è lei il problema.

## 2. Il numero che decide tutto

**Settanta giorni online. Zero vendite. Zero recensioni. Nessuna posizione in
classifica.**

Questo non è un libro con un problema di conversione: è un libro che **nessuno
ha ancora visto**. Amazon non gli dà posizione perché non ha storico di
vendite, e non ha storico di vendite perché nessuno lo trova. È il circolo che
regia descrive in `_profili/note-mercato.md` §1 per Amazon.it, e vale identico
su .com.

**Conseguenza che riordina tutto il piano:** i difetti degli interni — le sei
`C`, le fonti degli hadith mancanti, il lead magnet senza strada — **non sono
ciò che sta fermando questo libro.** Zero persone li hanno visti. Correggerli
adesso è rifinire un prodotto senza pubblico, e costa un ciclo di revisione.
Vanno corretti prima che arrivi volume, non prima che arrivi il primo lettore.

## 3. Lo scaffale, e dove sta il prezzo

Dai libri correlati sulla stessa pagina — stesso scaffale, molti sponsorizzati:

| Libro | Prezzo |
|---|---:|
| 30 Inspiring Stories of Prophets and Their Miracles | $10,99 |
| Allah Loves You, No Matter What | $11,76 |
| Eid with Ellie | $12,99 |
| My First Guide to Shahada | $12,99 |
| Noor and the Lesson of Letting Go | $13,55 |
| Biscuit Learns to Stay in Bed | $13,99 |
| 5-minute Bedtime Stories for Autistic Children vol. 2 | $14,99 |
| My Feelings, My Duas | $15,99 |
| A Better Muslim Every Day (diario 30 giorni) | $24,99 |

**Lo scaffale sta fra $10,99 e $15,99, mediana circa $13.** Questo libro sta a
**$19,99**, cioè il 40-50% sopra. Per un genitore che confronta quattro
copertine, è il libro caro senza una ragione visibile — perché la ragione, le
trenta tavole a colori, dalla miniatura non si vede.

**Ma il prezzo potrebbe non essere una scelta: potrebbe essere un vincolo.**
Un interno a colori su KDP ha due opzioni di stampa con costi molto diversi:

- **Colore premium** — costo fisso più una quota **per pagina**. Su 67 pagine
  diventa alto, e obbliga a un prezzo di copertina alto per non andare in
  perdita.
- **Colore standard** — sotto le ~108 pagine è un **costo fisso** molto più
  basso, e lascia margine a $13,99.

**Questa è la prima cosa da guardare, e sta su KDP in trenta secondi.** Nella
pagina di prezzo del libro, KDP mostra il *printing cost* calcolato sul libro
vero: quello è il numero, non una stima. Poi:

```
royalty = 0,60 × prezzo − printing cost
```

Se l'opzione è **standard**, il prezzo si può portare sullo scaffale oggi,
gratis, senza revisione, e resta margine. Se è **premium**, il libro è
strutturalmente fuori prezzo per il suo scaffale, e la decisione diventa
diversa e più seria: cambiare opzione di stampa significa ricaricare
l'interno.

Non tirare a indovinare: **leggi il printing cost su KDP e scrivilo qui.**

## 4. Cosa manca sulla scheda, e costa zero

Tutto quanto segue si cambia da soli, subito, senza revisione e senza rischio:

1. **Le categorie: ce n'è una sola, e KDP ne dà tre.** Due slot su tre sono
   buttati. E quella scelta è *Religious **Fiction***, mentre il libro insegna
   Sunnah reali dentro un racconto. Da valutare almeno:
   - Children's Books › Religions › Islam
   - Children's Books › Growing Up & Facts of Life › Health › Sleep
2. **I contenuti A+.** Assenti. Su un illustrato per bambini sono il posto
   dove le trenta tavole si vedono — cioè dove il prezzo si giustifica da solo.
3. **Le 7 parole chiave di backend.** Non si leggono dalla scheda: vanno
   guardate su KDP e scritte qui.
4. **L'edizione Kindle.** Non esiste. È una seconda scheda, un secondo prezzo
   d'ingresso e una seconda superficie di ricerca, e non costa stampa.
5. **La pagina autore di Kara Clem**, se non c'è.

## 5. La foliazione, e cosa dice l'aritmetica

**67 pagine**, spessore dorso 0,16 pollici. È il dato che mancava per montare
una copertina nuova.

L'aritmetica però dice una cosa da verificare. La descrizione dichiara «thirty
full-page illustrations», e la struttura letta dal PDF ha 30 notti più sette
sezioni di contorno:

```
30 notti × 2 pagine (tavola + testo)        = 60
mezzo titolo, frontespizio, colophon,
How to Use, Introduction, lettera finale,
Sunnah card                                 =  7
                                            ----
                                              67
```

Torna esatto — **e non lascia una pagina per il lead magnet.** È lo stesso
sospetto della `01 Prodotto/spec-dal-pdf.md` §4.5, adesso con un numero
accanto: gli interni promettono «turn the page», e nel conteggio quella pagina
non c'è.

Non è una prova: il contorno potrebbe essere disposto diversamente. **Ha
ragione l'artefatto** (regia §10): si guarda l'ultima pagina del PDF e si
scrive qui cosa c'è.
