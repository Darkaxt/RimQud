"""Register the isolated tunic to the fixed adult dromad; record edge ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad/v1'
OUT=HERE/'registered'
OUT.mkdir(exist_ok=True)
source=Image.open(HERE/'isolated-proposal.png').convert('RGBA')
body_model=json.loads((BODY/'model.json').read_text())
scale=.76
profile_width_fit=1.18
views=[('south',(250,650),(251,334),(256,502)),
       ('east',(750,650),(736,320),(244,482)),
       ('north',(1250,650),(1243,333),(256,492))]
model=dict(item='Cloth Robe',blueprint='Cloth Robe',family='dromad',
           slot='Body',laterality=0,canvas=[512,1024],contact=[256,950],views={},
           base_model=(BODY/'model.json').relative_to(ROOT).as_posix(),
           body_sha256=hashlib.sha256((BODY/'model.json').read_bytes()).hexdigest(),
           palette='Neutral grayscale; separate equipment foreground &y/detail y',
           policy='Actual equipped Cloth Robe on Tam, Body part 357, laterality 0; fixed unmutated adult race base',
           native_acceptance='Deferred until every conversion is generation-ready')
decisions=dict(source='../isolated-proposal.png',source_size=list(source.size),
               common_clothing_scale=scale,profile_width_fit=profile_width_fit,contact=[256,950],views={})
assemblies=[]
cloth_views=[]
for facing,seed,source_anchor,target_anchor in views:
    threshold=source.getchannel('A').point(lambda v:255 if v>=16 else 0)
    ImageDraw.floodfill(threshold,seed,128)
    selection=threshold.point(lambda v:255 if v==128 else 0)
    selection.save(OUT/f'selection-{facing}.png')
    region=selection.getbbox()
    a=ImageChops.multiply(source.getchannel('A'),selection)
    a=a.point(lambda v:0 if v<16 else (255 if v>=240 else v))
    gray=ImageOps.grayscale(source)
    im=Image.merge('RGBA',(gray,gray,gray,a)).crop(region)
    scale_x=scale*(profile_width_fit if facing=='east' else 1)
    im=im.resize((round(im.width*scale_x),round(im.height*scale)),Image.Resampling.LANCZOS)
    delta=(target_anchor[0]-round((source_anchor[0]-region[0])*scale_x),
           target_anchor[1]-round((source_anchor[1]-region[1])*scale))
    raw=Image.new('RGBA',(512,1024))
    raw.paste(im,delta)
    raw.save(OUT/f'registered-uncut-{facing}.png')
    cut=Image.new('L',raw.size)
    draw=ImageDraw.Draw(cut)
    if facing in ('south','north'):
        draw.polygon([(88,674),(148,712),(147,728),(73,687)],fill=255)
        draw.polygon([(364,712),(424,674),(439,687),(365,728)],fill=255)
    else:
        draw.polygon([(215,696),(290,710),(286,750),(290,785),(276,810),
                      (249,819),(224,802),(217,775),(204,747),(205,718)],fill=255)
        draw.ellipse((216,687,294,716),fill=255)
        draw.ellipse((219,745,292,818),fill=255)
    cut.save(OUT/f'arm-coverage-cut-{facing}.png')
    head_cut=Image.open(BODY/f'head-{facing}.png').getchannel('A')
    coverage=ImageChops.lighter(cut,head_cut)
    coverage.save(OUT/f'coverage-cut-{facing}.png')
    raw.putalpha(ImageChops.multiply(raw.getchannel('A'),ImageChops.invert(coverage)))
    raw.paste((0,0,0,0),mask=raw.getchannel('A').point(lambda v:255 if v==0 else 0))
    raw.save(OUT/f'robe-{facing}.png')
    body=Image.open(BODY/f'body-{facing}.png').convert('RGBA')
    head=Image.open(BODY/f'head-{facing}.png').convert('RGBA')
    combined=Image.alpha_composite(Image.alpha_composite(body,raw),head)
    combined.save(OUT/f'assembled-{facing}.png')
    assemblies.append((facing,combined))
    cloth_views.append((facing,raw))
    row=dict(body_model['views'][facing][0])
    row.update(component='item',file=f'dromad-cloth-robe-v1-{facing}.png',
               public_file=(OUT/f'robe-{facing}.png').relative_to(ROOT).as_posix(),
               sha256=hashlib.sha256((OUT/f'robe-{facing}.png').read_bytes()).hexdigest(),
               color_role='equipment',equipment_key='cloth-robe@Body@0',layer=.0007)
    model['views'][facing]=[row]
    decisions['views'][facing]=dict(seed=seed,region=region,selection=f'selection-{facing}.png',
        source_anchor=source_anchor,target_anchor=target_anchor,translation=delta,scale_x=scale_x,scale_y=scale,
        fit_reason='Profile width fitted to fixed hump and breast landmarks; no body distortion, per-view material-height scale remains .76.',
        head_cut=(BODY/f'head-{facing}.png').relative_to(ROOT).as_posix(),
        arm_cut=f'arm-coverage-cut-{facing}.png',
        edge_ownership='Head owns full neck/dulla; fixed body owns arms/hands. Garment owns goat-wool fabric and tonal shale freckles only.',
        layer_order=['fixed body','garment','fixed head'],body_unchanged=True)

font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(rows,title,name,guides=False):
    image=Image.new('RGB',(288*len(rows),650),'#142823')
    d=ImageDraw.Draw(image)
    d.text((18,12),title,font=font,fill='#e3cf43')
    for i,(facing,im) in enumerate(rows):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
        left,top=i*288+16,54
        image.paste(bg.convert('RGB').resize((256,512),Image.Resampling.LANCZOS),(left,top))
        if guides:
            x,y=left+128,top+475
            d.line((x,top,x,top+511),fill='#cebc45')
            d.line((left,y,left+255,y),fill='#70b8b0')
        d.text((left,578),facing.upper(),font=font,fill='#e3cf43')
    d.text((18,610),'Fixed adult base; separate neutral goat-wool robe. Native acceptance pending.',font=font,fill='#e5e8d8')
    image.save(OUT/name)
assemblies.append(('west (mirror)',ImageOps.mirror(dict(assemblies)['east'])))
plate(assemblies,'ADULT DROMAD / CLOTH ROBE / common contact (256, 950)','assembly-comparison.png',True)
plate(cloth_views,'CLOTH ROBE / wool and tonal freckles only / explicit neck and arm openings','registered-isolated-comparison.png')
small=Image.new('RGB',(480,340),'#142823')
for i,(_,im) in enumerate(assemblies):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS)
    small.paste(thumb,(i*120+35,15),thumb)
    thumb=thumb.resize((96,192),Image.Resampling.NEAREST)
    small.paste(thumb,(i*120+12,125),thumb)
small.save(OUT/'game-scale-review.png')
for name,data in [('model.json',model),('registration-decisions.json',decisions)]:
    (OUT/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
