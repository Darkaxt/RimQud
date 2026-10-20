"""Extend support tops beneath the sling without shifting the source foot positions."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent
svg=(HERE/'constructed-front.svg').read_text(encoding='utf-8')
replacements={
 'M12.05 10.9L13.5 14.7H13.05L11.65 11.15Z M13.05 10.7L12.3 14.15L12.7 14.35L13.55 10.95Z':'M12.05 8.9L13.5 14.7H13.05L11.65 9.15Z M13.55 8.4L12.3 14.15L12.7 14.35L14.05 8.65Z',
 'M3.3 11.65L6.5 17.95V18.5H6.05L2.9 11.9Z':'M3.05 9.45L6.5 17.95V18.5H6.05L2.65 9.7Z',
 'M6.65 11.8L3.35 16.85L3.05 16.6L6.1 11.5Z':'M7.9 10.7L3.35 16.85L3.05 16.6L7.35 10.4Z',
 'cx="4.75" cy="14.65"':'cx="4.7" cy="13.8"'}
for old,new in replacements.items():assert old in svg;svg=svg.replace(old,new)
(HERE/'constructed-front-v2.svg').write_bytes(svg.encode());(HERE/'constructed-front-v2.png').write_bytes(svg_to_bytes(svg_string=svg))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1200,780),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'CONSTRUCTION CORRECTION / supports must reach their seat attachment, not float below it',font=font,fill='#e3cf43')
for x,name,label in [(150,'constructed-front.png','Initial draft / support tops too short'),(730,'constructed-front-v2.png','Corrected / tops overlap beneath sling')]:
 im=Image.open(HERE/name).convert('RGBA').resize((320,480),Image.Resampling.LANCZOS);plate.paste(im,(x,70),im);draw.text((x-50,580),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Only upper wooden attachment geometry changes. Source sling, rails, lower foot positions and full-cell frame stay fixed.',
 'The seat is drawn in front of support tops; this is explicit under-seat occlusion, not detached floating wood.',
 'The original SVG/PNG remain preserved. The corrected construction is the actual ImageGen edit target.']):draw.text((20,655+i*30),line,font=font,fill='#e5e8d8')
plate.save(HERE/'construction-attachment-comparison.png');print('Connected support tops beneath unchanged sling; original draft and corrected editable geometry both retained.')
