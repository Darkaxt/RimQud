"""Fixed global stretch + bounded internal cuff refit, one source throughout.

All material comes from the recent red-key output; no older isolated robe.
The stretched outside contour and a narrow outside ink band remain exact.
Red-removed internal material is extended from this same garment's fabric.
"""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont,ImageChops,ImageOps

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
STRETCH=HERE.parent/'affine-fit-v1'
KEY=HERE.parent/'red-key-v1'
MASK=HERE.parent/'mask-fit-v4'
BODY=ROOT/'art/conversion/body-dromad/v2'
assert not (HERE/'result.json').exists(),'Preserve recorded attempts'
def asset(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def load(p):return Image.open(p).convert('RGBA')
def components(mask,min_area=200):
    labels,n=ndimage.label(mask);found=[]
    for i,sl in enumerate(ndimage.find_objects(labels),1):
        if sl is None:continue
        area=int(np.count_nonzero(labels[sl]==i));box=[sl[1].start,sl[0].start,sl[1].stop,sl[0].stop]
        if area>=min_area:found.append((i,box,area))
    return labels,found
def smooth(v):v=np.clip(v,0,1);return v*v*(3-2*v)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
params=json.loads((STRETCH/'result.json').read_text())
key=Image.open(KEY/'keyed-body-mask.png').convert('L')
record={'scope':'One-source global stretch plus bounded cuff refit experiment','source':asset(KEY/'extracted-visible-clothing-sheet.png'),'method':'Retain global red-cut stretch. Fill closed internal cut holes from neutral fabric in that same source. Apply smoothly bounded inverse cuff affine fields, zero at outer ink band; numerically limit displacement to keep visible material orientation positive. Apply target body exposure mask afterward. Body never warps.','older_isolated_source_used':False,'views':{},'native_acceptance':'Not attempted; full-set gate unchanged'}
assemblies={};baselines={}
for i,f in enumerate(['south','east','north']):
    im=load(STRETCH/f'red-cut-stretched-{f}.png');raw=np.array(im);body=load(BODY/f'selected-{f}.png')
    a=raw[:,:,3];support=ndimage.binary_fill_holes(a>16)
    holes=support&(a<16)
    # Neutral fabric, not old garment linework or generated red skin, supplies
    # the pixels removed with the original body. This is an explicit repair.
    # Binary red cutoff left mixed red/cloth antialias pixels. They are not
    # garment pigment: neutral cloth must not carry the red mannequin key.
    channels=raw[:,:,:3].astype(float)
    contaminated=(channels[:,:,0]-channels[:,:,1]>4)&(channels[:,:,0]-channels[:,:,2]>4)&support
    protected_outer=support&(ndimage.distance_transform_edt(support)<=7)
    repair=(holes|contaminated)&~protected_outer
    fabric=(a>200)&(channels.mean(axis=2)>100)&(channels.max(axis=2)-channels.min(axis=2)<4)
    nearest=ndimage.distance_transform_edt(~fabric,return_distances=False,return_indices=True)
    material=raw[:,:,:3].copy();material[repair]=raw[nearest[0][repair],nearest[1][repair],:3]
    neutral=material.astype(float).mean(axis=2).astype('uint8');material=np.repeat(neutral[:,:,None],3,axis=2)
    canonical_a=a.copy();canonical_a[holes]=255
    internal_source=np.dstack([material,canonical_a]).astype('uint8')
    Image.fromarray(internal_source).save(HERE/f'internal-hole-repair-{f}.png')
    Image.fromarray(np.uint8(repair)*255).save(HERE/f'repaired-region-{f}.png')
    # Exposed arm components are the only local fitting constraints.
    source_key=key.crop((i*512,0,(i+1)*512,1024))
    source_lab,source_parts=components(np.array(source_key)>100)
    arms=[p for p in source_parts if 550<p[1][1]<800 and p[1][3]<850]
    source_arm_mask=Image.fromarray(np.uint8(np.isin(source_lab,[p[0] for p in arms]))*255)
    inverse=params['views'][f]['red-cut']['inverse_affine']
    stretched_key=source_arm_mask.transform((512,1024),Image.Transform.AFFINE,tuple(inverse),Image.Resampling.NEAREST)
    sl,source_parts=components(np.array(stretched_key)>100)
    body_a=np.array(load(BODY/f'body-{f}.png').getchannel('A'))
    arm_paint=np.array(Image.open(HERE.parent/'v5'/f'body-over-clothing-{f}.png').convert('L'))
    target_arm=(arm_paint.astype(float)*body_a/255)>100
    tl,target_parts=components(target_arm)
    source_parts.sort(key=lambda p:(p[1][0]+p[1][2])/2);target_parts.sort(key=lambda p:(p[1][0]+p[1][2])/2)
    assert len(source_parts)==len(target_parts),(f,source_parts,target_parts)
    gy,gx=np.mgrid[0:1024,0:512];dx=np.zeros((1024,512));dy=np.zeros_like(dx);total=np.zeros_like(dx)
    distance_inside=ndimage.distance_transform_edt(support)
    lock=smooth((distance_inside-7)/36)
    local=[]
    for (sid,sbox,_),(tid,tbox,_) in zip(source_parts,target_parts):
        sw,sh=sbox[2]-sbox[0],sbox[3]-sbox[1];tw,th=tbox[2]-tbox[0],tbox[3]-tbox[1]
        sx=sw/tw;sy=sh/th;tx=sbox[0]-sx*tbox[0];ty=sbox[1]-sy*tbox[1]
        dist=ndimage.distance_transform_edt(tl!=tid)
        weight=(1-smooth((dist-12)/90))*lock
        ddx=sx*gx+tx-gx;ddy=sy*gy+ty-gy
        dx+=weight*ddx;dy+=weight*ddy;total+=weight
        local.append({'source_arm_bounds':sbox,'target_arm_bounds':tbox,'inverse_affine':[sx,0,tx,0,sy,ty]})
    norm=np.maximum(1,total);dx/=norm;dy/=norm
    dxd_y,dxd_x=np.gradient(dx);dyd_y,dyd_x=np.gradient(dy)
    visible_domain=support&(np.array(Image.open(MASK/f'robe-expose-{f}.png').convert('L'))<128)
    def determinant(t):return (1+t*dxd_x)*(1+t*dyd_y)-t*t*dxd_y*dyd_x
    # Bound the actual local inverse field rather than letting it fold. The
    # fixed numerical search is a geometry solve, not a retry/timing mechanism.
    strength=1.
    if np.min(determinant(1)[visible_domain])<.2:
        low,high=0.,1.
        for _ in range(24):
            mid=(low+high)/2
            if np.min(determinant(mid)[visible_domain])>=.2:low=mid
            else:high=mid
        strength=low
    mx=gx+strength*dx;my=gy+strength*dy
    warped=np.stack([ndimage.map_coordinates(material[:,:,c].astype(float),[my,mx],order=1,mode='nearest') for c in range(3)],axis=-1)
    # Exact outside pixels are copied, not reinterpolated.
    outer_band=support&(distance_inside<=7)
    warped[outer_band]=raw[:,:,:3][outer_band]
    # Alpha's outer contour remains fixed; only the original closed internal
    # holes were repaired before drawing the target exposed arms above it.
    intact=Image.fromarray(np.uint8(np.dstack([np.clip(warped,0,255),canonical_a])))
    intact.save(HERE/f'fitted-intact-{f}.png')
    exposure=Image.open(MASK/f'robe-expose-{f}.png').convert('L')
    visible=intact.copy();visible.putalpha(ImageChops.multiply(intact.getchannel('A'),ImageChops.invert(exposure)))
    visible.save(HERE/f'fitted-visible-{f}.png');composed=Image.alpha_composite(body,visible);composed.save(HERE/f'assembly-{f}.png')
    baselines[f]=load(STRETCH/f'red-cut-assembly-{f}.png');assemblies[f]=composed
    outline=np.array(intact)[:,:,:3];ba=np.array(body);ca=np.array(composed);protected=(np.array(exposure)>250)&(ba[:,:,3]>250)
    record['views'][f]={'source_stretch':asset(STRETCH/f'red-cut-stretched-{f}.png'),'source_arm_mask':asset(KEY/'keyed-body-mask.png'),'target_arm_mask':asset(HERE.parent/'v5'/f'body-over-clothing-{f}.png'),'constraints':local,'achieved_displacement_strength':strength,'outer_alpha_changed_pixels':int(np.count_nonzero((np.array(intact)[:,:,3]!=a)&~holes)),'outer_ink_band_changed_pixels':int(np.count_nonzero(outer_band&np.any(outline!=raw[:,:,:3],axis=2))),'exposed_body_interior_changed_pixels':int(np.count_nonzero(protected&np.any(ba[:,:,:3]!=ca[:,:,:3],axis=2))),'minimum_visible_inverse_jacobian':float(np.min(determinant(strength)[visible_domain])),'same_source_internal_fill_pixels':int(holes.sum()),'key_contaminated_pixels_repaired':int(np.count_nonzero(contaminated&repair)),'new_imagegen_call':False}
    np.savez_compressed(HERE/f'internal-map-{f}.npz',x=mx.astype('float32'),y=my.astype('float32'))

def plate(name,rows,title):
    out=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(out);d.text((18,12),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(rows.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*288;out.paste(bg.resize((256,512)).convert('RGB'),(x,48));d.line((x+128,48,x+128,559),fill='#e3cf43');d.line((x,523,x+255,523),fill='#70b8b0');d.text((x,578),f.upper(),font=font,fill='#e3cf43')
    d.text((18,618),'One red-cut source throughout. Fixed stretched outside and body; bounded internal cuff adjustment.',font=font,fill='#e5e8d8');out.save(HERE/name)
plate('assembly-comparison.png',assemblies,'HYBRID / fixed stretched outside; cuff refit and key-edge cleanup inside')
plate('same-source-profile-comparison.png',{'same source: direct':load(KEY/'direct-original-body-recomposition.png').crop((512,0,1024,1024)),'same source: stretch':baselines['east'],'same source: hybrid':assemblies['east']},'CONTROLLED COMPARISON / identical red-key clothing pixels as source')
close=Image.new('RGB',(1000,760),'#142823');d=ImageDraw.Draw(close)
for i,(label,im) in enumerate([('SAME SOURCE / STRETCH ONLY',baselines['east']),('SAME SOURCE / INTERNAL REFIT',assemblies['east'])]):
    bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);crop=bg.crop((165,590,330,835)).resize((440,653));close.paste(crop.convert('RGB'),(20+i*500,55));d.text((20+i*500,18),label,font=font,fill='#e3cf43')
close.save(HERE/'cuff-before-after-comparison.png')
record['visual_review']='Pending actual inspection; not selected production art'
(HERE/'result.json').write_bytes((json.dumps(record,indent=2)+'\n').encode())
print(json.dumps(record['views'],indent=2))
