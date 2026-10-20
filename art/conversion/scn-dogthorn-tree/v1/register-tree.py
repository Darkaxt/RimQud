"""Two fixed-frame dogthorn variants; separate neutral foliage/wood ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Never overwrite recorded registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];index=json.loads((HERE/'native-state-index.json').read_text());states=[];decisions=[];previews={}
def tint(im,c):
 c=bytes.fromhex(c);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
for n in [1,2]:
 source=Image.open(HERE/f'refined-variant-{n}.png').convert('RGBA');assert source.size==(1024,1536)
 neutral=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);ownership=Image.new('L',source.size);coverage=Image.new('L',source.size);np=[];dp=[];op=[];ap=[]
 for r,g,b,a in source.getdata():
  if a<16:np.append((0,0,0,0));dp.append((0,0,0,0));op.append(0);ap.append(0);continue
  a=255 if a>=240 else a;wood=r-g>=8 and g-b>=8 and r>=25
  v=max(r,g,b) if wood else round((r+g+b)/3)
  np.append((v,v,v,a));dp.append((v,v,v,a if wood else 0));op.append(a if wood else 0);ap.append(a)
 neutral.putdata(np);detail.putdata(dp);ownership.putdata(op);coverage.putdata(ap)
 for name,im in [('neutral-master',neutral),('wood-neutral-master',detail),('wood-ownership-mask',ownership),('source-coverage-mask',coverage)]:im.save(OUT/f'variant-{n}-{name}.png')
 primary=neutral.resize((256,256),Image.Resampling.LANCZOS);secondary=detail.resize((256,256),Image.Resampling.LANCZOS)
 for im in [primary,secondary]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.getdata()])
 primary.save(OUT/f'variant-{n}-primary-neutral.png');secondary.save(OUT/f'variant-{n}-detail-neutral.png');primary.getchannel('A').save(OUT/f'variant-{n}-coverage.png');secondary.getchannel('A').save(OUT/f'variant-{n}-detail-coverage.png')
 native=tint(primary,palette['G']);native.alpha_composite(tint(secondary,palette['w']));native.save(OUT/f'variant-{n}-native-preview.png');previews[n]=(primary,secondary,native)
 states.append(dict(variant=n,native_tile=index['states'][n-1]['tile'],primary=asset(OUT/f'variant-{n}-primary-neutral.png'),detail=asset(OUT/f'variant-{n}-detail-neutral.png'),coverage=asset(OUT/f'variant-{n}-coverage.png'),detail_coverage=asset(OUT/f'variant-{n}-detail-coverage.png')))
 decisions.append(dict(variant=n,input=asset(HERE/f'refined-variant-{n}.png'),source_alpha_bounds=coverage.getbbox(),wood_bounds=ownership.getbbox(),registration='Same1024x1536full canvas to256x256recipient transform; no per-variant alpha-bounds fit, root crop or individual recentering.'))
model=dict(entry='SCN-DOGTHORN-TREE',kind='fixed_plant_variants',blueprint='Dogthorn Tree',source=asset(HERE/'source-packet.json'),states=states,
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='One common full-cell mapping for both fixed native cosmetic variants.'),
 palette=dict(primary='actual native foliage foreground G',detail='actual native exposed wood detail w',rule='Both saved albedo layers are grayscale; brown extraction aid is not baked into neutral mode.'),
 state_owner='Native RandomTile builder selects sw_fattree1 or2; no new state machine, wind simulation or rotated views.',
 native_behavior='Native visibility, occlusion, physics, hanging support and plant/damage exceptions remain source-owned. Unknown custom shapes retain native fallback.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(Path(__file__).resolve())],variants=decisions,alpha='Keep source alpha>=16, normalize>=240, clear invisible RGB; retain complete crown/roots and true gaps. Exterior preview glow is discarded rather than assigned to bark.',
 wood_ownership='Warm-brown opaque pixels R-G>=8,G-B>=8,R>=25 identify wood. Neutral leaves remain primary; wood mask includes exposed roots, bark splinters and visible branches. Both roles become equal RGB.',
 source_limits='Leaves, bark grain and tiny root surfaces are authored refinement. Exact root topology is not mechanically exported anatomy; do not infer native collision or species variants from it.',
 omitted='No creature turnarounds or clothing apply. Both declared native cosmetic variants are independently constructed/refined and registered.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,845),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'DOGTHORN / both native variants / neutral foliage + separate wood ownership / native G + w',font=font,fill='#e3cf43')
for x,(n,k,label) in zip([20,380,740,1100],[(1,0,'Variant1 / neutral'),(2,0,'Variant2 / neutral'),(1,2,'Variant1 / native G+w'),(2,2,'Variant2 / native G+w')]):
 im=previews[n][k];big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,65),big);draw.text((x,525),label,font=font,fill='#e3cf43')
 for t,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+30+t*85,580),small)
for i,line in enumerate(['Both actual RandomTile variants retain different source-inspired crown/root layouts and a common cell frame.',
 'Foliage stays native primary G; crooked trunk, pointed bark spines and wide tangled roots receive native detail w.',
 'Neutral images contain no baked brown or green. Wood extraction masks and independent layers are inspectable.',
 'Fixed plant views need no creature turnarounds or clothing. Native selection, visibility/occlusion acceptance pending.']):draw.text((20,680+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
# Display actual isolated wood roles for cut-edge ownership inspection.
plate=Image.new('RGB',(1152,650),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'DOGTHORN / isolated neutral wood masks / no foliage hue baked into roots',font=font,fill='#e3cf43')
for x,n in [(150,1),(720,2)]:
 im=previews[n][1].resize((288,432),Image.Resampling.LANCZOS);plate.paste(im,(x,65),im);draw.text((x,540),f'Variant{n} wood / detail only',font=font,fill='#e5e8d8')
plate.save(OUT/'wood-ownership-comparison.png');print('Registered both dogthorn variants with neutral wood/foliage layers in one fixed frame.')
