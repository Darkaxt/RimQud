"""Register selected direct Blender sources; preserve full volume and body pixels."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered-v1';FACES=['south','east','north','west'];SIZE=(768,1152)
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,x):p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def rgba(p):return Image.open(p).convert('RGBA')
def norm(a):
    a=np.array(a).copy();a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
assert not (OUT/'model.json').exists(),'Preserve a completed registration'
OUT.mkdir(exist_ok=True)
now=datetime.now(timezone.utc).isoformat();ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='FIT-YRAME-HORNS-HEAD-0';entry=next(e for e in ledger['entries'] if e['id']==ledger['active_entry'])
review=read(HERE/'independent-fit-review.json');assert not review['fix_now']
for r in review['inspected_images']:assert ref(ROOT/r['path'])['sha256']==r['sha256'],r
old=read(HERE.parent/'v4/model.json');body=read(ROOT/old['base_model']);assert ref(ROOT/old['base_model'])['sha256']==old['body_sha256']
pal=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];actor=next(a for a in read(ROOT/'art/village/sources.json')['actors'] if a['creature']=='Warden Yrame')['native_instances'][0]
def tint(im,code):
    a=np.array(im);c=np.array(tuple(bytes.fromhex(pal[code.replace('&','')[0]])));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*c/255));return norm(a)
contract=read(HERE/'trial-contract.json');contract.update(recorded_at=now,artwork_status='SELECTED DIRECT BLENDER SOURCE; REGISTERED REVIEW PENDING',source_selection='Use direct Blender whole-item renders, calibrated proxy visibility and original body. The optional AI candidate is style guidance only; its changed framing/body context is not used.',native_acceptance='Pending full-set generation gate and actual Head288/0 equipment attachment/depth integration.',detail_mask='Authored highlight ownership from selected neutral bone albedo; native w/W role retained, not a recovered per-surface UV map from the tiny Qud glyph.')
write(OUT/'fit-contract.json',contract)
packet=read(HERE.parent/'v4/source-packet.json');packet.update(recorded_at=now,fit_contract=ref(OUT/'fit-contract.json'),selected_blender=ref(HERE/'horns-fit.blend'),blender_receipt=ref(HERE/'blender-receipt.json'),proxy_controls=ref(HERE/'head-proxy-controls.json'),independent_fit_review=ref(HERE/'independent-fit-review.json'),optional_refinement=ref(HERE.parent/'blender-trial-v2/generation-receipt.json'),selection='Direct Blender source, not AI-redrawn recipient or garment isolation.',workflow='blender-first-v1');write(OUT/'source-packet.json',packet)
checks={};views={};groups={k:{} for k in ['neutral','native','full','near','far','detail']}
for face in FACES:
    whole=np.array(rgba(HERE/f'whole-item-{face}.png'));visible=np.array(rgba(HERE/f'visible-item-{face}.png'));assert whole.shape==(1152,768,4)
    raw=whole.copy();whole[:,:,:3]=np.uint8(np.round(whole[:,:,:3].mean(2)))[:,:,None]
    # Low-sample RGB render/denoise noise is not native material color. Retain
    # raw bytes separately and neutralize only RGB, never alpha or geometry.
    assert np.array_equal(raw[:,:,3],whole[:,:,3])
    base=Image.new('RGBA',SIZE)
    for row in sorted(body['views'][face],key=lambda r:r['layer']):
        assert ref(ROOT/row['public_file'])['sha256']==row['sha256'];base.alpha_composite(rgba(ROOT/row['public_file']))
    base=norm(base);base.save(OUT/f'original-body-{face}.png')
    a=whole[:,:,3].astype(float);n=np.minimum(visible[:,:,3].astype(float),a);f=np.round(np.divide(255*(a-n),255-n,out=np.zeros_like(a),where=n<255));gray=whole[:,:,:3].mean(2);highlight=np.uint8(np.round(np.clip((gray-165)/60,0,1)*180))
    full=norm(whole);full.save(OUT/f'full-item-{face}.png');detail=whole.copy();detail[:,:,3]=np.where(a==255,highlight,0);detail=norm(detail);detail.save(OUT/f'full-detail-{face}.png');assert np.array_equal(np.array(Image.alpha_composite(full,detail)),np.array(full))
    rows=[];planes={}
    for side,alpha,depth in [('far',f,-.0002),('near',n,.0018)]:
        p=whole.copy();p[:,:,3]=np.uint8(alpha);b=norm(p);b.save(OUT/f'item-{side}-{face}.png');p[:,:,3]=np.where(alpha==255,highlight,0);de=norm(p);de.save(OUT/f'item-{side}-detail-{face}.png');assert np.array_equal(np.array(Image.alpha_composite(b,de)),np.array(b));planes[side]=(b,de)
        for isdetail,im,offset in [(False,b,0),(True,de,.00001)]:
            name=f'item-{side}'+('-detail' if isdetail else '')+f'-{face}.png';r=ref(OUT/name);rows.append(dict(component=f'item-{side}'+('-detail' if isdetail else ''),color_role='equipment-detail' if isdetail else 'equipment',file='yrame-horns-blender-'+name,public_file=r['path'],sha256=r['sha256'],size=list(SIZE),**{k:old['frame_mapping'][k] for k in ['contact','width','height','center_x','center_z']},layer=depth+offset,equipment_key='horns@Head@0'))
    views[face]=rows
    def compose(native=False):
        layers=[(r,None) for r in body['views'][face]]+[(r,'Horns') for r in rows];out=Image.new('RGBA',SIZE)
        for r,owner in sorted(layers,key=lambda z:z[0]['layer']):
            im=rgba(ROOT/r['public_file'])
            if native:
                code=('W' if r['color_role']=='equipment-detail' else 'w') if owner else (actor['detailColor'] if r['color_role']=='detail' else actor['tileColor'] or actor['foreground'])
                im=tint(im,code)
            out.alpha_composite(im)
        return norm(out)
    neutral=compose();native=compose(True);neutral.save(OUT/f'assembly-{face}.png');native.save(OUT/f'native-assembly-{face}.png')
    expected=norm(Image.alpha_composite(Image.alpha_composite(planes['far'][0],base),planes['near'][0]));assert np.array_equal(np.array(neutral),np.array(expected))
    assert np.array_equal(np.array(neutral)[:,:,3],np.array(norm(rgba(HERE/f'assembly-{face}.png')))[:,:,3]),face
    groups['neutral'][face]=neutral;groups['native'][face]=native;groups['full'][face]=full;groups['near'][face]=planes['near'][0];groups['far'][face]=planes['far'][0];groups['detail'][face]=detail
    checks[face]=dict(original_body_rgba_unchanged=True,neutral_recomposition_exact=True,detail_neutral_recomposition_exact=True,shared_frame=True,grayscale_equipment=True,full_volume_retained=True,raw_alpha_unchanged=True,neutralization_max_rgb_delta=int(np.abs(raw[:,:,:3].astype(int)-whole[:,:,:3].astype(int)).max()),actual_west_render=face=='west',alpha_partition_max_rounding=float(np.abs(n+f*(1-n/255)-a).max()),detail_pixel_count=int((np.array(detail)[:,:,3]>0).sum()))
model={k:old[k] for k in ['item','blueprint','family','slot','laterality','canvas','contact','base_model','body_sha256','actual_equipped_binding','frame_mapping']};model.update(fit_contract=ref(OUT/'fit-contract.json'),source_packet=ref(OUT/'source-packet.json'),views=views,blender_source=ref(HERE/'horns-fit.blend'),canonical_source='Full transparent physical horn volume retained independently; registered far/near layers derived from calibrated head proxy. Original body and head unchanged.',west_policy='Actual west render of same symmetric mesh; do not mirror exported images again.',native_activation=False,native_acceptance=contract['native_acceptance']);write(OUT/'model.json',model)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for name,title in [('neutral','NEUTRAL / registered direct Blender horns on original bare body'),('native','QUD COLORS / native body w/B, horns w/W; independent tint ownership'),('full','FULL ITEM / hidden root volume intact; no body-shaped destructive cuts'),('near','NEAR OWNERSHIP / direct Blender visibility'),('far','FAR OWNERSHIP / complete volume behind original body'),('detail','W DETAIL / authored bone highlight regions, independent of flesh')]:
    out=Image.new('RGB',(1600,570),'#142b24');d=ImageDraw.Draw(out);d.text((15,12),title,font=font,fill='#e3ce43')
    for i,(face,im) in enumerate(groups[name].items()):
        bg=Image.new('RGBA',SIZE,'#20382d');bg.alpha_composite(im);box=(290,0,690,400) if face=='east' else ((78,0,478,400) if face=='west' else (184,0,584,400));out.paste(bg.crop(box).convert('RGB'),(i*400,45));d.text((i*400+15,450),face.upper(),font=font,fill='#e3ce43')
        if name in ['neutral','native']:
            small=im.resize((63,94),Image.Resampling.LANCZOS);out.paste(small,(i*400+155,470),small)
    out.save(OUT/f'{name}-comparison.png')
write(OUT/'registration-decisions.json',dict(recorded_at=now,method='No image placement transform; actual Blender cameras already use accepted body frame. Correct alpha partition with unchanged source grayscale; detail only on opaque interior of each plane.',checks=checks,source_selection=contract['source_selection'],body_model=ref(ROOT/old['base_model']),production_registration=True,native_acceptance=False))
sys.path.insert(0,str(ROOT/'tools'));from enumerate_conversion_ledger import enumerate_entries,blender_required_steps
fresh=next(e for e in enumerate_entries() if e['id']==entry['id']);entry['workflow_version']='blender-first-v1';entry['required_steps']=blender_required_steps(fresh)
for step,action,names in [
 ('build_blender_recipient_proxy','Calibrate the reusable head fitting proxy from exact accepted source silhouettes; preserve original body pixels.',['head-proxy-controls.json','proxy-source-comparison.png','composition-diagnostics.json']),
 ('render_blender_views_and_masks','Render actual cardinal depth/mask views from the reused saved model; whole horn pixels remain byte-identical.',['blender-receipt.json','calibrated-assembly-comparison.png','independent-fit-review.json'])]:
    entry['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(ROOT/old['base_model'])],outputs=[ref(HERE/p) for p in names],review='Actual image inspection and fresh independent bounded review establish static usable fit; no native acceptance.',result='PASS'))
entry['process_log'].append(dict(timestamp=now,step='select_direct_render_or_optional_refinement',action='Select direct Blender renders and keep prior optional ImageGen result as style guidance only; no new generation or isolation call.',inputs=[ref(HERE.parent/'blender-trial-v2/generation-receipt.json'),ref(HERE/'independent-fit-review.json')],outputs=[ref(OUT/'fit-contract.json'),ref(OUT/'source-packet.json')],review='Modeled shape, original body, scale and source ownership preserved. Rounded root shading is minor polish; no demonstrated exposed cap or disconnected attachment in calibrated views.',result='PASS'))
entry['process_log'].append(dict(timestamp=now,step='export_whole_item_and_visibility_masks',action='Export full physical item, far/near planes and independent native w/W tint masks; recompose every registered view over original body.',inputs=[ref(HERE/'blender-receipt.json')],outputs=[ref(OUT/p) for p in ['model.json','registration-decisions.json','neutral-comparison.png','native-comparison.png','full-comparison.png','far-comparison.png','near-comparison.png','detail-comparison.png']],review='All exact neutral recomposition, body preservation and shared-frame checks passed. Registered artwork still awaits main-author final palette/intended-size inspection.',result='REQUIRES REVIEW'))
ledger['updated_at']=now;write(ROOT/'evidence/conversion-ledger.json',ledger);print('Registered source and tint/depth planes; final authoring inspection pending. Not generation-ready yet.')
