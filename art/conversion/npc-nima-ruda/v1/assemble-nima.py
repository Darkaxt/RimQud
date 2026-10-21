"""Assemble captured Nima using separate mutation/body/item art in one world frame."""
from pathlib import Path
from datetime import datetime,timezone
from html import escape
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(512,1264);PAD=240
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def rgba(p):return Image.open(p).convert('RGBA')
assert not (HERE/'model.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='NPC-NIMA-RUDA'
entry=next(e for e in ledger['entries'] if e['id']=='NPC-NIMA-RUDA')
sources=read(ROOT/'art/village/sources.json');actor=next(r for r in sources['actors'] if r['creature']=='Nima Ruda')['native_instances'][0]
assert actor['instance']==506 and actor['parts']==entry['metadata']['native_parts'] and sources['runtime_catalogue_sha256']==entry['metadata']['source_snapshot']
dependencies={};lineage=[]
for ident in entry['related_entries']:
    e=next(e for e in ledger['entries'] if e['id']==ident);assert e.get('generation_ready')
    p=ROOT/e['current_registration']['model']['path'];assert ref(p)==e['current_registration']['model'];model=read(p)
    for rows in model['views'].values():
        for r in rows:assert ref(ROOT/r['public_file'])['sha256']==r['sha256']
    dependencies[ident]=(model,e['current_registration']['model'])
    lineage.append(dict(entry=ident,model=e['current_registration']['model'],report='docs/conversion-entries/'+ident+'.html',plate=e['current_registration']['plate'],reused_generation_evidence=e['process_log'],new_imagegen_calls=0))
body,bodyref=dependencies['BODY-NIMA'];frame=body['registration'];assert frame['canvas']==list(SIZE) and frame['contact']==[256,1190]
fits=[(i,m,r) for i,(m,r) in dependencies.items() if i!='BODY-NIMA']
equipped={p['equipped']['blueprint']:(p,p['equipped']) for p in actor['parts'] if p.get('equipped')}
assert set(equipped)=={m['blueprint'] for _,m,_ in fits} and len(equipped)==5
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette']
def rgb(c):return np.frombuffer(bytes.fromhex(palette[c.replace('&','')[0]]),dtype=np.uint8)
def tint(im,primary,detail=None,weight=None):
    a=np.array(im);lum=a[:,:,:3].astype(float).mean(2);w=np.array(weight).astype(float)/255 if weight else np.zeros(lum.shape)
    c=(1-w[:,:,None])*rgb(primary)+w[:,:,None]*rgb(detail or primary)
    a[:,:,:3]=np.uint8(np.round(lum[:,:,None]*c/255));a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def rows_for(m,f):return (m['views'][f],False) if f in m['views'] else (m['views']['east'],True)
registered={};bindings={}
for ident,m,modelref in fits:
    part,item=equipped[m['blueprint']];assert (m['slot'],m['laterality'])==(part['type'],part['laterality'])
    rows_by_face={}
    for f in ['south','east','north','west']:
        rows,mirror=rows_for(m,f);padded=[]
        for r in rows:
            assert r['size']==[512,1024] and r['contact']==[256,950]
            assert abs(r['width']-frame['width'])<1e-12 and abs(r['height']/1024-frame['height']/1264)<1e-12
            assert abs(r['center_z']+120*r['height']/1024-frame['center_z'])<1e-12
            im=rgba(ROOT/r['public_file']);im=ImageOps.mirror(im) if mirror else im
            out=Image.new('RGBA',SIZE);out.paste(im,(0,PAD))
            folder=HERE/'padded-items'/m['blueprint'].lower().replace(' ','-');folder.mkdir(parents=True,exist_ok=True)
            path=folder/f'{r["component"]}-{f}.png';out.save(path)
            padded.append(dict(**{k:v for k,v in r.items() if k not in ['public_file','sha256','file','size','contact','height','center_z']},
                public_file=path.relative_to(ROOT).as_posix(),file=path.name,sha256=ref(path)['sha256'],size=list(SIZE),contact=frame['contact'],height=frame['height'],center_z=frame['center_z'],
                source_component=dict(path=r['public_file'],sha256=r['sha256']),padding_top=PAD,mirrored_from_east=mirror))
        rows_by_face[f]=padded
    registered[m['blueprint']]=rows_by_face
    bindings[m['blueprint']]=dict(entry=ident,model=modelref,equipped_instance=item['instance'],part_id=part['id'],parent_id=part['parent'],slot=part['type'],laterality=part['laterality'],manager=part['manager'])
def item_layer(name,f,colored):
    rows=registered[name][f];r=next(r for r in rows if r['component']=='item');a=np.array(rgba(ROOT/r['public_file'])).astype(float);alpha=a[:,:,3]/255
    dr=next((r for r in rows if r['component']=='item-detail'),None);d=np.array(rgba(ROOT/dr['public_file'])).astype(float) if dr else np.zeros_like(a);da=np.minimum(d[:,:,3]/255,alpha)
    item=equipped[name][1];pc=rgb(item.get('tileColor') or item['foreground']) if colored else np.array([255,255,255]);dc=rgb(item.get('detailColor') or item['foreground']) if colored else np.array([255,255,255])
    premul=a[:,:,:3]*pc[None,None,:]/255*(alpha-da)[:,:,None]+d[:,:,:3]*dc[None,None,:]/255*da[:,:,None]
    out=np.zeros_like(a,dtype=np.uint8);out[:,:,:3]=np.uint8(np.clip(np.round(np.divide(premul,alpha[:,:,None],out=np.zeros_like(premul),where=alpha[:,:,None]>0)),0,255));out[:,:,3]=np.uint8(np.round(alpha*255))
    overlay=next((r for r in rows if r['component']=='body-overlay'),None)
    if overlay:out[:,:,3]=np.uint8(np.round(out[:,:,3].astype(float)*(1-np.array(rgba(ROOT/overlay['public_file']))[:,:,3]/255)))
    out[out[:,:,3]==0,:3]=0
    return Image.fromarray(out),r['layer']
def compose(f,colored=False,enabled=None):
    enabled=list(equipped) if enabled is None else enabled
    far=[];near=[];worn=[];floating=[]
    for name in enabled:
        im,depth=item_layer(name,f,colored)
        if bindings[name]['slot']=='Hand':(far if depth<0 else near).append(im)
        elif bindings[name]['slot']=='Floating Nearby':floating.append(im)
        else:worn.append(({'Body':0,'Feet':1,'Head':2,'Face':3}[bindings[name]['slot']],im))
    out=Image.new('RGBA',SIZE)
    for im in far:out.alpha_composite(im)
    for r in body['views'][f]:
        im=rgba(ROOT/r['public_file']);w=Image.open(ROOT/r['detail_weight']['path']) if r.get('detail_weight') else None
        out.alpha_composite(tint(im,actor['detailColor'] if r.get('color_role')=='detail' else (actor.get('tileColor') or actor['foreground']),actor['detailColor'],w) if colored else im)
    for _,im in sorted(worn,key=lambda x:x[0]):out.alpha_composite(im)
    for im in near:out.alpha_composite(im)
    for im in floating:out.alpha_composite(im)
    return out
groups={name:{} for name in ['base','worn','full-neutral','full-native','hidden']+list(equipped)}
for f in ['south','east','north','west']:
    for label,colored,enabled in [('base',False,[]),('worn',False,['Leather Apron','Wide-brimmed Hat','Sandals']),('full-neutral',False,None),('full-native',True,None)]+[(name,False,[name]) for name in equipped]:
        im=compose(f,colored,enabled);im.save(HERE/f'{label.lower().replace(" ","-")}-{f}.png');groups[label][f]=im
    im=Image.new('RGBA',SIZE);im.save(HERE/f'hidden-{f}.png');groups['hidden'][f]=im
controls=read(ROOT/'art/conversion/fit-nima-pestle/v1/fit-controls.json')
anchors={f:dict(grip=[c['grip'][0],c['grip'][1]+PAD],angle=c['angle']) for f,c in controls.items()}
anchors['west']=dict(grip=[511-anchors['east']['grip'][0],anchors['east']['grip'][1]],angle=-anchors['east']['angle'])
decision=dict(captured_item=531,captured_part=181,parent_part=180,slot='Hand',laterality=6,manager='506::MultipleArms::Change',pixel_anchors=anchors,
    source_fact='Pestle531 actually occupies changed Hand181/6. Original item and fitting controls are retained; an equipment slot is not an articulated render bone.',
    authoring_decision='Retain the source-fitted ordinary-palm display on the unchanged original arm. The additional arm pair remains separate neutral art; no mechanical slot is renamed to follow a screen position.',
    unchanged='No source body/item deformation, rescale, new rig, mutation topology or gameplay state. Integer padding only.',
    pose_boundary='Static low-handle grip/display only; source-supported resting/ready/native motion and exact near/far hand acceptance remain integrated Stage3 work after full generation.')
write(HERE/'hand-attachment-decision.json',decision)
sphere=next(m for _,m,_ in fits if m['blueprint']=='Floating Glowsphere')
floatcentres={}
for f in ['south','east','north','west']:
    rr=next(r for r in registered['Floating Glowsphere'][f] if r['component']=='item');box=rgba(ROOT/rr['public_file']).getchannel('A').getbbox()
    floatcentres[f]=dict(center_px=[(box[0]+box[2])/2,(box[1]+box[3])/2],bounds=list(box))
write(HERE/'floating-attachment-decision.json',dict(captured_item=538,captured_part=195,slot='Floating Nearby',laterality=0,centres=floatcentres,
    source_binding=sphere['actual_equipped_binding'],source_state=sphere['source_state'],placement=sphere['placement'],
    distinction='Actual captured FloatingNearby195/0 is retained. AllowedParts Hand,FloatingNearby does not make this equipped object a hand weapon. Existing user-directed vertical-palm display is preserved; no orbit coordinates or physical hand grip are inferred.',
    optional_effects=sphere['authoring_effects'],optional_effects_registered_native=False,
    state_ownership='Native LightSource Lit/radius8 and AnimatedMaterialGeneric200tick color cycle remain native and untested. Snapshot Y/C palette is shown in static authoring; no new clock, lighting behavior, orbit or halo binding.'))
write(HERE/'dependency-lineage.json',dict(dependencies=lineage,rule='Reuse actual source/reference/manual/refinement/patch/extraction records; no new body, costume or ImageGen call for this assembly.'))
write(HERE/'assembly-source-packet.json',dict(entry=entry['id'],source=ref(ROOT/'art/village/sources.json'),source_snapshot=entry['metadata']['source_snapshot'],actor=actor,preflight_history=ref(HERE/'source-packet.json'),
    body_model=bodyref,equipment_bindings=bindings,registration=frame,hand_attachment=ref(HERE/'hand-attachment-decision.json'),new_imagegen_calls=0,floating_attachment=ref(HERE/'floating-attachment-decision.json'),body_palette_roles=body['palette_roles'],
    garment_ownership='Retain intact apron, hat and sandals with each original body visibility mask. Apply each only to its own item alpha at composition. Apron/hat may occlude the posterior tail root; the full spiral and additional arms remain independent body art. No global body redraw above other equipment.',native_activation=False))
write(HERE/'model.json',dict(entry=entry['id'],kind='captured_actor_layered_assembly',actor={k:v for k,v in actor.items() if k!='parts'},source=ref(HERE/'assembly-source-packet.json'),body_model=bodyref,equipment_bindings=bindings,
    views={f:dict(body=body['views'][f],equipment=[dict(**bindings[name],components=registered[name][f]) for name in equipped],neutral_preview=ref(HERE/f'full-neutral-{f}.png'),native_palette_preview=ref(HERE/f'full-native-{f}.png')) for f in groups['base']},
    registration=frame,hand_attachment=ref(HERE/'hand-attachment-decision.json'),floating_attachment=ref(HERE/'floating-attachment-decision.json'),composition='Far-held pestle, separate fixed body/mutation components with source g/w roles, apron/footwear/hat, near-held pestle, FloatingNearby glowsphere. Late body ownership local to each item; single coverage for item primary/detail.',
    native_activation=False,native_acceptance='Pending all-generation gate: real anatomy/parts/equip-unequip/visibility/hurt/look/save-load and source-supported held states. This assembly is static authoring only.'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for label,group in groups.items():
    sheet=Image.new('RGB',(1152,800),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'NIMA / '+label+' / fixed body and independent captured equipment',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(group.items()):
        thumb=im.resize((256,632),Image.Resampling.LANCZOS);x=16+i*284;sheet.paste(thumb,(x,50),thumb);d.line((x+128,50,x+128,682),fill='#a39846');d.line((x,645,x+256,645),fill='#75aaa0');d.text((x,710),f.upper(),font=font,fill='#e3cf43')
    d.text((18,755),'Static authoring. Actual Hand181/6 retained; no native pose/equipment acceptance.',font=font,fill='#e5e8d8');sheet.save(HERE/f'{label.lower().replace(" ","-")}-comparison.png')
sheet=Image.new('RGB',(1152,800),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'NIMA / captured outfit assembly, one item group at a time',font=font,fill='#e3cf43')
for i,(label,enabled) in enumerate([('BODY',[]),('APRON',['Leather Apron']),('WORN',['Leather Apron','Wide-brimmed Hat','Sandals']),('FULL',None)]):
    im=compose('south',True,enabled).resize((256,632),Image.Resampling.LANCZOS);sheet.paste(im,(16+i*284,50),im);d.text((16+i*284,710),label,font=font,fill='#e3cf43')
d.text((18,755),'The same body, separate mutations and five source items; no equipment baked into anatomy.',font=font,fill='#e5e8d8');sheet.save(HERE/'assembly-stages.png')
small=Image.new('RGB',(800,650),'#142823');d=ImageDraw.Draw(small);d.text((18,15),'NIMA / 48x119 frame; neutral then actual independent source palettes',font=font,fill='#e3cf43')
for j,label in enumerate(['full-neutral','full-native']):
    y=60+j*270
    for i,(f,im) in enumerate(groups[label].items()):
        im=im.resize((48,119),Image.Resampling.LANCZOS);small.paste(im,(i*200+20,y),im);large=im.resize((72,178),Image.Resampling.NEAREST);small.paste(large,(i*200+95,y),large);d.text((i*200+20,y+200),f.upper(),font=font,fill='#e3cf43')
d.text((18,620),'Unchanged physical body/item scale. Native acceptance pending full generation.',font=font,fill='#e5e8d8');small.save(HERE/'game-scale-comparison.png')
parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Nima conversion lineage</title><style>body{background:#142823;color:#e5e8d8;font:18px/1.6 Georgia,serif;max-width:1100px;margin:35px auto;padding:0 20px}a{color:#e3cf43}section{border-top:1px solid #526b5c;padding:20px 0}li{margin:10px 0}</style><h1>Nima: actual body and item generation history</h1><p>Every dependency below retains its actual original/reference/manual/refined/secondary/patched/extracted evidence. This NPC assembly reuses those exact versions; no new ImageGen call or costume was generated.</p>']
for dep in lineage:
    parts.append(f'<section><h2>{escape(dep["entry"])}</h2><p><a href="../../../../{escape(dep["report"])}">Full conversion report</a> · <a href="../../../../{escape(dep["model"]["path"])}">Exact model</a></p><ol>')
    for event in dep['reused_generation_evidence']:
        links=' · '.join(f'<a href="../../../../{escape(r["path"])}">{escape(Path(r["path"]).name)}</a>' for r in event.get('outputs',[]))
        parts.append(f'<li><strong>{escape(event["step"].replace("_"," "))}</strong> — {escape(event["result"])}<br>{escape(event["action"])}<br>{links}</li>')
    parts.append('</ol></section>')
parts.append('<p>Static authoring; integrated native acceptance remains pending.</p></html>');(HERE/'dependency-evidence.html').write_bytes(('\n'.join(parts)+'\n').encode())
print('Assembled five captured items over separate anatomy in the shared padded frame; visual review pending.')
