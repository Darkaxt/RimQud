"""Construct one reusable stone pestle; captured mutation binding is not remapped."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,math,re,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');MOD=Path('D:/Steam/steamapps/workshop/content/294100/2454918552');SIZE=(512,1024);FACES=['south','east','north']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
pattern='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><defs><linearGradient id="stone"><stop stop-color="#aaaaaa"/><stop offset=".4" stop-color="#e1e1e1"/><stop offset="1" stop-color="#999999"/></linearGradient></defs>
<path d="M254 450 C236 450 228 465 231 482 C233 501 242 517 246 537 L246 589 Q242 603 246 612 Q256 620 266 612 Q270 603 266 589 L266 537 C270 517 279 501 281 482 C284 463 274 450 254 450Z" fill="url(#stone)" stroke="#252525" stroke-width="5" stroke-linejoin="round"/>
<path d="M240 476 Q245 468 251 470 M242 485 L247 488 M265 477 L270 473 M253 499 L257 501" fill="none" stroke="#eeeeee" stroke-width="4" stroke-linecap="round"/>
<path d="M251 542 L251 584" fill="none" stroke="#c6c6c6" stroke-width="3" stroke-linecap="round"/></svg>'''
(HERE/'canonical-pattern.svg').write_text(pattern,encoding='utf-8');canonical=raster(pattern);canonical.save(HERE/'constructed-canonical.png')
powder='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><path d="M240 476 Q245 468 251 470 M242 485 L247 488 M265 477 L270 473 M253 499 L257 501" fill="none" stroke="white" stroke-width="4" stroke-linecap="round"/></svg>'''
raster(powder).getchannel('A').save(HERE/'canonical-detail.png')
# Grip is a preview landmark on the ordinary body, never a replacement for Hand181.
controls={'south':dict(grip=[126,525],angle=0,crop=[40,395,216,635]),'east':dict(grip=[277,535],angle=-20,crop=[190,395,366,635]),'north':dict(grip=[380,525],angle=0,crop=[294,395,470,635])}
def coefficients(c):
 a=math.radians(c['angle']);co,si=math.cos(a),math.sin(a);gx,gy=c['grip']
 # inverse of clockwise rotation about source grip (256,565)
 return [co,-si,256-co*gx+si*gy,si,co,565-si*gx-co*gy]
def place(im,c):return im.transform(SIZE,Image.Transform.AFFINE,coefficients(c),Image.Resampling.BICUBIC)
sheet=Image.new('RGBA',(1536,1024));neutral=sheet.copy();zoom=sheet.copy()
for i,f in enumerate(FACES):
 c=controls[f];c['inverse_affine']=coefficients(c);item=place(canonical,c);item.save(HERE/f'constructed-item-{f}.png');place(Image.open(HERE/'canonical-detail.png').convert('RGBA'),c).getchannel('R').save(HERE/f'detail-region-{f}.png')
 body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');mask=Image.new('L',SIZE);d=ImageDraw.Draw(mask)
 if f!='north':
  hx,hy=(111,525) if f=='south' else (267,535);d.ellipse((hx-34,hy-34,hx+34,hy+34),fill=255)
 mask.save(HERE/f'hand-visibility-{f}.png');a=np.array(body);hand=a.copy();hand[:,:,3]=np.minimum(a[:,:,3],np.array(mask));Image.fromarray(hand).save(HERE/f'original-hand-{f}.png')
 red=a.copy();red[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])))
 for target,base in [(sheet,Image.fromarray(red)),(neutral,body)]:
  assembled=Image.alpha_composite(item,base) if f=='north' else Image.alpha_composite(base,item)
  if f!='north':
   overlay=np.array(base);overlay[:,:,3]=np.minimum(overlay[:,:,3],np.array(mask));assembled=Image.alpha_composite(assembled,Image.fromarray(overlay))
  target.paste(assembled,(i*512,0))
  if target is sheet:zoom.paste(assembled.crop(c['crop']).resize((396,540),Image.Resampling.LANCZOS),(i*512+58,242))
sheet.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-grip-context.png');write(HERE/'fit-controls.json',controls)
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Pestle');assert sha(DONOR/original['reference_file'])==original['reference_sha256']
actor=next(a for a in json.loads((ROOT/'art/village/sources.json').read_text())['actors'] if a['creature']=='Nima Ruda');resident=actor['native_instances'][0];binding=next(p for p in resident['parts'] if (p.get('equipped') or {}).get('blueprint')=='Pestle');dp=MOD/'Textures/Things/Item/Equipment/WeaponMelee/LightClub.png'
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Items.xml');object_xml=re.search(r'<object\s+Name="Pestle"(?=\s|>).*?</object>',definitions.read_text(encoding='utf-8-sig'),re.S)
# The whole installed file contains control-character entities not accepted by ElementTree.
assert object_xml;obj=ET.fromstring(object_xml.group())
write(HERE/'source-packet.json',dict(entry='FIT-NIMA-PESTLE-HAND-6',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Nima Ruda',race='Human; ordinary female reusable item preview',original=original,observed_binding=binding,captured_resident=resident,installed_definition=dict(file=str(definitions),sha256=sha(definitions),object_xml=ET.tostring(obj,encoding='unicode')),body=ref(BODY/'model.json'),donor_reference=dict(file=str(dp),sha256=sha(dp),mod='Vanilla Weapons Expanded - Tribal',workshop_id='2454918552',about_sha256=sha(MOD/'About/About.xml'),role='Actual light-club asset supplies narrow grip / rounded bulb silhouette and neutral held-item convention only. Qud stone and powder identity overrides wooden material. HeavyClub inspected and rejected: too large and wrapped.'),design='Small smooth stone grinding pestle with bulbous end, narrow rounded grip and restrained powder flecks; no spikes, bandages, wooden grain, mortar or extra costume. Original glyph diagonal is an object pose, not a three-quarter camera.',authored_scale='Approximately 170 source pixels (~16 pixels in 48x96 preview). Authored readable size, not native measured length or dimension inferred from weight.',frame=dict(canvas=list(SIZE),contact=[256,950],camera='Strict SEN body; axially symmetric pestle placed by affine grip. West mirrors profile as an illustrative ordinary-hand preview only.',context_zoom_size=[396,540],context_zoom_origin=[58,242]),palette=dict(foreground='y',detail='Y',detail_assignment='Powder flecks are an authored assignment of the original bright detail role, not a chemical identification.'),mutation_boundary='Actual Hand181 parent180 laterality6 manager506::MultipleArms::Change, equipped531. Ordinary-hand preview is illustrative and MUST NOT remap this native binding. Extra-arm placement, handedness, named appearance and outfit/native acceptance remain unfinished.',native_acceptance='Pending full-set generation and mutation assembly'))
plate=Image.new('RGB',(1536,830),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);d.text((20,15),'NIMA > HUMAN BASE > PESTLE / exact source; actual mod convention; own construction',font=font,fill='#e3cf43')
orig=Image.open(DONOR/original['reference_file']).convert('RGBA').resize((160,240),Image.Resampling.NEAREST);plate.paste(orig,(24,80),orig);don=Image.open(dp).convert('RGBA');box=don.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();don=don.crop(box);don.thumbnail((250,150));plate.paste(don,(225,120),don)
for y,t in [(350,'Stone bulb / humoric powders'),(380,'Native y / bright Y detail'),(410,'Actual Hand181 / item531 / laterality6'),(440,'Mutation binding NOT ordinary-hand mapping'),(470,'LightClub: shape convention only'),(500,'Own stone material; no wood or wrap')]:d.text((20,y),t,font=font,fill='#e5e8d8')
for i,f in enumerate(FACES):
 im=neutral.crop((i*512,0,(i+1)*512,1024));bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,512)),(535+i*330,70));d.text((535+i*330,600),f.upper()+' / ORDINARY PREVIEW',font=font,fill='#e3cf43');crop=im.crop(controls[f]['crop']);plate.paste(crop.resize((132,180)),(590+i*330,625),crop.resize((132,180)))
plate.save(HERE/'source-comparison.png')
print('Pestle packet, canonical geometry, ordinary-hand grip and contextual zoom prepared; mutation binding preserved.')
