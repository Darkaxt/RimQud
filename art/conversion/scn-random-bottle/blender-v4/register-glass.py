"""Keep translucent coverage and conditional glass/liquid tint ownership separate."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
def linear(v):return np.where(v<=.04045,v/12.92,((v+.055)/1.055)**2.4)
assert not (OUT/'model.json').exists()
full=np.array(Image.open(HERE/'raw-filled-neutral.png').convert('RGBA'));con=np.array(Image.open(HERE/'raw-liquid-contribution.png').convert('RGBA'))
assert np.array_equal(full[:,:,3],con[:,:,3]),'Semantic pass must retain identical glass/liquid opacity'
lum=full[:,:,:3].mean(2)/255;part=con[:,:,:3].mean(2)/255
weight=np.clip(np.divide(linear(part),linear(lum),out=np.zeros(lum.shape),where=lum>0),0,1)
full[:,:,:3]=np.uint8(np.round(lum*255))[:,:,None];full[full[:,:,3]==0,:3]=0
coverage=full[:,:,3];dcov=np.uint8(np.round(coverage*weight))
primary=np.array(Image.fromarray(full).resize((256,256),Image.Resampling.LANCZOS));primary[primary[:,:,3]<4]=0
detail_alpha=np.minimum(np.array(Image.fromarray(dcov).resize((256,256),Image.Resampling.LANCZOS)),primary[:,:,3])
w=np.clip(np.divide(detail_alpha.astype(float),primary[:,:,3],out=np.zeros(detail_alpha.shape),where=primary[:,:,3]>0),0,1)
wb=np.uint8(np.round(w*255));detail=primary.copy();detail[:,:,3]=detail_alpha;detail[detail_alpha==0,:3]=0
files=dict(primary=Image.fromarray(primary),detail=Image.fromarray(detail),coverage=Image.fromarray(primary[:,:,3]),detail_weight=Image.fromarray(wb),detail_coverage=Image.fromarray(detail_alpha),authored_dualcolor_mask=Image.fromarray(np.dstack([wb,wb,wb,primary[:,:,3]])))
row=dict(native_tile='Items/sw_jug2.bmp')
for k,im in files.items():
 p=OUT/f'bottle-{k}.png';im.save(p);row[k]=ref(p)
empty=Image.open(HERE/'raw-empty-glass.png').convert('RGBA').resize((256,256),Image.Resampling.LANCZOS);empty.save(OUT/'empty-glass-authoring-layer.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];cyan=np.array(list(bytes.fromhex(palette['c'])));gold=np.array(list(bytes.fromhex(palette['W'])))
def tint(a,t,fg,dc):
 result=a.copy();result[:,:,:3]=np.uint8(np.round(a[:,:,:3]*((1-t[:,:,None])*fg+t[:,:,None]*dc)/255));result[result[:,:,3]==0,:3]=0;return Image.fromarray(result)
native=tint(primary,w,cyan,cyan);native.save(OUT/'native-c-c.png');probe=tint(primary,w,cyan,gold);probe.save(OUT/'illustrative-liquid-color-probe.png')
model=dict(entry='SCN-RANDOM-BOTTLE',kind='source_dualcolor_translucent_glass_container',blueprint='Random Bottle',workflow='blender-first-v1',source=ref(HERE.parent/'blender-v1/source-packet.json'),blender_source=ref(HERE/'bottle.blend'),blender_controls=ref(HERE/'model-controls.json'),
 registration=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One full source-cell projection. No alpha-bounds recentering.'),
 palette=dict(primary='c glass shell',detail='c default; native DetailColorByLiquid controls liquid color',rule='Single coverage, conditional liquid contribution. Glass stays translucent.'),
 formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background',frames=[row],
 glass_and_liquid=dict(shell='Actual hollow connected glass wall and handle with Fresnel opacity',liquid='Independent closed geometry inside the bowl',fill_height='Authored from original lower detail band, not a measured native volume',empty_authoring_layer=ref(OUT/'empty-glass-authoring-layer.png'),native_dispatch='Actual contents, volume, empty/filled state and seal dispatch remain native; no new state tiles or simulation authored.'),
 native_behavior='Capacity16, RandomLiquid1d8 filler, ManualSeal, LiquidVisibleWhenSealed, Transparent, ShattersOnHit and original physics/contents remain native.',view_policy='One fixed source map tile, no unsupported rotation/state family.',native_activation=False,native_acceptance='Pending full generation gate')
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(method='Same full-frame render plus identical-opacity black-glass semantic contribution. Linearized liquid/full RGB ratio gives conditional detail ownership, then same registration for all layers.',alpha_equal=True,detail_coverage_subset=bool(np.all(detail_alpha<=primary[:,:,3])),neutral_equal_rgb=bool(np.all(primary[:,:,0]==primary[:,:,1]) and np.all(primary[:,:,1]==primary[:,:,2])),new_native_states=False,new_imagegen_call=False,selection='Direct Blender glass optics preserve physical shell/handle and visible contained liquid.',native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1400,800),'#142823');d=ImageDraw.Draw(plate)
items=[('FILLED / neutral',Image.fromarray(full)),('EMPTY / glass layer',Image.open(HERE/'raw-empty-glass.png')),('SOURCE c/c',tint(full,weight,cyan,cyan)),('LIQUID ROLE / color probe',tint(full,weight,cyan,gold))]
for i,(label,im) in enumerate(items):
 im=im.convert('RGBA');bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((310,465)),(15+i*345,55));d.text((15+i*345,20),label,font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  small=im.resize(size,Image.Resampling.LANCZOS);plate.paste(small,(70+i*345+j*75,550),small)
for i,line in enumerate(['Transparent hollow glass shell and independent liquid; the native lower band suggests the authored fill extent.',
 'One source map frame/anchor. The gold liquid is an ownership demonstration, not a claimed native content.',
 'Same full-cell scale at 16x24 / 24x36 / 32x48. Empty glass is a retained authoring layer, not a new native tile.',
 'Original native liquid color, volume and sealing remain native. Authoring evidence only; no in-game acceptance yet.']):d.text((15,655+i*30),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
print('Translucent bottle registered with separate conditional liquid tint and single coverage.')
