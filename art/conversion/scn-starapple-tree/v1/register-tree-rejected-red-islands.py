"""One fixed starapple tree, neutral fruit mask and two native harvest tints."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Never overwrite logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');assert source.size==(1024,1536)
neutral=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);fruitmask=Image.new('L',source.size);coverage=Image.new('L',source.size);np=[];dp=[];fp=[];ap=[];red_points=set()
for index,(r,g,b,a) in enumerate(source.getdata()):
 if a<16:np.append((0,0,0,0));dp.append((0,0,0,0));fp.append(0);ap.append(0);continue
 a=255 if a>=240 else a;is_red=r-g>=12 and r-b>=12 and r>=30
 v=max(r,g,b) if is_red else round((r+g+b)/3)
 np.append((v,v,v,a));dp.append((v,v,v,a if is_red else 0));fp.append(a if is_red else 0);ap.append(a)
 if is_red:red_points.add((index%1024,index//1024))
groups=[]
while red_points:
 seed=red_points.pop();group={seed};todo=[seed]
 while todo:
  x,y=todo.pop()
  for dx,dy in [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]:
   q=(x+dx,y+dy)
   if q in red_points:red_points.remove(q);group.add(q);todo.append(q)
 if len(group)>=40:groups.append(dict(pixels=len(group),bounds=[min(x for x,y in group),min(y for x,y in group),max(x for x,y in group)+1,max(y for x,y in group)+1]))
assert len(groups)==6,groups
neutral.putdata(np);detail.putdata(dp);fruitmask.putdata(fp);coverage.putdata(ap)
for name,im in [('neutral-master',neutral),('fruit-neutral-master',detail),('fruit-ownership-mask',fruitmask),('source-coverage-mask',coverage)]:im.save(OUT/f'{name}.png')
primary=neutral.resize((256,256),Image.Resampling.LANCZOS);secondary=detail.resize((256,256),Image.Resampling.LANCZOS)
for im in [primary,secondary]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.getdata()])
primary.save(OUT/'primary-neutral.png');secondary.save(OUT/'detail-neutral.png');primary.getchannel('A').save(OUT/'coverage.png');secondary.getchannel('A').save(OUT/'detail-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,c):
 c=bytes.fromhex(c);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
previews={}
for state,color in [('ripe','R'),('unripe','K')]:
 native=tint(primary,palette['g']);native.alpha_composite(tint(secondary,palette[color]));native.save(OUT/f'{state}-native-preview.png');previews[state]=native
model=dict(entry='SCN-STARAPPLE-TREE',kind='harvest_tinted_fixed_plant',blueprint='Starapple Tree',native_tiles=['Terrain/sw_starappletree.bmp'],source=asset(HERE/'source-packet.json'),
 primary=asset(OUT/'primary-neutral.png'),detail=asset(OUT/'detail-neutral.png'),coverage=asset(OUT/'coverage.png'),detail_coverage=asset(OUT/'detail-coverage.png'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One full-cell transform for both harvest states. States share exactly the same primary, fruit layer and alpha; no geometry or anchor changes.'),
 palette=dict(primary='actual native TileColor g',detail='actual native DetailColor: R when ripe, K when unripe',neutral_preview='Equal RGB only; red extraction aid removed from both saved layers.'),
 states=dict(ripe=dict(primary='g',detail='R'),unripe=dict(primary='g',detail='K')),
 appearance='Sparse asymmetric fruit tree with ashen neutral bark texture and six source-inspired fruit marks. Native primary g tint is retained even on described ashen wood; no unsupported third fixed bark color.',
 state_owner='Native Harvestable owns ripeness, yield1, regeneration and tint. RipeTiles/UnripeTiles absent for this source. No fruit disappears or moves as an invented harvest effect.',
 native_behavior='Source visibility/occlusion, plant/hanging support and native harvest interaction remain unchanged; native binding/tint acceptance pending.',native_acceptance='Pending every-conversion-generated gate')
decisions=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(Path(__file__).resolve())],
 alpha='Actual alpha>=16 selected; interiors>=240normalized, invisible RGB cleared. Full sparse crown and true branch gaps retained; no exterior preview glow assigned to the object.',
 fruit_ownership='Red-dominant opaque pixels R-G>=12,R-B>=12,R>=30 identify fruit; six major connected components confirmed as an authoring mask inspection. Neutralized both primary and fruit roles.',
 refined_fruit_components=sorted(groups,key=lambda x:(x['bounds'][1],x['bounds'][0])),
 source_limit='Six glyph groups are authored fruit marks, not native harvest count. Native yield remains1. Branch texture is authored from description, and actual native primary tint remains g.',
 registration='Whole1024x1536image maps once to256square, shared by both harvest tints. Neither state is independently centered or rescaled.',
 omitted_views='Fixed-view plant does not require creature turnarounds, clothing or secondary facing. Ripeness is a source-defined color change with shared geometry.')
for name,value in [('model.json',model),('registration-decisions.json',decisions)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,845),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'STARAPPLE / neutral tree + fruit ownership / native ripe and unripe tints / identical geometry',font=font,fill='#e3cf43')
for x,im,label in [(20,primary,'Neutral / no baked red'),(380,secondary,'Separate neutral fruit role'),(740,previews['ripe'],'Ripe / native g + R'),(1100,previews['unripe'],'Unripe / native g + K')]:
 big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,525),label,font=font,fill='#e3cf43')
 for t,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+30+t*85,580),small)
for i,line in enumerate(['One tree, one fruit mask and one anchor: ripe/unripe appearance changes only through actual native detail tint.',
 'Six source-inspired fruit marks remain in place in both states. Native yield is one; harvest/regrowth stays native.',
 'Neutral mode is grayscale. Described ashen wood is neutral texture, while native primary g remains authoritative.',
 'No creature facings or clothing apply. Native ripeness/binding/visibility/occlusion acceptance remains pending.']):draw.text((20,680+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered one starapple tree with six fruit-mask components, fixed geometry and two native harvest tints.')
