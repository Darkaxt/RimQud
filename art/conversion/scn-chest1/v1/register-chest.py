"""Neutral source chest wood/latch and independent bright side-band coverage."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');assert source.size==(1024,1536)
structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5));structural.save(OUT/'opaque-structure-mask.png');selected.save(OUT/'selected-edge-mask.png')
owner=Image.new('L',source.size);owner.putdata([255 if a>=16 and r-b>=10 and g-b>=10 else 0 for r,g,b,a in source.get_flattened_data()]);owner.save(OUT/'band-ownership-mask.png')
primary=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);pp=[];dp=[]
for (r,g,b,a),edge,owns in zip(source.get_flattened_data(),selected.get_flattened_data(),owner.get_flattened_data()):
 if a<16 or not edge:pp.append((0,0,0,0));dp.append((0,0,0,0));continue
 a=255 if a>=240 else a;v=max(r,g) if owns else round((r+g+b)/3);pp.append((v,v,v,a));dp.append((v,v,v,a if owns else 0))
primary.putdata(pp);detail.putdata(dp);primary.save(OUT/'neutral-master.png');detail.save(OUT/'band-neutral-master.png')
primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS)
for im in [primary,detail]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.get_flattened_data()])
primary.save(OUT/'primary-neutral.png');detail.save(OUT/'detail-neutral.png');primary.getchannel('A').save(OUT/'coverage.png');detail.getchannel('A').save(OUT/'detail-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
native=tint(primary,palette['w']);native.alpha_composite(tint(detail,palette['W']));native.save(OUT/'native-w-W-preview.png')
model=dict(entry='SCN-CHEST1',kind='fixed_layered_furniture',blueprint='Chest1',native_tiles=['Assets_Content_Textures_Tiles_sw_chest.bmp'],source=asset(HERE/'source-packet.json'),primary=asset(OUT/'primary-neutral.png'),detail=asset(OUT/'detail-neutral.png'),coverage=asset(OUT/'coverage.png'),detail_coverage=asset(OUT/'detail-coverage.png'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One full1024x1536frame maps once to256square for the entire closed chest and side-band mask. No independent lid/band/latch bbox centering.'),
 palette=dict(primary='actual native wood and latch w',detail='actual native two side bands W',neutral_preview='Both production layers are equal-RGB grayscale. Gold extraction aid is removed.'),
 state_owner='One inherited fixed closed-chest tile. Chest1 changes inventory builder/tier/aggregation, not appearance. No alternate open/empty/full tile is declared.',native_behavior='Preserve native Container/inventory, smart-use, chest sound, organic furniture physics and non-occlusion. Keep unspecified source physics defaults and custom native fallback; no JDS storage gameplay is transplanted.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(Path(__file__).resolve())],alpha='Opaque structure A>=224plus two-pixel allowance retains actual A>=16only there; normalize>=240and clear transparent RGB. Discard exterior halo and preserve the closed chest silhouette and actual exterior alpha.',
 ownership='Gold side-band pixels R-B>=10,G-B>=10give the actual two-band mask; neutral max(R,G) retains band shading. Gray wood faces, lid, primary-role central latch, seam and scratched marks remain primary-owned with neutral mean-RGB.',
 registration='One full source-cell mapping preserves lid, wooden case, side bands and latch positions. No component is independently centered or fitted.',
 source_interpretation='Opaque wooden faces fill the original outline glyphs and connect side bands to the case. Scratched abstract notches follow the description, not readable language. Band material and exact plank/latch details are authored interpretation. No new visible loot is added.',
 omitted='No source random variants, open-lid/empty/full state, creature turnaround or NPC clothing applies. Native container/inventory, physics, visibility and custom fallback acceptance remains deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,840),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'CHEST1 / closed wood lid + primary latch + two bright side bands / neutral layers > native w + W',font=font,fill='#e3cf43')
for x,im,label in [(45,primary,'Neutral / no baked gold'),(515,detail,'Separate side-band detail role'),(985,native,'Native wood/latch w + bands W')]:
 big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,525),label,font=font,fill='#e3cf43')
 for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+40+i*85,580),small)
for i,line in enumerate(['Source shouldered closed lid, side bands, primary latch and scratch marks stay in one source-cell frame.',
 'Only two side bands receive W. The central latch stays primary w; neutral view has no baked yellow.',
 'No visible loot, donor crate brace or invented open/empty/full view: native inventory stays separate.',
 'Native container/inventory, source physics, visibility and custom fallback acceptance remain pending.']):draw.text((20,680+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered closed wood chest, neutral band ownership and native w/W preview.')
