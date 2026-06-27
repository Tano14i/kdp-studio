# KDP Studio — Agent Skills

Portable [Agent Skills](https://github.com/higgsfield-ai/skills) (open `SKILL.md`
standard) that package KDP Studio workflows so they run on the **Higgsfield
Supercomputer**, **Claude Code**, **Cursor**, or **Codex** — and act as a
**connector** to a running KDP Studio backend.

## Skills

| Skill | What it does |
|------|--------------|
| `fabio-kdp` | End-to-end coach for a full-content KDP book: niche → positioning → outline → drafting → listing + compliance gate → AI cover. Chains to `higgsfield-generate` for the cover and to the KDP Studio API for the heavy LLM stages. |

## Install

**Any agent that reads `~/.<agent>/skills/<name>/SKILL.md`** (Claude Code, Cursor, Codex):

```bash
# from the repo root
mkdir -p ~/.claude/skills
ln -s "$(pwd)/skills/fabio-kdp" ~/.claude/skills/fabio-kdp
# (Cursor: ~/.cursor/skills · Codex: ~/.codex/skills)
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
