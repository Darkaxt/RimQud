"""Neutral static mannequin and complete randomized-shell ownership, including highlights."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');assert source.size==(1024,1536)
structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5));structural.save(OUT/'opaque-structure-mask.png');selected.save(OUT/'selected-edge-mask.png')
cyan=Image.new('L',source.size);cyan.putdata([255 if a>=16 and g-r>=4 and b-r>=4 and min(g,b)>=20 else 0 for r,g,b,a in source.get_flattened_data()]);cyan.save(OUT/'shell-color-seed.png');near=cyan.filter(ImageFilter.MaxFilter(13))
primary=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);owner=Image.new('L',source.size);highlights=Image.new('L',source.size);pp=[];dp=[];op=[];hp=[]
for index,((r,g,b,a),edge,seed,close) in enumerate(zip(source.get_flattened_data(),selected.get_flattened_data(),cyan.get_flattened_data(),near.get_flattened_data())):
 if a<16 or not edge:pp.append((0,0,0,0));dp.append((0,0,0,0));op.append(0);hp.append(0);continue
 a=255 if a>=240 else a;inherited=bool(close) and min(r,g,b)>=225 and max(r,g,b)-min(r,g,b)<=18;owns=bool(seed) or inherited;v=max(g,b) if owns else round((r+g+b)/3)
 pp.append((v,v,v,a));dp.append((v,v,v,a if owns else 0));op.append(a if owns else 0);hp.append(a if inherited and not seed else 0)
primary.putdata(pp);detail.putdata(dp);owner.putdata(op);highlights.putdata(hp)
for name,im in [('neutral-master',primary),('shell-neutral-master',detail),('shell-ownership-mask',owner),('inherited-shell-highlight-mask',highlights)]:im.save(OUT/f'{name}.png')
primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS)
for im in [primary,detail]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.get_flattened_data()])
primary.save(OUT/'primary-neutral.png');detail.save(OUT/'detail-neutral.png');primary.getchannel('A').save(OUT/'coverage.png');detail.getchannel('A').save(OUT/'detail-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
def native(code):
 im=tint(primary,palette['y']);im.alpha_composite(tint(detail,palette[code]));return im
default=native('R');default.save(OUT/'default-y-R-preview.png')
for code in ['c','m','g']:native(code).save(OUT/f'illustrative-y-{code}-preview.png')
model=dict(entry='SCN-MANNEQUIN',kind='fixed_layered_furniture',blueprint='Mannequin',native_tiles=['Items/sw_mannequin.bmp'],source=asset(HERE/'source-packet.json'),primary=asset(OUT/'primary-neutral.png'),detail=asset(OUT/'detail-neutral.png'),coverage=asset(OUT/'coverage.png'),detail_coverage=asset(OUT/'detail-coverage.png'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One entire1024x1536frame maps once to256square for form, stand, right armature and both masks. No independently centered actor parts or contact normalization.'),
 palette=dict(primary='actual native armature/stem/base y',detail='actual chosen native Render.DetailColor from RandomColors=all; R is blueprint default only',neutral_preview='Warm raw wood tint and cyan shell markers are removed. Whole shell highlights inherit detail ownership; production RGB is equal.'),
 state_owner='Native RandomColors resolves actual detail tint. All shown color samples reuse exactly the same production geometry/masks; previews do not claim a captured random choice or alter its distribution.',
 equipment_boundary='Static mounted furniture graphic; no new actor body, apparel render path or independent arm/leg node. BodyType/rare Animated behavior retains native original fallback.',
 native_behavior='Preserve30-weight non-solid mounted furniture, non-takeability, AV2,Hitpoints80and rare animated/custom fallback. No donor training behavior.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(Path(__file__).resolve())],
 alpha='Actual opaque structure A>=224plus two-pixel edge allowance retains actual A>=16only near structure, normalizes>=240and clears invisible RGB. Remove detached exterior halo; preserve form/armature gaps and open base supports.',
 ownership='Cyan shell seed G-R>=4,B-R>=4,min(G,B)>=20plus near-white highlights minRGB>=225,range<=18within six pixels of cyan. Highlights belong to the fiberglass shell, not pale wood. No broad rectangular hull fills the concave shell cutouts. Warm wood and cyan pigments are neutralized.',
 registration='Complete source-cell mapping keeps head, torso/hip shells, left bent form, right jointed armature and stem/base in place. This furniture does not receive human actor contact normalization or new animation joints.',
 source_limits='Right-side marks and exact arm/joint/neck connections are uncertain authored interpretation. Static source form is not proof of a full native anatomy tree or new clothing system. No face, target, weapons or walking legs are added.',
 color_samples='Default R plus illustrative c/m/g use local native palette entries on identical files/geometry. Actual live RandomColors selection remains native and untested here.',
 omitted='One fixed ordinary furniture tile. No turnarounds, clothing fit, equipped-item overlays or fabricated animated mannequin are generated; native random color/physics/rare-animation acceptance stays deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,860),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'MANNEQUIN / static source form + armature + stand / neutral ownership > native y + randomized detail',font=font,fill='#e3cf43')
for x,im,label in [(45,primary,'Neutral / no baked wood or cyan'),(515,detail,'Isolated neutral randomized shell'),(985,default,'Default y + R / illustrative')]:
 big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,525),label,font=font,fill='#e3cf43')
 for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+40+i*85,580),small)
for i,line in enumerate(['Source head/torso/hip forms, bent side cues, stem and splayed base stay in one cell frame.',
 'Pale near-white shell highlights inherit randomized detail; wood armature and connectors remain primary y.',
 'Exact right armature/joints are authored interpretation. This is static furniture, not an actor/apparel rig.',
 'Random detail selection, source physics and rare animated/custom native acceptance remain pending.']):draw.text((20,695+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
samples=Image.new('RGB',(1440,760),'#142823');draw=ImageDraw.Draw(samples);draw.text((20,15),'NATIVE PALETTE SAMPLES / identical neutral textures and geometry / actual random choice stays native',font=font,fill='#e3cf43')
for i,code in enumerate(['R','c','m','g']):
 im=native(code).resize((240,360),Image.Resampling.LANCZOS);x=45+i*355;samples.paste(im,(x,80),im);draw.text((x,485),f'y frame / {code} detail'+(' (default)' if code=='R' else ' (sample)'),font=font,fill='#e3cf43')
draw.text((20,620),'Samples show mask ownership only: no new randomization, fixed red mannequin or captured live choice is claimed.',font=font,fill='#e5e8d8');samples.save(OUT/'palette-samples.png');print('Registered neutral static mannequin with shell-highlight ownership and native random-detail color boundary.')
