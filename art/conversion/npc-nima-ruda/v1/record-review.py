"""Record Nima's inspected five-item static assembly; native state review remains gated."""
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
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='NPC-NIMA-RUDA'
entry=next(e for e in ledger['entries'] if e['id']=='NPC-NIMA-RUDA')
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
expected={'Leather Apron':(529,176,'Body',0),'Wide-brimmed Hat':(530,177,'Head',0),'Pestle':(531,181,'Hand',6),'Sandals':(536,192,'Feet',0),'Floating Glowsphere':(538,195,'Floating Nearby',0)}
assert {name:(b['equipped_instance'],b['part_id'],b['slot'],b['laterality']) for name,b in model['equipment_bindings'].items()}==expected
assert model['registration']['canvas']==[512,1264] and model['registration']['contact']==[256,1190]
assert not model['native_activation'] and not packet['native_activation']
body=read(ROOT/model['body_model']['path'])
for f,view in model['views'].items():
    assert view['body']==body['views'][f]
    canvas=Image.new('RGBA',(512,1264))
    for r in view['body']:canvas.alpha_composite(Image.open(ROOT/r['public_file']).convert('RGBA'))
    assert np.array_equal(np.array(canvas),arr(HERE/f'base-{f}.png'))
    for b in view['equipment']:
        for r in b['components']:
            a=Image.open(ROOT/r['public_file']).convert('RGBA');original=Image.open(ROOT/r['source_component']['path']).convert('RGBA')
            if r['mirrored_from_east']:original=ImageOps.mirror(original)
            assert np.array_equal(np.array(a)[240:],np.array(original)) and not np.array(a)[:240].any()
            assert r['size']==[512,1264] and r['contact']==[256,1190]
            oldheight=r['height']*1024/1264;oldcenter=r['center_z']-120*oldheight/1024
            assert abs((r['center_z']+(632-1190)*r['height']/1264)-(oldcenter+(512-950)*oldheight/1024))<1e-12
    neutral=arr(HERE/f'full-neutral-{f}.png');assert np.array_equal(neutral[:,:,0],neutral[:,:,1]) and np.array_equal(neutral[:,:,1],neutral[:,:,2])
    assert not arr(HERE/f'hidden-{f}.png')[:,:,3].any()

decision=read(HERE/'hand-attachment-decision.json');floating=read(HERE/'floating-attachment-decision.json')
assert (decision['captured_part'],decision['laterality'],decision['captured_item'])==(181,6,531)
assert (floating['captured_part'],floating['slot'],floating['captured_item'])==(195,'Floating Nearby',538)
assert not floating['optional_effects_registered_native']
assert body['views']['west']!=body['views']['east']
for rows in body['views'].values():
    assert all(r['color_role']=='detail' for r in rows if r['component'].startswith('mutation-tail'))
    assert all(r['color_role']=='foreground' for r in rows if not r['component'].startswith('mutation-tail'))
now=datetime.now(timezone.utc).isoformat()
write(HERE/'historical-instruction-versions.json',dict(verified=historical,rule='Original dependency events stay unchanged; exact historical instruction bytes resolve in Git.'))
reason=('Inspected original Qud sprite, metadata, separate body/mutation art, all five single-item plates, staged assembly and all four neutral/native/intended-size views. '
        'Apron529 Body176, Hat530 Head177, Pestle531 Hand181/6, Sandals536 Feet192 and Glowsphere538 FloatingNearby195 match the captured outfit. '
        'Original body and item pixels remain unchanged; integer240px transparent padding preserves common scale, contact and masks. '
        'Apron straps/bib/hem, hat crown/brim, ordinary-palm pestle, ankle/instep sandal straps and floating sphere were reviewed against the separate extra arms and spiral tail. '
        'Tail roots may be occluded by worn gear, while complete tail geometry remains separate. West tail is explicitly projected, not mirrored from east. '
        'Every garment applies only its own late body ownership; no global body redraw over other equipment. '
        'Neutral layers remain gray; source g body/additional arms and w tail role remain separate from w/W apron, y/b hat, y/Y pestle, y/w sandals and Y/C sphere. '
        'The g/w split is the recorded art palette interpretation, not native per-limb colour metadata. '
        'Pestle Hand181/6 is retained as a static palm association. FloatingNearby195/0 remains the actual sphere slot despite its vertical-palm display alignment. '
        'Optional halo is not registered; native light and animated colour cycle remain native and untested. Jade eyes/scars remain postponed cosmetics. '
        'No new ImageGen call, baked costume, source body deformation, mutation framework or native acceptance; held states and lifecycle remain gated.')
write(HERE/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete captured five-item static authoring assembly only',reason=reason,checked_dependency_files=len(verified),
    checks=dict(exact_five_equipped_instances_and_parts=True,current_separate_anatomy_reused=True,all_four_cardinal_views=True,all_single_item_views_reviewed=True,source_pixels_unchanged=True,
    padding_preserves_world_frame=True,per_item_late_ownership=True,neutral_equal_RGB=True,independent_captured_palettes=True,tail_detail_role=True,explicit_west_tail=True,
    hand181_6_not_renamed=True,floating195_not_hand_weapon=True,optional_halo_unbound=True,authored_static_anchor_disclosed=True,hidden_preview_empty=True,new_imagegen_calls=0,native_activation=False),native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))

def event(step,action,ins,outs,review,result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result))
event(entry['required_steps'][0],'Reconcile actor506 anatomy, source palette and five equipped items after the separate mutation-art prerequisite was generated.',[],['assembly-source-packet.json','render-source-comparison.py','source-to-assembly.png'],'Original preflight remains historical. Current packet uses separate BODY-NIMA anatomy and exact actual parts; cosmetic detail remains postponed.')
event(entry['required_steps'][1],'Verify six current dependencies and retain all actual source/reference/manual/refinement/secondary/patch/extraction histories.',['assembly-source-packet.json'],['dependency-lineage.json','dependency-evidence.html','historical-instruction-versions.json'],'Current model/component hashes verified; older instruction inputs resolve to exact Git bytes. No new generation call.')
event(entry['required_steps'][2],'Assemble five source items with fixed separate body/mutation textures and integer-padded original fittings.',['assembly-source-packet.json','dependency-lineage.json'],['assemble-nima.py','model.json','hand-attachment-decision.json','floating-attachment-decision.json','assembly-stages.png'],'Exact RGBA source pixels, common physical scale/contact and actual slot identities retained. Each late mask affects its own item. Tail detail role and explicit west geometry preserved; optional halo not bound.')
event(entry['required_steps'][3],'Review every item independently on the unclothed named body, then the complete outfit in each facing.',['model.json'],['leather-apron-comparison.png','wide-brimmed-hat-comparison.png','pestle-comparison.png','sandals-comparison.png','floating-glowsphere-comparison.png','full-neutral-comparison.png'],'Apron/hat/sandal coverage, ordinary-palm tool, floating display and extra-arm/tail overlap inspected. Complete item/body pixels remain independently registered; no unrelated body redraw.')
event(entry['required_steps'][4],'Review independent source palettes, shared registration and intended-size static assembly.',['model.json'],['full-native-comparison.png','game-scale-comparison.png','hidden-comparison.png','record-review.py','authoring-review.json','artifact-manifest.json'],reason)
event(entry['required_steps'][5],'Retain integrated native anatomy/equipment/held-state/visibility/hurt/look/save review behind all-generation gate.',['model.json'],[],'Hidden authoring previews are empty. Real mutation/gear occlusion, equip/unequip, held states, native light/colour cycle and lifecycle remain untested. Entry remains UNFINISHED.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'full-neutral-comparison.png')),
    registration_summary='Captured Nima506: separate shared female body, additional arms and one spiral tail, plus Apron, Hat, Pestle, Sandals and Floating Glowsphere. Exact source pixels and world frame retained; Hand181/6 and FloatingNearby195/0 stay distinct. Static authoring only; native acceptance pending.',art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')))
entry['resolved_advancement_blocker']=dict(**entry.pop('advancement_blocker'),status='RESOLVED FOR GENERATION',evidence=[ref(HERE/'model.json'),ref(HERE/'hand-attachment-decision.json'),ref(HERE/'floating-attachment-decision.json')])
entry['apparel_dependencies']['status']='Current apron, hat and sandals generation-ready; exact padded source pixels reviewed on separate named anatomy. Native outfit acceptance pending.'
next_entry=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'));assert next_entry['id']=='NPC-TAM'
next_entry.update(status='IN PROGRESS',current_step=next_entry['required_steps'][0]);ledger.update(active_entry=next_entry['id'],updated_at=now)
assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_dependency_files=len(verified),native_acceptance='pending')))
