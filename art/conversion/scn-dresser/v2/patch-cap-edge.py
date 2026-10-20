"""Remove the old cap's unowned edge pixels before composed refinement."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert not (HERE/'cap-edge-correction.json').exists()
paths=['selected-front-neutral.png','ownership-south.png','constructed-south.png','front-guided-turnaround.png','constructed-turnaround.png']
for name in paths:(HERE/('before-edge-fix-'+name)).write_bytes((HERE/name).read_bytes())
a=np.array(Image.open(HERE/'selected-front-neutral.png').convert('RGBA'));own=np.array(Image.open(HERE/'ownership-south.png').convert('RGBA'));cap=np.array(Image.open(HERE/'parallel-front-cap.png').convert('RGBA'));old=a.copy();region=np.indices(a.shape[:2])[0]<163;inside=cap[:,:,3]>0;clear=region&~inside;removed=int(np.count_nonzero(clear&(a[:,:,3]>0)));a[clear]=0;own[clear]=0;a[:,:,3][region&inside]=cap[:,:,3][region&inside];own[:,:,:3][region&inside]=255;own[:,:,3][region&inside]=cap[:,:,3][region&inside];a[(a[:,:,3]==0)&region,:3]=0;own[(own[:,:,3]==0)&region,:3]=0
assert np.array_equal(a[163:],old[163:]);Image.fromarray(a).save(HERE/'selected-front-neutral.png');Image.fromarray(own).save(HERE/'ownership-south.png');weight=own[:,:,0].astype(float)/255;context=a.copy();context[:,:,:3]=np.uint8(a[:,:,:3].astype(float)*((1-weight[:,:,None])+weight[:,:,None]*np.array([.65,.9,1])));Image.fromarray(context).save(HERE/'constructed-south.png')
sheet=Image.new('RGBA',(1536,768))
for i,f in enumerate(['south','east','north']):sheet.alpha_composite(Image.open(HERE/f'constructed-{f}.png').convert('RGBA'),(i*512,0))
sheet.save(HERE/'front-guided-turnaround.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);plate=Image.new('RGB',(1440,760),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'DRESSER / corrected cap edges before refinement; retained lower body and full end/back',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((280,420),Image.Resampling.LANCZOS);plate.paste(im,(50+i*470,55),im);d.text((50+i*470,500),f.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Original cap unowned outline fragments removed before ImageGen. The new cap alpha owns its whole rectangle.',
 'Below authoring y163 all original selected body/front/pull/foot pixels are unchanged. Same16x24cell/pivot.',
 'Actual donor cap planes are parallel; source three-front identity and both native w roles retained.',
 'One source state. Complete end/back unbound; native container and Animated fallback acceptance pending.']):d.text((18,590+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'constructed-turnaround.png');record=dict(reason='Removing only colored owner left unowned old cap outline/fringe outside new rectangle. Whole old cap region now cleared; exact new cap alpha assigned before refinement.',removed_old_exterior_pixels=removed,upper_region_y_exclusive=163,original_lower_body_pixels_unchanged=True,inputs=[ref(HERE/'before-edge-fix-selected-front-neutral.png'),ref(HERE/'parallel-front-cap.png')],outputs=[ref(HERE/n) for n in ['selected-front-neutral.png','ownership-south.png','constructed-turnaround.png','front-guided-turnaround.png']]);(HERE/'cap-edge-correction.json').write_bytes((json.dumps(record,indent=2)+'\n').encode());print('Removed old cap fringe pixels:',removed,'; retained original lower-body pixels.')
