"""Register selected crook surface, completing the hidden grip before body depth."""
from pathlib import Path
import hashlib,json
import numpy as np
from scipy import ndimage,sparse
from scipy.sparse.linalg import spsolve
from PIL import Image,ImageDraw,ImageFont,ImageOps
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];BODY=ROOT/'art/conversion/body-human-male-older/v2';SIZE=(512,1024)
assert not (HERE/'model.json').exists()
def ref(p):return dict(path=p.relative_to(ROOT).as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
def write(name,d):(HERE/name).write_bytes((json.dumps(d,indent=2)+'\n').encode())
def read(p):return Image.open(p).convert('RGBA')
def tint(im,color):
    a=np.array(im);a[:,:,:3]=np.uint8(np.round(a[:,:,:3].mean(2)[:,:,None]*np.array(color)/255));return Image.fromarray(a)
raw=np.array(read(HERE/'refined-red-context.png')).astype(float)
pattern=np.array(read(HERE/'constructed-canonical.png'));envelope=pattern[:,:,3]>0
yy,xx=np.mgrid[0:1024,0:512].astype(float)
mx=(2*xx-302)*raw.shape[1]/1536
my=(2*yy-604)*raw.shape[0]/1280
rgb=np.stack([ndimage.map_coordinates(raw[:,:,c],[my,mx],order=1,mode='constant',cval=0) for c in range(3)],axis=-1)
alpha=ndimage.map_coordinates(raw[:,:,3],[my,mx],order=1,mode='constant',cval=0)
gray=np.clip(rgb@np.array([.2126,.7152,.0722])*1.35+35,0,255)
# Generated brown reed is selected by its actual color, then neutralized. Red body is not material.
wood=(rgb[:,:,0]>=rgb[:,:,1])&(rgb[:,:,1]>=rgb[:,:,2])&(rgb[:,:,0]<1.9*np.maximum(rgb[:,:,1],1))&(rgb[:,:,1]>25)
known=ndimage.binary_erosion(envelope,iterations=2)&wood&(alpha>128)&(gray>50)&(gray<245)
assert known[:490].any() and known[600:].any(),'Both crook and shaft need actual selected material.'
unknown=envelope&~known;uy,ux=np.where(unknown);n=len(uy);ids=np.full(envelope.shape,-1,np.int32);ids[uy,ux]=np.arange(n);degree=np.zeros(n);rhs=np.zeros(n);rr=[];cc=[]
for dy,dx in [(-1,0),(1,0),(0,-1),(0,1)]:
    ny,nx=uy+dy,ux+dx;q=np.flatnonzero((ny>=0)&(ny<1024)&(nx>=0)&(nx<512));q=q[envelope[ny[q],nx[q]]];degree[q]+=1;j=ids[ny[q],nx[q]];pending=j>=0;rr.extend(q[pending]);cc.extend(j[pending]);rhs[q[~pending]]+=gray[ny[q[~pending]],nx[q[~pending]]]
gray[uy,ux]=spsolve(sparse.coo_matrix((-np.ones(len(rr)),(rr,cc)),shape=(n,n)).tocsr()+sparse.diags(degree),rhs)
ink=pattern[:,:,:3].mean(2);gray[(ink<90)&envelope]=ink[(ink<90)&envelope];assert np.isfinite(gray[envelope]).all()
v=np.uint8(np.clip(np.round(gray),0,255));v[~envelope]=0;canonical=Image.fromarray(np.dstack([v,v,v,pattern[:,:,3]]));canonical.save(HERE/'intact-canonical.png')
detail=canonical.copy();region=np.array(Image.open(HERE/'canonical-detail-region.png').convert('L'));detail.putalpha(Image.fromarray(np.minimum(pattern[:,:,3],region)));a=np.array(detail);a[a[:,:,3]==0,:3]=0;detail=Image.fromarray(a);detail.save(HERE/'detail-canonical.png')
Image.fromarray(np.uint8(unknown)*255).save(HERE/'canonical-continuation.png')
packet=json.loads((HERE/'source-packet.json').read_text());controls=json.loads((HERE/'fit-controls.json').read_text());bm=json.loads((BODY/'model.json').read_text())
model=dict(item='Walking Stick',blueprint='Walking Stick',family='irudad',unmutated_body_family='human-male-older',slot='Hand',laterality=6,
    canvas=list(SIZE),contact=[256,950],base_model=ref(BODY/'model.json')['path'],body_sha256=ref(BODY/'model.json')['sha256'],
    actual_equipped_binding=packet['observed_binding'],weapon_metadata=packet['weapon_metadata'],views={},
    binding_scope=packet['fitting_scope'],display_attachment='Ordinary baseline palm proxy only. Actual Hand201/6 under Arm200 with 507::MultipleArms::Change is preserved, not renamed or accepted as integrated.',
    directional_art='Same unmarked planar crook surface for each cardinal body display, with mirrored back/profile as appropriate; actual donor Graphic_Single also uses one weapon surface. Directional placement/depth is authored, not a full 3D cane turnaround.',
    policy='Complete neutral dried brinestalk/crook. Source w primary and g accent stay separate. Original body unchanged; no invented staff-face, metal ring or mutation appendage.',
    pose='Stationary support/display near crook. Ready combat side pose requires forward horizontal projection and a distinct grip/angle/state mapping; not completed by this display.',
    west_policy='Mirrored east for authoring; native actual mutation-hand/aim state remains pending.',native_acceptance=packet['native_acceptance'])
groups={k:{} for k in ['assembly','palette','full','off','grip']};registered={}
for facing,c in controls.items():
    def place(im):
        source=ImageOps.mirror(im) if c['mirror'] else im
        return source.convert('RGBa').transform(SIZE,Image.Transform.AFFINE,c['inverse_affine'],Image.Resampling.BICUBIC).convert('RGBA')
    item=place(canonical);accent=place(detail);item.save(HERE/f'intact-item-{facing}.png');accent.save(HERE/f'item-detail-{facing}.png')
    body=read(BODY/f'selected-{facing}.png');hand=read(HERE/f'original-hand-{facing}.png');equipment=Image.alpha_composite(item,accent)
    off=Image.alpha_composite(body,equipment)
    assembly=Image.alpha_composite(equipment,body) if facing=='north' else Image.alpha_composite(off,hand)
    assembly.save(HERE/f'assembled-{facing}.png');off.save(HERE/f'depth-off-{facing}.png')
    colored_item=Image.alpha_composite(tint(item,(152,135,95)),tint(accent,(0,148,3)));body_color=tint(body,(152,135,95));hand_color=tint(hand,(152,135,95))
    colored=Image.alpha_composite(colored_item,body_color) if facing=='north' else Image.alpha_composite(Image.alpha_composite(body_color,colored_item),hand_color)
    colored.save(HERE/f'qud-palette-{facing}.png')
    for key,im in [('assembly',assembly),('palette',colored),('full',equipment),('off',off)]:groups[key][facing]=im
    gx,gy=c['grip'];groups['grip'][facing]=assembly.crop((gx-100,gy-150,gx+75,gy+70)).resize((315,396))
    rows=[]
    for component,stem,role,layer in [('item','intact-item','equipment',-.0002 if facing=='north' else .0018),('item-detail','item-detail','equipment-detail',-.00019 if facing=='north' else .00181),('body-overlay','original-hand','foreground',.0019)]:
        path=HERE/f'{stem}-{facing}.png';r=ref(path);row=dict(bm['views'][facing][0]);row.update(component=component,file=f'irudad-walking-stick-v1-{component}-{facing}.png',public_file=r['path'],sha256=r['sha256'],equipment_key='walking-stick@Hand@6',color_role=role,layer=layer);rows.append(row)
    model['views'][facing]=rows;registered[facing]=dict(controls=c,body=ref(BODY/f'selected-{facing}.png'),full_item=ref(HERE/f'intact-item-{facing}.png'),original_hand=ref(HERE/f'original-hand-{facing}.png'),body_unchanged=True,display_binding='Ordinary palm proxy, not actual mutation-hand attachment.')
for group in groups.values():group['west (mirror)']=ImageOps.mirror(group['east'])
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
def plate(images,name,title,zoom=False):
    out=Image.new('RGB',(1152,665),'#142823');d=ImageDraw.Draw(out);d.text((18,14),title,font=font,fill='#e3cf43')
    for i,(f,im) in enumerate(images.items()):
        bg=Image.new('RGBA',im.size,'#20382d');bg.alpha_composite(im);out.paste(bg.convert('RGB').resize((256,408 if zoom else 512)),(16+i*284,54));d.text((16+i*284,584),f.upper(),font=font,fill='#e3cf43')
    d.text((18,622),'Ordinary older-base display proxy. Actual changed Hand201/6 and native ready/resting acceptance pending.',font=font,fill='#e5e8d8');out.save(HERE/name)
for key,name,title,zoom in [('assembly','assembly-comparison.png','WALKING STICK / dried brinestalk and spiral crook / baseline proxy',False),('palette','independent-palette-comparison.png','SOURCE PALETTE / stalk w, separate accent g; original body w',False),('full','full-item-comparison.png','INTACT CANE / crook, open return and complete stalk before palm depth',False),('off','depth-off-comparison.png','DEPTH OFF / same full item before original palm/body ownership',False),('grip','grip-comparison.png','SUPPORT DISPLAY / source Hand201/6 retained; ordinary palm is only a proxy',True)]:plate(groups[key],name,title,zoom)
small=Image.new('RGB',(560,370),'#142823');draw=ImageDraw.Draw(small)
for i,(f,im) in enumerate(groups['assembly'].items()):
    thumb=im.resize((48,96),Image.Resampling.LANCZOS);small.paste(thumb,(i*140+45,20),thumb);thumb=thumb.resize((96,192),Image.Resampling.NEAREST);small.paste(thumb,(i*140+20,138),thumb);draw.text((i*140+4,344),f.upper(),font=font,fill='#e3cf43')
small.save(HERE/'game-scale-review.png');write('model.json',model)
write('registration-decisions.json',dict(raw=ref(HERE/'refined-red-context.png'),structural_gate=ref(HERE/'first-refinement-structural-review.json'),material_registration=dict(map_x='(2*x-302)*raw_width/1536',map_y='(2*y-604)*raw_height/1280',neutralization='Selected brown wood -> .2126R+.7152G+.0722B luminance, contrast1.35 and offset35 for neutral tintable surface.',known_pixels=int(known.sum()),completed_pixels=int(unknown.sum()),method='Same front contextual material inside fixed full canonical geometry. Harmonic continuation through hidden palm; original alpha, open crook and dark ink retained.',excluded='Red body, transparent backdrop, generated thickness/body changes and new metal-material interpretation.'),views=registered,new_imagegen_calls=1,second_isolation_call=False,mutation_binding_retained=True,actual_mutation_attachment_accepted=False,pose_followup=model['pose']))
print('Registered full neutral brinestalk/crook from the single contextual refinement; original body and source Hand201/6 preserved.')
