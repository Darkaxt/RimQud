"""Preserve source anatomy while carrying usable generated surface values into fixed curves."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'first-structural-review.json').exists()
a=np.array(Image.open(HERE/'secondary-views-raw.png').convert('RGBA'));gray=a[:,:,:3].astype(float).mean(2);y,x=np.indices(gray.shape)
sample=(a[:,:,3]>250)&(y>510)&(y<790)&(gray>160)&(gray<250)
low,high=np.percentile(gray[sample],[15,80]);assert 160<low<high<251
source=(HERE/'leg-construction.json').read_text();geometry=json.loads(source);old=geometry['geometry']['front_left_path']
new=old.replace('Q38 941 59 948 Q95 953 124 940 Q132 929 125 918','Q33 934 47 944 Q61 952 79 950 L109 947 Q126 946 131 937 Q134 926 125 918')
assert new!=old
for f in ['south','east','north']:
    svg=(HERE/f'extra-legs-{f}.svg').read_text().replace(old,new)
    svg=svg.replace('#d0d0d0',f'#{round(low):02x}'*0+'#'+f'{round(low):02x}'*3).replace('#eeeeee','#'+f'{round(high):02x}'*3).replace('#c4c4c4','#'+f'{round(low-5):02x}'*3)
    if f=='south':
        # Short curved toe divisions remain inside the foot, without a shoe-like ankle seam.
        svg=svg.replace('</svg>','<g fill="none" stroke="#7f7f7f" stroke-width="2.6" stroke-linecap="round"><path d="M50 933 Q52 940 58 943 M66 936 Q67 944 74 947 M83 936 Q85 944 91 946 M421 946 Q427 944 429 936 M438 947 Q445 944 446 936 M454 943 Q460 940 462 933"/></g></svg>')
    (HERE/f'patched-extra-legs-{f}.svg').write_bytes(svg.encode());(HERE/f'patched-extra-legs-{f}.png').write_bytes(svg_to_bytes(svg_string=svg))
    im=Image.open(HERE/f'patched-extra-legs-{f}.png').convert('RGBA');im.alpha_composite(Image.open(HERE/f'baseline-{f}.png').convert('RGBA'));im.save(HERE/f'patched-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);out=Image.new('RGB',(1152,680),'#142823');d=ImageDraw.Draw(out)
d.text((18,15),'YRAME / patched feet, generated surface values, exact original body restored',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'patched-{f}.png').convert('RGBA').resize((256,512),Image.Resampling.LANCZOS);xx=60+i*370;out.paste(im,(xx,55),im);d.text((xx,590),f.upper(),font=font,fill='#e3cf43')
d.text((18,640),'FOUR total feet / separate added pair. No source body redraw, equipment or native activation.',font=font,fill='#e5e8d8');out.save(HERE/'patched-turnaround.png')
review=dict(status='USABLE FOUR-FOOT PROPOSAL AND SURFACE REFERENCE; SHARED BODY RESTORED',
    accepted='First output preserves four human legs/feet in front/back, two arms/hands, one blank head and complete cardinal profile with natural overlap. Quiet neutral shading is useful.',
    defects=['Generated baseline body/head/ordinary legs are redrawn and independently placed/scaled in the sheet, so they cannot replace exact reusable baseline pixels.','Generated label/transparent-edge noise is not production art.'],
    correction='Restore exact original shared body/head. Retain separate editable added-leg curves and cardinal attachments; soften outer forefoot curves and add restrained curved toe divisions. Transfer measured generated limb luminance as surface guidance only, without importing generated body contours or foreign body lines.',
    sampled_limb_luminance=[float(low),float(high)],sample_region='alpha>250, y510:790, grayscale160:250 in actual first output',source_pixels_unchanged=True,native_activation=False)
write(HERE/'first-structural-review.json',review)
write(HERE/'manual-corrections.json',dict(previous=ref(HERE/'leg-construction.json'),new_front_left_path=new,front_right='Mirrored from corrected left',profile='Accepted existing geometry and naturally occluded far leg unchanged',surface_guidance=review['sampled_limb_luminance'],body='All original pixels unchanged; new pair stays separate behind body.',native_activation=False))
prompt='''Use case: precise-object-edit, restrained composed game-sprite refinement.
Image1 is the corrected Yrame three-view sheet, SOUTH/front, EAST/full right profile, NORTH/straight back. Image2 is the original source/reference and reusable baseline plate; it is reference only. Refine image1 gently with quiet grayscale limb shading and coherent outlines. Preserve the SAME selected contours, complete cardinal facings, scale, ground, pelvic connections and neutral pose. Transparent background; labels SOUTH/EAST/NORTH below the corresponding figures.
This is an adult female human with exactly TWO arms, TWO hands, ONE blank head and FOUR human legs/feet total: the unchanged baseline pair and ONE additional pair rooted behind the pelvis. Front/back must show all four grounded feet. In the complete east profile, far limbs overlap naturally; do not create detached feet, add a third leg pair or turn only the head. The added pair is HUMAN anatomy with rounded bare feet, not horse legs, hooves, trousers or an extra animal body. No tail.
The source is Warden Yrame from Caves of Qud. Native prose distinguishes hind and forelegs; captured anatomy has two plural Feet groups. Mutation level6 does not mean6legs. Keep the existing ordinary human body/head/two arms and original two legs/feet fixed. No new body design, demographic, pose or source-unsupported anatomy. Respect the patched rounded extra forefeet and subtle toe divisions, keeping all four feet on the same ground.
Neutral grayscale only, plain featureless nonsexual adult mannequin with no detailed anatomical features. No horns, chain mail, boots, sword, clothing, hair, eyes, veins, scars, freezing breath/hand effects, jewellery, fixed skin colors, blue pixels, scenery or ground shadow. Horns and boots are separate equipped objects; they must not be baked into this body. Preserve transparent margins and full figures. This is composed refinement, not an isolation request.
'''
(HERE/'composed-refinement-prompt.txt').write_bytes(prompt.encode())
ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text());assert ledger['active_entry']=='BODY-YRAME';entry=next(e for e in ledger['entries'] if e['id']=='BODY-YRAME');now=datetime.now(timezone.utc).isoformat()
entry['process_log'].append(dict(timestamp=now,step=entry['required_steps'][3],action='Run actual built-in ImageGen using manual front/profile/back plus race/body/source/reference facts.',inputs=[ref(HERE/n) for n in ['secondary-views-prompt.txt','constructed-turnaround.png','source-reference-baseline.png']],outputs=[ref(HERE/'secondary-views-raw.png'),ref(HERE/'first-structural-review.json')],review=review['accepted']+' '+review['correction'],result='PASS'))
entry['process_log'].append(dict(timestamp=now,step=entry['required_steps'][4],action='Inspect first structural result, restore exact shared body and patch only the added feet/surfaces before composed refinement.',inputs=[ref(HERE/n) for n in ['secondary-views-raw.png','first-structural-review.json']],outputs=[ref(HERE/n) for n in ['patch-extra-legs.py','manual-corrections.json','patched-extra-legs-south.svg','patched-extra-legs-east.svg','patched-extra-legs-north.svg','patched-turnaround.png','composed-refinement-prompt.txt']],review='First generated four-foot anatomy is coherent; full-body redraw is not imported. Canonical pelvic roots and profile overlap retained, outer feet rounded. Exact second contextual prompt prepared; registration and final review remain unfinished.',result='PASS'))
entry['current_step']=entry['required_steps'][4];ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Retained first actual output/review; restored source body and patched separate feet, ready for composed refinement.')
