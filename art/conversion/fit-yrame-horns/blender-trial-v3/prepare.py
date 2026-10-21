"""Correct the visible root axis and try simple Blender-native flat shading."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.interpolate import CubicSpline,PchipInterpolator
from datetime import datetime,timezone

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-trial-v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
# The previous root bent backward at its most anterior point while still over
# the forehead. Its round projected end read as a cap despite a buried start.
# Move that turn above the crown and let a longer outward/upward stem emerge.
control=np.array([[25,157,5],[50,120,40],[75,85,60],[105,122,-60],
 [112,191,-78],[102,253,-34],[88,255,35],[86,231,65],[89,216,64]],float)
radii=[26,26,25,24,21,16,11,7,.05]
length=np.r_[0,np.cumsum(np.linalg.norm(np.diff(control,axis=0),axis=1))];samples=np.linspace(0,length[-1],128)
data=dict(recorded_at=datetime.now(timezone.utc).isoformat(),control_points=control.tolist(),radius_at_control=radii,centerline=CubicSpline(length,control,axis=0)(samples).tolist(),radius=PchipInterpolator(length,radii)(samples).tolist(),previous_review=ref(OLD/'main-review-decision.json'),source_user_reference=ref(OLD/'user-ram-reference.png'),correction='Buried root begins deeper. Anterior turn moves up above crown, leaving a continuous upward/outward emergence near upper forehead. Main lower curl and short tip controls unchanged.',native_coordinates=False)
(HERE/'volume.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
s=(OLD/'build_blender.py').read_text(encoding='utf-8-sig').replace('radius=data[\'radius\'];sides=40',"radius=data['radius'];sides=24")
start=s.index("toon=nodes.new('ShaderNodeBsdfToon')")
end=s.index('# Freestyle supplies',start)
s=s[:start]+'''# Blender-native stepped shading from actual surface normals: neutral,
# stable and simple, without image quantization or generative redraw.
geometry=nodes.new('ShaderNodeNewGeometry')
dot=nodes.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.4,-.5,.76)
shade=nodes.new('ShaderNodeValToRGB');shade.color_ramp.interpolation='CONSTANT'
shade.color_ramp.elements[0].position=.10;shade.color_ramp.elements[0].color=(.24,.24,.24,1)
shade.color_ramp.elements[1].position=.70;shade.color_ramp.elements[1].color=(.78,.78,.78,1)
shade.color_ramp.elements.new(.40).color=(.50,.50,.50,1)
links.new(geometry.outputs['Normal'],dot.inputs[0]);links.new(dot.outputs['Value'],shade.inputs[0])
mix=nodes.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.34
links.new(shade.outputs[0],mix.inputs[1]);links.new(ramp.outputs[0],mix.inputs[2])
emit=nodes.new('ShaderNodeEmission');links.new(mix.outputs[0],emit.inputs['Color']);links.new(emit.outputs[0],nodes.get('Material Output').inputs['Surface'])
''' +s[end:]
s=s.replace("outline='Blender Freestyle visible horn collection,2.6px',shading='Blender Toon BSDF'", "outline='Blender Freestyle visible horn collection,2.6px',shading='Blender normal-based three neutral tone regions, groove modulation and emission'")
s=s.replace("for face,cam in cameras.items():", "for face,cam in cameras.items():\n    if face=='west':continue  # Symmetric geometry; inspect direct S/E/N first.")
s=s.replace("Second trial: user photo guides widened anterior roots and lower returning curl. Native readiness and skill deployment withheld.", "Third manual trial: continuous upper-forehead emergence, same main curl, simple rendered tone regions. Skill is updated; current horn fit remains unapproved.")
(HERE/'build_blender.py').write_text(s,encoding='utf-8',newline='\n')
print('Prepared corrected emergence and simple Blender-native tones. Main lower curl unchanged.')
