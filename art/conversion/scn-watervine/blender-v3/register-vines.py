"""Register all three Blender layouts with one geometry for both harvest tints."""
from pathlib import Path
import json,hashlib,copy
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'model.json').exists()
model=copy.deepcopy(json.loads((OLD/'registered/model.json').read_text()));palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def neutral(p):
    a=np.array(Image.open(p).convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def tint(im,color):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float)*np.array(list(bytes.fromhex(palette[color])))/255));return Image.fromarray(a)
previews={}
for state in model['states']:
    n=state['variant'];full=neutral(HERE/f'variant-{n}-neutral-master.png');wafer=neutral(HERE/f'variant-{n}-wafer-master.png')
    primary=full.resize((256,256),Image.Resampling.LANCZOS);detail=wafer.resize((256,256),Image.Resampling.LANCZOS)
    for im in [primary,detail]:
        a=np.array(im);a[a[:,:,3]<4]=0;im.paste(Image.fromarray(a))
    # Semantic detail owns only alpha already present in the complete image.
    da=np.minimum(np.array(detail)[:,:,3],np.array(primary)[:,:,3]);detail.putalpha(Image.fromarray(da))
    for key,im in [('primary',primary),('detail',detail)]:
        p=OUT/f'variant-{n}-{key}-neutral.png';im.save(p);state[key]=ref(p)
    for key,im in [('coverage',primary),('detail_coverage',detail)]:
        p=OUT/f'variant-{n}-{key}.png';im.getchannel('A').save(p);state[key]=ref(p)
    previews[n]={'neutral':full}
    for label,color in [('ripe','g'),('unripe','K')]:
        p=tint(primary,'w');p.alpha_composite(tint(detail,color));p.save(OUT/f'variant-{n}-{label}-preview.png')
        big=tint(full,'w');big.alpha_composite(tint(wafer,color));previews[n][label]=big
model.update(workflow='blender-first-v1',blender_source=ref(HERE/'vines.blend'),blender_controls=ref(HERE/'model-controls.json'),
    correction='Each creeping tendril starts inside its own actual stem endpoint. One editable layout supplies both harvest colors; native wafer positions and counts retained.',
    native_acceptance='Pending full generation gate')
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(method='One full source-cell mapping:512x768 direct renders to256x256 recipient. Same masks/geometry for ripe and unripe; no per-variant recentering.',
    primary='Neutral complete vine and wafers, native w',detail='Neutral physically rendered wafer ownership, native g or K',
    source_selection='Direct Blender three-tone surfaces and contour. No ImageGen call or second isolation.',native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,2050),'#142823');d=ImageDraw.Draw(plate)
for row,label in enumerate(['neutral','ripe','unripe']):
    y=45+row*650;d.text((20,y-25),'WATERVINE / '+label.upper()+' / connected source-layout stems and swollen wafers',font=font,fill='#e3cf43')
    for col,n in enumerate([1,2,3]):
        x=20+col*480;im=previews[n][label];bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((320,480)),(x+65,y))
        d.text((x+30,y+495),f'Variant{n} / same source cell',font=font,fill='#e3cf43')
        for k,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
            small=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(small,(x+60+k*95,y+540),small)
d.text((20,2010),'Common source anchor and native palette/state ownership. Static authoring; native acceptance pending.',font=font,fill='white');plate.save(OUT/'registration-comparison.png')
plate=Image.new('RGB',(1440,620),'#142823');d=ImageDraw.Draw(plate)
for col,n in enumerate([1,2,3]):
    for row,(label,path) in enumerate([('OLD',OLD/f'registered/variant-{n}-neutral-master.png'),('NEW',HERE/f'variant-{n}-neutral-master.png')]):
        im=Image.open(path).convert('RGBA').resize((512,768),Image.Resampling.LANCZOS).crop((45,600,470,745));bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB'),(col*480+20,row*280+40));d.text((col*480+20,row*280+10),f'{label} VARIANT{n} / BASES',font=font,fill='#e3cf43')
d.text((20,595),'Each new tendril overlaps its actual stem. No copied global basal strokes.',font=font,fill='white');plate.save(OUT/'basal-before-after.png')
print('Registered all three vine layouts and both native harvest tints; review pending.')
