"""Select sewing head/pedestal shading in fixed editable geometry; preserve open source shapes."""
from pathlib import Path
import json, hashlib, importlib.util
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
OUT=HERE/'registered'; OUT.mkdir(exist_ok=True)
def read(p): return Image.open(p).convert('RGBA')
def ref(p): return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d): p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (OUT/'model.json').exists()
review=json.loads((HERE/'first-structural-review.json').read_text())
assert review['status']=='PASS FOR MATERIAL ONLY'
pattern=np.array(read(HERE/'constructed.png')); own=np.array(read(HERE/'ownership.png'))
coverage_differences=int((pattern[:,:,3]!=own[:,:,3]).sum())
own[:,:,3]=pattern[:,:,3]; own[own[:,:,3]==0,:3]=0
Image.fromarray(own).save(OUT/'ownership-master.png')
helper=ROOT/'art/conversion/scn-book-table/v2/select-material.py'
spec=importlib.util.spec_from_file_location('fixed_material',helper)
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
master,stats=m.select(read(HERE/'refined-raw.png'),own,pattern)
master.save(OUT/'neutral-master.png')
a=np.array(master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'))
a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None]; a[a[:,:,3]==0,:3]=0
neutral=Image.fromarray(a); neutral.save(OUT/'primary-neutral.png')
coverage=a[:,:,3]
r=np.array(Image.fromarray(own).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'))[:,:,0]
r[coverage==0]=0
Image.fromarray(r).save(OUT/'detail-weight.png'); Image.fromarray(coverage).save(OUT/'coverage.png')
detail=a.copy(); detail[:,:,3]=np.uint8(np.round(coverage.astype(float)*r/255)); detail[detail[:,:,3]==0,:3]=0
detailim=Image.fromarray(detail); detailim.save(OUT/'detail-neutral.png')
Image.fromarray(detail[:,:,3]).save(OUT/'detail-coverage.png')
Image.fromarray(np.dstack([r,r,r,coverage])).save(OUT/'authored-dualcolor-mask.png')
primary_part=a.copy(); primary_part[:,:,3]=np.uint8(np.round(coverage.astype(float)*(1-r/255)))
primary_part[primary_part[:,:,3]==0,:3]=0
primaryim=Image.fromarray(primary_part); primaryim.save(OUT/'pedestal-primary-preview.png')
packet=json.loads((HERE/'source-packet.json').read_text())
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
fg=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8)
dc=np.frombuffer(bytes.fromhex(palette['C']),dtype=np.uint8)
ratio=r.astype(float)/255
rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*a[:,:,:1]/255))
rgb[coverage==0]=0
tint=Image.fromarray(np.dstack([rgb,coverage])); tint.save(OUT/'native-primary-w-detail-upper-c.png')
model=dict(entry='SCN-SEWING-MACHINE',kind='source_dualcolor_static_appliance',blueprint='Sewing Machine',native_tile='Items/sw_sewing_machine.bmp',source=ref(HERE/'source-packet.json'),registration=packet['frame'],camera=packet['construction']['camera'],palette=packet['palette'],native_state_owner=packet['native_state'],native_behavior=packet['native_behavior'],native_acceptance=packet['native_acceptance'],native_activation=False,view_policy='One fixed source/cardinal map face; no declared motion, power consumer or sewing gameplay part. Native non-solid physics/examiner/visibility remain native, no new crafting or orientation binding.',formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background')
model.update({key:ref(OUT/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]})
write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(helper=ref(helper),selection=stats,helper_roles=dict(wood='gray pedestal and needle metal; no wood material',top='machine C/head/guide/bed metal'),ownership_coverage_corrected_to_exact_pattern_pixels=coverage_differences,material_rule='One full generated portrait frame resampled to the existing512x768authoring frame for material RGB only. Exact constructed geometry, openings, ink, pivot and head/needle ownership retained; no bounding-box fitting. Generated halo, gap fill and exterior/head glow excluded. Same-material harmonic continuation fills rejected dark/displaced material pixels only.',new_imagegen_calls=1,second_isolation_call=False,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
plate=Image.new('RGB',(1440,760),'#142823'); d=ImageDraw.Draw(plate)
d.text((18,15),'QUD SEWING MACHINE / source C + needle + open pedestal / tiled w and C; glyph R separate',font=font,fill='#e3cf43')
for i,(label,im) in enumerate([('NEUTRAL',neutral),('PRIMARY / PEDESTAL+NEEDLE',primaryim),('DETAIL / MACHINE HEAD',detailim),('NATIVE w + C',tint)]):
    x=18+i*355; large=im.resize((320,480),Image.Resampling.LANCZOS); plate.paste(large,(x,65),large)
    d.text((x,560),label,font=font,fill='#e3cf43')
    for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):
        thumb=im.resize((w,h),Image.Resampling.LANCZOS); plate.paste(thumb,(x+45+j*90,600),thumb)
for i,line in enumerate(['One static source tile; no declared sewing/power/needle animation or new crafting gameplay.', 'True C and leg-frame openings retained; fixed needle, source roles and authored mounts. Generated halo/gap fill excluded.', 'Actual VFE sewing-head reference: metal shape/shading only. No donor tint/bench/props. Native acceptance pending.']):
    d.text((18,670+i*28),line,font=font,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png')
print(json.dumps(dict(result='Registered fixed sewing machine/pedestal layers; native acceptance pending',selection=stats)))
