"""Correct only chain/glint ink neutrality; preserve all original item/body geometry."""
from pathlib import Path
import json,hashlib,io,sys
from PIL import Image
import numpy as np
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'model.json').exists();m=json.loads((OLD/'model.json').read_text());changes={}
for f,rows in m['views'].items():
 s=(OLD/f'detail-region-{f}.svg').read_text().replace('#202523','#232323');(HERE/f'detail-region-{f}.svg').write_bytes(s.encode());im=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA');a=np.array(im);assert np.max(np.ptp(a[:,:,:3].astype(int),axis=2))==0;assert np.array_equal(a[:,:,3],np.array(Image.open(OLD/f'item-detail-{f}.png'))[:,:,3]);im.save(HERE/f'item-detail-{f}.png')
 for row in rows:
  if row['component']=='item-detail':row.update(file=f'human-female-telescopic-monocle-v2-item-detail-{f}.png',public_file=ref(HERE/f'item-detail-{f}.png')['path'],sha256=ref(HERE/f'item-detail-{f}.png')['sha256'])
 m['occlusion_sources'][f]['detail']=ref(HERE/f'detail-region-{f}.svg');changes[f]=dict(detail=ref(HERE/f'item-detail-{f}.png'),same_alpha=True,full_item_unchanged=True,body_mask_unchanged=True)
m['correction']='v1 chain/glint stroke had nonneutral #202523. v2 uses neutral #232323 before rasterization; source alpha and all full item/body geometry remain unchanged.';write('model.json',m);write('correction-decisions.json',dict(previous=ref(OLD/'model.json'),cause=m['correction'],new_imagegen_call=False,views=changes))
print('Neutral detail rasterized from corrected editable source; all original alpha bounds unchanged.')
