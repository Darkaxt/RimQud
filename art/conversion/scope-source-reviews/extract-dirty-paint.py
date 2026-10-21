"""Read-only source inspection of the invisible Dirty marker's visible cell-paint outputs."""
from pathlib import Path
import sys,json,hashlib,struct,importlib.util
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];OUT=HERE/'dirty';OUT.mkdir(exist_ok=True);PRIVATE=Path('E:/Temp/rimqud-native-scope-review-20261021')
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs');import UnityPy
spec=importlib.util.spec_from_file_location('decode',ROOT/'tools/extract_village_references.py');decode=importlib.util.module_from_spec(spec);spec.loader.exec_module(decode)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
tiles=['Tiles/tile-dirt1.png','assets_content_textures_tiles_tile-grass1.png','Terrain/sw_grass1.bmp','Terrain/sw_grass2.bmp','Terrain/sw_grass3.bmp'];wanted={decode.key(t):t for t in tiles};env=UnityPy.load('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/resources.assets');objects={o.path_id:o for o in env.objects};atlases={};states=[]
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:
  name,off=decode.string(raw,28)
  if name.lower() not in wanted:continue
  _,off=decode.string(raw,off);_,off=decode.string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotation=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40);assert not rotation
  if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
  im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y));path=PRIVATE/(Path(wanted[name.lower()]).stem+'-mask.png');crop.save(path);states.append(dict(native_tile=wanted[name.lower()],info_id=obj.path_id,atlas_id=atlas,rect=[x,y,w,h],private_mask=ref(path)))
 except (ValueError,UnicodeDecodeError,struct.error):continue
assert len(states)==5,states;states.sort(key=lambda st:tiles.index(st['native_tile']));pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1450,540),'#142823');d=ImageDraw.Draw(plate)
for i,st in enumerate(states):
 key='w' if i==0 else 'g';fg=np.array(list(bytes.fromhex(pal[key])));dt=np.array(list(bytes.fromhex(pal['k'])));a=np.array(Image.open(st['private_mask']['path']).convert('RGBA'));weight=a[:,:,:1]/255;im=Image.fromarray(np.dstack([np.uint8(np.round((1-weight)*fg+weight*dt)),a[:,:,3]]));bg=Image.new('RGBA',(224,336),'#'+pal['k']);bg.alpha_composite(im.resize((224,336),Image.Resampling.NEAREST));plate.paste(bg.convert('RGB'),(20+i*290,70));d.text((20+i*290,20),['DIRT1 PAINT','LEGACY GRASS1','SW GRASS1','SW GRASS2','SW GRASS3'][i],font=font,fill='#e3cf43')
for i,line in enumerate(['Actual invisible Dirty marker paints these5 tile aliases onto cells.', 'Dirt: native w or y / detail k; grass: native g or G / existing detail retained by source code.', 'This is source inspection only. Existing DirtFloor dots aliases do not establish coverage of tile-dirt1 or legacy grass1.']):d.text((20,430+i*30),line,font=font,fill='#e5e8d8')
plate.save(OUT/'painted-source-comparison.png');packet=dict(entry='SCOPE-DIRTY',source_code=[ref(PRIVATE/'Dirty.cs'),ref(PRIVATE/'DirtPicker.cs')],native_states=states,source_paint='Dirty.PaintCell sets w/y dirt1 with k detail, or g/G one of four grass tile aliases; source options and random choices remain native.',scope_question='Widget itself invisible; generated cell paint is visible. Verify actual alias coverage before no-art readiness. DirtFloor dots and grass1..3 do not by themselves cover all5 strings.',native_activation=False)
(OUT/'painted-tile-index.json').write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8',newline='\n');print('Exact5 paint tiles extracted privately and source inspection plate retained.')
