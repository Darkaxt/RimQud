"""Remove rejected converging bevel material without changing geometry or metal pixels."""
from pathlib import Path
import json,hashlib,shutil
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE/'registered';OUT=HERE/'registered-final'
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (HERE/'slab-material-correction.json').exists()
if OUT.exists():
    assert all(p.read_bytes()==(OLD/p.relative_to(OUT)).read_bytes() for p in OUT.rglob('*') if p.is_file()),'Resume only the verified unchanged partial copy.'
else:shutil.copytree(OLD,OUT)
write(HERE/'slab-material-source-review.json',dict(initial_attempt='Stopped before any master was saved because south source row366 had no valid samples after8pxerosion.',diagnostic='Inspected eroded gold rows: S259..365,E225..371,N257..365. Partial final directory byte-identical to initial registration.',correction='Use interior front-face samples347..360forS/N and350..365forE; retain edge erosion and fixed output geometry.'))
raw=np.array(read(HERE/'refined-turnaround-raw.png')).astype(float);olddec=json.loads((OLD/'registration-decisions.json').read_text());records={};palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
# Actual inspected interior row ranges; exclude rejected sloping border and bevel highlights.
ranges=dict(south=dict(plane=[260,328],face=[347,360]),east=dict(plane=[226,329],face=[350,365]),north=dict(plane=[260,329],face=[347,360]))
for f in ['south','east','north']:
    original=np.array(read(OLD/f/'neutral-master.png'));master=original.copy();pattern=np.array(read(HERE/f'patched-constructed-{f}.png'));own=np.array(read(OUT/f'ownership-{f}.png'));area=(own[:,:,0]>127)&(own[:,:,3]>0);a=olddec['views'][f]['raw_figure_material_bounds'];gold=(raw[:,:,0]-raw[:,:,2]>12)&(raw[:,:,1]-raw[:,:,2]>12)&(raw[:,:,3]>128);region=np.zeros(gold.shape,bool);region[a[1]:a[3],a[0]:a[2]]=True;gold=ndimage.binary_erosion(gold&region,iterations=8);front=10.5 if f in ['south','north'] else 11.85;back=6.9 if f in ['south','north'] else 5.55;count=0
    for y in range(master.shape[0]):
        xs=np.where(area[y])[0]
        if not len(xs):continue
        isface=y/32>=front;lo,hi=ranges[f]['face' if isface else 'plane'];fraction=np.clip(((y/32-front)/.55 if isface else (y/32-back)/(front-back)),0,1);sy=round(lo+fraction*(hi-lo));source=np.where(gold[sy])[0];source=source[(source>=a[0])&(source<a[2])];assert len(source)>4,(f,y,sy);u=np.linspace(source[0],source[-1],len(xs));gray=np.interp(u,np.arange(raw.shape[1]),raw[sy,:,:2].max(1));master[y,xs,:3]=np.uint8(np.round(gray))[:,None];count+=len(xs)
    ink=pattern[:,:,:3].mean(2);mask=area&(ink<120);master[mask,:3]=np.uint8(np.round(ink[mask]))[:,None];master[master[:,:,3]==0,:3]=0;assert np.array_equal(master[:,:,3],original[:,:,3]);assert np.array_equal(master[~area],original[~area]);Image.fromarray(master).save(OUT/f/'neutral-master.png');records[f]=dict(source_ranges=ranges[f],raw_gold_erosion_pixels=8,selected_marble_pixels=count,unchanged_all_non_marble_pixels=True,unchanged_alpha=True,rule='Per-row interior material rectification from actual raw slab planes; generated converging outer edge and displaced bright bevel excluded. Target plane/front boundary from fixed geometry, no geometry deformation.')
ImageOps.mirror(read(OUT/'east/neutral-master.png')).save(OUT/'west/neutral-master.png');records['west']=dict(rule='Mirror corrected E for symmetric unmarked end.')
groups={key:{} for key in ['neutral','marble-detail','coverage','native-y-C']}
for f in ['south','east','north','west']:
    folder=OUT/f;a=np.array(read(folder/'neutral-master.png').convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0;assert np.array_equal(a[:,:,3],np.array(read(OLD/f/'primary-neutral.png'))[:,:,3]);Image.fromarray(a).save(folder/'primary-neutral.png');role=np.array(Image.open(folder/'detail-weight.png'));detail=a.copy();detail[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*role/255));detail[detail[:,:,3]==0,:3]=0;Image.fromarray(detail).save(folder/'detail-neutral.png');fg=np.frombuffer(bytes.fromhex(palette['y']),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex(palette['C']),dtype=np.uint8);ratio=role.astype(float)/255;rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*a[:,:,:1]/255));rgb[a[:,:,3]==0]=0;tint=Image.fromarray(np.dstack([rgb,a[:,:,3]]));tint.save(folder/'native-y-upper-c-preview.png');groups['neutral'][f]=Image.fromarray(a);groups['marble-detail'][f]=Image.fromarray(detail);groups['coverage'][f]=Image.fromarray(np.dstack([a[:,:,3],a[:,:,3],a[:,:,3],np.full(a.shape[:2],255,np.uint8)]));groups['native-y-C'][f]=tint
model=json.loads((OLD/'model.json').read_text())
def update(v):
    if isinstance(v,dict):
        if 'path' in v and 'sha256' in v and v['path'].startswith(OLD.relative_to(ROOT).as_posix()+'/'):v.update(ref(ROOT/v['path'].replace('/registered/','/registered-final/')))
        else:
            for x in v.values():update(x)
    elif isinstance(v,list):
        for x in v:update(x)
update(model);write(OUT/'model.json',model);write(HERE/'slab-material-correction.json',dict(reason='First registered plate retained a converging pale edge from rejected generated camera inside an otherwise rectangular slab. Separate interior top-plane/front-face material mapping removes it without altering construction.',initial=ref(OLD/'model.json'),final=ref(OUT/'model.json'),views=records,new_imagegen_calls=0,unchanged_geometry_masks_pivot_scale=True));olddec['slab_material_correction']=ref(HERE/'slab-material-correction.json');write(OUT/'registration-decisions.json',olddec)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,images in groups.items():
    plate=Image.new('RGB',(1440,650),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),f'ORNATE TABLE / {group.upper()} / fixed parallel planes + rectified slab material / common source scale',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        x=18+i*355;large=im.resize((320,480),Image.Resampling.LANCZOS);plate.paste(large,(x,50),large);d.text((x,535),f.upper(),font=font,fill='#e3cf43')
        for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+45+j*90,565),thumb)
    d.text((18,625),'Actual y chromium/supports + C marble; same empty/full tile. Extra views unbound; native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{group}.png')
comparison=Image.new('RGB',(1440,650),'#142823');d=ImageDraw.Draw(comparison);d.text((18,15),'SLAB MATERIAL / initial sampled converging bevel versus corrected cardinal planes / geometry and masks unchanged',font=font,fill='#e3cf43')
for i,(f,version) in enumerate([('south',OLD),('south',OUT),('east',OLD),('east',OUT)]):
    im=read(version/f/'primary-neutral.png').resize((320,480),Image.Resampling.LANCZOS);comparison.paste(im,(18+i*355,55),im);d.text((18+i*355,550),f.upper()+' / '+('INITIAL' if version==OLD else 'CORRECTED'),font=font,fill='#e3cf43')
d.text((18,605),'Only marble RGB material remapped. All chromium pixels, coverage, tint ownership, frame, scale and anchor retained.',font=font,fill='#e5e8d8');comparison.save(HERE/'slab-material-comparison.png');print('Rectified slab interiors/front faces in sibling final registration; preserved initial evidence and exact masks.')
