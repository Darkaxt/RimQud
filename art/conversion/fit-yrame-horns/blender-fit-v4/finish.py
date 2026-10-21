"""Close the complete horn authoring fit, preserving native acceptance as pending."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,copy
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;OUT=HERE/'registered-v1';ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
sys.path.insert(0,str(ROOT/'tools'));from enumerate_conversion_ledger import enumerate_entries,validate,blender_required_steps
ledger=read(ROOT/'evidence/conversion-ledger.json');expected=enumerate_entries();validate(ledger,expected)
legacy=copy.deepcopy(ledger);le=next(e for e in legacy['entries'] if e['id']=='FIT-YRAME-HORNS-HEAD-0');le.pop('workflow_version');le['required_steps']=next(e for e in expected if e['id']==le['id'])['required_steps'];validate(legacy,expected)
try:blender_required_steps(next(e for e in expected if e['category']=='Race/body templates'))
except AssertionError:pass
else:raise AssertionError('Body workflow was incorrectly rerouted')
write(OUT/'ledger-workflow-diagnostics.json',dict(legacy_inventory_unchanged=True,explicit_blender_fitting_contract_valid=True,body_route_preserved=True,entries=len(expected),required_variants_unchanged=True))
entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert entry['id']=='FIT-YRAME-HORNS-HEAD-0';model=read(OUT/'model.json');decision=read(OUT/'registration-decisions.json');body=read(ROOT/model['base_model'])
for face,rows in model['views'].items():
    for r in rows:
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256'];a=np.array(Image.open(ROOT/r['public_file']).convert('RGBA'));assert not np.ptp(a[:,:,:3].astype(int),axis=2).any();assert not a[a[:,:,3]==0,:3].any()
    base=Image.new('RGBA',(768,1152))
    for original in sorted(body['views'][face],key=lambda r:r['layer']):
        assert ref(ROOT/original['public_file'])['sha256']==original['sha256']
        base.alpha_composite(Image.open(ROOT/original['public_file']).convert('RGBA'))
    expected_body=np.array(base);expected_body[expected_body[:,:,3]==0,:3]=0
    assert np.array_equal(expected_body,np.array(Image.open(OUT/f'original-body-{face}.png')))
    assert all(r['size']==[768,1152] and r['contact']==[384,1050] for r in rows)
    assert decision['checks'][face]['neutral_recomposition_exact'] and decision['checks'][face]['raw_alpha_unchanged']
review=read(HERE/'independent-fit-review.json')
for r in review['inspected_images']:assert ref(ROOT/r['path'])['sha256']==r['sha256']
now=datetime.now(timezone.utc).isoformat()
reason='Inspected all four registered neutral/native and intended-size views, full-source and near/far/detail plates. Source-silhouette-calibrated head proxy explains forehead-adjacent roots and distinct rear occlusion; full volume and original human head/ears/body remain intact. Fresh independent review found no demonstrated structural FIX NOW failure. Actual buried root-end faces are not visible in diagnostic renders. Rounded root shading/hard transition remains minor polish, not an exposed cut or disconnected base. Direct Blender source selected; prior AI candidate remains style guidance only. Exact shared frame and independent body w/B versus item w/W tint retained.'
author=dict(recorded_at=now,status='PASS',scope='Generation authoring only; not native acceptance',reason=reason,independent_review=ref(HERE/'independent-fit-review.json'),reviewer={'agent':'/root/calibrated_horn_fit_review','fork_turns':'none','reasoning_effort_requested':'low','model':'Inherited main model; no override'},dispositions=[{'finding':'Earlier apparent root cap','decision':'RESOLVED structural concern / MINOR POLISH appearance','evidence':[ref(HERE/'root-closeups.png'),ref(HERE/'root-end-diagnostics.json'),ref(HERE/'proxy-source-comparison.png')],'reason':'Visible crown contact has no background gap, continuous curl and coherent depth in the actual body compositions. Direct end-face render shows no exposed starting cap; this diagnostic supports rather than replaces observed fit. Root shading can be polished after full-set testing.'},{'finding':'Rear small root-side flank slivers','decision':'MINOR POLISH','reason':'Current volume and skull ownership explain them as continuous bone flank; no pasted frontal curl or detached segment observed.'},{'finding':'AI changed recipient/framing','decision':'NOT USED IN PRODUCTION SOURCE','reason':'Actual source is direct Blender export; source body bytes and image alpha verified unchanged.'}],registration_checks=decision['checks'],native_acceptance=model['native_acceptance'],limitations=['Skull depth and root positions are authored, not captured native joint coordinates.','Head proxy is a silhouette-constrained fitting aid, not a complete custom-body model.','No game, equip/unequip, animation or pose acceptance was performed.'])
write(OUT/'authoring-review.json',author)
write(OUT/'artifact-manifest.json',dict(recorded_at=now,entry=entry['id'],registration_script=ref(HERE/'register.py'),artifacts=[ref(p) for p in sorted(OUT.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
for step,action,names in [('construct_and_overlay_one_item','Select the intact reused Blender shape and calibrated original-head fit.',['fit-contract.json','source-packet.json','authoring-review.json']),('export_whole_item_and_visibility_masks','Verify whole volume, neutral material conversion and independent tint/near-far planes without changing source alpha or original body.',['model.json','registration-decisions.json','full-comparison.png','near-comparison.png','far-comparison.png']),('recompose_check_cuffs_attachment_occlusion_all_views','Inspect actual roots, separate flesh ears, curl clearance and front/back/side overlap on the original body.',['neutral-comparison.png','authoring-review.json']),('review_game_scale_and_palette','Review native w/W horn roles independently from w/B body at intended render size.',['native-comparison.png','detail-comparison.png','ledger-workflow-diagnostics.json','artifact-manifest.json'])]:
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'independent-fit-review.json'),ref(OUT/'fit-contract.json')],outputs=[ref(OUT/n) for n in names],review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')),current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-comparison.png')),registration_summary='Selected direct Blender horn volume on the unchanged accepted body, with calibrated head proxy, full four-view depth, independent native w/W masks and registered fixed physical frame. Native acceptance pending.')
entry.pop('advancement_blocker',None)
n=next(e for e in ledger['entries'] if e['id']=='ITEM-HORNS');assert not n.get('generation_ready');n.update(status='IN PROGRESS',current_step='resolve_item_identity_description_palette');ledger.update(active_entry=n['id'],updated_at=now);write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Horn fit generation authoring closed; ITEM-HORNS is sole active entry. Native acceptance pending.')
