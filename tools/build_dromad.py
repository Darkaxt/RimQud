"""Construct the bounded Tam sample from editable paths; no generative model.

Requires resvg-py==0.5.0 and Pillow. Every view uses the same 256x320 registration:
ground contact (128,296), neck seam (128,186). Body includes its limbs and hump;
the head layer includes the long neck. No independent animation rig is implied.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil

from PIL import Image
import resvg_py

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / 'art/dromad/rebuilt'
SIZE = [256, 320]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path(d, fill='url(#skin)', stroke='#303535', width=3):
    return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'


def ellipse(cx, cy, rx, ry, fill):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}"/>'


def shapes(view):
    # These paths are the authored interpretation. The silhouette is compact and
    # upright as in the native icon, not a four-legged donor camel recolor.
    if view == 'east':
        body = path('M80 208 C59 190 66 151 91 146 C115 142 119 166 130 176 C159 180 176 208 170 248 L162 284 Q149 300 138 292 L132 266 L116 266 L106 293 Q88 299 87 286 L84 253 Q65 252 70 236 Z')
        body += path('M145 194 Q173 201 175 225 L163 244 Q151 248 147 239 L155 218 L140 210', '#bcbcbc')
        body += path('M84 170 Q73 187 87 207 M101 230 Q119 241 141 230', 'none', '#747a78', 2)
        feet = path('M88 282 Q97 279 108 284 L106 294 L87 294 Z', '#e8e8e8') + path('M138 282 L162 281 L160 292 Q146 297 138 292 Z', '#dadada')
        head = path('M114 196 C109 168 118 139 127 118 L129 87 Q119 80 127 66 L124 48 Q134 48 143 61 L160 57 Q170 49 184 60 L203 68 Q229 64 234 80 Q238 94 220 100 L190 101 Q175 111 165 108 C156 142 155 173 151 194 Q136 207 114 196 Z')
        head += path('M146 66 Q141 51 149 39 Q164 41 168 58', '#e4e4e4')
        head += path('M174 81 Q185 87 197 84 M210 92 Q220 94 227 89', 'none', '#666d6a', 2)
        head += ellipse(175, 74, 3.5, 3.5, '#26312f') + ellipse(225, 80, 2.4, 2, '#414a47')
        head += path('M156 113 Q170 117 170 137 Q165 153 151 149', '#b1b8b3', '#303535', 2)
        detail = path('M158 119 Q166 123 165 136 Q162 146 156 143 Z', '#e2e2e2', 'none')
        # Side profile: covered hump/back on the LEFT, chest/front on the RIGHT.
        # Only the near sleeve is visible. The front opening stays on the chest,
        # rather than remaining centered as if the garment faced the viewer.
        robe = path('M110 177 Q100 148 83 153 Q60 156 64 186 L77 210 L79 278 Q114 293 163 280 L156 232 L173 231 L176 218 L158 193 L149 184 Q131 194 110 177 Z', 'url(#cloth)')
        robe += path('M110 177 Q125 197 149 184 M151 191 L154 207 M154 238 L157 276 M83 192 Q87 218 89 275 M119 221 L116 282', 'none', '#6f7b77', 2)
        robe += path('M147 201 Q154 207 158 220 L173 231 M82 277 Q116 289 161 279', 'none', '#dee4e0', 2)
        held = path('M179 277 L183 215 Q171 205 177 193 Q187 183 197 193 Q204 205 192 215 L188 279 Z', 'url(#wood)')
    else:
        north = view == 'north'
        body = path('M99 176 C84 156 100 139 116 147 Q136 140 153 161 L159 187 Q183 202 181 236 L169 267 L163 290 Q151 299 139 291 L134 270 L122 270 L117 292 Q103 300 91 290 L87 265 Q72 246 76 220 Q78 193 99 176 Z')
        body += path('M87 199 L77 237 Q78 249 90 247 L98 217 M165 198 L178 236 Q177 250 165 246 L157 218', '#b9bdbb')
        body += path('M100 164 Q125 150 150 171 M105 241 Q128 250 153 239', 'none', '#777e7b', 2)
        feet = path('M91 283 L117 283 L117 294 L90 294 Z', '#e4e4e4') + path('M139 283 L164 283 L165 294 L138 294 Z', '#d7d7d7')
        if north:
            head = path('M109 193 C108 162 102 129 105 105 Q94 90 101 71 L93 52 Q102 44 115 58 Q128 53 142 58 Q155 44 164 52 L157 72 Q164 91 151 106 C153 142 146 172 147 193 Q128 201 109 193 Z')
            head += path('M111 74 Q127 64 145 75 M123 90 L126 174', 'none', '#8b918d', 2)
            detail = ''
        else:
            head = path('M108 193 C108 163 103 133 105 111 Q91 96 101 75 L92 56 Q99 47 111 60 Q127 53 144 61 Q155 46 164 55 L155 77 Q164 97 151 111 C150 138 147 169 149 194 Q129 206 108 193 Z')
            head += path('M108 87 Q127 77 149 89 L151 106 Q129 120 105 106 Z', '#dddeda')
            head += ellipse(112, 80, 3, 3, '#26312f') + ellipse(144, 80, 3, 3, '#26312f')
            head += path('M112 99 L117 100 M138 99 L143 98 M117 109 Q128 112 140 109', 'none', '#555f5a', 2)
            head += path('M119 124 Q144 124 141 148 Q128 169 115 146 Z', '#b9bdb8', '#303535', 2)
            detail = path('M122 130 Q137 128 135 145 Q126 156 121 144 Z', '#e8e8e8', 'none')
        robe = path('M105 181 Q128 191 151 181 L170 192 L188 226 L171 236 L159 214 L175 281 Q129 297 80 281 L96 214 L84 236 L67 226 L85 193 Z', 'url(#cloth)')
        robe += path('M99 219 L91 277 M155 220 L164 277', 'none', '#6f7b77', 2)
        if not north:
            robe += path('M105 181 Q127 204 151 181 M127 194 L121 278', 'none', '#7d8984', 2)
        else:
            robe += path('M105 182 Q128 189 151 182 M97 207 Q128 192 160 206 M126 218 Q136 248 133 282', 'none', '#89968e', 2)
        robe += path('M82 280 Q127 292 174 280', 'none', '#e1e7e3', 2)
        held = path('M184 278 L181 216 Q167 205 175 194 Q184 186 194 193 Q201 207 190 216 L193 278 Z', 'url(#wood)')
    return {'body': body, 'body-detail': feet, 'head': head,
            'head-detail': detail, 'robe': robe, 'shillelagh': held}


def svg(content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="256" height="320" viewBox="0 0 256 320">
<defs><linearGradient id="skin" x2=".85" y2="1"><stop stop-color="#f1f1ed"/><stop offset=".6" stop-color="#c2c6c1"/><stop offset="1" stop-color="#8f9690"/></linearGradient>
<linearGradient id="cloth" x2="1" y2=".7"><stop stop-color="#e9eeeb"/><stop offset=".55" stop-color="#bccac2"/><stop offset="1" stop-color="#8c9b91"/></linearGradient>
<linearGradient id="wood" x2="1" y2="0"><stop stop-color="#c3c7bd"/><stop offset="1" stop-color="#7d887b"/></linearGradient></defs>
{content}</svg>'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root', type=Path, required=True)
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    catalogue = json.loads((REPO/'evidence/joppa-creature-catalogue.json').read_text())
    creature = next(c for c in catalogue['creatures'] if c['creature'] == 'Tam')
    raw = json.loads((args.root/'runs/catalogue-20261020/joppa-creature-catalogue.json').read_text())
    native = next(c for c in raw['actors'] if c['blueprint'] == 'Tam')
    topology = []
    by_id = {p['id']: p for p in native['parts']}
    for p in native['parts']:
        chain = []
        node = p
        while node is not None:
            chain.append(f"{node['type']}/{node['variant']}/{node['laterality']}")
            node = by_id.get(node['parent'])
        topology.append('>'.join(reversed(chain)))
    rows, views = [], {}
    donor = args.root/'donor'
    for direction in ['south', 'east', 'north']:
        layers = []
        for component, content in shapes(direction).items():
            source = OUT/f'{component}-{direction}.svg'
            source.write_text(svg(content)+'\n', encoding='utf-8', newline='\n')
            output = source.with_suffix('.png')
            output.write_bytes(resvg_py.svg_to_bytes(svg_path=str(source), skip_system_fonts=True))
            filename = 'dromad-'+output.name
            shutil.copy2(output, donor/filename)
            row = dict(subject='Adult dromad / Tam', file=output.relative_to(REPO).as_posix(),
                direction=direction, sha256=sha(output), size=SIZE,
                cutout_bounds=Image.open(output).getchannel('A').getbbox(),
                source_svg=source.relative_to(REPO).as_posix(), source_sha256=sha(source),
                kind='Deterministically rasterized original vector geometry', state='Native sample verification pending')
            rows.append(row)
            layer = 0 if component == 'body' else .0001 if component == 'body-detail' else .001 if component == 'head' else .0011 if component == 'head-detail' else .0007 if component == 'robe' else -.0002 if direction == 'north' else .0018
            if direction == 'north' and component.startswith('head'):
                layer = .0002 if component == 'head' else .0003
            layers.append(dict(component=component, file=filename, sha256=sha(output), layer=layer,
                color_role='detail' if component.endswith('detail') else 'equipment' if component in ['robe','shillelagh'] else 'foreground',
                width=1.65*256/320/(2/3), height=1.65, center_x=0, center_z=(296/320-.5)*1.65))
        views[direction] = layers
    packet = dict(creature='Tam', race='Dromad', race_description=creature['race_input']['description'],
        original_model=catalogue['original_models']['assets_content_textures_creatures_sw_dromad.bmp'],
        references=catalogue['reference_families']['dromad_camel_features'],
        anatomy='Humanoid', expected_topology=sorted(topology), views=views,
        interpretation='Compact upright two-contact body follows the original icon; hand-bearing anatomy is corroborated by native slots, not inferred from slots alone. Exact unseen surfaces are authored, not canonical anatomy evidence.',
        registration=dict(canvas=SIZE, contact=[128,296], neck_seam=[128,186], physical_height=1.65),
        equipment=[dict(blueprint=p['equipped']['blueprint'],slot=p['type'],description=p['equipped']['description']) for p in native['parts'] if p['equipped']],
        west='Mirror east; no asymmetric personal markings authored',
        supported_equipment=['Cloth Robe','Shillelagh'],
        policy='Native foreground and detail tint separate body/head layers. Equipment tint follows its own equipped item. All body parts remain in the body graphic; no invented arm/leg rig.',
        authoring='Explicit SVG paths; resvg-py==0.5.0; no ImageGen',
        source_sha256=sha(Path(__file__)))
    (OUT/'model.json').write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8')
    (args.root/'dromad.json').write_text(json.dumps(packet,indent=2)+'\n',encoding='utf-8')
    manifest_file = REPO/'art/manifest.json'
    manifest = json.loads(manifest_file.read_text())
    manifest['generation_tool'] = 'Per asset provenance: built-in image_gen drafts and explicitly authored vector geometry'
    manifest['images'] = [r for r in manifest['images'] if '/rebuilt/' not in r['file']] + rows
    for r in manifest['images']:
        if r['file'].startswith('art/dromad/head-'):
            r['state']='Superseded ImageGen concept; not production model or native integration'
    # Keep the previously saved tunic draft attributable, without adopting it for Tam.
    tunic = REPO/'art/woven-tunic/south.png'
    if tunic.exists() and not any(r['file']=='art/woven-tunic/south.png' for r in manifest['images']):
        im=Image.open(tunic)
        manifest['images'].append(dict(subject='Woven Tunic draft',file='art/woven-tunic/south.png',direction='south',
            sha256=sha(tunic),size=list(im.size),cutout_bounds=im.getchannel('A').getbbox(),
            kind='Earlier ImageGen garment concept',state='Retained draft; not used in deterministic Tam sample'))
    manifest_file.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Built three registered dromad views: body/head plus detail masks, robe and held shillelagh. Editable SVGs and native packet written.')


if __name__ == '__main__':
    main()
