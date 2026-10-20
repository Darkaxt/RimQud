"""Extract the actual unhung and hanging hammock source masks privately."""
from pathlib import Path
import json,hashlib,struct,sys
import UnityPy
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'tools'))
from extract_village_references import string
DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');PRIVATE=Path('E:/Temp/rimqud-native-hammock-20261020');PRIVATE.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(DATA/'Managed/Assembly-CSharp.dll')=='cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7'
env=UnityPy.load(str(DATA/'resources.assets'));objects={o.path_id:o for o in env.objects};infos={};atlases={}
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:
  name,off=string(raw,28)
  if name.lower() not in {x.lower() for x in ['Assets_Content_Textures_Items_sw_shawl.bmp','Assets_Content_Textures_Items_sw_hammock.bmp']}:continue
  _,off=string(raw,off);_,off=string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40)
  if not rotated and 0<w<=1024 and 0<h<=1024:infos[name.lower()]=(obj.path_id,atlas,x,y,w,h)
 except (ValueError,UnicodeDecodeError,struct.error):continue
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];lo,hi=bytes.fromhex(palette['y']),bytes.fromhex(palette['Y'])
plate=Image.new('RGB',(720,655),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
d.text((22,14),'HAMMOCK / actual unhung and hanging tiles / TileColor y + detail Y',font=font,fill='#e3cf43')
rows=[]
for n,(state,tile) in enumerate([('unhung','Assets_Content_Textures_Items_sw_shawl.bmp'),('hanging','Assets_Content_Textures_Items_sw_hammock.bmp')],1):
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
d.text((22,580),'Both actual native states retained; original masks stay private.',font=font,fill='#e5e8d8')
packet=dict(game_assembly_sha256=sha(DATA/'Managed/Assembly-CSharp.dll'),resources_path=str(DATA/'resources.assets'),
 selector='Hangable.Render replaces E.Tile with Items/sw_hammock.bmp while Hanging; otherwise Items/sw_shawl.bmp',states=rows,
 original_reference_limit='The older reference index exports only the default shawl-like tile. Actual hanging tile now has its own exact source evidence.')
(HERE/'native-state-index.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode());plate.save(HERE/'native-states-comparison.png');print('Read both actual native hammock appearances into private E-drive reference storage.')
