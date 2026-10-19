"""Extract reviewed worn graphics, distinct from inventory icons, for local use."""
import argparse
import hashlib
import json
from pathlib import Path
import UnityPy
from package_donor import DONOR_HASH

FAMILIES = {
    'tunic': [(3464, 'TribalA_Male_north'), (3113, 'TribalA_Male_east'), (1274, 'TribalA_Male_south')],
    'robe': [(3552, 'Duster_Male_north'), (1828, 'Duster_Male_east'), (1625, 'Duster_Male_south')],
    'cloak': [(176, 'Cape_Male_north'), (751, 'Cape_Male_east'), (1210, 'Cape_Male_south')],
    'hat': [(224, 'CowboyHat_north'), (505, 'CowboyHat_east'), (986, 'CowboyHat_south')],
}


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

    def extract(file, identity, name):
        texture = objects[identity].read()
        assert texture.m_Name == name
        image = texture.image.convert('RGBA')
        alpha = image.getchannel('A')
        lo, hi = alpha.getextrema()
        # Compressed cape backgrounds decode to alpha 3, below the donor
        # cutout threshold. Preserve those genuine pixels rather than editing.
        assert lo < 128 and hi == 255, name
        target = args.output / file
        image.save(target)
        rows.append(dict(file=file, source_id=identity, name=name, width=image.width,
                         height=image.height, alpha_bounds=alpha.getbbox(), alpha_range=[lo, hi],
                         cutout_bounds=alpha.point(lambda value: 255 if value >= 128 else 0).getbbox(),
                         png_sha256=hashlib.sha256(target.read_bytes()).hexdigest()))

    for family, textures in FAMILIES.items():
        for direction, (identity, name) in zip(['north', 'east', 'south'], textures):
            extract(f'worn-{family}-{direction}.png', identity, name)
    extract('held-sword.png', 228, 'Longsword')
    (args.output/'apparel-textures.json').write_text(json.dumps(rows, indent=2)+'\n', encoding='utf-8')
    print('Extracted thirteen reviewed worn/held graphics; raw resources remain local.')


if __name__ == '__main__':
    main()
