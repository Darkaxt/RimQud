"""Keep original humanoid arms above mail; keep fleece behind this shirt."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
import numpy as np
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'arm-owner-v2'
SIZE=(768,1152);FACES=['south','east','north']


def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def image(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def save(name,d):(OUT/name).write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())


def tint(im,color):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color)/255));a[a[:,:,3]==0,:3]=0
    return Image.fromarray(a)


assert not OUT.exists();OUT.mkdir()
old=read(HERE/'model.json');bm=read(ROOT/old['base_model']);model=dict(old);model['views']={};model['occlusion_sources']={}
colors={k:tuple(bytes.fromhex(v)) for k,v in read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'].items()}
groups={k:{} for k in ['assembly','palette','mask','overlay']};checks={}
for f in FACES:
    mask=np.array(Image.open(HERE/f'body-visibility-ready-{f}.png').convert('L'))
    source=next(r for r in bm['views'][f] if r['component']=='body' and r['color_role']=='foreground')
    foreground=image(ROOT/source['public_file']);a=np.array(foreground)
    mask[a[:,:,3]==0]=0
    Image.fromarray(mask).save(OUT/f'body-visibility-{f}.png')
    a[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*mask/255));a[a[:,:,3]==0,:3]=0
    overlay=Image.fromarray(a);overlay.save(OUT/f'body-overlay-{f}.png')
    base=image(HERE/f'original-body-{f}.png');cloth=image(HERE/f'intact-mail-{f}.png');detail=image(HERE/f'item-detail-{f}.png')
    assembly=Image.alpha_composite(Image.alpha_composite(base,cloth),overlay)
    native_body=Image.new('RGBA',SIZE)
    for row in sorted(bm['views'][f],key=lambda r:r['layer']):
        color=colors['B'] if row['color_role']=='detail' else colors['w'];native_body.alpha_composite(tint(image(ROOT/row['public_file']),color))
    metal=Image.alpha_composite(tint(cloth,colors['y']),tint(detail,colors['Y']))
    native=Image.alpha_composite(Image.alpha_composite(native_body,metal),tint(overlay,colors['w']))
    for k,im in [('assembly',assembly),('palette',native),('overlay',overlay),('mask',Image.fromarray(mask).convert('RGBA'))]:
        im.save(OUT/f'{k}-{f}.png');groups[k][f]=im
    rows=[dict(r) for r in old['views'][f] if r['component'] in ['item','item-detail','body-overlay']]
    row=next(r for r in rows if r['component']=='body-overlay');rr=ref(OUT/f'body-overlay-{f}.png');row.update(public_file=rr['path'],sha256=rr['sha256'],file=f'yrame-chain-mail-v2-arm-owner-body-overlay-{f}.png')
    model['views'][f]=rows;model['occlusion_sources'][f]=dict(original_body=ref(HERE/f'original-body-{f}.png'),full_mail=ref(HERE/f'intact-mail-{f}.png'),visibility=ref(OUT/f'body-visibility-{f}.png'),overlays=[rr],detail=ref(HERE/f'item-detail-{f}.png'),semantic_owner='Humanoid upper-body/arm foreground plane only. Fleece detail is not an exposed-arm owner and stays below mail.')
    detail_row=next(r for r in old['views'][f] if r['component']=='body-overlay-detail');old_fleece=np.array(image(ROOT/detail_row['public_file']))
    q=(old_fleece[:,:,3]>128)&(np.array(cloth)[:,:,3]>128)
    checks[f]=dict(removed_opaque_fleece_overlap_pixels=int(q.sum()),whole_mail_unchanged=True,original_body_unchanged=True,body_detail_overlay_rows=0)
model.update(source_version=ref(HERE/'model.json'),policy=old['policy']+' Only the original human arm foreground plane may appear above this item; underlying fleece remains below mail.',layer_order='Original body/head including fleece -> full mail -> y/Y metal detail -> original human-arm foreground overlay. No fleece overlay.')
for g in groups.values():g['west (mirror)']=ImageOps.mirror(g['east'])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)


def plate(key,name,title,torso=False):
    out=Image.new('RGB',(1200,500 if torso else 700),'#142823');d=ImageDraw.Draw(out);d.text((18,15),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(groups[key].items()):
        bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im)
        if torso:
            box=(320,240,768,720) if f=='east' else ((0,240,448,720) if f.startswith('west') else (160,240,608,720));display=bg.crop(box).resize((280,300),Image.Resampling.LANCZOS)
        else:display=bg.resize((280,420),Image.Resampling.LANCZOS)
        out.paste(display.convert('RGB'),(10+i*300,55));d.text((15+i*300,380 if torso else 500),f.upper(),font=font,fill='#e3cf43')
    d.text((18,out.height-55),'Original arms above full mail; fleece stays below. Body and garment geometry fixed.',font=font,fill='#e5e8d8');out.save(OUT/name)


plate('assembly','assembly-comparison.png','YRAME / source-bound centauroid mail; original arms own the foreground')
plate('assembly','shared-scale-torso-fit-comparison.png','MATCHED-SCALE FIT / same448 x480 crop and scale in all views',True)
plate('palette','independent-palette-comparison.png','NATIVE y / Y MAIL / original w arms above; B fleece stays below')
plate('mask','body-mask-comparison.png','BODY CLASS MASK / humanoid arms and hands; no fleece ownership')
plate('overlay','body-overlay-comparison.png','ORIGINAL ARM FOREGROUND / full source body remains unchanged')
small=Image.new('RGB',(600,390),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((64,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*150+40,20),thumb);big=thumb.resize((128,192),Image.Resampling.NEAREST);small.paste(big,(i*150+10,140),big);d.text((i*150+5,360),f.upper(),font=font,fill='#e3cf43')
small.save(OUT/'game-scale-review.png')
now=datetime.now(timezone.utc).isoformat();save('model.json',model)
save('ownership-correction.json',dict(recorded_at=now,reason='Native palette revealed fleece restoration beside hands. The shirt exposes original human arms, not fleece; remove the detail/fleece overlay without changing body or full garment.',
     previous=ref(HERE/'model.json'),views=checks,source_body=ref(ROOT/old['base_model']),scope='Late body visibility ownership only; no new generation, garment deformation or production-body redraw.'))
p=ROOT/'evidence/conversion-ledger.json';ledger=read(p);entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry']);assert entry['id']=='FIT-YRAME-CHAIN-MAIL-BODY-0'
entry['process_log'].append(dict(timestamp=now,step='recompose_check_cuffs_attachment_occlusion_all_views',phase='Correct body-role ownership revealed by native tint',action='Keep only the original human-arm foreground above this shirt; fleece detail remains below the complete metal.',inputs=[ref(HERE/'model.json'),ref(HERE/'independent-palette-comparison.png')],outputs=[ref(HERE/'apply-arm-ownership.py')]+[ref(OUT/n) for n in ['model.json','ownership-correction.json','assembly-comparison.png','shared-scale-torso-fit-comparison.png','independent-palette-comparison.png','body-mask-comparison.png','body-overlay-comparison.png']],review='Removed116 south and11 east opaque fleece-over-mail pixels. Original body, full mail, curved cuff geometry and physical frame unchanged; final review pending.',result='REQUIRES REVIEW'))
entry['current_registration']=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'assembly-comparison.png'));ledger['updated_at']=now;p.write_bytes((json.dumps(ledger,indent=2,ensure_ascii=False)+'\n').encode())
print('Corrected original-arm/fleece ownership only; prior candidate preserved and all current facings await final review.')
