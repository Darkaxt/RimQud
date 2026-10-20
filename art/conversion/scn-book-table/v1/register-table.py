"""Neutral source table wood and broad tabletop detail coverage."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');assert source.size==(1024,1536)
structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5));structural.save(OUT/'opaque-structure-mask.png');selected.save(OUT/'selected-edge-mask.png')
owner=Image.new('L',source.size);owner.putdata([255 if a>=16 and r-b>=10 and g-b>=10 else 0 for r,g,b,a in source.get_flattened_data()]);owner.save(OUT/'top-ownership-mask.png')
primary=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);pp=[];dp=[]
for (r,g,b,a),edge,owns in zip(source.get_flattened_data(),selected.get_flattened_data(),owner.get_flattened_data()):
 if a<16 or not edge:pp.append((0,0,0,0));dp.append((0,0,0,0));continue
 a=255 if a>=240 else a;v=max(r,g) if owns else round((r+g+b)/3);pp.append((v,v,v,a));dp.append((v,v,v,a if owns else 0))
primary.putdata(pp);detail.putdata(dp);primary.save(OUT/'neutral-master.png');detail.save(OUT/'top-neutral-master.png')
primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS)
for im in [primary,detail]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.get_flattened_data()])
primary.save(OUT/'primary-neutral.png');detail.save(OUT/'detail-neutral.png');primary.getchannel('A').save(OUT/'coverage.png');detail.getchannel('A').save(OUT/'detail-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
native=tint(primary,palette['w']);native.alpha_composite(tint(detail,palette['W']));native.save(OUT/'native-w-W-preview.png')
model=dict(entry='SCN-BOOK-TABLE',kind='fixed_layered_furniture',blueprint='Book Table',native_tiles=['Items/sw_table_low_drawers.bmp'],source=asset(HERE/'source-packet.json'),primary=asset(OUT/'primary-neutral.png'),detail=asset(OUT/'detail-neutral.png'),coverage=asset(OUT/'coverage.png'),detail_coverage=asset(OUT/'detail-coverage.png'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One full1024x1536frame maps once to256square for the entire low table and top mask. No independent top/drawer/foot bbox centering.'),
 palette=dict(primary='actual native drawer/housing/support wood w',detail='actual native tabletop W',neutral_preview='Both production layers are equal-RGB grayscale. Gold extraction aid is removed.'),
 state_owner='One source fixed tile. Book Table inherits Furniture directly, not Table; no generic Table empty/full appearance applies.',native_behavior='Preserve native Container/on inventory, non-solid/non-takeable80-weight organic furniture, non-occlusion and rare animated/custom fallback. No donor end-table mechanics.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(Path(__file__).resolve())],alpha='Opaque structure A>=224plus two-pixel allowance retains actual A>=16only there; normalize>=240and clear transparent RGB. Discard exterior halo and preserve under-rail support gap.',
 ownership='Gold tabletop pixels R-B>=10,G-B>=10give the actual top/front-edge mask; neutral max(R,G) retains top shading. Gray drawer faces, recessed pulls, housing, low rail and feet remain primary-owned with neutral mean-RGB.',
 registration='One full source-cell mapping preserves top, drawers, rail and feet positions. No component is independently centered or fitted.',
 source_interpretation='Opaque wooden faces fill the original outline glyphs. Precise shallow seams suggest puzzle-box joinery, not a new interactive mechanism. Source shows no books, papers or actual container inventory.',
 omitted='No source random variants, open/closed drawers, generic Table empty/full artwork, creature turnaround or NPC clothing applies. Native inventory, visibility and animated/custom fallback acceptance remains deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,840),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'BOOK TABLE / two low drawers + broad bare top / neutral layers > native w + W',font=font,fill='#e3cf43')
for x,im,label in [(45,primary,'Neutral / no baked gold'),(515,detail,'Separate tabletop detail role'),(985,native,'Native drawers w + top W')]:
 big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,525),label,font=font,fill='#e3cf43')
 for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+40+i*85,580),small)
for i,line in enumerate(['Broad source top, two side-by-side drawers, low rail and short feet remain in one source-cell frame.',
 'Tabletop tint ownership stops above the drawer housing. Neutral view contains no baked yellow.',
 'No absent books/papers or invented open/full state: native container contents remain separate.',
 'Native inventory, visibility and rare animated/custom fallback acceptance remain pending.']):draw.text((20,680+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered low drawer table, neutral tabletop ownership and native w/W preview.')
