"""Show actual calibrated-proxy fitting and its original-silhouette correspondence."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];FACES=['south','east','north','west'];SIZE=(768,1152)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def rgba(p):return Image.open(p).convert('RGBA')
bm=ROOT/'art/conversion/body-yrame/v3/registered-v2/model.json';body=read(bm)
plate=Image.new('RGB',(1600,600),'#142b24');overlay=Image.new('RGB',(1600,490),'#142b24');d=ImageDraw.Draw(plate);od=ImageDraw.Draw(overlay);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.text((15,12),'CALIBRATED HEAD PROXY / same retained Blender horn mesh and exact full-item pixels',font=font,fill='#e3ce43');od.text((15,12),'PROXY/SOURCE SILHOUETTE / white agreement; green source-only; magenta proxy-only',font=font,fill='#e3ce43')
diagnostics={}
for i,f in enumerate(FACES):
    base=Image.new('RGBA',SIZE)
    for row in sorted(body['views'][f],key=lambda x:x['layer']):base.alpha_composite(rgba(ROOT/row['public_file']))
    whole=np.array(rgba(HERE/f'whole-item-{f}.png'));vis=np.array(rgba(HERE/f'visible-item-{f}.png'));a=whole[:,:,3].astype(float);n=np.minimum(vis[:,:,3],a);faralpha=np.round(np.divide(255*(a-n),255-n,out=np.zeros_like(a),where=n<255));far=whole.copy();far[:,:,3]=faralpha;near=whole.copy();near[:,:,3]=n
    out=Image.alpha_composite(Image.alpha_composite(Image.fromarray(far),base),Image.fromarray(near));out.save(HERE/f'assembly-{f}.png');bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(out)
    box=(290,0,690,400) if f=='east' else ((78,0,478,400) if f=='west' else (184,0,584,400));plate.paste(bg.crop(box).convert('RGB'),(i*400,45));d.text((i*400+15,450),f.upper(),font=font,fill='#e3ce43');thumb=out.resize((63,94),Image.Resampling.LANCZOS);plate.paste(thumb,(i*400+150,485),thumb)
    source=np.array(rgba(ROOT/next(r['public_file'] for r in body['views'][f] if r['component']=='head')))[:,:,3]>128;proxy=np.array(rgba(HERE/f'proxy-silhouette-{f}.png'))[:,:,3]>128
    off={'south':0,'east':18,'north':16,'west':18}[f];roi=np.zeros_like(source);roi[96+off:265+off]=True;inter=(source&proxy&roi).sum();union=((source|proxy)&roi).sum()
    upper=np.zeros_like(source);upper[96+off:170+off]=True
    diag=np.zeros((*source.shape,4),np.uint8);diag[source&proxy]=[230,230,230,255];diag[source&~proxy]=[30,220,90,255];diag[proxy&~source]=[240,30,210,255];db=Image.new('RGBA',SIZE,'#20382d');db.alpha_composite(Image.fromarray(diag));overlay.paste(db.crop(box).convert('RGB'),(i*400,45));od.text((i*400+15,450),f.upper(),font=font,fill='#e3ce43')
    diagnostics[f]=dict(silhouette_iou_Y96_265=float(inter/union),upper_root_region_iou=float((source&proxy&upper).sum()/((source|proxy)&upper).sum()),source=ref(ROOT/next(r['public_file'] for r in body['views'][f] if r['component']=='head')),proxy=ref(HERE/f'proxy-silhouette-{f}.png'),full_item_byte_reused=ref(HERE/f'whole-item-{f}.png')['sha256']==ref(HERE.parent/'blender-trial-v2'/f'whole-item-{f}.png')['sha256'],alpha_partition_max_rounding=float(np.abs(n+faralpha*(1-n/255)-a).max()))
plate.save(HERE/'calibrated-assembly-comparison.png');overlay.save(HERE/'proxy-source-comparison.png');write(HERE/'composition-diagnostics.json',diagnostics)
contract=read(HERE.parent/'blender-trial-v2/trial-contract.json');contract.update(method='Resume unchanged v2 horn meshes and exact whole-item pixels; replace ellipsoid by source-silhouette-calibrated head fit proxy.',proxy=ref(HERE/'head-proxy-controls.json'),receipt=ref(HERE/'blender-receipt.json'),artwork_status='REQUIRES VISUAL REVIEW',limits='Source silhouettes constrain cardinal bounds; intervening depth is authored. Original body stays exact. No production registration or native acceptance yet.')
write(HERE/'trial-contract.json',contract)
ledger=read(ROOT/'evidence/conversion-ledger.json');e=next(e for e in ledger['entries'] if e['id']=='FIT-YRAME-HORNS-HEAD-0');now=datetime.now(timezone.utc).isoformat();e['process_log'].append(dict(timestamp=now,step='construct_and_overlay_one_item',action='Resume retained .blend without changing horn coordinates or full-item pixels; calibrate head fit proxy to accepted front/profile/back silhouettes and render actual four-view depth ownership.',inputs=[ref(HERE.parent/'blender-trial-v2/horns-trial.blend'),ref(bm)],outputs=[ref(HERE/p) for p in ['head-proxy-controls.json','horns-fit.blend','blender-receipt.json','calibrated-assembly-comparison.png','proxy-source-comparison.png','composition-diagnostics.json','trial-contract.json']],review='Actual proxy-source silhouette correspondence and unchanged horn pixels recorded. Root appearance pending closer visual review; no generation-ready or native claim.',result='REQUIRES REVIEW'));ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print(json.dumps(diagnostics,indent=2))
