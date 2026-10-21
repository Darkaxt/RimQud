"""Author a compact nonplanar ram curl; retain v7 as rejected evidence."""
from pathlib import Path
import json

here=Path(__file__).resolve().parent
source=(here.parent/'v7/construct.py').read_text(encoding='utf-8-sig')
source=source.replace('from scipy.ndimage import binary_erosion','from scipy.ndimage import binary_erosion\nfrom scipy.interpolate import CubicSpline, PchipInterpolator')
start=source.index('segments=np.array(')
end=source.index('verts=[];',start)
source=source[:start]+'''# X lateral, Y downward, Z forward. Compact ram-like coil around the
# lateral skull, with an outward-growing axis rather than one yawed flat spiral.
# Coordinates and thickness are authored, not inferred native joint coordinates.
control=np.array([[45,151,45],[68,126,53],[87,100,48],[105,82,5],
 [115,105,-55],[118,163,-70],[122,210,-25],[124,197,25],
 [118,166,35],[116,160,25]],float)
length=np.r_[0,np.cumsum(np.linalg.norm(np.diff(control,axis=0),axis=1))]
samples=np.linspace(0,length[-1],240)
centers=CubicSpline(length,control,axis=0)(samples)
arcs=np.r_[0,np.cumsum(np.linalg.norm(np.diff(centers,axis=0),axis=1))]
fraction=arcs/arcs[-1]
radius=PchipInterpolator(length,[17,17,18,18,17,15,13,10,5,.05])(samples)
''' +source[end:]
source=source.replace("lateral_splay=.82", "control_points=control.tolist(),radius_at_control=[17,17,18,18,17,15,13,10,5,.05]")
source=source.replace("root='Each tube starts INSIDE the skull proxy at X+/-32,Y165,Z32, broad radius17. It rises through a curved anterolateral crown emergence region; its hidden starting cross-section is never a flat cap resting on the forehead.'", "root='Full roots start inside the skull at X+/-45,Y151,Z45, radius17. Initial stem grows upward/outward through the anterior-lateral crown; original head occludes the buried portion. Actual visual emergence must be reviewed, not assumed from proxy depth.'")
source=source.replace("curl='Same original side sweep rises/backwards, then returns forward into a continuous tapered tip. Lateral splay0.82 supplies clearance outside the actual projected skull for the returning loop. No independently drawn rear peg.'", "curl='Compact thick ram curl: rise outward from crown, sweep backward then downward around lateral skull, return forward and upward to a short tapered point. X, Y and Z vary independently. Posterior broad sweep can hide the anterior short return in north; south shows that return in front of the back sweep. No threadlike second spiral.'")
source=source.replace("south='Front upper crown root interiors lie behind original skull; only the emerging tapered volume is visible. Returning curls are complete outside the head. Flesh ears are unchanged and separate.'", "south='Anterior emerging roots visible at upper lateral crown; short forward return crosses in front of posterior descending sweep. Coil stays mainly beside the skull. Original flesh ears remain separate.'")
source=source.replace("east='Anterior root rises above/forward of flesh ear, sweeps backwards to screen-left and returns forward. Far horn overlaps exactly. Root begins below the visible emergence, with no open flat cut.'", "east='Full compact loop rises from anterior upper crown, sweeps screen-left/back, drops around lateral skull then turns forward/up into a short point above the ear. Far horn may be hidden. Buried root has no exposed cap.'")
source=source.replace("north='Anterior bases are hidden by original skull. Posterior horn surfaces and full returning loop clear the skull, so the thin return is not clipped into a peg and disconnected broad bend. Depth/self-occlusion come from the same volume.'", "north='Anterior root interiors are behind skull. Posterior broad descending sweep is nearest and hides the overlapping forward return; no copied frontal tip laid over the back sweep. Visible root exit must join crown without a floating end.'")
source=source.replace("correction='Embed starting cross sections; reconstruct one round volume with non-root clearance instead of hiding a cut rear spiral.'", "correction='Reject v7 planar mirrored curl and excessive tube-to-thread taper. Reconstruct compact nonplanar ram curl with physical anterior return/posterior sweep occlusion; retain full source and fixed head.'")
source=source.replace("intermediate_clearance_correction=ref(HERE.parent/'v6/clearance-correction-plan.json'),", "intermediate_clearance_correction=ref(HERE.parent/'v6/clearance-correction-plan.json'),\n rejected_v7=ref(HERE.parent/'v7/independent-review-decision.json'),")
source=source.replace("EMBEDDED ROOTS / one continuous tapered volume with skull clearance", "COMPACT RAM CURL / anterior return and posterior sweep; manual proposal")
source=source.replace("far[:,:,3]=fa[:,:,3]-near[:,:,3]", "an=near[:,:,3].astype(float); af=fa[:,:,3].astype(float);far[:,:,3]=np.uint8(np.round(np.divide(255*(af-an),255-an,out=np.zeros_like(af),where=an<255)))")
source=source.replace("Construct embedded root prefixes and one round horn volume with wider returning-loop clearance; use curved skull proxy depth rather than a constant clip plane.", "Construct compact nonplanar ram curls with substantial taper and explicit forward-return/posterior-sweep overlap. Preserve full roots and fixed body; correct alpha partition for diagnostic layering.")
(here/'construct.py').write_text(source,encoding='utf-8',newline='\n')
print('Prepared editable v8 construction; no generation or registration.')
