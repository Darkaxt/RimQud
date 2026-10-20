"""Register shallow-water roles and compose the selected shallow/deep art."""
from pathlib import Path
import hashlib,json,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
PATH=ROOT/'art/conversion/scn-dirtpath/v1'
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGB')
g=ImageOps.grayscale(source).resize((512,512),Image.Resampling.LANCZOS)
# Shallower authored reflectance uses more native B and finer wavelets than deep.
g=g.point(lambda v:min(235,max(80,round(v*.9+40))))
g.save(OUT/'ripple-quadrant.png')
ripple=Image.new('L',(1024,1024));ripple.paste(g,(0,0));ripple.paste(ImageOps.mirror(g),(512,0))
ripple.paste(ImageOps.flip(g),(0,512));ripple.paste(ImageOps.flip(ImageOps.mirror(g)),(512,512));ripple.save(OUT/'ripple-blend.png')
base=Image.new('RGBA',(1024,1024),'white');base.save(OUT/'neutral-base.png')
highlight=base.copy();highlight.putalpha(ripple);highlight.save(OUT/'neutral-ripples.png')
coverage=Image.new('L',(1024,1024),255);coverage.save(OUT/'coverage.png')
lo=bytes.fromhex(palette['b']);hi=bytes.fromhex(palette['B'])
colored=Image.merge('RGB',tuple(ripple.point(lambda v,l=l,h=h:round(l+(h-l)*v/255)) for l,h in zip(lo,hi))).convert('RGBA');colored.save(OUT/'native-color-preview.png')
index=json.loads((PATH/'constructed-neighbor-index.json').read_text())
model=dict(kind='world_liquid_surface',subject='Shallow/wading water, original native blue family',
 layers=[dict(role='native liquid base',palette_preview='b',**asset(OUT/'neutral-base.png')),dict(role='native liquid ripple/detail',palette_preview='B',**asset(OUT/'neutral-ripples.png'))],
 ripple_blend=asset(OUT/'ripple-blend.png'),coverage=asset(OUT/'coverage.png'),
 material_size=[1024,1024],logical_cell_pixels=64,world_period_cells=[16,16],
 uv_policy='One continuous world-anchored period; do not restart/crop/fit per water cell or inherit a fixed donor ramp UV meaning.',
 palette=dict(base_hex=palette['b'],ripple_hex=palette['B'],source=asset(HERE/'source-packet.json')),
 color_contract='Neutral base and ripple-alpha layers receive source-owned native liquid colors. Preview uses exact b/B. Unsupported liquid mixtures/color states retain native fallback; preview palette alone does not resolve arbitrary liquids.',
 state_selector='Actual visible eligible open water-bearing volume below native swimming depth; keep native thin-puddle/wading distinctions. Shallow material also supplies only the underlying blend field beneath deep art; never change volume or traversability.',
 boundary_coverage=dict(bits=index['bits'],size=[64,64],center_eligible=True,
  semantics='Evaluate the shared geometric masks twice with distinct predicates: any eligible wet neighbor for shore, swimming-depth neighbor for depth blend. Depth boundary is not a dry shore.',
  masks=[dict(mask=m['mask'],**asset(PATH/m['file'])) for m in index['masks']],atlas=asset(PATH/'constructed-neighbor-atlas.png')),
 compositing='Wet coverage clips this shallow base against ground. Selected deep material overlays it using swimming-neighbor coverage multiplied by wet coverage. Shoreline and depth boundary remain independent; no foam or per-cell rim.',
 orientation='Single top-down material. No creature secondary views or clothing. Native animation timing is not replaced or inferred by a static authoring plate.',
 native_state='Generation-ready art only. Existing depth capture/world UV are retained source evidence; neutral tint roles, coverage/depth blending and native acceptance remain pending every-conversion-generated gate.')
model['paired_deep_model']=asset(ROOT/'art/conversion/tile-water-deep/v1/registered/model.json')
decisions=dict(source=asset(HERE/'refined-proposal.png'),source_size=list(source.size),quadrant=[512,512],material=[1024,1024],
 ripple_curve='min(235,max(80,round(luminance*.9+40))) after uniform resampling',
 extraction='Opaque white neutral base plus white neutral ripples with independent alpha; source colors are separate runtime-owned roles, not baked pixels.',
 seam_patch='Exact mirrored quadrant completion; possible bilateral repeat symmetry remains an authored limitation.',
 shoreline='All-wet predicate must drive the wet mask; deep predicate separately drives deep-over-shallow coverage. Both reuse the existing eight-neighbor mask geometry.',
 paired_material='Uses the already selected deep-water native-color authoring preview with its exact model provenance; does not regenerate or modify deep art.')
for n,o in [('model.json',model),('registration-decisions.json',decisions)]:
 (OUT/n).write_bytes((json.dumps(o,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
def plate(im,title,name):
 out=Image.new('RGB',(im.width,im.height+70),'#142823');out.paste(im.convert('RGB'),(0,50));ImageDraw.Draw(out).text((14,12),title,font=font,fill='#e3cf43');out.save(OUT/name)
def field(im,size):
 out=Image.new('RGBA',size)
 for y in range(0,size[1],im.height):
  for x in range(0,size[0],im.width):out.paste(im,(x,y))
 return out
plate(field(colored,(2048,2048)).resize((1024,1024),Image.Resampling.LANCZOS),'SHALLOW WATER / repeated source b/B surface / exact material borders','repeat-comparison.png')
comparison=Image.new('RGB',(1200,620),'#142823');d=ImageDraw.Draw(comparison)
d.text((18,12),'SHALLOW / neutral refined mask > registered b/B mix > single-cell scale',font=font,fill='#e3cf43')
for i,(title,im) in enumerate([('REFINED GRAYSCALE',ImageOps.grayscale(source)),('REGISTERED b/B',colored),('ONE LOGICAL CELL',colored.crop((256,256,320,320)))]):
 comparison.paste(im.resize((320,320),Image.Resampling.LANCZOS).convert('RGB'),(24+i*400,65));d.text((24+i*400,420),title,font=font,fill='#e5e8d8')
 cell=colored.crop((256,256,320,320))
 for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):comparison.paste(cell.resize((w,h),Image.Resampling.LANCZOS).convert('RGB'),(34+i*400+j*90,478))
 d.text((24+i*400,555),'16x24 / 24x36 / 32x48',font=font,fill='#e5e8d8')
comparison.save(OUT/'registration-comparison.png')
NEIGHBORS=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
def masks(cells,size):
 out=Image.new('L',size)
 for x,y in cells:
  bits=sum(1<<b for b,(dx,dy) in enumerate(NEIGHBORS) if (x+dx,y+dy) in cells)
  out.paste(Image.open(PATH/'constructed-neighbors'/f'{bits:03d}.png'),(x*64,y*64))
 return out
wet={(x,y) for y in range(1,10) for x in range(1,15) if ((x-7.5)/7)**2+((y-5)/4.5)**2<1}|{(1,5),(14,5)}
deep={(x,y) for x,y in wet if ((x-7.5)/4.0)**2+((y-5)/2.7)**2<1}
size=(16*64,11*64);ground=Image.open(ROOT/'art/conversion/tile-grassy-ground/v1/registered/native-k-preview.png').convert('RGBA')
wet_mask=masks(wet,size);deep_mask=masks(deep,size)
all_deep=field(ground,size);water=field(colored,size);water.putalpha(wet_mask);all_deep.alpha_composite(water)
plate(all_deep,'CONNECTED SHALLOW AUTHORING / selected shallow across wet cells / no cell rims','connected-water-comparison.png')
deep_selected=Image.open(ROOT/'art/conversion/tile-water-deep/v1/registered/native-color-preview.png').convert('RGBA')
depth=field(ground,size);shallow=field(colored,size);shallow.putalpha(wet_mask);depth.alpha_composite(shallow)
deep_layer=field(deep_selected,size);deep_layer.putalpha(ImageChops.multiply(deep_mask,wet_mask));depth.alpha_composite(deep_layer)
plate(depth,'SELECTED WATER AUTHORING / separate shallow + deep materials / independent wet/deep coverage','depth-transition-comparison.png')
examples=Image.new('RGB',(1200,350),'#142823');d=ImageDraw.Draw(examples)
d.text((16,12),'SHARED EIGHT-NEIGHBOR SHAPES / wet or deep eligibility supplied separately',font=font,fill='#e3cf43')
for i,(label,bits) in enumerate([('ISOLATED',0),('N-S',17),('N-E',5),('FULL',255),('CONCAVE / no NE',253)]):
 im=ground.crop((0,0,64,64));layer=colored.crop((256,256,320,320));layer.putalpha(Image.open(PATH/'constructed-neighbors'/f'{bits:03d}.png'));im.alpha_composite(layer)
 examples.paste(im.resize((192,192),Image.Resampling.LANCZOS).convert('RGB'),(24+i*240,60));d.text((24+i*240,280),label,font=font,fill='#e3cf43')
examples.save(OUT/'boundary-examples-comparison.png')

# Contextual side-by-side family view, preserving both independently selected resources.
family=Image.new('RGB',(1280,570),'#142823');dr=ImageDraw.Draw(family)
dr.text((16,12),'WATER FAMILY / two separate authored materials / same native b/B color roles',font=font,fill='#e3cf43')
for i,(label,im) in enumerate([('SHALLOW / fine brighter wavelets',colored),('DEEP / calm darker flowing surface',deep_selected)]):
 family.paste(im.resize((584,400),Image.Resampling.LANCZOS).convert('RGB'),(24+i*640,60));dr.text((24+i*640,488),label,font=font,fill='#e5e8d8')
family.save(OUT/'family-comparison.png')

# Static authored map identifies actual Pond placements, not runtime liquid spreading.
tree=ET.parse('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/Joppa.rpm').getroot()
ponds=set();walls=set();paths=set()
for c in tree.findall('cell'):
 xy=int(c.get('X')),int(c.get('Y'));names=[o.get('Name') for o in c.findall('object')]
 if 'Pond' in names:ponds.add(xy)
 if 'DirtPath' in names:paths.add(xy)
 if any('Wall' in n for n in names):walls.add(xy)
size=(80*64,25*64);static=field(ground,size)
road=field(Image.open(PATH/'registered/qud-material-preview.png').convert('RGBA'),size);road.putalpha(ImageChops.multiply(road.getchannel('A'),masks(paths,size)));static.alpha_composite(road)
water=field(colored,size);water.putalpha(masks(ponds,size));static.alpha_composite(water)
static=static.resize((1280,600),Image.Resampling.LANCZOS);dr=ImageDraw.Draw(static)
for x,y in walls:dr.rectangle((x*16,y*24,(x+1)*16-1,(y+1)*24-1),fill='#19332e',outline='#31483d')
plate(static,'STATIC JOPPA AUTHORING / declared Pond/path cells / wall blocks are context / no runtime spreading claim','static-joppa-authoring-comparison.png')
