"""Record complete directional horn authoring and explicit padded physical frame."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
assert not (HERE/'authoring-review.json').exists()
model=json.loads((HERE/'model.json').read_text());bm=json.loads((BODY/'model.json').read_text());checks={}
for f,rows in model['views'].items():
    body=read(HERE/f'original-body-{f}.png');original=read(BODY/f'selected-{f}.png');assert np.array_equal(np.array(body)[128:],np.array(original));assert not np.array(body)[:128,:,3].any()
    layers={};stats={}
    for depth in ['near','far']:
        item=read(HERE/f'intact-{depth}-{f}.png');detail=read(HERE/f'detail-{depth}-{f}.png');a=np.array(item);pattern=np.array(read(HERE/f'patched-constructed-{depth}-{f}.png'));assert np.array_equal(a[:,:,3],pattern[:,:,3]);assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2]);bounds=item.getchannel('A').getbbox()
        if bounds:assert bounds[1]>=16 and bounds[0]>0 and bounds[2]<512
        layers[depth]=Image.alpha_composite(item,detail);stats[depth]=dict(full_alpha_unchanged=True,neutral_rgb=True,bounds=bounds)
    expected=Image.alpha_composite(Image.alpha_composite(layers['far'],body),layers['near']);assert np.array_equal(np.array(expected),np.array(read(HERE/f'assembled-{f}.png')))
    for row in rows:
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256'];base=bm['views'][f][0];assert abs(row['height']/1152-base['height']/1024)<1e-12
        for y in [0,100,950]:
            before=base['center_z']+(512-y)*base['height']/1024;after=row['center_z']+(576-(y+128))*row['height']/1152;assert abs(before-after)<1e-12
    checks[f]=dict(original_body_pixels_preserved=True,identical_physical_frame_after_padding=True,exact_recomposition=True,layers=stats)
assert not np.array(read(HERE/'intact-far-south.png'))[:,:,3].any()
assert not np.array(read(HERE/'intact-near-north.png'))[:,:,3].any()
far=np.array(read(HERE/'intact-far-east.png'))[:,:,3];near=np.array(read(HERE/'intact-near-east.png'))[:,:,3];body=np.array(read(HERE/'original-body-east.png'))[:,:,3]
assert ((far>128)&(body>128)).any() and ((far>128)&(body<128)&(near<128)).any(),'Profile far root must be hidden while some far horn stays visible.'
binding=model['actual_equipped_binding'];assert binding['id']==288 and binding['laterality']==0 and binding['equipped']['instance']==575
reason=('Inspected pair continuity, tapered grooved-bone silhouette, distinct profile near/far overlap, rear root coverage, full sources before depth, native w/W palette and intended-size views. One contextual refinement selected; manual groove overrun patched before it and all initial evidence retained. Complete roots/hidden bone retained with separate layer order, not body-shaped cutouts. Top padding128 preserves every original body pixel, physical pixel scale and world landmark mapping across all facings. Actual natural Head288/0 binding retained. Native physical-frame/headgear acceptance and Yrame named mutations/outfit remain pending full-set generation.')
review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',scope='Generation authoring only',reason=reason,checks=checks,structural_gate=ref(HERE/'first-refinement-structural-review.json'),new_imagegen_calls=1,second_isolation_call=False,native_acceptance=model['native_acceptance'])
write(HERE/'authoring-review.json',review);write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
path=ROOT/'evidence/conversion-ledger.json';d=json.loads(path.read_text());ident='FIT-YRAME-HORNS-HEAD-0';assert d['active_entry']==ident;e=next(x for x in d['entries'] if x['id']==ident)
for step,action,names in [
 ('retrieve_isolated_item_and_masks','Register same contextual neutral bone into complete per-facing near/far sources; complete hidden roots and retain independent native gold detail without second generative isolation.',['register-horns.py','registration-decisions.json','full-item-comparison.png']),
 ('recompose_check_cuffs_attachment_occlusion_all_views','Replace historical frontal-pair profile with distinct near/far head depth and rear root coverage; preserve all body pixels and physical placement through explicit shared top padding.',['model.json','assembly-comparison.png','depth-off-comparison.png','near-far-ownership-comparison.png']),
 ('review_game_scale_and_palette','Inspect source w primary/W gold detail, full pair and intended-size cardinal displays; retain pending natural-head/gear precedence, padded native frame and named mutation assembly.',['independent-palette-comparison.png','game-scale-review.png','authoring-review.json','artifact-manifest.json'])]:
    e['process_log'].append(dict(timestamp=review['timestamp'],step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'refined-red-context.png'),ref(HERE/'first-refinement-structural-review.json')],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
e.pop('apparel_occlusion',None);e['natural_equipment_occlusion']=dict(representation='Intact near/far bone + original head layer depth',order='far -> original body/head -> near',canonical_alpha='Whole physical horn silhouette including hidden roots; no garment/sleeve mask',frame=model['frame_mapping'],native_binding='Pending full-set generation gate')
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),registration_summary='Separate great grooved natural horn pair with distinct near/far profile and rear head depth. Complete roots, w/W tint and original body retained; shared top padding preserves physical placement. Actual Head288/0 and Yrame native mutation/outfit acceptance pending.',native_acceptance=model['native_acceptance'])
next_id='ITEM-HORNS';next_e=next(x for x in d['entries'] if x['id']==next_id);next_e.update(status='IN PROGRESS',current_step='resolve_item_identity_description_palette');d.update(active_entry=next_id,updated_at=review['timestamp']);assert [x['id'] for x in d['entries'] if x['status']=='IN PROGRESS']==[next_id];write(path,d)
print('Directional horn art generation-ready; physical mapping preserved. Only Horns aggregate is active.')
