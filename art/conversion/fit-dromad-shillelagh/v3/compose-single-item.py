"""Primary staff evidence: current unclothed body plus this held item only."""
from pathlib import Path
import copy,hashlib,json
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];PREV=HERE.parent/'v2';BODY=ROOT/'art/conversion/body-dromad/v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
model=json.loads((PREV/'model.json').read_text());model['context_robe']=None;model['context']='Unclothed fixed body v2 plus Shillelagh only; no unrelated equipment.'
model['preview_rule']='Primary fitting evidence excludes other items. Any outfit context is separate and versioned.'
rows={};palettes={};manifest={}
for f in ['south','east','north']:
 body=read(BODY/f'selected-{f}.png');composed=body.copy();colored=body.copy()
 parts=model['views'][f]
 if f=='north':
  item=read(ROOT/parts[0]['public_file']);composed=Image.alpha_composite(item,body)
 else:
  for row in parts:composed=Image.alpha_composite(composed,read(ROOT/row['public_file']))
 for row in parts:
  if row['component']=='item':
   item=read(ROOT/row['public_file']);t=ImageOps.colorize(ImageOps.grayscale(item),(0,0,0),(177,201,195)).convert('RGBA');t.putalpha(item.getchannel('A'))
   colored=Image.alpha_composite(t,body) if f=='north' else Image.alpha_composite(colored,t)
  else:colored=Image.alpha_composite(colored,read(ROOT/row['public_file']))
 composed.save(HERE/f'assembled-{f}.png');rows[f]=composed;palettes[f]=colored
 manifest[f]=dict(body=ref(BODY/f'selected-{f}.png'),parts=[ref(ROOT/r['public_file']) for r in parts])
rows['west (mirror)']=ImageOps.mirror(rows['east']);palettes['west (mirror)']=ImageOps.mirror(palettes['east'])
def plate(images,name,title):
 out=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);d.text((18,12),title,font=font,fill='#e3cf43')
 for i,(f,im) in enumerate(images.items()):
  bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);x,y=16+i*288,54;out.paste(bg.convert('RGB').resize((256,512),Image.Resampling.LANCZOS),(x,y));d.line((x+128,y,x+128,y+511),fill='#cebc45');d.line((x,y+475,x+255,y+475),fill='#70b8b0');d.text((x,578),f.upper(),font=font,fill='#e3cf43')
 d.text((18,610),'One relevant item over the fixed unclothed body; native acceptance pending.',font=font,fill='#e5e8d8');out.save(HERE/name)
plate(rows,'assembly-comparison.png','DROMAD / SHILLELAGH ONLY / inward front/back grip, accepted profile')
plate(palettes,'palette-comparison.png','SINGLE ITEM / independent y/y equipment tint; neutral original body')
small=Image.new('RGB',(480,340),'#142823')
for i,im in enumerate(rows.values()):
 t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*120+35,15),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*120+12,125),t)
small.save(HERE/'game-scale-review.png');write(HERE/'model.json',model);write(HERE/'composition-inputs.json',dict(body=ref(BODY/'model.json'),item_model=ref(PREV/'model.json'),views=manifest,other_equipment=[],new_imagegen_call=False,item_geometry_changed=False))
print('Single-item staff previews composed; no robe; unchanged registered staff geometry.')
