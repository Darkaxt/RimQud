"""Read-only extraction of the installed sixteen painted metal wall states, kept private."""
from pathlib import Path
import sys,json,hashlib,struct
import UnityPy
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'tools'))
from extract_village_references import string
DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data')
PRIVATE=Path('E:/Temp/rimqud-native-rustedmetalwall-20261020');PRIVATE.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(DATA/'Managed/Assembly-CSharp.dll')=='cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7'
env=UnityPy.load(str(DATA/'resources.assets'));objects={o.path_id:o for o in env.objects};infos={};atlases={}
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:
  name,off=string(raw,28)
  if not name.lower().startswith('assets_content_textures_tiles_wall_metal-'):continue
  _,off=string(raw,off);_,off=string(raw,off)
  texture=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40)
  if not rotated and 0<w<=1024 and 0<h<=1024:infos[name.lower()]=(obj.path_id,texture,x,y,w,h)
 except (ValueError,UnicodeDecodeError,struct.error):continue
rows=[];missing=[];palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
lo,hi=bytes.fromhex(palette['r']),bytes.fromhex(palette['C'])
plate=Image.new('RGB',(1280,970),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
d.text((20,16),'ACTUAL RUSTED METAL WALL / sixteen cardinal source states / decoded r + C',font=font,fill='#e3cf43')
for mask in range(16):
 # Native eight-bit suffix is N,NE,E,SE,S,SW,W,NW; recipient is N,E,S,W.
 suffix=''.join(('1' if mask&bit else '0') if bit else '0' for bit in [1,0,2,0,4,0,8,0])
 tile='Assets_Content_Textures_Tiles_wall_metal-'+suffix+'.bmp';info=infos.get(tile.lower())
 if info is None:missing.append(dict(mask=mask,tile=tile));continue
 ident,atlas,x,y,w,h=info
 if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
 im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y));path=PRIVATE/f'{mask:02d}-mask.png';crop.save(path)
 rows.append(dict(mask=mask,native_suffix=suffix,tile=tile,info_id=ident,atlas_id=atlas,rect=[x,y,w,h],private_mask=dict(path=str(path),sha256=sha(path))))
 original=Image.new('RGBA',crop.size,'#'+palette['k'])
 for yy in range(h):
  for xx in range(w):
   rr,_,_,aa=crop.getpixel((xx,yy));f=rr/255
   if aa:original.putpixel((xx,yy),(*[round(a*(1-f)+b*f) for a,b in zip(lo,hi)],255))
 ox=mask%4*320+90;oy=mask//4*220+64
 plate.paste(original.resize((128,192),Image.Resampling.NEAREST).convert('RGB'),(ox,oy));d.text((mask%4*320+22,oy+192),f'{mask:02d}  {suffix}',font=font,fill='#e5e8d8')
all_states=[]
for tile,info in sorted(infos.items()):
 ident,atlas,x,y,w,h=info
 if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
 im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y));suffix=tile.rsplit('-',1)[1].split('.')[0]
 path=PRIVATE/f'native-{suffix}-mask.png';crop.save(path)
 all_states.append(dict(native_suffix=suffix,tile=tile,info_id=ident,atlas_id=atlas,rect=[x,y,w,h],private_mask=dict(path=str(path),sha256=sha(path))))
assert len(all_states)==256
packet=dict(game_assembly_sha256=sha(DATA/'Managed/Assembly-CSharp.dll'),resources_path=str(DATA/'resources.assets'),
 state_mapping='ZoneManager.PaintWall appends dash and N,NE,E,SE,S,SW,W,NW bits. Plate shows16cardinal-only contexts; recipient bits remain N1,E2,S4,W8. All installed native keys are indexed; diagonals remain explicit native source states.',
 inherited_reference_limit='The previously exported static tile-0-13 is an inherited placeholder, not the painted metal wall shape.',
originals=rows,all_native_states=all_states,missing=missing,available_metal_wall_keys=sorted(infos))
(HERE/'native-state-index.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
if missing:print(json.dumps(packet,indent=2));raise SystemExit('Missing required native metal wall cardinal states')
plate.save(HERE/'native-states-comparison.png');print('Extracted sixteen actual painted metal wall states privately; public contextual plate/metadata saved.')
