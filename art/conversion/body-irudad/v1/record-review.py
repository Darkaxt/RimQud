"""Close only Irudad anatomy generation; return the exact outstanding NPC assembly."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def array(p):return np.array(Image.open(p).convert('RGBA'))
assert not (OUT/'authoring-review.json').exists()
model=read(OUT/'model.json');packet=read(HERE/'source-packet.json');base=read(ROOT/packet['baseline']['path']);ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='BODY-IRUDAD'
parts=packet['native_parts'];assert len([p for p in parts if p['type']=='Arm'])==4 and len([p for p in parts if p['type']=='Hand'])==4
assert len([p for p in parts if p['type']=='Head'])==1 and len([p for p in parts if p['variant']=='Hands-Face'])==1 and len([p for p in parts if p['type']=='Tail'])==1
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
for f,rows in model['views'].items():
    source='east' if f=='west' else f
    for component in ['body','head']:
        row=next(r for r in rows if r['component']==component);original=next(r for r in base['views'][source] if r['component']==component)
        old=Image.open(ROOT/original['public_file']).convert('RGBA');expected=Image.new('RGBA',(512,1264));expected.alpha_composite(old,(0,240))
        if f=='west':expected=ImageOps.mirror(expected)
        assert np.array_equal(np.array(expected),array(ROOT/row['public_file']))
        old_ground=original['center_z']+(original['size'][1]/2-original['contact'][1])*original['height']/original['size'][1]
        new_ground=row['center_z']+(1264/2-row['contact'][1])*row['height']/1264
        assert abs(old_ground-new_ground)<1e-12 and abs(new_ground)<1e-12
        assert abs(original['height']/1024-row['height']/1264)<1e-12 and original['width']==row['width']
    for r in rows:
        a=array(ROOT/r['public_file']);assert a.shape==(1264,512,4);assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2])
        assert r['contact']==[256,1190]
        if r['component'] in ['mutation-raised-arms','mutation-tail']:
            part=r['component'].replace('mutation-','');p=HERE/('patched-tail-east.png' if part=='tail' and source=='east' else f'{part}-{source}.png')
            expected=Image.open(p).convert('RGBA')
            if f=='west':expected=ImageOps.mirror(expected)
            assert np.array_equal(a[:,:,3],np.array(expected)[:,:,3])
        if f=='west':
            east=next(x for x in model['views']['east'] if x['component']==r['component'])
            assert np.array_equal(a,np.array(ImageOps.mirror(Image.open(ROOT/east['public_file']).convert('RGBA'))))
    w=np.array(Image.open(OUT/f'hands-face-detail-weight-{f}.png'))
    face=array(OUT/f'hands-face-{f}.png');assert not w[face[:,:,3]==0].any()
    if f=='north':assert not w.any()
    else:assert w.any()
assert not model['native_activation'] and not packet['native_activation']
now=datetime.now(timezone.utc).isoformat()
reason=('Inspected source r/w glyph, native description/tree, actual Core human reference, shared older-human history, first and corrected manual views, both actual ImageGen outputs, restored base, separate final components and all four neutral/native/intended-size views. '
        'Four arms total, one ordinary head plus the mouthless interlaced-hands Face variant, two ordinary feet and one attached posterior barb-crowned tail. No rear eyes. '
        'Body/head pixel arrays are unchanged under240px transparent top padding; world pixel scale and ground remain exact. '
        'Both AI base redraws were rejected. First refined finger artwork and clean measured skin tones from the composed refinement are retained through explicit fixed coverage. '
        'Rejected striped UV continuation, repaired tail-root/depth proposal and misaligned first eye masks remain in history. Corrected detail masks follow actual enclosed white interiors. Manual ink green cast was neutralized on mutation pieces only; all final neutral RGB channels agree. '
        'Raised arms, hands-face and tail remain separate from the reusable older-human race template. No clothing, personal cosmetics, renderer/framework or native activation. '
        'Exact occupied Hand201/6 versus the neutral hands-face pose remains outstanding NPC-ELDERBOB authoring; native anatomy/equipment/visibility/hurt/look/save acceptance is pending the full-set gate.')
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete separate anatomy generation only; no NPC outfit or native acceptance',reason=reason,
    checks=dict(source_four_arms_and_hands=True,hands_face_not_extra_head=True,posterior_tail_with_barbs=True,body_and_head_pixels_unchanged=True,
    top_padding_preserves_world_scale_and_ground=True,separate_mutation_textures=True,all_four_cardinal_views=True,neutral_equal_RGB=True,actual_closed_eye_detail_masks=True,no_rear_eyes=True,native_activation=False),
    checked_source_files=len(verified),new_imagegen_calls=2,second_isolation_call=False,native_acceptance=model['native_acceptance']))
write(HERE/'generation-receipts.json',dict(tool='image_gen.imagegen',calls=[
    dict(prompt=ref(HERE/'secondary-views-prompt.txt'),inputs=[ref(HERE/'patched-construction-turnaround.png'),packet['donor_references'][0]],output=ref(HERE/'secondary-views-raw.png'),default_original='C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-d0e6c282-65c1-440a-8ce6-03fb839da89e.png',transparent_background=True),
    dict(prompt=ref(HERE/'composed-refinement-prompt.txt'),inputs=[ref(HERE/'corrected-composed-turnaround.png')],output=ref(HERE/'composed-refinement-raw.png'),default_original='C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-5efa157a-56e2-4b38-8a88-38ee034c54c1.png',transparent_background=True)]))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
entry=next(e for e in ledger['entries'] if e['id']=='BODY-IRUDAD')
def event(step,action,ins,outs,review,result='PASS',**extra):entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result,**extra))
event(entry['required_steps'][4],'Receive and inspect composed ImageGen refinement; retain usable skin finish while rejecting another base redraw.',['composed-refinement-prompt.txt','corrected-composed-turnaround.png'],['composed-refinement-raw.png','generation-receipts.json'],'Source count/orientation and mouthless joined hands remain usable. Generated body/foot proportions and alpha noise are rejected; no further prompt loop. Final art reuses the original body, first refined finger detail and clean skin levels from this composed output.',tool='image_gen.imagegen',prompt_file=ref(HERE/'composed-refinement-prompt.txt'),transparent_background=True)
event(entry['required_steps'][5],'Register independent mutation pieces and exact integer-padded original body/head in a shared physical frame.',['source-packet.json','composed-refinement-raw.png'],['register-irudad.py','registered/model.json','registered/registration-decisions.json','registered/neutral-comparison.png'],'Canvas512x1264/contact256,1190 extends upward by240px. Explicit height/center adjustment preserves the old body world position, scale and ground exactly. Posterior tail depth varies by facing. No mutation is baked into the reusable older-human model or converted to a render bone.')
event(entry['required_steps'][5],'Replace estimated eye-detail ellipses with actual refined closed eye interiors.',['registered/model.json'],['patch-eye-masks.py','eye-mask-misalignment.png','eye-mask-correction.json','registered/native-comparison.png'],'First native authoring view exposed partial eye-detail masks. Select the reviewed enclosed white interiors by their actual dark rims; no north mask, west mirrors east. Neutral artwork and all geometry/body pixels unchanged.')
event(entry['required_steps'][5],'Remove the manual mutation ink green cast and recompose the current registered reports.',['registered/model.json'],['neutralize-and-render.py','neutral-ink-correction.json','registered/neutral-comparison.png','registered/native-comparison.png'],'Authoring inspection found #292e2b source SVG ink retained slightly unequal RGB. Mutation-only grayscale preserves its luminance and alpha; original body/head pixels unchanged. Final neutral components and all neutral/source-palette previews now derive from the exact current model.')
event(entry['required_steps'][6],'Review actual all-direction anatomy, separate layers, neutral/source palettes, registration and intended scale.',['registered/model.json'],['record-review.py','registered/authoring-review.json','registered/game-scale-comparison.png','artifact-manifest.json'],reason)
event(entry['required_steps'][7],'Keep native named anatomy and outfit acceptance behind all-generation gate.',['registered/model.json'],[],'No native/game/harness tests or activation. BODY-IRUDAD generation-ready does not complete NPC-ELDERBOB; exact captured equipment attachment and later integrated anatomy/state/visibility/hurt/look/save remain required.','DEFERRED UNTIL ALL GENERATED')
entry.update(status='UNFINISHED',generation_ready=True,current_step=entry['required_steps'][-1],known_issues=[],current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-comparison.png')),
    registration_summary='Separate Irudad mutation art over the unchanged older-human base: raised arm pair, joined-hands face and posterior barbed tail. Transparent top padding preserves original world scale/ground. Four required views and source palettes are below. Actual captured outfit and Hand201/6 pose remain unfinished on NPC-ELDERBOB.',
    art_review=dict(status='PASS',reason=reason,record=ref(OUT/'authoring-review.json')))
npc=next(e for e in ledger['entries'] if e['id']=='NPC-ELDERBOB');assert npc['status']=='UNFINISHED'
npc.update(status='IN PROGRESS',current_step=npc['required_steps'][1],known_issues=['Separated BODY-IRUDAD art is now generation-ready. Verify current dependency versions, pad actual fittings to the same physical frame and resolve visual attachment of captured Walking Stick541 on changed Hand201/6 alongside the hands-face pose.'])
npc['advancement_blocker'].update(reason=npc['known_issues'][0],resolution='Complete the captured four-item authoring assembly with explicit original slot/pose metadata and shared padded frame.')
ledger.update(active_entry=npc['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(dict(generation_ready=sum(bool(e.get('generation_ready')) for e in ledger['entries']),total=len(ledger['entries']),active_entry=ledger['active_entry'],verified_source_files=len(verified),native_acceptance='pending')))
