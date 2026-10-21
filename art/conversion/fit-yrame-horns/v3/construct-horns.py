"""Construct one source-bound ram-like horn pair on the selected bare head."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,io,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(768,1152)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert not (HERE/'source-packet.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='FIT-YRAME-HORNS-HEAD-0'
entry=next(e for e in l['entries'] if e['id']==l['active_entry']);body_entry=next(e for e in l['entries'] if e['id']=='BODY-YRAME')
assert body_entry['generation_ready'];bref=body_entry['current_registration']['model'];assert ref(ROOT/bref['path'])==bref
body=read(ROOT/bref['path']);old=read(HERE.parent/'v2/source-packet.json');binding=old['actual_head_binding']
private=Path('E:/Temp/rimqud-yrame-centauroid-20261021')
sheep=[r for r in read(private/'sheep-references.json') if r['name'].startswith('SheepMale')]
packet=dict(entry=entry['id'],recorded_at=datetime.now(timezone.utc).isoformat(),original=old['original'],
    native_source=ref(HERE.parent/'v2/source-packet.json'),actual_head_binding=binding,
    natural_equipment='One mutation-created Horns item575, equipped on Head288, laterality0. Not a hand-held blade, costume or new body part.',
    base_body=bref,base_review=body_entry['art_review']['record'],frame=body['registration'],
    source_creature='Warden Yrame515 -> human-based mutant -> selected compact centauroid body -> separate equipped Horns575',
    references=dict(core_ram=sheep,head_attachment_convention=old['donor'],
        role='Actual Core ram curl/shading and existing Biotech/VTE directional head-attachment convention. Do not copy sheep head, small donor-knob proportions or donor gene logic.'),
    interpretation='Large grooved ram-like curled pair chosen from the original actor silhouette and user direction. Generic Horns prose remains recorded; above-crown arcs and tapering bone tips preserve its broad cues. Exact curl and crown coordinates are authored, not native sheep taxonomy or recovered joint coordinates.',
    palette=dict(foreground='w',detail='W',neutral='Grayscale bone albedo. Independent equipment tint; no skin, eye or clothing pixels.'),
    constraints=['Selected bare body/head RGBA remains unchanged','No clothing or other gear in primary previews',
                 'One common horn curve and paired upper-lateral crown roots across facings','Only natural exact-profile occlusion; no artificial root shift to show a second horn',
                 'Full horn shapes retained; curl-center openings are anatomy, not body-shaped destructive cutouts',
                 'No new native node, mutation resolver or equipment/game validation'])
write(HERE/'source-packet.json',packet)
# A single editable local curl, thick at skull and tapering into a returning point.
segments=[[[481,169],[475,116],[431,84],[404,116]],
          [[404,116],[366,155],[385,226],[427,237]],
          [[427,237],[455,246],[478,222],[473,200]],
          [[473,200],[469,181],[445,178],[434,191]],
          [[434,191],[426,201],[435,214],[445,208]]]
samples=[]
for segment in segments:
 p=np.array(segment,float)
 for t in np.linspace(0,1,25,endpoint=False):samples.append((1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3])
samples.append(np.array(segments[-1][-1],float));samples=np.array(samples)-[481,169]
fractions=np.linspace(0,1,len(samples));width=32*(1-fractions)**.7+.7
controls=dict(local_cubic_segments=segments,root_local_origin=[481,169],yaw_degrees=35,root_width_px=32.7,taper_width_px=.7,
    roots=dict(south=dict(left=[322,151],right=[446,151],crown_top=96),east=dict(near=[481,170],far=[481,170],crown_top=114),north=dict(left=[322,167],right=[446,167],crown_top=112)),
    root_policy='Paired upper-lateral crown roots, about55px below crown, above ears. East root uses the same cranial band, not the side of the face. Values follow selected head pixels; authored estimates.',
    projection='Local curl plane diverges35degrees from sagittal. Front/back project its fore/aft curl outward symmetrically; east gives the complete side coil. Same curve, physical scale and taper.',
    depth=dict(south='Both visible horns near the head surface',east='Near coil only visible; corresponding far coil fully occluded in exact profile',north='Both horns behind the original head',west='Mirror east anatomy, without changing item slot/laterality'),
    canonical_body=bref)
write(HERE/'attachment-controls.json',controls)
def points(f,side):
 a=np.deg2rad(35);u=samples[:,0];v=samples[:,1]
 if f=='east':out=np.stack([481+u*np.cos(a),170+v],1)
 else:
  y=151 if f=='south' else 167
  out=np.stack([384+side*(62-u*np.sin(a)),y+v],1)
 return out
def ribbon(p,w):
 tangent=np.gradient(p,axis=0);n=np.stack([-tangent[:,1],tangent[:,0]],1);n/=np.linalg.norm(n,axis=1)[:,None]
 poly=np.vstack([p+n*w[:,None]/2,(p-n*w[:,None]/2)[::-1]])
 return poly,n
def path(poly):return 'M'+' L'.join(f'{x:.3f} {y:.3f}' for x,y in poly)+' Z'
def make_svg(f):
 shapes=[];details=[];bones=[1] if f=='east' else [-1,1]
 for i,side in enumerate(bones):
  p=points(f,side);poly,n=ribbon(p,width);outline=path(poly)
  shapes.append(f'<clipPath id="horn{i}"><path d="{outline}"/></clipPath><path d="{outline}" fill="url(#bone)" stroke="#1c1c1c" stroke-width="5" stroke-linejoin="round"/>')
  highlight=path(ribbon(p+n*width[:,None]*.15,width*.22)[0])
  shapes.append(f'<g clip-path="url(#horn{i})"><path d="{highlight}" fill="#e2e2e2"/>')
  details.append(f'<path d="{highlight}" fill="white"/>')
  arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(p,axis=0),axis=1))]
  for target in np.arange(16,arc[-1]-12,18):
   j=np.argmin(abs(arc-target));a=p[j]+n[j]*width[j]*.40;b=p[j]-n[j]*width[j]*.40
   middle=p[j]+(p[min(j+2,len(p)-1)]-p[max(j-2,0)])*.25
   shapes.append(f'<path d="M{a[0]:.2f} {a[1]:.2f} Q{middle[0]:.2f} {middle[1]:.2f} {b[0]:.2f} {b[1]:.2f}" fill="none" stroke="#929292" stroke-width="2"/>')
  shapes.append('</g>')
 defs='<defs><linearGradient id="bone" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#a9a9a9"/><stop offset=".50" stop-color="#cfcfcf"/><stop offset="1" stop-color="#ababab"/></linearGradient></defs>'
 start='<svg xmlns="http://www.w3.org/2000/svg" width="768" height="1152" viewBox="0 0 768 1152">'
 return start+defs+''.join(shapes)+'</svg>',start+''.join(details)+'</svg>'
for f in ['south','east','north']:
 svg,detail=make_svg(f);(HERE/f'horns-{f}.svg').write_bytes(svg.encode());(HERE/f'horn-detail-{f}.svg').write_bytes(detail.encode())
 horn=Image.open(io.BytesIO(svg_to_bytes(svg_string=svg))).convert('RGBA');horn.save(HERE/f'horns-{f}.png')
 tint=Image.open(io.BytesIO(svg_to_bytes(svg_string=detail))).convert('RGBA');tint.save(HERE/f'horn-detail-{f}.png')
 base=Image.new('RGBA',SIZE)
 for r in sorted(body['views'][f],key=lambda r:r['layer']):base.alpha_composite(Image.open(ROOT/r['public_file']).convert('RGBA'))
 image=Image.new('RGBA',SIZE)
 if f=='north':image.alpha_composite(horn)
 image.alpha_composite(base)
 if f!='north':image.alpha_composite(horn)
 image.save(HERE/f'constructed-assembly-{f}.png')
 red=np.array(base);lum=red[:,:,:3].mean(2);red[:,:,0]=np.uint8(np.maximum(lum,48));red[:,:,1]=np.uint8(lum*.065);red[:,:,2]=np.uint8(lum*.065);red[red[:,:,3]==0,:3]=0
 keyed=Image.new('RGBA',SIZE)
 if f=='north':keyed.alpha_composite(horn)
 keyed.alpha_composite(Image.fromarray(red))
 if f!='north':keyed.alpha_composite(horn)
 keyed.save(HERE/f'red-context-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
sheet=Image.new('RGBA',(1200,450));draw=ImageDraw.Draw(sheet)
crop_boxes=dict(south=[184,0,584,400],east=[307,18,707,418],north=[184,16,584,416])
for i,(f,box) in enumerate(crop_boxes.items()):
 im=Image.open(HERE/f'red-context-{f}.png').crop(box);sheet.alpha_composite(im,(i*400,0));draw.text((i*400+15,420),{'south':'FRONT / SOUTH','east':'RIGHT PROFILE / EAST','north':'BACK / NORTH'}[f],font=font,fill='white')
sheet.save(HERE/'manual-context-turnaround.png')
write(HERE/'context-crops.json',dict(source_canvas=list(SIZE),sheet=[1200,450],view_boxes=crop_boxes,policy='Matched400px crop frames at original physical scale. Crop-only display; production textures remain in the body frame.'))
plate=Image.new('RGB',(1320,650),'#142823');d=ImageDraw.Draw(plate)
d.text((18,15),'YRAME / native Horns575 + actual Core ram + shared-curl manual head attachment',font=font,fill='#e3cf43')
original=Image.open('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/horns-reference.png').convert('RGBA').resize((96,144),Image.Resampling.NEAREST);plate.paste(original,(25,70),original)
for i,r in enumerate(sorted(sheep,key=lambda r:r['name'])):
 im=Image.open(r['path']).convert('RGBA');im.thumbnail((220,180));plate.paste(im,(190+i*270,65),im)
d.text((18,260),'Item glyph / w-W bone palette. Core ram gives curl only; source head/body and equipment semantics remain Qud.',font=font,fill='#e5e8d8')
small=sheet.resize((1056,396),Image.Resampling.LANCZOS);plate.paste(small,(130,275),small);plate.save(HERE/'source-reference-construction.png')
prompt='''Refine only the GRAYSCALE GROOVED RAM HORNS in this three-view game-sprite construction. Image1 is the exact edit target: one paired horn item fitted to the red-painted head of our adult female sheep-centauroid. Image2 supplies Qud identity and actual Core ram rendering reference; do not add the reference sheep or other figures to output.
Keep FRONT/SOUTH, complete RIGHT PROFILE/EAST and BACK/NORTH in the same three panels. Preserve the matched head scale, blank human head/neck shapes and upper-lateral crown roots ABOVE THE EARS. These are the SAME pair of horns in every facing, not horns on the forehead in front but new temple horns in profile. Keep the thick root, large returning curl, real open center, tapering tip and transverse bone grooves. Front/back project the coil narrowly; profile reveals the complete side coil. Natural occlusion is intentional: a far horn may be hidden by the nearer one. No extra horns to force a count. North horns sit behind the head.
Use restrained bone shading, broad light-gray highlights and gentle grooves, charcoal outlines, neutral grayscale. Preserve the original construction's curl shape/root positions and body registration; refine material/outline quality only. Keep the underlying mannequin RED including its body outlines, never gray/white: its pixels are ownership reference and will be discarded. Do not redraw body pixels into the horn, add hair/eyes/ears/cloth/helmet, or change head anatomy.
Output the same three contextual cropped views on a genuinely transparent background, with generous margins and no cast shadow. No second item-isolation drawing: retain horns ON the red head for this output. The original untouched head remains authoritative; final fitting is deterministic. Labels may be omitted; no extra annotation.'''
(HERE/'context-refinement-prompt.txt').write_bytes(prompt.encode())
now=datetime.now(timezone.utc).isoformat()
def event(step,action,ins,outs,review,result='PASS'):
 entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(p) for p in ins],outputs=[ref(p) for p in outs],review=review,result=result))
event(entry['required_steps'][0],'Resolve captured mutation-created Horns575 on Head288 and latest ram-like interpretation.',[HERE.parent/'v2/source-packet.json',ROOT/bref['path']],[HERE/'source-packet.json'],'One paired natural Head item, w/W bone roles. Generic point/groove description retained; no hand grip/drafted pose or invented sheep race.')
event(entry['required_steps'][1],'Select current bare centauroid head plus actual directional ram and existing head-attachment references.',[ROOT/bref['path']],[HERE/'source-reference-construction.png'],'Body scale/pivot fixed. Core curl and Biotech/VTE depth conventions only; no sheep head or donor gene logic transplanted.')
event(entry['required_steps'][2],'Construct one shared tapered curl, project paired crown roots consistently and overlay only this item.',[ROOT/bref['path']],[HERE/'construct-horns.py',HERE/'attachment-controls.json',HERE/'horns-south.svg',HERE/'horns-east.svg',HERE/'horns-north.svg',HERE/'manual-context-turnaround.png',HERE/'context-crops.json'],'Source-body pixels untouched. North is behind head; complete profile naturally hides far coil. Review manual geometry before actual contextual refinement.')
event(entry['required_steps'][3],'Prepare one contextual horn-surface refinement on a red ownership mannequin.',[HERE/'manual-context-turnaround.png',HERE/'source-reference-construction.png'],[HERE/'context-refinement-prompt.txt'],'Actual tool call pending; no isolated-item generation or native acceptance.','REQUIRES REVIEW')
entry['current_step']=entry['required_steps'][3];l['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',l)
print('Constructed shared-curve ram-like pair, fixed-body context and exact pending prompt; manual review required.')
