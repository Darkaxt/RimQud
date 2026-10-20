"""Inspect and register the refined front before requesting the remaining views."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil
import numpy as np
from scipy import ndimage
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
assert not (HERE/'first-front-structural-review.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,d):(HERE/n).write_bytes((json.dumps(d,indent=2)+'\n').encode())
raw=Path('C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-958e1dc7-3725-455f-abe3-4461f2e6c2fc.png');shutil.copyfile(raw,HERE/'refined-front-raw.png')
now=datetime.now(timezone.utc).isoformat()
review=dict(timestamp=now,status='PASS',scope='First front refinement structural inspection before extraction',raw=ref(HERE/'refined-front-raw.png'),findings=['Wooden table, supports/brace, radial burns, left three-phial rack and tall connected coil/alembic retained.','Rectangular tabletop boundaries stay parallel; no camera yaw or converging edge replacement.','All tips/feet and glass openings remain on the complete canvas. Generated extra edge thickness/glow are not selected alpha.','Use visible neutral wood and pale-cyan glass surfaces only; preserve original constructed geometry and full-cell frame.'],native_acceptance='Not performed; full-set generation gate unchanged.')
write('first-front-structural-review.json',review)
source=Image.open(HERE/'refined-front-raw.png').convert('RGBA').resize((512,768),Image.Resampling.LANCZOS);a=np.array(source).astype(float);ownership=np.array(Image.open(HERE/'ownership-south.png').convert('RGBA'));envelope=ownership[:,:,3]>0;glass=envelope&(ownership[:,:,0]>32);wood=envelope&~glass
gray=a[:,:,:3].mean(2);known_alpha=a[:,:,3]>64
neutral=np.ptp(a[:,:,:3],axis=2)<20;cyan=(a[:,:,1]-a[:,:,0]>5)&(a[:,:,2]-a[:,:,0]>5)
known_wood=wood&known_alpha&neutral&(gray>35)&(gray<245)
known_glass=glass&known_alpha&(cyan|((a[:,:,:3].min(2)>180)&neutral))
assert known_wood.any() and known_glass.any()
unknown=np.zeros(envelope.shape,bool)
for area,known in [(wood,known_wood),(glass,known_glass)]:
    missing=area&~known;unknown|=missing;indices=ndimage.distance_transform_edt(~known,return_distances=False,return_indices=True);gray[missing]=gray[indices[0][missing],indices[1][missing]]
v=np.uint8(np.clip(np.round(gray),0,255));v[~envelope]=0;base=Image.fromarray(np.dstack([v,v,v,ownership[:,:,3]]));base.save(HERE/'selected-front-neutral.png')
detail_alpha=np.uint8(np.round(ownership[:,:,3].astype(float)*ownership[:,:,0]/255));detail=base.copy();detail.putalpha(Image.fromarray(detail_alpha));b=np.array(detail);b[b[:,:,3]==0,:3]=0;detail=Image.fromarray(b);detail.save(HERE/'selected-front-detail.png')
colored=detail.copy();b=np.array(colored);b[:,:,:3]=np.uint8(np.round(b[:,:,:3]*np.array([119,191,207])/255));colored=Image.fromarray(b);context=Image.alpha_composite(base,colored);context.save(HERE/'selected-front-context.png');Image.fromarray(np.uint8(unknown)*255).save(HERE/'front-material-continuation.png')
write('front-material-selection.json',dict(raw=ref(HERE/'refined-front-raw.png'),structural_gate=ref(HERE/'first-front-structural-review.json'),method='Resize whole source once to common512x768. Select neutral wood and cyan/white glass material inside fixed full ownership coverage; continue unmatched edge pixels from nearest same material. Preserve constructed alpha/depth, excluding generated glow and geometry changes.',known_wood=int(known_wood.sum()),known_glass=int(known_glass.sum()),continued_pixels=int(unknown.sum()),scope='Selected front authoring anchor, not native registration or acceptance.'))
sheet=Image.new('RGBA',(2048,768));sheet.paste(context,(0,0))
for i,f in enumerate(['east','north','west'],1):sheet.paste(Image.open(HERE/f'constructed-{f}.png').convert('RGBA'),(i*512,0))
sheet.save(HERE/'front-guided-turnaround-input.png')
p=ROOT/'evidence/conversion-ledger.json';d=json.loads(p.read_text());assert d['active_entry']=='SCN-ALCHEMIST-TABLE';e=next(e for e in d['entries'] if e['id']==d['active_entry'])
for step,action,names in [('refine_materials_and_form','Refine the corrected front once, inspect structure before extraction, and retain raw output/prompt.',['refine-front-prompt.txt','refined-front-raw.png','first-front-structural-review.json']),('extract_register_color_coverage','Select same front wood/glass surface into fixed source coverage; exclude generated glow/edge/body changes and retain glass highlights in glass ownership.',['selected-front-neutral.png','selected-front-detail.png','front-material-continuation.png','front-material-selection.json']),('create_front_side_back_furniture_views','Use selected corrected front plus shared wider manual geometry to guide E/N and explicit asymmetric W; all views retain one scale/pivot.',['selected-front-context.png','front-guided-turnaround-input.png','turnaround-prompt.txt'])]:
    e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'source-packet.json'),ref(HERE/'constructed-south.png')],outputs=[ref(HERE/n) for n in names],review='First front structure is usable. Same surface material is selected without a second isolation call; original rectangular camera and source identity remain authoritative. Secondary views still need actual refinement/inspection.',result='PASS'))
d['updated_at']=now;p.write_bytes((json.dumps(d,indent=2)+'\n').encode());print('Inspected refined front and prepared source-bound front-guided four-view sheet.')
