"""Neutralize saved proposal and make deterministic, periodic material coverage."""
from pathlib import Path
import json,hashlib,random,xml.etree.ElementTree as ET
from PIL import Image,ImageChops,ImageDraw,ImageFilter,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
CELL=64
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
source=Image.open(HERE/'refined-patched-material.png').convert('RGBA')
a=source.getchannel('A').point(lambda v:0 if v<32 else (255 if v>=232 else v))
g=ImageOps.grayscale(source)
tile=Image.merge('RGBA',(g,g,g,a)).resize((512,512),Image.Resampling.LANCZOS)
tile.paste((0,0,0,0),mask=tile.getchannel('A').point(lambda v:255 if v==0 else 0))
tile.save(OUT/'neutral-quadrant.png')
# Reflection completes cut edge stones and guarantees compatible texture/alpha borders.
# The period doubles, while physical stone texel density is unchanged.
material=Image.new('RGBA',(1024,1024))
material.paste(tile,(0,0));material.paste(ImageOps.mirror(tile),(512,0))
material.paste(ImageOps.flip(tile),(0,512));material.paste(ImageOps.flip(ImageOps.mirror(tile)),(512,512))
material.save(OUT/'neutral-material.png')
material.getchannel('A').save(OUT/'stone-coverage.png')
decisions=dict(source='../refined-patched-material.png',source_size=list(source.size),
 cleanup='Alpha below 32 cleared; alpha >=232 normalized opaque; equal-RGB grayscale; invisible RGB cleared.',
 quadrant=[512,512],material=[1024,1024],period_in_logical_cells=[16,16],logical_cell_pixels=CELL,
 seam_patch='One square periodic field completed by exact horizontal/vertical reflection; no per-cell material fitting. Border-stone halves are paired by reflection. This can introduce mirror symmetry; review appearance at material and village scales.',
 shape_note='Generated stone shape/material proposal retained rather than misapplying the manual geometry mask to changed contours.',
 palette_source='../palette-and-surface-decisions.json',coverage_source='../constructed-neighbor-index.json',
 state='Selected neutral material and coverage; generation-ready authoring only. Runtime binding and native acceptance pending every-conversion-generated gate.')
(OUT/'registration-decisions.json').write_bytes((json.dumps(decisions,indent=2)+'\n').encode())
palette=json.loads((HERE/'palette-and-surface-decisions.json').read_text())['colors']
def rgb(k):return tuple(bytes.fromhex(palette[k]))
def tinted(im):
    g=im.getchannel('R');channels=[g.point(lambda v,k=k:round(v*k/255)) for k in rgb('w')]
    return Image.merge('RGBA',(*channels,im.getchannel('A')))
colored=tinted(material);colored.save(OUT/'qud-material-preview.png')
def grass(size):
    noise=Image.new('L',(max(3,size[0]//96+1),max(3,size[1]//96+1)));rng=random.Random(19146)
    noise.putdata([rng.randint(55,205) for _ in range(noise.width*noise.height)])
    noise=noise.resize(size,Image.Resampling.BICUBIC).filter(ImageFilter.GaussianBlur(12))
    return ImageOps.colorize(noise,tuple(round(c*.34) for c in rgb('g')),tuple(round(c*.54) for c in rgb('G')))
def field(size):
    im=Image.new('RGBA',size)
    for y in range(0,size[1],colored.height):
        for x in range(0,size[0],colored.width):im.paste(colored,(x,y))
    return im
def plate(image,title,name):
    output=Image.new('RGB',(image.width,image.height+74),'#142823');output.paste(image,(0,54))
    ImageDraw.Draw(output).text((14,12),title,font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16),fill='#e3cf43')
    output.save(OUT/name)
NEIGHBORS=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
def layout(cells,w,h,name,cell_w=64,cell_h=64,ghosts=None,title=''):
    im=field((w*CELL,h*CELL));coverage=Image.new('L',im.size)
    for x,y in cells:
        index=sum(1<<bit for bit,(dx,dy) in enumerate(NEIGHBORS) if (x+dx,y+dy) in cells)
        coverage.paste(Image.open(HERE/'constructed-neighbors'/f'{index:03d}.png'),(x*CELL,y*CELL))
    im.putalpha(ImageChops.multiply(im.getchannel('A'),coverage))
    bg=grass(im.size).convert('RGBA');bg.alpha_composite(im)
    bg=bg.resize((w*cell_w,h*cell_h),Image.Resampling.LANCZOS).convert('RGB')
    if ghosts:
        d=ImageDraw.Draw(bg)
        for x,y in ghosts:d.rectangle((x*cell_w,y*cell_h,(x+1)*cell_w-1,(y+1)*cell_h-1),fill='#19332e',outline='#31483d')
    plate(bg,title,name)
bg=grass((2048,2048)).convert('RGBA');bg.alpha_composite(field(bg.size))
plate(bg.resize((1024,1024),Image.Resampling.LANCZOS).convert('RGB'),
      'SELECTED MATERIAL / 2 x 2 periods / native brown over context green','repeat-comparison.png')
cells={(x,3) for x in range(1,14)}|{(x,4) for x in range(4,14)}|{(8,y) for y in range(1,9)}|{(9,y) for y in range(1,9)}|{(x,8) for x in range(9,15)}|{(2,8),(3,9),(3,8)}
layout(cells,16,11,'connections-comparison.png',title='SELECTED / connected surface and transparent grass interstices')
MAP=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/Joppa.rpm')
tree=ET.parse(MAP).getroot();cells=set();ghosts=set()
for cell in tree.findall('cell'):
    xy=int(cell.get('X')),int(cell.get('Y'));names=[x.get('Name') for x in cell.findall('object')]
    if 'DirtPath' in names:cells.add(xy)
    if any('Wall' in n for n in names):ghosts.add(xy)
layout(cells,80,25,'joppa-comparison.png',16,24,ghosts,
       'SELECTED STATIC JOPPA / path authoring only / context grass and walls / not gameplay')

# Keep the selected coverage source immutable; the model binds all 256 exact files.
def asset(path):
    return dict(path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest())
mask_source=json.loads((HERE/'constructed-neighbor-index.json').read_text())
model=dict(kind='connected_surface',blueprint='DirtPath',surface='cobblestone-like path over grass',
    neutral_material=asset(OUT/'neutral-material.png'),stone_coverage=asset(OUT/'stone-coverage.png'),
    material_size=[1024,1024],logical_cell_pixels=64,world_period_cells=[16,16],
    uv_policy='One world-anchored repeat. Path cells sample the same field; no per-cell material crop/fit or UV reset.',
    source_palette=dict(foreground='w',detail='w',hex=palette['w']),
    color_contract='Neutral grayscale albedo multiplied by the native brown w tint; alpha is stone coverage. This is a RimWorld-style terrain/albedo source, not a Kobold dual-color red-channel glyph mask.',
    detail_contract='Native foreground and detail are both w; no invented second pigment is needed. Grayscale supplies material value variation; grass is not baked into stone RGB.',
    coverage=dict(bits=mask_source['bits'],size=[64,64],center_occupied=True,
        masks=[dict(mask=r['mask'],**asset(HERE/r['file'])) for r in mask_source['masks']],
        atlas=asset(HERE/'constructed-neighbor-atlas.png'),
        apply='Multiply material alpha by the matching native eight-neighbor path coverage. Do not change native path/passability/visibility state.'),
    native_tile_selectors={f'Terrain/sw_ground_dots{i}.png':'neutral-material.png' for i in range(1,5)},
    variant_policy='Native selector identity is preserved; all four dot variants share the continuous surface material. No new state animation or random reroll is introduced.',
    layer='Ground surface; exact runtime binding/visibility reconciliation pending final integration',
    production_exclusions='Context grass and wall blocks in preview images are not production materials and receive no conversion credit.',
    authoring_evidence=dict(constructed='../constructed-stones.svg',refined='../refined-material-proposal.png',patched='../patched-neutral-material.png',refined_patched='../refined-patched-material.png'),
    state='Generation-ready authoring only; native acceptance pending all-conversions gate')
(OUT/'model.json').write_bytes((json.dumps(model,indent=2)+'\n').encode())

# Named cases make corner/diagonal state ownership inspectable without game tests.
cases=[('ISOLATED',0),('END / N',1),('STRAIGHT / N-S',17),('BEND / N-E',5),
       ('JUNCTION / N-E-S',21),('CROSS / cardinal',85),('DIAGONAL ONLY / NE',2),
       ('FILLED / ALL 8',255),('CONCAVE / no NE',253),('CORNER / N-NE-E',7)]
examples=Image.new('RGB',(1200,610),'#142823');d=ImageDraw.Draw(examples)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.text((16,12),'SELECTED EIGHT-NEIGHBOR COVERAGE / underlying world material is unchanged',font=font,fill='#e3cf43')
for i,(label,index) in enumerate(cases):
    x,y=(i%5)*240+24,(i//5)*285+55
    tile=colored.crop((64,64,128,128));mask=Image.open(HERE/'constructed-neighbors'/f'{index:03d}.png')
    tile.putalpha(ImageChops.multiply(tile.getchannel('A'),mask))
    bg=grass((64,64)).convert('RGBA');bg.alpha_composite(tile)
    examples.paste(bg.resize((192,192),Image.Resampling.LANCZOS).convert('RGB'),(x,y))
    d.text((x,y+204),label,font=font,fill='#e3cf43');d.text((x,y+226),f'mask {index:03d}',font=font,fill='#e5e8d8')
examples.save(OUT/'neighbor-examples-comparison.png')
