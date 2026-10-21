"""Remove repeated wire grain and retain source K/k contrast without changing geometry."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OLD=HERE/'registration-initial';assert not OLD.exists();OLD.mkdir()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
for name in ['neutral-family.png','native-K-family.png','game-scale-source-comparison.png']:shutil.copyfile(OUT/name,OLD/name)
controls=read(HERE/'construction-controls.json');selection=read(HERE/'material-selection.json');model=read(OUT/'model.json');palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];fg=np.frombuffer(bytes.fromhex(palette['K']),dtype=np.uint8);bg=tuple(bytes.fromhex(palette['k']));grains={}
for item in selection['selected']:
    name=item['material'];a=np.array(Image.open(ROOT/item['specimen']['path']).convert('RGBA'));g=a[:,:,:3].astype(float).mean(2)
    residual=np.clip(g-gaussian_filter(g,2.0),-18,18)*.45
    repeat=np.block([[residual,residual[:,::-1]],[residual[::-1,:],residual[::-1,::-1]]]);repeat=np.array(Image.fromarray(repeat.astype(np.float32)).resize((repeat.shape[1]*2,repeat.shape[0]*2),Image.Resampling.BICUBIC))
    grains[name]=np.tile(repeat,(int(np.ceil(768/repeat.shape[0])),int(np.ceil(512/repeat.shape[1]))))[:768,:512]
neutral={};native={}
for state,item in zip(model['states'],controls['states']):
    ident=state['id'];folder=OUT/ident;shutil.copyfile(folder/'primary-master.png',OLD/(ident+'-primary-master.png'))
    a=np.array(Image.open(ROOT/item['constructed']['path']).convert('RGBA'));luma=a[:,:,:3].astype(float).mean(2);total=np.zeros(luma.shape)
    for name in grains:
        weight=np.array(Image.open(folder/f'ownership-{name}-master.png').convert('L')).astype(float)/255;total+=weight
        if name!='wire':luma+=grains[name]*weight
    total=np.clip(total,0,1);luma=luma*(1-total)+(156+.35*luma)*total
    a[:,:,:3]=np.uint8(np.clip(np.round(luma),0,255))[:,:,None];a[a[:,:,3]==0,:3]=0;master=Image.fromarray(a);master.save(folder/'primary-master.png')
    out=np.array(master.resize((256,256),Image.Resampling.LANCZOS));out[:,:,:3]=np.uint8(np.round(out[:,:,:3].astype(float).mean(2)))[:,:,None];out[out[:,:,3]==0,:3]=0;im=Image.fromarray(out);im.save(folder/'primary-neutral.png');neutral[ident]=im
    colored=out.copy();colored[:,:,:3]=np.uint8(np.round(out[:,:,:3].astype(float)*fg/255));colored[colored[:,:,3]==0,:3]=0;im=Image.fromarray(colored);im.save(folder/'native-K.png');native[ident]=im
    state.update(primary=ref(folder/'primary-neutral.png'),master=ref(folder/'primary-master.png'),native_preview=ref(folder/'native-K.png'))
correction=dict(defects=['Initial wire specimen residual repeated as a visible band/grid, despite correct fragment alpha.','Initial broad material shading reduced K-on-k contrast below the source glyph presentation.'],
    changes=['Keep wire manual luminance/highlight geometry; do not transfer generated wire grain. Other3materials retain bounded generated surface residuals.','Compress only material-interior shading toward source foreground:156+0.35*luminance. Original ink, contour, recess and highlight ownership is retained.'],
    unchanged='Every manual curve, source-layout position, alpha gap/coverage, full source-cell mapping, primary K, background k, empty detail role and native selection/behavior.',
    previous=ref(OLD/'game-scale-source-comparison.png'),method=ref(HERE/'correct-readability.py'),native_activation=False)
write(HERE/'readability-correction.json',correction);model['readability_correction']=ref(HERE/'readability-correction.json');model['primary']=model['states'][-1]['primary'];write(OUT/'model.json',model)
decisions=read(OUT/'registration-decisions.json');decisions['final_correction']=ref(HERE/'readability-correction.json');write(OUT/'registration-decisions.json',decisions)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for label,group in [('neutral',neutral),('native-K',native)]:
    plate=Image.new('RGB',(1400,520),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'GARBAGE / '+label+' / all4native choices + distinct declared fallback',font=font,fill='#e3cf43')
    for i,(ident,im) in enumerate(group.items()):
        im=im.resize((224,336),Image.Resampling.LANCZOS);xx=25+i*275;plate.paste(im,(xx,55),im);d.text((xx,420),ident.upper(),font=font,fill='#e3cf43')
    d.text((18,475),'Same source-cell layout; native selection/behavior unchanged. No native acceptance.',font=font,fill='#e5e8d8');plate.save(OUT/f'{label}-family.png')
plate=Image.new('RGB',(1400,650),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'GARBAGE / original K on native k background, then new K art at24x36 and48x72',font=font,fill='#e3cf43');sources=read(HERE/'native-state-index.json')['states']
for i,(ident,im) in enumerate(native.items()):
    xx=25+i*275;mask=np.array(Image.open(sources[i]['private_mask']['path']).convert('RGBA'));original=Image.fromarray(np.dstack([np.broadcast_to(fg,mask[:,:,:3].shape),mask[:,:,3]]))
    for jj,tile in enumerate([original,im]):
        canvas=Image.new('RGBA',(96,144),(*bg,255));small=tile.resize((24,36),Image.Resampling.LANCZOS);canvas.alpha_composite(small,(8,10));canvas.alpha_composite(small.resize((48,72),Image.Resampling.NEAREST),(40,55));plate.paste(canvas.convert('RGB'),(xx,70+jj*190));d.text((xx,235+jj*190),'SOURCE' if jj==0 else 'REGISTERED',font=font,fill='#e3cf43')
    d.text((xx,490),ident.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Native primary K=#155352; background k=#0f3b3a. Restrained interior shading; no new colour role.',
    'Wire repeat removed; source-layout contours and all coverage remain unchanged. Source and artwork compared at intended sizes.',
    'Authoring only. No runtime renderer, native selection, scavenge, burning or visibility test was performed.']):d.text((18,550+i*30),line,font=font,fill='#e5e8d8')
plate.save(OUT/'game-scale-source-comparison.png');print('Corrected wire banding and excessive darkening; all source geometry/coverage and K/k palette retained.')
