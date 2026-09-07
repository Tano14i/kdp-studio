#!/usr/bin/env python3
"""KDP paperback wraparound TEMPLATE at exact measures (74 pages, white paper).
Generated artifact. The front/back 4K art drops into the marked panels; every
measure here is computed, never eyeballed. Cloudfront art was unreachable in the
build session, so this emits the measured guide, not the final composite."""
from PIL import Image, ImageDraw, ImageFont

DPI=300
def inch(x): return round(x*DPI)
PAGES=74; PAPER=0.002252  # white
SPINE=PAGES*PAPER          # 0.1666"
TRIM_W, TRIM_H = 6.0, 9.0
BLEED=0.125
SAFE=0.25
FULL_W=2*TRIM_W+SPINE+2*BLEED
FULL_H=TRIM_H+2*BLEED

W,H=inch(FULL_W),inch(FULL_H)
img=Image.new("RGB",(W,H),"#e9e9e9")
d=ImageDraw.Draw(img)
try:
    f=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",34)
    fb=ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",44)
except: f=fb=ImageFont.load_default()

bleed=inch(BLEED); trimw=inch(TRIM_W); spine=inch(SPINE); safe=inch(SAFE)
# x boundaries
back_x0=bleed; back_x1=back_x0+trimw
spine_x0=back_x1; spine_x1=spine_x0+spine
front_x0=spine_x1; front_x1=front_x0+trimw
top=bleed; bot=bleed+inch(TRIM_H)

def panel(x0,x1,color,label):
    d.rectangle([x0,top,x1,bot],fill=color)
    # safe area
    d.rectangle([x0+safe,top+safe,x1-safe,bot-safe],outline="#d33",width=3)
    d.text((x0+safe+12,top+safe+12),label,font=fb,fill="#ffffff")

panel(back_x0,back_x1,"#1b2233","BACK COVER\n(drop back-4k.png here)")
panel(front_x0,front_x1,"#241a2e","FRONT COVER\n(drop front-4k.png here)")
# spine
d.rectangle([spine_x0,top,spine_x1,bot],fill="#0e0e14")
d.text((spine_x0+4,(top+bot)//2),"SPINE %.4f in\nNO TEXT (<100 pp)"%SPINE,font=f,fill="#cccccc")
# barcode keep-out: lower-right of BACK panel (near spine), 2 x 1.2 in
bw,bh=inch(2.0),inch(1.2)
bx1=back_x1-safe; bx0=bx1-bw; by1=bot-safe; by0=by1-bh
d.rectangle([bx0,by0,bx1,by1],fill="#ffffff",outline="#333",width=3)
d.text((bx0+14,by0+14),"BARCODE\nKEEP EMPTY\n2.0 x 1.2 in",font=f,fill="#333")
# outer bleed frame
d.rectangle([0,0,W-1,H-1],outline="#999",width=2)
d.rectangle([bleed,bleed,W-bleed,H-bleed],outline="#3a3",width=2)  # trim line

out="02 Validazione/copertina-bozze/wraparound-template.png"
img.save(out,dpi=(DPI,DPI))
print("full cover: %.4f x %.4f in = %d x %d px @%ddpi"%(FULL_W,FULL_H,W,H,DPI))
print("spine: %.4f in (%d px)"%(SPINE,spine))
print("saved:",out)
