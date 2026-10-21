"""Actual third-trial cardinal evidence; no AI call or production registration."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];FACES=['south','east','north'];SIZE=(768,1152)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def rgba(p):return Image.open(p).convert('RGBA')
assert (HERE/'blender-receipt.json').exists()
bm=ROOT/'art/conversion/body-yrame/v3/registered-v2/model.json';body=read(bm)
plate=Image.new('RGB',(1200,550),'#142b24');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.text((15,12),'CURRENT BLENDER MODEL / revised upper-forehead emergence and simple rendered tones',font=font,fill='#e3ce43')
diagnostics={}
for i,face in enumerate(FACES):
    base=Image.new('RGBA',SIZE)
    for row in sorted(body['views'][face],key=lambda x:x['layer']):base.alpha_composite(rgba(ROOT/row['public_file']))
    whole=np.array(rgba(HERE/f'whole-item-{face}.png'));visible=np.array(rgba(HERE/f'visible-item-{face}.png'));a=whole[:,:,3].astype(float);n=np.minimum(visible[:,:,3],a);f=np.round(np.divide(255*(a-n),255-n,out=np.zeros_like(a),where=n<255))
    far=whole.copy();far[:,:,3]=f;near=whole.copy();near[:,:,3]=n
    im=Image.alpha_composite(Image.alpha_composite(Image.fromarray(far),base),Image.fromarray(near));im.save(HERE/f'assembly-{face}.png')
    bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);box=(290,0,690,400) if face=='east' else (184,0,584,400);plate.paste(bg.crop(box).convert('RGB'),(i*400,45));d.text((i*400+15,450),face.upper(),font=font,fill='#e3ce43')
    small=bg.resize((63,94),Image.Resampling.LANCZOS);plate.paste(small.convert('RGB'),(i*400+165,450))
    diagnostics[face]=dict(original_body=ref(bm),whole_item=ref(HERE/f'whole-item-{face}.png'),visible_item=ref(HERE/f'visible-item-{face}.png'),alpha_partition_max_rounding=float(np.max(np.abs(n+f*(1-n/255)-a))),body_repainted=False)
plate.save(HERE/'current-cardinal-comparison.png');write(HERE/'composition-diagnostics.json',diagnostics)
packet=read(HERE.parent/'blender-trial-v2/trial-contract.json');packet.update(artwork_status='UNAPPROVED CORRECTED BLENDER TRIAL',method='Direct Blender normal-based neutral tone regions + Freestyle; no ImageGen',volume=ref(HERE/'volume.json'),blender_receipt=ref(HERE/'blender-receipt.json'),required_trial_views=['south','east','north'],west='Symmetric geometry; production mirror/ownership still needs review. No separate west output claimed for this trial.',main_review='Pending actual rendered root inspection; no registration/readiness credit.')
write(HERE/'trial-contract.json',packet)
ledger=read(ROOT/'evidence/conversion-ledger.json');entry=next(e for e in ledger['entries'] if e['id']=='FIT-YRAME-HORNS-HEAD-0');now=datetime.now(timezone.utc).isoformat()
entry['process_log'].append(dict(timestamp=now,step='construct_and_overlay_one_item',action='Correct root axis/emergence in retained Blender shape controls; render three actual orthographic views with simpler Blender-native neutral tones and Freestyle contours. Keep original body unchanged and full item independent.',inputs=[ref(HERE.parent/'blender-trial-v2/main-review-decision.json'),ref(bm)],outputs=[ref(HERE/p) for p in ['volume.json','build_blender.py','horns-trial.blend','blender-receipt.json','current-cardinal-comparison.png','composition-diagnostics.json','trial-contract.json']],review='Corrected trial rendered for inspection. No ImageGen call or production registration; west remains explicitly pending.',result='REQUIRES REVIEW'));ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Third trial rendered and logged; no readiness claim.')
