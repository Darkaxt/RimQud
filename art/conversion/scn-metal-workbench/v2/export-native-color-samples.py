"""Export case-distinct Qud palette samples with Windows-safe descriptive names."""
from pathlib import Path
import json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];REG=HERE/'registered';OUT=HERE/'native-color-samples';OUT.mkdir(exist_ok=True)
assert not (OUT/'samples.json').exists(),'Preserve sample provenance'
def asset(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
base=Image.open(REG/'base-primary-neutral.png').convert('RGBA');stock=Image.open(REG/'occupied-detail-neutral.png').convert('RGBA');palette=json.loads((ROOT/'evidence/joppa-anatomy-study.json').read_text())['native_palette']
def tint(im,code):
 c=bytes.fromhex(palette[code]);v=im.getchannel('R');return Image.merge('RGBA',(*[v.point(lambda n,c=c:round(n*c/255)) for c in c],im.getchannel('A')))
rows=[]
for code,label in [('C','upper-c'),('w','lower-w'),('y','lower-y'),('W','upper-w')]:
 im=tint(base,'c');im.alpha_composite(tint(stock,code));p=OUT/f'occupied-primary-c-detail-{label}.png';im.save(p);rows.append(dict(detail_code=code,detail_rgb=palette[code],asset=asset(p)))
ambiguous=REG/'occupied-native-c-w-preview.png';assert ambiguous.read_bytes()==(OUT/'occupied-primary-c-detail-upper-w.png').read_bytes()
record=dict(inputs=[asset(REG/'base-primary-neutral.png'),asset(REG/'occupied-detail-neutral.png'),asset(Path(__file__).resolve())],samples=rows,
 correction='The original registration exporter used literal palette letters in filenames. Windows treats w and W filenames as the same path, so upper W overwrote the lower w preview. The preserved old occupied-native-c-w-preview.png therefore actually contains W tint. Production neutral layers, native palette contract and main selected plate are unaffected; these four explicit case-named files are authoritative color samples.',
 preserved_ambiguous_file=dict(**asset(ambiguous),actual_detail='W',status='Historical naming collision; use explicit upper/lower sample paths'))
(OUT/'samples.json').write_bytes((json.dumps(record,indent=2,ensure_ascii=False)+'\n').encode());print('Exported C,w,y,W samples with distinct Windows-safe paths; preserved ambiguous old file explicitly identified as W.')
