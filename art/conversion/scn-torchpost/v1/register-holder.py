"""Register neutral holder material, detail-only source tint and unchanged native effect ownership."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,math
import numpy as np
from scipy.ndimage import gaussian_filter,binary_erosion
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];CON=HERE/'construction-v3';OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def save(p,a):Image.fromarray(a).save(p)
assert not (OUT/'model.json').exists();controls=read(CON/'construction-controls.json');packet=read(HERE/'source-packet.json');raw=Image.open(HERE/'refined-raw.png').convert('RGBA');w,h=raw.size
boxes={'wood':[round(w*.163),round(h*.585),round(w*.184),round(h*.69)],'iron':[round(w*.095),round(h*.26),round(w*.145),round(h*.275)]};materials={};selection={}
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16);specimens=Image.new('RGB',(1300,650),'#142823');d=ImageDraw.Draw(specimens);small=raw.copy();small.thumbnail((760,440));specimens.paste(small,(20,75),small);d.text((20,20),'TORCHPOST / actual refinement: selected material interiors only',font=font,fill='#e3cf43')
for i,(name,box) in enumerate(boxes.items()):
    patch=raw.crop(box);a=np.array(patch);assert a[:,:,3].min()>=250;f=HERE/f'selected-{name}.png';patch.save(f);g=a[:,:,:3].astype(float).mean(2);limit=3 if name=='wood' else 1.5;residue=np.clip((g-gaussian_filter(g,2))*.15,-limit,limit);materials[name]=residue
    selection[name]=dict(box=box,specimen=ref(f),alpha_min=int(a[:,:,3].min()),limit_gray_levels=limit,role='Opaque unmarked material interior; no source chroma, mean lighting, contour, alpha or generated geometry transferred.')
    preview=patch.resize((440,180),Image.Resampling.NEAREST);specimens.paste(preview,(820,70+i*270),preview);d.text((820,40+i*270),name.upper()+' / GRAYSCALE RESIDUAL ONLY',font=font,fill='#e3cf43')
    scale=small.width/raw.width;d.rectangle(tuple(round(v*scale+(20 if j%2==0 else 75)) for j,v in enumerate(box)),outline='#e3cf43',width=2)
specimens.save(HERE/'selected-material-specimens.png')
write(HERE/'material-selection.json',dict(actual_source=ref(HERE/'refined-raw.png'),materials=selection,initial_box_note='Initial wood diagnostic box touched a dark boundary/strut. Final narrower/lower interior excludes it; initial box file retained as diagnostic history.',method='Mean RGB to neutral luminance; subtract Gaussian2 broad shading, attenuate15percent, clamp wood+/-3/iron+/-1.5. Fixed material ownership/ink/alpha remain authoritative. No warm generated wood hue, shiny border, flame or second isolation.'))
write(HERE/'first-structural-review.json',dict(status='PASS FOR CONTROLLED MATERIAL REGISTRATION',source=ref(HERE/'refined-raw.png'),review='Three complete flame-free holders retain common broad rim/short wood stem/connected supports, naturally narrower east depth, coherent reverse and open gaps. No structural failure requiring another contextual call. Actual refinement is heavier/shinier and has slight warm wood chroma; exclude generated geometry, alpha, hue and broad illumination.',patch='Initial strut endpoints moved inside rim volume; final inner/outer rim walls close far strut occlusion. Corrected shared construction preceded this actual generation. Final material transfer preserves that geometry and full native cell placement.',calls=1,second_isolation=False))
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];color=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8).astype(float)
def tint(a):
    rgb=np.uint8(np.rint(a[:,:,:3].astype(float).mean(2)[:,:,None]/255*color));rgb[a[:,:,3]==0]=0;return np.dstack([rgb,a[:,:,3]])
model=dict(entry='SCN-TORCHPOST',blueprint='Torchpost',kind='native-particle sconce: static detail-only holder furniture',source=ref(HERE/'source-packet.json'),construction=ref(CON/'construction-controls.json'),refinement=ref(HERE/'generation-receipt.json'),material_selection=ref(HERE/'material-selection.json'),structural_review=ref(HERE/'first-structural-review.json'),registration=controls['frame'],physical_dimensions=controls['physical_dimensions'],dimension_provenance=controls['provenance'],
    palette=packet['palette'],effects=packet['effects'],views={},binding='Exact Torchpost static nofire tile only. Native TorchpostFlames prefab/origin/visibility and LightSource Radius6 retained. Other furniture facings are unbound authoring; no runtime rotation or wall placement implemented.',
    states='Native foreground R/W/r/W animation and separate particle fire remain under existing owners. All static holder pixels are detail w, so foreground changes do not recolor it. Unlit Torchpost is separate blueprint, not an invented toggle/converted identity.',
    clothing='Not applicable to fixed sconce.',native_activation=False,native_acceptance='Pending full-ledger generation, then integrated exact tile/cell/pivot/detail-w/prefab visibility/lighting behavior and supported placement review. No native effect or state test during authoring.')
full=Image.new('RGBA',(1536,768));nativefull=Image.new('RGBA',(1536,768));rolefull=Image.new('RGBA',(1536,768))
for j,facing in enumerate(['south','east','north']):
    view=controls['views'][facing];a=np.array(Image.open(ROOT/view['constructed']['path']).convert('RGBA'));lum=a[:,:,:3].astype(float).mean(2);wood=np.array(Image.open(ROOT/view['material_ownership']['wood']['path']).convert('RGBA'))[:,:,3]>127;iron=np.array(Image.open(ROOT/view['material_ownership']['iron']['path']).convert('RGBA'))[:,:,3]>127
    for role,mask in [('wood',wood&~iron),('iron',iron)]:
        grain=materials[role];tiled=np.tile(grain,(math.ceil(768/grain.shape[0]),math.ceil(512/grain.shape[1])))[:768,:512];inside=binary_erosion(mask&(a[:,:,3]==255)&(lum>100),iterations=2);lum[inside]+=tiled[inside]
    gray=np.uint8(np.clip(np.rint(lum),0,255));master=np.dstack([gray,gray,gray,a[:,:,3]]);master[master[:,:,3]==0,:3]=0;target=OUT/facing;target.mkdir(exist_ok=True)
    small=np.array(Image.fromarray(master).resize((256,256),Image.Resampling.LANCZOS));small[:,:,:3]=np.uint8(np.rint(small[:,:,:3].astype(float).mean(2)))[:,:,None];small[small[:,:,3]==0,:3]=0;alpha=small[:,:,3];weight=np.where(alpha>0,255,0).astype(np.uint8);primary=np.zeros_like(small);dual=np.dstack([weight,weight,weight,alpha])
    for name,data in [('master-neutral.png',master),('primary-neutral.png',primary),('detail-neutral.png',small),('coverage.png',alpha),('detail-weight.png',weight),('detail-coverage.png',alpha),('authored-dualcolor-mask.png',dual),('native-detail-w.png',tint(small))]:save(target/name,data)
    model['views'][facing]={key:ref(target/name) for key,name in [('master','master-neutral.png'),('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png'),('native_preview','native-detail-w.png')]}
    full.alpha_composite(Image.fromarray(master),(j*512,0));nativefull.alpha_composite(Image.fromarray(tint(master)),(j*512,0));rm=np.dstack([np.ones((768,512,3),np.uint8)*255,master[:,:,3]]);rolefull.alpha_composite(Image.fromarray(rm),(j*512,0))
target=OUT/'west';target.mkdir(exist_ok=True);model['views']['west']={}
for key,r in model['views']['east'].items():
    src=ROOT/r['path'];p=target/src.name;Image.open(src).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(p);model['views']['west'][key]=ref(p)
model['west_policy']='Mirror east for this bilaterally symmetric structure/material convention; no markings or asymmetric source anatomy are mirrored onto another face.'
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(method=ref(HERE/'register-holder.py'),construction=ref(CON/'construction-controls.json'),material_selection=ref(HERE/'material-selection.json'),coverage='Exact selected manual master alpha retained. Empty upper cell/native origin preserved; no source padding cropped from production. No generated geometry/outline/alpha or altered particle origin.',
    colour='All source holder pixels are detail; primaryRGBA is completely empty, detail coverage equals object coverage, weight255 wherever covered. Neutral gray only; wood/iron material masks do not create new native tint channels. R/W/r foreground animation has no influence on static holder; native particle remains separate.',
    geometry='Correct strut endpoints inside shared rim volume, then add omitted inner/outer rim walls for far support occlusion before actual refinement. No independent side-panel compression or post-generation stretch.',presentation='Explicit crop(0,480,1536,720) for three-view refinement/report only. Registered sprites keep512x768masters/256square recipient through complete16x24cell mapping.',native_activation=False))
full.save(OUT/'full-cell-turnarounds.png')
for filename,sheet,title in [('neutral-turnarounds.png',full,'NEUTRAL HOLDER / S - E - N / no flame art'),('native-w-turnarounds.png',nativefull,'NATIVE DETAIL w / same holder, native fire remains separate'),('detail-coverage-turnarounds.png',rolefull,'WHITE = DETAIL w COVERAGE / primary empty')]:
    crop=sheet.crop((0,480,1536,720));plate=Image.new('RGB',(1536,330),'#142823');plate.paste(crop,(0,50),crop);d=ImageDraw.Draw(plate);d.text((20,12),title,font=font,fill='#e3cf43')
    for j,f in enumerate(['SOUTH','EAST','NORTH']):d.text((j*512+20,300),f+' / full native frame retained',font=font,fill='#e3cf43')
    plate.save(OUT/filename)
plate=Image.new('RGB',(1320,820),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'TORCHPOST / original holder and new art at equal full-cell scale / native particles not drawn',font=font,fill='#e3cf43')
original=np.array(Image.open(packet['original']['private_mask']['path']).convert('RGBA'));orig=np.zeros_like(original);orig[:,:,:3]=np.uint8(color);orig[:,:,3]=original[:,:,3]
for i,size in enumerate([(32,48),(48,72),(64,96),(96,144)]):
    xx=30+i*320;src=Image.fromarray(orig).resize(size,Image.Resampling.NEAREST);im=Image.open(ROOT/model['views']['south']['master']['path']).convert('RGBA');im=Image.fromarray(tint(np.array(im))).resize(size,Image.Resampling.LANCZOS);plate.paste(src,(xx,95),src);plate.paste(im,(xx+150,95),im);d.text((xx,280),str(size)+' / old -> new',font=font,fill='#e3cf43')
for i,foreground in enumerate(['R','W','r']):
    im=Image.open(ROOT/model['views']['south']['native_preview']['path']).convert('RGBA').resize((256,256));xx=100+i*400;plate.paste(im,(xx,375),im);d.text((xx,680),'Foreground '+foreground+' / detail w',font=font,fill='#e3cf43')
d.text((20,755),'Static pixels stay w for every foreground sample. Existing TorchpostFlames/LightSource own fire and lighting.',font=font,fill='#e5e8d8');plate.save(OUT/'source-native-scale-and-palette.png')
print('Registered detail-only w holder, three shared-geometry views+mirroredW, fixed source padding, native effect ownership unchanged.')
