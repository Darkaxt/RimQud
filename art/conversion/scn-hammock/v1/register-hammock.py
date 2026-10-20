"""Neutral native-state hammock layers with real open lattice and tile-specific color."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Preserve logged registration'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,color):
 c=bytes.fromhex(color);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
states=[];previews=[]
for state,tile in [('unhung','Items/sw_shawl.bmp'),('hanging','Items/sw_hammock.bmp')]:
 source=Image.open(HERE/f'refined-{state}.png').convert('RGBA');assert source.size==(1024,1536)
 structural=source.getchannel('A').point(lambda a:255 if a>=224 else 0);selected=structural.filter(ImageFilter.MaxFilter(5));structural.save(OUT/f'{state}-opaque-structure-mask.png');selected.save(OUT/f'{state}-selected-edge-mask.png')
 owner=Image.new('L',source.size);owner.putdata([255 if a>=16 and g-r>=4 and b-r>=4 and min(g,b)>=20 else 0 for r,g,b,a in source.get_flattened_data()]);owner.save(OUT/f'{state}-bright-strand-ownership-mask.png')
 primary=Image.new('RGBA',source.size);detail=Image.new('RGBA',source.size);pp=[];dp=[]
 for (r,g,b,a),edge,owns in zip(source.get_flattened_data(),selected.get_flattened_data(),owner.get_flattened_data()):
  if a<16 or not edge:pp.append((0,0,0,0));dp.append((0,0,0,0));continue
  a=255 if a>=240 else a;v=max(g,b) if owns else round((r+g+b)/3);pp.append((v,v,v,a));dp.append((v,v,v,a if owns else 0))
 primary.putdata(pp);detail.putdata(dp);primary.save(OUT/f'{state}-neutral-master.png');detail.save(OUT/f'{state}-bright-strand-neutral-master.png')
 primary=primary.resize((256,256),Image.Resampling.LANCZOS);detail=detail.resize((256,256),Image.Resampling.LANCZOS)
 for im in [primary,detail]:im.putdata([(0,0,0,0) if a<4 else (round((r+g+b)/3),)*3+(a,) for r,g,b,a in im.get_flattened_data()])
 primary.save(OUT/f'{state}-primary-neutral.png');detail.save(OUT/f'{state}-detail-neutral.png');primary.getchannel('A').save(OUT/f'{state}-coverage.png');detail.getchannel('A').save(OUT/f'{state}-detail-coverage.png')
 native=tint(primary,palette['y']);native.alpha_composite(tint(detail,palette['Y']));native.save(OUT/f'{state}-native-y-Y-preview.png')
 states.append(dict(state=state,native_tile=tile,primary=asset(OUT/f'{state}-primary-neutral.png'),detail=asset(OUT/f'{state}-detail-neutral.png'),coverage=asset(OUT/f'{state}-coverage.png'),detail_coverage=asset(OUT/f'{state}-detail-coverage.png')));previews.append((primary,detail,native))
model=dict(entry='SCN-HAMMOCK',kind='native_state_layered_furniture',blueprint='Hammock',source=asset(HERE/'source-packet.json'),states=states,
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],method='Each complete native-state1024x1536frame maps once to256square. No independent mesh/fringe/end-tip fitting or per-state alpha-bounds centering.'),
 palette=dict(primary='explicit native TileColor y, not glyph-only ColorString Y',detail='actual native Y bright strands',neutral_preview='Main ropes, former warm raw highlights and cyan markers are all neutralized. Selected production RGB channels are equal.'),
 state_owner='Native Hangable support/lifecycle owns Hanging. Render changes E.Tile to Items/sw_hammock.bmp only while hanging; default is Items/sw_shawl.bmp. Artwork does not create support rules or switch state.',
 native_behavior='Keep original Bed/Hangable,2-weight organic takeable non-solid physics, Hitpoints5and support checks. No baked trees/stand, moving ropes, fishing/vehicle behavior or unsupported new state. Native acceptance remains pending.',native_acceptance='Pending every-conversion-generated gate')
record=dict(inputs=[asset(HERE/'refined-unhung.png'),asset(HERE/'refined-hanging.png'),asset(Path(__file__).resolve())],
 alpha='Actual A>=224structure plus two-pixel allowance retains actual A>=16only near structure, normalizes>=240and clears invisible RGB. Exclude detached exterior/mesh-hole soft halo while retaining actual rope edges and open mesh. Original raw generations remain unchanged.',
 ownership='Cyan-designated fringe/selected strands/inner hanging edge use G-R>=4,B-R>=4,min(G,B)>=20and neutral max(G,B). Other rope/braids use neutral mean-RGB, removing the warm raw fiber tint. Detail is a rope color role, not a new material or equipment layer.',
 registration='Full source-cell mapping keeps both original state silhouettes and selected fringe/edge masks together. Native endpoint/support acceptance is explicitly pending; these are authored cell coordinates, not verified world attachments.',
 source_interpretation='Lattice openings are supported by the rope-lattice description, unlike opaque cushions. Exact braid texture, grid spacing, crossing order and small center frays remain authored interpretation. No opaque cloth backing, mannequin, baked support or animation is introduced.',
 omitted='Two real native states each received their own actual refinement. No extra donor facings or clothing fitting apply. Native support transitions, sleep, visibility and source physics acceptance stay deferred.')
for name,value in [('model.json',model),('registration-decisions.json',record)]: (OUT/name).write_bytes((json.dumps(value,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,1480),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'BRINESTRAW HAMMOCK / two real native states / neutral rope + bright strands > TileColor y + detail Y',font=font,fill='#e3cf43')
for row,ims in enumerate(previews):
 top=65+row*630
 for x,im,label in zip([45,515,985],ims,['Neutral rope lattice','Separate neutral bright strands','Native y main + Y detail']):
  big=im.resize((288,432),Image.Resampling.LANCZOS);plate.paste(big,(x,top),big);draw.text((x,top+450),('Unhung' if row==0 else 'Hanging')+' / '+label,font=font,fill='#e3cf43')
  for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
   small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+40+i*85,top+505),small)
for i,line in enumerate(['Portable loop/fringe and deep diagonal hanging sling retain their actual native state identities.',
 'Lattice holes stay open; warm raw fiber tint/cyan markers are removed from neutral production layers.',
 'Native TileColor y overrides glyph-only ColorString Y for these tile previews; bright detail remains Y.',
 'Support checks, hanging transition, endpoints, sleep, visibility and source physics acceptance remain pending.']):draw.text((20,1320+i*32),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print('Registered real portable/hanging hammock states, neutral mesh and explicit native y/Y tile roles.')
