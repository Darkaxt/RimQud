"""Package the bounded village art contract; retain unrecognized state natively."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import resvg_py

REPO=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def topology(actor):
    parts={p['id']:p for p in actor['parts']}
    def path(p):return (path(parts[p['parent']])+ '>' if p['parent'] in parts else '')+p['type']+'/'+str(p['variant'])+'/'+str(p['laterality'])
    return sorted(path(p) for p in parts.values())

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True);args=ap.parse_args()
    sources=json.loads((REPO/'art/village/sources.json').read_text(encoding='utf-8'))
    models=json.loads((REPO/'art/village/body-models.json').read_text(encoding='utf-8'))
    equipment=json.loads((REPO/'art/village/equipment-models.json').read_text(encoding='utf-8'))
    scenery=json.loads((REPO/'art/village/scenery-models.json').read_text(encoding='utf-8'))
    tam=json.loads((REPO/'art/dromad/layered/model.json').read_text(encoding='utf-8'));cat=json.loads((REPO/'art/ctesiphus/packaged.json').read_text(encoding='utf-8')) if (REPO/'art/ctesiphus/packaged.json').exists() else json.loads((args.root/'faithful-cat.json').read_text(encoding='utf-8'))
    models['dromad']={**tam,'family':'dromad'};models['ray-cat']={**cat,'family':'ray-cat'};equipment['dromad']={}
    # Preserve accepted cat pixels and existing Tam body/robe. Enlarge the held
    # item about its actual grip instead of moving the hand or scaling the body.
    tam_hand=next(p for a in sources['actors'] if a['creature']=='Tam' for p in a['native_instances'][0]['parts'] if p.get('equipped') and p['equipped']['blueprint']=='Shillelagh')
    for component,name,slot,lat in [('robe','Cloth Robe','Body',0),('shillelagh','Shillelagh','Hand',2)]:
        k=name.lower().replace(' ','-')+'@'+slot+'@'+str(lat);views={}
        for d,layers in tam['views'].items():
            layer=next(dict(p) for p in layers if p['component']==component);layer.update(color_role='equipment',equipment_key=k)
            if component=='shillelagh':
                gx,gy=tam['registration']['views'][d]['held_grip'];w,h=layer['size']
                s=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}"><path d="M{gx-5} {gy+155} L{gx-4} {gy-145} Q{gx-29} {gy-164} {gx-15} {gy-184} Q{gx} {gy-201} {gx+18} {gy-184} Q{gx+34} {gy-162} {gx+7} {gy-145} L{gx+7} {gy+155}Z" fill="#d1d3c9" stroke="#303735" stroke-width="7"/></svg>'
                f=REPO/f'art/village/equipment/dromad-shillelagh-{d}.svg';f.write_bytes(s.encode());png=f.with_suffix('.png');png.write_bytes(resvg_py.svg_to_bytes(svg_path=str(f),skip_system_fonts=True))
                filename='village-'+png.name;shutil.copy2(png,args.root/'donor'/filename);layer.update(file=filename,sha256=sha(png))
            views[d]=[layer]
        equipment['dromad'][k]=dict(blueprint=name,slot=slot,laterality=lat,views=views,authoring='Shillelagh upper shaft lengthened while keeping the hand grip and lower endpoint fixed' if component=='shillelagh' else 'Selected isolated robe with explicit cuff masks')
    for d in tam['views']:models['dromad']['views'][d]=[p for p in tam['views'][d] if p['component'] not in ['robe','shillelagh']]
    for d,row in cat['views'].items():models['ray-cat']['views'][d]=[{**row,'component':'body','color_role':'foreground','layer':0,'contact':[row['landmarks']['contact_x'],row['landmarks']['contact_y']]}]
    actors={}
    fixed={'Tam':'dromad','Ctesiphus':'ray-cat','Glowfish':'glowfish','ElderBob':'irudad','Nima Ruda':'nima','Warden Yrame':'yrame'}
    for a in sources['actors']:
        native=a['native_instances'][0]
        actors[a['creature']]=dict(family=fixed.get(a['creature'],'human'),anatomy=native['anatomy'],expected_topology=topology(native),
            species=a['race'],race_description=a['race_input']['description'],original_model_tiles=a['original_model_tiles'],
            fixed_palette=dict(foreground=native.get('tileColor') or native['foreground'],detail=native['detailColor']) if a['creature']=='Glowfish' else None,
            detail_guard=native['detailColor'] if a['creature']=='Ctesiphus' else None)
    data=dict(scope='The ten captured Joppa actor blueprints and 57 selected scenery targets; fixed named anatomy, actual equipment, native fallback for unrecognized state',
        actors=actors,bodies=models,equipment=equipment,scenery=scenery,
        invariants=['Qud owns simulation, inventory, anatomy and state','No independent limb rig','Source-aware palette and registered flat graphics','No generic mutation or third-party item resolver'],
        state='Packaged; integrated native batch acceptance pending')
    # Every generated PNG has provenance, including rejected proposals. Native
    # readbacks are recorded separately after the complete integrated batch.
    manifest_path=REPO/'art/manifest.json';manifest=json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest['images']=[r for r in manifest['images'] if not r['file'].startswith('art/village/')]
    from PIL import Image
    for p in sorted((REPO/'art/village').rglob('*.png')):
        image=Image.open(p);name=p.stem;direction=next((d for d in ['south','east','north'] if name.endswith('-'+d)),'three-view')
        entry=dict(subject='Source-bound Joppa conversion',file=p.relative_to(REPO).as_posix(),direction=direction,sha256=sha(p),size=list(image.size),cutout_bounds=image.getchannel('A').getbbox(),
            kind='Rejected anatomical proposal' if 'rejected' in name or 'draft' in name else 'Front-guided generated turnaround' if name=='turnaround' else 'Editable source geometry / registered layer',state='Native village acceptance pending')
        if p.with_suffix('.svg').exists():entry.update(source_svg=p.with_suffix('.svg').relative_to(REPO).as_posix(),source_sha256=sha(p.with_suffix('.svg')))
        manifest['images'].append(entry)
    write(manifest_path,manifest);print('Packaged ten actor rules, shared bodies and actual equipment, plus 57 scenery targets; original cat retained and Tam held item enlarged.')
    by_hash={r['sha256']:r['file'] for r in manifest['images']}
    for group in [*[m['views'] for m in models.values()],*[m['views'] for f in equipment.values() for m in f.values()],*[m['views'] for m in scenery['entries'].values()]]:
        for layers in group.values():
            for layer in layers:
                layer.setdefault('sha256',sha(args.root/'donor'/layer['file']))
                layer['public_file']=by_hash[layer['sha256']]
    write(REPO/'art/village/model.json',data);write(args.root/'village.json',data)
if __name__=='__main__':main()
