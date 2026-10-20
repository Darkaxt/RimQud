"""One deterministic adult-dromad garment-mask fitting experiment.

Four authored type envelopes/exposure rules; only the robe is fitted here.
Source garment pixels come from the actual red-key result. The retained full
robe supplies material absent behind the generated body. Body images never warp.
"""
from pathlib import Path
import json, hashlib, io
import numpy as np
from scipy import ndimage
from scipy.spatial import Delaunay
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageOps
import resvg_py

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-dromad/v2'
SOURCE=HERE.parent/'red-key-v1'
FULL=HERE.parent/'v1/registered'
ARMS=HERE.parent/'v5'
assert not (HERE/'fit-result.json').exists(), 'Preserve recorded experiments'
SIZE=(512,1024)
FACES=['south','east','north']
TYPES=['t-shirt','trousers','skirt','robe']

def asset(p):return {'path':p.relative_to(ROOT).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
def js(name,v):(HERE/name).write_bytes((json.dumps(v,indent=2)+'\n').encode())
def load(p):return Image.open(p).convert('RGBA')
def svgmask(name,path):
    p=HERE/(name+'.svg')
    p.write_bytes(('<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><path fill="white" d="'+path+'"/></svg>').encode())
    a=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))).getchannel('A')
    a.save(HERE/(name+'.png'));return np.array(a)
def save_rgba(name,arr):Image.fromarray(np.uint8(np.clip(arr,0,255))).save(HERE/name)

# Authored once against this unchanged race/body frame. Broad envelopes are
# garment cut/drape choices, not extra anatomy or inferred native equipment slots.
upper_front='M199 472 Q163 477 150 524 Q145 565 124 590 Q92 625 82 700 L128 733 L157 689 '
upper_back='M256 477 Q180 474 157 531 Q144 568 124 590 Q92 625 82 700 L128 733 L157 689 '
right_front='L355 689 L384 733 L431 700 Q416 625 384 590 Q359 566 350 531 Q341 491 314 508 L314 620 Q257 655 195 620Z'
right_back='L355 689 L384 733 L431 700 Q416 625 384 590 Q363 569 352 531 Q334 477 256 477Z'
side_top='M280 626 Q277 553 253 495 Q242 463 214 475 Q179 488 174 529 Q170 568 152 596 Q121 644 128 708 Q134 768 164 816 '
side_end='L377 815 Q415 754 399 696 Q388 661 370 640Z'
paths={
 'robe':{
  'south':upper_front+'L135 891 Q256 916 378 891 '+right_front,
  'north':upper_back+'L135 891 Q256 916 378 891 '+right_back,
  'east':side_top+'L153 891 Q271 915 392 890 '+side_end,
 },
 't-shirt':{
  'south':upper_front+'L147 799 Q256 821 365 799 '+right_front,
  'north':upper_back+'L147 799 Q256 821 365 799 '+right_back,
  'east':side_top.replace('Q134 768 164 816','Q133 758 151 788')+'Q274 817 390 789 Q412 745 399 696 Q388 661 370 640Z',
 },
 'skirt':{
  'south':'M145 754 Q256 781 369 754 L397 891 Q256 916 116 891Z',
  'north':'M145 754 Q256 781 369 754 L397 891 Q256 916 116 891Z',
  'east':'M151 758 Q279 781 389 758 L410 890 Q273 915 135 891Z',
 },
 'trousers':{
  'south':'M138 754 Q256 779 376 754 L369 819 L354 910 Q304 930 266 911 L260 843 L248 843 L243 911 Q194 929 139 910 L130 820Z',
  'north':'M138 754 Q256 779 376 754 L369 819 L354 910 Q304 930 266 911 L260 843 L248 843 L243 911 Q194 929 139 910 L130 820Z',
  'east':'M150 758 Q280 780 387 758 L360 834 L335 911 L279 916 L260 876 L250 919 L199 917 L193 850Z',
 },
}
raw=load(SOURCE/'dressed-red-output.png')
extracted=load(SOURCE/'extracted-visible-clothing-sheet.png')
redkey=Image.open(SOURCE/'keyed-body-mask.png').convert('L')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
profiles={'scope':'Adult dromad authored mask proposals; only robe material fitting attempted','body':asset(BODY/'model.json'),'legend':{'green':'required covered body','magenta':'exposed body/protected from this garment','cyan':'garment drape outside required body region','yellow':'fitting landmarks'},'types':{}}
mask_previews={};results={};assemblies={};before={};fitted_images={};key_parts={}

def components(mask,min_area=150):
    lab,n=ndimage.label(mask)
    rows=[]
    for i,sl in enumerate(ndimage.find_objects(lab),1):
        if sl is None:continue
        count=int(np.count_nonzero(lab[sl]==i))
        if count>=min_area:rows.append({'label':i,'area':count,'box':[sl[1].start,sl[0].start,sl[1].stop,sl[0].stop]})
    return lab,rows

for face_index,f in enumerate(FACES):
    body=load(BODY/f'selected-{f}.png');body_part=load(BODY/f'body-{f}.png');head=load(BODY/f'head-{f}.png')
    ba=np.array(body.getchannel('A'));body_a=np.array(body_part.getchannel('A'));ha=np.array(head.getchannel('A'))
    arm_paint=np.array(Image.open(ARMS/f'body-over-clothing-{f}.png').convert('L'))
    exposed_arms=np.uint8(arm_paint.astype(float)*body_a/255)
    feet=np.zeros((1024,512),np.uint8);feet[904:]=ba[904:]
    for typ in TYPES:
        target=svgmask(f'{typ}-envelope-{f}',paths[typ][f])
        if typ in ['robe','t-shirt']:
            protected=np.maximum.reduce([ha,exposed_arms,feet])
            lower=890 if typ=='robe' else 790
            required=(body_a>128)&(protected<128)
            required[:470]=False;required[lower:]=False
        else:
            protected=np.maximum(exposed_arms,feet)
            protected[:750]=ba[:750]
            required=(body_a>128)&(protected<128)
            required[:765]=False;required[890 if typ=='skirt' else 905:]=False
        protected=np.where(protected>=128,255,protected).astype('uint8')
        # Required body coverage is an explicit constraint. Expand only where
        # the authored envelope missed actual protected-free body, not to a bbox.
        added=required&(target<128)
        target=np.maximum(target,np.where(required,body_a,0).astype('uint8'))
        Image.fromarray(target).save(HERE/f'{typ}-target-{f}.png')
        Image.fromarray(protected).save(HERE/f'{typ}-expose-{f}.png')
        Image.fromarray(np.uint8(required)*255).save(HERE/f'{typ}-required-{f}.png')
        colored=np.array(body)
        covered=(target>128)&(protected<128)&(ba>128)
        colored[covered,:3]=(44,188,100);colored[(protected>128)&(ba>128),:3]=(218,91,214)
        outside=(target>128)&(ba<128);colored[outside]=(64,164,185,180)
        mask_previews[(typ,f)]=Image.fromarray(colored)
        profiles['types'].setdefault(typ,{'views':{},'fit_status':'robe experiment' if typ=='robe' else 'mask proposal only'})['views'][f]={'envelope':asset(HERE/f'{typ}-envelope-{f}.svg'),'target':asset(HERE/f'{typ}-target-{f}.png'),'expose':asset(HERE/f'{typ}-expose-{f}.png'),'required':asset(HERE/f'{typ}-required-{f}.png'),'required_body_added_to_envelope_pixels':int(added.sum())}
        if typ!='robe':continue

        source=np.array(extracted.crop((512*face_index,0,512*(face_index+1),1024)))
        source_key=np.array(redkey.crop((512*face_index,0,512*(face_index+1),1024)))
        lab,items=components(source_key>100)
        heads=[r for r in items if r['box'][1]<350]
        arms=[r for r in items if 550<r['box'][1]<800 and r['box'][3]<850]
        assert heads and arms,(f,items)
        head_bottom=max(r['box'][3] for r in heads)
        arm_top=min(r['box'][1] for r in arms);arm_bottom=max(r['box'][3] for r in arms)
        target_arm_lab,target_arm_parts=components(exposed_arms>100)
        assert target_arm_parts
        ty_top=min(r['box'][1] for r in target_arm_parts);ty_bottom=max(r['box'][3] for r in target_arm_parts)
        sy,sx=np.where(source[:,:,3]>128);yy,xx=np.where(target>128)
        target_head_bottom=int(np.where(ha>128)[0].max()+1)
        src_y=np.array([sy.min(),head_bottom,arm_top,arm_bottom,sy.max()],float)
        dst_y=np.array([yy.min(),target_head_bottom,ty_top,ty_bottom,yy.max()],float)
        assert np.all(np.diff(src_y)>0) and np.all(np.diff(dst_y)>0),(f,src_y,dst_y)
        map_y=np.interp(np.arange(1024),dst_y,src_y)
        # Source holes retain their material provenance: never sample red skin.
        full=np.array(load(FULL/f'registered-uncut-{f}.png'))
        fi=ndimage.distance_transform_edt(full[:,:,3]<128,return_distances=False,return_indices=True)
        full_rgb=full[fi[0],fi[1],:3]
        source_valid=source[:,:,3]>128
        si=ndimage.distance_transform_edt(~source_valid,return_distances=False,return_indices=True)
        source_rgb=source[si[0],si[1],:3]
        map_x=np.zeros((1024,512),np.float32);map_ys=np.repeat(map_y[:,None],512,axis=1).astype('float32')
        fallback_x=np.zeros_like(map_x);fallback_y=np.zeros_like(map_x)
        used_arm_rows=0
        fy,fx=np.where(full[:,:,3]>128);source_bounds=(int(sy.min()),int(sy.max()));full_bounds=(int(fy.min()),int(fy.max()))
        for y in range(1024):
            tar=np.flatnonzero(target[y]>128)
            if not len(tar):continue
            syi=int(np.clip(round(map_y[y]),0,1023))
            sr=np.flatnonzero(source_valid[syi])
            if not len(sr):sr=np.flatnonzero(source_valid[int(si[0,syi,256])])
            if not len(sr):continue
            tx=[float(tar[0]),float(tar[-1])];ss=[float(sr[0]),float(sr[-1])]
            # Internal cuff/forearm boundaries are not inferred from the outer
            # garment silhouette: use the named exposed-arm masks on both bodies.
            source_arms=np.flatnonzero(np.isin(lab[syi],[r['label'] for r in arms]))
            target_arms=np.flatnonzero(target_arm_lab[y]>0)
            pairs=[]
            if len(source_arms) and len(target_arms):
                for direction in [0,-1]:
                    a=float(target_arms[direction]);b=float(source_arms[direction])
                    if tx[0]+2<a<tx[-1]-2 and ss[0]+2<b<ss[-1]-2:pairs.append((a,b))
            if len(pairs)==2 and pairs[0][0]<pairs[1][0] and pairs[0][1]<pairs[1][1]:
                tx=[tx[0],pairs[0][0],pairs[1][0],tx[1]];ss=[ss[0],pairs[0][1],pairs[1][1],ss[1]];used_arm_rows+=1
            map_x[y]=np.interp(np.arange(512),tx,ss)
            # A separate full-cloth material coordinate map, same scanline
            # normalization, fills only pixels absent after red-body removal.
            fyf=np.interp(map_y[y],source_bounds,full_bounds);fyi=int(np.clip(round(fyf),0,1023))
            fr=np.flatnonzero(full[fyi,:,3]>128)
            if not len(fr):fr=np.array([fx.min(),fx.max()])
            fallback_x[y]=np.interp(np.arange(512),[tar[0],tar[-1]],[fr[0],fr[-1]])
            fallback_y[y]=fyf
        # The first experiment switched rowwise maps at cuffs, producing tears.
        # Here one continuous thin-plate inverse mesh fits semantic landmarks.
        control_rows=set(np.linspace(dst_y[0]+8,dst_y[-1]-4,15).astype(int).tolist())
        control_rows.update(int(v) for v in dst_y[1:-1])
        control_rows.update([int(ty_top+6),int((ty_top+ty_bottom)/2),int(ty_bottom-6)])
        controls={}
        source_envelope=ndimage.binary_fill_holes(source_valid)
        def runs(line):
            where=np.flatnonzero(line)
            if not len(where):return []
            splits=np.split(where,np.flatnonzero(np.diff(where)>1)+1)
            return [(int(v[0]),int(v[-1])) for v in splits if len(v)>2]
        for y in sorted(control_rows):
            syf=float(map_y[y]);syi=int(np.clip(round(syf),0,1023))
            tr=runs(target[y]>128);sr=runs(source_envelope[syi])
            if not tr or not sr:continue
            # Match separate shoulder lobes around the neckline independently.
            # A single left hump is never mapped to both shoulder lobes.
            for t0,t1 in tr:
                s0,s1=min(sr,key=lambda r:abs((r[0]+r[1])/2-(t0+t1)/2))
                controls[(float(t0),float(y))]=(float(s0),syf)
                controls[(float(t1),float(y))]=(float(s1),syf)
            if target[y,256]>128 and protected[y,256]<128 and source_envelope[syi,256]:
                controls[(256.,float(y))]=(256.,syf)
            sa=np.flatnonzero(np.isin(lab[syi],[r['label'] for r in arms]));ta=np.flatnonzero(target_arm_lab[y]>0)
            if len(sa) and len(ta):
                for direction in [0,-1]:controls[(float(ta[direction]),float(y))]=(float(sa[direction]),syf)
        targets=np.array(list(controls));sources=np.array(list(controls.values()))
        mesh=Delaunay(targets)
        gy,gx=np.mgrid[0:1024,0:512];query=np.column_stack([gx.ravel(),gy.ravel()])
        simplex=mesh.find_simplex(query);inside_mesh=simplex>=0;idx=simplex[inside_mesh]
        delta=query[inside_mesh]-mesh.transform[idx,2]
        first=np.einsum('nij,nj->ni',mesh.transform[idx,:2],delta)
        weights=np.column_stack([first,1-first.sum(axis=1)])
        sampled=np.einsum('ni,nij->nj',weights,sources[mesh.simplices[idx]])
        map_x.ravel()[inside_mesh]=sampled[:,0];map_ys.ravel()[inside_mesh]=sampled[:,1]
        js('mesh-controls-'+f+'.json',{'direction':'target to source','method':'continuous piecewise-affine triangular mesh','points':[{'target':list(k),'source':list(v)} for k,v in controls.items()],'triangles':mesh.simplices.tolist()})
        # Fallback material follows the same continuous field, normalized from
        # extracted garment extents to the retained complete source extents.
        fallback_y=np.interp(map_ys,source_bounds,full_bounds).astype('float32')
        source_xmin=float(sx.min());source_xmax=float(sx.max());full_xmin=float(fx.min());full_xmax=float(fx.max())
        fallback_x=np.interp(map_x,[source_xmin,source_xmax],[full_xmin,full_xmax]).astype('float32')
        coords=[map_ys,map_x];fcoords=[fallback_y,fallback_x]
        sample=np.stack([ndimage.map_coordinates(source_rgb[:,:,c].astype(float),coords,order=1,mode='nearest') for c in range(3)],axis=-1)
        support=ndimage.map_coordinates(source[:,:,3].astype(float),coords,order=1,mode='constant')
        fallback=np.stack([ndimage.map_coordinates(full_rgb[:,:,c].astype(float),fcoords,order=1,mode='nearest') for c in range(3)],axis=-1)
        missing=support<128
        sample[missing]=fallback[missing]
        # Keep the material grayscale; original key is never a material sample.
        gray=np.mean(sample,axis=2);rgba=np.stack([gray,gray,gray,target],axis=-1)
        intact=Image.fromarray(np.uint8(np.clip(rgba,0,255)));intact.save(HERE/f'fitted-intact-robe-{f}.png')
        visible=intact.copy();visible.putalpha(ImageChops.multiply(intact.getchannel('A'),Image.fromarray(255-protected)))
        visible.save(HERE/f'fitted-visible-robe-{f}.png')
        composed=Image.alpha_composite(body,visible);composed.save(HERE/f'fitted-assembly-{f}.png')
        previous=Image.alpha_composite(body,Image.fromarray(source));before[f]=previous;assemblies[f]=composed;fitted_images[f]=visible
        material_map=np.zeros((1024,512,4),np.uint8);inside=target>128
        material_map[inside&~missing]=(44,188,100,255);material_map[inside&missing]=(227,159,45,255)
        Image.fromarray(material_map).save(HERE/f'material-provenance-{f}.png')
        # Store the actual inverse deformation; no dependency on a repeated fit.
        np.savez_compressed(HERE/f'inverse-map-{f}.npz',x=map_x,y=map_ys)
        visible_required=required&(protected<16)
        va=np.array(visible.getchannel('A'));test_required=ndimage.binary_erosion(visible_required,iterations=2)
        exposed_test=(protected>250)&(ba>250)
        original_rgb=np.array(body)[:,:,:3];composed_rgb=np.array(composed)[:,:,:3]
        results[f]={'source_y_landmarks':src_y.tolist(),'target_y_landmarks':dst_y.tolist(),'landmark_names':['garment_top','neck_base','cuff_top','hand_bottom','hem'],'internal_arm_anchor_rows':used_arm_rows,'required_interior_uncovered_pixels':int(np.count_nonzero(test_required&(va<250))),'exposed_interior_changed_pixels':int(np.count_nonzero(exposed_test&np.any(original_rgb!=composed_rgb,axis=2))),'red_key_material_pixels':int(np.count_nonzero(inside&~missing)),'full_garment_backfill_pixels':int(np.count_nonzero(inside&missing)),'material_provenance':asset(HERE/f'material-provenance-{f}.png'),'mesh_controls':asset(HERE/f'mesh-controls-{f}.json'),'inverse_map':asset(HERE/f'inverse-map-{f}.npz'),'fixed_body':asset(BODY/f'selected-{f}.png')}

def plate(name,rows,title):
    out=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(out);d.text((18,12),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(rows.items()):
        bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);x=16+i*288;out.paste(bg.resize((256,512)).convert('RGB'),(x,48));d.line((x+128,48,x+128,559),fill='#e3cf43');d.line((x,523,x+255,523),fill='#70b8b0');d.text((x,578),f.upper(),font=font,fill='#e3cf43')
    d.text((18,618),'Original body, canvas and contact fixed. Mask/garment authoring experiment; no native acceptance.',font=font,fill='#e5e8d8');out.save(HERE/name)
for typ in TYPES:plate(typ+'-mask-comparison.png',{f:mask_previews[(typ,f)] for f in FACES},typ.upper()+' MASK / green cover; magenta expose; cyan drape')
plate('fitted-assembly-comparison.png',assemblies,'DEFORMED ROBE / extracted cloth -> fixed body-relative targets')
plate('unfitted-assembly-comparison.png',before,'BEFORE FIT / direct extracted cloth on original unchanged body')
plate('fitted-clothing-comparison.png',fitted_images,'DEFORMED VISIBLE CLOTH / complete warped source retained separately')
close=Image.new('RGB',(1080,900),'#142823');d=ImageDraw.Draw(close)
for i,(label,im) in enumerate([('BEFORE FIT',before['east']),('AFTER FIT',assemblies['east'])]):
    bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);close.paste(bg.resize((400,800)).convert('RGB'),(40+i*530,50));d.text((40+i*530,15),label,font=font,fill='#e3cf43')
close.save(HERE/'profile-before-after-comparison.png')
js('body-clothing-profiles.json',profiles)
js('fit-result.json',{'scope':'One adult dromad robe fit; other clothing types are mask proposals only','method':'Continuous piecewise-affine inverse mesh from neckline/cuff/hand/hem and outer/arm controls. RGB material warped from actual red-key extraction; complete retained cloth fills absent material. Target coverage/exposure masks determine final visibility. No body pixel deformation; no new ImageGen call.','inputs':[asset(SOURCE/'extracted-visible-clothing-sheet.png'),asset(SOURCE/'keyed-body-mask.png'),asset(BODY/'model.json')],'profile':asset(HERE/'body-clothing-profiles.json'),'views':results,'native_acceptance':'Not attempted; deferred until all conversions generated','visual_review':'Pending inspection; metrics alone do not establish garment quality.'})
print(json.dumps(results,indent=2))
