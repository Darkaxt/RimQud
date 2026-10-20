"""Record inspected Argyve generation evidence and advance exactly one ledger entry."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, subprocess
import numpy as np
from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(), sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p, data): p.write_bytes((json.dumps(data, indent=2, ensure_ascii=False)+'\n').encode())
def image(p): return np.array(Image.open(p).convert('RGBA'))

assert not (HERE/'authoring-review.json').exists()
ledger = read(ROOT/'evidence/conversion-ledger.json')
assert ledger['active_entry']=='NPC-ARGYVE' and ledger['stage']=='Stage 3 ACTIVE'
entry = next(e for e in ledger['entries'] if e['id']=='NPC-ARGYVE')
assert not entry['process_log']
packet, model, lineage = [read(HERE/n) for n in ['source-packet.json','model.json','dependency-lineage.json']]
verified = set()
historical_versions = []
historical_instruction_hashes = {
    ('skills/qud-creature-conversion/SKILL.md', '74d6f7498dad0e0079c152649b2b40143cbf201a748b48d0a5cd110a73975af2'),
    ('skills/qud-creature-conversion/references/apparel-fitting.md', '3549a1e4702f4b24dfcea5238880d092ef84a5809bd07bdcb6ececbf601f1f13'),
}
def check_refs(v):
    if isinstance(v, dict):
        key = 'path' if 'path' in v else ('public_file' if 'public_file' in v else None)
        if key and 'sha256' in v:
            p=Path(v[key]);p=p if p.is_absolute() else ROOT/p
            actual=hashlib.sha256(p.read_bytes()).hexdigest()
            if actual!=v['sha256']:
                relative=p.relative_to(ROOT).as_posix()
                assert (relative,v['sha256']) in historical_instruction_hashes, str(p)
                commit='dde9ca991c35ddef2b47a970a571d696ee0443bb'
                raw=subprocess.check_output(['git','show',commit+':'+relative],cwd=ROOT)
                assert hashlib.sha256(raw).hexdigest()==v['sha256']
                record=dict(path=relative,sha256=v['sha256'],commit=commit,current_sha256=actual,
                            url='https://github.com/Darkaxt/RimQud/blob/'+commit+'/'+relative,
                            reason='Historical dependency process input; current instructions have since changed. Original event remains unchanged.')
                if record not in historical_versions: historical_versions.append(record)
            verified.add(str(p))
        for x in v.values(): check_refs(x)
    elif isinstance(v,list):
        for x in v: check_refs(x)
for v in [packet, model, lineage]: check_refs(v)
assert not model['native_activation'] and not packet['native_activation']
assert set(model['views'])=={'south','east','north','west'}
expected={'Pocketed Vest':(518,315,'Body',0),'Telescopic Monocle':(587,317,'Face',0),'Steel Utility Knife':(588,320,'Hand',2),'Wrench':(590,322,'Hand',1),'Sandals':(521,326,'Feet',0)}
assert len(packet['equipped'])==5
assert {e['item']['blueprint']:(e['item']['instance'],e['part_id'],e['slot'],e['laterality']) for e in packet['equipped']}==expected
assert len(lineage['dependencies'])==6
body = read(ROOT/model['body_model']['path'])
frame_keys=['width','height','center_x','center_z','size','contact']
frame={k:body['views']['south'][0][k] for k in frame_keys}
for dep in lineage['dependencies']:
    source=next(e for e in ledger['entries'] if e['id']==dep['entry'])
    assert source['generation_ready'] and source['current_registration']['model']==dep['model']
    assert dep['new_imagegen_calls']==0
    for rows in read(ROOT/dep['model']['path'])['views'].values():
        for r in rows: assert {k:r[k] for k in frame_keys}==frame
for f,view in model['views'].items():
    neutral=image(HERE/f'full-neutral-{f}.png')
    assert neutral.shape==(1024,512,4)
    assert np.array_equal(neutral[:,:,0],neutral[:,:,1]) and np.array_equal(neutral[:,:,1],neutral[:,:,2])
    assert not image(HERE/f'hidden-{f}.png')[:,:,3].any()
    assert len(view['equipment'])==5
    monocle=next(e for e in view['equipment'] if e['blueprint']=='Telescopic Monocle')
    assert not monocle['mirrored_from_east']
    wrench=next(e for e in view['equipment'] if e['blueprint']=='Wrench')
    assert wrench['primary_palette']=='&y' and wrench['detail_palette']=='c'
    for b in view['equipment']:
        assert b['late_body_ownership']['component']=='body-overlay'
    # Original body/head assembly remains exactly the dependency in every facing.
    body_image=Image.new('RGBA',(512,1024))
    from PIL import ImageOps
    for row in body['views']['east' if f=='west' else f]:
        im=Image.open(ROOT/row['public_file']).convert('RGBA')
        body_image.alpha_composite(ImageOps.mirror(im) if f=='west' else im)
    assert np.array_equal(np.array(body_image),image(HERE/f'base-{f}.png'))

now=datetime.now(timezone.utc).isoformat()
write(HERE/'historical-instruction-versions.json',dict(verified=historical_versions))
reason=('Inspected original source, shared body, five actual fitted items, staged outfit, all four neutral/native directions and intended-size views. '
        'Actor519 is captured human/male with ordinary attached Humanoid tree; no age or eyebrow mutation invented. '
        'Original body/head, canvas512x1024, contact256,950 and all item physical mappings/pixels retained. '
        'Vest, monocle, sandals, knife Hand/2 and wrench Hand/1 remain independent; explicit monocle west is used. '
        'Far-hand source depths and per-item late body ownership avoid a whole-body overlay erasing other gear. '
        'Actual body c and independent item palettes are used, including wrench TileColor y overriding foreground c. '
        'Hair/beard/eyes/personal overlays remain postponed under A4. Held-item previews are stationary displays; ready/resting grip/angle/depth review is assigned to integrated Stage3 after generation. '
        'No native activation, game launch, harness acceptance or new ImageGen call. Crowded initial scale evidence retained and replaced by separated rows; art unchanged.')
write(HERE/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete NPC assembly generation authoring only',reason=reason,
    checked_dependency_files=len(verified),checks=dict(actual_five_equipped_part_bindings=True,all_four_cardinal_views=True,unchanged_body_and_item_source_hashes=True,
    shared_physical_frame_and_contact=True,neutral_equal_RGB=True,explicit_monocle_west=True,independent_captured_palettes=True,wrench_tile_color_override=True,
    per_item_late_ownership_not_global_body_redraw=True,hidden_preview_empty=True,new_imagegen_calls=0,native_activation=False),
    report_correction=dict(rejected=ref(HERE/'game-scale-comparison.png'),selected=ref(HERE/'game-scale-review.png'),reason='Original report rows overlap; separated row layout without changing the art.'),
    native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))

def event(step, action, inputs, outputs, review, result='PASS'):
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in inputs],outputs=[ref(HERE/n) for n in outputs],review=review,result=result))
event(entry['required_steps'][0], 'Resolve captured Argyve519 to the shared unmutated human male family and exact five equipped instances/parts.', [],
      ['source-packet.json','source-to-assembly.png'], 'Native description/ancestry, original mask hash, source snapshot and attached parts retained. Personal beard/eyebrow metadata kept under postponed A4 cosmetics; no inferred age, mutation or profession pose.')
event(entry['required_steps'][1], 'Verify current shared body and each of the five current item registrations and retain their complete earlier conversion history.', ['source-packet.json'],
      ['dependency-lineage.json','dependency-evidence.html','historical-instruction-versions.json'], 'Six generation-ready dependencies match exact current model/component hashes and physical mapping. Two old instruction inputs resolve byte-for-byte to Git dde9ca9; original events are unchanged. Linked original/reference/manual/refinement/patch/extraction/fitting records are reused, not invented NPC-specific generation calls.')
event(entry['required_steps'][2], 'Compose body, vest, monocle, sandals and both captured hand items without baking equipment into the body.', ['source-packet.json','dependency-lineage.json'],
      ['assemble-argyve.py','model.json','base-comparison.png','worn-comparison.png','assembly-stages.png'], 'Original body/item pixels unchanged. Per-item late ownership is applied only to its own cloth/tool coverage; source far-hand depths retained. Stationary display only, no accepted native weapon state.')
event(entry['required_steps'][3], 'Inspect all four facings, slot/laterality, explicit monocle west and fixed body/equipment registration.', ['model.json'],
      ['full-neutral-comparison.png','registration-comparison.png'], 'Shared frame/contact and source components verified. Full bodies remain cardinal; original visible arms/hands stay over the appropriate item without erasing unrelated equipment. No anatomical or fit correction required in this assembly.')
event(entry['required_steps'][4], 'Inspect independent captured palettes and game-size assembly; correct only the overlapping report layout.', ['model.json'],
      ['full-native-comparison.png','render-authoring-evidence.py','game-scale-comparison.png','game-scale-review.png','hidden-comparison.png','record-review.py','authoring-review.json','artifact-manifest.json'], reason)
event(entry['required_steps'][5], 'Retain native visibility/equipment/hurt/look/save and source-supported held-state review behind the complete generation gate.', ['model.json'], [],
      'Authoring hidden previews are empty; they do not prove native visibility. Native equip/unequip, near/far ordering, grip/ready/resting state, hurt, look and persistence remain pending integrated Stage3 after all156 entries are generated.', 'DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],
             current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'registration-comparison.png')),
             registration_summary='Captured Argyve519 assembled from the unchanged shared human-male body and five independent fitted items. Guides show the shared pivot/contact. Neutral, captured palettes, staged assembly and full dependency histories follow below. Cosmetics and native held-state acceptance remain explicitly pending under the specification.',
             art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')))
entry['apparel_dependencies']['status']='Current generation-ready vest, monocle and sandals verified; native outfit acceptance pending full-set gate.'
next_entry=next(e for e in ledger['entries'][ledger['entries'].index(entry)+1:] if not e.get('generation_ready'))
assert next_entry['id']=='NPC-ELDERBOB' and next_entry['status']=='UNFINISHED'
next_entry.update(status='IN PROGRESS',current_step=next_entry['required_steps'][0])
ledger.update(active_entry=next_entry['id'],updated_at=now)
assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_dependency_files=len(verified),native_acceptance='pending')))
