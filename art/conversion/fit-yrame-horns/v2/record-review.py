"""Review the cross-view forehead-root correction without redrawing bone."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SOURCE=HERE.parent/'v1';SIZE=(512,1152)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
assert not (HERE/'authoring-review.json').exists()
model=json.loads((HERE/'model.json').read_text());old=json.loads((SOURCE/'model.json').read_text());controls=json.loads((HERE/'attachment-controls.json').read_text());checks={}
for f,rows in model['views'].items():
    body=read(SOURCE/f'original-body-{f}.png');a=np.array(body);layers={}
    for depth in ['near','far']:
        dx,dy=controls[f][depth+'_translation']
        for stem in ['intact','detail']:
            source=read(SOURCE/f'{stem}-{depth}-{f}.png');expected=source.transform(SIZE,Image.Transform.AFFINE,[1,0,-dx,0,1,-dy],Image.Resampling.NEAREST);target=read(HERE/f'{stem}-{depth}-{f}.png');assert np.array_equal(np.array(expected),np.array(target))
            if dx==0 and dy==0:assert np.array_equal(np.array(source),np.array(target))
        layers[depth]=Image.alpha_composite(read(HERE/f'intact-{depth}-{f}.png'),read(HERE/f'detail-{depth}-{f}.png'))
    expected=Image.alpha_composite(Image.alpha_composite(layers['far'],body),layers['near']);assert np.array_equal(np.array(expected),np.array(read(HERE/f'assembled-{f}.png')))
    for x,y in controls[f]['roots']:assert a[round(y),round(x),3]>128,'Authored root lies on original skull, not outside it.'
    for row,prior in zip(rows,old['views'][f]):
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
        for k in ['width','height','center_x','center_z','size','contact','layer']:assert row[k]==prior[k]
    checks[f]=dict(original_body=True,exact_recomposition=True,only_integer_translations=True,physical_mapping_unchanged=True,forehead_roots=controls[f]['roots'])
reason=('User-identified inconsistency corrected by preserving selected frontal forehead roots and translating complete profile horns forward to the same forehead site: near51px, far40px. Reviewed front/profile/back root guide and before/after. Profile near/far roots now overlap on the anterior forehead instead of the mid-side of the skull; rear forehead roots remain hidden behind original head. South/north source pixels, selected bone material/size, full roots, native tint, body and physical mapping unchanged. No new ImageGen/isolation call. Anatomical landmarks remain authored estimates, not native skull bones; integrated natural-head/gear and Yrame assembly acceptance still pending.')
now=datetime.now(timezone.utc).isoformat();review=dict(timestamp=now,status='PASS',scope='Generation authoring correction only',reason=reason,checks=checks,shared_refinement=ref(SOURCE/'refined-red-context.png'),new_imagegen_calls=0,native_acceptance=model['native_acceptance'])
write(HERE/'authoring-review.json',review);write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
p=ROOT/'evidence/conversion-ledger.json';d=json.loads(p.read_text());assert d['active_entry']=='FIT-YRAME-HORNS-HEAD-0';e=next(x for x in d['entries'] if x['id']==d['active_entry'])
for step,action,names in [('recompose_check_cuffs_attachment_occlusion_all_views','Review one anatomical forehead-root site across all views, including rear roots hidden by original head. Translate full near/far bone and tint together; no silhouette/body redraw.',['model.json','assembly-comparison.png','profile-root-before-after.png','forehead-root-guide.png','registration-decisions.json']),('review_game_scale_and_palette','Review corrected forehead profile at intended size, unchanged source w/W colors and unchanged physical mapping.',['independent-palette-comparison.png','game-scale-review.png','authoring-review.json','artifact-manifest.json'])]:
    e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'attachment-controls.json'),ref(SOURCE/'refined-red-context.png')],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),registration_summary='Corrected paired high-forehead horn attachment across front/profile/back. Same full bone/material and original body; profile near/far moved forward, rear roots hidden. Source Head288/0 retained; native acceptance and full Yrame assembly pending.')
next_id='ITEM-HORNS';next(x for x in d['entries'] if x['id']==next_id).update(status='IN PROGRESS',current_step='verify_every_body_fitting_log');d.update(active_entry=next_id,updated_at=now);assert [x['id'] for x in d['entries'] if x['status']=='IN PROGRESS']==[next_id];write(p,d);print('Forehead attachment correction generation-ready; Horns aggregate needs refresh.')
