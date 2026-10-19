"""Freeze the creature -> race -> descriptions/references packet for one ray-cat sample."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import struct
import sys

import UnityPy
from PIL import Image
from package_donor import DONOR_HASH

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / 'tools'))
from audit_joppa_anatomy import xml

# Authored anatomical landmarks, in unmodified source-image pixels. These are
# body/feet references, not bounding-box fitting (which changes scale with tails).
LANDMARKS = {
    'south': dict(contact_x=566, contact_y=1144, body_top=553, donor_top=20, donor_contact=61),
    'east': dict(contact_x=625, contact_y=942, body_top=490, donor_top=17, donor_contact=52),
    'north': dict(contact_x=625, contact_y=1058, body_top=480, donor_top=7, donor_contact=60),
}


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def original_reference(qud_data, output):
    source = qud_data / 'resources.assets'
    env = UnityPy.load(str(source))
    objects = {o.path_id: o for o in env.objects}
    info = objects[8371]
    base = info.read_typetree(check_read=False)
    assert base['m_Name'] == 'Assets_Content_Textures_Creatures_sw_kitty.bmp'
    # Installed exTextureInfo serialized layout, audited against its class fields.
    raw = info.get_raw_data()
    position = 28
    for _ in range(3):
        length = struct.unpack_from('<i', raw, position)[0]
        position = (position + 4 + length + 3) // 4 * 4
    file_id, texture_id = struct.unpack_from('<iq', raw, position)
    values = struct.unpack_from('<17i', raw, position + 12)
    rotated, trim, threshold, trim_x, trim_y, raw_w, raw_h, x, y, w, h, *rest = values
    assert file_id == 0 and texture_id == 224 and not rotated and not trim
    assert (raw_w, raw_h, x, y, w, h) == (16, 24, 54, 780, 16, 24)
    atlas = objects[texture_id].read().image
    tile = atlas.crop((x, atlas.height-y-h, x+w, atlas.height-y))
    path = output / 'ctesiphus-original-mask.png'
    tile.save(path)
    return dict(tile='creatures/sw_kitty.bmp', info_id=8371, atlas_id=texture_id,
                rect=[x, y, w, h], resources_sha256=sha(source), mask_sha256=sha(path),
                private_file=path.name, meaning='Original dual-color shader mask, not an interpreted creature identity')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--qud-data', type=Path, required=True)
    ap.add_argument('--donor-data', type=Path, required=True)
    ap.add_argument('--root', type=Path, required=True)
    args = ap.parse_args()
    assert sha(args.donor_data/'resources.assets') == DONOR_HASH
    study = json.loads((REPO/'evidence/joppa-anatomy-study.json').read_text(encoding='utf-8'))
    creatures = args.qud_data/'StreamingAssets/Base/ObjectBlueprints/Creatures.xml'
    assert sha(creatures) == study['definition_sha256']['ObjectBlueprints/Creatures.xml']
    definitions = {o.get('Name'): o for o in xml(creatures).findall('object')}
    creature, race = definitions['Ctesiphus'], definitions['Ray Cat']
    assert creature.get('Inherits') == 'Ray Cat' and race.get('Inherits') == 'BaseCat'
    assert definitions['BaseCat'].get('Inherits')
    description = race.find("part[@Name='Description']").get('Short')
    assert 'small kitty' in description and 'glassy fibers' in description
    donor = args.root/'donor'
    donor.mkdir(parents=True, exist_ok=True)
    reference = original_reference(args.qud_data, donor)
    metadata = json.loads((donor/'pawn-textures.json').read_text(encoding='utf-8'))
    inputs = json.loads((REPO/'art/manifest.json').read_text(encoding='utf-8'))['images']
    views = {}
    for row in inputs:
        direction = row['direction']
        source = REPO/row['file']
        assert sha(source) == row['sha256']
        image = Image.open(source).convert('RGBA')
        assert image.getchannel('A').getextrema() == (0, 255)
        points = LANDMARKS[direction]
        assert abs(points['contact_y']-row['cutout_bounds'][3]) <= 1
        scale = .9/64 * (points['donor_contact']-points['donor_top'])/(points['contact_y']-points['body_top'])
        filename = 'faithful-cat-'+direction+'.png'
        shutil.copy2(source, donor/filename)  # Unmodified generated pixels.
        original = next(m for m in metadata if m['file'] == 'cat-'+direction+'.png')
        assert sha(donor/original['file']) == original['png_sha256']
        views[direction] = dict(file=filename, sha256=row['sha256'], size=row['size'],
            landmarks=points, width=image.width*scale/(2/3), height=image.height*scale,
            center_x=(image.width/2-points['contact_x'])*scale/(2/3),
            center_z=(points['contact_y']-image.height/2)*scale,
            donor_reference=dict(asset_name=original['name'], source_id=original['source_id'],
                                 png_sha256=original['png_sha256'], resources_sha256=DONOR_HASH))
    packet = dict(creature='Ctesiphus', race='Ray Cat', lineage=['Ctesiphus','Ray Cat','BaseCat'],
        race_description=description, individual_description=creature.find("part[@Name='Description']").get('Short'),
        qud_definition_sha256=sha(creatures), original_model=reference, views=views,
        expected_body=dict(Body=1, Head=1, Face=1, Back=1, Foot=4, Feet=2, Tail=1),
        primary_color='m', detail_color='y',
        detail_policy='This neutral animal base uses native foreground tint; changed native detail colors retain the original sprite rather than inventing a detail mask.',
        geometry_units='width/center_x are Qud cells (2/3 world unit); height/center_z are world units. Pixels retain uniform physical scale.',
        west='Mirror east; no asymmetrical markings asserted',
        generation_prompts_sha256=sha(REPO/'art/ctesiphus/generation-prompts.json'))
    (args.root/'faithful-cat.json').write_text(json.dumps(packet, indent=2)+'\n', encoding='utf-8')
    print('Frozen Ctesiphus -> Ray Cat -> native race description + three actual donor references + original Qud mask; generated pixels copied unchanged.')


if __name__ == '__main__':
    main()
