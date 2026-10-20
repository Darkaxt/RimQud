"""Enumerate and extract only actual sw_axle painted tiles, preserving private source art."""
from pathlib import Path
import sys,importlib.util,json,hashlib,struct,re
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs')
import UnityPy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PRIVATE=Path('E:/Temp/rimqud-native-wooden-transmission-20261021');PRIVATE.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert not (HERE/'native-state-index.json').exists();asset=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/resources.assets');assert sha(asset)=='61f5c811a061626bc646f7ee654afb4575c2b4b9ad703a05b18655b2505ed376'
spec=importlib.util.spec_from_file_location('source_decode',ROOT/'tools/extract_village_references.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
env=UnityPy.load(str(asset));objects={o.path_id:o for o in env.objects};infos=[];atlases={}
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:
  name,off=m.string(raw,28)
  if not name.lower().startswith('assets_content_textures_') or 'sw_axle' not in name.lower():continue
  _,off=m.string(raw,off);_,off=m.string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40);assert not rotated
  if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
  im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y));slug=re.sub(r'[^a-z0-9_-]','-',name.lower().split('textures_',1)[1]);p=PRIVATE/(slug+'-mask.png');crop.save(p);infos.append(dict(tile_key=name,info_id=obj.path_id,atlas_id=atlas,rect=[x,y,w,h],private_mask=dict(path=str(p),sha256=sha(p))))
 except (ValueError,UnicodeDecodeError,struct.error):continue
assert infos
(HERE/'native-state-index.json').write_bytes((json.dumps(dict(resources=dict(path=str(asset),sha256=sha(asset)),states=sorted(infos,key=lambda r:r['tile_key'])),indent=2)+'\n').encode());print('Actual states:',len(infos));print('\n'.join(x['tile_key'] for x in sorted(infos,key=lambda r:r['tile_key'])))
