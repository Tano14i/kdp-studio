# Report nicchia — First-Time Dungeon Master
Fase 1 · Amazon US (inglese) · 06/09/2026

## Indice
1. Cosa si è cercato
2. Tabella concorrenti
3. Curva del voto nel tempo
4. La domanda
5. Il varco
6. Verdetto
7. Cosa resta da verificare

## Nota di metodo (limite di questo ambiente)
Amazon.com e Goodreads sono **bloccati dal proxy di rete** di questa sessione:
non ho potuto misurare i numeri live (VERIFIED) direttamente sulle pagine
prodotto. I dati qui sotto vengono da **ricerca web** (motori/terze parti) e sono
etichettati di conseguenza. Il verdetto tiene conto di questo limite.
Etichette: `VERIFIED` = misurato live · `WEB` = da ricerca web, non live ·
`INFERENCE` = dedotto · `HYPOTHESIS` = da verificare · `USER-INPUT`.

## 1. Cosa si è cercato
- Mercato: Amazon US, reparto Libri. Giorno: 06/09/2026.
- Query: "first time dungeon master", "how to be a dungeon master beginner",
  "dungeon master guide beginner", "how to play D&D for beginners".
- Segmento rilevante: **guide self-pub per DM principianti** (NON i manuali
  ufficiali Wizards, che sono il contesto ma non il concorrente diretto di un
  self-pub KDP).

## 2. Tabella concorrenti
| ASIN/ISBN | Titolo | Autore | Voto | N. recensioni | Note | Fonte |
|---|---|---|---|---|---|---|
| B0B8F1G5G7 | Return of the Lazy Dungeon Master | Michael E. Shea (Sly Flourish) | ~4,7★ (HYP) | **1.600+** | Incumbent dominante, angolo "prep veloce/lazy" | WEB |
| B01AYDICU2 | The Lazy Dungeon Master (orig.) | Michael E. Shea | alto (HYP) | molte (HYP) | Classico del segmento fast-prep | WEB |
| B0DRZ2264T | How to Play D&D for Beginners | Eldric Silverquill | 4,6★ | ~17 (Amazon.ca) | Entrante self-pub 2024, poche recensioni = giovane | WEB |
| 0471783307 | Dungeon Master For Dummies | Slavicsek/Baker/Grubb (Wiley) | n/d | n/d | Tradizionale, datato (2006) | WEB |
| 1737737817 | Becoming Dungeon Master | Kenton Whitman | n/d | n/d | Indie, taglio "instruction manual" | WEB |
| — (Goodreads 221830931) | The Advanced RPG Beginner's Guide to Becoming a DM | n/d | n/d | n/d | Entrante 2025 | WEB |
| 1795076879 | ~~Your First Dungeon~~ | Alexander Paiz | 5★ (2-3 voti) | — | **ESCLUSO**: è un libro illustrato per bambini, non una guida | WEB |

Prezzi e date di uscita: **non raccolti live** (Amazon bloccato) → §7.

## 3. Curva del voto nel tempo
Non ricostruibile senza dati live (date di uscita + voti per titolo). `DA VERIFICARE`.
Ipotesi da testare (`HYPOTHESIS`): l'incumbent (Sly Flourish) è amato e stabile
sull'angolo "prep veloce"; gli entranti beginner recenti hanno **pochi voti** →
il posto "assoluto principiante + template pronti" sembra ancora poco presidiato.

## 4. La domanda
Segnali forti e convergenti (`WEB`, seconda fonte rispetto alle recensioni):
- **100.000+ nuovi giocatori D&D nel 2024**; oltre 50M hanno giocato a D&D.
- Mercato tabletop ~$13B nel 2024, CAGR ~9,1%. D&D è il leader di categoria.
- Ogni ondata di nuovi giocatori genera nuovi DM alle prime armi = il nostro avatar.
- L'incumbent con **1.600+ recensioni** dimostra che le guide di DM-prep si
  comprano in volume: la domanda esiste, non è teorica.
Suggerimenti di ricerca (completion API) **non raccolti** in questo ambiente → §7.

## 5. Il varco
`HYPOTHESIS` — Il best-seller (Sly Flourish) parla a chi **già masterizza** e
vuole prepararsi in meno tempo. Il nostro avatar è **una tacca prima**: non ha
ancora condotto la prima sessione, ha ansia da esordio, vuole tutto pronto.
Il varco: *"assoluto principiante + sistema step-by-step + template e checklist
inclusi + gestione dell'ansia della prima sessione"*. È coerente con titolo,
sottotitolo ("Fast Prep, Better Encounters, Confident Improvisation") e badge
"Templates & Checklists Included" già sulla copertina.
⚠️ Rischio: entriamo sul terreno "fast prep" dove l'incumbent è fortissimo. La
differenziazione deve stare tutta sul "prima volta / mano tenuta", non sul "lazy".

## 6. Verdetto
**DA VERIFICARE** (orientato al positivo).
- Domanda: **misurata e forte** (crescita nuovi giocatori + incumbent 1.600+ rec.).
- Varco: **plausibile ma non ancora dimostrato** con i numeri dei concorrenti.
- Manca il dato che trasforma "plausibile" in "aperto": review count e date dei
  competitor beginner recenti + curva del voto + volume dei suggerimenti.
Non è un SI FA pieno finché non ho quei numeri; non è un NON SI FA perché la
domanda c'è. → si prende il dato mancante (§7), poi si chiude.

## 7. Cosa resta da verificare (come prenderlo)
Serve una sessione con browser su Amazon.com US (o lo strumento `kdp_server.py`
di questo repo). Dati precisi da raccogliere:
1. **Tabella concorrenti live**: per i primi 15-25 risultati di "first time
   dungeon master" e "how to be a dungeon master" → ASIN, prezzo, voto, n.
   recensioni, data di uscita, n. pagine.
2. **Curva del voto per data di uscita** (il segnale chiave della skill).
3. **Domanda reale** dai suggerimenti (mercato US: `mid=ATVPDKIKX0DER`,
   host `completion.amazon.com`, `lop=en_US`): radici "how to dm", "dungeon
   master", "first d&d session", "dm prep", "dm tips" espanse lettera per lettera.
4. **Recensioni degli ASIN** in tabella → alimentano la validazione dell'avatar
   (`01 Ricerca/avatar-cliente.md`, oggi "presunto").

### Snippet suggerimenti (US) da eseguire nel browser
```js
const base = 'https://completion.amazon.com/api/2017/suggestions'
  + '?limit=11&alias=stripbooks&site-variant=desktop'
  + '&client-info=amazon-search-ui&mid=ATVPDKIKX0DER&lop=en_US'
  + '&page-type=Search&suggestion-type=KEYWORD&prefix=';
(await (await fetch(base + encodeURIComponent('how to dm'))).json())
  .suggestions.map(s => s.value)
```
Controllo anti-zero: interroga prima "dungeon" — se torna vuoto anche quello,
lo strumento è puntato male, non è il mercato a mancare.
