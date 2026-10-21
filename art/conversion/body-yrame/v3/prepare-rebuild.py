"""Preserve user-created centauroid alternatives and source-bound art direction."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, shutil, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[3]
PRIVATE=Path('E:/Temp/rimqud-yrame-centauroid-20261021')
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def ref(p):
    return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
assert not (HERE/'source-packet.json').exists()
old=read(HERE.parent/'v1/source-packet.json')
inputs={
 'horse':'C:/Users/darka/AppData/Local/Temp/codex-clipboard-e35cfa32-3dea-48ed-b987-778c1c579b57.png',
 'sheep':'C:/Users/darka/AppData/Local/Temp/codex-clipboard-948f20ca-e407-42f3-be5b-70acda9976c0.png'}
supplied=[]
for name,p in inputs.items():
    p=Path(p);out=HERE/('user-'+name+'-turnaround.png');shutil.copyfile(p,out)
    supplied.append(dict(kind=name,original=ref(p),project_copy=ref(out),reported_generator='ImageGen, reported by user; not a Codex-executed call',
        reported_prompt='Make our female human into a centaur (user paraphrase).' if name=='horse' else 'Not supplied; user describes a sheep-like alternative.',
        original_generation_inputs='Exact uploaded source files and generator receipt were not supplied.',format='RGB black-matted sheet, not transparent RGBA'))
horse=read(PRIVATE/'donor-references.json');sheep=read(PRIVATE/'sheep-references.json')
defs=Path('D:/Steam/steamapps/common/RimWorld/Data/Core/Defs/ThingDefs_Races/Races_Animal_SheepGroup.xml')
packet=dict(entry='BODY-YRAME',recorded_at=datetime.now(timezone.utc).isoformat(),
    resolved_identity=old['identity_chain'],captured_species='human',captured_gender='female',
    native_metadata=ref(HERE.parent/'v1/source-packet.json'),correction=ref(HERE.parent/'v2/source-body-plan-correction.json'),
    original=old['original'],source_description=old['captured_actor']['description'],
    visual_family='Human-based mutant with upright upper body and horizontal four-legged lower trunk; not the ordinary bipedal visual template.',
    source_facts=dict(fore_group=dict(part=297,parent=287,laterality=16,manager='515::MultipleLegs::Change',boots_instance=580),
        hind_group=dict(part=298,parent=287,laterality=64,manager='515::MultipleLegs::Add',equipped=None),
        horns=dict(part=288,instance=575,independent_equipment=True),physical_legs=4,
        mutation_level='MultipleLegs6 is a level, not six legs.',joint_coordinates='Unknown; native slots are not anatomical render bones.'),
    body_plan_decision=dict(status='Authoring choice based on source silhouette and user-supplied alternatives',
        selected_start='user-sheep-turnaround.png',reason='Compact sheep-like lower mass and ram-horn reading fit the source better than an elongated equine tail/body.',
        uncertain='Exact lower-body species, fleece, hoof anatomy and hidden joint positions are not established by native prose or slots.',
        direction='Keep the user-created centauroid attachments; reduce giant wool clumps to restrained map-readable fleece. Horns remain separate.',
        tail='Supplied alternatives add a tail. No Tail part, tail mutation or descriptive tail is captured; omit the unconfirmed tail in selected body art.'),
    palette=dict(native_tileColor='w',native_detailColor='B',neutral='Grayscale albedo with independent palette ownership.',
        authored_mapping='Upper torso/arms/head use w; predominantly blue lower source silhouette maps lower trunk/legs to B. This is render-region ownership, not a claim of permanent biological coat color. Head cosmetics remain outside this pass.'),
    ordinary_base=old['baseline'],supplied_generations=supplied,
    references=dict(core_packed_asset=horse['source_asset'],horse=horse['textures'],sheep=sheep,sheep_definition=ref(defs),human=old['donor_references'],
        roles='Human assets: upper-body cardinal convention. Sheep: compact quadruped mass, quiet fleece shading; male texture also supplies a later horn cue. Horse: alternative horizontal body proportions only. Core animal textures do not themselves draw individual legs; four legs come from Qud and the selected authoring candidate. No donor mane/tail/animal head/species, footprint or runtime behavior is transplanted.'),
    renderer='Authored fixed named body/Head art and ownership masks only. No new articulated legs, general mutation resolver or native activation.',
    registration='Use common contact/pivot and one physical pixel scale across facings; do not fit independent alpha bounds.',
    acceptance='Generation-time structural review and registration only. All native integration checks remain behind the full-generation gate.')
write(HERE/'source-packet.json',packet)
font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',16)
plate=Image.new('RGB',(1450,820),'#142823');d=ImageDraw.Draw(plate)
d.text((18,16),'YRAME / original silhouette + actual donor references + USER-SUPPLIED refined alternatives',font=font,fill='#e3cf43')
mask=np.array(Image.open(old['original']['private_mask']['path']).convert('RGBA'))
pal=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette']
colors=[np.frombuffer(bytes.fromhex(pal[c]),dtype=np.uint8) for c in ['w','B']]
rgb=np.where((mask[:,:,0]>127)[:,:,None],colors[1],colors[0]);original=Image.fromarray(np.dstack((rgb,mask[:,:,3])).astype('uint8')).resize((128,192),Image.Resampling.NEAREST)
plate.paste(original,(25,60),original);d.text((18,265),'QUD w / B',font=font,fill='#e3cf43')
for i,(label,p) in enumerate([('CORE FEMALE / upper body',Path(old['donor_references'][1]['path'])),('CORE SHEEP / compact mass',PRIVATE/'SheepMale_east.png'),('CORE HORSE / alternative',PRIVATE/'Horse_east.png')]):
    im=Image.open(p).convert('RGBA');im.thumbnail((230,190));x=240+i*390;plate.paste(im,(x,60),im);d.text((x-10,265),label,font=font,fill='#e3cf43')
for i,name in enumerate(['horse','sheep']):
    im=Image.open(HERE/('user-'+name+'-turnaround.png')).resize((680,453),Image.Resampling.LANCZOS)
    x=18+i*720;plate.paste(im,(x,315));d.text((x,780),name.upper()+' / user-reported ImageGen output',font=font,fill='#e3cf43')
plate.save(HERE/'source-reference-alternatives.png')
# An editable art-direction overlay, not a claim that these unseen joints were exported.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1536" height="1024" viewBox="0 0 1536 1024">
<image href="user-sheep-turnaround.png" width="1536" height="1024"/>
<g fill="none" stroke="#f4cc40" stroke-width="3" stroke-dasharray="10 8">
<path d="M145 402 Q250 425 350 402 M595 440 Q740 415 850 445 M1190 410 Q1290 425 1390 410"/>
<path d="M150 570 L140 740 L150 918 M195 570 L200 760 L204 946 M310 570 L300 760 L302 946 M360 570 L355 740 L355 918"/>
<path d="M660 540 L600 720 L595 940 M700 550 L655 730 L675 930 M936 530 L938 735 L938 942"/>
</g><g fill="#f4cc40" font-family="monospace" font-size="19">
<text x="120" y="995">FRONT / SOUTH</text><text x="620" y="995">RIGHT PROFILE / EAST</text><text x="1190" y="995">BACK / NORTH</text>
</g></svg>'''
(HERE/'manual-attachment-guides.svg').write_text(svg,encoding='utf-8')
write(HERE/'manual-direction.json',dict(kind='Editable attachment/region guides over the selected user-created turnaround; not a new hand-drawn creature.',
    source=ref(HERE/'user-sheep-turnaround.png'),guide=ref(HERE/'manual-attachment-guides.svg'),
    preserve='Horizontal trunk, forelegs under upright torso, hindlegs under rear trunk, original upper-body family and full cardinal facing.',
    changes='Restrained fleece; remove unconfirmed tail; retain four physical legs with natural far-side occlusion. Do not add sheep head, horns, clothing or equipment to this body.',
    front_anchor='Selected user-provided south/front is the corrected front design. V1/V2 biped-plus-legs shapes remain rejected history.',
    unknown='Guide points are authored pose landmarks, not native joint coordinates. Exact fitting/contact ownership follows registration of the selected refinement.'))
prompt='''Edit the supplied neutral gray female SHEEP-CENTAUR turnaround for a RimWorld-like layered game sprite.
Image 1 is the edit target: the user transformed our existing female human template into this compact sheep-centaur, and we accept its body plan. Image 2 is SOURCE AND RENDERING CONTEXT ONLY: Qud original sprite plus actual RimWorld Core references and the user's two alternatives. Do not copy the other figures from Image 2 into the output.
Keep exactly THREE full-body views in the existing order: straight FRONT/SOUTH, complete RIGHT PROFILE/EAST facing right, straight BACK/NORTH. Whole body turns; no three-quarter view. Preserve the selected humanoid upper torso, blank mannequin head, two arms and hands, horizontal compact sheep-like lower trunk and FOUR animal legs. Forelegs attach underneath the front trunk, hindlegs underneath the rump. Never attach human legs to the buttocks of a standing biped. Preserve the current natural profile overlap; an occluded far leg does not need to be artificially splayed into view.
Refine only these source-consistency issues: reduce the huge balloon-like wool clusters to a restrained short-fleece surface with a few broad soft tufts and a quieter contour, preserving body volume and the complete fore/hind attachment structure. Remove the unconfirmed tail in PROFILE and BACK; complete the ordinary lower-rump fleece where it was attached. There is no tail in the captured native body/mutation metadata. Retain the selected compact sheep-like proportions, slender lower legs and small cloven hooves as the current authored interpretation. Keep a smooth, featureless human upper body and normal circular mannequin hands. No extra anatomy details.
All albedo must be NEUTRAL GRAYSCALE: white/light gray forms, charcoal clean outlines, restrained gray shading. No fixed blue fur or colored skin; Qud colors are applied later through separate masks. No horns, mane, animal head, clothing, weapon, jewelry, eyes, hair or effects. Horns are a separate later equipped item.
Keep every full figure within its own panel with generous margins, matched physical scale and a common foot baseline. Use a genuinely TRANSPARENT background, no black matte, no labels, no guides, no checkerboard, no ground shadow. This is a restrained composed body refinement, not garment extraction and not a new species redesign.'''
(HERE/'composed-refinement-prompt.txt').write_text(prompt,encoding='utf-8')
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='BODY-YRAME'
e=next(x for x in ledger['entries'] if x['id']=='BODY-YRAME')
def event(step,action,ins,outs,review,result='PASS'):
 e['process_log'].append(dict(timestamp=datetime.now(timezone.utc).isoformat(),step=step,action=action,inputs=[ref(p) for p in ins],outputs=[ref(p) for p in outs],review=review,result=result))
event(e['required_steps'][0],'Resolve actual centauroid silhouette and preserve both user-created alternatives with honest generation provenance.',[HERE.parent/'v1/source-packet.json',HERE.parent/'v2/source-body-plan-correction.json'],[HERE/'source-packet.json',HERE/'user-horse-turnaround.png',HERE/'user-sheep-turnaround.png'],'Source confirms four legs and fore/hind slots. Compact sheep-like coat/hoof anatomy is an authored choice, not a new native race. User image generation is not claimed as a Codex tool call.')
event(e['required_steps'][1],'Inspect actual Core female, horse and sheep directional assets for their limited visual-reference roles.',[PRIVATE/'donor-references.json',PRIVATE/'sheep-references.json'],[HERE/'source-reference-alternatives.png'],'Actual Core animals supply mass/shading rather than separate leg nodes. Both original and alternative silhouettes are visible in context; private raw donor textures stay out of the public bundle.')
event(e['required_steps'][2],'Select user-supplied corrected front and establish editable coat/attachment guides in the coherent turnaround.',[HERE/'user-sheep-turnaround.png'],[HERE/'manual-attachment-guides.svg',HERE/'manual-direction.json'],'The corrected front replaces the rejected biped-plus-pair design. This records user-generated geometry reuse and manual art direction without pretending it was hand-drawn from scratch.')
event(e['required_steps'][3],'Reuse the user-provided complete profile and back produced with the corrected front family.',[HERE/'user-sheep-turnaround.png'],[],'All three supplied views show the compact horizontal lower trunk and quadrupedal legs. Exact original user generation inputs/settings are unknown and recorded as such. Tail/fleece corrections and alpha recovery remain required.')
event(e['required_steps'][4],'Prepare one contextual refinement of the selected user-supplied body, with explicit source facts and bounded corrections.',[HERE/'user-sheep-turnaround.png',HERE/'source-reference-alternatives.png'],[HERE/'prepare-rebuild.py',HERE/'composed-refinement-prompt.txt'],'Actual tool call and output pending; no generation-readiness or native acceptance claimed.','REQUIRES REVIEW')
e['current_step']=e['required_steps'][4];e['known_issues']=['Refine selected compact sheep-like centauroid: restrained fleece, omit unconfirmed tail, restore genuine alpha, then register body/head and independent w/B roles.']
ledger['updated_at']=datetime.now(timezone.utc).isoformat();write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Preserved both user alternatives, source/reference/guide evidence and exact pending refinement prompt.')
