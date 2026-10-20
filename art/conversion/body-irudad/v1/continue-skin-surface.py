"""Reproduce the inspected correction of striped UV continuation, without blurring ink."""
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy.ndimage import distance_transform_edt
HERE=Path(__file__).resolve().parent
raw=np.array(Image.open(HERE/'secondary-views-raw.png').convert('RGBA'))
gray=raw[:,:,:3].mean(2);valid=(raw[:,:,3]>250)&(gray>180)&(gray<253)
low,high=np.percentile(gray[valid],[15,75])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
sheet=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(sheet)
d.text((18,15),'IRUDAD / corrected composed views; stable skin tones, original base',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    for part in ['raised-arms','tail']:
        p=HERE/('patched-tail-east.png' if part=='tail' and f=='east' else f'{part}-{f}.png')
        source=np.array(Image.open(p).convert('RGBA'));alpha=source[:,:,3]
        ink=source[:,:,:3].mean(2)<100
        distance=distance_transform_edt(alpha>128)
        paint=low+(high-low)*np.clip(distance/24,0,1)
        out=source.copy();out[:,:,:3]=np.uint8(np.round(paint))[:,:,None]
        out[ink,:3]=source[ink,:3];out[alpha==0,:3]=0
        Image.fromarray(out).save(HERE/f'smooth-{part}-{f}.png')
    out=Image.new('RGBA',(512,1264))
    if f!='north':out.alpha_composite(Image.open(HERE/f'smooth-tail-{f}.png').convert('RGBA'))
    out.alpha_composite(Image.open(HERE/f'smooth-raised-arms-{f}.png').convert('RGBA'))
    out.alpha_composite(Image.open(HERE/f'baseline-{f}.png').convert('RGBA'))
    if f=='north':out.alpha_composite(Image.open(HERE/f'smooth-tail-{f}.png').convert('RGBA'))
    out.alpha_composite(Image.open(HERE/f'patched-refined-hands-face-{f}.png').convert('RGBA'))
    out.save(HERE/f'corrected-composed-{f}.png')
    im=out.resize((240,593),Image.Resampling.LANCZOS);sheet.paste(im,(40+i*330,55),im)
    d.text((40+i*330,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'Rejected striped surface projection. Generated finger art retained; geometric contour preserved.',font=font,fill='#e5e8d8')
sheet.save(HERE/'corrected-composed-turnaround.png')
print('Continued smooth measured skin tones within fixed geometry; no base/alpha/ink change.')
