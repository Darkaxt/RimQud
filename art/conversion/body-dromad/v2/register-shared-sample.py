"""Remove split-resampling fringe without changing anatomy, scale or contact.

Sample the complete selected figure once, then extract all layers from those
same registered RGB pixels. Preserve the old source, masks and recorded drafts.
"""
from pathlib import Path
import json, hashlib
from PIL import Image, ImageChops, ImageFilter, ImageOps, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent / 'v1'
assert not (HERE/'model.json').exists(), 'Preserve recorded versions'
def asset(p):
    return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
source = Image.open(OLD/'refined-patched-views.png').convert('RGBA')
decisions = json.loads((OLD/'registration-decisions.json').read_text())
model = json.loads((OLD/'model.json').read_text())
model['registration']['method'] = 'Same .84 scale, frame and contact as v1. Resample full selected figure once; derive body/head/detail from common registered RGB and final-frame ownership masks.'
model['views'] = {}
record = {'source':asset(OLD/'refined-patched-views.png'),'previous_model':asset(OLD/'model.json'),'method':model['registration']['method'],'anatomy_changed':False,'new_imagegen_call':False,'views':{}}
assembled = {}
for f in ['south','east','north']:
    d = decisions['views'][f]
    selection = Image.open(OLD/f'refined-selection-{f}.png').convert('L')
    a = ImageChops.multiply(source.getchannel('A'),selection)
    im = source.copy(); im.putalpha(a); im = im.crop(d['region'])
    alpha = im.getchannel('A').point(lambda v:0 if v<16 else (255 if v>=240 else v))
    g = ImageOps.grayscale(im)
    im = Image.merge('RGBA',(g,g,g,alpha))
    im = im.resize((round(im.width*.84),round(im.height*.84)),Image.Resampling.LANCZOS)
    full = Image.new('RGBA',(512,1024));full.paste(im,d['translation'])
    full.save(HERE/f'unsplit-{f}.png')
    head_mask = Image.open(OLD/f'head-mask-{f}.png').convert('L')
    # Binary ownership was already defined by the previous source geometry.
    # Underlap is confined to opaque interior pixels, preserving silhouette alpha.
    body_mask = ImageChops.invert(head_mask)
    interior = full.getchannel('A').point(lambda v:255 if v==255 else 0)
    body_mask = ImageChops.lighter(body_mask, ImageChops.multiply(body_mask.filter(ImageFilter.MaxFilter(5)),interior))
    detail_mask = Image.open(OLD/f'head-detail-mask-{f}.png').convert('L')
    rows=[];combined=Image.new('RGBA',full.size)
    for component,mask in [('body',body_mask),('head',head_mask),('head-detail',detail_mask)]:
        oldrow=next((r for r in json.loads((OLD/'model.json').read_text())['views'][f] if r['component']==component),None)
        if not oldrow:continue
        mask.save(HERE/f'{component}-mask-{f}.png')
        part=full.copy();part.putalpha(ImageChops.multiply(full.getchannel('A'),mask))
        part.save(HERE/f'{component}-{f}.png')
        row=dict(oldrow);row.update(file=f'dromad-v2-{component}-{f}.png',public_file=(HERE/f'{component}-{f}.png').relative_to(ROOT).as_posix(),sha256=asset(HERE/f'{component}-{f}.png')['sha256'])
        rows.append(row);combined=Image.alpha_composite(combined,part)
    combined.save(HERE/f'selected-{f}.png');assembled[f]=combined;model['views'][f]=rows
    record['views'][f]={'whole_sample':asset(HERE/f'unsplit-{f}.png'),'old_head_ownership':asset(OLD/f'head-mask-{f}.png'),'translation':d['translation'],'source_region':d['region'],'head_body_rgb_source':'Same registered whole image; no independent layer resampling'}
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assembled['west (mirror)']=ImageOps.mirror(assembled['east'])
plate=Image.new('RGB',(1152,660),'#142823');draw=ImageDraw.Draw(plate)
draw.text((18,14),'DROMAD / shared registered sample; original shape and contact retained',font=font,fill='#e3cf43')
for i,(f,im) in enumerate(assembled.items()):
    bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*288
    plate.paste(bg.convert('RGB').resize((256,512)),(x,54));draw.line((x+128,54,x+128,565),fill='#cebc45');draw.line((x,529,x+255,529),fill='#70b8b0');draw.text((x,584),f.upper(),font=font,fill='#e3cf43')
draw.text((18,620),'Body/head/detail remain separate. No anatomy or camera changes. Native acceptance pending.',font=font,fill='#e5e8d8');plate.save(HERE/'registration-comparison.png')
closeup=Image.new('RGB',(1050,690),'#142823');draw=ImageDraw.Draw(closeup)
for i,(label,im) in enumerate([('OLD SPLIT',Image.open(OLD/'selected-east.png')),('UNSPLIT SOURCE',Image.open(HERE/'unsplit-east.png')),('SHARED SAMPLE SPLIT',assembled['east'])]):
    bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);closeup.paste(bg.crop((240,450,355,650)).resize((345,600)).convert('RGB'),(i*350,45));draw.text((i*350+6,14),label,font=font,fill='#e3cf43')
closeup.save(HERE/'neck-junction-comparison.png')
small=Image.new('RGB',(480,340),'#142823')
for i,im in enumerate(assembled.values()):
    t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*120+35,15),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*120+12,125),t)
small.save(HERE/'game-scale-review.png')
for name,data in [('model.json',model),('registration-decisions.json',record)]:
    (HERE/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
print('Registered common-sample body/head/detail without changing source anatomy')
