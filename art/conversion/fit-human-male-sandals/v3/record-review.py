"""Record male-specific fitting of the corrected shared sandal source."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-male/v2'
SOURCE=ROOT/'art/conversion/fit-human-female-sandals/v3'
IDENT='FIT-HUMAN-MALE-SANDALS-FEET-0';NEXT='FIT-IRUDAD-SANDALS-FEET-0'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,data):p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
model=json.loads((HERE/'model.json').read_text())
checks={}
ankle_checks={}
for facing,rows in model['views'].items():
    body=np.array(Image.open(BODY/f'selected-{facing}.png').convert('RGBA'))
    item=np.array(Image.open(HERE/f'intact-sandals-{facing}.png').convert('RGBA'))
    overlay=np.array(Image.open(HERE/f'body-overlay-{facing}.png').convert('RGBA'))
    mask=np.array(Image.open(HERE/f'body-visibility-{facing}.png').convert('L'))
    assembled=np.array(Image.open(HERE/f'assembled-{facing}.png').convert('RGBA'))
    assert np.array_equal(item[:,:,0],item[:,:,1]) and np.array_equal(item[:,:,1],item[:,:,2])
    assert np.array_equal(body[:800],assembled[:800]) and np.array_equal(body[:,:,:3],overlay[:,:,:3])
    assert np.array_equal(overlay[:,:,3],np.uint8(np.round(body[:,:,3].astype(float)*mask/255)))
    for row in rows:
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
        assert row['contact']==[256,950] and row['size']==[512,1024]
    if facing in ['south','north']:
        ankle_checks[facing]={}
        for y in [884,888]:
            missing=(body[y,:,3]>128)&(mask[y]>127)
            assert not missing.any(),(facing,y,'incomplete ankle band')
            ankle_checks[facing][y]={'uncovered_ankle_pixels':int(missing.sum())}
    checks[facing]=dict(neutral_item=True,original_body_preserved=True,registered_file_hashes_match=True,late_visibility_exact=True,contact=[256,950])
reason='Inspected male SEN and mirrored west: continuous profile bands cover the foot height and reach the sole, with front/rear ankle bands spanning both original ankle edges, crossed front straps and rear heel supports. Source/refinement reused from female v3; whole-foot horizontal fitting matches the original male foot bounds, keeping vertical contact and original skin unchanged. Native palette remains sole y / straps w with illustrative body C. No new ImageGen call, native acceptance or named mutation assembly.'
review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',reason=reason,canonical_source=ref(SOURCE/'model.json'),structural_gate=ref(SOURCE/'first-refinement-structural-review.json'),new_imagegen_call=False,checks=checks,ankle_span_checks=ankle_checks)
write(HERE/'authoring-review.json',review)
write(HERE/'artifact-manifest.json',{'artifacts':[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']})
f=ROOT/'evidence/conversion-ledger.json';d=json.loads(f.read_text());assert d['active_entry']==IDENT
e=next(e for e in d['entries'] if e['id']==IDENT)
for step,action,outputs in [
 ('select_correct_body_and_references','Resolve the actual male Feet/0 bindings and fixed male body against the corrected shared Sandals source, native description/palette and original donor role.', ['source-packet.json']),
 ('construct_and_overlay_one_item','Fit corrected complete soles/straps per foot to the original male bounds; no deformation of body or removal of source material.', ['fit-sandals.py','registration-decisions.json','intact-garment-comparison.png']),
 ('imagegen_refine_in_context_on_unchanged_body','Reuse the exact contextual retry and its structural inspection from the shared source; no additional generation call.', ['source-packet.json']),
 ('retrieve_isolated_item_and_masks','Retain full fitted item and separate original-foot visibility, with the same coordinate map for leather, tint and masks.', ['model.json','body-overlay-comparison.png','mask-off-comparison.png']),
 ('recompose_check_cuffs_attachment_occlusion_all_views','Inspect all directional male fits for connected strap coverage and late body ownership.', ['assembly-comparison.png','footwear-comparison.png']),
 ('review_game_scale_and_palette','Inspect intended-size and independent native/body colors; verify file/frame and original body ownership invariants.', ['game-scale-review.png','independent-palette-comparison.png','authoring-review.json','artifact-manifest.json'])]:
    e['process_log'].append(dict(timestamp=review['timestamp'],step=step,action=action,inputs=[ref(SOURCE/'source-packet.json'),ref(SOURCE/'model.json'),ref(SOURCE/'refined-red-context.png'),ref(BODY/'model.json')],outputs=[ref(HERE/n) for n in outputs],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'footwear-comparison.png')),art_review=dict(status='PASS',reason=reason),registration_summary='v3 corrected full-width ankle and full-height Sandals straps fitted to original male feet; shared contextual retry, separate body/equipment tint and fixed contact.')
e['apparel_workflow']['status']='GENERATION READY'
e['known_issues']=[x for x in e['known_issues'] if not x.startswith(('Profile straps terminate below the foot upper contour','v2 front/back ankle bands'))]
next_e=next(e for e in d['entries'] if e['id']==NEXT);next_e['status']='IN PROGRESS';d.update(active_entry=NEXT,updated_at=review['timestamp'])
assert [e['id'] for e in d['entries'] if e['status']=='IN PROGRESS']==[NEXT]
write(f,d)
print('Male Sandals corrected; only Irudad Sandals is active. No native tests.')
