"""Register source-blue water roles, connected shores and depth blend art."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
PATH=ROOT/'art/conversion/scn-dirtpath/v1'
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGB')
g=ImageOps.grayscale(source).resize((512,512),Image.Resampling.LANCZOS)
# Keep the native b base dominant; only the original refined value field mixes B.
g=g.point(lambda v:min(210,max(0,round((v-18)*1.55))))
g.save(OUT/'ripple-quadrant.png')
ripple=Image.new('L',(1024,1024));ripple.paste(g,(0,0));ripple.paste(ImageOps.mirror(g),(512,0))
ripple.paste(ImageOps.flip(g),(0,512));ripple.paste(ImageOps.flip(ImageOps.mirror(g)),(512,512));ripple.save(OUT/'ripple-blend.png')
base=Image.new('RGBA',(1024,1024),'white');base.save(OUT/'neutral-base.png')
highlight=base.copy();highlight.putalpha(ripple);highlight.save(OUT/'neutral-ripples.png')
coverage=Image.new('L',(1024,1024),255);coverage.save(OUT/'coverage.png')
lo=bytes.fromhex(palette['b']);hi=bytes.fromhex(palette['B'])
colored=Image.merge('RGB',tuple(ripple.point(lambda v,l=l,h=h:round(l+(h-l)*v/255)) for l,h in zip(lo,hi))).convert('RGBA');colored.save(OUT/'native-color-preview.png')
index=json.loads((PATH/'constructed-neighbor-index.json').read_text())
model=dict(kind='world_liquid_surface',subject='Swimming-depth water, original native blue family',
 layers=[dict(role='native liquid base',palette_preview='b',**asset(OUT/'neutral-base.png')),dict(role='native liquid ripple/detail',palette_preview='B',**asset(OUT/'neutral-ripples.png'))],
 ripple_blend=asset(OUT/'ripple-blend.png'),coverage=asset(OUT/'coverage.png'),
 material_size=[1024,1024],logical_cell_pixels=64,world_period_cells=[16,16],
 uv_policy='One continuous world-anchored period; do not restart/crop/fit per water cell or inherit a fixed donor ramp UV meaning.',
 palette=dict(base_hex=palette['b'],ripple_hex=palette['B'],source=asset(HERE/'source-packet.json')),
 color_contract='Neutral base and ripple-alpha layers receive source-owned native liquid colors. Preview uses exact b/B. Unsupported liquid mixtures/color states retain native fallback; preview palette alone does not resolve arbitrary liquids.',
 state_selector='Actual visible eligible open water-bearing volume and native IsSwimmingDepth predicate; do not infer depth from art or change native volume.',
 boundary_coverage=dict(bits=index['bits'],size=[64,64],center_eligible=True,
  semantics='Evaluate the shared geometric masks twice with distinct predicates: any eligible wet neighbor for shore, swimming-depth neighbor for depth blend. Depth boundary is not a dry shore.',
  masks=[dict(mask=m['mask'],**asset(PATH/m['file'])) for m in index['masks']],atlas=asset(PATH/'constructed-neighbor-atlas.png')),
 compositing='Wet coverage clips all water against ground. Deep coverage blends this material over the separately authored shallow material within that wet domain; multiply by wet coverage. No white foam/cell rim.',
 orientation='Single top-down material. No creature secondary views or clothing. Native animation timing is not replaced or inferred by a static authoring plate.',
 native_state='Generation-ready art only. Existing depth capture/world UV are retained source evidence; neutral tint roles, coverage/depth blending and native acceptance remain pending every-conversion-generated gate.')
decisions=dict(source=asset(HERE/'refined-proposal.png'),source_size=list(source.size),quadrant=[512,512],material=[1024,1024],
 ripple_curve='min(210,max(0,round((luminance-18)*1.55))) after uniform resampling',
 extraction='Opaque white neutral base plus white neutral ripples with independent alpha; source colors are separate runtime-owned roles, not baked pixels.',
 seam_patch='Exact mirrored quadrant completion; possible bilateral repeat symmetry remains an authored limitation.',
 shoreline='All-wet predicate must drive the wet mask; deep predicate separately drives deep-over-shallow coverage. Both reuse the existing eight-neighbor mask geometry.',
 context_limit='Shallow entry is unfinished. Its uniform b/B high-mix stand-in in one authoring plate is labeled and receives no conversion credit.')
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
plate(field(colored,(2048,2048)).resize((1024,1024),Image.Resampling.LANCZOS),'DEEP WATER / repeated source b/B surface / exact material borders','repeat-comparison.png')
comparison=Image.new('RGB',(1200,620),'#142823');d=ImageDraw.Draw(comparison)
d.text((18,12),'DEEP WATER / neutral refined mask > registered b/B mix > single-cell scale',font=font,fill='#e3cf43')
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
plate(all_deep,'CONNECTED WATER AUTHORING / deep material across wet cells / no per-cell rims','connected-water-comparison.png')
shallow_color=tuple(round(l+(h-l)*.72) for l,h in zip(lo,hi))
depth=field(ground,size);shallow=Image.new('RGBA',size,(*shallow_color,255));shallow.putalpha(wet_mask);depth.alpha_composite(shallow)
deep_layer=field(colored,size);deep_layer.putalpha(ImageChops.multiply(deep_mask,wet_mask));depth.alpha_composite(deep_layer)
plate(depth,'DEPTH COVERAGE AUTHORING / selected deep over UNFINISHED flat shallow stand-in','depth-transition-comparison.png')
examples=Image.new('RGB',(1200,350),'#142823');d=ImageDraw.Draw(examples)
d.text((16,12),'SHARED EIGHT-NEIGHBOR SHAPES / wet or deep eligibility supplied separately',font=font,fill='#e3cf43')
for i,(label,bits) in enumerate([('ISOLATED',0),('N-S',17),('N-E',5),('FULL',255),('CONCAVE / no NE',253)]):
 im=ground.crop((0,0,64,64));layer=colored.crop((256,256,320,320));layer.putalpha(Image.open(PATH/'constructed-neighbors'/f'{bits:03d}.png'));im.alpha_composite(layer)
 examples.paste(im.resize((192,192),Image.Resampling.LANCZOS).convert('RGB'),(24+i*240,60));d.text((24+i*240,280),label,font=font,fill='#e3cf43')
examples.save(OUT/'boundary-examples-comparison.png')
