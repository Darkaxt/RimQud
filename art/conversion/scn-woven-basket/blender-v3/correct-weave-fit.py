"""Fit reed ribbons to deterministic outer-wall cross sections, without seam tunneling."""
from pathlib import Path
import bpy,json,hashlib,math
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'blender-v2'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'basket.blend').exists();bpy.ops.wm.open_mainfile(filepath=str(OLD/'basket.blend'));s=bpy.context.scene;body=bpy.data.objects['Complete woven bowl foundation'];bpy.context.view_layer.update();deps=bpy.context.evaluated_depsgraph_get();surface=bpy.data.meshes.new_from_object(body.evaluated_get(deps),depsgraph=deps);cache={}
def radius(y):
 if y in cache:return cache[y]
 z=24-y;values=[]
 for edge in surface.edges:
  a,b=(surface.vertices[k].co for k in edge.vertices)
  if min(a.z,b.z)<=z<=max(a.z,b.z):
   if abs(b.z-a.z)>1e-8:
    t=(z-a.z)/(b.z-a.z);p=a+(b-a)*t;values.append(math.sqrt(((p.x-8)/5.4)**2+(p.y/4.1)**2))
   else:values.extend(math.sqrt(((p.x-8)/5.4)**2+(p.y/4.1)**2) for p in [a,b])
 assert values,y;cache[y]=max(values);assert cache[y]>0;return cache[y]
def point(phi,y,offset):
 q=radius(y);normal=Vector((math.cos(phi)/5.4,math.sin(phi)/4.1,0)).normalized();return Vector((8+5.4*q*math.cos(phi),4.1*q*math.sin(phi),24-y))+normal*offset
for row in range(6):
 ob=bpy.data.objects[f'Complete weft course {row}'];y=14.4+.8*row
 for k in range(128):
  phi=k*2*math.pi/128;offset=.04+.045*math.cos(8*phi+row*math.pi)
  for i,edge in enumerate([-.25,.25]):ob.data.vertices[2*k+i].co=point(phi,y+edge,offset)
 ob.data.update()
for col in range(16):
 ob=bpy.data.objects[f'Bound vertical warp {col}'];phi=col*2*math.pi/16
 for k in range(65):
  y=13.9+(18.65-13.9)*k/64;offset=.04-.045*math.cos(col*math.pi+(y-14.4)*math.pi/.8)
  for i,edge in enumerate([-.055,.055]):ob.data.vertices[2*k+i].co=point(phi+edge,y,offset)
 ob.data.update()
bpy.context.view_layer.update();s.camera=bpy.data.objects['Reed vessel construction diagnostic'];s.render.filepath=str(HERE/'stage-03-refined-model-3d.png');bpy.ops.render.render(write_still=True);s.camera=bpy.data.objects['Fixed source map camera'];root=bpy.data.objects['Basket shared facing pivot']
for facing,angle in [('south',0),('east',-math.pi/2),('north',math.pi)]:root.rotation_euler.z=angle;s.render.filepath=str(HERE/f'{facing}-neutral-master.png');bpy.ops.render.render(write_still=True)
root.rotation_euler.z=0;bpy.context.view_layer.update()
controls=json.loads((OLD/'model-controls.json').read_text());controls.update(resumed_from=ref(OLD/'basket.blend'),review_trigger=ref(OLD/'independent-structural-review.json'),weave_fit_correction=dict(method='Intersect evaluated bowl mesh edges with each strand-height plane and take the outer normalized elliptical radius. No directional ray can tunnel through a mesh seam or select the far wall.',sampled_sections=len(cache),radius_range=[min(cache.values()),max(cache.values())],body_rim_handle_unchanged=True,all_ribbon_topology_preserved=True),new_imagegen_call=False,native_activation=False);controls['weave']['actual_wall_fit']='Deterministic evaluated outer-wall cross sections, alternating over/under displacement, real strand thickness.'
write('model-controls.json',controls);write('cross-section-profile.json',[dict(y_down=y,outer_radius_scale=q) for y,q in sorted(cache.items())]);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'basket.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'basket.blend'),controls=ref(HERE/'model-controls.json'),actual_views=['south','east','north'],new_imagegen_call=False,native_activation=False))
