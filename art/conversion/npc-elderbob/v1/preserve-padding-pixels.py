"""Keep even hidden source RGB unchanged under transparent top padding."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
assert not (HERE/'padding-correction.json').exists()
model=json.loads((HERE/'model.json').read_text());changed=[]
for f,view in model['views'].items():
    for binding in view['equipment']:
        for r in binding['components']:
            p=ROOT/r['public_file'];old=np.array(Image.open(p).convert('RGBA'))
            source=Image.open(ROOT/r['source_component']['path']).convert('RGBA')
            if r['mirrored_from_east']:source=ImageOps.mirror(source)
            out=Image.new('RGBA',(512,1264));out.paste(source,(0,240));new=np.array(out)
            assert np.array_equal(old[:,:,3],new[:,:,3])
            assert np.array_equal(old[old[:,:,3]>0],new[new[:,:,3]>0])
            if not np.array_equal(old,new):
                changed.append(dict(path=r['public_file'],before_sha256=r['sha256']))
                out.save(p);r['sha256']=hashlib.sha256(p.read_bytes()).hexdigest();changed[-1]['after_sha256']=r['sha256']
            r['padding_method']='Exact integer RGBA copy, including RGB in zero-alpha pixels'
(HERE/'model.json').write_bytes((json.dumps(model,indent=2,ensure_ascii=False)+'\n').encode())
(HERE/'padding-correction.json').write_bytes((json.dumps(dict(reason='Alpha compositing onto a blank padded canvas clears RGB values stored under source alpha0. Visible pixels and alpha were unchanged, but exact RGBA preservation requires direct paste.',correction='Copy source RGBA with integer paste at y+240, retaining transparent RGB as well. Every visible pixel and alpha value verified unchanged; assembled previews remain identical.',changed=changed,native_activation=False),indent=2)+'\n').encode())
print('Preserved exact source RGBA under padding; all visible pixels and alpha are unchanged.')
