"""Construct Qud brinestalk crook, retaining the actual changed Hand/6 binding."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, io, json, re, sys, xml.etree.ElementTree as ET
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
sys.path.insert(0, 'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-male-older/v2'; SIZE=(512,1024)
assert not (HERE/'source-packet.json').exists()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def private(p): return dict(file=str(p),sha256=sha(p),publication='Private installed reference; not copied as a standalone asset')
def write(name,d): (HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def svg(s): return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+s+'</svg>'
def raster(s): return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
shape='M249 885 C250 720 247 580 250 456 C246 438 239 431 225 430 C211 430 201 440 203 453 Q205 466 217 470 Q220 477 215 481 Q196 482 188 463 C174 440 189 411 213 402 C235 393 257 404 267 424 C275 437 276 453 274 470 L267 885 Q267 897 257 897 Q246 897 249 885Z'
outline=f'<path d="{shape}" fill="#c2c2c2" stroke="#282828" stroke-width="5" stroke-linejoin="round"/>'
grain='<path d="M257 478 C253 590 258 744 255 868 M200 434 Q213 411 235 415 Q251 420 258 442" fill="none" stroke="#929292" stroke-width="3" stroke-linecap="round"/><path d="M264 516 L261 606 M261 725 L260 818" fill="none" stroke="#dddddd" stroke-width="3" stroke-linecap="round"/>'
detail='<path d="M244 444 Q253 440 270 444 L274 463 Q261 460 250 468Z" fill="#b8b8b8"/><path d="M250 454 Q258 450 271 453" fill="none" stroke="#707070" stroke-width="2"/>'
pattern=svg(outline+grain); (HERE/'canonical-pattern.svg').write_bytes(pattern.encode()); canonical=raster(pattern);canonical.save(HERE/'constructed-canonical.png')
detail_svg=svg(detail);(HERE/'detail-region.svg').write_bytes(detail_svg.encode());raster(detail_svg).getchannel('A').save(HERE/'canonical-detail-region.png')
controls={'south':dict(grip=[105,550],palm=[91,550],mirror=False,crop=[0,352,256,992]),
          'east':dict(grip=[248,554],palm=[239,554],mirror=False,crop=[128,352,384,992]),
          'north':dict(grip=[405,550],palm=[419,550],mirror=True,crop=[256,352,512,992])}
sheet=Image.new('RGBA',(1536,1024));zoom=Image.new('RGBA',(1536,1280));neutral=sheet.copy()
for i,(f,c) in enumerate(controls.items()):
    gx,gy=c['grip'];px=255 if c['mirror'] else 256;c['inverse_affine']=[1,0,px-gx,0,1,500-gy]
    source=ImageOps.mirror(canonical) if c['mirror'] else canonical
    item=source.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC).convert('RGBA');item.save(HERE/f'constructed-item-{f}.png')
    body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');b=np.array(body);mask=Image.new('L',SIZE)
    if f!='north':
        x,y=c['palm'];ImageDraw.Draw(mask).ellipse((x-39,y-37,x+39,y+37),fill=255)
    mask.save(HERE/f'hand-visibility-{f}.png');hand=b.copy();hand[:,:,3]=np.minimum(b[:,:,3],np.array(mask));Image.fromarray(hand).save(HERE/f'original-hand-{f}.png')
    r=b.copy();r[:,:,:3]=np.uint8(np.round(b[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])))
    for target,base in [(sheet,Image.fromarray(r)),(neutral,body)]:
        assembled=Image.alpha_composite(item,base) if f=='north' else Image.alpha_composite(base,item)
        if f!='north':
            h=np.array(base);h[:,:,3]=np.minimum(h[:,:,3],np.array(mask));assembled=Image.alpha_composite(assembled,Image.fromarray(h))
        target.paste(assembled,(i*512,0))
        if target is sheet:zoom.paste(assembled.crop(c['crop']).resize((512,1280),Image.Resampling.LANCZOS),(i*512,0))
sheet.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-item-context.png');write('fit-controls.json',controls)
original=next(e for e in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if e['blueprint']=='Walking Stick')
original_file=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/original['reference_file'];assert sha(original_file)==original['reference_sha256']
actor=next(e for e in json.loads((ROOT/'art/village/sources.json').read_text())['actors'] if e['creature']=='ElderBob');resident=actor['native_instances'][0]
part=next(p for p in resident['parts'] if (p.get('equipped') or {}).get('blueprint')=='Walking Stick');parent=next(p for p in resident['parts'] if p['id']==part['parent'])
assert part['id']==201 and part['laterality']==6 and part['manager']=='507::MultipleArms::Change'
base=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');files=[base/n for n in ['Items.xml','PhysicalPhenomena.xml','RootObjects.xml']];texts={p:p.read_text(encoding='utf-8-sig') for p in files};chain=[];name='Walking Stick';effective={}
while name:
    matches=[(p,re.search(r'<object\s+Name="'+re.escape(name)+r'"(?=\s|>).*?</object>',s,re.S)) for p,s in texts.items()];matches=[(p,m) for p,m in matches if m];assert len(matches)==1
    file,m=matches[0];node=ET.fromstring(m.group());chain.append(dict(blueprint=name,parent=node.get('Inherits'),definition=private(file),parts=[dict(p.attrib) for p in node.findall('part')],uses_slots=[dict(p.attrib) for p in node.findall('tag') if p.get('Name')=='UsesSlots']));name=node.get('Inherits')
for row in reversed(chain):
    for p in row['parts']:effective.setdefault(p['Name'],{}).update({k:v for k,v in p.items() if k!='Name'})
assert not any(row['uses_slots'] for row in chain) and effective['Physics'].get('UsesTwoSlots','false').lower()=='false'
mod=Path('D:/Steam/steamapps/workshop/content/294100/2352893469');donor=mod/'Common/Textures/Things/Item/Equipment/WeaponMelee/HDM_Walkingstick.png';defs=mod/'1.5/Defs/ThingDefs_Misc/PrimitiveMelee.xml';bases=mod/'1.5/Defs/ThingDefs_Misc/ToolWeapon_Bases.xml';node=next(n for n in ET.parse(defs).getroot().findall('ThingDef') if n.findtext('defName')=='VBY_WalkingStick')
assert node.findtext('graphicData/texPath')=='Things/Item/Equipment/WeaponMelee/HDM_Walkingstick'
metadata=dict(item='Walking Stick',inheritance=chain,effective_parts=effective,
    handedness=dict(base_class='one-handed',inherited_UsesTwoSlots=False,UsesSlots=None,runtime_GetSlotsRequiredFor=None,
                    observed_occupancy=[dict(actor='ElderBob',instance=507,item=541,part=part,parent=parent)],
                    qualification='Base flags and single captured occupancy support one-hand item; actor-specific slot demand was not exported. Hand201/6 is mutation-managed, not an ordinary Hand/2.'),
    size=dict(native_dimensions=None,weight=4,weapon_class='Cudgel',description='Dried brinestalk, spiraled crook',canonical_bounds=list(canonical.getchannel('A').getbbox()),item_space_grip=[256,500],supporting_grip=None,raster_scale=1,pixel_world_scale=json.loads((BODY/'model.json').read_text())['pixel_world_scale'],
              reason='Authored approximately half-body-height walking cane, about500px including crook. Weight is not length. High grip is explicitly a resting/support display near the crook, not a ready combat grip.'),
    pose='Stationary walking/support display only. Separate ready/drafted side presentation must project forward/horizontal; native state and mutation-hand support remain pending.',
    donor=dict(mod='Primitive Tools',workshop_id='2352893469',package_id='PrimitiveTools.velcroboy333',about=private(mod/'About/About.xml'),texture=private(donor),definition=private(defs),defName='VBY_WalkingStick',texPath=node.findtext('graphicData/texPath'),graphicClass=node.findtext('graphicData/graphicClass'),uiIconScale=node.findtext('uiIconScale'),explicit_drawSize=node.findtext('graphicData/drawSize'),base_definition=private(bases),inherited_equippedAngleOffset='-65',
               qualification='Installed through1.5 reference; no LoadFolders.xml found, no current1.6/1.7 compatibility or active-mod claim. Actual walking-stick def/texture supplies flat narrow wood outline and shading only. Straight donor silhouette does not replace Qud crook; uiIconScale1.25 is not world length.'))
write('weapon-metadata.json',metadata)
packet=dict(entry='FIT-IRUDAD-WALKING-STICK-HAND-6',recorded_at=datetime.now(timezone.utc).isoformat(),original=original,
    creature=dict(blueprint='ElderBob',display_name='Elder Irudad',resident={k:v for k,v in resident.items() if k!='parts'},race=actor['race_input']),
    observed_binding=dict(part=part,parent=parent),body=ref(BODY/'model.json'),weapon_metadata=ref(HERE/'weapon-metadata.json'),
    fitting_scope='Ordinary older-human compatibility authoring on a baseline palm proxy. Keep actual changed Hand201/6 and manager verbatim; this does not finish the mutation attachment, hands-face, tail, pose or full Irudad assembly.',
    donor_reference=metadata['donor'],design='One continuous dried reed-like brinestalk with rounded spiraled crook and restrained longitudinal grain, not a straight log, metal cane or invented facial staff.',
    palette=dict(primary='w',detail='g',body='w',assignment='Warm native stalk w; separate small green binding/accent near crook informed by original six darker pixels. Accent placement is authored; no living leaves or extra parts inferred.'),
    frame=dict(canvas=list(SIZE),contact=[256,950],item_space_grip=[256,500],context_crop_size=[256,640],context_zoom_scale=2,context_sheet_size=[1536,1280],controls=controls),
    native_acceptance='Pending full-set generation and integrated mutation-hand binding, native ready/resting pose and Irudad individual assembly.')
write('source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);board=Image.new('RGB',(1152,700),'#142823');d=ImageDraw.Draw(board)
for i,(path,label) in enumerate([(original_file,'QUD ORIGINAL / sw_cudgel_11'),(donor,'ACTUAL MOD / straight wood style'),(HERE/'constructed-canonical.png','MANUAL / source crook retained')]):
    im=Image.open(path).convert('RGBA')
    if i==0: im=im.resize((160,240),Image.Resampling.NEAREST)
    else:
        im=im.crop(im.getchannel('A').getbbox());im.thumbnail((240,450),Image.Resampling.LANCZOS)
    board.paste(im,(i*384+80,80),im);d.text((i*384+12,560),label,font=font,fill='#e3cf43')
d.text((18,18),'WALKING STICK / original glyph + native brinestalk/crook + actual donor',font=font,fill='#e3cf43')
d.text((18,620),'Hand201/6 remains mutation-managed. Fixed ordinary older base is a fitting proxy only.',font=font,fill='#e5e8d8');board.save(HERE/'source-comparison.png')
ledger_path=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(ledger_path.read_text());assert ledger['active_entry']==packet['entry'];entry=next(e for e in ledger['entries'] if e['id']==packet['entry'])
for step,action,names in [('source_identity_description_slot_laterality','Resolve actual ElderBob507 item541, brinestalk/crook description, exact Hand201/6 manager and full inherited one-hand base metadata.',['source-packet.json','weapon-metadata.json']),('select_correct_body_and_references','Choose fixed ordinary older male body and actual Primitive Tools walking-stick texture/definition, recording historical version and donor-size limits.',['source-comparison.png']),('construct_and_overlay_one_item','Construct continuous brinestalk crook and separate native accent; overlay one item at a provisional baseline palm without remapping source mutation hand.',['canonical-pattern.svg','detail-region.svg','fit-controls.json','constructed-neutral-context.png','constructed-red-item-context.png','imagegen-prompt.txt'])]:
    entry['process_log'].append(dict(timestamp=packet['recorded_at'],step=step,action=action,inputs=[ref(HERE/'source-packet.json')],outputs=[ref(HERE/n) for n in names],review='Source identity and actual Hand/6 binding retained separately from ordinary-body display proxy. Crook is continuous; donor straight shape is style only. Ready/native mutation attachment not claimed.',result='PASS'))
entry.update(current_step='imagegen_refine_in_context_on_unchanged_body',known_issues=['Actual mutation-managed Hand201/6 attachment and ready/native state acceptance remain pending full-set assembly; ordinary-base authoring proxy is explicitly separate.'])
ledger['updated_at']=packet['recorded_at'];ledger_path.write_bytes((json.dumps(ledger,indent=2)+'\n').encode());print('Prepared source-bound brinestalk crook and exact mutation-hand metadata; ordinary-body display proxy only.')
