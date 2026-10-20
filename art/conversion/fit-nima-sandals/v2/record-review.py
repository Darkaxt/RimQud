"""Record Nima's exact shared fit and actual ordinary Feet binding."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SOURCE=ROOT/'art/conversion/fit-human-female-sandals/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,data):p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
model=json.loads((HERE/'model.json').read_text());shared=json.loads((SOURCE/'model.json').read_text())
part=model['actual_equipped_binding']
assert part['type']=='Feet' and part['laterality']==0 and part['manager'] is None
assert part['equipped']['blueprint']=='Sandals'
for facing,rows in model['views'].items():
    for row,source in zip(rows,shared['views'][facing]):
        assert row['public_file']==source['public_file'] and row['sha256']==source['sha256']
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
        assert row['contact']==[256,950] and row['size']==[512,1024]
reason='Nima ordinary Feet/0 uses the same fixed unmutated female base and identical Sandals source/palette. Corrected shared SEN/profile/west straps, full soles and original foot masks are reused byte-for-byte; reviewed shared footwear and intended-size evidence applies exactly. No extra body or ImageGen call. Body C on shared color plate is illustrative; this is not acceptance of Nima individual body/tail/extra-arm or native outfit assembly.'
review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS',reason=reason,actual_binding=part,canonical_source=ref(SOURCE/'model.json'),canonical_authoring_review=ref(SOURCE/'authoring-review.json'),structural_gate=ref(SOURCE/'first-refinement-structural-review.json'),new_imagegen_call=False,shared_pixels_unchanged=True)
write(HERE/'authoring-review.json',review)
write(HERE/'artifact-manifest.json',{'artifacts':[ref(p) for p in sorted(HERE.iterdir()) if p.is_file() and p.name!='artifact-manifest.json']})
f=ROOT/'evidence/conversion-ledger.json';d=json.loads(f.read_text());ident='FIT-NIMA-SANDALS-FEET-0';assert d['active_entry']==ident
e=next(e for e in d['entries'] if e['id']==ident)
for step,action,outputs in [
 ('source_identity_description_slot_laterality','Resolve Nima actual ordinary Feet/0 Sandals binding and identical native item/palette against the corrected shared source.',[HERE/'source-packet.json']),
 ('construct_and_overlay_one_item','Bind exact corrected source geometry on the same unmutated female feet; no redraw or resampling is required.',[HERE/'bind-shared-fit.py',HERE/'registration-decisions.json']),
 ('imagegen_refine_in_context_on_unchanged_body','Reuse the actual corrected contextual retry, prompt and structural review; no new generation call claimed.',[SOURCE/'imagegen-prompt.txt',SOURCE/'refined-red-context.png',SOURCE/'first-refinement-structural-review.json']),
 ('retrieve_isolated_item_and_masks','Retain identical full Sandals and late foot-ownership masks, separately bound to the actual item.',[HERE/'model.json',SOURCE/'intact-garment-comparison.png',SOURCE/'body-overlay-comparison.png']),
 ('recompose_check_cuffs_attachment_occlusion_all_views','Review exact shared directional footwear and original-foot composition; this does not complete individual mutations.',[SOURCE/'footwear-comparison.png',SOURCE/'mask-off-comparison.png']),
 ('review_game_scale_and_palette','Reconcile actual native item palette and shared neutral/intended-size evidence with Nima ordinary Feet binding.',[SOURCE/'game-scale-review.png',SOURCE/'independent-palette-comparison.png',HERE/'authoring-review.json',HERE/'artifact-manifest.json'])]:
    e['process_log'].append(dict(timestamp=review['timestamp'],step=step,action=action,inputs=[ref(SOURCE/'source-packet.json'),ref(SOURCE/'model.json')],outputs=[ref(p) for p in outputs],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',art_review={'status':'PASS','reason':reason},current_registration=dict(model=ref(HERE/'model.json'),plate=ref(SOURCE/'footwear-comparison.png')),registration_summary='v2 corrected full-height Sandals shared exactly with the unmutated female base, explicitly bound to Nima ordinary Feet/0; native and mutation assembly remain pending.')
e['apparel_workflow']['status']='GENERATION READY'
e['known_issues']=[x for x in e['known_issues'] if not x.startswith('Profile straps terminate below the foot upper contour')]
next_id='ITEM-SANDALS';next_e=next(e for e in d['entries'] if e['id']==next_id);next_e['status']='IN PROGRESS';d.update(active_entry=next_id,updated_at=review['timestamp'])
assert [e['id'] for e in d['entries'] if e['status']=='IN PROGRESS']==[next_id]
write(f,d)
print('Nima corrected shared Sandals binding recorded; only Sandals aggregate is active.')
