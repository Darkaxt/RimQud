"""Preserve the source wrench; fit actual Argyve ordinary offhand on male base."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,math,shutil
import numpy as np
from PIL import Image,ImageDraw
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SOURCE=ROOT/'art/conversion/fit-human-female-wrench/v1';BODY=ROOT/'art/conversion/body-human-male/v2';SIZE=(512,1024)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
packet=json.loads((SOURCE/'source-packet.json').read_text());metadata=json.loads((SOURCE/'weapon-metadata.json').read_text());body=json.loads((BODY/'model.json').read_text());female=json.loads((ROOT/packet['body']['path']).read_text())
for row in metadata['inheritance']:assert sha(Path(row['file']))==row['sha256']
binding=packet['observed_bindings'][0];assert binding['resident']['instance']==519 and binding['resident']['gender']=='male' and binding['part']['id']==322 and binding['part']['laterality']==1 and binding['part']['manager'] is None
live_source=json.loads((ROOT/'art/village/sources.json').read_text());resident=next(r for a in live_source['actors'] for r in a['native_instances'] if r['instance']==519);assert next(p for p in resident['parts'] if p['id']==322)==binding['part']
scale=female['pixel_world_scale']/body['pixel_world_scale']
for name in ['canonical-pattern.svg','constructed-canonical.png','canonical-head-region.png','canonical-shaft-region.png','intact-canonical.png','shaft-canonical.png']:
    shutil.copyfile(SOURCE/name,HERE/name);assert sha(SOURCE/name)==sha(HERE/name)
controls={'south':dict(grip=[372,555],angle=0,mirror=False),'east':dict(grip=[267,555],angle=-20,mirror=False),'north':dict(grip=[138,555],angle=15,mirror=True)}
sheet=Image.new('RGBA',(1536,1024));canonical=Image.open(HERE/'constructed-canonical.png').convert('RGBA')
for i,(f,c) in enumerate(controls.items()):
    a=math.radians(c['angle']);co,si=math.cos(a)/scale,math.sin(a)/scale;gx,gy=c['grip'];px=255 if c['mirror'] else 256;c['inverse_affine']=[co,-si,px-co*gx+si*gy,si,co,590-si*gx-co*gy]
    source=canonical.transpose(Image.Transpose.FLIP_LEFT_RIGHT) if c['mirror'] else canonical;item=source.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC).convert('RGBA');item.save(HERE/f'constructed-item-{f}.png')
    original=Image.open(BODY/f'selected-{f}.png').convert('RGBA');mask=Image.new('L',SIZE)
    if f=='south':ImageDraw.Draw(mask).ellipse((386-36,555-36,386+36,555+36),fill=255)
    mask.save(HERE/f'hand-visibility-{f}.png');h=np.array(original);h[:,:,3]=np.minimum(h[:,:,3],np.array(mask));hand=Image.fromarray(h);hand.save(HERE/f'original-hand-{f}.png')
    assembled=Image.alpha_composite(item,original) if f!='south' else Image.alpha_composite(Image.alpha_composite(original,item),hand);sheet.paste(assembled,(i*512,0))
sheet.save(HERE/'constructed-neutral-context.png');write('fit-controls.json',controls)
metadata.update(recipient_scope='Actual captured male Argyve519, ordinary offhand322/1 item590; shared male baseline fitting.')
metadata['handedness']['qualification']='One-hand base declaration and captured ordinary offhand; actor-specific slot-demand event remains unknown. Actual male equipped observation exists.'
metadata['size'].update(raster_scale=scale,pixel_world_scale=body['pixel_world_scale'],source_pixel_world_scale=female['pixel_world_scale'],canonical_source=ref(SOURCE/'intact-canonical.png'),canonical_geometry_identical=True,reason='Same source armlength Wrench, with male raster compensation preserving physical size. Body and palm anchors change; item geometry/material and canonical lower grip590 do not.')
write('weapon-metadata.json',metadata)
packet.update(entry='FIT-HUMAN-MALE-WRENCH-HAND-1',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Argyve519 captured male ordinary offhand',race='Human ordinary male',fitting_scope='Actual item590 on Hand322/1; not female compatibility or a new loadout. Named cosmetics/outfit and native offhand/pose acceptance remain pending.',body=ref(BODY/'model.json'),weapon_metadata=ref(HERE/'weapon-metadata.json'),shared_source=ref(SOURCE/'source-packet.json'),shared_refinement=dict(prompt=ref(SOURCE/'imagegen-prompt.txt'),context=ref(SOURCE/'refined-red-context.png'),structural_review=ref(SOURCE/'first-refinement-structural-review.json'),new_imagegen_call=False),frame=dict(canvas=list(SIZE),contact=[256,950],item_space_grip=[256,590],item_scale=scale,controls=controls),native_acceptance='Pending full-set generation, actual native offhand/ready-resting state and named Argyve assembly.')
write('source-packet.json',packet)
print('Prepared actual male offhand binding and identical complete armlength wrench, physical scale compensation',scale)
