"""Record inspected source-to-material oven conversion and pending native acceptance."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
import numpy as np
from PIL import Image

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]; OUT=HERE/'registered'
def read(p): return Image.open(p).convert('RGBA')
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d): p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (OUT/'authoring-review.json').exists()
now=datetime.now(timezone.utc).isoformat()
model=json.loads((OUT/'model.json').read_text()); packet=json.loads((HERE/'source-packet.json').read_text())
master=np.array(read(OUT/'neutral-master.png')); pattern=np.array(read(HERE/'constructed.png'))
own=np.array(read(OUT/'ownership-master.png'))
assert np.array_equal(master[:,:,3],pattern[:,:,3]) and np.array_equal(master[:,:,3],own[:,:,3])
assert np.array_equal(master[:,:,0],master[:,:,1]) and np.array_equal(master[:,:,1],master[:,:,2])
def at(x,y): return master[round(y*32),round(x*32),3]
assert at(8,12)==0 and at(8,19.5)==0  # Real arch and lower base slot.
assert at(8,16)==255 and at(3,16)==255 and at(11,3)==255
a=np.array(read(OUT/'primary-neutral.png')); coverage=np.array(Image.open(OUT/'coverage.png'))
w=np.array(Image.open(OUT/'detail-weight.png'))
assert a.shape==(256,256,4) and np.array_equal(a[:,:,3],coverage)
assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2])
assert not w[coverage==0].any()
assert not (coverage[0].any() or coverage[-1].any() or coverage[:,0].any() or coverage[:,-1].any())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
fg=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8)
dc=np.frombuffer(bytes.fromhex(palette['R']),dtype=np.uint8); ratio=w.astype(float)/255
rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*a[:,:,:1]/255))
rgb[coverage==0]=0
assert np.array_equal(np.dstack([rgb,coverage]),np.array(read(OUT/'native-primary-w-detail-upper-r.png')))
for val in model.values():
    if isinstance(val,dict) and 'path' in val: assert ref(ROOT/val['path'])['sha256']==val['sha256']
assert not model['native_activation'] and packet['frame']['authored_source_anchor']==[8,16]
reason='Reviewed exact JoppaOven/Oven ancestry, description and native w clay/R fire tile: right-offset chimney, flared cap, thick arch, central low fire and raised rectangular hearth/plinth with open base slot. Curved clay surfaces, shallow rim/bevel and wear are authored refinements; hidden depth remains unknown. Actual retained Apothecary1.5LegacyAssets kiln and matching definition/LoadFolders inspected: Graphic_Single,1x1,rotatablefalse, drawSize unspecified in inspected child/parent. Partial clay/dome shading reference only; no fieldstones, round base, centered chimney, donor footprint or gameplay copied, no active1.6loose-PNG claim. One actual contextual refinement reviewed before extraction. Generated halo, opaque/dark gap fill and fire glow rejected; usable material selected into exact editable coverage/ink and separate fire role with same-material continuation. Full neutral and native w/R plates and16x24/24x36/32x48views inspected; actual mouth/base gaps remain transparent, shared frame/pivot retained. Bounded installed Campfire code/definitions give AppleMatz cooking/heat, no body rendering override or declared unlit replacement; no new smoke, particles, food/log props or animation. Native preset/cooking/thermal/status/physics/visibility/save-load acceptance remains pending full-set generation.'
write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete generation authoring only',reason=reason,checks=dict(exact_fixed_geometry_alpha=True,arch_and_base_slot_transparent=True,neutral_equal_RGB=True,independent_fire_detail=True,single_coverage_native_palette_matches=True,transparent_frame_edges=True,shared_frame_pivot_scale=True,native_activation=False),new_imagegen_calls=1,second_isolation_call=False,native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
p=ROOT/'evidence/conversion-ledger.json'; data=json.loads(p.read_text())
assert data['active_entry']=='SCN-JOPPAOVEN'
e=next(e for e in data['entries'] if e['id']=='SCN-JOPPAOVEN')
def event(step,action,ins,outs,review,result='PASS',**extra):
    e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result,**extra))
event('resolve_object_description_original_tile_palette_state','Resolve Joppa clay oven description, ancestry, original tile and palette, cooking preset/heat and declared native visual states.',[],['source-packet.json','source-reference-construction.png'],'Version-pinned definitions plus bounded Campfire code metadata study; AppleMatz preset, CampfireHeatSelfOnly and unset ExtinguishBlueprint recorded. No game launch or invented fire/smoke/off state.')
event('select_render_reference_or_document_no_equivalent','Inspect actual retained Apothecary1.5charcoal kiln texture and matching child/parent/LoadFolders mapping.',['source-packet.json'],['source-reference-construction.png'],'Partial clay/dome material reference only. Retained legacy asset provenance explicit; current1.6bundle image not claimed. Donor round base, fieldstones, central chimney, footprint and mechanics excluded.')
event('construct_faithful_shape','Construct editable source-bound offset chimney, broad cap, thick arched mouth/fire and raised rectangular plinth with genuine openings.',['source-packet.json'],['construct-oven.py','constructed.svg','constructed.png','ownership.svg','ownership.png','manual-structural-review.json'],'Full source/donor/manual plate inspected before refinement. Smooth clay curvature/rim/wear authored, no measured hidden depth claimed. Separate fire ownership. No structural patch required by manual inspection.')
event('create_required_state_neighbor_variants','Retain one fixed native source appearance and original cooking/heat/status ownership.',['source-packet.json'],['constructed.png'],'This Machinery/appliances entry requires fixed map view and source-supported states. No child animation loop, rendering override or configured extinguish replacement found. No invented facing/state or placement logic.')
jr=json.loads((HERE/'first-structural-review.json').read_text())
event('refine_materials_and_form','Perform one actual built-in contextual clay refinement and inspect all structure before extraction.',['constructed.png','refine-prompt.txt'],['refined-raw.png','first-structural-review.json'],jr['review'],tool='image_gen.imagegen',prompt_file=ref(HERE/'refine-prompt.txt'),generation_file=jr['generated_file'],settings=dict(transparent_background=True,referenced_image_paths=[str(HERE/'constructed.png'),str(HERE/'source-reference-construction.png'),packet['reference']['texture']['path']]))
event('extract_register_color_coverage','Select neutral clay/fire luminance into fixed geometry and restore exact source openings, ink and independent detail role.',['refined-raw.png','first-structural-review.json','ownership.png'],['register-oven.py','registered/model.json','registered/registration-decisions.json','registered/neutral-master.png','registered/primary-neutral.png','registered/detail-neutral.png','registered/detail-weight.png'],'One full-frame material sampling; no generated-bounds fitting. Same-material continuation excludes halo, dark displaced seams, background plugs and fire glow. Existing helper role names wood/top mean clay/fire here. No second AI isolation or destructive opening approximation.')
event('visual_review_identity_and_connections_at_game_scale','Inspect original/manual/refined/registered art, true openings, neutral/primary/fire separation and native w/R at intended sizes.',['registered/model.json'],['record-review.py','registered/registration-comparison.png','registered/authoring-review.json','artifact-manifest.json'],reason)
event('native_state_review','Retain native cooking/preset/thermal/status/physics/visibility/save-load acceptance behind all-generation gate.',['registered/model.json'],[],'No native/game/harness validation or production activation; entry stays UNFINISHED pending integrated native acceptance.',result='DEFERRED UNTIL ALL GENERATED')
e.update(status='UNFINISHED',generation_ready=True,current_step='native_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'registration-comparison.png')),registration_summary='Source-bound Joppa clay oven: offset chimney, flared cap, true arch/fire and raised open plinth. Actual legacy RimWorld kiln reference, source/state metadata, editable manual geometry, one contextual refinement and fixed neutral/fire extraction logged. Native w/R palette preserved without generated glow/gap fill; one fixed source map face. Native cooking/thermal/physics/status acceptance pending.',native_acceptance=model['native_acceptance'],camera_review=dict(status='PASS',classification='SOURCE_FIXED_CARDINAL_MAP_FACE',reason='Shared source cell/pivot and straight source-facing arch/plinth; shallow clay volume authored without yaw or independent component scaling.',evidence=ref(OUT/'registration-comparison.png')))
idx=data['entries'].index(e); nxt=next(a for a in data['entries'][idx+1:] if not a.get('generation_ready'))
nxt.update(status='IN PROGRESS',current_step=nxt['required_steps'][0]); data.update(active_entry=nxt['id'],updated_at=now)
assert [a['id'] for a in data['entries'] if a['status']=='IN PROGRESS']==[nxt['id']]
write(p,data)
print(json.dumps(dict(generation_ready=sum(bool(a.get('generation_ready')) for a in data['entries']),total=len(data['entries']),next_active=nxt['id'],native_acceptance='PENDING')))
