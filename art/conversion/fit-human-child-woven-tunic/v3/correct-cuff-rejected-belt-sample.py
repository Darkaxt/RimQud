"""Remove rear cuff surfaces from the foreground export on the fixed body."""
from pathlib import Path
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageOps
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v2';BODY=ROOT/'art/conversion/body-human-child/v1'
assert not (HERE/'model.json').exists(),'Preserve recorded versions'
def asset(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def svgmask(name,path):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><path fill="white" d="'+path+'"/></svg>'
    p=HERE/(name+'.svg');p.write_bytes(svg.encode());(HERE/(name+'.png')).write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True));return Image.open(HERE/(name+'.png')).getchannel('A')
# Actual front fabric edges, not the lower/back edge of a closed cuff oval.
front_path='M105 533 L164 562 L174 580 L174 602 L95 602Z M347 562 L405 533 L416 602 L339 602 L339 580Z'
cap_path='M226 550 Q240 527 266 527 Q293 523 325 534 L324 563 L220 563Z'
arm_path='M224 551 Q237 530 255 528 Q275 523 295 530 L294 546 L289 560 Q290 580 295 607 L294 639 C305 645 315 658 303 676 C294 690 274 695 261 685 C246 676 244 656 255 645 L243 612 Q229 578 224 551Z'
cap=svgmask('rear-cuff-cap-region',cap_path);exposed=svgmask('exposed-profile-arm',arm_path)
model=json.loads((OLD/'model.json').read_text());model['views']={};model['layer_order']='unchanged body/head -> camera-visible tunic only; rear cuff fill excluded from exposed limb'
record={'supersedes':asset(OLD/'model.json'),'body':asset(BODY/'model.json'),'method':'Per-facing foreground cuff ownership. Preserve existing refined cloth/frame. Remove rear/interior cuff surfaces and foreign lower oval from the foreground layer; extend profile arm transparency through the true visible front cuff edge.','new_imagegen_call':False,'imagegen_provenance':'Actual v2 context refinement and isolation remain in the entry history; this is extraction/ownership correction, not a new generated proposal.','views':{}}
packet=json.loads((OLD/'source-packet.json').read_text());packet['correction']='Foreground-only cuff ownership; no opaque rear cap over exposed arm. Unchanged Qud item identity, body, frame, palette and refinement sources.';packet['supersedes']=asset(OLD/'source-packet.json');packet['new_imagegen_call']=False
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
assemblies={};garments={};before={}
for facing in ['south','east','north']:
    cloth=Image.open(OLD/f'tunic-{facing}.png').convert('RGBA');body=Image.open(BODY/f'selected-{facing}.png').convert('RGBA');before[facing]=Image.alpha_composite(body,cloth)
    if facing=='east':
        # The old sleeve cap also covered garment torso behind the near arm.
        # Restore that visible torso fabric from the existing intact cloth;
        # do not reveal bare chest or retain a dark back-facing cuff cap there.
        intact=Image.open(OLD/'intact-tunic-east.png').convert('RGBA');continuation=Image.new('RGBA',cloth.size)
        continuation.paste(intact.crop((0,44,512,1024)),(0,0))
        cloth=Image.composite(continuation,cloth,cap)
        cut=ImageChops.multiply(exposed,body.getchannel('A'))
        # Previously correct lower forearm/hand ownership remains in force.
        cut=ImageChops.lighter(cut,Image.open(OLD/'body-occlusion-east.png').convert('L'))
    else:cut=svgmask('rear-cuff-removal-'+facing,front_path)
    cut.save(HERE/f'foreground-cut-{facing}.png');cloth.putalpha(ImageChops.subtract(cloth.getchannel('A'),cut))
    cloth.paste((0,0,0,0),mask=cloth.getchannel('A').point(lambda a:255 if a==0 else 0));cloth.save(HERE/f'tunic-{facing}.png');garments[facing]=cloth
    composed=Image.alpha_composite(body,cloth);composed.save(HERE/f'assembled-{facing}.png');assemblies[facing]=composed
    row=dict(json.loads((OLD/'model.json').read_text())['views'][facing][0]);row.update(file=f'child-woven-tunic-v3-{facing}.png',public_file=(HERE/f'tunic-{facing}.png').relative_to(ROOT).as_posix(),sha256=asset(HERE/f'tunic-{facing}.png')['sha256']);model['views'][facing]=[row]
    record['views'][facing]={'source':asset(OLD/f'tunic-{facing}.png'),'foreground_cut':asset(HERE/f'foreground-cut-{facing}.png'),'output':asset(HERE/f'tunic-{facing}.png'),'body_unchanged':asset(BODY/f'selected-{facing}.png')}
record['profile_torso_material_continuation']={'source':asset(OLD/'intact-tunic-east.png'),'sample_offset_y':44,'region':asset(HERE/'rear-cuff-cap-region.png'),'purpose':'Remove generated rear-cap RGB/outline and retain actual visible torso cloth outside the exposed-arm mask. No fill is allowed over the exposed limb.'}
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(name,rows,title):
    p=Image.new('RGB',(1152,660),'#142823');d=ImageDraw.Draw(p);d.text((18,14),title,font=font,fill='#e3cf43')
    for i,(label,im) in enumerate(rows.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=i*288+16;p.paste(bg.convert('RGB').resize((256,512)),(x,54));d.line((x+128,54,x+128,565),fill='#cebc45');d.line((x,529,x+255,529),fill='#70b8b0');d.text((x,584),label.upper(),font=font,fill='#e3cf43')
    d.text((18,620),'Unchanged body and frame. Foreground clothing contains no opaque rear cuff cap over the limb.',font=font,fill='#e5e8d8');p.save(HERE/name)
assemblies['west (mirror)']=ImageOps.mirror(assemblies['east']);plate('assembly-comparison.png',assemblies,'HUMAN CHILD / foreground-only cloth; exposed arm clear through sleeve opening')
plate('foreground-cloth-comparison.png',garments,'PRODUCTION CLOTHING / rear cuff surfaces excluded; intact v2 remains reference only')
comparison=Image.new('RGB',(1000,640),'#142823');d=ImageDraw.Draw(comparison)
for x,im,label in [(30,before['east'],'BEFORE / opaque rear cuff'),(515,assemblies['east'],'AFTER / exposed actual arm')]:
    crop=im.crop((195,485,345,705)).resize((390,572),Image.Resampling.NEAREST);comparison.paste(crop,(x,45),crop);d.text((x,15),label,font=font,fill='#e3cf43')
comparison.save(HERE/'cuff-ownership-before-after.png')
small=Image.new('RGB',(480,340),'#142823')
for i,im in enumerate(assemblies.values()):
    t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*120+35,15),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*120+12,125),t)
small.save(HERE/'game-scale-review.png')
for n,v in [('model.json',model),('ownership-decisions.json',record)]: (HERE/n).write_bytes((json.dumps(v,indent=2)+'\n').encode())
