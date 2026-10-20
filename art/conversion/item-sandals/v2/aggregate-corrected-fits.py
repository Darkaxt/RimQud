"""Reconcile each individually corrected sandal fitting, without new generation."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
f=ROOT/'evidence/conversion-ledger.json';d=json.loads(f.read_text());assert d['active_entry']=='ITEM-SANDALS'
entry=next(e for e in d['entries'] if e['id']=='ITEM-SANDALS')
fits=[next(e for e in d['entries'] if e['id']==ident) for ident in entry['related_entries']]
assert len(fits)==4 and all(e['generation_ready'] and e['art_review']['status']=='PASS' for e in fits)
source=ROOT/'art/conversion/fit-human-female-sandals/v3'
packet=json.loads((source/'source-packet.json').read_text())
record=dict(item='Sandals',workflow='regional-curved-v1',source=packet['item'],
    supersedes=ref(HERE.parent/'v1/fittings.json'),
    scope='All four enumerated ordinary Feet/0 fittings separately corrected/reviewed after v1 profile-height and v2 rear-ankle-width rejection. Source/refinement reused truthfully; original bodies, full item sources and late ownership remain separate.',
    structural_correction=dict(profile='Continuous bands span upper foot contour to sole.',ankles='Curved front/rear bands span both ankle edges on actual fixed feet; target body-specific coverage checked.',context=ref(source/'refined-red-context.png'),inspection=ref(source/'first-refinement-structural-review.json')),
    fittings=[],palette='Native sole y / strap detail w. Body C in overview is illustrative and independent.',
    limits='Generation readiness only. Individual mutations, complete outfits and native acceptance remain pending the full-set gate. No new ImageGen or native test performed for aggregation.')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
out=Image.new('RGB',(1280,1030),'#142823');draw=ImageDraw.Draw(out)
draw.text((20,14),'SANDALS / corrected foot-height straps and full-width ankle bands',font=font,fill='#e3cf43')
draw.text((20,42),'One current item on fixed bases. Native y/w; body C illustrative. Native acceptance pending.',font=font,fill='#e5e8d8')
for row,e in enumerate(fits):
    registration=e['current_registration'];model_file=ROOT/registration['model']['path']
    assert ref(model_file)==registration['model'] and '/v3/' in registration['model']['path']
    model=json.loads(model_file.read_text());directory=model_file.parent
    art_source=source if e['id']=='FIT-NIMA-SANDALS-FEET-0' else directory
    review=json.loads((directory/'authoring-review.json').read_text());assert review['status']=='PASS'
    if e['id']!='FIT-NIMA-SANDALS-FEET-0':
        assert all(v['uncovered_ankle_pixels']==0 for face in review['ankle_span_checks'].values() for v in face.values())
    else:
        assert review['shared_pixels_unchanged'] and model['actual_equipped_binding']['manager'] is None
    for facing,rows in model['views'].items():
        for component in rows:assert ref(ROOT/component['public_file'])['sha256']==component['sha256']
    record['fittings'].append(dict(entry=e['id'],registration=registration,authoring_review=ref(directory/'authoring-review.json'),source_packet=ref(directory/'source-packet.json'),actual_review=e['art_review']))
    y=95+row*220;draw.text((20,y),e['name']+(' / exact shared female fit' if 'NIMA' in e['id'] else ''),font=font,fill='#e3cf43')
    for col,facing in enumerate(['south','east','north','west']):
        im=Image.open(art_source/f"palette-{'east' if facing=='west' else facing}.png").convert('RGBA')
        if facing=='west':im=ImageOps.mirror(im)
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
        out.paste(bg.crop((96,800,416,960)).resize((288,144)),(20+col*315,y+35))
        draw.text((20+col*315,y+185),facing.upper()+(' (MIRROR)' if facing=='west' else ''),font=font,fill='#e3cf43')
draw.text((20,1000),'Historical rejected versions and every correction step remain in each entry process log.',font=font,fill='#e5e8d8')
out.save(HERE/'body-fittings-comparison.png');write(HERE/'fittings.json',record)
reason='Reconciled the four current v3 authoring fits individually, including corrected rear ankle span and profile foot-height coverage. Reviewed same-source material/geometry provenance, target ownership and actual Nima/Irudad ordinary Feet bindings. Historical v1/v2 rejection retained; native equipment acceptance remains pending.'
for step,action in [
 ('resolve_item_identity_description_palette','Retain actual Sandals blueprint, strapped gravel-worn shoe description, original tile and native y/w palette.'),
 ('verify_every_body_fitting_log','Read current v3 models, full sources, masks and per-body authoring reviews for all four listed fits; require corrected ankle coverage and exact shared Nima binding.'),
 ('reprocess_under_regional_curved_v1','Reconcile full sole/strap sources, late body visibility and all required facings after structural source corrections; no new generation for aggregation.')]:
    entry['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,action=action,inputs=[e['current_registration']['model'] for e in fits]+[ref(source/'first-refinement-structural-review.json')],outputs=[ref(HERE/'fittings.json'),ref(HERE/'body-fittings-comparison.png')],review=reason,result='PASS'))
entry.update(status='UNFINISHED',generation_ready=True,current_step='record_item_acceptance_from_all_fittings',art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(HERE/'fittings.json'),plate=ref(HERE/'body-fittings-comparison.png')),registration_summary='Authoring overview of four current corrected v3 ordinary Feet/0 fittings; this JSON indexes their individual registrations. Profile-height and ankle-width rejections resolved. Native/mutation acceptance pending.')
entry['apparel_workflow']['status']='GENERATION READY'
entry['known_issues']=[x for x in entry['known_issues'] if not x.startswith(('Profile straps terminate below the foot upper contour','v2 front/back ankle bands'))]
next_id='FIT-HUMAN-MALE-STEEL-UTILITY-KNIFE-HAND-2';next_e=next(e for e in d['entries'] if e['id']==next_id);next_e['status']='IN PROGRESS'
d.update(active_entry=next_id,updated_at=datetime.now(timezone.utc).isoformat())
assert [e['id'] for e in d['entries'] if e['status']=='IN PROGRESS']==[next_id]
write(f,d)
print('Four corrected fits and Sandals aggregate generation-ready; male utility knife is the only active entry.')
