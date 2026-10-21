"""Register direct Blender states in the unchanged source frame; finish contours."""
from pathlib import Path
import copy,json,hashlib
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'model.json').exists()
model=copy.deepcopy(json.loads((OLD/'registered/model.json').read_text()))
model.update(workflow='blender-first-v1',blender_source=ref(HERE/'door.blend'),blender_controls=ref(HERE/'model-controls.json'),
    correction='Fixed jamb straps, shared hinge barrels and rotating leaf straps physically bridge frame and slate in both source states. One complete 3D leaf rotates around a shared left hinge axis.',
    source_packet=ref(OLD/'source-packet.json'),native_acceptance='Pending full generation gate; authoring only')
groups={};diagnostics={}
for state in ['closed','open']:
    parts={};rows=[]
    for name,role in [('frame','detail'),('leaf','foreground')]:
        raw=Image.open(HERE/f'raw-{state}-{name}.png').convert('RGBA');a=np.array(raw);alpha=a[:,:,3].copy();lum=np.uint8(np.round(a[:,:,:3].mean(2)))
        if name=='leaf':
            # Deterministic inner black contour on the direct alpha silhouette.
            distance=distance_transform_edt(alpha>=128)
            boundary=(distance<=1.8)&(alpha>0);lum[boundary]=np.minimum(lum[boundary],45)
        a[:,:,:3]=lum[:,:,None];a[alpha==0,:3]=0;finished=Image.fromarray(a)
        assert np.array_equal(np.array(finished)[:,:,3],alpha)
        finished.save(OUT/f'{state}-{name}-master.png');parts[name]=finished
        small=finished.resize((256,256),Image.Resampling.LANCZOS)
        p=OUT/f'{state}-{name}-neutral.png';small.save(p);coverage=OUT/f'{state}-{name}-coverage.png';small.getchannel('A').save(coverage)
        rows.append(dict(component=name,color_role=role,texture=ref(p),coverage=ref(coverage)))
    composition=Image.alpha_composite(parts['frame'],parts['leaf']);composition.save(OUT/f'{state}-neutral-composition.png')
    native=np.array(composition);native[:,:,:3]=np.uint8(np.round(native[:,:,:3].astype(float)*np.array([177,201,195])/255));native=Image.fromarray(native);native.save(OUT/f'{state}-native-preview.png')
    groups[state]=composition;groups[state+' / native']=native;model['states'][state]['layers']=rows
    diagnostics[state]=dict(alpha_unchanged_by_contour=True,frame_first_then_leaf=True,common_frame=[512,768],anchor=[8,16])
assert (OUT/'closed-frame-neutral.png').read_bytes()==(OUT/'open-frame-neutral.png').read_bytes()
assert (OUT/'closed-frame-master.png').read_bytes()==(OUT/'open-frame-master.png').read_bytes()
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(method='One fixed source-coordinate projection and full-canvas 256-square recipient mapping for both states. Complete source renders retained; only neutral RGB and 1.8px internal contour finishing.',
    depth='Frame first, shared fixed hinge/leaf layer above. Hardware overlaps actual jamb and slab; no invented floating panel.',checks=diagnostics,
    source_selection='Direct Blender projection with retained source slate wear; no new ImageGen call needed.',native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
plate=Image.new('RGB',(1440,825),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'DOOR / connected shared hinge axis / direct Blender states',font=font,fill='#e3cf43')
for x,key in zip([20,380,740,1100],['closed','open','closed / native','open / native']):
    image=groups[key];bg=Image.new('RGBA',image.size,'#20382d');bg.alpha_composite(image);plate.paste(bg.convert('RGB').resize((288,432)),(x,65));d.text((x,518),key,font=font,fill='#e3cf43')
    for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
        small=image.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+30+i*85,570),small)
for i,line in enumerate(['One fixed arch and pivot. Fixed jamb straps, barrel and rotating leaf straps overlap in both states.',
    'The complete slate leaf turns 90 degrees; no independently positioned open strip or bounding-box fit.',
    'Original surface hand wear retained; old painted hardware removed before mapping to real hinges.',
    'Frame/detail and leaf/foreground remain separate y/y roles. Native mechanics and visibility acceptance pending.']):d.text((20,670+32*i),line,font=font,fill='#e5e8d8')
plate.save(OUT/'states-comparison.png')
close=Image.new('RGB',(1200,530),'#142823');d=ImageDraw.Draw(close)
images=[('OLD CLOSED',OLD/'registered/closed-neutral-composition.png'),('NEW CLOSED',OUT/'closed-neutral-composition.png'),('OLD OPEN',OLD/'registered/open-neutral-composition.png'),('NEW OPEN',OUT/'open-neutral-composition.png')]
for i,(label,path) in enumerate(images):
    im=Image.open(path).convert('RGBA').crop((25,290,160,405));bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);close.paste(bg.convert('RGB').resize((270,230)),(i*300+10,55));d.text((i*300+10,15),label,font=font,fill='#e3cf43')
d.text((15,330),'Top hinge: old detached panel versus connected jamb strap / barrel / rotating slab strap.',font=font,fill='white')
d.text((15,370),'All images share source coordinates. Rear depth and hardware dimensions are authored.',font=font,fill='white');close.save(OUT/'hinge-before-after.png')
print('Both direct states registered; full-state independent review pending.')
