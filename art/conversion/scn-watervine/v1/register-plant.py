"""Neutral three-layout watervine with native ripe/unripe wafer tint ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Never overwrite logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];packet=json.loads((HERE/'source-packet.json').read_text());states=[];decisions=[];previews={}
def tint(im,c):
 c=bytes.fromhex(c);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
for n in [1,2,3]:
 source=Image.open(HERE/f'refined-variant-{n}.png').convert('RGBA');assert source.size==(1024,1536)
 structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selection=structural.filter(ImageFilter.MaxFilter(5));structural.save(OUT/f'variant-{n}-opaque-structure-mask.png');selection.save(OUT/f'variant-{n}-selected-edge-mask.png')
 neutral=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);growth=Image.new('L',source.size);np=[];dp=[];gp=[];opaque_growth=set()
 for index,(r,g,b,a) in enumerate(source.getdata()):
  if a<16 or not selection.getpixel((index%1024,index//1024)):np.append((0,0,0,0));dp.append((0,0,0,0));gp.append(0);continue
  a=255 if a>=240 else a;green=g-r>=6 and g-b>=6 and g>=20;v=min(245,round(g*1.65)) if green else round((r+g+b)/3)
  np.append((v,v,v,a));dp.append((v,v,v,a if green else 0));gp.append(a if green else 0)
  if green and a>=224:opaque_growth.add((index%1024,index//1024))
 groups=[]
 while opaque_growth:
  q=opaque_growth.pop();group={q};todo=[q]
  while todo:
   x,y=todo.pop()
   for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
    p=(x+dx,y+dy)
    if p in opaque_growth:opaque_growth.remove(p);group.add(p);todo.append(p)
  if len(group)>=40:groups.append(dict(pixels=len(group),bounds=[min(x for x,y in group),min(y for x,y in group),max(x for x,y in group)+1,max(y for x,y in group)+1]))
 neutral.putdata(np);detail.putdata(dp);growth.putdata(gp)
 for name,im in [('neutral-master',neutral),('wafer-neutral-master',detail),('wafer-ownership-mask',growth)]:im.save(OUT/f'variant-{n}-{name}.png')
 primary=neutral.resize((256,256),Image.Resampling.LANCZOS);secondary=detail.resize((256,256),Image.Resampling.LANCZOS)
 for im in [primary,secondary]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.getdata()])
 primary.save(OUT/f'variant-{n}-primary-neutral.png');secondary.save(OUT/f'variant-{n}-detail-neutral.png');primary.getchannel('A').save(OUT/f'variant-{n}-coverage.png');secondary.getchannel('A').save(OUT/f'variant-{n}-detail-coverage.png')
 previews[n]=dict(neutral=primary,detail=secondary)
 for state,color in [('ripe','g'),('unripe','K')]:
  native=tint(primary,palette['w']);native.alpha_composite(tint(secondary,palette[color]));native.save(OUT/f'variant-{n}-{state}-native-preview.png');previews[n][state]=native
 states.append(dict(variant=n,native_tile=packet['layouts'][n-1]['native_tile'],primary=asset(OUT/f'variant-{n}-primary-neutral.png'),detail=asset(OUT/f'variant-{n}-detail-neutral.png'),coverage=asset(OUT/f'variant-{n}-coverage.png'),detail_coverage=asset(OUT/f'variant-{n}-detail-coverage.png')))
 decisions.append(dict(variant=n,input=asset(HERE/f'refined-variant-{n}.png'),source_wafer_glyph_groups=len(packet['layouts'][n-1]['wafer_marks']),refined_opaque_wafer_components=sorted(groups,key=lambda x:(x['bounds'][1],x['bounds'][0])),registration='Shared full1024x1536image frame to256square; no independent component/variant bounding-box fit.'))
model=dict(entry='SCN-WATERVINE',kind='harvest_tinted_plant_variants',blueprint='Watervine',source=asset(HERE/'source-packet.json'),states=states,
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='All three source-inspired layouts use the same full-cell coordinate transform. Within each variant, ripe/unripe shares exactly the same layers and anchor.'),
 palette=dict(primary='actual native TileColor w',detail='actual native DetailColor: g when ripe, K when unripe',neutral_preview='Equal RGB in both saved layers; green extraction aid removed from neutral albedo.'),
 harvest_states=dict(ripe=dict(primary='w',detail='g'),unripe=dict(primary='w',detail='K')),
 state_owner='Native RandomTile chooses one of three layouts; native Harvestable owns ripeness, yield1 and regeneration. No new vine-merging, growth or state machine.',
 native_effects='Keep Fireflies.BeforeRenderEvent and its native night particle separately; no firefly/glow is baked into plant material.',
 appearance='Crooked furrowed salt-bearing vines with small thick moisture-swollen wafer knots instead of leaf sprays. Donor HaygrassA only informs narrow-stroke rendering.',
 native_behavior='Preserve inherited non-solid plant physics, non-occluding Render, LiquidNative water, harvest interaction and original particles. Native binding/state/visibility acceptance remains pending.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(Path(__file__).resolve())],variants=decisions,
 alpha='Keep alpha>=224structural art plus a two-pixel edge allowance, retaining actual alpha>=16only there. This removes detached soft exterior glow but preserves antialiased contours and true vine gaps.',
 wafer_ownership='Green-dominant opaque pixels G-R>=6,G-B>=6,G>=20 own swollen-wafer detail. Neutralize both primary and wafer layers; lift green-role neutral luminance without preserving its hue.',
 counts='Record actual opaque wafer components as authoring evidence; tiny glyph connected groups are visual interpretation, not a mechanical count or harvest yield. Compare intended layouts and note any refinement mismatch explicitly.',
 omitted_views='Fixed vegetation does not require creature turnarounds or clothing. Three actual layout variants and both native harvest tint states are shown.',
 native_limit='No game/harness run occurred. Source particle/harvest/render state behavior remains native and final integrated acceptance is deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
plate=Image.new('RGB',(1440,1510),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'WATERVINE / three source layouts / neutral and ripe w+g / identical geometry for unripe w+K',font=font,fill='#e3cf43')
for n in [1,2,3]:
 x=40+(n-1)*470
 for y,state,label in [(65,'neutral','Neutral / no baked green'),(705,'ripe','Ripe / native w + g')]:
  im=previews[n][state];big=im.resize((320,480),Image.Resampling.LANCZOS);plate.paste(big,(x,y),big);draw.text((x,y+500),f'Variant{n} / '+label,font=font,fill='#e3cf43')
  for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
   small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+50+i*90,y+550),small)
for i,line in enumerate(['Three native RandomTile layouts retain crooked vines and swollen wafer knots, not ordinary leaf/cereal heads.',
 'Vine stays native w; wafer detail changes g/K. Each variant uses unchanged geometry/anchor for harvest tints.',
 'Neutral images are grayscale. Native night fireflies remain independent particles; no glow is baked into these sprites.']):draw.text((20,1385+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
plate=Image.new('RGB',(1440,780),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'WATERVINE / actual unripe w + K / same three layouts and wafer masks',font=font,fill='#e3cf43')
for n in [1,2,3]:
 x=50+(n-1)*470;im=previews[n]['unripe'];big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,520),f'Variant{n} / unripe native w + K',font=font,fill='#e5e8d8')
draw.text((20,610),'Native Harvestable changes detail tint; it does not remove wafers, replace the tile or move the root positions.',font=font,fill='#e5e8d8');draw.text((20,650),'Yield remains one Vinewafer. Native interaction/state/visibility/particles acceptance remains pending.',font=font,fill='#e5e8d8');plate.save(OUT/'unripe-comparison.png')
print('Registered three watervine variants. Source and refined wafer components:',[(x['source_wafer_glyph_groups'],len(x['refined_opaque_wafer_components'])) for x in decisions])
