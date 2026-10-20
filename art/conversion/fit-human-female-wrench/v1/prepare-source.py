"""Source-bound armlength metal wrench; female compatibility, not new NPC gear."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,math,re,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';SIZE=(512,1024)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def svg(content):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+content+'</svg>'
def raster(content):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=content,skip_system_fonts=True))).convert('RGBA')
shaft='''<path d="M247 410 L265 410 L266 628 Q266 644 256 645 Q246 645 245 631Z" fill="#9c9c9c" stroke="#252525" stroke-width="5" stroke-linejoin="round"/>
<path d="M252 453 L252 606" fill="none" stroke="#bbbbbb" stroke-width="3" stroke-linecap="round"/>'''
head='''<path d="M245 423 L225 399 L225 349 Q227 332 244 330 H286 Q303 332 306 349 V379 H289 V353 H250 V385 H276 V405 L260 423Z" fill="#c8c8c8" stroke="#252525" stroke-width="5" stroke-linejoin="round"/>
<path d="M235 351 Q234 341 246 340 H281" fill="none" stroke="#e4e4e4" stroke-width="3" stroke-linecap="round"/>
<path d="M253 393 H271 M253 399 H271 M246 411 L264 411 M246 418 L264 418 M246 425 L264 425" fill="none" stroke="#666666" stroke-width="3" stroke-linecap="round"/>'''
pattern=svg(shaft+head);(HERE/'canonical-pattern.svg').write_bytes(pattern.encode());canonical=raster(pattern);canonical.save(HERE/'constructed-canonical.png');raster(svg(head)).getchannel('A').save(HERE/'canonical-head-region.png');raster(svg(shaft)).getchannel('A').save(HERE/'canonical-shaft-region.png')
controls={'south':dict(grip=[380,525],angle=0,mirror=False,crop=[256,128,512,640]),'east':dict(grip=[257,535],angle=-20,mirror=False,crop=[128,128,384,640]),'north':dict(grip=[126,525],angle=15,mirror=True,crop=[0,128,256,640])}
red_sheet=Image.new('RGBA',(1536,1024));neutral=red_sheet.copy();zoom=red_sheet.copy()
for i,(f,c) in enumerate(controls.items()):
    a=math.radians(c['angle']);co,si=math.cos(a),math.sin(a);gx,gy=c['grip'];px=255 if c['mirror'] else 256;c['inverse_affine']=[co,-si,px-co*gx+si*gy,si,co,590-si*gx-co*gy]
    source=canonical.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if c['mirror'] else canonical;item=source.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC).convert('RGBA');item.save(HERE/f'constructed-item-{f}.png')
    body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');mask=Image.new('L',SIZE)
    if f=='south':ImageDraw.Draw(mask).ellipse((395-34,525-34,395+34,525+34),fill=255)
    mask.save(HERE/f'hand-visibility-{f}.png');b=np.array(body);h=b.copy();h[:,:,3]=np.minimum(b[:,:,3],np.array(mask));Image.fromarray(h).save(HERE/f'original-hand-{f}.png');r=b.copy();r[:,:,:3]=np.uint8(np.round(b[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])))
    for target,base in [(red_sheet,Image.fromarray(r)),(neutral,body)]:
        assembled=Image.alpha_composite(item,base) if f!='south' else Image.alpha_composite(base,item)
        if f=='south':
            hand=np.array(base);hand[:,:,3]=np.minimum(hand[:,:,3],np.array(mask));assembled=Image.alpha_composite(assembled,Image.fromarray(hand))
        target.paste(assembled,(i*512,0))
        if target is red_sheet:zoom.paste(assembled.crop(c['crop']).resize(SIZE,Image.Resampling.LANCZOS),(i*512,0))
red_sheet.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-item-context.png');write('fit-controls.json',controls)
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Wrench');original_file=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/original['reference_file'];assert sha(original_file)==original['reference_sha256']
bindings=[]
for actor in json.loads((ROOT/'art/village/sources.json').read_text())['actors']:
    for resident in actor['native_instances']:
        for part in resident['parts']:
            if (part.get('equipped') or {}).get('blueprint')=='Wrench':bindings.append(dict(creature=actor['creature'],resident={k:v for k,v in resident.items() if k!='parts'},part=part))
assert len(bindings)==1 and bindings[0]['resident']['gender']=='male' and bindings[0]['part']['id']==322 and bindings[0]['part']['laterality']==1 and bindings[0]['part']['manager'] is None
base=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');files=[base/n for n in ['Items.xml','PhysicalPhenomena.xml','RootObjects.xml']];texts={p:p.read_text(encoding='utf-8-sig') for p in files};chain=[];name='Wrench';effective={};slots=[]
while name:
    matches=[(p,re.search(r'<object\s+Name="'+re.escape(name)+r'"(?=\s|>).*?</object>',s,re.S)) for p,s in texts.items()];matches=[(p,m) for p,m in matches if m];assert len(matches)==1,name
    p,m=matches[0];node=ET.fromstring(m.group());chain.append(dict(blueprint=name,parent=node.get('Inherits'),file=str(p),sha256=sha(p),physics=[dict(n.attrib) for n in node.findall('part') if n.get('Name')=='Physics'],uses_slots=[dict(n.attrib) for n in node.findall('tag') if n.get('Name')=='UsesSlots']));name=node.get('Inherits')
for row in reversed(chain):
    for fields in row['physics']:effective.update({k:v for k,v in fields.items() if k!='Name'})
    if row['uses_slots']:slots=row['uses_slots']
assert effective.get('UsesTwoSlots','false').lower()=='false' and not slots
donor_mod=Path('D:/Steam/steamapps/workshop/content/294100/2102143149');donor=donor_mod/'Textures/Things/Building/WorkshopProps/VFEPD_AdjustableWrench/VFEPD_AdjustableWrench.png';donor_def=donor_mod/'1.6/Defs/ThingDefs_Buildings/Buildings_WorkshopProps.xml';node=next(n for n in ET.parse(donor_def).getroot().findall('ThingDef') if n.findtext('defName')=='VFEPD_AdjustableWrench')
assert node.findtext('graphicData/texPath')=='Things/Building/WorkshopProps/VFEPD_AdjustableWrench/VFEPD_AdjustableWrench'
load=ET.parse(donor_mod/'LoadFolders.xml').getroot();load_map={tag:[li.text for li in load.find(tag).findall('li') if not li.attrib] for tag in ['v1.6','v1.7']};assert all('1.6' in values for values in load_map.values())
legacy=Path('D:/Steam/steamapps/workshop/content/294100/1814383360/Textures/Things/WeaponMelee/Wrench.png')
physics=Path('E:/Temp/qud-transplant-probe-pawns-20261019/scratch/inspect/XRL.World.Parts.Physics.decompiled.cs');go=physics.with_name('XRL.World.GameObject.decompiled.cs');assert 'public int Flags = 2;' in physics.read_text() and '(Flags & 8) == 8' in physics.read_text()
metadata=dict(item='Wrench',recipient_scope='Female compatibility template only; actual male Argyve519 offhand item590 retained separately.',inheritance=chain,effective_physics=effective,handedness=dict(declared_uses_two_slots=False,uses_slots=None,base_grip_class='one-handed',physics_default=dict(file=str(physics),sha256=sha(physics),flags=2,uses_two_slots_bit=8),runtime_requirement_semantics=dict(file=str(go),sha256=sha(go),method='GetSlotsRequiredFor delegates to actor-sensitive event'),runtime_get_slots_required_for=None,observed_occupancy=[dict(actor='Argyve',resident=519,item=590,occupied_parts=[dict(id=322,type='Hand',laterality=1,manager=None)],captured_get_slots_required_for=None)],qualification='One-handed base declaration and captured offhand occupancy; runtime event and female equip compatibility not exported.'),size=dict(native_dimensions=None,descriptive_length='An armlength',weight=effective.get('Weight'),weapon_class='Cudgel',authored_canonical_bounds=list(canonical.getchannel('A').getbbox()),head_bounds=list(Image.open(HERE/'canonical-head-region.png').getbbox()),shaft_bounds=list(Image.open(HERE/'canonical-shaft-region.png').getbbox()),primary_grip=[256,590],supporting_grip=None,raster_scale=1,pixel_world_scale=json.loads((BODY/'model.json').read_text())['pixel_world_scale'],reason='About315 authoring pixels overall, longer than the170px utility knife. Armlength is the native qualitative size cue; exact size remains authored, weight1 is not a dimension.'),donor_size_reference=dict(definition=dict(file=str(donor_def),sha256=sha(donor_def),defName=node.findtext('defName'),description=node.findtext('description'),texPath=node.findtext('graphicData/texPath'),explicit_drawSize=node.findtext('graphicData/drawSize')),load_folders=dict(file=str(donor_mod/'LoadFolders.xml'),sha256=sha(donor_mod/'LoadFolders.xml'),mapping=load_map),qualification='Actual decorative prop drawSize0.75 is not a pawn-held weapon length. Use its flat outline/material convention, retaining the larger hook/jaw and screwing iron from Qud.'),individual_variant='Actual Argyve wrench has Counterweighted/+1 To-Hit text. No additional counterweight graphic is exported; do not invent one.',pose='Stationary display only. Hand1 side is provisionally behind the body, not a new independent far-arm model; actual native handed/ready-resting state remains pending.')
write('weapon-metadata.json',metadata)
write('source-packet.json',dict(entry='FIT-HUMAN-FEMALE-WRENCH-HAND-1',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Female compatibility template; source male Argyve519',race='Human ordinary female',fitting_scope='No captured female wrench-equipped resident. This required template does not alter the actual Argyve loadout.',original=original,observed_bindings=bindings,body=ref(BODY/'model.json'),weapon_metadata=ref(HERE/'weapon-metadata.json'),donor_reference=dict(file=str(donor),sha256=sha(donor),mod='Vanilla Furniture Expanded - Props and Decor',workshop_id='2102143149',about_sha256=sha(donor_mod/'About/About.xml'),role='Actual 1.6/1.7 workshop decorative adjustable-wrench prop; flat view and material convention only, not native equipment behavior or size.'),additional_reference=dict(file=str(legacy),sha256=sha(legacy),mod='Vanilla Weapons Expanded',workshop_id='1814383360',role='Installed legacy wrench icon, not found as a current1.6 weapon definition. Rounded tool silhouette/shading only.'),design='Long worn metal shaft, broad hooked jaw opening and visible screwing-iron threads near neck, preserving Qud silhouette rather than replacing it with a tiny ordinary spanner. Source does not establish mechanical adjustment animation.',palette=dict(foreground='y',detail='c',resolution='Runtime TileColor &y overrides ColorString &c for primary. Original reference shows brighter hooked jaw and darker shaft; assign head primary y and shaft detail c.'),frame=dict(canvas=list(SIZE),contact=[256,950],item_space_grip=[256,590],context_zoom_scale=2,controls=controls),native_acceptance='Pending full-set generation gate, female compatibility and actual native offhand/pose state.'))
print('Prepared Qud armlength hooked wrench, actual ordinary offhand binding, limited actual mod references and female compatibility construction.')
