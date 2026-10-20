"""Index actual male and female-compatibility wrench authoring without new art."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
f=ROOT/'evidence/conversion-ledger.json';d=json.loads(f.read_text());assert d['active_entry']=='ITEM-WRENCH'
e=next(e for e in d['entries'] if e['id']=='ITEM-WRENCH');fits=[next(x for x in d['entries'] if x['id']==i) for i in e['related_entries']]
assert len(fits)==2 and all(x.get('generation_ready') and x['art_review']['status']=='PASS' for x in fits)
folders=[(ROOT/x['current_registration']['model']['path']).parent for x in fits]
assert (folders[0]/'intact-canonical.png').read_bytes()==(folders[1]/'intact-canonical.png').read_bytes()
models=[json.loads((p/'model.json').read_text()) for p in folders]
male=next(m for m in models if m['family']=='human-male');female=next(m for m in models if m['family']=='human-female')
for facing in ['south','east','north']:
    for axis in ['width','height']:
        assert abs(male['views'][facing][0][axis]*male['item_raster_scale']-female['views'][facing][0][axis])<1e-12
record=dict(item='Wrench',source=e['metadata']['original_reference'],fittings=[],
    scope='Actual captured male Argyve519 Hand322/1 item590 and separate female compatibility fitting. No captured female Wrench loadout is inferred.',
    source_identity='Armlength worn metal Wrench with broad hooked open jaw and screwing iron; native primary head y overrides foreground c, shaft detail c. Counterweighted text retained; no extra physical counterweight graphic is exported.',
    handedness='Full inherited one-hand base declaration and observed single ordinary Hand occupancy; actor-specific GetSlotsRequiredFor remains unknown.',
    scale='Identical complete canonical Wrench bytes and physical item size across bodies. Male raster compensation0.9828877005347593 with independent palm/angle/depth controls.',
    limits='Stationary authoring displays only; native offhand/ready-resting poses, equip state, named Argyve cosmetics/outfit and unsupported individual counterweight graphics remain pending the final full-set gate.',
    new_imagegen_calls=0)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);out=Image.new('RGB',(1152,1330),'#142823');draw=ImageDraw.Draw(out)
draw.text((18,14),'WRENCH / one physical item, two ordinary body fittings',font=font,fill='#e3cf43')
for row,(entry,p) in enumerate(zip(fits,folders)):
    model=json.loads((p/'model.json').read_text())
    for facing,components in model['views'].items():
        for component in components:assert ref(ROOT/component['public_file'])['sha256']==component['sha256']
    record['fittings'].append(dict(entry=entry['id'],registration=entry['current_registration'],metadata=ref(p/'weapon-metadata.json'),authoring_review=ref(p/'authoring-review.json'),observed_scope=model['binding_scope']))
    y=60+row*610;label='MALE / captured Argyve ordinary base' if model['family']=='human-male' else 'FEMALE / compatibility template only'
    draw.text((18,y),label,font=font,fill='#e3cf43')
    for col,facing in enumerate(['south','east','north','west']):
        im=Image.open(p/f"assembled-{'east' if facing=='west' else facing}.png").convert('RGBA')
        if facing=='west':im=ImageOps.mirror(im)
        bg=Image.new('RGBA',(512,1024),'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,512)),(16+col*284,y+36));draw.text((16+col*284,y+560),facing.upper()+(' (MIRROR)' if facing=='west' else ''),font=font,fill='#e3cf43')
draw.text((18,1290),'One item over unclothed fixed bases. Actual state/pose acceptance follows full-set generation.',font=font,fill='#e5e8d8');out.save(HERE/'body-fittings-comparison.png');write(HERE/'fittings.json',record)
reason='Reviewed both current fitting logs and registrations: actual Argyve ordinary Hand/1 plus explicitly separate female compatibility. Full canonical jaw/shaft material identical, common physical mapping verified, source palette and counterweight-description uncertainty retained. No new generation, native test or named outfit acceptance claimed.'
for step,action in [('resolve_item_identity_description_palette','Resolve actual armlength hooked Wrench, native head y/shaft c, inherited base handedness and counterweighted text without inventing an added weight.'),('verify_every_body_fitting_log','Reconcile both individually generation-ready fitting logs, full sources, palm ownership, directional displays, actual/compatibility scopes and equal physical item size.')]:
    e['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,action=action,inputs=[x['current_registration']['model'] for x in fits]+[ref(p/'weapon-metadata.json') for p in folders],outputs=[ref(HERE/'fittings.json'),ref(HERE/'body-fittings-comparison.png')],review=reason,result='PASS'))
e.update(status='UNFINISHED',generation_ready=True,current_step='record_item_acceptance_from_all_fittings',art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(HERE/'fittings.json'),plate=ref(HERE/'body-fittings-comparison.png')),registration_summary='Authoring index for the same armlength hooked Wrench: captured Argyve male offhand and female compatibility. Fixed bodies, complete canonical material and common physical scale. Native offhand/pose/named outfit remain pending.',native_acceptance='Pending complete requested generation set and integrated native acceptance.')
next_id='FIT-NIMA-FLOATING-GLOWSPHERE-FLOATING-NEARBY-0';next_e=next(x for x in d['entries'] if x['id']==next_id);next_e.update(status='IN PROGRESS',current_step='source_identity_description_slot_laterality')
d.update(active_entry=next_id,updated_at=datetime.now(timezone.utc).isoformat());assert [x['id'] for x in d['entries'] if x['status']=='IN PROGRESS']==[next_id]
write(f,d);print('Wrench authoring aggregate ready; only Nima floating Glowsphere fitting is active.')
