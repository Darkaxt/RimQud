"""Refit the unchanged physical Vibro Blade to current Yrame palm landmarks.

No new ImageGen call: this is reuse of the inspected full physical item and its
actual v1 contextual refinement. Resting/ready implementation remains deferred.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';SIZE=(768,1152)
FACES=['south','east','north','west']


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def image(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,v):(HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())


def canonical(im):
    a=np.array(im);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)


def tint(im,color):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color)/255));return canonical(Image.fromarray(a))


assert not (HERE/'model.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='FIT-YRAME-VIBRO-BLADE-HAND-2'
entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);be=next(e for e in ledger['entries'] if e['id']=='BODY-YRAME');assert be['generation_ready']
bref=be['current_registration']['model'];assert ref(ROOT/bref['path'])==bref;body=read(ROOT/bref['path']);previous=read(OLD/'source-packet.json');old_model=read(OLD/'model.json')
for r in read(OLD/'artifact-manifest.json')['files']:
    assert ref(ROOT/r['path'])['sha256']==r['sha256'],r['path']
assert hashlib.sha256(Path(previous['donor_reference']['file']).read_bytes()).hexdigest()==previous['donor_reference']['sha256']
ancestry=read(HERE/'blueprint-ancestry.json');assert all('UsesTwoSlots' not in p and 'UsesSlots' not in p for row in ancestry['ancestry'] for p in row['physics'])
default=read(ROOT/'art/conversion/fit-irudad-walking-stick/v1/handedness-evidence.json')['physics_default']
assert hashlib.sha256(Path(default['file']).read_bytes()).hexdigest()==default['sha256'] and not default['default_two_slots']
world_pixel=old_model['views']['south'][0]['height']/1024
scale=world_pixel/body['registration']['pixel_world_size'];grip=[256,570]
handedness=dict(classification='One-hand base class supported; actor-specific event demand unknown',
               ancestry=ref(HERE/'blueprint-ancestry.json'),physics_default=default,
               default_provenance='Previously captured project decompile, file hash verified; no new runtime call.',
               GetSlotsRequiredFor_actor_Hand=None,occupied_exported_parts=[previous['observed_binding']],
               donor_definition=ref(HERE/'donor-definition-evidence.json'),donor_drawSize='No explicit drawSize in inspected Core LongSword definition/ancestry; live graphic value not queried.',
               physical_dimensions='Not exported. Installed description long blade; captured weight3 vs installed2 remains unexplained and is not treated as a length.')
write('handedness-evidence.json',handedness)
controls=dict(south=dict(palm=[208,566],anchor=[218,566],angle=0,roi=[169,532,249,611],depth='near'),
              east=dict(palm=[529,585],anchor=[535,585],angle=15,roi=[480,548,577,626],depth='near'),
              north=dict(palm=[555,588],anchor=[545,588],angle=10,roi=[513,550,598,630],depth='far'),
              west=dict(palm=[238,585],anchor=[232,585],mirror_of='east',depth='far'))
now=datetime.now(timezone.utc).isoformat()
contract=dict(entry=entry['id'],recorded_at=now,status='PLANNED — actual new-body fit review pending',body=bref,
 item_sources=dict(manual=ref(OLD/'constructed-canonical.png'),refined=ref(OLD/'intact-canonical.png'),hilt=ref(OLD/'hilt-canonical.png')),
 frame=body['registration'],canonical_grip=grip,source_world_per_pixel=world_pixel,recipient_raster_scale=scale,
 native_facts='Vibro Blade576 on ordinary Hand292/2, parent Arm291. Opposite Hand294/1 unequipped. Installed matte ionic-plastifer blade/finger-rest hilt, native c/y colors. Actor slot-demand, charge state and exact physical dimensions unknown.',
 authored_estimates='Canonical dimensions/low-handle grip and palm anchors are authoring choices. Preserve v1 physical size; new body does not imply a larger weapon. West far-hand projection is hidden/unknown and estimated from mirrored profile overlap.',
 views=dict(
  south=dict(attachment='Right Hand292 is screen-left. Anchor218,566 sits inside and10px toward body from palm center208,566. Item-space grip256,570 stays30px above pommel and below finger-rest.',direction='Upright display, same intact blade. No claim of resting or drafted pose.',visibility='Original gripping hand covers the handle at contact; blade and finger-rest remain separate, with no forearm contour carried into the weapon.',depth='Body then full blade/hilt, then original right-hand foreground only.'),
  east=dict(attachment='Visible near right palm529,585, handle anchor535,585. Same low item-space grip and unchanged physical size.',direction='Existing15-degree forward lean for authoring display. Future drafted side pose must project forward horizontally,90degrees to upright body.',visibility='Near hand occludes handle; full physical item remains intact beneath it. No independent supporting hand implied.',depth='Body then blade/hilt, then original right-hand foreground.'),
  north=dict(attachment='Right Hand292 is screen-right, palm555,588. Anchor545,588 lies10px inward. Same canonical handle height.',direction='Existing10-degree display lean. Aim/state mapping remains pending.',visibility='Original rear body/hand occludes far weapon where silhouettes overlap. Do not cut hand-shaped holes in full weapon.',depth='Full weapon behind original body/head; no duplicate hand redraw needed.'),
  west=dict(attachment='Same equipped right Hand292 is far-side. Use mirrored profile projection232,585 as an explicit estimate; hidden actual far-hand coordinates were not exported.',direction='Mirror east item geometry/scale, with far-side depth rather than blindly mirroring the near-hand overlay.',visibility='Original visible left arm/body can hide the far right-held weapon; do not relabel item to Hand294 or invent another hand.',depth='Mirrored full weapon behind original west body. Native side/pose acceptance pending.')),
 pose_boundary='Only current authoring display is fitted here. Resting/ready angle/state implementation and review stay in Stage3 final assembly after all generation, per skill/user priority.')
write('fit-contract.json',contract)
packet=dict(previous);packet.update(recorded_at=now,body=bref,frame=body['registration'],race='Human-based named mutant, selected sheep-like centauroid; ordinary right Hand292/2 remains equipped.',
 previous_source=ref(OLD/'source-packet.json'),handedness=ref(HERE/'handedness-evidence.json'),fit_contract=ref(HERE/'fit-contract.json'),
 reused_generation=dict(raw=ref(OLD/'refined-red-context.png'),prompt=ref(OLD/'imagegen-prompt.txt'),registration=ref(OLD/'registration-decisions.json'),review=ref(OLD/'authoring-review.json'),new_imagegen_calls=0,
                       reason='Unchanged independent item source; only body/hand registration changes. Prior contextual body is ordinary-human reference, never claimed as a new-body generation.'),
 assembly_boundary=contract['pose_boundary'],native_acceptance='Pending full-generation gate, actual named Hand292/2, west far-side, equipped and resting/ready state acceptance.')
write('source-packet.json',packet)
source=image(OLD/'intact-canonical.png');normalized=canonical(source)
assert np.array_equal(np.array(source)[:,:,3],np.array(normalized)[:,:,3])
visible=np.array(source)[:,:,3]>0;assert np.array_equal(np.array(source)[visible],np.array(normalized)[visible]);normalized.save(HERE/'canonical-source.png')
source_detail=image(OLD/'hilt-canonical.png');detail=np.array(normalized);detail[:,:,3]=np.where(np.array(normalized)[:,:,3]==255,np.array(source_detail)[:,:,3],0).astype('uint8');detail=canonical(Image.fromarray(detail));detail.save(HERE/'canonical-hilt-source.png')
write('source-encoding-normalization.json',dict(previous=ref(OLD/'intact-canonical.png'),normalized=ref(HERE/'canonical-source.png'),
      action='Clear RGB only at alpha0; visible RGBA and full alpha unchanged. Derive opaque-interior hilt tint so neutral layer recomposition preserves the full silhouette.',
      discarded_invisible_rgb_pixels=int(((np.array(source)[:,:,3]==0)&(np.array(source)[:,:,:3].max(2)>0)).sum()),production_body_used=False))
manual=canonical(image(OLD/'constructed-canonical.png'));palette={k:tuple(bytes.fromhex(v)) for k,v in read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'].items()}
model=dict(item='Vibro Blade',blueprint='Vibro Blade',family='yrame',slot='Hand',laterality=2,canvas=list(SIZE),contact=body['registration']['contact'],base_model=bref['path'],body_sha256=bref['sha256'],frame_mapping=body['registration'],
 observed_binding=previous['observed_binding'],views={},fit_contract=ref(HERE/'fit-contract.json'),
 policy='One unchanged full physical weapon, low handle grip, original hand/body depth and independent c/y tint. No clothing in primary preview, no new generation, no charge effect or ready-pose implementation.',
 west_policy='Explicit far-side right-hand display: geometry mirrors east, depth differs. Hidden far hand projection is authored; no switch to left Hand294.',
 pose='Provisional display only; resting/ready game-state presentation remains final-assembly work after full-set generation.',native_acceptance=packet['native_acceptance'])
groups={k:{} for k in ['manual','assembly','palette','full','off','hand','mask','grip']};placed={};stats={}
for f in FACES:
    base=Image.new('RGBA',SIZE);native_body=Image.new('RGBA',SIZE)
    for row in sorted(body['views'][f],key=lambda r:r['layer']):
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256'];im=image(ROOT/row['public_file']);base.alpha_composite(im);native_body.alpha_composite(tint(im,palette['B'] if row['color_role']=='detail' else palette['w']))
    base.save(HERE/f'original-body-{f}.png')
    c=controls[f]
    if f=='west':
        item,hilt,construction=[ImageOps.mirror(im) for im in placed['east']]
        hand=ImageOps.mirror(groups['hand']['east']);mask=ImageOps.mirror(groups['mask']['east'])
        inverse=None
    else:
        t=np.deg2rad(c['angle']);rot=np.array([[np.cos(t),-np.sin(t)],[np.sin(t),np.cos(t)]])
        inv=rot.T/scale;shift=np.array(grip)-inv@np.array(c['anchor']);inverse=[inv[0,0],inv[0,1],shift[0],inv[1,0],inv[1,1],shift[1]]
        def place(im):return canonical(im.transform(SIZE,Image.Transform.AFFINE,inverse,Image.Resampling.BICUBIC))
        item,hilt,construction=place(normalized),place(detail),place(manual)
        h=np.array(hilt);h[:,:,:3]=np.array(item)[:,:,:3];h[np.array(item)[:,:,3]<255,3]=0;hilt=canonical(Image.fromarray(h))
        ba=np.array(base);x0,y0,x1,y1=c['roi'];cx,cy=c['palm'];crop=ba[y0:y1,x0:x1]
        light=(crop[:,:,:3].mean(2)>90)&(crop[:,:,3]>128);labels,n=ndimage.label(light);label=int(labels[cy-y0,cx-x0]);assert label>0,(f,'hand interior')
        inner=labels==label;assert 500<inner.sum()<3500,(f,int(inner.sum()))
        distance=ndimage.distance_transform_edt(~inner);ink=(crop[:,:,:3].mean(2)<160)&(crop[:,:,3]>0)
        m=np.zeros((SIZE[1],SIZE[0]),dtype='uint8');m[y0:y1,x0:x1]=np.uint8(inner|(ink&(distance<=8)))*255
        fg=next(row for row in body['views'][f] if row['component']=='body' and row['color_role']=='foreground');a=np.array(image(ROOT/fg['public_file']));m[a[:,:,3]==0]=0
        a[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*m/255));hand=canonical(Image.fromarray(a));mask=Image.fromarray(m).convert('RGBA')
        ax,ay=c['anchor'];assert m[ay,ax]>200 and np.array(hand)[ay,ax,3]>200,(f,'grip inside original palm')
    placed[f]=(item,hilt,construction)
    assert np.array_equal(np.array(Image.alpha_composite(item,hilt)),np.array(item))
    item.save(HERE/f'intact-item-{f}.png');hilt.save(HERE/f'item-detail-{f}.png');hand.save(HERE/f'original-hand-{f}.png');mask.getchannel('R').save(HERE/f'hand-visibility-{f}.png')
    off=Image.alpha_composite(base,item)
    if c['depth']=='far':assembly=Image.alpha_composite(item,base);suggestion=Image.alpha_composite(construction,base)
    else:assembly=Image.alpha_composite(off,hand);suggestion=Image.alpha_composite(Image.alpha_composite(base,construction),hand)
    equipment=Image.alpha_composite(tint(item,palette['c']),tint(hilt,palette['y']))
    colored=Image.alpha_composite(equipment,native_body) if c['depth']=='far' else Image.alpha_composite(Image.alpha_composite(native_body,equipment),tint(hand,palette['w']))
    for key,im in [('manual',suggestion),('assembly',assembly),('palette',colored),('full',item),('off',off),('hand',hand),('mask',mask)]:
        im=canonical(im);groups[key][f]=im;im.save(HERE/f'{key}-{f}.png')
    ax,ay=c['anchor'];groups['grip'][f]=assembly.crop((ax-85,ay-125,ax+85,ay+75))
    model['views'][f]=[]
    for component,p,role,layer in [('item',HERE/f'intact-item-{f}.png','equipment',-.0002 if c['depth']=='far' else .0018),('item-detail',HERE/f'item-detail-{f}.png','equipment-detail',-.00019 if c['depth']=='far' else .00181)]+([] if c['depth']=='far' else [('body-overlay',HERE/f'original-hand-{f}.png','foreground',.0019)]):
        row=dict(body['views'][f][0]);rr=ref(p);row.update(component=component,color_role=role,file=f'yrame-vibro-blade-v2-{component}-{f}.png',public_file=rr['path'],sha256=rr['sha256'],layer=layer,equipment_key='vibro-blade@Hand@2');row.pop('native_part',None);row.pop('mutation_anatomy',None);model['views'][f].append(row)
    stats[f]=dict(anchor=c['anchor'],palm=c['palm'],inverse_affine=inverse,mirror_of=c.get('mirror_of'),depth=c['depth'],canonical_item_space_grip=grip,
                  scale=scale,source_world_per_pixel=world_pixel,target_world_per_pixel=body['registration']['pixel_world_size'],original_body=ref(HERE/f'original-body-{f}.png'),hand=ref(HERE/f'original-hand-{f}.png'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)


def plate(key,name,title,zoom=False):
    out=Image.new('RGB',(1200,570 if zoom else 700),'#142823');d=ImageDraw.Draw(out);d.text((18,15),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(groups[key].items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);display=bg.resize((280,330) if zoom else (280,420),Image.Resampling.LANCZOS)
        out.paste(display.convert('RGB'),(10+i*300,55));d.text((15+i*300,440 if zoom else 500),f.upper()+(' / FAR' if controls[f]['depth']=='far' else ' / NEAR'),font=font,fill='#e3cf43')
    d.text((18,out.height-55),'Unchanged weapon size and body. Authoring display only; resting/ready/native state remains pending.',font=font,fill='#e5e8d8');out.save(HERE/name)


for key,name,title,zoom in [('manual','manual-fit-comparison.png','MANUAL SOURCE / unchanged construction on the selected body',False),('assembly','assembly-comparison.png','VIBRO BLADE / reused actual matte source, new-body palm fit',False),('palette','independent-palette-comparison.png','NATIVE c BLADE / y HILT / original w hands and B lower body',False),('full','full-item-comparison.png','FULL ITEM / physical size retained before hand/body depth',False),('off','depth-off-comparison.png','DEPTH OFF / compare complete tool with original body/hand ownership',False),('grip','grip-comparison.png','GRIP / low handle, inward front/back palm contact; west right hand is far',True)]:plate(key,name,title,zoom)
small=Image.new('RGB',(600,390),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((64,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*150+40,20),thumb);big=thumb.resize((128,192),Image.Resampling.NEAREST);small.paste(big,(i*150+10,140),big);d.text((i*150+5,360),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
write('model.json',model)
write('registration-decisions.json',dict(recorded_at=now,source=ref(HERE/'canonical-source.png'),hilt=ref(HERE/'canonical-hilt-source.png'),views=stats,
 physical_scale=dict(source_world_per_pixel=world_pixel,target_world_per_pixel=body['registration']['pixel_world_size'],raster_scale=scale,nominal450px_length_world=450*world_pixel,handle102px_world=102*world_pixel,reason='Unit/frame compensation only; no enlargement for the recipient Big/centauroid body.'),
 new_imagegen_calls=0,reused_actual_refinement=ref(OLD/'refined-red-context.png'),source_body_never_used=True,pose_boundary=contract['pose_boundary']))
for step,phase,names,text in [
 ('source_identity_description_slot_laterality','Resolve current Hand292/2, inherited slot evidence and source conflicts',['source-packet.json','blueprint-ancestry.json','handedness-evidence.json','donor-definition-evidence.json'],'Actual Vibro Blade576 remains on right Hand292/2. One-hand base class supported, actor-sensitive slot demand unknown; captured weight3 versus installed2 and unknown charge state retained.'),
 ('select_correct_body_and_references','Current centauroid and unchanged long matte blade source',['fit-contract.json','source-encoding-normalization.json'],'Current body and v1 full item/refinement/donor hashes verified. Record lower handle grip, body-relative size and far-side west projection before fitting.'),
 ('construct_and_overlay_one_item','Parametric full-weapon refit on original palms — review pending',['refit-blade.py','manual-fit-comparison.png','assembly-comparison.png','grip-comparison.png','registration-decisions.json','model.json'],'Same physical tool, new hand anchors and0.9726776 raster scale for frame compensation. South/north grips inward; west mirrors geometry but draws far, without switching equipped hand. Visual review pending.'),
 ('imagegen_refine_in_context_on_unchanged_body','Reuse actual v1 contextual refinement; no new generation',[], 'No new call: unchanged independent weapon retains actual prior contextual refinement and completed matte surface. Prior ordinary-human context is explicitly historical source evidence, not a claimed generation on the current body.'),
 ('retrieve_isolated_item_and_masks','Reuse intact neutral item and hilt, derive current original-hand masks',['canonical-source.png','canonical-hilt-source.png','source-encoding-normalization.json','full-item-comparison.png'],'Visible canonical RGBA/full alpha preserved; only invisible RGB cleared. Hilt tint constrained to opaque interiors to preserve neutral silhouette. New masks use actual current palm interiors/rims; no body-shaped weapon cutout.')]:
    outputs=[ref(HERE/n) for n in names]
    if step=='imagegen_refine_in_context_on_unchanged_body':outputs=[ref(OLD/'imagegen-prompt.txt'),ref(OLD/'refined-red-context.png'),ref(OLD/'authoring-review.json')]
    entry['process_log'].append(dict(timestamp=now,step=step,phase=phase,action=text,inputs=[bref,ref(OLD/'source-packet.json'),ref(OLD/'intact-canonical.png')],outputs=outputs,review=text,result='REQUIRES REVIEW' if step=='construct_and_overlay_one_item' else 'PASS'))
entry.update(current_step='recompose_check_cuffs_attachment_occlusion_all_views',generation_ready=False,current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),
 art_review=dict(status='REQUIRES REVIEW',reason='Current-body display fit with reused weapon. Inspect actual grip/contact, handedness/depth and preserved physical scale; no ready-pose or native acceptance.'),
 registration_summary='Current v2 candidate on selected centauroid. Same full matte blade/hilt and physical size, low item-space grip, inward right-hand anchors and explicit far-side west depth. Final authoring review pending.')
ledger['updated_at']=now;(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Reused actual refined full weapon at fixed physical size and fitted current palms; no new generation. All-view grip review pending.')
