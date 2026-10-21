"""Review complete current named outfit as generation evidence, not game acceptance."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(768,1152)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.resolve().relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def im(p):return Image.open(p).convert('RGBA')
def a(p):return np.array(im(p))
def write(n,v):(HERE/n).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def norm(im):
 v=np.array(im);v[v[:,:,3]==0,:3]=0;return v
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='NPC-WARDEN-YRAME';e=next(e for e in l['entries'] if e['id']==l['active_entry']);m=read(HERE/'model.json');checks={}
assert not e.get('generation_ready')
assert sorted(v['instance'] for v in m['equipment_bindings'].values())==[574,575,576,580]
for key in ['body_model']:
 r=m[key];assert ref(ROOT/r['path'])==r
for v in m['equipment_bindings'].values():assert ref(ROOT/v['model']['path'])==v['model']
for f,v in m['views'].items():
 base=Image.new('RGBA',SIZE)
 for r in sorted(v['body'],key=lambda r:r['layer']):
  assert ref(ROOT/r['public_file'])['sha256']==r['sha256'];base.alpha_composite(im(ROOT/r['public_file']))
 assert np.array_equal(norm(base),a(HERE/f'base-{f}.png'))
 peritem={}
 for item in v['equipment']:
  name=item['name'];rs=item['components']
  for r in rs:
   assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
   for k in ['size','contact','width','height','center_x','center_z']:assert r[k]==v['body'][0][k],(name,f,k)
  # Verify the assembly's isolated-item display agrees with already reviewed fits.
  fitting=Path(item['model']['path']).parent
  rounding_pixels=0
  if True:
   expected=ROOT/fitting/f'assembly-{f}.png';actual=HERE/(name.lower().replace(' ','-')+f'-{f}.png')
   expected_image=im(expected) if expected.exists() else ImageOps.mirror(im(expected.parent/'assembly-east.png'))
   delta=np.abs(norm(expected_image).astype(int)-a(actual).astype(int));changed=delta.max(2)>0
   if changed.any():
    # Precomposing the whole body versus its separate native tint/head planes
    # differs by one rounding unit at a semitransparent body edge over a far item.
    ba=np.array(base)[:,:,3]
    assert name=='Vibro Blade' and f in ['north','west'] and delta[:,:,:3].max()==1 and delta[:,:,3].max()<=1
    assert int(changed.sum())=={'north':1,'west':4}[f]
    assert np.all((ba[changed]>0)&(ba[changed]<255))
    rounding_pixels=int(changed.sum())
  peritem[name]=dict(source_hashes_unchanged=True,body_frame_unchanged=True,depth_layers=[r['layer'] for r in rs],explicit_mirror_operation=any(r.get('needs_assembly_mirror') for r in rs),partial_body_edge_rounding_pixels=rounding_pixels)
 assert all(not r.get('needs_assembly_mirror') for r in v['body'])
 checks[f]=dict(original_body_exact=True,shared_physical_frame=True,item_sources_and_bindings_unchanged=True,individual_compositions_agree_with_reviewed_fits=peritem)
assert np.array_equal(a(HERE/'base-west.png'),np.array(ImageOps.mirror(im(HERE/'base-east.png'))))
westblade=next(x for x in m['views']['west']['equipment'] if x['name']=='Vibro Blade');assert westblade['part_id']==292 and all(r['layer']<0 for r in westblade['components']) and not any(r.get('needs_assembly_mirror') for r in westblade['components'])
for f in ['south','east','north']:
 neutral=a(HERE/f'full-neutral-{f}.png');assert not np.ptp(neutral[:,:,:3].astype(int),axis=2).any()
for f in m['views']:
 for r in [m['views'][f]['neutral_preview'],m['views'][f]['native_palette_preview']]:assert ref(ROOT/r['path'])==r
now=datetime.now(timezone.utc).isoformat()
reason='Reviewed corrected source-to-outfit, all four neutral/native-palette facings, stages and intended-size plates. Compact four-legged fleece trunk with no tail remains separate from ordinary female baseline; connected crown roots and flesh ears are unchanged. Mail covers torso with curved sleeve ownership. Only fore Feet297/16 wears actual Boots580; hind pair is bare. Actual right Hand292/2 keeps low blade grip and far west depth. Exact current dependency textures and shared physical frame are unchanged. Earlier rejected double-mirrored west assembly is retained as v2 history. Current horns use actual west art with calibrated head proxy and independent w/W tint; no additional mirror. Root shading remains minor polish after current independent fit review. These are generation authoring results, not native equipment or pose acceptance.'
write('authoring-review.json',dict(recorded_at=now,status='PASS',scope='Complete named-outfit generation authoring only',reason=reason,checks=checks,contract=ref(HERE/'assembly-contract.json'),rejected_attempt=ref(HERE.parent/'v2/rejected-double-body-mirror/rejection.json'),
 per_view=dict(south='Paired crown roots attach, ears separate; mail shoulders continuous; both inner fore boots and outer bare hind feet visible. Right-hand blade is screen-left.',east='Correct right profile; mail short sleeve meets original arm, fore boot pair overlaps, hind hooves remain bare; original near palm above handle.',north='Skull hides anterior horn roots, dorsal shirt ends at lower-trunk junction; original hind legs hide far fore boots and original right arm/body hides weapon grip.',west='Current west body pixels used once, matching mirrored mail/horns/boots. Right weapon remains far rather than switching to visible left hand.'),
 new_imagegen_calls=0,source_history=ref(HERE/'dependency-lineage.json'),
 limitations=['Fixed named mutation art is an authored selected interpretation, not a reusable unmutated human race or generic mutation system.','Icy Vapor is retained as native natural-equipment/effect metadata; no decorative freezing particles or extra glove invented.','Physical hidden joints and west palm position are estimates.','Resting/ready horizontal side pose and all native equipment/visibility/hurt/look/save acceptance remain after full-set generation gate.']))
write('artifact-manifest.json',dict(recorded_at=now,entry=e['id'],artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.name!='artifact-manifest.json']))
for step,names in [('assemble_without_baking_equipment',['model.json','assembly-stages.png','dependency-evidence.html']),('review_anatomy_clothing_attachment_all_directions',['assembly-contract.json','full-neutral-comparison.png','full-native-comparison.png','../v2/rejected-double-body-mirror/rejection.json','authoring-review.json']),('review_neutral_and_qud_palette_at_game_scale',['source-to-assembly.png','original-native-glyph.png','game-scale-comparison.png','artifact-manifest.json'])]:
 e['process_log'].append(dict(timestamp=now,step=step,action=reason,inputs=[m['body_model']]+[x['model'] for x in m['equipment_bindings'].values()],outputs=[ref(HERE/n) for n in names],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='native_visibility_equipment_hurt_look_save_review',known_issues=[],art_review=dict(status='PASS',reason=reason,record=ref(HERE/'authoring-review.json')),registration_summary=reason)
e.pop('advancement_blocker',None)
n=next(e for e in l['entries'] if e['id']=='FIT-IRUDAD-BLACK-ROBES-BODY-0');assert not n.get('generation_ready');n.update(status='IN PROGRESS',current_step='source_identity_description_slot_laterality')
l.update(active_entry=n['id'],updated_at=now);(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode())
print('Current named Yrame outfit generation-ready; Irudad robe correction is the sole active entry. Native acceptance remains pending.')
