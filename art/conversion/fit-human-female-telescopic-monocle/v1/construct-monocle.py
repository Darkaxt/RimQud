"""Construct one optical item and explicit original-head ownership, not a new face."""
from pathlib import Path
from datetime import datetime,timezone
import sys,io,json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def svg(x):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+x+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
def ring(x,y):return f'<circle cx="{x}" cy="{y}" r="27" fill="none" stroke="#202523" stroke-width="10"/><circle cx="{x}" cy="{y}" r="27" fill="none" stroke="#bcbcbc" stroke-width="5"/><circle cx="{x}" cy="{y}" r="21" fill="#e9e9e9" fill-opacity=".2" stroke="#565656" stroke-width="2"/>'
chainpaths=dict(south='M200 119 C186 142 188 179 208 194 C226 208 244 203 243 181',east='M324 118 C303 142 301 176 316 191 C328 203 340 192 338 177',north='M307 119 C331 146 339 180 320 198 C308 209 296 197 300 182')
links=dict(south=[(195,132),(190,147),(192,163),(198,178),(210,191),(225,198),(238,192)],east=[(317,130),(309,145),(307,160),(310,176),(320,190),(333,189)],north=[(316,132),(326,148),(331,164),(329,180),(320,194),(307,200)])
primary={};detail={};lens={}
for f in ['south','east','north']:
 chain='<path d="'+chainpaths[f]+'" fill="none" stroke="#202523" stroke-width="4"/>'
 chain+=''.join(f'<ellipse cx="{x}" cy="{y}" rx="3.5" ry="5" fill="none" stroke="#e0e0e0" stroke-width="2.4"/>' for x,y in links[f])
 if f!='east':
  cx=222 if f=='south' else 286;hardware=ring(cx,98);glass=f'<circle cx="{cx}" cy="98" r="19" fill="white" fill-opacity=".13"/><path d="M{cx-12} 91 Q{cx-7} 82 {cx+2} 84" fill="none" stroke="white" stroke-width="3" stroke-linecap="round"/>'
 else:
  hardware='<path d="M320 78 Q343 73 370 77 L380 80 L380 119 Q349 124 320 119Z" fill="#aaa" stroke="#202523" stroke-width="5"/><path d="M330 78 V120 M347 77 V122 M365 78 V121" fill="none" stroke="#454545" stroke-width="3"/><ellipse cx="378" cy="100" rx="11" ry="23" fill="#d5d5d5" stroke="#202523" stroke-width="5"/>'
  glass='<ellipse cx="379" cy="100" rx="7" ry="17" fill="white" fill-opacity=".22"/><path d="M377 89 Q382 94 381 103" fill="none" stroke="white" stroke-width="2.6" stroke-linecap="round"/>'
 primary[f]=chain+hardware+glass;detail[f]=chain+glass;lens[f]=glass
primary['west']='<g transform="translate(512 0) scale(-1 1)">'+primary['east']+'</g>';detail['west']='<g transform="translate(512 0) scale(-1 1)">'+detail['east']+'</g>';lens['west']='<g transform="translate(512 0) scale(-1 1)">'+lens['east']+'</g>'
assert not (HERE/'constructed-red-head-context.png').exists()
contexts={};assemblies={};ownership={}
for f in ['south','east','north','west']:
 body=Image.open(BODY/f'selected-{"east" if f=="west" else f}.png').convert('RGBA');head=Image.open(BODY/f'head-{"east" if f=="west" else f}.png').convert('RGBA')
 if f=='west':body=ImageOps.mirror(body);head=ImageOps.mirror(head)
 for prefix,content in [('pattern',primary[f]),('detail-region',detail[f]),('glass',lens[f])]:
  s=svg(content);(HERE/f'{prefix}-{f}.svg').write_bytes(s.encode());raster(s).save(HERE/f'constructed-{prefix}-{f}.png')
 item=raster(svg(primary[f]));overlay=head.copy() if f in ['north','west'] else Image.new('RGBA',body.size);mask=overlay.getchannel('A');mask.save(HERE/f'body-visibility-{f}.png');overlay.save(HERE/f'body-overlay-{f}.png')
 a=np.array(body).copy();gray=a[:,:,:3].mean(2);a[:,:,0]=np.uint8(np.clip(gray*1.1,0,255));a[:,:,1]=np.uint8(gray*.08);a[:,:,2]=np.uint8(gray*.07);red=Image.fromarray(a)
 ro=red.copy();ro.putalpha(overlay.getchannel('A'));redcontext=Image.alpha_composite(Image.alpha_composite(red,item),ro)
 assembly=Image.alpha_composite(Image.alpha_composite(body,item),overlay);assembly.save(HERE/f'constructed-assembly-{f}.png');contexts[f]=redcontext;assemblies[f]=assembly;ownership[f]=overlay
out=Image.new('RGBA',(1536,1024))
for i,f in enumerate(['south','east','north']):out.alpha_composite(contexts[f].crop((64,0,448,384)).resize((512,512),Image.Resampling.LANCZOS),(i*512,256))
out.save(HERE/'constructed-red-head-context.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for name,rows,title in [('constructed-headwear-comparison.png',assemblies,'CONSTRUCTION / one eye, compact optical barrel and hanging chain'),('constructed-ownership-comparison.png',ownership,'ORIGINAL HEAD / rear/far-side occlusion; complete item retained')]:
 p=Image.new('RGB',(1152,460),'#142823');d=ImageDraw.Draw(p);d.text((18,14),title,font=font,fill='#e3cf43')
 for i,(f,im) in enumerate(rows.items()):
  bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x=16+i*284;p.paste(bg.crop((64,0,448,384)).convert('RGB').resize((256,256)),(x,80));d.line((x+128,80,x+128,336),fill='#e3cf43');d.text((x,360),f.upper(),font=font,fill='#e3cf43')
 d.text((18,422),'Body/contact unchanged. Ocular side is authored; native explicit-west binding remains pending.',font=font,fill='#e5e8d8');p.save(HERE/name)
decisions=dict(body=ref(BODY/'model.json'),construction_script=ref(HERE/'construct-monocle.py'),camera='SEN cardinal + explicit far-side west',authoring_mount='Wearer right eye; source Face/0 does not prescribe an eye',frame=[512,1024],contact=[256,950],lens_centers=dict(south=[222,98],east=[378,100],north=[286,98],west=[134,100]),depth=dict(south='above original head',east='near-side above original head',north='whole monocle behind original head/neck',west='same physical eye now far-side; original near-side head/neck overlays full item'),backdrop='Transparent source; no body-colored garment fill',source_completion='Complete optical geometry retained behind all original-head masks',runtime_limitation='Current probe/VillageArt.cs Direction maps both side facings to east. Authored west assets require explicit direction binding in final integration; no generation-time renderer edit/test.',native_acceptance='Pending full-set generation gate')
(HERE/'construction-decisions.json').write_bytes((json.dumps(decisions,indent=2)+'\n').encode())
lp=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(lp.read_text());entry=next(e for e in ledger['entries'] if e['id']=='FIT-HUMAN-FEMALE-TELESCOPIC-MONOCLE-FACE-0');assert ledger['active_entry']==entry['id']
entry['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step='construct_and_overlay_one_item',action='Constructed the single circular ocular, compact telescoping profile and source-inspired trailing chain on the original female body. Retained full optical geometry with separate original-head occlusion for north and far-side west; no complete-assembly mirror.',inputs=[ref(HERE/'source-packet.json'),ref(HERE/'construct-monocle.py')],outputs=[ref(HERE/n) for n in ['construction-decisions.json','constructed-red-head-context.png','constructed-headwear-comparison.png','constructed-ownership-comparison.png']],review='Construction candidate prepared; inspect before contextual refinement. Explicit-west renderer binding remains a final integration requirement, not an authoring-time game test.',result='CANDIDATE'))
entry['current_step']='construct_and_overlay_one_item';ledger['updated_at']=datetime.now(timezone.utc).isoformat();lp.write_bytes((json.dumps(ledger,indent=2)+'\n').encode());print('Constructed all four optical facings and retained original-head ownership; review pending.')
