"""Register the selected sheet, extract body/head masks, and author one robe overlay.

Source PNG is never overwritten or resampled. Pixel extraction is mechanical;
cloth refinement is a separate ImageGen step. Native evidence remains separate.
"""
import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil

from PIL import Image, ImageChops, ImageDraw, ImageFilter
import resvg_py

REPO=Path(__file__).resolve().parents[1]
OUT=REPO/'art/dromad/layered'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def write_json(p,value):p.write_bytes((json.dumps(value,indent=2)+'\n').encode())


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    args=ap.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    registration=json.loads((REPO/'art/dromad/registration.json').read_text())
    source=REPO/registration['source'];selected=json.loads((REPO/'art/dromad/nude/refinement.json').read_text())
    assert sha(source)==selected['selected_output_sha256']
    sheet=Image.open(source).convert('RGBA');w,h=registration['canvas'];scale=registration['pixel_world_scale']
    packet=json.loads((REPO/'art/dromad/rebuilt/model.json').read_text())
    rows=[];views={};overlay_sheet=Image.new('RGBA',(w*3,h))
    robe_registration=json.loads((REPO/'art/dromad/robe-registration.json').read_text())
    robe_source=REPO/robe_registration['source']
    refined_sheet=Image.open(robe_source).convert('RGBA')
    for index,(direction,points) in enumerate(registration['views'].items()):
        original=sheet.crop((points['source_x'],0,points['source_x']+w,h))
        # Ignore near-transparent generation residue outside the three sprites;
        # retain all actually visible source pixels and their exact RGB values.
        alpha=original.getchannel('A');alpha=alpha.point(lambda a:0 if a<8 else a)
        original.putalpha(alpha)
        head=Image.new('L',(w,h));ImageDraw.Draw(head).polygon([tuple(p) for p in points['head_mask']],fill=255)
        body=ImageChops.invert(head)
        # Underlap prevents mip-filter seams; it extends only two pixels under
        # the existing head, without generating or changing visible anatomy.
        underlap=body.filter(ImageFilter.MaxFilter(5))
        detail=Image.new('L',(w,h))
        if points['detail_mask']:ImageDraw.Draw(detail).polygon([tuple(p) for p in points['detail_mask']],fill=255)
        extracted={}
        for name,mask in [('body',underlap),('head',head),('head-detail',ImageChops.multiply(head,detail))]:
            part=original.copy();part.putalpha(ImageChops.multiply(alpha,mask));extracted[name]=part
        robe_svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="920" viewBox="0 0 512 920"><defs><linearGradient id="cloth" x2="1" y2=".5"><stop stop-color="#f1f0e9"/><stop offset=".6" stop-color="#c4cdc4"/><stop offset="1" stop-color="#929e93"/></linearGradient></defs><path d="{points['robe_path']}" fill="url(#cloth)" stroke="#303735" stroke-width="8" stroke-linejoin="round"/><path d="{points['robe_folds']}" fill="none" stroke="#869487" stroke-width="5" stroke-linecap="round"/></svg>'''
        (OUT/f'robe-overlay-{direction}.svg').write_bytes((robe_svg+'\n').encode())
        robe=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=robe_svg,skip_system_fonts=True))).convert('RGBA')
        # The side cuff has one visible sleeve, rather than a frontal two-sleeve
        # silhouette. Its hand opening is explicit in the overlay input.
        if direction=='east':
            sleeve=Image.new('L',(w,h));ImageDraw.Draw(sleeve).polygon([(255,670),(293,675),(294,717),(263,719),(245,697)],fill=255)
            robe.putalpha(ImageChops.subtract(robe.getchannel('A'),sleeve))
        extracted['robe-overlay']=robe
        grip=points['held_grip'];gx,gy=grip
        held_svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="512" height="920"><path d="M{gx-5} {gy+155} L{gx-4} {gy-10} Q{gx-29} {gy-29} {gx-15} {gy-47} Q{gx} {gy-61} {gx+18} {gy-45} Q{gx+33} {gy-23} {gx+7} {gy-9} L{gx+7} {gy+155} Z" fill="#d1d3c9" stroke="#303735" stroke-width="7"/></svg>'''
        (OUT/f'shillelagh-{direction}.svg').write_bytes((held_svg+'\n').encode())
        extracted['shillelagh']=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=held_svg,skip_system_fonts=True))).convert('RGBA')
        rp=robe_registration['views'][direction];rw,rh=robe_registration['canvas']
        extracted['robe']=refined_sheet.crop((rp['source_x'],0,rp['source_x']+rw,rh))
        # Isolated-generation sleeve outlines are not body anatomy. Open the
        # lower cuffs explicitly so their closed oval strokes do not cross hands.
        coverage_svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{rw}" height="{rh}"><path d="{rp["cuff_cutouts"]}" fill="white"/></svg>'
        (OUT/f'robe-coverage-{direction}.svg').write_bytes((coverage_svg+'\n').encode())
        cutout=Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=coverage_svg,skip_system_fonts=True))).getchannel('A')
        isolated=extracted['robe'];isolated.putalpha(ImageChops.subtract(isolated.getchannel('A'),cutout))
        composite=original.copy();composite.alpha_composite(robe)
        composite.alpha_composite(extracted['head'])
        overlay_sheet.alpha_composite(composite,(index*w,0))
        for name,image in extracted.items():
            if name=='head-detail' and image.getchannel('A').getbbox() is None:continue
            target=OUT/f'{name}-{direction}.png'
            image.save(target)
            rows.append(dict(subject='Registered adult dromad / Tam',file=target.relative_to(REPO).as_posix(),direction=direction,
                sha256=sha(target),size=list(image.size),cutout_bounds=image.getchannel('A').getbbox(),
                kind='Source-pixel extraction' if name in ['body','head','head-detail'] else 'Authored overlay / isolated apparel',
                state='Assembled sample awaiting native verification'))
        layers=[]
        for name in ['body','head','head-detail','robe','shillelagh']:
            if name not in extracted or name=='head-detail' and not points['detail_mask']:continue
            filename=f'dromad-refined-{name}-{direction}.png';target=OUT/f'{name}-{direction}.png'
            shutil.copy2(target,args.root/'donor'/filename)
            cx,cy=points['contact'];pw,ph=extracted[name].size;ps=scale
            if name=='robe':
                factor=robe_registration['uniform_scale_in_body_pixels'];ps*=factor
                cx=(cx-rp['body_anchor'][0])/factor+rp['source_anchor'][0]
                cy=(cy-rp['body_anchor'][1])/factor+rp['source_anchor'][1]
            layers.append(dict(component=name,file=filename,sha256=sha(target),size=[pw,ph],contact=[cx,cy],
                color_role='detail' if name=='head-detail' else 'equipment' if name in ['robe','shillelagh'] else 'foreground',
                width=pw*ps/(2/3),height=ph*ps,center_x=(pw/2-cx)*ps/(2/3),center_z=(cy-ph/2)*ps,
                layer=0 if name=='body' else .0002 if direction=='north' and name=='head' else .001 if name=='head' else .0011 if name=='head-detail' else .0007 if name=='robe' else -.0002 if direction=='north' else .0018))
        views[direction]=layers
    overlay=OUT/'robe-context.png';overlay_sheet.save(overlay)
    rows.append(dict(subject='Cloth Robe on selected unclothed dromad',file=overlay.relative_to(REPO).as_posix(),direction='three-view',
        sha256=sha(overlay),size=list(overlay_sheet.size),cutout_bounds=overlay_sheet.getchannel('A').getbbox(),kind='One-item context overlay for refinement',state='Not native evidence'))
    rows.append(dict(subject='Cloth Robe isolated refinement',file=robe_source.relative_to(REPO).as_posix(),direction='three-view',
        sha256=sha(robe_source),size=list(refined_sheet.size),cutout_bounds=refined_sheet.getchannel('A').getbbox(),
        kind='Built-in image_gen isolated garment output, unchanged pixels',state='Registered on the selected base'))
    packet.update(views=views,authoring='Selected ImageGen base, mechanically registered body/head masks and separately refined Cloth Robe',
        registration=registration,robe_registration=robe_registration,selected_base_sha256=sha(source),
        robe_source_sha256=sha(robe_source),supported_equipment=['Cloth Robe','Shillelagh'],held_part_laterality=2,
        policy='Approved base pixels retained; separate body/head, dulla detail, actual robe and right-hand Shillelagh. Unknown anatomy/equipment retains native sprite.')
    write_json(OUT/'model.json',packet);write_json(args.root/'dromad-refined.json',packet)
    manifest_file=REPO/'art/manifest.json';manifest=json.loads(manifest_file.read_text())
    manifest['images']=[r for r in manifest['images'] if not r['file'].startswith('art/dromad/layered/')] + rows
    write_json(manifest_file,manifest)
    print('Registered selected body/head and isolated robe with explicit contact transforms; native acceptance remains pending.')


if __name__=='__main__':main()
