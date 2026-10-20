"""Private exact atlas extraction of native industrial fan animation phases."""
from pathlib import Path
import json,hashlib,sys,struct,importlib.util
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs')
import UnityPy
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');PRIVATE=Path('E:/Temp/rimqud-native-fan-20261021')
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'native-frames.json').exists();assembly=private(DATA/'Managed/Assembly-CSharp.dll');assert assembly['sha256']=='cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7';spec=importlib.util.spec_from_file_location('native_reference',ROOT/'tools/extract_village_references.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper);wanted={helper.key(f'Tiles2/sw_fan_{k}.bmp'):k for k in range(1,5)};env=UnityPy.load(str(DATA/'resources.assets'));objects={o.path_id:o for o in env.objects};infos={}
for obj in env.objects:
 if obj.type.name!='MonoBehaviour':continue
 raw=obj.get_raw_data()
 try:
  name,off=helper.string(raw,28)
  if name.lower() not in wanted:continue
  _,off=helper.string(raw,off);_,off=helper.string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40);assert not rotated and (w,h)==(16,24);infos[wanted[name.lower()]]=(name,obj.path_id,atlas,x,y,w,h)
 except (ValueError,UnicodeDecodeError,struct.error):continue
assert len(infos)==4;PRIVATE.mkdir(exist_ok=True);rows=[];palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=bytes.fromhex(palette['y']);dc=bytes.fromhex(palette['c']);plate=Image.new('RGB',(1300,650),'#142823');font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);d=ImageDraw.Draw(plate);d.text((18,15),'INDUSTRIAL FAN / exact native rotor phases / y primary + c detail / Broken normally uses default frame3',font=font,fill='#e3cf43')
for i,k in enumerate(range(1,5)):
 name,ident,atlas,x,y,w,h=infos[k];im=objects[atlas].read().image.convert('RGBA');crop=im.crop((x,im.height-y-h,x+w,im.height-y));p=PRIVATE/f'frame-{k}-mask.png';crop.save(p);rows.append(dict(frame=k,native_phase=(k-1)*5,default=k==3,tile=name,info_id=ident,atlas_id=atlas,rect=[x,y,w,h],private_mask=private(p)));preview=Image.new('RGBA',crop.size)
 for yy in range(h):
  for xx in range(w):
   red,_,_,alpha=crop.getpixel((xx,yy));preview.putpixel((xx,yy),tuple(round(fg[c]*(1-red/255)+dc[c]*red/255) for c in range(3))+(alpha,))
 preview=preview.resize((256,384),Image.Resampling.NEAREST);plate.paste(preview,(20+i*320,65),preview);d.text((20+i*320,475),f'FRAME{k} / PHASE{(k-1)*5}'+(' / DEFAULT' if k==3 else ''),font=font,fill='#e3cf43')
d.text((18,535),'AnimatedMaterialGeneric length20, frames at0/5/10/15, requires operational Fan. Native logic owns phase/power/Broken.',font=font,fill='#e5e8d8');d.text((18,570),'Source face/map plane only; no new perspective facings, spin timing or repaired behavior implemented.',font=font,fill='#e5e8d8');plate.save(HERE/'native-frames-comparison.png');write(HERE/'native-frames.json',dict(assembly=assembly,resource=private(DATA/'resources.assets'),frames=rows,default_frame=3,native_phase_length=20,requires_operational_active_part='Fan',scope='Source metadata/art extraction only, not a native replacement test. Raw source kept private.'));print('Extracted4exact native source phases privately; source default frame3 retained.')
