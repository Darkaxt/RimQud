"""Close Torchpost static-holder generation, retaining native fire/light acceptance gate."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];CON=HERE/'construction-v3';OUT=HERE/'registered'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
assert not (OUT/'authoring-review.json').exists();ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='SCN-TORCHPOST' and ledger['stage']=='Stage 3 ACTIVE';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
model=read(OUT/'model.json');controls=read(CON/'construction-controls.json');source=read(HERE/'source-packet.json');receipt=read(HERE/'generation-receipt.json');verified=set()
def walk(v):
    if isinstance(v,dict):
        k='path' if 'path' in v else 'public_file' if 'public_file' in v else None
        if k and 'sha256' in v:
            p=Path(v[k]);p=p if p.is_absolute() else ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],str(p);verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
for v in [model,source,controls,receipt,read(HERE/'material-selection.json'),entry['process_log']]:walk(v)
assert len(source['ancestry'])==6 and source['resolved_parts']['LightSource']['Radius']=='6' and source['resolved_parts']['LightSource']['Lit']=='true'
assert source['resolved_parts']['PrefabImposter']['Prefab']=='Prefabs/Particles/TorchpostFlames'
assert receipt['actual_calls']==1 and not receipt['second_isolation_call'] and receipt['submitted_prompt']==(CON/'refinement-prompt.txt').read_text().strip() and not model['native_activation']
assert set(model['views'])=={'south','east','north','west'};color=np.frombuffer(bytes.fromhex('98875f'),dtype=np.uint8)
source_mask=rgba(Path(source['original']['private_mask']['path']));assert set(np.unique(source_mask[:,:,0][source_mask[:,:,3]>0]))=={255}
for facing,view in model['views'].items():
    master=rgba(ROOT/view['master']['path']);assert np.array_equal(master[:,:,0],master[:,:,1]) and np.array_equal(master[:,:,1],master[:,:,2])
    if facing!='west':
        original=rgba(ROOT/controls['views'][facing]['constructed']['path']);assert np.array_equal(master[:,:,3],original[:,:,3]);lum=original[:,:,:3].astype(float).mean(2);diff=np.abs(master[:,:,0].astype(float)-lum);assert diff[original[:,:,3]>0].max()<=3.6
    else:
        for k,v in view.items():assert np.array_equal(np.array(Image.open(ROOT/v['path'])),np.array(Image.open(ROOT/model['views']['east'][k]['path']))[:,::-1])
    assert not master[:480,:,3].any(),'Retained upper cell must be empty, not a baked flame.'
    primary=rgba(ROOT/view['primary']['path']);detail=rgba(ROOT/view['detail']['path']);assert not primary.any() and detail.shape==(256,256,4)
    assert np.array_equal(detail[:,:,0],detail[:,:,1]) and np.array_equal(detail[:,:,1],detail[:,:,2])
    expected=np.array(Image.fromarray(master).resize((256,256),Image.Resampling.LANCZOS));expected[:,:,:3]=np.uint8(np.rint(expected[:,:,:3].astype(float).mean(2)))[:,:,None];expected[expected[:,:,3]==0,:3]=0;assert np.array_equal(detail,expected)
    alpha=np.array(Image.open(ROOT/view['coverage']['path']).convert('L'));dc=np.array(Image.open(ROOT/view['detail_coverage']['path']).convert('L'));weight=np.array(Image.open(ROOT/view['detail_weight']['path']).convert('L'));dual=rgba(ROOT/view['authored_dualcolor_mask']['path']);assert np.array_equal(alpha,detail[:,:,3]) and np.array_equal(alpha,dc) and np.array_equal(dual[:,:,3],alpha) and np.array_equal(dual[:,:,0],weight)
    assert np.all(weight[alpha>0]==255)
    rgb=np.uint8(np.rint(detail[:,:,:3].astype(float).mean(2)[:,:,None]/255*color));rgb[alpha==0]=0;assert np.array_equal(np.dstack([rgb,alpha]),rgba(ROOT/view['native_preview']['path']))
    # No primary contribution is possible for any native animated foreground value.
    for fg in ['d74200','cfc041','a64a2e']:
        w=weight.astype(float)/255;c=np.frombuffer(bytes.fromhex(fg),dtype=np.uint8);mixed=(1-w[:,:,None])*c+w[:,:,None]*color;assert np.array_equal(mixed[alpha>0],np.broadcast_to(color,mixed.shape)[alpha>0])
now=datetime.now(timezone.utc).isoformat()
reason=('Reviewed exact Torchpost/MountedFurniture ancestry, description, flame-free source mask and actual Core WallTorch S/E/N reference/source render mapping. Source holder occupies only lower cell bbox(4,16)-(12,21); every opaque source pixel is detail w. '
    'Read installed AnimatedMaterialFire and RenderEvent.ApplyColors: native foreground changes R/W/r/W with priority30, leaving detail unchanged. Read PrefabImposter/BasePrefabImposter: separate TorchpostFlames native prefab/origin/visibility and LightSource Lit=true Radius6 remain owned by the game. No baked flame, primary-coloured static body, new particle art/clock, fuel/heat or donor wall offset imported. Unlit Torchpost is a separate blueprint, not a new toggle/converted identity. '
    'Editable shared physical construction retains broad rim, short stem and flanking supports with wood/iron materials. Source does not measure hidden depth/back/brace arrangement: width7.5/depth3.2/rim thickness.30/stem1.7x1.2x2.5/strut.32 and14degree camera are recorded authored dimensions, carried into exact refinement prompt. '
    'Initial strut ends lay inside the opening; revised ends join the rim volume. A remaining floating-cap appearance came from omitted inner/far rim walls; complete inner/outer faces now provide connected volume/occlusion. Initial and intermediate geometry retained. Corrections preceded actual refinement; final S/E/N share dimensions/cell pivot, no independent profile compression or stretched finished side. '
    'One real three-view holder-only ImageGen proposal retained. Open gaps, short stem and supports remain coherent, with no fire. Generated contours/alpha, shinier broad lighting and slight warm wood chroma are excluded. Inspected opaque unmarked wood/iron interiors supply bounded neutral high-frequency material residue through canonical ownership; no second isolation or invented retry. '
    'Exact selected master alpha and upper empty cell/native placement retained. Both material regions remain native detail w, not separate new palette channels. Every neutral RGB channel agrees; primaryRGBA empty, detail coverage equals object alpha, detail weight255 wherever covered. Static body tint is identical for R/W/r foreground examples. Source/native intended-size and full-cell plates reviewed. W mirrors symmetric E. '
    'All furniture views are authored, extras remain unbound. Authoring crop is explicit(0,480,1536,720); production512x768/256square mapping keeps full16x24cell. Clothing integration inapplicable. Native exact tile, particle anchoring/visibility, radius/foreground/detail interaction and cell acceptance stay pending until all pending generation is done.')
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Torchpost static-holder art authoring only; native fire/light ownership retained',reason=reason,verified_source_files=len(verified),actual_imagegen_calls=1,
    checks=dict(source_holder_only=True,all_native_pixels_detail=True,actual_directional_core_reference=True,shared_furniture_depth=True,solid_support_contact_correction=True,complete_rim_face_correction=True,one_actual_refinement=True,no_baked_flame=True,native_prefab_owner_retained=True,no_new_animation_clock=True,canonical_master_alpha_exact=True,upper_cell_transparent=True,neutral_equal_RGB=True,primary_empty=True,detail_full_coverage=True,foreground_does_not_recolor_holder=True,native_w_exact=True,west_mirror_exact=True,intended_size_reviewed=True,clothing_not_applicable=True,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
def event(step,action,ins,outs,review,result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result))
event(entry['required_steps'][2],'Review retained contact and rim-volume corrections in the manual three-view construction.',['manual-suggestion.png','construction-v2/manual-suggestion.png'],['construction-v3/manual-suggestion.png','construction-v3/construction-controls.json','construction-v3/construct-holder.py'],'First endpoint correction puts strut centres inside rim volume; complete inner/outer faces resolve far-cap occlusion. Both prior variants retained. Final source-cell pivot, width/depth/camera stay shared; no side-image stretching or changed native particle origin.')
event(entry['required_steps'][4],'Run actual holder-only three-view material refinement from corrected construction and source/Core plate.',['construction-v3/refinement-prompt.txt','construction-v3/refinement-target.png','source-reference.png'],['refined-raw.png','generation-receipt.json','first-structural-review.json'],'Three coherent short wood/iron holders, no flame added. Structural proposal usable as surface reference; selected geometry and alpha remain canonical. Exclude heavier borders/illumination and warm chroma before native detail-only tint registration.')
event(entry['required_steps'][5],'Register neutral wood/iron surfaces on fixed full-cell geometry and source detail-only w contract.',['construction-v3/construction-controls.json','refined-raw.png','source-packet.json'],['register-holder.py','material-selection.json','selected-material-specimens.png','registered/model.json','registered/registration-decisions.json','registered/detail-coverage-turnarounds.png'],'Selected opaque interiors supply bounded grayscale residue only. Master coverage exact, upper cell empty. Primary texture empty; detail coverage full and weight255. Native foreground animation, separate particle fire and radius6 unchanged. Crop is presentation-only.')
event(entry['required_steps'][6],'Inspect all directional, neutral/native and intended-size/source-palette evidence.',['registered/model.json'],['registered/neutral-turnarounds.png','registered/native-w-turnarounds.png','registered/full-cell-turnarounds.png','registered/source-native-scale-and-palette.png','record-review.py','registered/authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][7],'Retain native prefab alignment/visibility, lighting/palette, exact cell mapping and supported facing acceptance for integrated set.',['registered/model.json'],[],'No game launch, native activation, lighting/animation test, placement logic or harness. Native acceptance requires the full-ledger generation gate first.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-turnarounds.png')),registration_summary='Torchpost: source holder-only detail w, native flame/palette/light ownership resolved; actual Core S/E/N reference, shared-depth wood/iron construction with contact and rim-face corrections, one real refinement and neutral detail-only registration. Full source padding retained; extra views unbound. Native acceptance pending.',art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
following=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'));assert following['id']=='BODY-GLOWFISH';following.update(status='IN PROGRESS',current_step=following['required_steps'][0]);ledger.update(active_entry=following['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1;write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_files=len(verified),native_acceptance='pending')))
