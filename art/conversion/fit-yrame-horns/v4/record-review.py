"""Record the inspected all-view horn authoring result and exact asset evidence."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SIZE=(768,1152)


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def image(p):
    return Image.open(p).convert('RGBA')


def write(name,d):
    (HERE/name).write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())


def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())


assert not (HERE/'authoring-review.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json')
assert ledger['active_entry']=='FIT-YRAME-HORNS-HEAD-0'
entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
model=read(HERE/'model.json'); body=read(ROOT/model['base_model'])
assert ref(ROOT/model['base_model'])['sha256']==model['body_sha256']
checks={}
for facing in ['south','east','north']:
    base=Image.new('RGBA',SIZE)
    for r in sorted(body['views'][facing],key=lambda r:r['layer']):
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
        base.alpha_composite(image(ROOT/r['public_file']))
    assert np.array_equal(np.array(base),np.array(image(HERE/f'original-body-{facing}.png')))
    full=image(HERE/f'intact-item-{facing}.png')
    detail=image(HERE/f'detail-item-{facing}.png')
    assert np.array_equal(np.array(Image.alpha_composite(full,detail)),np.array(full))
    for r in model['views'][facing]:
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
        assert r['size']==list(SIZE)
        for k in ['contact','width','height','center_x','center_z']:
            assert r[k]==body['views'][facing][0][k],(facing,k)
        a=np.array(image(ROOT/r['public_file']))
        assert np.all(np.ptp(a[:,:,:3].astype(int),axis=2)==0)
        assert not a[a[:,:,3]==0,:3].any()
    expected=Image.alpha_composite(full,base) if facing=='north' else Image.alpha_composite(base,full)
    assert np.array_equal(np.array(expected),np.array(image(HERE/f'assembly-{facing}.png')))
    checks[facing]=dict(body_rgba_unchanged=True,shared_physical_frame=True,neutral_grayscale=True,
                        empty_alpha_rgb_zero=True,base_and_detail_recompose_exactly=True,depth_recomposition_exact=True)

# Independent tint-region evidence, kept in the report rather than production.
plate=Image.new('RGB',(1200,500),'#142823');draw=ImageDraw.Draw(plate)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
draw.text((18,15),'W DETAIL OWNERSHIP / highlighted bone only; original skin and ears excluded',font=font,fill='#e3cf43')
for i,facing in enumerate(['south','east','north']):
    im=image(HERE/f'detail-item-{facing}.png')
    bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im)
    box=(350,0,670,360) if facing=='east' else (224,0,544,360)
    plate.paste(bg.crop(box).convert('RGB').resize((320,360)),(40+i*395,60))
    draw.text((40+i*395,440),facing.upper(),font=font,fill='#e3cf43')
plate.save(HERE/'tint-detail-comparison.png')
now=datetime.now(timezone.utc).isoformat()
reason='Inspected actual refined output and registered neutral/native-tint, head closeups, full-body, full-item and intended-size plates. Broad roots join the same upper anterolateral crown; profile origin is above/forward of the original ear; north skull hides anterior roots. Ears remain flesh, curl tips remain bone, west mirrors east. Original body/physical frame unchanged. No clothing or other equipment in the primary preview.'
review=dict(recorded_at=now,status='PASS',scope='Generation authoring only',reason=reason,
            per_view=dict(south='Both roots continuously meet upper crown; paired returning curls stay above flesh ears.',
                          east='Near root is upper/anterior, above and forward of ear; complete backward curl has a separate tapering bone tip. Natural far-horn overlap is retained.',
                          north='Original skull occludes anterior roots. Visible posterior curls and tips are separate from both original flesh ears.',
                          west='Mirrored east anatomy preserves skull-relative root and ear ownership; no independent placement or slot change.'),
            checks=checks,fit_contract=ref(HERE/'fit-contract.json'),
            first_refinement=ref(HERE/'first-refinement-structural-review.json'),
            registration=ref(HERE/'registration-decisions.json'),actual_imagegen_calls=1,second_isolation_call=False,
            limitations=['Upper anterolateral root geometry and ram-like curl remain authored interpretation; no native skull coordinates are available.',
                         'Hidden north root interiors are deterministic manual continuation, not unseen anatomy recovered from ImageGen.',
                         model['native_acceptance']])
write('authoring-review.json',review)
write('artifact-manifest.json',dict(recorded_at=now,entry=entry['id'],artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
for step,action,names in [
    ('recompose_check_cuffs_attachment_occlusion_all_views','Compare every actual fitted facing with the attachment contract; inspect skull connection, bone/ear ownership and natural depth.',['head-fit-comparison.png','assembly-comparison.png','full-item-comparison.png','depth-ownership-comparison.png','model.json','authoring-review.json']),
    ('review_game_scale_and_palette','Review intended-size silhouette and independent w/W bone regions on the unchanged native w/B body; retain generation-only acceptance.',['game-scale-review.png','independent-palette-comparison.png','tint-detail-comparison.png','artifact-manifest.json'])]:
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'fit-contract.json'),ref(HERE/'context-refinement-raw.png')],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],
             art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),
             current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),
             registration_summary='Selected v4 natural Head288/0 horn fit on the unchanged centauroid body. Per-view crown attachment, flesh ears, full roots, shared scale and independent w/W tint reviewed. Named outfit and native acceptance remain pending.')
next_entry=next(e for e in ledger['entries'] if e['id']=='ITEM-HORNS')
assert not next_entry['generation_ready']
next_entry.update(status='IN PROGRESS',current_step='resolve_item_identity_description_palette')
ledger.update(active_entry=next_entry['id'],updated_at=now)
(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Horn fitting generation-ready; native review still pending. ITEM-HORNS is now the sole active entry.')
