"""Register selected front-guided turnarounds and explicit refined-image masks."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import re
import shutil
from PIL import Image,ImageDraw,ImageChops,ImageFilter
import resvg_py

REPO=Path(__file__).resolve().parents[1];BODIES=REPO/'art/village/bodies'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())

LANDMARKS={
 'human-male':dict(contacts=[[278.5,879],[262.5,879],[233,879]],neck=[420,420,420],heads=[[150,150,410,424],[140,150,390,424],[100,150,365,424]],hands=[[[143,663],[415,663]],[[259,663]],[[98,663],[370,663]]]),
 'human-female':dict(contacts=[[277,900],[261.5,903],[233,901]],neck=[390,390,390],heads=[[150,120,410,395],[135,120,395,395],[100,120,365,395]],hands=[[[139,640],[415,640]],[[258,640]],[[94,640],[370,640]]]),
 'irudad':dict(contacts=[[288,936],[271,936],[223,936]],neck=[420,420,420],heads=[[195,235,385,422],[200,230,386,424],[130,235,315,422]],hands=[[[148,664],[428,664]],[[269,664]],[[78,664],[362,664]]]),
 'nima':dict(contacts=[[263.5,957],[250,957],[237.5,957]],neck=[288,288,288],heads=[[175,65,350,291],[175,65,390,291],[130,65,330,291]],hands=[[[77,566],[446,566],[126,595],[400,595]],[[278,565],[357,565]],[[63,566],[423,566],[100,595],[385,595]]]),
 'yrame':dict(contacts=[[275,923],[270,923],[230,923]],neck=[410,410,410],heads=[[140,130,410,415],[180,130,450,415],[100,130,365,415]],hands=[[[120,661],[425,661]],[[340,667]],[[95,661],[375,661]]])}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True);args=ap.parse_args()
    all_models={}
    for family,lm in LANDMARKS.items():
        folder=BODIES/family;views={};raw=Image.open(folder/('turnaround-rejected-three-feet.png' if family=='yrame' else 'turnaround.png')).convert('RGBA')
        for index,direction in enumerate(['south','east','north']):
            x=index*512;w=512
            if family=='nima':x=[0,535,1024][index];w=[535,489,512][index]
            if family=='yrame':
                f=folder/f'four-feet-{direction}.svg';s=f.read_text(encoding='utf-8')
                # Keep complete hands at the waist cut; four feet are authored
                # geometry, not a claim that the rejected three-foot image passed.
                circles=lm['hands'][index]
                holes=''.join(f'<ellipse cx="{hx}" cy="{hy}" rx="47" ry="47"/>' for hx,hy in circles)
                s=re.sub(r'<clipPath id="upper">.*?</clipPath>',
                    '<clipPath id="upper"><rect width="512" height="650"/>'+holes+'</clipPath>',s,count=1)
                if direction=='north':s=s.replace('<g stroke=', '<g transform="translate(-45 0)" stroke=')
                f.write_bytes(s.encode());p=folder/f'four-feet-{direction}.png';p.write_bytes(resvg_py.svg_to_bytes(svg_path=str(f),resources_dir=str(folder.resolve()),skip_system_fonts=True));image=Image.open(p).convert('RGBA')
            else:image=raw.crop((x,0,x+w,1024))
            a=image.getchannel('A').point(lambda v:0 if v<8 else v);image.putalpha(a)
            head=Image.new('L',image.size);ImageDraw.Draw(head).rectangle(lm['heads'][index],fill=255)
            body=ImageChops.invert(head).filter(ImageFilter.MaxFilter(5));layers=[]
            for component,mask in [('body',body),('head',head)]:
                part=image.copy();part.putalpha(ImageChops.multiply(a,mask));p=folder/f'{component}-{direction}.png';part.save(p)
                scale=.00165;cx,cy=lm['contacts'][index];filename=f'village-{family}-{component}-{direction}.png';shutil.copy2(p,args.root/'donor'/filename)
                layers.append(dict(component=component,file=filename,sha256=sha(p),size=list(image.size),contact=[cx,cy],
                    color_role='foreground',width=w*scale/(2/3),height=1024*scale,center_x=(w/2-cx)*scale/(2/3),center_z=(cy-512)*scale,
                    layer=.001 if component=='head' else 0))
            views[direction]=layers
        model=dict(family=family,views=views,registration=lm,pixel_world_scale=.00165,canvas=[512,1024],
            geometry='Arms, hands, feet, tail and hands-face remain part of the body image. Head mask re-established on selected output. Two-pixel body underlap.',
            authoring='Front-guided ImageGen output with explicit masks' if family!='yrame' else 'Selected upper sprite plus deterministic four-foot geometry; rejected three-foot proposals retained',
            source_sha256={p.name:sha(p) for p in folder.glob('*.png') if p.name in ['front.png','turnaround.png','turnaround-rejected-three-feet.png']},
            state='Registered; apparel and native batch acceptance pending')
        write(folder/'model.json',model);all_models[family]=model
    # Fish uses explicit unequal source panels (the proposal did not honor equal
    # columns), registered by its anatomical body center rather than feet.
    folder=BODIES/'glowfish';raw=Image.open(folder/'turnaround.png').convert('RGBA');views={}
    for d,rect,center,scale in [('south',[0,0,400,1024],[210,500],.00135),('east',[400,0,1150,1024],[380,535],.00112),('north',[1150,0,1536,1024],[195,545],.00135)]:
        image=raw.crop(rect);p=folder/f'body-{d}.png';image.save(p);w,h=image.size;cx,cy=center;filename=f'village-glowfish-body-{d}.png';shutil.copy2(p,args.root/'donor'/filename)
        views[d]=[dict(component='body',file=filename,sha256=sha(p),size=[w,h],contact=center,color_role='fixed',
            width=w*scale/(2/3),height=h*scale,center_x=(w/2-cx)*scale/(2/3),center_z=(cy-h/2)*scale,layer=0)]
    model=dict(family='glowfish',views=views,source_sha256=sha(folder/'turnaround.png'),registration='Anatomical center and snout/tail length, not independently fitted silhouette boxes',
        palette='Authored native magenta/cyan; changed native palette retains original art',state='Registered; native fish batch acceptance pending')
    write(folder/'model.json',model);all_models['glowfish']=model
    write(REPO/'art/village/body-models.json',all_models)
    print('Registered six body families; primary/head masks and explicit contact transforms prepared.')
if __name__=='__main__':main()
