"""Register separate Nima anatomy and exact source body pixels; no native activation."""
from pathlib import Path
import json,hashlib,sys
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from tail_geometry_four_views import render_tail
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';SIZE=(512,1264)
def read(p):return json.loads(p.read_text())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (OUT/'model.json').exists();OUT.mkdir(exist_ok=True)
packet=read(HERE/'source-packet.json');body=read(ROOT/packet['baseline']['path']);frame=packet['frame'];geometry=read(HERE/'tail-construction-v2.json');review=read(HERE/'composed-structural-review.json')
assert review['status']=='USABLE COMPOSED SURFACE REFERENCE; BODY PIXELS REJECTED'
raw=np.array(Image.open(HERE/'composed-refinement-raw.png').convert('RGBA'));gray=raw[:,:,:3].mean(2);yy,xx=np.indices(gray.shape)
tail=(raw[:,:,3]>245)&(yy<400)&(gray>100)&(gray<235);skin=(raw[:,:,3]>245)&(yy>400)&(yy<810)&(gray>185)&(gray<253)
tl,th=np.percentile(gray[tail],[20,80]);sl,sh=np.percentile(gray[skin],[15,75])
render_tail(OUT,geometry,frame,float(tl),float(th))
views={};neutral={};native={};palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];rgb=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
def tint(im,c):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].astype(float).mean(2)[:,:,None]*rgb(c)/255));a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
for f in ['south','east','north','west']:
    source='east' if f=='west' else f;mirror=f=='west';rows=[]
    def add(p,component,depth,role='foreground',**extra):
        rows.append(dict(component=component,file=p.name,public_file=p.relative_to(ROOT).as_posix(),sha256=ref(p)['sha256'],size=list(SIZE),contact=frame['contact'],color_role=role,
            width=frame['width'],height=frame['height'],center_x=0,center_z=frame['center_z'],layer=depth,**extra))
    for r in body['views'][source]:
        p=ROOT/r['public_file'];assert ref(p)['sha256']==r['sha256'];im=Image.open(p).convert('RGBA');im=ImageOps.mirror(im) if mirror else im
        padded=Image.new('RGBA',SIZE);padded.paste(im,(0,240));out=OUT/f'{r["component"]}-{f}.png';padded.save(out)
        add(out,r['component'],r['layer'],original_component=dict(path=r['public_file'],sha256=r['sha256']),padding_top=240,mirrored_from_east=mirror)
    p=HERE/('patched-extra-arms-east.png' if source=='east' else f'extra-arms-{source}.png');a=np.array(Image.open(p).convert('RGBA'));alpha=a[:,:,3];ink=a[:,:,:3].mean(2)<100
    shade=sl+(sh-sl)*np.clip(distance_transform_edt(alpha>128)/23,0,1);out=a.copy();out[:,:,:3]=np.uint8(np.round(shade))[:,:,None];out[ink,:3]=a[ink,:3];out[alpha==0,:3]=0
    im=Image.fromarray(out);im=ImageOps.mirror(im) if mirror else im;p=OUT/f'extra-arms-{f}.png';im.save(p)
    add(p,'mutation-extra-arms',-.002,native_parts=[184,185,186,187],anatomy_role='Exactly one additional arm/hand pair; far limb occluded in complete profile',mirrored_from_east=mirror)
    for layer in ['back','front']:
        p=OUT/f'tail-{layer}-{f}.png';depth=-.004 if layer=='back' else (-.003 if f in ['east','west'] else .0012)
        add(p,'mutation-tail-'+layer,depth,'detail',native_part=193,parent_part=176,manager='506::Stinger',render_instance='one-tail-193',
            anatomy_role='One continuous spiral tail, one terminal stinger/bead; split only for draw order',projection='Explicit canonical world-space '+f+' view',mirrored_from_east=False)
    views[f]=sorted(rows,key=lambda r:r['layer']);n=Image.new('RGBA',SIZE);c=Image.new('RGBA',SIZE)
    for r in views[f]:
        im=Image.open(ROOT/r['public_file']).convert('RGBA');n.alpha_composite(im);c.alpha_composite(tint(im,'w' if r['color_role']=='detail' else 'g'))
    n.save(OUT/f'neutral-{f}.png');c.save(OUT/f'native-{f}.png');neutral[f]=n;native[f]=c
model=dict(entry='BODY-NIMA',kind='fixed_named_anatomy_with_separate_mutation_art',source=ref(HERE/'source-packet.json'),baseline_model=packet['baseline'],tail_geometry=ref(HERE/'tail-construction-v2.json'),
    palette_roles=ref(HERE/'source-palette-roles.json'),views=views,registration=frame,
    separation='Exact original body/head RGBA at integer y+240; one extra arm pair and one Tail193 are separate textures. Tail back/front are draw-order pieces of one appendage, not two tails. No generic mutation framework or render bones.',
    source_anatomy=packet['anatomy'],west_policy='Ordinary symmetric body/arm profile mirrors east; the asymmetric diagonal spiral tail uses explicit west world projection/depth, not an east bitmap mirror.',
    profile_depth='Both profile views place the posterior/midline tail behind the near arm/body volume. North preserves its posterior surface above the back; same geometry, no cuts in full tail.',
    native_activation=False,native_acceptance=packet['native_acceptance'])
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(frame=frame,tail_luminance=[float(tl),float(th)],skin_luminance=[float(sl),float(sh)],
    refinement='Both actual outputs retained as proposals. Duplicate stinger from first was corrected by second, but both redraw baseline. Only usable neutral surface values retained in deterministic geometry; original source body/head and one-tail topology restored. No AI isolation or third prompt loop.',
    tail_style='Quiet shaded facets and segment joints; invented diamond icons removed. Source g/w palette roles are separate metadata, not baked RGB.',
    body_pixels='Exact source RGBA paste including transparent RGB, no resampling.',native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for label,group in [('neutral',neutral),('native',native)]:
    sheet=Image.new('RGB',(1152,800),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'NIMA / '+label+' / separate extra arm pair and one spiral tail; original female base',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(group.items()):
        x=16+i*284;im=im.resize((256,632),Image.Resampling.LANCZOS);sheet.paste(im,(x,50),im);d.line((x+128,50,x+128,682),fill='#a39846');d.line((x,645,x+256,645),fill='#75aaa0');d.text((x,710),f.upper(),font=font,fill='#e3cf43')
    d.text((18,755),'Body contact/scale unchanged. Tail g/w appearance is source-interpreted; native acceptance pending.',font=font,fill='#e5e8d8');sheet.save(OUT/f'{label}-comparison.png')
sheet=Image.new('RGB',(800,650),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'NIMA / 48x119 whole frame; neutral then source appearance roles',font=font,fill='#e3cf43')
for j,group in enumerate([neutral,native]):
    y=60+j*270
    for i,(f,im) in enumerate(group.items()):
        small=im.resize((48,119),Image.Resampling.LANCZOS);sheet.paste(small,(20+i*200,y),small);large=small.resize((72,178),Image.Resampling.NEAREST);sheet.paste(large,(95+i*200,y),large);d.text((20+i*200,y+200),f.upper(),font=font,fill='#e3cf43')
d.text((18,620),'No clothes or cosmetics. Full outfit and native anatomy/state acceptance remain unfinished.',font=font,fill='#e5e8d8');sheet.save(OUT/'game-scale-comparison.png')
print('Registered all4cardinal views, separate source-role masks/components and exact unchanged body pixels; visual review pending.')
