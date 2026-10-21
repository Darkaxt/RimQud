"""Check prepared cast operations against the reviewed authoring compositions.

This is a bounded integration diagnostic, not a native renderer/game test.
Images are compared in memory; no source texture is changed or generated.
"""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageChops, ImageOps

REPO = Path(__file__).resolve().parents[1]


def check(root, version):
    staged = root / 'selected'
    source = staged / f'cast-v{version}.json'
    cast = json.loads(source.read_text())
    checks = []

    def image(row):
        path = root / row['file']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
        value = Image.open(path).convert('RGBA')
        return ImageOps.mirror(value) if row['assembly_mirror'] else value

    def item(operation):
        rows = operation['components']
        primary = np.array(image(next(row for row in rows if row['component'] == 'item'))).astype(float)
        alpha = primary[:, :, 3] / 255
        detail_row = next((row for row in rows if row['component'] == 'item-detail'), None)
        detail = np.array(image(detail_row)).astype(float) if detail_row else np.zeros_like(primary)
        da = np.minimum(detail[:, :, 3] / 255, alpha)
        premul = primary[:, :, :3] * (alpha - da)[:, :, None] + detail[:, :, :3] * da[:, :, None]
        result = np.zeros_like(primary, dtype=np.uint8)
        result[:, :, :3] = np.uint8(np.clip(np.round(np.divide(premul, alpha[:, :, None], out=np.zeros_like(premul), where=alpha[:, :, None] > 0)), 0, 255))
        result[:, :, 3] = np.uint8(np.round(alpha * 255))
        ownership = next((row for row in rows if row['component'] == 'body-overlay'), None)
        if ownership:
            mask = np.array(image(ownership))[:, :, 3].astype(float) / 255
            result[:, :, 3] = np.uint8(np.round(result[:, :, 3].astype(float) * (1 - mask)))
        result[result[:, :, 3] == 0, :3] = 0
        return Image.fromarray(result)

    for ident, actor in cast['cast'].items():
        model_blob = (staged / actor['model']['package_file']).read_bytes()
        assert hashlib.sha256(model_blob).hexdigest() == actor['model']['sha256']
        model = json.loads(model_blob)
        for facing, view in actor['views'].items():
            reviewed = model['views'][facing]
            reference = reviewed.get('neutral_preview', reviewed.get('assembled_preview'))
            expected_blob = (REPO / reference['path']).read_bytes()
            assert hashlib.sha256(expected_blob).hexdigest() == reference['sha256']
            expected = Image.open(REPO / reference['path']).convert('RGBA')
            actual = Image.new('RGBA', expected.size)
            if view['composition_mode'] == 'authored_depth_layers':
                for row in view['layers']:
                    actual.alpha_composite(image(row))
            else:
                for operation in view['draw_sequence']:
                    if operation['kind'] == 'body':
                        for row in operation['components']:
                            actual.alpha_composite(image(row))
                    else:
                        actual.alpha_composite(item(operation))
            delta = ImageChops.difference(actual, expected)
            visible = ImageChops.lighter(actual.getchannel('A'), expected.getchannel('A'))
            rgb = delta.convert('RGB')
            rgb.paste((0, 0, 0), (0, 0, *rgb.size), ImageOps.invert(visible.point(lambda a: 255 if a else 0)))
            checks.append(dict(entry=ident, facing=facing, composition_mode=view['composition_mode'], reference=reference,
                               visible_rgb_difference=rgb.getbbox(), alpha_difference=delta.getchannel('A').getbbox()))
    issues = [row for row in checks if row['visible_rgb_difference'] or row['alpha_difference']]
    result = dict(scope='Integration preparation diagnostic only: staged current operations versus already reviewed neutral authoring compositions. No native run or acceptance.',
                  cast_sha256=hashlib.sha256(source.read_bytes()).hexdigest(), checks=checks, issues=issues, native_acceptance=False)
    output = staged / f'cast-composition-diagnostic-v{version}.json'
    assert not output.exists(), 'Retain prior diagnostic evidence.'
    output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Cast composition comparisons:', len(checks), 'differences:', len(issues))
    for row in issues:
        print(row['entry'], row['facing'], row['visible_rgb_difference'], row['alpha_difference'])
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--cast-version', type=int, required=True)
    args = parser.parse_args()
    check(args.root, args.cast_version)
