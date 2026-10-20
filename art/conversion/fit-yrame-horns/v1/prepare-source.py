"""Construct separate directional horn pair on padded, unchanged ordinary head."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,re,sys,xml.etree.ElementTree as ET
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';SIZE=(512,1152)
assert not (HERE/'source-packet.json').exists()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def private(p):return dict(file=str(p),sha256=sha(p),publication='Private installed reference, no standalone donor texture copied')
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1152">'+s+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
front='M208 210 C171 188 143 153 143 111 C143 73 161 43 180 20 C169 65 166 100 177 133 C186 161 204 178 225 191Z'
front_ink='<path d="M157 82 Q164 86 172 87 M147 109 Q160 113 173 112 M153 140 Q167 140 183 135 M168 167 Q180 161 193 158 M190 190 Q199 179 209 179" fill="none" stroke="#686868" stroke-width="3" stroke-linecap="round"/>'
near='M246 212 C216 183 201 139 205 96 C208 62 220 39 239 21 C226 58 224 90 231 122 C237 150 251 176 270 191Z'
far='M263 204 C237 175 222 135 226 95 C229 66 242 42 257 27 C247 64 246 93 250 122 C255 149 266 170 283 187Z'
near_ink='<path d="M210 84 L228 87 M205 112 L231 111 M211 143 L240 134 M224 174 L252 160 M239 196 L263 177" fill="none" stroke="#686868" stroke-width="3" stroke-linecap="round"/>'
far_ink='<path d="M230 85 L248 89 M227 115 L251 113 M235 147 L261 138 M250 179 L273 164" fill="none" stroke="#767676" stroke-width="3" stroke-linecap="round"/>'
def horn(path,ink,shade='#c9c9c9'):return f'<path d="{path}" fill="{shade}" stroke="#292929" stroke-width="4" stroke-linejoin="round"/>'+ink
pair=horn(front,front_ink)+f'<g transform="translate(512 0) scale(-1 1)">{horn(front,front_ink)}</g>'
patterns={'south':dict(near=pair,far=''),'east':dict(near=horn(near,near_ink),far=horn(far,far_ink,'#b8b8b8')),
          'north':dict(near='',far=pair.replace('#c9c9c9','#bdbdbd'))}
sheet=Image.new('RGBA',(1536,640));neutral=Image.new('RGBA',(1536,1152));full={}
for i,(f,parts) in enumerate(patterns.items()):
    body=Image.new('RGBA',SIZE);body.paste(Image.open(BODY/f'selected-{f}.png').convert('RGBA'),(0,128));body.save(HERE/f'original-body-{f}.png')
    for depth,content in parts.items():
        text=svg(content);(HERE/f'pattern-{depth}-{f}.svg').write_bytes(text.encode());raster(text).save(HERE/f'constructed-{depth}-{f}.png')
    near_im=Image.open(HERE/f'constructed-near-{f}.png').convert('RGBA');far_im=Image.open(HERE/f'constructed-far-{f}.png').convert('RGBA')
    whole=Image.alpha_composite(far_im,near_im);whole.save(HERE/f'constructed-item-{f}.png');full[f]=whole
    assembled=Image.alpha_composite(Image.alpha_composite(far_im,body),near_im);neutral.paste(assembled,(i*512,0))
    b=np.array(body);b[:,:,:3]=np.uint8(np.round(b[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])));red=Image.alpha_composite(Image.alpha_composite(far_im,Image.fromarray(b)),near_im);sheet.paste(red.crop((0,0,512,640)),(i*512,0))
neutral.save(HERE/'constructed-neutral-context.png');sheet.save(HERE/'constructed-red-head-context.png')
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Horns');original_file=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/original['reference_file'];assert sha(original_file)==original['reference_sha256']
actor=next(x for x in json.loads((ROOT/'art/village/sources.json').read_text())['actors'] if x['creature']=='Warden Yrame');resident=actor['native_instances'][0];part=next(p for p in resident['parts'] if (p.get('equipped') or {}).get('blueprint')=='Horns');assert part['id']==288 and part['type']=='Head' and part['manager'] is None
base=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base/ObjectBlueprints');defs=base/'Items.xml';creatures=base/'Creatures.xml'
def node(p,n):return ET.fromstring(re.search(r'<object\s+Name="'+re.escape(n)+r'"(?=\s|>).*?</object>',p.read_text(encoding='utf-8-sig'),re.S).group())
hn=node(defs,'Horns');yn=node(creatures,'Warden Yrame');mutation=next(dict(m.attrib) for m in yn.findall('mutation') if m.get('Name')=='Horns');assert mutation['Variant']=='Horns'
mod=Path('D:/Steam/steamapps/workshop/content/294100/2016436324');donor_base=mod/'Textures/Things/Pawn/Humanlike/HeadAttachments/MiniHorns';gene_path=Path('D:/Steam/steamapps/common/RimWorld/Data/Biotech/Defs/GeneDefs/GeneDefs_Endogenes.xml');gene=next(n for n in ET.parse(gene_path).getroot().findall('GeneDef') if n.findtext('defName')=='Headbone_MiniHorns');rn=gene.find('renderNodeProperties/li')
palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
packet=dict(entry='FIT-YRAME-HORNS-HEAD-0',recorded_at=datetime.now(timezone.utc).isoformat(),original=original,
    creature={k:v for k,v in resident.items() if k!='parts'},race=actor['race_input'],actual_head_binding=part,
    natural_equipment=dict(definition=private(defs),parts=[dict(p.attrib) for p in hn.findall('part')],tags=[dict(p.attrib) for p in hn.findall('tag')],static_mutation=dict(definition=private(creatures),declaration=mutation,level_meaning='Declared level8 is not a horn count. Runtime shape description explicitly says a pair.')),
    body=ref(BODY/'model.json'),frame=dict(canvas=list(SIZE),contact=[256,1078],original_canvas=[512,1024],original_contact=[256,950],padding=[0,128],policy='Pad every facing, source body and masks identically at top; no rescale or independent centering. Preserve original physical pixel mapping. Horn textures use expanded canvas with explicit matching render height/center.'),
    donor=dict(mod='Vanilla Textures Expanded',workshop_id='2016436324',package_id='VanillaExpanded.VTEXE',about=private(mod/'About/About.xml'),load_folders=private(mod/'LoadFolders.xml'),assets={f:private(donor_base/f'MiniHorns_{f}.png') for f in patterns},definition=private(gene_path),defName='Headbone_MiniHorns',nodeClass=rn.findtext('nodeClass'),parentTagDef=rn.findtext('parentTagDef'),default_layer=rn.findtext('drawData/defaultData/layer'),north_layer=rn.findtext('drawData/dataNorth/layer'),role='Actual Biotech directional head-attachment convention and VTE replacement textures: pair front/back, overlapping single profile silhouette and north behind head. Small donor knobs do not replace Qud great grooved horns; donor gene/node logic is not ported.'),
    design='One pair of large tapered grooved bone horns, symmetric in front/back. East projects near/far roots onto same profile crown, with far horn behind original head and near horn above it; no frontal pair pasted onto profile. Curvature and unseen rear surfaces are authored interpretation of the sparse original and pair description.',
    palette=dict(primary='w',detail='W',primary_rgb=palette['w'],detail_rgb=palette['W'],body='w',resolution='TileColor w overrides ColorString y; W is source gold detail, not white. Neutral production textures and separate groove/highlight detail.'),
    scope='Separate mutation/natural-equipment overlay on reusable unmutated female body. Never bake horns, extra legs, freezing hands or named Big morphology into ordinary body. This authoring overlay does not implement a generalized mutation framework.',
    native_acceptance='Pending full-set generation, integrated natural Head288/0 attachment, headgear precedence, physical-frame mapping and Yrame full mutation/outfit assembly.')
write('source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15);board=Image.new('RGB',(1152,650),'#142823');d=ImageDraw.Draw(board);d.text((18,14),'HORNS / Qud original pair + actual directional head attachment + manual correction',font=font,fill='#e3cf43')
im=Image.open(original_file).convert('RGBA').resize((160,240),Image.Resampling.NEAREST);board.paste(im,(80,85),im);d.text((18,360),'QUD / great grooved bone pair',font=font,fill='#e3cf43')
for i,f in enumerate(patterns):
    im=Image.open(donor_base/f'MiniHorns_{f}.png').convert('RGBA');board.paste(im,(360+i*256,30),im);d.text((360+i*256,290),f.upper(),font=font,fill='#e3cf43')
    im=full[f].crop((96,0,416,256));im.thumbnail((240,200));board.paste(im,(355+i*256,355),im)
d.text((18,600),'Profile is near/far overlap, not frontal horns. Fixed body padded128px above; physical size unchanged.',font=font,fill='#e5e8d8');board.save(HERE/'source-comparison.png')
ledger_file=ROOT/'evidence/conversion-ledger.json';ledger=json.loads(ledger_file.read_text());assert ledger['active_entry']==packet['entry'];entry=next(e for e in ledger['entries'] if e['id']==packet['entry'])
for step,action,names in [('source_identity_description_slot_laterality','Resolve actual natural Horns575 on Head288/0, paired grooved-bone description, native TileColor w/detail W and separate declared mutation metadata.',['source-packet.json']),('select_correct_body_and_references','Select original ordinary female body and actual Biotech/VTE directional horn references and layer differences; retain great Qud silhouette.',['source-comparison.png']),('construct_and_overlay_one_item','Rebuild distinct front/profile/rear horn layers. Pad all facing frames equally without resizing body; far profile/rear horns go behind original head.',['constructed-neutral-context.png','constructed-red-head-context.png','pattern-near-east.svg','pattern-far-east.svg','imagegen-prompt.txt'])]:
    entry['process_log'].append(dict(timestamp=packet['recorded_at'],step=step,action=action,inputs=[ref(HERE/'source-packet.json')],outputs=[ref(HERE/n) for n in names],review='Pair count is source-supported. Directional near/far/root overlap is explicit; no frontal pair reused for profile, body mutation or unrecorded body rescale.',result='PASS'))
entry['current_step']='imagegen_refine_in_context_on_unchanged_body';ledger['updated_at']=packet['recorded_at'];ledger_file.write_bytes((json.dumps(ledger,indent=2)+'\n').encode());print('Prepared directional natural horn overlay, source palette and identical top padding; original body unchanged.')
