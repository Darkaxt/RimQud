"""Source-bound grassy substrate: native dark-teal field, separate grass paint."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import hashlib,json,random,math
from PIL import Image,ImageDraw,ImageFont,ImageOps
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
donor=next(x for x in json.loads((DONOR/'joppa-textures.json').read_text()) if x['file']=='marsh.png')
assert sha(DONOR/'marsh.png')==donor['png_sha256']
capture=Image.open(ROOT/'docs/images/village-original.png').convert('RGB')
colors=Counter(capture.crop((0,60,1204,740)).get_flattened_data()).most_common(8)
dominant=colors[0][0];assert dominant==tuple(bytes.fromhex(palette['k']))
sources=json.loads((ROOT/'art/village/sources.json').read_text())
floor=next(x for x in sources['scenery'] if x['blueprint']=='DirtFloor')
packet=dict(entry='TILE-MARSH',recorded_at=datetime.now(timezone.utc).isoformat(),
 subject='Grassy-ground substrate in the bounded village presentation; marsh.png is a historical adapter label, not a new Qud marsh blueprint',
 original_field_capture=asset(ROOT/'docs/images/village-original.png'),
 capture_context='Historical native game capture with grass paint, not a new capture or proof of current runtime binding.',
 field_sample=dict(rect=[0,60,1204,740],dominant_rgb=dominant,dominant_palette_role='k',common_colors=[dict(rgb=rgb,count=n) for rgb,n in colors]),
 native_source=dict(floor=floor,paint_sources=[asset(ROOT/f'art/conversion/tile-grass-{i}/v1/source-packet.json') for i in [1,2,3]],
                    explanation='Native floor/paint cells use sparse glyphs over a broad dark-teal background. There is no original full-color turf texture or independent grass-ground Description.Short to extract.'),
 donor_reference=dict(**donor,role='Actual RimWorld Marsh supplies restrained fine organic grain and broad low-contrast material modulation. Its donor color, moisture/terrain mechanics and any liquid interpretation are not adopted.'),
 historical_draft=asset(ROOT/'art/village/scenery/surface-marsh.png'),
 palette=dict(background_role='k',background_hex=palette['k'],grass_paint_role='native cell primary',preview_grass_hex=palette['g']),
 design='Continuous low-relief substrate tinted by native field background k, with restrained fine fiber/grain. No tall grass, baked shoot icons, sand fill, puddles, banks, water depth or new plant species. Grass1/2/3 remain separate paint layers.',
 frame='Top-down seamless ground surface; no creature views or clothing. Material UV is world-anchored and must not reset in each cell.',
 current_adapter_evidence=dict(renderer=asset(ROOT/'probe/JoppaRenderer.cs'),capture=asset(ROOT/'probe/JoppaSimulation.cs'),
    observation='Current broad ground branch selects marsh.png with Color.white and quad-local UV; the grass flag derives from native PaintTile. New neutral art requires source-aware background tint, world UV and layer/eligibility binding at final integration; the existing broad branch is not proof of that behavior.'),
 binding_scope='Visible grassy-field substrate in its source-owned native ground context. Do not blindly recolor every DirtFloor/indoor cell or overwrite native water and bare-soil roles. Preserve actual native visibility and paint/ground ownership.',
 required_states='Continuous filled material plus source-eligible grass/other-ground boundaries. Path coverage belongs to DirtPath above this layer; water depth belongs to water entries. Reuse compatible 8-neighbor coverage geometry, with grassy-ground eligibility semantics, rather than generating another atlas.',
 native_acceptance='Pending every-conversion-generated gate. Renderer/shader behavior is not changed by this authoring script.')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())

rng=random.Random(20517);side=512;defs=[];shapes=['<rect width="512" height="512" fill="#ededed"/>']
for i in range(28):
    x,y=rng.uniform(0,side),rng.uniform(0,side);rx,ry=rng.uniform(35,100),rng.uniform(28,90)
    tone=rng.randint(210,244)
    defs.append(f'<radialGradient id="m{i}"><stop offset="0" stop-color="rgb({tone},{tone},{tone})" stop-opacity=".35"/><stop offset="1" stop-color="rgb({tone},{tone},{tone})" stop-opacity="0"/></radialGradient>')
    for dx in [-side,0,side]:
        for dy in [-side,0,side]:
            if x+dx+rx<0 or x+dx-rx>side or y+dy+ry<0 or y+dy-ry>side:continue
            shapes.append(f'<ellipse cx="{x+dx:.2f}" cy="{y+dy:.2f}" rx="{rx:.2f}" ry="{ry:.2f}" fill="url(#m{i})"/>')
for i in range(1800):
    x,y=rng.uniform(0,side),rng.uniform(0,side);length=rng.uniform(1,4);angle=rng.uniform(0,math.pi*2)
    ex,ey=x+math.cos(angle)*length,y+math.sin(angle)*length;tone=rng.randint(172,255);width=rng.uniform(.3,.75)
    for dx in [-side,0,side]:
        for dy in [-side,0,side]:
            if max(x+dx,ex+dx)<0 or min(x+dx,ex+dx)>side or max(y+dy,ey+dy)<0 or min(y+dy,ey+dy)>side:continue
            shapes.append(f'<path d="M{x+dx:.2f} {y+dy:.2f} L{ex+dx:.2f} {ey+dy:.2f}" stroke="rgb({tone},{tone},{tone})" stroke-width="{width:.2f}" stroke-opacity=".3" stroke-linecap="round"/>')
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><defs>'+''.join(defs)+'</defs>'+''.join(shapes)+'</svg>'
(HERE/'constructed-ground.svg').write_bytes(svg.encode())
(HERE/'constructed-neutral.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-ground.svg'),skip_system_fonts=True))
neutral=Image.open(HERE/'constructed-neutral.png').convert('RGBA');g=ImageOps.grayscale(neutral)
base=bytes.fromhex(palette['k']);colored=Image.merge('RGB',tuple(g.point(lambda v,c=c:round(v*c/255)) for c in base))
colored.save(HERE/'constructed-qud-ground.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',18)
plate=Image.new('RGB',(1440,820),'#142823');d=ImageDraw.Draw(plate)
d.text((24,16),'GRASSY GROUND / native k substrate + separate native-tinted grass paint',font=font,fill='#e3cf43')
native=capture.resize((576,360),Image.Resampling.LANCZOS);plate.paste(native,(24,80))
d.text((24,465),'Native capture / dominant field #0F3B3A',font=font,fill='#e5e8d8')
ref=Image.open(DONOR/'marsh.png').convert('RGB').resize((320,320),Image.Resampling.LANCZOS);plate.paste(ref,(650,100))
d.text((650,465),'Actual RimWorld Marsh / grain only',font=font,fill='#e5e8d8')
plate.paste(colored.resize((320,320),Image.Resampling.LANCZOS),(1035,100));d.text((1010,465),'Manual neutral grain + native k',font=font,fill='#e5e8d8')
for i,text in enumerate(['Native glyphs do not supply a full turf texture; this low-relief material is an authored interpretation.',
                         'Keep the field background dark teal and add Grass1/2/3 separately with source-owned foreground color.',
                         'No new water, plant species, grass spawn pattern or simulation behavior is inferred from the donor name.',
                         'Existing adapter tint/UV/eligibility wiring remains final integration work, after all generation.']):
    d.text((24,535+i*33),text,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
sample=colored.resize((768,768),Image.Resampling.LANCZOS).convert('RGBA')
paths=[ROOT/'art/conversion/tile-grass-1/v1/registered-v2/grass1-neutral.png']+[ROOT/f'art/conversion/tile-grass-{i}/v1/registered/grass{i}-neutral.png' for i in [2,3]]
for row in range(12):
    for col in range(16):
        if (row*5+col*3)%4==0:
            glyph=Image.open(paths[(row+col)%3]).convert('RGBA');v=glyph.getchannel('R');color=bytes.fromhex(palette['g'])
            glyph=Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in color],glyph.getchannel('A'))).resize((48,72),Image.Resampling.LANCZOS)
            sample.alpha_composite(glyph,(col*48,row*56-8))
out=Image.new('RGB',(768,842),'#142823');out.paste(sample.convert('RGB'),(0,54));ImageDraw.Draw(out).text((14,12),'MANUAL / substrate plus three separate paint variants / authoring arrangement',font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14),fill='#e3cf43');out.save(HERE/'constructed-context-comparison.png')
