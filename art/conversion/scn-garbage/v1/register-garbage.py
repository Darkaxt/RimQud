"""Carry restrained generated surface grain into canonical source-layout geometry."""
from pathlib import Path
import json,hashlib,re,sys,io
import numpy as np
from scipy.ndimage import gaussian_filter
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';assert not OUT.exists();OUT.mkdir()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
controls=read(HERE/'construction-controls.json');selection=read(HERE/'material-selection.json');palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];fg=np.frombuffer(bytes.fromhex(palette['K']),dtype=np.uint8);bg=tuple(bytes.fromhex(palette['k']))
grains={}
for item in selection['selected']:
    a=np.array(Image.open(ROOT/item['specimen']['path']).convert('RGBA'));g=a[:,:,:3].astype(float).mean(2);assert a[:,:,3].min()>=250
    residual=g-gaussian_filter(g,2.0);residual=np.clip(residual,-18,18)*.45
    # Reflected repeats preserve edge values without bringing object contours into the texture.
    repeat=np.block([[residual,residual[:,::-1]],[residual[::-1,:],residual[::-1,::-1]]])
    repeat=np.array(Image.fromarray(repeat.astype(np.float32)).resize((repeat.shape[1]*2,repeat.shape[0]*2),Image.Resampling.BICUBIC))
    grains[item['material']]=np.tile(repeat,(int(np.ceil(768/repeat.shape[0])),int(np.ceil(512/repeat.shape[1]))))[:768,:512]
def ownership(svg,role):
    svg=re.sub(r'fill="#[0-9a-fA-F]{6}"','fill="#000000"',svg)
    svg=re.sub(r'stroke="(#[0-9a-fA-F]{6})"',lambda m:'stroke="'+('#ffffff' if role=='wire' and m[1] in ['#adadad','#d3d3d3'] else '#000000')+'"',svg)
    for material in grains:svg=svg.replace('fill="url(#'+material+')"','fill="'+('#ffffff' if material==role else '#000000')+'"')
    a=np.array(Image.open(io.BytesIO(svg_to_bytes(svg_string=svg))).convert('RGBA'));return a[:,:,:3].astype(float).mean(2)/255*a[:,:,3]/255
states=[];masters={};neutral={};native={}
for item in controls['states']:
    ident=item['id'];svg=(ROOT/item['editable']['path']).read_text();a=np.array(Image.open(ROOT/item['constructed']['path']).convert('RGBA'));original=a.copy();luma=a[:,:,:3].astype(float).mean(2)
    folder=OUT/ident;folder.mkdir();weights={}
    for material,grain in grains.items():
        weight=ownership(svg,material);weights[material]=weight;Image.fromarray(np.uint8(np.round(weight*255))).save(folder/f'ownership-{material}-master.png');luma+=grain*weight
    a[:,:,:3]=np.uint8(np.clip(np.round(luma),0,255))[:,:,None];a[a[:,:,3]==0,:3]=0;assert np.array_equal(a[:,:,3],original[:,:,3])
    master=Image.fromarray(a);master.save(folder/'primary-master.png');masters[ident]=master
    out=np.array(master.resize((256,256),Image.Resampling.LANCZOS));out[:,:,:3]=np.uint8(np.round(out[:,:,:3].astype(float).mean(2)))[:,:,None];out[out[:,:,3]==0,:3]=0
    primary=Image.fromarray(out);primary.save(folder/'primary-neutral.png');alpha=primary.getchannel('A');alpha.save(folder/'coverage.png')
    Image.new('RGBA',(256,256)).save(folder/'detail-neutral.png');Image.new('L',(256,256)).save(folder/'detail-weight.png');Image.new('L',(256,256)).save(folder/'detail-coverage.png')
    mask=Image.new('RGBA',(256,256));mask.putalpha(alpha);mask.save(folder/'authored-dualcolor-mask.png')
    colored=out.copy();colored[:,:,:3]=np.uint8(np.round(out[:,:,:3].astype(float)*fg/255));colored[colored[:,:,3]==0,:3]=0;Image.fromarray(colored).save(folder/'native-K.png');neutral[ident]=primary;native[ident]=Image.fromarray(colored)
    states.append(dict(id=ident,native_tile=item['native_tile'],role='RandomTile choice' if ident!='fallback' else 'Declared Render fallback; not a fifth random choice',
        **{key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]},
        material_ownership={m:ref(folder/f'ownership-{m}-master.png') for m in grains},master=ref(folder/'primary-master.png'),native_preview=ref(folder/'native-K.png')))
review=dict(status='PASS FOR MATERIAL REFERENCE; CANONICAL GEOMETRY AND INK RETAINED',
    accepted='Actual refinement retains five corresponding layouts and sparse fallback, with usable pitted metal, paper fibre, glass and wire surface texture. No missing required variant or extra whole appliance.',
    controlled_differences='Generated borders/highlights are heavier/glossier than selected Core map-art convention. Keep existing editable curves/outline/serif strokes and alpha; transfer only bounded high-frequency gray material residuals inside their authored ownership masks.',
    sample_correction='Initial paper pick included transparency/ink and metal pick approached a border. Rejected boxes/plate retained; final opaque interior specimens inspected before use.',
    transfer='Gray residual = clamp(specimen - Gaussian(specimen,sigma2),-18,18)*0.45. Reflect at tile edges, scale2, use common source-cell coordinates and material ownership. No object contour, label, source ink, alpha or secondary colour is transferred.',
    extra_refinement='No second isolation or redraw requested: generated material is usable and source geometry is retained. This is deterministic surface registration, not a fabricated second ImageGen step.',native_activation=False)
write(HERE/'first-structural-review.json',review)
write(HERE/'generation-receipt.json',dict(tool='built-in image_gen.imagegen',actual_calls=1,prompt=ref(HERE/'refinement-prompt.txt'),output=ref(HERE/'refined-raw.png'),original_generated_filename='exec-a3f430ee-fd80-463e-b97d-c4e37ca0ee56.png',transparent_background=True,
    referenced_images=[ref(HERE/n) for n in ['constructed-family.png','source-construction-comparison.png','source-reference-variants-reviewed.png']],second_isolation_call=False))
model=dict(entry='SCN-GARBAGE',kind='source_primary_native_random_tile_family',blueprint='Garbage',source=ref(HERE/'source-packet.json'),construction=ref(HERE/'construction-controls.json'),source_states=ref(HERE/'native-state-index.json'),palette_resolution=ref(HERE/'palette-resolution.json'),native_state_study=ref(HERE/'native-state-study.json'),registration=controls['frame'],camera=controls['camera'],
    palette=dict(primary='K',background='k',detail='Unused: all5source masks have visible R0 only',native_primary_rgb=palette['K'],native_background_rgb=palette['k'],rule='Gray material luminance modulates native primary K. Background belongs outside coverage; no fixed coloured production pixels or invented bright secondary tint.'),
    state_owner='Four actual RandomTile choices selected by native builder; fallback remains distinct and scoped to Garbage. No global replacement of generic font/glyph or procedural Core filth clustering.',
    native_behavior='Preserve Takeable=true, Solid=false, native Garbage scavenge/divination/stack consumption and separate BurnGenerateObjectInCell behavior. No changed inventory, rummage, fire, filth-cleaning, adjacency or animation system.',
    states=states,primary=states[-1]['primary'],detail=states[-1]['detail'],coverage=states[-1]['coverage'],detail_weight=states[-1]['detail_weight'],
    native_activation=False,native_acceptance='Pending full-set generation and real exact-key/variant-selection/visibility/palette/background/stack/rummage-consumption/burning-object behavior acceptance. Authoring only.')
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(method=ref(HERE/'register-garbage.py'),generated_material_selection=ref(HERE/'material-selection.json'),fixed_geometry='Each registered master alpha exactly equals its selected editable construction. All5states use the same512x768source-cell frame and256x256recipient mapping; no independent bounds fitting.',
    surface='Only bounded neutral generated grain changes inside authored glass/paper/metal/wire ownership; original contour/ink/highlights remain. All material roles share source primary K, not separate native colours.',
    detail='All detail images/weights/coverage empty; authored dual-color mask is visible R0 with exact registered coverage.',new_imagegen_calls=1,second_isolation_call=False,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for label,group in [('neutral',neutral),('native-K',native)]:
    plate=Image.new('RGB',(1400,520),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'GARBAGE / '+label+' / all4native choices + distinct declared fallback',font=font,fill='#e3cf43')
    for i,(ident,im) in enumerate(group.items()):
        im=im.resize((224,336),Image.Resampling.LANCZOS);xx=25+i*275;plate.paste(im,(xx,55),im);d.text((xx,420),ident.upper(),font=font,fill='#e3cf43')
    d.text((18,475),'Same source-cell layout; native selection/behavior unchanged. No native acceptance.',font=font,fill='#e5e8d8');plate.save(OUT/f'{label}-family.png')
plate=Image.new('RGB',(1400,650),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),'GARBAGE / original K on native k background, then new K art at24x36 and48x72',font=font,fill='#e3cf43')
source=read(HERE/'native-state-index.json')['states']
for i,(ident,im) in enumerate(native.items()):
    xx=25+i*275;mask=np.array(Image.open(source[i]['private_mask']['path']).convert('RGBA'));original=Image.fromarray(np.dstack([np.broadcast_to(fg,mask[:,:,:3].shape),mask[:,:,3]]))
    for jj,tile in enumerate([original,im]):
        canvas=Image.new('RGBA',(96,144),(*bg,255));small=tile.resize((24,36),Image.Resampling.LANCZOS);canvas.alpha_composite(small,(8,10));large=small.resize((48,72),Image.Resampling.NEAREST);canvas.alpha_composite(large,(40,55));plate.paste(canvas.convert('RGB'),(xx,70+jj*190));d.text((xx,235+jj*190),'SOURCE' if jj==0 else 'REGISTERED',font=font,fill='#e3cf43')
    d.text((xx,490),ident.upper(),font=font,fill='#e3cf43')
for i,line in enumerate(['Native primary K=#155352; background k=#0f3b3a. Texture shading varies luminance without adding a new colour role.',
    'All4RandomTile choices and fallback inspected. Gray bases, empty detail masks, transparent gaps and source mapping retained.',
    'Authoring comparison only. No runtime renderer, native selection, scavenge, burning or visibility test was performed.']):d.text((18,550+i*30),line,font=font,fill='#e5e8d8')
plate.save(OUT/'game-scale-source-comparison.png')
print('Registered five source-layout garbage textures with one primary K role and restrained generated surface grain; final visual review pending.')
