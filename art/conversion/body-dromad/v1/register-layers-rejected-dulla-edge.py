"""Register the inspected dromad sheet with explicit body/head/dulla ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFilter,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
source=Image.open(HERE/'refined-patched-views.png').convert('RGBA');assert source.size==(1490,1056)
views=[
 ('south',(245,700),(245,984),[(0,0),(1490,0),(1490,310),(323,310),(324,593),(309,612),(280,620),(238,617),(200,606),(171,586),(170,310),(0,310)],[(215,342),(250,345),(282,368),(295,405),(290,433),(265,460),(247,471),(225,456),(206,425),(205,411)]),
 ('east',(760,700),(727,984),[(0,0),(1490,0),(1490,300),(879,300),(877,605),(862,619),(836,616),(793,595),(760,560),(752,487),(752,300),(0,300)],[(833,331),(860,340),(881,367),(891,405),(886,431),(869,459),(853,466),(835,447),(819,414),(822,387)]),
 ('north',(1250,700),(1253,984),[(0,0),(1490,0),(1490,300),(1322,300),(1322,495),(1306,478),(1273,450),(1254,444),(1236,444),(1207,462),(1184,487),(1182,300),(0,300)],[])]
image_scale=.84;physical_height=1.4;world_scale=physical_height/round((984-81)*image_scale)
model=dict(family='dromad',canvas=[512,1024],contact=[256,950],views={},pixel_world_scale=world_scale,physical_body_height=physical_height,
 physical_height_kind='Authoring scale, not derived from native weight or an exported dromad height',
 geometry='Ordinary bipedal camelfolk: one head/long neck/dulla, two painted arms/hands and paired feet; intrinsic upper-back hump. No extra mutation appendages.',
 demographic_policy='Observed Tam male; no race-wide age/dimorphism established. No resident reassignment.',
 neutral_palette='Equal RGB grayscale in every layer. Foreground head/body and independent detail coverage remain separately tintable.',
 detail_interpretation='Dulla detail placement is an authored region for preserving a separate Qud detail role, not proven pixel-to-anatomy mapping of the original glyph.',
 registration=dict(contact=[256,950],method='One common .84 image scale then whole-figure/layer translation. Source connected silhouettes own the complete views.'),
 state='Generation-ready authoring only; native acceptance pending all-conversions gate')
decisions=dict(source='refined-patched-views.png',common_image_scale=image_scale,views={})
assembled=[];colored=[]
for facing,seed,old_contact,head_points,detail_points in views:
    selection=source.getchannel('A').point(lambda v:255 if v>=16 else 0);ImageDraw.floodfill(selection,seed,128);selection=selection.point(lambda v:255 if v==128 else 0)
    region=selection.getbbox();selection.save(HERE/f'source-selection-{facing}.png')
    image=source.copy();image.putalpha(ImageChops.multiply(source.getchannel('A'),selection));image=image.crop(region)
    a=image.getchannel('A').point(lambda v:0 if v<16 else (255 if v>=240 else v));g=ImageOps.grayscale(image);image=Image.merge('RGBA',(g,g,g,a))
    head=Image.new('L',source.size);ImageDraw.Draw(head).polygon(head_points,fill=255);head=head.crop(region)
    body=ImageChops.invert(head).filter(ImageFilter.MaxFilter(5))
    detail=Image.new('L',source.size)
    if detail_points:ImageDraw.Draw(detail).polygon(detail_points,fill=255)
    detail=ImageChops.multiply(detail.crop(region),head)
    size=(round(image.width*image_scale),round(image.height*image_scale))
    delta=(256-round((old_contact[0]-region[0])*image_scale),950-round((old_contact[1]-region[1])*image_scale))
    composite=Image.new('RGBA',(512,1024));owners=Image.new('RGBA',composite.size);rows=[]
    for component,mask,role,layer,tint in [('body',body,'foreground',0,'#739f96'),('head',head,'foreground',.001,'#d0bd66'),('head-detail',detail,'detail',.0011,'#c783bd')]:
        mask_scaled=mask.resize(size,Image.Resampling.NEAREST);canvas_mask=Image.new('L',(512,1024));canvas_mask.paste(mask_scaled,delta);canvas_mask.save(HERE/f'{component}-mask-{facing}.png')
        part=image.copy();part.putalpha(ImageChops.multiply(a,mask));part=part.resize(size,Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(512,1024));canvas.paste(part,delta);canvas.paste((0,0,0,0),mask=canvas.getchannel('A').point(lambda v:255 if v==0 else 0));path=HERE/f'{component}-{facing}.png';canvas.save(path)
        if component=='head-detail' and not detail_points:continue
        row=dict(component=component,file=f'dromad-v1-{path.name}',public_file=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),size=[512,1024],contact=[256,950],color_role=role,width=512*world_scale*1.5,height=1024*world_scale,center_x=0,center_z=(950-512)*world_scale,layer=layer)
        rows.append(row);composite=Image.alpha_composite(composite,canvas)
        paint=Image.new('RGBA',canvas.size,tint);paint.putalpha(canvas.getchannel('A'));owners=Image.alpha_composite(owners,paint)
    composite.save(HERE/f'selected-{facing}.png');assembled.append((facing,composite));colored.append(owners);model['views'][facing]=rows
    decisions['views'][facing]=dict(seed=seed,region=region,source_contact=old_contact,translation=delta,head_polygon=head_points,detail_polygon=detail_points,body_underlap_source_pixels=2)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1152,650),'#142823');draw=ImageDraw.Draw(plate)
draw.text((18,12),'DROMAD / body + long-neck head + separate dulla detail / common contact (256, 950)',font=font,fill='#e3cf43')
assembled.append(('west (mirror)',ImageOps.mirror(dict(assembled)['east'])))
for index,(facing,image) in enumerate(assembled):
    bg=Image.new('RGBA',image.size,'#20382d');bg.alpha_composite(image);left,top=index*288+16,54
    plate.paste(bg.convert('RGB').resize((256,512),Image.Resampling.LANCZOS),(left,top));x,y=left+128,top+475
    draw.line((x,top,x,top+511),fill='#cebc45');draw.line((left,y,left+255,y),fill='#70b8b0');draw.ellipse((x-4,y-4,x+4,y+4),outline='#fff6a0',width=2)
    draw.text((left,578),facing.upper(),font=font,fill='#e3cf43')
draw.text((18,610),'Neutral art; detail region placement is authored. Native acceptance remains pending.',font=font,fill='#e5e8d8');plate.save(HERE/'registration-comparison.png')
owner_plate=Image.new('RGBA',(1536,1024))
for index,image in enumerate(colored):owner_plate.alpha_composite(image,(index*512,0))
owner_plate.save(HERE/'ownership-comparison.png')
small=Image.new('RGB',(480,340),'#142823')
for index,(_,image) in enumerate(assembled):
    thumb=image.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(index*120+35,15),thumb);thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(index*120+12,125),thumb)
small.save(HERE/'game-scale-review.png')
for name,data in [('model.json',model),('registration-decisions.json',decisions)]:
    (HERE/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
