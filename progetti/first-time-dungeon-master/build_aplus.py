#!/usr/bin/env python3
"""Build KDP A+ content modules at exact sizes, using REAL product pages.
Generated artifact. Images come from the interior PDF, never mockups."""
from PIL import Image, ImageDraw, ImageFont
import os
OUT="04 Mercato/contenuti-a-plus"; os.makedirs(OUT,exist_ok=True)
FD="/usr/share/fonts/truetype/dejavu/"; LS="/usr/share/fonts/truetype/liberation/"
def font(path,sz): return ImageFont.truetype(path,sz)
SB=lambda s: font(LS+"LiberationSerif-Bold.ttf",s)
SR=lambda s: font(LS+"LiberationSerif-Regular.ttf",s)
SS=lambda s: font(FD+"DejaVuSans.ttf",s)
BG="#17141d"; PANEL="#201b13"; GOLD="#d9b25a"; CREAM="#efe6d2"; EMBER="#d98a45"; MUT="#b8ad97"

def grad(w,h,c1=(23,20,29),c2=(35,26,40)):
    im=Image.new("RGB",(w,h),c1); d=ImageDraw.Draw(im)
    for y in range(h):
        t=y/h; d.line([(0,y),(w,y)],fill=tuple(int(c1[i]+(c2[i]-c1[i])*t) for i in range(3)))
    return im

def framed_page(src, box_w, box_h, crop_frac=(0.0,0.06,1.0,0.62)):
    p=Image.open(src).convert("RGB"); W,H=p.size
    l,t,r,b=crop_frac; c=p.crop((int(W*l),int(H*t),int(W*r),int(H*b)))
    # fit into box preserving ratio
    cw,ch=c.size; scale=min(box_w/cw, box_h/ch); nw,nh=int(cw*scale),int(ch*scale)
    c=c.resize((nw,nh)); canvas=Image.new("RGB",(box_w,box_h),"#ffffff")
    canvas.paste(c,((box_w-nw)//2,(box_h-nh)//2)); return canvas

def wrap(d,txt,fnt,maxw):
    words=txt.split(); lines=[]; cur=""
    for w in words:
        t=(cur+" "+w).strip()
        if d.textlength(t,font=fnt)<=maxw: cur=t
        else: lines.append(cur); cur=w
    if cur: lines.append(cur);
    return lines

# ---------- 1. HEADER 970x600 ----------
im=grad(970,600); d=ImageDraw.Draw(im)
d.text((60,90),"FIRST-TIME",font=SB(50),fill=CREAM)
d.text((60,150),"DUNGEON MASTER",font=SB(50),fill=GOLD)
d.text((62,240),"Run your first game",font=SR(32),fill=MUT)
d.text((62,278),"with confidence.",font=SR(32),fill=MUT)
for i,t in enumerate(["Fast prep","Better encounters","Confident improvisation"]):
    d.text((64,350+i*44),"♦  "+t,font=SS(24),fill=CREAM)
th=framed_page("/tmp/apx/worksheet.png",300,440)
im.paste(Image.new("RGB",(310,450),"#c9a24a"),(600,80))  # gold frame
im.paste(th,(605,85))
im.save(f"{OUT}/01-header-970x600.png"); print("header")

# ---------- 2. TEXT BAND 970x300 ----------
im=grad(970,300,(32,27,19),(23,20,29)); d=ImageDraw.Draw(im)
d.text((60,50),"Prep a whole session in under an hour.",font=SB(42),fill=GOLD)
pts=["A timed, repeatable six-step system — no more Wednesday-night dread.",
     "Roll-and-go tables when your players go off-script (and they will).",
     "Fillable templates and checklists you can use at the table tonight."]
for i,t in enumerate(pts):
    d.text((60,130+i*46),"•",font=SS(28),fill=EMBER)
    d.text((90,130+i*46),t,font=SR(28),fill=CREAM)
im.save(f"{OUT}/02-textband-970x300.png"); print("textband")

# ---------- 3. THREE 300x300 (real pages) ----------
caps=[("worksheet","The 1-Hour Prep Worksheet"),
      ("improv","Roll-and-go improv tables"),
      ("bestiary","A starter bestiary, ready to drop in")]
for key,cap in caps:
    im=Image.new("RGB",(300,300),PANEL); d=ImageDraw.Draw(im)
    pg=framed_page(f"/tmp/apx/{key}.png",280,232, (0.0,0.06,1.0,0.5))
    im.paste(pg,(10,10))
    d.rectangle([0,252,300,300],fill="#14110b")
    for j,ln in enumerate(wrap(d,cap,SR(22),280)[:2]):
        d.text((14,258+j*22),ln,font=SR(22),fill=GOLD)
    im.save(f"{OUT}/03-{key}-300.png"); print("300",key)

# ---------- 4. FOUR 220x220 pillars ----------
pillars=[("Fast Prep","under an hour"),("Rulings on the Fly","no rule left you stuck"),
         ("Confident Improv","tables for the unplanned"),("Fair Encounters","no accidental wipes")]
for i,(t,s) in enumerate(pillars):
    im=grad(220,220,(32,27,19),(23,20,29)); d=ImageDraw.Draw(im)
    d.ellipse([80,26,140,86],outline=GOLD,width=3); d.text((97,42),"d20",font=SS(20),fill=GOLD)
    for j,ln in enumerate(wrap(d,t,SB(24),196)):
        d.text((16,108+j*28),ln,font=SB(24),fill=CREAM)
    d.text((16,180),s,font=SR(20),fill=MUT)
    im.save(f"{OUT}/04-pillar{i+1}-220.png"); print("pillar",i+1)
print("done ->",OUT)
