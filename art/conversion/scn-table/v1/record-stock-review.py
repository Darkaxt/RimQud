"""Save actual inspected contextual output before any stock material extraction."""
from pathlib import Path
from datetime import datetime,timezone
import argparse,json,hashlib,shutil
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
ap=argparse.ArgumentParser();ap.add_argument('--state',type=int,required=True,choices=range(1,5));ap.add_argument('--file',type=Path,required=True);ap.add_argument('--review',required=True);a=ap.parse_args();state=f'occupied-{a.state}';out=HERE/f'{state}-first-structural-review.json';assert not out.exists();shutil.copyfile(a.file,HERE/f'refined-{state}-raw.png');d=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS FOR STOCK MATERIAL',generated_file=str(a.file),raw=ref(HERE/f'refined-{state}-raw.png'),prompt_file=ref(HERE/f'{state}-normalized-prompt.txt'),review=a.review,geometry_selection='Retain every normalized selected empty base; use refined stock RGB only within exact normalized source-shaped vector alpha/ink, excluding generated repaint, shifts, cast shadows and colored fringe.',native_validation=False);out.write_bytes((json.dumps(d,indent=2)+'\n').encode());print('Saved raw and first structural review:',state)
