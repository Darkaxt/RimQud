"""Neutral source nailed-plank chair with an independently tinted hard seat."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');assert source.size==(1024,1536)
structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5))
structural.save(OUT/'opaque-structure-mask.png');selected.save(OUT/'selected-edge-mask.png')
owner=Image.new('L',source.size);owner.putdata([255 if a>=16 and g-r>=4 and b-r>=4 and min(g,b)>=20 else 0 for r,g,b,a in source.get_flattened_data()]);owner.save(OUT/'seat-ownership-mask.png')
primary=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);pp=[];dp=[]
for (r,g,b,a),edge,owns in zip(source.get_flattened_data(),selected.get_flattened_data(),owner.get_flattened_data()):
 if a<16 or not edge:pp.append((0,0,0,0));dp.append((0,0,0,0));continue
 a=255 if a>=240 else a;v=max(g,b) if owns else round((r+g+b)/3)
 pp.append((v,v,v,a));dp.append((v,v,v,a if owns else 0))
primary.putdata(pp);detail.putdata(dp);primary.save(OUT/'neutral-master.png');detail.save(OUT/'seat-neutral-master.png')
primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS)
for im in [primary,detail]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.get_flattened_data()])
primary.save(OUT/'primary-neutral.png');detail.save(OUT/'detail-neutral.png');primary.getchannel('A').save(OUT/'coverage.png');detail.getchannel('A').save(OUT/'detail-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
native=tint(primary,palette['w']);native.alpha_composite(tint(detail,palette['y']));native.save(OUT/'native-w-y-preview.png')
model=dict(entry='SCN-CHAIR',kind='fixed_layered_furniture',blueprint='Chair',native_tiles=['Items/sw_chair.bmp'],source=asset(HERE/'source-packet.json'),primary=asset(OUT/'primary-neutral.png'),detail=asset(OUT/'detail-neutral.png'),coverage=asset(OUT/'coverage.png'),detail_coverage=asset(OUT/'detail-coverage.png'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One full1024x1536frame maps once to256square for tall slatted wood back, supports and hard angled seat. No independent seat/back/support fitting or bbox centering.'),
 palette=dict(primary='actual native wood w',detail='actual native hard wooden seat y',neutral_preview='Both selected layers are equal-RGB neutral; pale cyan segmentation aid is removed.'),
 state_owner='One source fixed-map-view wooden Chair tile. Native sitting stays native; no donor facings or alternate occupied artwork is invented.',native_behavior='Preserve native Chair interaction, non-occlusion,20-weight non-takeable organic furniture, MissileCover10and rare Animated/custom fallback. No donor furniture dimensions, facings or mechanics are transplanted.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(Path(__file__).resolve())],
 alpha='Opaque structure A>=224plus two-pixel allowance retains actual A>=16only within it; normalize>=240and clear transparent RGB. Exterior glow is removed, with open slatted-back and support gaps preserved.',
 ownership='Actual pale-cyan hard-seat pixels G-R>=4,B-R>=4,min(G,B)>=20identify the wood seat. Their neutral value is max(G,B). Other surfaces are neutral mean-RGB wood. Slatted back, straight supports, seat rim and nail marks remain primary wood. The seat role is hard wood, not fabric.',
 registration='Shared full source-cell frame for oblique geometry and both masks. The hard seat, tall back and straight supports are not independently recentered.',
 source_interpretation='Plain nailed planks, two inner back bars and hard seat board seams elaborate the actual native source shape. Grain, exact nail placement and hidden attachments are authored interpretation. No padded seat, canvas, rounded back, armrests or occupant is added.',
 omitted='No source random layout, occupied tile or creature turnaround applies. No NPC clothing extraction applies to this fixed furniture; native sitting/cover/visibility and rare animated fallback acceptance remains deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,840),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'PLANK CHAIR / tall slatted back + hard angled seat / neutral layers > native w + y',font=font,fill='#e3cf43')
for x,im,label in [(45,primary,'Neutral / no baked cyan'),(515,detail,'Separate hard-seat tint role'),(985,native,'Native frame w + hard seat y')]:
 big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,525),label,font=font,fill='#e3cf43')
 for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+40+i*85,580),small)
for i,line in enumerate(['Source tall open back, straight planks, hard angled seat and visible support extents stay in one cell frame.',
 'Frame/seat ownership stays separate; back gaps and under-seat spaces remain transparent.',
 'Native y marks a hard wooden seat, not upholstery. No cushion, canvas, curved back, donor rotation or occupant.',
 'Native sitting, MissileCover, visibility and rare animated/custom fallback acceptance remain pending.']):draw.text((20,680+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered neutral nailed-plank chair, independent hard-seat ownership and native w/y preview.')
