"""Remove the manual ink's slight green cast and render current model evidence."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
assert not (HERE/'neutral-ink-correction.json').exists()
model=json.loads((OUT/'model.json').read_text());changed=[]
for f,rows in model['views'].items():
    for r in rows:
        if not r['component'].startswith('mutation-'):continue
        p=ROOT/r['public_file'];a=np.array(Image.open(p).convert('RGBA'));gray=np.uint8(np.round(a[:,:,:3].astype(float).mean(2)))
        if not np.array_equal(a[:,:,0],a[:,:,1]) or not np.array_equal(a[:,:,1],a[:,:,2]):
            before=r['sha256'];a[:,:,:3]=gray[:,:,None];a[a[:,:,3]==0,:3]=0;Image.fromarray(a).save(p);r['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();changed.append(dict(path=r['public_file'],before_sha256=before,after_sha256=r['sha256']))
(OUT/'model.json').write_bytes((json.dumps(model,indent=2)+'\n').encode())
(HERE/'neutral-ink-correction.json').write_bytes((json.dumps(dict(reason='Manual SVG ink #292e2b retains a slight green cast although the surface is gray. Neutral component bases must have equal RGB.',correction='Round mutation-only RGB to its existing mean; keep alpha, geometry and original body/head untouched. Rerender all current-model neutral and source-palette plates.',changed=changed,native_activation=False),indent=2)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];rgb=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
groups={'neutral':{},'native':{}}
for f,rows in model['views'].items():
    n=Image.new('RGBA',(512,1264));c=Image.new('RGBA',(512,1264))
    for r in rows:
        im=Image.open(ROOT/r['public_file']).convert('RGBA');n.alpha_composite(im);a=np.array(im);lum=a[:,:,:3].astype(float).mean(2);w=np.zeros(lum.shape)
        if r.get('detail_weight'):w=np.array(Image.open(ROOT/r['detail_weight']['path'])).astype(float)/255
        color=(1-w[:,:,None])*rgb('r')+w[:,:,None]*rgb('w');a[:,:,:3]=np.uint8(np.round(lum[:,:,None]*color/255));a[a[:,:,3]==0,:3]=0;c.alpha_composite(Image.fromarray(a))
    for key,im in [('neutral',n),('native',c)]:im.save(OUT/f'{key}-{f}.png');groups[key][f]=im
for label,group in groups.items():
    sheet=Image.new('RGB',(1152,800),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'IRUDAD / '+label+' / separate mutation pieces; exact reusable older-human baseline',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(group.items()):
        small=im.resize((256,632),Image.Resampling.LANCZOS);x=16+i*284;sheet.paste(small,(x,50),small);d.line((x+128,50,x+128,682),fill='#a39846');d.line((x,645,x+256,645),fill='#75aaa0');d.text((x,710),f.upper(),font=font,fill='#e3cf43')
    d.text((18,755),'Fixed physical scale and ground; no equipment, cosmetics or native anatomy acceptance.',font=font,fill='#e5e8d8');sheet.save(OUT/f'{label}-comparison.png')
sheet=Image.new('RGB',(800,650),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'IRUDAD / 48x119 whole frame; original body retains same pixel/world scale',font=font,fill='#e3cf43')
for j,group in enumerate(groups.values()):
    y=60+j*270
    for i,(f,im) in enumerate(group.items()):
        small=im.resize((48,119),Image.Resampling.LANCZOS);sheet.paste(small,(i*200+20,y),small);large=small.resize((72,178),Image.Resampling.NEAREST);sheet.paste(large,(i*200+95,y),large);d.text((i*200+20,y+200),f.upper(),font=font,fill='#e3cf43')
d.text((18,620),'Neutral then source r/w. Authoring only; captured outfit remains unfinished.',font=font,fill='#e5e8d8');sheet.save(OUT/'game-scale-comparison.png')
print('Neutralized mutation ink only; current model and all four-facing palette/scale reports regenerated.')
