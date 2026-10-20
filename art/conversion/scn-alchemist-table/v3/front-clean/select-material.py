"""Remove material-transfer streaks while retaining the same refined front source."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image
HERE=Path(__file__).resolve().parent;SOURCE=HERE.parent;ROOT=SOURCE.parents[3]
assert not (HERE/'selected-front-context.png').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
raw=np.array(Image.open(SOURCE/'refined-front-raw.png').convert('RGBA').resize((512,768),Image.Resampling.LANCZOS)).astype(float)
mask=np.array(Image.open(SOURCE/'ownership-south.png').convert('RGBA'));pattern=np.array(Image.open(SOURCE/'constructed-south.png').convert('RGBA'));envelope=mask[:,:,3]>0;glass=envelope&(mask[:,:,0]>32);gray=raw[:,:,:3].mean(2);neutral=np.ptp(raw[:,:,:3],axis=2)<20;cyan=(raw[:,:,1]-raw[:,:,0]>5)&(raw[:,:,2]-raw[:,:,0]>5);counts={}
for name,area,colors in [('wood',envelope&~glass,neutral),('glass',glass,cyan|(neutral&(raw[:,:,:3].min(2)>180)))]:
    known=ndimage.binary_erosion(area,iterations=1)&colors&(raw[:,:,3]>96)&(gray>115)&(gray<245)
    labels,nlabels=ndimage.label(area);unsupported=0
    for lab in range(1,nlabels+1):
        component=labels==lab
        if not (known&component).any():gray[component]=pattern[:,:,:3].mean(2)[component];known|=component;unsupported+=int(component.sum())
    unknown=area&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(area.shape,-1,np.int32);ids[uy,ux]=np.arange(n);degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
    for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
        ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<768)&(nx>=0)&(nx<512));q=q[area[ny[q],nx[q]]];degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
    if n:gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree),rhs)
    assert np.isfinite(gray[area]).all();counts[name]=dict(selected_interior=int(known.sum())-unsupported,continued=int(unknown.sum()),tiny_unsampled_geometry_pixels=unsupported)
ink=pattern[:,:,:3].mean(2);outline=envelope&(ink<110);gray[outline]=ink[outline];v=np.uint8(np.clip(np.round(gray),0,255));v[~envelope]=0;base=Image.fromarray(np.dstack([v,v,v,mask[:,:,3]]));base.save(HERE/'selected-front-neutral.png')
detail=base.copy();detail.putalpha(Image.fromarray(np.uint8(np.round(mask[:,:,3].astype(float)*mask[:,:,0]/255))));a=np.array(detail);a[a[:,:,3]==0,:3]=0;detail=Image.fromarray(a);detail.save(HERE/'selected-front-detail.png');a=np.array(detail);a[:,:,:3]=np.uint8(np.round(a[:,:,:3]*np.array([119,191,207])/255));context=Image.alpha_composite(base,Image.fromarray(a));context.save(HERE/'selected-front-context.png')
sheet=Image.new('RGBA',(2048,768));sheet.paste(context,(0,0))
for i,f in enumerate(['east','north','west'],1):sheet.paste(Image.open(SOURCE/f'constructed-{f}.png').convert('RGBA'),(i*512,0))
sheet.save(HERE/'front-guided-turnaround-input.png')
now=datetime.now(timezone.utc).isoformat();record=dict(timestamp=now,supersedes=ref(SOURCE/'selected-front-context.png'),same_refinement=ref(SOURCE/'refined-front-raw.png'),defect='Nearest-pixel continuation and sampled generated outlines left streaks at the fixed glass/wood boundary.',correction='Select brighter same-material interior, complete excluded boundaries harmonically, restore fixed manual dark contour. Keep all source coverage and glass ownership; no new generation or shifted geometry.',material_counts=counts,new_imagegen_calls=0)
(HERE/'material-correction.json').write_bytes((json.dumps(record,indent=2)+'\n').encode());p=ROOT/'evidence/conversion-ledger.json';d=json.loads(p.read_text());assert d['active_entry']=='SCN-ALCHEMIST-TABLE';e=next(e for e in d['entries'] if e['id']==d['active_entry']);e['process_log'].append(dict(timestamp=now,step='extract_register_color_coverage',action=record['defect']+' '+record['correction'],inputs=[ref(SOURCE/'refined-front-raw.png'),ref(SOURCE/'selected-front-context.png')],outputs=[ref(HERE/'material-correction.json'),ref(HERE/'selected-front-context.png'),ref(HERE/'front-guided-turnaround-input.png')],review='Initial transfer retained as superseded evidence. Same raw material and fixed alpha remain; clean front becomes the guide for actual secondary-view refinement.',result='PASS'));p.write_bytes((json.dumps(d,indent=2)+'\n').encode());print('Cleaned source-material selection; no new ImageGen call or structural/camera change.')
