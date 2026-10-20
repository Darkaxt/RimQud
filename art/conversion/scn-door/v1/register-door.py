"""Split actual refined arch/leaf; derive a native-positioned open slate edge."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageChops,ImageFilter
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
assert not (OUT/'model.json').exists(),'Never overwrite recorded registrations'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
source=Image.open(HERE/'refined-proposal.png').convert('RGBA');assert source.size==(1024,1536)
binary=source.getchannel('A').point(lambda a:255 if a>=16 else 0)
parts={}
for name,seed in [('frame',(100,900)),('leaf',(500,900))]:
 selection=binary.convert('RGB');ImageDraw.floodfill(selection,seed,(255,0,0),thresh=0)
 mask=Image.new('L',source.size);mask.putdata([255 if p==(255,0,0) else 0 for p in selection.getdata()])
 bounds=mask.getbbox();assert bounds is not None
 if name=='frame':assert bounds[0]<100 and bounds[2]>900 and bounds[1]<100
 else:assert 150<bounds[0]<250 and 750<bounds[2]<900 and bounds[1]>250
 mask.save(OUT/f'source-selection-{name}.png')
 cleaned=Image.new('RGBA',source.size)
 pixels=[]
 for rgba,owned in zip(source.getdata(),mask.getdata()):
  r,g,b,a=rgba
  if not owned:pixels.append((0,0,0,0));continue
  v=round((r+g+b)/3);pixels.append((v,v,v,255 if a>=240 else a))
 cleaned.putdata(pixels);cleaned.save(OUT/f'cleaned-{name}.png')
 parts[name]=cleaned.resize((512,768),Image.Resampling.LANCZOS)
 for y in range(768):
  for x in range(512):
   r,g,b,a=parts[name].getpixel((x,y))
   if a<8:parts[name].putpixel((x,y),(0,0,0,0))
   else:
    v=round((r+g+b)/3);parts[name].putpixel((x,y),(v,v,v,a))
# The frame is the same saved component for both states. Open is the native
# left edge-on panel, never a mirrored door or independently re-fitted frame.
edge_mask=Image.open(HERE/'constructed-open.png').convert('RGBA').getchannel('A')
# The manual open also contains a frame. Keep only the native leaf-strip ROI.
roi=Image.new('L',(512,768));ImageDraw.Draw(roi).rectangle((92,184,132,710),fill=255)
edge_mask=ImageChops.multiply(edge_mask,roi);box=edge_mask.getbbox()
material=parts['leaf'].crop((230,192,252,704)).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
edge=Image.new('RGBA',(512,768));edge.paste(material,box[:2]);edge.putalpha(edge_mask)
boundary=ImageChops.subtract(edge_mask,edge_mask.filter(ImageFilter.MinFilter(5)))
for y in range(box[1],box[3]):
 for x in range(box[0],box[2]):
  r,g,b,a=edge.getpixel((x,y));v=round((r+g+b)/3)
  if boundary.getpixel((x,y))>100:v=52
  elif x<box[0]+6:v=min(225,v+28)
  edge.putpixel((x,y),(v,v,v,a))
edge.save(OUT/'open-edge-neutral-master.png')
native_palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];fg=bytes.fromhex(native_palette['y']);bg='#'+native_palette['k']
model=dict(entry='SCN-DOOR',kind='stateful_object',native_frame=[16,24],manual_frame=[512,768],recipient_frame=[256,256],anchor=[8,16],
 state_owner='Native Door.SyncRender selects exact ClosedTile/OpenTile. No donor motion, state timer, solid/occlusion or input code is added.',
 mapping_rule='One full-canvas mapping for both states and all layers; never fit each alpha bounding box. Closed/basic and original blueprint thumbnail resolve to closed. Unknown/custom tiles retain native fallback.',
 original_states=asset(HERE/'native-state-index.json'),source_packet=asset(HERE/'source-packet.json'),
 palette=dict(primary='actual native foreground y',detail='actual native detail y',current_rgb=native_palette['y'],rule='Separate neutral leaf/frame roles; no baked tan, teal or rust orange.'),states={},native_acceptance='Pending all-conversions-generated gate')
assemblies={};native_previews={}
for state,leaf in [('closed',parts['leaf']),('open',edge)]:
 rows=[]
 for component,image,role in [('leaf',leaf,'foreground'),('frame',parts['frame'],'detail')]:
  path=OUT/f'{state}-{component}-neutral.png';final=image.resize((256,256),Image.Resampling.LANCZOS);final.save(path)
  coverage=OUT/f'{state}-{component}-coverage.png';final.getchannel('A').save(coverage)
  rows.append(dict(component=component,color_role=role,texture=asset(path),coverage=asset(coverage)))
 assembly=Image.alpha_composite(leaf,parts['frame']);assemblies[state]=assembly
 preview=Image.new('RGBA',assembly.size,bg);tinted=Image.new('RGBA',assembly.size)
 tinted.putdata([(*[round(v*c/255) for c in fg],a) for v,_,_,a in assembly.getdata()]);preview.alpha_composite(tinted);native_previews[state]=preview
 model['states'][state]=dict(native_tiles=([x['tile'] for x in json.loads((HERE/'native-state-index.json').read_text())['states'] if x['state'] in ['closed','blueprint-thumbnail']] if state=='closed' else ['Assets_Content_Textures_Tiles_sw_door_basic_open.bmp']),layers=rows,solid_occluding='native closed' if state=='closed' else 'native open')
 assembly.save(OUT/f'{state}-neutral-composition.png');preview.save(OUT/f'{state}-native-preview.png')
assert (OUT/'closed-frame-neutral.png').read_bytes()==(OUT/'open-frame-neutral.png').read_bytes()
assert (OUT/'closed-frame-coverage.png').read_bytes()==(OUT/'open-frame-coverage.png').read_bytes()
assert Image.open(OUT/'open-leaf-neutral.png').getchannel('A').getbbox()[2]<75,'Open panel must stay at native left edge'
decisions=dict(inputs=[asset(HERE/'refined-proposal.png'),asset(HERE/'constructed-open.png'),asset(Path(__file__).resolve())],
 extraction='Connected alpha components selected from actual refined output at threshold16. Invisible pixels cleared, nearly opaque interiors normalized and RGB made equal. One full-canvas downsample for both layers.',
 frame_ownership='Refined outer arch is detail-owned (source R255). It is exactly byte-identical between states.',
 leaf_ownership='Refined inner slate slab and its small hinges are foreground-owned (source R0). No frame or transparent gap is baked into it.',
 open_edge='Authored from the actual native left strip geometry; same selected slate material sampled away from front handle/handprint. No additional ImageGen call or unseen rear view is claimed.',
 derived_state='Open uses common arch plus edge-on leaf x3..4,y6..22. Foreground behind opening remains visible; native controls actual state and occlusion.',
 source_limits='Appearance extraction is authoring; no evidence yet of native replacement dispatch/state ordering.')
(OUT/'registration-decisions.json').write_bytes((json.dumps(decisions,indent=2)+'\n').encode())
(OUT/'model.json').write_bytes((json.dumps(model,indent=2)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,825),'#142823');d=ImageDraw.Draw(plate)
d.text((20,15),'DOOR / selected fixed-frame states / neutral layers and native y palette',font=font,fill='#e3cf43')
for x,(state,image) in zip([20,380,740,1100],[('closed / neutral',assemblies['closed']),('open / neutral',assemblies['open']),('closed / native y',native_previews['closed']),('open / native y',native_previews['open'])]):
 tile=Image.new('RGBA',(512,768),'#20382d');tile.alpha_composite(image);plate.paste(tile.convert('RGB').resize((288,432),Image.Resampling.LANCZOS),(x,65));d.text((x,518),state,font=font,fill='#e3cf43')
 for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
  small=image.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+30+i*85,570),small)
for i,line in enumerate(['Open and closed use byte-identical arch pixels and the same cell anchor; the state does not re-center either part.',
 'Leaf is primary-owned; arch is detail-owned. Both currently use native y. Neutral view is grayscale with separate alpha.',
 'Open slate edge follows the actual left strip and samples the same slate material without the front handle.',
 'No creature turnarounds or clothing apply. Native visibility, input and open/close integration acceptance remain pending.']):d.text((20,670+32*i),line,font=font,fill='#e5e8d8')
plate.save(OUT/'states-comparison.png')
print('Registered two source-bound Door states; identical arch bytes and shared source frame.')
