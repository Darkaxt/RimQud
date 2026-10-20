"""Register the selected shared human base and prepare one isolated native run."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
from PIL import Image,ImageDraw,ImageChops,ImageFilter,ImageOps
from patch_human_turnaround import neutral

ROOT=Path(__file__).resolve().parents[1];FOLDER=ROOT/'art/conversion/body-human-male/v1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.write_bytes((json.dumps(d,indent=2,ensure_ascii=False)+'\n').encode())

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--native-root',type=Path,required=True);ap.add_argument('--donor-root',type=Path,required=True);a=ap.parse_args()
    raw=Image.open(FOLDER/'refined-patched-views.png').convert('RGBA');views={};registration={};scale=1.21/919
    # Fixed front/back body axis and side contact selected on the inspected sheet.
    contacts=[(272,954),(260,952),(239,954)];necks=[(230,318),(212,260),(210,268)]
    plates=[];game_scale=Image.new('RGB',(900,300),'#142823');draw=ImageDraw.Draw(game_scale)
    for i,d in enumerate(['south','east','north']):
        im=neutral(raw.crop((i*512,0,(i+1)*512,1024)));im.save(FOLDER/f'selected-{d}.png')
        head=Image.new('L',im.size);hd=ImageDraw.Draw(head);hd.rectangle((0,0,512,252),fill=255);hd.rectangle((necks[i][0],252,necks[i][1],280),fill=255)
        body=ImageChops.invert(head).filter(ImageFilter.MaxFilter(5))
        cx,cy=contacts[i];rows=[];parts={}
        for component,mask in [('body',body),('head',head)]:
            mask.save(FOLDER/f'{component}-mask-{d}.png')
            part=im.copy();part.putalpha(ImageChops.multiply(im.getchannel('A'),mask));p=FOLDER/f'{component}-{d}.png';part.save(p);parts[component]=part
            rows.append(dict(component=component,file=f'human-base-v1-{component}-{d}.png',sha256=sha(p),size=[512,1024],contact=[cx,cy],
                color_role='foreground',width=512*scale/(2/3),height=1024*scale,center_x=(256-cx)*scale/(2/3),center_z=(cy-512)*scale,
                layer=.001 if component=='head' else 0,public_file=p.relative_to(ROOT).as_posix()))
        assembled=Image.alpha_composite(parts['body'],parts['head']);plates.append(assembled)
        registration[d]=dict(contact=[cx,cy],head_mask=f'head-mask-{d}.png',body_mask=f'body-mask-{d}.png',neck_x=list(necks[i]),neck_y=[252,280],
                             reconstruction_alpha_bbox=assembled.getchannel('A').getbbox(),maximum_rgb_chroma=max(max(v[:3])-min(v[:3]) for v in assembled.getdata()))
        # Native-size authoring review, explicitly not a native capture.
        thumb=assembled.resize((48,96),Image.Resampling.LANCZOS);x=50+i*280
        game_scale.paste(thumb,(x,65),thumb);game_scale.paste(thumb.resize((96,192),Image.Resampling.NEAREST),(x+70,20),thumb.resize((96,192),Image.Resampling.NEAREST));draw.text((x,240),d+' / 48x96 + 2x',fill='#e3cf43')
        views[d]=rows
    game_scale.save(FOLDER/'game-scale-review.png')
    sheet=Image.new('RGBA',(1536,1024))
    for i,im in enumerate(plates):sheet.alpha_composite(im,(i*512,0))
    sheet.save(FOLDER/'registered-assembly.png')
    model=dict(family='human-male',views=views,pixel_world_scale=scale,canvas=[512,1024],registration=registration,
        geometry='Painted arms/hands/legs/feet stay on body; head/neck uses explicit mask with two-pixel body underlap. West mirrors east.',
        palette='Equal-channel grayscale source, one foreground tint role; no fixed skin color. Separate apparel owns its own tint.',
        state='Body layers registered; native acceptance pending; historical clothing fits remain unaccepted.')
    write(FOLDER/'model.json',model)
    # Keep historical contracts and their hashes intact. This new run owns a
    # versioned candidate contract, with all previous images available locally.
    contract=json.loads((ROOT/'art/village/model.json').read_text(encoding='utf-8'));contract['bodies']['human-male']=model
    write(FOLDER/'native-contract.json',contract)
    native=a.native_root;assert str(native.resolve()).lower().startswith('e:\\temp\\qud-transplant-probe-')
    assert not (native/'launch-pawns.json').exists(),'Use a new owned run, never overwrite prior native evidence'
    (native/'donor').mkdir(parents=True,exist_ok=True)
    for p in a.donor_root.iterdir():
        if p.is_file() and p.suffix in ['.png','.json','.bundle']:shutil.copy2(p,native/'donor'/p.name)
    for rows in views.values():
        for row in rows:shutil.copy2(ROOT/row['public_file'],native/'donor'/row['file'])
    write(native/'village.json',contract)
    print('Registered neutral body/head masks and three views. Prepared isolated native contract without changing historical village inputs.')

if __name__=='__main__':main()
