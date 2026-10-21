"""Calibrate a head fitting proxy to actual body silhouettes, not an ellipsoid."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter1d
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-yrame/v3/registered-v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
images={f:np.array(Image.open(BODY/f'head-{f}.png'))[:,:,3]>128 for f in ['south','east','north']}
rows=[]
for y in range(94,268):
    ext={}
    for f,off in [('south',0),('east',18),('north',16)]:
        x=np.where(images[f][y+off])[0]
        if not len(x):break
        ext[f]=(float(x.min())-.5,float(x.max())+.5)
    if len(ext)!=3:continue
    s,e,n=ext['south'],ext['east'],ext['north']
    xmin=((s[0]-384)+(384-n[1]))/2;xmax=((s[1]-384)+(384-n[0]))/2
    rows.append([y,(xmin+xmax)/2,(xmax-xmin)/2,(e[0]+e[1])/2-470,(e[1]-e[0])/2])
rows=np.array(rows,float)
for col in range(1,5):rows[:,col]=gaussian_filter1d(rows[:,col],.7)
control=dict(recorded_at=datetime.now(timezone.utc).isoformat(),body_model=ref(BODY/'model.json'),source_head_images=[ref(BODY/f'head-{f}.png') for f in images],axes='X lateral, Y down, Z forward; Blender (X,-Z,-Y)/100',columns=['Y','X center','X radius','Z center','Z radius'],cross_sections=rows[::2].tolist(),method='Elliptical cross-sections constrained by actual south/north lateral extents and east fore/aft extents in the shared registered frame. Boundary samples smoothed0.7px; no body pixels changed.',limits='A silhouette-calibrated head-only fit proxy with authored intermediate depth. Not full 3D anatomy or a full recipient-body replica. Ear/nose depth within the silhouette is inferred.',diagnostic_comparison={'old_ellipsoid':{'center':[0,185,25],'radii':[90,90,70]},'actual_Y150':{'south_bounds':[317,451],'east_bounds':[432,574]},'mapping':'E x=470+Z, y=Y+18. Original 2D head/ears stay authoritative.'})
(HERE/'head-proxy-controls.json').write_text(json.dumps(control,indent=2)+'\n',encoding='utf-8',newline='\n')
print('Saved body-bound head proxy controls from all three accepted silhouettes.')
