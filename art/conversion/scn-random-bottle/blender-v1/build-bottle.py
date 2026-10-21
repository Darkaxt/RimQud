"""One hollow freeblown glass vessel with a physically connected loop handle."""
from pathlib import Path
import bpy,json,math,hashlib
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
assert not (HERE/'bottle.blend').exists()
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=16;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4
s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None';bpy.context.preferences.filepaths.save_version=0
def mat(name,values):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.55,-.75,.35)
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT'
    for elem,value,pos in [(ramp.color_ramp.elements[0],values[0],0),(ramp.color_ramp.elements[1],values[2],.72)]:elem.position=pos;elem.color=(value,value,value,1)
    elem=ramp.color_ramp.elements.new(.25);elem.color=(values[1],)*3+(1,);e=n.new('ShaderNodeEmission');o=n.new('ShaderNodeOutputMaterial');l.new(g.outputs['Normal'],dot.inputs[0]);l.new(dot.outputs['Value'],ramp.inputs[0]);l.new(ramp.outputs[0],e.inputs[0]);l.new(e.outputs[0],o.inputs[0]);return m
glass=mat('Neutral stylized glass - source c',(.2,.48,.78));band=glass.copy();band.name='Native liquid-dependent lower detail region';glint=mat('Neutral glass highlight',(.85,.9,.98))
hold=bpy.data.materials.new('Body holdout for liquid-color ownership');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0])
contours=bpy.data.collections.new('Vessel contour');s.collection.children.link(contours);s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for ls in list(fs.linesets):fs.linesets.remove(ls)
ls=fs.linesets.new('Glass silhouette');ls.select_by_collection=True;ls.collection=contours;ls.collection_negation='INCLUSIVE';ls.select_crease=False;ls.linestyle.color=(.018,.018,.018);ls.linestyle.thickness=1.8;ls.linestyle.caps='ROUND'
# Radius/y-down cross-section: outer base -> outer wall -> rolled mouth ->
# inner wall -> inner base. Hidden wall/depth dimensions are authored.
outer=[(0,20),(2.2,20),(3.3,19.3),(4,17),(4,14.2),(3.2,12.8),(2,11.5),(.95,10.3),(.9,5.4),(1.7,5),(1.7,4.5),(1.35,4.3)]
inner=[(1.13,4.5),(1.30,4.85),(.70,5.4),(.73,10.3),(1.82,11.5),(3.02,12.8),(3.82,14.2),(3.82,17),(3.12,19.1),(2,19.7),(0,19.7)]
profile=outer+inner;sides=96;verts=[];faces=[]
for r,y in profile:
    for k in range(sides):
        t=k*2*math.pi/sides;verts.append((8+r*math.cos(t),r*math.sin(t),24-y))
for j in range(len(profile)-1):
    for k in range(sides):faces.append((j*sides+k,j*sides+(k+1)%sides,(j+1)*sides+(k+1)%sides,(j+1)*sides+k))
mesh=bpy.data.meshes.new('Complete hollow glass wall');mesh.from_pydata(verts,[],faces);mesh.update();body=bpy.data.objects.new('Hollow freeblown glass body',mesh);s.collection.objects.link(body);contours.objects.link(body);mesh.materials.append(glass);mesh.materials.append(band)
for poly in mesh.polygons:
    poly.use_smooth=True;j=poly.index//sides;y=(profile[j][1]+profile[j+1][1])/2;poly.material_index=1 if y>=17 else 0
def curve(name,points,radius,material,outline=True):
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.resolution_u=20;data.bevel_depth=radius;data.bevel_resolution=5;sp=data.splines.new('BEZIER');sp.bezier_points.add(len(points)-1)
    for p,q in zip(sp.bezier_points,points):p.co=q;p.handle_left_type='AUTO';p.handle_right_type='AUTO'
    ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);data.materials.append(material)
    if outline:contours.objects.link(ob)
    return ob
handle_points=[[8.78,0,24-6.7],[11.2,0,24-6.15],[13.1,0,24-7.1],[13.35,0,24-9.7],[12.1,0,24-11.8],[10.2,0,24-12.8]]
handle=curve('Connected lunar-arc glass handle',handle_points,.23,glass)
highlights=[]
for label,points in [('bowl',[(3.12,12.9),(3.92,14.3),(3.92,16.7),(3.2,18.9)]),('neck',[(.92,5.7),(.92,7.4),(.92,9.7)])]:
    # Front-left highlight lies on the selected wall, not a detached cap/stripe.
    pts=[(8-r*.65,-r*.76-.025,24-y) for r,y in points];highlights.append(curve('Glass glint '+label,pts,.025,glint,False))
def camera(name,location,target,scale):
    d=bpy.data.cameras.new(name);d.type='ORTHO';d.ortho_scale=scale;ob=bpy.data.objects.new(name,d);s.collection.objects.link(ob);ob.location=location;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
front=camera('Fixed source map camera',(8,-42,12),(8,0,12),24);diag=camera('3D hollow-wall diagnostic',(28,-34,29),(8,0,12),25)
s.camera=diag;s.render.filepath=str(HERE/'stage-02-model-3d.png');bpy.ops.render.render(write_still=True)
s.camera=front;s.render.filepath=str(HERE/'raw-neutral-master.png');bpy.ops.render.render(write_still=True)
body.data.materials[0]=hold;handle.data.materials[0]=hold
for ob in highlights:ob.data.materials[0]=hold
s.render.use_freestyle=False;s.render.filepath=str(HERE/'raw-detail-pass.png');bpy.ops.render.render(write_still=True);s.render.use_freestyle=True
body.data.materials[0]=glass;handle.data.materials[0]=glass
for ob in highlights:ob.data.materials[0]=glint
write('model-controls.json',dict(source=ref(HERE/'source-packet.json'),outer_profile_radius_y=outer,inner_profile_radius_y=inner,handle_points_world=handle_points,handle_radius=.23,
    camera=dict(type='ORTHO',location=[8,-42,12],target=[8,0,12],ortho_scale=24,canvas=[512,768]),
    glass_method='Opaque stylized neutral glass surface matching native coverage; highlights imply glass. Native Transparent tag is preserved, not interpreted as a measured transmission value.',
    detail_region='Source-inspired lower wall at y>=17, independently liquid-colored by native detail. No new fill-height geometry.',
    authored_dimensions='Depth, wall thickness and smoothed lunar-arc handle are authored; original glyph/description do not provide measured dimensions.',new_imagegen_call=False,native_activation=False))
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'bottle.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'bottle.blend'),controls=ref(HERE/'model-controls.json'),actual_views=['fixed-source-map'],diagnostic_views=['oblique hollow-wall proof'],new_imagegen_call=False,native_activation=False))
print('Saved complete editable hollow bottle and connected handle; separate native detail ownership.')
