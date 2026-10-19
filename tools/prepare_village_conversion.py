"""Freeze native inputs and construct front anchors for the village body families.

Original game graphics and donor references stay private. Public packets retain
descriptions, anatomy, hashes and the authored interpretation for each target.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import resvg_py

REPO=Path(__file__).resolve().parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((json.dumps(d,indent=2)+'\n').encode())
def path(d,fill='#cbd0c7',stroke='#303a34',width=3.5):return f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{width}" stroke-linejoin="round" stroke-linecap="round"/>'
def circle(x,y,r,fill='#cbd0c7'):return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" stroke="#303a34" stroke-width="3.5"/>'
def svg(content):return '<svg xmlns="http://www.w3.org/2000/svg" width="256" height="320" viewBox="0 0 256 320">'+content+'</svg>\n'

def front(family):
    female=family in ['human-female','nima'];four=family in ['irudad','nima']
    body=path('M108 143 Q128 137 148 143 L162 169 L156 207 Q168 238 159 266 L155 292 L134 292 L129 272 L123 272 L118 292 L97 292 L94 266 Q85 238 100 207 L94 169 Z' if female else 'M103 143 Q128 137 153 143 L168 174 L157 215 L158 267 L153 292 L132 292 L128 269 L123 269 L120 292 L99 292 L95 267 L97 215 L86 174 Z')
    if family=='yrame':
        body=path('M95 198 Q74 214 69 245 L61 271 L64 280 L88 280 L96 250 L111 228 Z','#a7afa4')
        body+=path('M161 198 Q182 214 187 245 L195 271 L192 280 L168 280 L160 250 L145 228 Z','#a7afa4')
        body+=path('M104 214 L97 256 L92 287 L95 299 L118 299 L126 254 L130 227 Z')
        body+=path('M152 214 L159 256 L164 287 L161 299 L138 299 L130 254 L126 227 Z')
        body+=path('M105 141 Q128 133 151 141 L163 181 L154 221 Q128 234 101 221 L93 181 Z')
    if family=='nima':
        tail=path('M150 232 C216 246 238 197 223 149 C208 102 160 107 164 147 C166 172 203 170 199 146 C194 129 181 136 184 147', 'none','#303a34',19)
        tail+=path('M150 232 C216 246 238 197 223 149 C208 102 160 107 164 147 C166 172 203 170 199 146 C194 129 181 136 184 147','none','#cbd0c7',12)
        tail+=path('M182 146 L172 133 L177 118 L191 137 Z','#a5b3a5')
        for x,y in [(178,231),(207,218),(221,190),(220,160),(207,132)]:tail+=circle(x,y,3,'#e7eade')
        body=tail+body
    if family=='irudad':body=path('M151 252 Q199 276 211 244 L219 231 L225 246 L216 263 Q195 295 151 270 Z')+body
    arms=path('M102 152 Q87 151 81 173 L77 212 L88 222 L98 213 L105 176 M153 152 Q169 151 175 173 L179 212 L168 222 L158 213 L151 176')
    hands=circle(85,220,10)+circle(171,220,10)
    if four:
        if family=='irudad':
            arms+=path('M104 163 Q72 147 73 115 L79 82 L95 80 L92 113 Q91 129 112 135 M152 163 Q184 147 183 115 L177 82 L161 80 L164 113 Q165 129 144 135')
            arms+=path('M80 84 Q85 63 106 61 L128 53 L150 61 Q171 63 176 84 L156 96 L128 105 L100 96 Z','#c7cec2')
            arms+=path('M96 74 L122 69 M100 82 L123 77 M160 74 L134 69 M156 82 L133 77','none','#8a9686',2)
            arms+=circle(111,85,3,'#f2f2e9')+circle(145,85,3,'#f2f2e9')
        else:
            arms+=path('M102 181 Q75 183 66 209 L65 236 L79 244 L90 231 L91 208 M154 181 Q181 183 190 209 L191 236 L177 244 L166 231 L165 208')
            hands+=circle(73,243,9)+circle(183,243,9)
    head=path('M103 86 Q101 67 117 63 L140 63 Q156 67 154 86 L151 115 Q143 135 128 137 Q112 135 105 115 Z','#e2e4db')
    head+=path('M102 93 Q92 87 94 102 Q95 112 104 111 M154 93 Q164 87 162 102 Q161 112 152 111')
    # Irudad's hands-face is above his ordinary head. All four arms stay inside
    # one body graphic; it is not another anatomical Head or an articulated rig.
    if family=='irudad':
        head=path('M108 109 Q103 89 119 85 L138 85 Q153 89 149 109 L147 131 Q141 146 128 148 Q115 146 110 131 Z','#e2e4db')
    return body+arms+hands+head

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,required=True);args=ap.parse_args()
    catalogue=json.loads((REPO/'evidence/joppa-creature-catalogue.json').read_text(encoding='utf-8'))
    runtime=args.root/'runs/catalogue-20261020/joppa-creature-catalogue.json'
    native=json.loads(runtime.read_text(encoding='utf-8'))
    definitions=json.loads((args.root/'scratch/qud-baseline-definitions.json').read_text(encoding='utf-8'))
    actors=[]
    for entry in catalogue['creatures']:
        observed=[a for a in native['actors'] if a['blueprint']==entry['creature']]
        actors.append({**entry,'native_instances':observed,'state':'Source resolved; conversion pending except separately verified cat and dromad'})
    write(REPO/'art/village/sources.json',dict(scope='Captured Joppa actors and 67 selected baseline visible targets; age/sex art templates do not alter demographics',
        runtime_catalogue_sha256=sha(runtime),actors=actors,scenery=[d for d in definitions if d['selected'] and d['blueprint'] not in {a['creature'] for a in actors}],
        exclusions='Non-visible widgets and landmarks are not independent tiles; preserve native behavior. Unknown topology/state retains native graphics.'))
    for family in ['human-male','human-female','irudad','nima','yrame']:
        out=REPO/'art/village/bodies'/family;out.mkdir(parents=True,exist_ok=True)
        vector=out/'front.svg';vector.write_bytes(svg(front(family)).encode());(out/'front.png').write_bytes(resvg_py.svg_to_bytes(svg_path=str(vector),skip_system_fonts=True))
        write(out/'brief.json',dict(family=family,front_sha256=sha(out/'front.png'),source='../../sources.json',
            pipeline='Source identity/race/description/runtime body tree + original icon + actual donor references -> constructed front -> front-guided side/back -> registration -> separate actual equipment',
            body_plan='Captured named anatomy' if family in ['irudad','nima','yrame'] else 'Reusable ordinary human adult race/body template',
            interpretation='Neutral pose; no profession posture. Limbs remain pixels in the body graphic, not render bones.',
            state='Constructed front; turnaround pending'))
    print('Frozen ten actor source packets and scenery descriptions; constructed five adult body front anchors.')
if __name__=='__main__':main()
