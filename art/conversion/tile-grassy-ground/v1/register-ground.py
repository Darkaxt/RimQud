"""Register opaque neutral substrate and compose source-owned material layers."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
PATH=ROOT/'art/conversion/scn-dirtpath/v1'
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
source=Image.open(HERE/'refined-proposal.png').convert('RGB')
# Normalize the authored material value while retaining its low-relief detail.
g=ImageOps.grayscale(source).point(lambda v:min(255,round(v*.65+89))).resize((512,512),Image.Resampling.LANCZOS)
tile=Image.merge('RGBA',(g,g,g,Image.new('L',g.size,255)));tile.save(OUT/'neutral-quadrant.png')
material=Image.new('RGBA',(1024,1024));material.paste(tile,(0,0));material.paste(ImageOps.mirror(tile),(512,0))
material.paste(ImageOps.flip(tile),(0,512));material.paste(ImageOps.flip(ImageOps.mirror(tile)),(512,512))
material.save(OUT/'neutral-material.png');material.getchannel('A').save(OUT/'coverage.png')
def tint(im,key):
    color=bytes.fromhex(palette[key]);g=im.getchannel('R')
    return Image.merge('RGBA',(*[g.point(lambda v,c=c:round(v*c/255)) for c in color],im.getchannel('A')))
colored=tint(material,'k');colored.save(OUT/'native-k-preview.png')
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
mask_index=json.loads((PATH/'constructed-neighbor-index.json').read_text())
paint_paths=[ROOT/'art/conversion/tile-grass-1/v1/registered-v2/grass1-neutral.png']+[ROOT/f'art/conversion/tile-grass-{i}/v1/registered/grass{i}-neutral.png' for i in [2,3]]
paints=[tint(Image.open(p).convert('RGBA'),'g') for p in paint_paths]
model=dict(kind='world_ground_surface',subject='Source-bound grassy-field substrate',
 legacy_slot='marsh.png; historical adapter name, not a universal wet-terrain blueprint',
 neutral_material=asset(OUT/'neutral-material.png'),coverage=asset(OUT/'coverage.png'),
 material_size=[1024,1024],logical_cell_pixels=64,world_period_cells=[16,16],
 uv_policy='One world-anchored material repeat; no quad-local UV reset or independent per-cell fitting.',
 color_role='Source-owned native field background; preview is Qud k #'+palette['k'],
 palette=dict(role='k',hex=palette['k'],evidence=asset(HERE/'source-packet.json')),
 albedo_contract='Neutral near-white equal-RGB albedo, opaque within selected ground coverage, multiplied by actual native field-background tint. Do not use Color.white on neutral art as the final source-color binding.',
 paint_layers=[asset(p) for p in paint_paths],
 separation='Grass paint stays in separate primary-tinted source-cell layers; path, water and bare soil retain their own source/visibility roles. No discrete shoots or liquid is baked into this base.',
 eligibility='Visible source-owned grassy-field ground. Exact current-capture rule/tint/draw-order binding must be reconciled in final integration; do not blindly apply to every broad ground/tree/reed/water or indoor cell merely because the old adapter selected marsh.png there.',
 boundary_coverage=dict(bits=mask_index['bits'],size=[64,64],center_eligible=True,
    semantics='Use native eligibility for this ground material at neighbors; these are shared geometric masks, not DirtPath occupancy rules.',
    masks=[dict(mask=r['mask'],**asset(PATH/r['file'])) for r in mask_index['masks']],
    atlas=asset(PATH/'constructed-neighbor-atlas.png')),
 state='Generation-ready material authoring only; runtime tint/world-UV/eligibility/layer binding and native acceptance pending the every-conversion-generated gate')
decisions=dict(source='../refined-proposal.png',source_size=list(source.size),
 cleanup='Equal-RGB grayscale; value mapping min(255,.65*v+89); complete opaque ground coverage.',
 quadrant=[512,512],material=[1024,1024],period_cells=[16,16],
 seam_patch='Exact horizontal/vertical reflected completion at unchanged grain texel scale. This guarantees compatible discrete material borders; possible mirror symmetry is an authored limit.',
 palette='Native captured dominant field k, rather than the earlier temporary saturated-green context fill.',
 state='Selected art; no renderer/game mutation or native test.')
for name,obj in [('model.json',model),('registration-decisions.json',decisions)]:
    (OUT/name).write_bytes((json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
def plate(im,title,name):
    out=Image.new('RGB',(im.width,im.height+74),'#142823');out.paste(im.convert('RGB'),(0,54))
    ImageDraw.Draw(out).text((14,12),title,font=font,fill='#e3cf43');out.save(OUT/name)
def field(size):
    im=Image.new('RGBA',size)
    for y in range(0,size[1],1024):
        for x in range(0,size[0],1024):im.paste(colored,(x,y))
    return im
plate(field((2048,2048)).resize((1024,1024),Image.Resampling.LANCZOS),
      'SELECTED / 2 x 2 material periods / native dark-teal field k / no paint baked in','repeat-comparison.png')
NEIGHBORS=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
path_material=Image.open(PATH/'registered/qud-material-preview.png').convert('RGBA')
def layout(cells,width,height,name,cell_w=64,cell_h=64,ghosts=None,title=''):
    im=field((width*64,height*64))
    paths=Image.new('RGBA',im.size)
    for y in range(0,im.height,1024):
        for x in range(0,im.width,1024):paths.paste(path_material,(x,y))
    coverage=Image.new('L',im.size)
    for x,y in cells:
        bits=sum(1<<bit for bit,(dx,dy) in enumerate(NEIGHBORS) if (x+dx,y+dy) in cells)
        coverage.paste(Image.open(PATH/'constructed-neighbors'/f'{bits:03d}.png'),(x*64,y*64))
    paths.putalpha(ImageChops.multiply(paths.getchannel('A'),coverage));im.alpha_composite(paths)
    for row in range(height):
        for col in range(width):
            if (col,row) not in cells and (row*5+col*3)%4==0:
                sprite=paints[(row+col)%3].resize((64,96),Image.Resampling.LANCZOS)
                im.alpha_composite(sprite,(col*64,row*64-20))
    im=im.resize((width*cell_w,height*cell_h),Image.Resampling.LANCZOS)
    if ghosts:
        d=ImageDraw.Draw(im)
        for x,y in ghosts:d.rectangle((x*cell_w,y*cell_h,(x+1)*cell_w-1,(y+1)*cell_h-1),fill='#19332e',outline='#31483d')
    plate(im,title,name)
cells={(x,3) for x in range(1,14)}|{(x,4) for x in range(4,14)}|{(8,y) for y in range(1,9)}|{(9,y) for y in range(1,9)}|{(x,8) for x in range(9,15)}|{(2,8),(3,9),(3,8)}
layout(cells,16,11,'material-paint-path-comparison.png',title='AUTHORING / native-k substrate + three separate paints + selected stone path')
tree=ET.parse('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/Joppa.rpm').getroot();paths=set();walls=set()
for cell in tree.findall('cell'):
    xy=int(cell.get('X')),int(cell.get('Y'));names=[x.get('Name') for x in cell.findall('object')]
    if 'DirtPath' in names:paths.add(xy)
    if any('Wall' in n for n in names):walls.add(xy)
layout(paths,80,25,'static-joppa-authoring-comparison.png',16,24,walls,
       title='STATIC JOPPA AUTHORING / selected ground/path/paint / wall blocks and paint distribution are context')
examples=Image.new('RGB',(1200,370),'#142823');d=ImageDraw.Draw(examples)
d.text((16,12),'SHARED COVERAGE SHAPES / ground eligibility semantics / soil-color context is unfinished',font=font,fill='#e3cf43')
for i,(label,bits) in enumerate([('ISOLATED',0),('EDGE / N-S',17),('BEND / N-E',5),('FULL',255),('CONCAVE / no NE',253)]):
    im=colored.crop((64,64,128,128));im.putalpha(Image.open(PATH/'constructed-neighbors'/f'{bits:03d}.png'))
    bg=Image.new('RGBA',im.size,'#62573e');bg.alpha_composite(im);x=24+i*240
    examples.paste(bg.resize((192,192),Image.Resampling.LANCZOS).convert('RGB'),(x,65));d.text((x,280),label,font=font,fill='#e3cf43')
examples.save(OUT/'boundary-examples-comparison.png')
