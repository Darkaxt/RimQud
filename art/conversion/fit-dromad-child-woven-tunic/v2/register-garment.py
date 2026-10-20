"""Fit refined fabric to the explicit neck/hump pattern, never to a new body."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-dromad-child/v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
source=Image.open(HERE/'isolated-proposal.png').convert('RGBA')
regions={'south':(41,341,518,804),'east':(588,321,923,805),'north':(975,342,1451,804)}
body_model=json.loads((BODY/'model.json').read_text());model=json.loads((HERE.parent/'v1/registered/model.json').read_text());model['views']={}
model['layer_order']='body -> head/detail -> collar garment, with precise painted-arm overlap';model['body_sha256']=sha(BODY/'model.json')
decisions={'method':'Use a plain interior fabric swatch from the actual isolated refinement inside the explicit editable garment pattern. Discard generated contour/rope placement rather than warping body or extrapolating proposal holes. Body/head/frame are unchanged; editable paths own collar, sleeves, folds and rope.','material_swatch':[180,450,355,590],'body_sha256':sha(BODY/'model.json'),'views':{}}
assembled={};intact={};effective={}
for facing,region in regions.items():
    pattern=Image.open(HERE/f'constructed-{facing}.png').convert('RGBA');alpha=pattern.getchannel('A');target=alpha.getbbox();width=target[2]-target[0];height=target[3]-target[1]
    swatch=source.crop((180,450,355,590))
    assert swatch.getchannel('A').getextrema()[0]>=250,'Selected material must contain cloth, with no transparent gaps.'
    filled=ImageOps.grayscale(swatch).resize((width,height),Image.Resampling.LANCZOS)
    texture=Image.new('L',(512,1024));texture.paste(filled,target[:2]);pgray=ImageOps.grayscale(pattern)
    # Editable edge/rope ownership supplies the final contour, not a blanket
    # subtraction of the head. The refined output supplies fabric rendering.
    edge=ImageChops.multiply(pgray.point(lambda v:255 if v<190 else 0),alpha)
    texture.paste(pgray,mask=edge);cloth=Image.merge('RGBA',(texture,texture,texture,alpha));cloth.save(HERE/f'intact-tunic-{facing}.png');intact[facing]=cloth.copy()
    body=Image.open(BODY/f'body-{facing}.png').convert('RGBA');body=Image.alpha_composite(body,Image.open(BODY/f'head-{facing}.png').convert('RGBA'))
    detail=BODY/f'head-detail-{facing}.png'
    if detail.exists():body=Image.alpha_composite(body,Image.open(detail).convert('RGBA'))
    cut=Image.new('L',(512,1024))
    if facing=='east':cut=ImageChops.multiply(Image.open(HERE/'near-arm-ownership.png').getchannel('A'),body.getchannel('A'))
    cut.save(HERE/f'body-occlusion-{facing}.png');cloth.putalpha(ImageChops.subtract(alpha,cut));cloth.paste((0,0,0,0),mask=cloth.getchannel('A').point(lambda v:255 if v==0 else 0));cloth.save(HERE/f'tunic-{facing}.png');effective[facing]=cloth
    fit=Image.alpha_composite(body,cloth);fit.save(HERE/f'assembled-{facing}.png');assembled[facing]=fit
    row=dict(body_model['views'][facing][0]);row.update(component='item',file=f'dromad-child-woven-tunic-v2-{facing}.png',public_file=(HERE/f'tunic-{facing}.png').relative_to(ROOT).as_posix(),sha256=sha(HERE/f'tunic-{facing}.png'),color_role='equipment',equipment_key='woven-tunic@Body@0',layer=.0012)
    model['views'][facing]=[row];decisions['views'][facing]={'source_region':region,'pattern_bounds':target,'fabric_scale_xy':[width/(region[2]-region[0]),height/(region[3]-region[1])],'pattern':f'constructed-{facing}.svg','intact_file':f'intact-tunic-{facing}.png','overlap':f'body-occlusion-{facing}.png','preserved_frame':[512,1024],'contact':[256,950]}
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(name,images,title,guides=False):
    p=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(p);d.text((18,14),title,font=font,fill='#e3cf43')
    for i,(facing,im) in enumerate(images.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=i*288+16;p.paste(bg.convert('RGB').resize((256,512)),(x,54))
        if guides:d.line((x+128,54,x+128,565),fill='#cebc45');d.line((x,529,x+255,529),fill='#70b8b0')
        d.text((x,584),facing.upper(),font=font,fill='#e3cf43')
    d.text((18,620),'Unchanged body/dulla. Explicit collar and shoulder pattern; native acceptance pending.',font=font,fill='#e5e8d8');p.save(HERE/name)
assembled['west (mirror)']=ImageOps.mirror(assembled['east'])
plate('assembly-comparison.png',assembled,'DROMAD CHILD / fitted collar and hump, full shoulder coverage',True)
plate('registered-isolated-comparison.png',intact,'INTACT GARMENT / actual smooth long-neck pattern; no hand-shaped hole')
plate('effective-coverage-comparison.png',effective,'EFFECTIVE LAYER / body-owned profile arm overlap shown separately')
small=Image.new('RGB',(480,340),'#142823')
for i,im in enumerate(assembled.values()):
    t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*120+35,15),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*120+12,125),t)
small.save(HERE/'game-scale-review.png')
for n,data in [('model.json',model),('registration-decisions.json',decisions)]: (HERE/n).write_bytes((json.dumps(data,indent=2)+'\n').encode())
