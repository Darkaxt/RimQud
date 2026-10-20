"""Register both source cabinet layouts and explicit drawer/detail ownership."""
from pathlib import Path
from collections import deque
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registrations'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R')
 return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
variants=[];decisions=[];previews=[]
for number,expected in [(1,3),(2,8)]:
 source=Image.open(HERE/f'refined-variant-{number}.png').convert('RGBA');assert source.size==(1024,1536)
 structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5))
 structural.save(OUT/f'variant-{number}-opaque-structure-mask.png');selected.save(OUT/f'variant-{number}-selected-edge-mask.png')
 # Actual source-colored refined fronts form three/eight substantial islands.
 # Fill their rectangular interiors so achromatic pulls and pale highlights
 # inherit their owning drawer, rather than becoming primary-colored seams.
 points={(i%1024,i//1024) for i,(r,g,b,a) in enumerate(source.get_flattened_data()) if a>=224 and r-b>=12 and g-b>=12}
 seed=Image.new('L',source.size);seed.putdata([255 if (x,y) in points else 0 for y in range(1536) for x in range(1024)]);seed.save(OUT/f'variant-{number}-gold-seed.png')
 boxes=[]
 while points:
  first=points.pop();q=deque([first]);xs=[first[0]];ys=[first[1]];count=0
  while q:
   x,y=q.popleft();count+=1
   for p in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if p in points:points.remove(p);q.append(p);xs.append(p[0]);ys.append(p[1])
  if count>300:boxes.append(dict(pixels=count,rect=[min(xs),min(ys),max(xs)+1,max(ys)+1]))
 boxes.sort(key=lambda b:(b['rect'][1],b['rect'][0]));assert len(boxes)==expected,(number,boxes)
 owner=Image.new('L',source.size);draw=ImageDraw.Draw(owner)
 for box in boxes:
  x0,y0,x1,y1=box['rect'];draw.rectangle((x0,y0,x1-1,y1-1),fill=255)
 owner.save(OUT/f'variant-{number}-drawer-ownership-mask.png')
 primary=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);pp=[];dp=[]
 for (r,g,b,a),edge,owns in zip(source.get_flattened_data(),selected.get_flattened_data(),owner.get_flattened_data()):
  if a<16 or not edge:pp.append((0,0,0,0));dp.append((0,0,0,0));continue
  a=255 if a>=240 else a;v=max(r,g) if owns else round((r+g+b)/3)
  pp.append((v,v,v,a));dp.append((v,v,v,a if owns else 0))
 primary.putdata(pp);detail.putdata(dp)
 primary.save(OUT/f'variant-{number}-neutral-master.png');detail.save(OUT/f'variant-{number}-detail-neutral-master.png')
 primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS)
 for im in [primary,detail]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.get_flattened_data()])
 primary.save(OUT/f'variant-{number}-primary-neutral.png');detail.save(OUT/f'variant-{number}-detail-neutral.png')
 primary.getchannel('A').save(OUT/f'variant-{number}-coverage.png');detail.getchannel('A').save(OUT/f'variant-{number}-detail-coverage.png')
 native=tint(primary,palette['c']);native.alpha_composite(tint(detail,palette['W']));native.save(OUT/f'variant-{number}-native-c-W-preview.png')
 variants.append(dict(variant=number,native_tile=f'Items/sw_multi_cabinet_{number}.bmp',primary=asset(OUT/f'variant-{number}-primary-neutral.png'),detail=asset(OUT/f'variant-{number}-detail-neutral.png'),coverage=asset(OUT/f'variant-{number}-coverage.png'),detail_coverage=asset(OUT/f'variant-{number}-detail-coverage.png')))
 decisions.append(dict(variant=number,actual_gold_front_regions=boxes,input=asset(HERE/f'refined-variant-{number}.png'),ownership='Substantial opaque gold islands supply rectangular front bounds. Their interiors include achromatic recessed pulls and white highlights; adjacent case/shelves/brackets stay primary. These are explicit cabinet-surface regions, not creature limb masks.'))
 previews.append((primary,detail,native))
model=dict(entry='SCN-ARGYVE-MULTICABINET',kind='fixed_layered_furniture_variants',blueprint='Argyve Multicabinet',source=asset(HERE/'source-packet.json'),variants=variants,
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='Each entire1024x1536refined frame maps once to256square. No drawer, top box, foot, detail mask or variant is independently bbox-centered.'),
 palette=dict(primary='actual native c',detail='actual native W',neutral_preview='Equal-RGB case/front and detail layers; no baked gold remains in production.'),
 state_owner='Native inherited RandomTile selects one of two cosmetic layouts. No invented container-open/closed sprite or donor rotations.',
 inventory_boundary='Actual Argyve inventory population stays native. Tiny fixture storage marks are source-bound interpretation, not displayed contents.',
 native_behavior='Preserve source metal container/inventory/smart-use, solid physics and occluding behavior; no VFE research bonus or donor storage mechanics.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(Path(__file__).resolve()),asset(HERE/'source-packet.json')],variants=decisions,
 alpha='Opaque structure at actual A>=224plus two-pixel edge allowance; retain actual A>=16only within it, normalize>=240and clear invisible RGB. Discard detached exterior glow. Under-plinth opening remains transparent.',
 palette='Gray metal becomes neutral mean-RGB. Gold-owned fronts become neutral max(R,G); their hue is discarded. Native preview applies c to case and W to owned surfaces. Neutral view is actually grayscale.',
 registration='One full-cell frame/anchor per whole cabinet, including top storage block; source cosmetic variants remain distinct. No independent alpha-bounds centering.',
 source_interpretations='Opaque galvanized faces fill native outline glyphs; glyph gaps are not physically transparent doors. Partial original marks become dark recesses and nested storage. Top projections are brackets, not proven electronics.',
 omitted='No four-view creature turnaround, clothing or dynamically opening door state is declared for this source furniture. Native state/visibility/contact acceptance remains pending.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,1480),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'ARGYVE MULTICABINET / both actual native layouts / neutral ownership > native c + W',font=font,fill='#e3cf43')
for row,ims in enumerate(previews):
 top=65+row*630
 for x,im,label in zip([45,515,985],ims,['Neutral whole cabinet','Separate neutral W fronts','Native c + W palette']):
  big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,top),big);draw.text((x,top+450),f'Variant{row+1} / '+label,font=font,fill='#e3cf43')
  for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
   small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+40+i*85,top+505),small)
for i,line in enumerate(['Unequal drawers, recesses, narrow fronts, broad door and top storage box follow the two actual source layouts.',
 'Gold proposal color is removed. White highlights and dark pulls inherit the same selected front ownership.',
 'One shared source-cell frame; no per-compartment centering or invented open/closed animation.',
 'Inventory, source random selection, solidity and occlusion stay native. Native acceptance remains pending.']):draw.text((20,1320+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered both source layouts, three/eight owned detail regions, neutral layers and native c/W previews.')
