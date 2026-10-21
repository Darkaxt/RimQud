"""Register one normal animal geometry with neutral colour planes and stable swim pivot."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,math
import numpy as np
from scipy.ndimage import gaussian_filter,binary_erosion
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def save(p,a):Image.fromarray(a).save(p)
def rgba(p):return np.array(Image.open(p).convert('RGBA'))
assert not (OUT/'model.json').exists();controls=read(HERE/'turnaround-controls.json');packet=read(HERE/'source-packet.json');raw=Image.open(HERE/'composed-refined-raw.png').convert('RGBA');w,h=raw.size
box=[round(w*.128),round(h*.50),round(w*.144),round(h*.55)];spec=raw.crop(box);a=np.array(spec);assert a[:,:,3].min()>=250 and a[:,:,:3].min()>100;spec.save(HERE/'selected-south-skin.png');g=a[:,:,:3].astype(float).mean(2);residue=np.clip((g-gaussian_filter(g,2))*.20,-3,3)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1300,600),'#142823');d=ImageDraw.Draw(plate);small=raw.copy();small.thumbnail((800,450));plate.paste(small,(20,80),small);d.text((20,18),'ACTUAL COMPOSED REFINEMENT / SOUTH skin selected; NORTH geometry rejected',font=font,fill='#e3cf43');sample=spec.resize((400,350),Image.Resampling.NEAREST);plate.paste(sample,(870,90),sample);d.text((870,470),'Neutral residual only, +/-3',font=font,fill='#e3cf43');scale=small.width/raw.width;d.rectangle(tuple(round(v*scale+(20 if i%2==0 else 80)) for i,v in enumerate(box)),outline='#e3cf43',width=2);plate.save(HERE/'material-selection-review.png')
write(HERE/'material-selection.json',dict(source=ref(HERE/'composed-refined-raw.png'),selected_south_skin=dict(box=box,specimen=ref(HERE/'selected-south-skin.png'),alpha_min=int(a[:,:,3].min())),rejected='Initial E fin sample crossed dark ink; not used. Entire N anatomical proposal/extra fin-like mark excluded. No generated contour, alpha, changed proportions, new flecks or fin geometry adopted.',transfer='Gray high-pass specimen residual(Sigma2)*.20clamped+/-3 through eroded canonical primary skin only. Canonical fin shading/rays, body/head/barbels, exact six flecks, curl and alpha remain fixed. No second isolation; two actual generative calls retained.'))
manual=rgba(ROOT/controls['views']['south']['constructed']['path']);lum=manual[:,:,:3].astype(float).mean(2);ba=rgba(ROOT/controls['views']['south']['ownership']['body']['path'])[:,:,3].astype(float)/255;fa=rgba(ROOT/controls['views']['south']['ownership']['fins']['path'])[:,:,3].astype(float)/255;la=rgba(ROOT/controls['views']['south']['ownership']['flecks']['path'])[:,:,3].astype(float)/255
coverage=manual[:,:,3].astype(float)/255;dpre=la+fa*(1-ba)*(1-la);weight=np.divide(dpre,coverage,out=np.zeros_like(dpre),where=coverage>0);weight=np.clip(weight,0,1)
own=binary_erosion((ba==1)&(la==0)&(lum>150)&(lum<240),iterations=4);tiled=np.tile(residue,(math.ceil(768/residue.shape[0]),math.ceil(768/residue.shape[1])))[:768,:768];lum[own]+=tiled[own];gray=np.uint8(np.clip(np.rint(lum),0,255));master=np.dstack([gray,gray,gray,manual[:,:,3]]);master[master[:,:,3]==0,:3]=0
save(OUT/'south-surface-ownership.png',np.uint8(own)*255)
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];fg=np.frombuffer(bytes.fromhex(palette['m']),dtype=np.uint8).astype(float);de=np.frombuffer(bytes.fromhex(palette['C']),dtype=np.uint8).astype(float)
def tint(im,color):
    q=im.copy();q[:,:,:3]=np.uint8(np.rint(q[:,:,:3].astype(float)/255*color));q[q[:,:,3]==0,:3]=0;return q
model=dict(family='glowfish',entry='BODY-GLOWFISH',species='catfish',canvas=[768,768],contact=[384,384],contact_kind='fixed trunk/swim pivot, not a foot-contact point',world_canvas=[1.2,1.2],source=ref(HERE/'source-packet.json'),front=ref(HERE/'front-controls-patched.json'),construction=ref(HERE/'turnaround-controls.json'),
    actual_side_back=ref(HERE/'side-back-receipt.json'),actual_composed_refinement=ref(HERE/'composed-refinement-receipt.json'),structural_review=ref(HERE/'composed-structural-review.json'),material_selection=ref(HERE/'material-selection.json'),views={},channels={},
    palette=dict(primary='m',detail='C',primary_rgb='b154cf',detail_rgb='77bfcf',policy='Every production texture equal-RGB gray; no fixed-colour pixels. Independent neutral P/D alpha-over planes reproduce one object coverage. Native fish tint is applied at render time; palette-off shows gray everywhere.'),
    baseline='One normal catfish head/face, one dorsal fin, paired lateral fins, one tail fin, intrinsic barbels/gills. Native Gills/DarkVision/LightSource retained as behavior. No added mutation appendages, clothing, handheld default Bite or demographic changes.',
    rendering='Single whole animal graphic in every facing, drawn via two colour layers sharing exact geometry/frame/pivot/animation transform. Mechanical Head/Fin slots are metadata, not new articulated renderer nodes. S/E/N use actual fish-pawn swimming-plane cardinal convention. West mirrors E for ordinary symmetric anatomy/pose.',
    size_provenance='Shared1.2x1.2worldcanvas authored for this template, not native measured physical dimensions; no facing-specific scale or independent alpha-bounds centering. Visible curl may extend asymmetrically while trunk remains on fixed pivot.',
    natural_equipment='Observed Face default Glowfish_Bite is behavior, no separate item art. No actual worn/held equipment to fit on base.',native_activation=False,native_acceptance='Pending all-generation gate, then native whole-body facing/pivot/palette-off/m-C tint/lighting/water visibility/hurt/lifecycle and NPC assembly review. No game/harness validation during generation.')
neutral_plate=Image.new('RGB',(2304,850),'#142823');native_plate=Image.new('RGB',(2304,850),'#142823');mask_plate=Image.new('RGB',(2304,850),'#142823');plates=[neutral_plate,native_plate,mask_plate]
for j,(facing,k) in enumerate([('south',0),('east',1),('north',2)]):
    im=np.rot90(master,k).copy();wt=np.rot90(weight,k).copy();cov=im[:,:,3].astype(float)/255;top=cov*wt;bottom=np.divide(cov-top,1-top,out=np.zeros_like(cov),where=top<1-1e-12)
    # Exact alpha-over decomposition: top=coverage*detail_weight,
    # bottom=coverage*(1-detail_weight)/(1-top). No double coverage or carved limbs.
    p=im.copy();p[:,:,3]=np.uint8(np.rint(bottom*255));p[p[:,:,3]==0,:3]=0;q=im.copy();q[:,:,3]=np.uint8(np.rint(top*255));q[q[:,:,3]==0,:3]=0
    target=OUT/facing;target.mkdir(exist_ok=True)
    composed=Image.alpha_composite(Image.fromarray(p),Image.fromarray(q));native=Image.alpha_composite(Image.fromarray(tint(p,fg)),Image.fromarray(tint(q,de)))
    for name,data in [('master-neutral.png',im),('primary-neutral.png',p),('detail-neutral.png',q),('coverage.png',im[:,:,3]),('detail-weight.png',np.uint8(np.rint(wt*255))),('neutral-assembly.png',np.array(composed)),('native-m-C.png',np.array(native))]:save(target/name,data)
    items=[]
    for layer,(role,name) in enumerate([('foreground','primary-neutral.png'),('detail','detail-neutral.png')]):
        asset=ref(target/name);items.append(dict(component='body',file='glowfish-'+role+'-'+facing+'.png',public_file=asset['path'],sha256=asset['sha256'],size=[768,768],contact=[384,384],color_role=role,width=1.2,height=1.2,center_x=0,center_z=0,layer=layer,logical_body='whole animal; colour plane only'))
    model['views'][facing]=items;model['channels'][facing]={key:ref(target/name) for key,name in [('master','master-neutral.png'),('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('neutral_assembly','neutral-assembly.png'),('native_preview','native-m-C.png')]}
    for plate,pic in [(neutral_plate,composed),(native_plate,native),(mask_plate,Image.fromarray(np.dstack([np.uint8(70+wt*185)]*3+[im[:,:,3]])))]:plate.paste(pic,(j*768,35),pic)
target=OUT/'west';target.mkdir(exist_ok=True);model['channels']['west']={}
for key,r in model['channels']['east'].items():
    src=ROOT/r['path'];p=target/src.name;Image.open(src).transpose(Image.Transpose.FLIP_LEFT_RIGHT).save(p);model['channels']['west'][key]=ref(p)
model['views']['west']=[]
for item in model['views']['east']:
    item=item.copy();name=Path(item['public_file']).name;asset=ref(target/name);item.update(file=item['file'].replace('-east','-west'),public_file=asset['path'],sha256=asset['sha256']);model['views']['west'].append(item)
for plate,title in zip(plates,['NEUTRAL / palette OFF / SOUTH - EAST - NORTH','NATIVE m body + C fins/flecks / SOUTH - EAST - NORTH','OWNERSHIP / gray primary, white detail / fixed whole-animal body']):
    d=ImageDraw.Draw(plate);d.text((20,12),title,font=font,fill='#e3cf43')
    for j,face in enumerate(['SOUTH','EAST','NORTH']):d.text((j*768+20,815),face+' / same trunk pivot384,384',font=font,fill='#e3cf43')
neutral_plate.save(OUT/'neutral-turnarounds.png');native_plate.save(OUT/'native-m-C-turnarounds.png');mask_plate.save(OUT/'ownership-turnarounds.png')
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(timestamp=datetime.now(timezone.utc).isoformat(),method=ref(HERE/'register-body.py'),canonical=ref(HERE/'turnaround-controls.json'),rejected_proposal_geometry=ref(HERE/'composed-structural-review.json'),
    frame='768square and fixed384,384trunk/swim pivot/world1.2square for all views. S first, E=np.rot90(S,1),N=np.rot90(S,2),W=mirror(E); no per-facing resizing, alpha-bound centering, independently turned head or human foot pivot.',
    geometry='One ordinary whole catfish with source curl. Use exact corrected front-derived silhouettes and fin ownership; generated N extra fin-like mark/shape never enters production. All masks turn with the whole body, not separate animated limbs.',
    material='Only selected opaque S skin high-frequency gray residual, bounded+/-3 through eroded canonical skin. Initial fin specimen contaminated by ink and discarded. No generated N pixels, contour/alpha/proportions/extra flecks or baked color.',
    role_math='Detail premultiplied ownership=FleckA+FinA*(1-BodyA)*(1-FleckA); weight=detail_ownership/object_coverage. For layered PNG alpha-over: topA=coverage*weight, bottomA=coverage*(1-weight)/(1-topA). Gray luma common; foreground/detail native tints independent. Quantized authoring assembly checks record edge tolerance.',
    fixed_color='No fixed-color fallback or material chroma. Every production RGB channel equal. Pure native m/C appears only in explicit authoring preview; original source light/water/simulation ownership unchanged.',native_activation=False))
plate=Image.new('RGB',(1400,790),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'GLOWFISH / original m-C source, registered template and intended-size palette OFF/ON',font=font,fill='#e3cf43')
src=rgba(Path(packet['original']['private_mask']['path']));sw=src[:,:,0].astype(float)/255;rgb=np.uint8(np.rint((1-sw[:,:,None])*fg+sw[:,:,None]*de));oi=Image.fromarray(np.dstack([rgb,src[:,:,3]])).resize((160,240),Image.Resampling.NEAREST);plate.paste(oi,(50,70),oi)
for i,face in enumerate(['south','east','north']):
    v=model['channels'][face];ni=Image.open(ROOT/v['neutral_assembly']['path']).convert('RGBA');ci=Image.open(ROOT/v['native_preview']['path']).convert('RGBA');ni.thumbnail((260,260));ci.thumbnail((260,260));xx=300+i*350;plate.paste(ni,(xx,70),ni);plate.paste(ci,(xx,355),ci);d.text((xx,635),face+' / OFF above, ON below',font=font,fill='#e3cf43')
for j,size in enumerate([32,48,64,96]):
    im=Image.open(ROOT/model['channels']['east']['native_preview']['path']).convert('RGBA').resize((size,size),Image.Resampling.LANCZOS);xx=60+j*250;plate.paste(im,(xx,665),im);d.text((xx,765),str(size)+'px full square',font=font,fill='#e5e8d8')
plate.save(OUT/'source-palette-scale.png')
print('Registered normal whole catfish with fixed four facings, neutral layered P/D planes, common pivot and native m/C previews.')
