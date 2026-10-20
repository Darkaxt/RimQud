"""Record the inspected structural correction; preserve native acceptance gate."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-female/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,data):p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')

font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
comparison=Image.new('RGB',(1000,480),'#142823');draw=ImageDraw.Draw(comparison)
draw.text((18,16),'REAR ANKLE WIDTH / rejected narrow bands -> full-width curved bands',font=font,fill='#e3cf43')
for i,version in enumerate(['v2','v3']):
    source=HERE.parent/version/'palette-north.png'
    base=Image.new('RGBA',(512,1024),'#20382d');base.alpha_composite(Image.open(source).convert('RGBA'))
    comparison.paste(base.crop((120,860,390,955)).resize((438,154)),(22+i*500,85))
    draw.text((22+i*500,350),'REJECTED V2' if i==0 else 'CORRECTED V3 / same fixed feet',font=font,fill='#e3cf43')
draw.text((18,410),'Rear ankle bands now span both edges. Original feet, contact and item tint remain separate.',font=font,fill='#e5e8d8')
comparison.save(HERE/'ankle-width-before-after.png')

checks={}
ankle_checks={}
for facing in ['south','east','north']:
    body=np.array(Image.open(BODY/f'selected-{facing}.png').convert('RGBA'))
    cloth=np.array(Image.open(HERE/f'intact-sandals-{facing}.png').convert('RGBA'))
    construction=np.array(Image.open(HERE/f'constructed-cloth-{facing}.png').convert('RGBA'))
    overlay=np.array(Image.open(HERE/f'body-overlay-{facing}.png').convert('RGBA'))
    assembled=np.array(Image.open(HERE/f'assembled-{facing}.png').convert('RGBA'))
    mask=np.array(Image.open(HERE/f'body-visibility-{facing}.png'))
    assert np.array_equal(cloth[:,:,3],construction[:,:,3])
    assert np.array_equal(cloth[:,:,0],cloth[:,:,1]) and np.array_equal(cloth[:,:,1],cloth[:,:,2])
    assert np.array_equal(body[:800],assembled[:800])
    assert np.array_equal(body[:,:,:3],overlay[:,:,:3])
    expected=np.uint8(np.round(body[:,:,3].astype(float)*mask/255))
    assert np.array_equal(expected,overlay[:,:,3])
    assert Image.open(HERE/f'intact-sandals-{facing}.png').size==(512,1024)
    if facing in ['south','north']:
        ankle_checks[facing]={}
        for y in [884,888]:
            missing=(body[y,:,3]>128)&(mask[y]>127)
            assert not missing.any(), (facing,y,'ankle band does not span fixed body')
            ankle_checks[facing][y]={'uncovered_ankle_pixels':int(missing.sum())}
    checks[facing]=dict(body=ref(BODY/f'selected-{facing}.png'),full_item=ref(HERE/f'intact-sandals-{facing}.png'),fixed_geometry_alpha=True,neutral_rgb=True,body_above_footwear_unchanged=True,original_body_rgb_in_overlay=True,late_visibility_exact=True,contact=[256,950])
review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',scope='Generation-time art inspection only',
    reason='Inspected corrected SEN/west footwear, source retry and neutral/native palette. Profile bands run over the instep and forefoot upper contour and down to the sole instead of terminating halfway up the foot. Front/rear ankle bands now span both original ankle edges, with direct body/visibility checks at the actual band rows. Open skin between straps and back heel supports remains intentional. Source/feet/contact unchanged; AI body/background rejected, neutral material used with explicit corrected geometry. No native validation or named mutation assembly credit.',
    structural_gate=ref(HERE/'first-refinement-structural-review.json'),checks=checks,ankle_span_checks=ankle_checks,
    item_views=['south','east','north','west mirrors east'],
    native_acceptance='Pending complete requested generation set.')
write(HERE/'authoring-review.json',review)
manifest=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']
write(HERE/'artifact-manifest.json',{'artifacts':manifest})

ledger_file=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(ledger_file.read_text(encoding='utf-8'))
ident='FIT-HUMAN-FEMALE-SANDALS-FEET-0'
assert ledger['active_entry']==ident
entry=next(e for e in ledger['entries'] if e['id']==ident)
for step,action,outputs in [
 ('retrieve_isolated_item_and_masks','Register selected contextual neutral leather material onto the corrected complete sole/strap geometry; retain intact item and a separate original-foot visibility mask. No generative isolation.', ['register-sandals.py','registration-decisions.json','intact-garment-comparison.png','strap-detail-comparison.png','body-overlay-comparison.png','mask-off-comparison.png']),
 ('recompose_check_cuffs_attachment_occlusion_all_views','Recompose original body, complete Sandals, independent strap tint and exposed-foot overlay in every required facing.', ['model.json','assembly-comparison.png','footwear-comparison.png','ankle-width-before-after.png']),
 ('review_game_scale_and_palette','Inspect actual strap-height correction, all cardinal neutral/native colors and intended-size appearance before restoring authoring readiness.', ['independent-palette-comparison.png','game-scale-review.png','authoring-review.json','artifact-manifest.json'])]:
    entry['process_log'].append(dict(timestamp=review['timestamp'],step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'first-refinement-structural-review.json'),ref(HERE/'refined-red-context.png')],outputs=[ref(HERE/name) for name in outputs],review=review['reason'],result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',art_review={'status':'PASS','reason':review['reason']},current_registration={'model':ref(HERE/'model.json'),'plate':ref(HERE/'footwear-comparison.png')},registration_summary='v3 structural correction: full-width curved front/rear ankle bands and full-height connected profile straps; one contextual retry, fixed original feet and separate y/w leather ownership. Native acceptance pending.')
entry['apparel_workflow']['status']='GENERATION READY'
entry['known_issues']=[x for x in entry['known_issues'] if not x.startswith(('Profile straps terminate below the foot upper contour','v2 front/back ankle bands'))]
next_id='FIT-HUMAN-MALE-SANDALS-FEET-0'
next_entry=next(e for e in ledger['entries'] if e['id']==next_id);next_entry['status']='IN PROGRESS'
ledger.update(active_entry=next_id,updated_at=review['timestamp'])
assert [e['id'] for e in ledger['entries'] if e['status']=='IN PROGRESS']==[next_id]
write(ledger_file,ledger)
print('Female Sandals v3 generation-ready; male Sandals is the only active entry. Native checks remain deferred.')
