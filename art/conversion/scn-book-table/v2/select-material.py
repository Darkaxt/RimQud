"""Select wood/top material in fixed512x768 geometry; no AI isolation."""
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
        known=ndimage.binary_erosion(region,iterations=3)&(raw[:,:,3]>128)&(gray>150)&(gray<250)&colors
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
if __name__=='__main__':
    assert not (HERE/'selected-front-neutral.png').exists()
    own=np.array(read(HERE/'ownership-south.png'));master,stats=select(read(HERE/'refined-front-raw.png'),own,np.array(read(HERE/'constructed-south.png')));master.save(HERE/'selected-front-neutral.png');a=np.array(master);weight=own[:,:,0].astype(float)/255;a[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-weight[:,:,None])+weight[:,:,None]*np.array([1,.95,.4])));Image.fromarray(a).save(HERE/'selected-front-context.png');write(HERE/'front-material-selection.json',dict(material=stats,coverage='Exact constructed coverage and role ownership; generated glow and geometry excluded.',sampling='Whole generated portrait frame maps once to512x768; no independent component bounds fitting. Same-material continuation only; constructed dark ink retained.'))
    sheet=Image.new('RGBA',(1536,768));sheet.alpha_composite(Image.fromarray(a),(0,0))
    for i,f in enumerate(['east','north'],1):sheet.alpha_composite(read(HERE/f'constructed-{f}.png'),(i*512,0))
    sheet.save(HERE/'front-guided-turnaround.png')
    (HERE/'turnaround-prompt.txt').write_text('''Use case: sketch-to-render. Same Qud low Book Table in three cardinal map views. Image1 is the edit target:1536x768canvas, three equal512x768columns. LEFT SOUTH is the selected refined front; center EAST and right NORTH are exact shared-geometry proposals. Image2 is actual VTE EndTable_east, only a wood/map-camera reference. Keep selected front design and refine the side/back to match it.
Retain exact parallel rectangular tabletop planes, depth8 versus front width13.6, low housing/rail and short feet. Keep all current positions, proportions, pivots and common scale. No converging top edges, three-quarter yaw, sheared body, thin end-on profile or independent bounds fitting. South has exactly two side-by-side drawer fronts and rectangular recessed pulls. EAST is a complete plain end panel, NORTH a blank rear panel with fine seam. Do not copy drawers or pulls onto side/back. No additional drawer, knobs, books, papers, lamp, contents, open-state or puzzle mechanism. Puzzle-box identity uses precise modest joinery only.
Gray wood body and muted-gold tabletop including its edge remain separate material roles. Restrained wood grain and low-relief shading, clean dark contour; no elaborate ornament or sheen. Same1536x768frame and unchanged geometry. Transparent background/support gaps; no glow/shadow/scene/text/labels. No second object or variant designs.''',encoding='utf-8')
    print('Selected front material; prepared fixed-frame front-guided end/back refinement.')
