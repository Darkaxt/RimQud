"""Leave a clear gap between added and original feet without altering the base."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageDraw,ImageFont
import numpy as np
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'foot-clearance-correction.json').exists()
shutil.copyfile(OUT/'neutral-comparison.png',HERE/'registration-before-foot-clearance.png')
model=json.loads((OUT/'model.json').read_text());shift=12
for f in ['south','north']:
    p=OUT/f'extra-legs-{f}.png';shutil.copyfile(p,HERE/f'registration-initial-extra-legs-{f}.png');im=Image.open(p).convert('RGBA');out=Image.new('RGBA',im.size)
    out.paste(im.crop((0,0,256,1024)),(-shift,0));out.paste(im.crop((256,0,512,1024)),(256+shift,0));out.save(p)
    p=OUT/f'extra-legs-{f}.svg';s=p.read_text();end=s.index('</defs>');inner=s[end+7:s.rindex('</svg>')]
    defs=s[:end]+'<clipPath id="leftHalf"><rect x="0" y="0" width="256" height="1024"/></clipPath><clipPath id="rightHalf"><rect x="256" y="0" width="256" height="1024"/></clipPath></defs>'
    p.write_bytes((defs+f'<g transform="translate(-{shift} 0)"><g clip-path="url(#leftHalf)">'+inner+f'</g></g><g transform="translate({shift} 0)"><g clip-path="url(#rightHalf)">'+inner+'</g></g></svg>').encode())
    row=next(r for r in model['views'][f] if r['component']=='mutation-extra-legs');row['sha256']=ref(OUT/f'extra-legs-{f}.png')['sha256'];row['registration_adjustment']='Additional left/right legs translated outward12px as intact independent pieces, preserving original body and y950 contact.'
    alpha=Image.new('RGBA',im.size,'white');alpha.putalpha(out.getchannel('A'));alpha.save(OUT/f'extra-legs-alpha-{f}.png')
correction=dict(reason='Final registered south foot silhouettes merged at the left forefoot. Four separate ankles were present, but a clear toe gap improves cardinal readability.',
    transform=dict(facings=['south','north'],left_dx=-shift,right_dx=shift,dy=0,scale=1),
    unchanged='Original body/head RGBA, all limb shape curves, leg lengths, y950 contact, common horizontal pivot and accepted east/west profiles.',
    interpretation='Authored lateral spacing of additional pair only; no mechanical body slot or equipment laterality changed. Added roots remain hidden behind original pelvis.',native_activation=False)
write(HERE/'foot-clearance-correction.json',correction);model['foot_clearance']=ref(HERE/'foot-clearance-correction.json');write(OUT/'model.json',model)
groups={name:{} for name in ['neutral','native','extra-legs','extra-legs-alpha']};palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];color=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8)
for f,rows in model['views'].items():
    n=Image.new('RGBA',(512,1024));c=Image.new('RGBA',(512,1024))
    for r in rows:
        im=Image.open(ROOT/r['public_file']).convert('RGBA');n.alpha_composite(im);a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float).mean(2)[:,:,None]*color/255));a[a[:,:,3]==0,:3]=0;c.alpha_composite(Image.fromarray(a))
    n.save(OUT/f'neutral-{f}.png');c.save(OUT/f'native-{f}.png');groups['neutral'][f]=n;groups['native'][f]=c
    for name in ['extra-legs','extra-legs-alpha']:groups[name][f]=Image.open(OUT/f'{name}-{f}.png').convert('RGBA')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for name,group in groups.items():
    sheet=Image.new('RGB',(1152,680),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'YRAME / '+name+' / exact baseline + separate added pair',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(group.items()):
        xx=16+i*284;im=im.resize((256,512),Image.Resampling.LANCZOS);sheet.paste(im,(xx,55),im);d.line((xx+128,55,xx+128,567),fill='#a39846');d.line((xx,530,xx+256,530),fill='#75aaa0');d.text((xx,585),f.upper(),font=font,fill='#e3cf43')
    d.text((18,625),'FOUR feet total. Neutral base; no gear, cosmetic rime pattern or native acceptance.',font=font,fill='#e5e8d8');sheet.save(OUT/f'{name}-comparison.png')
sheet=Image.new('RGB',(800,650),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'YRAME / 48x96 frame, neutral then captured tileColor w',font=font,fill='#e3cf43')
for j,key in enumerate(['neutral','native']):
    yy=65+j*285
    for i,(f,im) in enumerate(groups[key].items()):
        small=im.resize((48,96),Image.Resampling.LANCZOS);sheet.paste(small,(20+i*200,yy),small);large=small.resize((72,144),Image.Resampling.NEAREST);sheet.paste(large,(95+i*200,yy),large);d.text((20+i*200,yy+185),f.upper(),font=font,fill='#e3cf43')
d.text((18,620),'B detail retained as source metadata; no invented permanent blue skin region.',font=font,fill='#e5e8d8');sheet.save(OUT/'game-scale-comparison.png')
print('Separated original/added toes by translating only added pair outward12px; original body and profile unchanged.')
