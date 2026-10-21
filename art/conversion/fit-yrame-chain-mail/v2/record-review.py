"""Record complete mail authoring evidence; native validation stays deferred."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SELECTED=HERE/'arm-owner-v2';SIZE=(768,1152)


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def image(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,v):(HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())


assert not (HERE/'authoring-review.json').exists()
model=read(SELECTED/'model.json');body=read(ROOT/model['base_model']);assert ref(ROOT/model['base_model'])['sha256']==model['body_sha256']
checks={}
for facing in ['south','east','north']:
    base=Image.new('RGBA',SIZE)
    for r in sorted(body['views'][facing],key=lambda r:r['layer']):
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256'];base.alpha_composite(image(ROOT/r['public_file']))
    assert np.array_equal(np.array(base),np.array(image(HERE/f'original-body-{facing}.png')))
    cloth=image(HERE/f'intact-mail-{facing}.png');detail=image(HERE/f'item-detail-{facing}.png')
    pattern=image(HERE/f'constructed-cloth-{facing}.png')
    assert np.array_equal(np.array(cloth)[:,:,3],np.array(pattern)[:,:,3])
    assert np.array_equal(np.array(Image.alpha_composite(cloth,detail)),np.array(cloth))
    rows=model['views'][facing];assert [r['component'] for r in rows]==['item','item-detail','body-overlay']
    for r in rows:
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
        for key in ['size','contact','width','height','center_x','center_z']:assert r[key]==body['views'][facing][0][key],(facing,key)
        a=np.array(image(ROOT/r['public_file']));assert (np.ptp(a[:,:,:3].astype(int),axis=2)==0).all();assert not a[a[:,:,3]==0,:3].any()
    mask=np.array(Image.open(SELECTED/f'body-visibility-{facing}.png').convert('L'))
    source=next(r for r in body['views'][facing] if r['component']=='body' and r['color_role']=='foreground')
    fg=np.array(image(ROOT/source['public_file']));expected=fg.copy();expected[:,:,3]=np.uint8(np.round(expected[:,:,3].astype(float)*mask/255));expected[expected[:,:,3]==0,:3]=0
    overlay=image(SELECTED/f'body-overlay-{facing}.png');assert np.array_equal(expected,np.array(overlay))
    result=Image.alpha_composite(Image.alpha_composite(base,cloth),overlay)
    assert np.array_equal(np.array(result),np.array(image(SELECTED/f'assembly-{facing}.png')))
    selected=(fg[:,:,3]==255)&(mask==255)
    assert np.array_equal(np.array(result)[selected],fg[selected])
    checks[facing]=dict(original_body_rgba_unchanged=True,full_garment_alpha_unchanged=True,
                        neutral_detail_recomposition_exact=True,physical_frame_unchanged=True,
                        zero_alpha_rgb_zero=True,body_mask_uses_only_original_arm_foreground=True,
                        body_fleece_overlay_rows=0,opaque_arm_rgba_error=0,exact_depth_recomposition=True)
now=datetime.now(timezone.utc).isoformat()
reason='Inspected original glyph/metadata and actual VAE mail references, per-view preconstruction contract, full manual shirt and original-body mask corrections, actual contextual output, full material completion, neutral/native palette, mask-off/on, same-scale all-view torso and intended-size plates. Connected shoulders, natural round neckline and curved short-sleeve mouths retain complete original arms/hands. Long front panel covers forechest; short dorsal hem leaves rear fleece exposed. Fleece stays under the shirt, not in its foreground mask. One full garment and independent y/Y metal regions; selected body/frame unchanged. West mirrors east.'
write('authoring-review.json',dict(recorded_at=now,status='PASS',scope='Generation authoring only',reason=reason,checks=checks,
      selected_model=ref(SELECTED/'model.json'),fit_contract=ref(HERE/'fit-contract.json'),
      per_view=dict(south='Round neck, connected shoulders, curved short cuffs and complete original arms/hands; long anterior hem covers upper forequarters.',
                    east='Near sleeve opens onto actual original arm; hand ownership excludes adjacent torso/fleece. Short dorsal hem and long forechest drop agree with front/back.',
                    north='Connected shoulders/back and short sleeves; short dorsal hem leaves rear fleece exposed. Original hands complete, no shoulder gaps.',
                    west='Mirror exact east cloth/body/mask; same Body287/0 binding and scale.'),
      actual_contextual_imagegen_calls=1,second_isolation_call=False,
      deformation='Identity fit constructed for selected body. No unnecessary whole-image stretch or regional mesh warp. Curved body-class ownership and full-source completion follow regional-curved-v1.',
      authored_interpretation='Shirt cut/neck/sleeves and long-front/short-dorsal hem are authored centauroid adaptation; no recovered native tailoring coordinates or new barding item claimed.',
      native_acceptance=model['native_acceptance']))
write('artifact-manifest.json',dict(recorded_at=now,entry='FIT-YRAME-CHAIN-MAIL-BODY-0',artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
path=ROOT/'evidence/conversion-ledger.json';ledger=read(path);assert ledger['active_entry']=='FIT-YRAME-CHAIN-MAIL-BODY-0';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
for step,action,outputs in [
    ('recompose_check_cuffs_attachment_occlusion_all_views','Review actual selected centauroid shirt against every fit-contract row, including original-arm/fleece ownership.',[ref(SELECTED/n) for n in ['model.json','assembly-comparison.png','shared-scale-torso-fit-comparison.png','body-mask-comparison.png','body-overlay-comparison.png']]+[ref(HERE/'authoring-review.json')]),
    ('review_game_scale_and_palette','Review independent y/Y mail, original w arms and B fleece at matched scale and intended display size.',[ref(SELECTED/n) for n in ['independent-palette-comparison.png','game-scale-review.png']]+[ref(HERE/'detail-comparison.png')]),
    ('reprocess_under_regional_curved_v1','Reconcile full manual/contextual mail completion, identity body fit, curved cuff masks and late original-arm ownership.',[ref(HERE/n) for n in ['authoring-review.json','artifact-manifest.json','intact-garment-comparison.png','continuation-comparison.png']])]:
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'fit-contract.json'),ref(HERE/'generation-receipt.json')],outputs=outputs,review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),
             current_registration=dict(model=ref(SELECTED/'model.json'),plate=ref(SELECTED/'assembly-comparison.png')),
             registration_summary='Selected centauroid v2 arm-owner fit: source-bound linked steel, connected shoulders/curved cuffs, long front and short dorsal hem, original human arms above full mail and fleece below. Shared body/frame and independent y/Y tint retained; native/outfit acceptance pending.')
entry['apparel_workflow']['status']='GENERATION READY'
next_entry=next(e for e in ledger['entries'] if e['id']=='ITEM-CHAIN-MAIL');assert not next_entry['generation_ready'];next_entry.update(status='IN PROGRESS',current_step='resolve_item_identity_description_palette')
ledger.update(active_entry=next_entry['id'],updated_at=now);path.write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Chain-mail fitting generation-ready; source-item aggregate is now the sole active entry. Native acceptance remains deferred.')
