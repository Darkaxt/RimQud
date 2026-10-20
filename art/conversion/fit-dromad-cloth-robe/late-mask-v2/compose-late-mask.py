"""Continuous cloth through fitting; fixed-body visibility is composed last.

One dressed red-key generation supplies material. The old isolated garment is
not an input. Hidden material is an explicit same-source harmonic continuation,
not recovered anatomy or another generated drawing.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageChops

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
KEY=HERE.parent/'red-key-v1'
AFFINE=HERE.parent/'affine-fit-v1'
REFIT=HERE.parent/'hybrid-fit-v2'
MASK=HERE.parent/'mask-fit-v4'
BODY=ROOT/'art/conversion/body-dromad/v2'
assert not (HERE/'result.json').exists(),'Preserve recorded experiment'
def asset(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def read(p):return Image.open(p).convert('RGBA')
raw=read(KEY/'dressed-red-output.png')
affine=json.loads((AFFINE/'result.json').read_text())
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
record={'scope':'Late body-mask composition experiment, adult dromad robe only','generation_source':asset(KEY/'dressed-red-output.png'),'prior_isolated_garment_used':False,'precut_material_input_used':False,'outside_contour_reference':'Previous stretched alpha contour retained; occluded arm notches completed inside the authored robe envelope','method':'Classify neutral fabric in original dressed image; complete its closed internal red-body regions by harmonic same-fabric continuation. Preserve continuous cloth during global stretch and bounded internal RGB refit. Compose fixed original body above it using a separate per-type visibility mask only at the end.','views':{},'native_acceptance':'Deferred; no game launch'}
assemblies={};off={};fulls={};overlays={};masks={}
for i,f in enumerate(['south','east','north']):
    cell=np.array(raw.crop((i*512,0,(i+1)*512,1024)))
    rgb=cell[:,:,:3].astype(float);a=cell[:,:,3]
    known=(rgb.max(axis=2)-rgb.min(axis=2)<5)&(a>128)
    envelope=ndimage.binary_fill_holes(known)
    unknown=envelope&~known
    gray=rgb.mean(axis=2)
    ids=np.full((1024,512),-1,np.int32);ys,xs=np.where(unknown);n=len(ys);ids[ys,xs]=np.arange(n)
    if n:
        degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[];vv=[]
        for ddy,ddx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny=ys+ddy;nx=xs+ddx;valid=(ny>=0)&(ny<1024)&(nx>=0)&(nx<512)
            q=np.flatnonzero(valid);q=q[envelope[ny[q],nx[q]]]
            degree[q]+=1;neighbor_id=ids[ny[q],nx[q]];u=neighbor_id>=0
            rr.extend(q[u].tolist());cc.extend(neighbor_id[u].tolist());vv.extend([-1.]*int(u.sum()))
            rhs[q[~u]]+=gray[ny[q[~u]],nx[q[~u]]]
        matrix=sparse.coo_matrix((vv,(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree)
        gray[ys,xs]=spsolve(matrix,rhs)
    complete=np.uint8(np.clip(gray,0,255));alpha=np.where(envelope,255,0).astype('uint8')
    material=Image.fromarray(np.dstack([complete,complete,complete,alpha]))
    material.save(HERE/f'continuous-source-{f}.png')
    Image.fromarray(np.uint8(unknown)*255).save(HERE/f'continued-material-region-{f}.png')
    inverse=tuple(affine['views'][f]['red-cut']['inverse_affine'])
    stretched=material.transform((512,1024),Image.Transform.AFFINE,inverse,Image.Resampling.BICUBIC)
    # Keep exactly the globally stretched outside shape already under discussion;
    # its closed internal limb hole no longer removes working cloth pixels.
    accepted=read(AFFINE/f'red-cut-stretched-{f}.png')
    support=ndimage.binary_fill_holes(np.array(accepted.getchannel('A'))>16)
    original_a=np.array(accepted.getchannel('A'))
    outside_a=original_a.copy();outside_a[support&(original_a<16)]=255
    stretched.putalpha(Image.fromarray(outside_a));stretched.save(HERE/f'stretched-full-texture-{f}.png')
    field=np.load(REFIT/f'internal-map-{f}.npz');st=np.array(stretched)
    sampled=np.stack([ndimage.map_coordinates(st[:,:,c].astype(float),[field['y'],field['x']],order=1,mode='nearest') for c in range(3)],axis=-1)
    outer_band=support&(ndimage.distance_transform_edt(support)<=7)
    sampled[outer_band]=st[:,:,:3][outer_band]
    full=Image.fromarray(np.uint8(np.dstack([np.clip(sampled,0,255),outside_a])))
    visibility=Image.open(MASK/f'robe-expose-{f}.png').convert('L')
    visibility.save(HERE/f'body-over-cloth-mask-{f}.png')
    body=read(BODY/f'selected-{f}.png')
    overlay=body.copy();overlay.putalpha(ImageChops.multiply(body.getchannel('A'),visibility));overlay.save(HERE/f'body-overlay-{f}.png')
    # Complete side-connected hand notches as well as closed holes. These are
    # missing cloth hidden by the original body, not physical garment openings.
    # Retain the chosen outside everywhere visible; fill only the authored robe
    # envelope behind fully opaque exposed body pixels.
    cloth=np.array(full)
    envelope_target=np.array(Image.open(MASK/f'robe-envelope-{f}.png').convert('RGBA'))[:,:,3]>128
    body_pixels=np.array(body);vis=np.array(visibility)
    hidden_cloth=envelope_target&(vis==255)&(body_pixels[:,:,3]>250)
    missing=hidden_cloth&(cloth[:,:,3]<255)
    trusted=(cloth[:,:,3]>250)&(cloth[:,:,:3].max(axis=2)-cloth[:,:,:3].min(axis=2)<5)&(cloth[:,:,:3].mean(axis=2)>100)
    nearest=ndimage.distance_transform_edt(~trusted,return_distances=False,return_indices=True)
    cloth[missing,:3]=cloth[nearest[0][missing],nearest[1][missing],:3]
    cloth[missing,3]=255
    full=Image.fromarray(cloth)
    full.save(HERE/f'fitted-full-texture-{f}.png')
    Image.fromarray(np.uint8(missing)*255).save(HERE/f'continued-arm-material-{f}.png')
    mask_off=Image.alpha_composite(body,full)
    # Replace selected original body RGBA once; do not double-composite its
    # partially transparent antialias pixels over another copy of the body.
    effective=Image.fromarray(np.uint8(vis*(body_pixels[:,:,3]>0)))
    composed=Image.composite(body,mask_off,effective)
    composed.save(HERE/f'assembly-{f}.png');mask_off.save(HERE/f'mask-off-{f}.png')
    assemblies[f]=composed;off[f]=mask_off;fulls[f]=full;overlays[f]=overlay
    ma=Image.new('RGBA',(512,1024));ma.paste(Image.merge('RGBA',(visibility,visibility,visibility,Image.new('L',(512,1024),255))));masks[f]=ma
    body_arr=np.array(body);out_arr=np.array(composed);mask_arr=np.array(visibility)
    exposed=(mask_arr>250)&(body_arr[:,:,3]>250)
    # The source texture remains present behind the hand: mask acts only on
    # final display, not on the retained full cloth asset.
    record['views'][f]={'closed_source_material_continued_pixels':n,'side_connected_hidden_material_completed_pixels':int(missing.sum()),'fully_selected_original_body_rgba_changed_pixels':int(np.count_nonzero((mask_arr==255)&(body_arr[:,:,3]>0)&np.any(body_arr!=out_arr,axis=2))),'body':asset(BODY/f'selected-{f}.png'),'source_material':asset(HERE/f'continuous-source-{f}.png'),'global_stretch':asset(HERE/f'stretched-full-texture-{f}.png'),'internal_map':asset(REFIT/f'internal-map-{f}.npz'),'full_texture':asset(HERE/f'fitted-full-texture-{f}.png'),'visibility_mask':asset(HERE/f'body-over-cloth-mask-{f}.png'),'original_body_overlay':asset(HERE/f'body-overlay-{f}.png'),'exposed_interior_changed_pixels':int(np.count_nonzero(exposed&np.any(body_arr[:,:,:3]!=out_arr[:,:,:3],axis=2))),'texture_alpha_changed_by_internal_rgb_fit':0,'added_hidden_material_alpha_pixels':int(np.count_nonzero(np.array(full.getchannel('A'))!=outside_a))}

def plate(name,rows,title):
    out=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(out);d.text((18,12),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(rows.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*288;out.paste(bg.resize((256,512)).convert('RGB'),(x,48));d.line((x+128,48,x+128,559),fill='#e3cf43');d.line((x,523,x+255,523),fill='#70b8b0');d.text((x,578),f.upper(),font=font,fill='#e3cf43')
    d.text((18,618),'Continuous garment retained. Body-region mask controls final depth; same original fixed body.',font=font,fill='#e5e8d8');out.save(HERE/name)
plate('assembly-comparison.png',assemblies,'LATE MASK / full cloth fitted first; original exposed body overlaid last')
plate('full-texture-comparison.png',fulls,'RETAINED FULL TEXTURE / no applied body visibility mask')
plate('body-mask-comparison.png',masks,'BODY VISIBILITY CONTROL / white original body above garment; black cloth')
plate('profile-comparison.png',{'precut: earlier':read(REFIT/'assembly-east.png'),'full cloth: mask off':off['east'],'full cloth: mask on':assemblies['east']},'SAME GENERATION SOURCE / material continuation and final mask shown separately')
record['visual_review']='Requires visual review. Missing cloth is an explicit same-source continuation. No native binding or production acceptance.'
(HERE/'result.json').write_bytes((json.dumps(record,indent=2)+'\n').encode())
print(json.dumps(record['views'],indent=2))
