"""Final Nima tail projection, including the asymmetric west-side depth view."""
from pathlib import Path
import numpy as np
from resvg_py import svg_to_bytes

def render_tail(folder,data,frame,low,high):
    centres=np.array(data['centreline']);stinger=np.array(data['stinger']);bead=np.array(data['bead'])
    sx=frame['width']/512;sz=frame['height']/1264
    def project(points,facing):
        p=np.array(points)
        h={'south':p[:,0],'east':p[:,1],'north':-p[:,0],'west':-p[:,1]}[facing]
        depth={'south':p[:,1],'east':p[:,0],'north':-p[:,1],'west':-p[:,0]}[facing]
        return np.column_stack([256+h/sx,1190-p[:,2]/sz]),depth
    light=np.array([-.4,.25,.85]);light/=np.linalg.norm(light)
    for facing in ['south','east','north','west']:
        parts={'back':[],'front':[]};surfaces=[]
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
                luminance=int(np.clip((low+high)/2+(high-low)/2*np.dot(normal,light),low,high))
                coords=' '.join(f'{x:.3f},{y:.3f}' for x,y in xy)
                shape=f'<polygon points="{coords}" fill="rgb({luminance},{luminance},{luminance})" stroke="#777777" stroke-width="1" stroke-linejoin="round"/>'
                layer='front' if depth.mean()>0 else 'back';surfaces.append((float(depth.mean()),layer,shape))
        for _,layer,shape in sorted(surfaces,key=lambda r:r[0]):parts[layer].append(shape)
        xy,depth=project(stinger,facing);coords=' '.join(f'{x:.3f},{y:.3f}' for x,y in xy);layer='front' if depth.mean()>0 else 'back'
        parts[layer].append(f'<polygon points="{coords}" fill="#d2d2d2" stroke="#2b2b2b" stroke-width="5" stroke-linejoin="round"/>')
        xy,_=project([bead],facing);x,y=xy[0]
        parts[layer].append(f'<ellipse cx="{x:.3f}" cy="{y:.3f}" rx="4.5" ry="7" fill="#fafafa" stroke="#555555" stroke-width="2"/>')
        for layer in ['back','front']:
            source='<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1264" viewBox="0 0 512 1264">'+''.join(parts[layer])+'</svg>'
            p=folder/f'tail-{layer}-{facing}.svg';p.write_bytes(source.encode());p.with_suffix('.png').write_bytes(svg_to_bytes(svg_string=source))
