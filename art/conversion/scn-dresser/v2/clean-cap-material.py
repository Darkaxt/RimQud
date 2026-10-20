"""Use cap interior material instead of importing the old sloped edge highlights."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1/registered'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert not (HERE/'cap-material-correction.json').exists()
source=np.array(Image.open(OLD/'neutral-master.png').convert('RGBA'));owner=np.array(Image.open(OLD/'cap-feet-ownership-mask.png').convert('L'));mask=(owner>127)&(source[:,:,3]>=240)&(np.indices(owner.shape)[0]<900);sy,sx=np.where(mask);lo,hi=int(sy.min())+4,int(sy.max())-4;left=np.zeros(source.shape[0]);right=left.copy()
for y in range(lo,hi+1):
    xs=np.flatnonzero(mask[y]);left[y]=xs.min()+6;right[y]=xs.max()-6
cap=np.array(Image.open(HERE/'parallel-front-cap.png').convert('RGBA'));inside=(cap[:,:,3]>0)&(np.indices(cap.shape[:2])[0]<163);ty,tx=np.where(inside);bounds=[int(tx.min()),int(ty.min()),int(tx.max()),int(ty.max())];yy,xx=np.indices((768,512));ry=lo+np.clip((yy-bounds[1])/(bounds[3]-bounds[1]),0,1)*(hi-lo);l=np.interp(ry,np.arange(len(left)),left);r=np.interp(ry,np.arange(len(right)),right);rx=l+np.clip((xx-bounds[0])/(bounds[2]-bounds[0]),0,1)*(r-l);v=ndimage.map_coordinates(source[:,:,0].astype(float),[ry,rx],order=1,mode='nearest');ink=cap[:,:,:3].mean(2);v[inside&(ink<120)]=ink[inside&(ink<120)]
a=np.array(Image.open(HERE/'selected-front-neutral.png').convert('RGBA'));before=a.copy();a[:,:,:3][inside]=np.uint8(np.round(v[inside]))[:,None];assert np.array_equal(a[:,:,3],before[:,:,3]) and np.array_equal(a[163:],before[163:]);Image.fromarray(a).save(HERE/'selected-front-neutral-clean.png');own=np.array(Image.open(HERE/'ownership-south.png').convert('RGBA'));w=own[:,:,0].astype(float)/255;context=a.copy();context[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-w[:,:,None])+w[:,:,None]*np.array([.65,.9,1])));Image.fromarray(context).save(HERE/'selected-front-context-clean.png')
sheet=Image.new('RGBA',(1536,768));sheet.alpha_composite(Image.fromarray(context),(0,0))
for i,f in enumerate(['east','north'],1):sheet.alpha_composite(Image.open(HERE/f'constructed-{f}.png').convert('RGBA'),(i*512,0))
sheet.save(HERE/'front-guided-turnaround-clean.png');record=dict(reason='Old sloped-cap edge highlights sampled at each scanline produced intermittent bright marks on new rectangular edges. Reuse opaque material interiors with6source-pixel horizontal and4vertical clearance, then retain new explicit dark perimeter.',source=ref(OLD/'neutral-master.png'),before=ref(HERE/'selected-front-neutral.png'),after=ref(HERE/'selected-front-neutral-clean.png'),composed=ref(HERE/'front-guided-turnaround-clean.png'),alpha_unchanged=True,body_below_y163_unchanged=True,new_generation=False);(HERE/'cap-material-correction.json').write_bytes((json.dumps(record,indent=2)+'\n').encode());print('Selected cap interior material; preserved alpha and lower-body pixels.')
