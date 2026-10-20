"""Read installed source atlas for exact ordinary table inventory appearances, privately."""
from pathlib import Path
import sys,json,hashlib,struct,importlib.util
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/unity-libs')
import UnityPy
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');PRIVATE=Path('E:/Temp/rimqud-native-table-20261021')
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'native-states.json').exists();assembly=private(DATA/'Managed/Assembly-CSharp.dll');assert assembly['sha256']=='cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7'
spec=importlib.util.spec_from_file_location('native_reference',ROOT/'tools/extract_village_references.py');helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper);wanted={helper.key('Assets_Content_Textures_Tiles_sw_table.bmp'):'empty',**{helper.key(f'Items/sw_table{i}.bmp'):f'occupied-{i}' for i in range(1,5)}};env=UnityPy.load(str(DATA/'resources.assets'));objects={o.path_id:o for o in env.objects};infos={}
for obj in env.objects:
    if obj.type.name!='MonoBehaviour':continue
    raw=obj.get_raw_data()
    try:
        name,off=helper.string(raw,28)
        if name.lower() not in wanted:continue
        _,off=helper.string(raw,off);_,off=helper.string(raw,off);atlas=struct.unpack_from('<q',raw,off+4)[0];rotated=struct.unpack_from('<i',raw,off+12)[0];x,y,w,h=struct.unpack_from('<4i',raw,off+40);assert not rotated and (w,h)==(16,24);infos[wanted[name.lower()]]=(name,obj.path_id,atlas,x,y,w,h)
    except (ValueError,UnicodeDecodeError,struct.error):continue
assert len(infos)==5;PRIVATE.mkdir(exist_ok=True);rows=[];palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1500,630),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'ORDINARY TABLE / exact native empty + four occupied tiles / actual w primary + illustrative C detail',font=font,fill='#e3cf43')
for i,state in enumerate(['empty']+[f'occupied-{k}' for k in range(1,5)]):
    name,ident,atlas,x,y,w,h=infos[state];image=objects[atlas].read().image.convert('RGBA');mask=image.crop((x,image.height-y-h,x+w,image.height-y));p=PRIVATE/f'{state}-mask.png';mask.save(p);rows.append(dict(state=state,tile=name,info_id=ident,atlas_id=atlas,rect=[x,y,w,h],private_mask=private(p)));preview=Image.new('RGBA',mask.size);fg=bytes.fromhex(palette['w']);detail=bytes.fromhex(palette['C'])
    for yy in range(h):
        for xx in range(w):
            r,g,b,a=mask.getpixel((xx,yy));preview.putpixel((xx,yy),tuple(round(fg[k]*(1-r/255)+detail[k]*r/255) for k in range(3))+(a,))
    preview=preview.resize((256,384),Image.Resampling.NEAREST);plate.paste(preview,(20+i*296,65),preview);d.text((20+i*296,475),state.upper(),font=font,fill='#e3cf43')
d.text((18,530),'Native Inventory chooses one occupied tile and independent detail C,c,y,W. Marks indicate stock, not specific inventory identity.',font=font,fill='#e5e8d8');d.text((18,565),'Raw masks/atlases remain private. This extraction does not launch the game or validate a replacement.',font=font,fill='#e5e8d8');plate.save(HERE/'native-states-comparison.png');write(HERE/'native-states.json',dict(assembly=assembly,resource=private(DATA/'resources.assets'),extractor=private(ROOT/'tools/extract_village_references.py'),states=rows,scope='Read-only exact installed atlas metadata/masks; raw source retained privately. Native Inventory owns state/random choice.'))
print(json.dumps(rows,indent=2))
