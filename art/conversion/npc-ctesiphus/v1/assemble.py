"""Source-bound Ctesiphus assembly with an explicitly empty worn outfit."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];FACES=['south','east','north','west']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def im(p):return Image.open(p).convert('RGBA')
assert not (HERE/'model.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='NPC-CTESIPHUS';e=next(x for x in l['entries'] if x['id']==l['active_entry']);b=next(x for x in l['entries'] if x['id']=='BODY-RAY-CAT');assert b['generation_ready'];bref=b['current_registration']['model'];assert ref(ROOT/bref['path'])==bref;body=read(ROOT/bref['path'])
s=read(ROOT/'art/village/sources.json');actor=next(a for g in s['actors'] if g['creature']=='Ctesiphus' for a in g['native_instances'] if a['instance']==566);assert actor['parts']==e['metadata']['native_parts'];assert not any(p.get('equipped') for p in actor['parts']);assert sum(p['type']=='Foot' for p in actor['parts'])==4 and sum(p['type']=='Tail' for p in actor['parts'])==1
now=datetime.now(timezone.utc).isoformat();packet=dict(recorded_at=now,entry=e['id'],source=ref(ROOT/'art/village/sources.json'),captured_actor=actor,body_model=bref,body_review=b['art_review'],equipment_bindings={},natural_equipment=[dict(part=p['id'],type=p['type'],laterality=p['laterality'],item=p['defaultItem']) for p in actor['parts'] if p.get('defaultItem')],
 equipment_policy='Observed worn/held list is empty. Cat Bite/Claw defaults are natural behavior on real Face/Foot parts, not inventory clothes or separate held objects. No collar or profession costume added.',body_policy='Reuse current intrinsic Ray Cat body/head/tint source; named historical artwork remains unchanged. Male capture does not establish age or extra sex geometry. No mutation appendages inferred.',
 palette=dict(primary=actor.get('tileColor') or actor['foreground'],detail=actor['detailColor']),history=dict(report='docs/conversion-entries/BODY-RAY-CAT.html',source_packet=ref(ROOT/'art/conversion/body-ray-cat/v1/source-packet.json'),generation=ref(ROOT/'art/conversion/body-ray-cat/v1/historical-generation-provenance.json'),manual=ref(ROOT/'art/conversion/body-ray-cat/v1/manual-ownership-controls.json')),new_imagegen_calls=0,native_acceptance='Pending full-set generation gate: actual visible/hidden, facing, independent tint, look/hurt/save and supported state.')
write('source-packet.json',packet);write('assembly-contract.json',dict(recorded_at=now,body=bref,frame=body['registration'],equipment={},views=dict(south='Front cat head/forepaws below trunk, tail rises behind; hind pair occluded.',east='Whole right profile; head right, tail rooted at left rump; fore/hind near paws and overlapped far pair.',north='Back of skull/ears, no face; lower-rump tail curves outside flank separately from head.',west='Exact corrected east mirror, including head and both tint planes.'),palette=packet['palette'],policy=packet['equipment_policy'],native_activation=False))
pal=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];colors={role:np.array(tuple(bytes.fromhex(pal[(actor['detailColor'] if role=='detail' else actor.get('tileColor') or actor['foreground']).replace('&','')[0]]))) for role in ['foreground','detail']};groups={k:{} for k in ['neutral','native']};checks={}
for f in FACES:
 neutral=Image.new('RGBA',tuple(body['canvas']));native=Image.new('RGBA',tuple(body['canvas']))
 for row in sorted(body['views'][f],key=lambda r:r['layer']):
  assert ref(ROOT/row['public_file'])['sha256']==row['sha256'];image=im(ROOT/row['public_file']);a=np.array(image);assert not np.ptp(a[:,:,:3].astype(int),axis=2).any();neutral.alpha_composite(image);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*colors[row['color_role']]/255));a[a[:,:,3]==0,:3]=0;native.alpha_composite(Image.fromarray(a))
 expected=Path(bref['path']).parent;assert np.array_equal(np.array(neutral),np.array(im(ROOT/expected/f'recomposed-neutral-{f}.png')));assert np.array_equal(np.array(native),np.array(im(ROOT/expected/f'native-palette-{f}.png')))
 neutral.save(HERE/f'neutral-{f}.png');native.save(HERE/f'native-palette-{f}.png');groups['neutral'][f]=neutral;groups['native'][f]=native;checks[f]=dict(source_hashes_current=True,body_pixels_and_frame_unchanged=True,neutral_and_palette_exact_body_reference=True,worn_items=0)
write('model.json',dict(entry=e['id'],kind='captured_actor_layered_assembly',body_model=bref,source=ref(HERE/'source-packet.json'),registration=body['registration'],equipment_bindings={},views={f:dict(body=body['views'][f],equipment=[],neutral_preview=ref(HERE/f'neutral-{f}.png'),native_palette_preview=ref(HERE/f'native-palette-{f}.png')) for f in FACES},native_activation=False,native_acceptance=packet['native_acceptance']))
write('composition-checks.json',checks)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
for key,name in [('neutral','neutral-comparison.png'),('native','native-palette-comparison.png')]:
 out=Image.new('RGB',(1200,420),'#142823');d=ImageDraw.Draw(out);d.text((15,15),'CTESIPHUS / '+key.upper()+' / current ray-cat layers; actual worn outfit is empty',font=font,fill='#e3cf43')
 for i,f in enumerate(FACES):
  bg=Image.new('RGBA',tuple(body['canvas']),'#20382d');bg.alpha_composite(groups[key][f]);out.paste(bg.resize((280,280),Image.Resampling.LANCZOS).convert('RGB'),(10+i*300,55));d.text((15+i*300,360),f.upper(),font=font,fill='#e3cf43')
 d.text((15,394),'Natural claws/bite retained as source behavior. No new drawing or native validation.',font=font,fill='#e5e8d8');out.save(HERE/name)
out=Image.new('RGB',(800,360),'#142823');d=ImageDraw.Draw(out)
for j,key in enumerate(['neutral','native']):
 for i,f in enumerate(FACES):
  image=groups[key][f].resize((64,64),Image.Resampling.LANCZOS);out.paste(image,(15+i*200,15+j*170),image);zoom=image.resize((128,128),Image.Resampling.NEAREST);out.paste(zoom,(75+i*200,15+j*170),zoom);d.text((15+i*200,150+j*170),f.upper(),font=font,fill='#e3cf43')
out.save(HERE/'game-scale-review.png')
for step,action,names in [('resolve_individual_race_and_runtime_metadata','Resolve actual Ctesiphus566, Ray Cat race, four physical paws, intrinsic tail and natural defaults.',['source-packet.json']),('verify_body_and_every_equipped_item_dependencies','Verify current generation-ready Ray Cat and explicit empty worn/held list; retain full actual generation and current registration lineage.',['assembly-contract.json','composition-checks.json']),('assemble_without_baking_equipment','Compose exact current body/head/tint rows, with no equipment. Actual all-view palette/shape review pending.',['assemble.py','model.json','neutral-comparison.png','native-palette-comparison.png','game-scale-review.png'])]:
 e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[bref],outputs=[ref(HERE/n) for n in names],review=action,result='REQUIRES REVIEW' if step=='assemble_without_baking_equipment' else 'PASS'))
e.update(current_step='review_anatomy_clothing_attachment_all_directions',generation_ready=False,current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'neutral-comparison.png')),art_review=dict(status='REQUIRES REVIEW',reason='Current exact-layer assembly written; authoring review pending.'));l['updated_at']=now;(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode());print('Ctesiphus current exact-layer empty-outfit assembly written; review pending.')
