"""
KDP Studio — Live Trend Backend v2
====================================
Endpoints:
  GET  /health
  GET  /discover        ← ZERO-BIAS: raw global data, no niche pre-selection
  POST /trends          ← niche-guided discovery
  POST /niches
  POST /generate
  POST /generate-all
  POST /package
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
}

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
class TrendRequest(BaseModel):
    platforms: list[str]
    niche: str
    keyword: Optional[str] = ""
    timeframe: Optional[str] = "week"   # day|week|month|3months|year

class NicheRequest(BaseModel):
    platforms: list[str]
    keyword: Optional[str] = ""
    timeframe: Optional[str] = "week"

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

class PackageRequest(BaseModel):
    trend_name: str
    trend_platform: str
    book_title: str
    book_subtitle: str
    book_type: str
    audience: str
    tone: Optional[str] = ""
    reader_persona: Optional[str] = ""

# ══════════════════════════════════════════════════════════════
# REDDIT HELPER
# ══════════════════════════════════════════════════════════════
async def fetch_reddit_posts(niche: str, keyword: str = "", timeframe: str = "week") -> list[dict]:
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
def call_claude(prompt: str, max_tokens: int = 4000) -> str:
    msg = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}]
    )
    if msg.stop_reason == "max_tokens":
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
    except json.JSONDecodeError:
        j = re.sub(r',\s*([\]}])', r'\1', j)
        j = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', j)
        return json.loads(j)

def build_voice_ctx(tone="", language="English", cultural_inspiration="",
                    chapter_length="medium", reader_persona="") -> str:
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
    lines.append(f"- Uniqueness seed: {now_stamp()} — use this to make this version distinct from any previous generation")
    lines.append(f"- IMPORTANT: Do NOT use generic self-help clichés. Make every sentence specific and surprising.")
    return "\n".join(lines)

# ══════════════════════════════════════════════════════════════
# ROUTES
# ══════════════════════════════════════════════════════════════
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
    return {
        "status": "ok",
        "reddit": reddit_ok,
        "reddit_mode": "public_json",
        "claude": bool(ANTHROPIC_KEY),
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


@app.get("/discover")
async def discover_unbiased():
    """
    Zero-bias discovery: fetch raw global signals from Reddit + Google Trends,
    then let Claude identify KDP opportunities — no niche pre-selection.
    """
    stamp = now_stamp()

    # Run all fetches in parallel
    reddit_posts, gtrends = await asyncio.gather(
        fetch_reddit_global(),
        fetch_google_trending_now()
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

    prompt = f"""You are a KDP publishing expert with zero preconceptions about what niche to target.

CURRENT MOMENT: {stamp}

You are about to read RAW, UNFILTERED social data — no topic was specified, no niche was chosen.
Your job: find what is organically emerging and identify KDP book opportunities from it.

RAW DATA:
{reddit_block}
{gtrends_block}

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

Return ONLY raw JSON, no markdown, ASCII-safe strings only:
{{"opportunities":[
{{
  "niche": "The organic niche you discovered (do not use predefined categories)",
  "pattern": "The specific pattern you noticed across multiple data points",
  "data_signals": ["exact Reddit post title or Google query 1", "signal 2", "signal 3"],
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
        result["meta"] = {
            "mode": "zero_bias_discovery",
            "reddit_posts_analyzed": len(reddit_posts),
            "reddit_subreddits": list(set(p["subreddit"] for p in reddit_posts))[:10],
            "google_daily_trending": gtrends.get("daily_trending", [])[:10],
            "google_realtime": gtrends.get("realtime", [])[:5],
            "fetched_at": stamp,
            "note": "No niche was specified — opportunities discovered purely from raw data"
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/trends")
async def get_trends(req: TrendRequest):
    year = datetime.now().year
    stamp = now_stamp()
    platforms_str = ", ".join(req.platforms)

    tf_info = get_timeframe(req.timeframe or "week")
    reddit_posts, gtrends = await asyncio.gather(
        fetch_reddit_posts(req.niche, req.keyword or "", req.timeframe or "week"),
        fetch_google_trends(req.niche, req.keyword or "", req.timeframe or "week")
    )

    reddit_summary = ""
    if reddit_posts:
        reddit_summary = f"REDDIT — Top viral posts this week (from: {', '.join(set(p['subreddit'] for p in reddit_posts[:10]))}):\n"
        for i, p in enumerate(reddit_posts[:15], 1):
            reddit_summary += f"{i}. [r/{p['subreddit']}] \"{p['title']}\" — {p['score']} upvotes\n"
    else:
        reddit_summary = "Reddit data unavailable this run.\n"

    gtrends_summary = ""
    if gtrends.get("avg_interest"):
        gtrends_summary = f"GOOGLE TRENDS — 7-day avg (seeds rotated each run):\n"
        for term, val in gtrends["avg_interest"].items():
            gtrends_summary += f"  '{term}': {val}/100\n"
        if gtrends.get("rising_queries"):
            gtrends_summary += "Rising breakout queries:\n"
            for term, queries in gtrends["rising_queries"].items():
                if queries:
                    tops = [q.get("query","") for q in queries[:3]]
                    gtrends_summary += f"  Under '{term}': {', '.join(tops)}\n"

    prompt = f"""You are a KDP publishing expert analyzing REAL social media data.

CURRENT MOMENT: {stamp}
ANALYSIS WINDOW: {tf_info["label"]} ({tf_info["gtrends"]})
STRATEGIC CONTEXT: {tf_info["strategy"]}

This is a UNIQUE run — identify trends emerging within the specified time window.
Match your recommendations to the window: short windows = act fast, long windows = find gaps.

REAL DATA COLLECTED RIGHT NOW:
{reddit_summary}
{gtrends_summary}

TASK: Identify 4 SPECIFIC, UNDERSERVED KDP book opportunities for the "{req.niche}" category.
Platforms context: {platforms_str}
{f'Keyword focus: "{req.keyword}"' if req.keyword else ''}

UNIQUENESS RULES:
- Do NOT suggest: generic journals, gratitude journals, mindfulness basics, morning routines
- Each trend must be backed by a SPECIFIC signal from the data above
- Find angles that feel fresh and slightly unexpected
- Think: what is JUST starting to emerge, not what has already peaked?

Return ONLY raw JSON, no markdown, ASCII-safe strings only:
{{"trends":[
{{"name":"SPECIFIC TREND","platform":"PLATFORM","description":"2 sentences with specific data reference","heat":4,"data_signal":"Quote the exact Reddit post title or Google Trends query that supports this","books":[
{{"type":"TYPE","title":"TITLE","subtitle":"SEO subtitle"}},
{{"type":"TYPE","title":"TITLE 2","subtitle":"SEO subtitle 2"}}
]}},
{{"name":"TREND 2","platform":"PLATFORM","description":"2 sentences","heat":5,"data_signal":"specific signal","books":[
{{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
{{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
]}},
{{"name":"TREND 3","platform":"PLATFORM","description":"2 sentences","heat":3,"data_signal":"signal","books":[
{{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
{{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
]}},
{{"name":"TREND 4","platform":"PLATFORM","description":"2 sentences","heat":4,"data_signal":"signal","books":[
{{"type":"TYPE","title":"TITLE","subtitle":"subtitle"}},
{{"type":"TYPE","title":"TITLE 2","subtitle":"subtitle 2"}}
]}}
]}}"""

    try:
        text = call_claude(prompt, 3000)
        result = parse_json_safe(text)
        result["meta"] = {
            "reddit_posts_found": len(reddit_posts),
            "gtrends_seeds_used": gtrends.get("terms", []),
            "gtrends_avg": gtrends.get("avg_interest", {}),
            "subreddits_used": list(set(p["subreddit"] for p in reddit_posts[:10])) if reddit_posts else [],
            "fetched_at": stamp,
            "timeframe": req.timeframe or "week",
            "timeframe_label": tf_info["label"],
            "timeframe_strategy": tf_info["strategy"],
            "data_sources": {
                "reddit": len(reddit_posts) > 0,
                "google_trends": bool(gtrends.get("avg_interest"))
            }
        }
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
    voice_ctx = build_voice_ctx(
        tone=req.tone,
        language=req.language or "English",
        cultural_inspiration=req.cultural_inspiration or "",
        chapter_length=req.chapter_length or "medium",
        reader_persona=req.reader_persona or ""
    )
    length_map = {"short": "800-1000", "medium": "1200-1600", "long": "2000-2500"}
    word_count = length_map.get(req.chapter_length or "medium", "1200-1600")

    if req.tab == "outline":
        prompt = f"""You are a bestselling KDP author. Create a detailed book outline.

{book_ctx}

{voice_ctx}

Write a professional outline with 10 chapters. For each chapter:
- Chapter number and punchy title
- 4 subsection titles (titles only, no descriptions)

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

{voice_ctx}

Write CHAPTER {n} completely:
- Chapter title as header
- Follow the opening style specified above EXACTLY
- 3-4 full sections with subheadings, content, prompts or exercises for {req.book_type}
- Chapter summary or key takeaways
- Target: {word_count} words

Follow the voice guidelines precisely. Make it feel like no other chapter in any other book."""
        max_tok = 4000

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
        text = call_claude(prompt, max_tok)
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
                reader_persona=req.reader_persona or ""
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
                text = call_claude(prompt, 4000)
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


@app.post("/package")
async def generate_package(req: PackageRequest):
    tone_note = f"Tone/voice of the book: {req.tone}" if req.tone else ""
    persona_note = f"Target reader persona: {req.reader_persona}" if req.reader_persona else ""
    stamp = now_stamp()

    prompt = f"""You are an Amazon KDP publishing expert. Generate a complete KDP listing package.

Book: "{req.book_title}" — {req.book_subtitle}
Type: {req.book_type}
Trend: "{req.trend_name}"
Audience: {req.audience}
Platform: {req.trend_platform}
{tone_note}
{persona_note}
Generated: {stamp}

Return ONLY raw JSON. No markdown. ASCII-safe strings only.

{{"kdp":{{"title":"optimized Amazon title max 200 chars","subtitle":"SEO subtitle max 200 chars","pen_name":"believable author name fitting this niche and tone","pen_name_rationale":"1 sentence why this name works","description":"Full Amazon description 400-600 words. Use <b> for headers, <br> for breaks. Hook, benefits, who it is for.","short_description":"80-word mobile preview","keywords":["kw1","kw2","kw3","kw4","kw5","kw6","kw7"],"categories":["Primary Amazon category","Secondary Amazon category"],"bisac":["BISAC 1","BISAC 2"],"price_ebook":4.99,"price_paperback":12.99,"page_count_estimate":120,"trim_size":"6x9","tagline":"Punchy tagline under 15 words","canva_cover":{{"main_prompt":"60-80 word Canva AI image prompt for cover background. Mood colors lighting style. No text in scene.","style":"one-word style","color_palette":["#hex1","#hex2","#hex3"],"color_palette_names":["name1","name2","name3"],"font_title":"Canva font for title","font_subtitle":"Canva font for subtitle and author","layout_tip":"One sentence on placement","variation_1":"Alternative 40-word prompt","variation_2":"Alternative 40-word prompt","canva_steps":"4-5 step instructions for KDP-ready cover in Canva"}}}}}}"""

    try:
        text = call_claude(prompt, 4000)
        return parse_json_safe(text)
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
    print(f"   Reddit mode:     Public JSON (no API key needed)")
    print(f"   Seed pool:       {sum(len(v) for v in NICHE_SEEDS.values())} seeds across {len(NICHE_SEEDS)} niches")
    print(f"   Subreddit pool:  {sum(len(v) for v in NICHE_SUBREDDIT_POOL.values())} subreddits across {len(NICHE_SUBREDDIT_POOL)} niches")
    print(f"   Opening styles:  {len(OPENING_STYLES)} rotating")
    print(f"   Tone variants:   {len(TONE_DESCRIPTORS)} rotating")
    print(f"\n   Docs:        http://localhost:8000/docs")
    print(f"   Zero-bias:   http://localhost:8000/discover\n")
    print(f"   Health: http://localhost:8000/health\n")

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False)
