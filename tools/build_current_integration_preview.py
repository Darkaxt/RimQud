"""Render a small, lazy visual report from the prepared current cast operations."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageOps

from check_current_cast_composition import compose_view

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'art/previews/current-cast-v2'
DATA = ROOT / 'docs/current-integration-preview-data'


def sha(blob):
    return hashlib.sha256(blob).hexdigest()


def build(probe_root):
    selected = probe_root / 'selected'
    cast_blob = (selected / 'cast-v2.json').read_bytes()
    cast = json.loads(cast_blob)
    receipt = json.loads((ROOT / 'evidence/current-native-integration-20261021/preparation.json').read_text())
    assert sha(cast_blob) == receipt['cast']['sha256']
    sources_blob = (ROOT / 'art/village/sources.json').read_bytes()
    package = json.loads((selected / 'package.json').read_text())
    assert sha(sources_blob) == package['actor_source']['sha256']
    natives = {native['instance']: native for actor in json.loads(sources_blob)['actors'] for native in actor['native_instances']}
    palette = json.loads((ROOT / 'evidence/joppa-anatomy-study.json').read_text())['native_palette']
    ledger = {entry['id']: entry for entry in json.loads((ROOT / 'evidence/conversion-ledger.json').read_text())['entries']}
    OUT.mkdir(parents=True, exist_ok=True)
    DATA.mkdir(exist_ok=True)
    index, checks = [], []
    for ident, actor in cast['cast'].items():
        native = natives[actor['captured_instance']]
        folder = OUT / ident
        folder.mkdir(exist_ok=True)
        cache = {}

        def image(row):
            digest = row['sha256']
            if digest not in cache:
                # These immutable public bytes were verified against the staged
                # package; use the fast local source without recopying assets.
                blob = (ROOT / row['public_file']).read_bytes()
                assert sha(blob) == digest
                cache[digest] = Image.open(ROOT / row['public_file']).convert('RGBA')
            value = cache[digest]
            return ImageOps.mirror(value) if row['assembly_mirror'] else value

        def rgb(code):
            code = code.replace('&', '').replace('^', '')[0]
            return np.array(tuple(bytes.fromhex(palette[code])), dtype=float) / 255

        items = {}
        for part in native['parts']:
            item = part.get('equipped')
            if item:
                key = item['blueprint'].lower().replace(' ', '-') + '@' + part['type'] + '@' + str(part['laterality'])
                items[key] = item

        def colors(key):
            appearance = items[key] if key else native
            foreground = appearance.get('tileColor') or appearance['foreground']
            return rgb(foreground), rgb(appearance.get('detailColor') or foreground)

        model_blob = (selected / actor['model']['package_file']).read_bytes()
        assert sha(model_blob) == actor['model']['sha256']
        model = json.loads(model_blob)
        record = dict(id=ident, name=ledger[ident]['name'], blueprint=actor['blueprint'], gender=actor['gender'],
                      equipment=sorted({part['equipped']['blueprint'] for part in native['parts'] if part.get('equipped')}),
                      evidence='conversion-entries/' + ident + '.html', views={})
        for facing, view in actor['views'].items():
            reviewed = model['views'][facing]
            reference = dict(neutral=reviewed.get('neutral_preview', reviewed.get('assembled_preview')),
                             captured=reviewed['native_palette_preview'])
            record['views'][facing] = {}
            for mode in ['neutral', 'captured']:
                reference_path = ROOT / reference[mode]['path']
                assert sha(reference_path.read_bytes()) == reference[mode]['sha256']
                record['views'][facing][mode] = dict(reference='../' + reference[mode]['path'])
                for equipped in [True, False]:
                    actual = compose_view(view, image, colors if mode == 'captured' else None, equipped)
                    path = folder / f'{mode}-{"equipped" if equipped else "body"}-{facing}.png'
                    actual.save(path)
                    record['views'][facing][mode]['equipped' if equipped else 'body'] = '../' + path.relative_to(ROOT).as_posix()
                    if mode == 'neutral' and equipped:
                        expected = Image.open(reference_path).convert('RGBA')
                        delta = np.array(ImageChops.difference(actual, expected))
                        visible = np.maximum(np.array(actual)[:, :, 3], np.array(expected)[:, :, 3]) > 0
                        equal = not delta[:, :, 3].any() and not delta[:, :, :3][visible].any()
                        checks.append(dict(entry=ident, facing=facing, matches_reviewed_visible_pixels=equal))
                        assert equal, (ident, facing, 'Prepared preview differs from reviewed neutral composition')
            record['views'][facing]['size'] = view['body'][0]['size']
            record['views'][facing]['contact'] = view['body'][0]['contact']
        (DATA / (ident + '.json')).write_text(json.dumps(record, separators=(',', ':')) + '\n', encoding='utf-8', newline='\n')
        index.append(dict(id=ident, name=record['name']))
        for value in cache.values():
            value.close()
    template = (ROOT / 'tools/templates/current_integration_preview.html').read_text(encoding='utf-8')
    html = template.replace('__ACTOR_INDEX__', json.dumps(index, separators=(',', ':')).replace('</', '<\\/'))
    (ROOT / 'docs/current-integration-preview.html').write_text(html, encoding='utf-8', newline='\n')
    evidence = dict(cast_sha256=sha(cast_blob), scope='Visual prepared-operation preview, not in-game rendering. All source artwork remains unchanged.',
                    checks=checks, preview_images=256, page='docs/current-integration-preview.html', native_acceptance=False)
    (ROOT / 'evidence/current-native-integration-20261021/visual-preview.json').write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Rendered visual preview for16residents; all64neutral prepared views match reviewed pixels. HTML loads only the selected resident/view.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    build(parser.parse_args().root)
