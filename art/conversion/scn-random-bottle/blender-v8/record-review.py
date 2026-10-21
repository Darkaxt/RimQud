"""Record actual retained bottle iterations, selected glass/liquid layers and cache."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';BASE=HERE.parent
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-RANDOM-BOTTLE';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);now=datetime.now(timezone.utc).isoformat()
review=read(HERE/'independent-structural-review.json');assert not review['fix_now'] and not review['consequential_defects'] and review['recommendation'].lower().startswith('accept')
for r in review['inputs']:
 p=ROOT/r['path'] if (ROOT/r['path']).exists() else BASE/r['path']
 assert hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],r
audit=read(HERE/'reopen-audit.json');assert audit['evaluated_surface']['connected_components']==1 and audit['evaluated_surface']['nonmanifold_edges']==0 and audit['evaluated_surface']['zero_area_faces']==0 and audit['liquid']['passed']
model=read(OUT/'model.json');assert not model['native_activation'];row=model['frames'][0]
for k in ['primary','detail','coverage','detail_weight','detail_coverage','authored_dualcolor_mask']:assert ref(ROOT/row[k]['path'])==row[k]
pa=np.array(Image.open(ROOT/row['primary']['path']).convert('RGBA'));da=np.array(Image.open(ROOT/row['detail']['path']).convert('RGBA'));weight=np.array(Image.open(ROOT/row['detail_weight']['path'])).astype(float)/255
assert pa.shape==(256,256,4) and not np.ptp(pa[:,:,:3].astype(int),axis=2).any() and np.all(da[:,:,3]<=pa[:,:,3])
assert np.array_equal(pa[:,:,3],np.array(Image.open(ROOT/row['coverage']['path'])))
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];cyan=np.array(list(bytes.fromhex(palette['c'])));expected=pa.copy();expected[:,:,:3]=np.uint8(np.round(pa[:,:,:3].astype(float)*cyan/255));expected[expected[:,:,3]==0,:3]=0
assert np.array_equal(expected,np.array(Image.open(OUT/'native-c-c.png')))
reason='Selected direct Blender translucent hollow glass with separate contained liquid, matching the user interpretation and actual freeblown-glass/Transparent/LiquidVisibleWhenSealed/DetailColorByLiquid source contracts. Original long neck, flared mouth, rounded bowl and right loop remain source-bound. Handle roots are rounded on the actual terminal mesh and joined to the wall. Retained v5/v6 sphere-union attempts were rejected for geometry defects; v7 retained a small sampled liquid/base overlap and was corrected by a6percent radial reduction of liquid only. Reopened v8 has one manifold glass/handle component, a separate closed liquid and positive sampled cavity/floor clearance. Fresh independent rendered-image review found no fix-now structural issue. High-resolution root highlights/grain are minor polish. Native liquid/color/seal/volume and full-set play-distance acceptance remain gated.'
write(OUT/'authoring-review.json',dict(status='PASS',reason=reason,independent_review=ref(HERE/'independent-structural-review.json'),reopen_audit=ref(HERE/'reopen-audit.json'),reviewer=dict(agent='/root/bottle_selected_render_review',fork_turns='none',reasoning_effort_requested='low',model='Inherited main model; no override'),checks=dict(neutral_equal_rgb=True,detail_coverage_subset=True,single_coverage_native_c_c_exact=True,fixed_full_cell_registration=True,source_state_family_unchanged=True),dispositions=[dict(finding='Root glint, bright neutral glass and subtle frontal mouth opening',decision='MINOR POLISH',reason='Main inspection shows actual transparent centers in the selected source-cyan face and a hollow rim in the angled diagnostic. Fixed cardinal camera makes the opening shallow. Fresh review agrees the source identity remains coherent; full-set native play-distance assessment remains required.')],native_acceptance='Pending full generation gate'))
write(HERE/'iteration-decisions.json',dict(selected='blender-v8',new_imagegen_call=False,versions={
 'blender-v1':'Initial complete editable hollow vessel; angular bowl/opaque geometry draft superseded.',
 'blender-v2':'Rounded glass geometry; independent review found abrupt/flat handle roots.',
 'blender-v3':'Actual manifold handle union; opaque geometry draft superseded by user transparency direction.',
 'blender-v4':'Translucent shell, separate liquid, roots seated in actual wall; visual root termination unresolved.',
 'blender-v5':'Rejected: equal-radius sphere cap unions introduced64 nonmanifold edges and7 zero-area faces.',
 'blender-v6':'Rejected: changed sphere overlap still produced degenerate Boolean warnings; no approval.',
 'blender-v7':'Rounded terminal mesh fixed handle geometry and passed visual review; sampled liquid/base overlap -.0443 blocks selection.',
 'blender-v8':'Selected: unchanged sound glass/handle and6percent radial liquid reduction, positive sampled clearance and final independent visual pass.'},native_activation=False))
registry_path=ROOT/'evidence/blender-shape-ledger.json';registry=read(registry_path);previous=ROOT/f'evidence/blender-shape-ledger-history/v{registry["revision"]}.json';assert previous.read_bytes()==registry_path.read_bytes();assert not any(a['entry']==entry['id'] for a in registry['assets'])
scripts=['build-bottle.py','refine-saved-bottle.py','fuse-saved-handle.py','glass-and-liquid.py','round-glass-roots.py','refine-root-overlap.py','round-terminal-mesh.py','refine-liquid-clearance.py'];versions=[]
decisions=read(HERE/'iteration-decisions.json')['versions']
for i,script in enumerate(scripts,1):
 p=BASE/f'blender-v{i}';versions.append(dict(version=p.name,blend=ref(p/'bottle.blend'),construction_script=ref(p/script),controls=ref(p/'model-controls.json'),receipt=ref(p/'blender-receipt.json'),status=decisions[p.name]))
registry['assets'].append(dict(entry=entry['id'],native_item='Random Bottle / native glass and random contents',versions=versions,approved_generation_version='blender-v8',approved_production_version=None,recommended_resume=ref(HERE/'bottle.blend')['path'],registered_model=ref(OUT/'model.json'),authoring_review=ref(OUT/'authoring-review.json'),reopen_verification=ref(HERE/'reopen-audit.json')))
registry['revision']+=1;registry['updated_at']=now;registry['prior_snapshots'].append(ref(previous));write(registry_path,registry);snapshot=ROOT/f'evidence/blender-shape-ledger-history/v{registry["revision"]}.json';snapshot.write_bytes(registry_path.read_bytes())
entry['persistent_3d_sources']=dict(latest_registry_path='evidence/blender-shape-ledger.json',registry_snapshot=ref(snapshot),resume=ref(HERE/'bottle.blend'),controls=ref(HERE/'model-controls.json'))
sys.path.insert(0,str(ROOT/'tools'));from enumerate_conversion_ledger import blender_required_steps,enumerate_entries,validate
entry['workflow_version']='blender-first-v1';entry['required_steps']=blender_required_steps(next(e for e in enumerate_entries() if e['id']==entry['id']))
events=[
 ('construct_faithful_shape','Construct an actual hollow freeblown vessel, neck, rolled mouth and complete loop handle in Blender.',[ref(BASE/'blender-v1/source-packet.json')],[ref(BASE/'blender-v1/stage-02-model-3d.png'),ref(BASE/'blender-v1/build-bottle.py')],'RECORDED'),
 ('refine_materials_and_form','Round bowl and join actual handle; retain independent root critique and actual corrections.',[ref(BASE/'blender-v2/independent-structural-review.json')],[ref(BASE/'blender-v3/reopen-audit.json'),ref(BASE/'blender-v4/glass-liquid-authoring-comparison.png')],'RECORDED'),
 ('refine_materials_and_form','Retain rejected rounded-root Boolean trials and failed liquid-clearance version; no discarded failure or fabricated AI refinement.',[ref(BASE/'blender-v5/reopen-audit.json'),ref(BASE/'blender-v7/reopen-audit.json')],[ref(HERE/'iteration-decisions.json'),ref(BASE/'blender-v7/independent-structural-review.json')],'REJECTED'),
 ('construct_faithful_shape','Select complete retained glass with rounded actual terminal mesh; separate native-detail liquid fits its actual cavity.',[ref(HERE/'source-packet.json')],[ref(HERE/'stage-02-model-3d.png'),ref(HERE/'model-controls.json')],'PASS'),
 ('create_required_state_neighbor_variants','Keep the single native map tile. Empty shell is authoring evidence; no new seal/fill/rotated state family.',[ref(HERE/'source-packet.json')],[ref(HERE/'raw-empty-glass.png'),ref(OUT/'model.json')],'PASS'),
 ('refine_materials_and_form','Use direct translucent Blender materials and separate visible contents; no ImageGen or second isolation call.',[ref(HERE/'iteration-decisions.json')],[ref(HERE/'raw-filled-neutral.png'),ref(HERE/'raw-liquid-contribution.png')],'PASS'),
 ('render_blender_views_and_masks','Render fixed original map face, empty-glass layer and conditional liquid contribution; retain editable model and immutable registry.',[ref(HERE/'bottle.blend')],[ref(HERE/'blender-receipt.json'),ref(HERE/'reopen-audit.json'),ref(snapshot)],'PASS'),
 ('extract_register_color_coverage','Preserve one translucent coverage and conditional glass/liquid tint under the full-cell frame/anchor.',[ref(HERE/'register-glass.py')],[ref(OUT/'model.json'),ref(OUT/'registration-decisions.json')],'PASS'),
 ('visual_review_identity_and_connections_at_game_scale','Inspect source identity, actual handle/glass volume, liquid visibility and intended-size native/color-role comparison.',[ref(HERE/'independent-structural-review.json')],[ref(OUT/'registration-comparison.png'),ref(OUT/'authoring-review.json')],'PASS')]
for step,action,inputs,outputs,result in events:entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=inputs,outputs=outputs,review=reason,result=result))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_state_review',known_issues=['High-resolution glass grain/root highlight is minor polish; native liquid/seal/volume behavior and play-distance acceptance pending.'],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'registration-comparison.png')),art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')),registration_summary='Transparent freeblown glass shell and contained independent liquid; direct retained Blender geometry, single coverage and native conditional detail tint.')
entry.pop('advancement_blocker',None);n=next(e for e in ledger['entries'] if e['id']=='SCN-VASE');assert not n.get('generation_ready');n.update(status='IN PROGRESS',current_step=n['required_steps'][0]);ledger.update(active_entry=n['id'],updated_at=now)
validate(ledger,enumerate_entries());write(ROOT/'evidence/conversion-ledger.json',ledger)
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(BASE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
print('Random Bottle generation authoring selected; Vase sole active entry. Native acceptance pending.')
