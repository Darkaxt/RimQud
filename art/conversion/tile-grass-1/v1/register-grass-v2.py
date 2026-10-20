"""Register both refined shoots together in the original rectangular paint frame."""
from pathlib import Path
import hashlib,json
from PIL import Image,ImageChops,ImageDraw,ImageFont,ImageOps

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
OUT=HERE/'registered-v2';OUT.mkdir(exist_ok=True)
source=Image.open(HERE/'refined-proposal.png').convert('RGBA')
binary=source.getchannel('A').point(lambda a:255 if a>=16 else 0)
union=Image.new('L',source.size)
for name,seed in [('long-right',(510,900)),('short-left',(400,850))]:
    selected=binary.copy();ImageDraw.floodfill(selected,seed,128)
    selected=selected.point(lambda v:255 if v==128 else 0)
    selected.save(OUT/f'source-selection-{name}.png');union=ImageChops.lighter(union,selected)
alpha=ImageChops.multiply(source.getchannel('A'),union).point(lambda v:0 if v<16 else (255 if v>=240 else v))
g=ImageOps.grayscale(source);neutral=Image.merge('RGBA',(g,g,g,alpha))
neutral.paste((0,0,0,0),mask=alpha.point(lambda v:255 if v==0 else 0))
neutral.save(OUT/'cleaned-proposal.png')
scale=.55;source_root=[524,991];target_root=[273,512]
scaled=neutral.resize((round(neutral.width*scale),round(neutral.height*scale)),Image.Resampling.LANCZOS)
delta=[target_root[0]-round(source_root[0]*scale),target_root[1]-round(source_root[1]*scale)]
registered=Image.new('RGBA',(512,768))
# An explicit authoring width correction, per shoot. Row centers/tips/root y do not move.
for name in ['long-right','short-left']:
    selection=Image.open(OUT/f'source-selection-{name}.png').convert('L')
    component=Image.merge('RGBA',(g,g,g,ImageChops.multiply(alpha,selection)))
    component.paste((0,0,0,0),mask=component.getchannel('A').point(lambda v:255 if v==0 else 0))
    component=component.resize((round(component.width*scale),round(component.height*scale)),Image.Resampling.LANCZOS)
    component_frame=Image.new('RGBA',(512,768));component_frame.paste(component,delta)
    patched=Image.new('RGBA',(512,768))
    for y in range(768):
        row=component_frame.crop((0,y,512,y+1));bounds=row.getchannel('A').point(lambda v:255 if v>=16 else 0).getbbox()
        if not bounds:continue
        left,_,right,_=bounds;center=(left+right-1)/2
        width=max(1,round((right-left)*1.5))
        line=row.crop((left,0,right,1)).resize((width,1),Image.Resampling.LANCZOS)
        patched.paste(line,(round(center-(width-1)/2),y))
    registered=Image.alpha_composite(registered,patched)
channels=registered.split();level=channels[0].point(lambda v:min(255,round(v*.76+55)))
registered=Image.merge('RGBA',(level,level,level,channels[3]))
registered.paste((0,0,0,0),mask=registered.getchannel('A').point(lambda v:255 if v==0 else 0))
registered.save(OUT/'grass1-neutral.png');registered.getchannel('A').save(OUT/'grass1-coverage.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,key):
    color=bytes.fromhex(palette[key]);g=im.getchannel('R')
    return Image.merge('RGBA',(*[g.point(lambda v,c=c:round(v*c/255)) for c in color],im.getchannel('A')))
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
model=dict(kind='native_cell_paint',native_tile='Terrain/sw_grass1.bmp',identity='Basic Grass 1',
 canvas=[512,768],native_cell=[16,24],nominal_native_anchor=[8,16],nominal_canvas_anchor=[256,512],
 refined_main_blade_root=target_root,
 neutral=asset(OUT/'grass1-neutral.png'),coverage=asset(OUT/'grass1-coverage.png'),
 color_role='Native cell primary foreground; no source detail region',
 palette_policy='Do not bake preview green into production RGB. Source references do not establish a universal paint color; preserve native cell tint/visibility, including non-green usages.',
 frame_policy='Keep the entire 16 x 24 source cell frame; nominal pivot is fixed. Both shoots share one .55 scale and one translation. After shared frame registration, each blade is widened x1.5 about its existing row centerline; root/tip y and nominal cell pivot remain fixed.',
 view_policy='One fixed map-paint view. No biological growth, facing rotation, wind or extra blades invented. Grass variants 2 and 3 remain separate entries.',
 layer='Native paint layer relative to ground; real draw-order/visibility binding pending final integration',
 state='Generation-ready authoring only; native acceptance pending every-conversion-generated gate')
decisions=dict(source='../refined-proposal.png',source_size=list(source.size),
 seeds=dict(long_right=[510,900],short_left=[400,850]),source_root=source_root,target_root=target_root,
 scale=scale,translation=delta,canvas=[512,768],
 correction='Selected both complete connected shoots, neutralized RGB and cleared invisible RGB; widened each blade x1.5 around its fixed per-row center and applied neutral value lift .76*v+55 for native-size readability. Original frame/scale translation is unchanged.',
 interpretation='Two shoots retained. The first too-thin registration is preserved as rejected history. This direct width/value authoring patch needs no additional generator loop; no extra blade or motion/facing state is invented.')
for name,obj in [('model.json',model),('registration-decisions.json',decisions)]:
    (OUT/name).write_bytes((json.dumps(obj,indent=2)+'\n').encode())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17)
plate=Image.new('RGB',(1280,660),'#142823');d=ImageDraw.Draw(plate)
d.text((20,14),'BASIC GRASS 1 / original frame retained / neutral source and cell-owned tint',font=font,fill='#e3cf43')
for i,(label,im) in enumerate([('NEUTRAL',registered),('NATIVE g PREVIEW',tint(registered,'g')),('NATIVE C PREVIEW',tint(registered,'C'))]):
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
                         'Two sparse shoots; no dense donor tuft. Colored images are previews, not production RGB.',
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
