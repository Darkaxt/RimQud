"""Show the two executed transforms, unchanged profile and unresolved ownership."""
from pathlib import Path
import hashlib, json
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
BASE = HERE.parent
FONT = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 15)
packet = json.loads((HERE/'source-packet.json').read_text())


def read(p):
    return Image.open(p).convert('RGBA')


def background(im):
    result = Image.new('RGBA', im.size, '#20382d')
    result.alpha_composite(im)
    return result.convert('RGB')


def plate(path, title, panels, foot):
    out = Image.new('RGB', (1152, 660), '#142823')
    draw = ImageDraw.Draw(out)
    draw.text((18, 12), title, font=FONT, fill='#e3cf43')
    for i, (label, im) in enumerate(panels):
        x = 16+i*284
        out.paste(background(im).resize((256, 512)), (x, 48))
        draw.line((x+128, 48, x+128, 559), fill='#e3cf43')
        draw.line((x, 523, x+255, 523), fill='#70b8b0')
        draw.text((x, 578), label, font=FONT, fill='#e3cf43')
    draw.text((18, 620), foot, font=FONT, fill='#e5e8d8')
    out.save(path)


review = {'scope': 'Front/back authoring comparison only; accepted profile unchanged',
          'source': packet['source'], 'visual_status': 'REQUIRES REWORK',
          'reason': 'Both transforms execute, but inherited visibility/cuff ownership and cloth overlap remain unresolved. A cleaner silhouette is not accepted garment fitting.',
          'views': {}, 'native_validation': 'Not performed; generation-first gate unchanged'}
sections = []
for facing, _ in [('south', 0), ('north', 2)]:
    panels = [('EARLIER LATE MASK', read(BASE/f'late-mask-v3/assembly-{facing}.png')),
              ('SAME-SOURCE WHOLE', read(HERE/f'three-band/whole-image-assembly-{facing}.png')),
              ('THREE BANDS', read(HERE/f'three-band/assembly-{facing}.png')),
              ('NINE GRID', read(HERE/f'nine-grid/assembly-{facing}.png'))]
    plate(HERE/f'comparison-{facing}.png', facing.upper()+' / earlier result, then identical-source transform comparison', panels,
          'Body and visibility fixed. Last three columns share one full source; lower robe frozen. No native test.')
    plate(HERE/f'cloth-{facing}.png', facing.upper()+' / retained cloth and final visibility, shown separately',
          [('SOURCE BEFORE FIT', read(HERE/f'full-source-{facing}.png')),
           ('THREE-BAND CLOTH', read(HERE/f'three-band/full-cloth-{facing}.png')),
           ('NINE-GRID CLOTH', read(HERE/f'nine-grid/full-cloth-{facing}.png')),
           ('FIXED BODY MASK', Image.open(BASE/f'mask-fit-v4/robe-expose-{facing}.png').convert('RGBA'))],
          'No arm holes punched for fitting. New concealed fabric was continued before either transform.')
    body = np.array(read(ROOT/f'art/conversion/body-dromad/v2/selected-{facing}.png'))
    mask = np.array(Image.open(BASE/f'mask-fit-v4/robe-expose-{facing}.png').convert('L'))
    required = np.array(Image.open(BASE/f'mask-fit-v4/robe-required-{facing}.png').convert('L')) > 128
    diagnostic = Image.new('RGB', (1440, 515), '#142823')
    d = ImageDraw.Draw(diagnostic)
    d.text((18, 12), 'CUFF OWNERSHIP / yellow inherited mask boundary; red body selected by neither cloth nor overlay', font=FONT, fill='#e3cf43')
    metrics = {}
    for i, mode in enumerate(['three-band', 'nine-grid']):
        cloth = np.array(read(HERE/f'{mode}/full-cloth-{facing}.png'))
        final = background(read(HERE/f'{mode}/assembly-{facing}.png'))
        overlay = np.array(final)
        exposed = mask > 128
        boundary = ndimage.binary_dilation(exposed) ^ ndimage.binary_erosion(exposed)
        arms_roi = np.zeros(mask.shape, bool)
        for box in packet['views'][facing]['target_arm_bounds']:
            arms_roi[max(0, box[1]-20):min(1024, box[3]+12), max(0, box[0]-12):min(512, box[2]+12)] = True
        unclaimed = arms_roi & (body[:, :, 3] > 128) & (mask < 128) & (cloth[:, :, 3] < 128)
        overlay[boundary & arms_roi] = [227, 207, 67]
        overlay[unclaimed] = [255, 82, 91]
        crop = Image.fromarray(overlay).crop((70, 620, 440, 825)).resize((666, 369))
        diagnostic.paste(crop, (18+i*720, 70))
        d.text((18+i*720, 48), mode.upper(), font=FONT, fill='#e3cf43')
        metrics[mode] = {'inherited_required_mask_pixels_below_cloth_alpha_128': int(np.count_nonzero(required & (body[:, :, 3] > 128) & (cloth[:, :, 3] < 128))),
                         'arm_roi_unclaimed_body_pixels': int(unclaimed.sum())}
    d.text((18, 461), 'Diagnostic ownership map, not an accepted clothing mask. Some red regions belong to exposed hand contours.', font=FONT, fill='#e5e8d8')
    d.text((18, 485), 'Do not stretch cloth over all red pixels: first distinguish the true cuff from the complete original hand.', font=FONT, fill='#e5e8d8')
    diagnostic.save(HERE/f'cuff-ownership-{facing}.png')
    review['views'][facing] = metrics
    sections.append(f'''<section id="{facing}"><h2>{'Front / south' if facing=='south' else 'Back / north'}</h2><p><a href="dromad-clothing-pipeline-{facing}.html">Equivalent existing-pipeline walkthrough</a></p><img loading="lazy" src="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/comparison-{facing}.png" alt="Earlier result, same-source whole stretch, three bands and nine grid for {facing}"><p>The first column is historical. The remaining three use identical reconstructed cloth and the same fixed body/mask. The lower region matches the common whole-image baseline pixel-for-pixel.</p><h3>Cloth versus visibility</h3><img loading="lazy" src="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/cloth-{facing}.png" alt="Uncut source cloth, regional cloth and separate body mask"><h3>Remaining cuff conflict</h3><img loading="lazy" src="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/cuff-ownership-{facing}.png" alt="Close-up showing inherited visibility boundary and unclaimed arm-edge pixels"><p>Red marks body pixels absent from both cloth coverage and the inherited foreground selection. Some are actual exposed hand contours that the old mask failed to include. The older required-coverage map therefore cannot be treated as a clean target without reviewing ownership. Both experiments remain unfinished.</p><details><summary>Exact source/target controls and full-size outputs</summary><p><a href="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/three-band/controls-{facing}.json">Three-band coordinates</a> Â· <a href="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/nine-grid/controls-{facing}.json">Nine-grid coordinates</a></p><img loading="lazy" src="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/three-band/controls-{facing}.png" alt="Three-band shared boundaries"><img loading="lazy" src="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/nine-grid/controls-{facing}.png" alt="Nine cells with shared boundaries"></details></section>''')

page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Dromad regional fitting comparison</title><style>body{margin:0;background:#142823;color:#e5e8d8;font:18px/1.55 Georgia,serif}main{max-width:1200px;margin:auto;padding:28px 20px 70px}a{color:#e3cf43}img{width:100%;height:auto;border:1px solid #526b5c}h1,h2,h3{line-height:1.2}section{margin:50px 0}aside{border-left:3px solid #e3cf43;padding-left:18px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #526b5c;padding:12px;text-align:left}summary{cursor:pointer;color:#e3cf43}details img{max-height:600px;object-fit:contain}a:focus-visible,summary:focus-visible{outline:2px solid #e3cf43}</style><main><nav><a href="dromad-clothing-pipeline.html">Profile pipeline</a> Â· <a href="dromad-clothing-pipeline-south.html">Front pipeline</a> Â· <a href="dromad-clothing-pipeline-north.html">Back pipeline</a> Â· <a href="#south">Front comparison</a> Â· <a href="#north">Back comparison</a></nav><h1>Three bands, then nine cells</h1><p>Both authoring experiments have been executed on the front and back, using the same raw generated clothing and fixed body visibility masks. The side composition was copied unchanged. No ImageGen call, game launch or native validation was performed.</p><aside><p><strong>Result: fitting remains unresolved.</strong> Three bands correct cuff height while holding the lower robe fixed. Nine cells additionally control the two sleeve widths separately. Neither automatically resolves the mismatch between the actual cuff edge, cloth overlap and the older painted visibility selection. These are comparative drafts, not accepted garments.</p></aside><table><tr><th>Method</th><th>What actually changes</th></tr><tr><td>Three bands</td><td>Landmark-based shoulder/cuff/transition bands, with shared boundaries. Upper width follows arm-center separation; middle joins the fixed lower section.</td></tr><tr><td>Nine cells</td><td>The same three rows plus left sleeve, torso and right sleeve columns. Cuff-row column positions follow the two actual arm rectangles independently.</td></tr><tr><td>Frozen</td><td>Body, mask and lower common-baseline pixels remain fixed. The accepted profile image is byte-for-byte unchanged.</td></tr></table><p>One continuous coordinate map samples the original complete cloth per method. Before fitting, exterior hand-occlusion notches were bridged between visible cloth edges and missing fabric continued from that same image. Those concealed surfaces are authored reconstruction, not recovered detail. No cutoff-derived alpha is reused.</p>'''+''.join(sections)+'''<h2>Side view retained</h2><p><a href="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/accepted-profile-unchanged.png">Accepted profile composition, unchanged</a></p><p><a href="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/source-packet.json">Source packet and reconstruction provenance</a> Â· <a href="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/three-band/result.json">Three-band measurements</a> Â· <a href="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/nine-grid/result.json">Nine-grid measurements</a> Â· <a href="../art/conversion/fit-dromad-cloth-robe/regional-fit-v1/authoring-review.json">Review and limitations</a></p></main>'''
page = page.replace('<nav>', '<nav><a href="dromad-curved-cuffs.html">Curved cuff follow-up</a> · ', 1)
(ROOT/'docs/dromad-regional-fitting.html').write_bytes(page.encode())
(HERE/'authoring-review.json').write_bytes((json.dumps(review, indent=2)+'\n').encode())
print('Rendered front/back technique, cloth and ownership comparisons; no readiness credit.')
