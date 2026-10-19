"""Copy verified unmodified native readbacks and update the Tam review page."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil

REPO=Path(__file__).resolve().parents[1]


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,required=True)
    args=ap.parse_args()
    evidence=json.loads((REPO/'evidence/dromad-result.json').read_text())
    frames={f['phase']:f for f in json.loads((args.root/'gameplay-frames.json').read_text())}
    mapping={'tam-original.png':'gameplay-dromad-south-original.png',
        'tam-south.png':'gameplay-dromad-south-replacement.png',
        'tam-east.png':'gameplay-dromad-east-replacement.png',
        'tam-north.png':'gameplay-dromad-north-replacement.png',
        'tam-robe-removed.png':'gameplay-dromad-robe-removed-replacement.png'}
    provenance_file=REPO/'docs/images/provenance.json'
    provenance=json.loads(provenance_file.read_text())
    for name,source in mapping.items():
        original=args.root/source;digest=hashlib.sha256(original.read_bytes()).hexdigest()
        assert evidence['native_image_sha256'][source]==digest
        shutil.copy2(original,provenance_file.parent/name)
        provenance['images']=[x for x in provenance['images'] if x['file']!=name]
        provenance['images'].append(dict(file=name,sha256=digest,
            kind='Native Qud map-camera readback; deterministic Tam sample; full frame unchanged',
            source_evidence='evidence/dromad-result.json',source_file=source))
    provenance_file.write_text(json.dumps(provenance,indent=2)+'\n',encoding='utf-8')
    page=REPO/'art/dromad/rebuilt/preview.html';text=page.read_text()
    text=re.sub(r'<p id="native-status">.*?</p>',
        '<p id="native-status">Verified in actual Qud: directional layers, native equip/unequip, palette, visibility, hurt, look and save/load. Full frames are unchanged; magnified windows only adjust the browser view.</p>',text)
    for name,phase in [('tam-east.png','dromad-east'),('tam-north.png','dromad-north'),('tam-robe-removed.png','dromad-robe-removed')]:
        c=next(c for c in frames[phase]['cells'] if c['source']=='Tam')
        src='../../../docs/images/'+name
        replacement=f'<svg role="img" aria-label="Magnified native Tam" viewBox="{c["screenX"]-35} {800-c["screenY"]-50} 70 70"><image href="{src}" width="1280" height="800"/></svg><a href="{src}">Full frame</a>'
        text=re.sub(r'<img src="'+re.escape(src)+r'"[^>]*>',replacement,text)
    page.write_text(text,encoding='utf-8')
    manifest_file=REPO/'art/manifest.json';manifest=json.loads(manifest_file.read_text())
    for row in manifest['images']:
        if '/dromad/rebuilt/' in row['file']:
            row['state']='Integrated in native Qud; bounded Tam sample verified'
    manifest.setdefault('review',{})['Tam']=dict(native_verified=True,
        geometry='Explicit editable SVG paths',equipment='Actual equipped Cloth Robe and Shillelagh',
        clothing_correction='East is a side profile with one visible sleeve, covered hump and front seam on the chest; north omits the front opening.',
        evidence='evidence/dromad-result.json')
    manifest_file.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print('Verified native Tam readbacks copied unchanged; provenance, manifest and inspection page updated.')


if __name__=='__main__':main()
