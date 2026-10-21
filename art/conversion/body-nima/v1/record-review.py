"""Close only source-bound Nima anatomy authoring and resume her actual outfit."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
assert not (OUT/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='BODY-NIMA' and ledger['stage']=='Stage 3 ACTIVE'
model=read(OUT/'model.json');packet=read(HERE/'source-packet.json');body=read(ROOT/packet['baseline']['path']);geometry=read(HERE/'tail-construction-v2.json')
parts=packet['captured_actor']['parts'];assert len([p for p in parts if p['type']=='Arm'])==4 and len([p for p in parts if p['type']=='Hand'])==4
assert len([p for p in parts if p['type']=='Head'])==1 and len([p for p in parts if p['type']=='Tail'])==1
tail=next(p for p in parts if p['type']=='Tail');assert (tail['id'],tail['parent'],tail['manager'])==(193,176,'506::Stinger')
assert np.array(geometry['centreline']).shape==(25,3) and np.array(geometry['stinger']).shape==(6,3) and np.array(geometry['bead']).shape==(3,)
verified=set()
def walk(v):
    if isinstance(v,dict):
        key='path' if 'path' in v else ('public_file' if 'public_file' in v else None)
        if key and 'sha256' in v:
            p=Path(v[key]);p=p if p.is_absolute() else ROOT/p;assert hashlib.sha256(p.read_bytes()).hexdigest()==v['sha256'],str(p);verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
walk(model);walk(packet)
assert not model['native_activation'] and not packet['native_activation']
for facing,rows in model['views'].items():
    source='east' if facing=='west' else facing
    for component in ['body','head']:
        r=next(r for r in rows if r['component']==component);old=next(r for r in body['views'][source] if r['component']==component)
        im=Image.open(ROOT/old['public_file']).convert('RGBA');im=ImageOps.mirror(im) if facing=='west' else im
        expected=Image.new('RGBA',(512,1264));expected.paste(im,(0,240));assert np.array_equal(np.array(expected),rgba(ROOT/r['public_file']))
        oldground=old['center_z']+(512-950)*old['height']/1024;newground=r['center_z']+(632-1190)*r['height']/1264
        assert abs(newground-oldground)<1e-12 and abs(newground)<1e-12
        assert r['width']==old['width'] and abs(r['height']/1264-old['height']/1024)<1e-12
    for r in rows:
        a=rgba(ROOT/r['public_file']);assert a.shape==(1264,512,4) and r['contact']==[256,1190]
        assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2])
        assert not a[0,:,3].any() and not a[-1,:,3].any() and not a[:,0,3].any() and not a[:,-1,3].any()
        if r['component'].startswith('mutation-tail'):
            assert r['native_part']==193 and r['render_instance']=='one-tail-193' and r['color_role']=='detail' and not r['mirrored_from_east']
        elif r['component']=='mutation-extra-arms':assert r['native_parts']==[184,185,186,187]
    assert len([r for r in rows if r['component'].startswith('mutation-tail')])==2
    assert len([r for r in rows if r['component']=='mutation-extra-arms'])==1
    for mode in ['neutral','native']:
        canvas=Image.new('RGBA',(512,1264));palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette']
        for r in rows:
            im=Image.open(ROOT/r['public_file']).convert('RGBA')
            if mode=='native':
                a=np.array(im);color=np.frombuffer(bytes.fromhex(palette['w' if r['color_role']=='detail' else 'g']),dtype=np.uint8)
                a[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float).mean(2)[:,:,None]*color/255));a[a[:,:,3]==0,:3]=0;im=Image.fromarray(a)
            canvas.alpha_composite(im)
        assert np.array_equal(np.array(canvas),rgba(OUT/f'{mode}-{facing}.png'))
now=datetime.now(timezone.utc).isoformat()
reason=('Inspected original g/w shape and full description/tree, actual Core female and Megafauna Pulmonoscorpius references, original and corrected manual views, both actual ImageGen outputs, sole-tail topology evidence, final separate components and all four neutral/native/intended-size views. '
        'Exactly four arms/hands, two ordinary feet, one ordinary blank head and one posterior Tail193 with a segmented inward spiral, one hooked endpoint and one bead. Surface24segments and numerical dimensions are authored, not native body-part counts. '
        'Initial zigzag helix, profile overlap defect and generated duplicate north stinger were corrected and retained in history. Second refinement corrects the duplicate but redraws the ordinary body, so only usable surface values are retained. '
        'Original female body/head RGBA pixels remain exact under240px top padding; physical scale and ground/contact are unchanged. Extra arm pair and tail front/back are separate from the reusable body. '
        'All views use one canonical3Dtail; west tail is explicitly projected, while symmetric base/arm profile may mirror. Profile body/near arm occludes the midline tail root. '
        'Neutral RGB is gray. Source g body/arms and w spiral appearance roles are explicit interpretations of original Render appearance, not biological pigment claims. No unproven natural-stinger color is imported. '
        'No clothing, personal jade-eye/scar cosmetics, generic mutation framework, new demographic/occupation pose, AI isolation or native activation. Actual five-item Nima outfit and final anatomy/equipment/visibility/hurt/look/save/state acceptance remain unfinished.')
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete separate Nima anatomy generation only',reason=reason,checks=dict(source_four_arms_and_hands=True,one_head_and_one_tail=True,one_stinger_endpoint_and_bead=True,unchanged_source_body_RGBA=True,
    unchanged_world_scale_and_ground=True,all_four_cardinal_views=True,explicit_asymmetric_west_tail=True,neutral_equal_RGB=True,no_canvas_clipping=True,source_palette_roles_explicit=True,separate_mutation_textures=True,native_activation=False),checked_source_files=len(verified),new_imagegen_calls=2,second_isolation_call=False,native_acceptance=model['native_acceptance']))
write(HERE/'generation-receipts.json',dict(tool='image_gen.imagegen',calls=[
    dict(prompt=ref(HERE/'secondary-views-prompt.txt'),inputs=[ref(HERE/'corrected-construction-turnaround.png'),ref(HERE/'source-reference-construction.png')],output=ref(HERE/'secondary-views-raw.png'),default_original='C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-232c05a6-733c-4c5c-b8d1-7c3906b88664.png',transparent_background=True),
    dict(prompt=ref(HERE/'composed-refinement-prompt.txt'),inputs=[ref(HERE/'patched-refined-turnaround.png'),ref(HERE/'tail-topology-evidence.png')],output=ref(HERE/'composed-refinement-raw.png'),default_original='C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-509f1338-c98c-4754-993e-558e7631bb27.png',transparent_background=True)]))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json' and '__pycache__' not in p.parts]))
entry=next(e for e in ledger['entries'] if e['id']=='BODY-NIMA')
def event(step,action,ins,outs,review,result='PASS',**extra):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result,**extra))
event(entry['required_steps'][4],'Receive composed refinement and inspect corrected one-tail topology; reject redrawn base pixels.',['composed-refinement-prompt.txt','patched-refined-turnaround.png','tail-topology-evidence.png'],['composed-refinement-raw.png','composed-structural-review.json','generation-receipts.json'],'Second actual output has one inner hooked stinger/bead instead of the first duplicate. Ordinary body/head/legs are still redrawn, so return to exact original body and canonical geometry; only usable surface finish retained. No further prompt loop or isolation.',tool='image_gen.imagegen',prompt_file=ref(HERE/'composed-refinement-prompt.txt'),transparent_background=True)
event(entry['required_steps'][5],'Register unchanged source body/head and separate extra-arm/spiral-tail layers with explicit four-view projection and source color roles.',['source-packet.json','tail-construction-v2.json','source-palette-roles.json','composed-refinement-raw.png'],['tail_geometry_four_views.py','register-nima.py','registered/model.json','registered/registration-decisions.json','registered/neutral-comparison.png','registered/native-comparison.png'],'Exact RGBA padding preserves world frame/ground. One Tail193 uses near/far draw-order pieces; no duplicated appendage. West tail is an explicit canonical projection because the diagonal spiral is asymmetric. Body/arms use source g, tail uses source w as stated appearance interpretation; neutral RGB remains gray.')
event(entry['required_steps'][6],'Review actual all-direction anatomy, final palette/registration and intended-size evidence.',['registered/model.json'],['record-review.py','registered/authoring-review.json','registered/game-scale-comparison.png','artifact-manifest.json'],reason)
event(entry['required_steps'][7],'Keep native named anatomy and five-item outfit acceptance behind full-generation gate.',['registered/model.json'],[],'No game launch, native/harness test or activation. Actual Pestle Hand181/6 and Glowsphere FloatingNearby195/0, all-item occlusion and integrated anatomy/equipment/state/visibility/hurt/look/save review remain required.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-comparison.png')),
    registration_summary='Unchanged shared female body plus separate additional arm pair and one segmented spiral Tail193. All four tail views use the same world geometry, including an explicit west projection. Body ground/physical scale are unchanged by top padding; source palette roles and authored interpretation are recorded. Nima outfit and native acceptance remain pending.',art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
npc=next(e for e in ledger['entries'] if e['id']=='NPC-NIMA-RUDA');assert npc['status']=='UNFINISHED'
npc.update(status='IN PROGRESS',current_step=npc['required_steps'][1],known_issues=['Separate BODY-NIMA anatomy is generation-ready. Assemble all five actual fittings in the same padded world frame, respect tail detail-w role and explicit west geometry, and review item/tail/arm occlusion and exact Hand181/6 versus FloatingNearby195/0 attachments.'])
npc['advancement_blocker'].update(reason=npc['known_issues'][0],resolution='Finish the source-bound five-item named assembly without baking gear or changing actual captured slots; keep native state acceptance behind full-generation gate.')
ledger.update(active_entry=npc['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_source_files=len(verified),native_acceptance='pending')))
