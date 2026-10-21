"""Register actual bent-sheet refinement through fixed canonical geometry and B/C roles."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from scipy.ndimage import gaussian_filter,binary_erosion
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_bytes((json.dumps(x,indent=2,ensure_ascii=False)+'\n').encode())
def save(p,a):Image.fromarray(a).save(p)
assert not (OUT/'model.json').exists();controls=read(HERE/'construction-controls.json');packet=read(HERE/'source-packet.json')
manual=np.array(Image.open(ROOT/controls['constructed']['path']).convert('RGBA'));raw=Image.open(HERE/'refined-raw.png').convert('RGBA');a=np.array(raw);assert a[690,610,3]==0 and a[835,420,3]==0
rb=read(HERE/'refined-subject-bounds.json')['bbox'];yy,xx=np.where(manual[:,:,3]>=128);tb=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)];sx=(rb[2]-rb[0])/(tb[2]-tb[0]);sy=(rb[3]-rb[1])/(tb[3]-tb[1]);tx=rb[0]-tb[0]*sx;ty=rb[1]-tb[1]*sy
aligned=np.array(raw.transform((512,768),Image.Transform.AFFINE,(sx,0,tx,0,sy,ty),Image.Resampling.BICUBIC));base=manual[:,:,:3].astype(float).mean(2);gen=aligned[:,:,:3].astype(float).mean(2)
valid=(aligned[:,:,3]>=240)&(gen>130)&(gen<251);den=gaussian_filter(valid.astype(float),9);surface=np.divide(gaussian_filter(gen*valid,9),den,out=np.zeros_like(gen),where=den>1e-8)
own=binary_erosion((manual[:,:,3]==255)&(base>175),iterations=4);delta=np.clip((surface-base)*.45,-12,12);lum=base.copy();lum[own]+=delta[own];gray=np.uint8(np.clip(np.rint(lum),0,255));master=np.dstack([gray,gray,gray,manual[:,:,3]]);master[master[:,:,3]==0,:3]=0
save(OUT/'surface-transfer-ownership.png',np.uint8(own)*255);save(OUT/'master-neutral.png',master)
detail=np.array(Image.open(ROOT/controls['ownership']['detail']['path']).convert('RGBA'))[:,:,3];detail=np.minimum(detail,master[:,:,3]);mw=np.uint8(np.rint(np.divide(detail.astype(float)*255,master[:,:,3],out=np.zeros(detail.shape,float),where=master[:,:,3]>0)));save(OUT/'master-detail-weight.png',mw)
small=np.array(Image.fromarray(master).resize((256,256),Image.Resampling.LANCZOS));small[:,:,:3]=np.uint8(np.rint(small[:,:,:3].astype(float).mean(2)))[:,:,None];small[small[:,:,3]==0,:3]=0
dc=np.minimum(np.array(Image.fromarray(detail).resize((256,256),Image.Resampling.LANCZOS)),small[:,:,3]);dw=np.uint8(np.rint(np.divide(dc.astype(float)*255,small[:,:,3],out=np.zeros(dc.shape,float),where=small[:,:,3]>0)))
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];fg=np.frombuffer(bytes.fromhex(palette['B']),dtype=np.uint8).astype(float);de=np.frombuffer(bytes.fromhex(palette['C']),dtype=np.uint8).astype(float)
def tinted(im,w):
    weight=w.astype(float)/255;rgb=np.uint8(np.rint(im[:,:,:3].astype(float).mean(2)[:,:,None]/255*((1-weight[:,:,None])*fg+weight[:,:,None]*de)));rgb[im[:,:,3]==0]=0;return np.dstack([rgb,im[:,:,3]])
for name,data in [('primary-neutral.png',small),('detail-neutral.png',small),('coverage.png',small[:,:,3]),('detail-weight.png',dw),('detail-coverage.png',dc),('authored-dualcolor-mask.png',np.dstack([dw,dw,dw,small[:,:,3]])),('native-B-C.png',tinted(small,dw))]:save(OUT/name,data)
write(HERE/'first-structural-review.json',dict(status='PASS FOR CONTROLLED REGISTRATION',actual_refinement=ref(HERE/'refined-raw.png'),actual_alpha_composite=ref(HERE/'refined-alpha-review.png'),
    review='Two opposed bent sheet surfaces, broad folds/dents and complete perimeter bridges retained. Both source open pockets are actually alpha0 at inspected positions; on-background composite confirms real air, not glass. No imported circuitry, rounded nugget, stack, pins or extra facets.',
    registration_correction='Generated subject size/center shifted and weak stray exterior alpha remains. Final geometry/frame/coverage and authored fold marks remain canonical; recover only bounded interior material shading, never generated alpha or independently fitted final bounds.',
    calls='One actual contextual refinement; source is structurally usable for the intended surface reference. No retry, second isolation or invented generation.'))
decisions=dict(timestamp=datetime.now(timezone.utc).isoformat(),source=ref(HERE/'source-packet.json'),construction=ref(HERE/'construction-controls.json'),refinement=ref(HERE/'generation-receipt.json'),actual_surface=ref(HERE/'refined-raw.png'),
    material_alignment=dict(raw_strong_component_bbox=rb,canonical_bbox=tb,inverse_affine=[sx,0,tx,0,sy,ty],purpose='Material correspondence only; final sheet scale/center/silhouette remain the full-cell manual construction.'),
    transfer='Normalized Gaussian9px material luma from valid alpha>=240 and grey130..251 interior;45percent mix, clipped+/-12levels, only eroded canonical opaque face ownership(base>175). Keep manual creases, curl edges, silhouettes and alpha. Exclude generated borders, shifted features, exterior alpha and invisible RGB haze.',
    tint='Native primary B=0096ff, detail C=77bfcf. Equal-RGB gray texture plus independent detail weight and single coverage. Neutral primary/detail inputs share coverage, blend by weight, not duplicate alpha-over.',
    identity='Bent metal sheet, not fractured microchip despite shared source mask. No electronic pads/traces. Binding is exact Scrap Metal; do not globally replace bit11.',views='One source-bound fixed map view; no source-supported furniture directions, stack-count art, repair/burning variant or body/clothing fit.',native_activation=False)
write(OUT/'registration-decisions.json',decisions)
model=dict(entry='SCN-SCRAP-METAL',blueprint='Scrap Metal',display_name='bent metal sheet',kind='source-bound fixed-map metal scrap',source=ref(HERE/'source-packet.json'),construction=ref(HERE/'construction-controls.json'),refinement=ref(HERE/'generation-receipt.json'),structural_review=ref(HERE/'first-structural-review.json'),decisions=ref(OUT/'registration-decisions.json'),registration=controls['frame'],
    master=ref(OUT/'master-neutral.png'),master_detail_weight=ref(OUT/'master-detail-weight.png'),primary=ref(OUT/'primary-neutral.png'),detail=ref(OUT/'detail-neutral.png'),coverage=ref(OUT/'coverage.png'),detail_weight=ref(OUT/'detail-weight.png'),detail_coverage=ref(OUT/'detail-coverage.png'),authored_dualcolor_mask=ref(OUT/'authored-dualcolor-mask.png'),native_preview=ref(OUT/'native-B-C.png'),
    palette=packet['palette'],binding='Exact Scrap Metal only; other blueprints using bit11 retain separate identity/art and palette.',states='One native fixed tile. Native Takeable/Solid=false/Stacker/TinkerItem Bits=B/disassembly behavior unchanged; no invented pile art, repaired state, burning appearance or animation.',views_and_clothing=controls['views'],native_activation=False,
    native_acceptance='Pending integrated Stage3 after full generation: exact identity/tile selection, B/C palette and coverage, cell size/center, visibility, pickup/stack/disassembly behavior. Art is not native acceptance.')
write(OUT/'model.json',model)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1400,900),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'SCRAP METAL / source shape -> fixed neutral sheet -> native B-C',font=font,fill='#e3cf43')
src=np.array(Image.open(packet['original']['private_mask']['path']).convert('RGBA'));g=np.uint8(225-src[:,:,0].astype(float)/255*75);ni=Image.fromarray(np.dstack([g,g,g,src[:,:,3]])).resize((320,480),Image.Resampling.NEAREST)
for x,im,label in [(25,ni,'SOURCE P/D'),(400,Image.fromarray(master),'REGISTERED NEUTRAL'),(880,Image.fromarray(tinted(master,mw)),'NATIVE B / C')]:
    im=im.copy();im.thumbnail((400,600));plate.paste(im,(x,50),im);d.text((x,670),label,font=font,fill='#e3cf43')
for j,sz in enumerate([(16,24),(24,36),(32,48),(48,72),(64,96)]):
    im=Image.fromarray(tinted(master,mw)).resize(sz,Image.Resampling.LANCZOS);plate.paste(im,(35+j*200,735),im);d.text((35+j*200,845),str(sz),font=font,fill='#e5e8d8')
plate.save(OUT/'source-neutral-native-scale.png')
mask=np.dstack([np.uint8(80+mw.astype(float)/255*175)]*3+[master[:,:,3]]);save(OUT/'primary-detail-ownership-view.png',mask)
process=Image.new('RGB',(1500,850),'#142823');d=ImageDraw.Draw(process);d.text((20,15),'BENT METAL SHEET / manual, actual refinement, alpha review and registered patch',font=font,fill='#e3cf43')
for i,(p,label) in enumerate([(HERE/'manual-suggestion.png','MANUAL + SOURCE'),(HERE/'refined-raw.png','ACTUAL REFINEMENT'),(HERE/'refined-alpha-review.png','SAVED ALPHA COMPOSITE'),(OUT/'source-neutral-native-scale.png','REGISTERED B/C + SCALE')]):
    im=Image.open(p).convert('RGBA');im.thumbnail((700,350));x=20+(i%2)*750;y=55+(i//2)*395;process.paste(im,(x,y),im);d.text((x,y+355),label,font=font,fill='#e3cf43')
process.save(OUT/'whole-process-comparison.png')
print('Registered bent metal sheet with fixed coverage/scale, actual refined shading, independent B/C weighting and intended-size previews.')
