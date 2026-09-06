# KDP Studio — Agent Skills

Portable [Agent Skills](https://github.com/higgsfield-ai/skills) (open `SKILL.md`
standard) that package KDP Studio workflows so they run on the **Higgsfield
Supercomputer**, **Claude Code**, **Cursor**, or **Codex** — and act as a
**connector** to a running KDP Studio backend.

## Skills

| Skill | What it does |
|------|--------------|
| `fabio-kdp` | End-to-end coach for a full-content KDP book: niche → positioning → outline → drafting → listing + compliance gate → AI cover. Chains to `higgsfield-generate` for the cover and to the KDP Studio API for the heavy LLM stages. |
| `regia` | Dirige il progetto: legge il dossier, capisce a che punto siamo, chiama la skill giusta e si ferma ai sette checkpoint. Copia versionata nel repo, ed è l'unica buona — vedi **`regia` vive qui** più sotto. |
| `ricerca-inversa` | Cerca l'**angolo** libero invece del tema libero: parte dai contenuti che girano e dai commenti sotto, e piega un tema occupato su un pubblico, un momento o un uso scoperti. La chiama `regia` come passo 1b, quando `ricerca-nicchia` chiude con NON SI FA. |
| `promozione-social` | Porta un libro **gia' pubblicato** davanti ai lettori su Instagram, TikTok e Facebook, in organico e senza mostrare il volto: identita' del pen name, tre format ripetibili, piano editoriale a 30 giorni, ponte verso la scheda Amazon e regole di taglio a 14 e 30 giorni. E' la fase che il metodo non copriva — dopo `pubblicazione-kdp`. |

## Install

These skills live in **`.claude/skills/`** inside the repo, so Claude Code
discovers them automatically as **project skills** whenever the repo is open —
including fresh Claude Code on the web sessions. No symlink or setup hook is
required: clone the repo, type `/fabio-kdp`, done.

**Other agents** (Cursor, Codex) that read `~/.<agent>/skills/<name>/SKILL.md`:

```bash
# from the repo root
mkdir -p ~/.cursor/skills   # or ~/.codex/skills
ln -s "$(pwd)/.claude/skills/fabio-kdp" ~/.cursor/skills/fabio-kdp
```

**Higgsfield Supercomputer** — use the official installer/marketplace flow:

```bash
curl -fsSL https://raw.githubusercontent.com/higgsfield-ai/cli/main/install.sh | sh
# then add this skill folder to your skills set, or publish it to the
# Supercomputer Skills Marketplace following higgsfield-ai/skills CONTRIBUTING.md
```

## Connector configuration

To offload the LLM-heavy stages to a running KDP Studio backend, set:

```bash
export KDP_STUDIO_URL="https://web-production-e6914.up.railway.app"
export KDP_API_KEY="..."   # only if the backend has KDP_API_KEY enabled
```

For the AI cover, the skill prefers the `higgsfield-generate` skill. The KDP
Studio `/api/generate-cover` endpoint is an alternative that uses Higgsfield
**Cloud** credits (separate from the Supercomputer subscription).

## `regia` vive qui — deciso il 06/09/2026

`regia` nasceva come skill dell'account, sincronizzata dentro la sessione in
`~/.claude/skills/synced/`. Quella cartella non è git: è una copia scaricata
all'avvio, che sparisce quando il contenitore viene riciclato e che il sync
successivo riscrive. Una modifica fatta lì dura una sessione e poi non esiste
più.

Serviva invece che la regia conoscesse le due skill nuove del repo. Per questo
`regia` è stata copiata qui e modificata qui, e **questa è da oggi l'unica
versione buona.**

### Le tre modifiche

1. **passo 1b** — `ricerca-inversa` entra nella mappa dopo `ricerca-nicchia`;
2. **il cancello del verdetto** — un `NON SI FA` sul tema non chiude più il
   progetto, lo manda al 1b. Si chiude solo se non regge nessuna delle quattro
   pieghe, e allora quel no vale di più: sono stati provati quattro angoli
   invece di zero;
3. **passo 14** — `promozione-social`. La mappa finiva alla pubblicazione, ed
   era un buco, non una scelta.

### Perché nel repo e non nell'account

Non perché le skill che la regia chiama vivano qui: **non è vero, e in una
versione precedente di questa nota c'era scritto il contrario.** I conti veri:

| Dove vive | Quante | Quali |
|---|---|---|
| Account | 9 | `progetto-libro` `ricerca-nicchia` `avatar-cliente` `concept-positioning` `outline-libro` `dna-stilistico` `revisione-manoscritto` `pubblicazione-kdp` `higgsfield-kdp-book` |
| Repo | 2 | `ricerca-inversa` `promozione-social` |

Nove su undici stanno nell'account. La ragione vera è un'altra, ed è doppia:

- **i progetti libro stanno in `progetti/`, dentro questo repo.** Per lavorare
  a un libro il repo si apre comunque, quindi la regia del repo è quella che
  viene caricata quando serve davvero;
- **una regia versionata ha una storia.** Le regole che contiene — il cancello
  del verdetto, «prima di credere a uno zero verifica di aver interrogato la
  cosa giusta», la verifica che copre tutto e mai un campione — sono nate da
  errori pagati. Vederle cambiare nel tempo, con il commit che spiega perché,
  vale più che averle in un posto solo.

### Il passo che resta da fare a mano

**Cancellare `regia` dalle skill dell'account, su claude.ai.** Non si può fare
da una sessione: qui si vede solo la copia sincronizzata, e cancellare quella
non cancella niente — al sync successivo torna.

Finché quella esiste, la situazione è questa:

| Dove lavori | Quale regia viene caricata | Conosce 1b e 14? |
|---|---|---|
| dentro `kdp-studio` | **questa** | sì |
| fuori da `kdp-studio` | quella dell'account | **no** |

Non è un conflitto e non rompe niente: dentro il repo vince questa. Il rischio
è più avanti — aprire la regia da un'altra parte fra sei mesi, non vedere il
passo 14, e non ricordare perché.
