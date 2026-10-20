"""Source-shaped pickets from actual painted fence states, not the placeholder tile."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
MOD=Path('D:/Steam/steamapps/workshop/content/294100/2608762624')
NATIVE=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Walls.xml')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
index=json.loads((HERE/'native-state-index.json').read_text());assert len(index['originals'])==16 and not index['missing']
for x in index['originals']:assert sha(Path(x['private_mask']['path']))==x['private_mask']['sha256']
about=ET.parse(MOD/'About/About.xml').getroot();native=ET.parse(NATIVE).getroot().find(".//object[@Name='BrinestalkFence']")
defs=MOD/'1.6/Defs/ThingDefs_Buildings/Buildings_Structure.xml'
fence=next(x for x in ET.parse(defs).getroot().findall('ThingDef') if x.findtext('label')=='picket fence')
packet=dict(entry='SCN-BRINESTALKFENCE',recorded_at=datetime.now(timezone.utc).isoformat(),
 identity='BrinestalkFence -> Wall',description=native.find("part[@Name='Description']").get('Short'),
 native_definition=dict(path=str(NATIVE),sha256=sha(NATIVE),selected=ET.tostring(native,encoding='unicode')),
 source_states=asset(HERE/'native-state-index.json'),source_context=asset(HERE/'native-states-comparison.png'),
 original_reference_correction='Earlier village reference index exported inherited tile-0-13 placeholder. Read-only resources extraction now supplies all16actual painted fence masks. Original index is retained, not overwritten or credited as the shape.',
 anatomy='Fixed map-view plant-stalk pickets with pale squared tops and short fibrous side projections. Isolated native state has3uprights at x3,7,11 over y7..16 in16x24frame. East/west states extend the row; north/south present a narrow edge-on strip with alternating pale caps.',
 palette=dict(primary='w',detail='y',background='retain actual source-owned native background through open alpha gaps'),
 donor_reference=dict(mod=about.findtext('name'),package_id=about.findtext('packageId'),workshop_id='2608762624',
  icon=dict(path=str(MOD/'Textures/Fences/PicketFence/PicketFence_MenuIcon.png'),sha256=sha(MOD/'Textures/Fences/PicketFence/PicketFence_MenuIcon.png')),
  atlas=dict(path=str(MOD/'Textures/Fences/PicketFence/PicketFence_Atlas.png'),sha256=sha(MOD/'Textures/Fences/PicketFence/PicketFence_Atlas.png')),
  definition=dict(path=str(defs),sha256=sha(defs),graphic_class=fence.findtext('graphicData/graphicClass'),link_type=fence.findtext('graphicData/linkType')),
  role='Actual Architect picket-fence presentation supplies low-relief edge weight and asymmetric edge-on/front connection convention. Qud counts, squared stalk tops, salt grain, palette and connection suffixes remain authoritative; triangular sawn boards and donor hue/order are not adopted.'),
 construction='Editable stripped stalks with slightly irregular squared/split tops and salt-tracing waves. The manual native-frame16state construction owns topology; refinement supplies restrained fibrous surface/outline, not independently invented connection shapes.',
 native_behavior='Solid organic, non-occluding, allows missiles and flyover; uses its own gate. Do not make open alpha gaps opaque, change collision/projectile rules, copy donor fence logic or add a mud wall cap.',
 frame=dict(native=[16,24],manual=[512,768],recipient_state=[256,256],native_anchor=[8,16],
  rule='Preserve source cell layout and side/cap placement. Every recipient state uses the same native-coordinate mapping, not independently fitted alpha bounds.'),
 native_acceptance='Deferred until every conversion is generation-ready')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
def front_post(x):
 return f'''<path d="M{x+.05} 16.98L{x-.02} 14.6 {x+.08} 12.2 {x-.04} 9.4 {x+.04} 7.06 {x+.78} 7.11 {x+1.03} 7.02 {x+1.34} 7.15 {x+1.96} 7.08 {x+2.02} 10.1 {x+1.93} 13.4 {x+1.98} 16.98Z" fill="url(#stalk)" stroke="#414141" stroke-width=".12"/>
 <path d="M{x+.12} 7.2Q{x+1} 7.3 {x+1.86} 7.19L{x+1.87} 8.7Q{x+1} 8.5 {x+.12} 8.73Z" fill="#dddddd"/>
 <path d="M{x+.2} 10.4Q{x+.8} 9.9 {x+1.3} 10.3T{x+1.8} 10.2 M{x+.2} 13.7Q{x+.85} 13.2 {x+1.8} 13.7 M{x+.7} 8.9Q{x+.5} 11 {x+.7} 12.4T{x+.65} 16.6" fill="none" stroke="#d9d9d9" stroke-width=".075"/>
 <path d="M{x} 10.1L{x-.6} 10.4 {x-.58} 10.9 {x+.05} 10.8 M{x} 15L{x-.6} 15.3 {x-.56} 15.8 {x+.04} 15.6" fill="#999999" stroke="#444444" stroke-width=".08"/>'''
svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24"><defs><linearGradient id="stalk"><stop stop-color="#606060"/><stop offset=".35" stop-color="#d2d2d2"/><stop offset=".7" stop-color="#bdbdbd"/><stop offset="1" stop-color="#6b6b6b"/></linearGradient></defs>'+''.join(front_post(x) for x in [3,7,11])+'</svg>'
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(HERE/'constructed-front.svg'),skip_system_fonts=True))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,770),'#142823');d=ImageDraw.Draw(plate)
d.text((20,16),'BRINESTALK FENCE / actual painted glyph > editable squared salt-grained pickets > Architect reference',font=font,fill='#e3cf43')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];raw=Image.open(Path(index['originals'][0]['private_mask']['path'])).convert('RGBA');original=Image.new('RGBA',raw.size,'#'+palette['k'])
for y in range(raw.height):
 for x in range(raw.width):
  rr,_,_,aa=raw.getpixel((x,y));f=rr/255
  if aa:original.putpixel((x,y),(*[round(a*(1-f)+b*f) for a,b in zip(bytes.fromhex(palette['w']),bytes.fromhex(palette['y']))],255))
plate.paste(original.resize((256,384),Image.Resampling.NEAREST).convert('RGB'),(45,80))
manual=Image.open(HERE/'constructed-front.png').convert('RGBA').resize((256,384),Image.Resampling.LANCZOS);plate.paste(manual,(480,80),manual)
donor=Image.open(MOD/'Textures/Fences/PicketFence/PicketFence_MenuIcon.png').convert('RGBA').resize((320,288),Image.Resampling.NEAREST);plate.paste(donor,(970,130),donor)
for x,t in [(20,'Actual isolated fence_.bmp'),(430,'Manual /3uprights + salt grain'),(925,'Actual VFE Architect picket icon')]:d.text((x,500),t,font=font,fill='#e5e8d8')
for i,t in enumerate(['Original placeholder has been corrected by actual painted-state extraction; all16native shapes are retained privately.',
 'Reference pointed sawn boards are not copied: Qud has narrow squared stripped stalks and pale salt-tracing grain.',
 'Use one restrained surface refinement and explicit state geometry; no opaque wall cap or continuous panel fill.',
 'Native alpha gaps, non-occlusion, projectile/flyover behavior and ordinary source colors remain separately owned.']):d.text((20,555+i*34),t,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png')
