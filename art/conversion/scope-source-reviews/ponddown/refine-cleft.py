"""Resume saved cleft; restrained lip bevel/grain and native semantic role pass."""
from pathlib import Path
import bpy,json,hashlib
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE/'blender-v1';OUT=HERE/'blender-v2';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'cleft.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'cleft.blend'));bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;controls=json.loads((OLD/'model-controls.json').read_text());primary=bpy.data.materials['Neutral lit stone lip - native primary'];detail=bpy.data.materials['Neutral cleft recess - native detail']
for ob in s.objects:
 if ob.type=='MESH':
  b=ob.modifiers.new('Small weathered cleft edges','BEVEL');b.width=.025;b.segments=2;b.limit_method='ANGLE'
for m,lo,hi in [(primary,.65,.80),(detail,.30,.46)]:
 n=m.node_tree.nodes;l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=8;noise.inputs['Detail'].default_value=1;l.new(g.outputs['Position'],noise.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(lo,)*3+(1,);r.color_ramp.elements[1].color=(hi,)*3+(1,);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],next(n for n in n if n.bl_idname=='ShaderNodeEmission').inputs[0])
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for old in list(fs.linesets):fs.linesets.remove(old)
ls=fs.linesets.new('Fine stone contour');ls.select_crease=False;ls.linestyle.color=(.04,)*3;ls.linestyle.thickness=.75;s.render.filepath=str(OUT/'refined-map-neutral.png');bpy.ops.render.render(write_still=True)
hold=bpy.data.materials.new('Primary holdout for detail ownership');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);slots=[(ob,i,slot.material) for ob in s.objects if ob.type=='MESH' for i,slot in enumerate(ob.material_slots) if slot.material and slot.material.get('native_role')=='primary']
for ob,i,m in slots:ob.data.materials[i]=hold
s.render.use_freestyle=False;s.render.filepath=str(OUT/'refined-map-detail.png');bpy.ops.render.render(write_still=True)
for ob,i,m in slots:ob.data.materials[i]=m
s.render.use_freestyle=True;cam=s.camera;data=bpy.data.cameras.new('Cleft diagnostic');data.type='ORTHO';data.ortho_scale=24;ob=bpy.data.objects.new('Cleft diagnostic',data);s.collection.objects.link(ob);ob.location=(22,-10,27);ob.rotation_euler=(Vector((8,12,0))-ob.location).to_track_quat('-Z','Y').to_euler();s.camera=ob;s.render.filepath=str(OUT/'refined-3d.png');bpy.ops.render.render(write_still=True);s.camera=cam
controls.update(resumed_from=ref(OLD/'cleft.blend'),refinement='Small bevels, restrained stone grain and fine contours; retain source semantic lit lips/recess and shared cell.',new_imagegen_call=False,selection_reason='Direct map-plane cleft geometry preserves exact native footprint/role grouping; optional ImageGen would not improve needed identity.',native_activation=False);write(OUT/'model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cleft.blend'));write(OUT/'blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(OUT/'cleft.blend'),actual_refined_renders=3,native_activation=False))
