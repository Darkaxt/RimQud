"""Register cardinal bench once, extract only actual gold stock over unchanged base."""
from pathlib import Path
from collections import deque
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def cleaned(im):
 core=im.getchannel('A').point(lambda a:255 if a>=224 else 0);edge=core.filter(ImageFilter.MaxFilter(5));out=im.copy();out.putdata([(r,g,b,255 if a>=240 else a) if a>=16 and keep else (0,0,0,0) for (r,g,b,a),keep in zip(im.get_flattened_data(),edge.get_flattened_data())]);return out,core,edge
base_raw=Image.open(HERE/'refined-empty.png').convert('RGBA');stock_raw=Image.open(HERE/'refined-occupied.png').convert('RGBA');assert base_raw.size==stock_raw.size==(1024,1536)
base,core,edge=cleaned(base_raw);core.save(OUT/'base-opaque-structure-mask.png');edge.save(OUT/'base-selected-edge-mask.png');stock_clean,stockcore,stockedge=cleaned(stock_raw)
# Seed actual opaque colored surfaces, excluding the generated colored transparency glow.
w,h=stock_raw.size;pixels=list(stock_raw.get_flattened_data());seeds=set(i for i,(r,g,b,a) in enumerate(pixels) if a>=224 and r-b>=12 and g-b>=12)
groups=[]
while seeds:
 first=seeds.pop();q=deque([first]);group=[first]
 while q:
  i=q.popleft();x,y=i%w,i//w
  for j in ([i-1] if x else [])+([i+1] if x+1<w else [])+([i-w] if y else [])+([i+w] if y+1<h else []):
   if j in seeds:seeds.remove(j);q.append(j);group.append(j)
 if len(group)>100:groups.append(group)
groups.sort(key=len,reverse=True);assert len(groups)==2,[(len(g)) for g in groups]
owner=Image.new('L',(w,h));draw=ImageDraw.Draw(owner);bounds=[]
for group in groups:
 rows={}
 for i in group:rows.setdefault(i//w,[]).append(i%w)
 for y,xs in rows.items():draw.line((min(xs),y,max(xs),y),fill=255)
 bounds.append([min(i%w for i in group),min(i//w for i in group),max(i%w for i in group)+1,max(i//w for i in group)+1])
# Two-pixel antialias/outline allowance, still clipped to actual generated alpha.
owner=owner.filter(ImageFilter.MaxFilter(5));owner.save(OUT/'stock-surface-ownership-mask.png')
base.putdata([(round((r+g+b)/3),)*3+(a,) if a else (0,0,0,0) for r,g,b,a in base.get_flattened_data()]);stock=Image.new('RGBA',(w,h));stock.putdata([(max(r,g),)*3+(a,) if owns and a else (0,0,0,0) for (r,g,b,a),owns in zip(stock_clean.get_flattened_data(),owner.get_flattened_data())])
base.save(OUT/'base-neutral-master.png');stock.save(OUT/'stock-neutral-master.png')
def small(im):
 out=im.resize((256,256),Image.Resampling.LANCZOS);out.putdata([(round((r+g+b)/3),)*3+(a,) if a>=4 else (0,0,0,0) for r,g,b,a in out.get_flattened_data()]);return out
base=small(base);stock=small(stock);empty_detail=Image.new('RGBA',(256,256));occupied=base.copy();occupied.alpha_composite(stock)
for name,im in [('base-primary-neutral',base),('empty-detail-neutral',empty_detail),('occupied-primary-neutral',occupied),('occupied-detail-neutral',stock)]:im.save(OUT/f'{name}.png')
for state,im,detail in [('empty',base,empty_detail),('occupied',occupied,stock)]:im.getchannel('A').save(OUT/f'{state}-coverage.png');detail.getchannel('A').save(OUT/f'{state}-detail-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,code):
 c=bytes.fromhex(palette[code]);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
native_empty=tint(base,'c');native_empty.save(OUT/'empty-native-c-preview.png');previews={}
for code in ['C','w','y','W']:
 im=tint(base,'c');im.alpha_composite(tint(stock,code));im.save(OUT/f'occupied-native-c-{code}-preview.png');previews[code]=im
model=dict(entry='SCN-METAL-WORKBENCH',kind='inventory_state_layered_furniture',blueprint='Metal Workbench',source=asset(HERE/'source-packet.json'),shared_base=asset(OUT/'base-primary-neutral.png'),
 states={state:dict(native_tile=tile,primary=asset(OUT/primary),detail=asset(OUT/detail),coverage=asset(OUT/f'{state}-coverage.png'),detail_coverage=asset(OUT/f'{state}-detail-coverage.png')) for state,tile,primary,detail in [('empty','Items/sw_table_metal.bmp','base-primary-neutral.png','empty-detail-neutral.png'),('occupied','Items/sw_table_metal_full.bmp','occupied-primary-neutral.png','occupied-detail-neutral.png')]},
 camera=dict(facing='south/front',projection='Parallel horizontal/vertical tabletop edges, vertical front supports, no yaw or converging depth. Same camera across states.'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One full1024x1536source frame maps once to256square. Occupied overlay stays in actual generated frame; unchanged selected empty base is reused. No bbox fitting or independent centering.'),
 palette=dict(primary='Native c across all steel, including edge highlights',empty_detail='C with no occupied detail coverage',occupied_detail='Actual native chosen C/w/y/W on stock only; sample previews do not choose or reroll state'),
 state_owner='Native Inventory determines EmptyTile/FullTile and independent FullDetailColor. Source marker is stock indication, not identified inventory or new crafting gameplay.',native_acceptance='Pending every-conversion-generated gate')
decisions=dict(inputs=[asset(HERE/'refined-empty.png'),asset(HERE/'refined-occupied.png'),asset(Path(__file__).resolve())],
 camera='Inspected actual saved empty and occupied proposals: rectangular tabletop boundaries and vertical supports remain cardinal. Intrinsic support foot notches and square apertures are not a new perspective.',
 alpha='A>=224structure plus two-pixel allowance retains actual A>=16only near structure, normalizes>=240and clears invisible RGB. Actual support holes and occupied handle center are alpha openings, not colored background RGB.',
 stock_extraction=dict(method='Two actual opaque-gold connected components (one slotted upright mark, one small circular mark); per-component row-span ownership includes internal achromatic shading and dark outlines with two-pixel allowance. Clip to actual cleaned alpha, so the slot remains open. No global gold halo or unchanged table surface is extracted.',core_bounds=bounds,core_sizes=[len(g) for g in groups]),
 same_base='Empty master and occupied base are exactly the same selected base file. Only extracted neutral stock is added. Raw occupied bench repaint is ignored.',
 palette='Neutral equal RGB for base and stock; original blue-gray/gold pigments removed. Empty detail layer is transparent because original empty mask has no covered detail pixels.',native='This is art generation/registration only. Native inventory transitions, color selection, visibility, physics and rare animated fallback remain pending.')
for name,data in [('model.json',model),('registration-decisions.json',decisions)]: (OUT/name).write_bytes((json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,1190),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'METAL WORKBENCH / corrected cardinal camera / one unchanged bench + isolated native occupied marker',font=font,fill='#e3cf43')
for row,items in enumerate([[(base,'Empty / neutral steel'),(occupied,'Occupied / same steel base'),(stock,'Isolated neutral stock')],[(native_empty,'Empty / native c'),(previews['C'],'Occupied / native c+C'),(previews['W'],'Occupied / native c+W sample')]]):
 for col,(im,label) in enumerate(items):
  x=45+470*col;y=55+480*row;big=im.resize((256,384),Image.Resampling.LANCZOS);plate.paste(big,(x,y),big);d.text((x,y+390),label,font=font,fill='#e3cf43')
  for i,(sw,sh) in enumerate([(16,24),(24,36),(32,48)]):
   smallim=im.resize((sw,sh),Image.Resampling.LANCZOS);plate.paste(smallim,(x+35+i*70,y+425),smallim)
for i,line in enumerate(['Parallel tabletop and straight supports: source identity retained, rejected tapered camera removed.',
 'No whole-table repaint between states; only the extracted upright stock mark and small mark are added.',
 'Steel stays primary c; native inventory selects occupied detail C/w/y/W. No baked gold or extra tools.',
 'Source physics, actual inventory/color transitions and visibility acceptance remain pending.']):d.text((20,1035+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered cardinal empty/occupied states, exact shared base and two stock ownership components:',bounds)
