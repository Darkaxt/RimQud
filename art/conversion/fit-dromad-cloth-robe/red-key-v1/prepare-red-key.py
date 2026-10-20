"""Bounded chroma-key garment experiment requested by the user.

Preserve full-frame body shape/alpha; recolor even its dark contours red so
body linework can be distinguished from neutral garment outlines.
"""
from pathlib import Path
from PIL import Image, ImageOps
import json, hashlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad/v2'
CLOTH=HERE.parent/'v5'
assert not (HERE/'input-packet.json').exists(), 'Preserve experiment inputs'
def asset(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
bare=Image.new('RGBA',(1536,1024));cloth=Image.new('RGBA',bare.size)
sources=[]
for i,facing in enumerate(['south','east','north']):
    b=Image.open(BODY/f'selected-{facing}.png').convert('RGBA')
    g=ImageOps.grayscale(b)
    red=g.point(lambda v:round(64+191*v/255))
    green=red.point(lambda v:round(v*.055))
    blue=red.point(lambda v:round(v*.04))
    keyed=Image.merge('RGBA',(red,green,blue,b.getchannel('A')))
    keyed.save(HERE/f'red-body-{facing}.png')
    bare.paste(keyed,(i*512,0))
    garment=Image.open(CLOTH/f'intact-robe-{facing}.png').convert('RGBA')
    cloth.paste(garment,(i*512,0))
    sources.append({'facing':facing,'body':asset(BODY/f'selected-{facing}.png'),'whole_garment':asset(CLOTH/f'intact-robe-{facing}.png'),'red_body':asset(HERE/f'red-body-{facing}.png'),'cell':[i*512,0,512,1024],'contact':[i*512+256,950]})
bare.save(HERE/'red-body-sheet.png');cloth.save(HERE/'whole-robe-sheet.png')
packet={'scope':'One garment chroma-key generation/extraction experiment; no further generative isolation; no production readiness claim','body_model':asset(BODY/'model.json'),'item':'Cloth Robe','native_description':'Particulate from the eons-sheared shale sticks in the fibers of goat wool. They make red freckles on the garment.','palette_policy':'For this removable keying experiment body alone is saturated red. Cloth stays neutral grayscale, including tonal freckles, for later equipment tint. Red is not new canonical skin color.','body_color_mapping':'R=64+191*original_luminance/255; G=.055R; B=.04R; original alpha/coordinates retained. Even body outlines stay dark red.','sources':sources,'outputs':[asset(HERE/'red-body-sheet.png'),asset(HERE/'whole-robe-sheet.png')]}
(HERE/'input-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
