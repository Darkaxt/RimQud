"""Register the inspected dromad sheet with explicit body/head/dulla ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFilter,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
source=Image.open(HERE/'refined-patched-views.png').convert('RGBA');assert source.size==(1489,1056)
views=[
 ('south',(225,680),(224,948),[(0,0),(1489,0),(1489,350),(297,350),(296,583),(281,600),(251,609),(215,605),(179,597),(157,584),(155,350),(0,350)],[(198,377),(224,382),(253,398),(272,435),(271,458),(256,483),(232,500),(210,488),(188,458),(184,440)]),
 ('east',(750,680),(724,947),[(0,0),(1489,0),(1489,340),(849,340),(850,608),(827,619),(807,615),(769,598),(736,562),(720,490),(718,340),(0,340)],[(790,374),(818,382),(843,406),(856,439),(852,462),(837,489),(832,500),(805,484),(782,457),(781,432)]),
 ('north',(1260,680),(1263,948),[(0,0),(1489,0),(1489,350),(1331,350),(1331,536),(1309,511),(1283,492),(1260,483),(1238,486),(1213,501),(1191,536),(1188,350),(0,350)],[])]
image_scale=.84;physical_height=.98;world_scale=physical_height/round((948-119)*image_scale)
model=dict(family='dromad-child',canvas=[512,1024],contact=[256,950],views={},pixel_world_scale=world_scale,physical_body_height=physical_height,
 physical_height_kind='Authoring scale, not derived from native weight or an exported dromad height',
 geometry='Ordinary bipedal camelfolk: one head/long neck/dulla, two painted arms/hands and paired feet; intrinsic upper-back hump. No extra mutation appendages.',
 demographic_policy='Authored child template, no canonical juvenile description or native age selector established. Male/female share geometry; no resident reassignment.',
 neutral_palette='Equal RGB grayscale in every layer. Foreground head/body and independent detail coverage remain separately tintable.',
 detail_interpretation='Dulla detail placement is an authored region for preserving a separate Qud detail role, not proven pixel-to-anatomy mapping of the original glyph.',
 registration=dict(contact=[256,950],method='One common .84 image scale then whole-figure/layer translation. Source connected silhouettes own the complete views.'),
 state='Generation-ready authoring only; native acceptance pending all-conversions gate',variants={'male':'shared geometry','female':'shared geometry'},clothing='FIT-DROMAD-CHILD-TEMPLATE-TUNIC owns the separate removable garment')
decisions=dict(source='refined-patched-views.png',common_image_scale=image_scale,views={})
assembled=[];colored=[]
for facing,seed,old_contact,head_points,detail_points in views:
    selection=source.getchannel('A').point(lambda v:255 if v>=16 else 0);ImageDraw.floodfill(selection,seed,128);selection=selection.point(lambda v:255 if v==128 else 0)
    region=selection.getbbox();selection.save(HERE/f'refined-selection-{facing}.png')
    image=source.copy();image.putalpha(ImageChops.multiply(source.getchannel('A'),selection));image=image.crop(region)
    a=image.getchannel('A').point(lambda v:0 if v<16 else (255 if v>=240 else v));g=ImageOps.grayscale(image);image=Image.merge('RGBA',(g,g,g,a))
    head=Image.new('L',source.size);ImageDraw.Draw(head).polygon(head_points,fill=255)
    detail=Image.new('L',source.size)
    if detail_points:ImageDraw.Draw(detail).polygon(detail_points,fill=255)
    # The profile flap projects beyond the otherwise straight neck edge. Its
    # complete outline belongs to head/neck, never to the torso layer.
    head=ImageChops.lighter(head,detail.filter(ImageFilter.MaxFilter(9))).crop(region)
    body=ImageChops.invert(head).filter(ImageFilter.MaxFilter(5))
    detail=ImageChops.multiply(detail.crop(region),head)
    size=(round(image.width*image_scale),round(image.height*image_scale))
    delta=(256-round((old_contact[0]-region[0])*image_scale),950-round((old_contact[1]-region[1])*image_scale))
    composite=Image.new('RGBA',(512,1024));owners=Image.new('RGBA',composite.size);rows=[]
    for component,mask,role,layer,tint in [('body',body,'foreground',0,'#739f96'),('head',head,'foreground',.001,'#d0bd66'),('head-detail',detail,'detail',.0011,'#c783bd')]:
        mask_scaled=mask.resize(size,Image.Resampling.NEAREST);canvas_mask=Image.new('L',(512,1024));canvas_mask.paste(mask_scaled,delta);canvas_mask.save(HERE/f'{component}-mask-{facing}.png')
        part=image.copy();part.putalpha(ImageChops.multiply(a,mask));part=part.resize(size,Image.Resampling.LANCZOS)
        canvas=Image.new('RGBA',(512,1024));canvas.paste(part,delta);canvas.paste((0,0,0,0),mask=canvas.getchannel('A').point(lambda v:255 if v==0 else 0));path=HERE/f'{component}-{facing}.png';canvas.save(path)
        if component=='head-detail' and not detail_points:continue
        row=dict(component=component,file=f'dromad-child-v1-{path.name}',public_file=path.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest(),size=[512,1024],contact=[256,950],color_role=role,width=512*world_scale*1.5,height=1024*world_scale,center_x=0,center_z=(950-512)*world_scale,layer=layer)
        rows.append(row);composite=Image.alpha_composite(composite,canvas)
        paint=Image.new('RGBA',canvas.size,tint);paint.putalpha(canvas.getchannel('A'));owners=Image.alpha_composite(owners,paint)
    composite.save(HERE/f'selected-{facing}.png');assembled.append((facing,composite));colored.append(owners);model['views'][facing]=rows
    decisions['views'][facing]=dict(seed=seed,selection_mask=f'refined-selection-{facing}.png',region=region,source_contact=old_contact,translation=delta,head_polygon=head_points,detail_polygon=detail_points,body_underlap_source_pixels=2,head_boundary_note='Profile/rear neck front-edge boundaries include the complete visible outline; dulla outline union belongs to head.')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1152,650),'#142823');draw=ImageDraw.Draw(plate)
draw.text((18,12),'CHILD DROMAD / featureless body + long-neck head + dulla detail / contact (256, 950)',font=font,fill='#e3cf43')
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
