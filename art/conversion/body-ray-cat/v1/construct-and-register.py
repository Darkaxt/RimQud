"""Current manual ownership plan and shared-frame registration of accepted art.

The current editable construction is not retrospectively claimed as a historical
ImageGen input. Existing accepted source silhouettes and physical size are kept.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,sys
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont,ImageOps,ImageFilter
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs');from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True);SIZE=(512,512);CONTACT=(256,448);PIXEL=.002;FACES=['south','east','north','west']
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def norm(im):
 a=np.array(im);a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
def save(im,name):
 p=OUT/name;norm(im).save(p);return p
def gray(im):
 a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];return norm(Image.fromarray(a))
assert not (OUT/'model.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='BODY-RAY-CAT';entry=next(e for e in l['entries'] if e['id']==l['active_entry']);legacy=read(HERE/'donor-reference-evidence.json')['legacy_registration']['views']
head_controls=dict(south=[[430,785],[710,785],[710,1008],[670,1042],[470,1042],[430,1000]],east=[[790,480],[1025,480],[1040,708],[936,780],[865,750],[775,690]],north=[[500,460],[750,460],[765,600],[725,680],[690,715],[550,715],[515,665],[490,590]])
highlight_rois=dict(south=[[485,610,585,765],[550,305,646,455]],east=[[395,665,550,790],[695,675,770,745],[300,410,372,510]],north=[[540,720,645,860],[775,710,850,890]])
now=datetime.now(timezone.utc).isoformat()
controls=dict(recorded_at=now,scope='Current manual plan after recovery of accepted historical art; not a historical generator input.',
 selected_source_policy='Preserve accepted intrinsic cat silhouette and physical scale, derive one common canvas/pivot. No named gear, mutation appendages or new whole-body redraw.',
 frame=dict(canvas=list(SIZE),contact=list(CONTACT),pixel_world_size=PIXEL,width=SIZE[0]*PIXEL/(2/3),height=SIZE[1]*PIXEL,center_x=0,center_z=(CONTACT[1]-SIZE[1]/2)*PIXEL),
 head_polygons_in_selected_source_pixels=head_controls,highlight_regions_in_selected_source_pixels=highlight_rois,
 palette_interpretation='Native m coat and y pale secondary areas. Muzzle/chest bib follows the actual named/generic pale front pattern. Existing sparse bright glass-fiber strokes supply small secondary highlights; their precise placement is authored, not decoded anatomy. No new eyes, spots or emitted light.',
 per_view=dict(south='Compact feline faces south. Head/ears and front muzzle are low/front; tail rises behind rump above torso. Fore paws near contact; hind pair naturally hidden. Pale muzzle/chest and a few existing glass strokes.',east='Whole right profile, head right and tail rooted at left rump. Two near paws read at contact, far pair naturally overlaps. Head/neck cut above foreleg; no paw becomes part of head. Pale muzzle/chest is anterior.',north='Back of head/ears only, no face. Tail root connects lower rump and curves outside right flank, with gap from skull. Rear paws visible, fore pair occluded. Front bib/muzzle hidden; only sparse existing glass strokes.',west='Exact mirrored east body/head/tint geometry, one mirror at output. Source markings have no established fixed laterality; no independent bounds fitting.'),
 chronology='Historical front and front-guided side/back plus corrected north were recovered byte-exact. Current editable geometry documents anatomy/ownership and registration; it is not falsely labeled as an input to those past calls.')
write(HERE/'manual-ownership-controls.json',controls)
# Editable hand-authored shape suggestions at the shared frame. These are kept
# separate from the immutable selected raster and are not used to redraw it.
manual=dict(
 south='<path d="M252 170 C252 132 253 96 256 58 Q258 32 275 34 Q291 35 290 49 Q283 61 277 51 L272 54 L271 171"/><ellipse cx="253" cy="244" rx="57" ry="87"/><path d="M215 365 Q208 393 216 444 Q231 454 245 443 L252 406 L259 443 Q278 454 290 443 L292 363Z"/><path d="M199 327 L197 290 L228 307 Q251 297 277 309 L305 290 L303 329 Q320 372 286 394 Q251 414 220 392 Q189 375 199 327Z"/>',
 east='<path d="M143 321 Q103 310 90 265 Q71 213 80 173 Q83 149 101 148 Q118 149 115 164 Q103 175 98 166 Q91 205 111 246 Q123 267 149 278"/><path d="M139 281 Q190 261 282 279 L352 269 Q377 218 394 211 L405 239 L431 214 L434 257 Q458 269 466 296 L451 312 Q426 311 412 322 L396 354 Q394 392 407 433 Q424 449 402 450 L379 443 L366 365 L325 344 Q250 367 203 345 L175 369 L172 429 Q191 447 169 450 L143 441 L132 389 Q116 346 139 281Z"/>',
 north='<path d="M208 377 Q207 407 211 443 Q227 454 244 444 L251 414 L263 444 Q283 454 300 442 L302 373Z"/><ellipse cx="253" cy="314" rx="57" ry="99"/><path d="M291 374 Q331 390 359 363 Q390 331 384 278 Q378 246 362 244 Q345 243 346 258 Q348 270 360 269 Q365 314 339 334 Q318 346 293 340"/><path d="M188 131 L185 79 L222 109 Q253 99 284 109 L320 79 L318 135 Q330 176 302 202 Q252 233 209 205 Q179 184 188 131Z"/>')
for f,paths in manual.items():
 svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 512 512"><g fill="#dedede" stroke="#252525" stroke-width="5" stroke-linejoin="round" stroke-linecap="round">'+paths+'</g></svg>'
 p=HERE/f'manual-{f}.svg';p.write_bytes(svg.encode());(HERE/f'manual-{f}.png').write_bytes(svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
sources={};groups={k:{} for k in ['full','neutral','native','ownership','detail','manual']};model=dict(entry=entry['id'],family='ray-cat',species='cat',kind='reusable_intrinsic_quadruped',canvas=list(SIZE),contact=list(CONTACT),registration=controls['frame'],source=ref(HERE/'source-packet.json'),manual_controls=ref(HERE/'manual-ownership-controls.json'),views={},
 policy='Intrinsic four-legged small cat and tail; unchanged accepted body plan, no named clothing or mutation appendages. Existing historical PNGs remain untouched. New grayscale layer derivatives have common physical frame and original-source head/body ownership.',
 native_acceptance='Pending full-generation gate and actual full village palette/facing/look/visibility acceptance; these are authoring assets only.')
for f in ['south','east','north']:
 r=legacy[f];src=ROOT/'art/ctesiphus'/(f+'-albedo.png');assert ref(src)['sha256']==r['sha256'];raw=Image.open(src).convert('RGBA');points=r['landmarks'];world=r['height']/r['size'][1];scale=world/PIXEL
 inverse=[1/scale,0,points['contact_x']-CONTACT[0]/scale,0,1/scale,points['contact_y']-CONTACT[1]/scale]
 placed=norm(raw.transform(SIZE,Image.Transform.AFFINE,inverse,Image.Resampling.BICUBIC));full=gray(placed);a=np.array(full);save(full,f'full-neutral-{f}.png')
 def point(q):return ((q[0]-points['contact_x'])*scale+CONTACT[0],(q[1]-points['contact_y'])*scale+CONTACT[1])
 mask=Image.new('L',SIZE);ImageDraw.Draw(mask).polygon([point(q) for q in head_controls[f]],fill=255);hm=np.array(mask)>0
 # Overlap is only original opaque source pixels inside the seam; no invented
 # external coverage and no extra head outline carried in the body layer.
 seam=hm&ndimage.binary_dilation(~hm,iterations=3)&(a[:,:,3]==255)
 body=a.copy();body[hm&~seam]=0;head=a.copy();head[~hm]=0
 detailmask=Image.new('L',SIZE);draw=ImageDraw.Draw(detailmask)
 if f=='south':
  draw.ellipse((228,371,279,396),fill=255);draw.polygon([(230,394),(277,394),(271,420),(252,433),(233,421)],fill=255)
 elif f=='east':
  draw.ellipse((439,284,470,311),fill=255);draw.polygon([(394,319),(421,317),(411,352),(399,373),(386,347)],fill=255)
 dm=np.array(detailmask.filter(ImageFilter.GaussianBlur(1.2)))
 roi=Image.new('L',SIZE);rd=ImageDraw.Draw(roi)
 for x0,y0,x1,y1 in highlight_rois[f]:rd.rectangle((*point((x0,y0)),*point((x1,y1))),fill=255)
 hi=(a[:,:,:3].mean(2)>244)&(np.array(roi)>0)&(a[:,:,3]==255);dm=np.maximum(dm,np.uint8(hi)*255);dm[a[:,:,3]<255]=0
 layers=[]
 for component,role,pixels,depth in [('body','foreground',body,0),('body','detail',body,.0001),('head','foreground',head,.001),('head','detail',head,.0011)]:
  pixels=pixels.copy()
  if role=='detail':pixels[:,:,3]=np.where(pixels[:,:,3]==255,dm,0)
  out=norm(Image.fromarray(pixels));p=save(out,f'{component}-{role}-{f}.png');layers.append(dict(component=component,color_role=role,file='ray-cat-'+p.name,public_file=ref(p)['path'],sha256=ref(p)['sha256'],size=list(SIZE),contact=list(CONTACT),width=model['registration']['width'],height=model['registration']['height'],center_x=0,center_z=model['registration']['center_z'],layer=depth,native_part_type='Head' if component=='head' else 'Body'))
 composed=Image.new('RGBA',SIZE);colored=Image.new('RGBA',SIZE);details=Image.new('RGBA',SIZE)
 for row in layers:
  im=Image.open(ROOT/row['public_file']).convert('RGBA');composed.alpha_composite(im);b=np.array(im);c=(177,84,207) if row['color_role']=='foreground' else (177,201,195);b[:,:,:3]=np.uint8(np.round(b[:,:,:3].mean(2)[:,:,None]*np.array(c)/255));colored.alpha_composite(norm(Image.fromarray(b)))
  if row['color_role']=='detail':details.alpha_composite(im)
 assert np.array_equal(np.array(norm(composed)),a),f
 save(colored,f'native-palette-{f}.png');save(composed,f'recomposed-neutral-{f}.png');save(details,f'detail-ownership-{f}.png');mask.save(OUT/f'head-region-mask-{f}.png')
 owned=a.copy();owned[:,:,:3]=np.uint8(np.round(owned[:,:,:3].mean(2)[:,:,None]*np.where(hm[:,:,None],np.array([.4,1,.8]),np.array([1,.45,.4]))));owned=norm(Image.fromarray(owned));save(owned,f'ownership-{f}.png')
 for key,im in [('full',full),('neutral',composed),('native',colored),('detail',details),('ownership',owned),('manual',Image.open(HERE/f'manual-{f}.png').convert('RGBA'))]:groups[key][f]=im
 model['views'][f]=layers;sources[f]=dict(source=ref(src),source_size=r['size'],source_landmarks=points,source_world_per_pixel=world,raster_scale=scale,inverse_affine=inverse,registered_alpha_bounds=full.getbbox(),head_polygon_source=head_controls[f],unchanged_physical_size=True,neutralization_max_source_rgb_spread=int(np.ptp(np.array(placed)[:,:,:3].astype(int),axis=2).max()),shared_contact=list(CONTACT),overlap_original_opaque_pixels=int(seam.sum()))
for key in groups:groups[key]['west']=ImageOps.mirror(groups[key]['east'])
model['views']['west']=[]
for row in model['views']['east']:
 im=ImageOps.mirror(Image.open(ROOT/row['public_file']).convert('RGBA'));p=save(im,Path(row['public_file']).name.replace('-east.png','-west.png'));model['views']['west'].append(dict(row,file='ray-cat-'+p.name,public_file=ref(p)['path'],sha256=ref(p)['sha256'],already_mirrored_from_east=True))
for key in ['full','neutral','native','ownership','detail']:
 name=dict(full='full-neutral',neutral='recomposed-neutral',native='native-palette',ownership='ownership',detail='detail-ownership')[key];save(groups[key]['west'],name+'-west.png')
write(OUT/'registration-decisions.json',dict(recorded_at=now,frame=model['registration'],views=sources,source_scale='Retain frozen legacy per-facing anatomical donor calibration. Per-view raster factors compensate existing source resolution, never independently fit alpha bounds.',head_split='Current polygon ownership and 3px internal opaque overlap; body includes all paws and intrinsic tail. Source head/body pixels unchanged except grayscale normalization/resampling.',tint='Native m coat and y secondary mask on original shade pixels. Secondary overlays constrained to opaque source interiors so neutral reconstruction and full alpha stay exact.',history=ref(HERE/'historical-generation-provenance.json'),new_imagegen_calls=0))
write(OUT/'model.json',model)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14)
for key,name,title in [('manual','manual-plan-comparison.png','CURRENT MANUAL SUGGESTION / editable anatomy plan, not a past generation input'),('neutral','assembly-comparison.png','ACCEPTED RAY CAT / common contact and physical frame; original shape retained'),('native','native-palette-comparison.png','NATIVE m COAT / separate y PALE MUZZLE, BIB AND SPARSE GLASS HIGHLIGHTS'),('ownership','ownership-comparison.png','CURRENT OWNERSHIP / salmon body+paws+tail; mint head+ears; no new geometry'),('detail','detail-comparison.png','DETAIL PLANE / original shade pixels only; no baked purple or glow')]:
  plate=Image.new('RGB',(1200,440),'#142823');d=ImageDraw.Draw(plate);d.text((15,15),title,font=font,fill='#e3cf43')
  for i,f in enumerate(FACES):
   bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(groups[key][f]);plate.paste(bg.resize((280,280),Image.Resampling.LANCZOS).convert('RGB'),(10+i*300,55));d.line((10+i*300+140,55,10+i*300+140,335),fill='#b2a94d');d.line((10+i*300,300,290+i*300,300),fill='#6b9d8a');d.text((15+i*300,360),f.upper(),font=font,fill='#e3cf43')
  d.text((15,407),'Source art preserved. New registration/ownership authoring; native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/name)
small=Image.new('RGB',(800,360),'#142823');d=ImageDraw.Draw(small)
for j,key in enumerate(['neutral','native']):
 for i,f in enumerate(FACES):
  im=groups[key][f].resize((64,64),Image.Resampling.LANCZOS);small.paste(im,(15+i*200,15+j*170),im);zoom=im.resize((128,128),Image.Resampling.NEAREST);small.paste(zoom,(75+i*200,15+j*170),zoom);d.text((15+i*200,150+j*170),f.upper(),font=font,fill='#e3cf43')
small.save(OUT/'game-scale-review.png')
for step,action,names in [('construct_front','Create current editable manual anatomy/ownership suggestion with shared frame and visible/hidden part plan. This is current work after historical approved generation; never represented as an input to past calls.',['manual-ownership-controls.json','manual-south.svg','manual-east.svg','manual-north.svg','registered/manual-plan-comparison.png']),('correct_anatomy_then_imagegen_refine_composed_views','Reuse actual corrected/refined selected view set: original north with neck-root tail is rejected; recorded actual north edit moves root to lower rump and separates tail from head. South/east retained as accepted. No additional generation or cosmetic redesign.',['historical-generation-provenance.json','north-before-tail-correction-historical-output.png','north-tail-correction-historical-output.png']),('register_required_layers_and_color_masks','Register accepted sources through frozen physical landmarks, derive neutral body/head plus independent detail and keep source pixels/shape, intrinsic tail/paws and west mirroring explicit. Actual visual review pending.',['registered/model.json','registered/registration-decisions.json','registered/assembly-comparison.png','registered/ownership-comparison.png','registered/native-palette-comparison.png','registered/detail-comparison.png','registered/game-scale-review.png'])]:
 entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/'source-packet.json')],outputs=[ref(HERE/n) for n in names],review=action,result='REQUIRES REVIEW' if step=='register_required_layers_and_color_masks' else 'PASS'))
entry.update(current_step='visual_review_anatomy_orientation_palette_all_views',current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'assembly-comparison.png')),art_review=dict(status='REQUIRES REVIEW',reason='Inspect source preservation, paw/head ownership, shared pivots, neutral recomposition and native tint at intended size.'))
l.update(updated_at=now);(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode());print('Current Ray Cat manual plan and registered candidate written; visual review pending. No new generation.')
