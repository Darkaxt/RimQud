"""Three native watervine layouts, source-positioned swollen wafers and furrowed vines."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,xml.etree.ElementTree as ET,math
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');NATIVE=DATA/'StreamingAssets/Base/ObjectBlueprints/ZoneTerrain.xml';DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
index=json.loads((HERE/'native-state-index.json').read_text());assert len(index['states'])==3
tree=ET.parse(NATIVE).getroot();native=tree.find(".//object[@Name='Watervine']");reference=next(x for x in json.loads((DONOR/'joppa-textures.json').read_text()) if x['file']=='reed.png');assert sha(DONOR/'reed.png')==reference['png_sha256']
code=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.Fireflies',str(DATA/'Managed/Assembly-CSharp.dll')],capture_output=True,check=True).stdout
lines=[
 [[(7.5,21),(7.3,15),(5.2,13),(4.5,10),(5.2,7),(4,4.5),(5.5,2)],[(12,21),(12.2,17),(11.7,14.5),(13,11),(12.3,8),(10.5,6.3)],[(3,21),(3.5,18),(2.6,16.8)]],
 [[(8.2,21.5),(9.5,18),(8.8,15),(8.7,12),(10.4,9),(8.5,7.5),(8.1,4.7),(7,2.5)],[(4.5,20.5),(3.5,17),(3.5,14.8),(2.5,13),(3.6,10)],[(12.6,21.8),(13,19.5),(12,17.5)]],
 [[(10.8,20.5),(12,18),(11.5,15.5),(10.4,13),(12,10),(10.5,7.5),(11.4,5),(12.3,3.4)],[(3.8,21.5),(3.2,18),(4.4,15),(3.8,12.7),(4.8,10.2),(3.2,8.6),(2.4,6)]]]
layouts=[]
for n,row in enumerate(index['states'],1):
 rawpath=Path(row['private_mask']['path']);assert sha(rawpath)==row['private_mask']['sha256'];raw=Image.open(rawpath).convert('RGBA');points={(x,y) for y in range(24) for x in range(16) if raw.getpixel((x,y))[3] and raw.getpixel((x,y))[0]==255};groups=[]
 while points:
  seed=points.pop();group={seed};todo=[seed]
  while todo:
   x,y=todo.pop()
   for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
    if q in points:points.remove(q);group.add(q);todo.append(q)
  groups.append(group)
 pads=[dict(center=[sum(x+.5 for x,y in group)/len(group),sum(y+.5 for x,y in group)/len(group)],source_pixels=sorted(group),radius=.34+.07*min(len(group)-1,3)) for group in groups]
 layouts.append(dict(variant=n,native_tile=row['tile'],vine_paths=lines[n-1],wafer_marks=pads))
packet=dict(entry='SCN-WATERVINE',recorded_at=datetime.now(timezone.utc).isoformat(),identity='Watervine -> Plant -> PhysicalObject',description=native.find("part[@Name='Description']").get('Short'),
 native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode'),parent=ET.tostring(tree.find(".//object[@Name='Plant']"),encoding='unicode')),
 original_states=asset(HERE/'native-state-index.json'),original_context=asset(HERE/'native-states-comparison.png'),layouts=layouts,
 harvest=dict(native.find("part[@Name='Harvestable']").attrib),palette=dict(primary='w',ripe_detail='g',unripe_detail='K',rule='The vine is native brown w; swollen wafers receive green g when ripe, dark teal K when unripe. One fixed geometry per source variant; no color baked into neutral albedo.'),
 donor_reference=dict(package='RimWorld Core',record=reference,path=str(DONOR/'reed.png'),sha256=sha(DONOR/'reed.png'),role='Actual HaygrassA supplies crisp narrow plant strokes and low-relief readable outline/shading only. No close equivalent for moisture-swollen wafers is claimed; grain heads, straight grass blades, donor color and crop mechanics are not adopted.'),
 construction='Explicit crooked furrowed vine paths follow each native layout. Source detail connected groups become authored small thick moisture-swollen wafer knots attached by short tendrils, not leaves or cereal heads. This visual grouping does not alter native Vinewafer yield1.',
 native_fireflies=dict(class_name='XRL.World.Parts.Fireflies',assembly_sha256=sha(DATA/'Managed/Assembly-CSharp.dll'),scoped_decompilation_sha256=hashlib.sha256(code).hexdigest(),behavior='BeforeRenderEvent may add a native firefly particle at night in an unlit active-zone cell. Keep this native particle event; no firefly or glow is baked into the plant bitmap.'),
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],authored_anchor=[8,16],rule='All three layouts and both harvest tints use one source-cell mapping; no per-object bounding-box fit or recentering.'),
 states='Three declared RandomTile shapes, each with ripe g/unripe K detail tints from Harvestable. No rotated creature views, clothing, automatic vine-merging or invented growth forms.',native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
for layout in layouts:
 n=layout['variant'];body='';pads='';segments=[]
 for path in layout['vine_paths']:
  pts=' '.join(f'{x},{y}' for x,y in path);body+=f'<polyline points="{pts}" fill="none" stroke="#454545" stroke-width=".62" stroke-linecap="round" stroke-linejoin="round"/><polyline points="{pts}" fill="none" stroke="#b8b8b8" stroke-width=".42" stroke-linecap="round" stroke-linejoin="round"/>'
  body+=f'<polyline points="{pts}" fill="none" stroke="#e2e2e2" stroke-width=".075" stroke-linecap="round"/>'
  segments+=list(zip(path[:-1],path[1:]))
 for pad in layout['wafer_marks']:
  x,y=pad['center'];r=pad['radius'];closest=None;distance=math.inf
  for (ax,ay),(bx,by) in segments:
   dx,dy=bx-ax,by-ay;t=max(0,min(1,((x-ax)*dx+(y-ay)*dy)/(dx*dx+dy*dy)));p=(ax+t*dx,ay+t*dy);d=(x-p[0])**2+(y-p[1])**2
   if d<distance:distance=d;closest=p
  ax,ay=closest;body+=f'<path d="M{ax} {ay}Q{(x+ax)/2} {y+.2} {x} {y}" fill="none" stroke="#a8a8a8" stroke-width=".14"/>'
  pads+=f'<path d="M{x-r} {y}Q{x-r*.8} {y-r*.9} {x} {y-r*.7}Q{x+r} {y-r*.8} {x+r} {y}Q{x+r*.9} {y+r*.8} {x} {y+r*.7}Q{x-r} {y+r*.8} {x-r} {y}Z" fill="#009403" stroke="#245224" stroke-width=".075"/><path d="M{x-r*.55} {y-.05}Q{x} {y-r*.35} {x+r*.55} {y-.05}" stroke="#54bb55" stroke-width=".06" fill="none"/>'
 # Small creeping root/tendril lines, not a new shared collision footprint.
 body+='<path d="M2.5 21Q4 20.5 5 21.6T8.2 21.6M10.5 21.5Q12 20.6 13.7 21.6" fill="none" stroke="#929292" stroke-width=".2" stroke-linecap="round"/>'
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{body}{pads}</svg>';path=HERE/f'constructed-variant-{n}.svg';path.write_bytes(svg.encode());(HERE/f'constructed-variant-{n}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(path),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,790),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'WATERVINE / three source layouts > furrowed vines with swollen wafers > actual Core stroke reference',font=font,fill='#e3cf43')
for x,n in [(20,1),(370,2),(720,3)]:
 im=Image.open(HERE/f'constructed-variant-{n}.png').resize((256,384),Image.Resampling.LANCZOS);plate.paste(im,(x,80),im);draw.text((x,510),f'Manual{n} / source wafer knots',font=font,fill='#e5e8d8')
im=Image.open(DONOR/'reed.png').convert('RGBA').resize((256,256),Image.Resampling.NEAREST);plate.paste(im,(1100,120),im);draw.text((1070,510),'Core HaygrassA / stroke style',font=font,fill='#e5e8d8')
for i,line in enumerate(['Source description calls for moisture-swollen wafers in place of leaves. No leafy reed/cereal canopy is copied.',
 'All three native glyphs have different vine/wafer layouts. Green in manual images identifies detail ownership only.',
 'Native Harvestable changes wafer tint g/K while vine w and geometry remain fixed; native yield remains one.',
 'Native Fireflies adds night particles independently. No glow/bugs are baked into these fixed-view sprites.']):draw.text((20,585+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Built three source-positioned watervine layouts with wafer counts',[len(x['wafer_marks']) for x in layouts])
