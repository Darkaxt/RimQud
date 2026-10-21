"""Show original source beside the unchanged separate anatomy and actual outfit."""
from pathlib import Path
import json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
packet=json.loads((ROOT/'art/conversion/body-irudad/v1/source-packet.json').read_text())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];rgb=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
a=np.array(Image.open(packet['original']['private_mask']['path']).convert('RGBA'));w=a[:,:,:1].astype(float)/255
original=Image.fromarray(np.dstack([np.uint8(np.round((1-w)*rgb('r')+w*rgb('w'))),a[:,:,3]]))
out=Image.new('RGB',(1400,950),'#142823');d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.text((18,15),'IRUDAD507 > source-bound separate older-human anatomy > actual four-item outfit',font=font,fill='#e3cf43')
for im,x,y,size in [(original,40,120,(160,240)),(Image.open(HERE/'base-south.png').convert('RGBA'),330,55,(240,593)),(Image.open(HERE/'full-neutral-south.png').convert('RGBA'),690,55,(240,593)),(Image.open(HERE/'full-native-south.png').convert('RGBA'),1050,55,(240,593))]:
    im=im.resize(size,Image.Resampling.NEAREST if im is original else Image.Resampling.LANCZOS);out.paste(im,(x,y),im)
for x,label in [(25,'ORIGINAL QUD r/w'),(310,'BODY + SEPARATE MUTATIONS'),(670,'NEUTRAL FOUR-ITEM OUTFIT'),(1030,'ACTUAL SOURCE PALETTES')]:d.text((x,680),label,font=font,fill='#e3cf43')
lines=['Exact actor507 / ordinary older-human base plus separate raised arms, Hands-Face211 and posterior Tail214.',
       'Black Robes539 Body196; Spectacles540 Face198; Walking Stick541 Hand201/6; Sandals546 Feet213.',
       'Current body and all original item pixels unchanged; transparent top padding keeps physical scale/contact fixed.',
       'Hand201/6 is retained verbatim. Static palm placement is an authored association, not a mechanical bone inference.',
       'Full robe and tail are retained; actual occlusion may hide the tail root. Per-item masks never redraw the entire body.',
       'No new ImageGen call or baked outfit. Native anatomy/visibility/equipment/pose/hurt/look/save acceptance pending.']
for i,line in enumerate(lines):d.text((18,735+i*30),line,font=font,fill='#e5e8d8')
out.save(HERE/'source-to-assembly.png');print('Rendered original source, separate body and actual neutral/native outfit.')
