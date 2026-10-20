"""Neutral chemistry fixture with explicit glass/wood cut-edge ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Never overwrite logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');assert source.size==(1024,1536)
structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5));structural.save(OUT/'opaque-structure-mask.png');selected.save(OUT/'selected-edge-mask.png')
cyan=Image.new('L',source.size);cyan.putdata([255 if a>=16 and g-r>=6 and b-r>=6 and min(g,b)>=20 else 0 for r,g,b,a in source.getdata()]);near_cyan=cyan.filter(ImageFilter.MaxFilter(13));cyan.save(OUT/'cyan-ownership-seed.png')
neutral=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);ownership=Image.new('L',source.size);highlight=Image.new('L',source.size);np=[];dp=[];op=[];hp=[]
for index,(r,g,b,a) in enumerate(source.getdata()):
 x,y=index%1024,index//1024
 if a<16 or not selected.getpixel((x,y)):np.append((0,0,0,0));dp.append((0,0,0,0));op.append(0);hp.append(0);continue
 a=255 if a>=240 else a
 # Actual image has only glass above y510; the wooden rack starts below y614.
 # Pale glass highlights are almost white and cannot be recovered by hue alone.
 inherited_highlight=min(r,g,b)>=225 and max(r,g,b)-min(r,g,b)<=18 and bool(near_cyan.getpixel((x,y)))
 glass=bool(cyan.getpixel((x,y))) or y<510 or inherited_highlight
 v=max(g,b) if glass else round((r+g+b)/3)
 np.append((v,v,v,a));dp.append((v,v,v,a if glass else 0));op.append(a if glass else 0);hp.append(a if inherited_highlight else 0)
neutral.putdata(np);detail.putdata(dp);ownership.putdata(op);highlight.putdata(hp)
for name,im in [('neutral-master',neutral),('glass-neutral-master',detail),('glass-ownership-mask',ownership),('inherited-glass-highlight-mask',highlight)]:im.save(OUT/f'{name}.png')
primary=neutral.resize((256,256),Image.Resampling.LANCZOS);secondary=detail.resize((256,256),Image.Resampling.LANCZOS)
for im in [primary,secondary]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.getdata()])
primary.save(OUT/'primary-neutral.png');secondary.save(OUT/'detail-neutral.png');primary.getchannel('A').save(OUT/'coverage.png');secondary.getchannel('A').save(OUT/'detail-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,c):
 c=bytes.fromhex(c);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
native=tint(primary,palette['w']);native.alpha_composite(tint(secondary,palette['C']));native.save(OUT/'native-w-C-preview.png')
model=dict(entry='SCN-ALCHEMIST-TABLE',kind='fixed_layered_furniture',blueprint='Alchemist Table',native_tiles=['Items/sw_alchemist_table.bmp'],source=asset(HERE/'source-packet.json'),
 primary=asset(OUT/'primary-neutral.png'),detail=asset(OUT/'detail-neutral.png'),coverage=asset(OUT/'coverage.png'),detail_coverage=asset(OUT/'detail-coverage.png'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One full-cell transform for tabletop, feet, rack, phials, glass loops and masks; no independently fitted tall glass bounds.'),
 palette=dict(primary='actual native furniture foreground w',detail='actual native glass detail C',neutral_preview='Both layers are equal RGB; cyan extraction aid is removed. Glass reflections inherit glass ownership, not wood tint.'),
 state_owner='One fixed tile; child deletes inherited empty/full tile/detail tags. Do not replace this fixture with generic empty/full Table art on inventory interaction.',
 fixture_boundary='Phial rack and alembic are described source bitmap fixtures. Actual carried inventory is separate native state, not additional baked objects.',
 native_behavior='Keep actual container/inventory, cover, non-occlusion and physics. No donor crafting/drug/research behavior. Rare animated/custom states retain native fallback.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(Path(__file__).resolve())],
 alpha='Actual alpha>=224structure plus two-pixel edge allowance; keep actual alpha>=16only there. Clear invisible RGB, normalize>=240and preserve glass/leg gaps. Detached exterior glow is not object coverage.',
 glass_ownership='Cyan-dominant pixels G-R>=6,B-R>=6,min(G,B)>=20 supply the actual color seed. The exclusively-glass upper region above y510is detail-owned. Near-white reflections within six pixels of cyan inherit glass ownership; hue alone would misassign those highlights to wood.',
 cut_edge_review='Wood rack crossbars and supports stay primary-owned. Phials remain behind the rack; separate glass plate allows inspection of vial/wood crossings. Reflection ownership is explicit rather than accepting every near-white pixel as wood.',
 registration='Entire1024x1536image maps once to256square. All components share the native-source cell frame; no tall-apparatus recentering or invented rotations.',
 source_limits='Three phial marks and precise tubing joins are authored interpretation constrained by the icon and description. They are decorative fixture forms, not native inventory objects or functional chemistry simulation.',
 omitted='One source fixed-map-view fixture; no creature turnarounds, separate clothing or inherited deleted empty/full variants apply. Native integration acceptance stays deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,840),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'ALCHEMIST TABLE / source-shaped fixture / neutral wood + glass ownership / native w + C',font=font,fill='#e3cf43')
for x,im,label in [(45,primary,'Neutral / no baked cyan'),(515,secondary,'Separate neutral glass role'),(985,native,'Native w wood + C glass')]:
 big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,525),label,font=font,fill='#e3cf43')
 for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+40+i*85,580),small)
for i,line in enumerate(['Radial scorch marks, left phial rack and tall alembic retain the source identity and one shared cell frame.',
 'Glass reflections and transparent gaps stay glass-owned; wooden rack edges do not become detached cyan strokes.',
 'One fixed fixture tile: inherited empty/full variants were deleted. Real inventory/interaction stays native.',
 'No creature facings or clothing apply. Native container/state/visibility/occlusion acceptance remains pending.']):draw.text((20,680+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered neutral scorched wood and independent cyan/glass ownership in a fixed source cell.')
