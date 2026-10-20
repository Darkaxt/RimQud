"""Register three refined shoots together in the original rectangular paint frame."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
source=Image.open(HERE/'refined-proposal.png').convert('RGBA')
binary=source.getchannel('A').point(lambda a:255 if a>=16 else 0)
union=Image.new('L',source.size)
for name,seed in [('long-left',(340,940)),('tall-middle',(530,900)),('short-right',(655,1010))]:
    selected=binary.copy();ImageDraw.floodfill(selected,seed,128)
    selected=selected.point(lambda v:255 if v==128 else 0)
    selected.save(OUT/f'source-selection-{name}.png');union=ImageChops.lighter(union,selected)
alpha=ImageChops.multiply(source.getchannel('A'),union).point(lambda v:0 if v<16 else (255 if v>=240 else v))
g=ImageOps.grayscale(source);neutral=Image.merge('RGBA',(g,g,g,alpha))
neutral.paste((0,0,0,0),mask=alpha.point(lambda v:255 if v==0 else 0))
neutral.save(OUT/'cleaned-proposal.png')
scale=.5;source_root=[534,932];target_root=[273,451]
scaled=neutral.resize((round(neutral.width*scale),round(neutral.height*scale)),Image.Resampling.LANCZOS)
delta=[target_root[0]-round(source_root[0]*scale),target_root[1]-round(source_root[1]*scale)]
registered=Image.new('RGBA',(512,768));registered.paste(scaled,delta)
channels=registered.split();level=channels[0].point(lambda v:min(255,round(v*.82+42)))
registered=Image.merge('RGBA',(level,level,level,channels[3]))
registered.paste((0,0,0,0),mask=registered.getchannel('A').point(lambda v:255 if v==0 else 0))
registered.save(OUT/'grass2-neutral.png');registered.getchannel('A').save(OUT/'grass2-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,key):
    color=bytes.fromhex(palette[key]);g=im.getchannel('R')
    return Image.merge('RGBA',(*[g.point(lambda v,c=c:round(v*c/255)) for c in color],im.getchannel('A')))
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
model=dict(kind='native_cell_paint',native_tile='Terrain/sw_grass2.bmp',identity='Basic Grass 2',
 canvas=[512,768],native_cell=[16,24],nominal_native_anchor=[8,16],nominal_canvas_anchor=[256,512],
 refined_main_blade_root=target_root,
 neutral=asset(OUT/'grass2-neutral.png'),coverage=asset(OUT/'grass2-coverage.png'),
 color_role='Native cell primary foreground; no source detail region',
 palette_policy='Do not bake preview green into production RGB. Source references do not establish a universal paint color; preserve native cell tint/visibility, including non-green usages.',
 frame_policy='Keep the entire 16 x 24 source cell frame; nominal pivot is fixed. All three shoots share one .5 scale and one translation. Their alpha bounds are not independently centered/fitted.',
 view_policy='One fixed map-paint view. No biological growth, facing rotation, wind or extra blades invented. Grass variants 1 and 3 are separate entries.',
 layer='Native paint layer relative to ground; real draw-order/visibility binding pending final integration',
 state='Generation-ready authoring only; native acceptance pending every-conversion-generated gate')
decisions=dict(source='../refined-proposal.png',source_size=list(source.size),
 seeds=dict(long_left=[340,940],tall_middle=[530,900],short_right=[655,1010]),source_root=source_root,target_root=target_root,
 scale=scale,translation=delta,canvas=[512,768],
 correction='Selected three complete connected shoots, neutralized RGB, lifted values .82*v+42 for native-size readability and cleared invisible RGB. Tool-preview glow was RGB in alpha-zero pixels, not visible plant coverage.',
 interpretation='The three-shoot silhouette and unequal root heights were retained. No structural shape error required another generator loop; extraction/registration completes this fixed-view paint refinement.')
for name,obj in [('model.json',model),('registration-decisions.json',decisions)]:
    (OUT/name).write_bytes((json.dumps(obj,indent=2)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
plate=Image.new('RGB',(1280,660),'#142823');d=ImageDraw.Draw(plate)
d.text((20,14),'BASIC GRASS 2 / original frame retained / neutral source and cell-owned tint',font=font,fill='#e3cf43')
for i,(label,im) in enumerate([('NEUTRAL',registered),('NATIVE g PREVIEW',tint(registered,'g')),('NATIVE O PREVIEW',tint(registered,'O'))]):
    bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im)
    x=20+i*280;plate.paste(bg.resize((256,384),Image.Resampling.LANCZOS).convert('RGB'),(x,70))
    d.line((x+128,70,x+128,453),fill='#cebc45');d.line((x,326,x+255,326),fill='#70b8b0')
    d.text((x,477),label,font=font,fill='#e3cf43')
small=tint(registered,'g')
for i,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
    thumb=small.resize((w,h),Image.Resampling.LANCZOS)
    bg=Image.new('RGBA',thumb.size,'#004808');bg.alpha_composite(thumb)
    x=900+i*110;plate.paste(bg.convert('RGB'),(x,95))
    enlarged=bg.resize((w*4,h*4),Image.Resampling.NEAREST);plate.paste(enlarged.convert('RGB'),(x-10,210))
    d.text((x-10,440),f'{w}x{h}',font=font,fill='#e3cf43')
for i,text in enumerate(['Guides mark the nominal cell pivot and y=16 paint anchor, not a humanoid foot contact.',
                         'Three sparse shoots; no dense donor tuft. Colored images are previews, not production RGB.',
                         'Other grass variants, ground material and native integration remain unfinished.']):
    d.text((20,550+i*28),text,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
field=Image.new('RGBA',(768,576),'#004808')
for row in range(12):
    for col in range(16):
        if (row*5+col*3)%4==0:
            glyph=tint(registered,'g').resize((48,72),Image.Resampling.LANCZOS)
            field.alpha_composite(glyph,(col*48,row*48-16))
field.convert('RGB').save(OUT/'paint-distribution-comparison.png')
