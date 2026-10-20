"""Register the isolated tunic to the fixed child dromad; record edge ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad-child/v1'
OUT=HERE/'registered'
OUT.mkdir(exist_ok=True)
source=Image.open(HERE/'isolated-proposal.png').convert('RGBA')
body_model=json.loads((BODY/'model.json').read_text())
scale=.78
views=[('south',(260,700),(261,515),(256,574)),
       ('east',(750,650),(710,476),(218,542)),
       ('north',(1240,700),(1240,502),(256,559))]
model=dict(item='Woven Tunic',blueprint='Woven Tunic',family='dromad-child',
           slot='Body',laterality=0,canvas=[512,1024],contact=[256,950],views={},
           base_model=(BODY/'model.json').relative_to(ROOT).as_posix(),
           body_sha256=hashlib.sha256((BODY/'model.json').read_bytes()).hexdigest(),
           palette='Neutral grayscale; separate equipment foreground &y/detail y',
           policy='Authored child fitting; no observed child wearer or native child selector assumed',
           native_acceptance='Deferred until every conversion is generation-ready')
decisions=dict(source='../isolated-proposal.png',source_size=list(source.size),
               common_clothing_scale=scale,contact=[256,950],views={})
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
    im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    delta=(target_anchor[0]-round((source_anchor[0]-region[0])*scale),
           target_anchor[1]-round((source_anchor[1]-region[1])*scale))
    raw=Image.new('RGBA',(512,1024))
    raw.paste(im,delta)
    raw.save(OUT/f'registered-uncut-{facing}.png')
    cut=Image.new('L',raw.size)
    draw=ImageDraw.Draw(cut)
    if facing in ('south','north'):
        draw.polygon([(95,711),(153,739),(151,752),(82,725)],fill=255)
        draw.polygon([(359,739),(417,711),(430,725),(361,752)],fill=255)
    else:
        draw.polygon([(219,709),(294,709),(290,744),(286,772),(289,797),
                      (270,821),(246,827),(225,812),(221,793),(223,775),(209,750),(209,727)],fill=255)
        draw.ellipse((216,702,301,742),fill=255)
        draw.ellipse((224,764,288,828),fill=255)
    cut.save(OUT/f'arm-coverage-cut-{facing}.png')
    head_cut=Image.open(BODY/f'head-{facing}.png').getchannel('A')
    coverage=ImageChops.lighter(cut,head_cut)
    coverage.save(OUT/f'coverage-cut-{facing}.png')
    raw.putalpha(ImageChops.multiply(raw.getchannel('A'),ImageChops.invert(coverage)))
    raw.paste((0,0,0,0),mask=raw.getchannel('A').point(lambda v:255 if v==0 else 0))
    raw.save(OUT/f'tunic-{facing}.png')
    body=Image.open(BODY/f'body-{facing}.png').convert('RGBA')
    head=Image.open(BODY/f'head-{facing}.png').convert('RGBA')
    combined=Image.alpha_composite(Image.alpha_composite(body,raw),head)
    combined.save(OUT/f'assembled-{facing}.png')
    assemblies.append((facing,combined))
    cloth_views.append((facing,raw))
    row=dict(body_model['views'][facing][0])
    row.update(component='item',file=f'dromad-child-woven-tunic-v1-{facing}.png',
               public_file=(OUT/f'tunic-{facing}.png').relative_to(ROOT).as_posix(),
               sha256=hashlib.sha256((OUT/f'tunic-{facing}.png').read_bytes()).hexdigest(),
               color_role='equipment',equipment_key='woven-tunic@Body@0',layer=.0007)
    model['views'][facing]=[row]
    decisions['views'][facing]=dict(seed=seed,region=region,selection=f'selection-{facing}.png',
        source_anchor=source_anchor,target_anchor=target_anchor,translation=delta,
        head_cut=(BODY/f'head-{facing}.png').relative_to(ROOT).as_posix(),
        arm_cut=f'arm-coverage-cut-{facing}.png',
        edge_ownership='Head owns full neck/dulla; fixed body owns arms/hands. Garment owns only cloth and rope.',
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
    d.text((18,610),'Fixed base; separate neutral cloth. Native acceptance pending.',font=font,fill='#e5e8d8')
    image.save(OUT/name)
assemblies.append(('west (mirror)',ImageOps.mirror(dict(assemblies)['east'])))
plate(assemblies,'CHILD DROMAD / WOVEN TUNIC / common contact (256, 950)','assembly-comparison.png',True)
plate(cloth_views,'WOVEN TUNIC / cloth and rope only / explicit neck and arm openings','registered-isolated-comparison.png')
small=Image.new('RGB',(480,340),'#142823')
for i,(_,im) in enumerate(assemblies):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS)
    small.paste(thumb,(i*120+35,15),thumb)
    thumb=thumb.resize((96,192),Image.Resampling.NEAREST)
    small.paste(thumb,(i*120+12,125),thumb)
small.save(OUT/'game-scale-review.png')
for name,data in [('model.json',model),('registration-decisions.json',decisions)]:
    (OUT/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
