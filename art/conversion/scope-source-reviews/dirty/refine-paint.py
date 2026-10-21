"""Resume the successfully saved manual model after the iteration diagnostic failure."""
from pathlib import Path
import bpy,json,math,hashlib
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE/'blender-v1';OUT=HERE/'blender-v2';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (OUT/'paint.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'paint.blend'));s=bpy.context.scene;bpy.context.preferences.filepaths.save_version=0;controls=json.loads((OLD/'model-controls.json').read_text());paths=controls['grass_paths_source_xy'];primary=bpy.data.materials['Neutral paint primary'];cols={name:bpy.data.collections[name] for name in ['dirt1','legacy-grass1']}
light=primary.copy();light.name='Neutral primary vein';next(n for n in light.node_tree.nodes if n.bl_idname=='ShaderNodeEmission').inputs[0].default_value=(.80,.80,.80,1)
def curve(p,t):return tuple((1-t)**3*p[0][k]+3*(1-t)**2*t*p[1][k]+3*(1-t)*t*t*p[2][k]+t**3*p[3][k] for k in range(2))
for ob in list(s.objects):
 if ob.type!='MESH':continue
 if 'blade' in ob.name:
  p=paths[int(ob.name[-1])-1];verts=[]
  for i in range(1,31):
   t=i/32;x,y=curve(p,t);a=curve(p,t-.001);b=curve(p,t+.001);dx,dy=b[0]-a[0],b[1]-a[1];norm=math.hypot(dx,dy);w=.055*math.sqrt(1-t);verts.extend([(x-dy/norm*w,24-y-dx/norm*w,.002),(x+dy/norm*w,24-y+dx/norm*w,.002)])
  me=bpy.data.meshes.new(ob.name+' center shading');me.from_pydata(verts,[],[(2*i,2*i+1,2*i+3,2*i+2) for i in range(29)]);me.update();vein=bpy.data.objects.new(ob.name+' subtle center shading',me);cols['legacy-grass1'].objects.link(vein);me.materials.append(light);vein['map_plane']=True
 else:
  m=primary.copy();m.name='Neutral fine-earth grain';n=m.node_tree.nodes;l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');noise=n.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=16;noise.inputs['Detail'].default_value=1;l.new(g.outputs['Position'],noise.inputs['Vector']);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].color=(.44,)*3+(1,);r.color_ramp.elements[1].color=(.72,)*3+(1,);l.new(noise.outputs['Fac'],r.inputs[0]);l.new(r.outputs[0],next(v for v in n if v.bl_idname=='ShaderNodeEmission').inputs[0]);ob.data.materials[0]=m
s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for old in list(fs.linesets):fs.linesets.remove(old)
ls=fs.linesets.new('Ground paint fine contours');ls.select_crease=False;ls.linestyle.color=(.055,)*3;ls.linestyle.thickness=.8
renders=[]
for name,c in cols.items():
 for ob in s.objects:
  if ob.type=='MESH':ob.hide_render=ob.name not in c.objects
 s.render.filepath=str(OUT/f'{name}-refined.png');bpy.ops.render.render(write_still=True);renders.append(ref(Path(s.render.filepath)))
controls.update(resumed_manual_model=ref(OLD/'paint.blend'),states=[dict(id=name,objects=[o.name for o in c.objects]) for name,c in cols.items()],refinement='Subtle primary blade center shading and fine rendered contours; the single dirt fleck gains restrained fine-earth grain.',diagnostic_recovery='Initial script iterated mutable scene objects while adding veins, visited an added vein name and failed before a refined save/render. Resume the intact saved manual .blend; iterate a frozen object list. No restart or rejected artwork claimed.',new_imagegen_call=False,selection_reason='Sparse fixed-cell art is preserved by direct Blender map-plane geometry/materials; no optional ImageGen call needed.',native_activation=False)
write(OUT/'model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'paint.blend'));write(OUT/'blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(OUT/'paint.blend'),refined_renders=renders,native_activation=False))
