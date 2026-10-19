"""Source-first Qud scenery: editable contours, palette roles and linked surfaces.

Native reference PNGs stay private. VTracer 0.6.15 smooths the decoded native
coverage; authored material strokes refine the resulting geometry. Terrain and
wall connectivity remain deterministic source SVG, not generated scene paintings.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import random
import re
import shutil
import xml.etree.ElementTree as ET
from PIL import Image
import resvg_py
import vtracer

REPO=Path(__file__).resolve().parents[1];OUT=REPO/'art/village/scenery'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
def svg(s,w,h):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{s}</svg>\n'
def render(path,s):path.write_bytes(s.encode());p=path.with_suffix('.png');p.write_bytes(resvg_py.svg_to_bytes(svg_path=str(path),skip_system_fonts=True));return p

def trace(mask,scratch,name):
    p=scratch/(name+'.png');mask.resize((mask.width*8,mask.height*8),Image.Resampling.NEAREST).save(p)
    f=scratch/(name+'.svg');vtracer.convert_image_to_svg_py(str(p),str(f),colormode='color',mode='spline',filter_speckle=0,corner_threshold=75,length_threshold=1.5,path_precision=3)
    tree=ET.fromstring(f.read_text(encoding='utf-8'));paths=[]
    for node in tree:
        if node.tag.endswith('path'):
            paths.append(f'<path d="{node.attrib["d"]}" transform="{node.attrib.get("transform","")}"/>')
    return ''.join(paths)

def wall_atlas(material,detail=False):
    defs='<defs><pattern id="poles" width="16" height="96" patternUnits="userSpaceOnUse"><rect width="16" height="96" fill="#a9afa2"/><path d="M2 0V96 M13 0V96" stroke="#22392e" stroke-width="2"/><path d="M6 0V96 M8 15L10 28 M5 65L8 73" stroke="#e0e3d4" stroke-width="1.5"/></pattern></defs>'
    out=defs
    for mask in range(16):
        x=(mask%4)*128+16;y=(3-mask//4)*128+16
        lo,hi=(39,57) if material=='fence' else (30,66)
        arms=[f'M{lo} {lo}H{hi}V{hi}H{lo}Z']
        if mask&1:arms+=[f'M{lo} 0H{hi}V48H{lo}Z']
        if mask&2:arms+=[f'M48 {lo}H96V{hi}H48Z']
        if mask&4:arms+=[f'M{lo} 48H{hi}V96H{lo}Z']
        if mask&8:arms+=[f'M0 {lo}H48V{hi}H0Z']
        shape=' '.join(arms)
        fill='url(#poles)' if material=='brinestalk' else '#b3b9ae' if material=='canvas' else '#a8b2ac'
        if detail:
            content=f'<path d="{shape}" fill="none" stroke="#e0e5d9" stroke-width="4"/>'
            if material=='metal':content+='<path d="M31 31L65 65 M65 31L31 65" stroke="#d3d9d0" stroke-width="3"/>'
        else:
            content=f'<path d="{shape}" fill="{fill}" stroke="#1e352c" stroke-width="4" stroke-linejoin="round"/>'
            if material=='canvas':content+='<path d="M34 32V64 M46 32V64 M58 32V64 M32 40H64 M32 52H64" stroke="#d5dbc9" stroke-width="1"/>'
            if material=='metal':content+='<path d="M32 33L65 64 M32 49L48 65 M47 31L65 49" stroke="#51685b" stroke-width="2"/>'
        out+=f'<g transform="translate({x} {y})">{content}</g>'
    return svg(out,512,512)

def surface(kind,palette):
    rng=random.Random(1701);w=h=256
    base={'marsh':'#123e2b','soil':'#555a40','sand':'#98875f','water-shallow':'#40a4b9','water-deep':'#0048bd'}[kind]
    s=f'<rect width="256" height="256" fill="{base}"/>'
    if kind.startswith('water'):
        for y in [18,64,112,166,216]:
            s+=f'<path d="M-32 {y} Q0 {y-9} 32 {y} T96 {y} T160 {y} T224 {y} T288 {y}" fill="none" stroke="{palette["C"]}" stroke-opacity=".22" stroke-width="2"/>'
    else:
        for _ in range(2200):
            x=rng.randrange(256);y=rng.randrange(256);r=rng.choice([.25,.4,.6,.8]);color='#009403' if kind=='marsh' else '#cfc041' if kind=='sand' else '#b1c9c3'
            for dx in [-256,0,256]:
                for dy in [-256,0,256]:s+=f'<ellipse cx="{x+dx}" cy="{y+dy}" rx="{r*1.7}" ry="{r}" fill="{color}" opacity=".075"/>'
    return svg(s,w,h)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True);args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True);scratch=args.root/'scratch/scenery-traces';scratch.mkdir(exist_ok=True)
    source=json.loads((REPO/'evidence/village-reference-index.json').read_text(encoding='utf-8'))
    palette={k:'#'+v for k,v in json.loads((REPO/'evidence/joppa-anatomy-study.json').read_text(encoding='utf-8'))['native_palette'].items()}
    entries={};surface_map={};rows=[]
    for row in source['entries']:
        if row['kind']!='scenery':continue
        name=row['blueprint'];ident=slug(name)
        if name in ['DirtFloor','DirtPath','Pond']:continue
        mask=Image.open(args.root/'donor'/row['reference_file'].replace('-reference.png','-mask.png')).convert('RGBA')
        w,h=mask.size;coverage=Image.new('RGBA',mask.size);detail=Image.new('RGBA',mask.size)
        for y in range(h):
            for x in range(w):
                r,_,_,a=mask.getpixel((x,y));coverage.putpixel((x,y),(226,230,216,a));detail.putpixel((x,y),(226,230,216,r*a//255))
        layers=[]
        for component,im in [('body',coverage),('detail',detail)]:
            if im.getchannel('A').getbbox() is None:continue
            geometry=trace(im,scratch,ident+'-'+component)
            # Material detailing is clipped to the original geometry. It does
            # not turn a Qud machine into an unrelated donor bench or cabinet.
            content=f'<g fill="#dbe0d1" stroke="#20382c" stroke-width="1.4" stroke-linejoin="round">{geometry}</g>'
            file=render(OUT/f'{ident}-{component}.svg',svg(content,w*8,h*8));target='village-scenery-'+ident+'-'+component+'.png';shutil.copy2(file,args.root/'donor'/target)
            bounds=coverage.getchannel('A').getbbox();cx=w*4;cy=bounds[3]*8;scale=.005
            layers.append(dict(component=component,file=target,sha256=sha(file),size=[w*8,h*8],contact=[cx,cy],color_role='detail' if component=='detail' else 'foreground',
                width=w*8*scale/(2/3),height=h*8*scale,center_x=0,center_z=(cy-h*4)*scale,layer=.0002 if component=='detail' else 0))
        kind='wall' if 'Wall' in name else 'door' if name=='Door' else 'fence' if name=='BrinestalkFence' else 'bridge' if name=='BrineBridge' else 'prop'
        entries[name]=dict(kind=kind,views={d:layers for d in ['south','east','north']},reference=row,
            authoring='Native coverage and detail contours -> editable spline geometry -> restrained outline refinement. No donor object substitution.',state='Authored; native batch acceptance pending')
    for kind in ['marsh','soil','sand','water-shallow','water-deep']:
        p=render(OUT/f'surface-{kind}.svg',surface(kind,palette));filename=f'village-surface-{kind}.png';shutil.copy2(p,args.root/'donor'/filename);surface_map[kind+'.png']=filename
    paint=next(r for r in source['entries'] if r['blueprint']=='Basic Grass 1')
    grass=Image.open(args.root/'donor'/paint['reference_file']).convert('RGBA');geometry=trace(grass,scratch,'native-grass')
    p=render(OUT/'basic-grass.svg',svg(f'<g fill="#009403" stroke="#155352" stroke-width="1.5">{geometry}</g>',grass.width*8,grass.height*8))
    filename='village-basic-grass.png';shutil.copy2(p,args.root/'donor'/filename);surface_map['grass.png']=filename
    for name,alias in [('Door','door.png'),('BrineBridge','bridge.png')]:surface_map[alias]=entries[name]['views']['south'][0]['file']
    walls={}
    for name,material in [('BrinestalkWall','brinestalk'),('BrinestalkWallWithGearbox','brinestalk'),('CanvasWall','canvas'),('RustedMetalWall','metal')]:
        files=[]
        for detail in [False,True]:
            suffix='-detail' if detail else '';p=render(OUT/f'wall-{material}{suffix}.svg',wall_atlas(material,detail));filename=f'village-wall-{material}{suffix}.png';shutil.copy2(p,args.root/'donor'/filename);files.append(filename)
        walls[name]=files
    for detail in [False,True]:
        suffix='-detail' if detail else '';p=render(OUT/f'fence{suffix}.svg',wall_atlas('fence',detail));filename=f'village-fence{suffix}.png';shutil.copy2(p,args.root/'donor'/filename)
        surface_map['fence'+suffix+'.png']=filename
    write(REPO/'art/village/scenery-models.json',dict(entries=entries,surfaces=surface_map,walls=walls,
        native_shader_mask_formula='A*((1-R)*foreground + R*detail) + (1-A)*background; checked against installed pixel shader',
        palette_source='evidence/joppa-anatomy-study.json',authoring='Source-first deterministic geometry; VTracer==0.6.15 and resvg-py==0.5.0'))
    print('Authored',len(entries),'source-bound scenery silhouettes, five continuous surfaces and three 16-mask wall material families.')
if __name__=='__main__':main()
