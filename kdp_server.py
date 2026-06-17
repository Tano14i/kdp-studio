"""
KDP Studio — Live Trend Backend v2
====================================
Endpoints:
  GET  /health
  GET  /discover          ← ZERO-BIAS: raw global data, no niche pre-selection
  POST /trends            ← niche-guided discovery
  POST /niches
  POST /generate          ← book-type-aware content generation
  POST /generate-all      ← sequential all chapters
  POST /analyze-market    ← competitor intelligence from pasted Amazon data
  POST /title-variants    ← 5 title angles (curiosity/benefit/problem/identity/authority)
  POST /package           ← multilingual KDP package
"""

import os, asyncio, json, random
from datetime import datetime
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import httpx
import anthropic

# ── Config ────────────────────────────────────────────────────
def env(key, default=""):
    return os.environ.get(key, default)

ANTHROPIC_KEY     = env("ANTHROPIC_API_KEY")
REDDIT_USER_AGENT = env("REDDIT_USER_AGENT", "KDPStudio/1.0 (personal use, no auth)")
YOUTUBE_API_KEY   = env("YOUTUBE_API_KEY")  # optional — enables YouTube Trending as a 3rd discovery source

app = FastAPI(title="KDP Studio API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
claude = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

# ══════════════════════════════════════════════════════════════
# UNIQUENESS ENGINE
# ══════════════════════════════════════════════════════════════

# ── 50+ rotating seed pool per nicchia ───────────────────────
NICHE_SEEDS = {
    "Self-help & Personal growth": [
        "dopamine detox", "nervous system reset", "somatic healing",
        "polyvagal theory", "window of tolerance", "parts work IFS",
        "inner child healing", "shadow work", "ego dissolution",
        "attachment repair", "emotional granularity", "cognitive load",
        "rejection therapy", "learned helplessness", "ego depletion",
        "body doubling ADHD", "delusional confidence", "main character energy",
        "soft life", "romanticize your life", "goblin mode recovery",
        "quiet quitting identity", "rest as resistance", "slow living",
        "digital minimalism", "intentional living", "radical acceptance",
        "self compassion practice", "inner critic work", "identity shifting",
        "neuroplasticity habits", "emotional adulthood", "boundaries healing",
    ],
    "Health & Wellness": [
        "cortisol face", "cycle syncing", "adrenal fatigue recovery",
        "gut brain axis", "seed cycling hormones", "lymphatic drainage",
        "zone 2 cardio", "VO2 max longevity", "cold exposure protocol",
        "mouth taping sleep", "circadian fasting", "autophagy trigger",
        "vagal tone exercises", "breathwork stress", "red light therapy",
        "carnivore healing", "elimination diet", "FODMAP gut health",
        "mineral deficiency symptoms", "hair loss cortisol women",
        "perimenopause symptoms", "testosterone optimization natural",
        "sleep architecture stages", "chronobiology optimization",
    ],
    "Finance & Money": [
        "loud budgeting", "soft saving", "no spend challenge",
        "cash stuffing envelopes", "doom spending anxiety",
        "financial therapy trauma", "money dysmorphia",
        "stealth wealth mindset", "barista FIRE", "coast FIRE",
        "geo arbitrage remote", "house hacking starter",
        "index fund simple path", "bond tent retirement",
        "value averaging strategy", "dividend snowball",
        "frugal hedonic adaptation", "lifestyle inflation trap",
        "financial independence immigrants", "first gen wealth building",
    ],
    "Relationships & Dating": [
        "anxious attachment healing", "fearful avoidant earned security",
        "disorganized attachment", "limerence recovery",
        "situationship clarity", "coercive control recovery",
        "narcissistic abuse healing", "DARVO pattern recognition",
        "love bombing aftermath", "trauma bonding escape",
        "enmeshment untangling", "parentification healing",
        "emotional immaturity parents", "chosen family building",
        "loneliness epidemic men", "male loneliness crisis",
        "female friendship adult", "platonic intimacy",
    ],
    "Productivity & Habits": [
        "body doubling technique", "temptation bundling",
        "implementation intentions", "friction reduction habits",
        "dopamine menu ADHD", "time blindness solutions",
        "ADHD paralysis tools", "executive function scaffolding",
        "ultradian rhythm work", "deep work newport",
        "time blocking template", "weekly review system",
        "second brain building", "progressive summarization",
        "GTD capture trusted", "slow productivity cal newport",
        "anti goals framework", "one thing gary keller",
        "essentialism mckeown", "digital detox productivity",
    ],
    "Spirituality & Mindset": [
        "synchronicity jung meaning", "spiritual bypassing awareness",
        "dark night of soul", "ego death integration",
        "non dual awareness", "present moment power tolle",
        "stoic journaling marcus aurelius", "memento mori practice",
        "amor fati framework", "negative visualization stoic",
        "ikigai finding purpose", "wabi sabi imperfection",
        "mono no aware grief", "ubuntu philosophy community",
        "ubuntu african philosophy", "hygge danish wellbeing",
        "lagom swedish balance", "friluftsliv outdoor mindset",
    ],
    "Fitness & Sports": [
        "hybrid athlete training", "zone 2 fat burning",
        "rucking benefits beginners", "functional fitness aging",
        "strength training women over 40", "perimenopause exercise",
        "protein timing muscle", "creatine women benefits",
        "mobility longevity routine", "fascia release techniques",
        "nervous system recovery training", "HRV optimization",
        "sleep for athletes", "deload week structure",
        "progressive overload beginners", "RPE training scale",
    ],
    "Parenting & Family": [
        "gentle parenting boundaries", "connection before correction",
        "playful parenting cohen", "PACE parenting DDP",
        "therapeutic parenting trauma", "sensory processing kids",
        "twice exceptional 2e parenting", "ADHD girls undiagnosed",
        "autism late diagnosis parenting", "PDA pathological demand",
        "interoception kids body signals", "co regulation adults",
        "reparenting yourself childhood", "adult children estrangement",
        "boomerang generation parenting", "sandwich generation stress",
    ],
    "Business & Entrepreneurship": [
        "solopreneur systems", "one person business model",
        "creator economy monetize", "audience of 1000 fans",
        "niche down riches", "info product validation",
        "cold email renaissance", "linkedin creator B2B",
        "bootstrapped SaaS indie", "micro SaaS niche",
        "productized service agency", "fractional executive model",
        "consulting accelerator positioning", "thought leadership monetize",
        "newsletter monetization beehiiv", "podcast to book funnel",
    ],
    "Neuroscience & Psychology": [
        "interoception body awareness", "neuroception safety",
        "polyvagal ladder states", "window of tolerance trauma",
        "EMDR self administered", "EFT tapping anxiety",
        "DNRS limbic retraining", "somatic experiencing body",
        "sensorimotor psychotherapy", "ACT hexaflex values",
        "schema therapy modes", "DBT skills emotional regulation",
        "mentalizing reflective function", "theory of mind adults",
        "alexithymia emotional awareness", "intolerance uncertainty therapy",
    ],
    "Any niche": [
        "quiet quitting burnout", "soft life boundaries", "delusional confidence",
        "main character energy", "romanticize your life", "dopamine detox",
        "nervous system healing", "situationship clarity", "loud budgeting",
        "cycle syncing hormones", "hybrid athlete", "gentle parenting",
        "solopreneur systems", "ikigai purpose", "cortisol dysregulation",
    ],
    # ── Italian / European market seeds ──────────────────────
    "Italian": [
        "benessere mentale italiano", "stile di vita sano", "mindfulness italia",
        "finanza personale giovani", "investire stipendio", "risparmio intelligente",
        "side hustle italiano", "lavoro da remoto", "freelance italia",
        "relazioni tossiche", "crescita personale", "autostima bassa",
        "come fare soldi online", "creator economy italia", "tiktok monetizzare",
        "alimentazione sana ricette", "dieta mediterranea salute",
        "sport a casa", "yoga principianti", "meditazione guidata",
        "genitoriale consapevole", "figli adolescenti", "coppia crisi",
    ],
    "Dutch": [
        "persoonlijke ontwikkeling", "mentale gezondheid", "burn-out herstel",
        "financieel vrij worden", "sparen jongeren", "beleggen beginners",
        "zelfstandige ondernemer", "thuiswerken productiviteit",
        "relaties verbeteren", "grenzen stellen", "angst overwinnen",
        "gezond eten simpel", "sporten thuis", "mindfulness dagelijks",
    ],
    "German": [
        "persoenliche entwicklung", "mentale gesundheit", "burnout erholung",
        "finanziell frei werden", "geld sparen tipps", "investieren anfaenger",
        "selbststaendig arbeiten", "produktivitaet steigern",
        "beziehungen verbessern", "grenzen setzen", "angst bewaeltigen",
        "gesund ernaehren einfach", "sport zuhause", "achtsamkeit alltag",
    ],
}

def get_language_seeds(keyword: str) -> list:
    """Detect if keyword is non-English and return appropriate seeds."""
    # Simple heuristic: check for common Italian/Dutch/German words
    kw_lower = keyword.lower()
    italian_markers = ['come', 'fare', 'soldi', 'vita', 'salute', 'lavoro', 'amore']
    dutch_markers = ['hoe', 'geld', 'leven', 'werk', 'gezond', 'relatie']
    german_markers = ['wie', 'geld', 'leben', 'arbeit', 'gesund', 'beziehung']
    
    if any(w in kw_lower for w in italian_markers):
        return NICHE_SEEDS.get("Italian", [])
    if any(w in kw_lower for w in dutch_markers):
        return NICHE_SEEDS.get("Dutch", [])
    if any(w in kw_lower for w in german_markers):
        return NICHE_SEEDS.get("German", [])
    return []

# ── 30+ subreddit pool per nicchia ───────────────────────────
NICHE_SUBREDDIT_POOL = {
    "Self-help & Personal growth": [
        "selfimprovement", "getdisciplined", "decidingtobebetter",
        "selfhelp", "productivity", "LifeAdvice", "findapath",
        "DecidingToBeBetter", "Mindfulness", "emotionalintelligence",
        "psychologyofsex", "InternalFamilySystems", "CPTSD",
        "raisedbynarcissists", "adulting", "quarterlifecrisis",
    ],
    "Health & Wellness": [
        "health", "wellness", "longevity", "biohacking", "nutrition",
        "Fasting", "intermittentfasting", "WellnessOver50",
        "PCOS", "Hashimotos", "thyroid", "chronicillness",
        "adhdwomen", "Fibromyalgia", "guthealth",
    ],
    "Finance & Money": [
        "personalfinance", "financialindependence", "frugal",
        "investing", "povertyfinance", "leanfire", "Fire",
        "Bogleheads", "debtfree", "DaveRamsey",
        "FirstTimeHomeBuyer", "churning", "beermoney",
        "digitalnomad", "eupersonalfinance",
    ],
    "Relationships & Dating": [
        "relationship_advice", "dating_advice", "dating",
        "socialskills", "attachment", "BreakUps", "ExNoContact",
        "NarcissisticAbuse", "raisedbynarcissists", "CPTSD",
        "MentalHealthSupport", "lonely", "FriendshipAdvice",
        "adulting", "MenGetsTooLittle",
    ],
    "Productivity & Habits": [
        "productivity", "getdisciplined", "habittracker",
        "nosurf", "digitalminimalism", "ADHD", "adhdwomen",
        "ObsidianMD", "Notion", "gtd", "Zettelkasten",
        "timemanagement", "neurodiversity", "lazyproductivity",
    ],
    "Spirituality & Mindset": [
        "spirituality", "meditation", "mindfulness", "stoicism",
        "awakened", "Jung", "consciousness", "Buddhism",
        "philosophy", "Psychonaut", "Sober", "AlAnon",
        "occult", "witchcraft", "tarot",
    ],
    "Fitness & Sports": [
        "fitness", "loseit", "xxfitness", "running", "bodyweightfitness",
        "weightlifting", "StrongFirst", "overcominggravity",
        "flexibility", "yoga", "swimming", "cycling",
        "intermittentfasting", "carnivore", "veganfitness",
    ],
    "Parenting & Family": [
        "Parenting", "beyondthebump", "mommit", "daddit",
        "raisingkids", "gentleparenting", "SingleParents",
        "autism", "ADHD", "specialneedssupport",
        "EstrangedAdultChild", "AgingParents", "Blended_Families",
    ],
    "Business & Entrepreneurship": [
        "entrepreneur", "smallbusiness", "startups",
        "SideProject", "passive_income", "Entrepreneur",
        "freelance", "digitalnomad", "ecommerce",
        "marketing", "sales", "consulting", "msp",
        "SaaS", "indiehackers",
    ],
    "Neuroscience & Psychology": [
        "psychology", "neuroscience", "cognitivescience",
        "behavioralscience", "therapy", "CPTSD", "BPD",
        "ADHD", "autism", "OCD", "anxiety", "depression",
        "schizoaffective", "bipolar", "mentalhealth",
    ],
    "Any niche": [
        "selfimprovement", "productivity", "wellness",
        "personalfinance", "psychology", "relationship_advice",
        "getdisciplined", "longevity", "entrepreneur", "mindfulness",
    ],
}

# ── Book type templates — specific structure per format ──────
BOOK_TYPE_TEMPLATES = {
    "Guided Journal": {
        "structure": "Each chapter contains: a 1-page intro explaining the theme, 4-6 guided journal prompts with 8-10 lines of writing space each, a reflection box at the end, and an affirmation. No long prose — prompts are the content.",
        "chapter_instruction": "Write the chapter intro (150-200 words), then 5 SPECIFIC journal prompts (each prompt is 1-2 sentences, thought-provoking and personal), then a closing reflection prompt.",
        "length_note": "Chapters are SHORT — prompts, not essays. 400-600 words of actual text per chapter, rest is writing space.",
        "unique_elements": "Include space cues like '[Write here...]' after each prompt. End each chapter with a 1-sentence affirmation in italics.",
    },
    "Workbook": {
        "structure": "Each chapter = one skill or concept. Sections: (1) Concept explanation 300w, (2) Why it matters, (3) Exercise or worksheet with fill-in sections, (4) Action steps checklist, (5) Progress tracker.",
        "chapter_instruction": "Write concept explanation, then create a structured EXERCISE with labeled fields the reader fills in (e.g. 'My current situation:', 'My goal:', 'Action I will take:'). End with a numbered action checklist.",
        "length_note": "Balance: 40% explanation, 60% exercises and worksheets. Make it interactive on the page.",
        "unique_elements": "Use checkbox lists for action steps. Include 'My Notes:' sections. Add a chapter score tracker (1-10 how well they applied the concept).",
    },
    "30-Day Challenge Book": {
        "structure": "Introduction + 30 daily entries. Each day = Day number, Theme, Challenge task (specific action), Reflection prompt, Done checkbox. Days build on each other progressively.",
        "chapter_instruction": "Each DAY entry: Day X header, 1-sentence theme, specific CHALLENGE TASK (what exactly to do today, actionable), 2 reflection prompts, space for notes.",
        "length_note": "Each day entry: 200-300 words max. The book is a daily companion, not an essay collection.",
        "unique_elements": "Start with a Week 1/2/3/4 overview. Include a habit tracker grid. Day 1 should be extremely easy, Day 30 should feel like a milestone.",
    },
    "Planner": {
        "structure": "Goal-setting intro + weekly/monthly spreads. Sections: Annual goals, Monthly intention pages, Weekly layout (Mon-Sun with priorities, tasks, notes), Daily log pages, Reflection pages.",
        "chapter_instruction": "Create a PLANNING SPREAD with labeled sections: Weekly Intention (1 sentence), Top 3 Priorities, Daily task columns (Mon-Sun), Wins of the week, What to improve.",
        "length_note": "Minimal prose — this is functional. Headers, labels, fill-in sections. The reader writes IN it.",
        "unique_elements": "Include a habit tracker, mood tracker, water intake log. Monthly review pages with percentage-completion fields.",
    },
    "Prompt Book": {
        "structure": "Organized by theme/section. Each page = one prompt. Variety of prompt types: writing prompts, thinking prompts, creative prompts, memory prompts. No answers provided.",
        "chapter_instruction": "Write 8-10 VARIED prompts for this chapter theme. Mix: open-ended questions, scenario-based prompts, memory exploration, creative imagination, values clarification. Each prompt on its own conceptual space.",
        "length_note": "Each prompt is 1-3 sentences maximum. The SPACE for the reader to write is the product. Include 8-10 lines of dotted space after each.",
        "unique_elements": "Categorize by difficulty or depth: Surface → Deeper → Core. Include occasional 'Big Question' prompts marked with a star.",
    },
    "Activity Book": {
        "structure": "Chapters by theme. Each chapter mixes: short reading (200w), activity or exercise (specific to the topic), reflection, and a mini-challenge to complete in daily life.",
        "chapter_instruction": "Write a short intro, then design ONE SPECIFIC ACTIVITY (e.g. mapping exercise, letter-writing, body scan, values sort, gratitude list with twist). Make it interactive and time-bound (10-15 min).",
        "length_note": "Activities should have clear instructions: Step 1, Step 2, Step 3. Include a 'You will need:' section if relevant.",
        "unique_elements": "Include estimated time per activity. Add 'Level up' variations for each activity (easier and harder versions).",
    },
    "Self-help Guide": {
        "structure": "Classic non-fiction structure. Each chapter: hook opening, core concept, research or evidence, personal application framework, case study or story, action steps.",
        "chapter_instruction": "Write a full chapter with: compelling opening (hook), main concept explained clearly, 1 research reference or expert insight, practical framework (3-step or similar), concrete action steps, chapter summary.",
        "length_note": "This is prose-heavy. Full paragraphs, narrative flow, 1200-2000 words per chapter.",
        "unique_elements": "End each chapter with 'Key Takeaways' (3 bullets) and 'This Week's Practice' (1 specific action). Include pull-quotes.",
    },
}

def get_book_template(book_type: str) -> dict:
    """Match book type string to template, with fuzzy matching."""
    book_type_lower = book_type.lower()
    for key, template in BOOK_TYPE_TEMPLATES.items():
        if key.lower() in book_type_lower or book_type_lower in key.lower():
            return template
    # Defaults
    if any(w in book_type_lower for w in ["journal", "diary"]):
        return BOOK_TYPE_TEMPLATES["Guided Journal"]
    if any(w in book_type_lower for w in ["work", "exercise"]):
        return BOOK_TYPE_TEMPLATES["Workbook"]
    if any(w in book_type_lower for w in ["plan", "organiz"]):
        return BOOK_TYPE_TEMPLATES["Planner"]
    if any(w in book_type_lower for w in ["challenge", "day"]):
        return BOOK_TYPE_TEMPLATES["30-Day Challenge Book"]
    return BOOK_TYPE_TEMPLATES["Self-help Guide"]

# ── Chapter opening styles pool ───────────────────────────────
OPENING_STYLES = [
    "Start with a vivid real-world scenario or micro-story (2-3 sentences) that drops the reader into the feeling",
    "Open with a provocative question that challenges a common assumption the reader holds",
    "Begin with a surprising statistic or research finding that reframes the chapter topic",
    "Open with a short quote from a non-English cultural tradition (philosophy, literature, folk wisdom)",
    "Start with a brief personal confession or vulnerability that immediately builds trust",
    "Open with a paradox or contradiction that the chapter will resolve",
    "Begin with a sensory description — a smell, sound, texture — that anchors the emotional tone",
    "Start with a bold, counter-intuitive claim that the reader will want to disprove or explore",
    "Open with a dialogue snippet or overheard conversation that captures the chapter's tension",
    "Begin with a very short poem, haiku, or lyrical fragment that sets the emotional key",
]

# ── Writing tone pool ─────────────────────────────────────────
TONE_DESCRIPTORS = [
    "warm and conversational, like a trusted friend who happens to be an expert",
    "precise and direct, no fluff — every sentence earns its place",
    "lyrical and reflective, with space for the reader to breathe between ideas",
    "academically grounded but emotionally accessible — cite concepts without jargon",
    "bold and challenging, pushing the reader past their comfort zone with compassion",
    "gentle and trauma-informed, never rushing, always meeting the reader where they are",
    "intellectually curious, exploring ideas from multiple cultural angles",
    "pragmatic and systems-oriented, always asking: what does the reader do next?",
]

# ── Uniqueness helpers ────────────────────────────────────────
def now_stamp() -> str:
    n = datetime.now()
    return f"{n.strftime('%A %d %B %Y')}, {n.strftime('%H:%M')} CET — week {n.isocalendar()[1]} of {n.year}"

# Timeframe → Reddit + Google Trends params
TIMEFRAME_MAP = {
    "day":      {"reddit_t": "day",   "gtrends": "now 1-d",    "label": "Oggi",          "strategy": "Pubblica entro 1-2 settimane o il momento passa"},
    "week":     {"reddit_t": "week",  "gtrends": "now 7-d",    "label": "Settimana",     "strategy": "Finestra ottimale KDP — caldo ma non ancora saturo"},
    "month":    {"reddit_t": "month", "gtrends": "today 1-m",  "label": "Mese",          "strategy": "Nicchia in crescita — meno urgenza, audience più definita"},
    "3months":  {"reddit_t": "month", "gtrends": "today 3-m",  "label": "3 Mesi",        "strategy": "Trend in consolidamento — cerca angoli non ancora coperti"},
    "year":     {"reddit_t": "year",  "gtrends": "today 12-m", "label": "Anno",          "strategy": "Nicchia matura — migliora libri esistenti o trova sub-nicchie"},
}

def get_timeframe(tf: str) -> dict:
    return TIMEFRAME_MAP.get(tf, TIMEFRAME_MAP["week"])

def pick_seeds(niche: str, keyword: str = "", n: int = 4) -> list[str]:
    pool = []
    # First check if keyword suggests a non-English language
    if keyword:
        lang_seeds = get_language_seeds(keyword)
        if lang_seeds:
            pool = lang_seeds
    # Then try niche-based pool
    if not pool:
        for k, v in NICHE_SEEDS.items():
            if k.lower() in niche.lower() or niche.lower() in k.lower():
                pool = v
                break
    if not pool:
        pool = NICHE_SEEDS["Any niche"]
    seeds = random.sample(pool, min(n, len(pool)))
    if keyword and keyword not in seeds:
        seeds[0] = keyword  # always include user keyword
    return seeds

def pick_subreddits(niche: str, n: int = 4) -> list[str]:
    pool = []
    for k, v in NICHE_SUBREDDIT_POOL.items():
        if k.lower() in niche.lower() or niche.lower() in k.lower():
            pool = v
            break
    if not pool:
        pool = NICHE_SUBREDDIT_POOL["Any niche"]
    return random.sample(pool, min(n, len(pool)))

def pick_opening_style() -> str:
    return random.choice(OPENING_STYLES)

def pick_tone() -> str:
    return random.choice(TONE_DESCRIPTORS)

# ══════════════════════════════════════════════════════════════
# PYDANTIC MODELS
# ══════════════════════════════════════════════════════════════
MARKET_LANG_CONFIG = {
    "English":    {"amazon": "Amazon.com", "subreddits": ["books","selfhelp","personalfinance","productivity","Fitness","mentalhealth","relationships","Parenting","Entrepreneur"]},
    "Italian":    {"amazon": "Amazon.it",  "subreddits": ["italy","italiani","crescitapersonale","ItalyInformatica","psicologia"]},
    "Spanish":    {"amazon": "Amazon.es / Amazon.com.mx", "subreddits": ["es","mexico","argentina","colombia","emprendimiento","psicologia"]},
    "German":     {"amazon": "Amazon.de",  "subreddits": ["de","Austria","finanzen","Persoenlichkeitsentwicklung","Switzerland"]},
    "French":     {"amazon": "Amazon.fr",  "subreddits": ["france","francophonie","Quebec","developpementpersonnel"]},
    "Portuguese": {"amazon": "Amazon.com.br", "subreddits": ["brasil","portugal","empreendedorismo","desabafos"]},
}

class TrendRequest(BaseModel):
    platforms: list[str]
    niche: str
    keyword: Optional[str] = ""
    timeframe: Optional[str] = "week"   # day|week|month|3months|year
    market_language: Optional[str] = "English"

class NicheRequest(BaseModel):
    platforms: list[str]
    keyword: Optional[str] = ""
    timeframe: Optional[str] = "week"

class PositioningRequest(BaseModel):
    author_identity: str       # chi sei come autore/publisher, come vuoi essere percepito
    ideal_reader: str           # psicografia del lettore ideale (non demografica)
    transformation: str         # trasformazione specifica che prometti
    competitors: Optional[str] = ""      # competitor diretti e differenziazione
    unfair_advantage: Optional[str] = "" # cosa sai/hai vissuto che altri non hanno

class GenerateRequest(BaseModel):
    trend_name: str
    book_title: str
    book_subtitle: str
    book_type: str
    audience: str
    tab: str
    chapter_num: Optional[int] = 1
    outline: Optional[str] = ""
    # New voice params
    tone: Optional[str] = ""
    language: Optional[str] = "English"
    cultural_inspiration: Optional[str] = ""
    chapter_length: Optional[str] = "medium"   # short|medium|long
    reader_persona: Optional[str] = ""
    custom_instructions: Optional[str] = ""

class AllChaptersRequest(BaseModel):
    trend_name: str
    book_title: str
    book_subtitle: str
    book_type: str
    audience: str
    outline: str
    tone: Optional[str] = ""
    language: Optional[str] = "English"
    cultural_inspiration: Optional[str] = ""
    chapter_length: Optional[str] = "medium"
    reader_persona: Optional[str] = ""
    custom_instructions: Optional[str] = ""

class PackageRequest(BaseModel):
    trend_name: str
    trend_platform: str
    book_title: str
    book_subtitle: str
    book_type: str
    audience: str
    tone: Optional[str] = ""
    reader_persona: Optional[str] = ""
    language: Optional[str] = "English"
    custom_instructions: Optional[str] = ""

# ══════════════════════════════════════════════════════════════
LANG_CODE_MAP = {
    "English": "en", "Italian": "it", "Spanish": "es",
    "German": "de", "French": "fr", "Portuguese": "pt",
}

# ══════════════════════════════════════════════════════════════
# GOOGLE / YOUTUBE AUTOCOMPLETE HELPERS
# ══════════════════════════════════════════════════════════════
async def fetch_google_autocomplete(query: str, lang_code: str = "en") -> list[str]:
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(
                "https://suggestqueries.google.com/complete/search",
                params={"client": "firefox", "q": query, "hl": lang_code},
                headers={"Accept-Language": lang_code}
            )
            if r.status_code != 200:
                return []
            data = r.json()
            return [s for s in (data[1] if len(data) > 1 else []) if s.lower() != query.lower()][:10]
    except Exception as e:
        print(f"[Google Autocomplete] {query}: {e}")
        return []

async def fetch_youtube_autocomplete(query: str, lang_code: str = "en") -> list[str]:
    try:
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(
                "https://suggestqueries.google.com/complete/search",
                params={"client": "firefox", "ds": "yt", "q": query, "hl": lang_code},
                headers={"Accept-Language": lang_code}
            )
            if r.status_code != 200:
                return []
            data = r.json()
            return [s for s in (data[1] if len(data) > 1 else []) if s.lower() != query.lower()][:10]
    except Exception as e:
        print(f"[YouTube Autocomplete] {query}: {e}")
        return []

async def fetch_multi_autocomplete(niche: str, lang_code: str = "en") -> dict:
    """Batch Google + YouTube autocomplete across multiple seed queries."""
    kw = niche.strip()
    seeds_google = [kw, f"{kw} book", f"{kw} guide", f"how to {kw}", f"best {kw}"]
    seeds_yt = [kw, f"how to {kw}", f"{kw} tips"]
    tasks = [fetch_google_autocomplete(s, lang_code) for s in seeds_google]
    tasks += [fetch_youtube_autocomplete(s, lang_code) for s in seeds_yt]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    google_seen, google_all = set(), []
    for r in results[:len(seeds_google)]:
        if isinstance(r, list):
            for s in r:
                if s not in google_seen:
                    google_seen.add(s); google_all.append(s)

    yt_seen, yt_all = set(), []
    for r in results[len(seeds_google):]:
        if isinstance(r, list):
            for s in r:
                if s not in yt_seen:
                    yt_seen.add(s); yt_all.append(s)

    return {"google": google_all[:25], "youtube": yt_all[:15]}

# ══════════════════════════════════════════════════════════════
# REDDIT HELPER
# ══════════════════════════════════════════════════════════════
async def fetch_reddit_posts(niche: str, keyword: str = "", timeframe: str = "week", force_subreddits: list = None) -> list[dict]:
    if force_subreddits:
        subreddits = random.sample(force_subreddits, min(4, len(force_subreddits)))
    else:
        subreddits = pick_subreddits(niche, n=4)
    tf = get_timeframe(timeframe)
    reddit_t = tf["reddit_t"]
    print(f"[Reddit] Subreddits: {subreddits} | timeframe: {reddit_t}")
    posts = []

    headers = {
        "User-Agent": REDDIT_USER_AGENT,
        "Accept": "application/json",
    }

    async with httpx.AsyncClient(timeout=12, headers=headers, follow_redirects=True) as client:
        async def fetch_sub(sub: str, sort: str) -> list[dict]:
            try:
                url = f"https://www.reddit.com/r/{sub}/{sort}.json"
                params = {"limit": 25, "raw_json": 1}
                if sort == "top":
                    params["t"] = reddit_t
                r = await client.get(url, params=params)
                if r.status_code == 429:
                    await asyncio.sleep(2)
                    r = await client.get(url, params=params)
                if r.status_code != 200:
                    return []
                result = []
                for item in r.json().get("data", {}).get("children", []):
                    p = item.get("data", {})
                    if p.get("stickied") or p.get("is_meta"):
                        continue
                    title = p.get("title", "")
                    if keyword and keyword.lower() not in (title + p.get("selftext","")).lower():
                        continue
                    result.append({
                        "subreddit": p.get("subreddit",""),
                        "title": title,
                        "score": p.get("score", 0),
                        "num_comments": p.get("num_comments", 0),
                        "upvote_ratio": p.get("upvote_ratio", 0),
                        "url": "https://reddit.com" + p.get("permalink",""),
                        "flair": p.get("link_flair_text",""),
                    })
                return result
            except Exception as e:
                print(f"[Reddit] r/{sub}/{sort}: {e}")
                return []

        tasks = [fetch_sub(sub, sort) for sub in subreddits for sort in ["top","hot"]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, list):
                posts.extend(r)

    seen, unique = set(), []
    for p in sorted(posts, key=lambda x: x["score"], reverse=True):
        if p["title"] not in seen:
            seen.add(p["title"])
            unique.append(p)
    print(f"[Reddit] {len(unique)} unique posts fetched")
    return unique[:25]

# ══════════════════════════════════════════════════════════════
# GOOGLE TRENDS HELPER
# ══════════════════════════════════════════════════════════════
async def fetch_google_trends(niche: str, keyword: str = "", timeframe: str = "week") -> dict:
    try:
        from pytrends.request import TrendReq
        terms = pick_seeds(niche, keyword, n=4)
        tf = get_timeframe(timeframe)
        gtrends_tf = tf["gtrends"]
        print(f"[GTrends] Seeds: {terms} | timeframe: {gtrends_tf}")

        def _fetch():
            pt = TrendReq(hl='en-US', tz=360, timeout=(10,25))
            pt.build_payload(terms, timeframe=gtrends_tf, geo='')
            interest = pt.interest_over_time()
            rising = {}
            try:
                related = pt.related_queries()
                for t in terms:
                    if t in related and related[t].get("rising") is not None:
                        df = related[t]["rising"]
                        rising[t] = df.head(5).to_dict('records') if not df.empty else []
            except Exception:
                pass
            avg = {}
            if not interest.empty:
                for t in terms:
                    if t in interest.columns:
                        avg[t] = int(interest[t].mean())
            return {"terms": terms, "avg_interest": avg, "rising_queries": rising}

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)
    except Exception as e:
        print(f"[GTrends] Error: {e}")
        return {"terms": [], "avg_interest": {}, "rising_queries": {}, "error": str(e)}

# ══════════════════════════════════════════════════════════════
# CLAUDE HELPER
# ══════════════════════════════════════════════════════════════
def call_claude(prompt: str, max_tokens: int = 4000, allow_truncated: bool = False) -> str:
    msg = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    if msg.stop_reason == "max_tokens" and not allow_truncated:
        raise ValueError("Risposta troncata — usa Capitolo Singolo o riduci la lunghezza.")
    return msg.content[0].text

def parse_json_safe(text: str) -> dict:
    import re
    text = text.replace('\u2018',"'").replace('\u2019',"'")
    text = text.replace('\u201c','"').replace('\u201d','"')
    text = text.replace('\u2014','-').replace('\u2013','-')
    m = re.search(r'\{[\s\S]*\}', text)
    if not m:
        raise ValueError("Nessun JSON nella risposta Claude")
    j = m.group(0)
    try:
        return json.loads(j)
    except json.JSONDecodeError as e:
        # "Extra data" means valid JSON followed by trailing text \u2014 truncate at e.pos
        if e.pos and e.pos > 0:
            try:
                return json.loads(j[:e.pos])
            except json.JSONDecodeError:
                pass
        j = re.sub(r',\s*([\]}])', r'\1', j)
        j = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', j)
        return json.loads(j)

def build_voice_ctx(tone="", language="English", cultural_inspiration="",
                    chapter_length="medium", reader_persona="", custom_instructions="") -> str:
    """Build a voice/style context block to inject into every content prompt."""
    length_map = {"short": "800-1000", "medium": "1200-1600", "long": "2000-2500"}
    word_count = length_map.get(chapter_length, "1200-1600")
    opening = pick_opening_style()
    writing_tone = tone if tone else pick_tone()
    lines = [
        f"WRITING VOICE & STYLE (follow precisely):",
        f"- Tone: {writing_tone}",
        f"- Output language: {language}",
        f"- Target word count: {word_count} words",
        f"- Chapter opening style: {opening}",
    ]
    if cultural_inspiration:
        lines.append(f"- Cultural lens: draw references, metaphors, or philosophy from {cultural_inspiration} tradition")
    if reader_persona:
        lines.append(f"- Write as if speaking directly to: {reader_persona}")
    if custom_instructions:
        lines.append(f"\nCUSTOM RESTRICTIONS (MANDATORY — apply to every sentence):\n{custom_instructions}")
    lines.append(f"- Uniqueness seed: {now_stamp()} — use this to make this version distinct from any previous generation")
    lines.append(f"- IMPORTANT: Do NOT use generic self-help clichés. Make every sentence specific and surprising.")
    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════
# ── Serve frontend HTML (so Railway hosts everything) ────────
@app.get("/")
async def serve_frontend():
    from fastapi.responses import FileResponse
    import os
    # Look for the frontend HTML in same dir as server
    base_dir = os.path.dirname(os.path.abspath(__file__))
    for name in ("kdp-trend-hunter.html", "index.html"):
        html_path = os.path.join(base_dir, name)
        if os.path.exists(html_path):
            return FileResponse(html_path, media_type="text/html")
    return {"message": "KDP Studio API running. Frontend not found — place kdp-trend-hunter.html in same folder."}


@app.get("/health")
async def health():
    # Return immediately — Reddit status checked async in background
    # This prevents the health check from timing out while waiting for Reddit
    return {
        "status": "ok",
        "reddit": True,   # assumed ok — verified at request time
        "reddit_mode": "public_json",
        "claude": bool(ANTHROPIC_KEY),
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health/full")
async def health_full():
    # Full health check including Reddit ping (slower, use only when needed)
    reddit_ok = False
    try:
        async with httpx.AsyncClient(timeout=5, headers={"User-Agent": REDDIT_USER_AGENT}) as c:
            r = await c.get("https://www.reddit.com/r/selfimprovement/hot.json?limit=1&raw_json=1")
            reddit_ok = r.status_code == 200
    except Exception:
        pass
    tiktok_ok = False
    try:
        async with httpx.AsyncClient(timeout=5) as c:
            r = await c.get("https://ads.tiktok.com/creative_radar_api/v1/popular_trend/hashtag/list", params={
                "page": 1, "limit": 1, "period": 7, "country_code": "US", "sort_by": "popular",
            }, headers={"User-Agent": "Mozilla/5.0", "Accept": "application/json"})
            tiktok_ok = r.status_code == 200
    except Exception:
        pass
    amazon_autocomplete_ok = False
    try:
        async with httpx.AsyncClient(timeout=5, headers={**AMAZON_HEADERS, "Accept": "application/json"}) as c:
            r = await c.get("https://completion.amazon.com/api/2017/suggestions", params={
                "limit": 1, "prefix": "journal", "suggestion-type": "KEYWORD",
                "page-type": "Search", "alias": "stripbooks", "mid": "ATVPDKIKX0DER",
            })
            amazon_autocomplete_ok = r.status_code == 200
    except Exception:
        pass
    return {
        "status": "ok",
        "reddit": reddit_ok,
        "reddit_mode": "public_json",
        "claude": bool(ANTHROPIC_KEY),
        "youtube": bool(YOUTUBE_API_KEY),
        "tiktok": tiktok_ok,
        "amazon_autocomplete": amazon_autocomplete_ok,
        "timestamp": datetime.utcnow().isoformat()
    }


# ══════════════════════════════════════════════════════════════
# ZERO-BIAS DISCOVERY ENGINE
# ══════════════════════════════════════════════════════════════

# Subreddits that reflect general human discourse — no niche bias
DISCOVERY_SUBREDDITS = [
    # Human experience & emotions
    "TrueOffMyChest", "offmychest", "self", "AITA", "confessions",
    "LifeAdvice", "NoStupidQuestions", "AskReddit", "Showerthoughts",
    # Behavior & change
    "ChangeMyView", "unpopularopinion", "raisedbynarcissists",
    "relationship_advice", "socialskills", "lonely",
    # Books & learning
    "books", "writing", "suggestmeabook", "NonFictionBookClub",
    # Broad wellness signals
    "mentalhealth", "anxiety", "depression", "selfimprovement",
    "findapath", "careerguidance", "adulting",
]

# Google Trends country codes to rotate (no topic seed)
DISCOVERY_COUNTRIES = ["US", "GB", "AU", "CA", "NL", "DE", "IT"]

async def fetch_reddit_global(limit_per_sub: int = 15) -> list[dict]:
    """
    Fetch top posts from r/all + a random mix of broad subreddits.
    No niche filtering whatsoever.
    """
    # Pick 5 random broad subreddits + always include r/all
    subs = ["all"] + random.sample(DISCOVERY_SUBREDDITS, min(5, len(DISCOVERY_SUBREDDITS)))
    print(f"[Discovery] Subreddits: {subs}")
    posts = []
    headers = {"User-Agent": REDDIT_USER_AGENT, "Accept": "application/json"}

    async with httpx.AsyncClient(timeout=12, headers=headers, follow_redirects=True) as client:
        async def fetch_one(sub: str, sort: str) -> list[dict]:
            try:
                url = f"https://www.reddit.com/r/{sub}/{sort}.json"
                params = {"limit": limit_per_sub, "raw_json": 1}
                if sort == "top":
                    params["t"] = "day"  # always today for zero-bias discovery
                r = await client.get(url, params=params)
                if r.status_code == 429:
                    await asyncio.sleep(2)
                    r = await client.get(url, params=params)
                if r.status_code != 200:
                    return []
                result = []
                for item in r.json().get("data", {}).get("children", []):
                    p = item.get("data", {})
                    if p.get("stickied") or p.get("is_meta"):
                        continue
                    # Skip purely entertainment/meme posts
                    if p.get("subreddit","").lower() in ["funny","memes","pics","gifs","videos"]:
                        continue
                    result.append({
                        "subreddit": p.get("subreddit",""),
                        "title": p.get("title",""),
                        "score": p.get("score", 0),
                        "num_comments": p.get("num_comments", 0),
                        "upvote_ratio": p.get("upvote_ratio", 0),
                        "url": "https://reddit.com" + p.get("permalink",""),
                        "selftext_snippet": p.get("selftext","")[:200],
                    })
                return result
            except Exception as e:
                print(f"[Discovery] r/{sub}/{sort}: {e}")
                return []

        tasks = [fetch_one(sub, sort) for sub in subs for sort in ["top","rising"]]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, list):
                posts.extend(r)

    # Deduplicate, sort by score
    seen, unique = set(), []
    for p in sorted(posts, key=lambda x: x["score"], reverse=True):
        if p["title"] not in seen:
            seen.add(p["title"])
            unique.append(p)

    print(f"[Discovery] {len(unique)} unique posts from global fetch")
    return unique[:40]


async def fetch_google_trending_now() -> dict:
    """
    Fetch what is trending on Google RIGHT NOW — no seed, no topic bias.
    Uses pytrends trending_searches and realtime_trending_searches.
    """
    try:
        from pytrends.request import TrendReq
        country = random.choice(DISCOVERY_COUNTRIES)
        print(f"[Discovery] Google trending in: {country}")

        def _fetch():
            pt = TrendReq(hl="en-US", tz=360, timeout=(10,25))
            results = {}

            # Daily trending searches — top ~20 queries of today
            try:
                df = pt.trending_searches(pn="united_states")
                results["daily_trending"] = df[0].tolist()[:20] if not df.empty else []
            except Exception as e:
                print(f"[GTrends Daily] {e}")
                results["daily_trending"] = []

            # Realtime trending — what is exploding RIGHT NOW
            try:
                rt = pt.realtime_trending_searches(pn="US")
                if rt is not None and not rt.empty:
                    titles = []
                    for col in ["title", "entityNames", "query"]:
                        if col in rt.columns:
                            titles = rt[col].dropna().tolist()[:15]
                            break
                    results["realtime"] = [str(t) for t in titles]
                else:
                    results["realtime"] = []
            except Exception as e:
                print(f"[GTrends Realtime] {e}")
                results["realtime"] = []

            return results

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, _fetch)

    except Exception as e:
        print(f"[GoogleTrending] {e}")
        return {"daily_trending": [], "realtime": [], "error": str(e)}


async def fetch_youtube_trending(limit: int = 25) -> list[dict]:
    """
    Fetch YouTube's official Trending feed (chart=mostPopular) — no search
    query, no niche bias. Requires YOUTUBE_API_KEY (free quota via
    Google Cloud Console). Returns [] if not configured or on error.
    """
    if not YOUTUBE_API_KEY:
        return []
    try:
        country = random.choice(["US", "GB", "AU", "CA"])
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get("https://www.googleapis.com/youtube/v3/videos", params={
                "part": "snippet,statistics",
                "chart": "mostPopular",
                "maxResults": limit,
                "regionCode": country,
                "key": YOUTUBE_API_KEY,
            })
            if r.status_code != 200:
                print(f"[YouTube] {r.status_code}: {r.text[:200]}")
                return []
            items = []
            for v in r.json().get("items", []):
                sn, st = v.get("snippet", {}), v.get("statistics", {})
                items.append({
                    "title": sn.get("title", ""),
                    "category_id": sn.get("categoryId", ""),
                    "channel": sn.get("channelTitle", ""),
                    "views": int(st.get("viewCount", 0)),
                    "region": country,
                })
            return items
    except Exception as e:
        print(f"[YouTube] {e}")
        return []


AMAZON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
}

async def fetch_amazon_book_count(query: str) -> dict:
    """
    Gap analysis: how many books on Amazon already match this niche.
    Scrapes the Amazon Books search results count. Returns count=None
    if blocked or unparseable — caller must handle gracefully.
    """
    import re
    try:
        async with httpx.AsyncClient(timeout=10, headers=AMAZON_HEADERS, follow_redirects=True) as client:
            r = await client.get("https://www.amazon.com/s", params={"k": query, "i": "stripbooks"})
            if r.status_code != 200:
                return {"query": query, "count": None}
            html = r.text
            m = re.search(r'of\s+(?:over\s+)?([\d,]+)\s+results', html, re.IGNORECASE)
            if not m:
                m = re.search(r'([\d,]+)\s+results?\s+for', html, re.IGNORECASE)
            if m:
                return {"query": query, "count": int(m.group(1).replace(",", ""))}
            return {"query": query, "count": None}
    except Exception as e:
        print(f"[Amazon Gap] {query}: {e}")
        return {"query": query, "count": None}


def classify_amazon_saturation(count: Optional[int]) -> tuple[str, str]:
    if count is None:
        return "unknown", "Dati Amazon non disponibili — verifica manualmente su Amazon"
    if count < 200:
        return "opportunity", f"Solo {count} libri su Amazon in questa nicchia — bassa concorrenza, buona opportunita"
    elif count < 1500:
        return "moderate", f"{count} libri su Amazon — concorrenza moderata, serve un angolo specifico"
    else:
        return "saturated", f"{count}+ libri su Amazon — nicchia satura, cerca una sotto-nicchia o angolo molto diverso"


async def fetch_amazon_autocomplete(query: str) -> list[str]:
    """
    Real demand signal: what Amazon's search-bar autocomplete suggests for this
    niche query — reflects actual searches typed by shoppers/readers in the
    Books store. Undocumented endpoint, degrades to [] on any failure.
    """
    try:
        headers = {**AMAZON_HEADERS, "Accept": "application/json"}
        async with httpx.AsyncClient(timeout=8, headers=headers) as client:
            r = await client.get("https://completion.amazon.com/api/2017/suggestions", params={
                "limit": 10,
                "prefix": query,
                "suggestion-type": "KEYWORD",
                "page-type": "Search",
                "alias": "stripbooks",
                "site-variant": "desktop",
                "version": "3",
                "event": "onKeyPress",
                "wc": "",
                "lop": "en_US",
                "mid": "ATVPDKIKX0DER",
            })
            if r.status_code != 200:
                return []
            data = r.json()
            suggestions = []
            for item in data.get("suggestions", []):
                val = item.get("value")
                if val and val.lower() != query.lower():
                    suggestions.append(val)
            return suggestions[:8]
    except Exception as e:
        print(f"[Amazon Autocomplete] {query}: {e}")
        return []


def classify_amazon_demand(suggestions: list[str]) -> tuple[bool, str]:
    if suggestions:
        return True, f"Amazon suggerisce {len(suggestions)} ricerche correlate — i lettori cercano attivamente in questa nicchia"
    return False, "Nessun suggerimento Amazon per questa query — la nicchia potrebbe essere troppo nuova o servire un angolo diverso"


async def fetch_tiktok_trending(limit: int = 20) -> list[dict]:
    """
    Fetch trending hashtags from TikTok Creative Center's public trend API
    (no auth/cookie required for the anonymous "popular" view). TikTok
    frequently changes or rate-limits this endpoint, so this source degrades
    gracefully to [] on any failure, like YouTube.
    """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en",
        }
        async with httpx.AsyncClient(timeout=10, headers=headers) as client:
            r = await client.get("https://ads.tiktok.com/creative_radar_api/v1/popular_trend/hashtag/list", params={
                "page": 1,
                "limit": limit,
                "period": 7,
                "country_code": "US",
                "sort_by": "popular",
            })
            if r.status_code != 200:
                print(f"[TikTok] {r.status_code}: {r.text[:200]}")
                return []
            data = r.json()
            items = []
            for h in data.get("data", {}).get("list", [])[:limit]:
                items.append({
                    "hashtag": h.get("hashtag_name", ""),
                    "rank": h.get("rank"),
                    "publish_cnt": h.get("publish_cnt", 0),
                    "video_views": h.get("video_views", 0),
                })
            return items
    except Exception as e:
        print(f"[TikTok] {e}")
        return []


@app.get("/discover")
async def discover_unbiased(market_language: str = "English"):
    """
    Zero-bias discovery: fetch raw global signals from Reddit + Google Trends,
    then let Claude identify KDP opportunities — no niche pre-selection.
    """
    stamp = now_stamp()

    # Run all fetches in parallel
    reddit_posts, gtrends, youtube_videos, tiktok_hashtags = await asyncio.gather(
        fetch_reddit_global(),
        fetch_google_trending_now(),
        fetch_youtube_trending(),
        fetch_tiktok_trending()
    )

    # Format Reddit data
    reddit_block = ""
    if reddit_posts:
        subs_seen = list(set(p["subreddit"] for p in reddit_posts))
        reddit_block = f"REDDIT — Top & Rising posts TODAY (from {len(subs_seen)} subreddits, no niche filter):\n"
        for i, p in enumerate(reddit_posts[:30], 1):
            snippet = f' | "{p["selftext_snippet"][:80]}..."' if p["selftext_snippet"] else ""
            reddit_block += f'{i}. [r/{p["subreddit"]}] "{p["title"]}" — {p["score"]} upvotes{snippet}\n'
    else:
        reddit_block = "Reddit data unavailable this run.\n"

    # Format Google Trends data
    gtrends_block = ""
    daily = gtrends.get("daily_trending", [])
    realtime = gtrends.get("realtime", [])
    if daily or realtime:
        gtrends_block = "GOOGLE TRENDS — What people are searching RIGHT NOW (no seed, pure signal):\n"
        if daily:
            gtrends_block += f"Today top searches: {', '.join(str(x) for x in daily[:15])}\n"
        if realtime:
            gtrends_block += f"Realtime exploding: {', '.join(str(x) for x in realtime[:10])}\n"
    else:
        gtrends_block = "Google Trends data unavailable this run.\n"

    # Format YouTube Trending data
    youtube_block = ""
    if youtube_videos:
        youtube_block = f"YOUTUBE — Trending NOW ({youtube_videos[0]['region']}, no search query, no niche filter):\n"
        for i, v in enumerate(youtube_videos[:20], 1):
            youtube_block += f'{i}. "{v["title"]}" — {v["channel"]} ({v["views"]:,} views)\n'
    else:
        youtube_block = "YouTube Trending data unavailable (YOUTUBE_API_KEY not set or request failed).\n"

    # Format TikTok Trending data
    tiktok_block = ""
    if tiktok_hashtags:
        tiktok_block = "TIKTOK — Trending hashtags THIS WEEK (no search query, no niche filter):\n"
        for i, h in enumerate(tiktok_hashtags[:20], 1):
            views = f" — {h['video_views']:,} views" if h.get("video_views") else ""
            tiktok_block += f'{i}. #{h["hashtag"]}{views}\n'
    else:
        tiktok_block = "TikTok Trending data unavailable this run.\n"

    lang_cfg = MARKET_LANG_CONFIG.get(market_language, MARKET_LANG_CONFIG["English"])
    amazon_market = lang_cfg["amazon"]
    lang_note = f"\nTARGET MARKET: {market_language} — all book titles and content must be in {market_language}, targeting {amazon_market} readers." if market_language != "English" else ""

    prompt = f"""You are a KDP publishing expert with zero preconceptions about what niche to target.

CURRENT MOMENT: {stamp}{lang_note}

You are about to read RAW, UNFILTERED social data — no topic was specified, no niche was chosen.
Your job: find what is organically emerging and identify KDP book opportunities from it.
{"Translate all book titles and subtitles into " + market_language + " — they must be ready to publish on " + amazon_market + "." if market_language != "English" else ""}

RAW DATA:
{reddit_block}
{gtrends_block}
{youtube_block}
{tiktok_block}

TASK: Identify 5 KDP book opportunities hidden inside this raw data.

RULES — THIS IS CRITICAL:
- You have NO idea what niche to look in — discover it FROM the data
- Each opportunity must come from a REAL signal above (quote it)
- Do NOT apply any pre-existing frameworks about "hot niches"
- Look for: recurring emotional themes, unanswered questions, pain points,
  cultural moments, linguistic patterns across multiple posts
- The niche for each book should emerge ORGANICALLY from patterns you see
- Be specific and surprising — avoid obvious conclusions
- Each of the 5 must be in a DIFFERENT niche/category

TITLE RULES — Amazon KDP rejects listings with "title": "subtitle"-style titles
or keyword-stuffed titles (combined title+subtitle over ~200 characters):
- "title": SHORT and punchy, under 60 characters, NO colon followed by a long
  second subtitle baked into it
- "subtitle": separate field for SEO/keywords, under 140 characters
- title + subtitle combined MUST be under 200 characters total

KDP FIT — for each opportunity, honestly assess:
- "kdp_fit": "high" | "medium" | "low" — how well this niche translates into a
  book/journal/workbook/planner people would actually PAY for, vs. a topic
  people only consume as free video/news/forum content
  - "high" = clear evergreen audience for a companion book/journal/workbook/planner
  - "medium" = possible but needs the right angle (e.g. fandom journal, not a "guide")
  - "low" = pure entertainment/news/gaming content — audience expects free video/wiki, not a paid book
- "kdp_fit_reason": 1 sentence explaining the verdict, specific to this niche

CROSS-SOURCE SCORING — for each opportunity:
- "sources": list which raw data blocks above (reddit, google, youtube, tiktok) contain
  a signal supporting this opportunity. Only include a source if you can quote
  a real signal from it in "data_signals".
- "stage": classify based on signal strength and cross-source presence:
  - "Esplode" = appears in 3-4 sources OR extremely strong signal in 2 (breaking out NOW)
  - "Forte" = appears in 2 sources with strong signal (high demand, validate competition)
  - "Crescita" = appears in 1-2 sources, growing but not yet saturated (optimal KDP window)
  - "Pre-virale" = weak/early signal in 1 source — gap opportunity but unproven demand

Return ONLY raw JSON, no markdown, ASCII-safe strings only:
{{"opportunities":[
{{
  "niche": "The organic niche you discovered (do not use predefined categories)",
  "pattern": "The specific pattern you noticed across multiple data points",
  "data_signals": ["exact Reddit post title or Google query or YouTube title 1", "signal 2", "signal 3"],
  "sources": ["reddit","google"],
  "stage": "Crescita",
  "kdp_fit": "high",
  "kdp_fit_reason": "1 sentence on why this fits a paid book/journal/workbook audience",
  "heat": 4,
  "why_now": "1 sentence: why this moment is the right time for this book",
  "books": [
    {{"type":"Book type","title":"Specific title","subtitle":"Amazon SEO subtitle"}},
    {{"type":"Book type 2","title":"Title 2","subtitle":"Subtitle 2"}}
  ]
}},
{{
  "niche": "Discovered niche 2",
  "pattern": "Pattern observed",
  "data_signals": ["signal 1","signal 2"],
  "sources": ["reddit"],
  "stage": "Pre-virale",
  "kdp_fit": "medium",
  "kdp_fit_reason": "1 sentence",
  "heat": 5,
  "why_now": "1 sentence",
  "books": [
    {{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
    {{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
  ]
}},
{{
  "niche": "Discovered niche 3",
  "pattern": "Pattern",
  "data_signals": ["signal 1","signal 2"],
  "sources": ["google","youtube"],
  "stage": "Forte",
  "kdp_fit": "low",
  "kdp_fit_reason": "1 sentence",
  "heat": 3,
  "why_now": "1 sentence",
  "books": [
    {{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
    {{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
  ]
}},
{{
  "niche": "Discovered niche 4",
  "pattern": "Pattern",
  "data_signals": ["signal 1","signal 2"],
  "sources": ["reddit","google","youtube"],
  "stage": "Esplode",
  "kdp_fit": "high",
  "kdp_fit_reason": "1 sentence",
  "heat": 4,
  "why_now": "1 sentence",
  "books": [
    {{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
    {{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
  ]
}},
{{
  "niche": "Discovered niche 5",
  "pattern": "Pattern",
  "data_signals": ["signal 1","signal 2"],
  "sources": ["reddit"],
  "stage": "Crescita",
  "kdp_fit": "medium",
  "kdp_fit_reason": "1 sentence",
  "heat": 5,
  "why_now": "1 sentence",
  "books": [
    {{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
    {{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
  ]
}}
]}}"""

    try:
        text = call_claude(prompt, 3500)
        result = parse_json_safe(text)

        # Gap analysis — cross-check each discovered niche against Amazon book count
        # and Amazon search autocomplete (real reader demand signal).
        # Run sequentially with a small delay: 10 concurrent requests to Amazon
        # from the same datacenter IP gets rate-limited/blocked almost every time.
        import urllib.parse
        opportunities = result.get("opportunities", [])
        for idx, o in enumerate(opportunities):
            niche = o.get("niche", "")
            if idx > 0:
                await asyncio.sleep(0.8)
            gr, suggestions = await asyncio.gather(
                fetch_amazon_book_count(niche),
                fetch_amazon_autocomplete(niche),
            )
            search_url = "https://www.amazon.com/s?" + urllib.parse.urlencode({"k": niche, "i": "stripbooks"})
            count = gr.get("count")
            level, note = classify_amazon_saturation(count)
            o["gap_analysis"] = {
                "amazon_results": count,
                "saturation": level,
                "note": note,
                "query": gr.get("query"),
                "search_url": search_url,
            }
            has_demand, demand_note = classify_amazon_demand(suggestions)
            o["amazon_demand"] = {
                "suggestions": suggestions,
                "has_signal": has_demand,
                "note": demand_note,
                "search_url": search_url,
            }

        result["meta"] = {
            "mode": "zero_bias_discovery",
            "reddit_posts_analyzed": len(reddit_posts),
            "reddit_subreddits": list(set(p["subreddit"] for p in reddit_posts))[:10],
            "google_daily_trending": gtrends.get("daily_trending", [])[:10],
            "google_realtime": gtrends.get("realtime", [])[:5],
            "youtube_videos_analyzed": len(youtube_videos),
            "youtube_configured": bool(YOUTUBE_API_KEY),
            "tiktok_hashtags_analyzed": len(tiktok_hashtags),
            "fetched_at": stamp,
            "note": "No niche was specified — opportunities discovered purely from raw data"
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/positioning")
async def positioning_to_books(req: PositioningRequest):
    """
    Inverse flow from /discover: instead of starting from 'what's trending'
    and writing a book toward it, start from the author's deliberate
    editorial positioning (identity, ideal reader psychographics, promised
    transformation, competitive differentiation, unfair advantage) and derive
    the niche, angle, and book concepts that express it.
    """
    stamp = now_stamp()

    prompt = f"""You are a KDP positioning strategist helping a publisher who has
ALREADY done market analysis and decided their editorial positioning — they are
NOT chasing trends. Your job is to translate their positioning into a clear
niche/angle and concrete book concepts that express it.

CURRENT MOMENT: {stamp}

AUTHOR/PUBLISHER POSITIONING BRIEF:
- Identity & desired perception: {req.author_identity}
- Ideal reader (psychographic, not demographic): {req.ideal_reader}
- Promised transformation: {req.transformation}
- Competitors & differentiation: {req.competitors or "not specified"}
- Unfair advantage (unique knowledge/experience): {req.unfair_advantage or "not specified"}

TASK:
1. Derive ONE clear editorial positioning statement that ties identity, reader,
   transformation and differentiation together into a coherent angle.
2. Derive the niche this positioning lives in (specific, not generic).
3. Propose 3 book concepts that EXPRESS this positioning — each a different
   format/angle on the same positioning, not random unrelated ideas.

TITLE RULES — Amazon KDP rejects listings with "title": "subtitle"-style titles
or keyword-stuffed titles (combined title+subtitle over ~200 characters):
- "title": SHORT and punchy, under 60 characters, NO colon followed by a long
  second subtitle baked into it
- "subtitle": separate field for SEO/keywords, under 140 characters
- title + subtitle combined MUST be under 200 characters total

Return ONLY raw JSON, no markdown, ASCII-safe strings only:
{{"positioning_summary":"2-3 sentences tying identity, reader, transformation and differentiation into one coherent editorial angle",
"niche":"the specific niche this positioning lives in",
"why_this_works":"1-2 sentences on why this positioning is differentiated and defensible vs competitors",
"books":[
  {{"type":"Book type","title":"Short punchy title","subtitle":"SEO subtitle expressing the positioning"}},
  {{"type":"Book type 2","title":"Title 2","subtitle":"Subtitle 2"}},
  {{"type":"Book type 3","title":"Title 3","subtitle":"Subtitle 3"}}
]}}"""

    try:
        text = call_claude(prompt, 2000)
        result = parse_json_safe(text)
        result["meta"] = {
            "mode": "positioning",
            "fetched_at": stamp,
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trends")
async def get_trends(req: TrendRequest):
    year = datetime.now().year
    stamp = now_stamp()
    platforms_str = ", ".join(req.platforms)

    lang = req.market_language or "English"
    lang_cfg = MARKET_LANG_CONFIG.get(lang, MARKET_LANG_CONFIG["English"])
    amazon_market = lang_cfg["amazon"]
    lang_subreddits = lang_cfg["subreddits"]

    lang_code = LANG_CODE_MAP.get(lang, "en")
    tf_info = get_timeframe(req.timeframe or "week")

    # Primary: Google + YouTube autocomplete (language-aware, works from any IP)
    # Secondary: Google Trends
    # Reddit: English only (low signal for non-EN markets)
    fetch_tasks = [
        fetch_multi_autocomplete(req.niche, lang_code),
        fetch_google_trends(req.niche, req.keyword or "", req.timeframe or "week"),
    ]
    if lang == "English":
        fetch_tasks.append(fetch_reddit_posts(req.niche, req.keyword or "", req.timeframe or "week", force_subreddits=lang_subreddits))
    results = await asyncio.gather(*fetch_tasks, return_exceptions=True)

    autocomplete_data = results[0] if isinstance(results[0], dict) else {"google": [], "youtube": []}
    gtrends = results[1] if isinstance(results[1], dict) else {}
    reddit_posts = results[2] if len(results) > 2 and isinstance(results[2], list) else []

    autocomplete_block = ""
    if autocomplete_data["google"]:
        autocomplete_block += f"GOOGLE SEARCH — What {lang} speakers actively search in this niche:\n"
        for s in autocomplete_data["google"][:20]:
            autocomplete_block += f'  - "{s}"\n'
    if autocomplete_data["youtube"]:
        autocomplete_block += f"\nYOUTUBE — What {lang} speakers want to learn (video intent):\n"
        for s in autocomplete_data["youtube"][:12]:
            autocomplete_block += f'  - "{s}"\n'
    if not autocomplete_block:
        autocomplete_block = "Autocomplete data unavailable this run.\n"

    gtrends_summary = ""
    if gtrends.get("avg_interest"):
        gtrends_summary = "GOOGLE TRENDS — Interest over time:\n"
        for term, val in gtrends["avg_interest"].items():
            gtrends_summary += f"  '{term}': {val}/100\n"
        if gtrends.get("rising_queries"):
            gtrends_summary += "Rising queries:\n"
            for term, queries in gtrends["rising_queries"].items():
                if queries:
                    tops = [q.get("query","") for q in queries[:3]]
                    gtrends_summary += f"  Under '{term}': {', '.join(tops)}\n"

    reddit_summary = ""
    if reddit_posts:
        reddit_summary = "\nREDDIT (English signal) — Viral posts:\n"
        for i, p in enumerate(reddit_posts[:12], 1):
            reddit_summary += f'{i}. [r/{p["subreddit"]}] "{p["title"]}" — {p["score"]} upvotes\n'

    prompt = f"""You are a KDP publishing expert analyzing REAL search intent data.

CURRENT MOMENT: {stamp}
ANALYSIS WINDOW: {tf_info["label"]}
STRATEGIC CONTEXT: {tf_info["strategy"]}
TARGET MARKET: {lang} — books must be written in {lang}, targeting {amazon_market}
{"IMPORTANT: All book titles, subtitles, descriptions must be in " + lang + ". Trends must resonate with " + lang + "-speaking readers and their cultural context." if lang != "English" else ""}

REAL SEARCH INTENT DATA (what people are actively searching right now):
{autocomplete_block}
{gtrends_summary}{reddit_summary}

TASK: Identify 4 SPECIFIC, UNDERSERVED KDP book opportunities for the "{req.niche}" category on {amazon_market}.
Platforms context: {platforms_str}
{f'Keyword focus: "{req.keyword}"' if req.keyword else ''}

INTERPRETATION GUIDE:
- Autocomplete queries = proven demand (people typing this = they want content on it)
- High Google Trends score = broad awareness
- Rising queries = emerging, not yet saturated — BEST opportunity
- Find the intersection: high search intent + low existing books = gap

UNIQUENESS RULES:
- Do NOT suggest: generic journals, gratitude journals, mindfulness basics, morning routines
- Each trend must cite a SPECIFIC autocomplete query from the data above as its signal
- Find angles that feel fresh and slightly unexpected

TITLE RULES:
- "title": SHORT and punchy, under 60 characters, NO colon-subtitle inside it
- "subtitle": separate SEO field, under 140 characters
- title + subtitle combined MUST be under 200 characters

Return ONLY raw JSON, no markdown, ASCII-safe strings only:
{{"trends":[
{{"name":"SPECIFIC TREND","platform":"Google/YouTube","description":"2 sentences citing a specific autocomplete query","heat":4,"data_signal":"Exact autocomplete query that proves demand","books":[
{{"type":"TYPE","title":"TITLE","subtitle":"SEO subtitle"}},
{{"type":"TYPE","title":"TITLE 2","subtitle":"SEO subtitle 2"}}
]}},
{{"name":"TREND 2","platform":"Google/YouTube","description":"2 sentences","heat":5,"data_signal":"exact signal","books":[
{{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
{{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
]}},
{{"name":"TREND 3","platform":"Google/YouTube","description":"2 sentences","heat":3,"data_signal":"signal","books":[
{{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
{{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
]}},
{{"name":"TREND 4","platform":"Google/YouTube","description":"2 sentences","heat":4,"data_signal":"signal","books":[
{{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
{{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
]}}
]}}"""

    try:
        text = call_claude(prompt, 3000)
        result = parse_json_safe(text)
        result["meta"] = {
            "reddit_posts_found": len(reddit_posts),
            "google_autocomplete_found": len(autocomplete_data["google"]),
            "youtube_autocomplete_found": len(autocomplete_data["youtube"]),
            "gtrends_avg": gtrends.get("avg_interest", {}),
            "fetched_at": stamp,
            "timeframe": req.timeframe or "week",
            "timeframe_label": tf_info["label"],
            "timeframe_strategy": tf_info["strategy"],
            "data_sources": {
                "google_autocomplete": len(autocomplete_data["google"]) > 0,
                "youtube_autocomplete": len(autocomplete_data["youtube"]) > 0,
                "reddit": len(reddit_posts) > 0,
                "google_trends": bool(gtrends.get("avg_interest"))
            }
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/validate-niche")
async def validate_niche(req: dict):
    """Quick validation: fetch autocomplete + Google Trends for a specific niche name."""
    niche = req.get("niche", "")
    market_language = req.get("market_language", "English")
    lang_code = LANG_CODE_MAP.get(market_language, "en")
    lang_cfg = MARKET_LANG_CONFIG.get(market_language, MARKET_LANG_CONFIG["English"])
    amazon_market = lang_cfg["amazon"]
    import urllib.parse

    autocomplete_data, gtrends = await asyncio.gather(
        fetch_multi_autocomplete(niche, lang_code),
        fetch_google_trends(niche, "", "month"),
    )

    search_url = "https://" + lang_cfg["amazon"].split("/")[0].replace("Amazon.", "amazon.") + "/s?" + urllib.parse.urlencode({"k": niche, "i": "stripbooks"})
    gtrends_url = "https://trends.google.com/trends/explore?" + urllib.parse.urlencode({"q": niche, "geo": lang_code.upper()})

    gt_score = None
    if gtrends.get("avg_interest"):
        vals = list(gtrends["avg_interest"].values())
        gt_score = round(sum(vals) / len(vals)) if vals else None

    return {
        "niche": niche,
        "market_language": market_language,
        "amazon_market": amazon_market,
        "google_suggestions": autocomplete_data.get("google", [])[:15],
        "youtube_suggestions": autocomplete_data.get("youtube", [])[:10],
        "google_trends_score": gt_score,
        "rising_queries": [q.get("query","") for qs in (gtrends.get("rising_queries") or {}).values() for q in qs[:2]][:6],
        "amazon_search_url": search_url,
        "google_trends_url": gtrends_url,
    }


@app.post("/niches")
async def discover_niches(req: NicheRequest):
    stamp = now_stamp()
    year = datetime.now().year

    tf_info = get_timeframe(req.timeframe or "week")
    general_posts, gtrends = await asyncio.gather(
        fetch_reddit_posts("Any niche", req.keyword or "", req.timeframe or "week"),
        fetch_google_trends("Any niche", req.keyword or "", req.timeframe or "week")
    )

    reddit_summary = ""
    if general_posts:
        subs_used = list(set(p["subreddit"] for p in general_posts))
        reddit_summary = f"Reddit posts this week (subreddits: {', '.join(subs_used[:6])}):\n"
        for p in general_posts[:20]:
            reddit_summary += f"- [r/{p['subreddit']}] \"{p['title']}\" ({p['score']} pts)\n"

    gtrends_summary = ""
    if gtrends.get("rising_queries"):
        gtrends_summary = f"Google rising queries (seeds: {', '.join(gtrends.get('terms',[]))}):\n"
        for term, queries in gtrends["rising_queries"].items():
            for q in queries[:3]:
                gtrends_summary += f"  - {q.get('query','')}\n"

    prompt = f"""You are a KDP niche analyst. Today is {stamp}.

REAL DATA:
{reddit_summary}
{gtrends_summary}

Find 8 SPECIFIC, UNDERSERVED KDP niches that are genuinely emerging RIGHT NOW.

RULES:
- NO generic suggestions (no "self-help journal", "gratitude journal", "mindfulness basics")
- Each niche must be supported by a specific signal from the data
- Look for niches that are JUST emerging, not already saturated
- Think cross-cultural, counter-intuitive, niche-within-niche angles
- Variety: each of the 8 must be in a different micro-category

Return ONLY raw JSON, ASCII-safe text only:
{{"niches":[
{{"name":"Specific 2-5 word niche","reason":"Why emerging now — 1 sentence referencing data","heat":4,"example_book":"Specific KDP title","data_signal":"Exact Reddit post or Google query that supports this"}},
{{"name":"Niche 2","reason":"1 sentence","heat":5,"example_book":"Title","data_signal":"signal"}},
{{"name":"Niche 3","reason":"1 sentence","heat":3,"example_book":"Title","data_signal":"signal"}},
{{"name":"Niche 4","reason":"1 sentence","heat":5,"example_book":"Title","data_signal":"signal"}},
{{"name":"Niche 5","reason":"1 sentence","heat":4,"example_book":"Title","data_signal":"signal"}},
{{"name":"Niche 6","reason":"1 sentence","heat":3,"example_book":"Title","data_signal":"signal"}},
{{"name":"Niche 7","reason":"1 sentence","heat":4,"example_book":"Title","data_signal":"signal"}},
{{"name":"Niche 8","reason":"1 sentence","heat":5,"example_book":"Title","data_signal":"signal"}}
]}}"""

    try:
        text = call_claude(prompt, 2500)
        result = parse_json_safe(text)
        result["meta"] = {
            "reddit_posts_found": len(general_posts),
            "gtrends_seeds": gtrends.get("terms",[]),
            "fetched_at": stamp
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate")
async def generate_content(req: GenerateRequest):
    book_ctx = (
        f'Book: "{req.book_title}" - {req.book_subtitle}\n'
        f'Type: {req.book_type}\n'
        f'Trend: "{req.trend_name}"\n'
        f'Audience: {req.audience}'
    )
    # Get book-type-specific template
    book_tmpl = get_book_template(req.book_type)
    book_format_ctx = f"""BOOK FORMAT RULES (follow precisely for {req.book_type}):
Structure: {book_tmpl["structure"]}
Chapter instruction: {book_tmpl["chapter_instruction"]}
Length note: {book_tmpl["length_note"]}
Unique elements: {book_tmpl["unique_elements"]}"""

    voice_ctx = build_voice_ctx(
        tone=req.tone,
        language=req.language or "English",
        cultural_inspiration=req.cultural_inspiration or "",
        chapter_length=req.chapter_length or "medium",
        reader_persona=req.reader_persona or "",
        custom_instructions=req.custom_instructions or ""
    )
    length_map = {"short": "800-1000", "medium": "1200-1600", "long": "2000-2500"}
    word_count = length_map.get(req.chapter_length or "medium", "1200-1600")

    if req.tab == "outline":
        prompt = f"""You are a bestselling KDP author. Create a detailed book outline.

{book_ctx}

{book_format_ctx}

{voice_ctx}

Write a professional outline with 10 chapters structured for a {req.book_type}.
For each chapter: chapter number, punchy title, and 4 subsection titles.

Format:
Chapter 1: Title
  1.1 Subsection
  1.2 Subsection
  1.3 Subsection
  1.4 Subsection

All 10 chapters. No extra text."""
        max_tok = 3000

    elif req.tab in ("chapter", "allchapters"):
        n = req.chapter_num or 1
        prompt = f"""You are a bestselling KDP author. Write Chapter {n}.

{book_ctx}
{f"Outline:{chr(10)}{req.outline[:600]}" if req.outline else ""}

{book_format_ctx}

{voice_ctx}

Write CHAPTER {n} completely following the book format rules above.
- Chapter title as header
- Follow the opening style specified above EXACTLY
- Follow the chapter instruction for {req.book_type} precisely
- Target: {word_count} words

Make it feel like no other chapter in any other book."""
        max_tok = 8000

    elif req.tab == "intro":
        prompt = f"""You are a bestselling KDP author. Write the Introduction AND Conclusion.

{book_ctx}
{voice_ctx}

INTRODUCTION ({word_count} words):
- Follow the opening style specified above
- Why this book exists and who it is for
- What the reader will gain
- How to use the book

CONCLUSION (600-800 words):
- Recap the transformation arc
- Motivational, specific closing
- Next steps / call to action"""
        max_tok = 3000

    elif req.tab == "full":
        prompt = f"""You are a bestselling KDP author. Write a complete {req.book_type}.

{book_ctx}
{voice_ctx}

Write the FULL book:
- Introduction (400-500 words)
- 6 complete chapters ({word_count} words each) with content, prompts, exercises
- Conclusion (300-400 words)

Follow voice guidelines throughout. Make every chapter feel distinct."""
        max_tok = 8000
    else:
        raise HTTPException(status_code=400, detail=f"Unknown tab: {req.tab}")

    try:
        allow_trunc = req.tab in ("chapter", "allchapters", "draft")
        text = call_claude(prompt, max_tok, allow_truncated=allow_trunc)
        return {"content": text, "tab": req.tab, "chapter_num": req.chapter_num}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate-all")
async def generate_all_chapters(req: AllChaptersRequest):
    import re as _re
    book_ctx = (
        f'Book: "{req.book_title}" - {req.book_subtitle}\n'
        f'Type: {req.book_type}\n'
        f'Trend: "{req.trend_name}"\n'
        f'Audience: {req.audience}'
    )
    length_map = {"short": "800-1000", "medium": "1200-1600", "long": "2000-2500"}
    word_count = length_map.get(req.chapter_length or "medium", "1200-1600")

    chapter_pattern = _re.compile(r'^(?:Chapter\s+)?(\d+)[:\.\)]\s*(.+)$', _re.MULTILINE | _re.IGNORECASE)
    chapters = []
    for m in chapter_pattern.finditer(req.outline):
        if '.' not in m.group(1):
            chapters.append({"num": int(m.group(1)), "title": m.group(2).strip()})
    seen_nums, unique_chapters = set(), []
    for ch in sorted(chapters, key=lambda x: x["num"]):
        if ch["num"] not in seen_nums:
            seen_nums.add(ch["num"])
            unique_chapters.append(ch)
    if not unique_chapters:
        raise HTTPException(status_code=400, detail="Nessun capitolo trovato. Genera prima l'Outline.")

    total = len(unique_chapters)
    outline_snippet = req.outline[:800]

    async def chapter_stream():
        for ch in unique_chapters:
            n, title = ch["num"], ch["title"]
            # Each chapter gets its own random opening style + uniqueness seed
            voice_ctx = build_voice_ctx(
                tone=req.tone,
                language=req.language or "English",
                cultural_inspiration=req.cultural_inspiration or "",
                chapter_length=req.chapter_length or "medium",
                reader_persona=req.reader_persona or "",
                custom_instructions=req.custom_instructions or ""
            )
            prompt = f"""You are a bestselling KDP author. Write Chapter {n} of {total}.

{book_ctx}
Chapter title: {title}
Outline reference:
{outline_snippet}

{voice_ctx}

Write CHAPTER {n} — "{title}" — completely:
- Open with chapter title as header
- Follow the opening style above EXACTLY — make it vivid and unexpected
- 3-4 full sections with subheadings
- Content, prompts or exercises appropriate for {req.book_type}
- Chapter summary at the end
- Target: {word_count} words

This chapter must feel completely distinct from chapters before it.
Use the uniqueness seed to ensure this version is unlike any previous generation."""

            try:
                text = call_claude(prompt, 8000, allow_truncated=True)
                yield json.dumps({
                    "chapter": n, "title": title, "content": text,
                    "total": total, "done": False
                }, ensure_ascii=False) + "\n"
            except Exception as e:
                yield json.dumps({
                    "chapter": n, "title": title, "content": "",
                    "error": str(e), "total": total, "done": False
                }) + "\n"

            await asyncio.sleep(0.5)

        yield json.dumps({"done": True, "total": total}) + "\n"

    return StreamingResponse(
        chapter_stream(),
        media_type="application/x-ndjson",
        headers={"X-Total-Chapters": str(total)}
    )


@app.post("/analyze-market")
async def analyze_market(req: dict):
    """
    Analyze market positioning based on user-pasted Amazon competitor data.
    User pastes titles/prices from Amazon search results, Claude analyzes.
    """
    titles = req.get("titles", [])         # list of competitor titles
    prices = req.get("prices", [])          # list of prices as strings
    book_title = req.get("book_title", "")
    book_type = req.get("book_type", "")
    niche = req.get("niche", "")
    stamp = now_stamp()

    if not titles:
        raise HTTPException(status_code=400, detail="Provide at least 3 competitor titles")

    competitors_block = "\n".join(
        f'- "{t}" — ${prices[i]}' if i < len(prices) and prices[i] else f'- "{t}"'
        for i, t in enumerate(titles)
    )

    prompt = f"""You are an Amazon KDP market analyst. Analyze this competitor data and give strategic advice.

My book: "{book_title}" ({book_type}) in niche: "{niche}"
Analysis date: {stamp}

COMPETITOR TITLES ON AMAZON:
{competitors_block}

Analyze and return ONLY raw JSON, ASCII-safe:
{{"analysis":{{
  "competitor_count": {len(titles)},
  "saturation_level": "low|medium|high",
  "saturation_score": 3,
  "avg_price_estimate": "$X.XX",
  "price_sweet_spot": "$X.XX - $X.XX",
  "title_patterns": ["pattern 1 seen in competitors","pattern 2","pattern 3"],
  "gaps_identified": ["gap or angle not covered by competitors 1","gap 2","gap 3"],
  "positioning_advice": "2-3 sentences on how to differentiate from these competitors",
  "recommended_title_angle": "Specific angle for MY book title that stands out from these competitors",
  "subtitle_keywords": ["keyword 1","keyword 2","keyword 3","keyword 4"],
  "verdict": "go|caution|avoid",
  "verdict_reason": "1 sentence explaining the verdict"
}}}}"""

    try:
        text = call_claude(prompt, 1500)
        result = parse_json_safe(text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/title-variants")
async def generate_title_variants(req: dict):
    """
    Generate 5 title variants with different positioning angles.
    """
    book_type = req.get("book_type", "")
    niche = req.get("niche", "")
    trend = req.get("trend", "")
    audience = req.get("audience", "")
    current_title = req.get("current_title", "")
    language = req.get("language", "English")
    real_keywords = req.get("real_keywords", [])

    kw_context = ""
    if real_keywords:
        kw_context = f"\nReal search terms from Google/Amazon autocomplete (use these to make titles resonate with actual searches): {', '.join(real_keywords[:15])}\n"

    prompt = f"""You are an Amazon KDP title expert. Generate 5 title variants with different angles.

Book type: {book_type}
Niche/trend: {niche} — {trend}
Audience: {audience}
Current working title: "{current_title}"
Output language: {language}{kw_context}

Generate 5 title + subtitle combinations, each with a DIFFERENT psychological angle:
1. CURIOSITY GAP — makes reader feel they are missing crucial knowledge
2. BENEFIT-DRIVEN — leads with the transformation or outcome
3. PROBLEM-AWARE — names the specific pain point first
4. IDENTITY-BASED — speaks to who the reader wants to become
5. AUTHORITY/METHOD — implies a specific system or proven approach

Return ONLY raw JSON, ASCII-safe:
{{"variants":[
{{"angle":"Curiosity Gap","title":"Title here","subtitle":"Subtitle here","why":"1 sentence why this angle works for this audience"}},
{{"angle":"Benefit-Driven","title":"Title here","subtitle":"Subtitle here","why":"1 sentence"}},
{{"angle":"Problem-Aware","title":"Title here","subtitle":"Subtitle here","why":"1 sentence"}},
{{"angle":"Identity-Based","title":"Title here","subtitle":"Subtitle here","why":"1 sentence"}},
{{"angle":"Authority/Method","title":"Title here","subtitle":"Subtitle here","why":"1 sentence"}}
]}}"""

    try:
        text = call_claude(prompt, 1500)
        return parse_json_safe(text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/package")
async def generate_package(req: PackageRequest):
    tone_note = f"Tone/voice of the book: {req.tone}" if req.tone else ""
    persona_note = f"Target reader persona: {req.reader_persona}" if req.reader_persona else ""
    custom_note = f"\nCUSTOM RESTRICTIONS (MANDATORY — apply to every field):\n{req.custom_instructions}" if req.custom_instructions else ""
    stamp = now_stamp()

    # Determine target marketplace from language
    lang = getattr(req, 'language', 'English') or 'English'
    marketplace_map = {
        "Italian": "Amazon.it",
        "Dutch": "Amazon.nl",
        "German": "Amazon.de",
        "French": "Amazon.fr",
        "Spanish": "Amazon.es",
        "English": "Amazon.com",
    }
    marketplace = marketplace_map.get(lang, "Amazon.com")
    lang_note = f"Output language: {lang} (optimize for {marketplace})" if lang != "English" else "Output language: English (optimize for Amazon.com and Amazon.co.uk)"

    prompt = f"""You are an Amazon KDP publishing expert. Generate a complete KDP listing package.

Book: "{req.book_title}" — {req.book_subtitle}
Type: {req.book_type}
Trend: "{req.trend_name}"
Audience: {req.audience}
Platform: {req.trend_platform}
{tone_note}
{persona_note}
{lang_note}{custom_note}
Generated: {stamp}

IMPORTANT: Write title, subtitle, description, tagline, and keywords in {lang}.
Keywords must be search terms that {lang}-speaking readers actually use on {marketplace}.

TITLE RULES — THIS IS CRITICAL, Amazon KDP REJECTS listings that violate this:
- "title": SHORT and punchy, under 60 characters. Must NOT contain a colon
  followed by a second long subtitle baked into it (e.g. do not write
  "Main Title: Long Secondary Subtitle Full Of Keywords" as the title)
- "subtitle": separate field for SEO/keywords, under 140 characters
- title + subtitle combined MUST be under 200 characters total — this is a
  hard Amazon limit and listings over it get rejected as "disappointing
  customer experience"

Return ONLY raw JSON. No markdown. ASCII-safe strings only.

{{"kdp":{{"title":"short punchy title, under 60 chars, no embedded subtitle","subtitle":"SEO subtitle, under 140 chars, title+subtitle combined under 200 chars total","pen_name":"believable author name fitting this niche and tone","pen_name_rationale":"1 sentence why this name works","description":"Full Amazon description 400-600 words. Use <b> for headers, <br> for breaks. Hook, benefits, who it is for.","short_description":"80-word mobile preview","keywords":["kw1","kw2","kw3","kw4","kw5","kw6","kw7"],"categories":["Primary Amazon category","Secondary Amazon category"],"bisac":["BISAC 1","BISAC 2"],"price_ebook":4.99,"price_paperback":12.99,"page_count_estimate":120,"trim_size":"6x9","tagline":"Punchy tagline under 15 words","canva_cover":{{"main_prompt":"60-80 word Canva AI image prompt for cover background. Mood colors lighting style. No text in scene.","style":"one-word style","color_palette":["#hex1","#hex2","#hex3"],"color_palette_names":["name1","name2","name3"],"font_title":"Canva font for title","font_subtitle":"Canva font for subtitle and author","layout_tip":"One sentence on placement","variation_1":"Alternative 40-word prompt","variation_2":"Alternative 40-word prompt","canva_steps":"4-5 step instructions for KDP-ready cover in Canva"}}}}}}"""

    try:
        text = call_claude(prompt, 4000)
        result = parse_json_safe(text)
        kdp = result.get("kdp", {})
        title = kdp.get("title", "") or ""
        subtitle = kdp.get("subtitle", "") or ""
        warnings = []
        # Amazon KDP hard limit: title + subtitle combined <= 200 chars.
        # If Claude still baked a second subtitle into the title (the
        # "Title: Long Keyword-Stuffed Subtitle" pattern that gets listings
        # rejected as "disappointing customer experience"), split it off.
        if ":" in title and len(title) > 60:
            head, _, tail = title.partition(":")
            head, tail = head.strip(), tail.strip()
            if head and len(head) < 60:
                title = head
                subtitle = (tail + (" — " + subtitle if subtitle else "")).strip(" —")
                warnings.append("Titolo conteneva un sottotitolo incorporato — separato automaticamente")
        if len(title) + len(subtitle) > 200:
            max_subtitle = max(0, 200 - len(title))
            if len(subtitle) > max_subtitle:
                subtitle = subtitle[:max_subtitle].rsplit(" ", 1)[0]
                warnings.append("Sottotitolo troncato per rispettare il limite Amazon di 200 caratteri (titolo+sottotitolo)")
        kdp["title"] = title
        kdp["subtitle"] = subtitle
        if warnings:
            kdp["title_warnings"] = warnings
        result["kdp"] = kdp
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════════════════════════════
# APIFY INTEGRATION
# ══════════════════════════════════════════════════════════════

APIFY_TOKEN = env("APIFY_TOKEN")
APIFY_BASE = "https://api.apify.com/v2"

NICHE_CATEGORY_URLS = {
    "Self-help": "https://www.amazon.com/Best-Sellers-Books-Self-Help/zgbs/books/4736",
    "Self-help & Personal growth": "https://www.amazon.com/Best-Sellers-Books-Self-Help/zgbs/books/4736",
    "Health": "https://www.amazon.com/Best-Sellers-Books-Health-Fitness-Dieting/zgbs/books/6",
    "Health & Wellness": "https://www.amazon.com/Best-Sellers-Books-Health-Fitness-Dieting/zgbs/books/6",
    "Finance": "https://www.amazon.com/Best-Sellers-Books-Business-Money/zgbs/books/2",
    "Finance & Money": "https://www.amazon.com/Best-Sellers-Books-Business-Money/zgbs/books/2",
    "Relationships": "https://www.amazon.com/Best-Sellers-Books-Relationships-Parenting-Personal-Development/zgbs/books/48",
    "Relationships & Dating": "https://www.amazon.com/Best-Sellers-Books-Relationships-Parenting-Personal-Development/zgbs/books/48",
    "Productivity": "https://www.amazon.com/Best-Sellers-Books-Time-Management/zgbs/books/173514",
    "Mindset": "https://www.amazon.com/Best-Sellers-Books-Success-Self-Motivation/zgbs/books/4019",
    "Fitness": "https://www.amazon.com/Best-Sellers-Books-Exercise-Fitness/zgbs/books/31",
    "Parenting": "https://www.amazon.com/Best-Sellers-Books-Parenting-Relationships/zgbs/books/4735",
    "Business": "https://www.amazon.com/Best-Sellers-Books-Entrepreneurship/zgbs/books/12901",
    "Psychology": "https://www.amazon.com/Best-Sellers-Books-Psychology-Counseling/zgbs/books/25",
}

MARKET_GEO_MAP = {
    "English": "US",
    "Italiano": "IT",
    "Tedesco": "DE",
    "Spagnolo": "ES",
    "Francese": "FR",
    "Portoghese": "BR",
}


async def run_actor(actor_id: str, input_data: dict, timeout_sec: int = 120) -> list:
    """Launch an Apify actor synchronously and return the dataset items."""
    if not APIFY_TOKEN:
        raise HTTPException(status_code=503, detail="APIFY_TOKEN non configurato — aggiungerlo nelle variabili d'ambiente Railway")
    actor_id_url = actor_id.replace("/", "~")
    async with httpx.AsyncClient(timeout=timeout_sec + 15) as client:
        try:
            run_res = await client.post(
                f"{APIFY_BASE}/acts/{actor_id_url}/runs",
                params={"token": APIFY_TOKEN, "waitForFinish": timeout_sec},
                json=input_data,
            )
            run_res.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Apify actor '{actor_id}' HTTP {e.response.status_code} — {e.response.text[:300]}",
            )
        run_data = run_res.json().get("data", {})
        dataset_id = run_data.get("defaultDatasetId")
        if not dataset_id:
            raise HTTPException(status_code=502, detail="Apify actor non ha restituito un dataset ID")
        try:
            data_res = await client.get(
                f"{APIFY_BASE}/datasets/{dataset_id}/items",
                params={"token": APIFY_TOKEN, "format": "json"},
            )
            data_res.raise_for_status()
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Apify dataset fetch HTTP {e.response.status_code}",
            )
        return data_res.json()


@app.post("/api/apify/trends")
async def apify_trends(req: dict):
    """Google Trends data for given keywords (automation-lab/google-trends-scraper)."""
    keywords = req.get("keywords", [])
    market_language = req.get("market_language", "English")
    geo = MARKET_GEO_MAP.get(market_language, "US")
    try:
        data = await run_actor(
            "automation-lab/google-trends-scraper",
            {"searchTerms": keywords, "timeRange": "today 3-m", "geo": geo, "outputMode": "interest_over_time"},
            timeout_sec=90,
        )
        return {"data": data, "geo": geo}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def _amazon_autocomplete(query: str) -> list[str]:
    """Call Amazon's autocomplete API (2017 version) directly — no Apify, sub-second."""
    async with httpx.AsyncClient(timeout=8) as client:
        res = await client.get(
            "https://completion.amazon.com/api/2017/suggestions",
            params={
                "lop": "en_US",
                "site-variant": "desktop",
                "category": "stripbooks",
                "prefix": query,
                "mid": "ATVPDKIKX0DER",
                "alias": "stripbooks",
            },
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Accept": "application/json",
                "Referer": "https://www.amazon.com/",
            },
        )
        res.raise_for_status()
        payload = res.json()
        # Format: {"suggestions": [{"value": "...", "refTag": "..."}, ...]}
        suggestions = payload.get("suggestions", [])
        return [s["value"] for s in suggestions if isinstance(s, dict) and s.get("value")]


@app.post("/api/apify/amazon-niche")
async def apify_amazon_niche(req: dict):
    """Amazon keyword autocomplete — direct call, no actor cold start."""
    keyword = req.get("keyword", "")
    if not keyword:
        return {"data": []}
    try:
        suggestions = await _amazon_autocomplete(keyword)
        return {"data": [{"platform": "amazon", "suggestions": suggestions}]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/apify/amazon-best")
async def apify_amazon_best(req: dict):
    """Amazon keyword autocomplete for a niche — direct call, no actor cold start."""
    niche = req.get("niche", "")
    if not niche:
        return {"data": []}
    try:
        suggestions = await _amazon_autocomplete(niche)
        return {"data": [{"platform": "amazon", "suggestions": suggestions}]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/apify/keywords")
async def apify_keywords(req: dict):
    """Multi-platform keyword suggestions + optional long-tail SEO metrics."""
    query = req.get("query", "")
    platforms = req.get("platforms", ["google", "amazon", "pinterest"])
    longtail = req.get("longtail", False)

    async def suggestions_call():
        return await run_actor(
            "keyword-auto-complete/keyword-suggestions",
            {"query": query, "platforms": platforms, "maxSuggestions": 15},
            timeout_sec=60,
        )

    async def longtail_call():
        if not longtail:
            return []
        return await run_actor(
            "powerai/long-tail-keyword-discovery",
            {"keyword": query, "country": "US", "limit": 20},
            timeout_sec=90,
        )

    try:
        sugg_data, lt_data = await asyncio.gather(
            suggestions_call(), longtail_call(), return_exceptions=True
        )
        if isinstance(sugg_data, Exception):
            sugg_data = []
        if isinstance(lt_data, Exception):
            lt_data = []
        return {"data": sugg_data, "longtail": lt_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/apify/captions")
async def apify_captions(req: dict):
    """Generate social media captions using platform-specific actors in parallel."""
    platforms = req.get("platforms", ["instagram", "facebook"])
    tone = req.get("tone", "warm")
    language = req.get("language", "it")
    custom_context = req.get("customContext", "")

    ACTOR_MAP = {
        "instagram": "powerai/instagram-ad-copywriter-creator",
        "facebook":  "powerai/facebook-ad-copywriter-creator",
        "twitter":   "easyapi/twitter-thread-generator",
        "linkedin":  "easyapi/linkedin-posts-generator",
    }

    async def run_platform(platform: str) -> list:
        actor_id = ACTOR_MAP.get(platform)
        if not actor_id:
            return []
        actor_input = {
            "topic":    custom_context or "Book promotion post",
            "tone":     tone,
            "language": language,
        }
        try:
            items = await run_actor(actor_id, actor_input, timeout_sec=90)
            for item in items:
                if isinstance(item, dict):
                    item["platform"] = platform
            return items
        except Exception as e:
            return [{"platform": platform, "caption": f"⚠️ {str(e)[:120]}", "error": True}]

    try:
        results = await asyncio.gather(*[run_platform(p) for p in platforms])
        flat = [item for sub in results for item in sub]
        return {"data": flat}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/apify/video-story")
async def apify_video_story(req: dict):
    """Generate AI story video (apify/ai-story-short-video-generator)."""
    prompt = req.get("prompt", "")
    duration = req.get("duration", 30)
    output_platform = req.get("outputPlatform", "instagram")
    try:
        data = await run_actor(
            "apify/ai-story-short-video-generator",
            {"prompt": prompt, "duration": duration, "outputPlatform": output_platform, "style": "cinematic"},
            timeout_sec=180,
        )
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/apify/video-ugc")
async def apify_video_ugc(req: dict):
    """Generate UGC video from cover image (actums/ai-ugc-video-maker)."""
    image_url = req.get("imageUrl", "")
    platform = req.get("platform", "tiktok")
    duration = req.get("duration", 30)
    try:
        data = await run_actor(
            "actums/ai-ugc-video-maker",
            {"imageUrl": image_url, "platform": platform, "duration": duration},
            timeout_sec=180,
        )
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/apify/social-post")
async def apify_social_post(req: dict):
    """Publish/analyze social content (alizarin_refrigerator-owner/social-media-mcp-server)."""
    caption = req.get("caption", "")
    platforms = req.get("platforms", [])
    social_keys = req.get("socialKeys", {})
    action = req.get("action", "post")
    topic = req.get("topic", "")
    image_url = req.get("imageUrl", "")
    try:
        data = await run_actor(
            "alizarin_refrigerator-owner/social-media-mcp-server",
            {
                "action": action,
                "caption": caption,
                "platforms": platforms,
                "apiKeys": social_keys,
                "topic": topic,
                "imageUrl": image_url,
            },
            timeout_sec=120,
        )
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/apify/influencers")
async def apify_influencers(req: dict):
    """Find influencers by niche (easyapi/find-my-influencers)."""
    niche = req.get("niche", "")
    platforms = req.get("platforms", ["instagram", "tiktok"])
    try:
        data = await run_actor(
            "easyapi/find-my-influencers",
            {"niche": niche, "platforms": platforms, "limit": 20},
            timeout_sec=120,
        )
        return {"data": data}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ══════════════════════════════════════════════════════════════
# ENTRY POINT
# ══════════════════════════════════════════════════════════════
if __name__ == "__main__":
    import uvicorn

    env_file = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(env_file):
        print(f"[KDP Studio] Loading .env")
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, _, val = line.partition("=")
                    os.environ[key.strip()] = val.strip().strip('"').strip("'")
        import sys
        _m = sys.modules[__name__]
        _m.ANTHROPIC_KEY     = env("ANTHROPIC_API_KEY")
        _m.REDDIT_USER_AGENT = env("REDDIT_USER_AGENT", "KDPStudio/1.0 (personal use, no auth)")
        _m.claude = anthropic.Anthropic(api_key=_m.ANTHROPIC_KEY)

    print("\n🚀 KDP Studio Backend v2")
    print(f"   Claude API:      {'OK' if ANTHROPIC_KEY else 'MISSING ANTHROPIC_API_KEY'}")
    print(f"   Apify:           {'OK' if APIFY_TOKEN else 'MISSING APIFY_TOKEN (Apify features disabled)'}")
    print(f"   Reddit mode:     Public JSON (no API key needed)")
    print(f"   Seed pool:       {sum(len(v) for v in NICHE_SEEDS.values())} seeds across {len(NICHE_SEEDS)} niches")
    print(f"   Subreddit pool:  {sum(len(v) for v in NICHE_SUBREDDIT_POOL.values())} subreddits across {len(NICHE_SUBREDDIT_POOL)} niches")
    print(f"   Opening styles:  {len(OPENING_STYLES)} rotating")
    print(f"   Tone variants:   {len(TONE_DESCRIPTORS)} rotating")
    print(f"\n   Docs:        http://localhost:8000/docs")
    print(f"   Zero-bias:   http://localhost:8000/discover\n")
    print(f"   Health: http://localhost:8000/health\n")

    port = int(os.environ.get("PORT", 8000))
    print(f"   Port: {port}")
    uvicorn.run(app, host="0.0.0.0", port=port, reload=False)
