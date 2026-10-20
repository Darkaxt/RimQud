"""Register sparse neutral soil coverage; keep native pigment/background separate."""
from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops,ImageStat
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
PATH=ROOT/'art/conversion/scn-dirtpath/v1'
GROUND=ROOT/'art/conversion/tile-grassy-ground/v1/registered'
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGB')
# Numeric black background is zero pigment, not opaque black game terrain.
g=ImageOps.grayscale(source).resize((512,512),Image.Resampling.LANCZOS)
alpha=g.point(lambda v:min(255,max(0,round((v-5)*2))))
alpha.save(OUT/'coverage-quadrant.png')
coverage=Image.new('L',(1024,1024));coverage.paste(alpha,(0,0));coverage.paste(ImageOps.mirror(alpha),(512,0))
coverage.paste(ImageOps.flip(alpha),(0,512));coverage.paste(ImageOps.flip(ImageOps.mirror(alpha)),(512,512))
coverage.save(OUT/'coverage.png')
neutral=Image.new('RGBA',coverage.size,'white');neutral.putalpha(coverage);neutral.save(OUT/'neutral-material.png')
def tint(im,key):
 v=im.getchannel('R');color=bytes.fromhex(palette[key])
 return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in color],im.getchannel('A')))
soil=tint(neutral,'w')
native=Image.new('RGBA',soil.size,'#'+palette['k']);native.alpha_composite(soil);native.save(OUT/'native-color-preview.png')
index=json.loads((PATH/'constructed-neighbor-index.json').read_text())
model=dict(kind='world_ground_pigment',subject='Source-owned packed DirtFloor, fine earth rather than cobbles',
 legacy_slot='soil.png; source eligibility must replace the old broad adapter choice',
 neutral_material=asset(OUT/'neutral-material.png'),coverage=asset(OUT/'coverage.png'),
 material_size=[1024,1024],logical_cell_pixels=64,world_period_cells=[16,16],
 color_roles=dict(primary='source-owned native foreground w',detail='same native w for this DirtFloor',background='preserve source-owned native field background k, not transparent black or white'),
 palette=dict(primary_hex=palette['w'],background_hex=palette['k'],evidence=asset(HERE/'source-packet.json')),
 uv_policy='One world-anchored material repeat; no cell-local UV reset or independent per-cell crop.',
 alpha_policy='Coverage of native-brown earth pigment. Most field background remains visible; alpha is not a water-depth or collision mask.',
 source_tile_aliases=json.loads((HERE/'source-packet.json').read_text())['native_selectors'],
 alias_limit='These are installed DirtFloor RandomTileOnMove aliases. Only dots1 exact mask was exported; continuous material preserves sparse style without claiming exact unseen point layouts.',
 eligibility='Actual visible native bare packed ground. Do not select solely from non-marsh branches or overwrite paths, water, furniture, grass paint or other named floor materials.',
 boundary_coverage=dict(bits=index['bits'],size=[64,64],center_eligible=True,
  semantics='Shared geometry uses bare-soil eligibility at neighbors, not path occupancy rules.',
  masks=[dict(mask=x['mask'],**asset(PATH/x['file'])) for x in index['masks']],atlas=asset(PATH/'constructed-neighbor-atlas.png')),
 separate_layers='Native background first, packed-earth pigment coverage next, then only source-owned paint/objects. Cobble paths remain a separate material.',
 state='Generation-ready authoring only; native color/UV/eligibility/layer integration and acceptance pending the every-conversion-generated gate')
decisions=dict(source=asset(HERE/'refined-proposal.png'),source_size=list(source.size),quadrant=[512,512],material=[1024,1024],
 opacity_curve='min(255,max(0,round((luminance-5)*2))) after uniform 512-square resampling; white neutral RGB with this independent alpha',
 rationale='Remove the numeric near-black pedestal, retain subtle compressed earth and make sparse grit readable without copying solid donor brown.',
 seam_patch='Exact horizontal/vertical reflected completion; pixel borders match without smoothing a cell grid. Mirror symmetry remains an authored limitation.',
 mean_coverage=ImageStat.Stat(coverage).mean[0]/255,
 palette='Native w deposits over native k background, separate from grassy paint and cobble paving.',
 native_state='No native rendering or game test performed')
for n,o in [('model.json',model),('registration-decisions.json',decisions)]:
 (OUT/n).write_bytes((json.dumps(o,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
def plate(im,title,name):
 out=Image.new('RGB',(im.width,im.height+70),'#142823');out.paste(im.convert('RGB'),(0,50));ImageDraw.Draw(out).text((14,12),title,font=font,fill='#e3cf43');out.save(OUT/name)
def field(material,size):
 out=Image.new('RGBA',size)
 for y in range(0,size[1],material.height):
  for x in range(0,size[0],material.width):out.paste(material,(x,y))
 return out
plate(field(native,(2048,2048)).resize((1024,1024),Image.Resampling.LANCZOS),
 'SOIL / repeated native-w pigment over native-k field / no cell seams','repeat-comparison.png')
comparison=Image.new('RGB',(1440,640),'#142823');d=ImageDraw.Draw(comparison)
d.text((20,12),'PACKED EARTH / original > manual > refined coverage > registered native-color material',font=font,fill='#e3cf43')
packet=json.loads((HERE/'source-packet.json').read_text());original=Image.new('RGBA',(16,24),'#'+palette['k'])
for p in packet['native_coverage']:original.putpixel((p['x'],p['y']),(*bytes.fromhex(palette['w']),255))
for i,(label,im) in enumerate([('ORIGINAL 16x24',original),('MANUAL',Image.open(HERE/'constructed-qud-preview.png')),('REFINED COVERAGE',ImageOps.grayscale(source)),('SELECTED k + w',native)]):
 comparison.paste(im.resize((288,360 if i==0 else 288),Image.Resampling.NEAREST if i==0 else Image.Resampling.LANCZOS).convert('RGB'),(24+i*360,60))
 d.text((24+i*360,436),label,font=font,fill='#e3cf43')
 for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  # Materials show one logical cell, not an entire 16-cell period shrunk to one cell.
  cell_source=im if i==0 else im.crop((64,64,128,128))
  cell=cell_source.resize((w,h),Image.Resampling.LANCZOS).convert('RGB');comparison.paste(cell,(30+i*360+j*90,485))
 d.text((24+i*360,565),'16x24 / 24x36 / 32x48',font=font,fill='#e5e8d8')
comparison.save(OUT/'registration-comparison.png')
NEIGHBORS=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
ground=Image.open(GROUND/'native-k-preview.png').convert('RGBA')
examples=Image.new('RGB',(1200,360),'#142823');d=ImageDraw.Draw(examples)
d.text((16,12),'SHARED BOUNDARY GEOMETRY / native bare-soil eligibility / ground + soil are separate',font=font,fill='#e3cf43')
for i,(label,bits) in enumerate([('ISOLATED',0),('N-S',17),('N-E',5),('FULL',255),('CONCAVE / no NE',253)]):
 im=ground.crop((0,0,64,64));pigment=soil.crop((0,0,64,64));edge=Image.open(PATH/'constructed-neighbors'/f'{bits:03d}.png')
 pigment.putalpha(ImageChops.multiply(pigment.getchannel('A'),edge));im.alpha_composite(pigment)
 examples.paste(im.resize((192,192),Image.Resampling.LANCZOS).convert('RGB'),(24+i*240,64));d.text((24+i*240,285),label,font=font,fill='#e3cf43')
examples.save(OUT/'boundary-examples-comparison.png')
path_material=Image.open(PATH/'registered/qud-material-preview.png').convert('RGBA')
paint_paths=[ROOT/'art/conversion/tile-grass-1/v1/registered-v2/grass1-neutral.png']+[ROOT/f'art/conversion/tile-grass-{i}/v1/registered/grass{i}-neutral.png' for i in [2,3]]
paints=[tint(Image.open(p).convert('RGBA'),'g') for p in paint_paths]
def layout(soil_cells,path_cells,width,height,name,cell_w=64,cell_h=64,walls=None,title=''):
 size=(width*64,height*64);im=field(ground,size)
 for cells,material in [(soil_cells,soil),(path_cells,path_material)]:
  layer=field(material,size);mask=Image.new('L',size)
  for x,y in cells:
   bits=sum(1<<b for b,(dx,dy) in enumerate(NEIGHBORS) if (x+dx,y+dy) in cells)
   mask.paste(Image.open(PATH/'constructed-neighbors'/f'{bits:03d}.png'),(x*64,y*64))
  layer.putalpha(ImageChops.multiply(layer.getchannel('A'),mask));im.alpha_composite(layer)
 for y in range(height):
  for x in range(width):
   if (x,y) not in soil_cells|path_cells and (x*3+y*5)%5==0:
    im.alpha_composite(paints[(x+y)%3].resize((64,96),Image.Resampling.LANCZOS),(x*64,y*64-20))
 im=im.resize((width*cell_w,height*cell_h),Image.Resampling.LANCZOS)
 if walls:
  dr=ImageDraw.Draw(im)
  for x,y in walls:dr.rectangle((x*cell_w,y*cell_h,(x+1)*cell_w-1,(y+1)*cell_h-1),fill='#19332e',outline='#31483d')
 plate(im,title,name)
soil_cells={(x,y) for x in range(2,7) for y in range(2,8)}|{(x,y) for x in range(10,15) for y in range(3,7)}
paths={(x,9) for x in range(16)}|{(8,y) for y in range(10)}
layout(soil_cells,paths,16,11,'soil-ground-path-comparison.png',title='AUTHORING / native-k field + bare packed earth + cobbles + separate grass paint')
tree=ET.parse('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/Joppa.rpm').getroot()
soils=set();paths=set();walls=set()
for c in tree.findall('cell'):
 xy=int(c.get('X')),int(c.get('Y'));names=[o.get('Name') for o in c.findall('object')]
 if 'DirtFloor' in names:soils.add(xy)
 if 'DirtPath' in names:paths.add(xy)
 if any('Wall' in n for n in names):walls.add(xy)
layout(soils-paths,paths,80,25,'static-joppa-authoring-comparison.png',16,24,walls,
 title='STATIC JOPPA AUTHORING / native floor/path placement / walls and paint distribution are context')
