"""Select dark chest wood and bright band material in fixed source geometry."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(512,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return Image.open(p).convert('RGBA')
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def select(raw,own,pattern):
    raw=np.array(raw.resize(SIZE,Image.Resampling.LANCZOS)).astype(float);area=own[:,:,3]>0;top=own[:,:,0]>127;gray=np.where(top,raw[:,:,:2].max(2),raw[:,:,:3].mean(2));spread=np.ptp(raw[:,:,:3],axis=2);stats={}
    for name,region,colors in [('wood',area&~top,spread<24),('top',area&top,(raw[:,:,0]-raw[:,:,2]>12)&(raw[:,:,1]-raw[:,:,2]>12))]:
        # Exclude displaced generated dark seams from material interiors;
        # target outline/rail ink is supplied by the fixed construction.
        known=ndimage.binary_erosion(region,iterations=3)&(raw[:,:,3]>128)&(gray>(45 if name=='wood' else 150))&(gray<250)&colors
        labels,num=ndimage.label(region);unsampled=0
        for k in range(1,num+1):
            comp=labels==k
            if not (known&comp).any():gray[comp]=pattern[:,:,:3].mean(2)[comp];known|=comp;unsampled+=int(comp.sum())
        unknown=region&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(region.shape,-1,np.int32);ids[uy,ux]=np.arange(n);degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
        for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<768)&(nx>=0)&(nx<512));q=q[region[ny[q],nx[q]]];degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
        if n:gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree),rhs)
        stats[name]=dict(selected=int(known.sum())-unsampled,continued=n,unsampled_constructed_pixels=unsampled)
    ink=pattern[:,:,:3].mean(2);gray[area&(ink<120)]=ink[area&(ink<120)];assert np.isfinite(gray[area]).all();v=np.uint8(np.clip(np.round(gray),0,255));v[~area]=0
    return Image.fromarray(np.dstack([v,v,v,own[:,:,3]])),stats
