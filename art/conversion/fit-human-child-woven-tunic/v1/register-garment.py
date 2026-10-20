"""Register isolated cloth; explicit coverage cuts preserve the fixed base limbs."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-child/v1'
source=Image.open(HERE/'isolated-proposal.png').convert('RGBA')
scale=.54
views=[('south',(0,0,560,1056),(270,240),(256,426)),('east',(570,0,940,1056),(738,252),(274,433)),('north',(950,0,1490,1056),(1219,240),(256,426))]
body_model=json.loads((BODY/'model.json').read_text(encoding='utf-8'))
model=dict(item='Woven Tunic',blueprint='Woven Tunic',family='human-child',slot='Body',laterality=0,views={},canvas=[512,1024],contact=[256,950],base_model=(BODY/'model.json').relative_to(ROOT).as_posix(),
           palette='Neutral grayscale; independent native item foreground &y/detail y',body_sha256=hashlib.sha256((BODY/'model.json').read_bytes()).hexdigest(),
           policy='Authored child fitting, no observed equipped child or native child selector assumed',native_acceptance='Deferred until all conversions generated')
decisions=dict(source='isolated-proposal.png',common_clothing_scale=scale,views={})
assemblies=[];cloth_views=[]
for facing,region,source_anchor,target_anchor in views:
    im=source.crop(region);a=im.getchannel('A').point(lambda v:0 if v<16 else (255 if v>=240 else v));g=ImageOps.grayscale(im)
    im=Image.merge('RGBA',(g,g,g,a)).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    delta=(target_anchor[0]-round((source_anchor[0]-region[0])*scale),target_anchor[1]-round(source_anchor[1]*scale))
    raw=Image.new('RGBA',(512,1024));raw.paste(im,delta);raw.save(HERE/f'registered-uncut-{facing}.png')
    cut=Image.new('L',raw.size);draw=ImageDraw.Draw(cut)
    if facing in ['south','north']:
        draw.polygon([(124,537),(171,563),(170,573),(112,550)],fill=255)
        draw.polygon([(344,563),(391,537),(404,550),(345,575)],fill=255)
    else:
        draw.polygon([(252,555),(288,549),(303,599),(307,629),(301,645),(268,649),(256,628),(250,595)],fill=255)
        draw.ellipse((249,634,311,696),fill=255)
    raw.paste((0,0,0,0),mask=cut)
    raw.paste((0,0,0,0),mask=raw.getchannel('A').point(lambda v:255 if v==0 else 0))
    cut.save(HERE/f'coverage-cut-{facing}.png');raw.save(HERE/f'tunic-{facing}.png')
    body=Image.open(BODY/f'body-{facing}.png').convert('RGBA');head=Image.open(BODY/f'head-{facing}.png').convert('RGBA')
    combined=Image.alpha_composite(Image.alpha_composite(body,raw),head);combined.save(HERE/f'assembled-{facing}.png')
    assemblies.append((facing,combined));cloth_views.append((facing,raw))
    row=dict(body_model['views'][facing][0]);row.update(component='item',file=f'child-woven-tunic-v1-{facing}.png',public_file=(HERE/f'tunic-{facing}.png').relative_to(ROOT).as_posix(),sha256=hashlib.sha256((HERE/f'tunic-{facing}.png').read_bytes()).hexdigest(),color_role='equipment',equipment_key='woven-tunic@Body@0',layer=.0007)
    model['views'][facing]=[row]
    decisions['views'][facing]=dict(region=region,source_anchor=source_anchor,target_anchor=target_anchor,translation=delta,
       cut_mask=f'coverage-cut-{facing}.png',purpose='Open lower sleeve/near-arm coverage so actual base forearm and hand remain visible; remove closing cuff strokes.',body_file=(BODY/f'selected-{facing}.png').relative_to(ROOT).as_posix())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
plate=Image.new('RGB',(1152,650),'#142823');draw=ImageDraw.Draw(plate);draw.text((18,12),'CHILD / WOVEN TUNIC / unchanged base + independent clothing',font=font,fill='#e3cf43')
assemblies.append(('west (mirror)',ImageOps.mirror(dict(assemblies)['east'])))
for i,(facing,im) in enumerate(assemblies):
    bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);left,top=i*288+16,54
    plate.paste(bg.convert('RGB').resize((256,512),Image.Resampling.LANCZOS),(left,top));x,y=left+128,top+475
    draw.line((x,top,x,top+511),fill='#cebc45');draw.line((left,y,left+255,y),fill='#70b8b0');draw.text((left,578),facing.upper(),font=font,fill='#e3cf43')
draw.text((18,610),'Body is fixed. Neutral garment has its own tint. Native acceptance remains pending.',font=font,fill='#e5e8d8');plate.save(HERE/'assembly-comparison.png')
small=Image.new('RGB',(480,340),'#142823')
for i,(_,im) in enumerate(assemblies):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*120+35,15),thumb);thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*120+12,125),thumb)
small.save(HERE/'game-scale-review.png')
for name,data in [('model.json',model),('registration-decisions.json',decisions)]:
    (HERE/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
