"""Close the complete three-layout vine correction and preserve editable sources."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OLD=HERE.parent/'v1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-WATERVINE';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);now=datetime.now(timezone.utc).isoformat()
review=read(HERE/'independent-structural-review.json');assert not review['fix_now']
for r in review['inspected_images']+review['read_documents']:assert ref(ROOT/r['path'])['sha256']==r['sha256']
model=read(OUT/'model.json');prior=read(OLD/'registered/model.json');controls=read(HERE/'model-controls.json');source=read(OLD/'source-packet.json')
assert controls['source_layouts']==source['layouts']
for key in ['registration','harvest_states','state_owner','native_effects','native_behavior']:assert model[key]==prior[key]
assert len(model['states'])==3 and read(HERE/'reopen-audit.json')['reopened']
for row,old in zip(model['states'],prior['states']):
    assert row['variant']==old['variant'] and row['native_tile']==old['native_tile']
    for key in ['primary','detail','coverage','detail_coverage']:assert ref(ROOT/row[key]['path'])==row[key]
    for key in ['primary','detail']:
        a=np.array(Image.open(ROOT/row[key]['path']).convert('RGBA'));assert a.shape==(256,256,4) and not np.ptp(a[:,:,:3].astype(int),axis=2).any()
    n=row['variant'];ripe=np.array(Image.open(OUT/f'variant-{n}-ripe-preview.png'));unripe=np.array(Image.open(OUT/f'variant-{n}-unripe-preview.png'));assert np.array_equal(ripe[:,:,3],unripe[:,:,3])
for r in [source['native_definition'],source['donor_reference']]:assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
reason='Inspected all three layouts, original/new basal closeups, source metadata, exact wafer positions, neutral/ripe/unripe rows and intended-size examples. Basal tendrils now begin inside their own eight actual stem bases rather than a shared copied y row. Wafer tethers meet evaluated curved stems; source crooked paths/wafer centers and counts remain bound to the native layouts. Main stems and low-relief swollen wafers are editable in the saved Blender source, with simple neutral tones and black contours. Fresh independent review found no demonstrated structural FIX NOW defect. Native RandomTile, Harvestable colors/yield, Fireflies and physics/state bindings are unchanged and unvalidated behind the full generation gate.'
write(OUT/'authoring-review.json',dict(status='PASS',reason=reason,scope='Generation authoring only',independent_review=ref(HERE/'independent-structural-review.json'),
    reviewer=dict(agent='/root/watervine_structure_review',fork_turns='none',reasoning_effort_requested='low',model='Inherited main model; no override'),
    dispositions=[dict(finding='Review calls stage02 an earlier render',decision='Clarified evidence role',reason='Stage02 is the current saved-model 3D diagnostic from a deliberately oblique camera, not an earlier production frame. Fixed map masters govern source registration; no extra facing or independent recentering is used.')],
    new_imagegen_call=False,native_acceptance='Pending full generation gate'))
write(HERE/'source-packet.json',dict(source=ref(OLD/'source-packet.json'),description=source['description'],original_context=source['original_context'],donor_reference=source['donor_reference'],
    fit_contract=dict(facing='Source fixed map view; three distinct cosmetic layouts, no invented directional turns.',contact='Every basal tendril begins within its own stem radius; tether anchors follow evaluated actual curved stems.',
        wafer_positions='Exact source-packet authored centers/radii and counts retained; invisible low-relief depth authored.',palette='Stem w; swollen wafers g ripe or K unripe. Both states share exact model and masks.'),
    selected_model=ref(HERE/'vines.blend'),direct_source_selection='Simple Blender tones/contours retain shape; no additional ImageGen treatment needed.',native_acceptance='Pending full generation gate'))
registry_path=ROOT/'evidence/blender-shape-ledger.json';registry=read(registry_path);snapshot_old=ROOT/f'evidence/blender-shape-ledger-history/v{registry["revision"]}.json';assert snapshot_old.read_bytes()==registry_path.read_bytes()
registry['assets'].append(dict(entry='SCN-WATERVINE',native_item='Watervine / three RandomTile layouts / shared ripe-unripe geometry',versions=[
    dict(version='blender-v2',blend=ref(HERE.parent/'blender-v2/vines.blend'),construction_script=ref(HERE.parent/'blender-v2/build-vines.py'),controls=ref(HERE.parent/'blender-v2/model-controls.json'),status='Basal correction retained; tether anchor correction required'),
    dict(version='blender-v3',blend=ref(HERE/'vines.blend'),construction_script=ref(HERE/'refine-tethers.py'),controls=ref(HERE/'model-controls.json'),receipt=ref(HERE/'blender-receipt.json'),status='GENERATION SELECTED / native pending')],
    approved_generation_version='blender-v3',approved_production_version=None,recommended_resume=ref(HERE/'vines.blend')['path'],registered_model=ref(OUT/'model.json'),authoring_review=ref(OUT/'authoring-review.json'),reopen_verification=ref(HERE/'reopen-audit.json')))
registry['revision']+=1;registry['updated_at']=now;registry['prior_snapshots'].append(ref(snapshot_old));write(registry_path,registry);snapshot=ROOT/f'evidence/blender-shape-ledger-history/v{registry["revision"]}.json';snapshot.write_bytes(registry_path.read_bytes())
entry['persistent_3d_sources']=dict(latest_registry_path='evidence/blender-shape-ledger.json',registry_snapshot=ref(snapshot),resume=ref(HERE/'vines.blend'),controls=ref(HERE/'model-controls.json'))
for folder in [HERE.parent/'blender-v2',HERE]:write(folder/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(folder.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
sys.path.insert(0,str(ROOT/'tools'));from enumerate_conversion_ledger import blender_required_steps,enumerate_entries,validate
entry['workflow_version']='blender-first-v1';entry['required_steps']=blender_required_steps(next(e for e in enumerate_entries() if e['id']==entry['id']))
events=[
 ('resolve_object_description_original_tile_palette_state','Retain installed Watervine description, three native layouts, actual wafer roles and harvest colors.',[ref(OLD/'source-packet.json')],[ref(HERE/'source-packet.json')]),
 ('select_render_reference_or_document_no_equivalent','Reuse the actual Core HaygrassA narrow-stroke reference, without copying cereal heads or crop behavior.',[ref(OLD/'source-construction-comparison.png')],[ref(HERE/'source-packet.json')]),
 ('construct_faithful_shape','Build editable complete curved stems, attached basal tendrils, tethers and low-relief wafers from source layout controls.',[],[ref(HERE.parent/'blender-v2/build-vines.py'),ref(HERE/'stage-02-model-variant-1.png'),ref(HERE/'stage-02-model-variant-2.png'),ref(HERE/'stage-02-model-variant-3.png')]),
 ('create_required_state_neighbor_variants','Retain three distinct source layouts with identical geometry for both native harvest color states.',[ref(HERE/'model-controls.json')],[ref(OUT/'registration-comparison.png')]),
 ('refine_materials_and_form','Use restrained Blender normal-based tones, salt-furrow highlights and contour; correct tethers on the reused saved geometry.',[ref(HERE.parent/'blender-v2/rejection.json')],[ref(HERE/'refine-tethers.py'),ref(HERE/'blender-receipt.json')]),
 ('render_blender_views_and_masks','Render complete fixed map views and separate wafer ownership; retain reopenable model.',[ref(HERE/'vines.blend')],[ref(HERE/'reopen-audit.json'),ref(snapshot)]),
 ('extract_register_color_coverage','Apply common full-cell mapping and independent stem/wafer masks; keep native state/anchor bindings.',[ref(HERE/'register-vines.py')],[ref(OUT/'model.json'),ref(OUT/'registration-decisions.json')]),
 ('visual_review_identity_and_connections_at_game_scale','Review actual bases, tethers, wafer identity and all three tint/size rows; disposition independent findings.',[ref(HERE/'independent-structural-review.json')],[ref(OUT/'basal-before-after.png'),ref(OUT/'registration-comparison.png'),ref(OUT/'authoring-review.json')])]
for step,action,inputs,outputs in events:entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=inputs,outputs=outputs,review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_state_review',known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'registration-comparison.png')),
    art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')),registration_summary='Direct Blender source layouts: continuous basal tendrils, actual curved-stem wafer attachments and unchanged native harvest frame/palette/state bindings. Native acceptance pending.')
entry.pop('advancement_blocker',None);ledger['current_structural_correction_queue']['ordered_entries']=[x for x in ledger['current_structural_correction_queue']['ordered_entries'] if x!=entry['id']]
ledger.setdefault('resolved_structural_corrections',[]).append(dict(entry=entry['id'],recorded_at=now,reason=reason,registration=entry['current_registration']))
n=next(e for e in ledger['entries'] if e['id']=='SCN-WOODEN-WATER-WHEEL');assert not n['generation_ready'];n.update(status='IN PROGRESS',current_step=n['required_steps'][0]);ledger.update(active_entry=n['id'],updated_at=now)
validate(ledger,enumerate_entries());write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Three Watervine layouts generation-ready; water wheel sole active entry. Native acceptance pending.')
