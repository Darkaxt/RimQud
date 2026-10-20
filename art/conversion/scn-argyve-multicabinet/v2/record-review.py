"""Reconcile the complete two-layout furniture authoring outcome, not native use."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1';OUT=HERE/'registered-final'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
assert not (OUT/'authoring-review.json').exists()
model=json.loads((OUT/'model.json').read_text());packet=json.loads((HERE/'source-packet.json').read_text());checks={}
for variant in model['variants']:
    n=variant['variant'];assert set(variant['views'])=={'south','east','north','west'}
    for f,view in variant['views'].items():
        primary=read(ROOT/view['primary']['path']);a=np.array(primary);weight=np.array(Image.open(ROOT/view['detail_weight']['path']).convert('L'));coverage=np.array(Image.open(ROOT/view['coverage']['path']).convert('L'))
        assert primary.size==(256,256) and np.array_equal(a[:,:,3],coverage)
        assert np.array_equal(a[:,:,0],a[:,:,1]) and np.array_equal(a[:,:,1],a[:,:,2]);assert not weight[coverage==0].any()
        if f=='south':assert np.array_equal(a,np.array(read(OLD/f'registered/variant-{n}-primary-neutral.png')))
        else:
            manual=read(HERE/f'variant-{n}-ownership-{f}.png').convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA');assert np.array_equal(coverage,np.array(manual)[:,:,3])
        ratio=weight.astype(float)/255;fg=np.frombuffer(bytes.fromhex('40a4b9'),dtype=np.uint8);dc=np.frombuffer(bytes.fromhex('cfc041'),dtype=np.uint8);rgb=np.uint8(np.round((fg[None,None,:]*(1-ratio[:,:,None])+dc[None,None,:]*ratio[:,:,None])*a[:,:,:1]/255));rgb[coverage==0]=0
        assert np.array_equal(np.dstack([rgb,coverage]),np.array(read(OUT/f'variant-{n}'/f/'native-c-W-preview.png')))
        for value in view.values():
            if isinstance(value,dict) and 'path' in value:assert ref(ROOT/value['path'])['sha256']==value['sha256']
        assert view['source_cell']==[16,24] and view['authored_anchor']==[8,16] and not view['native_activation']
        checks[f'{n}/{f}']=dict(neutral_rgb=True,source_palette_formula=True,exact_coverage=True,shared_cell_pivot=True,retained_selected_front=f=='south',native_activation=False)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
plate=Image.new('RGB',(1440,700),'#142823');d=ImageDraw.Draw(plate);d.text((18,14),'CAMERA / actual installed directional VFE reference, accepted Qud front, authored complete end',font=font,fill='#e3cf43')
for i,f in enumerate(['south','east','north']):
    im=read(Path(packet['directional_reference']['textures'][f]['path']));big=im.resize((256,256),Image.Resampling.NEAREST);plate.paste(big,(20+i*280,75),big);d.text((20+i*280,350),f'REFERENCE / {f.upper()}',font=font,fill='#e3cf43')
for x,f,label in [(870,'south','RETAINED FRONT'),(1150,'east','AUTHORED END')]:
    im=read(OUT/'variant-1'/f/'native-c-W-preview.png').resize((256,384),Image.Resampling.LANCZOS);plate.paste(im,(x,55),im);d.text((x,465),label,font=font,fill='#e3cf43')
for i,line in enumerate(['Reference: Graphic_Multi, drawSize2x2, footprint1x1; alpha widths124/83/124 on256-square frames.',
 'Reference transparent margins accounted for. Qud depth8.8 / front14 is an explicit authored estimate.',
 'Accepted fronts have parallel verticals and shallow cap bevel; no three-quarter redraw is needed.',
 'New ends retain broad panel volume; rear has no invented drawers. Both source cosmetic layouts are preserved.',
 'Extra directions unbound. No copied donor research mechanic, footprint, inventory or runtime rotation.']):d.text((18,525+i*30),line,font=font,fill='#e5e8d8')
plate.save(HERE/'reference-camera-comparison.png')
reason=('Reviewed source description and both original cosmetic layouts, actual installed VFE S/E/N reference with Graphic_Multi/drawSize/footprint/margins, accepted-front camera, authored substantial end depth, front-guided constructed/refined E/N/W, structural reviews before extraction, same-material transfer and its detail-luminance correction, exact coverage and independent neutral c/W ownership. Selected front pixels are unchanged. Rear/end surfaces and depth remain authored interpretations, with no new drawer/open states. Eight views share a cell/pivot; native container, placement, orientation and palette acceptance remain pending full-set generation.')
now=datetime.now(timezone.utc).isoformat();write(OUT/'authoring-review.json',dict(timestamp=now,status='PASS',scope='Complete entry generation authoring only',reason=reason,checks=checks,new_imagegen_calls=2,retained_previous_front_generations=2,patch='Generated geometry/background excluded; manual seams and constructed coverage retained. Initial gold luminance transfer superseded; original registered trial retained.',native_acceptance=model['native_acceptance']))
write(HERE/'artifact-manifest.json',dict(artifacts=[ref(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p!=HERE/'artifact-manifest.json']))
p=ROOT/'evidence/conversion-ledger.json';d=json.loads(p.read_text());ident='SCN-ARGYVE-MULTICABINET';assert d['active_entry']==ident;e=next(e for e in d['entries'] if e['id']==ident)
def event(step,action,ins,outs,review=reason,result='PASS',**extra):
    e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(HERE/n) for n in ins],outputs=[ref(HERE/n) for n in outs],review=review,result=result,**extra))
event('select_render_reference_or_document_no_equivalent','Inspect installed directional textures with actual current1.6 definition and LoadFolders; measure alpha bounds in shared draw frame. Resolve earlier shallow-cap camera review without regenerating accepted fronts.',[],['source-packet.json','reference-camera-comparison.png'])
event('construct_faithful_shape','Preserve two selected front designs, author missing full-width side/rear surfaces with explicit inferred depth and topbox/bracket relationships. Keep original two cosmetic states.', ['source-packet.json'],['construct-turnarounds.py','constructed-all-layouts.png','manual-structural-review.json'])
event('create_front_side_back_furniture_views','Construct complete S/E/N/W sets per layout from selected fronts in common frame, including opposite front-edge lips and topbox rear location.', ['source-packet.json'],[f'variant-{n}-front-guided-turnaround.png' for n in [1,2]])
for n in [1,2]:
    raw=f'variant-{n}-refined-turnaround-raw.png';review=f'variant-{n}-structural-review.json';jr=json.loads((HERE/review).read_text())
    event('refine_materials_and_form',f'Actual built-in ImageGen contextual turnaround refinement for cosmetic layout{n}; existing selected front supplied as anchor.',[f'variant-{n}-front-guided-turnaround.png',f'variant-{n}-turnaround-prompt.txt'],[raw,review],review=jr['review'],tool='image_gen.imagegen',prompt_file=ref(HERE/f'variant-{n}-turnaround-prompt.txt'),generation_file=jr['generated_file'],settings=dict(transparent_background=True,referenced_image_paths=[str(HERE/f'variant-{n}-front-guided-turnaround.png'),'D:/Steam/steamapps/workshop/content/294100/1718190143/Textures/NewThings/Misc/FilingCabinet/FilingCabinet_south.png']))
event('extract_register_color_coverage','Transfer same-material luminance into fixed new-view geometry, exclude generated background/halo, retain manual seams and exact original fronts. Preserve initial material transfer; correct gold normalization to match front extraction without another AI redraw.', ['source-packet.json','variant-1-refined-turnaround-raw.png','variant-2-refined-turnaround-raw.png'],['register-turnarounds.py','registered/all-layouts-native.png','registered-final/model.json','registered-final/registration-decisions.json','registered-final/all-layouts-neutral.png','registered-final/all-layouts-detail.png','registered-final/all-layouts-coverage.png'])
event('visual_review_identity_and_connections_at_game_scale','Inspect complete eight-view art outcome at enlarged and16x24/24x36/32x48sizes; reconcile front continuity, source states, volume, neutral layers, color roles, shared pivot and complete coverage.', ['registered-final/model.json'],['registered-final/all-layouts-native.png','registered-final/authoring-review.json','artifact-manifest.json'])
event('native_state_review','Keep source random cosmetic selection, container inventory/smart-use, occlusion/solidity and actual placement/extra-view bindings behind full-set generation gate.', ['registered-final/model.json'],[],review='No native activation or game/harness launch. Additional directions are authoring assets only; the entry remains UNFINISHED pending native acceptance.',result='DEFERRED UNTIL ALL GENERATED')
e.update(status='UNFINISHED',generation_ready=True,current_step='native_state_review',known_issues=[],art_review=dict(status='PASS',reason=reason),current_registration=dict(model=ref(OUT/'model.json'),plate=ref(OUT/'all-layouts-native.png')),registration_summary='Both actual multicabinet layouts now have source-bound S/E/N plus explicit W. Existing irregular front pixels retained; substantial authored side depth informed by actual directional render metadata. Front-guided refinement, structural reviews, material correction, neutral color roles and all-view evidence logged. Extra directions unbound; native container/placement/state acceptance pending.',native_acceptance=model['native_acceptance'],camera_review=dict(status='PASS',classification='CARDINAL_SOURCE_BOUND',reason='Straight fronts and shallow bevel retained after actual donor comparison. Full end depth explicitly authored; parallel structural axes and common frame.',evidence=ref(HERE/'reference-camera-comparison.png')))
e['furniture_views'].update(completed_views=['south','east','north','west'],west_policy='Explicit authored west with opposite front-edge lip; source topbox/rear relationships retained.',native_binding='Two native cosmetic layouts retained; south proposed fixed tile, additional directions unbound. No runtime rotation activation.')
next_id='SCN-BED';ne=next(e for e in d['entries'] if e['id']==next_id);ne.update(status='IN PROGRESS',current_step=ne['required_steps'][0]);d.update(active_entry=next_id,updated_at=now);assert [a['id'] for a in d['entries'] if a['status']=='IN PROGRESS']==[next_id];write(p,d)
print('Multicabinet complete as generation authoring; native acceptance pending. Bed is sole active entry.')
