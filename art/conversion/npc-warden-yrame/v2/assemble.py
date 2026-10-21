"""Assemble current selected sources without modifying any body/item pixels."""
from pathlib import Path
from datetime import datetime,timezone
from html import escape
import hashlib,json
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];FACES=['south','east','north','west'];SIZE=(768,1152)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def image(p):return Image.open(p).convert('RGBA')
def norm(im):
 a=np.array(im);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
assert not (HERE/'authoring-review.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='NPC-WARDEN-YRAME';entry=next(e for e in l['entries'] if e['id']==l['active_entry'])
source=read(ROOT/'art/village/sources.json');actor=next(a for g in source['actors'] if g['creature']=='Warden Yrame' for a in g['native_instances'] if a['instance']==515);assert actor['parts']==entry['metadata']['native_parts']
deps={};lineage=[]
for ident in entry['related_entries']:
 e=next(e for e in l['entries'] if e['id']==ident);assert e['generation_ready'];r=e['current_registration']['model'];assert ref(ROOT/r['path'])==r;m=read(ROOT/r['path'])
 for rows in m['views'].values():
  for row in rows:assert ref(ROOT/row['public_file'])['sha256']==row['sha256']
 deps[ident]=(m,r);lineage.append(dict(entry=ident,model=r,report='docs/conversion-entries/'+ident+'.html',process_log=e['process_log'],new_imagegen_calls=0))
body,bref=deps['BODY-YRAME'];equipped={p['equipped']['blueprint']:(p,p['equipped']) for p in actor['parts'] if p.get('equipped')};assert len(equipped)==4
fits={m['blueprint']:(m,r) for k,(m,r) in deps.items() if k!='BODY-YRAME'};assert set(fits)==set(equipped)
bindings={};resolved={}
for name,(m,r) in fits.items():
 p,item=equipped[name];assert (m['slot'],m['laterality'])==(p['type'],p['laterality']);assert m['body_sha256']==bref['sha256']
 bindings[name]=dict(model=r,instance=item['instance'],part_id=p['id'],slot=p['type'],laterality=p['laterality'],manager=p['manager'])
 resolved[name]={}
 for f in FACES:
  mirror=f not in m['views'];assert not mirror or f=='west';rows=m['views']['east' if mirror else f]
  resolved[name][f]=[]
  for row in rows:
   for key in ['size','contact','width','height','center_x','center_z']:assert row[key]==body['views'][f][0][key],(name,f,key)
   resolved[name][f].append(dict(row,needs_assembly_mirror=mirror))
now=datetime.now(timezone.utc).isoformat()
contract=dict(recorded_at=now,entry=entry['id'],body=bref,equipment=bindings,frame=body['registration'],
 policy='Authoring assembly of independently reviewed current versions only. Source textures remain intact and immutable; late original-body ownership overlays use their original tint roles. No new drawing, deformation or ImageGen call.',
 views=dict(south='Mail covers connected shoulders and anterior chest drop. Near horns grow from upper crown; flesh ears remain separate. Only inner fore pair wears boots; outer hind pair stays bare. Right Hand292 is screen-left and covers its low inward blade grip.',
 east='Mail covers upright torso with curved short sleeve; fleece lower trunk remains separate. Crown roots sit above/forward of ear. Near/far fore boots overlap naturally, hind hooves bare. Blade is near, low original palm above handle.',
 north='Original skull hides anterior horn roots. Short dorsal mail ends at horizontal trunk junction. Complete fore boots and right-hand weapon remain behind the original body; visible hind pair stays bare. Right hand is screen-right.',
 west='Body, mail, boots and horn anatomy mirror east. Blade keeps the actually equipped right Hand292 and uses explicit far-side depth, so it is not moved onto the visible left hand. No independent rescaling.'),
 unknowns='Joint/skull/far-palm coordinates and garment tailoring are authored estimates. Source supports fore/hind groups and four actual equipped objects, not an ovine species identity. No tail inferred.',
 boundaries='Static source-bound generation assembly. Icy Vapor stays native metadata/effect. Resting/ready blade display, equip/unequip, visibility, hurt/look/save and native activation await full-set generation gate.')
write('assembly-contract.json',contract)
write('dependency-lineage.json',dict(dependencies=lineage,reuse='Each full illustrated dependency history is linked with exact current model hashes; no new contextual generation for an outfit assembled from usable sources.'))
packet=dict(entry=entry['id'],recorded_at=now,source=ref(ROOT/'art/village/sources.json'),captured_actor=actor,body=bref,baseline=body['baseline_model'],equipment=bindings,contract=ref(HERE/'assembly-contract.json'),
 original=read(ROOT/'art/conversion/body-yrame/v3/source-packet.json')['original'],source_body_metadata=ref(ROOT/'art/conversion/body-yrame/v3/source-packet.json'),dependency_lineage=ref(HERE/'dependency-lineage.json'),
 native_state='Not activated or tested; all native acceptance remains pending.',mutation_boundary='Selected fixed named mutation variant, separate from reusable ordinary female. No generic mutation-render framework implementation claimed.',new_imagegen_calls=0)
write('source-packet.json',packet)
pal=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette']
def color(c):return tuple(bytes.fromhex(pal[c.replace('&','')[0]]))
def tint(im,c):
 a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color(c))/255));return norm(Image.fromarray(a))
def layers(f,native,enabled):
 rows=[(r,None) for r in body['views'][f]]
 rows.extend((r,n) for n in enabled for r in resolved[n][f]);rows.sort(key=lambda pair:pair[0]['layer'])
 for r,n in rows:
  im=image(ROOT/r['public_file']);im=ImageOps.mirror(im) if r.get('needs_assembly_mirror') else im
  if native:
   role=r['color_role']
   if n and role.startswith('equipment'):
    it=equipped[n][1];c=it['detailColor'] if role=='equipment-detail' else it.get('tileColor') or it['foreground']
   else:c=actor['detailColor'] if role=='detail' else actor['tileColor'] or actor['foreground']
   im=tint(im,c)
  yield im
def compose(f,native=False,enabled=None):
 enabled=list(equipped) if enabled is None else enabled;out=Image.new('RGBA',SIZE)
 for im in layers(f,native,enabled):out.alpha_composite(im)
 return norm(out)
groups={k:{} for k in ['base','worn','full-neutral','full-native']+list(equipped)};slug=lambda n:n.lower().replace(' ','-')
for f in FACES:
 for name,native,enabled in [('base',False,[]),('worn',False,['Chain Mail','Horns','Leather Boots']),('full-neutral',False,None),('full-native',True,None)]+[(n,False,[n]) for n in equipped]:
  im=compose(f,native,enabled);im.save(HERE/f'{slug(name)}-{f}.png');groups[name][f]=im
write('model.json',dict(entry=entry['id'],kind='captured_actor_layered_assembly',source=ref(HERE/'source-packet.json'),body_model=bref,equipment_bindings=bindings,registration=body['registration'],
 views={f:dict(body=body['views'][f],equipment=[dict(name=n,**bindings[n],components=resolved[n][f]) for n in equipped],neutral_preview=ref(HERE/f'full-neutral-{f}.png'),native_palette_preview=ref(HERE/f'full-native-{f}.png')) for f in FACES},
 composition='Stable sort exact current components by recorded depth; far items, original body/head, full near items and original-body ownership overlays. Tint planes remain separate; sources are never body-cut.',native_activation=False,native_acceptance=contract['boundaries']))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(group,name,title):
 out=Image.new('RGB',(1200,620),'#142823');d=ImageDraw.Draw(out);d.text((18,15),title,font=font,fill='#e3cf43')
 for i,(label,im) in enumerate(group.items()):
  bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);out.paste(bg.resize((280,420),Image.Resampling.LANCZOS).convert('RGB'),(10+i*300,55));d.text((15+i*300,500),label.upper(),font=font,fill='#e3cf43')
 d.text((18,575),'Current exact sources; separate equipment and native palettes. Static authoring only.',font=font,fill='#e5e8d8');out.save(HERE/name)
for name,g in groups.items():plate(g,f'{slug(name)}-comparison.png','YRAME / '+name+' / current centauroid and real equipped items')
plate({k:compose('south',True,v) for k,v in [('BODY',[]),('MAIL',['Chain Mail']),('WORN',['Chain Mail','Horns','Leather Boots']),('FULL',None)]},'assembly-stages.png','YRAME / body -> steel mail -> actual fore boots and crown horns -> right-hand blade')
small=Image.new('RGB',(800,480),'#142823');d=ImageDraw.Draw(small)
for j,key in enumerate(['full-neutral','full-native']):
 for i,(f,im) in enumerate(groups[key].items()):
  thumb=im.resize((64,96),Image.Resampling.LANCZOS);small.paste(thumb,(15+i*200,20+j*230),thumb);large=thumb.resize((96,144),Image.Resampling.NEAREST);small.paste(large,(90+i*200,20+j*230),large);d.text((15+i*200,190+j*230),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-comparison.png')
orig=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/warden-yrame-reference.png');assert hashlib.sha256(orig.read_bytes()).hexdigest()==packet['original']['reference_sha256']
maskref=packet['original']['private_mask'];maskpath=Path(maskref['path']);assert hashlib.sha256(maskpath.read_bytes()).hexdigest()==maskref['sha256']
mask=np.array(image(maskpath));blend=mask[:,:,0].astype(float)/255;g=np.zeros_like(mask);g[:,:,:3]=np.uint8(np.round((1-blend[:,:,None])*np.array(color(actor['tileColor']))+blend[:,:,None]*np.array(color(actor['detailColor']))));g[:,:,3]=mask[:,:,3];glyph=norm(Image.fromarray(g));glyph.save(HERE/'original-native-glyph.png')
out=Image.new('RGB',(960,620),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'YRAME / original Qud shape and palette -> selected authored assembly',font=font,fill='#e3cf43');out.paste(glyph.resize((192,288),Image.Resampling.NEAREST),(30,150),glyph.resize((192,288),Image.Resampling.NEAREST))
for i,key in enumerate(['full-neutral','full-native']):
 im=groups[key]['south'].resize((320,480),Image.Resampling.LANCZOS);out.paste(im,(280+i*340,65),im);d.text((280+i*340,565),key.upper(),font=font,fill='#e3cf43')
out.save(HERE/'source-to-assembly.png')
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Yrame current source lineage</title><style>body{background:#142823;color:#e5e8d8;font:18px/1.6 Georgia,serif;max-width:1100px;margin:35px auto;padding:0 20px}a{color:#e3cf43}section{border-top:1px solid #526b5c;padding:20px 0}</style><h1>Yrame current body and equipment lineage</h1><p>Current exact sources and their full construction/refinement/patch histories. Static authoring assembly; native acceptance pending.</p>']
for row in lineage:
 parts.append('<section><h2>'+escape(row['entry'])+'</h2><p><a href="../../../../'+escape(row['report'])+'">Full illustrated generation evidence</a></p><p>Selected model: <a href="../../../../'+escape(row['model']['path'])+'">'+escape(row['model']['path'])+'</a><br>SHA256 '+row['model']['sha256']+'</p></section>')
parts.append('</html>');(HERE/'dependency-evidence.html').write_bytes(('\n'.join(parts)+'\n').encode())
for step,action,names in [('resolve_individual_race_and_runtime_metadata','Reconcile source human-based female mutant with selected compact fleece centauroid, actual fore/hind anatomy and separate ordinary female base.',['source-packet.json','source-to-assembly.png']),('verify_body_and_every_equipped_item_dependencies','Verify current body and all four actual equipped item models/hashes/physical frames; retain full illustrated histories and per-view contracts.',['dependency-lineage.json','dependency-evidence.html','assembly-contract.json']),('assemble_without_baking_equipment','Compose exact current layers at shared scale, retaining full garment/item sources and late original-body ownership. No redraw, warping or new ImageGen call. Review pending.',['assemble.py','model.json','base-comparison.png','chain-mail-comparison.png','horns-comparison.png','vibro-blade-comparison.png','leather-boots-comparison.png','assembly-stages.png','full-neutral-comparison.png','full-native-comparison.png'])]:
 entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[bref]+[r for _,r in fits.values()],outputs=[ref(HERE/n) for n in names],review=action,result='REQUIRES REVIEW' if step=='assemble_without_baking_equipment' else 'PASS'))
entry.update(current_step='review_anatomy_clothing_attachment_all_directions',current_registration=dict(model=ref(HERE/'model.json'),plate=ref(HERE/'full-neutral-comparison.png')),generation_ready=False,art_review=dict(status='REQUIRES REVIEW',reason='Current-version source assembly constructed; inspect complete outfit and individual components before authoring acceptance.'))
l.update(updated_at=now);(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode())
print('Current five-source Yrame assembly written. All-view outfit/palette review pending; no native validation.')
