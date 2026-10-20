"""Source-shaped chemistry table: scorched wood, phial rack and tall alembic."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,math,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');REF=MOD/'Textures/Things/Building/Production/TableDrugLab_south.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
text=NATIVE.read_text(encoding='utf-8-sig')
def obj(name):return ET.fromstring(re.search(r'<object Name="'+re.escape(name)+r'"\s[^>]*>.*?</object>',text,re.S).group())
native,parent=obj('Alchemist Table'),obj('Table');about=ET.parse(MOD/'About/About.xml').getroot();j=json.loads((ROOT/'evidence/conversion-ledger.json').read_text(encoding='utf-8'));e=next(x for x in j['entries'] if x['id']=='SCN-ALCHEMIST-TABLE');original=e['metadata']['original_reference'];rawpath=DONOR/'village-originals/alchemist-table-mask.png';assert sha(rawpath)==original['native_mask_sha256'];raw=Image.open(rawpath).convert('RGBA')
packet=dict(entry=e['id'],recorded_at=datetime.now(timezone.utc).isoformat(),identity='Alchemist Table -> Table -> Furniture',description=native.find("part[@Name='Description']").get('Short'),
 native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode'),table_parent=ET.tostring(parent,encoding='unicode')),
 original_reference=original,private_original=dict(path=str(rawpath),sha256=sha(rawpath)),
 source_shape='Wide two-row wooden tabletop at native y14..15, two visible supports/feet below it, phial rack on the left and tall pale-cyan alembic glass loops/tubing above and to the right. Preserve the upright source-map silhouette rather than replacing it with a flat modern counter.',
 palette=dict(primary='w',detail='C',native_primary_rgb='98875f',native_detail_rgb='77bfcf',rule='Wood/table/rack/scorch shading is primary; phials/alembic glass is detail. Cyan in the constructed/refined image is an ownership aid; both selected layers become grayscale.'),
 donor_reference=dict(mod=about.findtext('name'),package_id=about.findtext('packageId'),workshop_id='2016436324',path=str(REF),sha256=sha(REF),role='Actual installed TableDrugLab_south replacement supplies clean low-relief chemical-glassware shading and outline/readability only. Do not copy its flat metal counter, layout, modern apparatus, facing logic or drug-lab mechanics.'),
 construction='Editable source-positioned wooden tabletop/legs, radial scorch marks, left wooden rack with three authored phial marks and one tall looping alembic apparatus. Phial count is interpretation of three source rack tips, not native inventory item count.',
 states='Child deletes inherited EmptyTile, FullTile, EmptyDetailColor and FullDetailColor tags. Declared furniture art is one fixed source tile; do not fabricate empty/full variants or hide the described rack/alembic after opening inventory.',
 inventory_boundary='Inherited Container/Inventory and population remain native. The rack/alembic in the source bitmap are decorative fixture art; this does not convert or bake independently carried inventory items into the table.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],authored_anchor=[8,16],rule='One source-cell mapping for table, rack, glass and coverage; no independent centering/bounds fitting of tall apparatus.'),
 native_behavior='Preserve non-occluding Render, inherited organic/wood furniture, container/cover and actual inventory actions. Rare animated/custom states retain native fallback; no crafting/research/drug mechanic is transplanted.',native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
wood='''<path d="M3.15 15.35L4.1 15.5 4.25 21.7 4.7 22.5 2.65 22.5 3.1 21.8ZM11.1 15.5L12.05 15.35 12.15 21.7 13.1 22.45 10.8 22.45 11.1 21.7Z" fill="#a2a2a2" stroke="#424242" stroke-width=".16"/>
<path d="M4.05 19.9H11.25V20.55H4.05Z" fill="#919191" stroke="#414141" stroke-width=".1"/>
<path d="M1.4 12.55H13.5L14.85 14.6H1.05Z" fill="#c1c1c1" stroke="#424242" stroke-width=".14"/>
<path d="M1.05 14.6H14.85V15.6H1.05Z" fill="#939393" stroke="#424242" stroke-width=".16"/>
<path d="M1.4 13.25H13.8M1.6 13.95H14.2M3.55 16.4L3.7 21.6M11.55 16.4L11.65 21.6" fill="none" stroke="#777777" stroke-width=".065"/>
<path d="M1.25 14.77H14.65M3.32 16.6V21.8M11.3 16.6V21.7" stroke="#d7d7d7" stroke-width=".065" fill="none"/>'''
wood+='<ellipse cx="8.2" cy="13.4" rx="1.45" ry=".6" fill="#7a7a7a" opacity=".35"/>'
for i in range(13):
 angle=i*math.tau/13;x1,y1=8.2+math.cos(angle)*.45,13.4+math.sin(angle)*.18;x2,y2=8.2+math.cos(angle)*1.7,13.4+math.sin(angle)*.65
 wood+=f'<path d="M{x1} {y1}L{x2} {y2}" stroke="#646464" stroke-width=".065" opacity=".75"/>'
# Three small phials and the high looping alembic are source decorative fixtures.
glass='''<path d="M6.7 4Q5.4 3.8 5.25 2.7Q5.1 1.15 6.7 1.2Q8.35 1.1 8.25 2.6Q8.2 3.6 7.65 3.9L8.5 4.45Q10.1 4.95 11.25 3.65Q12.45 1.7 13.6 2.7L14.3 3.6 13.7 4.8 12.9 4.4 12.45 5.35 11.3 5.75 11.15 10.8" fill="none" stroke="#3b6870" stroke-width=".34" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M6.7 4Q5.4 3.8 5.25 2.7Q5.1 1.15 6.7 1.2Q8.35 1.1 8.25 2.6Q8.2 3.6 7.65 3.9L8.5 4.45Q10.1 4.95 11.25 3.65Q12.45 1.7 13.6 2.7L14.3 3.6 13.7 4.8 12.9 4.4 12.45 5.35 11.3 5.75 11.15 10.8" fill="none" stroke="#77bfcf" stroke-width=".18" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M8.3 4.4L6.3 7.7 6.15 12.6" stroke="#70b8c8" stroke-width=".2" fill="none"/>
<path d="M10.6 10.3H11.7V11.3Q13.1 11.7 13.2 12.75Q13.25 13.6 11.1 13.65Q9.05 13.6 9.1 12.75Q9.15 11.65 10.6 11.3Z" fill="#77bfcf" fill-opacity=".28" stroke="#4d9bac" stroke-width=".18"/>
<path d="M10.85 10.65V11.5Q9.6 12 9.7 12.9M5.65 2.1Q5.45 3.25 6.4 3.5M12 3Q13 2.35 13.45 3.3" stroke="#c6edf4" stroke-width=".1" fill="none"/>'''
rack='''<path d="M2.1 9.65H6.7V10.2H2.1ZM2.1 12.7H6.7V13.3H2.1ZM2.1 9.7H2.55V13.9H2.1ZM6.25 9.7H6.7V13.9H6.25Z" fill="#9f9f9f" stroke="#444444" stroke-width=".1"/>'''
for x in [2.8,4.3,5.8]:
 glass+=f'<path d="M{x-.27} 8.1H{x+.27}V11.7Q{x} 12.1 {x-.27} 11.7Z" fill="#77bfcf" fill-opacity=".35" stroke="#59a7b7" stroke-width=".13"/><path d="M{x-.12} 8.5V11.55" stroke="#c4edf4" stroke-width=".07"/>'
for name,content in [('front',wood+glass+rack),('wood',wood+rack),('glass',glass)]:
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{content}</svg>'
 (HERE/f'constructed-{name}.svg').write_bytes(svg.encode());(HERE/f'constructed-{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{name}.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,790),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'ALCHEMIST TABLE / source upright chemistry fixture > editable scorched table + rack + alembic > VTE lab',font=font,fill='#e3cf43')
lo,hi=bytes.fromhex('98875f'),bytes.fromhex('77bfcf');original=Image.new('RGBA',raw.size);original.putdata([(*[round(a*(1-r/255)+b*r/255) for a,b in zip(lo,hi)],alpha) for r,_,_,alpha in raw.getdata()]);im=original.resize((256,384),Image.Resampling.NEAREST);plate.paste(im,(45,80),im)
im=Image.open(HERE/'constructed-front.png').resize((256,384),Image.Resampling.LANCZOS);plate.paste(im,(525,80),im)
im=Image.open(REF).convert('RGBA');im.thumbnail((400,300));plate.paste(im,(990,140),im)
for x,label in [(20,'Native shape / w wood + C glass'),(480,'Manual / radial scorch + fixtures'),(955,'VTE TableDrugLab_south / style')]:draw.text((x,510),label,font=font,fill='#e5e8d8')
for i,line in enumerate(['Description and source define a scorched table, left phial rack and tall alembic; do not substitute a generic counter.',
 'Native w/C color roles stay separate. Gray wood and cyan glass during refinement are extraction aids only.',
 'Inherited empty/full tile tags are explicitly deleted; this fixture remains one fixed source view despite container use.',
 'Inventory, cover and rare animated/custom behavior stay native. No donor drug-lab/crafting mechanics are imported.']):draw.text((20,585+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
