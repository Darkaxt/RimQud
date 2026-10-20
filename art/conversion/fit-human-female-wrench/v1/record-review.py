"""Record complete wrench authoring; native offhand acceptance stays gated."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
model=json.loads((HERE/'model.json').read_text());canonical=np.array(read(HERE/'intact-canonical.png'));pattern=np.array(read(HERE/'constructed-canonical.png'))
assert np.array_equal(canonical[:,:,3],pattern[:,:,3]) and canonical[365,270,3]==0,'Preserve open jaw; incidental generated background is not metal.'
assert np.array_equal(canonical[:,:,0],canonical[:,:,1]) and np.array_equal(canonical[:,:,1],canonical[:,:,2])
checks={}
for facing,rows in model['views'].items():
    body=read(BODY/f'selected-{facing}.png');item=read(HERE/f'intact-item-{facing}.png');detail=read(HERE/f'item-detail-{facing}.png');hand=read(HERE/f'original-hand-{facing}.png');equipment=Image.alpha_composite(item,detail)
    expected=Image.alpha_composite(equipment,body) if facing!='south' else Image.alpha_composite(Image.alpha_composite(body,equipment),hand)
    assert np.array_equal(np.array(expected),np.array(read(HERE/f'assembled-{facing}.png')))
    b=np.array(body);h=np.array(hand);visible=h[:,:,3]>0;assert np.array_equal(b[visible,:3],h[visible,:3])
    a=np.array(item);unobscured=int(((a[:,:,3]>128)&(b[:,:,3]<128)).sum());assert unobscured>0
    for row in rows:assert ref(ROOT/row['public_file'])['sha256']==row['sha256'] and row['contact']==[256,950] and row['size']==[512,1024]
    checks[facing]=dict(original_body_and_palm=True,exact_recomposition=True,full_item_retained=True,unobscured_item_pixels=unobscured,registered_file_hashes_match=True)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);comparison=Image.new('RGB',(650,650),'#142823');draw=ImageDraw.Draw(comparison);draw.text((18,14),'ONE FIXED FEMALE BASE / different source-guided tool lengths',font=font,fill='#e3cf43')
knife=ROOT/'art/conversion/fit-human-female-steel-utility-knife/v1';sources=[(knife/'assembled-south.png','Small folding utility knife'),(HERE/'assembled-south.png','Armlength Wrench / offhand')]
for i,(path,label) in enumerate(sources):
    im=read(path);bg=Image.new('RGBA',(512,1024),'#20382d');bg.alpha_composite(im);comparison.paste(bg.convert('RGB').resize((256,512)),(20+i*325,60));draw.text((20+i*325,590),label,font=font,fill='#e3cf43')
comparison.save(HERE/'weapon-size-comparison.png')
reason='Inspected SEN/mirrored west, complete open jaw/neck/shaft, lower palm grip, neutral and native y-head/c-shaft palette and intended-size appearance. Armlength cue informs authored scale, larger than utility knife; decorative prop drawSize is not treated as weapon length. Original source alpha/ink and body pixels preserved. Contextual metal selected after first structural review; hidden grip completed before placement. Female compatibility only; actual male offhand and native near/far/ready/resting state remain pending.'
review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',scope='Generation authoring only',reason=reason,checks=checks,structural_gate=ref(HERE/'first-refinement-structural-review.json'),jaw_opening_preserved=True,canonical_alpha_unchanged=True,new_imagegen_calls=1,native_acceptance=model['native_acceptance'])
write(HERE/'authoring-review.json',review);write(HERE/'scale-comparison-inputs.json',dict(type='One item per panel on the same fixed body; size comparison only',sources=[ref(p) for p,_ in sources],body=ref(BODY/'model.json')))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']))
f=ROOT/'evidence/conversion-ledger.json';d=json.loads(f.read_text());ident='FIT-HUMAN-FEMALE-WRENCH-HAND-1';assert d['active_entry']==ident;e=next(x for x in d['entries'] if x['id']==ident)
for step,action,outputs in [
 ('retrieve_isolated_item_and_masks','Extract neutral contextual metal only into fixed complete hooked wrench; explicitly complete hidden grip and preserve open jaw, head/shaft tint regions and original hand mask.', ['register-wrench.py','registration-decisions.json','full-item-comparison.png','depth-off-comparison.png']),
 ('recompose_check_cuffs_attachment_occlusion_all_views','Recompose actual full tool with original body/hand depth; inspect every cardinal display and mirrored profile without drawing a new far arm.', ['model.json','assembly-comparison.png','grip-comparison.png']),
 ('review_game_scale_and_palette','Inspect source-guided armlength size against the small utility knife on one fixed body, independent native colors and intended-size view.', ['independent-palette-comparison.png','game-scale-review.png','weapon-size-comparison.png','scale-comparison-inputs.json','authoring-review.json','artifact-manifest.json'])]:
    e['process_log'].append(dict(timestamp=review['timestamp'],step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'refined-red-context.png'),ref(HERE/'first-refinement-structural-review.json')],outputs=[ref(HERE/n) for n in outputs],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'assembly-comparison.png')),registration_summary='Female compatibility Wrench: Qud hooked metal jaw and armlength shaft, lower Hand/1 grip, full item and original body depth, primary y/shaft c. Actual male binding and native offhand/pose state retained separately.',native_acceptance=model['native_acceptance'])
next_id='FIT-HUMAN-MALE-WRENCH-HAND-1';next_e=next(x for x in d['entries'] if x['id']==next_id);next_e.update(status='IN PROGRESS',current_step='source_identity_description_slot_laterality')
d.update(active_entry=next_id,updated_at=review['timestamp']);assert [x['id'] for x in d['entries'] if x['status']=='IN PROGRESS']==[next_id];write(f,d)
print('Female Wrench compatibility generation-ready; only male Wrench is active.')
