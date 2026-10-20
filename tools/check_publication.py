"""Check the documented public file set, image provenance and local links."""
import ast
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    paths = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0')
    files = [ROOT / path for path in paths if path]
    allowed = {'.md', '.json', '.png', '.jpg', '.py', '.cs', '.ps1', '.html', '.svg', '.txt'}
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        assert p.suffix in allowed or rel in {'.gitignore', '.gitattributes', 'LICENSE'}, rel
        if p.suffix == '.json':
            json.loads(p.read_text(encoding='utf-8'))
        if p.suffix == '.py':
            ast.parse(p.read_text(encoding='utf-8'), filename=rel)
        if p.suffix == '.svg':
            import xml.etree.ElementTree as ET
            assert ET.fromstring(p.read_text(encoding='utf-8')).tag.endswith('svg'), rel
        if p.suffix not in {'.png', '.jpg'}:
            data = p.read_text(encoding='utf-8')
            assert not re.search(r'C:[/\\]Users[/\\]|(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]{15,}', data, re.I), rel
        if p.suffix == '.md':
            for link in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', p.read_text(encoding='utf-8')):
                if '://' not in link and not link.startswith('#'):
                    target = (p.parent / link.split('#')[0]).resolve()
                    assert target.is_relative_to(ROOT) and target.exists(), (rel, link)
    manifest = json.loads((ROOT / 'docs/images/provenance.json').read_text(encoding='utf-8'))
    listed = set()
    for entry in manifest['images']:
        path = ROOT / 'docs/images' / entry['file']
        data = path.read_bytes()
        assert data.startswith(b'\xff\xd8\xff') if path.suffix == '.jpg' else data.startswith(b'\x89PNG\r\n\x1a\n'), path.name
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], path.name
        if path.suffix == '.png':
            width, height = struct.unpack('>II', data[16:24])
            assert width > 0 and height > 0
        listed.add(path.resolve())
    art = json.loads((ROOT / 'art/manifest.json').read_text(encoding='utf-8'))
    art_paths = set()
    for entry in art['images']:
        path = ROOT / entry['file']
        assert path.is_relative_to(ROOT / 'art') and path.suffix == '.png'
        data = path.read_bytes()
        assert hashlib.sha256(data).hexdigest() == entry['sha256']
        assert list(struct.unpack('>II', data[16:24])) == entry['size']
        if entry.get('source_svg'):
            assert hashlib.sha256((ROOT/entry['source_svg']).read_bytes()).hexdigest() == entry['source_sha256']
        art_paths.add(path.resolve())
    directions = {entry['direction'] for entry in art['images']}
    assert {'south', 'east', 'north'} <= directions <= {'south', 'east', 'north', 'three-view'}
    assert listed | art_paths == {p.resolve() for p in files if p.suffix in {'.png', '.jpg'}}
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    embedded = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', readme)
    engine = {entry['file'] for entry in manifest['images']
              if entry['kind'].startswith('Actual Qud-engine readback')}
    scenes = {'joppa-original.png', 'joppa-replacement.png',
              'joppa-gameplay-original.png', 'joppa-gameplay-replacement.png',
              'joppa-pawns-original.png', 'joppa-pawns-replacement.png',
              'joppa-foreground-hud.jpg', 'joppa-foreground-menu.jpg'}
    scenes |= {'joppa-hurt-'+actor+'-'+sample+'.png' for actor in ['human', 'animal'] for sample in ['start', 'mid', 'end']}
    scenes |= {prefix+'-'+side+'.png' for prefix in ['joppa-coverage', 'joppa-coverage-gameplay'] for side in ['original', 'replacement']}
    scenes |= {'joppa-apparel-'+side+'.png' for side in ['original','replacement','swapped','hurt']}
    scenes |= {'joppa-raycat-original.png','joppa-raycat-south.png'}
    native_gallery = {'joppa-raycat-east.png','joppa-raycat-north.png',
                      'tam-original.png','tam-south.png','tam-east.png','tam-north.png','tam-robe-removed.png'}
    native_gallery |= {'tam-refined-'+name+'.png' for name in ['original','south','east','north','robe-removed']}
    scenes |= {'tam-refined-original.png','tam-refined-south.png'}
    scenes |= {'village-original.png','village-replacement.png'}
    native_gallery |= {'village-east.png','village-north.png','village-garments-removed.png','village-deep-water.png'}
    assert len(embedded) == 40 and len(engine) == 11
    assert {Path(path).name for path in embedded} == engine | scenes | {'front-derived-refined.png'}
    archive = (ROOT / 'docs/html-visual-study.md').read_text(encoding='utf-8')
    archived = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', archive)
    assert len(archived) == 4 and len(listed) == 57
    assert {Path(path).name for path in archived} == {p.name for p in listed} - engine - scenes - native_gallery
    result = json.loads((ROOT / 'evidence/integration-result.json').read_text(encoding='utf-8'))
    assert result['donor_shaders_loaded_and_rendered'] == 6 and result['paired_scene_frames'] == 3
    review = json.loads((ROOT / 'evidence/foreground-review.json').read_text())
    assert review['mouse_walking'] and review['native_menu_by_mouse'] and review['native_save_and_quit']
    for name, digest in review['source_sha256'].items():
        revision = review.get('source_revision')
        source = subprocess.check_output(['git', 'show', revision + ':probe/' + name], cwd=ROOT) if revision else (ROOT / 'probe' / name).read_bytes()
        assert hashlib.sha256(source).hexdigest() == digest, name
    pawn = json.loads((ROOT / 'evidence/pawns-stage1-result.json').read_text())
    assert pawn['stage'] == 1 and all(pawn['pawn_scene'][k] for k in ['layered_human', 'directional_animal', 'native_npc_targeting'])
    for name, digest in pawn['source_sha256'].items():
        revision = pawn.get('source_revision')
        source = subprocess.check_output(['git', 'show', revision + ':probe/' + name], cwd=ROOT) if revision else (ROOT / 'probe' / name).read_bytes()
        assert hashlib.sha256(source).hexdigest() == digest, name
    reaction = json.loads((ROOT / 'evidence/pawns-stage2-result.json').read_text())
    assert reaction['stage'] == 2 and reaction['pawn_scene']['native_movement_facing']
    for actor in ['human', 'animal']:
        state = reaction['pawn_scene']['native_reactions'][actor]
        assert state['actual_hp_loss'] == 1 and state['no_game_tick_advance'] and state['finite_flash']
    for name, digest in reaction['source_sha256'].items():
        revision = reaction.get('source_revision')
        source = subprocess.check_output(['git', 'show', revision + ':probe/' + name], cwd=ROOT) if revision else (ROOT / 'probe' / name).read_bytes()
        assert hashlib.sha256(source).hexdigest() == digest, name
    coverage = json.loads((ROOT / 'evidence/joppa-stage3-result.json').read_text())
    assert coverage['stage'] == 3 and coverage['authored']['coverage']['temporary_replacement_types'] == 26
    assert coverage['authored']['coverage']['native_fallback_types'] == 41
    revision = coverage.get('source_revision')
    for name, digest in coverage['source_sha256'].items():
        source = subprocess.check_output(['git', 'show', revision + ':probe/' + name], cwd=ROOT) if revision else (ROOT / 'probe' / name).read_bytes()
        assert hashlib.sha256(source).hexdigest() == digest, name
    contract = subprocess.check_output(['git', 'show', revision + ':probe/joppa-coverage.json'], cwd=ROOT) if revision else (ROOT/'probe/joppa-coverage.json').read_bytes()
    assert hashlib.sha256(contract.replace(b'\r\n', b'\n')).hexdigest() == coverage['mapping_contract_sha256']
    apparel = json.loads((ROOT / 'evidence/pawns-stage4-result.json').read_text())
    assert apparel['stage'] == 4 and apparel['saves_settings_preserved']
    assert apparel['pawn_scene']['equipped_items']
    for name, digest in apparel['source_sha256'].items():
        revision = apparel.get('source_revision')
        source = subprocess.check_output(['git', 'show', revision + ':probe/' + name], cwd=ROOT) if revision else (ROOT/'probe'/name).read_bytes()
        assert hashlib.sha256(source).hexdigest() == digest, name
    cat = json.loads((ROOT/'evidence/faithful-cat-result.json').read_text(encoding='utf-8'))
    assert cat['pawn_scene']['faithful_ray_cat']['actual_mesh_contact_verified']
    assert cat['pawn_scene']['faithful_ray_cat']['native_save_load']
    for name, digest in cat['source_sha256'].items():
        revision = cat.get('source_revision')
        source = subprocess.check_output(['git','show',revision+':probe/'+name],cwd=ROOT) if revision else (ROOT/'probe'/name).read_bytes()
        assert hashlib.sha256(source).hexdigest() == digest, name
    preview = (ROOT/'art/ctesiphus/preview.html').read_text(encoding='utf-8')
    assert all(name in preview for name in ['joppa-raycat-east.png','joppa-raycat-north.png'])
    dromad = json.loads((ROOT/'evidence/dromad-result.json').read_text(encoding='utf-8'))
    assert dromad['native_equip_unequip'] and dromad['native_save_load'] and dromad['saves_settings_preserved']
    assert hashlib.sha256((ROOT/'art/dromad/rebuilt/model.json').read_bytes()).hexdigest() == dromad['model_sha256']
    for name,digest in dromad['source_sha256'].items():
        revision=dromad.get('source_revision')
        source=subprocess.check_output(['git','show',revision+':probe/'+name],cwd=ROOT) if revision else (ROOT/'probe'/name).read_bytes()
        assert hashlib.sha256(source).hexdigest() == digest, name
    refined=json.loads((ROOT/'evidence/dromad-refined-result.json').read_text(encoding='utf-8'))
    assert all(refined[k] for k in ['native_equip_unequip','native_four_way_facing','native_save_load','saves_settings_preserved'])
    assert hashlib.sha256((ROOT/refined['model_file']).read_bytes()).hexdigest()==refined['model_sha256']
    for name,digest in refined['source_sha256'].items():
        revision=refined.get('source_revision')
        source=subprocess.check_output(['git','show',revision+':probe/'+name],cwd=ROOT) if revision else (ROOT/'probe'/name).read_bytes()
        assert hashlib.sha256(source).hexdigest()==digest,name
    for entry in manifest['images']:
        if entry.get('source_evidence')=='evidence/dromad-refined-result.json':
            assert entry['sha256']==refined['native_image_sha256'][entry['source_file']]
    selected = json.loads((ROOT/'art/dromad/nude/refinement.json').read_text(encoding='utf-8'))
    assert selected['selected_by_user'] and selected['user_clothed_image_used'] is False
    assert selected['source_masks_registered_to_refinement'] is False
    assert selected['refined_masks_registered'] and selected['native_integration']
    assert hashlib.sha256((ROOT/'art/dromad/nude'/selected['selected_output']).read_bytes()).hexdigest() == selected['selected_output_sha256']
    village=json.loads((ROOT/'evidence/village-result.json').read_text(encoding='utf-8'))
    assert village['resident_count']==16 and len(village['actor_blueprints'])==10 and village['selected_scenery_types']==57
    assert all(village[k] for k in ['native_equipment_removal_restore','native_save_load','native_shallow_deep_water','saves_settings_preserved'])
    assert hashlib.sha256((ROOT/village['model_file']).read_bytes()).hexdigest()==village['model_sha256']
    for name,digest in village['source_sha256'].items():
        assert hashlib.sha256((ROOT/'probe'/name).read_bytes()).hexdigest()==digest,name
    for entry in manifest['images']:
        if entry.get('source_evidence')=='evidence/village-result.json':assert entry['sha256']==village['native_image_sha256'][entry['source_file']]
    from enumerate_conversion_ledger import enumerate_entries,validate,markdown
    ledger=json.loads((ROOT/'evidence/conversion-ledger.json').read_text(encoding='utf-8'))
    validate(ledger,enumerate_entries())
    assert (ROOT/'docs/conversion-ledger.md').read_text(encoding='utf-8')==markdown(ledger)
    print(f'Publication checks passed: {len(files)} public files; {len(listed)} contextual images and {len(art_paths)} artwork/mask assets; links, hashes, evidence source identities, JSON, SVG and Python syntax valid.')


if __name__ == '__main__':
    main()
