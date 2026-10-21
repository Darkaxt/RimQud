"""Record inspected generation-only blade fitting; preserve native acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def im(p):return Image.open(p).convert('RGBA')
def write(name,v):(HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def array(p):return np.array(im(p))
assert not (HERE/'authoring-review.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='FIT-YRAME-VIBRO-BLADE-HAND-2'
e=next(e for e in l['entries'] if e['id']==l['active_entry']);m=read(HERE/'model.json');b=read(ROOT/m['base_model']);c=read(HERE/'fit-contract.json');d=read(HERE/'registration-decisions.json')
assert ref(ROOT/m['base_model'])['sha256']==m['body_sha256'];checks={}
old=array(HERE.parent/'v1/intact-canonical.png');new=array(HERE/'canonical-source.png')
assert np.array_equal(old[:,:,3],new[:,:,3]) and np.array_equal(old[old[:,:,3]>0],new[old[:,:,3]>0])
assert abs(d['physical_scale']['raster_scale']*d['physical_scale']['target_world_per_pixel']-d['physical_scale']['source_world_per_pixel'])<1e-14
for f,rows in m['views'].items():
 base=Image.new('RGBA',tuple(m['canvas']))
 for r in sorted(b['views'][f],key=lambda r:r['layer']):
  assert ref(ROOT/r['public_file'])['sha256']==r['sha256'];base.alpha_composite(im(ROOT/r['public_file']))
 assert np.array_equal(np.array(base),array(HERE/f'original-body-{f}.png'))
 full=im(HERE/f'intact-item-{f}.png');detail=im(HERE/f'item-detail-{f}.png');hand=im(HERE/f'original-hand-{f}.png')
 assert np.array_equal(np.array(Image.alpha_composite(full,detail)),np.array(full))
 for r in rows:
  assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
  for k in ['size','contact','width','height','center_x','center_z']:assert r[k]==b['views'][f][0][k],(f,k)
  a=array(ROOT/r['public_file']);assert not a[a[:,:,3]==0,:3].any();assert np.all(np.ptp(a[:,:,:3].astype(int),axis=2)==0)
 far=d['views'][f]['depth']=='far'
 expected=Image.alpha_composite(full,base) if far else Image.alpha_composite(Image.alpha_composite(base,full),hand)
 assert np.array_equal(np.array(expected),array(HERE/f'assembly-{f}.png'))
 if far:
  a=np.array(base);v=array(HERE/f'assembly-{f}.png');assert np.array_equal(a[a[:,:,3]==255],v[a[:,:,3]==255])
 else:
  x,y=d['views'][f]['anchor'];assert np.array(hand)[y,x,3]>200
  a=np.array(hand);v=array(HERE/f'assembly-{f}.png');assert np.array_equal(a[a[:,:,3]==255],v[a[:,:,3]==255])
 checks[f]=dict(unchanged_body_and_frame=True,exact_neutral_recomposition=True,exact_depth_composition=True,production_grayscale_and_empty_rgb=True,far_original_body_preserved=far,near_original_palm_preserved=not far)
assert np.array_equal(array(HERE/'intact-item-west.png'),np.array(ImageOps.mirror(im(HERE/'intact-item-east.png'))))
now=datetime.now(timezone.utc).isoformat()
reason='Reviewed manual and actual refined source refits, whole weapon, original-palm closeups, native c/y palette and intended-size plates. Lower handle sits toward the inner side of the correct front/back palm. Profile right-hand depth is near east and far west, without switching to the visible left hand. Same physical blade size and body/frame retained. Upright authoring display is provisional; resting/ready and native acceptance remain pending.'
review=dict(recorded_at=now,status='PASS',scope='Generation authoring only',reason=reason,checks=checks,
 canonical_visible_rgba_and_alpha_unchanged=True,physical_size_preserved=True,fit_contract=ref(HERE/'fit-contract.json'),
 per_view=dict(south='Continuous low handle enters the inner side of screen-left right palm; original hand is above intact handle.',east='Low handle meets original near right palm; finger-rest remains above grip. Slight forward lean is display-only.',north='Same right hand is screen-right; handle enters inward and far weapon sits behind original back/arm.',west='Mirrored item geometry with far right-hand depth. Original near left arm/body hides the grip; visible blade emerges forward. Hidden far palm position is an authored estimate, not recovered coordinates.'),
 visual_evidence=[ref(HERE/n) for n in ['manual-fit-comparison.png','assembly-comparison.png','grip-comparison.png','independent-palette-comparison.png','full-item-comparison.png','game-scale-review.png']],
 new_imagegen_calls=0,reused_generation=ref(HERE.parent/'v1/refined-red-context.png'),
 limitations=['Actor-sensitive slot demand, hidden west palm projection, charge state and native dimensions are unknown.','Captured weight3 versus installed2 remains recorded.','Display angle is not approval of resting/drafted presentation. Horizontal drafted side pose belongs to final assembly after the full-generation gate.'])
write('authoring-review.json',review)
write('artifact-manifest.json',dict(recorded_at=now,entry=e['id'],artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
for step,names in [('construct_and_overlay_one_item',['manual-fit-comparison.png','fit-contract.json']),('recompose_check_cuffs_attachment_occlusion_all_views',['assembly-comparison.png','grip-comparison.png','full-item-comparison.png','construction-attempt-notes.json','authoring-review.json']),('review_game_scale_and_palette',['independent-palette-comparison.png','game-scale-review.png','artifact-manifest.json'])]:
 e['process_log'].append(dict(timestamp=now,step=step,action=reason,inputs=[ref(HERE/'source-packet.json')],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_equipment_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),held_pose_review='Pending final assembly after all entries are generation-ready',registration_summary=reason)
n=next(e for e in l['entries'] if e['id']=='ITEM-VIBRO-BLADE');assert not n['generation_ready'];n.update(status='IN PROGRESS',current_step='resolve_item_identity_description_palette')
l.update(active_entry=n['id'],updated_at=now);(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode())
print('Blade fit generation-ready; ITEM-VIBRO-BLADE is the sole active entry. Native and pose acceptance remain pending.')
