"""Use contextual material, intact editable pattern and curved body visibility."""
from pathlib import Path
import sys, io, json, hashlib, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageOps
sys.path.insert(0, 'E:/Temp/rimqud-conversion-runtime/python-libs')
import resvg_py

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
OLD = HERE.parent/'v2'
BODY = ROOT/'art/conversion/body-dromad-child/v1'
assert not (HERE/'model.json').exists()
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)


def ref(p):
    return {'path': p.relative_to(ROOT).as_posix(), 'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}


def read(p):
    return Image.open(p).convert('RGBA')


def svg_image(svg):
    return Image.open(io.BytesIO(resvg_py.svg_to_bytes(svg_string=svg, skip_system_fonts=True))).convert('RGBA')


def tinted(im, color):
    a = np.array(im).copy(); gray = a[:, :, :3].mean(axis=2)
    a[:, :, :3] = np.uint8(np.round(gray[:, :, None]*np.array(color)/255))
    return Image.fromarray(a)


def compose(body, cloth, mask):
    coverage = Image.fromarray(np.uint8(np.array(mask)*(np.array(body)[:, :, 3] > 0)))
    return Image.composite(body, Image.alpha_composite(body, cloth), coverage)


def plate(name, rows, title):
    out = Image.new('RGB', (1152, 660), '#142823'); d = ImageDraw.Draw(out)
    d.text((18, 14), title, font=FONT, fill='#e3cf43')
    for i, (f, im) in enumerate(rows.items()):
        bg = Image.new('RGBA', im.size, '#20382d'); bg.alpha_composite(im)
        x = 16+i*284; out.paste(bg.convert('RGB').resize((256, 512)), (x, 54))
        d.line((x+128, 54, x+128, 565), fill='#e3cf43'); d.line((x, 529, x+255, 529), fill='#70b8b0')
        d.text((x, 584), f.upper(), font=FONT, fill='#e3cf43')
    d.text((18, 620), 'Authored child template; no resident reassignment. Fixed body, frame and independent garment visibility.', font=FONT, fill='#e5e8d8')
    out.save(HERE/name)


source = read(OLD/'refined-context.png')
swatch_box = [180, 585, 320, 665]
swatch = source.crop(tuple(swatch_box))
assert swatch.getchannel('A').getextrema()[0] > 240
swatch.save(HERE/'contextual-fabric-swatch.png')
model = json.loads((OLD/'model.json').read_text()); body_model = json.loads((BODY/'model.json').read_text())
model.update(workflow='regional-curved-v1', views={}, occlusion_sources={}, representation='Full constructed cloth with contextual fabric and separate curved original-body visibility',
             layer_order='body -> head/detail -> collar garment .0012 -> exposed-arm overlay .0013',
             native_acceptance='Pending full-set generation gate; no observed child wearer or native selector established')
record = {'workflow':'regional-curved-v1','source':ref(OLD/'refined-context.png'),'body':ref(BODY/'model.json'),
          'new_imagegen_call':False,'isolated_proposal_used':False,'material_swatch':swatch_box,
          'fit':'Retain body-matched editable pattern, already registered to this child. No additional stretch needed; no adult coordinates reused.',
          'views':{}}
arm_paths = {
    'south': 'M101 741 Q123 745 154 764 Q151 774 161 781 C174 791 174 808 160 818 C154 823 149 825 143 825 C125 825 113 813 114 798 Q116 787 124 780 Q122 760 101 741Z M411 741 Q389 745 358 764 Q361 774 351 781 C338 791 338 808 352 818 C358 823 363 825 369 825 C387 825 399 813 398 798 Q396 787 388 780 Q390 760 411 741Z',
    'east': 'M212 744 Q237 758 273 753 L273 773 C291 782 290 806 274 818 C263 826 245 826 232 815 C220 802 221 788 229 777 Q215 760 212 744Z',
    'north': 'M101 741 Q123 745 154 764 Q151 774 161 781 C174 791 174 808 160 818 C154 823 149 825 143 825 C125 825 113 813 114 798 Q116 787 124 780 Q122 760 101 741Z M411 741 Q389 745 358 764 Q361 774 351 781 C338 791 338 808 352 818 C358 823 363 825 369 825 C387 825 399 813 398 798 Q396 787 388 780 Q390 760 411 741Z'}
assembled = {}; garments = {}; masks = {}; off = {}; colored = {}; overlays = {}
for f in ['south','east','north']:
    pattern_svg = (OLD/f'constructed-{f}.svg').read_text()
    # The garment's physical cuff and body mask both use smooth cross-sections.
    pattern_svg = pattern_svg.replace('L150 761','Q126 746 150 761').replace('L364 761','Q386 746 364 761')
    (HERE/f'pattern-{f}.svg').write_bytes(pattern_svg.encode())
    pattern = svg_image(pattern_svg); alpha = pattern.getchannel('A'); box = alpha.getbbox()
    texture = Image.new('L', (512,1024)); texture.paste(ImageOps.grayscale(swatch).resize((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS),box[:2])
    pgray = ImageOps.grayscale(pattern)
    ink = Image.fromarray(np.uint8((np.array(pgray)<190)&(np.array(alpha)>0))*255)
    texture.paste(pgray,mask=ink)
    cloth = Image.merge('RGBA',(texture,texture,texture,alpha)); cloth.save(HERE/f'intact-tunic-{f}.png')
    # The top of this region is the curved sleeve opening; its closed bottom
    # follows the exposed hand region and clips only original body alpha.
    mask_svg = '<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><path fill="white" d="'+arm_paths[f]+'"/></svg>'
    (HERE/f'body-visibility-{f}.svg').write_bytes(mask_svg.encode())
    coverage = svg_image(mask_svg).getchannel('A'); coverage.save(HERE/f'body-visibility-{f}.png')
    body = read(BODY/f'selected-{f}.png')
    composed = compose(body,cloth,coverage); composed.save(HERE/f'assembled-{f}.png')
    mask_off = Image.alpha_composite(body,cloth); mask_off.save(HERE/f'mask-off-{f}.png')
    over = body.copy(); over.putalpha(Image.fromarray(np.uint8(np.round(np.array(body)[:,:,3].astype(float)*np.array(coverage)/255))))
    over.save(HERE/f'body-overlay-{f}.png')
    color = compose(tinted(body,(152,135,95)),tinted(cloth,(177,201,195)),coverage); color.save(HERE/f'palette-{f}.png')
    assembled[f],garments[f],masks[f],off[f],colored[f],overlays[f] = composed,cloth,coverage.convert('RGBA'),mask_off,color,over
    row = dict(body_model['views'][f][0]); row.update(component='item',file=f'dromad-child-tunic-v4-{f}.png',public_file=ref(HERE/f'intact-tunic-{f}.png')['path'],sha256=ref(HERE/f'intact-tunic-{f}.png')['sha256'],equipment_key='woven-tunic@Body@0',color_role='equipment',layer=.0012)
    overlay = dict(row); overlay.update(component='body-overlay',file=f'dromad-child-tunic-overlay-v4-{f}.png',public_file=ref(HERE/f'body-overlay-{f}.png')['path'],sha256=ref(HERE/f'body-overlay-{f}.png')['sha256'],color_role='foreground',layer=.0013)
    model['views'][f] = [row,overlay]
    model['occlusion_sources'][f] = {'cloth':ref(HERE/f'intact-tunic-{f}.png'),'mask':ref(HERE/f'body-visibility-{f}.png'),'editable_mask':ref(HERE/f'body-visibility-{f}.svg')}
    record['views'][f] = {'pattern':ref(HERE/f'pattern-{f}.svg'),'body':ref(BODY/f'selected-{f}.png'),**model['occlusion_sources'][f]}
for images in [assembled,garments,masks,off,colored,overlays]:images['west (mirror)'] = ImageOps.mirror(images['east'])
plate('assembly-comparison.png',assembled,'DROMAD CHILD / continuous contextual fabric and curved body visibility')
plate('intact-garment-comparison.png',garments,'FULL SOURCE / no generated isolation or body-shaped cloth cutoff')
plate('body-mask-comparison.png',masks,'BODY MASK / natural cuff cross-sections; original anatomy only')
plate('body-overlay-comparison.png',overlays,'EXPOSED BODY / original forearms and hands, independent of equipment tint')
plate('mask-off-comparison.png',off,'MASK OFF / intact cloth retained underneath the exposed arm')
plate('independent-palette-comparison.png',colored,'PALETTE OWNERSHIP / illustrative body w; actual Woven Tunic y')
small = Image.new('RGB',(560,370),'#142823');d=ImageDraw.Draw(small)
for i,(f,im) in enumerate(assembled.items()):
    t=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(t,(i*140+45,20),t);t=t.resize((96,192),Image.Resampling.NEAREST);small.paste(t,(i*140+20,138),t);d.text((i*140+4,344),f.upper(),font=FONT,fill='#e3cf43')
small.save(HERE/'game-scale-review.png')
packet = json.loads((OLD/'source-packet.json').read_text());packet.update(workflow='regional-curved-v1',reprocessing=record)
for name,data in [('model.json',model),('source-packet.json',packet),('registration-decisions.json',record)]:
    (HERE/name).write_bytes((json.dumps(data,indent=2)+'\n').encode())
print('Reprocessed child tunic: actual contextual swatch, complete editable cloth, separate curved body masks; review pending.')
