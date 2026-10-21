"""Register actual retry surface on the fixed chip frame, coverage and P/D ownership."""
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
assert not (OUT/'model.json').exists()
controls=read(HERE/'construction-controls-patched.json');source=read(HERE/'source-packet-corrected.json');manual=np.array(Image.open(ROOT/controls['constructed']['path']).convert('RGBA'));raw=Image.open(HERE/'refined-retry.png').convert('RGBA');a=np.array(raw)
assert a[630,610,3]==0 and a[820,400,3]==0
raw_bbox=read(HERE/'retry-subject-bounds.json')['bbox']; yy,xx=np.where(manual[:,:,3]>=128);target=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
sx=(raw_bbox[2]-raw_bbox[0])/(target[2]-target[0]);sy=(raw_bbox[3]-raw_bbox[1])/(target[3]-target[1]);tx=raw_bbox[0]-target[0]*sx;ty=raw_bbox[1]-target[1]*sy
aligned=np.array(raw.transform((512,768),Image.Transform.AFFINE,(sx,0,tx,0,sy,ty),Image.Resampling.BICUBIC))
base=manual[:,:,:3].astype(float).mean(2);gen=aligned[:,:,:3].astype(float).mean(2);good=(aligned[:,:,3]>=240)&(gen>135)&(gen<250)
# Restrict material recovery to opaque, unmarked face interiors. Do not transfer generated
# contours, circuit-line shifts, changed fracture outline, alpha or halo into the canonical sprite.
recovered=np.divide(gaussian_filter(gen*good,9),gaussian_filter(good.astype(float),9),out=np.zeros_like(gen),where=gaussian_filter(good.astype(float),9)>1e-8)
own=binary_erosion((manual[:,:,3]==255)&(base>180),iterations=4)
delta=np.clip((recovered-base)*.45,-12,12);lum=base.copy();lum[own]+=delta[own];gray=np.uint8(np.clip(np.rint(lum),0,255));master=np.dstack([gray,gray,gray,manual[:,:,3]]);master[master[:,:,3]==0,:3]=0
save(OUT/'surface-transfer-ownership.png',np.uint8(own)*255);save(OUT/'master-neutral.png',master)
detail=np.array(Image.open(ROOT/controls['ownership']['detail']['path']).convert('RGBA'))[:,:,3];detail=np.minimum(detail,master[:,:,3]);mw=np.uint8(np.rint(np.divide(detail.astype(float)*255,master[:,:,3],out=np.zeros(detail.shape,float),where=master[:,:,3]>0)));save(OUT/'master-detail-weight.png',mw)
small=np.array(Image.fromarray(master).resize((256,256),Image.Resampling.LANCZOS));small[:,:,:3]=np.uint8(np.rint(small[:,:,:3].astype(float).mean(2)))[:,:,None];small[small[:,:,3]==0,:3]=0
dc=np.minimum(np.array(Image.fromarray(detail).resize((256,256),Image.Resampling.LANCZOS)),small[:,:,3]);dw=np.uint8(np.rint(np.divide(dc.astype(float)*255,small[:,:,3],out=np.zeros(dc.shape,float),where=small[:,:,3]>0)))
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];c=np.frombuffer(bytes.fromhex(palette['C']),dtype=np.uint8).astype(float)
def tint(im):
    rgb=np.uint8(np.rint(im[:,:,:3].astype(float).mean(2)[:,:,None]/255*c));rgb[im[:,:,3]==0]=0;return np.dstack([rgb,im[:,:,3]])
for name,data in [('primary-neutral.png',small),('detail-neutral.png',small),('coverage.png',small[:,:,3]),('detail-weight.png',dw),('detail-coverage.png',dc),('authored-dualcolor-mask.png',np.dstack([dw,dw,dw,small[:,:,3]])),('native-C-C.png',tint(small))]:save(OUT/name,data)
review=dict(status='PASS FOR CONTROLLED REGISTRATION',actual_refinement=ref(HERE/'refined-retry.png'),alpha_composite=ref(HERE/'retry-alpha-review.png'),
    inspection='Both source pockets now have zero alpha at inspected interior positions; actual opaque background composite confirms empty space. Refined fragments/contact traces/bridges are coherent. RGB-only tool preview showed invisible grey/haze, so it is not accepted as alpha evidence.',
    remaining='Generated subject moved/rescaled slightly and has stray low-alpha exterior pixels. Do not import alpha or independently fit final item to generated bounds. Recover material inside canonical opaque face regions only; fixed manual geometry/frame/ink and P/D masks remain authoritative.',
    retry='One targeted retry after first rejection; no third call or second isolation. Source-geometry correction and bounded surface registration are deterministic.')
write(HERE/'retry-structural-review.json',review)
decisions=dict(timestamp=datetime.now(timezone.utc).isoformat(),source=ref(HERE/'source-packet-corrected.json'),construction=ref(HERE/'construction-controls-patched.json'),actual_surface=ref(HERE/'refined-retry.png'),
    material_alignment=dict(raw_strong_component_bbox=raw_bbox,canonical_bbox=target,inverse_affine=[sx,0,tx,0,sy,ty],purpose='Sample material correspondence only. Final sprite frame, size, silhouette and masks never follow generated bounds.'),
    transfer='Normalized Gaussian9px interior surface luma, excluding generated alpha<240, dark ink/boundaries and clipping transfer to +/-12levels at45percent. Eroded canonical gray>180 opaque face ownership protects original traces/ink/edge/coverage. Actual refined surface becomes subtle broad material shading, not a redraw.',
    colour='Equal-RGB gray master/recipient. One coverage plane plus independent detail weight. Both source tint roles C=77bfcf; same-colour current palette does not permit destroying role ownership. Neutral primary/detail inputs share coverage and blend by weight, not duplicate alpha-over.',
    masks='Exact canonical master alpha; source open pockets and outer background remain zero alpha. Reject generated stray/haze alpha. Rim contact extension preserved.',
    view='One fixed source-bound non-furniture resource view; secondary cardinal views and equipment fitting inapplicable.',native_activation=False)
write(OUT/'registration-decisions.json',decisions)
model=dict(entry='SCN-SCRAP-ELECTRONICS',blueprint='Scrap Electronics',display_name='fractured microchip',kind='source-bound fixed-map scrap resource',source=ref(HERE/'source-packet-corrected.json'),construction=ref(HERE/'construction-controls-patched.json'),
    first_refinement=ref(HERE/'generation-first-receipt.json'),selected_refinement=ref(HERE/'generation-retry-receipt.json'),first_rejection=ref(HERE/'first-structural-review.json'),retry_review=ref(HERE/'retry-structural-review.json'),registration=controls['frame'],decisions=ref(OUT/'registration-decisions.json'),
    master=ref(OUT/'master-neutral.png'),master_detail_weight=ref(OUT/'master-detail-weight.png'),primary=ref(OUT/'primary-neutral.png'),detail=ref(OUT/'detail-neutral.png'),coverage=ref(OUT/'coverage.png'),detail_weight=ref(OUT/'detail-weight.png'),detail_coverage=ref(OUT/'detail-coverage.png'),authored_dualcolor_mask=ref(OUT/'authored-dualcolor-mask.png'),native_preview=ref(OUT/'native-C-C.png'),
    palette=source['palette'],binding='Exact Scrap Electronics only. Shared bit11.bmp is not a global replacement key for Scrap Metal, Crystal or Energy.',
    states='One source-defined map tile. Preserve native stack/disassemble/Takeable/Solid behavior; no invented stack image, repaired state, animation, direction or burning texture.',
    views_and_clothing=controls['views'],native_activation=False,native_acceptance='Pending integrated Stage3 after full generation: exact identity/tile selection, C/C palette/coverage/cell mapping, pickup/stack/disassembly/visibility behavior. Authoring is not native acceptance.')
write(OUT/'model.json',model)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1400,900),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'SCRAP ELECTRONICS / fixed geometry + actual refined surface / native C-C',font=font,fill='#e3cf43')
native=np.array(Image.open(source['original']['private_mask']['path']).convert('RGBA'));g=np.uint8(225-native[:,:,0].astype(float)/255*75);src=Image.fromarray(np.dstack([g,g,g,native[:,:,3]]));src=src.resize((320,480),Image.Resampling.NEAREST)
for x,im,label in [(25,src,'ORIGINAL P/D'),(400,Image.fromarray(master),'REGISTERED NEUTRAL'),(880,Image.fromarray(tint(master)),'NATIVE C / C')]:
    im=im.copy();im.thumbnail((400,600));plate.paste(im,(x,50),im);d.text((x,670),label,font=font,fill='#e3cf43')
for j,sz in enumerate([(16,24),(24,36),(32,48),(48,72),(64,96)]):
    im=Image.fromarray(tint(master)).resize(sz,Image.Resampling.LANCZOS);plate.paste(im,(35+j*200,735),im);d.text((35+j*200,845),str(sz),font=font,fill='#e5e8d8')
plate.save(OUT/'source-neutral-native-scale.png')
progress=Image.new('RGB',(1500,860),'#142823');d=ImageDraw.Draw(progress);d.text((20,15),'SCRAP ELECTRONICS / whole actual refinement trail; canonical shape retained',font=font,fill='#e3cf43')
items=[(HERE/'manual-suggestion.png','MANUAL + ORIGINAL'),(HERE/'refined-first-rejected.png','FIRST / REJECT POCKET FILL'),(HERE/'retry-alpha-review.png','RETRY / ACTUAL ALPHA'),(OUT/'source-neutral-native-scale.png','REGISTERED / NATIVE COLOUR')]
for i,(p,label) in enumerate(items):
    im=Image.open(p).convert('RGBA');im.thumbnail((700,350));x=20+(i%2)*750;y=60+(i//2)*400;progress.paste(im,(x,y),im);d.text((x,y+355),label,font=font,fill='#e3cf43')
progress.save(OUT/'whole-process-comparison.png')
print('Registered fixed-scale chip, independent role masks, actual retry material and native C/C intended-size plate.')
