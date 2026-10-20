"""Source-bound sandals on existing paired feet, with sole/strap body ownership."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, sys, io
import numpy as np
from PIL import Image
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
BODY=ROOT/'art/conversion/body-human-female/v2'
DONOR=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')
MOD=Path('D:/Steam/steamapps/workshop/content/294100/1814987817')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=sha(p))
def svg(x):return '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024">'+x+'</svg>'
def raster(s):return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=s,skip_system_fonts=True))).convert('RGBA')
def path(d,fill='#d7d7d4',stroke=True):return '<path d="'+d+'" fill="'+fill+'"'+(' stroke="#252525" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"' if stroke else '')+'/>'
def pair(x,pivot=512):return x+'<g transform="translate('+str(pivot)+' 0) scale(-1 1)">'+x+'</g>'

sole={
 'south':pair(path('M160 887 Q179 885 195 900 L219 932 Q223 946 199 950 L145 950 Q122 946 128 932 L150 906Z')),
 'east':path('M199 910 Q216 910 240 916 L329 931 Q342 941 335 950 L203 950 Q190 946 193 934Z'),
 'north':pair(path('M161 893 Q186 891 205 909 L216 935 Q219 947 199 950 H162 Q145 947 151 932Z'),505)}
strap_paths={
 'south':pair(path('M153 890 Q176 883 196 896 L203 908 Q181 896 152 903Z')+path('M143 915 L151 907 L208 931 L203 940Z')+path('M187 904 L196 909 L145 940 L137 933Z')),
 'east':path('M199 881 Q231 878 269 893 L272 904 Q234 891 198 894Z')+path('M202 891 L213 892 L222 938 Q217 943 207 940Z')+path('M261 876 Q268 881 274 888 L285 938 Q279 944 269 941 L259 908 Q256 895 257 884Z')+path('M289 897 Q299 900 308 905 L325 940 Q320 946 312 945 L299 920Z'),
 'north':pair(path('M160 884 Q178 881 197 889 L201 903 Q179 896 159 899Z')+path('M158 913 Q180 925 209 914 L214 929 Q182 940 153 927Z')+path('M178 897 L187 898 L188 929 L179 929Z'),505)}
# The full sole remains intact; the original foot is restored over it except
# where the real straps physically cover skin. These are not leg-shaped cuts.
full=Image.new('RGBA',(1536,1024));neutral=Image.new('RGBA',(1536,1024));zoom=Image.new('RGBA',(1536,1024))
for i,f in enumerate(sole):
    main=svg(sole[f]+strap_paths[f]);(HERE/f'pattern-{f}.svg').write_bytes(main.encode());cloth=raster(main);cloth.save(HERE/f'constructed-cloth-{f}.png')
    # Remove stroke color only for the coverage layer; outlines remain in cloth.
    detail_svg=svg(strap_paths[f].replace('#d7d7d4','white').replace('#252525','white'))
    (HERE/f'strap-coverage-{f}.svg').write_bytes(detail_svg.encode());strap=raster(detail_svg).getchannel('A');strap.save(HERE/f'detail-region-{f}.png')
    feet=svg('<rect x="96" y="800" width="320" height="153" fill="white"/>');(HERE/f'foot-body-region-{f}.svg').write_bytes(feet.encode());foot=raster(feet).getchannel('A')
    mask=Image.fromarray(np.uint8(np.round(np.array(foot).astype(float)*(1-np.array(strap)/255))));mask.save(HERE/f'body-visibility-{f}.png')
    body=Image.open(BODY/f'selected-{f}.png').convert('RGBA');a=np.array(body);gray=a[:,:,:3].mean(axis=2);a[:,:,:3]=np.uint8(np.round(gray[:,:,None]*np.array([1,.12,.16])));red=Image.fromarray(a)
    for target,base in [(full,red),(neutral,body)]:
        out=Image.composite(base,Image.alpha_composite(base,cloth),mask);target.paste(out,(i*512,0))
        if target is full:
            crop=out.crop((96,640,416,960)).resize((512,512),Image.Resampling.LANCZOS);zoom.paste(crop,(i*512,256))
full.save(HERE/'constructed-red-context.png');neutral.save(HERE/'constructed-neutral-context.png');zoom.save(HERE/'constructed-red-feet-context.png')
original=next(x for x in json.loads((ROOT/'evidence/village-reference-index.json').read_text())['entries'] if x['blueprint']=='Sandals')
assert sha(DONOR/original['reference_file'])==original['reference_sha256']
bindings=[]
for actor in json.loads((ROOT/'art/village/sources.json').read_text())['actors']:
 for resident in actor['native_instances']:
  for part in resident['parts']:
   if (part.get('equipped') or {}).get('blueprint')=='Sandals':bindings.append(dict(actor=actor['creature'],gender=resident['gender'],instance=resident['instance'],part=part))
packet=dict(entry='FIT-HUMAN-FEMALE-SANDALS-FEET-0',workflow='regional-curved-v1',recorded_at=datetime.now(timezone.utc).isoformat(),item=original,observed_bindings=bindings,body=ref(BODY/'model.json'),
 donor=dict(package='Vanilla Apparel Expanded',about_sha256=sha(MOD/'About/About.xml'),private_path=(MOD/'Textures/Things/Footwear/Shoes.png').as_posix(),sha256=sha(MOD/'Textures/Things/Footwear/Shoes.png'),role='Actual mod inventory shoe icon supplies compact sole/material/outline convention only, not worn directional foot anatomy. No exact worn-sandal equivalent selected.'),
 design='Open strapped sandals, lightly cracked thin soles from gravel walking; no closed shoes or laces copied from donor. Crossed front straps, ankle band and rear heel straps are authored interpretations. Both feet share the single native Feet/0 item; profile far foot remains occluded by the registered body rather than invented.',
 palette=dict(foreground='y',detail='w',detail_assignment='Straps; sole remains primary. Neutral assets retain separate masks and native equipment-detail ownership.'),
 frame=dict(canvas=[512,1024],contact=[256,950],sole_bottom=950,body_unchanged=True,zoom_crop=[96,640,416,960],zoom_scale=1.6,zoom_origin_y=256,west='Mirror east; symmetric strapped pair, no handed accessories'),
 coverage='Whole sole before fitting; original foot body overlays sole except where straps cover skin. Full sandal and independent foot/strap masks remain separate. Real open-sandal skin exposure is deliberate design, not a body-colored garment patch.',
 native_acceptance='Pending all-conversions gate; no foot bones, animation support or outfit precedence inferred from this art')
(HERE/'source-packet.json').write_bytes((json.dumps(packet,indent=2)+'\n').encode())
print('Prepared corrected female sandals v2: complete soles/straps, foot ownership, shared contact and enlarged contextual source.')
