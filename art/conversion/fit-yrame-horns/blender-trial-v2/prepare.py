"""Apply the user's ram reference to the editable Blender trial, not the skill."""
from pathlib import Path
import json,hashlib
import numpy as np
from scipy.interpolate import CubicSpline,PchipInterpolator
from datetime import datetime,timezone

HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-trial-v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
photo=Path('C:/Users/darka/AppData/Local/Temp/codex-clipboard-40bda210-6189-4ff6-9e04-6716fa56a249.png')
# Preserve the user-provided visual evidence with the trial.
(HERE/'user-ram-reference.png').write_bytes(photo.read_bytes())
control=np.array([[40,157,30],[60,136,60],[82,104,25],[105,122,-60],
 [112,191,-78],[102,253,-34],[88,255,35],[86,231,65],[89,216,64]],float)
radii=[26,26,25,24,21,16,11,7,.05]
arc=np.r_[0,np.cumsum(np.linalg.norm(np.diff(control,axis=0),axis=1))];sample=np.linspace(0,arc[-1],260)
centers=CubicSpline(arc,control,axis=0)(sample);radius=PchipInterpolator(arc,radii)(sample)
data=dict(recorded_at=datetime.now(timezone.utc).isoformat(),control_points=control.tolist(),radius_at_control=radii,centerline=centers.tolist(),radius=radius.tolist(),source_user_reference=ref(HERE/'user-ram-reference.png'),interpretation='Broad upper anterior crown root; backward sweep around lateral ear region; downward then forward curl into a short upward point near lower cheek. Ram curl applied to fixed human head, not a sheep head.',native_coordinates=False,body_unchanged=True)
(HERE/'volume.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8',newline='\n')
s=(OLD/'build_blender.py').read_text(encoding='utf-8-sig').replace("VOLUME=HERE.parent/'v9/volume.json'","VOLUME=HERE/'volume.json'")
s=s.replace("bone=material('Neutral bone - material only',(.62,.62,.62))","bone=material('Neutral bone - toon render trial',(.72,.72,.72))")
s=s.replace("links.new(attr.outputs['Fac'],mult.inputs[0]);links.new(mult.outputs[0],cos.inputs[0]);links.new(cos.outputs[0],ramp.inputs[0]);links.new(ramp.outputs[0],nodes.get('Principled BSDF').inputs['Base Color'])", """links.new(attr.outputs['Fac'],mult.inputs[0]);links.new(mult.outputs[0],cos.inputs[0]);links.new(cos.outputs[0],ramp.inputs[0])
toon=nodes.new('ShaderNodeBsdfToon');toon.component='DIFFUSE';toon.inputs['Size'].default_value=.68;toon.inputs['Smooth'].default_value=.055
links.new(ramp.outputs[0],toon.inputs['Color']);links.new(toon.outputs[0],nodes.get('Material Output').inputs['Surface'])
# Freestyle supplies actual render-time contours, excluding the skull proxy.
horn_lines=bpy.data.collections.new('Horn contour selection');scene.collection.children.link(horn_lines)
scene.render.use_freestyle=True
fs=scene.view_layers[0].freestyle_settings
for ls in list(fs.linesets):fs.linesets.remove(ls)
ls=fs.linesets.new('Visible horn silhouettes');ls.select_by_collection=True;ls.collection=horn_lines;ls.collection_negation='INCLUSIVE'
ls.select_crease=False;ls.select_border=True;ls.select_silhouette=True;ls.select_contour=True;ls.select_external_contour=True
ls.linestyle.color=(.012,.012,.012);ls.linestyle.thickness=2.6;ls.linestyle.caps='ROUND'
""")
s=s.replace("obj.data.materials.append(bone)","obj.data.materials.append(bone);horn_lines.objects.link(obj)")
s=s.replace("scene['trial_scope']='Test before applying skill change; all horn generation readiness remains withheld'", "scene['trial_scope']='Second trial: user photo guides widened anterior roots and lower returning curl. Native readiness and skill deployment withheld.'")
s=s.replace("scene.camera=probe\nscene.render.resolution_x=900;scene.render.resolution_y=900\nscene.render.filepath", "scene.camera=probe\nscene.render.resolution_x=900;scene.render.resolution_y=900\nscene.render.filepath",1)
s=s.replace("for mode in ['whole-item','with-skull','visible-item']:","for mode in ['whole-item','with-skull','visible-item']:")
s=s.replace("skull.hide_render=False;skull.data.materials[0]=skullmat", "skull.hide_render=False;skull.data.materials[0]=skullmat\n# Remove unused startup brushes/materials instead of saving external brush links.\nbpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)")
s=s.replace("render_engine=scene.render.engine,samples=16", "render_engine=scene.render.engine,outline='Blender Freestyle visible horn collection,2.6px',shading='Blender Toon BSDF',samples=16")
(HERE/'build_blender.py').write_text(s,encoding='utf-8',newline='\n')
print('Prepared photo-guided wider forehead roots and lower curl, Blender Toon BSDF and Freestyle. Skill unchanged.')
