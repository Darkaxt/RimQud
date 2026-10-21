"""Replace the unclear ascending helix with one visible, rear-attached planar spiral."""
from pathlib import Path
import json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
from tail_geometry import render_tail
HERE=Path(__file__).resolve().parent
assert not (HERE/'tail-construction-v2.json').exists()
packet=json.loads((HERE/'source-packet.json').read_text());frame=packet['frame']
u=np.array([2**-.5,2**-.5,0]);centre=np.array([-.08,-.23,1.06])
angle=np.linspace(-np.pi/2,2.25*np.pi,550);radius=np.linspace(.30,.14,len(angle))
coil=centre+radius[:,None]*np.cos(angle)[:,None]*u
coil[:,2]+=radius*np.sin(angle)
end=coil[0];p0=np.array([.02,-.16,.55]);p1=np.array([-.18,-.34,.62]);p2=end-u*.08
t=np.linspace(0,1,120)[:,None];rise=(1-t)**3*p0+3*(1-t)**2*t*p1+3*(1-t)*t**2*p2+t**3*end
dense=np.concatenate([rise,coil[1:]]);distance=np.concatenate([[0],np.cumsum(np.linalg.norm(np.diff(dense,axis=0),axis=1))]);samples=np.linspace(0,distance[-1],25)
centres=np.column_stack([np.interp(samples,distance,dense[:,j]) for j in range(3)])
end=centres[-1];stinger=np.array([end,end+u*.04+np.array([0,0,.01]),end+u*.075+np.array([0,0,-.015]),end+u*.10+np.array([0,0,-.095]),end+u*.025+np.array([0,0,-.045]),end-u*.025+np.array([0,0,-.02])]);bead=end+u*.10+np.array([0,0,-.115])
data=dict(centreline=centres.tolist(),stinger=stinger.tolist(),bead=bead.tolist(),segments=24,plane='Vertical spiral with horizontal direction rotated45deg relative to the body; intrinsic tail direction only, cardinal body unchanged.',
          source_dimensions='Unknown; all numerical dimensions and24surface segments authored from source great/spiral/jeweled cues.',frame=frame)
(HERE/'tail-construction-v2.json').write_bytes((json.dumps(data,indent=2)+'\n').encode())
render_tail(HERE,centres,stinger,bead,frame,'patched')
# In a true profile, the far extra arm/hand is occluded by the near one.
path='M225 591 Q170 594 141 662 Q109 737 128 816 L141 905 Q155 925 176 912 L165 810 Q157 751 184 705 L245 657 Z'
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1264" viewBox="0 0 512 1264"><path d="'+path+'" fill="#e3e3e3" stroke="#2b2b2b" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/><ellipse cx="151" cy="930" rx="21" ry="22" fill="#e8e8e8" stroke="#2b2b2b" stroke-width="8"/></svg>'
(HERE/'patched-extra-arms-east.svg').write_bytes(svg.encode());(HERE/'patched-extra-arms-east.png').write_bytes(svg_to_bytes(svg_string=svg))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);sheet=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(sheet)
d.text((18,15),'NIMA / corrected shared spiral; clean profile arm overlap, unchanged base',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    out=Image.new('RGBA',(512,1264));out.alpha_composite(Image.open(HERE/f'patched-tail-back-{f}.png').convert('RGBA'))
    out.alpha_composite(Image.open(HERE/('patched-extra-arms-east.png' if f=='east' else f'extra-arms-{f}.png')).convert('RGBA'))
    out.alpha_composite(Image.open(HERE/f'baseline-{f}.png').convert('RGBA'));out.alpha_composite(Image.open(HERE/f'patched-tail-front-{f}.png').convert('RGBA'));out.save(HERE/f'patched-construction-{f}.png')
    im=out.resize((240,593),Image.Resampling.LANCZOS);sheet.paste(im,(40+i*330,55),im);d.text((40+i*330,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'Source limb count is four; side far limbs may be occluded. Tail remains one appendage.',font=font,fill='#e5e8d8');sheet.save(HERE/'patched-construction-turnaround.png')
(HERE/'manual-corrections.json').write_bytes((json.dumps(dict(rejected='constructed-turnaround.png',changes=['Ascending helical tail read as a zigzag; replace with one inward-coiling spiral on a shared vertical plane, still projected from3D into cardinal views.','Profile far extra arm created an awkward inner stub; establish natural near/far occlusion, retaining two additional arms in front/back and the source4arm tree.'],unchanged='Entire baseline body/head pixel arrays, physical scale/contact, original two arms/hands/feet and neutral pose.'),indent=2)+'\n').encode())
print('Corrected visible spiral and profile occlusion; original proposal preserved.')
