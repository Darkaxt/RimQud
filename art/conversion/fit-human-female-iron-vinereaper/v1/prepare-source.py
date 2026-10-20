"""Qud crescent iron vinereaper; female baseline fitting and full item source."""
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
shaft='''<path d="M248 328 Q256 320 265 328 L265 600 Q265 615 256 618 Q247 615 247 601Z" fill="#929292" stroke="#252525" stroke-width="5"/>
<path d="M253 363 L253 557" fill="none" stroke="#afafaf" stroke-width="3" stroke-linecap="round"/>'''
head='''<path d="M160 250 C237 235 288 282 289 338 C291 399 238 435 162 413 C202 400 226 374 226 338 C226 301 204 273 160 250Z" fill="#b7b7b7" stroke="#252525" stroke-width="5" stroke-linejoin="round"/>
<path d="M173 254 C232 252 276 290 277 338 C279 385 234 418 176 411" fill="none" stroke="#d9d9d9" stroke-width="4" stroke-linecap="round"/>
<path d="M257 316 L270 316 M257 344 L270 344" fill="none" stroke="#696969" stroke-width="3" stroke-linecap="round"/>'''
pattern=svg(shaft+head);(HERE/'canonical-pattern.svg').write_text(pattern,encoding='utf-8');canonical=raster(pattern);canonical.save(HERE/'constructed-canonical.png');raster(svg(head)).getchannel('A').save(HERE/'canonical-head-region.png');raster(svg(shaft)).getchannel('A').save(HERE/'canonical-shaft-region.png')
# Full item remains unchanged. These are provisional ordinary upright display poses,
# not a ready/resting gameplay-state system or inferred attack animation.
controls={'south':dict(grip=[126,525],angle=0,mirror=False,crop=[0,130,256,642]),'east':dict(grip=[277,535],angle=-25,mirror=False,crop=[220,130,476,642]),'north':dict(grip=[380,525],angle=0,mirror=True,crop=[256,130,512,642])}
def coefficients(c):
 a=math.radians(c['angle']);co,si=math.cos(a),math.sin(a);gx,gy=c['grip'];return [co,-si,256-co*gx+si*gy,si,co,580-si*gx-co*gy]
sheet=Image.new('RGBA',(1536,1024));neutral=sheet.copy();zoom=sheet.copy()
for i,f in enumerate(FACES):
 c=controls[f];c['inverse_affine']=coefficients(c);source=canonical.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if c['mirror'] else canonical;item=source.transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC);item.save(HERE/f'constructed-item-{f}.png');body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');mask=Image.new('L',SIZE);d=ImageDraw.Draw(mask)
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
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Iron Vinereaper');assert sha(DONOR/original['reference_file'])==original['reference_sha256']
actors=json.loads((ROOT/'art/village/sources.json').read_text())['actors'];bindings=[]
for actor in actors:
 for resident in actor['native_instances']:
  if resident.get('gender')=='female':
   for part in resident['parts']:
    if (part.get('equipped') or {}).get('blueprint')=='Iron Vinereaper':bindings.append(dict(creature=actor['creature'],resident={k:v for k,v in resident.items() if k!='parts'},part=part))
assert len(bindings)==4
mod=Path('D:/Steam/steamapps/workshop/content/294100/1814383360');dp=mod/'Textures/Things/WeaponMelee/Axe.png';rejected=Path('D:/Steam/steamapps/workshop/content/294100/2352893469/Common/Textures/Things/Item/Equipment/WeaponMelee/HDM_FlintSickle.png')
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Items.xml');fragment=re.search(r'<object\s+Name="Iron Vinereaper"(?=\s|>).*?</object>',definitions.read_text(encoding='utf-8-sig'),re.S);assert fragment;obj=ET.fromstring(fragment.group())
write(HERE/'source-packet.json',dict(entry='FIT-HUMAN-FEMALE-IRON-VINEREAPER-HAND-2',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Observed female Joppa farmers and convert; shared race fitting',race='Human, ordinary female baseline',original=original,observed_bindings=bindings,installed_definition=dict(file=str(definitions),sha256=sha(definitions),object_xml=ET.tostring(obj,encoding='unicode')),source_resolution='Runtime and installed description agree on wrought-iron crescent for watervine. Actual head/shaft form follows glyph; shaft material not explicitly stated, so no wood grain or bindings are invented.',body=ref(BODY/'model.json'),donor_reference=dict(file=str(dp),sha256=sha(dp),mod='Vanilla Weapons Expanded',workshop_id='1814383360',about_sha256=sha(mod/'About/About.xml'),role='Actual Axe texture: flat crescent cutting-head and straight-shaft readability. Qud head silhouette and material govern reconstruction; no combat code or occupation posture.'),rejected_reference=dict(file=str(rejected),sha256=sha(rejected),mod='Primitive Tools',workshop_id='2352893469',role='Inspected flint sickle; composite chipped teeth and bent wooden handle conflict with wrought-iron crescent. Not selected.'),design='Forged crescent head with open inner curve and simple straight shaft; same tool in every facing. Head mounted at shaft end; restrained edge shading. No teeth, wraps, wood grain, gems or invented farmer costume.',authored_scale='Approximately380 source pixels /36 pixels in48x96 preview. Authored readable scale, not dimension inferred from weight.',frame=dict(canvas=list(SIZE),contact=[256,950],item_space_grip=[256,580],camera='Strict SEN body; stationary upright/diagonal authoring display, not ready/drafted pose. Back mirrors unmarked blade surface to show opposite side. West mirrors profile.',context_zoom_scale=2,context_crops={f:c['crop'] for f,c in controls.items()}),palette=dict(foreground='y',detail='y',detail_assignment='Original differentiates head and shaft masks but maps both to native y. Preserve separate material regions without inventing a new color.'),assembly_boundary='All four captured female equipment bindings are ordinary Hand/laterality2 with no mutation manager. Generic body fit does not complete named cosmetics/outfits. Ready one-handed weapons project forward/horizontally in side view, about90 degrees to upright body; final pose/state work remains after full generation.',native_acceptance='Pending full-set generation and actual native equipment/resting-ready state'))
plate=Image.new('RGB',(1536,850),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);d.text((20,15),'HUMAN FEMALE > IRON VINEREAPER / original crescent; actual mod axe; own SEN',font=font,fill='#e3cf43')
orig=Image.open(DONOR/original['reference_file']).convert('RGBA').resize((160,240),Image.Resampling.NEAREST);plate.paste(orig,(24,80),orig);don=Image.open(dp).convert('RGBA');box=don.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();don=don.crop(box);don.thumbnail((270,150));plate.paste(don,(210,130),don)
for y,t in [(350,'Wrought-iron crescent / watervine tool'),(380,'Native head y / shaft y'),(410,'4 observed female Hand/2 bindings'),(440,'No mutation managers / no invented grip bones'),(470,'Actual mod Axe: flat crescent convention'),(500,'Display poses only; ready pose pending')]:d.text((20,y),t,font=font,fill='#e5e8d8')
for i,f in enumerate(FACES):
 im=neutral.crop((i*512,0,(i+1)*512,1024));bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,512)),(535+i*330,70));d.text((535+i*330,600),f.upper()+' / ORDINARY PREVIEW',font=font,fill='#e3cf43');cx,cy=controls[f]['grip'];crop=im.crop((cx-60,cy-95,cx+65,cy+60));crop=crop.resize((150,186));plate.paste(crop,(580+i*330,635),crop)
plate.save(HERE/'source-comparison.png');print('Prepared crescent iron vinereaper and four exact female Hand/2 bindings; display poses are provisional.')
