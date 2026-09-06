# Scheda di raccolta concorrenti — Amazon.it
Da compilare nel browser, con l'estensione KDP attiva · aggiornato il 06/09/2026

## Indice
1. A cosa serve e perche' non e' automatizzabile
2. Cosa aprire
3. Cosa copiare — parte A, i numeri
4. Cosa copiare — parte B, le recensioni (la parte che conta)
5. Dove mettere quello che raccogli
6. Cosa ne ricavo io

## 1. A cosa serve e perche' non e' automatizzabile

Tre nicchie si sono chiuse con NON SI FA perche' manca sempre lo stesso dato:
prezzi, recensioni, BSR dei concorrenti. Senza, non si distingue un tema
occupato **bene** da uno occupato **male**, e ogni nicchia sembra chiusa.

Dal contenitore di sviluppo quel dato non si raggiunge:

| Strada | Esito |
|---|---|
| richiesta diretta a `www.amazon.it/s` | **503** (IP di datacenter) |
| recupero pagina | **503** |
| Chromium via proxy del container | **connessione resettata su ogni host**, anche example.com |
| backend su Railway con Apify | disponibile, ma serve la chiave e il redeploy |

Il tuo browser invece e' un browser normale, con la tua estensione KDP che
mostra BSR e recensioni gia' nella pagina dei risultati. Venti minuti li'
valgono piu' di qualunque altra cosa io possa tentare da qui.

## 2. Cosa aprire

**Aggiornato il 06/09 sera.** Le tre nicchie elencate qui prima erano scelte
per *tema*. Adesso due progetti hanno un **angolo** candidato (passo 1b), e la
ricerca cambia bersaglio: non piu' «quanti libri ci sono su questo tema», ma
**«qualcuno vende gia' questo angolo?»**. E' una domanda a cui si risponde in
venti minuti, e finche' non ha risposta i due progetti restano fermi.

Scegli **un** progetto e falla intera. Meglio uno completo che due a meta'.

### A — autosabotaggio, angolo «adulto con ADHD» (consigliato)

`progetti/autosabotaggio/01 Ricerca/01b-angolo.md`. E' il consigliato perche'
il tema ha la miglior combinazione crescita+volume gia' misurata (indice 2,59,
277.000 visite/anno) e perche' la domanda decisiva si risponde contando.

- https://www.amazon.it/s?k=adhd+adulti&i=stripbooks
- https://www.amazon.it/s?k=adhd+adulti&i=stripbooks&s=review-rank
- https://www.amazon.it/s?k=procrastinazione+adhd&i=stripbooks
- https://www.amazon.it/s?k=adhd+donne+adulte&i=stripbooks

**La domanda che decide:** dei libri che escono, quanti sono **clinici**
(manuale, diagnosi, per professionisti o genitori di bambini) e quanti sono
**pratici per l'adulto che ce l'ha**? Se in mezzo non c'e' niente, l'angolo e'
vero. Segna accanto a ogni riga `clinico` o `pratico`.

**Da controllare in piu':** `adhd adulti` arriva dall'autocomplete senza nome
d'autore attaccato. In questo repo una query nuda ha gia' ingannato due volte
perche' *era* un titolo. Guarda se esiste un libro che si chiama cosi'.

### B — rabbia-genitoriale, angolo «il dopo, non il prima»

`progetti/rabbia-genitoriale/01 Ricerca/01b-angolo.md`. Tredici concorrenti
vendono tutti «come non urlare». L'angolo e' cosa si fa **dopo**.

- https://www.amazon.it/s?k=dopo+aver+urlato+ai+figli&i=stripbooks
- https://www.amazon.it/s?k=senso+di+colpa+genitori&i=stripbooks
- https://www.amazon.it/s?k=chiedere+scusa+ai+figli&i=stripbooks
- https://www.amazon.it/s?k=riparare+rapporto+con+i+figli&i=stripbooks

**La domanda che decide:** qualcuno vende gia' il dopo invece del prima? Qui
un risultato **vuoto o fuori tema e' una buona notizia**, ed e' il contrario
di come si leggono le altre ricerche di questa scheda.

**Da controllare in piu':** gli ASIN veri di *Urlare non serve a nulla*
(Novara) e *Come non odiare tuo marito dopo i figli* (Dunn). Quelli dedotti
dagli ISBN di Goodreads rispondono 500, quindi le loro righe nella tabella dei
numeri sono vuote. Basta l'URL della pagina Amazon.

### Endometriosi: non piu' in lista

Era la prima delle tre, ed era la piu' promettente. **Sospesa il 06/09 sera
per decisione dell'autore: tema troppo medico** — vedi
`progetti/endometriosi/00-dossier-metodo.md` §7. I collegamenti e i tre ASIN
restano scritti li' dentro, se un giorno riparte.

### Se cerchi per tema e non per angolo

Vale ancora la regola vecchia: il terzo collegamento ordinato per novita'
(`&s=date-desc-rank`) dice se la nicchia si sta riempiendo adesso. Se i primi
risultati sono tutti degli ultimi sei mesi, ci stanno entrando in molti
proprio ora.

## 3. Cosa copiare — parte A, i numeri

**Primi 10 libri** della prima pagina. Una riga per libro, campi separati da
punto e virgola:

```
asin;titolo;autore;prezzo_cartaceo;prezzo_kindle;n_recensioni;stelle;bsr;data_pubblicazione;pagine
```

- **asin** — sta nell'URL del libro dopo `/dp/`
- **bsr** — il numero di Bestseller in Libri, quello che l'estensione mostra
  in pagina; se ne mostra due, prendi quello generale di «Libri»
- **data_pubblicazione** — serve per la curva: un libro del 2019 con 400
  recensioni e uno del 2026 con 40 dicono cose molto diverse
- se un campo non lo trovi scrivi `?`, **non lasciarlo vuoto e non inventarlo**

Un'assenza dichiarata la so gestire; un numero inventato mi fa sbagliare il
verdetto, ed e' esattamente il modo in cui questa giornata e' gia' andata
storta tre volte.

## 4. Cosa copiare — parte B, le recensioni (la parte che conta)

**Questa e' la parte che vale il viaggio.** I numeri dicono se la nicchia e'
affollata; le recensioni dicono se e' affollata di libri *buoni*.

Prendi i **3 libri con piu' recensioni** e per ciascuno apri le recensioni
filtrate a **1, 2 e 3 stelle** (nella pagina del libro: «Vedi tutte le
recensioni» → filtro per stelle).

Copia **10-15 recensioni negative per libro**, testo intero, cosi' come sono.
Non riassumerle: le parole esatte del lettore sono il materiale grezzo
dell'avatar, e un riassunto le rende inservibili.

Cerchi in particolare le frasi che cominciano cosi':
- «mi aspettavo che parlasse di…»
- «troppo generico / tutto gia' sentito»
- «sembra scritto con l'AI / riempitivo»
- «niente di pratico»
- «non parla mai di…»

Quelle frasi sono il vuoto. Non e' un tema che manca: e' una **promessa non
mantenuta** dai libri che ci sono gia'.

## 5. Dove mettere quello che raccogli

```
progetti/<nicchia>/01 Ricerca/concorrenti.csv     <- la parte A
progetti/<nicchia>/01 Ricerca/recensioni-negative.txt  <- la parte B
```

Per le recensioni separa un libro dall'altro con una riga cosi':

```
=== ASIN B0XXXXXXXX — Titolo del libro ===
```

Oppure incollamele direttamente in chat: le sistemo io nei file giusti.

## 6. Cosa ne ricavo io

Dalla parte A, subito: fascia di prezzo reale, densita' di concorrenza, curva
di declino delle recensioni, eta' media dei titoli e ritmo di ingresso di
nuovi libri. Cioe' la meta' quantitativa che manca alla fase 1, e un verdetto
con i numeri accanto invece che senza.

Dalla parte B: la fase 2, `avatar-cliente`. Le lamentele che si ripetono su
libri diversi sono i capitoli del tuo, e l'ordine in cui si ripetono e'
l'ordine dell'indice.

Bastano **una nicchia, dieci libri e tre liste di recensioni** per far ripartire
tutto il metodo.
