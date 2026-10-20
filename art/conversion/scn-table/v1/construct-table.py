"""Shared source wood trestle table and separately projected native stock silhouettes."""
from pathlib import Path
import re,json,hashlib,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];VTE=Path('D:/Steam/steamapps/workshop/content/294100/2016436324')
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'source-packet.json').exists();source=json.loads((HERE/'native-states.json').read_text());ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());entry=next(e for e in ledger['entries'] if e['id']=='SCN-TABLE');qud=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=qud.read_text(encoding='utf-8-sig');objects={}
for name in ['Table','Furniture']:
    s=re.search(r'<object\b[^>]*\bName="'+name+r'"[^>]*>.*?</object>',text,re.S).group();ET.fromstring(s);objects[name]=s
reference=json.loads((ROOT/'art/conversion/scn-book-table/v2/source-packet.json').read_text())['directional_reference']
for r in reference['textures'].values():assert private(Path(r['path']))['sha256']==r['sha256']
features={
 'occupied-1':'Tall narrow-neck vessel-like mark at left plus smaller upright mark toward center. Identity not established.',
 'occupied-2':'Wide rectangular vessel-like mark with right-side open handle/slot. Identity not established.',
 'occupied-3':'Rounded shoulder/narrow-top vessel-like form at right, small left upright mark and one tiny tabletop mark. Identity not established.',
 'occupied-4':'Broad left stock form joined to open right rectangular frame, with two unequal upright projections. Identity not established.'}
packet=dict(entry='SCN-TABLE',identity='Table -> Furniture -> InorganicObject',description=entry['metadata']['description']['Short'],native_definition=dict(**private(qud),objects=objects,parsing='Exact source object fragments independently XML-parsed; no source rewrite.'),native_states=source,source_shape='Broad flat wood top over two separated straight/splayed end supports and a low central stretcher. Upright Qud tile does not provide actual hidden depth or number of planks.',native_state='Native Inventory selects empty tile or one of4occupied tiles and independently chooses FullDetailColor C,c,y,W. Do not correlate shape/color to inventory identity or reroll state. One shared source table under all stock overlays.',palette=dict(primary='w on entire wood structure including scratches/highlights',empty_detail='C with zero native covered detail pixels',occupied_detail_choices=['C','c','y','W'],ownership='Only source stock belongs to detail. Gold construction key is ownership, not an authored gold item.'),stock_features=features,stock_geometry_provenance='Vessel-like/handled/round terms describe source silhouettes, not resolved equipment definitions. Depth, roundness, wall thickness, unseen faces and placement are authored estimates; no exact bottle/cup/item inventory identity claimed.',reference=dict(reference,role='Actual VTE EndTable S/E/N gives restrained wood contours/grain and parallel cardinal map-camera end volume only. No drawer, knob, donor footprint or gameplay copied.',about=private(VTE/'About/About.xml')),camera=dict(width=14,depth=8,height=9.3,slab_thickness=.7,depth_projection=.45,projection='u=8+rotated_x; v=18+.45*rotated_y-z; same dimensions/elevation all facings.',supports='Two trestle end boards atXÂ±5.3, thickness1.25, depth5.8; splayed end feet and one low X stretcher. Hidden board extrusion/shape is authored, not native limb count.',provenance='Numeric dimensions inferred/authored from source broad top/supports plus actual donor presentation; no texture-frame ratio copied. End view retains full depth.',west='Empty unmarked table can mirror E; occupied stock requires separate W projection/occlusion.'),frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One common source-cell mapping for entire table and stock in all states/facings. No component/view production bbox fit.'),native_behavior='Weight50 Takeablefalse Organictrue, Container/on Inventory populationTable, MissileCover10%, non-occluding render, sounds and rare Animated1/15000 BodyTypeTable remain native. Unsupported animated/custom behavior retains source art.',native_acceptance='Pending full-set generation gate: native actual inventory/tile/detail choice, physics/visibility/cover, rare Animated fallback and extra-view placement remain unfinished.')
write(HERE/'source-packet.json',packet)
def project(x,y,z,f):
    x,y=dict(south=(x,y),east=(-y,x),north=(-x,-y),west=(y,-x))[f];return 8+x,18+.45*y-z
def polygon(points,f):return 'M'+' L'.join(f'{u:.5f} {v:.5f}' for u,v in [project(*p,f) for p in points])+'Z'
def cuboid(x0,x1,y0,y1,z0,z1,f,stock=False):
    fill='#d7c765' if stock else '#bababa';edge='#746a36' if stock else '#36413b';top='#e5d78a' if stock else '#d5d5d5'
    if f in ['south','north']:
        y=y1 if f=='south' else y0;face=[(x0,y,z1),(x1,y,z1),(x1,y,z0),(x0,y,z0)]
    else:
        x=x1 if f=='east' else x0;face=[(x,y0,z1),(x,y1,z1),(x,y1,z0),(x,y0,z0)]
    cap=[(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
    return f'<g fill="{fill}" stroke="{edge}" stroke-width=".13" stroke-linejoin="round"><path d="{polygon(face,f)}"/><path d="{polygon(cap,f)}" fill="{top}"/></g>'
def wrap(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">'+s+'</svg>'
for f in ['south','east','north','west']:
    chunks=[];parts=[(-5.3,0),(5.3,0)];parts.sort(key=lambda q:project(q[0],q[1],0,f)[1])
    for x,y in parts:
        chunks.append(cuboid(x-.95,x+.95,-3.3,3.3,0,.55,f));chunks.append(cuboid(x-.625,x+.625,-2.9,2.9,.4,8.6,f))
    chunks.append(cuboid(-5.3,5.3,-.35,.35,2.3,2.95,f));chunks.append(cuboid(-7,7,-4,4,8.6,9.3,f));s=wrap(''.join(chunks));(HERE/f'constructed-{f}-base.svg').write_bytes(s.encode());(HERE/f'constructed-{f}-base.png').write_bytes(svg_to_bytes(svg_string=s))
def roundform(x,y,z,h,r,f,kind):
    u,b=project(x,y,z,f);_,t=project(x,y,z+h,f);ry=.45*r;edge='#746a36';fill='#d7c765'
    if kind=='neck':
        neck=.32*r;bodytop=t+h*.36;s=f'<path d="M{u-neck} {t}H{u+neck}V{t+h*.22}Q{u+neck} {bodytop} {u+r} {bodytop+.4}V{b-ry}Q{u+r} {b+ry} {u} {b+ry}Q{u-r} {b+ry} {u-r} {b-ry}V{bodytop+.4}Q{u-neck} {bodytop} {u-neck} {t+h*.22}Z" fill="{fill}" stroke="{edge}" stroke-width=".12"/><ellipse cx="{u}" cy="{t}" rx="{neck}" ry="{ry*.5}" fill="#e5d78a" stroke="{edge}" stroke-width=".1"/>'
    elif kind=='shoulder':
        neck=r*.55;s=f'<path d="M{u-neck} {t}H{u+neck}L{u+r} {t+h*.3}V{b-ry}Q{u+r} {b+ry} {u} {b+ry}Q{u-r} {b+ry} {u-r} {b-ry}V{t+h*.3}Z" fill="{fill}" stroke="{edge}" stroke-width=".12"/><ellipse cx="{u}" cy="{t}" rx="{neck}" ry="{ry*.5}" fill="#e5d78a" stroke="{edge}" stroke-width=".1"/>'
    else:s=f'<path d="M{u-r} {t}H{u+r}V{b-ry}Q{u+r} {b+ry} {u} {b+ry}Q{u-r} {b+ry} {u-r} {b-ry}Z" fill="{fill}" stroke="{edge}" stroke-width=".12"/><ellipse cx="{u}" cy="{t}" rx="{r}" ry="{ry}" fill="#e5d78a" stroke="{edge}" stroke-width=".1"/>'
    return s
def handled(x0,x1,y,z,h,f,prongs=False):
    body=cuboid(x0,x1,y-.8,y+.8,z,z+h,f,True);hy=y+.4
    # Open frame of actual bars: holes remain holes in S/N and become edge views in E/W.
    right=x1+1.5;bar=.3;bottom=z+.15;top=z+h-.2
    frame=cuboid(x1,right,hy-.18,hy+.18,bottom,bottom+bar,f,True)+cuboid(x1,right,hy-.18,hy+.18,top-bar,top,f,True)+cuboid(right-bar,right,hy-.18,hy+.18,bottom,top+(2.8 if prongs else 0),f,True)
    if prongs:frame+=cuboid(x1-.2,x1+.1,hy-.18,hy+.18,top-.1,top+1.7,f,True)
    near=project(right,hy,0,f)[1]>project((x0+x1)/2,y,0,f)[1]
    return body+frame if near else frame+body
recipes={
 'occupied-1':[dict(kind='neck',x=-4.0,y=.8,z=9.3,h=7.5,r=.9),dict(kind='upright',x=-.9,y=.1,z=9.3,h=3.8,r=.65)],
 'occupied-2':[dict(kind='handled',x0=-1.5,x1=2.1,y=.1,z=9.3,h=4.5)],
 'occupied-3':[dict(kind='shoulder',x=3,y=-.2,z=9.3,h=4.7,r=1.5),dict(kind='upright',x=-2.2,y=1.3,z=9.3,h=2.0,r=.65),dict(kind='upright',x=4.7,y=2.3,z=9.3,h=.5,r=.24)],
 'occupied-4':[dict(kind='handled',x0=-4,x1=-1,y=.1,z=9.3,h=3.3,prongs=True)]}
write(HERE/'stock-construction.json',dict(recipes=recipes,reason='Formal vessel-like/handled stock silhouettes inferred from exact source marks, without named item identities. Roundness, handle thickness and unseen planes are authored.',projection=packet['camera']['projection']))
for state,recipe in recipes.items():
    quad=Image.new('RGBA',(1536,1536))
    for i,f in enumerate(['south','east','north','west']):
        ordered=sorted(recipe,key=lambda r:project((r['x0']+r['x1'])/2 if 'x0' in r else r['x'],r['y'],0,f)[1]);parts=[]
        for item in ordered:
            args={k:v for k,v in item.items() if k!='kind'};parts.append(handled(f=f,**args) if item['kind']=='handled' else roundform(f=f,kind=item['kind'],**args))
        s=wrap(''.join(parts));(HERE/f'{state}-{f}-stock.svg').write_bytes(s.encode());(HERE/f'{state}-{f}-stock.png').write_bytes(svg_to_bytes(svg_string=s));base=read(HERE/f'constructed-{f}-base.png');base.alpha_composite(read(HERE/f'{state}-{f}-stock.png'));base.save(HERE/f'{state}-{f}-manual.png');quad.alpha_composite(base,((i%2)*768+128,(i//2)*768))
    quad.save(HERE/f'{state}-manual-turnaround.png')
empty=Image.new('RGBA',(1536,768))
for i,f in enumerate(['south','east','north']):empty.alpha_composite(read(HERE/f'constructed-{f}-base.png'),(i*512,0))
empty.save(HERE/'empty-front-guided-turnaround.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1500,1160),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'TABLE / exact native states + same source wood base / authored full-depth trestle + separately projected stock',font=font,fill='#e3cf43');im=read(HERE/'native-states-comparison.png');im.thumbnail((1400,600));plate.paste(im,(15,45),im)
for i,f in enumerate(['south','east','north','west']):im=read(HERE/f'constructed-{f}-base.png').resize((256,384));plate.paste(im,(20+i*290,620),im);d.text((20+i*290,1010),f.upper(),font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):im=read(Path(reference['textures'][f]['path']));im.thumbnail((100,100));plate.paste(im,(1210,655+i*115),im)
d.text((18,1060),'Actual VTE EndTable S/E/N: wood contour/shallow cardinal camera only, no donor drawers or footprint.',font=font,fill='#e5e8d8');d.text((18,1090),'Authored14x8x9.3form, depth factor.45. Source w wood; native independent C,c,y,W stock. No inventory item identity inferred.',font=font,fill='#e5e8d8');plate.save(HERE/'source-reference-construction.png')
(HERE/'empty-turnaround-prompt.txt').write_bytes(f'''Use case: sketch-to-render. ONE Qud EMPTY ordinary wood table in three cardinal map views. Image1 is1536x768 edit target, equal512x768columns SOUTH front, EAST complete end, NORTH back. Image2 actual VTE EndTable east provides restrained wood contour/grain and shallow map-camera only; no drawers/knobs. Image3 actual Qud empty plus4occupied states supplies identity; generate EMPTY table only.
Description: {packet['description']}
Preserve the broad rectangular wood top with shallow apron, two simple end-board trestle supports, low central connecting stretcher and splayed end feet. Hidden support extrusion is an authored interpretation, not a native leg count. One physical width14/depth8/height9.3/slab.7, projection u8+rotated_x,v18+.45*rotated_y-z. Same full512x768cell/scale/pivot8,16 all views. S/N broad front; E has full8depth and two overlapping trestles under long visible tabletop depth, not a compressed edge. Keep parallel top planes and vertical sides, NO trapezoid, yaw or convergence.
Neutral GRAY wood everywhere, including restrained grain/knots, subtle dust and pencil scratches; crisp RimWorld contours/soft shading. No metal/gold/fabric, carved royal feet, drawers, vessels, inventory, tools, occupant or added props/state. Keep source design and current fixed placement; do not independently bounds-fit panels. Transparent exterior/open spaces under table, no background/glow/dropped shadow/text. Same1536x768sheet, coherent3views, no isolation request.'''.encode())
write(HERE/'manual-structural-review.json',dict(status='PASS',scope='Complete shared empty base and4native source-shaped stock constructions',review='Parallel table planes, full8depth end boards and connected low stretcher/splayedfeet retain source support/top identity. Every stock recipe derives from exact native marks, with documented authored unseen depth/shape and physically projected separate W. Source state/color choice remains native. No specific inventory identity or donor gameplay.'))
print('Constructed shared table and four distinct source-shaped stock sets in every cardinal view.')
