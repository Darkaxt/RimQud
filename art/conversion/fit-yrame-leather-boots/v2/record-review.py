"""Record complete fore-pair boot generation evidence; defer native acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(768,1152)


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def image(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,v):(HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())


assert not (HERE/'authoring-review.json').exists()
model=read(HERE/'model.json');bm=read(ROOT/model['base_model']);assert ref(ROOT/model['base_model'])['sha256']==model['body_sha256']
assert model['actual_equipped_binding']['id']==297 and model['laterality']==16
assert bm['source_anatomy']['hind_group']['equipped'] is None
checks={}
for f in ['south','east','north']:
    base=Image.new('RGBA',SIZE)
    for r in sorted(bm['views'][f],key=lambda r:r['layer']):
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256'];base.alpha_composite(image(ROOT/r['public_file']))
    assert np.array_equal(np.array(base),np.array(image(HERE/f'original-body-{f}.png')))
    pattern=np.array(image(HERE/f'constructed-boots-{f}.png'))
    names=['far','near'] if f=='east' else ['left','right']
    full=Image.new('RGBA',SIZE)
    for name in names:
        part=image(HERE/f'intact-{name}-{f}.png');wire=image(HERE/f'wire-{name}-{f}.png')
        if f=='east':manual=np.array(image(HERE/f'boot-{name}-east.png'))
        else:
            manual=pattern.copy()
            if name=='left':manual[:,384:]=0
            else:manual[:,:384]=0
        assert np.array_equal(np.array(part)[:,:,3],manual[:,:,3])
        assert np.array_equal(np.array(Image.alpha_composite(part,wire)),np.array(part))
        if f=='north':assert not np.array(wire)[:,:,3].any()
        full.alpha_composite(part)
    assert np.array_equal(np.array(full),np.array(image(HERE/f'intact-boots-{f}.png')))
    for r in model['views'][f]:
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
        for key in ['size','contact','width','height','center_x','center_z']:assert r[key]==bm['views'][f][0][key],(f,key)
        a=np.array(image(ROOT/r['public_file']));assert (np.ptp(a[:,:,:3].astype(int),axis=2)==0).all();assert not a[a[:,:,3]==0,:3].any()
    result=image(HERE/f'assembly-{f}.png')
    if f=='north':
        expected=Image.alpha_composite(full,base)
        opaque=np.array(base)[:,:,3]==255
        assert np.array_equal(np.array(result)[opaque],np.array(base)[opaque])
        assert all(r['layer']<0 for r in model['views'][f])
    else:
        overlay=image(HERE/f'overlay-{f}.png');assert not np.array(overlay)[940:,:,3].any(),'Closed boots cannot restore bare fore hooves'
        expected=Image.alpha_composite(Image.alpha_composite(base,full),overlay)
        visible_bare=(np.array(base)[:,:,3]==255)&(np.array(full)[:,:,3]==0)
        assert np.array_equal(np.array(result)[visible_bare],np.array(base)[visible_bare])
    assert np.array_equal(np.array(expected),np.array(result))
    checks[f]=dict(original_body_rgba_unchanged=True,full_physical_boot_alphas_unchanged=True,
                   neutral_wire_recomposition_exact=True,physical_frame_unchanged=True,
                   no_baked_color_or_zero_alpha_rgb=True,hind_group_equipped=False,
                   no_bare_fore_hoof_overlay=True,north_original_opaque_body_unchanged=(f=='north'),exact_depth_recomposition=True)
now=datetime.now(timezone.utc).isoformat()
reason='Inspected source glyph/native binding and actual VAE closed-boot icon, selected fore/hind anatomy, preconstruction per-view fit contract, full manual pair, actual contextual refinement, full leather continuation and independent editable wire. Registered geometry covers fore shins/hooves with continuous closed shafts, toes and soles. Curved cuff-entry visibility restores original shin only; no bare fore hoof is painted above leather. Profile near/far overlap is natural. North original bare hind legs/hooves occlude intact fore boots, with no duplicated hind footwear or rear lace ladder. Body and shared physical frame remain fixed. Neutral/native w/y, full-source/depth-off, all facings at matched scale and intended-size art reviewed.'
write('authoring-review.json',dict(recorded_at=now,status='PASS',scope='Generation authoring only',reason=reason,checks=checks,
      fit_contract=ref(HERE/'fit-contract.json'),selected_model=ref(HERE/'model.json'),
      per_view=dict(south='Inner fore pair wears closed boots; both outer hind hooves stay bare. Original legs enter curved cuffs; wire belongs to front boot faces.',
                    east='Fore pair beneath upright torso is booted, near-over-far. Two hind feet remain bare at the rear. Complete source far boot retained under near boot.',
                    north='Visible hind legs/hooves remain original bare body. Fore boots behind them retain full hidden alpha; plain heel seams, no rear-facing wire.',
                    west='Mirror exact east pair/body/cuff masks; fore Feet297/16 binding and common physical scale unchanged.'),
      authored_limits=['Native joint/tailoring coordinates unknown; all boot anchor geometry and hidden rear heel projections are authored estimates.',
                       'Source figure changes do not alter production geometry; per-part sampling transfers leather only.',
                       'Rear hidden leather shares actual profile plain-leather samples; no recovery of unseen generated detail claimed.',
                       'Approximately4px sole thickness below bare contact is recorded; body pivot/contact is not shifted.'],
      actual_contextual_imagegen_calls=1,second_isolation_call=False,
      deformation='Identity fit constructed for this body. Regional body-class work is curved cuff entry and explicit fore/hind depth, not forced bitmap deformation.',
      native_acceptance=model['native_acceptance']))
write('artifact-manifest.json',dict(recorded_at=now,entry='FIT-YRAME-LEATHER-BOOTS-FEET-16',artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
path=ROOT/'evidence/conversion-ledger.json';ledger=read(path);assert ledger['active_entry']=='FIT-YRAME-LEATHER-BOOTS-FEET-16';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
for step,action,names in [
 ('recompose_check_cuffs_attachment_occlusion_all_views','Compare closed fore-foot coverage, curved cuff entry and natural near/far/hind depth against every fit-contract row.',['model.json','assembly-comparison.png','footwear-comparison.png','intact-boots-comparison.png','depth-off-comparison.png','body-mask-comparison.png','body-overlay-comparison.png','authoring-review.json']),
 ('review_game_scale_and_palette','Review intended-size footwear and independent native w leather/y wire on unchanged B lower-body anatomy.',['independent-palette-comparison.png','wire-detail-comparison.png','game-scale-review.png']),
 ('reprocess_under_regional_curved_v1','Reconcile source-bound full boots, actual contextual leather, completed hidden regions and late original-body cuff/rear depth.',['authoring-review.json','artifact-manifest.json','registration-decisions.json','continuation-comparison.png'])]:
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'fit-contract.json'),ref(HERE/'generation-receipt.json')],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),
             current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),
             registration_summary='Selected v2 closed fore Feet297/16 pair on current centauroid. Full physical leather/wire, curved cuff entry and original hind depth separate; added hind feet remain bare. Shared body/frame unchanged. Actual native equipment and full outfit acceptance pending.')
entry['apparel_workflow']['status']='GENERATION READY'
next_entry=next(e for e in ledger['entries'] if e['id']=='ITEM-LEATHER-BOOTS');assert not next_entry['generation_ready'];next_entry.update(status='IN PROGRESS',current_step='resolve_item_identity_description_palette')
ledger.update(active_entry=next_entry['id'],updated_at=now);path.write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Equipped fore-pair boot fitting generation-ready. Leather Boots inventory aggregate is now sole active entry; native acceptance remains deferred.')
