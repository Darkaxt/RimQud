"""Record Yrame's inspected four-item static assembly; native state review remains gated."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,subprocess
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def arr(p):return np.array(Image.open(p).convert('RGBA'))
assert not (HERE/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='NPC-WARDEN-YRAME'
entry=next(e for e in ledger['entries'] if e['id']=='NPC-WARDEN-YRAME')
model=read(HERE/'model.json');packet=read(HERE/'assembly-source-packet.json');lineage=read(HERE/'dependency-lineage.json')
verified=set();historical=[]
old={('skills/qud-creature-conversion/SKILL.md','74d6f7498dad0e0079c152649b2b40143cbf201a748b48d0a5cd110a73975af2'),('skills/qud-creature-conversion/references/apparel-fitting.md','3549a1e4702f4b24dfcea5238880d092ef84a5809bd07bdcb6ececbf601f1f13')}
def walk(v):
    if isinstance(v,dict):
        key='path' if 'path' in v else ('public_file' if 'public_file' in v else None)
        if key and 'sha256' in v:
            p=Path(v[key]);p=p if p.is_absolute() else ROOT/p;actual=hashlib.sha256(p.read_bytes()).hexdigest()
            if actual!=v['sha256']:
                rel=p.relative_to(ROOT).as_posix();assert (rel,v['sha256']) in old,(str(p),actual,v['sha256'])
                commit='dde9ca991c35ddef2b47a970a571d696ee0443bb';assert hashlib.sha256(subprocess.check_output(['git','show',commit+':'+rel],cwd=ROOT)).hexdigest()==v['sha256']
                record=dict(path=rel,sha256=v['sha256'],commit=commit,current_sha256=actual,url='https://github.com/Darkaxt/RimQud/blob/'+commit+'/'+rel)
                if record not in historical:historical.append(record)
            verified.add(str(p))
        for x in v.values():walk(x)
    elif isinstance(v,list):
        for x in v:walk(x)
for v in [model,packet,lineage]:walk(v)
expected={'Chain Mail':(574,287,'Body',0),'Horns':(575,288,'Head',0),'Vibro Blade':(576,292,'Hand',2),'Leather Boots':(580,297,'Feet',16)}
assert {n:(b['instance'],b['part_id'],b['slot'],b['laterality']) for n,b in model['equipment_bindings'].items()}==expected
assert model['registration']['canvas']==[512,1152] and model['registration']['contact']==[256,1078]
assert not model['native_activation'] and not packet['native_activation']
for f,view in model['views'].items():
    canvas=Image.new('RGBA',(512,1152))
    for r in view['body']:canvas.alpha_composite(Image.open(ROOT/r['public_file']).convert('RGBA'))
    assert np.array_equal(np.array(canvas),arr(HERE/f'base-{f}.png'))
    for r in view['body']+[r for b in view['equipment'] for r in b['components']]:
        a=arr(ROOT/r['public_file']);old=Image.open(ROOT/r['source_component']['path']).convert('RGBA');old=ImageOps.mirror(old) if r['mirrored_from_east'] else old;pad=r['padding_top']
        assert pad in [0,128] and np.array_equal(a[pad:],np.array(old)) and not a[:pad].any()
        assert r['size']==[512,1152] and r['contact']==[256,1078]
        sourceheight=r['height']*(1152-pad)/1152;sourcecenter=r['center_z']-pad/2*r['height']/1152
        assert abs((r['center_z']+(576-1078)*r['height']/1152)-(sourcecenter+((1152-pad)/2-(1078-pad))*sourceheight/(1152-pad)))<1e-12
    n=arr(HERE/f'full-neutral-{f}.png');assert np.array_equal(n[:,:,0],n[:,:,1]) and np.array_equal(n[:,:,1],n[:,:,2])
    assert not arr(HERE/f'hidden-{f}.png')[:,:,3].any()
    horns=next(b for b in view['equipment'] if b['name']=='Horns');assert all(r['padding_top']==0 for r in horns['components'])
    if f=='north':assert {r['component'] for r in horns['components']}=={'item-far','item-far-detail'}
    if f in ['east','west']:assert {r['component'] for r in horns['components']}=={'item-far','item-far-detail','item-near','item-near-detail'}
feet=[p for p in packet['captured_actor']['parts'] if p['type']=='Feet'];assert [(p['id'],p['equipped']['instance'] if p.get('equipped') else None) for p in feet]==[(297,580),(298,None)]
now=datetime.now(timezone.utc).isoformat()
write(HERE/'historical-instruction-versions.json',dict(verified=historical,rule='Original dependency events stay unchanged; these exact historical instruction bytes resolve in Git.'))
reason=('Inspected original glyph, full captured metadata, separate four-foot anatomy, all four single-item plates, assembly stages, complete neutral/native and intended-size views. '
        'Mail574 Body287, natural Horns575 Head288, Blade576 Hand292/2 and Boots580 changed Feet297/16 match the capture. Added Feet298/64 remains unequipped; no duplicate boots or invented frozen-hand garment. '
        'High-forehead horns retain existing near/far layers: north roots are behind the original head, profiles overlap naturally, south roots remain on forehead. No temple-root substitution or baked horn anatomy. '
        'Existing1152px horn canvas governs the assembly. Exact body/mail/blade/boots RGBA is copied at y+128 while existing horn pixels stay at y+0; physical pixel scale and ground/contact are unchanged. '
        'Mail cuffs/shoulders/hem, boots on the original pair, independent added bare feet, and static blade palm/depth reviewed in all facings. Each late mask affects only its own item; no original body redraw erases another piece. '
        'Neutral RGB remains gray. Body uses captured tileColor w; horns use w/W, mail y/Y, blade c/y and boots w/y independently. Source B detail and natural Icy Vapor metadata remain retained without an invented permanent-skin region or new particle effect. '
        'All five dependencies retain actual original/reference/manual/refinement/secondary/patch/extraction histories; no new ImageGen call or costume for this assembly. '
        'Static blade display is not ready/resting or native held-state acceptance. No mutation framework, game launch or native acceptance; those remain required after full generation.')
write(HERE/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete four-item static Yrame authoring assembly only',reason=reason,verified_dependency_files=len(verified),
    checks=dict(exact_four_equipped_instances_and_parts=True,current_separate_four_foot_body=True,boots297_only_no_duplicate298=True,natural_horns288_separate=True,horn_forehead_near_far_preserved=True,
    all_four_views_and_single_item_plates_reviewed=True,exact_RGBA_integer_padding=True,world_frame_preserved=True,per_item_late_ownership=True,neutral_equal_RGB=True,independent_palettes=True,
    source_B_and_IcyVapor_metadata_retained=True,hidden_preview_empty=True,new_imagegen_calls=0,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
def event(step,action,ins,outs,review,result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result))
event(entry['required_steps'][0],'Reconcile Yrame515 actual four-item capture after separate extra-leg generation.',['source-packet.json'],['assembly-source-packet.json','render-source-comparison.py','source-to-assembly.png'],'Original preflight retained. Two actual Feet groups remain distinct, Horns remains natural equipped Head288 item, Icy Vapor is native default Hands equipment rather than an additional worn glove.')
event(entry['required_steps'][1],'Verify all five current body/item dependencies and preserve their actual performed conversion histories.',['assembly-source-packet.json'],['dependency-lineage.json','dependency-evidence.html','historical-instruction-versions.json'],'Current models/components match; older instruction inputs resolve to exact Git bytes. Named body now generation-ready; no new generation call for outfit.')
event(entry['required_steps'][2],'Assemble exact separate source components in the existing horn-compatible1152px frame.',['assembly-source-packet.json','dependency-lineage.json'],['assemble-yrame.py','model.json','assembly-stages.png'],'Body/mail/blade/boots padded128px; horns unshifted. Near/far horn layers preserve forehead roots and body occlusion. Boots only on original changed Feet297; added pair remains bare. No rescale or global body overlay.')
event(entry['required_steps'][3],'Inspect every actual item separately on the unclothed named body and the complete outfit in all facings.',['model.json'],['chain-mail-comparison.png','horns-comparison.png','vibro-blade-comparison.png','leather-boots-comparison.png','full-neutral-comparison.png'],'Mail/arms, original booted feet versus bare added pair, forehead roots/near-far horns and static blade palm/depth visually reviewed. No new profession pose, mutation anatomy or baked gear.')
event(entry['required_steps'][4],'Inspect independent captured palettes, original registration and intended-size full assembly.',['model.json'],['full-native-comparison.png','game-scale-comparison.png','hidden-comparison.png','record-review.py','authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][5],'Retain native mutation/body/slot/equipment/visibility/held state/hurt/look/save and natural-effect acceptance behind full-generation gate.',['model.json'],[],'Authoring hidden preview is empty. Native Horns/Feet precedence, equip/unequip, supported held states and Icy Vapor effects remain untested; entry stays UNFINISHED.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'full-neutral-comparison.png')),
    registration_summary='Yrame515: separate four-foot body with actual mail, near/far forehead horns, static blade and boots on changed Feet297 only. Source pixels and world scale/contact preserved in horn-compatible frame; actual natural/equipped state retained. Native acceptance pending.',art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')))
entry['resolved_advancement_blocker']=dict(**entry.pop('advancement_blocker'),status='RESOLVED FOR GENERATION',evidence=[ref(HERE/'model.json'),ref(HERE/'authoring-review.json')])
entry['apparel_dependencies']['status']='Current mail and boots reviewed on separate named body. Boots580 only on Feet297/16; native outfit acceptance pending.'
following=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'));assert following['id']=='NPC-WATERVINEFARMERJOPPA-01'
following.update(status='IN PROGRESS',current_step=following['required_steps'][0]);ledger.update(active_entry=following['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_dependency_files=len(verified),native_acceptance='pending')))
