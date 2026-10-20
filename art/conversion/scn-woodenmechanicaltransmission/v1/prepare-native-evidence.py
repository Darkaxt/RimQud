"""Bind extracted axle keys to exact phases/neighbor flags and show contextual native art."""
from pathlib import Path
import json,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];p=HERE/'native-state-index.json';data=json.loads(p.read_text());pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=np.frombuffer(bytes.fromhex(pal['w']),dtype=np.uint8);plate=Image.new('RGB',(1440,960),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
for row in data['states']:
 m=re.search(r'sw_axle_([123])_([nsew]*)\.png$',row['tile_key']);assert m;phase=int(m[1]);suffix=m[2];mask=sum(dict(n=1,e=2,s=4,w=8)[s] for s in suffix);row.update(phase=phase,native_suffix=suffix,neighbor_mask=mask,native_tile=f'Tiles/sw_axle_{phase}_{suffix}.png');a=np.array(Image.open(row['private_mask']['path']).convert('RGBA'));im=Image.fromarray(np.dstack([np.broadcast_to(fg,a[:,:,:3].shape),a[:,:,3]])).resize((96,144),Image.Resampling.NEAREST);x=(phase-1)*480+(mask%4)*120;y=(mask//4)*230+35;plate.paste(im,(x+10,y),im);d.text((x+7,y+150),f'{phase}:{mask:02d} {suffix or "none"}',font=font,fill='#e3cf43')
data['mapping']='Source suffix order n,s,e,w; neighbor bits N1 E2 S4 W8. Three actual phases per each of16suffixes, unpowered uses phase1.';assert len(data['states'])==48 and len({(r['phase'],r['neighbor_mask']) for r in data['states']})==48;p.write_bytes((json.dumps(data,indent=2)+'\n').encode());plate.save(HERE/'native-family-comparison.png');print('Bound all48actual source keys; contextual source plate saved.')
