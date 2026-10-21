"""Select clean interior generated specimens; retain rejected picks for evidence."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'material-specimens';assert not OUT.exists();OUT.mkdir()
raw=Image.open(HERE/'refined-raw.png').convert('RGBA');a=np.array(raw);g=a[:,:,:3].astype(float).mean(2)
settings={'metal':([642,397,735,520],24,24,105,170,13),'paper':([603,174,683,276],20,20,165,215,10),'glass':([90,343,153,383],24,20,110,168,12),'wire':([120,179,138,232],8,20,145,190,10)}
records=[]
for name,(roi,w,h,minimum,target,spread) in settings.items():
    candidates=[]
    for y in range(roi[1],roi[3]-h+1):
        for x in range(roi[0],roi[2]-w+1):
            patch=g[y:y+h,x:x+w];alpha=a[y:y+h,x:x+w,3]
            if alpha.min()<250 or patch.min()<minimum:continue
            score=abs(float(patch.mean())-target)*.25+abs(float(patch.std())-spread)
            candidates.append((score,x,y))
    assert candidates,name
    _,x,y=min(candidates);box=[x,y,x+w,y+h];crop=raw.crop(box);path=OUT/(name+'.png');crop.save(path)
    records.append(dict(material=name,source_box=box,source=dict(path='art/conversion/scn-garbage/v1/refined-raw.png',sha256=hashlib.sha256((HERE/'refined-raw.png').read_bytes()).hexdigest()),
        specimen=dict(path=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()),alpha_min=int(a[y:y+h,x:x+w,3].min()),luminance=dict(minimum=float(g[y:y+h,x:x+w].min()),mean=float(g[y:y+h,x:x+w].mean()),std=float(g[y:y+h,x:x+w].std())),
        rule='Opaque interior within manually identified same-material ROI; excludes object rim, transparent pixels and dark printed ink. Only bounded high-frequency gray residual is transferred, not source contours/labels.'))
(HERE/'material-selection.json').write_bytes((json.dumps(dict(selected=records,rejected_initial='material-specimen-boxes.json and material-specimen-review.png retained: paper had transparency/ink, metal approached border. No rejected pixels copied into production.'),indent=2)+'\n').encode())
plate=Image.new('RGB',(1100,350),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
for i,r in enumerate(records):
    im=Image.open(ROOT/r['specimen']['path']).convert('RGBA').resize((192,192),Image.Resampling.NEAREST);plate.paste(im,(25+i*275,55),im);d.text((25+i*275,270),r['material']+' '+str(r['source_box']),font=font,fill='#e3cf43')
plate.save(HERE/'selected-material-specimens.png');print(json.dumps(records,indent=2))
