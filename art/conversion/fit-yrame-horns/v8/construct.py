"""Yrame horn correction: embedded roots, round volume and explicit skull clearance.

One local authoring construction. Fixed original body pixels and frame; no game
or renderer change. The skull proxy is an authored fit aid, not native anatomy.
"""
from pathlib import Path
from datetime import datetime, timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
from scipy.ndimage import binary_erosion
from scipy.interpolate import CubicSpline, PchipInterpolator
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(768,1152)
FACES=['south','east','north'];OLD=HERE.parent/'v5'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def image(p):return Image.open(p).convert('RGBA')
def norm(im):
 a=np.array(im);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
assert not (HERE/'fit-contract.json').exists(),'Preserve observed attempts'
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='FIT-YRAME-HORNS-HEAD-0'
previous=read(OLD/'fit-contract.json');body=read(ROOT/previous['body']['path']);assert ref(ROOT/previous['body']['path'])==previous['body']
now=datetime.now(timezone.utc).isoformat()
contract=dict(entry=l['active_entry'],recorded_at=now,body=previous['body'],frame=previous['frame'],native_facts=previous['native_facts'],
 user_interpretation='Symmetric sheep/ram-like grooved horns; preserve this selected interpretation rather than replace it with straight spikes.',
 rejection=ref(OLD/'independent-critical-review.md'),
 intermediate_manual_review=ref(HERE.parent/'v6/independent-manual-review.json'),
 intermediate_clearance_correction=ref(HERE.parent/'v6/clearance-correction-plan.json'),
 rejected_v7=ref(HERE.parent/'v7/independent-review-decision.json'),
 root='Full roots start inside the skull at X+/-45,Y151,Z45, radius17. Initial stem grows upward/outward through the anterior-lateral crown; original head occludes the buried portion. Actual visual emergence must be reviewed, not assumed from proxy depth.',
 curl='Compact thick ram curl: rise outward from crown, sweep backward then downward around lateral skull, return forward and upward to a short tapered point. X, Y and Z vary independently. Posterior broad sweep can hide the anterior short return in north; south shows that return in front of the back sweep. No threadlike second spiral.',
 skull_proxy=dict(center=[0,185,25],radii=[90,90,70],meaning='Authored ellipsoid fitted to existing S/E/N head contours, not native skull coordinates. Used for item/body depth only; original head pixels remain authoritative.'),
 projection=dict(south='screen384+X,125+relativeY; camera+Z',east='screen470+Z,143+relativeY; camera+X',north='screen384-X,141+relativeY; camera-Z',registration='Y uses the same125 reference; E/N add18/16px to match unchanged source head landmarks. Common physical scale; no per-facing bounds fit.'),
 views=dict(south='Anterior emerging roots visible at upper lateral crown; short forward return crosses in front of posterior descending sweep. Coil stays mainly beside the skull. Original flesh ears remain separate.',
 east='Full compact loop rises from anterior upper crown, sweeps screen-left/back, drops around lateral skull then turns forward/up into a short point above the ear. Far horn may be hidden. Buried root has no exposed cap.',
 north='Anterior root interiors are behind skull. Posterior broad descending sweep is nearest and hides the overlapping forward return; no copied frontal tip laid over the back sweep. Visible root exit must join crown without a floating end.',
 west='Mirror east geometry and depth for symmetric Head288/0 item; no source/body scale or binding change.'),
 gates=['Check complete manual views and root/return closeups before refinement.','Fresh independent review after each contextual refinement, before extraction or fitting.','Numerical clearance is diagnostic; visible attachment and flow must also pass.'])
write(HERE/'fit-contract.json',contract)
packet=read(OLD/'source-packet.json');packet.update(recorded_at=now,fit_contract=ref(HERE/'fit-contract.json'),previous_attempt=ref(OLD/'generation-receipt.json'),correction='Reject v7 planar mirrored curl and excessive tube-to-thread taper. Reconstruct compact nonplanar ram curl with physical anterior return/posterior sweep occlusion; retain full source and fixed head.');write(HERE/'source-packet.json',packet)

# X lateral, Y downward, Z forward. Compact ram-like coil around the
# lateral skull, with an outward-growing axis rather than one yawed flat spiral.
# Coordinates and thickness are authored, not inferred native joint coordinates.
control=np.array([[45,151,45],[68,126,53],[87,100,48],[105,82,5],
 [115,105,-55],[118,163,-70],[122,210,-25],[124,197,25],
 [118,166,35],[116,160,25]],float)
length=np.r_[0,np.cumsum(np.linalg.norm(np.diff(control,axis=0),axis=1))]
samples=np.linspace(0,length[-1],240)
centers=CubicSpline(length,control,axis=0)(samples)
arcs=np.r_[0,np.cumsum(np.linalg.norm(np.diff(centers,axis=0),axis=1))]
fraction=arcs/arcs[-1]
radius=PchipInterpolator(length,[17,17,18,18,17,15,13,10,5,.05])(samples)
verts=[];normals=[];parameters=[];triangles=[];ring=32
for side_sign in [-1,1]:
 c=centers.copy();c[:,0]*=side_sign;tangent=np.gradient(c,axis=0);tangent/=np.linalg.norm(tangent,axis=1)[:,None]
 a=np.cross(tangent,[1.,0,0]);a/=np.linalg.norm(a,axis=1)[:,None];b=np.cross(tangent,a);offset=len(verts)
 for j,point in enumerate(c):
  for k in range(ring):
   angle=k*2*np.pi/ring;n=a[j]*np.cos(angle)+b[j]*np.sin(angle);verts.append(point+n*radius[j]);normals.append(n);parameters.append(fraction[j])
 for j in range(len(c)-1):
  for k in range(ring):
   p=offset+j*ring+k;q=offset+j*ring+(k+1)%ring;triangles.extend([[p,q,p+ring],[q,q+ring,p+ring]])
verts=np.array(verts);normals=np.array(normals);parameters=np.array(parameters);triangles=np.array(triangles)
skullcenter=np.array([0,185,25]);skullradii=np.array([90,90,70]);q=np.sum(((verts-skullcenter)/skullradii)**2,axis=1)
# Root emergence is intentionally embedded. Everything after the early rising
# crown section must be physically outside the skull, including every return tip.
nonroot=parameters>.25;clearance=dict(nonroot_minimum_ellipsoid_q=float(q[nonroot].min()),nonroot_vertices_inside_proxy=int((q[nonroot]<1).sum()),root_start_ellipsoid_q=float(np.sum(((centers[0]-skullcenter)/skullradii)**2)),threshold='q<1 inside; q=1 surface; q>1 outside. Diagnostic only.')
assert clearance['nonroot_vertices_inside_proxy']==0, 'Non-root physical clearance unresolved'
write(HERE/'volume.json',dict(centerline=centers.tolist(),radius=radius.tolist(),cross_section_vertices=ring,control_points=control.tolist(),radius_at_control=[17,17,18,18,17,15,13,10,5,.05],skull_proxy=contract['skull_proxy'],clearance=clearance))

def render(f):
 scale=2;w,h=768,420
 if f=='south':xy=np.stack([384+verts[:,0],verts[:,1]],1);dep=verts[:,2];n=normals
 elif f=='north':xy=np.stack([384-verts[:,0],verts[:,1]+16],1);dep=-verts[:,2];n=np.stack([-normals[:,0],normals[:,1],-normals[:,2]],1)
 else:xy=np.stack([470+verts[:,2],verts[:,1]+18],1);dep=verts[:,0];n=normals[:,[2,1,0]]
 xy*=scale;depth=np.full((h*scale,w*scale),-np.inf);gray=np.zeros_like(depth);param=np.zeros_like(depth)
 light=np.array([-.4,-.6,.7]);light/=np.linalg.norm(light)
 for ids in triangles:
  if f=='east' and verts[ids,0].mean()<0:continue
  p=xy[ids];lo=np.maximum(np.floor(p.min(0)).astype(int),0);hi=np.minimum(np.ceil(p.max(0)).astype(int)+1,[w*scale,h*scale]);x0,y0=lo;x1,y1=hi
  if np.any(hi<=lo):continue
  xx,yy=np.meshgrid(np.arange(x0,x1)+.5,np.arange(y0,y1)+.5);den=(p[1,1]-p[2,1])*(p[0,0]-p[2,0])+(p[2,0]-p[1,0])*(p[0,1]-p[2,1])
  if abs(den)<1e-8:continue
  aa=((p[1,1]-p[2,1])*(xx-p[2,0])+(p[2,0]-p[1,0])*(yy-p[2,1]))/den
  bb=((p[2,1]-p[0,1])*(xx-p[2,0])+(p[0,0]-p[2,0])*(yy-p[2,1]))/den;cc=1-aa-bb;zz=aa*dep[ids[0]]+bb*dep[ids[1]]+cc*dep[ids[2]];region=depth[y0:y1,x0:x1];keep=(aa>=0)&(bb>=0)&(cc>=0)&(zz>region)
  if not keep.any():continue
  nn=aa[:,:,None]*n[ids[0]]+bb[:,:,None]*n[ids[1]]+cc[:,:,None]*n[ids[2]];nn/=np.maximum(np.linalg.norm(nn,axis=2)[:,:,None],1e-8)
  t=aa*parameters[ids[0]]+bb*parameters[ids[1]]+cc*parameters[ids[2]];grooves=np.maximum(np.cos(t*2*np.pi*19),0)**18
  tone=165+55*np.maximum((nn*light).sum(2),0)-23*grooves;region[keep]=zz[keep];gray[y0:y1,x0:x1][keep]=tone[keep];param[y0:y1,x0:x1][keep]=t[keep]
 occupied=np.isfinite(depth);edge=occupied&~binary_erosion(occupied,iterations=5);gray[edge]=35
 # Curved skull depth at every ray, replacing the previous constant depth24.
 xx,yy=np.meshgrid((np.arange(w*scale)+.5)/scale,(np.arange(h*scale)+.5)/scale)
 if f=='east':a=(xx-495)/70;b=(yy-203)/90;head_depth=90*np.sqrt(np.maximum(1-a*a-b*b,0))
 else:
  a=(xx-384)/90;b=(yy-(201 if f=='north' else 185))/90;term=1-a*a-b*b
  head_depth=(-25 if f=='north' else 25)+70*np.sqrt(np.maximum(term,0))
 footprint=(a*a+b*b)<=1;near=occupied&((depth>head_depth)|~footprint)
 rgba=np.zeros((*depth.shape,4),np.uint8);rgba[:,:,:3]=np.uint8(np.clip(gray,0,255))[:,:,None];rgba[:,:,3]=occupied*255
 def down(a):
  out=Image.new('RGBA',SIZE);out.alpha_composite(Image.fromarray(a).resize((w,h),Image.Resampling.LANCZOS));return norm(out)
 full=down(rgba);front=rgba.copy();front[~near]=0;front=down(front)
 # Store a nondestructive ownership mask, not a body-shaped hole in full art.
 fulla=np.array(full)[:,:,3].astype(float);fronta=np.array(front)[:,:,3].astype(float);weight=np.uint8(np.round(np.clip(fronta/np.maximum(fulla,1),0,1)*255))
 visible_return=int((occupied&(param>.60)&footprint&~near).sum())
 return full,weight,dict(return_vertices_occluded_in_skull_projection=visible_return,meaning='Raster samples rather than mesh vertices. Inspect visible flow as well as this diagnostic.')

font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);groups={};diagnostics={}
for f in FACES:
 full,weight,diagnostics[f]=render(f);full.save(HERE/f'intact-manual-{f}.png');Image.fromarray(weight).save(HERE/f'near-ownership-{f}.png')
 base=Image.new('RGBA',SIZE)
 for row in sorted(body['views'][f],key=lambda x:x['layer']):base.alpha_composite(image(ROOT/row['public_file']))
 base.save(HERE/f'original-body-{f}.png');fa=np.array(full);near=fa.copy();near[:,:,3]=np.uint8(np.round(fa[:,:,3].astype(float)*weight/255));far=fa.copy();an=near[:,:,3].astype(float); af=fa[:,:,3].astype(float);far[:,:,3]=np.uint8(np.round(np.divide(255*(af-an),255-an,out=np.zeros_like(af),where=an<255)))
 # Full item remains independent. Split planes are diagnostic only at this point.
 assembly=Image.alpha_composite(Image.alpha_composite(norm(Image.fromarray(far)),base),norm(Image.fromarray(near)));assembly.save(HERE/f'manual-assembly-{f}.png');groups[f]=assembly
 red=np.array(base);lum=red[:,:,:3].mean(2);red[:,:,0]=np.uint8(np.maximum(lum,48));red[:,:,1]=np.uint8(lum*.065);red[:,:,2]=np.uint8(lum*.065);red[red[:,:,3]==0,:3]=0
 context=Image.alpha_composite(Image.alpha_composite(norm(Image.fromarray(far)),Image.fromarray(red)),norm(Image.fromarray(near)));context.save(HERE/f'red-context-{f}.png')
write(HERE/'clearance-diagnostics.json',dict(geometry=clearance,projections=diagnostics,limits='Proxy and sample tests support visual inspection; they do not prove anatomy or visual acceptance.'))
plate=Image.new('RGB',(1200,490),'#142823');draw=ImageDraw.Draw(plate);draw.text((15,12),'COMPACT RAM CURL / anterior return and posterior sweep; manual proposal',font=font,fill='#e3cf43')
sheet=Image.new('RGBA',(1200,400))
for i,(f,im) in enumerate(groups.items()):
 bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);box=(310,0,670,360) if f=='east' else (204,0,564,360);plate.paste(bg.crop(box).convert('RGB'),(i*400+20,45));draw.text((i*400+20,425),f.upper(),font=font,fill='#e3cf43')
 box=(290,0,690,400) if f=='east' else (184,0,584,400);sheet.alpha_composite(image(HERE/f'red-context-{f}.png').crop(box),(i*400,0))
draw.text((15,465),'Fixed bare head and shared physical frame; manual review pending; no production registration',font=font,fill='#e5e8d8');plate.save(HERE/'manual-head-comparison.png');sheet.save(HERE/'manual-context-turnaround.png')
entry=next(e for e in l['entries'] if e['id']==l['active_entry']);entry['process_log'].append(dict(timestamp=now,step='construct_and_overlay_one_item',action='Construct compact nonplanar ram curls with substantial taper and explicit forward-return/posterior-sweep overlap. Preserve full roots and fixed body; correct alpha partition for diagnostic layering.',inputs=[previous['body'],ref(OLD/'independent-critical-review.md')],outputs=[ref(HERE/p) for p in ['construct.py','fit-contract.json','source-packet.json','volume.json','clearance-diagnostics.json','manual-head-comparison.png','manual-context-turnaround.png']],review='Manual views and numerical clearance diagnostics produced; visual inspection pending before any contextual refinement.',result='REQUIRES REVIEW'));l['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',l)
print(json.dumps(clearance,indent=2));print('Manual construction created; no new ImageGen call or registration yet.')
