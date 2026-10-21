"""Resume the saved complete model; refine fabric/edges and render all16 map states."""
from pathlib import Path
import bpy,json,hashlib,math,sys
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE.parent/'blender-v2';OUT.mkdir(exist_ok=True)
sys.path.insert(0,str(HERE));from importlib.util import spec_from_file_location,module_from_spec
spec=spec_from_file_location('canvas_helpers',HERE/'build-canvas.py');helpers=module_from_spec(spec);spec.loader.exec_module(helpers)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(OUT/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'canvas.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(HERE/'canvas.blend'));bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;controls=json.loads((HERE/'model-controls.json').read_text());outline=bpy.data.collections.new('Physical contours');s.collection.children.link(outline)
cloth=helpers.mat('Subdued square duck weave - native primary','primary',(.38,.78));n=cloth.node_tree.nodes;l=cloth.node_tree.links;geo=next(x for x in n if x.bl_idname=='ShaderNodeNewGeometry');em=next(x for x in n if x.bl_idname=='ShaderNodeEmission');ramp=next(x for x in n if x.bl_idname=='ShaderNodeValToRGB');waves=[]
for axis in ['X','Z']:
 w=n.new('ShaderNodeTexWave');w.wave_type='BANDS';w.bands_direction=axis;w.inputs['Scale'].default_value=40;w.inputs['Distortion'].default_value=0;l.new(geo.outputs['Position'],w.inputs['Vector']);waves.append(w)
mix=n.new('ShaderNodeMath');mix.operation='MULTIPLY';l.new(waves[0].outputs['Fac'],mix.inputs[0]);l.new(waves[1].outputs['Fac'],mix.inputs[1]);color=n.new('ShaderNodeMixRGB');color.blend_type='MULTIPLY';color.inputs[0].default_value=.055;l.new(ramp.outputs[0],color.inputs[1]);l.new(mix.outputs[0],color.inputs[2]);l.new(color.outputs[0],em.inputs[0])
for ob in list(s.objects):
 if ob.type!='MESH':continue
 if 'complete thick fabric' in ob.name:
  ob.data.materials[0]=cloth
  for face in ob.data.polygons:face.use_smooth=True
 if ob.get('physical'):
  outline.objects.link(ob)
  if 'picket' in ob.name:
   b=ob.modifiers.new('Small square picket bevel','BEVEL');b.width=ob.get('bevel_width',.002);b.segments=3;b.limit_method='ANGLE'
for st in controls['states']:
 for direction,point in controls['attachment_anchors'].items():
  ob=bpy.data.objects.new(f'{st["mask"]:02d} attachment {direction}',None);ob.empty_display_type='PLAIN_AXES';ob.empty_display_size=.06;ob.location=point;bpy.data.collections[st['collection']].objects.link(ob);ob['attachment_only']=True
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for old in list(fs.linesets):fs.linesets.remove(old)
ls=fs.linesets.new('Cloth and picket silhouette only');ls.select_by_collection=True;ls.collection=outline;ls.collection_negation='INCLUSIVE';ls.select_crease=False;ls.linestyle.color=(.012,)*3;ls.linestyle.thickness=1.5;ls.linestyle.caps='ROUND'
hold=bpy.data.materials.new('Primary holdout for semantic role');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0]);slots=[(ob,i,slot.material) for ob in s.objects if ob.type=='MESH' for i,slot in enumerate(ob.material_slots) if slot.material and slot.material.get('native_role')=='primary'];visible=[]
for st in controls['states']:
 visible.append(dict(mask=st['mask'],objects=helpers.select_state(st)));s.camera=bpy.data.objects['Fixed cardinal map camera'];s.render.filepath=str(OUT/f'{st["mask"]:02d}-map-neutral.png');bpy.ops.render.render(write_still=True)
 for ob,i,material in slots:ob.data.materials[i]=hold
 s.render.use_freestyle=False;s.render.filepath=str(OUT/f'{st["mask"]:02d}-map-detail.png');bpy.ops.render.render(write_still=True)
 for ob,i,material in slots:ob.data.materials[i]=material
 s.render.use_freestyle=True
 if st['mask'] in [3,15]:
  s.camera=bpy.data.objects['Diagnostic cloth volume'];s.render.filepath=str(OUT/f'{st["mask"]:02d}-refined-3d.png');bpy.ops.render.render(write_still=True)
helpers.select_state(controls['states'][15]);s.camera=bpy.data.objects['Fixed cardinal map camera'];controls.update(resumed_from=ref(HERE/'canvas.blend'),refinement='Small square picket bevel, subdued procedural square weave and physical contours; complete fabric and native-role folded regions retained.',actual_visible_states=visible,new_imagegen_call=False,selection_reason='Direct shared geometry preserves connected arms and crop continuations. Optional ImageGen would add no necessary detail and is not performed.',native_activation=False)
write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'canvas.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(OUT/'canvas.blend'),controls=ref(OUT/'model-controls.json'),actual_refined_renders=34,new_imagegen_call=False,native_activation=False));print('All16 states rendered from saved complete model with explicit per-object visibility.')
