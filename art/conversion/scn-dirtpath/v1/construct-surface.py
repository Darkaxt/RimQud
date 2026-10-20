"""Editable periodic stones and 8-neighbor path coverage; authoring only."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,random,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFilter,ImageFont,ImageOps
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SIDE=512;CELL=64
DISPLAY=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/Display.txt')
MAP=DISPLAY.parent/'Joppa.rpm'
palette=json.loads(DISPLAY.read_text(encoding='utf-8-sig').rstrip('\x00\r\n '))['colors']
captured=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
assert all(palette[k].lower()==captured[k].lower() for k in ['w','g','G'])
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rgb(key):return tuple(bytes.fromhex(palette[key]))
evidence=dict(recorded_at=datetime.now(timezone.utc).isoformat(),
 installed_display_sha256=sha(DISPLAY),captured_palette=dict(path='evidence/joppa-anatomy-study.json',sha256=sha(ROOT/'evidence/joppa-anatomy-study.json')),
 colors={k:palette[k] for k in ['w','W','g','G','k','K']},
 decision='Production source is neutral stone RGB plus coverage. Preview uses exact native w, g and G anchors with authored value shading. Grass preview is context only, not completion of a grass entry.',
 static_map=dict(file=str(MAP),sha256=sha(MAP),kind='Installed static Joppa layout; not a capture of the current generated/runtime zone'),
 geometry='Twenty staggered rows of twenty irregular stones on a 512-square periodic field; about six stones per logical 64-square cell. Arrangement is authored under the requested cobblestone interpretation, not native per-pixel canonical geometry.',
 neighbor_contract='Center is a path cell. Bits clockwise N=1, NE=2, E=4, SE=8, S=16, SW=32, W=64, NW=128. 256 local states, native occupancy unchanged.',
 coverage_method='Blur the 3x3 occupancy field at .16 cell radius then smoothstep .54 to .82. Crop the center cell; no per-cell material rescaling. At absent outer neighbors the edge fades inside its cell. Diagonal occupancy controls corner coverage.',
 uv_contract='One shared world-anchored repeating material, period eight logical cells in each axis. Connected masks modulate coverage only. Do not restart stone UV at every cell.',
 native_variants='All four inherited ground-dot selectors retain their identities and map to the same continuous material. Native random dot placement does not require inventing a new animation or rerolling the surface.',
 state='Construction suggestion only; material refinement/extraction and visual selection pending. Native review deferred.')
(HERE/'palette-and-surface-decisions.json').write_bytes((json.dumps(evidence,indent=2)+'\n').encode())

rng=random.Random(20640);step=SIDE/20;shapes=[];stones=[]
for row in range(20):
    for col in range(20):
        cx=(col+.5+(row%2)*.5)*step+rng.uniform(-1.5,1.5)
        cy=(row+.5)*step+rng.uniform(-1.3,1.3)
        w=step-rng.uniform(2.5,5);h=step-rng.uniform(2.5,5)
        x,y=cx-w/2,cy-h/2;r=rng.uniform(2.5,4.5)
        points=[(x+r,y),(x+w-r,y+rng.uniform(-1,1)),(x+w,y+r),
                (x+w+rng.uniform(-1,1),y+h-r),(x+w-r,y+h),
                (x+r,y+h+rng.uniform(-1,1)),(x,y+h-r),(x,y+r)]
        tone=rng.randint(174,224);stones.append(dict(id=row*20+col,points=points,tone=tone))
        for ox in [-SIDE,0,SIDE]:
            for oy in [-SIDE,0,SIDE]:
                if x+ox+w<0 or x+ox>SIDE or y+oy+h<0 or y+oy>SIDE:continue
                path='M'+' L'.join(f'{px+ox:.2f} {py+oy:.2f}' for px,py in points)+'Z'
                shapes.append(f'<path d="{path}" fill="rgb({tone},{tone},{tone})" stroke="#626262" stroke-width="1.1" stroke-linejoin="round"/>')
                shapes.append(f'<path d="M{x+r+ox:.2f} {y+1.5+oy:.2f} L{x+w-r+ox:.2f} {y+1.5+oy:.2f}" fill="none" stroke="#e1e1e1" stroke-opacity=".46" stroke-width=".9"/>')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512">'+''.join(shapes)+'</svg>'
(HERE/'constructed-stones.svg').write_bytes(svg.encode())
(HERE/'constructed-neutral.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-stones.svg'),skip_system_fonts=True))
(HERE/'stone-geometry.json').write_bytes((json.dumps(dict(period=SIDE,stones=stones),indent=2)+'\n').encode())
neutral=Image.open(HERE/'constructed-neutral.png').convert('RGBA')
neutral.getchannel('A').save(HERE/'constructed-stone-coverage.png')

NEIGHBORS=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
def coverage(mask):
    im=Image.new('L',(CELL*3,CELL*3));d=ImageDraw.Draw(im)
    d.rectangle((CELL,CELL,CELL*2-1,CELL*2-1),fill=255)
    for bit,(dx,dy) in enumerate(NEIGHBORS):
        if mask&(1<<bit):d.rectangle(((dx+1)*CELL,(dy+1)*CELL,(dx+2)*CELL-1,(dy+2)*CELL-1),fill=255)
    im=im.filter(ImageFilter.GaussianBlur(CELL*.16)).crop((CELL,CELL,CELL*2,CELL*2))
    def remap(v):
        t=max(0,min(1,(v/255-.54)/(.82-.54)));return round(255*t*t*(3-2*t))
    return im.point(remap)

MASKS=HERE/'constructed-neighbors';MASKS.mkdir(exist_ok=True)
atlas=Image.new('L',(1024,1024));records=[]
for index in range(256):
    im=coverage(index);p=MASKS/f'{index:03d}.png';im.save(p)
    atlas.paste(im,((index%16)*CELL,(index//16)*CELL))
    records.append(dict(mask=index,file=p.relative_to(HERE).as_posix(),sha256=sha(p)))
atlas.save(HERE/'constructed-neighbor-atlas.png')
(HERE/'constructed-neighbor-index.json').write_bytes((json.dumps(dict(bits=dict(zip(['N','NE','E','SE','S','SW','W','NW'],[1,2,4,8,16,32,64,128])),cell=CELL,masks=records),indent=2)+'\n').encode())

def tint_material(im):
    base=rgb('w');result=Image.new('RGBA',im.size);px=result.load();src=im.load()
    for y in range(im.height):
        for x in range(im.width):
            r,g,b,a=src[x,y];v=r/255
            px[x,y]=tuple(round(k*v) for k in base)+(a,)
    return result
colored=tint_material(neutral);colored.save(HERE/'constructed-qud-stones.png')
def grass(size):
    # Context only: smooth seeded tonal variation, not a converted grass texture.
    noise=Image.new('L',(max(3,size[0]//96+1),max(3,size[1]//96+1)))
    seed=random.Random(19146)
    noise.putdata([seed.randint(55,205) for _ in range(noise.width*noise.height)])
    noise=noise.resize(size,Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(12))
    low=tuple(round(c*.34) for c in rgb('g'))
    high=tuple(round(c*.54) for c in rgb('G'))
    return ImageOps.colorize(noise,low,high)

def material_field(size,im):
    field=Image.new('RGBA',size)
    for y in range(0,size[1],im.height):
        for x in range(0,size[0],im.width):field.paste(im,(x,y))
    return field
def draw_layout(cells,width,height,name,cell_w=CELL,cell_h=CELL,ghosts=None,title=''):
    field=material_field((width*CELL,height*CELL),colored)
    cov=Image.new('L',field.size)
    for x,y in cells:
        mask=sum(1<<bit for bit,(dx,dy) in enumerate(NEIGHBORS) if (x+dx,y+dy) in cells)
        cov.paste(coverage(mask),(x*CELL,y*CELL))
    field.putalpha(ImageChops.multiply(field.getchannel('A'),cov))
    bg=grass(field.size).convert('RGBA');bg.alpha_composite(field)
    bg=bg.resize((width*cell_w,height*cell_h),Image.Resampling.LANCZOS).convert('RGB')
    if ghosts:
        d=ImageDraw.Draw(bg)
        for x,y in ghosts:d.rectangle((x*cell_w,y*cell_h,(x+1)*cell_w-1,(y+1)*cell_h-1),fill='#19332e',outline='#31483d')
    output=Image.new('RGB',(bg.width,bg.height+74),'#142823');output.paste(bg,(0,54))
    ImageDraw.Draw(output).text((14,12),title,font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16),fill='#e3cf43')
    output.save(HERE/name)

from PIL import ImageChops
# A connected arrangement explicitly exercises a long run, two widths, bend and junction.
cells={(x,3) for x in range(1,14)}|{(x,4) for x in range(4,14)}|{(8,y) for y in range(1,9)}|{(9,y) for y in range(1,9)}|{(x,8) for x in range(9,15)}|{(2,8),(3,9),(3,8)}
draw_layout(cells,16,11,'constructed-connections-comparison.png',title='MANUAL STONES / connected fill, ends, bends, junction and diagonal neighbors')
repeated=grass((1024,1024)).convert('RGBA');repeated.alpha_composite(material_field(repeated.size,colored))
repeated.convert('RGB').save(HERE/'constructed-repeat-comparison.png')
tree=ET.parse(MAP).getroot();paths=set();ghosts=set()
for cell in tree.findall('cell'):
    xy=(int(cell.get('X')),int(cell.get('Y')));names=[o.get('Name') for o in cell.findall('object')]
    if 'DirtPath' in names:paths.add(xy)
    if any('Wall' in n for n in names):ghosts.add(xy)
draw_layout(paths,80,25,'constructed-joppa-comparison.png',16,24,ghosts,
            'STATIC JOPPA LAYOUT / path authoring only / other objects unconverted / not a game capture')
(HERE/'layout-decisions.json').write_bytes((json.dumps(dict(static_map_path_cells=len(paths),width=80,height=25,
 logical_material_cell=64,preview_cell=[16,24],walls='Context-only dark blocks from static map, not converted wall art',
 dynamic_zone='Static map differs from generated runtime zone; no current gameplay state inferred'),indent=2)+'\n').encode())
