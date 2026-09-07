#!/usr/bin/env python3
"""Build the 6x9 print interior PDF from the manuscript markdown.
Generated artifact; layout is derived from the manuscript, not hand-authored.
Run: python3 build_interior.py ; prints real page count."""
import re, glob, os, sys
from reportlab.lib.pagesizes import inch
from reportlab.lib.units import inch as IN
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
    Spacer, PageBreak, Preformatted, KeepTogether, FrameBreak)
from reportlab.lib.styles import ParagraphStyle

LS = "/usr/share/fonts/truetype/liberation/"
FD = "/usr/share/fonts/truetype/dejavu/"
pdfmetrics.registerFont(TTFont("Serif", LS+"LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Bold", LS+"LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Serif-Italic", LS+"LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("Serif-BoldItalic", LS+"LiberationSerif-BoldItalic.ttf"))
pdfmetrics.registerFont(TTFont("Mono", FD+"DejaVuSansMono.ttf"))
pdfmetrics.registerFontFamily("Serif", normal="Serif", bold="Serif-Bold",
                              italic="Serif-Italic", boldItalic="Serif-BoldItalic")

BASE = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(BASE, "03 Produzione", "manoscritto")
OUT = os.path.join(BASE, "03 Produzione", "interni")
os.makedirs(OUT, exist_ok=True)
PDF = os.path.join(OUT, "first-time-dungeon-master-interior.pdf")

PW, PH = 6*IN, 9*IN
MARGIN_IN, MARGIN_OUT, MARGIN_TB = 0.7*IN, 0.6*IN, 0.7*IN

body = ParagraphStyle("body", fontName="Serif", fontSize=11.2, leading=16.0,
    alignment=TA_LEFT, spaceAfter=7, firstLineIndent=0)
h_chap = ParagraphStyle("hchap", fontName="Serif-Bold", fontSize=18, leading=22,
    spaceBefore=0, spaceAfter=16)
h_sub = ParagraphStyle("hsub", fontName="Serif-Bold", fontSize=12, leading=15,
    spaceBefore=10, spaceAfter=4)
title_style = ParagraphStyle("title", fontName="Serif-Bold", fontSize=26, leading=30,
    alignment=TA_CENTER, spaceAfter=10)
subtitle_style = ParagraphStyle("subtitle", fontName="Serif-Italic", fontSize=13, leading=17,
    alignment=TA_CENTER, spaceAfter=40)
author_style = ParagraphStyle("author", fontName="Serif", fontSize=13, leading=17,
    alignment=TA_CENTER)
quote = ParagraphStyle("quote", fontName="Serif-Italic", fontSize=9.6, leading=13.6,
    leftIndent=16, rightIndent=10, spaceBefore=6, spaceAfter=8, borderColor="#888888",
    borderWidth=0, textColor="#222222")
MONO_ADV = 0.602  # DejaVuSansMono advance width per em
def mono_style(buf, avail_pt):
    maxw = max((len(l) for l in buf), default=1)
    fit = avail_pt / (maxw * MONO_ADV) if maxw else 7.7
    size = max(6.0, min(7.7, fit))
    return ParagraphStyle("mono", fontName="Mono", fontSize=size, leading=size*1.24,
        leftIndent=2, spaceBefore=6, spaceAfter=8, backColor="#f2f2f2", borderPadding=5)

def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
def inline(s):
    s = esc(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\*\w])\*(?!\s)(.+?)(?<!\s)\*(?![\*\w])", r"<i>\1</i>", s)
    return s
def mono_clean(s):
    return (s.replace("→","->").replace("⃝","[ ]").replace("·","-")
             .replace("’","'").replace("“",'"').replace("”",'"'))

def flow_for(md, is_front):
    out=[]; lines=md.split("\n"); i=0; para=[]
    def flush():
        nonlocal para
        if para:
            out.append(Paragraph(inline(" ".join(para).strip()), body)); para=[]
    while i < len(lines):
        ln=lines[i]
        if ln.startswith("```"):
            flush(); i+=1; buf=[]
            while i<len(lines) and not lines[i].startswith("```"):
                buf.append(mono_clean(lines[i])); i+=1
            i+=1
            avail = (PW-MARGIN_OUT-MARGIN_IN) - 2*5 - 2  # frame - borderPadding - leftIndent
            out.append(KeepTogether(Preformatted("\n".join(buf), mono_style(buf, avail))))
            continue
        s=ln.strip()
        if s=="---": flush(); i+=1; continue
        if s.startswith("# "):
            flush()
            if is_front:
                out.append(Spacer(1,1.4*IN))
                out.append(Paragraph(inline(s[2:]), title_style))
            i+=1; continue
        if s.startswith("### "):
            flush()
            out.append(Paragraph(inline(s[4:]), subtitle_style if is_front else h_sub))
            i+=1; continue
        if s.startswith("## "):
            flush(); out.append(PageBreak())
            if not is_front: out.append(Spacer(1, 0.7*IN))
            out.append(Paragraph(inline(s[3:]), h_chap)); i+=1; continue
        if s.startswith("###"):  # h3 e.g. subtitle line "### A Step..."
            flush(); out.append(Paragraph(inline(s.lstrip("# ")), subtitle_style)); i+=1; continue
        if s.startswith(">"):
            flush(); qbuf=[]
            while i<len(lines) and lines[i].strip().startswith(">"):
                qbuf.append(lines[i].strip()[1:].strip()); i+=1
            out.append(Paragraph(inline(" ".join(qbuf)), quote)); continue
        if s=="":
            flush(); i+=1; continue
        para.append(s); i+=1
    flush()
    return out

part_divider = ParagraphStyle("part", fontName="Serif-Bold", fontSize=22, leading=26,
    alignment=TA_CENTER, spaceBefore=0, spaceAfter=8)
part_sub = ParagraphStyle("partsub", fontName="Serif-Italic", fontSize=12, leading=16,
    alignment=TA_CENTER)
toc_h = ParagraphStyle("toch", fontName="Serif-Bold", fontSize=16, leading=20, spaceAfter=14)
toc_i = ParagraphStyle("toci", fontName="Serif", fontSize=10.6, leading=17)

PARTS = {
 "01": ("Part I", "Run Your First Session"),
 "04": ("Part II", "Handle the Table"),
 "07": ("Part III", "Build the Adventure"),
 "10": ("Part IV", "Keep It Going"),
 "12": ("Extras", "When You're Ready for More"),
 "80": ("Appendices", "Adventures, Monsters, and Tables"),
}

def title_of(f):
    m=re.search(r'^## (?:Chapter \d+: )?(.+)$', open(f).read(), re.M)
    m2=re.search(r'^## (Chapter \d+: .+|Appendix: .+)$', open(f).read(), re.M)
    return (m2.group(1) if m2 else (m.group(1) if m else os.path.basename(f)))

files=sorted(glob.glob(os.path.join(MAN,"*.md")))
chap_files=[f for f in files if not os.path.basename(f).startswith(("00","90"))]

story=[]
# front matter
story += flow_for(open(files[0]).read(), True)
# table of contents
story.append(PageBreak()); story.append(Paragraph("Contents", toc_h))
for f in chap_files:
    key=os.path.basename(f)[:2]
    if key in PARTS:
        p=PARTS[key]
        story.append(Spacer(1,6))
        story.append(Paragraph("<b>%s. %s</b>"%(p[0],esc(p[1])), toc_i))
    story.append(Paragraph(esc(title_of(f)), toc_i))
# body with part dividers
for f in chap_files:
    key=os.path.basename(f)[:2]
    if key in PARTS:
        p=PARTS[key]
        story.append(PageBreak()); story.append(Spacer(1,2.6*IN))
        story.append(Paragraph(p[0], part_divider))
        story.append(Paragraph(esc(p[1]), part_sub))
    story += flow_for(open(f).read(), False)
# back matter
story += flow_for(open([f for f in files if os.path.basename(f).startswith("90")][0]).read(), False)

class Doc(BaseDocTemplate):
    def __init__(self,*a,**k): super().__init__(*a,**k)
def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 3:  # skip page numbers on the first front-matter pages
        canvas.setFont("Serif", 8.5)
        canvas.drawCentredString(PW/2, 0.38*IN, str(doc.page))
    canvas.restoreState()

frame = Frame(MARGIN_OUT, MARGIN_TB, PW-MARGIN_OUT-MARGIN_IN, PH-2*MARGIN_TB, id="f")
doc = Doc(PDF, pagesize=(PW,PH), leftMargin=MARGIN_OUT, rightMargin=MARGIN_IN,
          topMargin=MARGIN_TB, bottomMargin=MARGIN_TB)
doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=on_page)])
doc.build(story)

# page count
import pymupdf
n=pymupdf.open(PDF).page_count
print("PDF:", PDF)
print("PAGES:", n)
