"""Resume saved cloth model; restore source red-region weight and edge-on width."""
from pathlib import Path
import bpy,json,hashlib,math,importlib.util
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE.parent/'blender-v3';OUT.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('canvas_helpers',HERE.parent/'blender-v1/build-canvas.py');helpers=importlib.util.module_from_spec(spec);spec.loader.exec_module(helpers)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(OUT/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'canvas.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(HERE/'canvas.blend'));s=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0;controls=json.loads((HERE/'model-controls.json').read_text());detail=bpy.data.materials['Native detail folded edge and top hem']
for ob in list(s.objects):
 if ob.type!='MESH':continue
 if 'central squared picket' in ob.name:
  for v in ob.data.vertices:v.co.x*=.118/.085
 if 'red picket cap' in ob.name:
  for v in ob.data.vertices:v.co.x*=.124/.088
 if any(f' {dir} ' in ob.name for dir in ['N','S']) and ('fabric' in ob.name or 'upper hem' in ob.name):
  for v in ob.data.vertices:v.co.x*=3
 if 'edge tie' in ob.name:
  for v in ob.data.vertices:v.co.x*=.135/.051
 if 'lower outer colored fold' in ob.name:bpy.data.objects.remove(ob,do_unlink=True)
profiles=dict(E=[(.25,.015),(.30,.075),(.35,.09),(.38,.15),(.43,.17),(.46,.235),(.62,.235),(.62,.015)],W=[(.10,.015),(.10,.10),(.20,.115),(.22,.17),(.27,.19),(.28,.27),(.33,.26),(.34,.06),(.50,.04),(.62,.015)])
for st in controls['states']:
 c=bpy.data.collections[st['collection']]
 for bit,dir,sign in [(2,'E',1),(8,'W',-1)]:
  if not st['mask']&bit:continue
  for side in [-1,1]:
   verts=[]
   for t,z in profiles[dir]:
    v=(z-.015)/(.38-.015);y=side*(.034/2+.0008)+.007*math.sin(2*math.pi*t)*math.sin(math.pi*v)**2;zz=z-.008*math.sin(math.pi*t)**2;verts.append((sign*t,y,zz))
   points=[Vector(p) for p in verts];faces=tessellate_polygon([points]);ob=helpers.mesh(f'{st["mask"]:02d} {dir} source-weighted folded region {side}',verts,[tuple(t) for t in faces],c,[detail],physical=False);ob['exclude_outline']=True
 st['objects']=[ob.name for ob in c.objects if ob.type=='MESH']
hold=bpy.data.materials.new('Primary holdout for semantic role');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);slots=[(ob,i,slot.material) for ob in s.objects if ob.type=='MESH' for i,slot in enumerate(ob.material_slots) if slot.material and slot.material.get('native_role')=='primary'];visible=[]
for st in controls['states']:
 visible.append(dict(mask=st['mask'],objects=helpers.select_state(st)));s.camera=bpy.data.objects['Fixed cardinal map camera'];s.render.filepath=str(OUT/f'{st["mask"]:02d}-map-neutral.png');bpy.ops.render.render(write_still=True)
 for ob,i,material in slots:ob.data.materials[i]=hold
 s.render.use_freestyle=False;s.render.filepath=str(OUT/f'{st["mask"]:02d}-map-detail.png');bpy.ops.render.render(write_still=True)
 for ob,i,material in slots:ob.data.materials[i]=material
 s.render.use_freestyle=True
 if st['mask'] in [3,15]:
  s.camera=bpy.data.objects['Diagnostic cloth volume'];s.render.filepath=str(OUT/f'{st["mask"]:02d}-refined-3d.png');bpy.ops.render.render(write_still=True)
helpers.select_state(controls['states'][15]);s.camera=bpy.data.objects['Fixed cardinal map camera'];controls.update(resumed_from=ref(HERE/'canvas.blend'),actual_visible_states=visible,source_balance_correction=dict(post_width=.118,cap_width=.124,panel_thickness_NS=.12,tie_width=.135,fold_profiles_t_z=profiles,reason='Fresh review caught undersized red lower regions and narrow NS strips. Actual native E and W folds differ: E rises toward outer edge; W includes a taller inward tongue and lower outer return. These source groups replace mirrored tiny triangles, without changing joint/camera/crop geometry.'),native_activation=False)
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'canvas.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(OUT/'canvas.blend'),controls=ref(OUT/'model-controls.json'),actual_refined_renders=34,new_imagegen_call=False,native_activation=False))
