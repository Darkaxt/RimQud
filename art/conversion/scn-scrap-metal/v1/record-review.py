"""Close source-bound bent-sheet authoring; native acceptance remains deferred."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
assert not (OUT/'authoring-review.json').exists();ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-SCRAP-METAL' and ledger['stage']=='Stage 3 ACTIVE';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
model=read(OUT/'model.json');source=read(HERE/'source-packet.json');controls=read(HERE/'construction-controls.json');receipt=read(HERE/'generation-receipt.json');verified=set()
def walk(v):
    if isinstance(v,dict):
        k='path' if 'path' in v else 'public_file' if 'public_file' in v else None
        if k and 'sha256' in v:
            p=Path(v[k]);p=p if p.is_absolute() else ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],str(p);verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
for v in [model,source,controls,receipt,entry['process_log'],read(OUT/'registration-decisions.json')]:walk(v)
assert source['identity']==' -> '.join(n['name'] for n in source['ancestry']) and len(source['ancestry'])==6
assert source['display_name']=='bent metal sheet' and source['palette']['primary']=='B' and source['palette']['detail']=='C'
assert source['resolved_parts']['TinkerItem']['Bits']=='B' and not source['variants']['random_builder']
assert receipt['actual_calls']==1 and not receipt['second_isolation_call'] and not model['native_activation'];assert receipt['submitted_prompt']==(HERE/'refinement-prompt.txt').read_text().strip()
manual=rgba(ROOT/controls['constructed']['path']);master=rgba(ROOT/model['master']['path']);assert np.array_equal(manual[:,:,3],master[:,:,3]);assert np.array_equal(master[:,:,0],master[:,:,1]) and np.array_equal(master[:,:,1],master[:,:,2])
own=np.array(Image.open(OUT/'surface-transfer-ownership.png').convert('L'))>0;base=manual[:,:,:3].astype(float).mean(2);diff=master[:,:,0].astype(float)-base;assert np.max(np.abs(diff[own]))<=12.6 and np.max(np.abs(diff[(~own)&(manual[:,:,3]>0)]))<=.6
for x,y in [(300,345),(210,410),(30,30)]:assert master[y,x,3]==0
raw=rgba(HERE/'refined-raw.png');assert raw[690,610,3]==0 and raw[835,420,3]==0
small=rgba(ROOT/model['primary']['path']);assert small.shape==(256,256,4) and np.array_equal(small,rgba(ROOT/model['detail']['path']));assert np.array_equal(small[:,:,0],small[:,:,1]) and np.array_equal(small[:,:,1],small[:,:,2])
expected=np.array(Image.fromarray(master).resize((256,256),Image.Resampling.LANCZOS));expected[:,:,:3]=np.uint8(np.rint(expected[:,:,:3].astype(float).mean(2)))[:,:,None];expected[expected[:,:,3]==0,:3]=0;assert np.array_equal(expected,small)
coverage=np.array(Image.open(ROOT/model['coverage']['path']).convert('L'));weight=np.array(Image.open(ROOT/model['detail_weight']['path']).convert('L'));dual=rgba(ROOT/model['authored_dualcolor_mask']['path']);assert np.array_equal(coverage,small[:,:,3]) and np.array_equal(dual[:,:,0],weight) and np.array_equal(dual[:,:,3],coverage) and weight.max()==255
fg=np.frombuffer(bytes.fromhex('0096ff'),dtype=np.uint8);de=np.frombuffer(bytes.fromhex('77bfcf'),dtype=np.uint8);w=weight.astype(float)/255;rgb=np.uint8(np.rint(small[:,:,:3].astype(float).mean(2)[:,:,None]/255*((1-w[:,:,None])*fg+w[:,:,None]*de)));rgb[coverage==0]=0;assert np.array_equal(np.dstack([rgb,coverage]),rgba(ROOT/model['native_preview']['path']))
now=datetime.now(timezone.utc).isoformat()
reason=('Inspected exact Scrap Metal definition, complete six-node inherited metadata and source bit11 mask: bent metal sheet from machine-fossil scrap, primary B=0096ff and detail C=77bfcf, no source RandomTile or TileColor override. '
    'Actual installed VTE Steel_a/Core Steel reference supplies broad quiet metal facets/contrast only; its rounded lump, brown palette, stack pictures and smelting mechanics are not imported. Source diamond perimeter/two opposing occupied regions/open quadrants and small cell occupancy remain authoritative. '
    'Editable manual sheet includes source-bound P/D regions with shallow curled folds/dents and fine creases, explicitly authored unseen material interpretation. No electronic circuit traces/pads/pins, intact modern chip, stack of plates or generic nugget despite shared source tile with other scrap. '
    'One actual contextual ImageGen refinement retained complete. Both internal pockets are genuinely zero alpha in saved output, confirmed with actual colored-background composite; RGB-only preview of invisible grey/haze is not used as transparency evidence. Refined surfaces/bridges/folds are usable, so no retry or second isolation was invented. '
    'Generated subject placement/extent differs slightly and weak stray exterior alpha remains. Material correspondence aligns sampling only; final source frame/center/scale/geometry/creases and exact manual coverage stay fixed. Bounded broad shading from valid opaque generated interiors transfers through eroded authored face ownership; generated outline, alpha, stray fill/halo and shifted details excluded. '
    'Neutral master/recipient RGB channels match. Production uses one coverage plane and independent P/D weight: native blue B and cyan C remain separate. Neutral colour inputs share coverage and combine by weight, not duplicate alpha-over. Full-cell512x768master to256square recipient mapping and intended-size B/C views inspected. Source empty quadrants and outer canvas remain transparent. '
    'This entry binds exact Scrap Metal only; other bit11 identities do not inherit readiness or its palette. One source-supported fixed map view; furniture turnarounds and clothing integration inapplicable. Native pickup/stack/disassembly, exact identity/tile, palette/coverage, visibility and cell mapping acceptance stay pending after all ledger generation.')
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete Scrap Metal bent-sheet art generation only',reason=reason,verified_source_files=len(verified),actual_imagegen_calls=1,
    checks=dict(exact_identity=True,complete_ancestry=True,source_B_C_roles=True,actual_mod_reference=True,editable_bent_sheet=True,no_circuitry=True,source_pockets_retained=True,one_actual_refinement=True,saved_alpha_reviewed=True,canonical_master_alpha_exact=True,material_transfer_bounded=True,generated_stray_alpha_excluded=True,full_cell_mapping=True,neutral_equal_RGB=True,independent_detail_weight=True,native_B_C_exact=True,intended_size_reviewed=True,exact_blueprint_not_global_bit11=True,secondary_views_not_applicable=True,clothing_not_applicable=True,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
def event(step,action,ins,outs,review,result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result))
event(entry['required_steps'][4],'Run actual bent-sheet ImageGen refinement; inspect form and real saved-alpha pockets before registration.',['refinement-prompt.txt','constructed-sheet.png','source-reference.png'],['refined-raw.png','generation-receipt.json','refined-alpha-review.png','refined-subject-bounds.json','first-structural-review.json'],'One actual proposal retains bent folds, two source surfaces, perimeter bridges and real zero-alpha pockets. No circuit marks/round nugget. Actual alpha composite resolves invisible RGB grey in tool thumbnail. No retry required for usable material reference.')
event(entry['required_steps'][5],'Patch generated surface through fixed geometry, canonical coverage and native B/C weighting.',['construction-controls.json','source-packet.json','refined-raw.png'],['register-sheet.py','registered/model.json','registered/registration-decisions.json','registered/primary-detail-ownership-view.png','registered/surface-transfer-ownership.png'],'Geometry/frame/center and manual fold/crease marks stay fixed. Align material sampling only, transfer bounded opaque interior shading; reject generated outlines, alpha and exterior haze. Separate detail weight plus single coverage retain exact source B/C tint semantics.')
event(entry['required_steps'][6],'Review source/manual/refinement/registered comparison and native intended-size colors.',['registered/model.json'],['registered/source-neutral-native-scale.png','registered/whole-process-comparison.png','record-review.py','registered/authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][7],'Defer exact identity/tile, B/C palette/coverage, cell mapping and native item lifecycle acceptance until all generation.',['registered/model.json'],[],'No runtime activation, game launch, inventory-state test, native batch or harness. Full-ledger generation gate remains binding.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'source-neutral-native-scale.png')),registration_summary='Scrap Metal: own bent-sheet identity and source B/C roles; actual VTE metal shading reference, editable curled sheet, one real refinement with saved-alpha inspection, fixed-geometry surface registration and native intended-size views. Exact identity binding despite shared bit11. Native acceptance pending.',art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
following=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'));assert following['id']=='SCN-TORCHPOST';following.update(status='IN PROGRESS',current_step=following['required_steps'][0]);ledger.update(active_entry=following['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1;write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_files=len(verified),native_acceptance='pending')))
