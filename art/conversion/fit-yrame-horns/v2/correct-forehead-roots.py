"""Correct profile attachment to match the selected paired forehead roots."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SOURCE=HERE.parent/'v1';SIZE=(512,1152)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
    import numpy as np
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
path=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(path.read_text());fit=next(e for e in ledger['entries'] if e['id']=='FIT-YRAME-HORNS-HEAD-0');aggregate=next(e for e in ledger['entries'] if e['id']=='ITEM-HORNS')
assert ledger['active_entry']=='SCN-ALCHEMIST-TABLE'
next(e for e in ledger['entries'] if e['id']==ledger['active_entry']).update(status='UNFINISHED',current_step=None)
now=datetime.now(timezone.utc).isoformat()
for e in [fit,aggregate]:
    e.update(generation_ready=False,status='UNFINISHED',art_review=dict(status='REQUIRES REWORK',reason='User identified inconsistent horn roots: front forehead versus side attachment in the profile. Match all views to the selected paired forehead roots.'))
    e['process_log'].append(dict(timestamp=now,step='recompose_check_cuffs_attachment_occlusion_all_views' if e is fit else 'verify_every_body_fitting_log',action='Withdraw prior horn authoring readiness after user identified inconsistent anatomical root placement across facings.',inputs=[e['current_registration']['model'],e['current_registration']['plate']],outputs=[],review='The selected front shows paired forehead roots. Old profile near/far roots were too far back, suggesting a different side attachment. Preserve v1 evidence and correct the profile attachment before readiness.',result='REQUIRES REWORK'))
fit.update(status='IN PROGRESS',current_step='construct_and_overlay_one_item');ledger.update(active_entry=fit['id'],updated_at=now);path.write_bytes((json.dumps(ledger,indent=2)+'\n').encode())
old=json.loads((SOURCE/'model.json').read_text());packet=json.loads((SOURCE/'source-packet.json').read_text());packet.update(recorded_at=now,source_version=ref(SOURCE/'source-packet.json'),shared_refinement=dict(raw=ref(SOURCE/'refined-red-context.png'),prompt=ref(SOURCE/'imagegen-prompt.txt'),structural_gate=ref(SOURCE/'first-refinement-structural-review.json'),new_call=False),root_correction='Use one anatomical site: paired high forehead roots. Preserve selected south and north surfaces/depth; translate intact profile near horn51px forward and far horn40px forward so their roots project to the same forehead, not the temple.')
write('source-packet.json',packet)
controls=dict(anatomical_site='Paired high forehead, selected by front design and donor forehead attachment convention; authored estimate, not exported skull bones.',
              south=dict(near_translation=[0,0],far_translation=[0,0],roots=[[216.5,200.5],[295.5,200.5]]),
              east=dict(near_translation=[51,0],far_translation=[40,0],old_roots=[[258,201.5],[273,195.5]],roots=[[309,201.5],[313,195.5]],near_root_span=[[297,212],[321,191]],far_root_span=[[303,204],[323,187]]),
              north=dict(near_translation=[0,0],far_translation=[0,0],roots=[[216.5,200.5],[295.5,200.5]],visibility='Forehead roots hidden behind original rear head; only horns beyond the head silhouette show.'),
              west='Mirror corrected east geometry, roots and original head together; no independent root repositioning.')
write('attachment-controls.json',controls)
model=dict(old);model['views']={};model.update(source_version=ref(SOURCE/'model.json'),attachment_controls=ref(HERE/'attachment-controls.json'),anatomical_attachment=controls['anatomical_site'],policy='Independent whole near/far horns rooted in the paired high forehead in every facing. Same selected surface, bone geometry/size and original body. Separate head depth hides roots in rear; no temple-root substitution.')
groups={k:{} for k in ['assembly','palette','full','off','ownership']};palette=packet['palette'];registered={}
for f in ['south','east','north']:
    body=read(SOURCE/f'original-body-{f}.png');layers={};details={};rows=[]
    for depth in ['near','far']:
        dx,dy=controls[f][depth+'_translation']
        for stem in ['intact','detail']:
            source=read(SOURCE/f'{stem}-{depth}-{f}.png');image=source.transform(SIZE,Image.Transform.AFFINE,[1,0,-dx,0,1,-dy],Image.Resampling.NEAREST);image.save(HERE/f'{stem}-{depth}-{f}.png')
            (layers if stem=='intact' else details)[depth]=image
    near=Image.alpha_composite(layers['near'],details['near']);far=Image.alpha_composite(layers['far'],details['far']);full=Image.alpha_composite(far,near);assembly=Image.alpha_composite(Image.alpha_composite(far,body),near);off=Image.alpha_composite(body,full)
    for stem,im in [('assembled',assembly),('intact-item',full),('depth-off',off)]:im.save(HERE/f'{stem}-{f}.png')
    def color_layer(depth):return Image.alpha_composite(tint(layers[depth],tuple(bytes.fromhex(palette['primary_rgb']))),tint(details[depth],tuple(bytes.fromhex(palette['detail_rgb']))))
    colored=Image.alpha_composite(Image.alpha_composite(color_layer('far'),tint(body,(152,135,95))),color_layer('near'));colored.save(HERE/f'qud-palette-{f}.png')
    ownership=Image.alpha_composite(Image.alpha_composite(tint(layers['far'],(230,185,30)),body),tint(layers['near'],(40,165,220)))
    for key,im in [('assembly',assembly),('palette',colored),('full',full),('off',off),('ownership',ownership)]:groups[key][f]=im
    for row in old['views'][f]:
        row=dict(row);original_file=Path(row['public_file']);name=original_file.name;r=ref(HERE/name);row.update(public_file=r['path'],sha256=r['sha256'],file=row['file'].replace('-v1-','-v2-'));rows.append(row)
    model['views'][f]=rows;registered[f]=dict(body=ref(SOURCE/f'original-body-{f}.png'),roots=controls[f]['roots'],near_translation=controls[f]['near_translation'],far_translation=controls[f]['far_translation'],full_alpha_and_material_translated_together=True)
for group in groups.values():group['west (mirror)']=ImageOps.mirror(group['east'])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(images,name,title):
    out=Image.new('RGB',(1152,750),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,576)),(16+i*284,54));d.text((16+i*284,660),f.upper(),font=font,fill='#e3cf43')
    d.text((18,708),'One forehead attachment across views. Original body, horn size/material and physical frame unchanged.',font=font,fill='#e5e8d8');out.save(HERE/name)
for key,name,title in [('assembly','assembly-comparison.png','YRAME / paired forehead roots consistently projected into profile'),('palette','independent-palette-comparison.png','NATIVE PALETTE / unchanged w bone, W gold detail; body w separate'),('full','full-item-comparison.png','INTACT HORNS / same selected surface; profile attachment translated forward'),('off','depth-off-comparison.png','DEPTH OFF / full foreground-root projections before original head covers rear'),('ownership','near-far-ownership-comparison.png','DEPTH GUIDE / forehead near cyan, far gold; report colors only')]:plate(groups[key],name,title)
guide=Image.new('RGB',(1152,490),'#142823');d=ImageDraw.Draw(guide);d.text((18,14),'ONE ANATOMICAL ROOT SITE / forehead, not side of skull',font=font,fill='#e3cf43')
for i,(f,im) in enumerate(groups['assembly'].items()):
    bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);draw=ImageDraw.Draw(bg);roots=controls['east' if f.startswith('west') else f]['roots']
    if f.startswith('west'):roots=[[511-x,y] for x,y in roots]
    for x,y in roots:draw.ellipse((x-6,y-6,x+6,y+6),outline='#e3cf43',width=2)
    guide.paste(bg.crop((96,0,416,360)).convert('RGB').resize((256,288)),(16+i*284,60));d.text((16+i*284,375),f.upper(),font=font,fill='#e3cf43')
d.text((18,430),'Circles mark authored roots, including roots hidden by the rear head. Guide colors stay outside production.',font=font,fill='#e5e8d8');guide.save(HERE/'forehead-root-guide.png')
comparison=Image.new('RGB',(700,570),'#142823');d=ImageDraw.Draw(comparison);d.text((18,14),'PROFILE / old temple-like roots -> corrected forehead roots',font=font,fill='#e3cf43')
for i,(folder,label) in enumerate([(SOURCE,'V1 / superseded'),(HERE,'V2 / forehead')]):
    im=read(folder/'assembled-east.png');bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);comparison.paste(bg.crop((120,0,380,360)).convert('RGB').resize((312,432)),(18+i*350,60));d.text((18+i*350,515),label,font=font,fill='#e3cf43')
comparison.save(HERE/'profile-root-before-after.png')
small=Image.new('RGB',(560,405),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((48,108),Image.Resampling.LANCZOS);small.paste(thumb,(i*140+45,20),thumb);big=thumb.resize((96,216),Image.Resampling.NEAREST);small.paste(big,(i*140+20,150),big);d.text((i*140+4,380),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',dict(timestamp=now,shared_refinement=ref(SOURCE/'refined-red-context.png'),previous_registration=ref(SOURCE/'model.json'),reason=packet['root_correction'],views=registered,near_far_depth_unchanged=True,body_and_physical_frame_unchanged=True,new_imagegen_calls=0,second_isolation_call=False))
ledger=json.loads(path.read_text());fit=next(e for e in ledger['entries'] if e['id']=='FIT-YRAME-HORNS-HEAD-0');fit['process_log'].append(dict(timestamp=now,step='construct_and_overlay_one_item',action='User correction: keep the selected frontal high-forehead horn roots and move whole profile horns forward to the matching forehead projection.',inputs=[ref(SOURCE/'model.json'),ref(SOURCE/'refined-red-context.png')],outputs=[ref(HERE/'source-packet.json'),ref(HERE/'attachment-controls.json'),ref(HERE/'model.json'),ref(HERE/'profile-root-before-after.png'),ref(HERE/'forehead-root-guide.png')],review='Near profile horn translated51px and far40px. Their roots now project to the same high forehead instead of the mid-side of the skull. South/north and every original body pixel stay fixed; no new generation or native acceptance.',result='PASS'));path.write_bytes((json.dumps(ledger,indent=2)+'\n').encode());print('Corrected profile roots to shared forehead site; previous readiness withdrawn pending visual review.')
