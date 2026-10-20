"""Keep metal balls readable; constrain sculpted claws rather than hand-like digits."""
from pathlib import Path
import json,sys
from PIL import Image
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent
assert not (HERE/'patched-front-guided-turnaround.png').exists()
old='M-.18 7.47Q.45 7.2 .95 7.8L1.08 8.28Q.82 8.65 .62 8.22L.45 7.88Q.52 8.7 .24 8.62Q-.05 8.56 .02 8.04Q-.42 8.4-.55 8.1Q-.66 7.75-.18 7.47Z'
new='M-.08 7.53Q.35 7.35 .77 7.62L.9 8.08Q.85 8.38 .66 8.21L.51 7.95Q.55 8.5 .34 8.5Q.13 8.5 .15 7.98Q-.02 8.37-.24 8.21Q-.4 8.07-.23 7.77Z'
sheet=Image.new('RGBA',(1536,768))
for i,f in enumerate(['south','east','north','west']):
    for prefix in ['constructed','ownership']:
        s=(HERE/f'{prefix}-{f}.svg').read_text();assert s.count(old)==4;s=s.replace(old,new);(HERE/f'patched-{prefix}-{f}.svg').write_bytes(s.encode());(HERE/f'patched-{prefix}-{f}.png').write_bytes(svg_to_bytes(svg_string=s))
    if i<3:sheet.alpha_composite(Image.open(HERE/f'patched-constructed-{f}.png').convert('RGBA'),(512*i,0))
sheet.save(HERE/'patched-front-guided-turnaround.png')
(HERE/'claw-foot-patch.json').write_bytes((json.dumps(dict(reason='First manual inspection showed wide finger-like claw silhouettes. Constrain sculpted claws around their existing ball; keep cabriole legs, corner positions, tabletop, frame, camera and roles unchanged.',method='Editable local path substitution, four actual corner feet per facing and matching role geometry.',before='front-guided-turnaround.png',after='patched-front-guided-turnaround.png',new_imagegen_calls=0),indent=2)+'\n').encode())
p=HERE/'turnaround-prompt.txt';s=p.read_text();s=s.replace('Image1 is1536x768 edit target','Image1 is1536x768 patched edit target').replace('Four physical corner supports','Claws tightly cup round balls, no finger-like hands or detached digits. Four physical corner supports');(HERE/'patched-turnaround-prompt.txt').write_bytes(s.encode())
print('Patched all claw contours and ownership together; source limbs/frame/scale unchanged.')
