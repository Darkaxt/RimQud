"""Actual six-state cardinal overview and intended-size authoring samples."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];states=['catalogue','tombstone1','tombstone2','tombstone3','tombstone4','resheph'];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1440,1350),'#142823');d=ImageDraw.Draw(plate);paths=[]
for i,st in enumerate(states):
 for j,f in enumerate(['south','east','north']):
  p=HERE/f'{st}-{f}-neutral.png';im=Image.open(p).convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((220,330),Image.Resampling.LANCZOS),(10+i*240,35+j*375));d.text((10+i*240,10+j*375),st+' / '+f,font=font,fill='#e3cf43');paths.append(p)
 im=Image.open(HERE/f'{st}-south-neutral.png').convert('RGBA')
 for k,size in enumerate([(16,24),(24,36),(32,48)]):
  sm=im.resize(size,Image.Resampling.LANCZOS);plate.paste(sm,(30+i*240+k*65,1160),sm)
d.text((15,1250),'Actual S/E/N renders from each model; source-cell scale fixed. Small south:16x24,24x36,32x48.',font=font,fill='#e5e8d8');d.text((15,1285),'Solid carved interpretations and hidden support depth are authored. Native game acceptance remains pending.',font=font,fill='#e5e8d8');plate.save(HERE/'all-state-view-overview.png');paths += [HERE/'all-state-view-overview.png',HERE.parent/'blender-v1/source-state-reference-comparison.png',HERE.parent/'blender-v1/source-packet.json'];(HERE/'review-inputs.json').write_text(json.dumps([dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],indent=2)+'\n',encoding='utf-8',newline='\n')
