---
name: fabio-kdp
description: End-to-end coach for publishing a FULL CONTENT book on Amazon KDP — validated niche, outline, chapter drafting, KDP listing, compliance check, and AI cover. Use when the user wants to write and publish a real readable book (non-fiction or fiction), not a low-content notebook/planner.
version: 0.1.0
argument-hint: "fabio-kdp \"<niche or book idea>\" [--market it|com|de|fr|es] [--lang Italian|English]"
allowed-tools: [WebFetch, Bash, higgsfield-generate]
---

## Use when
- The user wants to create a **full content** KDP book: real prose meant to be read — non-fiction guides, self-help, how-to, children's stories, fiction.
- They ask for help "from idea to published book", a writing roadmap, or to run any single full-content stage (niche, outline, chapters, listing, cover).
- They mention KDP / Amazon self-publishing and a topic to write about.

## NOT for
- **Low/no content** (notebooks, planners, journals, coloring, logbooks). Those are repetitive-page products — route to a low-content workflow instead.
- Publishing actions that require the user's KDP login (uploading the manuscript, setting price, hitting Publish). Produce the assets; the human publishes.
- Bypassing Amazon policy. Every output must pass the compliance gate (Stage 5).

## Chain
Skills communicate through **return values**, not implicit state. Run stages in order; each stage's output is the next stage's input.
- This skill emits a `book_state` object that accumulates: `niche`, `title`, `subtitle`, `outline`, `chapters[]`, `listing`, `cover_prompt`.
- **Cover**: when reaching Stage 6, hand `cover_prompt` to **`higgsfield-generate`** (`--aspect 2:3` for 6×9, `3:4` for 8.5×11) and consume the returned image URL. Finish the listing before starting the cover conversation.
- If `KDP_STUDIO_URL` is set, prefer the **Connector** (below) for the heavy LLM stages; otherwise execute the stage prompts yourself.

## Stage flow
A full-content book is built in 7 sequential stages. Never skip Stage 6 (compliance).

1. **Niche validation** — confirm the idea is sellable before writing a word.
2. **Reader avatar** — build the ideal reader persona before positioning.
3. **Positioning** — title, subtitle, angle, target reader.
4. **Outline** — chapter structure with a promise per chapter.
5. **Drafting** — write chapters to the outline, one at a time.
6. **Listing + Compliance** — KDP metadata, then a hard policy gate.
7. **Cover** — AI cover via higgsfield-generate, then assembly checklist.

---

### Stage 1 — Niche validation
Goal: a go/no-go with evidence. Ask for the market (default Amazon.it / Italian) if not given.
Produce, in the target language:
- Competition level (Low/Med/High) + why; demand score 1-10; opportunity score 1-10.
- Top 10 buyer-intent Amazon keywords for the niche.
- Realistic monthly sales band and price range with KDP margin.
- The reader's #1 pain and the transformation the book promises.
Gate: if opportunity < 4/10, propose 2 adjacent sub-niches and stop. Do not write a book nobody searches for.

### Stage 2 — Reader avatar
Build the ideal reader persona from **real competitor data**, not assumptions. Follow this research sequence:

**Step 2a — Competitor discovery**
Search Amazon in the target market for the top 5–8 books in the niche. For each: title, author, ASIN, star rating, number of reviews, price. Use WebFetch on Amazon search results pages (e.g. `https://www.amazon.it/s?k=burnout+lavoro`).

**Step 2b — Review mining**
For each top competitor, fetch the review pages (most helpful + most recent, both positive and negative). Collect verbatim quotes from:
- ⭐⭐⭐⭐⭐ reviews: what readers loved, the transformation they described, the exact words they used.
- ⭐⭐⭐ and below reviews: what was missing, what frustrated them, what they wished the book had covered.
Use WebFetch on Amazon review URLs (e.g. `https://www.amazon.it/product-reviews/<ASIN>?sortBy=helpful`).

**Step 2c — Avatar synthesis**
From the review data, extract and produce a named, vivid avatar in the target language:
- **Who they are**: age range, occupation, family situation, daily context — inferred from review language and context clues.
- **Their specific pain**: the exact lived moment they describe — copy verbatim phrases from reviews ("piansi in macchina dopo una riunione", "mi svegliavo già stanco").
- **Their fears**: what they express fearing if nothing changes; reluctance or shame about seeking help.
- **Their desire**: the concrete transformation they mention wanting — career, energy, relationships, identity.
- **Their objections**: complaints in negative reviews about what didn't work or felt generic/useless.
- **The gap**: what no competitor book delivers that reviewers explicitly request — this is your positioning edge.
- **Their voice**: 3–5 verbatim phrases from reviews that capture how they talk about the problem. Use these exact phrases in chapter hooks and the listing description.
- **Name + one-sentence narrative**: e.g. "Giulia, 38, marketing manager, hasn't taken a real break in two years and tells herself it's fine."

Use the avatar — especially the verbatim phrases and the gap — as direct input for every subsequent stage.

### Stage 3 — Positioning
Produce 5 title+subtitle combinations using distinct angles (Reframe, Contrarian, USP, Authority, Process). Score each on clarity, memorability, curiosity, relevance, differentiation. Recommend one. Hard rule: title + subtitle ≤ 200 characters; the title is the real title, not a keyword dump.

### Stage 4 — Outline
Build the chapter map: an intro, 7–12 chapters, a conclusion. For each chapter give a one-line promise (what the reader can do after it) and 3–5 beats. Keep a logical learning/story arc. Confirm the outline with the user before drafting.

### Stage 5 — Drafting
Write **one chapter per turn** to keep quality high. For each chapter: open with a hook, deliver on the chapter promise, use examples/steps, close with a takeaway or transition. Match a consistent voice (ask once: tone, reading level, person). Target the agreed length. After each chapter, summarize progress (`chapters[n]/total`) and offer to continue.

### Stage 6 — Listing + Compliance (mandatory gate)
Generate the KDP listing: title, subtitle, 7 backend keywords, 400–600-word HTML description (use `<b>`/`<br>`), 5 bullet benefits, 2 categories, BISAC codes, ebook + paperback price.
Then run the **compliance gate** — reject and fix anything that violates KDP:
- Title: real title only; no generic-keyword stuffing, no placeholders, no "free/bestseller/#1", no other authors/brands; title+subtitle ≤ 200 chars.
- Keywords: accurate; no misleading/competitor/brand terms; no "free/bestseller/on sale/Kindle Unlimited/%"; 2-3 words; no title repeats.
- Description: matches the real content; no fake reviews, no external links/URLs, no review solicitation.
- Content: original, non-infringing; public-domain only with substantial added value.
- **AI disclosure**: the manuscript/cover are AI-generated — tell the user to declare AI content in the KDP workflow.
Only pass the book forward when the gate is clean.

### Stage 7 — Cover + assembly
- Build a cover prompt: mood, palette, subject, lighting, art style, **no text in the image**. Hand it to `higgsfield-generate` (`--aspect 2:3` 6×9, `3:4` 8.5×11, resolution 2K+). Return the image URL.
- Deliver the assembly checklist: manuscript export (DOCX/PDF), front/back matter, trim size, paste cover, set categories/keywords/price, **declare AI content**, publish.

---

## Connector — KDP Studio API (optional, recommended)
If the environment exposes `KDP_STUDIO_URL` (a running KDP Studio backend), offload the LLM-heavy stages to its endpoints instead of generating locally. Send header `X-API-Key: $KDP_API_KEY` when set. All POST, JSON.

| Stage | Endpoint | Body keys |
|------|----------|-----------|
| 1 niche | `POST /niches` | `niche`, `market_language` |
| 1 discover | `GET /discover?market_language=` | — |
| 2 avatar | client-side (no endpoint) | — |
| 3 titles | `POST /title-variants` | `niche`, `trend`, `audience`, `current_title`, `language` |
| 4-5 write | `POST /generate` / `POST /generate-all` | `book_type`, `title`, `outline`/chapter params |
| 6 listing | `POST /package` | `book_title`, `book_subtitle`, `book_type`, `audience`, `language` (returns `ai_disclosure_required`) |
| 6 compliance | client-side rules (mirror the Stage-6 gate above) | — |
| 6 cover | `POST /api/generate-cover` | `prompt`, `trim_size`, `resolution` (uses Higgsfield Cloud) |

Example:
```bash
curl -s "$KDP_STUDIO_URL/package" -H "Content-Type: application/json" \
  ${KDP_API_KEY:+-H "X-API-Key: $KDP_API_KEY"} \
  -d '{"book_title":"...","book_subtitle":"...","book_type":"self-help","audience":"...","language":"Italian"}'
```
Note: `/api/generate-cover` needs Higgsfield **Cloud** credits (separate from the Supercomputer subscription). When Cloud keys are absent, generate the cover with the `higgsfield-generate` skill instead.

See `references/method.md` for the prompt templates used at each stage and `references/compliance.md` for the full KDP policy checklist.
