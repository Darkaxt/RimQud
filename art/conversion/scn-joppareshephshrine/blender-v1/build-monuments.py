"""Editable source-guided shallow sculptural monuments for all native shrine tiles."""
from pathlib import Path
import bpy,bmesh,json,hashlib
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8',newline='\n')
assert not (HERE/'monuments.blend').exists();bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False);s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4;s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None';bpy.context.preferences.filepaths.save_version=0
def mat(name,role,values):
 m=bpy.data.materials.new(name);m['native_role']=role;m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.55,-.75,.35);r=n.new('ShaderNodeValToRGB');r.color_ramp.interpolation='LINEAR'
 for e,v,pos in [(r.color_ramp.elements[0],values[0],0),(r.color_ramp.elements[1],values[2],.72)]:e.position=pos;e.color=(v,)*3+(1,)
 e=r.color_ramp.elements.new(.25);e.color=(values[1],)*3+(1,);em=n.new('ShaderNodeEmission');o=n.new('ShaderNodeOutputMaterial');l.new(g.outputs['Normal'],dot.inputs[0]);l.new(dot.outputs['Value'],r.inputs[0]);l.new(r.outputs[0],em.inputs[0]);l.new(em.outputs[0],o.inputs[0]);return m
primary=mat('Neutral carved monument - native primary','primary',(.20,.46,.78));detail=mat('Neutral secondary stone/slip region - native detail','detail',(.18,.40,.65))
profiles=[
 ('catalogue',2.0,[(7,1.1),(9,1.1),(9,4),(10.3,3.9),(10.5,2.2),(11.7,2.4),(13,4),(13.8,5.3),(13.8,10.6),(13,10.6),(13,9),(11,9),(10,10.2),(10,13),(11,13.4),(11,16),(12,16.5),(12,19),(4,19),(4,16.5),(5,16),(5,13.4),(6,13),(6,10.2),(5,9),(3,9),(3,9.9),(2.2,9.9),(2.2,5.3),(3,4),(4.3,2.4),(5.5,2.2),(5.7,3.9),(7,4)]),
 ('tombstone1',2.0,[(5,3),(11,3),(12,4),(12.9,5),(12.9,19),(3.1,19),(3.1,5),(4,4)]),
 ('tombstone2',2.0,[(6.1,2.1),(7.8,2.1),(8.4,3.4),(9.2,4.4),(9.8,3.2),(10.8,3.2),(11.4,4.2),(12.8,5.6),(12.9,19),(3.1,19),(3.1,5.8),(4.4,4.2),(5.2,3.4)]),
 ('tombstone3',2.0,[(3.1,6.1),(12.9,6.1),(12.9,19),(3.1,19)]),
 ('tombstone4',2.0,[(7.1,4.1),(12.9,4.1),(12.9,19),(3.1,19),(3.1,10.1),(4.3,9.2),(5.1,6.5)]),
 ('resheph',3.0,[(7.1,1.5),(8.2,1.2),(9.8,1.8),(10.3,3),(9.4,3.5),(10,4.6),(10,5.7),(9.1,6.4),(9,8.4),(10.8,9.8),(12.3,10.7),(13.6,12.4),(13.5,13.8),(12.3,14.7),(12.7,16.7),(12.7,18.8),(13.2,19.2),(12.9,20.8),(5,20.8),(5.1,18),(5.3,15.8),(5,14.7),(3.4,14.7),(2.1,13.5),(2.1,5.3),(3.1,4.4),(3.6,5.2),(3.4,8.7),(5.1,8.7),(6.7,10),(7.1,8.3),(7.1,6.3),(6,5.5),(6.1,4.5),(7.1,3.9),(7.8,3.9),(7.2,3.2)])]
states=[];index=json.loads((HERE/'native-state-index.json').read_text())
def attach(ob,collection,root,role):
 for c in list(ob.users_collection):c.objects.unlink(ob)
 collection.objects.link(ob);ob['physical']=True;ob['native_role']=role;ob.parent=root;ob.matrix_parent_inverse=root.matrix_world.inverted();return ob
for i,(name,depth,outline) in enumerate(profiles):
 c=bpy.data.collections.new(name);s.collection.children.link(c);root=bpy.data.objects.new(name+' shared pivot',None);s.collection.objects.link(root);root.location=(8,0,0);bpy.context.view_layer.update();count=len(outline);verts=[(x,y,24-z) for y in [-depth/2,depth/2] for x,z in outline];faces=[tuple(range(count-1,-1,-1)),tuple(range(count,2*count))]+[(k,(k+1)%count,(k+1)%count+count,k+count) for k in range(count)];mesh=bpy.data.meshes.new(name+' complete closed carved profile');mesh.from_pydata(verts,[],faces);mesh.update();bm=bmesh.new();bm.from_mesh(mesh);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(mesh);bm.free();ob=bpy.data.objects.new(name+' complete relief',mesh);c.objects.link(ob);ob['physical']=True;ob['native_role']='primary';ob.parent=root;ob.matrix_parent_inverse=root.matrix_world.inverted();mesh.materials.append(primary)
 if i>0:
  base_y=22 if name=='resheph' else 20;body_y=20.8 if name=='resheph' else 19
  for part,xwidth,ydepth,low,high,role,ycenter in [('broad plinth',14,depth+1.4,base_y,base_y+1,'detail',0),('rear seating key',4.8,depth*.65,body_y-.3,base_y+.25,'detail',depth*.28)]:
   bpy.ops.mesh.primitive_cube_add(size=2,location=(8,ycenter,24-(low+high)/2));piece=bpy.context.object;piece.name=name+' '+part;piece.scale=(xwidth/2,ydepth/2,(high-low)/2);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);piece.data.materials.append(detail);attach(piece,c,root,role)
 states.append(dict(id=name,native_tile=index['states'][i]['native_tile'],source_mask=index['states'][i]['private_mask'],profile_x_y_down=outline,depth=depth,root=root.name,collection=c.name,physical_objects=[o.name for o in c.objects],authored_interpretation='Source-guided shallow carved monument. Interior negative strokes will become incisions on solid stone rather than literal holes. Hidden depth and rear seating key are authored.' if name!='resheph' else 'Abstract source-shaped sculptural relief, not a claimed anatomical portrait or gospel scene. Source head/highlight gaps are completed as continuous stone; left upright and lower secondary-colored mass remain distinct. Hidden depth and rear seating key are authored.'))
def camera(name,loc,target,scale):
 d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
front=camera('Shared cardinal map camera',(8,-44,18),(8,0,12),24);diag=camera('Monument diagnostic',(30,-37,27),(8,0,12),25)
for st in states:
 for other in states:bpy.data.collections[other['collection']].hide_render=other!=st
 s.camera=front;s.render.filepath=str(HERE/f'{st["id"]}-manual-south.png');bpy.ops.render.render(write_still=True);s.camera=diag;s.render.filepath=str(HERE/f'{st["id"]}-manual-3d.png');bpy.ops.render.render(write_still=True)
for st in states:bpy.data.collections[st['collection']].hide_render=st['id']!='resheph'
s.camera=front;write('model-controls.json',dict(source=ref(HERE/'source-packet.json'),native_states=ref(HERE/'native-state-index.json'),states=states,camera=dict(type='ORTHO',location=[8,-44,18],target=[8,0,12],ortho_scale=24,canvas=[512,768]),registration=dict(source_cell=[16,24],authored_anchor=[8,16],recipient=[256,256]),physical_translation='Complete connected monuments replace symbolic interior gaps with surface carving. Source ground bars become supported plinths using rear keys; catalogue positions and state-relative heights remain in one source cell. These are authored support/volume estimates, not native dimensions.',new_imagegen_call=False,native_activation=False));bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'monuments.blend'));write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'monuments.blend'),controls=ref(HERE/'model-controls.json'),actual_manual_renders=12,native_activation=False))
