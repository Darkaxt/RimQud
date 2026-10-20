"""Editable chrome-steel bench with two perforated supports and stock marker."""
from pathlib import Path
import re,json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');MOD=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');REF=MOD/'Textures/Things/Building/Production/TableMachining_south.png'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
text=NATIVE.read_text(encoding='utf-8-sig');objects={name:re.search(r'<object\b[^>]*\bName="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group() for name in ['Metal Workbench','Metal Table','Table','Furniture']};about=ET.parse(MOD/'About/About.xml').getroot();states=json.loads((HERE/'native-state-index.json').read_text())
packet=dict(entry='SCN-METAL-WORKBENCH',identity='Metal Workbench -> Metal Table -> Table -> Furniture',description=ET.fromstring(objects['Metal Table']).find("part[@Name='Description']").get('Short'),native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),objects=objects),native_states=states,
 source_shape='Wide flat trapezoidal top over two broad perforated plate supports; occupied tile adds one tall rectangular handled/slotted mark on the right and one small mark on the left. Exact stock-item identity is not established.',
 palette=dict(primary='c',empty_detail='C',occupied_detail_choices=['C','w','y','W'],rule='Actual empty mask contains no covered detail pixels. Whole chrome-steel structure follows primary c, including its highlights. Occupied decorative marker follows native chosen detail. No bright-metal edge is arbitrarily assigned detail.'),
 donor_reference=dict(mod=about.findtext('name'),package_id=about.findtext('packageId'),workshop_id='2016436324',path=str(REF),sha256=sha(REF),about_path=str(MOD/'About/About.xml'),about_sha256=sha(MOD/'About/About.xml'),role='Actual Vanilla Textures Expanded TableMachining_south supplies readable cold metal contours, shallow plane shading and restrained edge wear only. No machinery, tools, countertop plan, facing system or crafting mechanics are copied.'),
 construction='Flat beaten chrome-steel work surface with trapezoid perspective, shallow apron and two broad slotted side supports. Tiny visible joints connect supports to the underside: authored physical interpretation of the source pixel gap, not a floating tabletop. Occupied marker is a rectangular upright slotted component and a small circular mark, not an identified native inventory item.',
 states='Inherited Metal Table EmptyTile sw_table_metal.bmp; FullTile sw_table_metal_full.bmp. Inventory.CheckEmptyState/CheckNonEmptyState independently choose comma-expanded tile/detail values. Empty C; occupied C/w/y/W. Do not correlate a new item identity to native color or reroll native state.',
 inventory_boundary='Table Container/Inventory population, non-takeable100-weight inorganic metal furniture, cover and sounds stay native. Stock marker represents the native occupied tile, not actual held inventory, a research bench or imported production functionality. Rare animated/custom cases retain native fallback.',
 frame=dict(native=[16,24],manual=[512,768],recipient=[256,256],authored_source_anchor=[8,16],rule='Same entire source-cell frame for empty base and occupied component; no independent bbox centering or per-state scaling.'),native_acceptance='Pending all-conversions-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
base='''<g stroke="#344247" stroke-linejoin="round">
<path d="M1.4 10.5H4.1L4 17.55H2.1V18.6H1.4Z M11.9 10.5H14.6V18.6H13.9V17.55H12Z" fill="#a1a8ab" stroke-width=".17"/>
<path d="M2.15 13.9H3.35V15.05H2.15ZM12.65 13.9H13.85V15.05H12.65Z" fill="#253d35" stroke-width=".15"/>
<path d="M3.95 6.05H12.05L14.85 9.45H1.15Z" fill="#c7c7c7" stroke-width=".18"/>
<path d="M1.15 9.45H14.85V10.85H1.15Z" fill="#999999" stroke-width=".18"/>
<path d="M1.4 9.7H14.55M1.7 11.2V17.9M12.2 11.2V17.25" fill="none" stroke="#dddddd" stroke-width=".075"/>
<path d="M5 7L8.2 7.15M6.6 8.1L11.6 7.75M3.6 8.65L6 8.6M9.4 8.85L12.8 8.55" stroke="#a7a7a7" stroke-width=".055" fill="none"/>
</g>'''
# A transparent opening, not a painted dark square, cuts each broad support.
base=base.replace('<g stroke=', '<defs><mask id="supports"><rect width="16" height="24" fill="white"/><rect x="2.15" y="13.9" width="1.2" height="1.15" fill="black"/><rect x="12.65" y="13.9" width="1.2" height="1.15" fill="black"/></mask></defs><g mask="url(#supports)" stroke=')
stock='''<g stroke="#756b32" stroke-linejoin="round"><path d="M9.05 3.1H11.85V8.95H9.05Z" fill="#d7c765" stroke-width=".16"/><path d="M9.05 3.1L9.4 2.9H12.1L11.85 3.1V8.95L12.1 8.7V2.9" fill="#b5a64e" stroke-width=".1"/><rect x="9.7" y="3.8" width="1.45" height="1.25" rx=".05" fill="#46574b" stroke-width=".11"/><path d="M9.35 5.5V8.6M9.35 3.3H11.55" stroke="#f0e5aa" stroke-width=".075"/><circle cx="7.55" cy="8.45" r=".26" fill="#d7c765" stroke-width=".08"/></g>'''
# Cut the upper stock handle hole through alpha too.
stock='<defs><mask id="slot"><rect width="16" height="24" fill="white"/><rect x="9.7" y="3.8" width="1.45" height="1.25" rx=".05" fill="black"/></mask></defs><g mask="url(#slot)">'+stock+'</g>'
for name,content in [('empty',base),('occupied',base+stock),('stock',stock)]:
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">{content}</svg>'
 (HERE/f'constructed-{name}.svg').write_bytes(svg.encode());(HERE/f'constructed-{name}.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/f'constructed-{name}.svg'),skip_system_fonts=True))
plate=Image.new('RGB',(1440,830),'#142823');draw=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);draw.text((20,15),'METAL WORKBENCH / two actual native stock states > editable flat steel bench > actual VTE metal reference',font=font,fill='#e3cf43')
for x,state in [(35,'empty'),(510,'occupied')]:
 im=Image.open(HERE/f'constructed-{state}.png').resize((288,432),Image.Resampling.LANCZOS);plate.paste(im,(x,65),im);draw.text((x,530),'Editable '+state+' / same frame',font=font,fill='#e3cf43')
im=Image.open(REF).convert('RGBA');im.thumbnail((410,320));plate.paste(im,(975,165),im);draw.text((975,530),'VTE machining / metal style only',font=font,fill='#e3cf43')
for i,line in enumerate(['Source low trapezoid top and two perforated plate supports; no copied donor machines or tools.',
 'Tiny support connections are authored physical interpretation; actual support holes stay transparent.',
 'Empty contains primary c only. Occupied marker is a source-shaped ambiguous part, with native detail tint.',
 'Gold here identifies stock ownership only; neutral output must not bake gold or reassign metal edge highlights.',
 'Actual inventory selects empty/occupied tile and independent color. No new crafting or item-identification logic.']):draw.text((20,615+i*32),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
