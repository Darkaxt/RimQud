"""Transfer usable refinement to separate fixed add-ons; restore the exact base."""
from pathlib import Path
import json
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;SIZE=(512,1264)
raw=Image.open(HERE/'secondary-views-raw.png').convert('RGBA')
# Surface UV correspondence only. These transforms never move production geometry.
maps={'south':(.85,.82,23,7),'east':(.85,.82,532,7),'north':(.85,.82,990,7)}
face_crops={'south':(164,72,319,187),'east':(713,76,826,166),'north':(1127,69,1289,183)}
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
sheet=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'IRUDAD / actual refined surface, exact base restored; separate anatomy retained',font=font,fill='#e3cf43')
for index,f in enumerate(['south','east','north']):
    sx,sy,tx,ty=maps[f]
    sampled=np.array(raw.transform(SIZE,Image.Transform.AFFINE,(sx,0,tx,0,sy,ty),Image.Resampling.BILINEAR))
    gray=sampled[:,:,:3].mean(2);valid=(sampled[:,:,3]>235)&(gray>155)
    _,nearest=distance_transform_edt(~valid,return_indices=True);surface=gray[tuple(nearest)]
    for part in ['raised-arms','hands-face','tail']:
        p=HERE/('patched-tail-east.png' if part=='tail' and f=='east' else f'{part}-{f}.png')
        source=np.array(Image.open(p).convert('RGBA'));alpha=source[:,:,3];out=source.copy()
        if part=='hands-face':
            # Programmatic extraction in place, constrained by the editable piece alpha.
            bbox=Image.fromarray(alpha).getbbox();crop=raw.crop(face_crops[f]).resize((bbox[2]-bbox[0],bbox[3]-bbox[1]),Image.Resampling.LANCZOS)
            paint=Image.new('RGBA',SIZE);paint.paste(crop,bbox[:2]);paint=np.array(paint);g=paint[:,:,:3].mean(2);usable=(paint[:,:,3]>180)&(alpha>0)
            _,n=distance_transform_edt(~usable,return_indices=True);g=g[tuple(n)]
            out[:,:,:3]=np.uint8(np.round(g))[:,:,None];out[:,:,3]=alpha
        else:
            ink=source[:,:,:3].mean(2)<100
            out[:,:,:3]=np.uint8(np.round(surface))[:,:,None]
            out[ink,:3]=source[ink,:3]
        out[alpha==0,:3]=0
        Image.fromarray(out).save(HERE/f'patched-refined-{part}-{f}.png')
    assembly=Image.new('RGBA',SIZE)
    for part in (['tail','raised-arms'] if f!='north' else ['raised-arms']):assembly.alpha_composite(Image.open(HERE/f'patched-refined-{part}-{f}.png').convert('RGBA'))
    assembly.alpha_composite(Image.open(HERE/f'baseline-{f}.png').convert('RGBA'))
    if f=='north':assembly.alpha_composite(Image.open(HERE/f'patched-refined-tail-{f}.png').convert('RGBA'))
    assembly.alpha_composite(Image.open(HERE/f'patched-refined-hands-face-{f}.png').convert('RGBA'))
    assembly.save(HERE/f'patched-refined-{f}.png');im=assembly.resize((240,593),Image.Resampling.LANCZOS);sheet.paste(im,(40+index*330,55),im);d.text((40+index*330,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'Original base unchanged; generated body redraw rejected. Source controls alpha, count and attachments.',font=font,fill='#e5e8d8');sheet.save(HERE/'patched-refined-turnaround.png')
review=dict(status='PATCHED FOR VISUAL REVIEW',first_output='secondary-views-raw.png',accepted='Usable gray skin shading and clearer interlaced hands-face interior; correct four arms, mouthless face, white eyes only on front/profile and posterior barbs.',
    rejected='Generated body/head/feet proportions differ from the selected reusable base, label pixels/background/stray alpha and independent image placement are not production art.',
    correction='Restore the unchanged padded base. Retain editable separate add-on coverage and posterior depth. Programmatically transfer only usable generated surface; do not request isolation or treat generated bounds as body registration.',
    surface_uv_maps=maps,hands_face_surface_crops=face_crops,body_resampled=False,native_activation=False)
(HERE/'first-structural-review.json').write_bytes((json.dumps(review,indent=2)+'\n').encode())
print('Restored exact baseline and separate geometry, transferred usable first refinement; review pending.')
