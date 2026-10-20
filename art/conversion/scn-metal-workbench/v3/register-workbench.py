"""Register shared steel/stock components and single-coverage native color states."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,importlib.util,shutil,sys,xml.etree.ElementTree as ET
import numpy as np
from scipy import ndimage
from PIL import Image,ImageDraw,ImageFont
sys.path.insert(0,'E:/Temp/rimqud-conversion-runtime/python-libs')
from resvg_py import svg_to_bytes
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'registered';OUT.mkdir(exist_ok=True)
def read(p):return Image.open(p).convert('RGBA')
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
assert not (OUT/'model.json').exists()
rawpath=Path('C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb/exec-3e0690be-cb17-4cda-9e86-c0c1b25009a2.png');shutil.copyfile(rawpath,HERE/'refined-occupied-raw.png');raw=read(HERE/'refined-occupied-raw.png')
review='Inspected full actual occupied refinement before extraction: S/N slotted stock plate plus small mark, opposite stock positions, E plate hiding the mark and W mark visible, broad solid bench ends retained. Stock has readable metal volume without inventing an item identity. Generated bench repaint, new shadows, shifted panel registration and fringes are excluded. Retain every selected empty base and source S stock; sample only new E/N/W stock material into fixed coverage. Add an editable rim to the constructed N slot, matching the source open slot rather than relying on generated boundary.'
write(HERE/'occupied-first-structural-review.json',dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS FOR STOCK MATERIAL',generated_file=str(rawpath),raw=ref(HERE/'refined-occupied-raw.png'),prompt_file=ref(HERE/'occupied-turnaround-prompt.txt'),review=review,frame=list(raw.size),native_validation=False))
# Preserve unpatched construction. Add only a narrow rim outside its existing slot.
svg=(HERE/'constructed-north-stock.svg').read_text();node=ET.fromstring(svg);slot=node.find('.//{http://www.w3.org/2000/svg}mask/{http://www.w3.org/2000/svg}path').get('d');pos=svg.rfind('</g>');svg=svg[:pos]+f'<path d="{slot}" fill="none" stroke="#756b32" stroke-width=".12" mask="url(#slot)"/>'+svg[pos:];(HERE/'patched-north-stock.svg').write_bytes(svg.encode());(HERE/'patched-north-stock.png').write_bytes(svg_to_bytes(svg_string=svg));a=np.array(read(HERE/'patched-north-stock.png'));a[:,:,:3]=a[:,:,:3].max(2)[:,:,None];a[a[:,:,3]==0,:3]=0;Image.fromarray(a).save(HERE/'patched-north-stock-neutral.png')
helperpath=ROOT/'art/conversion/scn-chest1/v2/select-dark-wood-material.py';spec=importlib.util.spec_from_file_location('fixed_material',helperpath);helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
def components(mask):
    labels,n=ndimage.label(mask);rows=[]
    for k in range(1,n+1):
        ys,xs=np.where(labels==k)
        if len(xs)>=5:rows.append((len(xs),(int(xs.min()),int(ys.min()),int(xs.max())+1,int(ys.max())+1)))
    return sorted(rows,reverse=True)
selection={};stockmasters={}
for i,f in enumerate(['south','east','north','west']):
    if f=='south':stockmasters[f]=read(HERE/'selected-south-stock-neutral.png');selection[f]=dict(rule='Retain actual selected v2 front stock at shared0.95registration; no new AI redraw accepted.');continue
    col,row=i%2,i//2;panel=raw.crop((round(col*raw.width/2),round(row*raw.height/2),round((col+1)*raw.width/2),round((row+1)*raw.height/2)));panel.save(HERE/f'occupied-generated-{f}-material-panel.png');a=np.array(panel).astype(float);gold=(a[:,:,0]-a[:,:,2]>12)&(a[:,:,1]-a[:,:,2]>12)&(a[:,:,3]>128);sources=components(gold)
    pattern=np.array(read(HERE/('patched-north-stock-neutral.png' if f=='north' else f'constructed-{f}-stock-neutral.png')));targets=components(pattern[:,:,3]>128);assert len(sources)>=len(targets);mapped=Image.new('RGBA',(512,768));mapping=[]
    for (_,sb),(_,tb) in zip(sources,targets):
        material=panel.crop(sb).resize((tb[2]-tb[0],tb[3]-tb[1]),Image.Resampling.LANCZOS);mapped.alpha_composite(material,(tb[0],tb[1]));mapping.append(dict(source_material_bounds=list(sb),target_component_bounds=list(tb)))
    mapped.save(HERE/f'occupied-{f}-mapped-material.png');own=pattern.copy();own[:,:,:3]=255;master,stats=helper.select(mapped,own,pattern);master.save(HERE/f'selected-{f}-stock-neutral.png');stockmasters[f]=master;selection[f]=dict(mapping=mapping,stats=stats,rule='Component bounds transform RGB material coordinates only; final stock alpha/placement/openings/ink copied from fixed projected construction. Internal top role is all stock, wood unused. Gold is removed by max(R,G) luminance; no second AI isolation.')
write(HERE/'occupied-material-selection.json',dict(helper=ref(helperpath),views=selection,north_slot_patch=ref(HERE/'patched-north-stock.svg'),generated_bench_repaint='Not used. Occupied and empty share the exact same selected bench per facing.'))
packet=json.loads((HERE/'source-packet.json').read_text());palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette'];views={};groups={k:{} for k in ['empty-neutral','occupied-neutral','stock-neutral','coverage','detail-weight','empty-native-c','occupied-upper-c','occupied-lower-w','occupied-lower-y','occupied-upper-w']};checks={}
def production(im):
    a=np.array(im.convert('RGBa').resize((256,256),Image.Resampling.LANCZOS).convert('RGBA'));a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)))[:,:,None];a[a[:,:,3]==0,:3]=0;return Image.fromarray(a)
for f in ['south','east','north','west']:
    folder=OUT/f;folder.mkdir(exist_ok=True);base_master=read(HERE/f'shared-{f}-base-neutral.png');stock_master=stockmasters[f];base_master.save(folder/'base-neutral-master.png');stock_master.save(folder/'stock-neutral-master.png');base=production(base_master);stock=production(stock_master);base.save(folder/'base-neutral.png');stock.save(folder/'stock-neutral.png');b=np.array(base).astype(float)/255;s=np.array(stock).astype(float)/255;ab=b[:,:,3];ast=s[:,:,3];lb=b[:,:,0];ls=s[:,:,0];alpha=ast+ab*(1-ast);premult=ls*ast+lb*ab*(1-ast);lum=np.divide(premult,alpha,out=np.zeros_like(alpha),where=alpha>0);weight=np.divide(ls*ast,premult,out=np.zeros_like(alpha),where=premult>0);weight[(premult==0)&(ast>0)]=1
    states={};errors={}
    for state in ['empty','occupied']:
        if state=='empty':a=np.array(base);ratio=np.zeros_like(alpha)
        else:a=np.uint8(np.round(np.dstack([lum,lum,lum,alpha])*255));ratio=weight
        ratio=np.uint8(np.clip(np.round(ratio*255),0,255));ratio[a[:,:,3]==0]=0;a[a[:,:,3]==0,:3]=0;primary=Image.fromarray(a);primary.save(folder/f'{state}-primary-neutral.png');Image.fromarray(a[:,:,3]).save(folder/f'{state}-coverage.png');Image.fromarray(ratio).save(folder/f'{state}-detail-weight.png');detail=a.copy();detail[:,:,3]=np.uint8(np.round(a[:,:,3].astype(float)*ratio/255));detail[detail[:,:,3]==0,:3]=0;Image.fromarray(detail).save(folder/f'{state}-detail-neutral.png');Image.fromarray(detail[:,:,3]).save(folder/f'{state}-detail-coverage.png');Image.fromarray(np.dstack([ratio,ratio,ratio,a[:,:,3]])).save(folder/f'{state}-authored-dualcolor-mask.png')
        fields={k:ref(folder/f'{state}-{name}') for k,name in [('primary','primary-neutral.png'),('detail','detail-neutral.png'),('coverage','coverage.png'),('detail_weight','detail-weight.png'),('detail_coverage','detail-coverage.png'),('authored_dualcolor_mask','authored-dualcolor-mask.png')]};fields['native_tile']='Items/sw_table_metal'+('_full' if state=='occupied' else '')+'.bmp';states[state]=fields;groups[f'{state}-neutral'][f]=primary
        for name,code in ([('empty-native-c','C')] if state=='empty' else [('occupied-upper-c','C'),('occupied-lower-w','w'),('occupied-lower-y','y'),('occupied-upper-w','W')]):
            fg=np.frombuffer(bytes.fromhex(palette['c']),dtype=np.uint8).astype(float);dc=np.frombuffer(bytes.fromhex(palette[code]),dtype=np.uint8).astype(float);r=ratio.astype(float)/255;rgb=np.uint8(np.round((fg[None,None,:]*(1-r[:,:,None])+dc[None,None,:]*r[:,:,None])*a[:,:,:1]/255));rgb[a[:,:,3]==0]=0;im=Image.fromarray(np.dstack([rgb,a[:,:,3]]));im.save(folder/f'{name}-preview.png');groups[name][f]=im
            if state=='occupied':
                exact=np.divide((ls*ast)[:,:,None]*dc+(lb*ab*(1-ast))[:,:,None]*fg,alpha[:,:,None],out=np.zeros((256,256,3)),where=alpha[:,:,None]>0);valid=a[:,:,3]>0;errors[code]=float(np.abs(exact[valid]-rgb[valid]).max())
    groups['stock-neutral'][f]=stock;groups['coverage'][f]=Image.fromarray(np.uint8(np.round(np.stack([alpha,alpha,alpha,np.ones_like(alpha)],2)*255)));w=np.uint8(np.round(weight*255));groups['detail-weight'][f]=Image.fromarray(np.dstack([w,w,w,np.uint8(np.round(alpha*255))]));views[f]=dict(states=states,shared_base=ref(folder/'base-neutral.png'),separate_stock=ref(folder/'stock-neutral.png'),canvas=[256,256],authoring_canvas=[512,768],authored_anchor=[8,16],native_bound_proposal=f=='south',native_activation=False)
    edge=np.array(groups['occupied-neutral'][f])[:,:,3];checks[f]=dict(max_unpremultiplied_palette_quantization_error=errors,production_edge_alpha_sum=int(edge[0].sum()+edge[-1].sum()+edge[:,0].sum()+edge[:,-1].sum()),same_base_all_states=True,empty_detail_pixels=0,production_geometry='Common whole frame; one coverage, independent luminance-weighted detail mix. Component masters remain intact.')
model=dict(entry='SCN-METAL-WORKBENCH',kind='directional_inventory_state_dualcolor_furniture',blueprint='Metal Workbench',source=ref(HERE/'source-packet.json'),views=views,states=views['south']['states'],shared_base=views['south']['shared_base'],registration=packet['frame'],camera=packet['camera'],palette=packet['palette'],state_owner=packet['inventory_boundary'],native_acceptance=packet['native_acceptance'],west_policy='Symmetric unmarked base mirrors E; occupied stock has independent physical W projection and near/far overlap.',color_formula='A*L*((1-R)*foreground+R*detail)+(1-A)*background; R equals stock premultiplied luminance divided by total premultiplied luminance, preserving tinted component overlap with one coverage.')
write(OUT/'model.json',model);write(OUT/'registration-decisions.json',dict(checks=checks,material_selection=ref(HERE/'occupied-material-selection.json'),retained_front='Selected v2 material with one common0.95whole-object registration for every component/facing/state',component_composition='Empty base retained exactly; occupied stock separately alpha-overlaid. Combined neutral luminance and detail weight derived analytically, not a second full-opacity detail overdraw.',new_imagegen_calls=2,second_isolation_call=False,native_activation=False))
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
for group,images in groups.items():
    plate=Image.new('RGB',(1440,650),'#142823');d=ImageDraw.Draw(plate);d.text((18,15),f'METAL WORKBENCH / {group.upper()} / full end volume + independent stock projection / shared scale',font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        x=18+i*355;large=im.resize((320,480),Image.Resampling.LANCZOS);plate.paste(large,(x,50),large);d.text((x,535),f.upper(),font=font,fill='#e3cf43')
        for j,(w,h) in enumerate([(16,24),(24,36),(32,48)]):thumb=im.resize((w,h),Image.Resampling.LANCZOS);plate.paste(thumb,(x+45+j*90,565),thumb)
    d.text((18,625),'Steel primary c; stock detail C/w/y/W chosen by native Inventory. Extra views unbound; native acceptance pending.',font=font,fill='#e5e8d8');plate.save(OUT/f'all-views-{group}.png')
print(json.dumps(checks,indent=2))
