# Produzione video — Higgsfield

Aperta il 07/09/2026. Account: piano **plus**, **39,59 crediti** al momento
dell'apertura.

## Indice
1. La regola: si produce adesso, si pubblica al giorno 1
2. Il modello, e perché non quello consigliato
3. Le illustrazioni si richiamano per URL, non si ricaricano
4. Il prompt, e le tre cose che deve vietare
5. Cosa è stato generato
6. Cosa manca per farne un contenuto pubblicabile

## 1. La regola: si produce adesso, si pubblica al giorno 1

Siamo dentro la settimana di farming, e il piano dice di non pubblicare. Non
è in contraddizione: `promozione-social` fase 5 dice **«i contenuti si
producono in blocco, non uno al giorno»**. Produrre nella settimana di
farming è esattamente il posto giusto — al giorno 1 sono pronti.

## 2. Il modello, e perché non quello consigliato

Il primo preventivo era su **Seedance 2.5**, il modello di default:
**32,5 crediti per un video da 5 secondi.** Su 39,59 disponibili ne fa uno e
il conto è finito.

| Modello | 5 s · 9:16 | Note |
|---|---:|---|
| Seedance 2.5 | **32,5** | default del catalogo |
| **Kling v3.0** std, `sound: off` | **7,5** | **scelto** — 4,3 volte meno |

**L'audio generato si spegne, e non è solo per il prezzo.** Il format F1 vuole
il **suono vero della pagina che gira**, registrato da chi filma
(`references/formati.md` §2-bis). Una traccia audio inventata dal modello
andrebbe comunque buttata. Qui spegnerla costa meno **ed è la scelta giusta**.

Higgsfield ha anche proposto il preset **«IN THE DARK»**: rifiutato. Su un
libro della buonanotte per bambini un preset che si chiama così va nella
direzione opposta a tutto il resto.

## 3. Le illustrazioni si richiamano per URL, non si ricaricano

Le trenta tavole del libro **sono state generate su questo stesso account**:
i file su Drive si chiamano `hf_<data>_<ora>_<uuid>.png`, che è la
convenzione con cui Higgsfield nomina i download.

Quindi l'indirizzo si ricostruisce dal nome del file:

```
https://d8j0ntlcm91z4.cloudfront.net/user_<user-id>/<nome-del-file-di-drive>
```

e si importa con `media_import_url`, senza ricaricare niente. Verificato il
07/09 su due file: funziona.

**Il CDN però è bloccato dal proxy di questo contenitore** (403 sul CONNECT),
quindi Higgsfield le immagini le vede e io no. Conseguenza pratica: **posso
animarle ma non posso giudicarle, né sapere a quale notte corrisponde
ognuna.** Il giudizio sul risultato è dell'autore.

## 4. Il prompt, e le tre cose che deve vietare

```
Very gentle ambient animation of this existing children's book illustration.
Keep the artwork exactly as it is. The warm lamp light breathes softly, stars
twinkle slowly in the night sky, the blanket and fabric settle almost
imperceptibly, and the camera makes a barely perceptible slow push-in. Calm,
quiet, bedtime mood. Do NOT add, remove or change any character or figure.
Do NOT add any text, lettering, writing, captions, letters, numbers,
calligraphy or watermarks anywhere in the frame.
```

Tre divieti, e nessuno è decorativo:

1. **Niente testo, lettere, numeri, calligrafia.** È la regola 6.3
   dell'identità. Lo stesso generatore ha già scritto `10 Bedfor` su una
   grafica e sei `C` dentro il libro. In un video il rischio è più alto, non
   più basso — e testo arabo storpiato in questa nicchia non è un refuso.
   **Il testo si aggiunge dopo, digitato.**
2. **Niente personaggi aggiunti o modificati.** È la regola 6.2: il Profeta ﷺ
   non è mai raffigurato. Le tavole del libro rispettano la regola; un modello
   che aggiunge una figura la romperebbe.
3. **Movimento quasi impercettibile.** Non è timidezza: su un libro della
   buonanotte **la calma è il prodotto**. Un'animazione vistosa contraddice
   quello che si vende.

## 5. Cosa è stato generato

| # | Sorgente (file di Drive) | Job | Esito | Costo |
|---|---|---|---|---:|
| V1 | `hf_20260629_080940_ad7a4565…` | `81934212-ad2c-4948-b726-f3f95ee4dfc6` | ✅ 720×1280 · 5 s · muto | 7,5 |
| V2 | `hf_20260629_082356_6b1c95c5…` | `b2ccec61-631f-4db7-b2cb-3b31a1eb3761` | ✅ 720×1280 · 5 s · muto | 7,5 |

File:
`hf_20260907_141139_81934212-ad2c-4948-b726-f3f95ee4dfc6.mp4`
`hf_20260907_141147_b2ccec61-631f-4db7-b2cb-3b31a1eb3761.mp4`

**Spesi 15 crediti, ne restano circa 24,6 — cioè altri tre video.**

Due e non cinque di proposito: non vedo né le immagini di partenza né il
risultato, quindi prima che il budget finisca il controllo di qualità lo fa
l'autore. Se questi due reggono, gli altri tre si fanno subito; se non
reggono, sono costati quindici crediti invece di trentasette.

## 6. Cosa manca per farne un contenuto pubblicabile

Un video animato **non è ancora un F1**. Mancano tre cose, e si fanno fuori da
Higgsfield:

1. **Il testo a schermo, digitato**, che compare **progressivamente** — un
   blocco per volta. Senza voce è il testo a dare il ritmo
   (`references/formati.md` §2-bis). Le frasi stanno in
   `materia-prima.md` §1 e nel piano.
2. **L'audio.** Il suono vero della pagina che gira, registrato col telefono a
   venti-trenta centimetri in una stanza silenziosa, con sotto una base
   strumentale al 10-15%. **Un video muto su TikTok viene mostrato di meno**:
   l'audio lì è un canale di distribuzione, non una decorazione.
3. **La copertina in chiusura**, un secondo. È quella la CTA — non serve
   scrivere «lo trovi su Amazon».

E una scelta che nasce dalla ricerca di oggi
(`01 Ricerca/report-concorrenti.md` §9): la recensione che ha spiegato perché
il concorrente vende dice *«there's a puppy who literally does all the same
things she does at bedtime»*. **Il video deve mostrare Yusuf che fa la cosa
che fa il bambino di chi guarda** — non una bella illustrazione notturna
generica. Quando si scelgono le tavole da animare, si scelgono per **gesto**,
non per bellezza.
