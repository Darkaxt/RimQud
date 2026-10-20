"""Register separate fixed mutation art with unchanged, padded reusable body layers."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.ndimage import distance_transform_edt
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
SIZE=(512,1264);PAD=240;FACES=['south','east','north','west']
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def rgba(p):return Image.open(p).convert('RGBA')
packet=json.loads((HERE/'source-packet.json').read_text());base=json.loads((ROOT/packet['baseline']['path']).read_text());assert not (OUT/'model.json').exists()
raw=np.array(rgba(HERE/'composed-refinement-raw.png'));gray=raw[:,:,:3].mean(2);valid=(raw[:,:,3]>250)&(gray>180)&(gray<253);low,high=np.percentile(gray[valid],[15,75])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
views={};neutral={};native={};palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];rgb=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
def tint(im,code,weight=None,detail=None):
    a=np.array(im);lum=a[:,:,:3].astype(float).mean(2);w=np.array(weight).astype(float)/255 if weight else np.zeros(lum.shape)
    color=(1-w[:,:,None])*rgb(code)+w[:,:,None]*rgb(detail or code)
    a[:,:,:3]=np.uint8(np.round(lum[:,:,None]*color/255));a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
for f in FACES:
    source='east' if f=='west' else f;mirror=f=='west';rows=[]
    def save(im,name,component,depth,original=None,**extra):
        if mirror:im=ImageOps.mirror(im)
        p=OUT/f'{name}-{f}.png';im.save(p)
        row=dict(component=component,file=p.name,public_file=p.relative_to(ROOT).as_posix(),sha256=ref(p)['sha256'],size=list(SIZE),contact=packet['frame']['contact'],color_role='foreground',
                 width=packet['frame']['width'],height=packet['frame']['height'],center_x=0,center_z=packet['frame']['center_z'],layer=depth,**extra)
        if original:row['original_component']=original;row['padding_top']=PAD
        rows.append(row);return row
    for r in base['views'][source]:
        old=ROOT/r['public_file'];assert ref(old)['sha256']==r['sha256'];im=Image.new('RGBA',SIZE);im.alpha_composite(rgba(old),(0,PAD));save(im,r['component'],r['component'],r['layer'],dict(path=r['public_file'],sha256=r['sha256']))
    for part in ['raised-arms','tail']:
        p=HERE/('patched-tail-east.png' if part=='tail' and source=='east' else f'{part}-{source}.png')
        a=np.array(rgba(p));alpha=a[:,:,3];ink=a[:,:,:3].mean(2)<100;dist=distance_transform_edt(alpha>128);field=low+(high-low)*np.clip(dist/24,0,1);out=a.copy();out[:,:,:3]=np.uint8(np.round(field))[:,:,None];out[ink,:3]=a[ink,:3];out[alpha==0,:3]=0
        save(Image.fromarray(out),part,'mutation-'+part,(-.002 if part=='raised-arms' else (.0005 if f=='north' else -.003)),anatomy_role=('Two extra raised arms; exact logical hand-pose mapping pending individual assembly' if part=='raised-arms' else 'One posterior Tail214; not a reusable human race feature'))
    face=rgba(HERE/f'patched-refined-hands-face-{source}.png')
    weight=Image.new('L',SIZE);d=ImageDraw.Draw(weight)
    # Only the white eye interiors belong to the actor's source detail role.
    if source=='south':
        d.ellipse((212,165,232,179),fill=255);d.ellipse((280,164,300,178),fill=255)
    elif source=='east':d.ellipse((313,153,326,165),fill=255)
    a=np.array(face);w=np.minimum(np.array(weight),a[:,:,3]);weight=Image.fromarray(w)
    if mirror:weight=ImageOps.mirror(weight)
    weight_path=OUT/f'hands-face-detail-weight-{f}.png';weight.save(weight_path)
    face_row=save(face,'hands-face','mutation-hands-face',.0012,native_part=211,parent_part=210,detail_weight=ref(weight_path),detail_color_role='detail',anatomy_role='Joined/interlaced hands forming mouthless face; not an added Head node')
    views[f]=sorted(rows,key=lambda r:r['layer'])
    n=Image.new('RGBA',SIZE);c=Image.new('RGBA',SIZE)
    for r in views[f]:
        im=rgba(ROOT/r['public_file']);n.alpha_composite(im)
        weight=Image.open(ROOT/r['detail_weight']['path']) if r.get('detail_weight') else None
        c.alpha_composite(tint(im,'r',weight,'w'))
    n.save(OUT/f'neutral-{f}.png');c.save(OUT/f'native-{f}.png');neutral[f]=n;native[f]=c
model=dict(entry='BODY-IRUDAD',kind='fixed_named_anatomy_with_separate_mutation_art',source=ref(HERE/'source-packet.json'),baseline_model=packet['baseline'],views=views,registration=packet['frame'],
    anatomy_contract=packet['anatomy'],color_contract='Neutral grayscale, actor r primary and w eye detail from original Qud mask. Single component alpha coverage with independent detail weight. Natural Stinger default-item w/B metadata retained in source, not inferred as a separate visible equipment recolor.',
    separation='Padded baseline body/head remain exact original pixel arrays; raised arms, hands-face and posterior tail are independent textures. No mutation baked into the reusable older-human base. No render bones or general framework added.',
    native_activation=False,native_acceptance=packet['native_acceptance'])
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(body_pixels='Original current body/head pixels at integer y+240 only; no resampling or silhouette change.',frame=packet['frame'],
    refinement_decision='Both actual AI outputs retain anatomy but redraw body/head/feet. Reject those body pixels. First output supplies readable interlaced-finger art; composed refinement supplies measured clean skin luminance range for stable geometric continuation. Rejected striped UV transfer retained. No second isolation.',
    composed_refinement_skin_luminance_levels=[float(low),float(high)],native_part_binding='All actual IDs/parents/managers retained; mechanical part slots are not articulated render bones. Raised neutral pose versus occupied Hand201/6 remains NPC-ELDERBOB authoring work.',native_activation=False))
for label,group in [('neutral',neutral),('native',native)]:
    sheet=Image.new('RGB',(1152,800),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'IRUDAD / '+label+' / separate mutation pieces; exact reusable older-human baseline',font=font,fill='#e3cf43')
    for i,f in enumerate(FACES):
        im=group[f].resize((256,632),Image.Resampling.LANCZOS);x=16+i*284;sheet.paste(im,(x,50),im);d.line((x+128,50,x+128,682),fill='#a39846');d.line((x,645,x+256,645),fill='#75aaa0');d.text((x,710),f.upper(),font=font,fill='#e3cf43')
    d.text((18,755),'Fixed physical scale and ground; no equipment, cosmetics or native anatomy acceptance.',font=font,fill='#e5e8d8');sheet.save(OUT/f'{label}-comparison.png')
sheet=Image.new('RGB',(800,650),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'IRUDAD / 48x119 whole frame; original body retains same pixel/world scale',font=font,fill='#e3cf43')
for j,group in enumerate([neutral,native]):
    y=60+j*270
    for i,f in enumerate(FACES):
        im=group[f].resize((48,119),Image.Resampling.LANCZOS);sheet.paste(im,(i*200+20,y),im);large=im.resize((72,178),Image.Resampling.NEAREST);sheet.paste(large,(i*200+95,y),large);d.text((i*200+20,y+200),f.upper(),font=font,fill='#e3cf43')
d.text((18,620),'Neutral then source r/w. Authoring only; captured outfit remains unfinished.',font=font,fill='#e5e8d8');sheet.save(OUT/'game-scale-comparison.png')
print('Registered separate mutation textures and padded unchanged base; all four neutral/native views ready for authoring inspection.')
