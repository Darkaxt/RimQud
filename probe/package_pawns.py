"""Extract the small hash-pinned local donor set for the layered NPC/prop scene."""
import argparse
import hashlib
import json
from pathlib import Path
import UnityPy
from package_donor import DONOR_HASH

TEXTURES = {
    'human-body-north.png': (691, 'Naked_Male_north'),
    'human-body-east.png': (367, 'Naked_Male_east'),
    'human-body-south.png': (2302, 'Naked_Male_south'),
    'human-head-north.png': (1329, 'Male_Average_Normal_north'),
    'human-head-east.png': (2929, 'Male_Average_Normal_east'),
    'human-head-south.png': (2403, 'Male_Average_Normal_south'),
    'human-body-female-north.png': (1854, 'Naked_Female_north'),
    'human-body-female-east.png': (2143, 'Naked_Female_east'),
    'human-body-female-south.png': (1653, 'Naked_Female_south'),
    'human-head-female-north.png': (1260, 'Female_Average_Normal_north'),
    'human-head-female-east.png': (1596, 'Female_Average_Normal_east'),
    'human-head-female-south.png': (3108, 'Female_Average_Normal_south'),
    'dromedary-reference-north.png': (3049, 'Dromedary_north'),
    'dromedary-reference-east.png': (526, 'Dromedary_east'),
    'dromedary-reference-south.png': (2777, 'Dromedary_south'),
    'cat-north.png': (255, 'Cat_north'),
    'cat-east.png': (2037, 'Cat_east'),
    'cat-south.png': (1253, 'Cat_south'),
    'chair-north.png': (3213, 'DiningChair_north'),
    'chair-east.png': (3157, 'DiningChair_east'),
    'chair-south.png': (1647, 'DiningChair_south'),
}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--donor-data', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    source = args.donor_data / 'resources.assets'
    assert hashlib.sha256(source.read_bytes()).hexdigest() == DONOR_HASH
    args.output.mkdir(parents=True, exist_ok=True)
    env = UnityPy.load(str(source))
    objects = {o.path_id: o for o in env.objects if o.type.name == 'Texture2D'}
    rows = []
    for filename, (identity, name) in TEXTURES.items():
        texture = objects[identity].read()
        assert texture.m_Name == name
        image = texture.image.convert('RGBA')
        assert image.getchannel('A').getextrema() == (0, 255), name
        bbox = image.getchannel('A').getbbox()
        assert bbox is not None
        target = args.output / filename
        image.save(target)
        rows.append(dict(file=filename, source_id=identity, name=name,
                         width=image.width, height=image.height, alpha_bounds=bbox,
                         png_sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
    (args.output / 'pawn-textures.json').write_text(json.dumps(rows, indent=2) + '\n')
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
