"""Bind the selected current artwork to the isolated native rendering test."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]


def canonical(tile):
    tile = tile.lower()
    return tile if tile.startswith('assets_content_textures_') else 'assets_content_textures_' + tile.replace('/', '_')


def build(root):
    selected = root / 'selected'
    package = json.loads((selected / 'package.json').read_text())
    cast = json.loads((selected / 'cast-v2.json').read_text())
    out = selected / 'runtime'
    out.mkdir(exist_ok=True)
    exports = {}

    def read(ref):
        blob = (ROOT / ref['path']).read_bytes()
        assert hashlib.sha256(blob).hexdigest() == ref['sha256'], ref['path']
        return json.loads(blob)

    def image(ref, mirror=False, mask=False, size=None):
        if not ref:
            return None
        path = ref.get('public_file', ref.get('path'))
        key = (path, mirror, mask, tuple(size) if size else None)
        if key not in exports:
            blob = (ROOT / path).read_bytes()
            assert hashlib.sha256(blob).hexdigest() == ref['sha256'], path
            with Image.open(ROOT / path) as source:
                value = source.convert('L' if mask else 'RGBA')
            if mirror:
                value = ImageOps.mirror(value)
            if size:
                value = value.resize(size, Image.Resampling.LANCZOS)
            else:
                value.thumbnail((256, 256), Image.Resampling.LANCZOS)
            name = hashlib.sha256(repr(key).encode()).hexdigest() + '.png'
            value.save(out / name)
            exports[key] = name
        return exports[key]

    def row(layer, size):
        mirror = layer['assembly_mirror']
        return dict(file=image(layer, mirror, size=size), role=layer['color_role'],
                    key=layer.get('equipment_key'),
                    weight=image(layer.get('detail_weight'), mirror, True, size))

    actors = {}
    for ident, actor in cast['cast'].items():
        views = {}
        for facing, view in actor['views'].items():
            frame = view['body'][0]
            w, h = frame['size']
            size = (round(w * 256 / h), 256)
            ops = []
            if view['composition_mode'] == 'authored_depth_layers':
                ops = [dict(kind='layer', **row(layer, size)) for layer in view['layers']]
            else:
                for operation in view['draw_sequence']:
                    if operation['kind'] == 'body':
                        ops.extend(dict(kind='layer', **row(layer, size)) for layer in operation['components'])
                    else:
                        components = operation['components']
                        primary = next(x for x in components if x['component'] == 'item')
                        detail = next((x for x in components if x['component'] == 'item-detail'), None)
                        ownership = next((x for x in components if x['component'] == 'body-overlay'), None)
                        ops.append(dict(kind='item', file=image(primary, primary['assembly_mirror'], size=size),
                                        detail=image(detail, detail['assembly_mirror'], size=size) if detail else None,
                                        ownership=image(ownership, ownership['assembly_mirror'], size=size) if ownership else None,
                                        key=operation['key']))
            views[facing] = dict(size=size, width=frame['width'], height=frame['height'],
                                 center_x=frame['center_x'], center_z=frame['center_z'], ops=ops)
        actors[ident] = {k: actor[k] for k in ['blueprint', 'gender', 'species', 'anatomy', 'expected_topology']}
        actors[ident].update(views=views, equipment=sorted(x['key'] for x in actor['views']['south']['equipment']))

    scenery, omissions = {}, []

    def recipe(node):
        if 'views' in node:
            return recipe(node['views']['south'])
        if 'layers' in node and isinstance(node['layers'], list) and node['layers'] and isinstance(node['layers'][0], dict):
            return [dict(kind='layer', file=image(layer['texture']), role=layer['color_role']) for layer in node['layers'] if 'texture' in layer]
        primary = node.get('primary', node.get('neutral'))
        if primary and isinstance(primary, dict):
            return [dict(kind='item', file=image(primary), detail=image(node.get('detail')), key=None)]
        return None

    def aliases(node):
        values = []
        for field in ['native_tile', 'tile', 'source_tile']:
            if isinstance(node.get(field), str):
                values.append(node[field])
        for field in ['native_tiles', 'aliases', 'native_tile_aliases']:
            if isinstance(node.get(field), list):
                values.extend(x for x in node[field] if isinstance(x, str))
        return values

    def source_tiles(model):
        ref = model.get('source_packet', model.get('source'))
        if not isinstance(ref, dict) or not ref.get('path', '').endswith('.json'):
            return []
        packet = read(ref)
        result = []
        def walk(value):
            if isinstance(value, dict):
                for k, v in value.items():
                    if k.lower() in ['tile', 'native_tile'] and isinstance(v, str) and v.lower().endswith(('.png', '.bmp')):
                        result.append(v)
                    elif isinstance(v, (dict, list)):
                        walk(v)
            elif isinstance(value, list):
                for v in value:
                    walk(v)
        walk(packet)
        return sorted(set(result))

    for ident, ref in package['scenery'].items():
        model = read(ref)
        if ident in ['SCN-DIRTPATH', 'SCN-DIRTFLOOR', 'SCN-POND', 'SCOPE-DIRTY']:
            continue
        blueprint = model.get('blueprint', 'Door' if ident == 'SCN-DOOR' else None)
        if not blueprint:
            raise ValueError((ident, 'Missing exact blueprint'))
        bindings = {}
        mask_bindings = {}
        def bind(node):
            ops = recipe(node)
            tiles = aliases(node)
            if ops:
                for tile in tiles:
                    bindings[canonical(tile)] = ops
                if 'mask' in node:
                    mask_bindings[str(node['mask'])] = ops
            # Only south has a native facing binding for fixed scenery.
            for field in ['states', 'frames', 'variants']:
                values = node.get(field)
                if isinstance(values, dict):
                    for child in values.values():
                        if isinstance(child, dict): bind(child)
                elif isinstance(values, list):
                    for child in values:
                        if isinstance(child, dict): bind(child)
            if 'views' in node:
                bind(node['views']['south'])
        bind(model)
        default = recipe(model)
        for tile in aliases(model) or source_tiles(model):
            if default:
                bindings.setdefault(canonical(tile), default)
        explicit_default = model.get('default_tile_binding')
        if explicit_default:
            # Keep the default selector's declared variant, never first by luck.
            for variant in model.get('variants', []):
                if str(variant.get('variant')) == str(explicit_default.get('variant')):
                    bindings[canonical(explicit_default['native_tile'])] = recipe(variant)
        if not bindings and not mask_bindings:
            omissions.append(ident)
        scenery[blueprint] = dict(entry=ident, tiles=bindings, masks=mask_bindings,
                                 connected=blueprint in ['BrinestalkWall', 'BrinestalkWallWithGearbox'],
                                 conditional=model.get('conditional_blueprint'))

    dirty = read(package['scenery']['SCOPE-DIRTY'])
    paint = {}
    for alias in dirty['all_native_aliases']:
        node = read(alias['shared_model']) if 'shared_model' in alias else next(x for x in dirty['new_states'] if x['id'] == alias['new_state'])
        paint[canonical(alias['native_tile'])] = recipe(node)
    floor = read(read(package['scenery']['SCN-DIRTFLOOR'])['material_model'])
    path = read(package['scenery']['SCN-DIRTPATH'])
    pond = read(package['scenery']['SCN-POND'])
    surfaces = dict(soil=dict(file=image(floor['neutral_material'], size=(1024,1024)), aliases=[canonical(x) for x in floor['source_tile_aliases']]),
                    path=dict(file=image(path['neutral_material'], size=(1024,1024)), aliases=[canonical(x) for x in path['native_tile_selectors']] if isinstance(path['native_tile_selectors'], list) else []))
    for name, ref in pond['materials'].items():
        model = read(ref)
        surfaces[name] = dict(base=image(model['layers'][0], size=(1024,1024)), ripple=image(model['layers'][1], size=(1024,1024)))
    boundaries = {str(x['mask']): image(x, mask=True, size=(64,64)) for x in path['coverage']['masks']}
    Image.new('RGBA',(1,1),'white').save(out/'white.png')
    data = dict(schema=1, actors=actors, scenery=scenery, paint=paint, surfaces=surfaces, boundaries=boundaries,
                cast_sha256=hashlib.sha256((selected/'cast-v2.json').read_bytes()).hexdigest(),
                package_sha256=hashlib.sha256((selected/'package.json').read_bytes()).hexdigest(),
                unmapped=omissions, native_acceptance=False)
    (out/'contract.json').write_text(json.dumps(data, separators=(',', ':'))+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(dict(actor_rules=len(actors), scenery_rules=len(scenery), tile_bindings=sum(len(x['tiles']) for x in scenery.values()), exported_images=len(exports), unmapped=omissions)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True, type=Path)
    build(parser.parse_args().root)
