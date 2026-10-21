"""Fit one source-bound closed boot pair to Yrame's equipped fore Feet16 group."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,io,json,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];SIZE=(768,1152);FACES=['south','east','north']


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,v):(HERE/name).write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def svg(s):return '<svg xmlns="http://www.w3.org/2000/svg" width="768" height="1152" viewBox="0 0 768 1152">'+s+'</svg>'
def raster(s):return Image.open(io.BytesIO(svg_to_bytes(svg_string=s))).convert('RGBA')
def shape(d,fill='#c5c5c5',width=4):return f'<path d="{d}" fill="{fill}" stroke="#282828" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
def mirror(s):return '<g transform="translate(768 0) scale(-1 1)">'+s+'</g>'


assert not (HERE/'source-packet.json').exists()
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='FIT-YRAME-LEATHER-BOOTS-FEET-16'
entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);be=next(e for e in ledger['entries'] if e['id']=='BODY-YRAME');assert be['generation_ready']
bref=be['current_registration']['model'];assert ref(ROOT/bref['path'])==bref;body=read(ROOT/bref['path'])
previous=read(HERE.parent/'v1/source-packet.json');binding=previous['actual_binding'];assert binding['id']==297 and binding['laterality']==16
assert body['source_anatomy']['fore_group']['boots_instance']==580 and body['source_anatomy']['hind_group']['equipped'] is None
donor=Path(previous['donor_reference']['file']);assert hashlib.sha256(donor.read_bytes()).hexdigest()==previous['donor_reference']['sha256']
glyph=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor/village-originals/leather-boots-reference.png');assert hashlib.sha256(glyph.read_bytes()).hexdigest()==previous['item']['reference_sha256']
now=datetime.now(timezone.utc).isoformat()
upper=dict(
 south='M312 872 Q340 862 368 872 L364 930 Q369 950 364 971 L371 1003 Q378 1035 355 1048 Q330 1055 295 1048 Q280 1042 279 1027 L294 983 Q310 963 310 944Z',
 east='M489 866 Q517 858 544 868 L538 929 Q534 951 544 976 L573 1005 Q585 1030 571 1045 Q552 1057 523 1049 L500 1049 Q482 1043 483 1027 L486 997 Q473 979 480 952 L484 910Z',
 north='M300 856 Q328 846 356 856 L350 917 Q345 944 352 974 L360 1005 Q364 1023 348 1032 H306 Q286 1028 290 1010 L302 972 Q311 945 304 917Z')
sole=dict(
 south='M282 1032 Q323 1045 372 1032 L370 1043 Q359 1053 331 1051 L297 1050 Q282 1045 281 1038Z',
 east='M484 1030 Q528 1044 580 1032 L575 1043 Q555 1053 528 1052 L501 1051 Q484 1046 482 1039Z',
 north='M289 1018 Q325 1028 361 1018 L358 1028 Q350 1034 331 1034 H309 Q291 1031 289 1025Z')
cuff=dict(
 south='M312 872 Q340 862 368 872 L367 887 Q340 897 312 886Z',
 east='M489 866 Q517 858 544 868 L542 883 Q516 893 488 881Z',
 north='M300 856 Q328 846 356 856 L354 871 Q328 881 301 870Z')
seam=dict(
 south='M320 895 Q321 936 316 972 M357 896 Q352 942 356 979 M296 1006 Q330 994 365 1014',
 east='M496 891 Q491 939 494 973 M535 892 Q527 941 538 977 M538 982 Q559 995 567 1014 M490 1009 L494 1028',
 north='M310 882 Q319 926 311 972 M346 883 Q338 927 345 974 M328 881 L329 1016 M297 1007 Q327 995 354 1009')
wire=dict(
 south='M328 897 L348 909 L326 922 L347 935 L324 948 L345 963 M348 897 L328 909 L348 922 L326 935 L347 948 L326 963',
 east='M532 893 L541 905 L530 918 L539 931 L529 945 L540 959 M540 893 L532 905 L541 918 L530 931 L539 945 L531 959',north='')
singles={}
for f in FACES:
    cord=f'<path d="{wire[f]}" fill="none" stroke="#eeeeee" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>' if wire[f] else ''
    s=shape(upper[f])+shape(sole[f],'#858585',3)+shape(cuff[f],'#b3b3b3',3)+f'<path d="{seam[f]}" fill="none" stroke="#858585" stroke-width="2.5" stroke-linecap="round"/>'+cord
    singles[f]=(s,cord)
contract=dict(entry=entry['id'],recorded_at=now,status='PLANNED — visual comparison pending',body=bref,item_source=ref(HERE.parent/'v1/source-packet.json'),frame=body['registration'],
 native_facts='Leather Boots580 on fore Feet297/16 (MultipleLegs::Change). Added hind Feet298/64 is unequipped. Boar leather and recovered gold-wire lacing; actual native w leather/y wire. Native joint/tailoring coordinates unknown.',
 authored_estimates='Closed hoof-shaped footwear, mid-lower-leg shafts and full toe/sole coverage adapt the source boots to selected animal forelegs. Anchors and hidden rear projections are authored, not exported limb coordinates.',
 geometry=dict(uppers=upper,soles=sole,cuffs=cuff,seams=seam,laces=wire,profile_far_translation=[-25,-24]),
 views=dict(
  south=dict(attachment='Two cuffs around the inner/front lower legs, centers approximately340/428 at y878. Do not put boots on the outer/rear pair.',coverage='Closed shafts follow the foreleg shins and cover complete original fore hooves/toes. Soles use the existing1050 contact; no bare hoof or cleft restored over leather.',visibility='Both fore boots in front; the two outer hind hooves stay bare. Natural curved cuff mouths retain original leg entry, with laces on front faces.',depth='Original body -> full paired boots -> original fore-shin cuff-entry pixels only.'),
  east=dict(attachment='Near boot on the foreleg beneath the upright torso, cuff near517,874. Far fore boot is the same physical source translated25px back and24px up, matching overlapping fore stance.',coverage='Near and far fore feet receive closed leather; hind feet nearx170/270 remain bare. Toe housings point screen-right; heel/instep/sole thickness remain plausible.',visibility='Near fore boot occludes much of the far one. Keep any naturally visible far heel/shaft; do not move it merely to show a second whole boot. Narrow front lace edge only.',depth='Original body -> far fore boot -> near fore boot -> original fore-shin entry above the curved cuff. No bare-foot overlay.'),
  north=dict(attachment='Rear projections of the same fore boot pair, behind the visible hind legs; cuffs centered about328/440 at y862 and soles near1034.',coverage='Full fore boot shapes retained underneath. The nearer hind legs/hooves are unequipped and retain original pixels. Added boot thickness may peek beyond the hind silhouette naturally.',visibility='Original hind pair hides most fore footwear. Rear boot heel seams are plain; front wire laces are hidden. Do not duplicate footwear onto the visible hind pair to force a count.',depth='Complete paired fore boots behind the original body/hind legs; separate depth/mask evidence shows the hidden item.'),
  west=dict(attachment='Mirror exact east body, pair and cuff masks together. Same fore Feet297/16 binding.',coverage='Same closed fore pair, bare hind hooves and common physical size.',visibility='Mirrored natural near/far overlap; no invented asymmetry.',depth='Same east depth order after mirroring.')),
 gate='Inspect all contextual views and full hidden sources before extraction/fitting advancement. No bare-foot cutout or second generative item isolation. Native acceptance remains deferred.')
write('fit-contract.json',contract)
packet=dict(entry=entry['id'],workflow='regional-curved-v1',recorded_at=now,creature='Warden Yrame',race='Human-based named mutant; selected sheep-like centauroid body variant.',item=previous['item'],actual_binding=binding,
 body=bref,frame=body['registration'],source_anatomy=body['source_anatomy'],previous_superseded_source=ref(HERE.parent/'v1/source-packet.json'),donor_reference=previous['donor_reference'],fit_contract=ref(HERE/'fit-contract.json'),
 design='One pair of closed boar-leather boots on equipped fore Feet16 only, shaped around the selected hooves. Simple cuff/sole and separate recovered wire; no spurs, plates, open toes or additional hind footwear.',
 palette=previous['palette'],native_acceptance='Pending full-set generation gate, actual Feet297/16 equipment/unequip behavior and full named outfit.')
write('source-packet.json',packet)
cuff_masks=dict(south='M310 832 H371 V873 Q340 891 310 872Z',east='M483 824 H550 V868 Q517 886 485 867Z')
for f in FACES:
    base=Image.new('RGBA',SIZE)
    for row in sorted(body['views'][f],key=lambda r:r['layer']):
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256'];base.alpha_composite(Image.open(ROOT/row['public_file']).convert('RGBA'))
    assert np.array_equal(np.array(base),np.array(Image.open(HERE/f'original-body-{f}.png').convert('RGBA')))
    s,cord=singles[f]
    if f=='east':parts=dict(far='<g transform="translate(-25 -24)">'+s+'</g>',near=s);details=dict(far='<g transform="translate(-25 -24)">'+cord+'</g>',near=cord)
    else:parts=dict(pair=s+mirror(s));details=dict(pair=cord+mirror(cord))
    full=Image.new('RGBA',SIZE);detail=Image.new('RGBA',SIZE)
    for name,content in parts.items():
        text=svg(content);(HERE/f'boot-{name}-{f}.svg').write_bytes(text.encode());part=raster(text);part.save(HERE/f'boot-{name}-{f}.png');full.alpha_composite(part)
        detail.alpha_composite(raster(svg(details[name])))
    full.save(HERE/f'constructed-boots-{f}.png');detail.getchannel('A').save(HERE/f'detail-region-{f}.png')
    if f=='north':
        ma=np.zeros((SIZE[1],SIZE[0]),dtype='uint8');ma[760:1080]=255
    else:
        q=cuff_masks[f];content=q+('' if f=='east' else '')
        text=svg(f'<path d="{q}" fill="white"/>'+ (mirror(f'<path d="{q}" fill="white"/>') if f=='south' else '<g transform="translate(-25 -24)"><path d="'+q+'" fill="white"/></g>'))
        (HERE/f'cuff-visibility-{f}.svg').write_bytes(text.encode());ma=np.array(raster(text).getchannel('A'))
    ba=np.array(base);ma[ba[:,:,3]==0]=0;Image.fromarray(ma).save(HERE/f'body-visibility-{f}.png')
    red=ba.copy();lum=ba[:,:,:3].mean(2);red[:,:,0]=np.uint8(np.maximum(lum,48));red[:,:,1]=np.uint8(lum*.065);red[:,:,2]=np.uint8(lum*.065);red[red[:,:,3]==0,:3]=0
    for name,im in [('constructed-neutral',base),('constructed-red',Image.fromarray(red))]:
        if f=='north':result=Image.alpha_composite(full,im)
        else:result=Image.composite(im,Image.alpha_composite(im,full),Image.fromarray(ma))
        result.save(HERE/f'{name}-{f}.png')
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
# Common foot crop retains the fore and hind groups for placement review.
for prefix,name in [('constructed-neutral','manual-neutral-turnaround.png'),('constructed-red','manual-context-turnaround.png')]:
    sheet=Image.new('RGBA',(1800,390));d=ImageDraw.Draw(sheet)
    for i,f in enumerate(FACES):
        im=Image.open(HERE/f'{prefix}-{f}.png').convert('RGBA').crop((100,740,700,1100));sheet.alpha_composite(im,(i*600,0));d.text((i*600+15,370),f.upper(),font=font,fill='white')
    sheet.save(HERE/name)
write('context-crops.json',dict(canvas=list(SIZE),sheet=[1800,390],crop=[100,740,700,1100],scale=1,policy='Identical physical foot crop in each facing, with intact transparent margin below1050. Rear body depth intentionally hides fore footwear in north.'))
plate=Image.new('RGB',(1800,850),'#142823');d=ImageDraw.Draw(plate);d.text((20,15),'YRAME / Boots580 on fore Feet297/16 ONLY / native glyph + actual VAE icon + current-body construction',font=font,fill='#e3cf43')
im=Image.open(glyph).convert('RGBA').resize((96,144),Image.Resampling.NEAREST);plate.paste(im,(40,75),im)
im=Image.open(donor).convert('RGBA');im.thumbnail((200,200));plate.paste(im,(240,55),im)
for i,f in enumerate(FACES):
    im=Image.open(HERE/f'constructed-boots-{f}.png').convert('RGBA').crop((240,800,620,1080));im.thumbnail((380,280));plate.paste(im,(545+i*410,60),im);d.text((545+i*410,355),'FULL SOURCE / '+f.upper(),font=font,fill='#e3cf43')
d.text((20,410),'Closed boar leather; source gold-wire description, native w/y roles. Icon camera is not a worn-facing reference.',font=font,fill='#e5e8d8')
im=Image.open(HERE/'manual-neutral-turnaround.png').convert('RGBA');plate.paste(im,(0,455),im);plate.save(HERE/'source-reference-construction.png')
for step,phase,names,text in [
 ('source_identity_description_slot_laterality','Resolve actual equipped fore pair and bare added hind pair',['source-packet.json','fit-contract.json'],'Boots580 remain on fore Feet297/16; added hind Feet298/64 is unequipped. Joint/anchor and hoof-tailoring geometry are authored estimates.'),
 ('select_correct_body_and_references','Selected centauroid feet and actual closed-footwear reference',['bare-foot-landmark-review.png','source-reference-construction.png'],'Selected body and original glyph/current donor icon hashes verified. Source icon supplies leather/form cues only; no foot-node support or oblique worn camera inferred.'),
 ('construct_and_overlay_one_item','Full boot pair, closed toes and natural fore/hind depth — review pending',['construct-boots.py','manual-neutral-turnaround.png','manual-context-turnaround.png','context-crops.json'],'Per-view fit contract predates construction. Full near/far boot sources and independent wire retained; no duplicate hind boots and no bare hoof overlay. Manual structural review pending.')]:
    entry['process_log'].append(dict(timestamp=now,step=step,phase=phase,action=text,inputs=[bref,ref(HERE.parent/'v1/source-packet.json')],outputs=[ref(HERE/n) for n in names],review=text,result='REQUIRES REVIEW' if step.startswith('construct') else 'PASS'))
entry['current_step']='construct_and_overlay_one_item';entry['apparel_workflow']['status']='IN PROGRESS';ledger['updated_at']=now
(ROOT/'evidence/conversion-ledger.json').write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Constructed one closed fore boot pair on the fixed body, with bare hind feet and complete hidden rear sources; visual review pending.')
