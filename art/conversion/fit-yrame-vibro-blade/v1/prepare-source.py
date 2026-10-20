"""Source-bound matte ionic-plastifer blade, full tool plus item-space grip."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,math,re,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');SIZE=(512,1024);FACES=['south','east','north']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+s+'</svg>'
blade='''<path d="M256 150 L274 194 L271 436 L267 478 L246 478 L241 436 L240 194Z" fill="#bdbdbd" stroke="#252525" stroke-width="5" stroke-linejoin="round"/>
<path d="M256 164 L256 458" fill="none" stroke="#a8a8a8" stroke-width="3"/>
<path d="M249 415 L249 457 M263 421 L262 461" fill="none" stroke="#717171" stroke-width="4" stroke-linecap="round"/>'''
hilt='''<path d="M245 477 Q233 476 230 487 L230 499 Q231 508 239 508 L245 499 L245 581 Q244 597 256 601 Q269 597 269 582 L267 499 L281 495 Q287 491 282 484 L267 479Z" fill="#777777" stroke="#252525" stroke-width="5" stroke-linejoin="round"/>
<path d="M251 515 L262 515 M251 537 L263 537 M251 559 L263 559 M251 582 L263 582" fill="none" stroke="#aaaaaa" stroke-width="3" stroke-linecap="round"/>'''
pattern=svg(blade+hilt);(HERE/'canonical-pattern.svg').write_text(pattern,encoding='utf-8');canonical=raster(pattern);canonical.save(HERE/'constructed-canonical.png');raster(svg(blade)).getchannel('A').save(HERE/'canonical-blade-region.png');raster(svg(hilt)).getchannel('A').save(HERE/'canonical-hilt-region.png')
# Full item remains unchanged. These are provisional ordinary upright display poses,
# not a ready/resting gameplay-state system or inferred attack animation.
controls={'south':dict(grip=[126,525],angle=0,crop=[0,60,256,572]),'east':dict(grip=[277,535],angle=-15,crop=[170,60,426,572]),'north':dict(grip=[380,525],angle=-10,crop=[256,60,512,572])}
def coefficients(c):
 a=math.radians(c['angle']);co,si=math.cos(a),math.sin(a);gx,gy=c['grip'];return [co,-si,256-co*gx+si*gy,si,co,570-si*gx-co*gy]
sheet=Image.new('RGBA',(1536,1024));neutral=sheet.copy();zoom=sheet.copy()
for i,f in enumerate(FACES):
 c=controls[f];c['inverse_affine']=coefficients(c);item=canonical.transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC);item.save(HERE/f'constructed-item-{f}.png');body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');mask=Image.new('L',SIZE);d=ImageDraw.Draw(mask)
 if f!='north':
  hx,hy=(111,525) if f=='south' else (267,535);d.ellipse((hx-34,hy-34,hx+34,hy+34),fill=255)
 mask.save(HERE/f'hand-visibility-{f}.png');a=np.array(body);hand=a.copy();hand[:,:,3]=np.minimum(a[:,:,3],np.array(mask));Image.fromarray(hand).save(HERE/f'original-hand-{f}.png');red=a.copy();red[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])))
 for target,base in [(sheet,Image.fromarray(red)),(neutral,body)]:
  assembled=Image.alpha_composite(item,base) if f=='north' else Image.alpha_composite(base,item)
  if f!='north':
   overlay=np.array(base);overlay[:,:,3]=np.minimum(overlay[:,:,3],np.array(mask));assembled=Image.alpha_composite(assembled,Image.fromarray(overlay))
  target.paste(assembled,(i*512,0))
  if target is sheet:zoom.paste(assembled.crop(c['crop']).resize(SIZE,Image.Resampling.LANCZOS),(i*512,0))
sheet.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-item-context.png');write(HERE/'fit-controls.json',controls)
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Vibro Blade');assert sha(DONOR/original['reference_file'])==original['reference_sha256']
actor=next(a for a in json.loads((ROOT/'art/village/sources.json').read_text())['actors'] if a['creature']=='Warden Yrame');resident=actor['native_instances'][0];binding=next(p for p in resident['parts'] if (p.get('equipped') or {}).get('blueprint')=='Vibro Blade');dp=DONOR/'held-sword.png';assert sha(dp)=='354435cab7416e253faa2c60994fb2b822e700f8fbbebde0ea72b3b3bf84f5fd'
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Items.xml');fragment=re.search(r'<object\s+Name="Vibro Blade"(?=\s|>).*?</object>',definitions.read_text(encoding='utf-8-sig'),re.S);assert fragment;obj=ET.fromstring(fragment.group())
write(HERE/'source-packet.json',dict(entry='FIT-YRAME-VIBRO-BLADE-HAND-2',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Warden Yrame',race='Human; ordinary female baseline for reusable equipment',original=original,observed_binding=binding,captured_resident=resident,installed_definition=dict(file=str(definitions),sha256=sha(definitions),object_xml=ET.tostring(obj,encoding='unicode')),source_resolution='Runtime captured generic unidentified-device text and weight3, while installed definition identifies matte ionic plastifer, finger-rest hilt, energy cell and weight2. Preserve both; reason for observed weight difference unknown. Charge state not exported here.',body=ref(BODY/'model.json'),donor_reference=dict(file=str(dp),sha256=sha(dp),game='RimWorld Core',name='Longsword',source_id=228,provenance=ref(ROOT/'evidence/pawns-stage4-result.json'),role='Actual extracted Core longsword: economical long-blade silhouette, hilt and flat held-item outline convention. Qud material/finger-rest/palette override polished metal and crossguard. No donor combat logic.'),rejected_reference=dict(file='D:/Steam/steamapps/workshop/content/294100/1814383360/Textures/Things/WeaponMelee/CombatKnife.png',role='Inspected actual Vanilla Weapons Expanded knife; blade proportions too short. Core longsword selected instead.'),design='Long narrow matte pointed blade, source root grooves, finger-rest hilt and short lower grip. No serrations, engraved runes, emissive aura, exaggerated crossguard or invented cell placement. Grooves interpret sparse root pixels rather than asserting unseen mechanism.',authored_scale='Approximately450 source pixels /42 pixels in48x96 view. Readable authored size, not a dimension inferred from weight.',frame=dict(canvas=list(SIZE),contact=[256,950],item_space_grip=[256,570],camera='Strict SEN body; one flat axial tool with per-facing angle/depth. West mirror is provisional ordinary right-hand display.',context_zoom_scale=2,context_crops={f:c['crop'] for f,c in controls.items()}),palette=dict(foreground='c',detail='y',detail_assignment='Primary matte blade / source-native contrasting hilt. Separate equal-RGB neutral textures; no teal or glow baked in.'),assembly_boundary='Actual Hand292 parent291 laterality2 has no mutation manager. Ordinary right-hand binding is retained; named Big shape, horns/rime details, extra feet and outfit remain unfinished. Resting/ready poses and actual native attachment await final assembly.',native_acceptance='Pending full-set generation and actual native equipped/pose state'))
plate=Image.new('RGB',(1536,850),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);d.text((20,15),'YRAME > HUMAN BASE > VIBRO BLADE / original identity; actual Core reference; own SEN',font=font,fill='#e3cf43')
orig=Image.open(DONOR/original['reference_file']).convert('RGBA').resize((160,240),Image.Resampling.NEAREST);plate.paste(orig,(24,80),orig);don=Image.open(dp).convert('RGBA');box=don.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();don=don.crop(box);don.thumbnail((270,150));plate.paste(don,(210,130),don)
for y,t in [(350,'Long matte ionic-plastifer blade'),(380,'Finger-rest hilt / native c and y'),(410,'Actual Hand292 / item576 / laterality2'),(440,'Original generic description retained'),(470,'Core Longsword: convention, not identity'),(500,'Charge motion / ready pose not authored')]:d.text((20,y),t,font=font,fill='#e5e8d8')
for i,f in enumerate(FACES):
 im=neutral.crop((i*512,0,(i+1)*512,1024));bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,512)),(535+i*330,70));d.text((535+i*330,600),f.upper()+' / ORDINARY PREVIEW',font=font,fill='#e3cf43');cx,cy=controls[f]['grip'];crop=im.crop((cx-60,cy-95,cx+65,cy+60));crop=crop.resize((150,186));plate.paste(crop,(580+i*330,635),crop)
plate.save(HERE/'source-comparison.png');print('Prepared matte blade, full finger-rest hilt, lower handle grip and exact ordinary Hand292/2 binding.')
