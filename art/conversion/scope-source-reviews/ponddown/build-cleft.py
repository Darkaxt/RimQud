"""Editable shallow map-plane cleft with source-owned dark recess and irregular lit stone lips."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
from mathutils.geometry import tessellate_polygon
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OUT=HERE/'blender-v1';OUT.mkdir(exist_ok=True)
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(p,v):p.write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
def mat(name,role,value):
 m=bpy.data.materials.new(name);m['native_role']=role;m.use_nodes=True;n=m.node_tree.nodes;n.clear();em=n.new('ShaderNodeEmission');em.inputs[0].default_value=(value,)*3+(1,);o=n.new('ShaderNodeOutputMaterial');m.node_tree.links.new(em.outputs[0],o.inputs[0]);return m
def loops(cells):
 edges=set()
 for x,y in cells:
  for a,b in [((x,y),(x+1,y)),((x+1,y),(x+1,y+1)),((x+1,y+1),(x,y+1)),((x,y+1),(x,y))]:
   if (b,a) in edges:edges.remove((b,a))
   else:edges.add((a,b))
 result=[]
 while edges:
  a,b=min(edges);edges.remove((a,b));poly=[a];end=b
  while end!=a:
   poly.append(end);options=sorted((u,v) for u,v in edges if u==end);assert options,(end,edges)
   # At a diagonal pixel touch retain separate consistent boundary turns.
   prev=poly[-2];dx,dy=end[0]-prev[0],end[1]-prev[1]
   options.sort(key=lambda e:-(dx*(e[1][1]-end[1])-dy*(e[1][0]-end[0])));edge=options[0];edges.remove(edge);end=edge[1]
  # Round only the pixel corners, with a small native-coordinate bevel in plan.
  rounded=[]
  for i,b in enumerate(poly):
   a=poly[i-1];c=poly[(i+1)%len(poly)];cross=(b[0]-a[0])*(c[1]-b[1])-(b[1]-a[1])*(c[0]-b[0])
   if not cross:continue
   rounded.extend([(b[0]*.82+a[0]*.18,b[1]*.82+a[1]*.18),(b[0]*.82+c[0]*.18,b[1]*.82+c[1]*.18)])
  result.append(rounded)
 return result
def solid(name,poly,z0,z1,material):
 points=[Vector((x,24-y,0)) for x,y in poly];tri=tessellate_polygon([points]);N=len(points);verts=[(p.x,p.y,z) for z in [z0,z1] for p in points];faces=[tuple(reversed(t)) for t in tri]+[tuple(i+N for i in t) for t in tri]+[(i,(i+1)%N,(i+1)%N+N,i+N) for i in range(N)];me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();ob=bpy.data.objects.new(name,me);bpy.context.scene.collection.objects.link(ob);me.materials.append(material);ob['physical']=True;ob['native_role']=material['native_role'];return ob
assert not (OUT/'cleft.blend').exists();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.context.preferences.filepaths.save_version=0;s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard';s.view_settings.look='None';source=json.loads((HERE/'source-packet.json').read_text());image=bpy.data.images.load(source['source_tile']['private_mask']['path'],check_existing=False);w,h=image.size;data=list(image.pixels);allcells=set();primarycells=set()
for y in range(h):
 for x in range(w):
  k=((h-1-y)*w+x)*4
  if data[k+3]>.5:
   allcells.add((x,y))
   if data[k]<.5:primarycells.add((x,y))
bpy.data.images.remove(image);primary=mat('Neutral lit stone lip - native primary','primary',.74);detail=mat('Neutral cleft recess - native detail','detail',.50);outlines=[]
for role,cells,z0,z1,material in [('recess',allcells,-.20,-.06,detail),('lit lips',primarycells,-.09,.015,primary)]:
 for i,poly in enumerate(loops(cells)):
  ob=solid(role+f' {i+1}',poly,z0,z1,material);outlines.append(dict(object=ob.name,role=material['native_role'],source_outline=poly,z=[z0,z1]))
camdata=bpy.data.cameras.new('Fixed map camera');camdata.type='ORTHO';camdata.ortho_scale=24;cam=bpy.data.objects.new('Fixed map camera',camdata);s.collection.objects.link(cam);cam.location=(8,12,30);cam.rotation_euler=(0,0,0);s.camera=cam;s.render.filepath=str(OUT/'manual-map.png');bpy.ops.render.render(write_still=True)
controls=dict(entry='SCOPE-PONDDOWN',source=ref(HERE/'source-packet.json'),outlines=outlines,camera=dict(location=[8,12,30],type='ORTHO',scale=24,canvas=[512,768]),registration=dict(native_cell=[16,24],canvas=[512,768],rule='Original complete rectangular map frame; no alpha recenter/fit or extra facings.'),interpretation='Source sparse cleft opening and asymmetric lit-lip topology become shallow closed3D recess/lip fragments. Small18percent corner rounding and depth are authored; native negative/background regions remain open. This is a cleft decal, not newly cut terrain/physical stairs.',native_activation=False)
write(OUT/'model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(OUT/'cleft.blend'));write(OUT/'blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(OUT/'cleft.blend'),actual_manual_renders=1,native_activation=False))
