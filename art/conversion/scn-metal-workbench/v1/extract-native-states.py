"""Read both actual Metal Table inventory appearances; keep raw masks private."""
from pathlib import Path
import json,hashlib,struct,sys
import UnityPy
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'tools'))
from extract_village_references import string
DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');PRIVATE=Path('E:/Temp/rimqud-native-metal-workbench-20261020');PRIVATE.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(DATA/'Managed/Assembly-CSharp.dll')=='cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7'
tiles=['Assets_Content_Textures_Items_sw_table_metal.bmp','Assets_Content_Textures_Items_sw_table_metal_full.bmp'];env=UnityPy.load(str(DATA/'resources.assets'));objects={o.path_id:o for o in env.objects};infos={};atlases={}
for o in env.objects:
 if o.type.name!='MonoBehaviour':continue
 raw=o.get_raw_data()
 try:
  name,off=string(raw,28)
  if name.lower() not in {x.lower() for x in tiles}:continue
  _,off=string(raw,off);_,off=string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40)
  if not rotated and 0<w<=1024 and 0<h<=1024:infos[name.lower()]=(o.path_id,atlas,x,y,w,h)
 except (ValueError,UnicodeDecodeError,struct.error):continue
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];lo,hi=bytes.fromhex(palette['c']),bytes.fromhex(palette['C']);plate=Image.new('RGB',(900,650),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);d.text((20,15),'METAL WORKBENCH / actual empty + occupied native tiles / c primary + C detail example',font=font,fill='#e3cf43');rows=[]
for n,(state,tile) in enumerate(zip(['empty','occupied'],tiles)):
 ident,atlas,x,y,w,h=infos[tile.lower()]
 if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
 im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y));p=PRIVATE/f'{state}-mask.png';assert not p.exists(),'Preserve source extraction';crop.save(p)
 rows.append(dict(state=state,tile=tile,info_id=ident,atlas_id=atlas,rect=[x,y,w,h],private_mask=dict(path=str(p),sha256=sha(p))))
 view=Image.new('RGBA',crop.size);view.putdata([(*[round(a*(1-r/255)+b*r/255) for a,b in zip(lo,hi)],alpha) for r,g,b,alpha in crop.get_flattened_data()]);view=view.resize((256,384),Image.Resampling.NEAREST);plate.paste(view,(65+n*450,95),view);d.text((40+n*450,515),state+' / original16x24',font=font,fill='#e5e8d8')
 for yy in range(h):
  row=''.join('.' if crop.getpixel((xx,yy))[3]<128 else ('+' if crop.getpixel((xx,yy))[0]>=128 else '#') for xx in range(w))
  if '#'in row or '+'in row:print(state,yy,row)
d.text((20,585),'Occupied decorations indicate stock, not identified inventory or a donor crafting recipe.',font=font,fill='#e5e8d8')
(HERE/'native-state-index.json').write_bytes((json.dumps(dict(game_assembly_sha256=sha(DATA/'Managed/Assembly-CSharp.dll'),states=rows,selector='Inventory.CheckEmptyState/CheckNonEmptyState use inherited Metal Table EmptyTile/FullTile and independent detail-color choice.'),indent=2)+'\n').encode());plate.save(HERE/'native-states-comparison.png')
