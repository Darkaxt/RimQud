"""Prepare an unclothed adult race reference and explicit source-layer masks.

No user-supplied clothed image is read. The older dressed native diagnostic is
preserved. Uses the same constructed body/head paths, without robe or weapon.
"""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw
import resvg_py
from build_dromad import shapes,svg,path,ellipse

REPO=Path(__file__).resolve().parents[1]
OUT=REPO/'art/dromad/nude'


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    args=ap.parse_args();OUT.mkdir(parents=True,exist_ok=True)
    rows=[];views={}
    for direction in ['south','east','north']:
        parts=shapes(direction)
        if direction=='east':
            # The far leg is behind the torso and lands higher in the elevated
            # side view. Both feet extend toward +X (east), not toward camera.
            body=path('M107 244 L126 248 L121 271 Q139 273 138 280 Q128 286 109 284 Q99 284 100 276 L102 260 Z','#a6aea4')
            body+=path('M100 187 C105 170 104 146 85 145 C60 146 60 181 76 201 C64 220 74 244 99 255 L126 262 L126 281 Q143 281 159 288 Q168 292 162 297 L135 298 Q119 296 116 289 L114 267 L108 255 Q151 268 166 247 C180 222 170 198 151 188 Z')
            body+=path('M145 199 Q160 200 165 216 L157 237 Q147 241 144 232 L150 217 L138 210', '#bdc3bd')
            body+=path('M145 233 Q138 236 141 246 Q149 251 157 242 L157 237', '#c6cbc4', '#303535',2)
            body+=path('M84 163 Q70 185 86 199 M92 221 Q114 238 137 227 M123 277 L134 279 M145 291 L157 292', 'none', '#747d74',2)
        else:
            body=path('M98 180 C84 164 96 144 114 146 Q140 139 154 161 L158 186 C176 200 176 222 168 243 L160 265 L160 281 Q174 290 162 297 L140 297 Q131 293 136 284 L133 265 L123 265 L118 285 Q121 297 107 298 L91 296 Q79 290 91 281 L88 264 L78 243 C66 219 77 194 98 180 Z')
            body+=path('M92 200 Q82 204 78 224 L79 243 Q87 250 95 241 L99 217 M163 200 Q174 205 177 224 L176 242 Q168 250 160 241 L156 218', '#c0c6bf')
            body+=path('M79 240 Q72 244 79 254 Q88 259 95 249 L95 241 M160 241 L160 251 Q169 259 177 251 L177 242', '#c8cec6','#303535',2)
            body+=path('M93 290 L108 291 M144 291 L159 290', 'none', '#768074',2)
            if direction=='south':
                body+=path('M110 240 Q129 248 147 239', 'none','#899185',2)
            else:
                body+=path('M104 172 Q127 156 151 176 M128 201 L128 238', 'none','#899185',2)
        # Round-foot construction is a neutral anatomical interpretation, not
        # separate boots. The old icon does not unambiguously assign its yellow
        # detail pixels to bare feet, so these are the same skin color as the body.
        composition=Image.new('RGBA',(256,320))
        for component,content in [('body',body),('head',parts['head'])]:
            content=content.replace('#e8e8e8','#c2c6c1').replace('#e4e4e4','#c2c6c1').replace('#d7d7d7','#b4bab3').replace('#dadada','#b4bab3')
            vector=OUT/f'{component}-{direction}.svg';vector.write_text(svg(content)+'\n',encoding='utf-8')
            p=vector.with_suffix('.png');p.write_bytes(resvg_py.svg_to_bytes(svg_path=str(vector),skip_system_fonts=True))
            im=Image.open(p).convert('RGBA');composition.alpha_composite(im)
            mask=Image.new('RGBA',im.size,'white');mask.putalpha(im.getchannel('A'));mask_path=OUT/f'{component}-mask-{direction}.png';mask.save(mask_path)
            for file,kind in [(p,'Constructed unclothed race component'),(mask_path,'Explicit source component coverage mask')]:
                rows.append(dict(subject='Adult dromad unclothed reference',file=file.relative_to(REPO).as_posix(),direction=direction,
                    sha256=hashlib.sha256(file.read_bytes()).hexdigest(),size=[256,320],cutout_bounds=im.getchannel('A').getbbox(),
                    kind=kind,state='Authoring input; not native integration or an extracted refined garment'))
        target=OUT/f'base-{direction}.png';composition.save(target)
        views[direction]=target.name
        rows.append(dict(subject='Adult dromad unclothed reference',file=target.relative_to(REPO).as_posix(),direction=direction,
            sha256=hashlib.sha256(target.read_bytes()).hexdigest(),size=[256,320],cutout_bounds=composition.getchannel('A').getbbox(),
            kind='Constructed unclothed adult dromad; body/head composite',state='Authoring input, no clothing or held item'))
    # One creature / three registered views; no labels or other game assets in
    # the transparent ImageGen edit target. Native source references stay local.
    sheet=Image.new('RGBA',(768,320))
    for i,direction in enumerate(views):sheet.alpha_composite(Image.open(OUT/views[direction]),(i*256,0))
    sheet_path=OUT/'base-three-views.png';sheet.save(sheet_path)
    rows.append(dict(subject='Adult dromad unclothed reference',file=sheet_path.relative_to(REPO).as_posix(),direction='three-view',
        sha256=hashlib.sha256(sheet_path.read_bytes()).hexdigest(),size=[768,320],cutout_bounds=sheet.getchannel('A').getbbox(),
        kind='Transparent registered unclothed source turnarounds; south/east/north',state='Refinement input; no user image used'))
    labeled=Image.new('RGBA',(768,360));labeled.alpha_composite(sheet,(0,0))
    draw=ImageDraw.Draw(labeled)
    for i,label in enumerate(['FRONT / SOUTH','RIGHT SIDE / EAST','BACK / NORTH']):
        box=draw.textbbox((0,0),label,font_size=20)
        draw.text((i*256+(256-box[2])/2,328),label,fill='#c8d8ce',font_size=20)
    labeled_path=OUT/'base-labeled.png';labeled.save(labeled_path)
    rows.append(dict(subject='Adult dromad unclothed reference',file=labeled_path.relative_to(REPO).as_posix(),direction='three-view',
        sha256=hashlib.sha256(labeled_path.read_bytes()).hexdigest(),size=[768,360],cutout_bounds=labeled.getchannel('A').getbbox(),
        kind='Labeled constructed turnaround; labels outside anatomy',state='Corrected side feet face east; far leg occluded'))
    record=dict(subject='Tam -> adult Dromad',authoring='Constructed vector body/head; no clothing',
        sources=['../rebuilt/model.json','../../../evidence/joppa-creature-catalogue.json'],
        canvas_per_view=[256,320],contact=[128,296],neck_seam=[128,186],views=views,
        masks='Separate body-mask and head-mask per view; these describe constructed source coverage, not a guarantee of ImageGen output registration',
        anatomy='Stylized nonsexual adult race template; compact torso, two hand-bearing arms, paired feet, long camel-like head/neck, dulla and hump',
        interpretation='Unseen anatomy and neutral feet are authored interpretation. Original yellow detail is not asserted to be boots or intrinsic foot pigmentation.',
        side_geometry='Right-facing silhouette; both foot extensions point east, the far leg is behind the near leg with a higher ground projection. No reused front-facing spread stance.',
        excluded_inputs='User clothed refinement image not read or supplied to generation',
        clothing='Not part of this phase. Later, one native equipped item over the refined unclothed body, then isolated extraction and registration checks.',
        source_script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (OUT/'construction.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    manifest_path=REPO/'art/manifest.json';manifest=json.loads(manifest_path.read_text())
    manifest['images']=[r for r in manifest['images'] if not r['file'].startswith('art/dromad/nude/')] + rows
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Unclothed adult dromad source views, separate body/head components and explicit masks saved; no clothing image consumed.')


if __name__=='__main__':main()
