"""Extract only reviewed Joppa prop/scenery resources from local donor installs."""
import argparse
import hashlib
import json
from pathlib import Path

import UnityPy
from package_donor import DONOR_HASH

FAMILIES = {
    'bed': [(1268, 'Bed_north'), (1676, 'Bed_east'), (1155, 'Bed_south')],
    'bedroll': [(3011, 'Bedroll_north'), (2576, 'Bedroll_east'), (848, 'Bedroll_south')],
    'dresser': [(318, 'Dresser_north'), (700, 'Dresser_east'), (2802, 'Dresser_south')],
    'table': [(1644, 'Table1x2_north'), (1443, 'Table1x2_east')],
    'bookcase': [(612, 'BookcaseSmall_north'), (3227, 'BookcaseSmall_east'), (2945, 'BookcaseSmall_south')],
    'workbench': [(1326, 'TableMachining_north'), (1944, 'TableMachining_east'), (1008, 'TableMachining_south')],
    'tailor': [(1926, 'TableTailorElectric_north'), (1609, 'TableTailorElectric_east'), (3280, 'TableTailorElectric_south')],
}
SINGLE = {'wall-planks.png': (1398, 'Wall_Atlas_Planks'),
          'wall-metal.png': (392, 'Wall_Atlas_Smooth'),
          'fence.png': (1474, 'Fence_Atlas_Smooth'), 'bridge.png': (638, 'WoodFloor')}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--donor-data', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    source = args.donor_data / 'resources.assets'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == DONOR_HASH
    env = UnityPy.load(str(source))
    objects = {o.path_id: o for o in env.objects if o.type.name == 'Texture2D'}
    args.output.mkdir(parents=True, exist_ok=True)
    rows = []

    def save(filename, image, **origin):
        image = image.convert('RGBA')
        bbox = image.getchannel('A').getbbox()
        assert bbox is not None
        target = args.output / filename
        image.save(target)
        rows.append(dict(file=filename, width=image.width, height=image.height,
                         alpha_bounds=bbox, png_sha256=hashlib.sha256(target.read_bytes()).hexdigest(), **origin))

    def extract(filename, identity, name):
        texture = objects[identity].read()
        assert texture.m_Name == name
        save(filename, texture.image, source_id=identity, name=name, source_package='RimWorld core')

    for family, textures in FAMILIES.items():
        for direction, (identity, name) in zip(['north', 'east', 'south'], textures):
            extract(f'prop-{family}-{direction}.png', identity, name)
        if len(textures) == 2:  # inspected Graphic_Multi south fallback to north
            identity, name = textures[0]
            extract(f'prop-{family}-south.png', identity, name)
    for filename, (identity, name) in SINGLE.items():
        extract(filename, identity, name)
    (args.output / 'coverage-textures.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
