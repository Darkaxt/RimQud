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
    allowed = {'.md', '.json', '.png', '.py', '.cs', '.ps1', '.html'}
    for p in files:
        rel = p.relative_to(ROOT).as_posix()
        assert p.suffix in allowed or rel in {'.gitignore', '.gitattributes', 'LICENSE'}, rel
        if p.suffix == '.json':
            json.loads(p.read_text(encoding='utf-8'))
        if p.suffix == '.py':
            ast.parse(p.read_text(encoding='utf-8'), filename=rel)
        if p.suffix != '.png':
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
        assert data.startswith(b'\x89PNG\r\n\x1a\n'), path.name
        assert hashlib.sha256(data).hexdigest() == entry['sha256'], path.name
        width, height = struct.unpack('>II', data[16:24])
        assert width > 0 and height > 0
        listed.add(path.resolve())
    assert listed == {p.resolve() for p in files if p.suffix == '.png'}
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    embedded = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', readme)
    engine = {entry['file'] for entry in manifest['images']
              if entry['kind'].startswith('Actual Qud-engine readback')}
    scenes = {'joppa-original.png', 'joppa-replacement.png'}
    assert len(embedded) == 13 and len(engine) == 11
    assert {Path(path).name for path in embedded} == engine | scenes
    archive = (ROOT / 'docs/html-visual-study.md').read_text(encoding='utf-8')
    archived = re.findall(r'!\[[^\]]*\]\(([^)]+)\)', archive)
    assert len(archived) == 4 and len(listed) == 17
    assert {Path(path).name for path in archived} == {p.name for p in listed} - engine - scenes
    result = json.loads((ROOT / 'evidence/integration-result.json').read_text(encoding='utf-8'))
    assert result['donor_shaders_loaded_and_rendered'] == 6 and result['paired_scene_frames'] == 3
    print(f'Publication checks passed: {len(files)} public files, 2 Joppa scenes and 11 material readbacks in README; 4 archived concepts; links, hashes, JSON and Python syntax valid.')


if __name__ == '__main__':
    main()
