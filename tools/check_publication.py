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
    allowed = {'.md', '.json', '.png', '.jpg', '.py', '.cs', '.ps1', '.html'}
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        assert p.suffix in allowed or rel in {'.gitignore', '.gitattributes', 'LICENSE'}, rel
        if p.suffix == '.json':
            json.loads(p.read_text(encoding='utf-8'))
        if p.suffix == '.py':
            ast.parse(p.read_text(encoding='utf-8'), filename=rel)
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
    assert listed == {p.resolve() for p in files if p.suffix in {'.png', '.jpg'}}
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
    assert len(embedded) == 33 and len(engine) == 11
    assert {Path(path).name for path in embedded} == engine | scenes
    archive = (ROOT / 'docs/html-visual-study.md').read_text(encoding='utf-8')
    archived = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', archive)
    assert len(archived) == 4 and len(listed) == 37
    assert {Path(path).name for path in archived} == {p.name for p in listed} - engine - scenes
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
    print(f'Publication checks passed: {len(files)} public files; 22 Joppa views, 11 material readbacks and 4 archived concepts; links, hashes, reviewed source identities, JSON and Python syntax valid.')


if __name__ == '__main__':
    main()
