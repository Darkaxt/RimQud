"""Bind the Pond subject to the two performed water conversions without regenerating."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image,ImageDraw,ImageFont,ImageChops
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
SHALLOW=ROOT/'art/conversion/tile-water-shallow/v1';DEEP=ROOT/'art/conversion/tile-water-deep/v1'
PATH=ROOT/'art/conversion/scn-dirtpath/v1'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
sources=json.loads((ROOT/'art/village/sources.json').read_text())
pond=next(x for x in sources['scenery'] if x['blueprint']=='Pond')
plant=next(x for x in sources['scenery'] if x['blueprint']=='Watervine')
refs=json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries']
ref=next(x for x in refs if x.get('blueprint')=='Watervine')
raw_path=DONOR/'village-originals/watervine-mask.png'
assert hashlib.sha256(raw_path.read_bytes()).hexdigest()==ref['native_mask_sha256']
packet=dict(entry='SCN-POND',recorded_at=datetime.now(timezone.utc).isoformat(),subject=pond,
 source_packets=[dict(entry='TILE-WATER-SHALLOW',**asset(SHALLOW/'source-packet.json')),dict(entry='TILE-WATER-DEEP',**asset(DEEP/'source-packet.json'))],
 reuse='All original/reference/manual/refinement/extraction steps are the actual recorded producer conversions. This Pond row binds them to its native blueprint and required states; no duplicate ImageGen or new liquid simulation.',
 original_limit='Pond default puddle mask is not its dynamic connected liquid atlas. Retained native pool context and installed LiquidVolume are the source for pool identity and state semantics.',
 required_states=dict(shallow='Native thin/wading water state selects the shallow resource without conflating those native movement categories.',deep='Native IsSwimmingDepth selects deep material. Do not turn every Pond deep merely because this authored state exists.',
  shore='All visible eligible wet neighbors control shoreline. Swimming neighbors separately control deep-to-shallow blending; a depth edge is not a bank.',
  foreground='Water underlay must not consume the native winning foreground object. Transparent foreground art is drawn afterward using its own tint/visibility, with no water tint, opaque black box or liquid silhouette clipping.'),
 context_foreground=dict(subject=plant,original_reference=ref,
  role='Unconverted native Watervine glyph used only to inspect transparent foreground-over-liquid composition. It receives no vegetation conversion credit.'),
 native_acceptance='Actual object priority, appearance/visibility, liquid state and moving/equipping behavior remain behind the every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
model=dict(kind='liquid_blueprint_art_binding',blueprint='Pond',native_description='A pool of liquid.',
 materials=dict(shallow=asset(SHALLOW/'registered/model.json'),swimming=asset(DEEP/'registered/model.json')),
 native_state='Actual visible open water-bearing LiquidVolume; native depth predicates and actual volume/mixture. No inferred or modified fluids.',
 shared_geometry=asset(PATH/'constructed-neighbor-index.json'),
 source=asset(HERE/'source-packet.json'),
 layer_contract=['Source-owned ground/background','Shallow liquid clipped by actual wet coverage','Deep liquid blended only within the wet domain using native swimming-neighbor coverage','Independent native visible foreground or its separately converted art, retaining its own tint/alpha and draw priority'],
 separation='This binding does not replace actors/plants/props with water, tint them blue or mark their unfinished conversions complete. Preserve native fallback on unsupported liquids/states.',
 state='Generation-ready authored recipe only; runtime binding and native acceptance pending')
(HERE/'model.json').write_bytes((json.dumps(model,indent=2,ensure_ascii=False)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
ground=Image.open(ROOT/'art/conversion/tile-grassy-ground/v1/registered/native-k-preview.png').convert('RGBA')
shallow=Image.open(SHALLOW/'registered/native-color-preview.png').convert('RGBA');deep=Image.open(DEEP/'registered/native-color-preview.png').convert('RGBA')
NEIGHBORS=[(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
def field(im,size):
 out=Image.new('RGBA',size)
 for y in range(0,size[1],im.height):
  for x in range(0,size[0],im.width):out.paste(im,(x,y))
 return out
def mask(cells,size):
 out=Image.new('L',size)
 for x,y in cells:
  bits=sum(1<<b for b,(dx,dy) in enumerate(NEIGHBORS) if (x+dx,y+dy) in cells)
  out.paste(Image.open(PATH/'constructed-neighbors'/f'{bits:03d}.png'),(x*64,y*64))
 return out
wet={(x,y) for x in range(1,15) for y in range(1,10) if ((x-7.5)/7)**2+((y-5)/4.5)**2<1}
swimming={(x,y) for x,y in wet if ((x-7.5)/4)**2+((y-5)/2.7)**2<1};size=(1024,704)
water=field(ground,size);wetmask=mask(wet,size);deepmask=mask(swimming,size)
for material,coverage in [(shallow,wetmask),(deep,ImageChops.multiply(deepmask,wetmask))]:
 layer=field(material,size);layer.putalpha(coverage);water.alpha_composite(layer)
# Decode the actual original foreground mask according to its native render roles.
raw=Image.open(raw_path).convert('RGBA');glyph=Image.new('RGBA',raw.size)
primary=bytes.fromhex(palette['w']);detail=bytes.fromhex(palette['g'])
for y in range(raw.height):
 for x in range(raw.width):
  rr,_,_,aa=raw.getpixel((x,y));f=rr/255
  glyph.putpixel((x,y),(*[round(p*(1-f)+q*f) for p,q in zip(primary,detail)],aa))
foreground=Image.new('RGBA',size)
for x,y in [(3,4),(5,6),(9,4),(11,6)]:foreground.alpha_composite(glyph.resize((64,96),Image.Resampling.NEAREST),(x*64,y*64-32))
assembled=water.copy();assembled.alpha_composite(foreground)
out=Image.new('RGB',(1280,905),'#142823');dr=ImageDraw.Draw(out)
dr.text((18,14),'POND AUTHORING / selected shallow + deep / original Watervine is foreground CONTEXT ONLY',font=font,fill='#e3cf43')
out.paste(assembled.resize((1024,704),Image.Resampling.LANCZOS).convert('RGB'),(128,60))
dr.text((18,792),'No water tint or coverage clipping applied to the separate native foreground.',font=font,fill='#e5e8d8')
dr.text((18,826),'This is an authored pool layout; native depth/foreground behavior is not tested here.',font=font,fill='#e5e8d8')
out.save(HERE/'foreground-comparison.png')
states=Image.new('RGB',(1440,742),'#142823');dr=ImageDraw.Draw(states)
dr.text((18,12),'POND / selected same wet footprint, three authored state/foreground views',font=font,fill='#e3cf43')
for i,(label,material) in enumerate([('SHALLOW ONLY',shallow),('SWIMMING ONLY',deep),('MIXED + NATIVE FOREGROUND',None)]):
 if material is None:im=assembled
 else:
  im=field(ground,size);layer=field(material,size);layer.putalpha(wetmask);im.alpha_composite(layer)
 states.paste(im.resize((448,308),Image.Resampling.LANCZOS).convert('RGB'),(16+i*480,70));dr.text((16+i*480,412),label,font=font,fill='#e5e8d8')
 small=im.resize((256,264),Image.Resampling.LANCZOS);states.paste(small.convert('RGB'),(16+i*480,452))
 dr.text((288+i*480,492),'16x24',font=font,fill='#e3cf43');dr.text((288+i*480,520),'per cell',font=font,fill='#e3cf43')
states.save(HERE/'states-comparison.png')
