"""Fit the same complete utility knife to Argyve's ordinary male base."""
from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,math,shutil
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=ROOT/'art/conversion/fit-human-female-steel-utility-knife/v1'
BODY=ROOT/'art/conversion/body-human-male/v2'
SIZE=(512,1024);FACES=['south','east','north'];FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'authoring-review.json').exists(), 'Preserve reviewed registrations.'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(name,data):(HERE/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,color):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color)/255));return Image.fromarray(a)

packet=json.loads((SOURCE/'source-packet.json').read_text());metadata=json.loads((SOURCE/'weapon-metadata.json').read_text())
for row in metadata['inheritance']:
    assert sha(Path(row['file']))==row['sha256'],row['blueprint']
for evidence in [metadata['handedness']['physics_default'],metadata['handedness']['runtime_requirement_semantics'],metadata['donor_size_reference']['definition'],metadata['donor_size_reference']['load_folders'],metadata['donor_size_reference']['base_defs'],packet['donor_reference']]:
    assert sha(Path(evidence['file']))==evidence['sha256']
actors=json.loads((ROOT/'art/village/sources.json').read_text())['actors'];bindings=[]
for actor in actors:
    for resident in actor['native_instances']:
        for part in resident['parts']:
            if (part.get('equipped') or {}).get('blueprint')=='Steel Utility Knife':
                bindings.append(dict(creature=actor['creature'],resident={k:v for k,v in resident.items() if k!='parts'},part=part))
assert len(bindings)==1 and bindings[0]['creature']=='Argyve' and bindings[0]['resident']['gender']=='male'
part=bindings[0]['part'];assert part['id']==320 and part['laterality']==2 and part['manager'] is None
assert part['equipped']['instance']==588 and part['equipped']['description']==packet['original']['description']
resident=next(r for a in actors for r in a['native_instances'] if r['instance']==519)
occupied=[p for p in resident['parts'] if (p.get('equipped') or {}).get('instance')==588]
assert len(occupied)==1
female_body=json.loads((ROOT/'art/conversion/body-human-female/v2/model.json').read_text());bm=json.loads((BODY/'model.json').read_text())
item_scale=female_body['pixel_world_scale']/bm['pixel_world_scale']
assert abs(item_scale*bm['pixel_world_scale']-female_body['pixel_world_scale'])<1e-12
for name in ['canonical-pattern.svg','constructed-canonical.png','canonical-blade-region.png','canonical-handle-region.png','intact-canonical.png','handle-canonical.png']:
    shutil.copyfile(SOURCE/name,HERE/name);assert sha(SOURCE/name)==sha(HERE/name)
metadata.update(recipient_scope='Captured male Argyve519, ordinary Hand320/laterality2; shared male race template fitting.')
metadata['handedness']['evidence']='Full inherited UsesTwoSlots/UsesSlots declarations and audited Physics defaults support the one-handed base class. Captured Argyve item588 occupies ordinary Hand320/2; actor-specific demand remains unexported.'
metadata['handedness']['unknown']='No actor-specific slot-demand event exported; preserve null rather than infer an event result from a single occupied part.'
metadata['size'].update(canonical_source=ref(HERE/'constructed-canonical.png'),selected_refined_source=ref(SOURCE/'intact-canonical.png'),canonical_geometry_identical=True,pixel_world_scale=bm['pixel_world_scale'],raster_scale=item_scale,world_mapping={k:bm['views']['south'][0][k] for k in ['width','height']},source_pixel_world_scale=female_body['pixel_world_scale'],reason='Reuse the identical small folding knife. Male raster compensation preserves its canonical physical size rather than scaling the item up with the recipient. Grip590 remains32px from the canonical lower bound622; weight1 is not length.')
write('weapon-metadata.json',metadata)
controls={'south':dict(grip=[138,555],angle=0,mirror=False),'east':dict(grip=[290,555],angle=-20,mirror=False),'north':dict(grip=[372,555],angle=-40,mirror=True)}
def inverse(c):
    angle=math.radians(c['angle']);co,si=math.cos(angle)/item_scale,math.sin(angle)/item_scale;gx,gy=c['grip'];px=255 if c['mirror'] else 256
    return [co,-si,px-co*gx+si*gy,si,co,590-si*gx-co*gy]
canonical=read(HERE/'intact-canonical.png');detail=read(HERE/'handle-canonical.png');constructed=read(HERE/'constructed-canonical.png')
groups={k:{} for k in ['assembly','palette','full','off','grip','construct']};constructed_sheet=Image.new('RGBA',(1536,1024));red_sheet=constructed_sheet.copy()
model=dict(item='Steel Utility Knife',blueprint='Steel Utility Knife',family='human-male',slot='Hand',laterality=2,canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],observed_bindings=bindings,views={},weapon_metadata=ref(HERE/'weapon-metadata.json'),item_raster_scale=item_scale,binding_scope='Actual male Argyve Hand/2 item. Shared ordinary baseline fitting does not complete his beard, pockets, cosmetics or full named outfit.',policy='Same canonical small folding knife and selected refined material as compatibility fit; separate Y blade/y handle, original hand above item. No new generated body or narrative painting.',west_policy='Mirrored opposite unmarked blade side; actual painted-instance/aim state remains pending.',pose='Stationary authoring display only. One-handed ready profile projects forward horizontally, approximately90deg to upright body. Native ready/resting state remains pending full-set assembly.',native_acceptance='Pending all-conversions gate and native equipment/pose acceptance')
registration={}
for i,facing in enumerate(FACES):
    c=controls[facing];c['inverse_affine']=inverse(c)
    def place(im):
        im=ImageOps.mirror(im) if c['mirror'] else im
        return im.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC).convert('RGBA')
    item=place(canonical);hilt=place(detail);manual=place(constructed)
    for stem,im in [('intact-item',item),('item-detail',hilt),('constructed-item',manual)]:im.save(HERE/f'{stem}-{facing}.png')
    body=read(BODY/f'selected-{facing}.png');mask=Image.new('L',SIZE)
    if facing!='north':
        hx,hy=(124,555) if facing=='south' else (279,555);ImageDraw.Draw(mask).ellipse((hx-36,hy-36,hx+36,hy+36),fill=255)
    mask.save(HERE/f'hand-visibility-{facing}.png');a=np.array(body);hand=a.copy();hand[:,:,3]=np.minimum(a[:,:,3],np.array(mask));hand=Image.fromarray(hand);hand.save(HERE/f'original-hand-{facing}.png')
    equipment=Image.alpha_composite(item,hilt);off=Image.alpha_composite(body,equipment)
    assembled=Image.alpha_composite(equipment,body) if facing=='north' else Image.alpha_composite(off,hand)
    manual_assembly=Image.alpha_composite(manual,body) if facing=='north' else Image.alpha_composite(Image.alpha_composite(body,manual),hand)
    red=tint(body,(255,31,41));red_hand=tint(hand,(255,31,41));red_assembly=Image.alpha_composite(manual,red) if facing=='north' else Image.alpha_composite(Image.alpha_composite(red,manual),red_hand)
    constructed_sheet.paste(manual_assembly,(i*512,0));red_sheet.paste(red_assembly,(i*512,0))
    assembled.save(HERE/f'assembled-{facing}.png');off.save(HERE/f'depth-off-{facing}.png')
    native_item=Image.alpha_composite(tint(item,(255,255,255)),tint(hilt,(177,201,195)))
    native_body=tint(body,(64,164,185));native_hand=tint(hand,(64,164,185))
    palette=Image.alpha_composite(native_item,native_body) if facing=='north' else Image.alpha_composite(Image.alpha_composite(native_body,native_item),native_hand)
    palette.save(HERE/f'qud-palette-{facing}.png')
    for key,im in [('assembly',assembled),('palette',palette),('full',equipment),('off',off),('construct',manual_assembly)]:groups[key][facing]=im
    gx,gy=c['grip'];groups['grip'][facing]=assembled.crop((gx-70,gy-180,gx+90,gy+70)).resize((256,400))
    model['views'][facing]=[]
    for component,stem,role,layer in [('item','intact-item','equipment',-.0002 if facing=='north' else .0018),('item-detail','item-detail','equipment-detail',-.00019 if facing=='north' else .00181),('body-overlay','original-hand','foreground',.0019)]:
        p=HERE/f'{stem}-{facing}.png';r=ref(p);row=dict(bm['views'][facing][0]);row.update(component=component,file=f'human-male-steel-utility-knife-v1-{component}-{facing}.png',public_file=r['path'],sha256=r['sha256'],equipment_key='steel-utility-knife@Hand@2',color_role=role,layer=layer);model['views'][facing].append(row)
    registration[facing]=dict(inverse_affine=c['inverse_affine'],mirror=c['mirror'],item_space_grip=[256,590],body_hand_landmark=c['grip'],body=ref(BODY/f'selected-{facing}.png'),full_item=ref(HERE/f'intact-item-{facing}.png'),original_hand=ref(HERE/f'original-hand-{facing}.png'),scale=item_scale,physical_item_scale_changed=False,body_pixels_changed=False)
constructed_sheet.save(HERE/'constructed-neutral-context.png');red_sheet.save(HERE/'constructed-red-context.png')
for group in groups.values():group['west (mirror)']=ImageOps.mirror(group['east'])
def plate(images,name,title,zoom=False):
    out=Image.new('RGB',(1152,665),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
    for i,(facing,im) in enumerate(images.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,400 if zoom else 512)),(16+i*284,54));d.text((16+i*284,584),facing.upper(),font=FONT,fill='#e3cf43')
    d.text((18,622),'Fixed original body; same physical knife. Stationary display only; native ready/resting poses pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
for key,name,title,zoom in [('construct','constructed-comparison.png','MANUAL SOURCE / same small folding knife fitted to fixed male base',False),('assembly','assembly-comparison.png','MALE / STEEL UTILITY KNIFE / lower grip and full canonical blade',False),('palette','independent-palette-comparison.png','NATIVE COLORS / Argyve body c, steel blade Y and handle y',False),('full','full-item-comparison.png','FULL KNIFE / intact blade, folding pivot and handle before body depth',False),('off','depth-off-comparison.png','DEPTH OFF / intact tool before original palm and rear body ownership',False),('grip','grip-comparison.png','GRIP / original palm over lower handle; same blade and pivot',True)]:plate(groups[key],name,title,zoom)
small=Image.new('RGB',(560,370),'#142823');draw=ImageDraw.Draw(small)
for i,(facing,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*140+45,20),thumb);thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*140+20,138),thumb);draw.text((i*140+4,344),facing.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
donor=Path(packet['donor_reference']['file']);original_file=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/packet['original']['reference_file'];assert sha(original_file)==packet['original']['reference_sha256']
comparison=Image.new('RGB',(1152,665),'#142823');draw=ImageDraw.Draw(comparison);draw.text((18,14),'SOURCE CHAIN / Qud folding knife > actual mod reference > fixed male fitting',font=FONT,fill='#e3cf43')
orig=read(original_file).resize((160,240),Image.Resampling.NEAREST);comparison.paste(orig,(30,80),orig)
don=read(donor);bounds=don.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();don=don.crop(bounds);don.thumbnail((160,240));comparison.paste(don,(220,80),don)
for y,t in [(350,'Qud: dull folding utility knife'),(380,'VWE CombatKnife: outline only'),(410,'No military guard / new paint scene'),(440,'Observed Argyve519 > Hand320/2'),(470,'One-hand declaration; event unknown'),(500,'Same canonical physical item size')]:draw.text((20,y),t,font=FONT,fill='#e5e8d8')
for i,facing in enumerate(FACES):
    bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(groups['assembly'][facing]);comparison.paste(bg.convert('RGB').resize((210,420)),(450+i*230,80));draw.text((450+i*230,530),facing.upper(),font=FONT,fill='#e3cf43')
comparison.save(HERE/'source-comparison.png')
packet.update(entry='FIT-HUMAN-MALE-STEEL-UTILITY-KNIFE-HAND-2',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Argyve, captured male519; ordinary male race fitting',race='Human, ordinary male baseline',fitting_scope='Actual captured male ordinary Hand320/2 item588; named cosmetics/outfit and native state not accepted by this fit.',observed_bindings=bindings,body=ref(BODY/'model.json'),weapon_metadata=ref(HERE/'weapon-metadata.json'),shared_source=ref(SOURCE/'source-packet.json'),shared_refinement=dict(context=ref(SOURCE/'refined-red-context.png'),prompt=ref(SOURCE/'imagegen-prompt.txt'),registration=ref(SOURCE/'registration-decisions.json'),selected_item=ref(SOURCE/'intact-canonical.png'),new_imagegen_call=False,reason='Same complete physical item and material already selected; recipient change requires grip/scale/depth fitting, not another drawing.'),frame=dict(canvas=list(SIZE),contact=[256,950],item_space_grip=[256,590],item_scale=item_scale,controls=controls,mirror_anchor='x256 becomes255 under Pillow flip'),assembly_boundary=model['binding_scope'],native_acceptance=model['native_acceptance'])
write('source-packet.json',packet);write('fit-controls.json',controls);write('model.json',model);write('registration-decisions.json',dict(canonical_source=ref(SOURCE/'intact-canonical.png'),source_reused_byte_for_byte=True,new_imagegen_calls=0,second_isolation_call=False,views=registration,material='Selected original contextual refinement and completion reused; no new body, alpha or geometry generation. Exact canonical full blade/handle before per-facing transforms.',pose=model['pose']))
scaleplate=Image.new('RGB',(1152,690),'#142823');draw=ImageDraw.Draw(scaleplate);draw.text((18,14),'SAME KNIFE / female compatibility and male Argyve base / common physical mapping',font=FONT,fill='#e3cf43')
for i,(family,facing) in enumerate([('female','south'),('male','south'),('female','east'),('male','east')]):
    folder=HERE if family=='male' else SOURCE;im=read(folder/f'assembled-{facing}.png');factor=bm['pixel_world_scale']/female_body['pixel_world_scale'] if family=='male' else 1;im=im.resize((round(256*factor),round(512*factor)),Image.Resampling.LANCZOS);x=16+i*284+(256-im.width)//2;y=560-round(475*factor);bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);scaleplate.paste(bg.convert('RGB'),(x,y));draw.line((16+i*284,560,271+i*284,560),fill='#70b8b0');draw.text((16+i*284,592),family.upper()+' / '+facing.upper(),font=FONT,fill='#e3cf43')
draw.text((18,628),'World-size compensation only; knife geometry, selected material and canonical lower grip unchanged.',font=FONT,fill='#e5e8d8');scaleplate.save(HERE/'cross-body-scale-comparison.png')
print('Prepared/registered identical small knife on male base, actual Argyve Hand/2, scale',item_scale,'no new ImageGen call; authoring inspection pending.')
