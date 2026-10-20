"""Reusable closed boar-leather boots, separate from mutation-part placement."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-female/v2';DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor');MOD=Path('D:/Steam/steamapps/workshop/content/294100/1814987817');SIZE=(512,1024);FACES=['south','east','north']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+s+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
def shape(d,fill='#d2d2d2',width=5):return f'<path d="{d}" fill="{fill}" stroke="#252525" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>'
def mirror(s,pivot=505):return '<g transform="translate('+str(pivot)+' 0) scale(-1 1)">'+s+'</g>'
uppers={
 'south':'M146 778 Q188 766 234 778 L227 842 Q217 873 220 895 L238 922 Q247 943 219 947 H143 Q118 944 124 929 L146 900 Q154 877 149 851Z',
 'east':'M177 778 Q224 764 274 778 L269 848 Q262 881 272 895 L332 916 Q349 925 344 941 Q339 947 321 947 H201 Q183 945 185 933 L193 904 Q199 884 194 855Z',
 'north':'M146 778 Q188 766 234 778 L226 842 Q215 878 224 906 L235 925 Q242 941 218 947 H157 Q124 943 126 928 Q149 909 153 897 Q160 876 153 852Z'}
soles={
 'south':'M125 929 Q178 943 239 929 L240 938 Q237 947 217 947 H143 Q124 944 123 938Z',
 'east':'M185 933 Q260 944 345 931 L345 940 Q339 947 321 947 H201 Q184 945 184 938Z',
 'north':'M127 929 Q180 941 237 928 L238 937 Q235 947 217 947 H157 Q126 943 125 937Z'}
cuffs={
 'south':'M146 778 Q188 766 234 778 L233 793 Q188 783 147 793Z',
 'east':'M177 778 Q224 764 274 778 L273 793 Q225 783 179 794Z',
 'north':'M146 778 Q188 766 234 778 L232 793 Q188 783 147 793Z'}
seams={
 'south':'M158 799 Q156 854 161 890 M221 800 Q213 850 210 890 M150 909 Q186 899 223 915',
 'east':'M188 800 Q201 849 204 896 M260 801 Q253 858 264 898 M263 902 Q284 902 304 916 M201 912 L205 927',
 'north':'M159 800 Q166 855 161 900 M222 800 Q213 858 219 902 M188 797 Q188 862 187 923 M143 917 Q186 905 226 918'}
wire={
 'south':'M172 806 L207 820 L170 835 L205 850 L169 865 L201 881 M207 806 L172 820 L207 835 L171 850 L205 865 L173 881',
 'east':'M247 802 L261 815 L247 829 L261 843 L247 856 L261 870 L251 882 M261 802 L247 815 L261 829 L247 843 L261 856 L249 870 L259 882',
 'north':''}
sheet=Image.new('RGBA',(1536,1024));neutral=sheet.copy();zoom=sheet.copy();individuals={}
for i,f in enumerate(FACES):
 upper=shape(uppers[f]);sole=shape(soles[f],'#858585',4);cuff=shape(cuffs[f],'#bbbbbb',4);seam=f'<path d="{seams[f]}" fill="none" stroke="#838383" stroke-width="3" stroke-linecap="round"/>'
 cord=f'<path d="{wire[f]}" fill="none" stroke="#ededed" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>' if wire[f] else ''
 single=upper+sole+cuff+seam+cord;whole=single if f=='east' else single+mirror(single,505 if f=='south' else 504)
 pattern=svg(whole);(HERE/f'pattern-{f}.svg').write_text(pattern,encoding='utf-8');boots=raster(pattern);boots.save(HERE/f'constructed-cloth-{f}.png')
 # Back view hides front laces; no invented back-facing wire ladder.
 detail=cord if f=='east' else cord+mirror(cord,505 if f=='south' else 504)
 raster(svg(detail)).getchannel('A').save(HERE/f'detail-region-{f}.png')
 if f=='east':parts={'profile':single}
 else:parts={'left':single,'right':mirror(single,505 if f=='south' else 504)}
 individuals[f]={}
 for name,s in parts.items():
  p=HERE/f'boot-region-{name}-{f}.png';raster(svg(s)).getchannel('A').save(p);individuals[f][name]=ref(p)
 # Closed boot covers the foot: no body/skin overlay is restored over its upper.
 Image.new('L',SIZE).save(HERE/f'body-visibility-{f}.png')
 body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');ba=np.array(body);red=ba.copy();red[:,:,:3]=np.uint8(np.round(ba[:,:,:3].mean(2)[:,:,None]*np.array([1,.12,.16])))
 for target,base in [(sheet,Image.fromarray(red)),(neutral,body)]:
  assembled=Image.alpha_composite(base,boots);target.paste(assembled,(i*512,0))
  if target is sheet:zoom.paste(assembled.crop((96,700,416,960)).resize((512,416),Image.Resampling.LANCZOS),(i*512,304))
sheet.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-feet-context.png')
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Leather Boots');assert sha(DONOR/original['reference_file'])==original['reference_sha256']
actor=next(a for a in json.loads((ROOT/'art/village/sources.json').read_text())['actors'] if a['creature']=='Warden Yrame');resident=actor['native_instances'][0];binding=next(p for p in resident['parts'] if (p.get('equipped') or {}).get('blueprint')=='Leather Boots');dp=MOD/'Textures/Things/Footwear/Boots.png'
write(HERE/'source-packet.json',dict(entry='FIT-YRAME-LEATHER-BOOTS-FEET-16',workflow='regional-curved-v1',recorded_at=datetime.now(timezone.utc).isoformat(),creature='Warden Yrame',race='Human; ordinary female baseline for reusable footwear',item=original,actual_binding=binding,captured_resident=resident,body=ref(BODY/'model.json'),
 donor_reference=dict(file=str(dp),sha256=sha(dp),mod='Vanilla Apparel Expanded',workshop_id='1814987817',about_sha256=sha(MOD/'About/About.xml'),role='Actual inventory boot icon: closed leather shaft/toe/sole and neutral outlines. Oblique inventory camera is not a worn cardinal reference and no directional foot-node support is inferred.'),
 design='Closed mid-calf boar-leather boots with laced fronts, simple cuff and sole. Source pair reconstructed at fixed feet; bright cord is separate from leather. Back view shows heel seam and hides front laces. No buckles, armor plates, spurs, open toes or added costume.',
 palette=dict(foreground='w',detail='y',detail_assignment='Gold wire by native description, through actual y detail role; no gold/yellow baked into neutral texture.'),
 frame=dict(canvas=[512,1024],contact=[256,950],ground='Boot sole contour approximately y950; original body/contact unchanged',camera='Strict front/south, right profile/east, back/north; west mirrors east',foot_zoom_crop=[96,700,416,960],foot_zoom_size=[512,416],foot_zoom_origin=[0,304]),
 individual_boot_regions=individuals,
 mutations='Actual equipped Feet297 has laterality16 and manager515::MultipleLegs::Change. Baseline pair and individual boot sources do not resolve this mutation placement. Preserve exact binding and defer duplicated foot placement/occlusion to named mutation assembly and final native gate. No remap to Feet0 or claim that only two native feet exist.',
 native_acceptance='Pending full-set generation gate and mutation-specific foot placement'))
plate=Image.new('RGB',(1536,1080),'#142823');d=ImageDraw.Draw(plate);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',17);d.text((24,18),'YRAME > ORDINARY HUMAN BASE > LEATHER BOOTS / source, actual mod and own views',font=font,fill='#e3cf43')
orig=Image.open(DONOR/original['reference_file']).convert('RGBA').resize((160,240),Image.Resampling.NEAREST);plate.paste(orig,(24,95),orig);don=Image.open(dp).convert('RGBA');box=don.getchannel('A').point(lambda a:255 if a>128 else 0).getbbox();don=don.crop(box);don.thumbnail((240,240));plate.paste(don,(260,100),don)
for y,t in [(355,'Qud glyph / normalized primary-detail'),(385,'Boar leather; recovered gold-wire laces'),(415,'Actual Feet297 / item580 / laterality16'),(445,'Native leather w / wire y'),(475,'Mod icon is inventory-only, not worn art'),(505,'Mutation-managed binding stays unresolved')]:d.text((24,y),t,font=font,fill='#e5e8d8')
for i,f in enumerate(FACES):
 im=neutral.crop((i*512,0,(i+1)*512,1024));bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);plate.paste(bg.convert('RGB').resize((256,512)),(535+i*330,95));d.text((535+i*330,635),'CONSTRUCTED / '+f.upper(),font=font,fill='#e3cf43');plate.paste(bg.crop((96,700,416,960)).convert('RGB').resize((288,234)),(519+i*330,690))
d.text((24,1025),'One closed footwear item on fixed unclothed base. Individual boot sources retained; no mutated-foot placement or native claim.',font=font,fill='#e5e8d8');plate.save(HERE/'source-comparison.png')
print('Prepared source-bound closed boots, neutral laces, individual boot regions and exact mutation binding.')
