"""Construct one separate additional human leg pair on Yrame's fixed female base."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(512,1024)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
assert not (HERE/'constructed-turnaround.png').exists()
packet=read(HERE/'source-packet.json');base=read(ROOT/packet['baseline']['path']);assert ref(ROOT/packet['baseline']['path'])==packet['baseline']
left='M187 525 Q151 537 120 591 Q83 645 68 713 Q65 744 80 778 L76 878 Q51 900 40 921 Q38 941 59 948 Q95 953 124 940 Q132 929 125 918 L113 884 L127 777 Q136 747 127 716 L156 641 Q190 612 210 568 Z'
profile='M243 525 Q207 506 170 557 Q107 614 90 688 Q80 726 105 760 L101 866 Q78 892 65 921 Q62 939 83 947 L161 948 Q180 944 182 934 Q181 922 160 917 L137 894 L143 765 Q153 733 143 703 Q158 657 191 631 Q227 610 251 567 Z'
outline='#2d2d2d'
def path(d,fill='url(#limb)',width=7):return f'<path d="{d}" fill="{fill}" stroke="{outline}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
def save(name,parts):
    svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><defs><linearGradient id="limb" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#d0d0d0"/><stop offset=".45" stop-color="#eeeeee"/><stop offset="1" stop-color="#c4c4c4"/></linearGradient></defs>'+''.join(parts)+'</svg>'
    (HERE/(name+'.svg')).write_bytes(svg.encode());(HERE/(name+'.png')).write_bytes(svg_to_bytes(svg_string=svg))
for f in ['south','east','north']:
    if f=='east':
        # Same extra pair, with far hind leg behind near hind leg and ordinary forelegs.
        parts=['<g transform="translate(40 0)">'+path(profile,'#c9c9c9')+'</g>',path(profile),'<path d="M118 693 Q102 727 122 757 M135 919 L153 927" fill="none" stroke="#a4a4a4" stroke-width="4" stroke-linecap="round"/>']
    else:
        parts=[path(left),'<g transform="translate(512 0) scale(-1 1)">'+path(left)+'</g>']
        if f=='south':
            parts+=['<path d="M88 711 Q108 701 121 721 M391 721 Q404 701 424 711 M57 926 L73 934 M86 928 L95 939 M417 939 L426 928 M439 934 L455 926" fill="none" stroke="#a4a4a4" stroke-width="3" stroke-linecap="round"/>']
    save('extra-legs-'+f,parts)
    baseline=Image.new('RGBA',SIZE)
    for r in sorted(base['views'][f],key=lambda r:r['layer']):
        assert ref(ROOT/r['public_file'])['sha256']==r['sha256'];baseline.alpha_composite(Image.open(ROOT/r['public_file']).convert('RGBA'))
    baseline.save(HERE/f'baseline-{f}.png')
    assembled=Image.open(HERE/f'extra-legs-{f}.png').convert('RGBA');assembled.alpha_composite(baseline);assembled.save(HERE/f'constructed-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
sheet=Image.new('RGB',(1152,680),'#142823');d=ImageDraw.Draw(sheet);d.text((18,15),'YRAME / fixed human base + ONE separate additional leg pair / manual proposal',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=Image.open(HERE/f'constructed-{f}.png').convert('RGBA').resize((256,512),Image.Resampling.LANCZOS);x=60+i*370;sheet.paste(im,(x,55),im);d.text((x,590),{'south':'FRONT / SOUTH','east':'RIGHT PROFILE / EAST','north':'BACK / NORTH'}[f],font=font,fill='#e3cf43')
d.text((18,640),'Two original feet plus two added feet; natural profile occlusion. No horns, gear or particle effects.',font=font,fill='#e5e8d8');sheet.save(HERE/'constructed-turnaround.png')
write(HERE/'leg-construction.json',dict(source_part_groups=[297,298],parent_body=287,baseline_group=dict(part=297,laterality=16,manager='515::MultipleLegs::Change',equipped_boots=580),added_group=dict(part=298,laterality=64,manager='515::MultipleLegs::Add',equipped=None),
    interpretation='Four human legs/feet total. Original two baseline legs/feet remain unchanged; separate new pair attaches behind the pelvis. Front/back show four grounded feet; complete profile permits far-side overlap, not a detached foot to prove a count.',
    geometry=dict(front_left_path=left,front_right='Horizontal mirror in512px frame',profile_near_path=profile,profile_far='Same shape translated40px right, drawn behind near hind leg and unchanged body',attachment='Authored pelvic overlap around y525-640, hidden by original pelvis',foot_contact='Shared original y950 ground; no independent bounding-box rescale'),
    source_vs_authored='Two paired Feet slots, managers and explicit hind/foreleg prose are source facts. Spacing, knee bends, relative depth and unseen attachment surfaces are authored estimates; no human-to-horse species conversion.',
    frame=dict(canvas=[512,1024],contact=[256,950]),native_activation=False))
print('Constructed separate extra pair and front/profile/back over unchanged body; manual visual review pending.')
