"""Correct g/G preview collision on Windows; neutral production artwork stays byte-identical."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'blender-v2/registered';pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
before=ref(OUT/'legacy-grass1-native-g.png');plate=Image.new('RGB',(1180,610),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);paths=[]
for i,(name,key,label) in enumerate([('dirt1','w','w'),('dirt1','y','y'),('legacy-grass1','g','dark-green-g'),('legacy-grass1','G','bright-green-G')]):
 p=np.array(Image.open(OUT/f'{name}-neutral.png'));tint=p.copy();tint[:,:,:3]=np.uint8(np.round(p[:,:,:3].astype(float)*np.array(list(bytes.fromhex(pal[key])))/255));tint[tint[:,:,3]==0,:3]=0;path=OUT/f'{name}-native-{label}.png';Image.fromarray(tint).save(path);paths.append(ref(path));im=Image.fromarray(tint);bg=Image.new('RGBA',(240,360),'#'+pal['k']);bg.alpha_composite(im.resize((240,360),Image.Resampling.LANCZOS));plate.paste(bg.convert('RGB'),(15+i*290,60));d.text((15+i*290,20),name+' / native '+key,font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize(size,Image.Resampling.LANCZOS);bg=Image.new('RGBA',size,'#'+pal['k']);bg.alpha_composite(small);plate.paste(bg.convert('RGB'),(30+i*290+j*75,450))
d.text((15,540),'Two new exact aliases; existing sw_grass1/2/3 reused by source/model hashes.',font=font,fill='#e5e8d8');d.text((15,570),'Invisible producer stays native. Source-cell primary tint and one coverage; no gameplay/native acceptance yet.',font=font,fill='#e5e8d8');plate.save(OUT/'registration-comparison.png')
(OUT/'preview-name-correction.json').write_text(json.dumps(dict(reason='Case-only g/G filenames collided on Windows and bright G overwrote the dark preview. Exact palette comparison caught this before readiness. Explicit dark-green-g/bright-green-G names resolve it; production neutral/coverage and reviewed raw art unchanged.',rejected_ambiguous_preview=before,current_unique_previews=paths,native_activation=False),indent=2)+'\n',encoding='utf-8');print('Distinct Windows-safe g/G preview names saved; prior ambiguous preview retained as diagnostic evidence.')
