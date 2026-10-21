"""One explicit swept horn volume, orthographic facings and depth ownership.

Local Yrame authoring construction, not a runtime renderer. No body pixels move.
The previous 2D ribbon had no front/back surface or depth at its returning tip.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
SIZE=(768,1152); FACES=['south','east','north']; OLD=HERE.parent/'v4'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def image(p):return Image.open(p).convert('RGBA')
def norm(a):a=np.array(a);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
now=datetime.now(timezone.utc).isoformat()
assert not (HERE/'fit-contract.json').exists() or ((HERE/'rejected-root-depth/rejection.json').exists() and not (HERE/'context-refinement-raw.png').exists()), 'Preserve observed attempts before correction'
l=read(ROOT/'evidence/conversion-ledger.json')
previous_active='SCN-RANDOM-BOTTLE'
for e in l['entries']:
 if e['id']==previous_active:e['status']='UNFINISHED'
 if e['id'] in ['FIT-YRAME-HORNS-HEAD-0','ITEM-HORNS','NPC-WARDEN-YRAME']:
  e.update(generation_ready=False,status='IN PROGRESS' if e['id']=='FIT-YRAME-HORNS-HEAD-0' else 'UNFINISHED',known_issues=['Back horn curl repeats front projection; physical surface/depth reversal not established.'])
  e['art_review']=dict(status='REQUIRES CORRECTION',reason=e['known_issues'][0])
  e['process_log'].append(dict(timestamp=now,step='reopen_rear_curl_structure',action='User identified repeated front-facing curl in rear view. Retain previous outputs/reviews as superseded evidence; reopen horn fit, aggregate and dependent outfit only.',inputs=[ref(OLD/'model.json')],outputs=[],result='FAIL',review='Manual front/back ribbon projection was identical apart from root translation; north was placed wholly behind the skull. Root continuity did not prove a coherent rear curl.'))
l.update(active_entry='FIT-YRAME-HORNS-HEAD-0',updated_at=now)
write(ROOT/'evidence/conversion-ledger.json',l)
old=read(OLD/'fit-contract.json');body=read(ROOT/old['body']['path']);assert ref(ROOT/old['body']['path'])==old['body']
contract=dict(entry=l['active_entry'],recorded_at=now,body=old['body'],frame=old['frame'],native_facts=old['native_facts'],
 authored_estimate='Ram-like backward curl; 3D tube, root separation, lateral splay and skull depth are authored estimates, not native joint coordinates.',
 previous_attempt=ref(OLD/'authoring-review.json'),previous_active_entry=previous_active,
 geometry='One shared tapered round tube. X lateral, Y down, Z forward. Starts at paired upper anterolateral crown; rises then sweeps towards negative Z (back). Returning tip turns forward above ears. Cross sections retain volume, and camera rotation reverses near/far tube surfaces.',
 depth='Intact item retained. Source volume determines near/far ownership; original skull separates anterior roots from posterior arc. Masks are derived only after full item drawing, without changing the bare head or adding ears.',
 views=dict(south='Upper anterior crown roots visible. Posterior arc is farther away; inner returning tip has its own self-occlusion. Original flesh ears stay below the coil.',
 east='Root above/forward of original ear. Initial arc rises and sweeps screen-left towards back, then returns forward. Exact right profile, common scale; far horn overlaps near horn.',
 north='Anterior roots are behind original skull. Posterior tube arc is nearer than the skull and overlaps its upper sides. Returning tip can be concealed by that nearer tube surface; never paste the front inner spiral onto the rear. No bone ear.',
 west='Mirror east for the symmetric natural paired item; same binding Head288/0, no independent enlargement.'),
 acceptance='Inspect self-occlusion, rear surface, root depth and tip visibility in manual and first refined views before registration. A similar symmetric silhouette alone is neither proof of error nor proof of coherence.')
write(HERE/'fit-contract.json',contract)
packet=read(OLD/'source-packet.json');packet.update(recorded_at=now,fit_contract=ref(HERE/'fit-contract.json'),previous_attempt=ref(OLD/'model.json'),correction=contract['geometry']);write(HERE/'source-packet.json',packet)

# Keep the selected side-curve proportions. Add the missing circular cross-section
# and lateral depth; do not swap an unrelated rear silhouette into the item.
segments=np.array(old['shared_segments'],float)
points=[]
for p in segments:
 for t in np.linspace(0,1,28,endpoint=False):points.append((1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3])
points=np.vstack([points,segments[-1,-1]])-np.array([510,143])
fraction=np.linspace(0,1,len(points));radius=(30*(1-fraction)**.7+.7)/2
vertices=[];normals=[];params=[];faces=[]
for side in [-1,1]:
 u,v=points.T
 center=np.stack([side*(40-u*.38),v,u+40],1)
 tangent=np.gradient(center,axis=0);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
 # Tube section normals span the plane perpendicular to the centerline.
 a=np.cross(tangent,np.array([1.,0,0]));a/=np.linalg.norm(a,axis=1)[:,None];b=np.cross(tangent,a)
 offset=len(vertices)
 for j,c in enumerate(center):
  for k in range(24):
   theta=k*2*np.pi/24;n=a[j]*np.cos(theta)+b[j]*np.sin(theta)
   vertices.append(c+n*radius[j]);normals.append(n);params.append(fraction[j])
 for j in range(len(center)-1):
  for k in range(24):
   p=offset+j*24+k;q=offset+j*24+(k+1)%24;r=p+24;s=q+24
   faces.extend([[p,q,r],[q,s,r]])
verts=np.array(vertices);norms=np.array(normals);params=np.array(params);faces=np.array(faces)
write(HERE/'volume.json',dict(axes='X lateral / Y down / Z forward',centerline_east=points.tolist(),radius=radius.tolist(),section_vertices=24,lateral_splay=.38,root_half_separation=40,root_forward_depth=40,depth_head_surface=24,reason='Shared tube defines visibility and shading in all views, replacing flat front/back ribbons.'))

def render(facing):
 # Small head frame at 2x, z-buffered surfaces; physical output frame unchanged.
 scale=2;w,h=768,420
 if facing=='east':xy=np.stack([470+verts[:,2],143+verts[:,1]],1);depth=verts[:,0];nn=norms[:,[2,1,0]]
 elif facing=='north':xy=np.stack([384-verts[:,0],141+verts[:,1]],1);depth=-verts[:,2];nn=np.stack([-norms[:,0],norms[:,1],-norms[:,2]],1)
 else:xy=np.stack([384+verts[:,0],125+verts[:,1]],1);depth=verts[:,2];nn=norms
 xy*=scale;z=np.full((h*scale,w*scale),-np.inf);gray=np.zeros(z.shape);surface=np.zeros(z.shape)
 light=np.array([-.4,-.6,.7]);light/=np.linalg.norm(light)
 for ids in faces:
  # Near horn alone in strict profile; the matching far horn is completely occluded.
  if facing=='east' and verts[ids,0].mean()<0:continue
  p=xy[ids];x0,y0=np.maximum(np.floor(p.min(0)).astype(int),0);x1,y1=np.minimum(np.ceil(p.max(0)).astype(int)+1,[w*scale,h*scale])
  if x1<=x0 or y1<=y0:continue
  xx,yy=np.meshgrid(np.arange(x0,x1)+.5,np.arange(y0,y1)+.5)
  den=(p[1,1]-p[2,1])*(p[0,0]-p[2,0])+(p[2,0]-p[1,0])*(p[0,1]-p[2,1])
  if abs(den)<1e-8:continue
  aa=((p[1,1]-p[2,1])*(xx-p[2,0])+(p[2,0]-p[1,0])*(yy-p[2,1]))/den
  bb=((p[2,1]-p[0,1])*(xx-p[2,0])+(p[0,0]-p[2,0])*(yy-p[2,1]))/den;cc=1-aa-bb
  zz=aa*depth[ids[0]]+bb*depth[ids[1]]+cc*depth[ids[2]];region=z[y0:y1,x0:x1]
  keep=(aa>=0)&(bb>=0)&(cc>=0)&(zz>region)
  if not keep.any():continue
  n=aa[:,:,None]*nn[ids[0]]+bb[:,:,None]*nn[ids[1]]+cc[:,:,None]*nn[ids[2]];n/=np.maximum(np.linalg.norm(n,axis=2)[:,:,None],1e-8)
  t=aa*params[ids[0]]+bb*params[ids[1]]+cc*params[ids[2]]
  grooves=np.maximum(np.cos(t*2*np.pi*14),0)**16
  tone=165+55*np.maximum((n*light).sum(2),0)-26*grooves
  region[keep]=zz[keep];gray[y0:y1,x0:x1][keep]=tone[keep];surface[y0:y1,x0:x1][keep]=n[:,:,2][keep]
 from scipy.ndimage import binary_erosion
 occupied=np.isfinite(z);edge=occupied&~binary_erosion(occupied,iterations=3)
 gray[edge]=35;rgba=np.zeros((*z.shape,4),np.uint8);rgba[:,:,:3]=np.uint8(np.clip(gray,0,255))[:,:,None];rgba[:,:,3]=occupied*255
 out=Image.new('RGBA',SIZE);out.alpha_composite(Image.fromarray(rgba).resize((w,h),Image.Resampling.LANCZOS))
 # Average only finite depth samples in each output pixel. This masks depth,
 # not the source contour, and does not infer skull shape from equipment slots.
 zz=np.where(occupied,z,0).reshape(h,scale,w,scale).sum((1,3));count=occupied.reshape(h,scale,w,scale).sum((1,3));zz/=np.maximum(count,1)
 near=np.zeros((SIZE[1],SIZE[0]),bool);near[:h]=zz>24 if facing!='east' else count>0
 return norm(out),near

font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
groups={}
for f in FACES:
 horn,near=render(f);horn.save(HERE/f'intact-manual-{f}.png');Image.fromarray(near.astype('uint8')*255).save(HERE/f'near-ownership-{f}.png')
 base=Image.new('RGBA',SIZE)
 for r in sorted(body['views'][f],key=lambda r:r['layer']):base.alpha_composite(image(ROOT/r['public_file']))
 a=np.array(horn);far=a.copy();far[near]=0;front=a.copy();front[~near]=0
 assembly=Image.alpha_composite(Image.alpha_composite(Image.fromarray(far),base),Image.fromarray(front));assembly.save(HERE/f'manual-assembly-{f}.png');groups[f]=assembly
 base.save(HERE/f'original-body-{f}.png')
 red=np.array(base);lum=red[:,:,:3].mean(2);red[:,:,0]=np.uint8(np.maximum(lum,48));red[:,:,1]=np.uint8(lum*.065);red[:,:,2]=np.uint8(lum*.065);red[red[:,:,3]==0,:3]=0
 context=Image.alpha_composite(Image.alpha_composite(Image.fromarray(far),Image.fromarray(red)),Image.fromarray(front));context.save(HERE/f'red-context-{f}.png')
def plate(images,name,title):
 out=Image.new('RGB',(1200,490),'#142823');d=ImageDraw.Draw(out);d.text((16,12),title,font=font,fill='#e3cf43')
 for i,(f,im) in enumerate(images.items()):
  bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);box=(330,0,650,360) if f=='east' else (224,0,544,360);out.paste(bg.crop(box).convert('RGB'),(i*400+40,45));d.text((i*400+40,425),f.upper(),font=font,fill='#e3cf43')
 d.text((16,460),'One volume / original bare head fixed / full independent bone / authoring only',font=font,fill='#e5e8d8');out.save(HERE/name)
plate(groups,'manual-head-comparison.png','VOLUME CONSTRUCTION / rear surface and tip occlusion reverse with the camera')
sheet=Image.new('RGBA',(1200,400))
for i,f in enumerate(FACES):
 box=(307,0,707,400) if f=='east' else (184,0,584,400);sheet.alpha_composite(image(HERE/f'red-context-{f}.png').crop(box),(i*400,0))
sheet.save(HERE/'manual-context-turnaround.png')
write(HERE/'manual-review.json',dict(status='REQUIRES VISUAL REVIEW',contract=ref(HERE/'fit-contract.json'),construction=ref(HERE/'volume.json'),evidence=ref(HERE/'manual-head-comparison.png'),claim='No generated refinement yet. Front/back depth is now calculated from one volume, not duplicated ribbon art.'))
print('Reopened three dependent entries; constructed one horn volume with per-view self-occlusion. Manual review pending.')
