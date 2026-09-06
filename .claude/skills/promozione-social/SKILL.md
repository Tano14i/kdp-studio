---
name: promozione-social
description: Porta un libro gia' pubblicato davanti ai lettori su Instagram, TikTok e Facebook senza budget pubblicitario e senza mostrare il volto. Costruisce identita' del pen name, format ripetibili, piano editoriale a 30 giorni e il ponte verso la scheda Amazon. Usa quando un libro e' pubblicato e non lo trova nessuno.
version: 0.1.0
argument-hint: "promozione-social \"<nome-progetto>\" [--pen-name <nome>] [--volto si|no] [--voce mia|sintetica|nessuna]"
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

## A cosa serve

Il metodo di questo repo porta un libro fino alla scheda Amazon e li' si ferma.
Una scheda senza traffico non vende: su Amazon.it la saggistica pratica e'
occupata (vedi `_profili/note-mercato.md` §1), quindi un titolo nuovo non
emerge da solo nella ricerca interna. Il traffico va portato da fuori.

Questa skill costruisce quel traffico dai social, in organico. Non insegna a
usare le app: produce i contenuti, il calendario e le regole di taglio.

## Usa quando

- Un libro e' **pubblicato**, ha un ASIN, e non lo scopre nessuno.
- Serve un piano editoriale a 30 giorni per un pen name.
- Bisogna decidere quali format tenere dopo due settimane di dati.

## NON per

- Libri non ancora pubblicati. Senza scheda Amazon la CTA punta al vuoto.
  Se il libro non c'e', il problema e' a monte: `ricerca-nicchia`.
- Pubblicita' a pagamento. Qui si lavora a costo zero. Le ADS sono un'altra
  fase, e si aprono solo su un contenuto che ha gia' funzionato in organico.
- Gestire gli account al posto dell'autore. Questa skill produce i materiali
  e il calendario; l'autore pubblica, o lo fa un programmatore di post.

## Il cancello d'ingresso

**Non si genera un solo contenuto prima di avere questi dati.** Un hook
scritto senza sapere di cosa parla il libro e' testo che sembra giusto e non
lo e', ed e' esattamente l'errore che questo repo ha gia' pagato tre volte in
un giorno (vedi i dossier, sezione «Errori commessi»).

| # | Dato | Perche' serve |
|---|------|---------------|
| 1 | ASIN + link Amazon | e' la destinazione di ogni CTA |
| 2 | Titolo e sottotitolo esatti | entrano nella bio e nelle chiusure |
| 3 | Descrizione della scheda | e' gia' la promessa, riscritta in versione social |
| 4 | Indice dei capitoli | ogni capitolo e' un filone di contenuti |
| 5 | Copertina (immagine) | compare in ogni video sottolineare |
| 6 | Recensioni ricevute, testo intero | le parole vere dei lettori sono gli hook |
| 7 | Stato di vendita, anche a spanne | decide se si promuove o si ripubblica |

Se manca il 6 perche' il libro non ha recensioni, si procede lo stesso: gli
hook si ricavano dall'indice e dalle recensioni **dei concorrenti**
(`01 Ricerca/recensioni-negative.txt`, se raccolte). Va scritto nel dossier
che sono di seconda mano.

Se manca l'1, ci si ferma. Senza destinazione non c'e' campagna.

## Configurazione

Tre interruttori decidono quali format sono ammessi. Vanno fissati prima del
piano, e scritti nel dossier.

| Interruttore | Valori | Effetto |
|---|---|---|
| `volto` | si / no | `no` esclude i format parlati in camera |
| `voce` | mia / sintetica / nessuna | `nessuna` obbliga al testo a schermo |
| `partenza` | zero / esistente | `zero` impone la settimana di farming |

**Volto e voce sono due decisioni diverse.** Un pen name anonimo puo'
comunque usare la voce dell'autore: nessuno la riconosce, e una voce vera
regge molto meglio della sintetica. Vanno chiesti separatamente: chi dice
«resto anonima» quasi sempre sta rispondendo solo sul volto.

Il catalogo dei format e la loro compatibilita' con questi interruttori stanno
in `references/formati.md`. Il protocollo di partenza a freddo, con la
settimana di farming e le regole di apertura degli account, sta in
`references/avvio-a-freddo.md`.

## Fasi

Sei fasi in ordine. Le prime tre si fanno una volta sola per pen name; le
ultime tre sono il ciclo che si ripete ogni mese.

### 1. Identita' del pen name — *una volta*

Nome account, bio, link in bio, storie in evidenza, immagine profilo.
Regole e formule in `references/avvio-a-freddo.md` §2.

Esce: `_profili/<pen-name>/identita.md`

### 2. Materia prima — *una volta per libro*

Si estraggono dai dati del cancello, in quest'ordine:

1. **Le frasi del libro** che stanno in piedi da sole. Dieci-quindici, prese
   dai capitoli. Sono il carburante dei video sottolineare.
2. **Le lamentele dei lettori**, dalle recensioni. Testo esatto, non
   parafrasato. Sono gli hook piu' forti che esistono, perche' non li ha
   scritti un autore.
3. **Un filone per capitolo**, dall'indice. Un capitolo che risponde a un
   problema vero regge da solo tre o quattro contenuti.

Esce: `progetti/<progetto>/05 Social/materia-prima.md`

**Regola:** ogni hook deve poter essere tracciato a una riga di questo file.
Un hook che non viene da nessuna parte e' un hook inventato.

### 3. Scelta dei format — *una volta*

Dal catalogo si scelgono **tre format, non di piu'**. Tre format ripetuti
trenta volte battono dieci format provati tre volte: l'algoritmo impara cosa
sei, e l'autore impara a produrli in minuti invece che in ore.

Criterio di scelta, in ordine: compatibili con gli interruttori → producibili
in meno di 5 minuti l'uno → almeno uno adatto a TikTok e uno a Instagram.

Esce: la riga «Format attivi» nel dossier.

### 4. Piano editoriale — *ogni mese*

Trenta contenuti, ognuno con: giorno, piattaforma, format, hook, testo
completo, CTA, brief visivo. Non bozze da rifinire: testo pronto.

Lo scheletro del mese, il ritmo e le ondate stanno in
`references/avvio-a-freddo.md` §4.

Esce: `progetti/<progetto>/05 Social/piano-<mese>.md`

### 5. Produzione e pubblicazione — *ogni mese*

I contenuti si producono **in blocco**, non uno al giorno. Una sessione da
un'ora per dieci video sottolineare; una per i caroselli.

Se in sessione ci sono strumenti collegati, si usano: Canva o Adobe Express
per i caroselli, Higgsfield per il video, Blotato per programmare e per
rileggere le metriche. Se non ci sono, la skill consegna i brief e pubblica
l'autore. **La skill non e' bloccata dall'assenza degli strumenti**: il piano
resta valido, cambia solo chi preme i tasti.

### 6. Misura e taglio — *a 14 e a 30 giorni*

Si guarda una cosa sola per piattaforma, e si taglia. Le soglie e le regole di
decisione stanno in `references/formati.md` §4.

Esce: aggiornamento del dossier, con cosa e' stato tagliato e perche'.

## Da non dimenticare

- **La CTA non vende il libro, apre una curiosita'.** «Lo trovi su Amazon» in
  fondo a un video che non ha ancora dato niente e' la ragione numero uno per
  cui un profilo di self publisher non cresce. Prima si da', poi si chiede, e
  il rapporto sano e' molto sbilanciato verso il dare.
- **Il libro va mostrato, non nominato.** Un libro fisico in campo, sfogliato
  o sottolineato, fa il lavoro che una frase promozionale non fa. Per questo i
  format faceless funzionano: il protagonista e' l'oggetto, non la persona.
- **Un contenuto morto non e' un format morto.** Serve un campione. La regola
  di taglio e' sul format dopo dieci uscite, mai sul singolo pezzo.
- **Il piano editoriale non e' il contenuto.** Un calendario con «lunedi:
  carosello motivazionale» non e' lavoro fatto: e' lavoro rimandato. Se il
  testo non e' scritto, il contenuto non esiste.
- **Amazon non e' raggiungibile da questo contenitore.** Il proxy di rete
  blocca `amazon.it` (403 sul CONNECT, anche su `completion.amazon.it`), e
  prima ancora l'IP di datacenter prendeva 503. Ogni dato Amazon arriva
  dall'autore, come in `scheda-raccolta.md`. Non tentare la strada automatica:
  e' gia' stata percorsa e documentata come chiusa.
- **Le metriche le legge chi ha l'accesso.** Se Blotato o gli account non sono
  collegati, i numeri della fase 6 li porta l'autore. Un numero inventato per
  chiudere un ciclo di misura fa tagliare il format sbagliato.

## Rapporto con le altre skill

| Skill | Rapporto |
|---|---|
| `pubblicazione-kdp` | viene prima: senza scheda viva non si promuove |
| `avatar-cliente` | fornisce le lamentele, se il libro non ha recensioni proprie |
| `dna-stilistico` | la voce dei post e' la stessa del libro, non un'altra |
| `regia` | chiama questa skill dopo il checkpoint 7 |

Le recensioni raccolte qui tornano indietro: sono materia prima per
`avatar-cliente` sul libro successivo. E' l'unica fonte di recensioni su cui
l'autore ha accesso completo e gratuito.
