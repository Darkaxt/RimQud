"""Editable complete cloth/pickets for all16 native neighbor states; no game operation."""
from pathlib import Path
import bpy,bmesh,json,hashlib,math
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
def camera(name,loc,target,scale):
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;ob=bpy.data.objects.new(name,d);bpy.context.scene.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
def mat(name,role,values,weave=False):
 m=bpy.data.materials.new(name);m['native_role']=role;m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links
 g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.35,-.70,.62);r=n.new('ShaderNodeValToRGB');r.color_ramp.elements[0].position=0;r.color_ramp.elements[0].color=(values[0],)*3+(1,);r.color_ramp.elements[1].position=.85;r.color_ramp.elements[1].color=(values[1],)*3+(1,);l.new(g.outputs['Normal'],dot.inputs[0]);l.new(dot.outputs['Value'],r.inputs[0]);em=n.new('ShaderNodeEmission');out=n.new('ShaderNodeOutputMaterial');l.new(r.outputs[0],em.inputs[0]);l.new(em.outputs[0],out.inputs[0])
 if weave:
  tex=n.new('ShaderNodeTexNoise');tex.inputs['Scale'].default_value=60;tex.inputs['Detail'].default_value=1;l.new(g.outputs['Position'],tex.inputs['Vector']);mix=n.new('ShaderNodeMixRGB');mix.blend_type='MULTIPLY';mix.inputs[0].default_value=.07;l.new(r.outputs[0],mix.inputs[1]);l.new(tex.outputs['Fac'],mix.inputs[2]);l.new(mix.outputs[0],em.inputs[0])
 return m
def attach(ob,c,role,physical=True):
 for old in list(ob.users_collection):old.objects.unlink(ob)
 c.objects.link(ob);ob['state_collection']=c.name;ob['native_role']=role;ob['physical']=physical;return ob
def cube(name,loc,scale,c,material):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);ob=bpy.context.object;ob.name=name;ob.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(material);return attach(ob,c,material['native_role'])
def mesh(name,verts,faces,c,mats,roles=None,physical=True):
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free();ob=bpy.data.objects.new(name,me);c.objects.link(ob);ob['state_collection']=c.name;ob['native_role']='mixed' if len(mats)>1 else mats[0]['native_role'];ob['physical']=physical
 for m in mats:me.materials.append(m)
 if roles:
  for p,role in zip(me.polygons,roles):p.material_index=role
 return ob
def make_panel(prefix,axis,sign,c,primary,detail):
 # Endcaps are outside the crop on connected edges; central post owns the joint.
 L=.62 if axis=='x' else 1.08;start=.031;H=.38;bottom=.015;th=.034 if axis=='x' else .040;NU=24;NV=8
 def position(u,v,side,offset=0):
  t=start+(L-start)*u;z=bottom+(H-bottom)*v-.008*math.sin(math.pi*t)**2;bulge=.007*math.sin(2*math.pi*t)*(math.sin(math.pi*v)**2);q=side*(th/2+offset)+bulge
  return (sign*t,q,z) if axis=='x' else (q,sign*t,z)
 vs=[position(u/NU,v/NV,side) for side in [-1,1] for v in range(NV+1) for u in range(NU+1)];stride=(NU+1)*(NV+1);fs=[];roles=[]
 for layer in range(2):
  for v in range(NV):
   for u in range(NU):
    k=layer*stride+v*(NU+1)+u;fs.append((k,k+1,k+NU+2,k+NU+1));roles.append(0)
 for u in range(NU):
  a=u;b=NV*(NU+1)+u;fs.extend([(a,a+stride,a+stride+1,a+1),(b,b+1,b+stride+1,b+stride)]);roles.extend([1,1])
 for v in range(NV):
  for u in [0,NU]:
   a=v*(NU+1)+u;b=(v+1)*(NU+1)+u;fs.append((a,b,b+stride,a+stride));roles.append(1)
 body=mesh(prefix+' complete thick fabric',vs,fs,c,[primary,detail],roles)
 # Complete hem follows shared world positions, without a per-cell end cap in frame.
 hv=[position(u/NU,v,side,.003) for side in [-1,1] for v in [.89,1.015] for u in range(NU+1)];stride2=2*(NU+1);hf=[]
 for layer in range(2):
  for u in range(NU):
   k=layer*stride2+u;hf.append((k,k+1,k+NU+2,k+NU+1))
 for u in range(NU):hf.extend([(u,u+stride2,u+stride2+1,u+1),(NU+1+u,NU+2+u,NU+2+u+stride2,NU+1+u+stride2)])
 for u in [0,NU]:hf.append((u,u+NU+1,u+NU+1+stride2,u+stride2))
 hem=mesh(prefix+' red upper hem',hv,hf,c,[detail]);hem['bevel_allowed']=False
 if axis=='x':
  for side in [-1,1]:
   # Lower outer fold ownership follows actual tent_e/w; not a hole or cutout.
   tri=[position(.56,0,side,.0005),position(1,0,side,.0005),position(1,.48,side,.0005)]
   ob=mesh(prefix+f' lower outer colored fold {side}',tri,[(0,1,2)],c,[detail],physical=False);ob['exclude_outline']=True
 return body,hem
def select_state(st):
 for ob in bpy.context.scene.objects:
  if ob.type in {'MESH','CURVE'}:ob.hide_render=ob.get('state_collection')!=st['collection']
 visible=sorted(ob.name for ob in bpy.context.scene.objects if ob.type in {'MESH','CURVE'} and not ob.hide_render)
 assert visible==sorted(st['objects']);return visible
def main():
 assert not (HERE/'canvas.blend').exists();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);bpy.context.preferences.filepaths.save_version=0
 s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.pixel_aspect_x=3/math.sqrt(2);s.render.pixel_aspect_y=1;s.render.film_transparent=True;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard';s.view_settings.look='None'
 primary=mat('Native primary cloth and picket','primary',(.35,.76));detail=mat('Native detail folded edge and top hem','detail',(.26,.63));states=[]
 for mask in range(16):
  c=bpy.data.collections.new(f'Canvas mask {mask:02d}');s.collection.children.link(c)
  post=cube(f'{mask:02d} central squared picket',(0,0,.195),(.085,.065,.39),c,primary);post['bevel_width']=.006
  cap=cube(f'{mask:02d} red picket cap',(0,0,.382),(.088,.070,.035),c,detail);cap['bevel_width']=.003
  for bit,axis,sign,dir in [(1,'y',1,'N'),(2,'x',1,'E'),(4,'y',-1,'S'),(8,'x',-1,'W')]:
   if mask&bit:make_panel(f'{mask:02d} {dir}',axis,sign,c,primary,detail)
  # Source edge-on connectors have primary crossbars; model these as small ties.
  for bit,sign in [(1,1),(4,-1)]:
   if mask&bit:
    for y in [.28,.64,.96]:cube(f'{mask:02d} edge tie {sign} {y}',(0,sign*y,.38),(.051,.024,.013),c,primary)
  states.append(dict(mask=mask,neighbors=[d for b,d in [(1,'N'),(2,'E'),(4,'S'),(8,'W')] if mask&b],collection=c.name,objects=[o.name for o in c.objects]))
 cam=camera('Fixed cardinal map camera',(0,-8,8+1/6),(0,0,1/6),1);diag=camera('Diagnostic cloth volume',(1.8,-2.8,1.7),(0,0,.19),1.75);s.camera=cam;bpy.context.view_layer.update()
 projections={label:list(world_to_camera_view(s,cam,Vector(p))) for label,p in [('anchor',(0,0,0)),('east_ground',(.5,0,0)),('west_ground',(-.5,0,0)),('north_ground',(0,.5,0)),('south_ground',(0,-.5,0)),('post_top',(0,0,.39))]}
 # Effective landscape camera yields x width1, y height sqrt(.5).
 assert abs(projections['anchor'][0]-.5)<1e-5 and abs(projections['anchor'][1]-1/3)<1e-5,projections
 assert abs(projections['east_ground'][0]-1)<1e-5 and abs(projections['north_ground'][1]-projections['anchor'][1]-.5)<1e-5,projections
 for st in states:
  select_state(st)
  if st['mask'] in [0,3,10,15]:
   s.camera=cam;s.render.filepath=str(HERE/f'{st["mask"]:02d}-manual-map.png');bpy.ops.render.render(write_still=True)
   if st['mask']==15:
    s.camera=diag;s.render.filepath=str(HERE/'manual-3d.png');bpy.ops.render.render(write_still=True)
 select_state(states[15]);s.camera=cam
 controls=dict(source=ref(HERE/'source-packet.json'),states=states,camera=dict(location=list(cam.location),rotation=list(cam.rotation_euler),ortho_scale=1,elevation_degrees=45,pixel_aspect=[3/math.sqrt(2),1],canvas=[512,768],projections=projections),registration=dict(native_cell=[16,24],anchor=[8,16],recipient=[256,256],rule='Full common cell. Only declared connected sides may reach frame; no per-state bounds fitting.'),physical_parameters=dict(post=[.085,.065,.39],panel_height=.38,panel_bottom=.015,panel_thickness_EW=.034,panel_thickness_NS=.04,end_extension_EW=.62,end_extension_NS=1.08,reason='Complete mesh continuations beyond connected crop edges avoid end-cap seams. Native tile edges are texture crop planes, not exposed physical ends.'),attachment_anchors=dict(N=[0,.5,0],E=[.5,0,0],S=[0,-.5,0],W=[-.5,0,0]),authored_estimates='Hidden physical thickness,45-degree map elevation and subtle cloth tension. Camera pixel aspect preserves square ground-cell projection through source16x24 to recipient256x256 mapping.',native_activation=False)
 write('model-controls.json',controls);bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'canvas.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'canvas.blend'),controls=ref(HERE/'model-controls.json'),actual_manual_renders=5,native_activation=False))
if __name__=='__main__':main()
