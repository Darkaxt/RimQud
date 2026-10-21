"""Restore canonical anatomy and continue usable first-refinement surface values."""
from pathlib import Path
import json,re,sys
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;SIZE=(512,1264)
assert not (HERE/'first-structural-review.json').exists()
a=np.array(Image.open(HERE/'secondary-views-raw.png').convert('RGBA'));gray=a[:,:,:3].mean(2);yy,xx=np.indices(gray.shape)
tail=(a[:,:,3]>245)&(yy<400)&(gray>100)&(gray<235)
skin=(a[:,:,3]>245)&(yy>400)&(yy<810)&(gray>185)&(gray<253)
tail_low,tail_high=np.percentile(gray[tail],[20,80]);skin_low,skin_high=np.percentile(gray[skin],[15,75])
for f in ['south','east','north']:
    for layer in ['back','front']:
        source=(HERE/f'patched-tail-{layer}-{f}.svg').read_text()
        def recolor(match):
            value=int(match[1]);g=round(tail_low+(value-195)/44*(tail_high-tail_low));return f'fill="rgb({g},{g},{g})"'
        source=re.sub(r'fill="rgb\((\d+),\d+,\d+\)"',recolor,source)
        source=source.replace('stroke="#393939" stroke-width="2.5"','stroke="#777777" stroke-width="1"')
        # Jeweled is a quiet facet finish, not a row of invented diamond ornaments.
        source=re.sub(r'<path d="[^"]*" fill="#f5f5f5" stroke="#777777" stroke-width="1.5"/>','',source)
        (HERE/f'patched-refined-tail-{layer}-{f}.svg').write_bytes(source.encode())
        rendered=np.array(Image.open(__import__('io').BytesIO(svg_to_bytes(svg_string=source))).convert('RGBA'))
        alpha=np.array(Image.open(HERE/f'patched-tail-{layer}-{f}.png').convert('RGBA'))[:,:,3]
        rendered[:,:,:3]=np.uint8(np.round(rendered[:,:,:3].astype(float).mean(2)))[:,:,None]
        rendered[:,:,3]=alpha;rendered[alpha==0,:3]=0
        Image.fromarray(rendered).save(HERE/f'patched-refined-tail-{layer}-{f}.png')
    p=HERE/('patched-extra-arms-east.png' if f=='east' else f'extra-arms-{f}.png')
    arm=np.array(Image.open(p).convert('RGBA'));alpha=arm[:,:,3];ink=arm[:,:,:3].mean(2)<100
    shade=skin_low+(skin_high-skin_low)*np.clip(distance_transform_edt(alpha>128)/23,0,1)
    out=arm.copy();out[:,:,:3]=np.uint8(np.round(shade))[:,:,None];out[ink,:3]=arm[ink,:3];out[alpha==0,:3]=0
    Image.fromarray(out).save(HERE/f'patched-refined-extra-arms-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);sheet=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(sheet)
d.text((18,15),'NIMA / corrected composed views: ONE stinger, exact shared base, quiet surfaces',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    out=Image.new('RGBA',SIZE)
    for name in ['tail-back']+(['tail-front'] if f=='east' else [])+['extra-arms']:
        out.alpha_composite(Image.open(HERE/f'patched-refined-{name}-{f}.png').convert('RGBA'))
    out.alpha_composite(Image.open(HERE/f'baseline-{f}.png').convert('RGBA'))
    if f!='east':out.alpha_composite(Image.open(HERE/f'patched-refined-tail-front-{f}.png').convert('RGBA'))
    out.save(HERE/f'patched-refined-{f}.png');im=out.resize((240,593),Image.Resampling.LANCZOS);sheet.paste(im,(40+i*330,55),im);d.text((40+i*330,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'Generated duplicate stinger and body redraw rejected. One canonical tail; body pixels unchanged.',font=font,fill='#e5e8d8');sheet.save(HERE/'patched-refined-turnaround.png')
write=lambda p,data:p.write_bytes((json.dumps(data,indent=2)+'\n').encode())
write(HERE/'first-structural-review.json',dict(status='GENERATED ANATOMY REJECTED; USABLE SURFACE VALUES',accepted='Four-arm interpretation and restrained neutral skin/chitin shading usable as material reference.',
    defects=['North adds a second outer hooked stinger/bead in addition to the inner terminal.','Base body/head/legs are redrawn and rescaled relative to the selected female body.','Generated fewer/larger tail plates are not canonical mechanical part counts.'],
    correction='Restore exact original body and fixed source geometry with one endpoint/stinger/bead. Transfer measured surface luminance only; quiet facet lines and remove invented diamond icons. Do not extract invalid generated anatomy or request AI isolation.',
    measured_tail_luminance=[float(tail_low),float(tail_high)],measured_skin_luminance=[float(skin_low),float(skin_high)],native_activation=False))
# Full-tail topology view makes the sole endpoint explicit even where the body occludes it.
data=json.loads((HERE/'tail-construction-v2.json').read_text());frame=data['frame'];sx=frame['width']/512;sz=frame['height']/1264
sheet=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'NIMA / complete tail topology without body occlusion / one ROOT and one TIP',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.new('RGBA',SIZE)
    for layer in ['back','front']:im.alpha_composite(Image.open(HERE/f'patched-refined-tail-{layer}-{f}.png').convert('RGBA'))
    im=im.resize((240,593),Image.Resampling.LANCZOS);ox=40+i*330;oy=55;sheet.paste(im,(ox,oy),im)
    for label,p in [('ROOT / Tail193',data['centreline'][0]),('ONE TIP',data['bead'])]:
        h=p[0] if f=='south' else (p[1] if f=='east' else -p[0]);x=ox+(256+h/sx)*240/512;y=oy+(1190-p[2]/sz)*593/1264
        d.ellipse((x-3,y-3,x+3,y+3),outline='#e3cf43',width=2);d.text((ox,y+12),label,font=font,fill='#e3cf43')
    d.text((ox,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'The body hides parts of this same tail. Never add another hook or bead to a visible outer bend.',font=font,fill='#e5e8d8');sheet.save(HERE/'tail-topology-evidence.png')
prompt='''Use case: precise-object-edit, restrained composed game-sprite refinement.
Input1 is the corrected three-view Nima sheet: SOUTH/front, EAST/complete right profile, NORTH/straight back. Input2 is the full-tail topology diagram WITHOUT BODY OCCLUSION: it proves one root and ONE terminal hooked stinger and ONE tiny bead. Diagram annotations are not production art. Do not duplicate this tail or add an outer hook on its closed bend.
Refine input1 very gently with consistent neutral grayscale skin and organic/chitinous jeweled-segment shading. Keep the SAME source-constructed contours, spiral, attachments, four arms total/four hands total, two legs/feet, ordinary blank head and shared physical body scale. No new body, pose, clothes, cosmetics, claws, extra head or three-quarter camera. Same fixed cardinal direction in each panel. Transparent background; labels SOUTH/EAST/NORTH underneath.
Native Nima source: great spiral segmented tail climbs over back and neck, ending in ONE stinger with a tiny bead. The tail outer bend is continuous, not another endpoint. Specifically fix the previous failure: NORTH MUST NOT HAVE BOTH AN OUTER HOOK/BEAD AND AN INNER HOOK/BEAD. The inner terminal shown in the topology diagram is the only tip; keep that exact topology. SOUTH/EAST may hide that tip behind the original body; do not invent a second visible hook just for readability. Keep the full connected tail rooted at the rear pelvis, with its one inward spiral, preserving near/far depth. In the east profile, the near arm/body covers the midline tail root. Far arms overlap naturally in a complete profile.
Keep original body/head/feet shape, limb positions and mild featureless adult mannequin anatomy unchanged. No sexual anatomical detail, jade eyes, scars, hair, apron, hat, sandals, pestle or floating sphere. Tail is organic segmented cuticle with quiet polished facets, not a metal cable, necklace or rows of literal jewel ornaments. No colored pixels, glow, dramatic smoke or background. Never add extra limbs, stingers or beads. This is composed refinement only, not garment/body isolation.
'''
(HERE/'composed-refinement-prompt.txt').write_bytes(prompt.encode())
print('Restored exact base and one-tail topology; usable neutral surface values retained, corrected composed sheet and topology evidence prepared.')
