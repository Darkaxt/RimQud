"""Correct foreground hand ownership from actual original closed hand contours."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
SIZE=(768,1152);FACES=['south','east','north']


def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def write(name,v):
    (HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())


assert not (HERE/'hand-ownership-correction.json').exists()
controls=dict(south=[dict(center=[208,566],box=[169,532,249,610],replace_below=535),dict(center=[556,566],box=[515,532,597,610],replace_below=535)],
              east=[dict(center=[529,585],box=[480,552,577,625],replace_below=557)],
              north=[dict(center=[210,588],box=[168,551,251,629],replace_below=562),dict(center=[555,588],box=[513,551,597,629],replace_below=562)])
records={}
for facing in FACES:
    body=Image.open(HERE/f'original-body-{facing}.png').convert('RGBA');ba=np.array(body)
    mask=np.array(Image.open(HERE/f'body-visibility-{facing}.png').convert('L'))
    before=mask.copy();hands=np.zeros(mask.shape,dtype='uint8')
    for control in controls[facing]:
        x0,y0,x1,y1=control['box'];cx,cy=control['center']
        crop=ba[y0:y1,x0:x1];ink=(crop[:,:,:3].mean(2)<90)&(crop[:,:,3]>128)
        filled=ndimage.binary_fill_holes(ink)
        labels,n=ndimage.label(filled)
        label=int(labels[cy-y0,cx-x0]);assert label>0,(facing,control)
        component=labels==label
        # Closed source hand disk plus its original ink; one antialias border.
        component=ndimage.binary_dilation(component,iterations=1)
        component[crop[:,:,3]==0]=False
        hands[y0:y1,x0:x1]=np.maximum(hands[y0:y1,x0:x1],np.uint8(component)*255)
        start=control['replace_below']
        # Replace the lower hand ROI, not the curved cuff or the rest of the arm.
        mask[start:y1,x0:x1]=hands[start:y1,x0:x1]
    mask[ba[:,:,3]==0]=0
    Image.fromarray(mask).save(HERE/f'body-visibility-final-{facing}.png')
    Image.fromarray(hands).save(HERE/f'hand-ownership-{facing}.png')
    cloth=Image.open(HERE/f'constructed-cloth-{facing}.png').convert('RGBA')
    red=ba.copy();lum=ba[:,:,:3].mean(2);red[:,:,0]=np.uint8(np.maximum(lum,48));red[:,:,1]=np.uint8(lum*.065);red[:,:,2]=np.uint8(lum*.065);red[red[:,:,3]==0,:3]=0
    for prefix,base in [('patched-neutral',body),('patched-red',Image.fromarray(red))]:
        result=Image.composite(base,Image.alpha_composite(base,cloth),Image.fromarray(mask))
        result.save(HERE/f'{prefix}-{facing}.png')
    records[facing]=dict(controls=controls[facing],source_body=ref(HERE/f'original-body-{facing}.png'),
                         previous_mask=ref(HERE/f'body-visibility-{facing}.png'),final_mask=ref(HERE/f'body-visibility-final-{facing}.png'),
                         changed_mask_pixels=int(np.count_nonzero(before!=mask)),
                         method='Fill the actual original closed hand-ink contour from the hand-center seed, retain its ink/one antialias border, and replace only the named hand ROI. Curved cuff and garment unchanged.')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for prefix,name in [('patched-red','patched-context-turnaround.png'),('patched-neutral','patched-neutral-turnaround.png')]:
    sheet=Image.new('RGBA',(1440,540));d=ImageDraw.Draw(sheet)
    for i,f in enumerate(FACES):
        im=Image.open(HERE/f'{prefix}-{f}.png').convert('RGBA').crop((144,240,624,720))
        sheet.alpha_composite(im,(i*480,0));d.text((i*480+15,510),f.upper(),font=font,fill='white')
    sheet.save(HERE/name)
source=Image.open(HERE/'source-reference-construction.png').convert('RGB')
# Keep the source and actual donor portion, replace only the construction panel.
source.paste('#142823',(0,360,1440,900))
im=Image.open(HERE/'patched-neutral-turnaround.png').convert('RGBA');source.paste(im,(0,360),im)
source.save(HERE/'patched-source-reference-construction.png')
now=datetime.now(timezone.utc).isoformat()
write('hand-ownership-correction.json',dict(recorded_at=now,status='REQUIRES VISUAL REVIEW',
      reason='Initial profile mask copied torso beside the hand into the foreground. Correct actual hand ownership before contextual generation.',
      garment_geometry_unchanged=True,body_rgba_unchanged=True,views=records))
ledger=read(ROOT/'evidence/conversion-ledger.json');entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
assert entry['id']=='FIT-YRAME-CHAIN-MAIL-BODY-0'
entry['process_log'].append(dict(timestamp=now,step='construct_and_overlay_one_item',phase='Patch original hand ownership before refinement',
     action='Reject the initial profile visibility mask because it restores torso pixels around the hand; derive exact closed hand regions from the unchanged original drawing.',
     inputs=[ref(HERE/'manual-neutral-turnaround.png'),ref(HERE/'fit-contract.json')],
     outputs=[ref(HERE/n) for n in ['patch-hand-ownership.py','hand-ownership-correction.json','patched-neutral-turnaround.png','patched-context-turnaround.png','patched-source-reference-construction.png']],
     review='Full mail and original body unchanged. Only original-body visibility corrected; patched facings still require visual comparison with the fit contract.',result='REQUIRES REVIEW'))
ledger['updated_at']=now
(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Corrected hand ownership using actual source contours; review patched context before refinement.')
