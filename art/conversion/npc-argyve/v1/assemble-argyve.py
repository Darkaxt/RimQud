"""Assemble captured Argyve519 from current shared body and five independent equipped fits."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(512,1024);CONTACT=[256,950]
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def private(p):return dict(path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'model.json').exists();ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());entry=next(e for e in ledger['entries'] if e['id']=='NPC-ARGYVE');assert ledger['active_entry']==entry['id']
sources=json.loads((ROOT/'art/village/sources.json').read_text());assert sources['runtime_catalogue_sha256']==entry['metadata']['source_snapshot'];row=next(r for r in sources['actors'] if r['creature']=='Argyve');actor=next(a for a in row['native_instances'] if a['instance']==519);assert actor['parts']==entry['metadata']['native_parts'];assert actor['species']=='human' and actor['gender']=='male'
dependencies={};lineage=[]
for ident in entry['related_entries']:
 d=next(e for e in ledger['entries'] if e['id']==ident);assert d.get('generation_ready');r=d['current_registration']['model'];p=ROOT/r['path'];assert ref(p)['sha256']==r['sha256'];m=json.loads(p.read_text());dependencies[ident]=(m,r)
 for rows in m['views'].values():
  for component in rows:
   p=ROOT/component['public_file'];assert ref(p)['sha256']==component['sha256'];assert component['size']==list(SIZE) and component['contact']==CONTACT
 lineage.append(dict(entry=ident,model=r,plate=d['current_registration']['plate'],report='docs/conversion-entries/'+ident+'.html',reused_generation_evidence=d['process_log'],new_imagegen_calls=0))
body,bodyref=dependencies['BODY-HUMAN-MALE'];fits=[(ident,m,r) for ident,(m,r) in dependencies.items() if ident!='BODY-HUMAN-MALE'];equipped={p['equipped']['blueprint']:(p,p['equipped']) for p in actor['parts'] if p.get('equipped')};assert set(equipped)=={m['blueprint'] for _,m,_ in fits};assert len(equipped)==5
for ident,m,r in fits:
 part,item=equipped[m['blueprint']];assert (m['slot'],m['laterality'])==(part['type'],part['laterality']);assert m['family']=='human-male'
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def rgb(code):return np.frombuffer(bytes.fromhex(palette[(code or '&w').replace('&','').replace('^','')[0]]),dtype=np.uint8)
def tint(im,color):
 a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*color[None,None,:]/255));a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def rows_for(m,facing):
 if facing in m['views']:return m['views'][facing],False
 assert facing=='west';return m['views']['east'],True
def loadrow(r,mirror=False):
 im=read(ROOT/r['public_file']);return ImageOps.mirror(im) if mirror else im
def item_layer(m,facing,colored=False):
 rows,mirror=rows_for(m,facing);p=next(r for r in rows if r['component']=='item');a=np.array(loadrow(p,mirror)).astype(float);alpha=a[:,:,3]/255
 detail=next((r for r in rows if r['component']=='item-detail'),None);d=np.array(loadrow(detail,mirror)).astype(float) if detail else np.zeros_like(a);da=np.minimum(d[:,:,3]/255,alpha)
 _,native=equipped[m['blueprint']];pc=rgb(native.get('tileColor') or native['foreground']) if colored else np.array([255,255,255]);dc=rgb(native.get('detailColor') or native.get('tileColor') or native['foreground']) if colored else np.array([255,255,255])
 premul=(a[:,:,:3]*pc[None,None,:]/255*(alpha-da)[:,:,None]+d[:,:,:3]*dc[None,None,:]/255*da[:,:,None]);out=np.zeros_like(a,dtype=np.uint8);out[:,:,:3]=np.uint8(np.clip(np.round(np.divide(premul,alpha[:,:,None],out=np.zeros_like(premul),where=alpha[:,:,None]>0)),0,255));out[:,:,3]=np.uint8(np.round(alpha*255))
 # Late ownership on the current item only: never redraw a whole-body overlay above unrelated gear.
 overlay=next((r for r in rows if r['component']=='body-overlay'),None)
 if overlay:
  b=np.array(loadrow(overlay,mirror))[:,:,3].astype(float)/255;out[:,:,3]=np.uint8(np.round(out[:,:,3].astype(float)*(1-b)));out[out[:,:,3]==0,:3]=0
 return Image.fromarray(out),p['layer'],dict(rows=rows,mirrored_from_east=mirror,late_body_ownership=overlay,primary_palette=native.get('tileColor') or native['foreground'],detail_palette=native.get('detailColor') or native['foreground'])
def compose(facing,colored=False,enabled=None):
 chosen=[m for _,m,_ in fits if enabled is None or m['blueprint'] in enabled];behind=[];foreground=[];worn=[];bindings=[]
 for m in chosen:
  layer,depth,binding=item_layer(m,facing,colored);bindings.append(dict(blueprint=m['blueprint'],slot=m['slot'],laterality=m['laterality'],**binding))
  if m['slot']=='Hand':(behind if depth<0 else foreground).append(layer)
  else:worn.append(({'Body':0,'Feet':1,'Face':2}[m['slot']],layer))
 canvas=Image.new('RGBA',SIZE)
 for im in behind:canvas.alpha_composite(im)
 rows,mirror=rows_for(body,facing)
 for r in rows:
  im=loadrow(r,mirror);canvas.alpha_composite(tint(im,rgb(actor.get('tileColor') or actor['foreground'])) if colored else im)
 for _,im in sorted(worn,key=lambda x:x[0]):canvas.alpha_composite(im)
 for im in foreground:canvas.alpha_composite(im)
 return canvas,bindings
views={};groups={k:{} for k in ['base','worn','full-neutral','full-native','hidden']}
for facing in ['south','east','north','west']:
 for label,colored,enabled in [('base',False,[]),('worn',False,['Pocketed Vest','Telescopic Monocle','Sandals']),('full-neutral',False,None),('full-native',True,None)]:
  im,bindings=compose(facing,colored,enabled);im.save(HERE/f'{label}-{facing}.png');groups[label][facing]=im
  if label=='full-neutral':views[facing]=dict(body=rows_for(body,facing)[0],body_mirror=(facing=='west'),equipment=bindings,assembled_preview=ref(HERE/f'{label}-{facing}.png'))
  if label=='full-native':views[facing]['native_palette_preview']=ref(HERE/f'{label}-{facing}.png')
 hidden=Image.new('RGBA',SIZE);hidden.save(HERE/f'hidden-{facing}.png');groups['hidden'][facing]=hidden
write(HERE/'dependency-lineage.json',dict(dependencies=lineage,rule='Reuse the exact accepted-for-authoring body and item models with their actual original/reference/manual/refinement/patch/extraction logs. No new race body, profession pose, costume or ImageGen call.'))
qud=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Creatures.xml');native_definition=re.search(r'<object\s+Name="Argyve"[^>]*>.*?</object>',qud.read_text(encoding='utf-8-sig'),re.S).group();original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Argyve');mask=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/original['reference_file'].replace('-reference','-mask');assert private(mask)['sha256']==original['native_mask_sha256']
packet=dict(entry=entry['id'],captured_actor={k:v for k,v in actor.items() if k!='parts'},identity_chain=row['lineage'],race_description=row['race_input'],source_snapshot=entry['metadata']['source_snapshot'],source=ref(ROOT/'art/village/sources.json'),catalogue=ref(ROOT/'evidence/joppa-creature-catalogue.json'),native_definition=dict(**private(qud),object=native_definition),original=dict(**original,private_mask=private(mask)),runtime_parts=actor['parts'],mutation_boundary='Retained attached tree is ordinary Humanoid; no extra limb attachment captured. Active mutation list was not fully exported; eyebrow prose is uncertain, not proof of physical mutation. Do not invent extra limbs.',age='No explicit age/life-stage established; captured adult male body family is authoring selection, no demographic change.',cosmetic_boundary='Per authoritative A4/user scope, hair/eyes/beards/personal overlays postponed beyond initial conversion. Argyve beard/eyebrow/scrap description retained, not baked into shared body or fabricated as equipment.',dependencies=[dict(entry=i,model=r) for i,(m,r) in dependencies.items()],equipped=[dict(part_id=p['id'],parent=p['parent'],slot=p['type'],laterality=p['laterality'],item=it,fit_entry=next(i for i,m,r in fits if m['blueprint']==it['blueprint'])) for p,it in equipped.values()],assembly_contract=dict(canvas=list(SIZE),contact=CONTACT,geometry='Original body/head and full item pixels retained; only composition and late ownership applied. No rescale or position change.',ownership='Body first, source-declared far-hand gear behind body, worn vest/footwear/monocle in disjoint regions, near-hand gear above outfit. Each item applies only its own body-overlay alpha at composition; no full-body redraw above other equipment.',color='Captured body c; actual item TileColor overrides foreground; independent per-item primary/detail. One coverage for primary/detail within item, no copied whole-outfit body tint.',weapon_pose='Existing stationary authoring display fits only; no ready/drafted/resting acceptance claimed. Authoritative spec assigns item-specific grip/angle/depth/native pose review to integrated Stage3 after all-generation gate; no new Qud drafting mechanic.',native_visibility='Hidden previews show no actor layers; native visibility/hurt/look/save and held-state behavior remain untested behind full-generation gate.'),native_activation=False,native_acceptance='Pending integrated Stage3 after all156generation entries: actual visibility/equip-unequip/near-far hand/resting-ready/hurt/look/save-load. This packet is authoring only.')
write(HERE/'source-packet.json',packet);model=dict(entry=entry['id'],kind='captured_actor_layered_assembly',actor=packet['captured_actor'],source=ref(HERE/'source-packet.json'),body_model=bodyref,equipment_models=[dict(entry=i,model=r,slot=m['slot'],laterality=m['laterality'],equipped_instance=equipped[m['blueprint']][1]['instance'],part_id=equipped[m['blueprint']][0]['id']) for i,m,r in fits],views=views,registration=body['registration'],assembly_contract=packet['assembly_contract'],cosmetic_boundary=packet['cosmetic_boundary'],native_activation=False,native_acceptance=packet['native_acceptance']);write(HERE/'model.json',model)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(label,title):
 out=Image.new('RGB',(1152,680),'#142823');d=ImageDraw.Draw(out);d.text((18,15),title,font=font,fill='#e3cf43')
 for i,(f,im) in enumerate(groups[label].items()):
  thumb=im.resize((256,512),Image.Resampling.LANCZOS);out.paste(thumb,(16+i*284,55),thumb);d.text((16+i*284,585),f.upper(),font=font,fill='#e3cf43')
 d.text((18,625),'Captured five-item outfit; body/items separate. Personal cosmetics outside initial scope; native acceptance pending.',font=font,fill='#e5e8d8');out.save(HERE/f'{label}-comparison.png')
for label,title in [('base','ARGYVE / reused unmutated human-male body, no occupation pose'),('worn','ARGYVE / actual vest + monocle + sandals / no held-item occlusion'),('full-neutral','ARGYVE / all5captured items / neutral layers / stationary display'),('full-native','ARGYVE / actual c body and independent captured item palettes'),('hidden','ARGYVE / hidden actor contribution is empty / authoring only')]:plate(label,title)
out=Image.new('RGB',(1152,680),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'ARGYVE / same south assembly, one actual item group at a time',font=font,fill='#e3cf43')
stages=[('BODY',[]),('VEST',['Pocketed Vest']),('WORN',['Pocketed Vest','Telescopic Monocle','Sandals']),('FULL',None)]
for i,(label,enabled) in enumerate(stages):
 im,_=compose('south',True,enabled);im=im.resize((256,512),Image.Resampling.LANCZOS);out.paste(im,(16+i*284,55),im);d.text((16+i*284,585),label,font=font,fill='#e3cf43')
d.text((18,625),'No outfit baked into body. Held items preserve captured hand/laterality and selected physical size.',font=font,fill='#e5e8d8');out.save(HERE/'assembly-stages.png')
small=Image.new('RGB',(720,510),'#142823');d=ImageDraw.Draw(small);d.text((18,15),'ARGYVE / intended-size neutral and captured palettes',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north','west']):
 for j,label in enumerate(['full-neutral','full-native']):
  im=groups[label][f].resize((48,96),Image.Resampling.LANCZOS);small.paste(im,(i*180+65,60+j*195),im);large=im.resize((72,144),Image.Resampling.NEAREST);small.paste(large,(i*180+50,60+j*195+100),large)
 d.text((i*180+20,475),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-comparison.png')
a=np.array(read(mask));r=a[:,:,:1].astype(float)/255;fg=rgb(actor['foreground']);dc=rgb(actor['detailColor']);originalim=Image.fromarray(np.dstack([np.uint8(np.round((1-r)*fg+r*dc)),a[:,:,3]]));out=Image.new('RGB',(1400,880),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'ARGYVE519 > human/male baseline + five captured fitted items > layered assembly',font=font,fill='#e3cf43')
for im,x,y,size in [(originalim,40,85,(192,288)),(groups['base']['south'],350,65,(224,448)),(groups['full-neutral']['south'],700,65,(224,448)),(groups['full-native']['south'],1040,65,(224,448))]:
 im=im.resize(size,Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);out.paste(im,(x,y),im)
for x,label in [(25,'ORIGINAL SOURCE'),(325,'SHARED BODY'),(670,'NEUTRAL OUTFIT'),(1000,'CAPTURED PALETTES')]:d.text((x,555),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Exact runtime Humanoid tree, actor519/parts315..328 and5items recorded; no age or eyebrow mutation inferred.', 'Body and each item reuse logged original/RimWorld reference/manual/ImageGen/refinement/patch/extraction evidence.', 'Vest518 Body315; monocle587 Face317; knife588 Hand320/2; wrench590 Hand322/1; sandals521 Feet326.', 'Body/item pixels and contact256,950 unchanged. West mirrors symmetric assets; monocle uses explicit west model.', 'Hair/beard/eyes/personal overlays explicitly postponed by A4; item-specific ready/resting native pose review after generation.', 'This is stationary body/outfit authoring, not native equip/visibility/hurt/look/save acceptance or a new generation call.']):d.text((18,625+35*i),line,font=font,fill='#e5e8d8')
out.save(HERE/'source-to-assembly.png');print('Assembled captured Argyve519/five items/all4views with independent palettes and local late ownership; review pending.')
