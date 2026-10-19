"""Author fully clothed child templates without assigning ages to Qud residents.

No selected Qud actor exports a life-stage selector. These are reviewable art
variants, never a heuristic age override. Adult dromad sexes share the selected
race body because the sources establish no distinct sexual morphology.
"""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import resvg_py

REPO=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True);a=ap.parse_args()
    families={}
    for race in ['human','dromad']:
        folder=REPO/'art/village/age-templates'/race;folder.mkdir(parents=True,exist_ok=True);views={}
        for d in ['south','east','north']:
            side=d=='east';back=d=='north'
            # Short torso, larger head/body proportion, closed shoes and plain
            # tunic. Explicit whole-side geometry, not a uniformly scaled adult.
            body='M179 600 Q164 630 176 724 L190 803 H235 L247 737 H265 L279 803 H323 L337 724 Q346 630 329 600Z' if not side else 'M210 600 Q180 640 199 733 L212 803 H265 L270 753 L286 803 H326 L320 692 Q322 628 296 600Z'
            head='M179 400 Q174 324 253 319 Q336 324 333 400 Q329 475 256 479 Q179 472 179 400Z'
            if side:head='M220 326 Q304 315 321 361 L348 379 Q358 406 325 415 L315 465 Q249 494 213 442 Q180 372 220 326Z'
            neck='M229 461 V524 H282 V461Z'
            if race=='dromad':
                neck='M221 302 L218 591 Q253 608 291 590 L291 302Z'
                head='M210 306 L185 254 L204 244 L232 267 Q261 253 290 267 L317 244 L336 254 L309 306 Q333 365 303 396 Q256 421 213 394 Q187 360 210 306Z'
                if side:head='M216 283 L208 239 L228 245 L250 273 Q287 259 304 287 L345 308 Q368 328 352 350 L292 361 L284 403 L228 401 Q198 353 216 283Z'
                body+=' M208 596 Q178 542 152 575 Q134 614 185 654Z' if side else ' M200 601 Q160 552 154 600 Q151 625 183 650Z'
            face='' if back else ('<circle cx="282" cy="359" r="7"/>' if side else '<circle cx="225" cy="365" r="7"/><circle cx="286" cy="365" r="7"/>')
            if race=='dromad' and not back:face+=('<path d="M300 327 Q331 336 345 328" fill="none"/>' if side else '<ellipse cx="258" cy="363" rx="47" ry="28" fill="#c8cec0"/>')
            y=501 if race=='human' else 570
            robe=f'M215 {y} Q254 {y+20} 295 {y} L331 {y+28} L351 677 L321 690 L306 641 L322 745 Q256 763 191 745 L205 641 L190 690 L160 677 L181 {y+28}Z'
            if side:robe=f'M221 {y} Q260 {y+17} 291 {y} L316 {y+24} L331 674 L301 683 L288 636 L315 745 Q257 760 202 743 L193 {y+55}Z'
            components={'body':f'<path d="{body}" fill="#aab7a6"/><path d="{neck}" fill="#dce0d4"/>','head':f'<path d="{head}" fill="#dce0d4"/><g fill="#27392e">{face}</g>','tunic':f'<path d="{robe}" fill="#c6d0b9"/><path d="M235 {y+49}L224 729 M280 {y+46}L292 730" fill="none" stroke="#849981" stroke-width="4"/>'}
            layers=[]
            for index,(name,shape) in enumerate(components.items()):
                svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="512" height="1024"><g stroke="#283a30" stroke-width="7" stroke-linejoin="round">{shape}</g></svg>\n'
                p=folder/f'{name}-{d}.svg';p.write_bytes(svg.encode());png=p.with_suffix('.png');png.write_bytes(resvg_py.svg_to_bytes(svg_path=str(p),skip_system_fonts=True))
                filename=f'village-child-{race}-{name}-{d}.png';shutil.copy2(png,a.root/'donor'/filename)
                scale=.00165;layers.append(dict(component=name,file=filename,public_file=png.relative_to(REPO).as_posix(),sha256=hashlib.sha256(png.read_bytes()).hexdigest(),size=[512,1024],contact=[256,807],color_role='foreground',width=512*scale/(2/3),height=1024*scale,center_x=0,center_z=(807-512)*scale,layer=index*.001))
            views[d]=layers
        families[race]=dict(family=race+'-child',views=views,fully_clothed=True,gender='Shared neutral child template',selection='Unbound: no native life-stage field established for selected Joppa actors',authoring='Explicit age-proportion geometry; Qud race description and adult family; donor Child body convention is presentation reference only')
    data=dict(templates=families,adult_dromad_sexes='Same selected adult body; no source-supported sex morphology difference',animal_variants='Retain selected ray cat and fish. No juvenile or sex-specific morphology established in captured sources.',native_age_selection=False)
    (REPO/'art/village/age-templates.json').write_bytes((json.dumps(data,indent=2)+'\n').encode())
    print('Authored fully clothed human/dromad child templates; native residents and demographics unchanged.')
if __name__=='__main__':main()
