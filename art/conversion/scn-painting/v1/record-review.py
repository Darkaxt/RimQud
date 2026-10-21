"""Close Painting art authoring only, with current evidence and native gate preserved."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';CON=HERE/'construction-v2'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
assert not (OUT/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-PAINTING' and ledger['stage']=='Stage 3 ACTIVE';entry=next(e for e in ledger['entries'] if e['id']=='SCN-PAINTING')
model=read(OUT/'model.json');controls=read(CON/'construction-controls.json');source=read(HERE/'source-packet.json');receipt=read(HERE/'generation-receipt.json')
verified=set()
def walk(v):
    if isinstance(v,dict):
        key='path' if 'path' in v else 'public_file' if 'public_file' in v else None
        if key and 'sha256' in v:
            p=Path(v[key]);p=p if p.is_absolute() else ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],str(p);verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
for value in [model,controls,source,receipt,read(HERE/'native-state-index.json'),read(HERE/'material-selection.json'),entry['process_log']]:walk(value)
assert len(model['states'])==2 and receipt['actual_calls']==1 and not receipt['second_isolation_call'] and not model['native_activation']
assert receipt['submitted_prompt']==(CON/'refinement-prompt.txt').read_text().strip()
assert source['palette']['declared_tile_primary']=='w' and len(source['palette']['random_detail'])==8
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];pcol=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8);dcol=np.frombuffer(bytes.fromhex(palette['R']),dtype=np.uint8)
dimensions=[]
for state,construction in zip(model['states'],controls['states']):
    assert state['native_tile']==construction['native_tile']
    assert set(state['views'])=={'south','east','north','west'}
    for facing,view in state['views'].items():
        master=rgba(ROOT/view['master']['path']);assert np.array_equal(master[:,:,0],master[:,:,1]) and np.array_equal(master[:,:,1],master[:,:,2])
        if facing!='west':
            manual=rgba(ROOT/construction['views'][facing]['constructed']['path']);assert np.array_equal(master[:,:,3],manual[:,:,3])
            lum=manual[:,:,:3].astype(float).mean(2);assert np.max(np.abs(master[:,:,0].astype(float)-lum))<=3.6
        else:
            for key,r in view.items():assert np.array_equal(np.array(Image.open(ROOT/r['path'])),np.array(Image.open(ROOT/state['views']['east'][key]['path']))[:,::-1])
        small=rgba(ROOT/view['primary']['path']);assert small.shape==(256,256,4) and np.array_equal(small[:,:,0],small[:,:,1]) and np.array_equal(small[:,:,1],small[:,:,2])
        assert np.array_equal(small,rgba(ROOT/view['detail']['path']))
        coverage=np.array(Image.open(ROOT/view['coverage']['path']).convert('L'));assert np.array_equal(small[:,:,3],coverage)
        weight=np.array(Image.open(ROOT/view['detail_weight']['path']).convert('L'));dual=rgba(ROOT/view['authored_dualcolor_mask']['path']);assert np.array_equal(dual[:,:,0],weight) and np.array_equal(dual[:,:,3],coverage)
        if facing in ['east','north','west']:assert not weight.any(),facing
        else:assert weight.max()==255
        w=weight.astype(float)/255;rgb=np.uint8(np.rint((small[:,:,:3].astype(float).mean(2)/255)[:,:,None]*((1-w[:,:,None])*pcol+w[:,:,None]*dcol)));rgb[coverage==0]=0
        assert np.array_equal(np.dstack([rgb,coverage]),rgba(ROOT/view['native_preview']['path']))
        alpha=master[:,:,3]>127;yy,xx=np.where(alpha);dimensions.append(dict(state=state['id'],facing=facing,visible_bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]))
now=datetime.now(timezone.utc).isoformat()
reason=('Reviewed both actual native Painting masks, exact Painting/MountedFurniture/Furniture ancestry, description and colour-selection code, actual installed VTE/Ideology Lectern S/E/N reference, editable landscape/portrait easels and full physical turnarounds. '
    'Source paint motifs stay abstract and distinct; negative pixels inside canvas are explicitly interpreted as dark image space on continuous linen rather than holes. No invented depicted subject or lectern identity/ritual mechanics. '
    'Initial flat support strips collapsed in profile; rejected first construction retained. Corrected square-section solid support projection retains shared5.6unitdepth, canvas thickness and14degree map-camera before actual ImageGen refinement. All directions share full source-cell frame, physical dimensions and placement pivot; no panel-width target, independent bounds fitting or inflated edge-on canvas. '
    'One actual composed six-view ImageGen proposal retained. It added unsupported metal fittings and excessive grain; canonical manual geometry, alpha and source paint ownership remain authoritative, with only bounded neutral high-frequency material grain transferred. Rejected generated details and complete raw output are retained; no second isolation or fabricated refinement. '
    'Eight native tile-detail examples shown beside both original source designs at intended sizes. RandomColors.MainColor affects glyph ColorString only, while Cell uses declared TileColor w; native independently selects detail fromm/W/r/R/b/B/g/G. Neutral gray textures, single coverage and separate detail weight prevent baked colours or background fill. Reverse is unpainted; profile retains full stand depth; W mirrors symmetric E. '
    'Both designs have S/E/N plus mirroredW authoring. Extra furniture views are unbound; no native rotation, automatic placement or altered random selector. Clothing integration is inapplicable. Source/reference/prompt/artifact hashes checked and coverage/tint contracts inspected. Native palette/state/visibility/cell binding acceptance remains pending after full-ledger generation.')
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Painting art authoring only: two native designs, directional construction/refinement/registration',reason=reason,verified_source_files=len(verified),visible_bounds=dimensions,
    checks=dict(two_native_designs=True,source_metadata_and_masks=True,actual_directional_donor=True,shared_physical_depth=True,solid_support_correction=True,source_abstract_motifs=True,one_actual_refinement=True,unsupported_generated_details_excluded=True,manual_master_alpha_exact=True,neutral_equal_RGB=True,independent_detail_weight=True,source_tile_primary_w=True,eight_native_detail_choices=True,all_views_reviewed=True,west_mirror_exact=True,clothing_not_applicable=True,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
def event(step,action,inputs,outputs,review,result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in inputs],outputs=[ref(HERE/n) for n in outputs],review=review,result=result))
event(entry['required_steps'][2],'Inspect first profiles; replace collapsed flat support strips with projected solid square-section beams, retaining source designs.',['manual-suggestion.png','construction-controls.json'],['construction-v2/manual-suggestion.png','construction-v2/constructed-turnarounds.png','construction-v2/construct-painting.py'],'First profile beam width vanished because its flat strip normal aligned with view. New physical square sections reproject in every facing; no stretching or independent side bounds. Initial views remain as rejected construction evidence.')
event(entry['required_steps'][4],'Run and inspect actual six-view contextual ImageGen material refinement from corrected construction and native/reference plate.',['construction-v2/refinement-prompt.txt','construction-v2/constructed-turnarounds.png','source-reference.png'],['refined-raw.png','generation-receipt.json','first-structural-review.json'],'Six corresponding easels and both native abstract designs retained, with profile stand depth and unpainted reverse. Reject added corner metal/bolts, heavier shading and changed alpha as canonical art; useful interior surface texture retained.')
event(entry['required_steps'][4],'Patch refinement through authoritative geometry and selected quiet material interiors.',['refined-raw.png','construction-v2/construction-controls.json'],['material-selection-preview.png','material-selection.json','selected-linen.png','selected-wood.png','register-painting.py'],'No second AI isolation. Actual inspected unmarked linen/wood interiors supply only bounded high-pass neutral grain; no generated border, alpha, metal fittings, changed paint layout or specular shading. Patch shown in registered neutral S/E/N views.')
event(entry['required_steps'][5],'Register two designs with S/E/N and mirrored W, gray textures, one coverage plane and native primary/detail weighting.',['construction-v2/construction-controls.json','source-packet.json','material-selection.json'],['registered/model.json','registered/registration-decisions.json','registered/ownership-turnarounds.png'],'Shared full-cell mapping; master alpha exactly canonical geometry. Runtime tile foreground w and eight actual native detail options remain source-owned. Separate colour inputs combine by weight, not duplicate alpha-over. Reverse/profile detail planes empty.')
event(entry['required_steps'][6],'Review complete turnarounds, source palette comparison and intended-size silhouettes.',['registered/model.json'],['registered/neutral-turnarounds.png','registered/source-and-native-palettes.png','record-review.py','registered/authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][7],'Keep exact source tile/random colour mapping, visibility and native registration acceptance pending.',['registered/model.json'],[],'No game launch, runtime activation, rotation logic, native batch or test harness. Art authoring only; full-ledger generation gate remains binding.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-turnarounds.png')),registration_summary='Painting: two actual landscape/portrait native choices, source-bound abstract motifs, corrected solid supports and shared physical S/E/N (+mirroredW) construction; one actual ImageGen material proposal patched through canonical geometry. Neutral primary/detail weight and eight native detail examples. Native acceptance pending.',art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
following=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'));following.update(status='IN PROGRESS',current_step=following['required_steps'][0]);ledger.update(active_entry=following['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_files=len(verified),native_acceptance='pending')))
