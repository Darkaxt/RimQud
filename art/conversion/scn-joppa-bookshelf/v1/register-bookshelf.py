"""Neutral sparse bookshelf layouts with whole-spine ownership and native empty tint."""
from pathlib import Path
from collections import deque
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def hull(points):
 pts=sorted(set(points))
 def cross(o,a,b):return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
 lower=[]
 for p in pts:
  while len(lower)>=2 and cross(lower[-2],lower[-1],p)<=0:lower.pop()
  lower.append(p)
 upper=[]
 for p in reversed(pts):
  while len(upper)>=2 and cross(upper[-2],upper[-1],p)<=0:upper.pop()
  upper.append(p)
 return lower[:-1]+upper[:-1]
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
variants=[];decisions=[];previews=[];isolated=[]
for n,expected in [(1,12),(2,10),(3,7)]:
 source=Image.open(HERE/f'refined-variant-{n}.png').convert('RGBA');assert source.size==(1024,1536)
 structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5));structural.save(OUT/f'variant-{n}-opaque-structure-mask.png');selected.save(OUT/f'variant-{n}-selected-edge-mask.png')
 points={(i%1024,i//1024) for i,(r,g,b,a) in enumerate(source.get_flattened_data()) if a>=224 and r-b>=10 and g-b>=10}
 seed=Image.new('L',source.size);seed.putdata([255 if (x,y) in points else 0 for y in range(1536) for x in range(1024)]);seed.save(OUT/f'variant-{n}-gold-seed.png');groups=[]
 while points:
  first=points.pop();q=deque([first]);group=[first]
  while q:
   x,y=q.popleft()
   for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in points:points.remove(p);q.append(p);group.append(p)
  if len(group)>300:groups.append(group)
 assert len(groups)==expected,(n,len(groups),expected)
 owner=Image.new('L',source.size);draw=ImageDraw.Draw(owner);surfaces=[]
 for group in groups:
  polygon=hull(group);draw.polygon(polygon,fill=255);xs=[p[0] for p in group];ys=[p[1] for p in group];surfaces.append(dict(opaque_gold_pixels=len(group),bounds=[min(xs),min(ys),max(xs)+1,max(ys)+1],ownership_hull=polygon))
 owner.save(OUT/f'variant-{n}-spine-ownership-mask.png')
 primary=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);pp=[];dp=[]
 for (r,g,b,a),edge,owns in zip(source.get_flattened_data(),selected.get_flattened_data(),owner.get_flattened_data()):
  if a<16 or not edge:pp.append((0,0,0,0));dp.append((0,0,0,0));continue
  a=255 if a>=240 else a;v=max(r,g) if owns else round((r+g+b)/3);pp.append((v,v,v,a));dp.append((v,v,v,a if owns else 0))
 primary.putdata(pp);detail.putdata(dp);primary.save(OUT/f'variant-{n}-neutral-master.png');detail.save(OUT/f'variant-{n}-spine-neutral-master.png')
 primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS)
 for im in [primary,detail]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.get_flattened_data()])
 primary.save(OUT/f'variant-{n}-primary-neutral.png');detail.save(OUT/f'variant-{n}-detail-neutral.png');primary.getchannel('A').save(OUT/f'variant-{n}-coverage.png');detail.getchannel('A').save(OUT/f'variant-{n}-detail-coverage.png')
 stocked=tint(primary,palette['w']);stocked.alpha_composite(tint(detail,palette['W']));stocked.save(OUT/f'variant-{n}-stocked-w-W-preview.png')
 empty=tint(primary,palette['w']);empty.alpha_composite(tint(detail,palette['k']));empty.save(OUT/f'variant-{n}-empty-w-k-preview.png')
 variants.append(dict(variant=n,native_tile=f'Items/sw_bookshelf{n}.bmp',primary=asset(OUT/f'variant-{n}-primary-neutral.png'),detail=asset(OUT/f'variant-{n}-detail-neutral.png'),coverage=asset(OUT/f'variant-{n}-coverage.png'),detail_coverage=asset(OUT/f'variant-{n}-detail-coverage.png')))
 decisions.append(dict(variant=n,input=asset(HERE/f'refined-variant-{n}.png'),actual_spine_surfaces=sorted(surfaces,key=lambda s:(s['bounds'][1],s['bounds'][0])),ownership='Each substantial opaque-gold component supplies its own actual convex spine surface. Fill interior achromatic seams/highlight bands with the same detail ownership, preserving leaning shape rather than assigning gray bands to wood. No geometry is moved or fitted.'))
 previews.append((primary,stocked,empty));isolated.append(detail)
model=dict(entry='SCN-JOPPA-BOOKSHELF',kind='inventory_tinted_furniture_variants',blueprint='Joppa Bookshelf',source=asset(HERE/'source-packet.json'),variants=variants,
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='Each entire1024x1536layout maps once to256square for frame and every spine mask. No independent book/shelf/layout bbox centering.'),
 palette=dict(primary='actual native wooden frame w',stocked_detail='actual native FullDetailColor W',empty_detail='actual native EmptyDetailColor k',neutral_preview='All production layers are equal-RGB neutral. Achromatic bands inside spines stay book-owned.'),
 state_owner='Inherited RandomTile selects three cosmetic layouts. Inventory.CheckEmptyState/CheckNonEmptyState changes detail tint k/W with the same tile/geometry; no removal/repopulation of pictured book marks. Native inventory items/population remain separate.',
 native_behavior='Preserve mounted organic50-weight furniture, native HangingSupport, container/on interaction, sounds, non-takeability and Joppa inventory population. No JPT research/knowledge mechanics or donor facing model.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(HERE/'source-packet.json'),asset(Path(__file__).resolve())],variants=decisions,
 alpha='Actual opaque structure A>=224plus two-pixel allowance retains actual A>=16only near structure, normalizes>=240and clears invisible RGB. Remove detached glow and preserve open compartment gaps; no opaque backing panel is accepted.',
 ownership='Opaque gold seed R-B>=10,G-B>=10selects12/10/7actual source-pattern spine surfaces. Their individual convex hulls include gray highlight/seam bands without selecting adjacent wooden frame. Gold-owned values become neutral max(R,G); other frame surfaces neutral mean-RGB.',
 registration='Full native-cell transform for all source layouts, wood/frame and spine masks; a hull is ownership only and never a per-book geometry fit.',
 source_limits='Sparse counts/leaning/flat arrangements follow exact native pixel groups. Book heights seated on boards, bottom board and open backing are authored physical interpretation. Cosmetic spines do not identify or count actual inventory objects.',
 stock_state='Stocked W and empty k use identical production bytes and geometry; only native detail tint changes. Empty preview does not claim books were individually removed or furniture inventory tested.',
 omitted='Three actual native layouts received three real refinement calls. Full/empty is a source tint state, not new artwork or donor bookcase state. No creature turnarounds/clothing. Native inventory/state/visibility/support acceptance stays deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,1830),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'JOPPA BOOKSHELF / three actual sparse layouts / neutral wood + spine ownership > native full W / empty k',font=font,fill='#e3cf43')
for row,ims in enumerate(previews):
 top=55+row*520
 for x,im,label in zip([45,515,985],ims,['Neutral / no baked gold','Stocked / native w + W','Empty tint / native w + k']):
  big=im.resize((272,408),Image.Resampling.LANCZOS);plate.paste(big,(x,top),big);draw.text((x,top+420),f'Layout{row+1} / '+label,font=font,fill='#e3cf43')
  for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
   small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+35+i*85,top+460),small)
for i,line in enumerate(['Three native spine arrangements retain upright/flat/leaning groups and source sparse gaps.',
 'Whole spines own their gray seams/highlights; native empty tint changes every owned book surface consistently.',
 'Same production geometry/masks in stocked and empty views. Inventory state does not create or identify book items.',
 'Open-backed compartments and bottom board are authored interpretation. Native state/support/visibility stays pending.']):draw.text((20,1660+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
ownership=Image.new('RGB',(1440,800),'#142823');draw=ImageDraw.Draw(ownership);draw.text((20,15),'SPINE OWNERSHIP / isolated neutral book surfaces including achromatic bands / no wooden shelf strokes',font=font,fill='#e3cf43')
for n,im in enumerate(isolated,1):
 x=65+(n-1)*470;big=im.resize((288,432),Image.Resampling.LANCZOS);ownership.paste(big,(x,75),big);draw.text((x,550),f'Layout{n} / '+str([12,10,7][n-1])+' spine surfaces',font=font,fill='#e3cf43')
draw.text((20,665),'Book-mask hulls preserve leaning shapes and internal gray bands without changing position or source-cell registration.',font=font,fill='#e5e8d8');draw.text((20,705),'Wood frame, cap and boards remain primary. Native full/empty preview differs only in detail tint W/k.',font=font,fill='#e5e8d8');ownership.save(OUT/'ownership-comparison.png')
print('Registered three neutral bookshelf layouts, whole-spine ownership and geometry-identical full/empty tint previews.')
