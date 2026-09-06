# KDP Studio — Agent Skills

Portable [Agent Skills](https://github.com/higgsfield-ai/skills) (open `SKILL.md`
standard) that package KDP Studio workflows so they run on the **Higgsfield
Supercomputer**, **Claude Code**, **Cursor**, or **Codex** — and act as a
**connector** to a running KDP Studio backend.

## Skills

| Skill | What it does |
|------|--------------|
| `fabio-kdp` | End-to-end coach for a full-content KDP book: niche → positioning → outline → drafting → listing + compliance gate → AI cover. Chains to `higgsfield-generate` for the cover and to the KDP Studio API for the heavy LLM stages. |
| `regia` | Dirige il progetto: legge il dossier, capisce a che punto siamo, chiama la skill giusta e si ferma ai sette checkpoint. Copia versionata nel repo — vedi **Nota su `regia`** più sotto. |
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

## Nota su `regia`

`regia` esisteva già come skill dell'account, sincronizzata in
`~/.claude/skills/synced/`. La copia qui dentro è la stessa, con tre
modifiche che servono a far conoscere alla regia le due skill nuove del repo:

1. **passo 1b** — `ricerca-inversa` entra nella mappa dopo `ricerca-nicchia`;
2. **il cancello del verdetto** — un `NON SI FA` sul tema non chiude più il
   progetto, lo manda al 1b. Si chiude solo se non regge nessuna delle quattro
   pieghe;
3. **passo 14** — `promozione-social`, perché la mappa finiva alla
   pubblicazione e quello era un buco.

**Attenzione alla duplicazione.** Finché esiste anche la copia sincronizzata
dell'account, ci sono due `regia` con contenuto diverso, e quella dell'account
non conosce né `ricerca-inversa` né `promozione-social`. Due strade, una va
scelta:

- **portare le tre modifiche nella skill dell'account** e cancellare questa
  copia — sensato se `regia` deve valere anche fuori da kdp-studio;
- **tenere questa e togliere quella dall'account** — sensato se `regia` è di
  fatto la regia *di questo repo*, visto che le skill che chiama vivono qui.

La seconda è più coerente con dove stanno le cose oggi, ma è una decisione
dell'autore e non va presa di nascosto.
