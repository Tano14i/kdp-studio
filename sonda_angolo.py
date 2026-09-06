#!/usr/bin/env python3
"""Sonda un ANGOLO su Amazon.it, non un tema. E' la verifica del passo 1b.

`ricerca-inversa` §4 dice che l'angolo trovato nei commenti e' un'ipotesi
finche' non e' verificato sullo scaffale. Questo script prende quella verifica
e la fa a macchina, con i due soli canali che dal contenitore rispondono
davvero:

  1. completion.amazon.it — l'autocomplete del reparto Libri, interrogato a
     scala di prefissi (vedi `scandaglia`). Dice se la lingua dell'angolo
     esiste nell'indice di Amazon e se ha gia' un padrone (quando il
     suggerimento arriva col nome dell'autore attaccato).

     ATTENZIONE a cosa NON dice: l'autocomplete indicizza solo query con
     abbastanza volume, e un angolo sta sotto quella soglia per definizione.
     Un angolo muto qui non e' un angolo senza mercato — e' lo strumento
     sbagliato per la domanda. E' l'autocomplete che ha prodotto cinque
     NON SI FA di fila (note-mercato.md §1 e §4): usarlo per giudicare un
     angolo ne produrrebbe un sesto per costruzione. Serve a misurare chi
     occupa la testa della domanda, non a bocciare la coda.
  2. www.amazon.it/dp/<ASIN> — la scheda di un libro gia' noto. Da' titolo,
     valutazione, numero di recensioni e prezzo, cioe' quanto e' occupata la
     casella, non solo se lo e'.

CIO' CHE QUESTO SCRIPT NON PUO' FARE, e che va preso dal browser dell'autore
con `scheda-raccolta.md`:

  - la pagina di ricerca `www.amazon.it/s` risponde 503 (IP di datacenter):
    quindi non si scoprono ASIN nuovi, si misurano solo quelli gia' noti;
  - `www.amazon.it/product-reviews/...` risponde con la pagina anti-robot:
    niente testo delle recensioni, quindi niente BSR e niente curva.

    python3 sonda_angolo.py --frasi frasi.txt --asin 8845410048,885902420X \
        --out "progetti/<nicchia>/01 Ricerca/dati-angolo.json"

Il file di uscita e' GENERATO: non si modifica a mano. Se il report e il file
divergono, ha ragione il file — `regia` §10.
"""
import argparse, json, pathlib, random, re, sys, time, html
import urllib.parse, urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36")

# Mercato italiano. Il mid sbagliato non da' errore: da' zero suggerimenti,
# che si legge come "nessuna domanda". Vedi note-mercato.md §6.
MID_IT = "APJ6JRA9NG5V4"
SUGGEST = ("https://completion.amazon.it/api/2017/suggestions"
           "?mid={mid}&alias=stripbooks&prefix={prefix}"
           "&client-info=amazon-search-ui&limit=11")

# La scheda prodotto risponde davvero circa una volta su quattro: le altre
# tornano la pagina anti-robot, che pesa meno di 10 KB. La soglia distingue le
# due cose senza doverle interpretare.
PAGINA_VERA_MIN_BYTE = 50_000


def _get(url: str, timeout: int = 25) -> bytes:
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept-Language": "it-IT,it;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/json",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _suggerisci(prefisso: str) -> list[str]:
    url = SUGGEST.format(mid=MID_IT, prefix=urllib.parse.quote(prefisso))
    for tentativo in range(3):
        try:
            dati = json.loads(_get(url, timeout=15).decode("utf-8", "replace"))
            return [s.get("value", "") for s in dati.get("suggestions", [])]
        except Exception:
            time.sleep(1 + tentativo)
    return []


def scandaglia(frase: str, minimo: int = 8) -> dict:
    """Scala di prefissi, dal piu' lungo al piu' corto, finche' uno risponde.

    Interrogare l'autocomplete con la frase intera e leggere lo zero come
    "nessuna domanda" e' l'errore gia' commesso e registrato due volte in
    questo repo: l'autocomplete completa per prefisso, e una frase gia'
    completa non ha continuazioni per costruzione. Quindi non si chiede una
    volta sola: si accorcia finche' qualcosa torna, e si scrive QUALE
    prefisso ha risposto.

    Cosi' i due zeri diventano distinguibili:
      - `esito: "muto"`   nessun prefisso risponde, nemmeno corto → la lingua
        dell'angolo non e' nell'indice di Amazon;
      - `esito: "risale"` risponde solo un prefisso piu' corto → la frase
        esiste come tema ma non con le parole dell'angolo.
    """
    prefissi = []
    p = frase.strip()
    while len(p) >= minimo:
        prefissi.append(p)
        p = p[:-3].rstrip()
    for prefisso in prefissi:
        trovati = _suggerisci(prefisso)
        time.sleep(0.3)
        if trovati:
            return {
                "prefisso_che_risponde": prefisso,
                "suggerimenti": trovati,
                "esito": "intera" if prefisso == frase.strip() else "risale",
            }
    return {"prefisso_che_risponde": None, "suggerimenti": [], "esito": "muto"}


def _testo(frammento: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", frammento))).strip()


def scheda(asin: str, tentativi: int = 8) -> dict:
    """Numeri di una scheda gia' nota. Ritenta: la maggior parte delle
    risposte e' la pagina anti-robot, e distinguerle dalla dimensione e'
    piu' onesto che fingere che non succeda."""
    url = f"https://www.amazon.it/dp/{asin}"
    ultima_corta = b""
    ultimo_codice = None
    for tentativo in range(tentativi):
        try:
            grezzo = _get(url)
        except urllib.error.HTTPError as e:
            # urllib solleva su 4xx/5xx: senza catturare il codice, un 404
            # (ASIN sbagliato) e un 503 (blocco) diventano lo stesso errore.
            ultimo_codice, grezzo = e.code, b""
        except Exception:
            grezzo = b""
        if len(grezzo) < PAGINA_VERA_MIN_BYTE:
            ultima_corta = grezzo
        if len(grezzo) >= PAGINA_VERA_MIN_BYTE:
            s = grezzo.decode("utf-8", "replace")
            def primo(pattern, gruppo=1):
                m = re.search(pattern, s, re.S)
                return _testo(m.group(gruppo))[:300] if m else None
            prezzi = sorted(set(re.findall(r'"displayPrice":"([^"]+)"', s)))
            nrec = primo(r'id="acrCustomerReviewText"[^>]*>(.*?)</span>')
            return {
                "asin": asin,
                "titolo": primo(r'id="productTitle"[^>]*>(.*?)</span>'),
                "valutazione": primo(r'id="acrPopover"[^>]*title="([^"]*)"'),
                "recensioni": re.sub(r"[^\d]", "", nrec) if nrec else None,
                "prezzo": prezzi[0] if prezzi else None,
                "tentativi": tentativo + 1,
                "letto_il": time.strftime("%Y-%m-%d"),
            }
        time.sleep(2 + random.random() * 3)

    # Le pagine corte non sono tutte la stessa cosa, e chiamarle tutte
    # "anti-robot" e' un avviso che mente: manderebbe a ritentare un ASIN che
    # semplicemente non esiste. Le due si distinguono dal contenuto.
    corpo = ultima_corta.decode("utf-8", "replace")
    if ultimo_codice == 404:
        causa = ("404: nessun libro con questo ASIN su amazon.it — ritentare NON "
                 "serve, l'ASIN e' sbagliato o e' di un'altra edizione")
    elif ultimo_codice:
        causa = f"HTTP {ultimo_codice} su {tentativi} tentativi"
    elif "api-services-support@amazon.com" in corpo or "captcha" in corpo.lower():
        causa = f"pagina anti-robot su {tentativi} tentativi — ritentare puo' servire"
    elif ultima_corta:
        causa = (f"ASIN inesistente su amazon.it (risposta di {len(ultima_corta)} byte, "
                 f"senza marcatore anti-robot) — ritentare NON serve, l'ASIN e' sbagliato")
    else:
        causa = f"nessuna risposta in {tentativi} tentativi"
    return {"asin": asin, "errore": causa}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--frasi", help="file con una frase per riga, come la direbbe il lettore")
    p.add_argument("--asin", default="", help="ASIN/ISBN separati da virgola")
    p.add_argument("--out", required=True, help="file JSON di uscita (generato)")
    a = p.parse_args()

    frasi = []
    if a.frasi:
        frasi = [r.strip() for r in pathlib.Path(a.frasi).read_text(encoding="utf-8").splitlines()
                 if r.strip() and not r.startswith("#")]
    asins = [x.strip() for x in a.asin.split(",") if x.strip()]

    lingua = {}
    for f in frasi:
        lingua[f] = scandaglia(f)
        e = lingua[f]
        print(f"  [{e['esito']:6}] {f}"
              + (f"  <- {e['prefisso_che_risponde']!r}: {e['suggerimenti']}"
                 if e["suggerimenti"] else ""), file=sys.stderr)

    # Una scheda gia' letta non si perde perche' oggi Amazon ha bloccato il
    # tentativo: la lettura riuscita ieri resta vera. Senza questo, ogni
    # rigenerazione cancellerebbe a caso qualche riga del report — e la regola
    # e' che quando il file e il report divergono ha ragione il file, quindi un
    # file che dimentica farebbe cancellare misure vere.
    precedenti = {}
    dest = pathlib.Path(a.out)
    if dest.exists():
        try:
            for vecchia in json.loads(dest.read_text(encoding="utf-8")).get("schede", []):
                if vecchia.get("titolo"):
                    precedenti[vecchia["asin"]] = vecchia
        except (OSError, ValueError):
            pass

    schede = []
    for asin in asins:
        s = scheda(asin)
        if not s.get("titolo") and asin in precedenti:
            s = dict(precedenti[asin], ripreso_da_lettura_precedente=True,
                     errore_di_oggi=s.get("errore"))
            print(f"  {asin}: {s['titolo'][:60]} (lettura del {s.get('letto_il')}, "
                  f"oggi {s['errore_di_oggi']})", file=sys.stderr)
        else:
            print(f"  {asin}: {s.get('titolo') or s.get('errore')}", file=sys.stderr)
        schede.append(s)

    out = {
        "generato_il": time.strftime("%Y-%m-%d %H:%M"),
        "mercato": "amazon.it",
        "lingua_dell_angolo": lingua,
        "schede": schede,
        "limiti": [
            "www.amazon.it/s risponde 503: nessun ASIN nuovo si scopre da qui",
            "www.amazon.it/product-reviews risponde anti-robot: niente testo recensioni ne' BSR",
        ],
    }
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    vuote = [f for f, s in lingua.items() if s["esito"] == "muto"]
    print(f"\nScritto {dest}", file=sys.stderr)
    print(f"  frasi sondate: {len(lingua)}, di cui senza alcun suggerimento: {len(vuote)}",
          file=sys.stderr)
    print(f"  schede lette: {sum(1 for s in schede if s.get('titolo'))}/{len(schede)}",
          file=sys.stderr)
    if vuote:
        print("  ATTENZIONE — frasi mute a ogni lunghezza di prefisso. Non e' una "
              "misura di domanda:\n  l'autocomplete indicizza solo cio' che ha "
              "volume, e un angolo per definizione\n  sta sotto quella soglia. "
              "Vedi note-mercato.md §4.", file=sys.stderr)
        for f in vuote:
            print(f"    - {f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
