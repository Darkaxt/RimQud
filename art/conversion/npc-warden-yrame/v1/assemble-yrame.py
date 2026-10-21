"""Assemble Yrame's four real equipped objects over separately authored anatomy."""
from pathlib import Path
from html import escape
import json,hashlib
import numpy as np
from PIL import Image,ImageOps,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(512,1152);FACES=['south','east','north','west']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def rgba(p):return Image.open(p).convert('RGBA')
assert not (HERE/'model.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='NPC-WARDEN-YRAME';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
source=read(ROOT/'art/village/sources.json');actor=next(a for s in source['actors'] if s['creature']=='Warden Yrame' for a in s['native_instances'] if a['instance']==515)
assert actor['parts']==entry['metadata']['native_parts']
dependencies={};lineage=[]
for ident in entry['related_entries']:
    dep=next(e for e in ledger['entries'] if e['id']==ident);assert dep['generation_ready'];mref=dep['current_registration']['model'];assert ref(ROOT/mref['path'])==mref;model=read(ROOT/mref['path'])
    for rows in model['views'].values():
        for r in rows:assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
    dependencies[ident]=(model,mref);lineage.append(dict(entry=ident,model=mref,plate=dep['current_registration']['plate'],report='docs/conversion-entries/'+ident+'.html',reused_generation_evidence=dep['process_log'],new_imagegen_calls=0))
body,bodyref=dependencies['BODY-YRAME'];r=body['views']['south'][0];unit=r['height']/1024
frame=dict(canvas=list(SIZE),contact=[256,1078],width=r['width'],height=r['height']*1152/1024,center_x=r['center_x'],center_z=r['center_z']+64*unit,
    method='Adopt existing horn canvas1152/contact1078. Copy body/mail/blade/boots RGBA at y+128; existing horn pixels stay at y+0. No resampling or physical size change.')
def normalize(rows,mirror,folder):
    folder.mkdir(parents=True,exist_ok=True);result=[]
    for r in rows:
        pad=1152-r['size'][1];assert r['size'][0]==512 and pad in [0,128] and r['contact'][1]+pad==1078
        assert r['width']==frame['width'] and abs(r['height']/r['size'][1]-unit)<1e-12
        assert abs(r['center_z']+pad/2*unit-frame['center_z'])<1e-12
        im=rgba(ROOT/r['public_file']);im=ImageOps.mirror(im) if mirror else im;out=Image.new('RGBA',SIZE);out.paste(im,(0,pad));p=folder/(r['component']+'.png');out.save(p)
        result.append(dict(**{k:v for k,v in r.items() if k not in ['file','public_file','sha256','size','contact','height','center_z','mirrored_from_east','padding_top']},file=p.name,public_file=p.relative_to(ROOT).as_posix(),sha256=ref(p)['sha256'],size=list(SIZE),contact=frame['contact'],height=frame['height'],center_z=frame['center_z'],source_component=dict(path=r['public_file'],sha256=r['sha256']),padding_top=pad,mirrored_from_east=mirror))
    return result
bodyviews={f:normalize(body['views'][f],False,HERE/'registered-body'/f) for f in FACES}
equipped={p['equipped']['blueprint']:(p,p['equipped']) for p in actor['parts'] if p.get('equipped')};assert len(equipped)==4
fits={m['blueprint']:(m,ref_) for key,(m,ref_) in dependencies.items() if key!='BODY-YRAME'};assert set(fits)==set(equipped)
registered={};bindings={}
for name,(m,mref) in fits.items():
    p,item=equipped[name];assert (p['type'],p['laterality'])==(m['slot'],m['laterality'])
    registered[name]={f:normalize(m['views'][f] if f in m['views'] else m['views']['east'],f not in m['views'],HERE/'registered-items'/name.lower().replace(' ','-')/f) for f in FACES}
    bindings[name]=dict(model=mref,instance=item['instance'],part_id=p['id'],parent=p['parent'],slot=p['type'],laterality=p['laterality'],manager=p['manager'],equipment_kind='mutation-created natural Head equipment' if name=='Horns' else 'captured equipped object')
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];color=lambda c:np.frombuffer(bytes.fromhex(palette[c.replace('&','')[0]]),dtype=np.uint8)
def primitives(name,f,native):
    rows=registered[name][f];item=equipped[name][1];result=[]
    for r in rows:
        if r['component'] not in ['item','item-near','item-far']:continue
        a=np.array(rgba(ROOT/r['public_file'])).astype(float);alpha=a[:,:,3]/255
        detail=next((d for d in rows if d['component']==r['component']+'-detail'),None)
        # Ordinary fitting detail is named item-detail; split horns use matching near/far detail.
        d=np.array(rgba(ROOT/detail['public_file'])).astype(float) if detail else np.zeros_like(a);da=np.minimum(d[:,:,3]/255,alpha)
        pc=color(item.get('tileColor') or item['foreground']) if native else np.array([255,255,255]);dc=color(item.get('detailColor') or item['foreground']) if native else np.array([255,255,255])
        premul=a[:,:,:3]*pc/255*(alpha-da)[:,:,None]+d[:,:,:3]*dc/255*da[:,:,None]
        out=np.zeros_like(a,dtype=np.uint8);out[:,:,:3]=np.uint8(np.clip(np.round(np.divide(premul,alpha[:,:,None],out=np.zeros_like(premul),where=alpha[:,:,None]>0)),0,255));out[:,:,3]=np.uint8(np.round(alpha*255))
        overlay=next((d for d in rows if d['component']=='body-overlay'),None)
        if overlay:out[:,:,3]=np.uint8(np.round(out[:,:,3].astype(float)*(1-np.array(rgba(ROOT/overlay['public_file']))[:,:,3]/255)))
        out[out[:,:,3]==0,:3]=0;result.append((Image.fromarray(out),r['layer']))
    assert result;return result
def compose(f,native=False,enabled=None):
    enabled=list(equipped) if enabled is None else enabled;far=[];worn=[];near=[]
    for name in enabled:
        for im,depth in primitives(name,f,native):
            if depth<0:far.append(im)
            elif bindings[name]['slot'] in ['Body','Feet']:worn.append(({'Body':0,'Feet':1}[bindings[name]['slot']],im))
            else:near.append(im)
    out=Image.new('RGBA',SIZE)
    for im in far:out.alpha_composite(im)
    for r in sorted(bodyviews[f],key=lambda r:r['layer']):
        im=rgba(ROOT/r['public_file'])
        if native:
            a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float).mean(2)[:,:,None]*color(actor['tileColor'])/255));a[a[:,:,3]==0,:3]=0;im=Image.fromarray(a)
        out.alpha_composite(im)
    for _,im in sorted(worn,key=lambda v:v[0]):out.alpha_composite(im)
    for im in near:out.alpha_composite(im)
    return out
groups={n:{} for n in ['base','worn','full-neutral','full-native','hidden']+list(equipped)};slug=lambda n:n.lower().replace(' ','-')
for f in FACES:
    for label,native,enabled in [('base',False,[]),('worn',False,['Chain Mail','Leather Boots','Horns']),('full-neutral',False,None),('full-native',True,None)]+[(n,False,[n]) for n in equipped]:
        im=compose(f,native,enabled);im.save(HERE/f'{slug(label)}-{f}.png');groups[label][f]=im
    im=Image.new('RGBA',SIZE);im.save(HERE/f'hidden-{f}.png');groups['hidden'][f]=im
write(HERE/'dependency-lineage.json',dict(dependencies=lineage,rule='Reuse exact five body/item histories with their actual source/reference/manual/refinement/patch/extraction events. No new ImageGen call for outfit assembly.'))
write(HERE/'assembly-source-packet.json',dict(entry=entry['id'],source=ref(ROOT/'art/village/sources.json'),source_snapshot=entry['metadata']['source_snapshot'],preflight=ref(HERE/'source-packet.json'),captured_actor=actor,body_model=bodyref,equipment_bindings=bindings,frame=frame,
    feet='Boots580 occupies changed Feet297/16 only; do not duplicate onto added Feet298/64. Separate additional legs remain unbooted.',
    horns='Horns575 is actual mutation-created Head288/0 equipment. Keep existing high-forehead near/far layers; rear roots are hidden by original head, not moved to temples.',
    pose='Blade576 retains current static Hand292/2 display. Resting/ready angle/grip/state/native motion acceptance remains integrated Stage3 after full generation.',
    colour='Each item retains its captured palette. Body uses source tileColor w; native B detail has no invented skin region, as documented on BODY-YRAME. Icy Vapor remains native natural equipment/effect metadata.',native_activation=False))
write(HERE/'model.json',dict(entry=entry['id'],kind='captured_actor_layered_assembly',source=ref(HERE/'assembly-source-packet.json'),body_model=bodyref,equipment_bindings=bindings,registration=frame,
    views={f:dict(body=bodyviews[f],equipment=[dict(name=n,**bindings[n],components=registered[n][f]) for n in equipped],neutral_preview=ref(HERE/f'full-neutral-{f}.png'),native_palette_preview=ref(HERE/f'full-native-{f}.png')) for f in FACES},
    composition='Far horn/blade pieces -> separate body/additional legs/head -> mail and original-pair boots -> near horns/blade. Local late ownership only affects its own item; no global body redraw.',
    native_activation=False,native_acceptance='Pending complete generation: actual mutation/feet/equipment/head-depth/visibility/held state/hurt/look/save and native Icy Vapor effect acceptance. Static authoring only.'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for label,group in groups.items():
    sheet=Image.new('RGB',(1152,740),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'YRAME / '+label+' / four source-equipped objects, separate anatomy',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(group.items()):
        xx=16+i*284;im=im.resize((256,576),Image.Resampling.LANCZOS);sheet.paste(im,(xx,50),im);d.line((xx+128,50,xx+128,626),fill='#a39846');d.line((xx,589,xx+256,589),fill='#75aaa0');d.text((xx,650),f.upper(),font=font,fill='#e3cf43')
    d.text((18,700),'Boots580 on Feet297 only; horns keep forehead near/far depth. Native acceptance pending.',font=font,fill='#e5e8d8');sheet.save(HERE/f'{slug(label)}-comparison.png')
sheet=Image.new('RGB',(1152,740),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'YRAME / captured outfit assembly in stages',font=font,fill='#e3cf43')
for i,(label,enabled) in enumerate([('BODY',[]),('MAIL',['Chain Mail']),('WORN',['Chain Mail','Leather Boots','Horns']),('FULL',None)]):
    im=compose('south',True,enabled).resize((256,576),Image.Resampling.LANCZOS);sheet.paste(im,(16+i*284,50),im);d.text((16+i*284,650),label,font=font,fill='#e3cf43')
d.text((18,700),'Original body and items unchanged; added leg pair remains separate and unequipped.',font=font,fill='#e5e8d8');sheet.save(HERE/'assembly-stages.png')
sheet=Image.new('RGB',(800,650),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'YRAME / 48x108 frame; neutral then actual independent palettes',font=font,fill='#e3cf43')
for j,key in enumerate(['full-neutral','full-native']):
    yy=60+j*275
    for i,(f,im) in enumerate(groups[key].items()):
        small=im.resize((48,108),Image.Resampling.LANCZOS);sheet.paste(small,(20+i*200,yy),small);large=small.resize((72,162),Image.Resampling.NEAREST);sheet.paste(large,(95+i*200,yy),large);d.text((20+i*200,yy+190),f.upper(),font=font,fill='#e3cf43')
d.text((18,620),'Same physical scale/contact. Static display only; native acceptance pending.',font=font,fill='#e5e8d8');sheet.save(HERE/'game-scale-comparison.png')
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Yrame generation lineage</title><style>body{background:#142823;color:#e5e8d8;font:18px/1.6 Georgia,serif;max-width:1100px;margin:35px auto;padding:0 20px}a{color:#e3cf43}section{border-top:1px solid #526b5c;padding:20px 0}</style><h1>Yrame: actual body and item generation history</h1><p>Exact existing versions are assembled here. No new body, costume or ImageGen call.</p>']
for dep in lineage:
    parts.append('<section><h2>'+escape(dep['entry'])+'</h2><a href="../../../../'+escape(dep['report'])+'">Full illustrated history</a><ol>')
    for event in dep['reused_generation_evidence']:
        links=' · '.join('<a href="../../../../'+escape(r['path'])+'">'+escape(Path(r['path']).name)+'</a>' for r in event.get('outputs',[]))
        parts.append('<li><strong>'+escape(event['step'])+'</strong> — '+escape(event['result'])+'<br>'+escape(event['action'])+'<br>'+links+'</li>')
    parts.append('</ol></section>')
parts.append('<p>Native acceptance remains pending.</p></html>');(HERE/'dependency-evidence.html').write_bytes(('\n'.join(parts)+'\n').encode())
print('Assembled actual four-item outfit in horn-compatible frame; individual/full visual review pending.')
