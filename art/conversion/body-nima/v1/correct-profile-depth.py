"""Put the posterior midline tail behind the near arm/body in the profile view."""
from pathlib import Path
import json
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent
assert not (HERE/'profile-depth-correction.json').exists()
out=Image.new('RGBA',(512,1264))
for name in ['patched-tail-back-east','patched-tail-front-east','patched-extra-arms-east','baseline-east']:
    out.alpha_composite(Image.open(HERE/(name+'.png')).convert('RGBA'))
out.save(HERE/'corrected-construction-east.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);sheet=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(sheet)
d.text((18,15),'NIMA / selected manual front and consistent cardinal tail; profile depth corrected',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    p=HERE/('corrected-construction-east.png' if f=='east' else f'patched-construction-{f}.png')
    im=Image.open(p).convert('RGBA').resize((240,593),Image.Resampling.LANCZOS);sheet.paste(im,(40+i*330,55),im);d.text((40+i*330,665),f.upper(),font=font,fill='#e3cf43')
d.text((18,715),'Near profile arm/body occludes the midline tail root; one separate tail retained in full.',font=font,fill='#e5e8d8');sheet.save(HERE/'corrected-construction-turnaround.png')
(HERE/'profile-depth-correction.json').write_bytes((json.dumps(dict(rejected='patched-construction-turnaround.png',reason='The2Dbody-plane split exposed a small midline tail-root facet over the near extra forearm. A mechanical body plane is not the full body/arm volume.',correction='In east/west profile, draw the whole posterior/midline tail behind the near extra arm and original body. Keep same canonical3Dgeometry and tail layers; north retains its visible posterior surface above the back. This is an explicit authored occlusion choice, not a new body bone or altered source topology.',unchanged='All geometry, body/head pixels, scale, contact and source4arm/one-tail anatomy.'),indent=2)+'\n').encode())
print('Corrected posterior tail/near arm depth in profile; earlier views retained.')
