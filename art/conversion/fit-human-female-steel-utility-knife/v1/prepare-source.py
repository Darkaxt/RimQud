"""Small Qud folding utility knife; female compatibility, observed male item source."""
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
handle='''<path d="M244 547 Q256 539 268 547 L271 604 Q270 617 257 620 Q244 618 242 608Z" fill="#929292" stroke="#252525" stroke-width="4"/>
<path d="M249 566 L249 604 M263 569 L264 602" fill="none" stroke="#686868" stroke-width="3" stroke-linecap="round"/>
<circle cx="256" cy="552" r="6" fill="#bcbcbc" stroke="#555555" stroke-width="2"/>'''
blade='''<path d="M246 545 L246 481 Q247 464 267 455 L272 526 L263 545Z" fill="#d6d6d6" stroke="#252525" stroke-width="4" stroke-linejoin="round"/>
<path d="M250 537 L250 482 Q252 469 266 460" fill="none" stroke="#eeeeee" stroke-width="3" stroke-linecap="round"/>
<path d="M260 484 L263 507" fill="none" stroke="#999999" stroke-width="3" stroke-linecap="round"/>'''
pattern=svg(handle+blade);(HERE/'canonical-pattern.svg').write_text(pattern,encoding='utf-8');canonical=raster(pattern);canonical.save(HERE/'constructed-canonical.png');raster(svg(blade)).getchannel('A').save(HERE/'canonical-blade-region.png');raster(svg(handle)).getchannel('A').save(HERE/'canonical-handle-region.png')
# Full item remains unchanged. These are provisional ordinary upright display poses,
# not a ready/resting gameplay-state system or inferred attack animation.
controls={'south':dict(grip=[126,525],angle=0,mirror=False,crop=[50,340,226,596]),'east':dict(grip=[277,535],angle=-20,mirror=False,crop=[200,340,376,596]),'north':dict(grip=[380,525],angle=-15,mirror=True,crop=[310,340,486,596])}
ITEM_SCALE=1.0
def coefficients(c):
 a=math.radians(c['angle']);co,si=math.cos(a),math.sin(a);gx,gy=c['grip'];pivot=255 if c['mirror'] else 256;return [co,-si,pivot-co*gx+si*gy,si,co,590-si*gx-co*gy]
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
  if target is sheet:zoom.paste(assembled.crop(c['crop']).resize((352,512),Image.Resampling.LANCZOS),(i*512+80,240))
sheet.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-item-context.png');write(HERE/'fit-controls.json',controls)
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Steel Utility Knife');assert sha(DONOR/original['reference_file'])==original['reference_sha256']
actors=json.loads((ROOT/'art/village/sources.json').read_text())['actors'];bindings=[]
for actor in actors:
 for resident in actor['native_instances']:
  for part in resident['parts']:
   if (part.get('equipped') or {}).get('blueprint')=='Steel Utility Knife':bindings.append(dict(creature=actor['creature'],resident={k:v for k,v in resident.items() if k!='parts'},part=part))
assert len(bindings)==1
assert bindings[0]['creature']=='Argyve' and bindings[0]['resident']['gender']=='male'
mod=Path('D:/Steam/steamapps/workshop/content/294100/1814383360');dp=mod/'Textures/NewThings/CombatKnife.png'
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Items.xml');fragment=re.search(r'<object\s+Name="Steel Utility Knife"(?=\s|>).*?</object>',definitions.read_text(encoding='utf-8-sig'),re.S);assert fragment;obj=ET.fromstring(fragment.group())
write(HERE/'source-packet.json',dict(entry='FIT-HUMAN-FEMALE-STEEL-UTILITY-KNIFE-HAND-2',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Female human compatibility template; item observed on Argyve male519',race='Human, ordinary female baseline',fitting_scope='Required female compatibility fitting, not an observed female NPC loadout. No female knife-equipped resident was captured in this catalogue.',original=original,observed_bindings=bindings,installed_definition=dict(file=str(definitions),sha256=sha(definitions),object_xml=ET.tostring(obj,encoding='unicode')),source_resolution='Core description specifies a use-dull finger-smudged folding knife. Actual Argyve item588 also has a painted sultan-history description/reputation property. Capture provides ordinary tile/palette and text; no separate painting graphic exported. Preserve individual property rather than inventing a miniature scene in every generic knife.',body=ref(BODY/'model.json'),donor_reference=dict(file=str(dp),sha256=sha(dp),mod='Vanilla Weapons Expanded',workshop_id='1814383360',about_sha256=sha(mod/'About/About.xml'),role='Actual current VWE_MeleeWeapon_CombatKnife texPath via LoadFolders1.6/1.7. Small blade/handle outline and restrained flat shading only. Fixed military knife is not a folding utility knife; omit its guard and reconstruct Qud folding pivot/handle.'),design='Small open folding utility knife: use-dull steel blade, simple recessed handle, pivot and thumb nick. No military guard, serration, ornate dagger or imaginary painted scene. Open depiction follows source glyph/description; no fold-toggle mechanic inferred.',authored_scale='Approximately170 source pixels /16 pixels at48x96, comparable to Pestle and substantially shorter than Vinereaper/Vibro Blade displays. Authored readable size; native numeric dimensions unavailable, weight1 is not length.',frame=dict(canvas=list(SIZE),contact=[256,950],item_space_grip=[256,590],camera='Strict SEN body; stationary authoring display only. Opposite blade side mirrors; native ready/resting aim remains pending.',context_zoom_scale=2,context_zoom_origin=[80,240],context_zoom_size=[352,512],context_crops={f:c['crop'] for f,c in controls.items()}),palette=dict(foreground='Y',detail='y',detail_assignment='Native bright steel blade Y and contrasting handle y. Separate neutral equal-RGB regions; no fixed skin/paint colors.'),assembly_boundary='Actual source is male Argyve Hand320/laterality2, no mutation manager. Female recipient is authored compatibility only. Ready one-handed side pose must be forward/horizontal90deg to body; no native female equip or named outfit acceptance claimed.',native_acceptance='Pending full-set generation and actual native compatibility/equipped/resting-ready state'))
plate=Image.new('RGB',(1536,850),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);d.text((20,15),'FEMALE COMPATIBILITY > STEEL UTILITY KNIFE / actual source and current mod reference',font=font,fill='#e3cf43')
orig=Image.open(DONOR/original['reference_file']).convert('RGBA').resize((160,240),Image.Resampling.NEAREST);plate.paste(orig,(24,80),orig);don=Image.open(dp).convert('RGBA');box=don.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();don=don.crop(box);don.thumbnail((270,150));plate.paste(don,(210,130),don)
for y,t in [(350,'Small use-dull folding utility knife'),(380,'Native blade Y / handle y'),(410,'Source: Argyve519 / item588 / Hand320'),(440,'Female fit is compatibility, not a resident'),(470,'Current mod knife: shading/proportions only'),(500,'Painted history text retained; no graphic')]:d.text((20,y),t,font=font,fill='#e5e8d8')
for i,f in enumerate(FACES):
 im=neutral.crop((i*512,0,(i+1)*512,1024));bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,512)),(535+i*330,70));d.text((535+i*330,600),f.upper()+' / ORDINARY PREVIEW',font=font,fill='#e3cf43');cx,cy=controls[f]['grip'];crop=im.crop((cx-60,cy-95,cx+65,cy+60));crop=crop.resize((150,186));plate.paste(crop,(580+i*330,635),crop)
plate.save(HERE/'source-comparison.png')
# Source-specific metadata pass for this active entry; no game process or runtime query.
base=definitions.parent;files=[base/n for n in ['Items.xml','PhysicalPhenomena.xml','RootObjects.xml']];texts={p:p.read_text(encoding='utf-8-sig') for p in files};chain=[];name='Steel Utility Knife';effective={};slots=[]
while name:
 matches=[(p,re.search(r'<object\s+Name="'+re.escape(name)+r'"(?=\s|>).*?</object>',text,re.S)) for p,text in texts.items()];matches=[(p,m) for p,m in matches if m];assert len(matches)==1,name
 path,match=matches[0];node=ET.fromstring(match.group());physics=[dict(p.attrib) for p in node.findall('part') if p.get('Name')=='Physics'];uses=[dict(p.attrib) for p in node.findall('tag') if p.get('Name')=='UsesSlots'];chain.append(dict(blueprint=name,parent=node.get('Inherits'),file=str(path),sha256=sha(path),physics=physics,uses_slots=uses));name=node.get('Inherits')
for row in reversed(chain):
 for fields in row['physics']:effective.update({k:v for k,v in fields.items() if k!='Name'})
 if row['uses_slots']:slots=row['uses_slots']
assert effective.get('UsesTwoSlots','false').lower()=='false' and not slots and not effective.get('UsesSlots')
physics_source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/scratch/inspect/XRL.World.Parts.Physics.decompiled.cs');go_source=physics_source.with_name('XRL.World.GameObject.decompiled.cs');physics_text=physics_source.read_text();assert 'public int Flags = 2;' in physics_text and '(Flags & 8) == 8' in physics_text
donor_def=mod/'1.6/Defs/ThingDefs_Misc/Weapons/MeleeIndustrial.xml';donor_node=next(n for n in ET.parse(donor_def).getroot().findall('ThingDef') if n.findtext('defName')=='VWE_MeleeWeapon_CombatKnife');assert donor_node.findtext('graphicData/texPath')=='NewThings/CombatKnife'
rimbase=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Misc/Weapons/BaseWeapons.xml');nodes={n.get('Name'):n for n in ET.parse(rimbase).getroot().findall('ThingDef') if n.get('Name')};parent=donor_node.get('ParentName');donor_chain=[];draw_size=donor_node.findtext('graphicData/drawSize')
while parent:
 n=nodes[parent];donor_chain.append(dict(name=parent,parent=n.get('ParentName'),explicit_draw_size=n.findtext('graphicData/drawSize')))
 if draw_size is None:draw_size=n.findtext('graphicData/drawSize')
 parent=n.get('ParentName')
assert draw_size is None # No explicit XML size: do not invent an engine/runtime value.
occupancy=[]
for b in bindings:
 item_id=b['part']['equipped']['instance'];res=b['resident'];actor=next(a for a in actors if a['creature']==b['creature']);full_resident=next(n for n in actor['native_instances'] if n['instance']==res['instance']);parts=[p for p in full_resident['parts'] if (p.get('equipped') or {}).get('instance')==item_id];assert len(parts)==1
 occupancy.append(dict(actor=b['creature'],resident=res['instance'],item=item_id,occupied_parts=[dict(id=p['id'],type=p['type'],laterality=p['laterality'],manager=p['manager']) for p in parts],captured_get_slots_required_for=None))
canonical_bounds=canonical.getchannel('A').getbbox();blade_bounds=Image.open(HERE/'canonical-blade-region.png').getbbox();handle_bounds=Image.open(HERE/'canonical-handle-region.png').getbbox();body_model=json.loads((BODY/'model.json').read_text())
metadata=dict(item='Steel Utility Knife',recipient_scope='Female compatibility template; observed source item is male Argyve only.',inheritance=chain,effective_physics=effective,handedness=dict(declared_uses_two_slots=False,uses_slots=None,base_grip_class='one-handed',evidence='No inherited UsesTwoSlots/UsesSlots override; Physics default Flags2 excludes bit8. Source Argyve snapshot occupies one Hand; no female equip observation.',physics_default=dict(file=str(physics_source),sha256=sha(physics_source),flags=2,uses_two_slots_bit=8),runtime_requirement_semantics=dict(file=str(go_source),sha256=sha(go_source),method='GetSlotsRequiredFor delegates to actor-sensitive event'),runtime_get_slots_required_for=None,unknown='No actor-specific slot-demand event exported; female compatibility is authoring only.',observed_occupancy=occupancy),size=dict(native_dimensions=None,native_size_class=None,descriptive_length=None,weight=effective.get('Weight'),weapon_class='ShortBlades',native_description='Use-dull finger-smudged knife folds in on itself; no numeric length.',authored_canonical_bounds=list(canonical_bounds),blade_bounds=list(blade_bounds),handle_bounds=list(handle_bounds),primary_grip=[256,590],supporting_grip=None,reason='Small one-handed folding knife, approximately170px overall and75px handle, shorter than the long-blade/harvesting-tool designs on this same base. Weight1 is not length.',canonical_source=ref(HERE/'constructed-canonical.png'),pixel_world_scale=body_model['pixel_world_scale'],raster_scale=ITEM_SCALE,world_mapping=dict(width=body_model['views']['south'][0]['width'],height=body_model['views']['south'][0]['height']),units='Registered authoring/world mapping, not meters or native measured dimensions.'),donor_size_reference=dict(definition=dict(file=str(donor_def),sha256=sha(donor_def),defName='VWE_MeleeWeapon_CombatKnife',description=donor_node.findtext('description'),texPath=donor_node.findtext('graphicData/texPath'),equipped_angle_offset=donor_node.findtext('equippedAngleOffset')),load_folders=dict(file=str(mod/'LoadFolders.xml'),sha256=sha(mod/'LoadFolders.xml'),mapping='1.6 and1.7 select1.6'),base_defs=dict(file=str(rimbase),sha256=sha(rimbase),inheritance=donor_chain),explicit_xml_drawSize=draw_size,runtime_graphic_drawSize=None,qualification='No explicit XML drawSize or live graphic value available; donor small knife is visual reference, not a numeric length.'),individual_variant='Observed Argyve painted-story text retained in original description. No additional paint texture/mask exported, so no invented narrative scene is baked into generic knife.',pose='Stationary display only; forward/horizontal ready side pose and native state remain unfinished.')
write(HERE/'weapon-metadata.json',metadata);packet=json.loads((HERE/'source-packet.json').read_text());packet['weapon_metadata']=ref(HERE/'weapon-metadata.json');packet['frame']['item_scale']=ITEM_SCALE;packet['frame']['mirror_anchor']='Pillow flip maps sourcex256 to255; north inverse uses255';write(HERE/'source-packet.json',packet)
print('Prepared small folding knife, one-handed base declaration and honest female compatibility scope; runtime slot demand unknown.')
