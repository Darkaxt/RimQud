"""Sample the corrected neutral detail source through the existing exact male fit."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';SOURCE=ROOT/'art/conversion/fit-human-female-telescopic-monocle/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'model.json').exists();m=json.loads((OLD/'model.json').read_text());controls=json.loads((OLD/'registration-decisions.json').read_text())['views'];changes={}
for f,rows in m['views'].items():
 c=controls[f];s=c['uniform_scale'];tx=c['translation_x'];ty=c['translation_y'];source=Image.open(SOURCE/f'item-detail-{f}.png').convert('RGBA');im=source.convert('RGBa').transform((512,1024),Image.Transform.AFFINE,(1/s,0,-tx/s,0,1/s,-ty/s),Image.Resampling.BICUBIC).convert('RGBA');a=np.array(im);assert np.max(np.ptp(a[:,:,:3].astype(int),axis=2))==0;assert np.array_equal(a[:,:,3],np.array(Image.open(OLD/f'item-detail-{f}.png'))[:,:,3]);im.save(HERE/f'item-detail-{f}.png')
 xml=ET.fromstring((SOURCE/f'detail-region-{f}.svg').read_text());content=''.join(ET.tostring(n,encoding='unicode') for n in xml);svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g transform="translate('+str(tx)+' '+str(ty)+') scale('+str(s)+')">'+content+'</g></svg>';(HERE/f'fitted-detail-region-{f}.svg').write_bytes(svg.encode())
 for row in rows:
  if row['component']=='item-detail':row.update(file=f'human-male-telescopic-monocle-v2-item-detail-{f}.png',public_file=ref(HERE/f'item-detail-{f}.png')['path'],sha256=ref(HERE/f'item-detail-{f}.png')['sha256'])
 m['occlusion_sources'][f]['detail']=ref(HERE/f'fitted-detail-region-{f}.svg');changes[f]=dict(source=ref(SOURCE/f'item-detail-{f}.png'),uniform_scale=s,translation_x=tx,translation_y=ty,single_premultiplied_sample=True,same_alpha=True,full_item_unchanged=True,body_mask_unchanged=True)
m['correction']='v2 refits corrected neutral female detail before premultiplied resampling; alpha, full item and target-original anatomy remain unchanged.';write('model.json',m);write('correction-decisions.json',dict(previous=ref(OLD/'model.json'),source=ref(SOURCE/'model.json'),cause='Inherited v1 colored chain ink; fix source before resampling, not a post-tint coverup.',new_imagegen_call=False,views=changes));print('Male corrected neutral source fitted with unchanged controls and exact old alpha.')
