"""Project Nima's one authored segmented tail into fixed cardinal body frames."""
from pathlib import Path
import numpy as np
from resvg_py import svg_to_bytes

def render_tail(folder,centres,stinger,bead,frame,prefix,low=195,high=239):
    sx=frame['width']/512;sz=frame['height']/1264
    def project(points,facing):
        p=np.array(points);h=p[:,0] if facing=='south' else (p[:,1] if facing=='east' else -p[:,0])
        depth=p[:,1] if facing=='south' else (p[:,0] if facing=='east' else -p[:,1])
        return np.column_stack([256+h/sx,1190-p[:,2]/sz]),depth
    light=np.array([-.4,.25,.85]);light/=np.linalg.norm(light)
    for facing in ['south','east','north']:
        parts={'back':[],'front':[]};details={'back':[],'front':[]};surfaces=[]
        for index,(a,b) in enumerate(zip(centres[:-1],centres[1:])):
            axis=b-a;axis/=np.linalg.norm(axis)
            guide=np.array([0.,0,1]) if abs(axis[2])<.9 else np.array([1.,0,0])
            u=np.cross(axis,guide);u/=np.linalg.norm(u);v=np.cross(axis,u)
            radius=.033-.009*index/(len(centres)-2);angles=np.arange(8)*np.pi/4
            ring0=np.array([a+radius*(np.cos(w)*u+np.sin(w)*v) for w in angles])
            ring1=np.array([b+radius*.94*(np.cos(w)*u+np.sin(w)*v) for w in angles])
            for k in range(8):
                p=np.array([ring0[k],ring0[(k+1)%8],ring1[(k+1)%8],ring1[k]])
                xy,depth=project(p,facing);normal=np.cos(angles[k]+np.pi/8)*u+np.sin(angles[k]+np.pi/8)*v
                luminosity=int(np.clip((low+high)/2+(high-low)/2*np.dot(normal,light),low,high))
                coords=' '.join(f'{x:.3f},{y:.3f}' for x,y in xy)
                shape=f'<polygon points="{coords}" fill="rgb({luminosity},{luminosity},{luminosity})" stroke="#393939" stroke-width="2.5" stroke-linejoin="round"/>'
                layer='front' if depth.mean()>0 else 'back';surfaces.append((float(depth.mean()),layer,shape))
            centre=(a+b)/2;xy,depth=project([centre],facing);x,y=xy[0];layer='front' if depth[0]>0 else 'back'
            details[layer].append(f'<path d="M{x:.2f} {y-6:.2f} L{x+5:.2f} {y:.2f} L{x:.2f} {y+6:.2f} L{x-5:.2f} {y:.2f}Z" fill="#f5f5f5" stroke="#777777" stroke-width="1.5"/>')
        for _,layer,shape in sorted(surfaces,key=lambda r:r[0]):parts[layer].append(shape)
        xy,depth=project(stinger,facing);coords=' '.join(f'{x:.3f},{y:.3f}' for x,y in xy);layer='front' if depth.mean()>0 else 'back'
        parts[layer].append(f'<polygon points="{coords}" fill="#d2d2d2" stroke="#2b2b2b" stroke-width="5" stroke-linejoin="round"/>')
        xy,_=project([bead],facing);x,y=xy[0]
        shape=f'<ellipse cx="{x:.3f}" cy="{y:.3f}" rx="4.5" ry="7" fill="#fafafa" stroke="#555555" stroke-width="2"/>'
        parts[layer].append(shape);details[layer].append(shape)
        for layer in ['back','front']:
            for name,shapes in [(f'{prefix}-tail-{layer}-{facing}',parts[layer]+details[layer]),(f'{prefix}-tail-detail-{layer}-{facing}',details[layer])]:
                svg='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1264" viewBox="0 0 512 1264">'+''.join(shapes)+'</svg>'
                (folder/(name+'.svg')).write_bytes(svg.encode());(folder/(name+'.png')).write_bytes(svg_to_bytes(svg_string=svg))
