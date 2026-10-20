"""Resolve the real cudgel, then construct one held asset and directional placements."""
from pathlib import Path
from datetime import datetime,timezone
import xml.etree.ElementTree as ET
import hashlib,json,math,re
from PIL import Image,ImageDraw,ImageFont,ImageChops
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad/v1'
ROBE=ROOT/'art/conversion/fit-dromad-cloth-robe/v1/registered'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
MOD=Path('D:/Steam/steamapps/workshop/content/294100/2454918552')
REF=MOD/'Textures/Things/Item/Equipment/WeaponMelee/LightClub.png'
DEFS=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Items.xml')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
snippet=re.search(r'<object Name="Shillelagh"[^>]*>.*?</object>',DEFS.read_text(encoding='utf-8-sig'),re.S).group(0)
bp=ET.fromstring(snippet)
declared={x.get('Name'):dict(x.attrib) for x in bp if x.tag=='part'}
race=json.loads((BODY/'source-packet.json').read_text())
binding=next(x for x in race['body']['attached_parts'] if x.get('equipped') and x['equipped']['blueprint']=='Shillelagh')
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Shillelagh')
assert sha(DONOR/original['reference_file'])==original['reference_sha256']
packet=dict(entry='FIT-DROMAD-SHILLELAGH-HAND-2',recorded_at=datetime.now(timezone.utc).isoformat(),
 creature='Tam',race='Dromad',original=original,observed_binding=binding,
 installed_definition=dict(file=str(DEFS),sha256=sha(DEFS),inherits=bp.get('Inherits'),parts=declared,object_xml=snippet),
 source_resolution='Captured runtime description is generic puzzling-device text and weight differs. Exact installed Shillelagh blueprint resolves a wooden stick with an oaken knot. Preserve both; identification state and reason for weight difference were not exported.',
 body=asset(BODY/'model.json'),robe_context=asset(ROBE/'model.json'),
 donor_reference=dict(file=str(REF),sha256=sha(REF),mod='Vanilla Weapons Expanded - Tribal',package_id='VanillaExpanded.VWETB',about_sha256=sha(MOD/'About/About.xml'),workshop_id='2454918552',role='Simple elongated wooden-club silhouette, neutral material and clean outline convention; no direct Qud shape equivalence.'),
 reference_selection='Also inspected Vanilla Textures Expanded Club; its spiked head is unsuitable for the described oaken knot, so selected the Tribal light club instead.',
 art_policy='One axial held-item texture, mechanically placed in each facing like a RimWorld held weapon. No invented front/back anatomy; placements and hand/depth ownership are directional.',
 authored_scale='Approximately 500 source pixels end to end, about two thirds of the selected adult height. Enlarged relative to the historical short staff after user feedback; not a native measured length.',
 palette='Neutral equal-RGB source with native equipment &y/detail y; no yellow or brown baked into model.',
 native_acceptance='Deferred until every conversion is generated')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024" viewBox="0 0 512 1024"><g fill="#b9bcb3" stroke="#343a34" stroke-width="6" stroke-linejoin="round"><path d="M249 938 L244 524 Q220 516 220 491 Q218 466 239 452 Q263 440 281 456 Q296 474 288 498 Q281 517 268 523 L270 939 Q260 950 249 938Z"/><path d="M251 525 Q258 649 255 764 L257 928 M233 479 Q251 459 278 476 M231 497 Q251 513 276 496" fill="none" stroke="#92978e" stroke-width="4"/><path d="M252 478 Q265 471 270 483 Q269 494 256 493Z" fill="#a6aaa1" stroke-width="3"/></g></svg>'''
(HERE/'constructed-item.svg').write_bytes(svg.encode())
(HERE/'constructed-item.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-item.svg'),skip_system_fonts=True))
item=Image.open(HERE/'constructed-item.png').convert('RGBA')
placements=dict(south=dict(grip=[105,777],angle=0,hand=[126,777],layer=.0018),
                east=dict(grip=[270,777],angle=25,hand=[250,778],layer=.0018),
                north=dict(grip=[408,777],angle=0,hand=[388,777],layer=-.0002))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
sheet=Image.new('RGBA',(1536,1088))
for i,(f,v) in enumerate(placements.items()):
    angle=math.radians(v['angle']);c,s=math.cos(angle),math.sin(angle);x,y=v['grip']
    affine=(c,s,256-c*x-s*y,-s,c,776+s*x-c*y)
    held=item.transform((512,1024),Image.Transform.AFFINE,affine,Image.Resampling.BICUBIC)
    hand=Image.new('L',held.size);d=ImageDraw.Draw(hand);hx,hy=v['hand'];d.ellipse((hx-32,hy-33,hx+32,hy+33),fill=255)
    if f!='north':held.putalpha(ImageChops.multiply(held.getchannel('A'),ImageChops.invert(hand)))
    held.save(HERE/f'constructed-held-{f}.png');hand.save(HERE/f'constructed-hand-cut-{f}.png')
    pawn=Image.open(ROBE/f'assembled-{f}.png').convert('RGBA')
    combined=Image.alpha_composite(held,pawn) if f=='north' else Image.alpha_composite(pawn,held)
    combined.save(HERE/f'constructed-fit-{f}.png');sheet.alpha_composite(combined,(i*512,0))
    ImageDraw.Draw(sheet).text((i*512+115,1040),dict(south='FRONT / SOUTH',east='RIGHT SIDE / EAST',north='BACK / NORTH')[f],font=font,fill='#b9b9b9')
(HERE/'placement-suggestion.json').write_bytes((json.dumps(placements,indent=2)+'\n').encode())
sheet.save(HERE/'constructed-fit-comparison.png')
plate=Image.new('RGB',(1400,700),'#142823');d=ImageDraw.Draw(plate)
d.text((24,18),'TAM > DROMAD > SHILLELAGH / exact definition resolves generic capture',font=font,fill='#e3cf43')
for im,xy,size in [(Image.open(DONOR/original['reference_file']),(40,120),(160,240)),(Image.open(REF),(280,210),(400,150)),(item,(740,80),(280,560)),(Image.open(ROBE/'assembled-south.png'),(1060,80),(280,560))]:
    im=im.convert('RGBA');im=im.crop(im.getbbox());factor=min(size[0]/im.width,size[1]/im.height)
    im=im.resize((round(im.width*factor),round(im.height*factor)),Image.Resampling.NEAREST if xy[0]<700 else Image.Resampling.LANCZOS);plate.paste(im,xy,im)
for xy,text in [((24,430),'Qud original glyph'),((250,430),'Actual installed Tribal LightClub'),((250,465),'Reference: wood/outline, not a sword'),((740,650),'Editable oaken-knot stick'),((1060,650),'Fixed adult / robe')]:d.text(xy,text,font=font,fill='#e5e8d8')
plate.save(HERE/'source-comparison.png')
