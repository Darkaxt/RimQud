"""Neutral cardinal plank chair, retaining complete hard-seat tint ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve selected output history'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
raw=Image.open(HERE/'refined-front.png').convert('RGBA');assert raw.size==(1024,1536)
core=raw.getchannel('A').point(lambda a:255 if a>=224 else 0);edge=core.filter(ImageFilter.MaxFilter(5));seed=Image.new('L',raw.size);seed.putdata([255 if a>=16 and g-r>=8 and b-r>=8 else 0 for r,g,b,a in raw.get_flattened_data()]);near=seed.filter(ImageFilter.MaxFilter(13))
whole=Image.new('RGBA',raw.size);seat=Image.new('RGBA',raw.size);ownership=Image.new('L',raw.size);wp=[];sp=[];op=[]
for (r,g,b,a),keep,owns,nearby in zip(raw.get_flattened_data(),edge.get_flattened_data(),seed.get_flattened_data(),near.get_flattened_data()):
 if a<16 or not keep:wp.append((0,0,0,0));sp.append((0,0,0,0));op.append(0);continue
 a=255 if a>=240 else a;owns=bool(owns) or (bool(nearby) and min(r,g,b)>=225 and max(r,g,b)-min(r,g,b)<=18);v=max(g,b) if owns else round((r+g+b)/3)
 wp.append((v,v,v,a));sp.append((v,v,v,a if owns else 0));op.append(a if owns else 0)
whole.putdata(wp);seat.putdata(sp);ownership.putdata(op)
for name,im in [('opaque-structure-mask',core),('selected-edge-mask',edge),('seat-color-seed',seed),('seat-ownership-mask',ownership),('neutral-master',whole),('seat-neutral-master',seat)]:im.save(OUT/f'{name}.png')
whole=whole.resize((256,256),Image.Resampling.LANCZOS);seat=seat.resize((256,256),Image.Resampling.LANCZOS)
for im in [whole,seat]:im.putdata([(round((r+g+b)/3),)*3+(a,) if a>=4 else (0,0,0,0) for r,g,b,a in im.get_flattened_data()])
whole.save(OUT/'primary-neutral.png');seat.save(OUT/'detail-neutral.png');whole.getchannel('A').save(OUT/'coverage.png');seat.getchannel('A').save(OUT/'detail-coverage.png')
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
native=tint(whole,'98875f');native.alpha_composite(tint(seat,'b1c9c3'));native.save(OUT/'native-w-y-preview.png')
model=dict(entry='SCN-CHAIR',kind='fixed_layered_furniture',blueprint='Chair',native_tiles=['Items/sw_chair.bmp'],source=asset(HERE/'source-packet.json'),primary=asset(OUT/'primary-neutral.png'),detail=asset(OUT/'detail-neutral.png'),coverage=asset(OUT/'coverage.png'),detail_coverage=asset(OUT/'detail-coverage.png'),
 camera=dict(facing='south/front',projection='Straight back/posts and supports; rectangular hard seat with horizontal/vertical parallel edges. No diagonal footprint, yaw or three-quarter view.'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One entire1024x1536frame maps once to256square for frame, seat, supports and masks. Reconstructed cardinal camera, no separate bbox fitting.'),palette=dict(primary='Native frame/back/support w',detail='Native hard plank seat y; tint does not imply cloth',neutral='Equal RGB in both production layers; no baked cyan or wood pigment'),
 state_owner='One fixed native furniture tile. Camera correction does not invent facing selection or an occupied graphic.',native_behavior='Preserve native sitting,20-weight non-takeable organic furniture, cover/non-occlusion and rare animated/custom native fallback.',native_acceptance='Pending every-conversion-generated gate')
decisions=dict(inputs=[asset(HERE/'refined-front.png'),asset(Path(__file__).resolve())],camera='Inspected actual selected refinement against constructed cardinal front and actual named donor Chair_south. Horizontal/vertical structure is retained; older oblique proposal remains rejected history.',
 alpha='Opaque A>=224plus two-pixel allowance retains actual A>=16near structure, normalizes>=240and clears invisible RGB. Open slatted back and under-seat gaps stay transparent.',
 ownership='Cyan seed G-R>=8/B-R>=8plus near-white highlights within six pixels gives whole hard-seat ownership, including bevel/plank seams. Gray frame/nails/supports remain primary. No clothing or body pixels are involved.',
 geometry='Two inner back slats, rails and nailed hard plank seat retain source identity under reprojection. Rear support overlap is authored; not proof of a two-legged physical chair.',native='Authoring only: no game/harness launch, renderer change, new facing mechanic or claimed sitting/visibility acceptance.')
for name,data in [('model.json',model),('registration-decisions.json',decisions)]: (OUT/name).write_bytes((json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
plate=Image.new('RGB',(1440,860),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);d.text((20,15),'CHAIR / corrected cardinal SOUTH / nailed plank frame + hard seat / neutral ownership > native w+y',font=font,fill='#e3cf43')
for x,im,label in [(45,whole,'Neutral / straight cardinal frame'),(515,seat,'Isolated hard wooden seat'),(985,native,'Native w frame + y hard seat')]:
 big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);d.text((x,530),label,font=font,fill='#e3cf43')
 for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+35+i*80,585),small)
for i,line in enumerate(['Qud slatted-back/hard-seat identity is retained; the oblique source camera is reconstructed as cardinal south.',
 'Parallel seat boundaries, horizontal back rails and vertical supports replace the diagonal display-model pose.',
 'Seat is hard wood despite pale native y tint; no fabric, upholstery, canvas sling or additional legs are invented.',
 'One native fixed view; actual sitting/physics/visibility and rare animated/custom fallback remain pending.']):d.text((20,695+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered corrected cardinal Chair with separate neutral hard-seat ownership.')
