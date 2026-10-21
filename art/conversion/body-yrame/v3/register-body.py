"""Register selected centauroid art; split head and source-bound tint ownership."""
from pathlib import Path
import json, hashlib, io, sys
import numpy as np
from scipy import ndimage as ndi
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered-v2'
SIZE=(768,1152);CONTACT=(384,1050)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert not OUT.exists();OUT.mkdir()
raw=Image.open(HERE/'composed-refinement-raw.png').convert('RGBA')
base=read(ROOT/'art/conversion/body-human-female/v2/model.json')
oldhead=np.array(Image.open(ROOT/base['views']['south'][1]['public_file']).convert('RGBA'))[:,:,3]>128
oldw=np.nonzero(oldhead)[1].ptp()+1 if hasattr(np.nonzero(oldhead)[1],'ptp') else int(np.ptp(np.nonzero(oldhead)[1]))+1
rawa=np.array(raw);smain=rawa[:220,:480,3]>128;neww=int(np.ptp(np.nonzero(smain)[1]))+1
unit=(base['views']['south'][0]['height']/1024)*oldw/neww
frame=dict(canvas=list(SIZE),contact=list(CONTACT),width=SIZE[0]*unit/(2/3),height=SIZE[1]*unit,center_x=0,
           center_z=(CONTACT[1]-SIZE[1]/2)*unit,pixel_world_size=unit,
           physical_scale='One common world/pixel scale calibrated to the existing female SOUTH head width, including ears, at alpha>128. Authored family-scale choice, not a recovered native height.',
           source_head_width=oldw,refined_head_width=neww,
           units='width and center_x are Qud cell-width units (2/3 world); height and center_z are world units. No per-facing rescale.')
source_views=dict(south=dict(box=[0,0,480,1024],pivot_x=252,ground_y=983,head_cut=211),
                  east=dict(box=[480,0,1040,1024],pivot_x=785,ground_y=969,head_cut=205),
                  north=dict(box=[1040,0,1536,1024],pivot_x=1288,ground_y=969,head_cut=210))
lower_paths={
 'south':'M0 500 L100 500 Q135 460 160 447 Q180 438 183 420 Q210 454 252 457 Q292 454 317 420 Q330 444 354 456 Q390 475 400 500 L480 500 L480 1024 H0 Z',
 'east':'M0 445 L320 445 Q350 441 372 415 Q386 440 408 451 Q435 468 474 475 Q500 485 560 510 L560 1024 H0 Z',
 'north':'M0 490 L110 490 Q145 445 174 425 Q205 442 248 445 Q292 442 322 425 Q355 450 385 490 L496 490 L496 1024 H0 Z'}
left_arm='M135 280 L180 290 L159 370 L118 451 L104 484 L105 508 L90 534 L61 534 L45 513 L48 488 L66 472 L95 413 L113 357 Z'
arm_overrides={
 'south':'<path d="'+left_arm+'"/><g transform="translate(500 0) scale(-1 1)"><path d="'+left_arm+'"/></g><circle cx="76" cy="507" r="30"/><circle cx="421" cy="507" r="30"/>',
 'east':'<path d="M376 250 L403 250 L438 350 L444 420 L467 480 L469 507 L454 531 L429 521 L424 496 L404 430 L384 350 Z"/><circle cx="454" cy="502" r="31"/>',
 'north':'<path d="'+left_arm+'"/><g transform="translate(496 0) scale(-1 1)"><path d="'+left_arm+'"/></g><circle cx="77" cy="507" r="32"/><circle cx="417" cy="507" r="32"/>'}
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette']
colors={k:np.frombuffer(bytes.fromhex(palette[k]),dtype=np.uint8) for k in ['w','B']}
groups={k:{} for k in ['neutral','native','body-foreground','body-detail','head','detail-weight']};views={};checks={}
def translate(im,x,y):
 out=Image.new('RGBA',SIZE);out.paste(im,(int(x),int(y)));return out
def to_rgba(gray,alpha):
 a=np.zeros((*gray.shape,4),dtype=np.uint8);a[:,:,:3]=gray[:,:,None];a[:,:,3]=np.uint8(np.clip(np.round(alpha*255),0,255));a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
for f,layout in source_views.items():
 crop=raw.crop(layout['box']);a=np.array(crop)
 # Drop stray low-alpha background noise, keeping the original saved antialias
 # around the single connected actual figure. No silhouette redraw or AI isolation.
 labels,n=ndi.label(a[:,:,3]>128);counts=np.bincount(labels.ravel());counts[0]=0;main=labels==counts.argmax()
 support=ndi.distance_transform_edt(~main)<=3
 removed=int(((a[:,:,3]>0)&~support).sum());a[~support]=0
 gray=np.uint8(np.round(a[:,:,:3].astype(float).mean(2)));a[:,:,:3]=gray[:,:,None];a[a[:,:,3]==0,:3]=0
 cleaned=Image.fromarray(a);dx=CONTACT[0]-(layout['pivot_x']-layout['box'][0]);dy=CONTACT[1]-layout['ground_y']
 master=translate(cleaned,dx,dy);master.save(OUT/f'neutral-{f}.png')
 svg=('<svg xmlns="http://www.w3.org/2000/svg" width="'+str(crop.width)+'" height="1024">'
      '<rect width="100%" height="100%" fill="black"/><path d="'+lower_paths[f]+'" fill="white"/>'
      '<g fill="black">'+arm_overrides[f]+'</g></svg>')
 (HERE/f'lower-body-ownership-{f}.svg').write_text(svg,encoding='utf-8')
 # resvg antialiases just the ownership curve, leaving art RGB and contour intact.
 mask=Image.open(io.BytesIO(svg_to_bytes(svg_string=svg))).convert('RGBA')
 m=np.array(translate(mask,dx,dy))[:,:,0]/255
 ar=np.array(master);A=ar[:,:,3].astype(float)/255;g=ar[:,:,:3].mean(2).astype(np.uint8)
 yy=np.indices(A.shape)[0];headsel=yy<(layout['head_cut']+dy)
 HA=A*headsel;BA=A*(~headsel);DA=BA*m
 FA=np.divide(BA*(1-m),1-DA,out=np.zeros_like(BA),where=(1-DA)>0)
 parts={'body-foreground':to_rgba(g,FA),'body-detail':to_rgba(g,DA),'head':to_rgba(g,HA)}
 rows=[]
 for name,im in parts.items():
  path=OUT/f'{name}-{f}.png';im.save(path)
  rows.append(dict(component='head' if name=='head' else 'body',color_role='detail' if name=='body-detail' else 'foreground',
      file=path.name,public_file=path.relative_to(ROOT).as_posix(),sha256=ref(path)['sha256'],size=list(SIZE),contact=list(CONTACT),
      width=frame['width'],height=frame['height'],center_x=0,center_z=frame['center_z'],
      layer={'body-foreground':0,'body-detail':.0001,'head':.001}[name],native_part=288 if name=='head' else 287,
      mutation_anatomy='Remodeled lower trunk and four legs are carried by logical body art; no independent render bones.' if name!='head' else 'Head288; Horns575 remain separate equipment.'))
  groups[name][f]=im
 weight=Image.new('RGBA',SIZE,'white');weight.putalpha(Image.fromarray(np.uint8(np.round(m*A*255))));weight.save(OUT/f'detail-weight-{f}.png');groups['detail-weight'][f]=weight
 neutral=Image.new('RGBA',SIZE);native=Image.new('RGBA',SIZE)
 for name in ['body-foreground','body-detail','head']:
  im=parts[name];neutral.alpha_composite(im);data=np.array(im);c=colors['B' if name=='body-detail' else 'w']
  data[:,:,:3]=np.uint8(np.round(data[:,:,:3].astype(float)*c/255));data[data[:,:,3]==0,:3]=0;native.alpha_composite(Image.fromarray(data))
 groups['neutral'][f]=neutral;groups['native'][f]=native;native.save(OUT/f'native-{f}.png')
 expected=np.array(master).astype(int);actual=np.array(neutral).astype(int);vis=expected[:,:,3]>0
 alphaerr=int(np.abs(expected[:,:,3]-actual[:,:,3]).max());rgberr=int(np.abs(expected[:,:,:3][vis]-actual[:,:,:3][vis]).max())
 assert alphaerr<=1 and rgberr<=1,(f,alphaerr,rgberr)
 checks[f]=dict(alpha_recomposition_error=alphaerr,rgb_recomposition_error=rgberr,discarded_remote_low_alpha_pixels=removed,
     source_crop=layout['box'],translation=[dx,dy],source_pivot=layout['pivot_x'],source_ground=layout['ground_y'],
     head_cut_source_y=layout['head_cut'],geometry='Actual refined figure pixels and contour retained after background-noise cleanup; no independent body/head/foot rescale.')
 views[f]=rows
# Mirror only the bare symmetric anatomy; source fore/hind slot identity is retained.
views['west']=[]
for r in views['east']:
 p=ROOT/r['public_file'];name=p.name.replace('-east','-west');out=OUT/name
 ImageOps.mirror(Image.open(p).convert('RGBA')).save(out)
 views['west'].append(dict(r,file=name,public_file=out.relative_to(ROOT).as_posix(),sha256=ref(out)['sha256'],mirrored_from_east=True))
for key,group in groups.items():
 group['west']=ImageOps.mirror(group['east']);group['west'].save(OUT/f'{key}-west.png')
foot_anchors=dict(south=dict(fore=[[192,970],[303,970]],hind=[[148,938],[354,938]],visible='Four distinct hooves.'),
 east=dict(fore=[[945,956],[922,949]],hind=[[592,950],[673,937]],visible='Near and far hind legs visible; far fore leg partly occluded by near fore leg.'),
 north=dict(fore=[],hind=[[1230,954],[1350,954]],visible='Hind pair occludes forefeet in the selected straight back view; four legs remain present in anatomy.'))
model=dict(entry='BODY-YRAME',kind='fixed_named_centauroid_mutation_variant',source=ref(HERE/'source-packet.json'),
    baseline_model=ref(ROOT/'art/conversion/body-human-female/v2/model.json'),baseline_policy='Ordinary human female source unchanged. This named mutation variant replaces lower-body geometry, rather than adding a pair to a visible biped.',
    views=views,registration=frame,source_views=source_views,
    palette_roles=dict(foreground='w: upper body, arms/hands and head',detail='B: lower trunk/legs and fleece; neutral albedo remains grayscale.',
                       interpretation='Original visible palette role applied parametrically; not permanent baked biological blue.'),
    source_anatomy=read(HERE/'source-packet.json')['source_facts'],
    foot_attachment_map=dict(coordinates='Untranslated source-sheet authoring landmarks, not native joint locations or articulated bones.',
       view_landmarks=foot_anchors,fore_part=297,hind_part=298,boots_instance=580,boots_binding='Only fore Feet297/16; no boots on hind Feet298/64. Refit required; no equipment is present here.'),
    body_geometry='Upright human-family upper torso joins a horizontal compact sheep-like lower trunk. Four animal legs attach below its fore and hind regions. No tail, animal head or horns are baked into this body.',
    authoring_uncertainty='Compact fleece and cloven hooves are the selected visual interpretation, not a native sheep species declaration.',
    west_policy='Mirrored bare east anatomy only. Equipment handedness/slot binding remains independent.',
    no_new_nodes='Two tint planes share one logical body transform; head retains the existing separate head role. No four-leg animation or mutation framework implemented.',
    native_activation=False,native_acceptance='Pending all-entry generation gate and final runtime direction/tint/equipment/visibility/hurt/look/save review.')
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(frame=frame,views=checks,
    production_albedo='All RGB neutral grayscale; RGB at alpha0 cleared. Saved alpha is real, no gray halo on actual composite.',
    color_ownership='Editable curves follow the lower-body transition; arm/hand overrides keep smooth human skin in w. Separate alpha-over planes reconstruct the same neutral figure to <=1 channel value.',
    head='Head and upper neck separated inside the neck strip; body/head recomposition verified at saved-pixel level.',
    physical_mapping='Common physical scale and per-facing stance pivots; torso naturally shifts forward in profile while the lower-body footprint pivot stays fixed.',native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for key,group in groups.items():
 plate=Image.new('RGB',(1450,760),'#142823');d=ImageDraw.Draw(plate)
 d.text((18,15),'YRAME / compact centauroid / '+key+' / authoring candidate',font=font,fill='#e3cf43')
 for i,(f,im) in enumerate(group.items()):
  x=14+i*360;small=im.resize((320,480),Image.Resampling.LANCZOS);plate.paste(small,(x,55),small)
  cx=x+CONTACT[0]*320/SIZE[0];gy=55+CONTACT[1]*480/SIZE[1]
  d.line((cx,55,cx,535),fill='#9d954a');d.line((x,gy,x+320,gy),fill='#79aaa0');d.text((x,560),f.upper(),font=font,fill='#e3cf43')
  tiny=im.resize((64,96),Image.Resampling.LANCZOS);plate.paste(tiny,(x+128,605),tiny)
 d.text((18,725),'Bare model only. Four legs; source fore/hind groups retained. Native acceptance pending.',font=font,fill='#e5e8d8')
 plate.save(OUT/f'{key}-comparison.png')
print('Registered common768x1152 frame, real alpha, bare body/head, w/B tint planes and four authoring views. Visual review pending.')
