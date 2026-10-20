"""One neutral axial cudgel, registered with per-facing grip and hand ownership."""
from pathlib import Path
import hashlib,json,math
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
BODY=ROOT/'art/conversion/body-dromad/v1'
ROBE=ROOT/'art/conversion/fit-dromad-cloth-robe/v1/registered'
source=Image.open(HERE/'isolated-proposal.png').convert('RGBA')
selection=source.getchannel('A').point(lambda v:255 if v>=16 else 0)
ImageDraw.floodfill(selection,(505,650),128)
selection=selection.point(lambda v:255 if v==128 else 0)
selection.save(OUT/'source-selection.png');region=selection.getbbox()
alpha=ImageChops.multiply(source.getchannel('A'),selection).point(lambda v:0 if v<16 else (255 if v>=240 else v))
gray=ImageOps.grayscale(source);im=Image.merge('RGBA',(gray,gray,gray,alpha)).crop(region)
scale=500/(region[3]-region[1]);source_grip=(506,988)
im=im.resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
canonical=Image.new('RGBA',(512,1024))
delta=(256-round((source_grip[0]-region[0])*scale),776-round((source_grip[1]-region[1])*scale))
canonical.paste(im,delta)
canonical.paste((0,0,0,0),mask=canonical.getchannel('A').point(lambda v:255 if v==0 else 0))
canonical.save(OUT/'canonical-item.png')
body_model=json.loads((BODY/'model.json').read_text())
placements=json.loads((HERE/'placement-suggestion.json').read_text())
model=dict(item='Shillelagh',blueprint='Shillelagh',family='dromad',slot='Hand',laterality=2,
           canvas=[512,1024],contact=[256,950],views={},
           base_model=(BODY/'model.json').relative_to(ROOT).as_posix(),
           body_sha256=hashlib.sha256((BODY/'model.json').read_bytes()).hexdigest(),
           context_robe=(ROBE/'model.json').relative_to(ROOT).as_posix(),
           palette='Neutral grayscale; independent native equipment foreground &y/detail y',
           axial_texture='canonical-item.png; one held-weapon image reused with explicit facing transforms',
           policy='Actual Tam Hand part 362, laterality 2. Enlarged visual length is authored, not measured native size.',
           native_acceptance='Pending every-conversion-generated gate')
decisions=dict(source='../isolated-proposal.png',source_size=list(source.size),selection='source-selection.png',
               region=region,source_grip=source_grip,uniform_scale=scale,canonical_translation=delta,
               canonical_grip=[256,776],canonical_length_pixels=500,views={})
assemblies=[];items=[]
for facing,v in placements.items():
    angle=math.radians(v['angle']);c,s=math.cos(angle),math.sin(angle);x,y=v['grip']
    affine=(c,s,256-c*x-s*y,-s,c,776+s*x-c*y)
    held=canonical.transform((512,1024),Image.Transform.AFFINE,affine,Image.Resampling.BICUBIC)
    held.save(OUT/f'unoccluded-{facing}.png')
    hand=Image.new('L',held.size);d=ImageDraw.Draw(hand);hx,hy=v['hand']
    d.ellipse((hx-32,hy-33,hx+32,hy+33),fill=255)
    actual_body=Image.open(BODY/f'body-{facing}.png').convert('RGBA')
    hand=ImageChops.multiply(hand,actual_body.getchannel('A'))
    hand.save(OUT/f'hand-coverage-{facing}.png')
    if facing!='north':held.putalpha(ImageChops.multiply(held.getchannel('A'),ImageChops.invert(hand)))
    held.paste((0,0,0,0),mask=held.getchannel('A').point(lambda v:255 if v==0 else 0))
    held.save(OUT/f'item-{facing}.png')
    pawn=Image.open(ROBE/f'assembled-{facing}.png').convert('RGBA')
    combined=Image.alpha_composite(held,pawn) if facing=='north' else Image.alpha_composite(pawn,held)
    combined.save(OUT/f'assembled-{facing}.png');assemblies.append((facing,combined));items.append((facing,held))
    row=dict(body_model['views'][facing][0])
    row.update(component='item',file=f'dromad-shillelagh-v1-{facing}.png',
               public_file=(OUT/f'item-{facing}.png').relative_to(ROOT).as_posix(),
               sha256=hashlib.sha256((OUT/f'item-{facing}.png').read_bytes()).hexdigest(),
               color_role='equipment',equipment_key='shillelagh@Hand@2',layer=v['layer'])
    model['views'][facing]=[row]
    decisions['views'][facing]=dict(**v,inverse_affine=affine,
        hand_mask=f'hand-coverage-{facing}.png',hand_cut_applied=facing!='north',
        depth='Behind entire pawn' if facing=='north' else 'In front; actual hand coverage removed from item',
        ownership='One continuous wooden item; underlying fixed hand supplies all skin/hand outlines.')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(rows,title,name,guides=False):
    plate=Image.new('RGB',(288*len(rows),650),'#142823');d=ImageDraw.Draw(plate)
    d.text((18,12),title,font=font,fill='#e3cf43')
    for i,(facing,im) in enumerate(rows):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);left,top=i*288+16,54
        plate.paste(bg.convert('RGB').resize((256,512),Image.Resampling.LANCZOS),(left,top))
        if guides:
            d.line((left+128,top,left+128,top+511),fill='#cebc45');d.line((left,top+475,left+255,top+475),fill='#70b8b0')
        d.text((left,578),facing.upper(),font=font,fill='#e3cf43')
    d.text((18,610),'Fixed body/robe; independent held item. Native acceptance pending.',font=font,fill='#e5e8d8')
    plate.save(OUT/name)
assemblies.append(('west (mirror)',ImageOps.mirror(dict(assemblies)['east'])))
plate(assemblies,'DROMAD / SHILLELAGH / fixed body contact (256, 950)','assembly-comparison.png',True)
plate(items,'SHILLELAGH / one axial item / actual hand and rear occlusion','registered-isolated-comparison.png')
small=Image.new('RGB',(480,340),'#142823')
for i,(_,im) in enumerate(assemblies):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*120+35,15),thumb)
    thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*120+12,125),thumb)
small.save(OUT/'game-scale-review.png')
for name,data in [('model.json',model),('registration-decisions.json',decisions)]:
    (OUT/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
