"""Read exactly Ray Cat's generic tile; keep raw installed graphics private."""
from pathlib import Path
import sys,struct,json,hashlib
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs')
import UnityPy
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'tools'));from extract_village_references import string
data=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/resources.assets')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
legacy=json.loads(Path('E:/Temp/qud-transplant-probe-pawns-20261019/faithful-cat.json').read_text());assert sha(data)==legacy['original_model']['resources_sha256']
env=UnityPy.load(str(data));objects={o.path_id:o for o in env.objects};hits=[]
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:name,off=string(raw,28)
 except (ValueError,UnicodeDecodeError,struct.error):continue
 if name.lower()!='assets_content_textures_creatures_sw_cat.bmp':continue
 _,off=string(raw,off);_,off=string(raw,off);texture=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40);assert not rotated
 atlas=objects[texture].read().image.convert('RGBA');tile=atlas.crop((x,atlas.height-y-h,x+w,atlas.height-y));p=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/ray-cat-generic-mask.png');tile.save(p)
 hits.append(dict(blueprint='Ray Cat',tile='creatures/sw_cat.bmp',resources_sha256=sha(data),texture_info=obj.path_id,atlas=texture,rect=[x,y,w,h],private_file=str(p),sha256=sha(p),policy='Alpha coverage, red channel detail ownership under pinned Kobold two-color contract. Different generic glyph from named Ctesiphus sw_kitty.bmp.'))
assert len(hits)==1
(HERE/'generic-original-reference.json').write_bytes((json.dumps(hits[0],indent=2)+'\n').encode());print('Extracted exact generic Ray Cat tile privately; public record contains provenance only.')
