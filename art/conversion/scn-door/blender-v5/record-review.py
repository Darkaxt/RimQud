"""Close the source-bound Blender door correction and retain every editable attempt."""
from pathlib import Path
from datetime import datetime,timezone
import sys,json,hashlib,copy
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OLD=HERE.parent/'v1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'authoring-review.json').exists()
lp=ROOT/'evidence/conversion-ledger.json';ledger=read(lp);assert ledger['active_entry']=='SCN-DOOR'
entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);now=datetime.now(timezone.utc).isoformat()
source=read(OLD/'source-packet.json')
for r in [source['native_definition'],source['donor_reference']]:
    assert hashlib.sha256(Path(r['path']).read_bytes()).hexdigest()==r['sha256']
review=read(HERE/'independent-structural-review.json')
for r in review['images']:assert ref(ROOT/r['path'])['sha256']==r['sha256']
assert all(f['severity'] in ['none','minor'] for f in review['findings'])
model=read(OUT/'model.json');prior=read(OLD/'registered/model.json')
for k in ['native_frame','manual_frame','recipient_frame','anchor','state_owner','mapping_rule','original_states']:assert model[k]==prior[k]
for state,v in model['states'].items():
    assert v['native_tiles']==prior['states'][state]['native_tiles'] and v['solid_occluding']==prior['states'][state]['solid_occluding']
    for row in v['layers']:
        assert ref(ROOT/row['texture']['path'])==row['texture'];a=np.array(Image.open(ROOT/row['texture']['path']).convert('RGBA'));assert not np.ptp(a[:,:,:3].astype(int),axis=2).any()
        assert ref(ROOT/row['coverage']['path'])==row['coverage'];assert np.array_equal(a[:,:,3],np.array(Image.open(ROOT/row['coverage']['path'])))
assert (OUT/'closed-frame-neutral.png').read_bytes()==(OUT/'open-frame-neutral.png').read_bytes()
assert read(HERE/'reopen-audit.json')['reopened'] and read(HERE/'blender-receipt.json')['geometry_unchanged']
reason='Inspected both direct source-bound states, 3D model, registered neutral/native colors, intended-size rows and hinge closeups. Fixed straps overlap actual jamb and barrel; rotating straps overlap the same complete slate leaf. Open/closed share one physical axis and common frame, without an independently placed floating strip. Old painted hinge fragments were removed from the retained slate material before mapping; hand wear, seams and right recessed handle remain. Independent reviewer found no consequential structural defect. Plain dark hardware and flat open thickness are minor material polish; retained for full-set play-distance assessment. Native collision/visibility/state mechanics remain pending.'
write(OUT/'authoring-review.json',dict(status='PASS',reason=reason,scope='Static generation authoring only',independent_review=ref(HERE/'independent-structural-review.json'),
    reviewer=dict(agent='/root/door_hinge_review',fork_turns='none',reasoning_effort_requested='low',model='Inherited main model; no override'),
    dispositions=[dict(finding='Plain dark hardware and flat open thickness',decision='MINOR POLISH',reason='Connected silhouette and source identity are readable; optional surface polish can follow full-set play-distance testing.')],
    native_acceptance='Pending full generation gate'))
write(HERE/'source-packet.json',dict(source=ref(OLD/'source-packet.json'),description=source['description'],original_states=source['source_states'],
    original_context=source['original_context'],donor_reference=source['donor_reference'],palette=source['palette'],
    fit_contract=dict(closed='Broad source slate within the fixed arch; left fixed jamb straps bridge to pivot barrels and moving slate straps; recessed handle on right.',
        open='Same leaf rotates 90 degrees about left hinge. Source edge remains left, straps connect barrel to fixed jamb. Broad face detail becomes occluded by real geometry.',
        frame='Common 16x24 source frame and anchor8,16; no fitting to individual state bounds.',depth='Frame, slab thickness and hardware dimensions are authored estimates.'),
    construction=ref(HERE.parent/'blender-v4/build-door.py'),selected_editable_model=ref(HERE/'door.blend'),
    no_new_imagegen_call=True,selection='Retain direct Blender geometry and existing source surface with deterministic continuation/contours. No additional style generation was necessary.',native_acceptance='Pending full generation gate'))
# The mutable convenience index has immutable snapshots for evidence hashes.
registry_path=ROOT/'evidence/blender-shape-ledger.json';registry=read(registry_path);old_hash=ref(registry_path)['sha256']
old_snapshot=ROOT/f'evidence/blender-shape-ledger-history/v{registry["revision"]}.json'
assert old_snapshot.read_bytes()==registry_path.read_bytes()
def snapshot_refs(value):
    if isinstance(value,dict):
        if value.get('path')=='evidence/blender-shape-ledger.json' and value.get('sha256')==old_hash:
            value.update(path=old_snapshot.relative_to(ROOT).as_posix(),original_path='evidence/blender-shape-ledger.json',snapshot_note='Exact prior registry bytes retained before advancing the mutable index.')
        for v in value.values():snapshot_refs(v)
    elif isinstance(value,list):
        for v in value:snapshot_refs(v)
snapshot_refs(ledger)
versions=[]
for n in [2,3,4,5]:
    folder=HERE.parent/f'blender-v{n}'
    versions.append(dict(version=folder.name,blend=ref(folder/'door.blend'),controls=ref(folder/'model-controls.json'),receipt=ref(folder/'blender-receipt.json'),
        construction_script=ref(folder/('refine-saved-material.py' if n==5 else 'build-door.py')),
        status='GENERATION SELECTED / native pending' if n==5 else read(folder/'rejection.json')['status'],actual_states=['closed','open']))
registry['assets'].append(dict(entry='SCN-DOOR',native_item='Door / actual closed and open runtime tiles',versions=versions,approved_generation_version='blender-v5',approved_production_version=None,
    recommended_resume=ref(HERE/'door.blend')['path'],next_edit='Resume saved geometry and edit neutral material or hardware locally; do not restart model.',
    registered_model=ref(OUT/'model.json'),authoring_review=ref(OUT/'authoring-review.json'),reopen_verification=ref(HERE/'reopen-audit.json')))
registry['revision']+=1;registry['updated_at']=now;registry['prior_snapshots'].append(ref(old_snapshot));write(registry_path,registry)
snapshot=ROOT/f'evidence/blender-shape-ledger-history/v{registry["revision"]}.json';snapshot.write_bytes(registry_path.read_bytes())
entry['persistent_3d_sources']=dict(latest_registry_path='evidence/blender-shape-ledger.json',registry_snapshot=ref(snapshot),resume=ref(HERE/'door.blend'),controls=ref(HERE/'model-controls.json'))
for folder in [HERE.parent/f'blender-v{n}' for n in [2,3,4,5]]:
    write(folder/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(folder.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
sys.path.insert(0,str(ROOT/'tools'));from enumerate_conversion_ledger import blender_required_steps,enumerate_entries,validate
entry['workflow_version']='blender-first-v1';entry['required_steps']=blender_required_steps(next(e for e in enumerate_entries() if e['id']==entry['id']))
events=[
 ('resolve_object_description_original_tile_palette_state','Retain exact installed Door description, actual runtime open/closed tiles and native y/y roles.',[ref(OLD/'source-packet.json')],[ref(HERE/'source-packet.json')]),
 ('select_render_reference_or_document_no_equivalent','Reuse the actual Core DoorSimple_Mover reference for restrained panel shading only; no donor sliding mechanics.',[ref(OLD/'source-construction-comparison.png')],[ref(HERE/'source-packet.json')]),
 ('construct_faithful_shape','Model fixed source arch, complete slate slab and connected jamb/barrel/moving straps in Blender.',[],[ref(HERE.parent/'blender-v2/stage-02-model-3d.png'),ref(HERE.parent/'blender-v2/rejection.json'),ref(HERE.parent/'blender-v3/rejection.json'),ref(HERE.parent/'blender-v4/rejection.json'),ref(HERE/'stage-02-model-3d.png')]),
 ('create_required_state_neighbor_variants','Derive closed and 90-degree open from the same physical pivot/leaf; retain source-fixed map views only.',[ref(HERE/'model-controls.json')],[ref(HERE/'raw-closed-full.png'),ref(HERE/'raw-open-full.png')]),
 ('refine_materials_and_form','Retain usable source slate wear, remove baked fake hinges, solve neutral material continuation and finish inner contours. No new AI call.',[ref(HERE/'surface-preparation.json')],[ref(HERE/'slate-surface-without-old-hardware.png'),ref(OUT/'hinge-before-after.png')]),
 ('render_blender_views_and_masks','Export whole leaf/hardware and fixed frame separately from actual saved Blender state views.',[ref(HERE/'door.blend')],[ref(HERE/'blender-receipt.json'),ref(HERE/'reopen-audit.json'),ref(snapshot)]),
 ('extract_register_color_coverage','Register common full-canvas frame and source palette ownership without state recentering.',[ref(HERE/'register-door.py')],[ref(OUT/'model.json'),ref(OUT/'registration-decisions.json')]),
 ('visual_review_identity_and_connections_at_game_scale','Inspect all state/color/size evidence and disposition fresh independent structural findings.',[ref(HERE/'independent-structural-review.json')],[ref(OUT/'states-comparison.png'),ref(OUT/'authoring-review.json')])]
for step,action,inputs,outputs in events:entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=inputs,outputs=outputs,review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_state_review',known_issues=['Minor hardware/open-face material polish; native state/visibility remains pending.'],
    current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'states-comparison.png')),art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')),
    registration_summary='Direct Blender source door with complete slate leaf, connected shared hinges and fixed arch in both native states. Palette/frame/state bindings retained; native acceptance pending.')
entry.pop('advancement_blocker',None)
q=ledger['current_structural_correction_queue'];q['ordered_entries']=[x for x in q['ordered_entries'] if x!=entry['id']]
ledger.setdefault('resolved_structural_corrections',[]).append(dict(entry=entry['id'],recorded_at=now,reason=reason,registration=entry['current_registration']))
n=next(e for e in ledger['entries'] if e['id']=='SCN-DOGTHORN-TREE');assert not n['generation_ready'];n.update(status='IN PROGRESS',current_step=n['required_steps'][0]);ledger.update(active_entry=n['id'],updated_at=now)
validate(ledger,enumerate_entries());write(lp,ledger)
print('Door generation authoring closed; Dogthorn is sole active entry. Native acceptance pending.')
