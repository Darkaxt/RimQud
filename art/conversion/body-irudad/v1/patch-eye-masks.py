"""Follow the actual refined eye interiors instead of estimated ellipse coordinates."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from scipy.ndimage import label
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
assert not (HERE/'eye-mask-correction.json').exists()
shutil.copyfile(OUT/'native-comparison.png',HERE/'eye-mask-misalignment.png')
model=json.loads((OUT/'model.json').read_text());palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];rgb=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
seeds={'south':[(218,166),(285,166)],'east':[(318,157)],'north':[]};counts={}
for f in ['south','east','north']:
    a=np.array(Image.open(OUT/f'hands-face-{f}.png').convert('RGBA'));gray=a[:,:,:3].mean(2)
    lab,n=label((gray>180)&(a[:,:,3]>128));weight=np.zeros(a.shape[:2],dtype=np.uint8);counts[f]=[]
    for x,y in seeds[f]:
        component=int(lab[y,x]);assert component>0
        selected=lab==component;count=int(selected.sum());assert 40<count<500,(f,count)
        weight[selected]=np.uint8(np.round(np.clip((gray[selected]-180)/65,0,1)*255));counts[f].append(count)
    Image.fromarray(weight).save(OUT/f'hands-face-detail-weight-{f}.png')
ImageOps.mirror(Image.open(OUT/'hands-face-detail-weight-east.png')).save(OUT/'hands-face-detail-weight-west.png')
native={};neutral={};font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for f,rows in model['views'].items():
    canvas=Image.new('RGBA',(512,1264))
    for r in rows:
        im=Image.open(ROOT/r['public_file']).convert('RGBA');a=np.array(im);lum=a[:,:,:3].astype(float).mean(2);w=np.zeros(lum.shape)
        if r.get('detail_weight'):
            p=ROOT/r['detail_weight']['path'];r['detail_weight']=ref(p);w=np.array(Image.open(p)).astype(float)/255
        color=(1-w[:,:,None])*rgb('r')+w[:,:,None]*rgb('w');a[:,:,:3]=np.uint8(np.round(lum[:,:,None]*color/255));a[a[:,:,3]==0,:3]=0;canvas.alpha_composite(Image.fromarray(a))
    canvas.save(OUT/f'native-{f}.png');native[f]=canvas;neutral[f]=Image.open(OUT/f'neutral-{f}.png').convert('RGBA')
(OUT/'model.json').write_bytes((json.dumps(model,indent=2)+'\n').encode())
sheet=Image.new('RGB',(1152,800),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'IRUDAD / native / separate mutation pieces; exact reusable older-human baseline',font=font,fill='#e3cf43')
for i,(f,im) in enumerate(native.items()):
    small=im.resize((256,632),Image.Resampling.LANCZOS);x=16+i*284;sheet.paste(small,(x,50),small);d.line((x+128,50,x+128,682),fill='#a39846');d.line((x,645,x+256,645),fill='#75aaa0');d.text((x,710),f.upper(),font=font,fill='#e3cf43')
d.text((18,755),'Fixed physical scale and ground; no equipment, cosmetics or native anatomy acceptance.',font=font,fill='#e5e8d8');sheet.save(OUT/'native-comparison.png')
sheet=Image.new('RGB',(800,650),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'IRUDAD / 48x119 whole frame; original body retains same pixel/world scale',font=font,fill='#e3cf43')
for j,group in enumerate([neutral,native]):
    y=60+j*270
    for i,(f,im) in enumerate(group.items()):
        small=im.resize((48,119),Image.Resampling.LANCZOS);sheet.paste(small,(i*200+20,y),small);large=small.resize((72,178),Image.Resampling.NEAREST);sheet.paste(large,(i*200+95,y),large);d.text((i*200+20,y+200),f.upper(),font=font,fill='#e3cf43')
d.text((18,620),'Neutral then source r/w. Authoring only; captured outfit remains unfinished.',font=font,fill='#e5e8d8');sheet.save(OUT/'game-scale-comparison.png')
(HERE/'eye-mask-correction.json').write_bytes((json.dumps(dict(rejected='eye-mask-misalignment.png',reason='Estimated eye ellipses were shifted relative to the transferred refined white eye interiors; they exposed only a partial detail area.',correction='Select each actual enclosed light interior using explicit reviewed seed points, following its refined dark eye rim. No north eyes, west mirrors the corrected east mask.',seeds=seeds,interior_pixel_counts=counts,unchanged='All neutral art, body/head pixels, anatomy geometry and primary alpha; only detail-weight mask and native authoring previews corrected.',native_activation=False),indent=2)+'\n').encode())
print('Corrected actual enclosed eye detail masks; native palettes rerendered without any neutral/body change.')
