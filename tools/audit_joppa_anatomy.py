"""Read installed definitions for the bounded Joppa art/body study; no game writes."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def xml(path):
    # Some shipped descriptions contain numeric references illegal in XML 1.0.
    # Normalize those references in this offline read only; installed bytes stay intact.
    def numeric(match):
        value = match[1]
        number = int(value[1:], 16) if value.startswith('x') else int(value)
        valid = number in (9, 10, 13) or 32 <= number <= 0xd7ff or 0xe000 <= number <= 0xfffd or 0x10000 <= number <= 0x10ffff
        return match[0] if valid else '\ufffd'
    return ET.fromstring(re.sub(r'&#(x[0-9a-fA-F]+|[0-9]+);', numeric, path.read_text(encoding='utf-8-sig')))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--qud-data', type=Path, required=True)
    ap.add_argument('--rimworld-data', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    repo = Path(__file__).resolve().parents[1]
    base = args.qud_data / 'StreamingAssets/Base'
    definitions = {}
    for path in sorted((base / 'ObjectBlueprints').glob('*.xml')):
        for obj in xml(path).findall('object'):
            definitions[obj.get('Name')] = (obj, path)
    used = set()

    def inherited(name, ancestry=()):
        assert name not in ancestry, ('inheritance cycle', name)
        obj, path = definitions[name]
        used.add(path)
        parent = obj.get('Inherits')
        out = inherited(parent, ancestry + (name,)) if parent in definitions else {}
        out = {k: v.copy() for k, v in out.items() if v.get('Value') != '*noinherit'}
        for child in obj:
            name_key = child.get('Name') or child.get('Blueprint') or ''
            if child.tag.startswith('remove'):
                out.pop((child.tag[6:], name_key), None)
                continue
            key = (child.tag, name_key)
            if child.get('Value') == '*delete':
                out.pop(key, None)
            else:
                out[key] = {**out.get(key, {}), **child.attrib}
        return out

    contract = json.loads((repo / 'probe/joppa-coverage.json').read_text(encoding='utf-8'))
    rows = []
    for entry in contract['entries']:
        name = entry['blueprint']
        if not entry['baseline_selected']:
            continue
        merged = inherited(name)
        render = merged.get(('part', 'Render'), {})
        body = merged.get(('part', 'Body'), {})
        rows.append(dict(blueprint=name, source=definitions[name][1].name,
                         tile=render.get('Tile'), tile_color=render.get('TileColor'),
                         foreground=render.get('ColorString'), detail=render.get('DetailColor'),
                         anatomy=body.get('Anatomy'), species=merged.get(('tag', 'Species'), {}).get('Value'),
                         gender=merged.get(('tag', 'Gender'), {}).get('Value'),
                         random_gender=merged.get(('tag', 'RandomGender'), {}).get('Value'),
                         mutations=[v for (kind, _), v in merged.items() if kind == 'mutation'],
                         random_tile=merged.get(('builder', 'RandomTile'), {}).get('Tiles'),
                         age_evidence=[v for (kind, key), v in merged.items() if key in {'Age', 'LifeStage', 'Child', 'Juvenile'}]))
    assert len(rows) == 67
    assert next(x for x in rows if x['blueprint'] == 'Mehmet')['random_tile'] is None
    assert next(x for x in rows if x['blueprint'] == 'WatervineFarmerJoppa')['random_tile'].count(',') == 5
    actors = [x for x in rows if x['anatomy']]
    assert len(actors) == 10
    bodies = xml(base / 'Bodies.xml')
    anatomy = {n.get('Name'): [dict(p.attrib) for p in n.iter('part')]
               for n in bodies.iter('anatomy') if n.get('Name') in {a['anatomy'] for a in actors}}
    rw = args.rimworld_data.parent / 'Data/Core/Defs/Misc'
    body_file = rw / 'BodyTypeDefs/BodyTypes.xml'
    life_file = rw / 'LifeStageDefs/LifeStages.xml'
    evidence = dict(scope='Installed static definitions for 67 selected baseline types. Not a runtime body-tree census; mutation execution, dismemberment and random builders can change instances.',
                    qud_assembly_sha256=digest(args.qud_data / 'Managed/Assembly-CSharp.dll'),
                    rimworld_assembly_sha256=digest(args.rimworld_data / 'Managed/Assembly-CSharp.dll'),
                    definition_sha256={str(p.relative_to(base)).replace('\\', '/'): digest(p) for p in sorted(used | {base/'Bodies.xml'})},
                    donor_definition_sha256={str(p.relative_to(rw)).replace('\\', '/'): digest(p) for p in [body_file, life_file]},
                    art_targets=rows, actor_blueprints=[a['blueprint'] for a in actors],
                    base_anatomies=anatomy,
                    donor_body_types=[b.findtext('defName') for b in xml(body_file)],
                    donor_human_life_stages=[dict(name=l.findtext('defName'), body_size=l.findtext('bodySizeFactor'), head_size=l.findtext('headSizeFactor'), developmental_stage=l.findtext('developmentalStage')) for l in xml(life_file) if 'Humanlike' in (l.findtext('defName') or '')],
                    checks={'selected_contract_reconciled': True, 'removed_random_builder_respected': True, 'age_fields_found_in_selected_actors': any(a['age_evidence'] for a in actors)})
    assert evidence['qud_assembly_sha256'] == 'cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7'
    assert evidence['rimworld_assembly_sha256'] == '5cf1b5be399d5b1c9c56ca72c9d35b4ecf307feacf5859d04ac5a1aa5926356a'
    args.output.write_text(json.dumps(evidence, indent=2) + '\n', encoding='utf-8', newline='\n')
    print('Reconciled 67 static art targets and ten actor blueprints against installed sources; runtime anatomy is explicitly separate.')


if __name__ == '__main__':
    main()
