"""Source-locked low-relief wheel, with explicitly authored inset supports."""
from pathlib import Path
import bpy,json,math,hashlib,xml.etree.ElementTree as ET
from mathutils import Vector
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];OLD=HERE.parent/'v1'
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n',encoding='utf-8')
assert not (HERE/'wheel.blend').exists()
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=12;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=4
s.render.resolution_x=512;s.render.resolution_y=768;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.render.image_settings.file_format='PNG';s.view_settings.view_transform='Standard';s.view_settings.look='None';bpy.context.preferences.filepaths.save_version=0
def mat(name,values):
    m=bpy.data.materials.new(name);m.use_nodes=True;n=m.node_tree.nodes;n.clear();l=m.node_tree.links;g=n.new('ShaderNodeNewGeometry');dot=n.new('ShaderNodeVectorMath');dot.operation='DOT_PRODUCT';dot.inputs[1].default_value=(-.3,-.8,.5)
    ramp=n.new('ShaderNodeValToRGB');ramp.color_ramp.interpolation='CONSTANT'
    for elem,value,pos in [(ramp.color_ramp.elements[0],values[0],0),(ramp.color_ramp.elements[1],values[2],.7)]:elem.position=pos;elem.color=(value,value,value,1)
    elem=ramp.color_ramp.elements.new(.25);elem.color=(values[1],)*3+(1,);e=n.new('ShaderNodeEmission');o=n.new('ShaderNodeOutputMaterial');l.new(g.outputs['Normal'],dot.inputs[0]);l.new(dot.outputs['Value'],ramp.inputs[0]);l.new(ramp.outputs[0],e.inputs[0]);l.new(e.outputs[0],o.inputs[0]);return m
wood=mat('Wet rotted neutral wood - native w',(.07,.14,.24));grain=mat('Restrained dark wet wood furrow',(.025,.04,.07));detailmat=mat('Neutral source inset detail - native y',(.32,.5,.68))
hold=bpy.data.materials.new('Primary holdout for independent detail');hold.use_nodes=True;n=hold.node_tree.nodes;n.clear();h=n.new('ShaderNodeHoldout');o=n.new('ShaderNodeOutputMaterial');hold.node_tree.links.new(h.outputs[0],o.inputs[0])
contours=bpy.data.collections.new('Wheel source contour');s.collection.children.link(contours);s.render.use_freestyle=True;fs=s.view_layers[0].freestyle_settings
for ls in list(fs.linesets):fs.linesets.remove(ls)
ls=fs.linesets.new('Visible shape edges');ls.select_by_collection=True;ls.collection=contours;ls.collection_negation='INCLUSIVE';ls.select_crease=False;ls.linestyle.color=(.01,.01,.01);ls.linestyle.thickness=1.7;ls.linestyle.caps='ROUND'
def world(x,y,depth=0):return (x,depth,24-y)
def curve(name,points,radius,material,group,cyclic=False):
    data=bpy.data.curves.new(name,'CURVE');data.dimensions='3D';data.bevel_depth=radius;data.bevel_resolution=4;sp=data.splines.new('POLY');sp.points.add(len(points)-1)
    for p,q in zip(sp.points,points):p.co=(*q,1)
    sp.use_cyclic_u=cyclic;ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);contours.objects.link(ob);data.materials.append(material);group.append(ob);return ob
def box(name,center,size,material,group):
    bpy.ops.mesh.primitive_cube_add(size=1,location=center);ob=bpy.context.object;ob.name=name;ob.dimensions=size;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);ob.data.materials.append(material);contours.objects.link(ob);group.append(ob);return ob
def prism(name,points,depth,front,material,group):
    vs=[world(x,y,front) for x,y in points]+[world(x,y,front+depth) for x,y in points];n=len(points);faces=[tuple(reversed(range(n))),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    mesh=bpy.data.meshes.new(name);mesh.from_pydata(vs,[],faces);mesh.update();ob=bpy.data.objects.new(name,mesh);s.collection.objects.link(ob);contours.objects.link(ob);mesh.materials.append(material);group.append(ob);return ob
common=[];inset=[];phases={};segments=[]
# Source silhouette is an authored low-relief adaptation, not a recovered
# engineering dimension, physical wheel simulation, or a new native mechanism.
curve('Fixed tall source rim',[world(8+6.35*math.cos(t),11.88+10.28*math.sin(t)) for t in [i*2*math.pi/192 for i in range(192)]],.43,wood,common,True)
box('Native left inner spine',world(7.45,11.9),(.7,.58,19.6),wood,common)
for y in [8.8,15.2]:
    box(f'Authored rear inset support at{y}',world(10.75,y,.16),(6.85,.7,.24),wood,common)
    # Grain along actual mounting wood only; it is not a background or water.
    curve(f'Support seam {y}',[world(7.4,y-.035,-.20),world(13.9,y-.035,-.20)],.018,grain,common)
curve('Authored inset carrier',[world(10.85+1.6*math.cos(t),12+6.6*math.sin(t),-.25) for t in [i*2*math.pi/192 for i in range(192)]],.10,detailmat,inset,True)
for k,ys in {1:[5.3,11.3,17.3],2:[3.3,7.3,13.3,19.3],3:[4.3,9.3,15.3]}.items():
    body=[];detail=[]
    for j,y in enumerate(ys):
        left=2.2 if y<5 or y>18 else 1.45
        prism(f'Phase{k} wet wood paddle{j}',[(left,y),(7.6,y),(7.6,y+3.3),(5.5,y+3.3),(left,y+.85)],.55,-.34,wood,body)
        for x in [4.6,6.2]:curve(f'Phase{k} paddle groove{j} {x}',[world(x,y+.4,-.355),world(x-.08,y+2.3,-.355)],.025,grain,body)
    # Retain the already source-bound merged native marking runs exactly.
    root=ET.fromstring((OLD/f'frame-{k}-patched-constructed.svg').read_text())
    for j,rect in enumerate(node for node in root if node.tag.endswith('rect')):
        x,y,w,h=[float(rect.get(v)) for v in ['x','y','width','height']];cx,cy=x+w/2,y+h/2
        box(f'Phase{k} source detail run{j}',world(cx,cy,-.32),(w,.26,h),detailmat,detail)
        angle=math.atan2((cy-12)/6.6,(cx-10.85)/1.6);ax,ay=10.85+1.6*math.cos(angle),12+6.6*math.sin(angle)
        curve(f'Phase{k} inset marking attachment{j}',[world(ax,ay,-.25),world(cx,cy,-.25)],.085,detailmat,detail)
        segments.append(dict(frame=k,native_run=[x,y,w,h],authored_carrier_contact=[ax,ay],segment_center=[cx,cy]))
    phases[k]=(body,detail)
def camera(name,location,target,scale):
    data=bpy.data.cameras.new(name);data.type='ORTHO';data.ortho_scale=scale;ob=bpy.data.objects.new(name,data);s.collection.objects.link(ob);ob.location=location;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();return ob
front=camera('Source cardinal map camera',(8,-45,12),(8,0,12),24);diag=camera('3D construction diagnostic only',(26,-34,22),(8,0,12),27)
for k,(body,detail) in phases.items():
    for key,group in phases.items():
        for ob in group[0]+group[1]:ob.hide_render=key!=k
    s.camera=diag;s.render.filepath=str(HERE/f'stage-02-model-phase-{k}.png');bpy.ops.render.render(write_still=True)
    s.camera=front;s.render.filepath=str(HERE/f'frame-{k}-neutral-master.png');bpy.ops.render.render(write_still=True)
    originals={ob:ob.data.materials[0] for ob in common+body}
    for ob in originals:ob.data.materials[0]=hold
    s.render.use_freestyle=False;s.render.filepath=str(HERE/f'frame-{k}-detail-pass.png');bpy.ops.render.render(write_still=True);s.render.use_freestyle=True
    for ob,m in originals.items():ob.data.materials[0]=m
for k,group in phases.items():
    for ob in group[0]+group[1]:ob.hide_render=k!=1
s.camera=front
write('model-controls.json',dict(source=ref(OLD/'corrected-source-packet.json'),prior_inspection=ref(HERE.parent/'inspection-v2/independent-inspection.json'),
    interpretation='Right source detail runs are rendered as markings on an authored supported carrier. Two rear wet-wood braces make that carrier belong to the existing rim/spine. No unique native attachment topology is asserted.',
    authored_rear_braces=dict(center_x=10.75,y_down=[8.8,15.2],dimensions=[6.85,.7,.24],depth=.16),inset_carrier=dict(center=[10.85,12],radii=[1.6,6.6],tube_radius=.1,depth=-.25),
    source_segment_runs=segments,camera=dict(type='ORTHO',location=[8,-45,12],target=[8,0,12],ortho_scale=24,canvas=[512,768]),
    limits=['Low relief source-locked shape; hidden depth and supports authored.','Not a recovered gearbox model, axle, motor, collision geometry or physically simulated rotating wheel.','Native phases/timing/HydroTurbine semantics retained; no native activation.'],new_imagegen_call=False))
bpy.ops.wm.save_as_mainfile(filepath=str(HERE/'wheel.blend'))
write('blender-receipt.json',dict(version=bpy.app.version_string,build=bpy.app.build_hash.decode(),model=ref(HERE/'wheel.blend'),controls=ref(HERE/'model-controls.json'),native_phases=[1,2,3],source_frame=[16,24],anchor=[8,16],native_activation=False,new_imagegen_call=False))
print('Saved supported low-relief source wheel in all three native phase layouts.')
