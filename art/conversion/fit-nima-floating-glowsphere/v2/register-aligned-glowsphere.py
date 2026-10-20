"""Register neutral opal, independent color region and source-inspired optional halo."""
from pathlib import Path
import hashlib,io,json,sys
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';SIZE=(512,1024);FONT=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,c):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));return Image.fromarray(a)
SOURCE=HERE.parent/'v1'
packet=json.loads((HERE/'source-packet.json').read_text());controls=json.loads((HERE/'fit-controls.json').read_text());core=read(HERE/'intact-canonical.png');detail=read(HERE/'detail-canonical.png');halo=read(HERE/'optional-halo-canonical.png')
bm=json.loads((BODY/'model.json').read_text());groups={k:{} for k in ['assembly','palette','nohalo','full','halo','detail']};registered={}
phase_colors=[('0 / Y-C',(255,255,255),(119,191,207)),('50 / y-c',(177,201,195),(64,164,185)),('100 / C-Y',(119,191,207),(255,255,255)),('150 / c-y',(64,164,185),(177,201,195))]
model=dict(item='Floating Glowsphere',blueprint='Floating Glowsphere',family='nima',unmutated_body_family='human-female',slot='Floating Nearby',laterality=0,canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],actual_equipped_binding=packet['observed_bindings'][0]['part'],views={},authoring_effects={},source_state=packet['effective_parts'],view_policy=packet['views'],binding_scope='Actual Nima ordinary Floating Nearby195/0, not a hand or mutation appendage. Unmutated shared body only; individual Nima body/outfit unfinished.',placement='User-directed vertical alignment above one ordinary baseline palm in every view. Native Floating Nearby binding remains195/0; these are display anchors, not exported orbit coordinates.',policy='Complete neutral opal and independent native-color region. Optional halo/light marks remain a separate authoring asset, outside core item alpha.',west_policy='Mirror east for authoring; no asymmetric hardware or markings.',native_acceptance=packet['native_acceptance'])
for f,c in controls.items():
    def place(im):return im.transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC)
    item=place(core);region=place(detail);glow=place(halo);body=read(BODY/f'selected-{f}.png');item.save(HERE/f'intact-item-{f}.png');region.save(HERE/f'item-detail-{f}.png');glow.save(HERE/f'optional-halo-{f}.png')
    nohalo=Image.alpha_composite(body,Image.alpha_composite(item,region));assembly=Image.alpha_composite(Image.alpha_composite(glow,body),Image.alpha_composite(item,region));assembly.save(HERE/f'assembled-{f}.png');nohalo.save(HERE/f'halo-off-{f}.png')
    colored_item=Image.alpha_composite(tint(item,phase_colors[0][1]),tint(region,phase_colors[0][2]));colored=Image.alpha_composite(Image.alpha_composite(tint(glow,phase_colors[0][2]),tint(body,(0,148,3))),colored_item);colored.save(HERE/f'qud-palette-{f}.png')
    for key,im in [('assembly',assembly),('palette',colored),('nohalo',nohalo),('full',Image.alpha_composite(item,region)),('halo',glow),('detail',region)]:groups[key][f]=im
    rows=[]
    for component,stem,role,layer in [('item','intact-item','equipment',.0018),('item-detail','item-detail','equipment-detail',.00181)]:
        p=HERE/f'{stem}-{f}.png';r=ref(p);row=dict(bm['views'][f][0]);row.update(component=component,file=f'nima-floating-glowsphere-v2-{component}-{f}.png',public_file=r['path'],sha256=r['sha256'],equipment_key='floating-glowsphere@Floating Nearby@0',color_role=role,layer=layer);rows.append(row)
    model['views'][f]=rows;model['authoring_effects'][f]=dict(halo=ref(HERE/f'optional-halo-{f}.png'),color_role='equipment-detail',layer=-.0003,registered_native=False,requires='Only bind if final renderer supports the intended translucent effect; native LightSource radius8 remains independent.')
    registered[f]=dict(center=c['center'],inverse_affine=c['inverse_affine'],body=ref(BODY/f'selected-{f}.png'),full_item=ref(HERE/f'intact-item-{f}.png'),detail=ref(HERE/f'item-detail-{f}.png'),body_unchanged=True,body_or_hand_mask='No garment or hand cutout. Separate floating foreground item may overlap torso in projection; no new limb or held-pose claim.')
for images in groups.values():images['west (mirror)']=ImageOps.mirror(images['east'])
def plate(images,name,title):
    out=Image.new('RGB',(1152,665),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=FONT,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,512)),(16+i*284,54));d.text((16+i*284,584),f.upper(),font=FONT,fill='#e3cf43')
    d.text((18,622),'Fixed base; vertical palm alignment. Optional halo separate; native orbit/light/animation acceptance pending.',font=FONT,fill='#e5e8d8');out.save(HERE/name)
for key,name,title in [('assembly','assembly-comparison.png','NIMA / floating opal vertically above one hand / same full sphere'),('palette','independent-palette-comparison.png','NATIVE KEY0 / Nima body g, sphere Y and detail C'),('nohalo','halo-off-comparison.png','CORE ITEM / full opal without optional halo; no body/hand cutout'),('full','full-item-comparison.png','INDEPENDENT ITEM / unchanged spherical surface at authored display anchors'),('halo','optional-halo-comparison.png','OPTIONAL EFFECT / neutral halo and broken light marks, separate from sphere'),('detail','detail-region-comparison.png','DETAIL OWNERSHIP / curved internal region, independent animated native tint')]:plate(groups[key],name,title)
phases=Image.new('RGB',(1152,620),'#142823');draw=ImageDraw.Draw(phases);draw.text((18,14),'SOURCE COLOR KEYS / static previews; no timing or new animation logic',font=FONT,fill='#e3cf43')
for i,(label,primary,secondary) in enumerate(phase_colors):
    merged=Image.alpha_composite(tint(core,primary),tint(detail,secondary));bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(tint(halo,secondary));bg.alpha_composite(merged);phases.paste(bg.crop((192,448,320,576)).resize((256,256)),(16+i*284,65));draw.text((16+i*284,350),label,font=FONT,fill='#e3cf43')
    neutral=Image.alpha_composite(core,detail);bb=Image.new('RGBA',SIZE,'#20382d');bb.alpha_composite(neutral);phases.paste(bb.crop((208,464,304,560)).resize((96,96)),(96+i*284,405))
draw.text((18,552),'Native AnimationLength200 retained; units unresolved. All production RGB remain neutral.',font=FONT,fill='#e5e8d8');phases.save(HERE/'native-color-keys-comparison.png')
small=Image.new('RGB',(560,370),'#142823');draw=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*140+45,20),thumb);thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*140+20,138),thumb);draw.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model);write('registration-decisions.json',dict(shared_source=ref(SOURCE/'intact-canonical.png'),shared_refinement=ref(SOURCE/'refined-red-context.png'),structural_gate=ref(SOURCE/'first-refinement-structural-review.json'),anchor_correction=ref(HERE/'hand-alignment-correction.json'),views=registered,new_imagegen_calls=0,second_isolation_call=False,geometry_and_material_unchanged=True,native_slot_unchanged=True,native_states_owned_by_source=True))
print('Registered same floating opal above palm columns; no redraw, body change or native slot/state change.')
