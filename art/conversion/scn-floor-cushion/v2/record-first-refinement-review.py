"""Record actual four contextual refinements before material extraction."""
from pathlib import Path
import hashlib,json
from datetime import datetime,timezone
from PIL import Image
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
ids=['5b417643-65ec-491b-bd33-857d3a04c430','d3adedf7-bb76-4883-872f-1f9b7db42fbd','544eac34-bad0-4249-9995-1430619b1a93','3cf81873-e77a-43a8-9367-3d683f4b2954']
reviews=[]
for n,ident in enumerate(ids,1):
    folder=HERE/f'variant-{n}';p=folder/'first-structural-review.json';assert not p.exists()
    raw=folder/'refined-turnaround-raw.png';generated=Path('C:/Users/darka/.codex/generated_images/01a15150-6512-7ae1-9634-400d4b94d6cb')/f'exec-{ident}.png';assert raw.read_bytes()==generated.read_bytes()
    patterns=['Three tufts, central star-fold rotates to opposite edge on N.','Four diamond-arranged tufts retained across the three broad views.','No top buttons added; edge folds rotate S lower edge to E left edge to N upper edge.','Three diagonal tufts retained, diagonal reverses screen slope in E.'][n-1]
    review=dict(timestamp=datetime.now(timezone.utc).isoformat(),status='PASS FOR MATERIAL SELECTION',pattern=n,review=patterns+' Continuous stuffed fabric and lower cyan role remain intact, no face, holes, occupant or loose/glowing feathers. Broad cardinal pad preserved. Generated panel/frame placement, tuft/outline width and exterior antialias fringe drift from manual input: retain exact manual geometry/ink/owner and map only interior cloth material by explicit crown/binding/side landmarks. No second isolation. This is generation-time art inspection, not native validation.',generated_file=str(generated),raw_dimensions=list(Image.open(raw).size),inputs=[ref(folder/'constructed-turnaround.png'),ref(folder/'turnaround-prompt.txt')],output=ref(raw),native_acceptance='Pending full-set generation gate')
    p.write_bytes((json.dumps(review,indent=2)+'\n').encode());reviews.append(ref(p))
(HERE/'first-refinement-reviews.json').write_bytes((json.dumps(dict(reviews=reviews,new_imagegen_calls=4,inspected_before_extraction=True),indent=2)+'\n').encode())
print('Recorded four inspected contextual refinements and exact original generated-file hashes before extraction.')
