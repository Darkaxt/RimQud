"""Extract actual refined stalks and green-role mask; preserve one cell registration."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageChops
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Never overwrite logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');assert source.size==(1024,1536)
binary=source.getchannel('A').point(lambda a:255 if a>=16 else 0);selected=Image.new('L',source.size);regions={}
for name,seed in [('left',(260,800)),('center',(500,1000)),('right',(740,900))]:
 area=binary.convert('RGB');ImageDraw.floodfill(area,seed,(255,0,0),thresh=0)
 mask=Image.new('L',source.size);mask.putdata([255 if p==(255,0,0) else 0 for p in area.getdata()]);bounds=mask.getbbox();assert bounds
 assert bounds[2]-bounds[0]<350,(name,bounds);selected=ImageChops.lighter(selected,mask);mask.save(OUT/f'source-selection-{name}.png');regions[name]=dict(seed=seed,bounds=bounds)
selected.save(OUT/'source-selection-all.png');neutral=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);green=Image.new('L',source.size)
np=[];dp=[];gp=[]
for (r,g,b,a),owned in zip(source.getdata(),selected.getdata()):
 if not owned:np.append((0,0,0,0));dp.append((0,0,0,0));gp.append(0);continue
 a=255 if a>=240 else a;is_green=g-r>=6 and g-b>=6 and g>=20
 v=min(245,round(g*1.65)) if is_green else round((r+g+b)/3)
 np.append((v,v,v,a));dp.append((v,v,v,a if is_green else 0));gp.append(a if is_green else 0)
neutral.putdata(np);detail.putdata(dp);green.putdata(gp)
neutral.save(OUT/'neutral-cleaned-master.png');detail.save(OUT/'detail-neutral-master.png');green.save(OUT/'green-ownership-mask.png')
primary=neutral.resize((256,256),Image.Resampling.LANCZOS);secondary=detail.resize((256,256),Image.Resampling.LANCZOS)
# Reapply exact equal-RGB and transparent-zero contracts after resampling.
for im in [primary,secondary]:
 im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.getdata()])
primary.save(OUT/'primary-neutral.png');secondary.save(OUT/'detail-neutral.png');primary.getchannel('A').save(OUT/'coverage.png');secondary.getchannel('A').save(OUT/'detail-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 channels=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in channels],im.getchannel('A')))
native=tint(primary,palette['w']);native.alpha_composite(tint(secondary,palette['g']));native.save(OUT/'native-w-g-preview.png')
model=dict(entry='SCN-BRINESTALK',kind='fixed_layered_plant',blueprint='Brinestalk',native_tiles=['assets_content_textures_tiles_tile-brinestalk.png'],source=asset(HERE/'source-packet.json'),
 primary=asset(OUT/'primary-neutral.png'),detail=asset(OUT/'detail-neutral.png'),coverage=asset(OUT/'coverage.png'),detail_coverage=asset(OUT/'detail-coverage.png'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='Shared full-canvas transform for the whole three-stalk object; all component positions retained. Never center separate stalk bounds or crop each stem independently.'),
 palette=dict(primary='actual native foreground w',detail='actual native detail g',neutral_preview='Equal RGB; grayscale only, including all growth regions. Native preview receives separate w/g tint; no green is baked into primary albedo.'),
 supported_states='One declared fixed map view. No random builder or native connected variants are present in the inspected object/Plant definitions.',
 native_behavior='Preserve layer3, source visibility, inherited non-solid physics and occluding=true; authored gaps do not alter occlusion. Damage/spring/plant exceptions stay native.',
 native_acceptance='Pending every-conversion-generated gate')
decisions=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(Path(__file__).resolve())],connected_selections=regions,
 alpha='Select three complete disconnected opaque components at threshold16; clear unowned/transparent RGB; normalize alpha>=240. Tool-preview exterior glow is not used as object coverage.',
 detail_ownership='Green-dominant opaque growth pixels (G-R>=6,G-B>=6,G>=20) own detail; slightly warm grayscale stalks do not. Neutralize both roles and expose saved mask. Green brightness lifted to retain shape without preserving baked hue.',
 registration='Entire1024x1536output maps once to256square recipient texture. No individual bounds fit, rotation, new roots or moving pivot.',
 source_limits='Ragged fibers are authored refinement; green growth placement follows source-constrained construction. No branch anatomy or simulation state is inferred from donor bamboo.',
 omitted_views='Fixed vegetation has no required creature turnarounds or separate equipment/clothing. No unsupported wind/growth or merged-plant state was invented.')
for name,value in [('model.json',model),('registration-decisions.json',decisions)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,790),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'BRINESTALK / extracted stalks + growth ownership / neutral and native palette / fixed cell frame',font=font,fill='#e3cf43')
for x,im,label in [(45,primary,'Selected neutral / no baked color'),(515,secondary,'Separate neutral growth layer'),(985,native,'Native w + g preview')]:
 big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,520),label,font=font,fill='#e3cf43')
 for n,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+30+85*n,570),small)
for n,line in enumerate(['Three original stalk positions and irregular heights share one source-cell transform; no independent centering.',
 'Green is extracted as a separate neutral role/mask. The neutral switch cannot leave fixed green growth pixels.',
 'Native brown w and green g are runtime tint roles, not colors copied from the bamboo reference.',
 'Fixed plant view: no creature turnarounds or clothing. Native visibility, spring and occlusion acceptance pending.']):draw.text((20,665+n*28),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
# Authored shoreline composition, using the already selected water material.
water=Image.open(ROOT/'art/conversion/tile-water-shallow/v1/registered/material-neutral.png') if (ROOT/'art/conversion/tile-water-shallow/v1/registered/material-neutral.png').exists() else None
scene=Image.new('RGBA',(768,480),'#'+palette['k'])
for x,y in [(70,40),(260,125),(465,55)]:scene.alpha_composite(native.resize((160,240),Image.Resampling.LANCZOS),(x,y))
context=Image.new('RGB',(1152,600),'#142823');context.paste(scene.convert('RGB'),(192,60));ImageDraw.Draw(context).text((20,15),'BRINESTALK AUTHORING / adjacent separate source objects / native w + g over field',font=font,fill='#e3cf43');context.save(OUT/'cluster-comparison.png')
print('Registered three stalks with neutral albedo, independent neutral green-growth role and fixed source frame.')
