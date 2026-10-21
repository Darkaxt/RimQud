"""Authoring-only all-state, intended-size and multicell proofs before registration."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=np.array(list(bytes.fromhex(pal['w'])));dt=np.array(list(bytes.fromhex(pal['r'])));idx=json.loads((OLD/'native-state-index.json').read_text());source={};target={};font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for st in idx['originals']:
 mask=st['mask'];a=np.array(Image.open(st['private_mask']['path']).convert('RGBA'));w=a[:,:,:1]/255;source[mask]=Image.fromarray(np.dstack([np.uint8(np.round((1-w)*fg+w*dt)),a[:,:,3]]))
 a=np.array(Image.open(HERE/f'{mask:02d}-map-neutral.png').convert('RGBA'));da=np.array(Image.open(HERE/f'{mask:02d}-map-detail.png').convert('RGBA'))[:,:,3];w=np.divide(da.astype(float),a[:,:,3],out=np.zeros_like(da,dtype=float),where=a[:,:,3]>0);w=np.minimum(w,1)[:,:,None];rgb=np.uint8(np.round(a[:,:,:3]*((1-w)*fg+w*dt)/255));target[mask]=Image.fromarray(np.dstack([rgb,a[:,:,3]]))
def stamp(plate,im,xy,size,nearest=False):
 bg=Image.new('RGBA',size,'#20382d');bg.alpha_composite(im.resize(size,Image.Resampling.NEAREST if nearest else Image.Resampling.LANCZOS));plate.paste(bg.convert('RGB'),xy)
plate=Image.new('RGB',(1440,1120),'#142823');d=ImageDraw.Draw(plate)
for mask in range(16):
 x=mask%4*360;y=mask//4*280;d.text((x+10,y+7),f'{mask:02d}: source / Blender',font=font,fill='#e3cf43');stamp(plate,source[mask],(x+25,y+35),(120,180),True);stamp(plate,target[mask],(x+180,y+35),(120,180))
 stamp(plate,target[mask],(x+130,y+228),(16,24));stamp(plate,target[mask],(x+190,y+223),(24,36));stamp(plate,target[mask],(x+250,y+218),(32,48))
plate.save(HERE/'all-state-source-comparison.png')
cells={(x,y) for y in range(1,6) for x in range(1,6) if x in [1,5] or y in [1,5] or x==3 or y==3};mapping={}
for x,y in cells:mapping[(x,y)]=sum(b for b,dx,dy in [(1,0,-1),(2,1,0),(4,0,1),(8,-1,0)] if (x+dx,y+dy) in cells)
plate=Image.new('RGB',(1440,850),'#142823');d=ImageDraw.Draw(plate)
for col,(title,images) in enumerate([('ACTUAL NATIVE MASKS',source),('BLENDER SHARED FRAME',target)]):
 d.text((20+col*720,15),title,font=font,fill='#e3cf43')
 for (x,y),mask in mapping.items():stamp(plate,images[mask],(20+col*720+x*92,50+y*92),(92,92),col==0)
 d.text((20+col*720,735),'Corners / T junctions / crossing / straight joins',font=font,fill='#e5e8d8')
d.text((20,790),'Same native 7x7 cell layout. No new gate/door connection flags, no game capture.',font=font,fill='#e5e8d8');plate.save(HERE/'joined-corners-comparison.png')
plate=Image.new('RGB',(1340,650),'#142823');d=ImageDraw.Draw(plate)
d.text((20,20),'ATTACHMENT CONTRACT / native paint group remains authoritative',font=font,fill='#e3cf43')
for x in range(3):
 stamp(plate,target[[2,10,8][x]],(30+x*150,100),(150,225));d.text((45+x*150,340),['end E','straight EW','end W'][x],font=font,fill='#e5e8d8')
for x,y in [(105,250),(255,250),(405,250)]:d.ellipse((x-3,y-3,x+3,y+3),fill='#e3cf43')
for y,line in enumerate(['Gold points: unchanged shared picket/ground anchors.', 'Cardinal attachment empties saved at half-cell boundaries.', 'Canvas self-neighbors select all16 native masks.', 'Brinestalk Gate is the native UsesGate placement choice.', 'Gate PaintWith=brinestalkfence; Canvas has no group.', 'Do not invent a Canvas-to-gate neighbor flag.', 'SingleTrack PaintWith=* can connect by native code.', 'MultiTrack wildcard requires a nonempty source group.', 'Other furniture/doors: only source-supported matches.', 'Native gate art and state mechanics remain unchanged.']):d.text((525,105+y*34),line,font=font,fill='#e5e8d8')
d.text((20,565),'Joined crops extend without exposed endcaps. This diagram documents fit interfaces; it is not a converted gate.',font=font,fill='#e5e8d8');plate.save(HERE/'attachment-contract-comparison.png')
inputs=[ref(OLD/'native-states-comparison.png'),ref(OLD/'manual-3d.png'),ref(OLD/'03-manual-map.png'),ref(HERE/'all-state-source-comparison.png'),ref(HERE/'joined-corners-comparison.png'),ref(HERE/'attachment-contract-comparison.png'),ref(HERE/'03-refined-3d.png'),ref(HERE/'15-refined-3d.png')]+[ref(HERE/f'{i:02d}-map-neutral.png') for i in range(16)]
write('review-inputs.json',dict(entry='SCN-CANVASWALL',inputs=inputs,source='Native hanging square duck-weave flax canvas on thin pickets; all16 N1/E2/S4/W8 states. One central tan-primary picket with red cap; E/W broad tan fabric, red top hem and lower outer red fold; N/S narrow red edge-on strip with tan ties. Native w/r tint. Full16x24 common cell becomes256square. Connected edges intentionally touch/cross frame; other edges must remain clear.',authored='Complete 3D cloth/pickets, hidden thickness and45degree cardinal map camera are authored estimates. No roof tent, masonry, decorative swag, arbitrary new gate join or native behavior.',required='Review all16 states versus source and fixed manual geometry. Check self-joins and corners/T/cross in joined proof, continuity, duplicate caps/borders, contact, clipping, source palette/material roles and intended16x24/24x36 size. Named gate has different paint group; attachment diagram documents limitations and anchors only.',expected_output='Compact findings with state/region/evidence/confidence/severity and correction principle; recommendation pass or hold. Do not edit/regenerate/delegate. No native acceptance claim.'))
print('All16/source, joined corners and attachment boundary proofs prepared for fresh independent review.')
