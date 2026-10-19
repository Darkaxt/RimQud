"""Read-only extraction of source-bound Qud tiles into PRIVATE reference storage.

Decodes this inspected Unity build's exTextureInfo layout. Public output contains
only provenance, descriptions and hashes; raw native graphics stay below --root.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import UnityPy
from PIL import Image

REPO=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def key(s):
    s=s.replace('\\','/').lower()
    if s.startswith('assets_content_textures_'):return s
    return 'assets_content_textures_'+s.replace('/','_')
def string(raw,offset):
    n=struct.unpack_from('<i',raw,offset)[0]
    if n<0 or n>500:raise ValueError('Not an inspected texture-info string')
    end=offset+4+n;return raw[offset+4:end].decode('utf-8'),(end+3)&~3

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True)
    ap.add_argument('--data',type=Path,default=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data'));args=ap.parse_args()
    assert sha(args.data/'Managed/Assembly-CSharp.dll')=='cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7'
    sources=json.loads((REPO/'art/village/sources.json').read_text(encoding='utf-8'))
    wanted={}
    for row in sources['scenery']:
        render=row.get('render') or {};tile=render.get('Tile')
        if not tile and render.get('RenderString'):
            glyph=render['RenderString'];tile='text/'+str(int(glyph) if glyph.isdigit() else ord(glyph)) + '.bmp'
        if tile:wanted[row['blueprint']]=dict(tile=tile,description=(row.get('description') or {}).get('Short',''),render=row['render'],kind='scenery')
    for row in sources['actors']:
        for actor in row['native_instances']:
            wanted.setdefault(row['creature'],dict(tile=actor.get('tile') or row['original_model_tiles'][0],description=actor['description'],kind='creature'))
            for part in actor['parts']:
                item=part.get('equipped')
                if item and item.get('tile'):wanted[item['blueprint']]=dict(item,kind='equipment')
    for i in [1,2,3]:wanted['Basic Grass '+str(i)]=dict(tile=f'Terrain/sw_grass{i}.bmp',description='Native visible cell grass paint; not a crop or a new game object',kind='paint')
    env=UnityPy.load(str(args.data/'resources.assets'));objects={o.path_id:o for o in env.objects};infos={};atlases={}
    for obj in env.objects:
        if obj.type.name!='MonoBehaviour':continue
        raw=obj.get_raw_data()
        try:
            name,off=string(raw,28)
            if not name.lower().startswith('assets_content_textures_'):continue
            _,off=string(raw,off);_,off=string(raw,off)
            texture=struct.unpack_from('<q',raw,off+4)[0]
            rotated=struct.unpack_from('<i',raw,off+12)[0]
            x,y,w,h=struct.unpack_from('<4i',raw,off+40)
            if rotated or not(0<w<=1024 and 0<h<=1024):continue
            infos[name.lower()]=(obj.path_id,texture,x,y,w,h)
        except (ValueError,UnicodeDecodeError,struct.error):continue
    out=args.root/'donor/village-originals';out.mkdir(parents=True,exist_ok=True);rows=[];missing=[]
    for name,row in wanted.items():
        info=infos.get(key(row['tile']))
        if info is None:missing.append(dict(blueprint=name,tile=row['tile']));continue
        ident,atlas,x,y,w,h=info
        if atlas not in atlases:atlases[atlas]=objects[atlas].read().image.convert('RGBA')
        im=atlases[atlas];crop=im.crop((x,im.height-y-h,x+w,im.height-y))
        slug=re.sub('[^a-z0-9]+','-',name.lower()).strip('-');raw_path=out/(slug+'-mask.png');crop.save(raw_path)
        # Verified against this build's compiled Kobold dual-color pixel shader:
        # rgb = A*((1-R)*foreground + R*detail) + (1-A)*background.
        # Alpha is coverage; black opaque pixels are PRIMARY, not background.
        reference=Image.new('RGBA',crop.size)
        for yy in range(h):
            for xx in range(w):
                red,_,_,alpha=crop.getpixel((xx,yy))
                reference.putpixel((xx,yy),((225,229,216,alpha) if red<128 else (143,160,138,alpha)))
        ref_path=out/(slug+'-reference.png');reference.save(ref_path)
        rows.append(dict(**{**row,'blueprint':name},reference_file=ref_path.relative_to(args.root/'donor').as_posix(),
            native_mask_sha256=sha(raw_path),reference_sha256=sha(ref_path),info_id=ident,atlas_id=atlas,rect=[x,y,w,h]))
    result=dict(scope='Native tile references; graphics retained privately, not a public asset bundle',entries=rows,missing=missing)
    (REPO/'evidence/village-reference-index.json').write_bytes((json.dumps(result,indent=2)+'\n').encode())
    print('Private references:',len(rows),'unresolved:',missing)
if __name__=='__main__':main()
