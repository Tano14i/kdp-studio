# Full Content method — stage prompt templates

Use these as the system/user prompt scaffolding when executing a stage locally
(i.e. when the KDP Studio connector is not available). Fill `{…}` placeholders.
Always write the deliverable in `{lang}` and optimize for `{market}`.

## Stage 1 — Niche validation
```
You are a KDP full-content publishing analyst. Market: {market}, language: {lang}.
Niche/idea: "{niche}". Book type: {type}.
Return: competition (Low/Med/High + why), demand 1-10, opportunity 1-10,
monthly sales band, price range + KDP margin, the reader's #1 pain, the
transformation the book promises, and the Top 10 buyer-intent Amazon keywords.
If opportunity < 4/10, propose 2 adjacent sub-niches and recommend stopping.
```

## Stage 2 — Positioning (5 titles)
```
Generate 5 title + subtitle pairs for "{niche}" ({type}, {audience}) in {lang}.
Use 5 distinct angles: Reframe, Contrarian, USP, Authority, Process.
Score each 1-10 on clarity, memorability, curiosity, relevance, differentiation.
Hard rule: title + subtitle <= 200 chars; the title is the real title, not a
keyword dump; no "free/bestseller/#1", no other authors/brands. Recommend one.
```

## Stage 3 — Outline
```
Create a chapter outline for "{title}" ({type}, {lang}): an introduction,
7-12 chapters, a conclusion. Per chapter: a one-line reader promise (what they
can DO after) + 3-5 beats. Keep a coherent learning/story arc.
```

## Stage 4 — Drafting (one chapter per call)
```
Write Chapter {n} of "{title}" in {lang}. Promise: "{chapter_promise}".
Voice: {tone}, {person}, reading level {level}. ~{words} words.
Open with a hook, deliver the promise with examples/steps, end with a takeaway
or transition to Chapter {n+1}. Output clean prose only (no meta commentary).
```

## Stage 5 — Listing
```
Create a complete {market} listing in {lang} for "{title}" ({type}, {audience}).
Output: title, subtitle, 7 backend keywords, 400-600 word HTML description
(<b>/<br>), 5 benefit bullets, 2 Amazon categories, 2 BISAC codes, ebook +
paperback price. Apply the KDP compliance rules in references/compliance.md to
every field. Flag that the content is AI-generated and must be disclosed.
```

## Stage 6 — Cover prompt (hand to higgsfield-generate)
```
A book-cover background for "{title}" ({niche}, {style}). Describe subject,
mood, color palette, lighting, and art style in 60-80 words. NO text or
typography in the image. Aspect {2:3 for 6x9 | 3:4 for 8.5x11}, resolution 2K+.
```
