"""Four actual source cushion patterns, neutral fabric and separate lower binding."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter,ImageChops
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
variants=[];decisions=[];previews=[]
for n in range(1,5):
 source=Image.open(HERE/f'refined-variant-{n}.png').convert('RGBA');assert source.size==(1024,1536)
 structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5))
 structural.save(OUT/f'variant-{n}-opaque-structure-mask.png');selected.save(OUT/f'variant-{n}-selected-edge-mask.png')
 owner=Image.new('L',source.size);owner.putdata([255 if a>=16 and g-r>=4 and b-r>=4 and min(g,b)>=20 else 0 for r,g,b,a in source.get_flattened_data()]);owner.save(OUT/f'variant-{n}-binding-ownership-mask.png')
 primary=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);pp=[];dp=[]
 for (r,g,b,a),edge,owns in zip(source.get_flattened_data(),selected.get_flattened_data(),owner.get_flattened_data()):
  if a<16 or not edge:pp.append((0,0,0,0));dp.append((0,0,0,0));continue
  a=255 if a>=240 else a;v=max(g,b) if owns else round((r+g+b)/3);pp.append((v,v,v,a));dp.append((v,v,v,a if owns else 0))
 primary.putdata(pp);detail.putdata(dp);primary.save(OUT/f'variant-{n}-neutral-master.png');detail.save(OUT/f'variant-{n}-binding-neutral-master.png')
 primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS)
 for im in [primary,detail]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.get_flattened_data()])
 primary.save(OUT/f'variant-{n}-primary-neutral.png');detail.save(OUT/f'variant-{n}-detail-neutral.png');primary.getchannel('A').save(OUT/f'variant-{n}-coverage.png');detail.getchannel('A').save(OUT/f'variant-{n}-detail-coverage.png')
 native=tint(primary,palette['w']);native.alpha_composite(tint(detail,palette['y']));native.save(OUT/f'variant-{n}-native-w-y-preview.png')
 variants.append(dict(variant=n,native_tile=f'Items/sw_cushion{n}.bmp',primary=asset(OUT/f'variant-{n}-primary-neutral.png'),detail=asset(OUT/f'variant-{n}-detail-neutral.png'),coverage=asset(OUT/f'variant-{n}-coverage.png'),detail_coverage=asset(OUT/f'variant-{n}-detail-coverage.png')))
 decisions.append(dict(variant=n,input=asset(HERE/f'refined-variant-{n}.png'),actual_opaque_cyan_bounds=ImageChops.multiply(owner,structural).getbbox(),pattern=['Three-dimple/star fold','Four diamond-arranged dimples','Plain top/lower folds','Three diagonal dimples/crease'][n-1]));previews.append((primary,detail,native))
model=dict(entry='SCN-FLOOR-CUSHION',kind='fixed_layered_furniture_variants',blueprint='Floor Cushion',source=asset(HERE/'source-packet.json'),variants=variants,
 default_tile_binding=dict(native_tile='Items/sw_floor_cushion.png',variant=1,reason='Exact default coverage and source shader-relevant R wherever covered match variant1. Invisible RGB differs; not raw RGBA identity.'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='Every entire1024x1536frame maps once to256square. No separate tuft-pattern, cushion/body or binding bbox fitting. Review plate uses one identical display-only window after restoring physical2:3aspect; production files retain full canvas.'),
 palette=dict(primary='actual native stuffed fabric w',detail='actual native lower/front binding y',neutral_preview='All production layers are equal-RGB neutral; cyan authoring aid is removed. Tuft indents remain shaded opaque primary fabric.'),
 state_owner='Native RandomTile chooses four cosmetic patterns, not orientations. Default visible shape binds to variant1; no new packed/occupied state.',native_behavior='Preserve native Chair Level-1,2-weight BaseChair-derived furniture, inherited takeability/cover, non-occlusion and rare Animated/custom fallback. Stuffing does not add glow or loose feathers. No donor seating mechanics.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(Path(__file__).resolve()),asset(HERE/'source-packet.json')],variants=decisions,
 alpha='Actual opaque structure A>=224plus two-pixel edge allowance; retain actual A>=16only there, normalize>=240and clear invisible RGB. Remove detached exterior halo. Cushion fabric stays opaque through tufts and creases.',
 ownership='Actual cyan binding G-R>=4,B-R>=4,min(G,B)>=20is neutralized with max(G,B). Gray upper fabric/buttons/creases remain mean-RGB primary. Inspected opaque cyan bounds lie only on lower/front binding, not upper fabric.',
 registration='Same full native-cell mapping for all four whole cushions and each role mask. Review crop is a fixed shared window from restored288x432display frames, y125..325; it is not a production texture crop or per-variant centering.',
 source_limits='Tuft count/positions and folds follow native visible patterns as authored cloth interpretation. They are not faces, physical holes, mechanical attachment nodes or loose/luminous stuffing. Variant3 keeps its plain top.',
 omitted='Four source cosmetic patterns require four real refinements. No creature turnarounds, clothing or invented sitting/packed sprite states apply. Native seating/physics/visibility/rare-animation acceptance remains deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,1450),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'FLOOR CUSHION / four native patterns / neutral stuffed fabric + binding > actual native w + y',font=font,fill='#e3cf43')
for row,ims in enumerate(previews):
 top=65+row*300
 for x,im,label in zip([45,515,985],ims,['Neutral whole cushion','Separate neutral binding','Native w fabric + y binding']):
  big=im.resize((288,432),Image.Resampling.LANCZOS).crop((0,125,288,325));plate.paste(big,(x,top),big);draw.text((x,top+205),f'Variant{row+1} / '+label,font=font,fill='#e3cf43')
  for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
   small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+40+i*85,top+240),small)
for i,line in enumerate(['Three-dimple/star, four-point tufts, plain top/lower folds and diagonal creases remain distinct actual variants.',
 'Fabric/tufts are opaque. Only lower/front binding receives y. No baked cyan, faces, loose feathers or glow.',
 'Enlarged panels use one common review window; production retains the full identical source-cell frame.',
 'Default thumbnail visibly binds to variant1. Native selection/seating/cover/rare-animation acceptance stays pending.']):draw.text((20,1305+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered four neutral cushion patterns, lower binding masks and default visible-equivalent binding.')
