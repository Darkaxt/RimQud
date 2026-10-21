"""Show actual source/donor/manual/refinement and intended cell-size evidence."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
index=json.loads((HERE/'painted-tile-index.json').read_text());pal=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);plate=Image.new('RGB',(1440,1000),'#142823');d=ImageDraw.Draw(plate);donors=[]
for i,key in enumerate(['soil','grass']):
 file=DONOR/(key+'.png');metadata=json.loads((ROOT/('art/conversion/tile-soil/v1/source-packet.json' if i==0 else 'art/conversion/tile-grass-1/v1/source-packet.json')).read_text())['donor_reference'];assert ref(file)['sha256']==metadata['png_sha256'];donors.append(dict(asset=ref(file),metadata=metadata,role='Fine earth grain only, not filled terrain' if i==0 else 'Blade taper and primary shading only, not dense tuft/species'))
packet=dict(entry='SCOPE-DIRTY',source_index=ref(HERE/'painted-tile-index.json'),scope_source_hold=ref(HERE/'source-scope-hold.json'),additional_visible_states=[s['native_tile'] for s in index['native_states'][:2]],donors=donors,frame='Native16x24 retained as512x768 full cell. Nominal source anchor8,16 is not a foot pivot. One fixed ground-plane camera, no extra facings.',source_facts='Dirt1 has one primary pixel at7,11; legacy grass1 has16 primary pixels in3 separated rising strokes. No source detail pixels. Dirty randomly assigns w/y + k detail for dirt, g/G grass with prior detail retained.',authored_interpretation='One small irregular earth fleck and3 sparse tapered map-plane blades preserve original occupancy/roots/tips. Fine grain, taper and center shading are authored, not a new plant species/animation.',native_behavior='Keep native options, paint distribution/tile random choice, strings, per-cell foreground/detail/background, visibility and draw order. Invisible widget itself has no drawn sprite.',new_imagegen_call=False,selection='Direct Blender map-plane geometry preserves sparse cell layout; optional ImageGen omitted.',native_acceptance='Pending full generation gate')
write(HERE/'blender-v2/source-and-reference-supplement.json',packet)
for i,name in enumerate(['dirt1','legacy-grass1']):
 color='w' if i==0 else 'g';fg=np.array(list(bytes.fromhex(pal[color])));st=index['native_states'][i];a=np.array(Image.open(st['private_mask']['path']).convert('RGBA'));source=Image.fromarray(np.dstack([np.uint8(np.round((1-a[:,:,:1]/255)*fg)),a[:,:,3]]));donor=Image.open(donors[i]['asset']['path']).convert('RGBA');manual=Image.open(HERE/f'blender-v1/{name}-manual.png').convert('RGBA');refined=Image.open(HERE/f'blender-v2/{name}-refined.png').convert('RGBA')
 for j,(label,im) in enumerate([('SOURCE',source),('RIMWORLD REFERENCE',donor),('MANUAL MAP PLANE',manual),('REFINED / PRIMARY '+color,refined)]):
  im=im.copy()
  if j in [2,3]:
   ar=np.array(im);ar[:,:,:3]=np.uint8(np.round(ar[:,:,:3]*fg/255));im=Image.fromarray(ar)
  size=(240,360) if j!=1 else (240,240);bg=Image.new('RGBA',(260,380),'#'+pal['k']);small=im.resize(size,Image.Resampling.NEAREST if j in [0,1] else Image.Resampling.LANCZOS);bg.alpha_composite(small,((260-size[0])//2,(380-size[1])//2));plate.paste(bg.convert('RGB'),(20+j*355,45+i*475));d.text((20+j*355,15+i*475),label,font=font,fill='#e3cf43')
 for j,size in enumerate([(16,24),(24,36),(32,48)]):
  ar=np.array(refined);ar[:,:,:3]=np.uint8(np.round(ar[:,:,:3]*fg/255));im=Image.fromarray(ar).resize(size,Image.Resampling.LANCZOS);bg=Image.new('RGBA',size,'#'+pal['k']);bg.alpha_composite(im);plate.paste(bg.convert('RGB'),(1090+j*85,445+i*475))
plate.save(HERE/'blender-v2/source-manual-refined-comparison.png')
inputs=[ref(HERE/'painted-source-comparison.png'),ref(HERE/'blender-v2/source-manual-refined-comparison.png')]+[ref(HERE/f'blender-v{v}/{name}-{suffix}.png') for v,suffix in [(1,'manual'),(2,'refined')] for name in ['dirt1','legacy-grass1']]
write(HERE/'blender-v2/review-inputs.json',dict(entry='SCOPE-DIRTY / two newly uncovered paint aliases',inputs=inputs,source=packet['source_facts'],contract=packet['frame'],authored=packet['authored_interpretation'],required='One fixed map view for each source alias; compare actual source layout, sparse coverage/roots/tips and intended16x24 size. No broad ground fill, new species, rotation, wind, fixed green/brown or drawn widget. Neutral raw art remains primary-only.3 other grass aliases reuse exact prior source-bound registrations; no new generation claimed for those.',expected_output='Compact findings/confidence/severity/correction and pass/hold for registration; read-only, no generation/tests/delegation.'))
print('Two actual source/donor/manual/refined comparisons and intended-size review packet retained.')
