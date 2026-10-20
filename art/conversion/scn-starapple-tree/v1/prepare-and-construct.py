"""Source-shaped starapple: one tree and a separate native harvest-color fruit role."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,subprocess,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
DATA=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data');NATIVE=DATA/'StreamingAssets/Base/ObjectBlueprints/ZoneTerrain.xml'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');MOD=Path('D:/Steam/steamapps/workshop/content/294100/2134308522');REF=MOD/'Textures/Things/Plant/Trees/VCE_TreeApple/VCE_TreeAppleA.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
j=json.loads((ROOT/'evidence/conversion-ledger.json').read_text(encoding='utf-8'));entry=next(e for e in j['entries'] if e['id']=='SCN-STARAPPLE-TREE');original=entry['metadata']['original_reference'];rawpath=DONOR/'village-originals/starapple-tree-mask.png';assert sha(rawpath)==original['native_mask_sha256']
tree=ET.parse(NATIVE).getroot();native=tree.find(".//object[@Name='Starapple Tree']");ripe=tree.find(".//object[@Name='Starapple Tree Ripe']");about=ET.parse(MOD/'About/About.xml').getroot();defs=MOD/'1.6/Defs/ThingDefs_Plants/Plants_Cultivated_Trees.xml'
code=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.Harvestable',str(DATA/'Managed/Assembly-CSharp.dll')],capture_output=True,check=True).stdout
raw=Image.open(rawpath).convert('RGBA');points={(x,y) for y in range(24) for x in range(16) if raw.getpixel((x,y))[3] and raw.getpixel((x,y))[0]==255};groups=[]
while points:
 group={points.pop()};todo=list(group)
 while todo:
  x,y=todo.pop()
  for q in [(x-1,y),(x+1,y),(x,y-1),(x,y+1)]:
   if q in points:points.remove(q);group.add(q);todo.append(q)
 groups.append(sorted(group))
assert len(groups)==6
packet=dict(entry='SCN-STARAPPLE-TREE',recorded_at=datetime.now(timezone.utc).isoformat(),identity='Starapple Tree -> Tree -> Plant -> PhysicalObject',
 description=native.find("part[@Name='Description']").get('Short'),native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode'),ripe_sibling=ET.tostring(ripe,encoding='unicode')),
 original_reference=original,private_original=dict(path=str(rawpath),sha256=sha(rawpath)),fruit_glyph_groups=groups,
 interpretation='Six visible source detail clusters are authored as fruit: two larger cross-like marks and four small marks. This is visual glyph interpretation, not a six-fruit yield claim; native Harvestable.OnSuccessAmount is1.',
 harvest=dict(native.find("part[@Name='Harvestable']").attrib),
 installed_state_evidence=dict(assembly_sha256=sha(DATA/'Managed/Assembly-CSharp.dll'),class_name='XRL.World.Parts.Harvestable',scoped_decompilation_sha256=hashlib.sha256(code).hexdigest(),facts=['Native ripe/unripe updates assign TileColor and DetailColor. These blueprints declare no RipeTiles or UnripeTiles.',
 'Both states keep primary TileColor g. Ripe detail R and unripe detail K change fruit appearance without replacing this source tile.',
 'Starapple Tree starts with1:5ripe chance; Starapple Tree Ripe starts1:1, but has the same Render/Description and subsequent Harvestable appearance roles.']),
 palette=dict(primary='g',ripe_detail='R',unripe_detail='K',native_primary_rgb='009403',native_ripe_rgb='d74200',native_unripe_rgb='155352',
  description_palette_boundary='Description says ashen branches, but native tile primary is g. Express pale/ashen bark through neutral texture values; retain native g tint rather than inventing a third fixed-white bark color.'),
 donor_reference=dict(mod=about.findtext('name'),package_id=about.findtext('packageId'),workshop_id='2134308522',path=str(REF),sha256=sha(REF),definition_path=str(defs),definition_sha256=sha(defs),role='Actual Vanilla Plants Expanded apple tree supplies readable red pome fruit, leaf clustering and outline/shading conventions. Do not copy its round dense crown, straight trunk, cultivar mechanics, donor colors or fruit count.'),
 construction='Editable crooked ashen-textured tree with source-inspired asymmetric sparse crown, exposed branches/root flare and six source-positioned fruit glyphs. Red marks aid fruit ownership extraction; final layers are neutral grayscale.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],authored_anchor=[8,16],rule='One fixed frame for primary and fruit role in both harvest states. No per-state crop/recenter; state changes tint only.'),
 states='One fixed map view with ripe/unripe tint states. No creature turnarounds, clothing, random crown, seasonal models or new harvest mechanics are required.',native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
wood='''<path d="M7 21.5Q7.8 19 7.7 16L7.2 14.5 8.5 14.6 8.7 16.6 8.6 20.8 10.4 21.8 12.5 22.3 9.1 22 8 22.7 6.1 22.1 3.3 22.6 5.5 21.7Z" fill="#bcbcbc" stroke="#414141" stroke-width=".13"/>
<path d="M8 16.6Q6.7 13.2 5.2 11.6L3.4 9.2 3.2 6.1 4.5 3.4 7 2.3M8 15.5Q11 12.8 12.4 9.5L13.3 6.4 12.8 3.5 10.5 2M5.6 12L3.4 12.2 1.5 12.4M9.5 14.2L11.5 14.1 13.5 14.4M6.8 13.8L4.6 13.4M6 9.5L5.2 7.1 4.5 6.3M10.7 11.4L9.5 11.5M12.5 7.5L11.5 6.4" fill="none" stroke="#555555" stroke-width=".52" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M8 16.6Q6.7 13.2 5.2 11.6L3.4 9.2 3.2 6.1 4.5 3.4 7 2.3M8 15.5Q11 12.8 12.4 9.5L13.3 6.4 12.8 3.5 10.5 2M5.6 12L3.4 12.2 1.5 12.4M9.5 14.2L11.5 14.1 13.5 14.4M6.8 13.8L4.6 13.4M6 9.5L5.2 7.1 4.5 6.3M10.7 11.4L9.5 11.5M12.5 7.5L11.5 6.4" fill="none" stroke="#cfcfcf" stroke-width=".29" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M7.6 21.6Q8 19 8 17.4M7.2 20.6L7.3 18.9M8.3 21L8.4 19" stroke="#e7e7e7" stroke-width=".07" fill="none"/>'''
foliage=''
for i,(x,y,rx,ry) in enumerate([(6.1,2.6,2.5,1.3),(9.8,2.9,2.2,1.25),(4.4,4.6,2,1.1),(3,6.8,1.5,1.25),(3.6,9.2,2.1,1.8),(6.8,7.9,1.75,.9),(13,8.3,.9,.8),(12.3,11.5,1.25,.8)]):
 foliage+=f'<path d="M{x-rx} {y}Q{x-rx*.8} {y-ry} {x-rx*.25} {y-ry*.65}L{x} {y-ry} {x+rx*.3} {y-ry*.7}Q{x+rx*.95} {y-ry*.6} {x+rx} {y}L{x+rx*.7} {y+ry*.3}Q{x+rx*.6} {y+ry} {x} {y+ry*.8}L{x-rx*.5} {y+ry}Z" fill="#{["ababab","bfbfbf","cecece"][i%3]}" stroke="#515151" stroke-width=".1"/>'
 for dx,dy in [(-.4,-.1),(.35,.2)]:foliage+=f'<path d="M{x+dx-.3} {y+dy}q.25 -.4 .75 -.15q-.2 .35 -.75 .15" stroke="#8a8a8a" stroke-width=".06" fill="none"/>'
fruits=''
for x,y,r in [(11.5,6.5,.7),(4.5,13.5,.7),(4.5,6.5,.32),(9.5,11.5,.32),(1.5,12.5,.32),(13.5,14.5,.32)]:
 fruits+=f'<path d="M{x} {y-r*.7}Q{x-r*.8} {y-r*1.05} {x-r} {y-r*.1}Q{x-r*.9} {y+r*.9} {x} {y+r}Q{x+r*.9} {y+r*.8} {x+r} {y-r*.1}Q{x+r*.8} {y-r*1.05} {x} {y-r*.7}Z" fill="#d74200" stroke="#74331c" stroke-width=".08"/><ellipse cx="{x-r*.32}" cy="{y-r*.2}" rx="{r*.15}" ry="{r*.3}" fill="#ffac91"/>'
for name,content in [('front',wood+foliage+fruits),('tree',wood+foliage),('fruit',fruits)]:
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{content}</svg>'
 (HERE/f'constructed-{name}.svg').write_bytes(svg.encode());(HERE/f'constructed-{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{name}.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,790),'#142823');draw=ImageDraw.Draw(plate)
draw.text((20,15),'STARAPPLE / actual ripe + unripe source colors > editable sparse fruit tree > installed apple reference',font=font,fill='#e3cf43')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
for x,color,label in [(30,'R','Native ripe / g + R'),(365,'K','Native unripe / g + K')]:
 lo,hi=bytes.fromhex(palette['g']),bytes.fromhex(palette[color]);im=Image.new('RGBA',raw.size)
 im.putdata([(*[round(a*(1-r/255)+b*r/255) for a,b in zip(lo,hi)],alpha) for r,_,_,alpha in raw.getdata()]);im=im.resize((256,384),Image.Resampling.NEAREST);plate.paste(im,(x,80),im);draw.text((x,505),label,font=font,fill='#e5e8d8')
im=Image.open(HERE/'constructed-front.png').resize((256,384),Image.Resampling.LANCZOS);plate.paste(im,(720,80),im);draw.text((700,505),'Manual / source fruit positions',font=font,fill='#e5e8d8')
im=Image.open(REF).convert('RGBA').resize((288,288),Image.Resampling.NEAREST);plate.paste(im,(1100,105),im);draw.text((1070,505),'VPE apple / rendering reference',font=font,fill='#e5e8d8')
for i,line in enumerate(['Native Harvestable changes detail tint only: ripe R, unripe K. Primary remains g and the tree/fruit placement stays fixed.',
 'Six source detail clusters supply six authored fruit marks; the actual native harvest yield remains one Starapple.',
 'Ashen description informs neutral bark texture; native g tint remains authoritative. No fixed third white bark color.',
 'Ripe sibling shares appearance. One real conversion can be bound to it with explicit source comparison and process reuse.']):draw.text((20,585+32*i),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
