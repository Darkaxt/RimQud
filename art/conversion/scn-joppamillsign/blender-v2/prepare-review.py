"""Show actual model renders and intended-size silhouettes without native testing."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
plate=Image.new('RGB',(1240,710),'#142823');d=ImageDraw.Draw(plate)
names=['south-neutral-master.png','east-neutral-master.png','north-neutral-master.png','stage-03-refined-model-3d.png']
for i,name in enumerate(names):
 im=Image.open(HERE/name).convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
 plate.paste(bg.convert('RGB').resize((280,420),Image.Resampling.LANCZOS),(15+i*310,50));d.text((15+i*310,15),['SOUTH','EAST','NORTH','3D DIAGNOSTIC'][i],font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  sm=im.resize(size,Image.Resampling.LANCZOS);plate.paste(sm,(55+i*310+j*70,510),sm)
for i,line in enumerate(['Source painted terracotta plaque; negative pictogram cells translated to dark paint on solid clay.',
 'Two actual rear supports; blank back. One physical frame, real S/E/N model rotations.',
 'South alone maps the native tile. Small images:16x24,24x36,32x48. No native acceptance.']):d.text((15,590+i*30),line,font=font,fill='#e5e8d8')
plate.save(HERE/'three-view-authoring-comparison.png')
paths=[HERE.parent/'blender-v1/source-reference-comparison.png',HERE.parent/'blender-v1/manual-neutral-master.png',HERE.parent/'blender-v1/source-packet.json',HERE/'three-view-authoring-comparison.png']+[HERE/n for n in names]
(HERE/'review-inputs.json').write_text(json.dumps([dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in paths],indent=2)+'\n',encoding='utf-8')
