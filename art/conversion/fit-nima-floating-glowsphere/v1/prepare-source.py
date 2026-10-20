"""Source-bound palm-sized opal; separate floating item, color mask and halo."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,re,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';SIZE=(512,1024)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+s+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
body='''<defs><radialGradient id="opal" cx="35%" cy="29%" r="72%"><stop offset="0" stop-color="#efefef"/><stop offset=".55" stop-color="#cecece"/><stop offset="1" stop-color="#898989"/></radialGradient><clipPath id="surface"><circle cx="256" cy="512" r="28.3"/></clipPath></defs>
<circle cx="256" cy="512" r="30" fill="url(#opal)" stroke="#252525" stroke-width="3.4"/>
<g clip-path="url(#surface)"><path d="M233 507 C246 494 268 499 275 512 C282 524 265 536 251 539 C268 525 267 514 253 510 C244 508 239 511 233 517Z" fill="#b2b2b2"/>
<path d="M240 503 Q246 493 256 494" fill="none" stroke="#f7f7f7" stroke-width="4" stroke-linecap="round"/>
<path d="M268 516 Q272 521 266 527" fill="none" stroke="#d8d8d8" stroke-width="2" stroke-linecap="round"/></g>'''
detail='''<defs><clipPath id="surface"><circle cx="256" cy="512" r="28.3"/></clipPath></defs><g clip-path="url(#surface)"><path d="M233 507 C246 494 268 499 275 512 C282 524 265 536 251 539 C268 525 267 514 253 510 C244 508 239 511 233 517Z" fill="white"/></g>'''
(HERE/'canonical-pattern.svg').write_bytes(svg(body).encode());raster(svg(body)).save(HERE/'constructed-canonical.png');(HERE/'detail-region.svg').write_bytes(svg(detail).encode());raster(svg(detail)).getchannel('A').save(HERE/'canonical-detail-region.png')
controls={'south':dict(center=[444,330],crop=[256,128,512,640]),'east':dict(center=[380,330],crop=[256,128,512,640]),'north':dict(center=[64,330],crop=[0,128,256,640])}
redsheet=Image.new('RGBA',(1536,1024));neutral=redsheet.copy();zoom=redsheet.copy();canonical=Image.open(HERE/'constructed-canonical.png').convert('RGBA')
for i,(f,c) in enumerate(controls.items()):
    cx,cy=c['center'];c['inverse_affine']=[1,0,256-cx,0,1,512-cy];item=canonical.transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC);item.save(HERE/f'constructed-item-{f}.png')
    original=Image.open(BODY/f'selected-{f}.png').convert('RGBA');a=np.array(original);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])))
    for target,base in [(redsheet,Image.fromarray(a)),(neutral,original)]:
        assembled=Image.alpha_composite(base,item);target.paste(assembled,(i*512,0))
        if target is redsheet:zoom.paste(assembled.crop(c['crop']).resize(SIZE,Image.Resampling.LANCZOS),(i*512,0))
redsheet.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-item-context.png');write('fit-controls.json',controls)
original=next(e for e in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if e['blueprint']=='Floating Glowsphere');original_file=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/original['reference_file'];assert sha(original_file)==original['reference_sha256']
actors=json.loads((ROOT/'art/village/sources.json').read_text())['actors'];bindings=[]
for actor in actors:
    for resident in actor['native_instances']:
        for part in resident['parts']:
            if (part.get('equipped') or {}).get('blueprint')=='Floating Glowsphere':bindings.append(dict(creature=actor['creature'],resident={k:v for k,v in resident.items() if k!='parts'},part=part))
assert len(bindings)==1 and bindings[0]['resident']['instance']==506
part=bindings[0]['part'];assert part['id']==195 and part['type']=='Floating Nearby' and part['laterality']==0 and part['manager'] is None
base=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');files=[base/n for n in ['Items.xml','PhysicalPhenomena.xml','RootObjects.xml']];texts={p:p.read_text(encoding='utf-8-sig') for p in files};chain=[];name='Floating Glowsphere';effective={}
while name:
    matches=[(p,re.search(r'<object\s+Name="'+re.escape(name)+r'"(?=\s|>).*?</object>',t,re.S)) for p,t in texts.items()];matches=[(p,m) for p,m in matches if m];assert len(matches)==1,name
    p,m=matches[0];node=ET.fromstring(m.group());parts=[dict(n.attrib) for n in node.findall('part')];chain.append(dict(blueprint=name,parent=node.get('Inherits'),file=str(p),sha256=sha(p),parts=parts));name=node.get('Inherits')
for row in reversed(chain):
    for fields in row['parts']:effective.setdefault(fields['Name'],{}).update({k:v for k,v in fields.items() if k!='Name'})
assert effective['Armor']['WornOn']=='Floating Nearby' and effective['GlowsphereProperties']['AllowedParts']=='Hand,Floating Nearby'
assert effective['LightSource']['Radius']=='8' and effective['AnimatedMaterialGeneric']['AnimationLength']=='200'
mod=Path('D:/Steam/steamapps/workshop/content/294100/2038001322');donor=mod/'Textures/BiomesIslands_Things/Item/Pearl/Pearl.png';jade=Path('D:/Steam/steamapps/workshop/content/294100/2016436324/Textures/Things/Item/Resource/Jade/Jade_a.png')
write('source-packet.json',dict(entry='FIT-NIMA-FLOATING-GLOWSPHERE-FLOATING-NEARBY-0',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Nima Ruda506',race='Human ordinary female baseline; individual mutations remain separate',original=original,observed_bindings=bindings,body=ref(BODY/'model.json'),inheritance=chain,effective_parts=effective,
    donor_reference=dict(file=str(donor),sha256=sha(donor),mod='Biomes! Islands',workshop_id='2038001322',about_sha256=sha(mod/'About/About.xml'),load_folders_sha256=sha(mod/'LoadFolders.xml'),role='Actual installed Pearl texture: compact rounded opal/pearl outline and smooth shading only. No floating-opal equipment equivalent claimed.',version_limits='Installed About/LoadFolders advertise through1.5; no associated Pearl definition found in inspected1.5 Defs. Historical style asset, not proof of active1.6/1.7 support or a mod installation.'),rejected_reference=dict(file=str(jade),sha256=sha(jade),role='Actual installed Jade texture inspected; angular rock silhouette does not match palm-sized opal sphere. Not selected.'),
    design='Palm-sized smooth opal-like sphere with a broad softly curved internal light region. No pupil/iris, limbs, mount, metal cage, necklace or pedestal. About64px diameter versus68px baseline palm diameter; scale is authored from native qualitative size cue.',
    palette=dict(foreground='Y',detail='C',animation=effective['AnimatedMaterialGeneric'],unit='Native animation units not resolved; do not interpret200 as turns or seconds.',neutral='All production RGB equal-channel grayscale; detail and optional halo own their native tint separately.'),
    frame=dict(canvas=list(SIZE),contact=[256,950],canonical_center=[256,512],radius=30,centers={f:c['center'] for f,c in controls.items()},placement='Authored shoulder-adjacent floating display anchors, not exported native orbit coordinates. No attachment to a hand or mutation-granted part.',context_zoom_scale=2),
    views='One rotationally symmetric, unmarked spherical surface reused in all required body facings. No distinct front/back anatomy or hardware is established; same scale/center basis, per-facing placement only. West mirrors east for authoring.',
    light='Keep lit radius8 under native LightSource ownership. A separate optional low-alpha art halo is an authoring effect, not a replacement world light, orbit or lighting implementation.',
    source_conflicts='Captured Weight0 while inherited static Physics has its own base Weight. No runtime weight-event export or unit conversion inferred; weight is not a sphere dimension.',
    native_acceptance='Pending complete generation set, native floating-slot/light/material-animation state and Nima individual mutation/outfit assembly.'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1152,650),'#142823');draw=ImageDraw.Draw(plate);draw.text((18,14),'SOURCE CHAIN / Qud palm-sized floating opal > actual Pearl style reference > fixed base',font=font,fill='#e3cf43')
for i,(path,label) in enumerate([(original_file,'Original Qud / native Y and C'),(donor,'Biomes! Islands / limited Pearl style'),(HERE/'constructed-canonical.png','Own neutral opal / no baked color')]):
    im=Image.open(path).convert('RGBA');box=im.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();im=im.crop(box);im=im.resize((256,256),Image.Resampling.NEAREST if i==0 else Image.Resampling.LANCZOS);plate.paste(im,(40+i*380,90),im);draw.text((18+i*380,390),label,font=font,fill='#e3cf43')
for y,t in [(450,'Actual Nima Floating Nearby195/0, no mutation manager; no hand or body cutout.'),(480,'Sphere shape is invariant across views; position is authored, not native orbit metadata.'),(510,'Native lit radius8 and four color keys retained; no new lighting or animation implementation.')]:draw.text((18,y),t,font=font,fill='#e5e8d8')
plate.save(HERE/'source-comparison.png')
print('Prepared palm-sized floating opal, actual Nima slot, version-qualified Pearl reference and native four color keys.')
