"""Record actual per-layout composed refinements before material extraction."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
ids=['312fd8df-7d31-45e7-855f-8e705a2d5c7f','b4c1e8d3-1a7a-463d-8137-5f7464ae1cc2','7a59e833-c9ba-450a-a901-d8c6995cc4e2']
for n,ident in enumerate(ids,1):
    folder=HERE/f'variant-{n}';p=folder/'first-structural-review.json';assert not p.exists();raw=folder/'refined-turnaround-raw.png';generated=Path('C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb')/f'exec-{ident}.png';assert raw.read_bytes()==generated.read_bytes()
    counts=[[4,4,4],[4,3,3],[2,3,2]][n-1]
    record=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS FOR MATERIAL SELECTION',review=f'Source sparse counts{counts}, horizontal/upright/leaning identity, parallel cap, complete closed end and open rear retained. No donor4thlevel, contents or backing. Generated panel widths/positions, nail/edge treatment and book highlights drift, and exterior fringe is present. Retain selected patched front exactly; use generated E/N wood/book material only inside manual coverage/role/ink. Material-coordinate registration may account for unequal generated panel spacing; production geometry/scale/pivot remain constructed. Open rear and hidden depth remain authored. First structural inspection precedes extraction; no native acceptance.',raw_dimensions=list(Image.open(raw).size),generated_file=str(generated),inputs=[ref(folder/'front-guided-turnaround-patched.png'),ref(folder/'turnaround-prompt.txt')],output=ref(raw))
    p.write_bytes((json.dumps(record,indent=2)+'\n').encode())
print('Recorded all3composed refinements and actual generated file hashes before material extraction.')
