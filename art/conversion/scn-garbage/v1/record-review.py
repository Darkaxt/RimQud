"""Record complete Garbage family authoring; native acceptance remains behind full generation."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
assert not (OUT/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-GARBAGE' and ledger['stage']=='Stage 3 ACTIVE';entry=next(e for e in ledger['entries'] if e['id']=='SCN-GARBAGE')
model=read(OUT/'model.json');packet=read(HERE/'source-packet.json');source=read(HERE/'native-state-index.json');controls=read(HERE/'construction-controls.json');receipt=read(HERE/'generation-receipt.json');selection=read(HERE/'material-selection.json')
verified=set()
def walk(v):
    if isinstance(v,dict):
        key='path' if 'path' in v else ('public_file' if 'public_file' in v else None)
        if key and 'sha256' in v:
            p=Path(v[key]);p=p if p.is_absolute() else ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],str(p);verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
for v in [model,packet,source,controls,receipt,selection]:walk(v)
assert len(model['states'])==5 and {s['native_tile'] for s in model['states']}=={s['native_tile'] for s in source['states']}
assert len([s for s in model['states'] if s['role']=='RandomTile choice'])==4
assert model['states'][-1]['id']=='fallback' and model['states'][-1]['native_tile']==packet['required_native_art']['declared_fallback']
assert receipt['actual_calls']==1 and not receipt['second_isolation_call'] and not model['native_activation']
assert model['registration']['manual']==[512,768] and model['registration']['recipient']==[256,256]
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];color=np.frombuffer(bytes.fromhex(palette['K']),dtype=np.uint8)
for state,construction,native in zip(model['states'],controls['states'],source['states']):
    assert state['native_tile']==construction['native_tile']==native['native_tile']
    original=rgba(ROOT/construction['constructed']['path']);master=rgba(ROOT/state['master']['path']);assert np.array_equal(original[:,:,3],master[:,:,3])
    assert np.array_equal(master[:,:,0],master[:,:,1]) and np.array_equal(master[:,:,1],master[:,:,2])
    p=rgba(ROOT/state['primary']['path']);assert p.shape==(256,256,4) and np.array_equal(p[:,:,0],p[:,:,1]) and np.array_equal(p[:,:,1],p[:,:,2])
    expected=np.array(Image.fromarray(master).resize((256,256),Image.Resampling.LANCZOS));expected[:,:,:3]=np.uint8(np.round(expected[:,:,:3].astype(float).mean(2)))[:,:,None];expected[expected[:,:,3]==0,:3]=0
    assert np.array_equal(expected,p)
    coverage=np.array(Image.open(ROOT/state['coverage']['path']).convert('L'));assert np.array_equal(p[:,:,3],coverage)
    detail=rgba(ROOT/state['detail']['path']);assert not detail.any()
    assert not np.array(Image.open(ROOT/state['detail_weight']['path']).convert('L')).any() and not np.array(Image.open(ROOT/state['detail_coverage']['path']).convert('L')).any()
    mask=rgba(ROOT/state['authored_dualcolor_mask']['path']);assert not mask[:,:,:3].any() and np.array_equal(mask[:,:,3],coverage)
    assert not p[0,:,3].any() and not p[-1,:,3].any() and not p[:,0,3].any() and not p[:,-1,3].any()
    tinted=p.copy();tinted[:,:,:3]=np.uint8(np.round(p[:,:,:3].astype(float)*color/255));tinted[tinted[:,:,3]==0,:3]=0;assert np.array_equal(tinted,rgba(ROOT/state['native_preview']['path']))
    raw=rgba(Path(native['private_mask']['path']));assert set(raw[raw[:,:,3]>0,0].tolist())=={0}
now=datetime.now(timezone.utc).isoformat()
reason=('Inspected all four actual RandomTile sprites and declared fallback, exact native metadata and source K/^k roles, actual Core TrashA/B/C Graphic_Cluster references, editable five-layout construction, actual ImageGen proposal, rejected and corrected material specimens, fixed-geometry surface registration, initial wire/contrast defects and corrected neutral/native/intended-size plates. '
        'Layouts retain source-relative fragments and sparse fallback; glass lens, ink serif, acid-eaten lug and wire ribbon are authored interpretations of ambiguous blobs, not measured source object identities. No modern bottle/can heap, native filth placement or donor contents/palette/mechanics imported. '
        'Refinement supplies restrained neutral surface grain only; canonical curves, ink and full-cell geometry remain authoritative. Rejected paper edge/ink sample is not used. Repeated wire grain removed and excessive interior darkening compressed for source K/k readability without changing alpha or material identities. '
        'All five master alpha planes exactly match selected manual coverage. Common512x768source-cell frame maps to256x256recipient without individual bounds fitting; neutral RGB remains gray. Every source visible R is0, so all material roles share primary K; detail/weight/coverage are empty and ^k stays outside the object. '
        'Four initial random choices and declared fallback stay distinct, scoped to Garbage rather than global glyph art. Native Garbage code consumes a stack object instead of assigning an empty tile; separate TrashFire-table object creation does not invent a burning Garbage state. '
        'Fixed map debris needs no directional turnaround or clothing assembly. Takeability, non-solid status, stack/rummage/divination/fire behavior remain native. One actual ImageGen call retained, no second isolation or fabricated refinement. Native selection/visibility/palette/stack/burning acceptance remains unfinished after full generation.')
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete five-state Garbage art generation only',reason=reason,verified_source_files=len(verified),
    checks=dict(four_actual_random_choices=True,declared_fallback_distinct=True,native_consumption_not_empty_sprite=True,actual_Core_reference=True,editable_source_layouts=True,one_actual_refinement=True,
    rejected_samples_retained=True,no_generated_border_or_ink_import=True,wire_band_removed=True,source_K_k_contrast_reviewed=True,exact_manual_master_alpha=True,common_full_cell_mapping=True,
    neutral_equal_RGB=True,source_primary_K_only=True,detail_planes_empty=True,background_not_baked=True,all_five_intended_size_reviewed=True,secondary_views_not_applicable=True,clothing_integration_not_applicable=True,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
def event(step,action,ins,outs,review,result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result))
event(entry['required_steps'][4],'Run actual five-layout ImageGen material refinement from manual design, native silhouettes and exact Core reference plate.',['refinement-prompt.txt','constructed-family.png','source-construction-comparison.png','source-reference-variants-reviewed.png'],['refined-raw.png','generation-receipt.json','first-structural-review.json'],'Five corresponding piles and sparse fallback retained; generated border/gloss is not canonical. Actual proposal retained whole. Usable surface texture is selected without another AI isolation or invented directional views.')
event(entry['required_steps'][4],'Inspect/reject contaminated first specimen picks and select opaque material interiors for restrained transfer.',['refined-raw.png'],['material-specimen-boxes.json','material-specimen-review.png','select-materials.py','material-selection.json','selected-material-specimens.png'],'First paper pick contained transparency/printed stroke and metal approached an edge. New same-material interior patches exclude those pixels. Only bounded neutral high-frequency residual is transferred through authored ownership; no generated contour, alpha or label.')
event(entry['required_steps'][5],'Register all five fixed source layouts with neutral primary/empty-detail/coverage channels and native K preview.',['construction-controls.json','material-selection.json','palette-resolution.json'],['register-garbage.py','registered/model.json','registered/registration-decisions.json'],'Master alpha exactly matches manual construction; all five source-cell mappings and sparse fallback retained. Single primary K role; all detail planes empty. No background cap, secondary material palette, per-pile bounds fit or runtime activation.')
event(entry['required_steps'][5],'Correct observed wire repeat and overly dark shading while retaining source geometry and palette.',['registered/model.json'],['correct-readability.py','readability-correction.json','registration-initial/neutral-family.png','registration-initial/native-K-family.png','registration-initial/game-scale-source-comparison.png'],'Initial registered evidence retained. Remove generated wire grain and compress material-interior shading only; original contours/ink/recesses/highlights/coverage and K/k roles remain. No repeated ImageGen request or changed native behavior.')
event(entry['required_steps'][6],'Inspect complete five-layout neutral/native and source-comparison views at intended map sizes.',['registered/model.json'],['registered/neutral-family.png','registered/native-K-family.png','registered/game-scale-source-comparison.png','record-review.py','registered/authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][7],'Retain native exact-key/random-selection/visibility/palette/rummage-stack/fire acceptance behind all-generation gate.',['registered/model.json'],[],'Authoring previews only. No native activation, game launch, state simulation or harness test. Entry remains UNFINISHED pending integrated Stage3 acceptance.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-family.png')),
    registration_summary='Garbage: four actual RandomTile choices plus distinct declared fallback, source-layout glass/ink/lug/wire interpretations, one controlled material refinement and explicit wire/contrast corrections. Neutral primary K only; empty detail and transparent gaps, shared source-cell mapping. Native selection/consumption/fire acceptance pending.',
    art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
following=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'));assert following['id']=='SCN-PAINTING'
following.update(status='IN PROGRESS',current_step=following['required_steps'][0]);ledger.update(active_entry=following['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_source_files=len(verified),native_acceptance='pending')))
