"""Correct cell-width/world-height units without changing any fish pixels."""
from pathlib import Path
from datetime import datetime,timezone
from copy import deepcopy
import json,hashlib
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE/'registered-v2';OUT=HERE/'registered-v3';OUT.mkdir(exist_ok=True)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(OUT/n).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
assert not (OUT/'model.json').exists()
l=read(ROOT/'evidence/conversion-ledger.json');assert l['active_entry']=='BODY-GLOWFISH';e=next(e for e in l['entries'] if e['id']==l['active_entry']);oldref=e['current_registration']['model'];assert ref(ROOT/oldref['path'])==oldref;m=deepcopy(read(OLD/'model.json'));cell=2/3
assert m['world_canvas']==[1.2,1.2] and m['contact']==[384,384];rows=[]
for f,parts in m['views'].items():
 for r in parts:
  assert r['width']==1.2 and r['height']==1.2 and r['center_x']==0 and r['center_z']==0;assert ref(ROOT/r['public_file'])['sha256']==r['sha256'];r['width']=m['world_canvas'][0]/cell
  assert abs(r['width']*cell/r['size'][0]-r['height']/r['size'][1])<1e-14;rows.append(dict(facing=f,component=r['component'],role=r['color_role'],file=r['public_file'],sha256=r['sha256'],width_before_cells=1.2,width_after_cells=r['width'],world_width_before=.8,world_width_after=r['width']*cell,world_height=r['height']))
now=datetime.now(timezone.utc).isoformat();write('frame-units-correction.json',dict(recorded_at=now,old_model=oldref,renderer=ref(ROOT/'probe/JoppaRenderer.cs'),renderer_contract='CellWidth=2/3 at line19; SpriteLayer world width=width*CellWidth at line257. Height already uses world units. This is read-only source inspection, no native/game validation.',error='Old width1.2 cell units would yield0.8 world while height1.2 world and declared canvas1.2x1.2 imply square physical pixel scale.',correction='Set width=1.2/(2/3)=1.8 Qud cell units for both color planes in every view. Canvas/pivot, center offsets, height, layers, every PNG and world_canvas remain unchanged.',affected_rows=rows))
m.update(registration=dict(canvas=m['canvas'],contact=m['contact'],width=m['world_canvas'][0]/cell,height=m['world_canvas'][1],center_x=0,center_z=0,pixel_world_size=m['world_canvas'][1]/m['canvas'][1],units='width and center_x in Qud cell-width units; height and center_z in world units. Shared1.2x1.2world frame, no per-facing resize.'),frame_correction=ref(OUT/'frame-units-correction.json'),supersedes=oldref)
write('model.json',m)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
out=Image.new('RGB',(1200,680),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'GLOWFISH / same exact textures; previous cell-width mapping versus corrected world-square',font=font,fill='#e3cf43')
for j,(label,w) in enumerate([('PREVIOUS: 0.8 x 1.2 world',160),('CORRECT: 1.2 x 1.2 world',240)]):
 for i,f in enumerate(['south','east','north','west']):
  image=Image.open(ROOT/m['channels'][f]['neutral_assembly']['path']).convert('RGBA');image=image.resize((w,240),Image.Resampling.LANCZOS);out.paste(image,(i*300+(300-w)//2,55+j*300),image);d.text((i*300+12,310+j*300),f.upper(),font=font,fill='#e3cf43')
 d.text((18,285+j*300),label,font=font,fill='#e3cf43')
d.text((18,650),'Generation mapping illustration; no image regeneration, resampling of production assets or native test.',font=font,fill='#e5e8d8');out.save(OUT/'physical-frame-comparison.png')
for key,title,channel in [('neutral','neutral-turnarounds.png','neutral_assembly'),('native','native-palette-turnarounds.png','native_preview')]:
 out=Image.new('RGB',(1200,440),'#142823');d=ImageDraw.Draw(out);d.text((18,15),'GLOWFISH / '+key.upper()+' / exact selected pixels in corrected shared world-square frame',font=font,fill='#e3cf43')
 for i,f in enumerate(['south','east','north','west']):
  bg=Image.new('RGBA',(768,768),'#20382d');bg.alpha_composite(Image.open(ROOT/m['channels'][f][channel]['path']).convert('RGBA'));out.paste(bg.resize((280,280),Image.Resampling.LANCZOS).convert('RGB'),(10+i*300,55));d.text((i*300+15,360),f.upper(),font=font,fill='#e3cf43')
 d.text((18,407),'1.8 cells wide equals1.2 world units. Native acceptance remains after full-generation gate.',font=font,fill='#e5e8d8');out.save(OUT/title)
e['process_log'].append(dict(timestamp=now,step='register_required_layers_and_color_masks',action='Correct shared frame unit mapping only: width1.8 cells maps1.2 world, matching1.2-world height. Keep all8 source layer PNGs, both tint roles, pivot and depth unchanged. Actual generated mapping review pending.',inputs=[oldref,ref(ROOT/'probe/JoppaRenderer.cs')],outputs=[ref(OUT/n) for n in ['frame-units-correction.json','model.json','physical-frame-comparison.png','neutral-turnarounds.png','native-palette-turnarounds.png']],review='No new art or ImageGen/native call. Inspect physical-frame mapping before generation-ready credit.',result='REQUIRES REVIEW'));e.update(current_step='visual_review_anatomy_orientation_palette_all_views',current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'neutral-turnarounds.png')));l['updated_at']=now;(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(l,indent=2,ensure_ascii=False)+'\n').encode());print('Glowfish frame metadata corrected; actual source pixels unchanged. Mapping review pending.')
