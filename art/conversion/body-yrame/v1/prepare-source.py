"""Resolve Yrame's missing body prerequisite without claiming a finished conversion."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,re
import numpy as np
from PIL import Image,ImageDraw,ImageFont
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
NPC=ROOT/'art/conversion/npc-warden-yrame/v1'
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
def write(p,v):p.write_bytes((json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode())
def ref(p):return dict(path=p.relative_to(ROOT).as_posix() if p.is_relative_to(ROOT) else p.as_posix(),sha256=hashlib.sha256(p.read_bytes()).hexdigest())
ledger=read(ROOT/'evidence/conversion-ledger.json');assert ledger['active_entry']=='NPC-WARDEN-YRAME'
npc=next(e for e in ledger['entries'] if e['id']=='NPC-WARDEN-YRAME');entry=next(e for e in ledger['entries'] if e['id']=='BODY-YRAME')
assert not npc['process_log'] and not entry['process_log'] and not (HERE/'source-packet.json').exists()
sources=read(ROOT/'art/village/sources.json');source=next(s for s in sources['actors'] if s['creature']=='Warden Yrame');actor=next(a for a in source['native_instances'] if a['instance']==515)
assert actor['parts']==npc['metadata']['native_parts'] and sources['runtime_catalogue_sha256']==npc['metadata']['source_snapshot']
dependencies=[]
for ident in npc['related_entries']:
    dep=next(e for e in ledger['entries'] if e['id']==ident)
    record=dep.get('current_registration',{}).get('model')
    if record:assert ref(ROOT/record['path'])==record
    dependencies.append(dict(entry=ident,generation_ready=bool(dep.get('generation_ready')),model=record))
assert [d['entry'] for d in dependencies if not d['generation_ready']]==['BODY-YRAME']
baseline=next(e for e in ledger['entries'] if e['id']=='BODY-HUMAN-FEMALE');assert baseline['generation_ready']
baseref=baseline['current_registration']['model'];assert ref(ROOT/baseref['path'])==baseref
feet=[p for p in actor['parts'] if p['type']=='Feet']
assert [(p['id'],p['laterality'],p['manager']) for p in feet]==[(297,16,'515::MultipleLegs::Change'),(298,64,'515::MultipleLegs::Add')]
assert feet[0]['equipped']['instance']==580 and feet[1]['equipped'] is None
equipped=[dict(part_id=p['id'],slot=p['type'],laterality=p['laterality'],item=p['equipped']) for p in actor['parts'] if p.get('equipped')]
assert len(equipped)==4
NPC.mkdir(parents=True,exist_ok=True);now=datetime.now(timezone.utc).isoformat()
preflight=dict(entry=npc['id'],recorded_at=now,source=ref(ROOT/'art/village/sources.json'),source_snapshot=npc['metadata']['source_snapshot'],captured_actor=actor,dependencies=dependencies,
    equipped_items=equipped,missing_prerequisite='BODY-YRAME',next_action='Generate separate additional leg pair on the unchanged shared female body, retaining both Feet groups and existing item fits. Then return to the four-item NPC assembly.',
    boundaries='Horns575 stays actual Head288 equipment. Default Icy Vapor579 on grouped Hands174 is native natural equipment, not an invented extra glove or additional arm. No costume, horn or freezing effect is baked into the baseline body. Native mutation/equipment behavior remains behind the full-generation gate.')
write(NPC/'source-packet.json',preflight)
native=Path('D:/Steam/steamapps/common/Caves of Qud/CoQ_Data/StreamingAssets/Base');defs=native/'ObjectBlueprints/Creatures.xml';bodydefs=native/'Bodies.xml'
fragment=re.search(r'<object Name="Warden Yrame"(?=\s|>).*?</object>',defs.read_text(),re.S)
assert fragment
feetdef=next(line.strip() for line in bodydefs.read_text().splitlines() if '<bodyparttype Type="Feet"' in line)
private=Path('E:/Temp/qud-transplant-probe-pawns-20261019/scratch/inspect/XRL.World.Parts.Mutation.MultipleLegs.decompiled.cs')
assert ref(private)['sha256']==read(ROOT/'evidence/joppa-anatomy-study.json')['private_source_audit']['XRL.World.Parts.Mutation.MultipleLegs']
original=next(r for r in read(ROOT/'evidence/village-reference-index.json')['entries'] if r['blueprint']=='Warden Yrame')
mask=Path('E:/Temp/qud-transplant-probe-pawns-20261019/donor')/original['reference_file'].replace('-reference','-mask');assert ref(mask)['sha256']==original['native_mask_sha256']
donors=read(ROOT/'art/conversion/body-nima/v1/source-packet.json')['donor_references'][:3]
for r in donors:assert ref(Path(r['path']))['sha256']==r['sha256']
packet=dict(entry=entry['id'],recorded_at=now,identity_chain=source['lineage'],race_description=source['race_input'],captured_actor=actor,source=ref(ROOT/'art/village/sources.json'),source_snapshot=npc['metadata']['source_snapshot'],preflight=ref(NPC/'source-packet.json'),
    native_definition=dict(**ref(defs),fragment=fragment.group()),feet_type=dict(**ref(bodydefs),fragment=feetdef),private_multiple_legs_source=ref(private),
    original=dict(**original,private_mask=ref(mask)),baseline=baseref,baseline_history=ref(ROOT/'art/conversion/body-human-female/v1/source-packet.json'),donor_references=donors,
    anatomy=dict(baseline='Reuse unmutated female human body/head and original two arms/hands and paired legs/feet unchanged.',
        additions='One separate extra leg/foot pair: Feet297/16 changed and Feet298/64 added. The paired Feet type has Mobility2 and plural=true; native description explicitly distinguishes hind and forelegs. Four physical feet is the supported interpretation, not mutation Level6 interpreted as six legs.',
        native_parts=actor['parts'],algorithm_summary='Installed MultipleLegs adds one Feet group, changes the original group laterality to16 and assigns Add/Change managers. Do not turn grouped slots into render bones.',
        equipment='Horns, mail, blade and boots stay separate current fitting entries. Boots580 occupy only Feet297/16, not both pairs. Icy Vapor remains native natural equipment metadata.'),
    interpretation=dict(no_whole_body_equivalent='Core female cardinal assets supply ordinary human rendering and shading only. No whole four-legged-human donor equivalent is claimed; additional-leg geometry must be authored from Qud facts.',
        geometry='Pelvis attachment, spacing, overlap and unseen surfaces remain authored interpretations. Preserve the existing shared body and item frame/contact; do not repeat the rejected three-foot silhouette.',
        palette='Native tileColor w and detail B are retained. Per-component assignments require a recorded authoring decision; prose freezing vapour is not permission to flood blue into the neutral base.',
        cosmetics='Keep face blank. No new personal hair, eyes, scars, veins or freezing particles in this body phase.',
        native='No mutation framework, native body activation, game launch or lifecycle/animation acceptance during generation.'))
write(HERE/'source-packet.json',packet)
palette=read(ROOT/'evidence/joppa-anatomy-study.json')['native_palette'];rgb=lambda c:np.frombuffer(bytes.fromhex(palette[c]),dtype=np.uint8)
a=np.array(Image.open(mask).convert('RGBA'));w=a[:,:,:1].astype(float)/255
original_im=Image.fromarray(np.dstack([np.uint8(np.round((1-w)*rgb('w')+w*rgb('B'))),a[:,:,3]]))
model=read(ROOT/baseref['path']);out=Image.new('RGB',(1400,900),'#142823');d=ImageDraw.Draw(out);font=ImageFont.truetype('C:/Windows/Fonts/consola.ttf',15)
d.text((18,15),'YRAME515 > original + metadata + actual Core reference > unchanged reusable female base',font=font,fill='#e3cf43')
out.paste(original_im.resize((160,240),Image.Resampling.NEAREST),(35,100),original_im.resize((160,240),Image.Resampling.NEAREST))
for i,f in enumerate(['south','east','north']):
    donor=Image.open(donors[i]['path']).convert('RGBA').resize((180,180),Image.Resampling.NEAREST);out.paste(donor,(260,60+i*190),donor)
    im=Image.new('RGBA',(512,1024))
    for r in sorted(model['views'][f],key=lambda r:r['layer']):im.alpha_composite(Image.open(ROOT/r['public_file']).convert('RGBA'))
    im=im.resize((240,480),Image.Resampling.LANCZOS);out.paste(im,(540+i*280,65),im);d.text((540+i*280,570),f.upper()+' BASE / UNMUTATED',font=font,fill='#e3cf43')
d.text((25,590),'QUD ORIGINAL w/B',font=font,fill='#e3cf43');d.text((260,655),'ACTUAL CORE FEMALE',font=font,fill='#e3cf43')
lines=['Two paired Feet groups: changed297/16 has Boots580; added298/64 is unequipped. Supported interpretation:4feet.',
       'Next: construct ONE separate additional leg pair. This plate intentionally shows the unmutated baseline only.',
       'Horns575/Head288, Mail574/Body287, Blade576/Hand292 and Boots580/Feet297 stay separate actual items.',
       'Historical three-foot proposals and later unrefined patches remain rejected/history, not generation credit.',
       'No whole donor equivalent or exact unseen anatomy claimed. No new body art or native acceptance yet.']
for i,line in enumerate(lines):d.text((18,715+i*31),line,font=font,fill='#e5e8d8')
out.save(HERE/'source-reference-baseline.png')
def event(e,step,action,ins,outs,review):e['process_log'].append(dict(timestamp=now,step=step,action=action,inputs=[ref(p) for p in ins],outputs=[ref(p) for p in outs],review=review,result='PASS'))
event(npc,npc['required_steps'][0],'Resolve Yrame515 exact source anatomy, original/palette and four equipped objects.',[ROOT/'art/village/sources.json'],[NPC/'source-packet.json'],'Retain actual item slots, both paired Feet groups and natural Icy Vapor distinction. No profession costume or unexported item inferred.')
event(npc,npc['required_steps'][1],'Verify four current fitting models and identify missing source-bound BODY-YRAME prerequisite.',[NPC/'source-packet.json'],[HERE/'source-packet.json'],'Current fitting model hashes match. Named additional-leg art has no current registration, so the NPC assembly cannot receive generation-ready credit.')
npc.update(status='UNFINISHED',current_step=npc['required_steps'][1],known_issues=['Missing separately authored BODY-YRAME four-foot anatomy prerequisite; four-item assembly and native acceptance remain unfinished.'],advancement_blocker=dict(requirement='Source-bound four-foot named anatomy and actual four-item assembly',reason='BODY-YRAME has no current generation-ready registered model. Old three-foot proposals and unrefined four-foot patches do not satisfy this workflow.',classification='internal',resolution='Finish BODY-YRAME on the unchanged female base with separate added leg pair, then assemble current four actual fittings without duplicating Boots580 onto unequipped Feet298.',dependent='NPC-WARDEN-YRAME authoring and later integrated native acceptance'))
entry.update(status='IN PROGRESS',current_step=entry['required_steps'][2],known_issues=['Source, actual Feet297/298 managers, paired-feet definition and Core references resolved. Additional-leg construction, actual secondary/refinement calls, patches, registration and review remain unfinished.'])
event(entry,entry['required_steps'][0],'Resolve Yrame source description, original sprite, actual Feet groups and unmutated female prerequisite.',[ROOT/'art/village/sources.json',ROOT/'evidence/joppa-anatomy-study.json'],[HERE/'prepare-source.py',HERE/'source-packet.json',HERE/'source-reference-baseline.png'],'Two paired Feet groups and explicit hind/foreleg prose support four feet; source level6 is not appendage count. Actual slots and natural/equipped distinction retained.')
event(entry,entry['required_steps'][1],'Inspect actual Core female cardinal references as baseline rendering guidance.',[HERE/'source-packet.json'],[HERE/'source-reference-baseline.png'],'Actual south/east/north donor PNG hashes verified and views inspected. These provide human style/outline only. No whole-body equivalent, donor mechanics or speculative species change. Manual additional-leg design is next; the plate does not claim generated mutant art.')
ledger.update(active_entry=entry['id'],updated_at=now);assert sum(e['status']=='IN PROGRESS' for e in ledger['entries'])==1
write(ROOT/'evidence/conversion-ledger.json',ledger)
print('Recorded Yrame NPC preflight and missing body source/reference phases; BODY-YRAME is sole active entry.')
