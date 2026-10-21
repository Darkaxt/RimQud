"""Limit the profile correction to the hand's closed light interior and ink rim.

Keep already good front/back masks. A connected dark-outline component can
include adjacent body ink; using the closed hand interior avoids that ownership.
"""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];FACES=['south','east','north']


def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())


assert not (HERE/'mask-contour-refinement.json').exists()
controls={}
for f in FACES:
    base=Image.open(HERE/f'original-body-{f}.png').convert('RGBA');ba=np.array(base)
    mask=np.array(Image.open(HERE/f'body-visibility-{f}.png').convert('L'))
    if f=='east':
        x0,y0,x1,y1=480,552,577,625;crop=ba[y0:y1,x0:x1]
        light=(crop[:,:,:3].mean(2)>90)&(crop[:,:,3]>128)
        labels,n=ndimage.label(light);label=int(labels[585-y0,529-x0]);assert label>0
        interior=labels==label;assert 700<interior.sum()<3500
        distance=ndimage.distance_transform_edt(~interior)
        ink=(crop[:,:,:3].mean(2)<160)&(crop[:,:,3]>0)
        hand=interior|(ink&(distance<=8))
        ystart=557
        mask[ystart:y1,x0:x1]=np.uint8(hand[ystart-y0:])*255
        controls[f]=dict(seed=[529,585],roi=[x0,y0,x1,y1],replace_below=ystart,
                        interior_pixels=int(interior.sum()),rim_distance_limit=8,
                        method='Original closed light hand interior plus nearby original dark rim only; exclude surrounding torso/fleece light pixels.')
    else:
        controls[f]=dict(method='Retain the inspected initial curved forearm/hand mask; no correction needed.')
    mask[ba[:,:,3]==0]=0
    Image.fromarray(mask).save(HERE/f'body-visibility-ready-{f}.png')
    cloth=Image.open(HERE/f'constructed-cloth-{f}.png').convert('RGBA')
    red=ba.copy();lum=ba[:,:,:3].mean(2);red[:,:,0]=np.uint8(np.maximum(lum,48));red[:,:,1]=np.uint8(lum*.065);red[:,:,2]=np.uint8(lum*.065);red[red[:,:,3]==0,:3]=0
    for prefix,im in [('ready-neutral',base),('ready-red',Image.fromarray(red))]:
        assembled=Image.composite(im,Image.alpha_composite(im,cloth),Image.fromarray(mask))
        assembled.save(HERE/f'{prefix}-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for prefix,name in [('ready-red','ready-context-turnaround.png'),('ready-neutral','ready-neutral-turnaround.png')]:
    sheet=Image.new('RGBA',(1440,540));draw=ImageDraw.Draw(sheet)
    for i,f in enumerate(FACES):
        sheet.alpha_composite(Image.open(HERE/f'{prefix}-{f}.png').convert('RGBA').crop((144,240,624,720)),(i*480,0));draw.text((i*480+15,510),f.upper(),font=font,fill='white')
    sheet.save(HERE/name)
plate=Image.open(HERE/'source-reference-construction.png').convert('RGB');plate.paste('#142823',(0,360,1440,900));im=Image.open(HERE/'ready-neutral-turnaround.png').convert('RGBA');plate.paste(im,(0,360),im);plate.save(HERE/'ready-source-reference-construction.png')
now=datetime.now(timezone.utc).isoformat()
record=dict(recorded_at=now,reason='First patch followed connected dark hand ink into nearby body ink. Keep original good front/back masks; refine only profile hand ownership from its closed light interior and original rim.',
            previous=ref(HERE/'hand-ownership-correction.json'),body_and_cloth_unchanged=True,views=controls,
            final_masks=[ref(HERE/f'body-visibility-ready-{f}.png') for f in FACES])
(HERE/'mask-contour-refinement.json').write_bytes((json.dumps(record,indent=2)+'\n').encode())
p=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(p.read_text(encoding='utf-8'));entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert entry['id']=='FIT-YRAME-CHAIN-MAIL-BODY-0'
entry['process_log'].append(dict(timestamp=now,step='construct_and_overlay_one_item',phase='Constrain profile hand mask to actual hand interior/rim',action=record['reason'],inputs=[ref(HERE/'hand-ownership-correction.json')],outputs=[ref(HERE/n) for n in ['refine-hand-ownership.py','mask-contour-refinement.json','ready-neutral-turnaround.png','ready-context-turnaround.png','ready-source-reference-construction.png']],review='Body and full mail unchanged. All facings require final manual comparison before refinement.',result='REQUIRES REVIEW'))
ledger['updated_at']=now;p.write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Kept initial front/back masks and corrected only actual profile hand interior/rim; review final manual context.')
