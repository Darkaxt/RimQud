"""Reconstruct native brinestalk as three uneven fibrous salt-rotted pilings."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/ZoneTerrain.xml')
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');REF=MOD/'Textures/Things/Plant/TreeBamboo/TreeBambooA.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
j=json.loads((ROOT/'evidence/conversion-ledger.json').read_text(encoding='utf-8'));entry=next(e for e in j['entries'] if e['id']=='SCN-BRINESTALK');original=entry['metadata']['original_reference']
mask=DONOR/'village-originals/brinestalk-mask.png';reference=DONOR/'village-originals/brinestalk-reference.png';assert sha(mask)==original['native_mask_sha256'] and sha(reference)==original['reference_sha256']
tree=ET.parse(NATIVE).getroot();native=tree.find(".//object[@Name='Brinestalk']");parent=tree.find(".//object[@Name='Plant']");about=ET.parse(MOD/'About/About.xml').getroot()
packet=dict(entry='SCN-BRINESTALK',recorded_at=datetime.now(timezone.utc).isoformat(),identity='Brinestalk -> Plant -> PhysicalObject',
 description=native.find("part[@Name='Description']").get('Short'),
 native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode'),parent=ET.tostring(parent,encoding='unicode')),
 original_reference=original,private_original=dict(mask=dict(path=str(mask),sha256=sha(mask)),context=dict(path=str(reference),sha256=sha(reference))),
 reference_color_note='Historical reference PNG uses standardized pale preview swatches, not literal native w/g. This comparison decodes the original mask with the installed native palette; the old export remains unchanged as shape evidence.',
 source_shape='Three distinct crooked fibrous stalks at native x4.5,7.5,11.5. Left extends y2..16, center y6..22, right y3..18. Green caps and side knots occupy small source detail regions. No broad leaf canopy is present.',
 palette=dict(primary='w',detail='g',native_primary_rgb='98875f',native_detail_rgb='009403',rule='Opaque black mask is stalk/foreground; white is small green growth/detail. Extract neutral albedo and independent detail mask after refinement; never bake green into neutral view.'),
 donor_reference=dict(mod=about.findtext('name'),package_id=about.findtext('packageId'),workshop_id='2016436324',path=str(REF),sha256=sha(REF),
  role='Actual installed bamboo replacement supplies three-stalk cylindrical shading, crisp contours and fibrous rendering convention only. Broad canopy, bamboo leaf shape, uniform segmentation and donor colors are not adopted.',definition='Texture override at a Core asset path, not a new plant blueprint or required mechanics mod.'),
 construction='Explicit editable three-piling geometry with uneven source heights, salt furrows, loose fibers and small green cap/side growths. Green during refinement is a color-role extraction aid; final selected layers are neutral grayscale.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],authored_anchor=[8,16],rule='One source-cell mapping; do not fit or center individual stalks or alpha bounds. The anchor is authored registration, not a newly measured runtime physical root position.'),
 states='Installed object/Plant parent declares one fixed tile and no random tile builder, open/close, ripeness or neighbor-painting state. No fabricated facing, clothing, canopy-merging or growth simulation is required for this fixed view.',
 native_behavior='Render layer3, occluding=true, LiquidNative water; inherited Physics Solid=false. Keep spring/plant state, visibility and source mechanics native. Sparse alpha does not redefine occlusion.',
 native_acceptance='Deferred until all pending conversions are generated')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
defs='<defs><linearGradient id="fiber"><stop stop-color="#676767"/><stop offset=".36" stop-color="#c8c8c8"/><stop offset=".75" stop-color="#a7a7a7"/><stop offset="1" stop-color="#676767"/></linearGradient></defs>'
stems=[
 'M3.8 15.9L3.15 15.65 3.6 14.7 3.9 13.2 3.65 10.9 3.15 10.8 3.6 9.6 4 8.3 3.7 6.8 3.2 6.4 3.8 5.6 4.05 3.5 3.6 2.8 4.7 2.65 5.2 3.25 5 5.5 4.5 6.6 4.8 8.4 4.65 10.4 4.75 12.6 4.65 14.4 4.6 16Z',
 'M7.05 21.9L7.1 20.1 7 19.1 6.5 18.7 7 17.8 7.05 16.3 6.65 16.2 7.2 14.8 7.2 13.3 7.65 12.5 7.1 11.6 6.65 11.2 7.05 10.2 7 8.8 6.65 8.3 7.1 7.6 7.2 6.7 8.15 6.65 8.1 8.2 8.65 8.6 8.1 9.6 7.8 10.7 8.35 11.8 8.05 13 8.75 13.5 8.9 14.1 8.05 14.7 8.2 16.4 7.85 17.8 8.45 18.5 8.05 19.3 8.15 21.1 7.7 21.9Z',
 'M11 17.9L10.9 16.2 11.1 14.8 10.8 13.1 10.9 11.5 10.3 11.1 10.7 10.2 11 8.9 11 7.7 10.9 6.2 10.55 4.3 10.75 3.8 11.8 3.7 11.6 5.5 11.9 6.9 12.7 7.35 12.4 8.1 11.8 8.4 11.55 9.6 11.5 11.1 12 12.5 11.9 14 11.6 15.6 12 17.5 11.8 18.1Z']
growths=['M3.25 2.15Q4.3 1.8 4.75 2.8L3.7 2.85Z','M2.3 9.2Q3.1 8.65 3.9 9.5L3.45 10.05 2.5 9.8Z',
 'M7.1 6.3Q8.15 5.8 8.6 6.55L8 7.2 7.3 6.95Z','M8 15.15Q8.8 14.9 8.8 15.5L8.1 16Z','M7.75 19.05Q8.5 18.85 8.55 19.4L8 19.9Z',
 'M10.85 3.35Q12 2.6 12.6 3.4L12.05 4.05 11.3 3.85Z','M12 11.4Q13.2 11.1 13.65 11.8L12.7 12.35 12 12.1Z','M10.6 9.25Q10 9 10.15 9.8L10.8 10.1Z']
body=''.join(f'<path d="{p}" fill="url(#fiber)" stroke="#414141" stroke-width=".12"/>' for p in stems)
for x,top,bottom in [(4.2,3.2,15.5),(7.6,7.1,21.5),(11.3,4.3,17.6)]:
 body+=f'<path d="M{x} {top}Q{x-.25} {(top+bottom)/2} {x} {bottom}" stroke="#dddddd" stroke-width=".08" fill="none"/>'
 for y in [top+2.5,top+5,top+8]:
  if y<bottom:body+=f'<path d="M{x-.35} {y}q.4 -.2 .75 .05m-.5 .3l.35 .05" stroke="#757575" stroke-width=".07" fill="none"/>'
detail=''.join(f'<path d="{p}" fill="#009403" stroke="#245024" stroke-width=".08"/>' for p in growths)
for name,content in [('front',body+detail),('body',body),('detail',detail)]:
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{defs}{content}</svg>'
 (HERE/f'constructed-{name}.svg').write_bytes(svg.encode());(HERE/f'constructed-{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{name}.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,745),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'LIVING BRINESTALK / native fibrous salt-rot > editable three-piling design > actual installed bamboo reference',font=font,fill='#e3cf43')
raw=Image.open(mask).convert('RGBA');native=Image.new('RGBA',raw.size)
lo,hi=bytes.fromhex('98875f'),bytes.fromhex('009403')
native.putdata([(*[round(a*(1-r/255)+b*r/255) for a,b in zip(lo,hi)],alpha) for r,_,_,alpha in raw.getdata()])
native=native.resize((256,384),Image.Resampling.NEAREST);plate.paste(native,(55,80),native)
manual=Image.open(HERE/'constructed-front.png').resize((256,384),Image.Resampling.LANCZOS);plate.paste(manual,(525,80),manual)
donor=Image.open(REF).convert('RGBA').resize((320,320),Image.Resampling.NEAREST);plate.paste(donor,(1010,95),donor)
for x,label in [(20,'Qud original / w stalk + g knots'),(480,'Manual / three uneven pilings'),(960,'Vanilla Textures Expanded bamboo')]:draw.text((x,500),label,font=font,fill='#e5e8d8')
for i,line in enumerate(['Source description and actual glyph define fibrous salt-rotted pilings, small green growths and irregular heights.',
 'Bamboo is only a stalk shading/outline reference. No broad canopy, tree crown, new crop yield or donor plant behavior.',
 'Green in the refinement input identifies source detail ownership; final registered albedo will be neutral.',
 'One fixed native tile; no invented facings, clothing, random species or connected/merged vegetation state.']):draw.text((20,570+32*i),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
