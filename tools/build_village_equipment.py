"""Fit actual captured items to registered bodies as separate editable layers.

One item is constructed at a time from its own native reference/description.
Opening contours stay open; hands and heads are never copied into garment art.
No profession costumes, inventory-only decoration or new limb animation nodes.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import resvg_py
from PIL import Image

REPO=Path(__file__).resolve().parents[1];OUT=REPO/'art/village/equipment'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def slug(s):return re.sub('[^a-z0-9]+','-',s.lower()).strip('-')
def path(d,fill='#d6ddce',width=7):return f'<path d="{d}" fill="{fill}" stroke="#26382e" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
def svg(s,w=512,h=1024):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">{s}</svg>\n'

def garment(name,d,cx,ny,foot,hands):
    side=d=='east';back=d=='north';hy=hands[0][1];hem=foot-(65 if 'Robe' in name else 160)
    if name=='Leather Apron':
        p=path(f'M{cx-53} {ny+5} L{cx+53} {ny+5} L{cx+70} {ny+157} L{cx+102} {foot-145} Q{cx} {foot-110} {cx-102} {foot-145} L{cx-70} {ny+157}Z')
        detail=path(f'M{cx-80} {ny+166} Q{cx} {ny+182} {cx+80} {ny+166} M{cx-42} {ny+8} V{ny+70} M{cx+42} {ny+8}V{ny+70}','none',5)
        if back:p=path(f'M{cx-49} {ny+4} L{cx+51} {ny+158} M{cx+49} {ny+4} L{cx-51} {ny+158}','none',13);detail=''
        elif side:
            p=path(f'M{cx+35} {ny+7} L{cx+85} {ny+20} L{cx+75} {ny+158} L{cx+92} {foot-145} L{cx+32} {foot-130} L{cx+28} {ny+158}Z')
            p+=path(f'M{cx-55} {ny+12}Q{cx} {ny-12} {cx+46} {ny+18}','none',8)
            detail=path(f'M{cx-65} {ny+170}H{cx+75}','none',6)
        return p,detail
    if name=='Pocketed Vest':
        p=path(f'M{cx-47} {ny-3} L{cx-98} {ny+35} L{cx-70} {ny+115} L{cx-80} {foot-220} L{cx+80} {foot-220} L{cx+70} {ny+115} L{cx+98} {ny+35} L{cx+47} {ny-3} L{cx} {ny+63}Z')
        detail=''
        if back:p=path(f'M{cx-47} {ny-3} L{cx-98} {ny+35} L{cx-70} {ny+115} L{cx-80} {foot-220} L{cx+80} {foot-220} L{cx+70} {ny+115} L{cx+98} {ny+35} L{cx+47} {ny-3} Q{cx} {ny+15} {cx-47} {ny-3}Z')
        elif side:p=path(f'M{cx-36} {ny+12} Q{cx-75} {ny+25} {cx-70} {ny+75} L{cx-55} {foot-220} L{cx+55} {foot-220} L{cx+72} {ny+65} L{cx+24} {ny+12} L{cx+6} {ny+72}Z')
        if not back:
            for x in ([cx+26] if side else [cx-55,cx+25]):
                for y in [ny+112,ny+176]:detail+=path(f'M{x-15} {y}H{x+20}V{y+35}Q{x} {y+45} {x-15} {y+35}Z','#aebcb0',4)
        return p,detail
    if side:
        hx=hands[0][0];p=path(f'M{cx-45} {ny+2} Q{cx-104} {ny+8} {cx-110} {ny+80} L{cx-80} {hem} Q{cx} {hem+24} {cx+85} {hem} L{cx+65} {hy-90} L{hx+33} {hy-28} L{hx-30} {hy-32} L{cx-4} {ny+134} L{cx-30} {ny+90} L{cx+45} {ny+12} Q{cx} {ny+42} {cx-45} {ny+2}Z')
    else:
        left=min(hands[:2],key=lambda h:h[0]);right=max(hands[:2],key=lambda h:h[0]);lx,ly=left;rx,ry=right
        p=path(f'M{cx-48} {ny} Q{cx} {ny+26} {cx+48} {ny} L{cx+108} {ny+29} L{rx+25} {ry-48} L{rx-25} {ry-29} L{cx+69} {ny+139} L{cx+88} {hem} Q{cx} {hem+25} {cx-88} {hem} L{cx-69} {ny+139} L{lx+25} {ly-29} L{lx-25} {ly-48} L{cx-108} {ny+29}Z')
    detail=path(f'M{cx-51} {ny+74} L{cx-61} {hem-12} M{cx+40} {ny+72} L{cx+59} {hem-11}','none',4)
    if name=='Woven Tunic':detail+=path(f'M{cx-76} {ny+193} Q{cx} {ny+217} {cx+77} {ny+193} M{cx+5} {ny+207} L{cx+23} {ny+257}','none',9)
    if name=='Chain Mail':
        detail=''
        for y in range(int(ny+70),int(hem-15),26):
            for x in range(int(cx-54),int(cx+55),24):detail+=f'<ellipse cx="{x}" cy="{y}" rx="10" ry="7" fill="none" stroke="#a4b2a4" stroke-width="4"/>'
    return p,detail

def item_shape(name,slot,d,cx,ny,foot,hands,laterality,head_top):
    if slot=='Body':return garment(name,d,cx,ny,foot,hands)
    if slot=='Head':
        top=head_top-33
        if name=='Horns':
            a=path(f'M{cx-67} {top+90} Q{cx-156} {top+29} {cx-145} {top-93} Q{cx-100} {top-19} {cx-36} {top+35}Z')
            a+=path(f'M{cx+67} {top+90} Q{cx+156} {top+29} {cx+145} {top-93} Q{cx+100} {top-19} {cx+36} {top+35}Z')
            return a,path(f'M{cx-81} {top+33}L{cx-116} {top+5} M{cx+81} {top+33}L{cx+116} {top+5}','none',5)
        return path(f'M{cx-125} {top+103} Q{cx} {top+51} {cx+125} {top+103} L{cx+125} {top+123} Q{cx} {top+154} {cx-125} {top+123}Z')+path(f'M{cx-72} {top+100} L{cx-60} {top+24} Q{cx} {top-4} {cx+60} {top+24} L{cx+72} {top+100}Z'),path(f'M{cx-72} {top+87}Q{cx} {top+110} {cx+72} {top+87}','none',10)
    if slot=='Face':
        if d=='north':return '',''
        y=ny-110
        if name=='Spectacles':return f'<g fill="none" stroke="#d9e3d6" stroke-width="6"><ellipse cx="{cx-31}" cy="{y}" rx="24" ry="20"/><ellipse cx="{cx+31}" cy="{y}" rx="24" ry="20"/><path d="M{cx-7} {y}H{cx+7}"/></g>',''
        return f'<circle cx="{cx+30}" cy="{y}" r="25" fill="none" stroke="#e1e8d9" stroke-width="9"/>',path(f'M{cx+45} {y+18}L{cx+56} {y+69}','none',5)
    if slot=='Feet':
        a='';b=''
        xs=[cx-46,cx+46] if d!='east' else [cx-16,cx+23]
        for x in xs:
            a+=path(f'M{x-26} {foot-42}H{x+22}L{x+30} {foot-5}Q{x} {foot+4} {x-29} {foot-5}Z')
            b+=path(f'M{x-22} {foot-25}L{x+24} {foot-12}','none',6)
        return a,b
    if slot=='Floating Nearby':return f'<circle cx="{cx+180}" cy="{ny+20}" r="29" fill="#eff5e8" stroke="#293f34" stroke-width="6"/>',f'<circle cx="{cx+171}" cy="{ny+12}" r="9" fill="#ffffff"/>'
    # Native right hand is viewer-left in front, viewer-right in back. Read each
    # actual laterality; two held items do not share an invented universal grip.
    if d=='east':gx,gy=hands[0]
    elif laterality in [1,5,9]:gx,gy=max(hands[:2],key=lambda h:h[0]) if d=='south' else min(hands[:2],key=lambda h:h[0])
    else:gx,gy=min(hands[:2],key=lambda h:h[0]) if d=='south' else max(hands[:2],key=lambda h:h[0])
    if name in ['Walking Stick','Shillelagh']:return path(f'M{gx-6} {foot-15} L{gx-6} {gy-185} Q{gx-37} {gy-227} {gx-10} {gy-239} Q{gx+20} {gy-251} {gx+20} {gy-220} L{gx+7} {gy-183} L{gx+7} {foot-15}Z'),' '
    if name=='Iron Vinereaper':return path(f'M{gx-6} {gy+120} L{gx-6} {gy-55} Q{gx-42} {gy-92} {gx-45} {gy-131} Q{gx+60} {gy-87} {gx+31} {gy-34} L{gx+7} {gy-43} L{gx+7} {gy+120}Z'),path(f'M{gx-43} {gy-129} Q{gx+19} {gy-96} {gx+28} {gy-44}','none',5)
    if name=='Wrench':return path(f'M{gx-6} {gy+95} L{gx-8} {gy-98} L{gx-34} {gy-121} L{gx-31} {gy-163} L{gx-14} {gy-142} H{gx+13} L{gx+31} {gy-163} L{gx+33} {gy-121} L{gx+8} {gy-98} L{gx+7} {gy+95}Z'),''
    if name=='Pestle':return path(f'M{gx-11} {gy+65} Q{gx-23} {gy+69} {gx-25} {gy+49} L{gx-13} {gy-115} Q{gx-43} {gy-149} {gx} {gy-174} Q{gx+43} {gy-149} {gx+13} {gy-115} L{gx+18} {gy+49}Z'),''
    return path(f'M{gx-7} {gy+55} L{gx-7} {gy-12} L{gx-17} {gy-34} L{gx-11} {gy-146} L{gx} {gy-193} L{gx+11} {gy-146} L{gx+17} {gy-34} L{gx+7} {gy-12} L{gx+7} {gy+55}Z'),path(f'M{gx} {gy-163}V{gy-38}','none',4)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True);args=ap.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    sources=json.loads((REPO/'art/village/sources.json').read_text(encoding='utf-8'));models=json.loads((REPO/'art/village/body-models.json').read_text(encoding='utf-8'));results={}
    for family in ['human-male','human-female','irudad','nima','yrame']:
        actors=[a for a in sources['actors'] if (a['creature']=='ElderBob' if family=='irudad' else a['creature']=='Nima Ruda' if family=='nima' else a['creature']=='Warden Yrame' if family=='yrame' else a['race']=='human' and a['creature'] not in ['ElderBob','Nima Ruda','Warden Yrame'])]
        items={}
        for actor in actors:
            for instance in actor['native_instances']:
                for part in instance['parts']:
                    if part.get('equipped'):items[(part['equipped']['blueprint'],part['type'],part['laterality'])]=part['equipped']
        model=models[family];results[family]={}
        for (name,slot,laterality),native in items.items():
            family_key=slug(name)+'@'+slot+'@'+str(laterality);views={}
            for i,d in enumerate(['south','east','north']):
                base=model['views'][d][0];cx,cy=base['contact'];ny=model['registration']['neck'][i];hands=model['registration']['hands'][i]
                head=Image.open(REPO/f'art/village/bodies/{family}/head-{d}.png');head_top=head.getchannel('A').point(lambda a:255 if a>=192 else 0).getbbox()[1]
                primary,detail=item_shape(name,slot,d,cx,ny,cy,hands,laterality,head_top);layers=[]
                for component,s in [('item',primary),('item-detail',detail.strip())]:
                    if not s:continue
                    if component=='item-detail' and slot=='Body':s=f'<defs><clipPath id="garment">{primary}</clipPath></defs><g clip-path="url(#garment)">{s}</g>'
                    p=OUT/f'{family}-{slug(name)}-{slot.lower()}-{laterality}-{component}-{d}.svg';p.write_bytes(svg(s,base['size'][0],1024).encode());png=p.with_suffix('.png');png.write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
                    file='village-'+png.name;shutil.copy2(png,args.root/'donor'/file)
                    layers.append({**base,'component':component,'file':file,'sha256':sha(png),'color_role':'equipment-detail' if component=='item-detail' else 'equipment',
                        'equipment_key':family_key,'layer':.0023 if slot in ['Head','Face'] else -.0002 if d=='north' and slot=='Hand' else .0018 if slot in ['Hand','Floating Nearby'] else .0008 if component=='item-detail' else .0007})
                views[d]=layers
            results[family][family_key]=dict(blueprint=name,slot=slot,laterality=laterality,native=native,views=views,
                authoring='One source-bound item, constructed as editable separate primary/detail geometry; open cuffs do not contain body pixels')
    write(REPO/'art/village/equipment-models.json',results);print('Prepared separately fitted native equipped-item layers for five adult body families.')
if __name__=='__main__':main()
