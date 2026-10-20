"""Same-material sampling; fixed bed geometry and color ownership stay explicit."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SHAPE=(768,768)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return Image.open(p).convert('RGBA')
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def select(raw,own,pattern):
    raw=np.array(raw).astype(float);area=own[:,:,3]>0;fabric=own[:,:,0]>127
    cyan=(raw[:,:,1]-raw[:,:,0]>12)&(raw[:,:,2]-raw[:,:,0]>12)&(raw[:,:,3]>224)&(raw[:,:,:3].mean(2)>100)
    sy,sx=np.where(cyan);ty,tx=np.where(fabric);assert len(sx)>100 and len(tx)>100
    src=[int(sx.min()),int(sy.min()),int(sx.max()),int(sy.max())];dst=[int(tx.min()),int(ty.min()),int(tx.max()),int(ty.max())]
    yy,xx=np.indices(SHAPE);rx=src[0]+(xx-dst[0])*(src[2]-src[0])/(dst[2]-dst[0]);ry=src[1]+(yy-dst[1])*(src[3]-src[1])/(dst[3]-dst[1]);sample=np.stack([ndimage.map_coordinates(raw[:,:,c],[ry,rx],order=1,mode='nearest') for c in range(4)],axis=2)
    # Map material by pad landmarks only. This never moves output geometry,
    # original pivot, masks or any view bounds.
    gray=sample[:,:,:3].max(2);spread=np.ptp(sample[:,:,:3],axis=2);stats={}
    for name,region,colors in [('wood',area&~fabric,spread<24),('fabric',area&fabric,(sample[:,:,1]-sample[:,:,0]>8)&(sample[:,:,2]-sample[:,:,0]>8))]:
        known=ndimage.binary_erosion(region,iterations=2)&(sample[:,:,3]>128)&(gray>90)&(gray<250)&colors
        labels,num=ndimage.label(region);unsampled=0
        for k in range(1,num+1):
            comp=labels==k
            if not (known&comp).any():gray[comp]=pattern[:,:,:3].mean(2)[comp];known|=comp;unsampled+=int(comp.sum())
        unknown=region&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(region.shape,-1,np.int32);ids[uy,ux]=np.arange(n);degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
        for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<768)&(nx>=0)&(nx<768));q=q[region[ny[q],nx[q]]];degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
        if n:gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree),rhs)
        stats[name]=dict(selected=int(known.sum())-unsampled,continued=n,unsampled_constructed_pixels=unsampled)
    ink=pattern[:,:,:3].mean(2);gray[area&(ink<120)]=ink[area&(ink<120)];assert np.isfinite(gray[area]).all();v=np.uint8(np.clip(np.round(gray),0,255));v[~area]=0
    return Image.fromarray(np.dstack([v,v,v,own[:,:,3]])),dict(material=stats,source_fabric_landmarks=src,target_fabric_landmarks=dst,rule='Material-only affine from actual cyan-pad bounds to fixed fabric landmarks; original complete frame/geometry unchanged. Same-material harmonic continuation, constructed dark outline and explicitly counted tiny unsampled wood regions. Cyan removed with shared max-channel luminance.')
if __name__=='__main__':
    assert not (HERE/'selected-front-neutral.png').exists()
    own=np.array(read(HERE/'ownership-south.png'));master,stats=select(read(HERE/'refined-front-raw.png'),own,np.array(read(HERE/'constructed-south.png')));master.save(HERE/'selected-front-neutral.png')
    a=np.array(master);role=own[:,:,0]>127;a[:,:,:3]=np.where(role[:,:,None],a[:,:,:3].astype(float)*np.array([.65,.9,1]),a[:,:,:3]);Image.fromarray(a).save(HERE/'selected-front-context.png')
    sheet=Image.new('RGBA',(2304,768));sheet.alpha_composite(Image.fromarray(a),(0,0))
    for i,f in enumerate(['east','north'],1):sheet.alpha_composite(read(HERE/f'constructed-{f}.png'),(i*768,0))
    sheet.save(HERE/'front-guided-turnaround.png');write(HERE/'front-material-selection.json',stats)
    (HERE/'turnaround-prompt.txt').write_text('''Use case: sketch-to-render. Complete this SAME Qud hillfolk bed in three cardinal map views. Image1 is the edit target: three768x768panels on2304x768canvas. LEFT SOUTH is selected refined front; keep its design and surface. CENTER EAST is the complete horizontal long-side map view; RIGHT NORTH is the back/end-facing orientation. Image2 is the actual RimWorld VTE east bed reference ONLY for map camera and broad side footprint. No pillow, extra blanket, occupant or modern mattress.
Canonical identity: wooden slats/frame, open curved headboard with vertical bars, low foot rail, four short supports and one plain fabric pad stuffed with watervine chaff. Keep all construction geometry, correct occlusion, headboard gaps and bracket/post connections. Refine the center/right wood grain and softly stuffed fabric to match the selected left. Do not narrow the broad side view or turn it into an edge-on elevation. Keep parallel axes and exact same width/length, placement and margins; no three-quarter yaw, diagonal shear, converging edges or independently scaled bed per panel. South has headboard above; east has headboard left; north has headboard below in front of pad, hiding the appropriate pad edge. No frontal headboard pasted onto horizontal side.
Gray wood, pale cyan fabric ownership aid across all panels; cyan not final native tint. Restrain folds, no pillow/blanket division/ornate carvings/metal caps. Exactly three equal columns, same2304x768canvas, genuine transparent backdrop and open gaps. No glow, shadow, scene, text or labels.''',encoding='utf-8')
    print('Selected front material in fixed geometry; prepared front-guided E/N refinement.')
