"""Select contextual metal inside fixed wrench geometry; complete hidden grip."""
from pathlib import Path
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-male/v2';SIZE=(512,1024);FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
SOURCE=ROOT/'art/conversion/fit-human-female-wrench/v1'
canonical=read(HERE/'intact-canonical.png');detail=read(HERE/'shaft-canonical.png')
assert canonical.tobytes()==read(SOURCE/'intact-canonical.png').tobytes()
packet=json.loads((HERE/'source-packet.json').read_text());controls=json.loads((HERE/'fit-controls.json').read_text());bm=json.loads((BODY/'model.json').read_text());groups={k:{} for k in ['assembly','palette','full','off','grip']};registered={}
model=dict(item='Wrench',blueprint='Wrench',family='human-male',slot='Hand',laterality=1,canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],observed_bindings=packet['observed_bindings'],weapon_metadata=packet['weapon_metadata'],views={},binding_scope='Actual captured male Argyve519 ordinary Hand322/1. Shared male baseline only; side far-hand depth is provisional authoring, not a new limb model.',policy='Complete hooked metal jaw/shaft with visible thread detail and lower grip. Head primary y, shaft detail c. Original body preserved; no decorative-prop size substitution or invented counterweight.',west_policy='Mirrored unmarked profile source for authoring; actual left/right near/far hand and native aim-state mapping pending.',pose='Stationary authoring display only. Ready one-handed side presentation must project forward/horizontally90deg to upright body; resting/ready/native offhand state remains unfinished.',native_acceptance='Pending full-set generation and actual native offhand, pose state and named Argyve assembly.')
for facing,c in controls.items():
    def place(im):
        source=ImageOps.mirror(im) if c['mirror'] else im
        return source.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC).convert('RGBA')
    item=place(canonical);shaft_item=place(detail);item.save(HERE/f'intact-item-{facing}.png');shaft_item.save(HERE/f'item-detail-{facing}.png');body=read(BODY/f'selected-{facing}.png');hand=read(HERE/f'original-hand-{facing}.png');equipment=Image.alpha_composite(item,shaft_item)
    off=Image.alpha_composite(body,equipment);assembly=Image.alpha_composite(equipment,body) if facing!='south' else Image.alpha_composite(off,hand)
    assembly.save(HERE/f'assembled-{facing}.png');off.save(HERE/f'depth-off-{facing}.png')
    colored_item=Image.alpha_composite(tint(item,(177,201,195)),tint(shaft_item,(64,164,185)));body_color=tint(body,(64,164,185));hand_color=tint(hand,(64,164,185));colored=Image.alpha_composite(colored_item,body_color) if facing!='south' else Image.alpha_composite(Image.alpha_composite(body_color,colored_item),hand_color);colored.save(HERE/f'qud-palette-{facing}.png')
    for key,im in [('assembly',assembly),('palette',colored),('full',equipment),('off',off)]:groups[key][facing]=im
    gx,gy=c['grip'];groups['grip'][facing]=assembly.crop((gx-70,gy-160,gx+80,gy+95)).resize((240,408))
    rows=[]
    for component,stem,role,layer in [('item','intact-item','equipment',.0018 if facing=='south' else -.0002),('item-detail','item-detail','equipment-detail',.00181 if facing=='south' else -.00019),('body-overlay','original-hand','foreground',.0019)]:
        p=HERE/f'{stem}-{facing}.png';r=ref(p);row=dict(bm['views'][facing][0]);row.update(component=component,file=f'human-male-wrench-v1-{component}-{facing}.png',public_file=r['path'],sha256=r['sha256'],equipment_key='wrench@Hand@1',color_role=role,layer=layer);rows.append(row)
    model['views'][facing]=rows;registered[facing]=dict(inverse_affine=c['inverse_affine'],mirror=c['mirror'],item_space_grip=[256,590],body_hand_landmark=c['grip'],body=ref(BODY/f'selected-{facing}.png'),full_item=ref(HERE/f'intact-item-{facing}.png'),original_hand=ref(HERE/f'original-hand-{facing}.png'),body_pixels_changed=False)
for group in groups.values():group['west (mirror)']=ImageOps.mirror(group['east'])
def plate(images,name,title,zoom=False):
    out=Image.new('RGB',(1152,665),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,408 if zoom else 512)),(16+i*284,54));d.text((16+i*284,584),f.upper(),font=FONT,fill='#e3cf43')
    d.text((18,622),'Actual male offhand. Fixed body; armlength tool; native offhand/pose acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
for key,name,title,zoom in [('assembly','assembly-comparison.png','WRENCH / Qud hooked jaw and armlength shaft / actual male offhand',False),('palette','independent-palette-comparison.png','PALETTE / primary head y, shaft c; actual Argyve body c, independent',False),('full','full-item-comparison.png','FULL METAL TOOL / complete jaw opening, neck, threaded iron and lower shaft',False),('off','depth-off-comparison.png','DEPTH OFF / full tool before original palm/body ownership',False),('grip','grip-comparison.png','GRIP / original front palm; side/back far tool under original body',True)]:plate(groups[key],name,title,zoom)
small=Image.new('RGB',(560,370),'#142823');draw=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*140+45,20),thumb);thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*140+20,138),thumb);draw.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
model['item_raster_scale']=packet['frame']['item_scale']
write('model.json',model);write('registration-decisions.json',dict(canonical_source=ref(SOURCE/'intact-canonical.png'),structural_gate=ref(SOURCE/'first-refinement-structural-review.json'),source_reused_byte_for_byte=True,views=registered,new_imagegen_calls=0,second_isolation_call=False,item_scale=packet['frame']['item_scale'],physical_item_size_changed=False,pose_followup=model['pose']))
print('Registered identical full Wrench on male ordinary offhand, no new ImageGen call; authoring review pending.')
