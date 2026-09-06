# Report di nicchia — rabbia-genitoriale
Fase 1 · Amazon.it, italiano · aggiornato il 06/09/2026

## Indice
1. Verdetto
2. Come e' stata misurata la domanda
3. La domanda che esiste
4. I concorrenti trovati
5. L'errore di lettura che ho fatto, e perche'
6. Cosa manca per un verdetto completo
7. Se si volesse insistere lo stesso
8. Come rifare questa misura
9. Correzione del 06/09: il segnale «+libro» era falso

---

## 1. Verdetto

**NON SI FA**, nella formulazione «educare senza urlare / come non urlare ai figli».

Non perche' manchi la domanda: la domanda c'e'. Perche' lo scaffale e' gia'
occupato da almeno dieci libri che dicono la stessa cosa alla stessa persona
con lo stesso sottotitolo, e almeno due di questi hanno dietro un editore vero.

Un libro fermato oggi costa una giornata. Lo stesso libro fermato dopo il
manoscritto costa tre mesi.

## 2. Come e' stata misurata la domanda

Sorgente: autocomplete del reparto Libri di Amazon.it
(`completion.amazon.it`, mid `APJ6JRA9NG5V4`, alias `stripbooks`).
E' cio' che i lettori digitano davvero nella barra di ricerca.

Due passaggi:

| Passaggio | Chiamate | Query uniche | Cosa cercava |
|---|---|---|---|
| Mappa generale | 2.118 | 89 | quali problemi si cercano su Amazon.it |
| Approfondimento nicchia | 510 | **17** | quanto e' larga *questa* nicchia |

Le 17 query da 510 chiamate sono gia' un dato, e non buono: il linguaggio di
questa nicchia e' **stretto** nell'indice di Amazon. Per confronto, la sola
radice «come non » ne aveva prodotte 23 da sola.

Dati grezzi: `harvest_demand.py --market it` alla radice del repo.

## 3. La domanda che esiste

Query nude, senza titolo o autore attaccato:

- `come non urlare ai figli`
- `come non crescere degli str[onzi]`
- `come non reagire alle provocazioni`
- `capricci libro` ← il suffisso «libro». **Lo avevo letto come segnale di
  vuoto: era sbagliato, vedi §9.**
- `capricci istruzioni per l'uso`, `capricci e regole`, `capricci non nemici`

Query che arrivano **con un autore attaccato** — cioe' ricerche gia' possedute
da un titolo preciso:

- `educare senza urlare camilla moreno`
- `educare senza urlare moreno marchetti`
- `educare senza urlare kindle`, `educare senza urlare libro`
- `educare con calma ed ikigai`

Quando Amazon suggerisce il nome dell'autore dopo il tema, quel tema ha gia'
un padrone. Qui ne ha piu' di uno.

## 4. I concorrenti trovati

Cercati fuori da Amazon (la pagina di ricerca amazon.it e' irraggiungibile da
qui, vedi §6), quindi l'elenco e' **parziale per difetto**: sono quelli
emersi in due sole ricerche, non un censimento.

Pen name in stile KDP, stesso posizionamento, stessa formula di sottotitolo:

| Autore | Titolo |
|---|---|
| Moreno, Camilla + Marchetti, Dario | Educare Senza Urlare: 4 Libri in 1 |
| Merini, Letizia | Educare Senza Urlare: 4 libri in 1 (e un secondo titolo) |
| Monte, Michela | Educare Senza Urlare: Guida Definitiva per Genitori Esauriti |
| Ferro, Beatrice | Educare senza Urlare: La chiave per una Disciplina Positiva |
| Speranza, Lucia | Educare i Figli Senza Urlare (dichiarato Vol. 1 di una serie) |
| De Rossi, Daniele | Educare Senza Urlare (metodo Montessori) |
| Ferrer Pinto, Carla | Educare senza Urlare (guida pratica) |
| Frost, Lula | Mamma non urlare |
| Marchetti, Allegra | Mamma non Urlare |
| Panozzo, Giulia | ORA BASTA! Come smettere di urlare |

Con dietro un editore vero, non autopubblicati:

| Autore | Titolo | Editore |
|---|---|---|
| Naumburg, Carla | Smettila di urlare | tradotto, ISBN 8822736478 |
| Dunn, Jancee | Come non odiare tuo marito dopo i figli | Sonzogno, 2017 |
| Novara, Daniele | Urlare non serve a nulla | marchio noto in Italia |

Dieci pen name che si contendono la stessa frase, e tre ancore con
distribuzione in libreria. Non e' un vuoto: e' una rissa.

Il colpo piu' duro e' il sottotitolo di Michela Monte, che copre gia'
letteralmente l'angolo che avevo ipotizzato scoperto: *«per Genitori
Esauriti … Evitando Capricci. Tecniche per il Controllo della Rabbia»*.

## 5. L'errore di lettura che ho fatto, e perche'

Avevo presentato questa nicchia con due query «nude» come punto di forza,
scrivendo che nessun libro le possedeva.

Su `come non odiare tuo marito dopo i figli` era **sbagliato**, ed era
sbagliato il ragionamento, non solo la conclusione. Quella query arrivava
nuda per il motivo opposto a quello che avevo dedotto: *e'* un titolo, quello
di Jancee Dunn per Sonzogno, e chi la digita sta cercando quel libro per nome.

La regola che ne esce, e che vale per ogni misura futura:

> Una query senza autore attaccato non e' una query libera. Puo' essere una
> query cosi' famosa da non aver bisogno del nome dell'autore. Prima di
> chiamarla vuota, si cerca il titolo.

Registrato anche nel dossier di metodo: era una conclusione che stava per
decidere l'investimento, e andava verificata da due angoli prima di essere
scritta come fatto. L'ho verificata al secondo angolo, non al primo.

## 6. Cosa manca per un verdetto completo

Manca la meta' quantitativa, e va detto invece di essere colmato a stima:

- **prezzi** dei concorrenti
- **numero e andamento delle recensioni** (la curva di declino)
- **BSR** e la sua tendenza
- il **conteggio totale** dei libri sulla query

Nessuno di questi e' ottenibile da qui: `www.amazon.it/s` risponde **503** sia
via richiesta diretta sia via recupero pagina, perche' l'IP e' di datacenter.
Le due strade per averli sono il backend su Railway con le chiavi Apify, o un
controllo manuale su Amazon.it.

Il verdetto di §1 **non dipende** da questi numeri: dieci concorrenti diretti
con lo stesso posizionamento bastano da soli. Quei numeri servirebbero solo a
misurare *quanto* e' saturo, non *se*.

## 7. Se si volesse insistere lo stesso

Avevo indicato uno spiraglio in `capricci libro`, sulla base del suffisso
«libro». **Quello spiraglio non esiste**: il segnale su cui poggiava si e'
rivelato falso il giorno stesso, vedi §9. E il sottotitolo di Monte contiene
comunque gia' «Evitando Capricci».

Non resta nessuno spiraglio in questa nicchia.

## 8. Come rifare questa misura

```
python3 harvest_demand.py --market it --out domanda-it.json
```

Il file di uscita e' generato, non sorgente: non si modifica a mano. Se il
totale torna zero, e' lo strumento puntato male, non il mercato vuoto —
`python3 test_amazon_markets.py` lo dice in trenta secondi.

## 9. Correzione del 06/09: il segnale «+libro» era falso

Questo report, nella sua prima stesura, trattava il suffisso «libro» in una
query come segnale di vuoto di mercato. La misura della nicchia successiva
(`progetti/autosabotaggio`) lo ha smentito: `autosabotaggio libri`,
`vittimismo libro` e `procrastinazione libro` hanno rispettivamente sei, tre e
sei libri, con bestseller da editore in cima.

La causa vera e' che su Amazon.it l'alias `stripbooks` non filtra ai soli
libri — lo stesso difetto per cui la radice «guida per» restituiva box doccia.
Chi vuole un libro aggiunge «libro» perche' il filtro del reparto e' rotto,
non perche' il libro manchi.

Il verdetto NON SI FA di §1 **non cambia**: non poggiava su quel segnale ma
sui dieci concorrenti diretti e sulle tre ancore con editore. Cambia il §7:
lo spiraglio indicato li' non esiste.
