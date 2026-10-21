"""Correct the rejected disconnected manual loop before contextual generation."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys,re
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs');from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'construction-v2';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(OUT/n).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
assert not (OUT/'construction.json').exists();source=(HERE/'construction.svg').read_text();oldstrap=re.search(r'<path d="M337.*?/>',source).group(0)
strap='<path d="M358 313 L389 330 L361 366 L339 351Z" fill="url(#cloth)" stroke="#303030" stroke-width="8" stroke-linejoin="round"/><path d="M445 280 A50 60 0 1 1 345 280 A50 60 0 1 1 445 280Z M423 280 A28 37 0 1 0 367 280 A28 37 0 1 0 423 280Z" fill-rule="evenodd" fill="url(#cloth)" stroke="#303030" stroke-width="8" stroke-linejoin="round"/>'
for name in ['construction','primary-canonical','detail-canonical']:
 text=(HERE/(name+'.svg')).read_text();text=text.replace(oldstrap,strap);p=OUT/(name+'.svg');p.write_bytes(text.encode());(OUT/(name+'.png')).write_bytes(svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
base=Image.open(OUT/'construction.png').convert('RGBA');primary=Image.open(OUT/'primary-canonical.png').convert('RGBA');detail=Image.open(OUT/'detail-canonical.png').convert('RGBA');P=np.array(primary)[:,:,3].astype(float)/255;D=np.array(detail)[:,:,3].astype(float)/255;A=np.array(base)[:,:,3].astype(float)/255;W=np.divide(D*(1-P),A,out=np.zeros_like(A),where=A>0);Image.fromarray(np.uint8(np.round(W*255))).save(OUT/'detail-weight.png')
lab,n=ndimage.label(A>128/255);sizes=ndimage.sum(A>128/255,lab,range(1,n+1));assert n==1 and sizes[0]>60000,(n,sizes)
# One continuous cap/neck/body/loop, while the actual loop's center remains open.
assert A[280,395]==0 and A[350,350]>.9 and A[285,240]>.9
a=np.array(base);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*((1-W[:,:,None])*np.array([.58,.70,.47])+W[:,:,None])));a[a[:,:,3]==0,:3]=0;Image.fromarray(a).save(OUT/'refinement-input.png')
now=datetime.now(timezone.utc).isoformat();write('construction.json',dict(recorded_at=now,supersedes=ref(HERE/'construction.json'),manual=ref(OUT/'construction.svg'),source=ref(HERE/'source-packet.json'),error='Initial open C-shaped ribbon was disconnected from the round body. Rejected before ImageGen; retained as history.',correction='Closed cloth loop with a short tab entering the upper-right cloth shoulder behind the main cover. One connected physical object; loop center stays transparent.',checks=dict(connected_alpha_components=n,loop_center_open=True,cap_neck_body_continuous=True),unchanged='Round cover/central reinforcement, cap/neck, exact source cell frame and g/w material ownership remain. No long strap, jerrycan or decorative additions.'))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);out=Image.new('RGB',(1000,600),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'CANTEEN / correct structural attachment before contextual refinement',font=font,fill='#e3cf43')
for i,(path,label) in enumerate([(HERE/'refinement-input.png','REJECTED: detached hook'),(OUT/'refinement-input.png','PATCH: connected closed loop')]):
 image=Image.open(path).convert('RGBA').resize((256,384),Image.Resampling.LANCZOS);out.paste(image,(100+i*490,70),image);d.text((40+i*490,500),label,font=font,fill='#e3cf43')
d.text((18,565),'Same Qud round canteen, fixed source frame, short cloth loop and connected aluminum cap/neck.',font=font,fill='#e5e8d8');out.save(OUT/'loop-attachment-patch.png')
prompt=(HERE/'refinement-prompt.txt').read_text();prompt=prompt.replace('short attached upper-right cloth carry loop','short CLOSED upper-right cloth carry loop with its lower tab clearly joining the shoulder').replace('The upper loop stays short and attached at the upper side','The upper loop has one open center but a fully closed cloth ring and a lower tab continuous with the upper-right body shoulder; it stays short and attached at the upper side');(OUT/'refinement-prompt.txt').write_bytes(prompt.encode())
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='SCN-CANTEEN';e=next(e for e in l['entries'] if e['id']==l['active_entry']);reason='Inspected the manual full canteen and found its first carry-hook disconnected. Patched closed cloth loop into body shoulder, with open center and complete cap/neck join. Exact geometry mask now has one connected component; loop center remains transparent. Actual contextual refinement still pending.';e['process_log'].append(dict(timestamp=now,step='construct_faithful_shape',action=reason,inputs=[ref(HERE/'construction.json')],outputs=[ref(OUT/n) for n in ['construction.json','construction.svg','construction.png','refinement-input.png','loop-attachment-patch.png']],review=reason,result='PASS'));e.update(current_step='refine_materials_and_form',art_review=dict(status='REQUIRES REVIEW',reason='Patched manual source ready for actual contextual refinement.'));l['updated_at']=now;(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode());print('Patched source has one connected cap/neck/body/loop component; inspect before ImageGen.')
