"""Record actual contextual turnaround inspection before source selection."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
for state,ident in [('unhung','164ee549-16d8-4c09-984f-e23ea5a78e40'),('hanging','ffaa288a-9410-4d83-a9c5-448017908fd8')]:
    folder=HERE/state;p=folder/'first-structural-review.json';assert not p.exists();raw=folder/'refined-turnaround-raw.png';generated=Path('C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb')/f'exec-{ident}.png';assert raw.read_bytes()==generated.read_bytes()
    review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS FOR ROPE MATERIAL ONLY',review=('Portable loop/two strips, bound cut edges and fringes remain; end view retains folded depth.' if state=='unhung' else 'Hanging saddle retains low-left/high-right endpoints in S, reversed in N, full-width end trough and center fray.')+' Generated rope has usable intertwined-fiber surface, but placement/thickness drift, colored exterior fringe, some translucent fill across holes and warm RGB are rejected. Production must retain exact editable rope alpha, open holes, constructed crossing ink and explicit role weights; material sampling only. No new support/occupant/clothing/state or changed native mechanics. This is pre-extraction authoring inspection, not native validation.',raw_dimensions=list(Image.open(raw).size),generated_file=str(generated),inputs=[ref(folder/('constructed-turnaround-patched.png' if state=='unhung' else 'constructed-turnaround.png')),ref(folder/'turnaround-prompt.txt')],output=ref(raw))
    p.write_bytes((json.dumps(review,indent=2)+'\n').encode())
print('Recorded two actual contextual refinements, rejected matte/shape artifacts and bounded material-only selection before extraction.')
