"""Patch this entry's proposed views: preserve front, register, clean alpha/color.

This does not create other bodies or infer anatomy from image segmentation.
"""
import json
from pathlib import Path
from PIL import Image,ImageOps

ROOT=Path(__file__).resolve().parents[1];FOLDER=ROOT/'art/conversion/body-human-male/v1'

def neutral(im):
    alpha=im.getchannel('A').point(lambda a:0 if a<16 else 255 if a>=240 else a)
    gray=ImageOps.grayscale(im);out=Image.merge('RGBA',(gray,gray,gray,alpha))
    # RGB in transparent pixels must not mislead previews or edge sampling.
    out.paste((0,0,0,0),(0,0),alpha.point(lambda a:255 if a==0 else 0))
    return out

def main():
    raw=Image.open(FOLDER/'secondary-views.png').convert('RGBA')
    front=Image.open(FOLDER/'refined-front.png').convert('RGBA')
    # Explicit inspected body regions. Footer labels are not part of the sprite.
    panels=[front,raw.crop((512,0,1024,950)),raw.crop((1024,0,1536,950))]
    normalized=[];record=[]
    for i,im in enumerate(panels):
        bbox=im.getchannel('A').point(lambda a:255 if a>=220 else 0).getbbox()
        crop=neutral(im.crop(bbox))
        if i==0:
            # Set one physical scale from the selected front. Later views use the
            # same source-sheet scale; their silhouette widths are not normalized.
            sc=900/crop.height
        else:sc=1
        size=(round(crop.width*sc),round(crop.height*sc));crop=crop.resize(size,Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(512,1024));x=round(256-size[0]/2);y=930-size[1]
        canvas.alpha_composite(crop,(x,y));canvas.save(FOLDER/('patched-'+['south','east','north'][i]+'.png'));normalized.append(canvas)
        record.append(dict(direction=['south','east','north'][i],source='refined-front.png' if i==0 else 'secondary-views.png',source_body_rect=bbox,
                           uniform_scale=sc,placement=[x,y],feet_baseline=930,canvas=[512,1024]))
    sheet=Image.new('RGBA',(1536,1024))
    for i,im in enumerate(normalized):sheet.alpha_composite(im,(i*512,0))
    sheet.save(FOLDER/'patched-views.png')
    (FOLDER/'patch-decisions.json').write_bytes((json.dumps(dict(
        anatomy_review='No added/missing limb correction required: side occlusion supports two arms/legs; short feet face right. Back has no face or front toes.',
        corrections=['Replace generated front with the exact selected refined-front silhouette, uniformly rescaled.',
                     'Crop footer labels away from all sprite panels; report supplies reliable view labels.',
                     'Convert low-chroma generated fill to equal-channel grayscale, retaining shading.',
                     'Clear alpha below 16; restore near-opaque alpha >=240; keep intermediate antialiasing. Clear RGB wherever alpha is zero.',
                     'Align each inspected view to y=930; do not stretch panel widths to match.'],
        registration=record),indent=2)+'\n').encode())
    print('Patched selected front, neutral palette, alpha and contact; side/back anatomy retained.')

if __name__=='__main__':main()
