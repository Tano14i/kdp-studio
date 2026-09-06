# Generatore slide — Martina Riva

`slides-martina-riva.py` produce le slide dei caroselli social in HTML e le
renderizza in PNG 1080×1920 con Chromium headless. Nasce come sostituto dei
template Blotato, che ignoravano il font richiesto, lasciavano due terzi del
frame vuoto e stampavano boilerplate in inglese («Written by …») su contenuti
italiani.

## Uso

```sh
# 1. font (una volta sola)
curl -s "https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Lato:wght@300;400;700&display=swap" -o f.css
# scaricare i .ttf da f.css in ~/.fonts, poi:
fc-cache -f

# 2. generare l'HTML
python3 slides-martina-riva.py

# 3. renderizzare
CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
for f in build/*.html; do
  "$CHROME" --headless --disable-gpu --no-sandbox --hide-scrollbars \
    --force-device-scale-factor=1 --window-size=1080,1920 \
    --screenshot="${f%.html}.png" "file://$PWD/$f"
done
```

## Design

Palette presa dalla copertina del libro: crema `#FAF3E6` → `#EFE0C6`, oro
`#C9A227`, testo `#2B2118`. Titoli in Playfair Display, testo in Lato.
Farfalla in SVG, quattro ali speculari, coerente con l'illustrazione di
copertina.

Le costanti di contenuto (`TYPES`, `QUOTES`) stanno in fondo al file: per una
nuova serie si modificano quelle e si rilancia.
