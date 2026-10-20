"""Two Qud almond lenses on the original older-human head, separate from body art."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,io,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-male-older/v2'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');MOD=Path('D:/Steam/steamapps/workshop/content/294100/1814987817')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def ext(p):return dict(path=p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),publication='Private installed reference, not copied to repository')
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+s+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
almonds='M194 100 Q223 77 251 100 Q225 121 194 100Z M261 100 Q289 77 317 100 Q288 121 261 100Z'
temples='M195 99 Q183 97 174 116 L171 128 M316 99 Q329 97 338 116 L341 128 M251 99 Q256 94 261 99'
rearhooks='M174 116 Q161 120 168 135 M338 116 Q351 120 344 135'
outlines=dict(south=almonds,east='M332 86 Q343 99 333 115 Q326 100 332 86Z',north=almonds)
wires=dict(south=temples,east='M333 94 Q286 73 220 111 L215 126',north=temples+' '+rearhooks)
glints=dict(south='M207 98 Q223 87 235 95 M273 98 Q289 87 302 96',east='M333 94 Q337 99 334 105',north='M207 98 Q223 87 235 95 M273 98 Q289 87 302 96')
assert not (HERE/'source-packet.json').exists();contexts=[];assemblies={};font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for f in ['south','east','north']:
 wire='<path d="'+wires[f]+'" fill="none" stroke="#2b2b2b" stroke-width="4.5" stroke-linecap="round"/><path d="'+wires[f]+'" fill="none" stroke="#c8c8c8" stroke-width="2.2" stroke-linecap="round"/>'
 lens='<path d="'+outlines[f]+'" fill="#ededed" fill-opacity=".13" stroke="#292929" stroke-width="5"/><path d="'+outlines[f]+'" fill="none" stroke="#cdcdcd" stroke-width="2.4"/>'
 detail='<path d="'+glints[f]+'" fill="none" stroke="white" stroke-width="2.6" stroke-linecap="round"/>'
 for prefix,s in [('pattern',wire+lens+detail),('detail-region',detail)]:
  source=svg(s);(HERE/f'{prefix}-{f}.svg').write_bytes(source.encode());raster(source).save(HERE/f'constructed-{prefix}-{f}.png')
 item=raster(svg(wire+lens+detail));body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');head=Image.open(BODY/f'head-{f}.png').convert('RGBA');overlay=head if f=='north' else Image.new('RGBA',body.size);overlay.save(HERE/f'body-overlay-{f}.png');overlay.getchannel('A').save(HERE/f'body-visibility-{f}.png')
 a=np.array(body);gray=a[:,:,:3].mean(2);a[:,:,:3]=np.uint8(np.round(gray[:,:,None]*np.array([1,.1,.1])));red=Image.fromarray(a);redoverlay=red.copy();redoverlay.putalpha(overlay.getchannel('A'));contexts.append(Image.alpha_composite(Image.alpha_composite(red,item),redoverlay));assembly=Image.alpha_composite(Image.alpha_composite(Image.alpha_composite(body,item),raster(svg(detail))),overlay);assembly.save(HERE/f'constructed-assembly-{f}.png');assemblies[f]=assembly
sheet=Image.new('RGBA',(1536,1024))
for i,im in enumerate(contexts):sheet.alpha_composite(im.crop((64,0,448,384)).resize((512,512),Image.Resampling.LANCZOS),(i*512,256))
sheet.save(HERE/'constructed-red-head-context.png');assemblies['west (mirror)']=ImageOps.mirror(assemblies['east']);plate=Image.new('RGB',(1152,460),'#142823');draw=ImageDraw.Draw(plate);draw.text((18,14),'SPECTACLES / almond glass in thin wireframe cups; original head and rear depth',font=font,fill='#e3cf43')
for i,(f,im) in enumerate(assemblies.items()):
 bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*284;plate.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,80));draw.line((x+128,80,x+128,336),fill='#e3cf43');draw.text((x,360),f.upper(),font=font,fill='#e3cf43')
draw.text((18,422),'Complete frames/glass retained behind the rear head mask. No invented eyes, hair, strap or monocle.',font=font,fill='#e5e8d8');plate.save(HERE/'constructed-headwear-comparison.png')
lp=ROOT/'evidence/conversion-ledger.json';d=json.loads(lp.read_text());e=next(e for e in d['entries'] if e['id']=='FIT-IRUDAD-SPECTACLES-FACE-0');assert d['active_entry']==e['id'];item=next(e for e in d['entries'] if e['id']=='ITEM-SPECTACLES')['metadata']['original_reference'];assert hashlib.sha256((DONOR/item['reference_file']).read_bytes()).hexdigest()==item['reference_sha256'];actor=next(e for e in d['entries'] if e['id']=='NPC-ELDERBOB');part=next(p for p in actor['metadata']['native_parts'] if (p.get('equipped') or {}).get('blueprint')=='Spectacles');assert part['type']=='Face' and part['manager'] is None and part['laterality']==0
packet=dict(entry=e['id'],workflow='regional-curved-v1',item=item,actual_face_binding=part,body=ref(BODY/'model.json'),reference=ext(DONOR/item['reference_file']),donor=dict(mod='Vanilla Apparel Expanded',workshop_id='1814987817',about=ext(MOD/'About/About.xml'),assets=[ext(MOD/f'Textures/Things/Headgear/Glasses/Glasses_{f}.png') for f in ['south','east','north']],role='Directional face attachment, profile temple and rear hook visibility; donor rectangular heavy frame is replaced by Qud thin wire cups and almond glass.'),design='Two almond glass lenses in thin wire rims, small bridge, simple temple wires/hooks and restrained glass glints. Profile lens is edge-on; no dark opaque sunglasses, round monocle, pupils, hair or broad strap.',palette=dict(primary='y',detail='Y',assignment='Pale native frame with separate white lens glints; neutral RGB/alpha source before tint.'),frame=dict(canvas=[512,1024],contact=[256,950],zoom_crop=[64,0,448,384],zoom_scale=4/3,zoom_origin_y=256,facings=['south','east','north'],west='Mirror east; symmetric paired lenses'),depth='Keep complete physical frames and transparent glass. Original head overlays hidden rear frame surfaces; front/profile are near-side equipment above head.',mutations='Unmutated older-human base only. Irudad mutation-body and full NPC outfit remain unfinished; this actual ordinary Face/0 binding does not complete them.',native_acceptance='Pending full-set generation gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
for step,action,ns in [('source_identity_description_slot_laterality','Resolved actual two-almond glass/wire-cup description, original sprite/y-Y palette and Irudad ordinary Face part 198/item 540.',['source-packet.json']),('select_correct_body_and_references','Selected unchanged older-human base and inspected actual Vanilla Apparel Expanded SEN Glasses assets for directional attachment only. Qud almond lenses and thin wire identity override the donor heavy rectangular frame.',['source-packet.json']),('construct_and_overlay_one_item','Constructed full paired almond lenses, bridge and temples in SEN, separate glints and original-head rear depth, with common fixed frame/contact.',['constructed-headwear-comparison.png','constructed-red-head-context.png','pattern-south.svg','pattern-east.svg','pattern-north.svg'])]:
 e['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,action=action,inputs=[ref(HERE/'prepare-source.py'),ref(BODY/'model.json')],outputs=[ref(HERE/n) for n in ns],review='Prepared source-bound candidate. Inspect lens shape, profile and rear visibility before refinement; no native validation.',result='CANDIDATE' if step.startswith('construct') else 'PASS'))
e['current_step']='construct_and_overlay_one_item';d['updated_at']=datetime.now(timezone.utc).isoformat();lp.write_bytes((json.dumps(d,indent=2)+'\n').encode());print('Spectacles source and paired almond/wire construction prepared; review pending.')
