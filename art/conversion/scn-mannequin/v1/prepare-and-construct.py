"""Mounted wood/fiberglass mannequin, distinct from an actor body or equipment rig."""
from pathlib import Path
import hashlib,json,re,subprocess
import xml.etree.ElementTree as ET
from PIL import Image,ImageDraw,ImageFont
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
definitions=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints/Furniture.xml');text=definitions.read_text(encoding='utf-8-sig')
objects={name:re.search(r'<object\b[^>]*Name="'+re.escape(name)+r'"[^>]*>.*?</object>',text,re.S).group(0) for name in ['Mannequin','MountedFurniture','Furniture']};obj=ET.fromstring(objects['Mannequin']);description=obj.find("part[@Name='Description']").get('Short')
source=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/mannequin-mask.png');assert digest(source)=='17e5061ae5916c72d8cd693d6e548445b7080b888419ecb57d1dd1628bf46d07'
donor=Path('D:/Steam/steamapps/workshop/content/294100/2778569619/Textures/CombatTrainingDummy_south.png');about=Path('D:/Steam/steamapps/workshop/content/294100/2778569619/About/About.xml')
assembly=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/Managed/Assembly-CSharp.dll');code=subprocess.run(['C:/Users/darka/.dotnet/tools/ilspycmd.exe','-t','XRL.World.Parts.RandomColors',str(assembly)],capture_output=True,check=True).stdout
packet=dict(entry='SCN-MANNEQUIN',identity='Mannequin -> MountedFurniture -> Furniture',description=description,native_definition=dict(path=str(definitions),sha256=digest(definitions),objects=objects),
 original=dict(path=str(source),sha256=digest(source),tile='Items/sw_mannequin.bmp',canvas=[16,24],info_id=9823,atlas_id=185,rect=[108,182,16,24]),
 source_shape='Colored featureless head at upper-left/center, separated upper torso and hip-form marks over a pale central stem with split base supports. Pale angled marks on the right and colored marks left of the torso are ambiguous arm/armature cues, not proof of extra limbs or a game actor skeleton.',
 palette=dict(primary='y',default_detail='R',native_primary_rgb='b1c9c3',default_detail_rgb='d74200',random_detail='RandomColors DetailColor=all',rule='Head/torso/hip shell and colored left bent-form marks receive actual native randomized detail. Stem/base/right armature remain primary y. Cyan in authoring only identifies shell ownership; final production layers are neutral. Default R preview is a blueprint illustration, not a claimed captured random result.'),
 donor_reference=dict(mod='Combat Training (Continued)',package_id='Mlie.CombatTraining',workshop_id='2778569619',path=str(donor),sha256=digest(donor),about_path=str(about),about_sha256=digest(about),role='Actual installed CombatTrainingDummy_south supplies restrained featureless dummy/form contours, shallow surface shading and stand readability only. Its X eyes, target circles, soft sack shape, donor training behavior and source colors are not copied.'),
 reference_limits='VFE Vikings training dummy was viewed but not selected: helmet, shield and sword would change source identity. No exact wood/fiberglass tailoring mannequin equivalent was found in inspected named assets.',
 construction='Editable static upper-body form has a featureless oval head, simple torso/hip shell, one colored bent left arm and one pale jointed right armature following the sparse source marks. A pale central stem and splayed supports follow the lower primary marks; no walking legs or actor pose system is added. Exact arm connections, joints, neck connectors, material seams and unseen surfaces are authored interpretation, not native anatomical metadata.',
 native_state=dict(owner='XRL.World.Parts.RandomColors',assembly_sha256=digest(assembly),decompiled_stdout_sha256=hashlib.sha256(code).hexdigest(),rule='RandomColors DetailColor=all resolves with Crayons.GetRandomColorAll and writes native Render.DetailColor. Keep actual chosen color native. One ordinary fixed tile is declared; rare Animated builder/BodyType WoodenHumanoid is a separate native behavior and requires original fallback.'),
 equipment_boundary='Ordinary mannequin definition declares no Mannequin-specific clothing/apparel render path. BodyType is animated-furniture metadata, not a reusable human actor body, independent arm/leg render nodes or proof of wearable equipment. This entry converts the static furniture graphic only.',
 frame=dict(native_canvas=[16,24],manual_canvas=[512,768],recipient_canvas=[256,256],authored_source_anchor=[8,16],rule='One complete source-cell transform for shell, armature, stem/base and masks. No independently centered head/armature or actor contact normalization.'),native_behavior='Preserve mounted30-weight non-solid furniture, AV2,Hitpoints80, source non-takeability and rare animated/custom fallback. No donor training mechanics or new clothing framework.',native_acceptance='Pending every-conversion-generated gate')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2,ensure_ascii=False)+'\n').encode())
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="768" viewBox="0 0 16 24">
<g stroke="#303030" stroke-width=".14" stroke-linejoin="round">
<path d="M7.05 13.85H7.55V20.55H7.05Z M7.3 20.2L4.6 22.35H4.1L6.7 20.05Z M7.3 20.2L9.8 22.35H10.35L7.9 20.05Z M7.1 20.4L6.7 22.55H7.25L7.65 20.4Z" fill="#b7b7b7"/>
<path d="M7.1 5.1H7.55V8.2H7.1Z M7.15 9.75H7.55V13.15H7.15Z" fill="#aaa"/>
<path d="M9.75 7.75L10.25 7.9L12.55 11.05L12.25 11.45L9.8 8.3Z M12.25 11.45L13.05 8.55H13.5L12.8 11.5Z M13.05 8.75L14.65 5.65L15.25 5.2L15.4 5.6L14.95 6.05L13.55 8.9Z" fill="#b7b7b7"/>
<circle cx="12.55" cy="11.2" r=".23" fill="#999"/>
<path d="M4.45 7.25L4.8 7.15L4.85 8.8L6.2 9.15L6 9.7L4.25 9.25Z" fill="#8dd3dd"/>
<path d="M8.6 7.15L10.4 7.2L10.1 7.85L8.3 8.35L7.8 9.85L5.45 10.5L5.2 9.75L6.4 9L6.85 8.15Z" fill="#8dd3dd"/>
<path d="M5.65 12.3L6.1 12.2L6.25 13L8.85 12.9L9.2 12.15L9.6 12.3L8.4 14.5H6.4Z" fill="#8dd3dd"/>
<ellipse cx="7.05" cy="3.85" rx="1.3" ry="1.75" fill="#8dd3dd"/>
<path d="M6.2 3Q6.35 2.55 6.75 2.4 M6.15 9.9L7.45 9.5 M6.7 13.75H8.2" fill="none" stroke="#cdeff3" stroke-width=".1"/>
</g></svg>'''
(HERE/'constructed-front.svg').write_bytes(svg.encode());(HERE/'constructed-front.png').write_bytes(svg_to_bytes(svg_string=svg))
mask=Image.open(source).convert('RGBA');native=Image.new('RGBA',mask.size);native.putdata([tuple(round((1-r/255)*f+r/255*d) for f,d in zip(bytes.fromhex('b1c9c3'),bytes.fromhex('d74200')))+(a,) for r,g,b,a in mask.get_flattened_data()])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);plate=Image.new('RGB',(1440,980),'#142823');draw=ImageDraw.Draw(plate);draw.text((20,15),'MANNEQUIN / source colored form + pale armature/stand > editable static furniture > actual dummy reference',font=font,fill='#e3cf43')
for x,im,label in [(60,native,'Original / default y + R'),(530,Image.open(HERE/'constructed-front.png').convert('RGBA'),'Editable form + armature + base'),(1000,Image.open(donor).convert('RGBA'),'Actual training dummy / style only')]:
 big=im.resize((288,432),Image.Resampling.NEAREST if im.size==(16,24) else Image.Resampling.LANCZOS);plate.paste(big,(x,80),big);draw.text((x,555),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Static source head/torso/hip-form marks, bent side forms, pale stem and splayed base remain distinct.',
 'Right-side armature interpretation is uncertain: exact joints are authored, not a native anatomy or clothing rig.',
 'No eyes, face, target, helmet, shield, sword, walking legs or mannequin-specific apparel system is introduced.',
 'Default R is illustrative; actual RandomColors detail selection stays native. Neutral layers will support its chosen tint.',
 'One fixed source furniture view. Native random color, physics and rare animated/custom fallback stay pending.']):draw.text((20,660+i*42),line,font=font,fill='#e5e8d8')
plate.save(HERE/'source-construction-comparison.png');print('Prepared source mannequin form/armature interpretation, native random-detail ownership and actual dummy reference.')
