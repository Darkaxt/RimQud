"""Close the supported source-wheel interpretation and resume uncreated entries."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OLD=HERE.parent/'v1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-WOODEN-WATER-WHEEL';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);now=datetime.now(timezone.utc).isoformat()
review=read(HERE/'independent-structural-review.json');assert not review['fix_now']
for r in review['inspected_images']:assert ref(ROOT/r['path'])['sha256']==r['sha256']
model=read(OUT/'model.json');prior=read(OLD/'registered-final/model.json');source=read(OLD/'corrected-source-packet.json')
for key in ['registration','camera','palette','native_state_owner','native_behavior','view_policy','formula','native_activation']:assert model[key]==prior[key]
assert read(HERE/'reopen-audit.json')['reopened'] and not model['native_activation']
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];fg=np.array(list(bytes.fromhex(palette['w'])));dc=np.array(list(bytes.fromhex(palette['y'])))
checks={}
for row,old in zip(model['frames'],prior['frames']):
    assert row['frame']==old['frame'] and row['native_tile']==old['native_tile']
    for key in ['primary','detail','coverage','detail_weight','detail_coverage','authored_dualcolor_mask']:assert ref(ROOT/row[key]['path'])==row[key]
    a=np.array(Image.open(ROOT/row['primary']['path']).convert('RGBA'));d=np.array(Image.open(ROOT/row['detail']['path']).convert('RGBA'));weight=np.array(Image.open(ROOT/row['detail_weight']['path'])).astype(float)/255
    assert a.shape==(256,256,4) and not np.ptp(a[:,:,:3].astype(int),axis=2).any() and not np.ptp(d[:,:,:3].astype(int),axis=2).any()
    assert np.all(d[:,:,3]<=a[:,:,3])
    expected=a.copy();expected[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float)*((1-weight[:,:,None])*fg+weight[:,:,None]*dc)/255));expected[expected[:,:,3]==0,:3]=0
    assert np.array_equal(expected,np.array(Image.open(OUT/f'frame-{row["frame"]}-native-w-y.png')))
    checks[row['frame']]=dict(neutral_equal_rgb=True,detail_subset=True,one_coverage_native_recomposition_exact=True,frame_and_native_tile_unchanged=True)
reason='Inspected all three Blender source-map phases, native w/y compositions, intended-size rows and oblique construction diagnostic. Two minimal rear wet-wood supports join the inset carrier to the existing spine/rim; every source-bound detail run meets that carrier. This resolves visible ownership without claiming a native axle, motor or uniquely recovered mounting topology. Source shape/paddle phase identity and native detail positions remain bound to the earlier source guide; low-relief depth/supports are explicitly authored. Fresh independent review found no consequential structural FIX NOW issue. Thin support readability is minor polish for full-set play-distance assessment. Exact frame, palette/one-coverage formula and native HydroTurbine/animation behavior fields are retained; native acceptance remains gated.'
write(OUT/'authoring-review.json',dict(status='PASS',reason=reason,scope='Generation authoring only',checks=checks,independent_review=ref(HERE/'independent-structural-review.json'),
    reviewer=dict(agent='/root/blender_waterwheel_review',fork_turns='none',reasoning_effort_requested='low',model='Inherited main model; no override'),
    dispositions=[dict(finding='Thin support readability at smallest preview',decision='MINOR POLISH',reason='Actual masters and model show coherent attachment; assess prominence in the full-set native play-distance test rather than inventing larger machinery.')],
    native_acceptance='Pending full generation gate'))
write(HERE/'source-packet.json',dict(source=ref(OLD/'corrected-source-packet.json'),description=source['description'],original_frames=source['native_frames'],palette=source['palette'],
    source_facts=['Tall rounded rim, near-left paddle bands and phase-dependent right detail marks.','Native HydroTurbine/MechanicalPowerTransmission/Circuitry fields do not uniquely identify inset attachment geometry.'],
    authored_interpretation=model['authored_support_interpretation'],fit_contract=dict(view='One fixed cardinal source map face; three existing native phases.',contact='Rear supports overlap spine, rim and carrier; source detail runs connect to carrier.',
        occlusion='Rear wood below light inset runs; no filled background endplate.',scale='Common 16x24 source cell, 512x768 manual frame, 256-square recipient and anchor8,16.'),
    original_ambiguity=ref(HERE.parent/'inspection-v2/independent-inspection.json'),selected_model=ref(HERE/'wheel.blend'),selection='Direct Blender surfaces and contours; no further 2D patch loop or ImageGen refinement.',native_acceptance='Pending full generation gate'))
registry_path=ROOT/'evidence/blender-shape-ledger.json';registry=read(registry_path);old_snapshot=ROOT/f'evidence/blender-shape-ledger-history/v{registry["revision"]}.json';assert old_snapshot.read_bytes()==registry_path.read_bytes()
asset=dict(entry=entry['id'],native_item='Wooden Water Wheel / three native source phases',versions=[dict(version='blender-v2',blend=ref(HERE/'wheel.blend'),construction_script=ref(HERE/'build-wheel.py'),controls=ref(HERE/'model-controls.json'),receipt=ref(HERE/'blender-receipt.json'),status='GENERATION SELECTED / native pending')],
    approved_generation_version='blender-v2',approved_production_version=None,recommended_resume=ref(HERE/'wheel.blend')['path'],registered_model=ref(OUT/'model.json'),authoring_review=ref(OUT/'authoring-review.json'),reopen_verification=ref(HERE/'reopen-audit.json'))
existing=next((a for a in registry['assets'] if a['entry']==entry['id']),None)
if existing:
    # Resume the exact observed partial closure after uncreated ledger rows
    # proved to omit the optional generation_ready field. Do not duplicate the
    # already saved immutable registry version or regenerate any artwork.
    assert existing==asset
    snapshot=old_snapshot
else:
    registry['assets'].append(asset);registry['revision']+=1;registry['updated_at']=now;registry['prior_snapshots'].append(ref(old_snapshot));write(registry_path,registry);snapshot=ROOT/f'evidence/blender-shape-ledger-history/v{registry["revision"]}.json';snapshot.write_bytes(registry_path.read_bytes())
entry['persistent_3d_sources']=dict(latest_registry_path='evidence/blender-shape-ledger.json',registry_snapshot=ref(snapshot),resume=ref(HERE/'wheel.blend'),controls=ref(HERE/'model-controls.json'))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
sys.path.insert(0,str(ROOT/'tools'));from enumerate_conversion_ledger import blender_required_steps,enumerate_entries,validate
entry['workflow_version']='blender-first-v1';entry['required_steps']=blender_required_steps(next(e for e in enumerate_entries() if e['id']==entry['id']))
events=[
 ('resolve_object_description_original_tile_palette_state','Retain installed source shape/description, native three phase tiles and w/y roles.',[ref(OLD/'corrected-source-packet.json')],[ref(HERE/'source-packet.json')]),
 ('select_render_reference_or_document_no_equivalent','Reuse the actual VTE watermill blade material/reference evidence without copying a whole donor mill.',[ref(OLD/'source-reference-construction.png')],[ref(HERE/'source-packet.json')]),
 ('construct_faithful_shape','Resolve inset relationship with explicitly authored supported carrier in a complete editable low-relief Blender model.',[ref(HERE.parent/'inspection-v2/independent-inspection.json')],[ref(HERE/'build-wheel.py'),ref(HERE/'stage-02-model-phase-1.png')]),
 ('create_required_state_neighbor_variants','Preserve the three source-bound paddle/detail patterns, common frame and original native clock ownership.',[ref(HERE/'model-controls.json')],[ref(HERE/'stage-02-model-phase-2.png'),ref(HERE/'stage-02-model-phase-3.png')]),
 ('refine_materials_and_form','Select direct simple neutral Blender wood/detail material and contours; no additional AI or 2D isolation.',[ref(HERE/'model-controls.json')],[ref(HERE/'frame-1-neutral-master.png'),ref(HERE/'frame-2-neutral-master.png'),ref(HERE/'frame-3-neutral-master.png')]),
 ('render_blender_views_and_masks','Render complete phase objects and independent visible detail masks; verify editable model reopens.',[ref(HERE/'wheel.blend')],[ref(HERE/'blender-receipt.json'),ref(HERE/'reopen-audit.json'),ref(snapshot)]),
 ('extract_register_color_coverage','Register source-fixed phases with exact one-coverage native w/y formula and detail ownership.',[ref(HERE/'register-wheel.py')],[ref(OUT/'model.json'),ref(OUT/'registration-decisions.json')]),
 ('visual_review_identity_and_connections_at_game_scale','Inspect all phase/tint/size views and disposition fresh independent structural findings.',[ref(HERE/'independent-structural-review.json')],[ref(OUT/'registration-comparison.png'),ref(OUT/'authoring-review.json')])]
for step,action,inputs,outputs in events:entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=inputs,outputs=outputs,review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_state_review',known_issues=['Thin support readability is minor polish; native behavior remains unvalidated.'],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'registration-comparison.png')),
    art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')),registration_summary='Direct Blender low-relief source wheel with authored rear supports and connected inset carrier in all three native phases. Original palette/frame/state behavior fields retained; native acceptance pending.')
entry.pop('advancement_blocker',None);ledger['current_structural_correction_queue']['ordered_entries']=[x for x in ledger['current_structural_correction_queue']['ordered_entries'] if x!=entry['id']]
ledger.setdefault('resolved_structural_corrections',[]).append(dict(entry=entry['id'],recorded_at=now,reason=reason,registration=entry['current_registration']))
n=next(e for e in ledger['entries'] if e['id']=='SCN-RANDOM-BOTTLE');assert not n.get('generation_ready');n.update(status='IN PROGRESS',current_step=n['required_steps'][0]);ledger.update(active_entry=n['id'],updated_at=now)
validate(ledger,enumerate_entries());write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Water-wheel generation authoring closed; Random Bottle sole active entry. Native acceptance pending.')
