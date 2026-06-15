# KDP Studio — Deploy Online

## Architettura
```
GitHub repo (kdp-backend)  →  Railway (backend Python, sempre online)
GitHub repo (kdp-frontend) →  GitHub Pages (HTML statico, gratis)
```

---

## PARTE 1 — Backend su Railway (15 minuti)

### 1. Crea repo GitHub per il backend

Vai su github.com → New repository → nome: `kdp-backend` → Public → Create

Sul tuo PC, apri PowerShell nella cartella KDP Studio:
```powershell
cd "C:\Users\Gebruiker\Desktop\KDP\KDP Studio\kdp hunter"
git init
git add kdp_server.py requirements.txt Procfile railway.toml
git commit -m "KDP Studio backend"
git remote add origin https://github.com/TUO_USERNAME/kdp-backend.git
git push -u origin main
```

### 2. Deploy su Railway

1. Vai su **railway.app** → Login con GitHub
2. **New Project** → **Deploy from GitHub repo**
3. Seleziona `kdp-backend`
4. Railway detecta Python automaticamente e fa il deploy

### 3. Aggiungi variabili d'ambiente su Railway

Nel tuo progetto Railway → **Variables** → aggiungi:
```
ANTHROPIC_API_KEY = sk-ant-la-tua-chiave
REDDIT_USER_AGENT = KDPStudio/1.0 (personal use)
YOUTUBE_API_KEY = (opzionale) chiave YouTube Data API v3 — attiva YouTube Trending
                  come 3a fonte nella Scoperta Zero-Bias. Senza questa variabile
                  il tool funziona comunque con Reddit + Google Trends.
                  Ottienila gratis su console.cloud.google.com → abilita
                  "YouTube Data API v3" → crea credenziale "API key".
```

### 4. Copia il tuo URL Railway

Vai su **Settings** → **Domains** → copia l'URL tipo:
```
https://kdp-backend-production-xxxx.up.railway.app
```

---

## PARTE 2 — Frontend su GitHub Pages (10 minuti)

### 1. Aggiorna il frontend con il tuo URL Railway

Apri `kdp-trend-hunter.html` con Notepad, trova questa riga dentro `<head>`:
```html
<!-- Aggiungi questa riga con il TUO URL Railway -->
<meta name="kdp-backend" content="https://kdp-backend-production-xxxx.up.railway.app">
```
Incollala subito dopo il tag `<meta charset="UTF-8">`.

### 2. Crea repo GitHub per il frontend

```powershell
# Crea una nuova cartella
mkdir C:\KDPFrontend
copy "C:\Users\Gebruiker\Desktop\KDP\KDP Studio\kdp hunter\kdp-trend-hunter.html" C:\KDPFrontend\index.html
cd C:\KDPFrontend
git init
git add index.html
git commit -m "KDP Studio frontend"
git remote add origin https://github.com/TUO_USERNAME/kdp-frontend.git
git push -u origin main
```

### 3. Attiva GitHub Pages

Su github.com → repo `kdp-frontend` → **Settings** → **Pages**
→ Source: **main branch** → **Save**

Il tuo URL sarà:
```
https://TUO_USERNAME.github.io/kdp-frontend/
```

---

## Risultato finale

- **Frontend**: `https://TUO_USERNAME.github.io/kdp-frontend/` — sempre online, gratis
- **Backend**: `https://kdp-backend-production-xxxx.up.railway.app` — sempre online

### Costi
- GitHub Pages: **gratis** (illimitato)
- Railway free tier: **$5/mese di crediti gratis** — sufficiente per uso personale
  - Se superi i crediti: upgrade a $20/mese o usa **Render.com** (free tier con sleep)

---

## Aggiornare il codice in futuro

Ogni volta che modifichi il backend:
```powershell
cd "C:\Users\Gebruiker\Desktop\KDP\KDP Studio\kdp hunter"
git add kdp_server.py
git commit -m "update"
git push
```
Railway fa il redeploy automaticamente in 1-2 minuti.

Per il frontend:
```powershell
copy "kdp-trend-hunter.html" C:\KDPFrontend\index.html
cd C:\KDPFrontend
git add index.html
git commit -m "update frontend"
git push
```
GitHub Pages si aggiorna in 30 secondi.

---

## Alternativa: tutto su Railway (più semplice)

Se vuoi evitare GitHub Pages, puoi servire anche l'HTML dal backend Python.
Aggiungere al server:
```python
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")
```
E mettere `kdp-trend-hunter.html` → `index.html` nella stessa cartella del server.
Così hai un solo URL per tutto.

