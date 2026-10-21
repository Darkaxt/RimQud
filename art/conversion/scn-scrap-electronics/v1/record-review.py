"""Close Scrap Electronics generation, preserving exact native identity and pending acceptance."""
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
assert not (OUT/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-SCRAP-ELECTRONICS' and ledger['stage']=='Stage 3 ACTIVE';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
model=read(OUT/'model.json');controls=read(HERE/'construction-controls-patched.json');packet=read(HERE/'source-packet-corrected.json');first=read(HERE/'generation-first-receipt.json');retry=read(HERE/'generation-retry-receipt.json')
verified=set()
def walk(v):
    if isinstance(v,dict):
        k='path' if 'path' in v else 'public_file' if 'public_file' in v else None
        if k and 'sha256' in v:
            p=Path(v[k]);p=p if p.is_absolute() else ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],str(p);verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
for v in [model,controls,packet,first,retry,entry['process_log'],read(OUT/'registration-decisions.json')]:walk(v)
assert len(packet['ancestry'])==6 and packet['identity']==' -> '.join(n['name'] for n in packet['ancestry'])
assert first['call_number']==1 and retry['call_number']==2 and not model['native_activation']
assert first['submitted_prompt']==(HERE/'refinement-prompt-patched.txt').read_text().strip() and retry['submitted_prompt']==(HERE/'refinement-retry-prompt.txt').read_text().strip()
assert packet['variants']['native_tile_choices']==['items/bit11.bmp'] and not packet['variants']['random_tile_builder']
manual=rgba(ROOT/controls['constructed']['path']);master=rgba(ROOT/model['master']['path']);assert np.array_equal(manual[:,:,3],master[:,:,3]);assert np.array_equal(master[:,:,0],master[:,:,1]) and np.array_equal(master[:,:,1],master[:,:,2])
own=np.array(Image.open(OUT/'surface-transfer-ownership.png').convert('L'))>0;base=manual[:,:,:3].astype(float).mean(2);delta=master[:,:,0].astype(float)-base
assert np.max(np.abs(delta[own]))<=12.6 and np.max(np.abs(delta[(~own)&(manual[:,:,3]>0)]))<=.6
# Canonical pocket centres and true outer background remain transparent.
for x,y in [(300,345),(210,410),(30,30)]:assert master[y,x,3]==0,(x,y)
rr=rgba(HERE/'refined-retry.png');assert rr[630,610,3]==0 and rr[820,400,3]==0
small=rgba(ROOT/model['primary']['path']);detail=rgba(ROOT/model['detail']['path']);assert small.shape==(256,256,4) and np.array_equal(small,detail)
assert np.array_equal(small[:,:,0],small[:,:,1]) and np.array_equal(small[:,:,1],small[:,:,2])
expected=np.array(Image.fromarray(master).resize((256,256),Image.Resampling.LANCZOS));expected[:,:,:3]=np.uint8(np.rint(expected[:,:,:3].astype(float).mean(2)))[:,:,None];expected[expected[:,:,3]==0,:3]=0;assert np.array_equal(expected,small)
coverage=np.array(Image.open(ROOT/model['coverage']['path']).convert('L'));weight=np.array(Image.open(ROOT/model['detail_weight']['path']).convert('L'));dual=rgba(ROOT/model['authored_dualcolor_mask']['path']);assert np.array_equal(small[:,:,3],coverage) and np.array_equal(dual[:,:,0],weight) and np.array_equal(dual[:,:,3],coverage);assert weight.max()==255
color=np.frombuffer(bytes.fromhex('77bfcf'),dtype=np.uint8);rgb=np.uint8(np.rint(small[:,:,:3].astype(float).mean(2)[:,:,None]/255*color));rgb[coverage==0]=0;assert np.array_equal(np.dstack([rgb,coverage]),rgba(ROOT/model['native_preview']['path']))
now=datetime.now(timezone.utc).isoformat()
reason=('Reviewed exact Scrap Electronics definition and six-node inherited chain, fractured-microchip identity/prose, source bit11 P/D mask and C/C palette, actual installed VTE SignalChip/Biotech Graphic_Single reference and editable source-bound manual shape. '
    'Two opposing occupied triangles, open fracture pockets and diamond rim remain source recognisable; traced/contact marks, shallow edge and fracture notches are explicitly authored. No generic green PCB, intact SignalChip housing, wires/extra pins, pile or donor mechanic imported. '
    'Fixed small8x8native-pixel occupancy in full16x24cell maps through512x768master to256square recipient; native orientation belongs to the shape, not an added perspective camera. Two tiny rim-junction gaps were patched by editable endpoint extension before contextual refinement. '
    'First actual ImageGen proposal partly filled an empty pocket with alpha154 and stray haze; rejected whole output/prompt/receipt retained. One targeted retry restored both zero-alpha pockets and smooth restrained surfaces. Actual saved-alpha composite, not RGB-only tool thumbnail, confirms transparency. No third call or AI isolation. '
    'Retry moved/rescaled the subject and has weak stray exterior alpha. Deterministic material alignment is a sampling correspondence only; canonical geometry, circuit marks, source scale/center and exact coverage remain fixed. Opaque unmarked generated interiors supply bounded broad shading through eroded authored face ownership. No generated alpha, shifted contour, stray fill/halo or extra line transferred. '
    'Final master coverage exactly matches patched construction; true holes and outer canvas are transparent. Equal-RGB neutral inputs retain source P/D weighting even though both runtime colours are C=77bfcf. Coverage and colour weight are separate; inputs combine by weight, not duplicate alpha-over. Native C/C intended-size plate reviewed. '
    'Bind only exact Scrap Electronics. Scrap Metal/Crystal/Energy reuse bit11 and retain distinct unfinished identities. No source RandomTile or extra repaired/burning/stack image: one fixed map view, no furniture turnaround or clothing integration. Native inventory/stack/disassembly/visibility/palette/cell mapping acceptance remains pending behind full-ledger generation.')
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete Scrap Electronics art authoring only',reason=reason,verified_source_files=len(verified),actual_imagegen_calls=2,
    checks=dict(exact_identity_and_source=True,six_node_ancestry=True,actual_mod_reference=True,editable_manual_shape=True,rim_contact_patch=True,first_refinement_rejected=True,targeted_retry=True,retry_true_pockets_zero_alpha=True,no_invisible_RGB_misclassification=True,canonical_master_alpha_exact=True,generated_exterior_alpha_excluded=True,material_transfer_bounded=True,full_cell_mapping=True,neutral_equal_RGB=True,primary_detail_weight_separate=True,native_C_C_exact=True,intended_size_reviewed=True,shared_tile_not_global_binding=True,secondary_views_not_applicable=True,clothing_not_applicable=True,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
def event(step,action,ins,outs,review,result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result))
event(entry['required_steps'][4],'Run targeted second ImageGen refinement and inspect real saved-alpha composite.',['refinement-retry-prompt.txt','patched-chip.png','source-reference.png','refined-first-rejected.png'],['refined-retry.png','generation-retry-receipt.json','retry-alpha-review.png','retry-subject-bounds.json','retry-structural-review.json'],'Retry preserves coherent fragments/bridges and true zero-alpha pockets. Grey RGB in transparent pixels made tool preview misleading; actual alpha composite confirms open background. Subject alignment and weak stray alpha are handled by canonical geometry; no third generation or isolation.')
event(entry['required_steps'][5],'Register actual refined surface onto fixed source geometry and separate neutral P/D weighting.',['construction-controls-patched.json','refined-retry.png','source-packet-corrected.json'],['register-chip.py','registered/registration-decisions.json','registered/model.json','registered/surface-transfer-ownership.png'],'Refinement affects bounded interior material shading only. Exact patched manual alpha/center/scale/circuit marks and source open pockets retained; generated alpha/contours/halo excluded. C/C source tint is applied later through separate colour weight and coverage, not baked into neutral textures.')
event(entry['required_steps'][6],'Inspect original/manual/rejected/retry/registered evidence and native C/C at intended map sizes.',['registered/model.json'],['registered/source-neutral-native-scale.png','registered/whole-process-comparison.png','record-review.py','registered/authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][7],'Retain exact-blueprint tile, palette, visibility, stack/pickup/disassembly and cell mapping acceptance for final integrated set.',['registered/model.json'],[],'Art authoring only; no native activation, game launch, state simulation or harness test. All pending conversions must finish generation first.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'source-neutral-native-scale.png')),registration_summary='Scrap Electronics: exact fractured-microchip identity, source diamond fracture pockets and C/C roles; actual VTE chip rendering reference, editable manual/contact patch, first ImageGen rejection and targeted retry, fixed-geometry surface registration and native intended-size evidence. Shared bit11 scoped to exact blueprint. Native acceptance pending.',art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
following=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'));assert following['id']=='SCN-SCRAP-METAL';following.update(status='IN PROGRESS',current_step=following['required_steps'][0]);ledger.update(active_entry=following['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1;write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_files=len(verified),native_acceptance='pending')))
