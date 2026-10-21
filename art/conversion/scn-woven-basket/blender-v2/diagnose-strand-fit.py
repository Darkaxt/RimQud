from pathlib import Path
import bpy,math,json
p=Path(__file__).resolve().parent;bpy.ops.wm.open_mainfile(filepath=str(p/'basket.blend'));rows=[]
for col in range(16):
 ob=bpy.data.objects[f'Bound vertical warp {col}'];phi=col*2*math.pi/16;values=[(v.co.x-8)*math.cos(phi)+v.co.y*math.sin(phi) for v in ob.data.vertices];rows.append(dict(strand=ob.name,min_radial=min(values),max_radial=max(values)))
for row in range(6):
 ob=bpy.data.objects[f'Complete weft course {row}'];values=[(v.co.x-8)*math.cos((i//2)*2*math.pi/128)+v.co.y*math.sin((i//2)*2*math.pi/128) for i,v in enumerate(ob.data.vertices)];rows.append(dict(strand=ob.name,min_radial=min(values),max_radial=max(values)))
print(json.dumps(rows,indent=2));(p/'strand-fit-diagnostic.json').write_text(json.dumps(rows,indent=2)+'\n',encoding='utf-8')
