"""Show Nima's original sprite, separate anatomy and actual five-item assembly."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
packet=json.loads((ROOT/'art/conversion/body-nima/v1/source-packet.json').read_text())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
rgb=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
a=np.array(Image.open(packet['original']['private_mask']['path']).convert('RGBA'));w=a[:,:,:1].astype(float)/255
original=Image.fromarray(np.dstack([np.uint8(np.round((1-w)*rgb('g')+w*rgb('w'))),a[:,:,3]]))
out=Image.new('RGB',(1400,950),'#142823');d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.text((18,15),'NIMA506 > source-bound separate anatomy > actual five-item outfit',font=font,fill='#e3cf43')
for im,x,y,size in [(original,40,120,(160,240)),(Image.open(HERE/'base-south.png').convert('RGBA'),330,55,(240,593)),(Image.open(HERE/'full-neutral-south.png').convert('RGBA'),690,55,(240,593)),(Image.open(HERE/'full-native-south.png').convert('RGBA'),1050,55,(240,593))]:
    im=im.resize(size,Image.Resampling.NEAREST if im is original else Image.Resampling.LANCZOS);out.paste(im,(x,y),im)
for x,label in [(25,'ORIGINAL QUD g/w'),(310,'BODY + SEPARATE MUTATIONS'),(670,'NEUTRAL FIVE-ITEM OUTFIT'),(1030,'ACTUAL SOURCE PALETTES')]:d.text((x,680),label,font=font,fill='#e3cf43')
lines=['Actor506 / shared female base, separate additional arms and one segmented spiral Tail193.',
       'Apron529 Body176; Hat530 Head177; Pestle531 Hand181/6; Sandals536 Feet192; Glowsphere538 FloatingNearby195.',
       'Current body and all item pixels unchanged; transparent top padding preserves physical scale and contact.',
       'Ordinary body/additional arms retain source g; tail uses source detail w. West tail is explicitly projected.',
       'Pestle hand identity and floating slot remain distinct. Optional halo and native light/colour cycle are unbound.',
       'Static authoring only. Cosmetic jade eyes/scars remain postponed; native equipment/pose/hurt/look/save pending.']
for i,line in enumerate(lines):d.text((18,735+i*30),line,font=font,fill='#e5e8d8')
out.save(HERE/'source-to-assembly.png')
print('Rendered original source, separate anatomy and neutral/native five-item outfit.')
