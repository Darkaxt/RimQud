"""One scale; full-frame intact art and separate painted-arm ownership."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-child/v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def mask_path(path,name):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><path fill="white" d="'+path+'"/></svg>'
    p=HERE/(name+'.svg');p.write_bytes(svg.encode());out=HERE/(name+'.png')
    out.write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True));return Image.open(out).getchannel('A')
source=Image.open(HERE/'isolated-proposal.png').convert('RGBA');scale=.62
views=[('south',(0,0,570,1056),(265,284),(256,418)),('east',(570,0,960,1056),(748,284),(274,418)),('north',(960,0,1489,1056),(1226,284),(256,418))]
body_model=json.loads((BODY/'model.json').read_text(encoding='utf-8'))
model=json.loads((HERE.parent/'v1/model.json').read_text(encoding='utf-8'));model['views']={}
model['body_sha256']=sha(BODY/'model.json');model['layer_order']='body -> head -> tunic collar; profile forearm ownership removes cloth over actual foreground limb'
decisions={'source':'isolated-proposal.png','common_scale':scale,'body_unchanged_sha256':sha(BODY/'model.json'),'views':{},'policy':'Intact art retained; effective alpha removes only registered body-owned forearm/hand below cuff. No new limb render node. Clothing above head extraction seam; no face coverage.'}
assembled={};intact={};effective={};masks={}
for facing,region,anchor,target in views:
    im=source.crop(region);a=im.getchannel('A').point(lambda v:0 if v<16 else v);g=ImageOps.grayscale(im)
    im=Image.merge('RGBA',(g,g,g,a)).resize((round(im.width*scale),round(im.height*scale)),Image.Resampling.LANCZOS)
    delta=(target[0]-round((anchor[0]-region[0])*scale),target[1]-round(anchor[1]*scale))
    raw=Image.new('RGBA',(512,1024));raw.paste(im,delta);raw.save(HERE/f'registered-proposal-{facing}.png')
    # A genuine collar opening, distinct from foreground arm/body overlap.
    collarpath=('M214 380 L298 380 L295 415 Q256 447 217 415Z' if facing!='east' else 'M240 374 L310 389 L308 423 Q276 417 246 407Z')
    collar=mask_path(collarpath,f'neck-opening-{facing}')
    raw.putalpha(ImageChops.subtract(raw.getchannel('A'),collar));raw.save(HERE/f'intact-tunic-{facing}.png');intact[facing]=raw.copy()
    body=Image.open(BODY/f'selected-{facing}.png').convert('RGBA')
    cut=Image.new('L',raw.size)
    if facing=='east':cut=Image.open(HERE/'near-arm-ownership.png').getchannel('A')
    else:
        # Local cuff ownership only, below the sleeve edge and away from torso.
        cut=mask_path('M97 546 L150 573 L170 587 L169 607 L90 607Z M362 573 L415 546 L422 607 L343 607 L342 587Z',f'cuff-ownership-{facing}')
    cut=ImageChops.multiply(cut,body.getchannel('A'));cut.save(HERE/f'body-occlusion-{facing}.png');masks[facing]=cut
    raw.putalpha(ImageChops.subtract(raw.getchannel('A'),cut));raw.paste((0,0,0,0),mask=raw.getchannel('A').point(lambda v:255 if v==0 else 0))
    raw.save(HERE/f'tunic-{facing}.png');effective[facing]=raw
    composed=Image.alpha_composite(body,raw);composed.save(HERE/f'assembled-{facing}.png');assembled[facing]=composed
    row=dict(body_model['views'][facing][0]);row.update(component='item',file=f'child-woven-tunic-v2-{facing}.png',public_file=(HERE/f'tunic-{facing}.png').relative_to(ROOT).as_posix(),sha256=sha(HERE/f'tunic-{facing}.png'),color_role='equipment',equipment_key='woven-tunic@Body@0',layer=.0012)
    model['views'][facing]=[row];decisions['views'][facing]={'region':region,'source_anchor':anchor,'target_anchor':target,'translation':delta,'intact_file':f'intact-tunic-{facing}.png','body_occlusion_mask':f'body-occlusion-{facing}.png','neck_opening':f'neck-opening-{facing}.png'}
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(name,images,title,guide=False):
    p=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(p);d.text((18,14),title,font=font,fill='#e3cf43')
    for i,(facing,im) in enumerate(images.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=i*288+16;p.paste(bg.convert('RGB').resize((256,512)),(x,54))
        if guide:d.line((x+128,54,x+128,565),fill='#cebc45');d.line((x,529,x+255,529),fill='#70b8b0')
        d.text((x,584),facing.upper(),font=font,fill='#e3cf43')
    d.text((18,620),'Fixed body and contact. Authoring only; native acceptance waits for the full set.',font=font,fill='#e5e8d8');p.save(HERE/name)
assembled['west (mirror)']=ImageOps.mirror(assembled['east'])
plate('assembly-comparison.png',assembled,'HUMAN CHILD / continuous shoulders, collar edge and separate foreground-arm ownership',True)
plate('registered-isolated-comparison.png',intact,'INTACT GARMENT / neckline is real; body overlap is not missing cloth')
plate('effective-coverage-comparison.png',effective,'EFFECTIVE FLAT LAYER / intentional body overlap; intact garment preserved separately')
small=Image.new('RGB',(480,340),'#142823')
for i,im in enumerate(assembled.values()):
    t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*120+35,15),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*120+12,125),t)
small.save(HERE/'game-scale-review.png')
for n,v in [('model.json',model),('registration-decisions.json',decisions)]: (HERE/n).write_bytes((json.dumps(v,indent=2)+'\n').encode())
