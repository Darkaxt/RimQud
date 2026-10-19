"""Add a small hash-pinned donor texture selection to an existing local package."""
import argparse
import hashlib
import json
from pathlib import Path
import UnityPy
from package_donor import DONOR_HASH

TEXTURES = {'crop.png': (1136, 'RicePlantA'), 'reed.png': (1040, 'HaygrassA'),
            'grass.png': (1797, 'GrassA'), 'sand.png': (525, 'Sand'),
            'door.png': (2541, 'DoorSimple_Mover'), 'marsh.png': (2096, 'Marsh'),
            'water-shallow.png': (2778, 'WaterShallowRamp'),
            'water-deep.png': (3315, 'WaterDeepRamp')}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--donor-data', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    path = args.donor_data / 'resources.assets'
    assert hashlib.sha256(path.read_bytes()).hexdigest() == DONOR_HASH
    env = UnityPy.load(str(path))
    objects = {o.path_id: o for o in env.objects if o.type.name == 'Texture2D'}
    rows = []
    for filename, (identity, name) in TEXTURES.items():
        texture = objects[identity].read()
        assert texture.m_Name == name
        target = args.output / filename
        texture.image.save(target)
        rows.append(dict(file=filename, source_id=identity, name=name,
                         width=texture.m_Width, height=texture.m_Height,
                         png_sha256=hashlib.sha256(target.read_bytes()).hexdigest()))
    (args.output / 'joppa-textures.json').write_text(json.dumps(rows, indent=2))
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
