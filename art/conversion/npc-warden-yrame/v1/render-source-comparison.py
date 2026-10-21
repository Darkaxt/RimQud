"""Show original Yrame beside separate anatomy and the exact four-item outfit."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
p=json.loads((ROOT/'art/conversion/body-yrame/v1/source-packet.json').read_text());palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];rgb=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
a=np.array(Image.open(p['original']['private_mask']['path']).convert('RGBA'));w=a[:,:,:1].astype(float)/255;original=Image.fromarray(np.dstack([np.uint8(np.round((1-w)*rgb('w')+w*rgb('B'))),a[:,:,3]]))
out=Image.new('RGB',(1400,920),'#142823');d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.text((18,15),'YRAME515 > source-bound separate legs > actual four-item outfit',font=font,fill='#e3cf43')
for im,x,y,size in [(original,40,120,(160,240)),(Image.open(HERE/'base-south.png').convert('RGBA'),330,55,(240,540)),(Image.open(HERE/'full-neutral-south.png').convert('RGBA'),690,55,(240,540)),(Image.open(HERE/'full-native-south.png').convert('RGBA'),1050,55,(240,540))]:
    im=im.resize(size,Image.Resampling.NEAREST if im is original else Image.Resampling.LANCZOS);out.paste(im,(x,y),im)
for x,label in [(25,'ORIGINAL QUD w/B'),(310,'BODY + SEPARATE LEGS'),(670,'NEUTRAL FOUR-ITEM OUTFIT'),(1030,'ACTUAL SOURCE PALETTES')]:d.text((x,630),label,font=font,fill='#e3cf43')
lines=['Mail574 Body287; Horns575 Head288; Blade576 Hand292/2; Boots580 Feet297/16. No invented extra equipment.',
       'Added Feet298/64 is UNEQUIPPED. Never duplicate Boots580 onto the added pair merely to fill the silhouette.',
       'High-forehead horns keep near/far depth; north roots stay behind the head rather than moving to the temples.',
       'Body/mail/blade/boots: exact RGBA y+128; horns already use this1152px frame. Physical scale/contact unchanged.',
       'Source w body and each item palette remain independent. B metadata retained; no guessed rime skin region.',
       'Default Icy Vapor is native natural equipment/effect metadata. Stationary blade display, no native acceptance.']
for i,line in enumerate(lines):d.text((18,700+i*30),line,font=font,fill='#e5e8d8')
out.save(HERE/'source-to-assembly.png')
print('Rendered original, separate anatomy and actual neutral/native outfit.')
