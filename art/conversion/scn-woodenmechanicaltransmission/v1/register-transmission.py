"""One neutral wood plane, all48native connection/phase geometries and shared edge material."""
from pathlib import Path
import json,hashlib,importlib.util
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (OUT/'model.json').exists();assert json.loads((HERE/'first-structural-review.json').read_text())['status']=='PASS FOR MATERIAL ONLY';packet=json.loads((HERE/'source-packet.json').read_text())
# Union is a sampling surface only. Fill all candidate phase slots here; output slots stay exact.
union=np.zeros((768,512),np.uint8)
for phase in [1,2,3]:
 for mask in range(16):union=np.maximum(union,np.array(read(HERE/f'p{phase}-m{mask:02d}-constructed.png'))[:,:,3])
union[round(6.1*32):round(12.9*32),round(3.1*32):round(12.9*32)]=255
own=np.zeros((768,512,4),np.uint8);own[:,:,3]=union;pattern=np.zeros_like(own);pattern[:,:,:3]=181;pattern[:,:,3]=union;pattern[union==0,:3]=0
helper=ROOT/'art/conversion/scn-chest1/v2/select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('wood_material',helper);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);material,stats=m.select(read(HERE/'material-excluding-slot.png'),own,pattern);gray=np.array(material)[:,:,0].astype(float)
# Match only the short edge samples used by adjacent shafts; interior grain stays untouched.
edge_y=(gray[0]+gray[-1])/2;gray[:8]=edge_y;gray[-8:]=edge_y
edge_x=(gray[:,0]+gray[:,-1])/2;gray[:,:8]=edge_x[:,None];gray[:,-8:]=edge_x[:,None]
g=np.uint8(np.clip(np.round(gray),0,255));g[union==0]=0;Image.fromarray(np.dstack([g,g,g,union])).save(OUT/'shared-wood-material.png')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];color=np.frombuffer(bytes.fromhex(palette['w']),dtype=np.uint8);states=[];neutralplate=Image.new('RGB',(1440,960),'#142823');nativeplate=neutralplate.copy();font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',14);nd=ImageDraw.Draw(neutralplate);td=ImageDraw.Draw(nativeplate)
for phase in [1,2,3]:
 for mask in range(16):
  folder=OUT/f'p{phase}-m{mask:02d}';folder.mkdir(exist_ok=True);pattern=np.array(read(HERE/f'p{phase}-m{mask:02d}-constructed.png'));own=np.array(read(HERE/f'p{phase}-m{mask:02d}-ownership.png'));own[:,:,3]=pattern[:,:,3];own[own[:,:,3]==0,:3]=0
  ink=pattern[:,:,:3].mean(2);v=g.copy();marks=(pattern[:,:,3]>0)&(ink<120);v[marks]=np.uint8(np.minimum(ink[marks],gray[marks]*.65));v[pattern[:,:,3]==0]=0;master=Image.fromarray(np.dstack([v,v,v,pattern[:,:,3]]));master.save(folder/'neutral-master.png');a=np.array(master.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0;neutral=Image.fromarray(a);neutral.save(folder/'primary-neutral.png');coverage=a[:,:,3];r=np.array(Image.fromarray(own).convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'))[:,:,0];r[coverage==0]=0;Image.fromarray(coverage).save(folder/'coverage.png');Image.fromarray(r).save(folder/'detail-weight.png');Image.fromarray(np.dstack([r,r,r,coverage])).save(folder/'authored-dualcolor-mask.png');d=a.copy();d[:,:,3]=np.uint8(np.round(coverage.astype(float)*r/255));d[d[:,:,3]==0,:3]=0;Image.fromarray(d).save(folder/'detail-neutral.png');Image.fromarray(d[:,:,3]).save(folder/'detail-coverage.png');rgb=np.uint8(np.round(a[:,:,:3].astype(float)*color[None,None,:]/255));rgb[coverage==0]=0;tint=Image.fromarray(np.dstack([rgb,coverage]));tint.save(folder/'native-w-w.png')
  source=next(r for r in packet['native_states']['states'] if r['phase']==phase and r['neighbor_mask']==mask);states.append(dict(phase=phase,neighbor_mask=mask,native_suffix=source['native_suffix'],native_tile=source['native_tile'],unpowered_reuses=(phase==1),**{key:ref(folder/name) for key,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]}))
  x=(phase-1)*480+(mask%4)*120;y=(mask//4)*230+35
  for plate,draw,im in [(neutralplate,nd,neutral),(nativeplate,td,tint)]:
   thumb=im.resize((96,144),Image.Resampling.LANCZOS);plate.paste(thumb,(x+10,y),thumb);draw.text((x+7,y+150),f'{phase}:{mask:02d} {source["native_suffix"] or "none"}',font=font,fill='#e3cf43')
neutralplate.save(OUT/'neutral-family.png');nativeplate.save(OUT/'native-family.png');model=dict(entry='SCN-WOODENMECHANICALTRANSMISSION',kind='source_dualcolor_native_painted_16x3_family',blueprint='WoodenMechanicalTransmission',source=ref(HERE/'source-packet.json'),registration=packet['frame'],camera=packet['construction']['camera'],palette=packet['palette'],native_state_owner=packet['native_state'],native_behavior=packet['native_behavior'],native_acceptance=packet['native_acceptance'],native_activation=False,formula='coverage*luminance*((1-detail_weight)*foreground+detail_weight*detail)+(1-coverage)*background; actual foreground=detail=w',states=states);write(OUT/'model.json',model)
write(OUT/'registration-decisions.json',dict(helper=ref(helper),selection=stats,material_rule='Single gray wood role selected in union sampling geometry with generated-slot corridor excluded; source primary/detail bothw are separate production roles over one wood plane. Harmonic continuation fills unavailable surface without default-slot ink. Per-state geometry/ink/coverage determine real slots/branches. Same shared coordinates and eight-source-pixel edge material samples match NS/EW endpoints; no per-state image fitting.',new_imagegen_calls=1,second_isolation_call=False,native_activation=False))
# Context is authoring composition only: center cross with straight pieces, plus intended-size swatches.
plate=Image.new('RGB',(1440,950),'#142823');d=ImageDraw.Draw(plate);titlefont=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);d.text((18,15),'WOODEN MECHANICAL TRANSMISSION /48source pieces / shared wood + native w/w / authoring context',font=titlefont,fill='#e3cf43')
layout={(1,1):15,(1,0):5,(1,2):5,(0,1):10,(2,1):10}
for phase in [1,2,3]:
 ox=25+(phase-1)*465
 for (x,y),mask in layout.items():
  im=read(OUT/f'p{phase}-m{mask:02d}'/'native-w-w.png').resize((135,180),Image.Resampling.LANCZOS);plate.paste(im,(ox+x*135,65+y*180),im)
 d.text((ox,640),f'PHASE{phase} / NATIVE CONNECTION CONTEXT',font=titlefont,fill='#e3cf43')
 for i,mask in enumerate([0,3,5,10,15]):
  im=read(OUT/f'p{phase}-m{mask:02d}'/'native-w-w.png').resize((24,36),Image.Resampling.LANCZOS);plate.paste(im,(ox+25+i*75,700),im)
for i,line in enumerate(['All16connection layouts and3native phases retained. Unpowered uses phase1; static glyph216 remains native fallback.', 'One gray wood refinement; exact source-parameter geometry owns slots/branch directions and shared edge profiles.', 'Native charge-activity/SyncTile/MergeConduit/grid/repaint/timing unchanged. Context is authoring, no native acceptance.']):d.text((18,810+i*35),line,font=titlefont,fill='#e5e8d8')
plate.save(OUT/'registration-comparison.png');print(json.dumps(dict(result='Registered48native connection/phase pieces',selection=stats,native_activation=False)))
