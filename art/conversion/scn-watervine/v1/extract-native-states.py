"""Extract the three actual RandomTile watervine source masks privately."""
from pathlib import Path
import json,hashlib,struct,sys
import UnityPy
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'tools'))
from extract_village_references import string
DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');PRIVATE=Path('E:/Temp/rimqud-native-watervine-20261020');PRIVATE.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(DATA/'Managed/Assembly-CSharp.dll')=='cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7'
env=UnityPy.load(str(DATA/'resources.assets'));objects={o.path_id:o for o in env.objects};infos={};atlases={}
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:
  name,off=string(raw,28)
  if name.lower() not in {x.lower() for x in ['Assets_Content_Textures_Tiles_sw_watervine1.bmp','Assets_Content_Textures_Tiles_sw_watervine2.bmp','Assets_Content_Textures_Tiles_sw_watervine3.bmp']}:continue
  _,off=string(raw,off);_,off=string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40)
  if not rotated and 0<w<=1024 and 0<h<=1024:infos[name.lower()]=(obj.path_id,atlas,x,y,w,h)
 except (ValueError,UnicodeDecodeError,struct.error):continue
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];lo,hi=bytes.fromhex(palette['w']),bytes.fromhex(palette['g'])
plate=Image.new('RGB',(1080,655),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
d.text((22,14),'WATERVINE / three actual RandomTile variants / native w vine + g wafers',font=font,fill='#e3cf43')
rows=[]
for n,(state,tile) in enumerate([('variant-1','Assets_Content_Textures_Tiles_sw_watervine1.bmp'),('variant-2','Assets_Content_Textures_Tiles_sw_watervine2.bmp'),('variant-3','Assets_Content_Textures_Tiles_sw_watervine3.bmp')],1):
 info=infos.get(tile.lower());assert info is not None,(tile,sorted(infos))
 ident,atlas,x,y,w,h=info
 if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
 im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y));path=PRIVATE/f'{n}-mask.png';crop.save(path)
 rows.append(dict(state=state,tile=tile,info_id=ident,atlas_id=atlas,rect=[x,y,w,h],private_mask=dict(path=str(path),sha256=sha(path))))
 preview=Image.new('RGBA',crop.size,'#'+palette['k'])
 for yy in range(h):
  for xx in range(w):
   rr,_,_,aa=crop.getpixel((xx,yy));f=rr/255
   if aa:preview.putpixel((xx,yy),(*[round(a*(1-f)+b*f) for a,b in zip(lo,hi)],255))
 plate.paste(preview.resize((256,384),Image.Resampling.NEAREST).convert('RGB'),(45+(n-1)*360,84));d.text((30+(n-1)*360,500),f'{state} /16x24',font=font,fill='#e5e8d8')
d.text((22,580),'Three native RandomTile shapes retained; originals stay private.',font=font,fill='#e5e8d8')
packet=dict(game_assembly_sha256=sha(DATA/'Managed/Assembly-CSharp.dll'),resources_path=str(DATA/'resources.assets'),
 selector='RandomTile builder sw_watervine1,2,3.bmp',states=rows,
 original_reference_limit='The older reference index exports only the static first tile; all three actual RandomTile variants now have exact source evidence.')
(HERE/'native-state-index.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode());plate.save(HERE/'native-states-comparison.png');print('Read all three actual native watervine variants into private E-drive reference storage.')
