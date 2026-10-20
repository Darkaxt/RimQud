"""Extract only the three declared millstone masks to private reference storage."""
from pathlib import Path
import sys,importlib.util,json,hashlib,struct
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs')
import UnityPy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIVATE=Path('E:/Temp/rimqud-native-millstone-20261021');PRIVATE.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (HERE/'native-frames.json').exists()
data=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');asset=data/'resources.assets'
assert sha(asset)=='61f5c811a061626bc646f7ee654afb4575c2b4b9ad703a05b18655b2505ed376'
spec=importlib.util.spec_from_file_location('source_decode',ROOT/'tools/extract_village_references.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
wanted={m.key(f'Items/sw_millstone_{i}.bmp'):i for i in [1,2,3]};env=UnityPy.load(str(asset));objects={o.path_id:o for o in env.objects};found={}
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:
  name,off=m.string(raw,28)
  if name.lower() not in wanted:continue
  _,off=m.string(raw,off);_,off=m.string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40);assert not rotated
  im=objects[atlas].read().image.convert('RGBA');crop=im.crop((x,im.height-y-h,x+w,im.height-y));i=wanted[name.lower()];p=PRIVATE/f'frame-{i}-mask.png';crop.save(p);found[i]=dict(frame=i,tile=f'Items/sw_millstone_{i}.bmp',info_id=obj.path_id,atlas_id=atlas,rect=[x,y,w,h],private_mask=dict(path=str(p),sha256=sha(p)))
 except (ValueError,UnicodeDecodeError,struct.error):continue
assert set(found)=={1,2,3}
(HERE/'native-frames.json').write_bytes((json.dumps(dict(resources=dict(path=str(asset),sha256=sha(asset)),frames=[found[k] for k in sorted(found)]),indent=2)+'\n').encode())
for k in sorted(found):
 from PIL import Image
 im=Image.open(found[k]['private_mask']['path']).convert('RGBA');print('FRAME',k)
 for y in range(im.height):print(''.join(' ' if im.getpixel((x,y))[3]==0 else 'D' if im.getpixel((x,y))[0]>127 else 'P' for x in range(im.width)))
