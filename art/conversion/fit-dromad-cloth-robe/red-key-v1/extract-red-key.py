"""Extract from this one generated output; no generative isolation or local fit."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import hashlib,json

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad/v2'
assert not (HERE/'key-extraction.json').exists(), 'Preserve recorded outputs'
def asset(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
raw=Image.open(HERE/'dressed-red-output.png').convert('RGBA')
cloth=raw.copy();removed=Image.new('L',raw.size);keyed=Image.new('RGBA',raw.size)
cp=cloth.load();rp=raw.load();mp=removed.load();kp=keyed.load()
removed_count=0;neutral_count=0
for y in range(raw.height):
    for x in range(raw.width):
        r,g,b,a=rp[x,y];other=max(g,b)
        red=(r-other>=4 and r>=1.6*other)
        if red:
            mp[x,y]=a;kp[x,y]=(r,g,b,a);cp[x,y]=(0,0,0,0)
            if a>=16:removed_count+=1
        elif a<16:
            cp[x,y]=(0,0,0,0)
        else:neutral_count+=1
cloth.save(HERE/'extracted-visible-clothing-sheet.png')
removed.save(HERE/'keyed-body-mask.png')
keyed.save(HERE/'keyed-body-only.png')
original=Image.new('RGBA',raw.size)
for i,f in enumerate(['south','east','north']):original.paste(Image.open(BODY/f'selected-{f}.png'),(512*i,0))
direct=Image.alpha_composite(original,cloth);direct.save(HERE/'direct-original-body-recomposition.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
plate=Image.new('RGB',(1536,1180),'#142823');d=ImageDraw.Draw(plate)
for row,(label,im) in enumerate([('ONE GENERATED DRESSED OUTPUT / no generative isolation',raw),('PROGRAMMATIC RED REMOVAL / visible clothing from those exact pixels',cloth),('DIRECT RECOMPOSITION / unchanged original bodies, no local fitting',direct)]):
    bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
    plate.paste(bg.resize((540,360),Image.Resampling.LANCZOS).convert('RGB'),(20,row*390+30))
    # Profile enlarged using the same cell for all three rows, without recentering.
    cell=bg.crop((512,0,1024,1024));plate.paste(cell.resize((180,360)).convert('RGB'),(600,row*390+30))
    crop=bg.crop((675,600,830,820));plate.paste(crop.resize((310,440)).crop((0,0,310,340)).convert('RGB'),(860,row*390+30))
    d.text((20,row*390+8),label,font=font,fill='#e3cf43')
plate.save(HERE/'red-key-extraction-comparison.png')
evidence={'scope':'One chroma-key extraction experiment; no production selection','raw_output':asset(HERE/'dressed-red-output.png'),'key_rule':'R-max(G,B)>=4 and R>=1.6*max(G,B); remove saturated red including dark red contours. Preserve non-key RGBA; alpha<16 discarded as low-coverage fringe. No geometry scaling/warping.','red_pixels_alpha_ge_16':removed_count,'retained_pixels_alpha_ge_16':neutral_count,'outputs':[asset(HERE/n) for n in ['extracted-visible-clothing-sheet.png','keyed-body-mask.png','keyed-body-only.png','direct-original-body-recomposition.png','red-key-extraction-comparison.png']],'limits':'Chroma-key identifies visible garment/body coverage in the generated frame. It cannot prove unchanged body geometry or recover hidden rear cloth. Original whole garment remains a separate retained source.'}
(HERE/'key-extraction.json').write_bytes((json.dumps(evidence,indent=2)+'\n').encode())
print(json.dumps({'red_removed':removed_count,'clothing_retained':neutral_count,'size':raw.size}))
