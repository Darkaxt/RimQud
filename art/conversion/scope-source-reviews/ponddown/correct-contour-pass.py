"""Keep corrected thin decal geometry; remove physical-object contours leaking across shallow layers."""
from pathlib import Path
import bpy,json,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE/'blender-v3';OUT=HERE/'blender-v4';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'cleft.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'cleft.blend'));bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;controls=json.loads((OLD/'model-controls.json').read_text());s.render.use_freestyle=False;s.camera=bpy.data.objects['Fixed map camera'];s.render.filepath=str(OUT/'refined-map-neutral.png');bpy.ops.render.render(write_still=True)
hold=bpy.data.materials.new('Primary holdout for detail ownership');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);slots=[(ob,i,slot.material) for ob in s.objects if ob.type=='MESH' for i,slot in enumerate(ob.material_slots) if slot.material and slot.material.get('native_role')=='primary']
for ob,i,m in slots:ob.data.materials[i]=hold
s.render.filepath=str(OUT/'refined-map-detail.png');bpy.ops.render.render(write_still=True)
for ob,i,m in slots:ob.data.materials[i]=m
s.camera=bpy.data.objects['Cleft diagnostic'];s.render.filepath=str(OUT/'refined-3d.png');bpy.ops.render.render(write_still=True);s.camera=bpy.data.objects['Fixed map camera'];controls.update(resumed_from=ref(OLD/'cleft.blend'),contour_correction='Same continuous caps, source outline, bevels, role materials and camera. Freestyle physical-object silhouette pass disabled for this thin layered map decal; evaluate whether remaining diagnostic cross-face hairline vanishes. Native primary/detail contrast supplies the cleft edge, without an extra drawn overlay contour.',native_activation=False);write(OUT/'model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cleft.blend'));write(OUT/'blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(OUT/'cleft.blend'),actual_correction_renders=3,geometry_changed=False,native_activation=False))
