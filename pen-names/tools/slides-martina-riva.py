# -*- coding: utf-8 -*-
import os, html, subprocess, sys

OUT = "/tmp/claude-0/-home-user-kdp-studio/81efdd96-f417-5bc8-8fb9-a64e2dea0c8d/scratchpad/build"
os.makedirs(OUT, exist_ok=True)

CREAM_A = "#FAF3E6"
CREAM_B = "#EFE0C6"
GOLD    = "#C9A227"
GOLD_L  = "#E3C46B"
INK     = "#2B2118"
INK_S   = "#5A4A38"

BUTTERFLY = '''
<svg class="bfly" viewBox="0 0 200 190" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="0.8" y2="1">
      <stop offset="0%" stop-color="#EAD08C"/>
      <stop offset="55%" stop-color="#C9A227"/>
      <stop offset="100%" stop-color="#A07C14"/>
    </linearGradient>
    <g id="wings">
      <path d="M100 62 C 126 30, 166 12, 182 32 C 197 51, 172 88, 106 104 Z"/>
      <path d="M104 110 C 146 112, 168 134, 156 156 C 144 177, 116 166, 101 130 Z"/>
    </g>
  </defs>
  <g fill="url(#g)" opacity=".20">
    <use href="#wings"/>
    <use href="#wings" transform="translate(200,0) scale(-1,1)"/>
  </g>
  <g fill="none" stroke="url(#g)" stroke-width="2.3" stroke-linejoin="round">
    <use href="#wings"/>
    <use href="#wings" transform="translate(200,0) scale(-1,1)"/>
  </g>
  <g stroke="url(#g)" fill="none" stroke-linecap="round">
    <path d="M100 58 C 96 90, 96 118, 100 142" stroke-width="5"/>
    <path d="M100 56 C 93 40, 84 30, 73 25" stroke-width="2.2"/>
    <path d="M100 56 C 107 40, 116 30, 127 25" stroke-width="2.2"/>
  </g>
  <g fill="url(#g)"><circle cx="72" cy="24" r="3.6"/><circle cx="128" cy="24" r="3.6"/></g>
</svg>'''

CSS = f"""
@page {{ margin:0 }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:1080px; height:1920px; }}
body {{
  font-family:'Lato', sans-serif;
  color:{INK};
  background:
    radial-gradient(120% 70% at 50% 0%, #FFFBF2 0%, rgba(255,251,242,0) 60%),
    radial-gradient(90% 55% at 15% 100%, rgba(201,162,39,.10) 0%, rgba(201,162,39,0) 70%),
    linear-gradient(168deg, {CREAM_A} 0%, {CREAM_B} 100%);
}}
.slide {{
  width:1080px; height:1920px; position:relative;
  display:flex; flex-direction:column;
  padding:110px 96px 96px;
}}
.frame {{
  position:absolute; inset:44px;
  border:2px solid rgba(43,33,24,.22);
  pointer-events:none;
}}
.frame::after {{
  content:''; position:absolute; inset:14px;
  border:1px solid rgba(201,162,39,.42);
}}
.eyebrow {{
  font-family:'Lato',sans-serif; font-weight:700;
  font-size:26px; letter-spacing:.30em; text-transform:uppercase;
  color:{GOLD}; 
}}
.grow {{ flex:1 1 auto; display:flex; flex-direction:column; justify-content:center; }}
h1 {{ font-family:'Playfair Display',serif; font-weight:700; color:{INK}; }}
.rule {{ display:flex; align-items:center; gap:20px; }}
.rule i {{ display:block; height:1.5px; background:linear-gradient(90deg,{GOLD},rgba(201,162,39,.15)); flex:1; }}
.rule b {{ width:11px; height:11px; background:{GOLD}; transform:rotate(45deg); flex:none; }}
.foot {{
  display:flex; justify-content:space-between; align-items:flex-end;
  font-size:26px; color:{INK_S}; letter-spacing:.04em;
}}
.foot .hand {{ color:{GOLD}; font-weight:700; letter-spacing:.14em; }}
.bfly {{ display:block; }}

/* ---- intro ---- */
.intro {{ text-align:center; }}
.intro .grow {{ align-items:center; }}
.intro .foot, .cta .foot {{ width:100%; }}
.intro .bfly {{ width:272px; margin:0 auto 54px; }}
.intro h1 {{ font-size:132px; line-height:1.03; letter-spacing:-.015em; }}
.intro .sub {{
  font-weight:300; font-size:44px; line-height:1.5; color:{INK_S};
  max-width:760px; margin:52px auto 0;
}}
.intro .rule {{ width:520px; margin:56px auto 0; }}
.swipe {{
  margin-top:64px; font-size:28px; letter-spacing:.26em; text-transform:uppercase;
  color:{GOLD}; font-weight:700;
}}

/* ---- item ---- */
.num {{
  font-family:'Playfair Display',serif; font-weight:700;
  font-size:238px; line-height:.80; color:{GOLD}; opacity:.9;
  letter-spacing:-.03em;
}}
.item h1 {{ font-size:120px; line-height:1.05; margin-top:26px; letter-spacing:-.01em; }}
.item .rule {{ width:280px; margin:44px 0 44px; }}
.item .body {{
  font-weight:300; font-size:54px; line-height:1.52; color:{INK_S}; max-width:870px;
}}

/* ---- quote ---- */
.quote {{ text-align:center; }}
.quote .foot {{ width:100%; }}
.quote .grow {{ align-items:center; }}
.quote .mark {{
  font-family:'Playfair Display',serif; font-weight:700; color:{GOLD};
  font-size:190px; line-height:.55; opacity:.55; margin-bottom:34px;
}}
.quote .q {{
  font-family:'Playfair Display',serif; font-weight:500; color:{INK};
  font-size:82px; line-height:1.26; letter-spacing:-.01em; max-width:880px;
}}
.quote .rule {{ width:400px; margin:64px auto 34px; }}
.quote .by {{
  font-size:28px; letter-spacing:.26em; text-transform:uppercase;
  color:{GOLD}; font-weight:700;
}}

/* ---- cta ---- */
.cta {{ text-align:center; }}
.cta .grow {{ align-items:center; }}
.cta .bfly {{ width:220px; margin:0 auto 48px; }}
.cta h1 {{ font-size:104px; line-height:1.08; }}
.cta .sub {{ font-weight:300; font-size:44px; color:{INK_S}; margin-top:40px; }}
.cta .book {{
  margin-top:74px; padding:44px 56px;
  border:1.5px solid rgba(201,162,39,.55); background:rgba(255,255,255,.42);
}}
.cta .book .t {{ font-family:'Playfair Display',serif; font-size:52px; font-weight:600; line-height:1.2; }}
.cta .book .a {{ margin-top:18px; font-size:30px; letter-spacing:.14em; text-transform:uppercase; color:{GOLD}; font-weight:700; }}
"""

FOOT = ('<div class="foot"><span>Smetti di Chiedere il Permesso</span>'
        '<span class="hand">@martina.rivabooks</span></div>')

def page(cls, inner):
    return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>
<div class="slide {cls}"><div class="frame"></div>{inner}</div>
</body></html>"""

def intro(eyebrow, title_html, sub):
    return page("intro", f"""
<div class="eyebrow">{eyebrow}</div>
<div class="grow">
  {BUTTERFLY}
  <h1>{title_html}</h1>
  <div class="rule"><i></i><b></b><i></i></div>
  <div class="sub">{html.escape(sub)}</div>
  <div class="swipe">scorri &rarr;</div>
</div>
{FOOT}""")

def item(n, name, body, eyebrow):
    return page("item", f"""
<div class="eyebrow">{eyebrow}</div>
<div class="grow">
  <div class="num">{n:02d}</div>
  <h1>{html.escape(name)}</h1>
  <div class="rule"><i></i><b></b></div>
  <div class="body">{html.escape(body)}</div>
</div>
{FOOT}""")

def cta(title, sub, booktitle):
    foot = ('<div class="foot"><span>Martina Riva</span>'
            '<span class="hand">@martina.rivabooks</span></div>')
    return page("cta", f"""
<div class="eyebrow">Martina Riva</div>
<div class="grow">
  {BUTTERFLY}
  <h1>{html.escape(title)}</h1>
  <div class="sub">{html.escape(sub)}</div>
  <div class="book">
    <div class="t">{html.escape(booktitle)}</div>
    <div class="a">Disponibile su Amazon</div>
  </div>
</div>
{foot}""")

# ---------------- content ----------------
EB = "I 5 volti del bisogno di piacere"
TYPES = [
 ("Il Pacificatore", "Spegne ogni conflitto sul nascere. Dice sì per non far arrabbiare nessuno, e si porta a casa la rabbia che ha evitato."),
 ("Il Salvatore",    "Si occupa dei problemi di tutti tranne i suoi. Se non serve a qualcuno, non sa più bene chi è."),
 ("Il Perfezionista","Crede che basti non sbagliare mai per meritarsi affetto. Alza l'asticella, e la colpa resta comunque lì."),
 ("L'Invisibile",    "Non chiede, non disturba, non occupa spazio. Poi si stupisce che nessuno si accorga di cosa gli serve."),
 ("Il Camaleonte",   "Diventa chi ha davanti: cambia tono, opinioni, gusti. A fine giornata non sa più cosa pensa davvero."),
]

pages = []
pages.append(("A1", intro("Martina Riva",
    "I 5 volti<br>del bisogno<br>di piacere",
    "Quasi nessuno riconosce il proprio al primo colpo.")))
for i,(n,b) in enumerate(TYPES, start=1):
    pages.append((f"A{i+1}", item(i, n, b, EB)))
pages.append(("A7", cta("In quale ti sei riconosciuto?",
    "Scrivilo nei commenti.", "Smetti di Chiedere il Permesso")))

def quote(text, eyebrow):
    foot = ('<div class="foot"><span>Martina Riva</span>'
            '<span class="hand">@martina.rivabooks</span></div>')
    return page("quote", f"""
<div class="eyebrow">{html.escape(eyebrow)}</div>
<div class="grow">
  <div class="mark">&ldquo;</div>
  <div class="q">{html.escape(text)}</div>
  <div class="rule"><i></i><b></b><i></i></div>
  <div class="by">Smetti di Chiedere il Permesso</div>
</div>
{foot}""")

QUOTES = [
 "Sai cosa vorresti dire. E poi dici sì.",
 "Il senso di colpa arriva sempre prima della parola.",
 "Non sei debole. Sei dentro un meccanismo che il tuo cervello ha costruito per proteggerti.",
 "Il senso di colpa non è la tua coscienza. È il guardiano della gabbia.",
 "Puoi dire no senza spiegazioni, senza scuse, senza premesse.",
 "Il permesso che hai sempre cercato fuori è sempre stato dentro di te.",
]
for i,q in enumerate(QUOTES, start=1):
    pages.append((f"B{i}", quote(q, "Martina Riva")))
pages.append(("B7", cta("Ti sei riconosciuto?",
    "Il libro è su Amazon.", "Smetti di Chiedere il Permesso")))

for name, doc in pages:
    open(os.path.join(OUT, name + ".html"), "w").write(doc)
print("written", len(pages))
