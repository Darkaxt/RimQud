"""Enumerate the existing Joppa inventories; never infer art completion.

First run: --date YYYY-MM-DD. Subsequent --render preserves the audited record;
--check checks inventory coverage, rendering, one active entry and evidence gates.
This records work; it does not generate art, launch games or mark assets complete.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'evidence/conversion-ledger.json'
DOC=ROOT/'docs/conversion-ledger.md'
INPUTS=['art/village/sources.json','art/village/model.json','art/village/age-templates.json',
        'evidence/village-reference-index.json','evidence/joppa-creature-catalogue.json','probe/joppa-coverage.json']

def read(path):return json.loads((ROOT/path).read_text(encoding='utf-8'))
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def slug(s):return re.sub('[^A-Z0-9]+','-',s.upper()).strip('-')
def files(paths):
    return [dict(path=p,sha256=digest(ROOT/p)) for p in sorted(set(paths)) if (ROOT/p).is_file()]

def enumerate_entries():
    source=read(INPUTS[0]);model=read(INPUTS[1]);ages=read(INPUTS[2]);index=read(INPUTS[3]);baseline=read(INPUTS[5])
    refs={r['blueprint']:r for r in index['entries']};entries=[]
    def add(key,category,name,*,targets=(),links=(),variants=(),artifacts=(),issues=(),steps=None,metadata=None,disposition='Convert and review'):
        entry=dict(id=key,category=category,name=name,source_targets=list(targets),related_entries=list(links),
            required_variants=list(variants),disposition=disposition,status='UNFINISHED',current_step=None,
            required_steps=steps or ['source_identity_description_metadata','original_and_render_reference_decision','construct_shape',
                'create_required_views_states','correct_errors_and_refine','extract_register_palette_masks','visual_review_all_views_at_game_scale','native_review_applicable_states'],
            known_issues=list(issues),metadata=metadata or {},historical_artifacts=files(artifacts),process_log=[])
        entries.append(entry);return entry
    def layers(m):return [l['public_file'] for view in m['views'].values() for l in view if l.get('public_file')]
    def family(actor,native):
        f=model['actors'][actor]['family'];return 'human-'+native['gender'] if f=='human' else f
    equipment={}
    for f,items in model['equipment'].items():
        for k,item in items.items():equipment.setdefault(item['blueprint'],[]).append((f,k,item))
    for name,fittings in sorted(equipment.items()):
        links=['FIT-'+slug(f+'-'+k) for f,k,_ in fittings]
        add('ITEM-'+slug(name),'Equipment inventory',name,targets=[name],links=links,metadata=dict(original_reference=refs.get(name),
            actual_slots=sorted({i['slot'] for _,_,i in fittings})),issues=['Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion.'])
        entries[-1]['required_steps']=['resolve_item_identity_description_palette','verify_every_body_fitting_log','record_item_acceptance_from_all_fittings']
        for f,k,item in fittings:
            issue=['Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log.']
            if f=='dromad' and name=='Cloth Robe':issue=['Earlier isolated/refined robe and cuff masks exist; re-audit every view under the reset. No completion credit carried forward.']
            if name=='Horns':issue=['Known defect: the same frontal pair is drawn for every view; side attachment and overlap are wrong.']
            if name=='Chain Mail':issue=['Known defect: generic garment does not fit Yrame correctly.']
            if name=='Shillelagh':issue=['User reported staff too small. Later shaft enlargement has not been accepted as resolution; review proportions and grip in every view.']
            add('FIT-'+slug(f+'-'+k),'Body/equipment fittings',f+' / '+name+' / '+item['slot']+' / laterality '+str(item['laterality']),
                targets=[name],links=['ITEM-'+slug(name),'BODY-'+slug(f)],variants=['south','east','north','west mirror/handedness review'],
                artifacts=layers(item),issues=issue,metadata=dict(body_family=f,equipment_key=k,slot=item['slot'],laterality=item['laterality']),
                steps=['source_identity_description_slot_laterality','select_correct_body_and_references','construct_and_overlay_one_item',
                    'imagegen_refine_in_context_on_unchanged_body','retrieve_isolated_item_and_masks','recompose_check_cuffs_attachment_occlusion_all_views',
                    'review_game_scale_and_palette','native_equipment_state_review'])
    for f,body in sorted(model['bodies'].items()):
        folder=ROOT/'art/village/bodies'/f;extra=[p.relative_to(ROOT).as_posix() for p in folder.rglob('*') if p.is_file()]
        issues=['Existing art/registration and native checks are historical only; restart the logged workflow.']
        base={'irudad':'BODY-HUMAN-MALE-OLDER','nima':'BODY-HUMAN-FEMALE','yrame':'BODY-HUMAN-FEMALE'}.get(f)
        if base:issues+=['Latest user rule: reuse the unmutated human base; do not bake individual mutations into a new race body. Preserve mutation metadata for the separate framework. The named mutation assembly remains unfinished.']
        if f=='yrame':issues+=['ImageGen three-foot proposals were rejected; four-foot geometry was patched afterward without a completed composed refinement.']
        if f in ['human-male','human-female']:issues+=['Shared-human-base consistency must be reviewed across named human variants; independent turnarounds allowed unsupported proportion drift. The standard human shown in the gallery has tapered leg stubs without recognizable feet; construct and review feet and contact in every orientation.']
        if f=='irudad':issues+=['Native second arm pair/hands-face is supported, but the upright mannequin omits the described hunched back and elderly proportions. Reconstruct the elder silhouette from sprite plus full description.',
                                'Native description explicitly specifies a short barb-crowned tail and the blueprint includes Stinger. The displayed smooth curled tail does not clearly preserve the barbed tip; review against description in all views.',
                                'The initial constructed torso shared human geometry, but independently generated/registered turnarounds drifted in torso, leg and head proportions. Derive from the selected shared human base and record each source-supported age/anatomy change.']
        if f=='glowfish':issues+=['Known defect: magenta/cyan are baked into fixed-color pixels; palette-off is not neutral. Establish neutral base and separate Qud color masks.',
                                 'Existing east-guided turnaround is not evidence of the complete agreed front-first process.']
        if f=='ray-cat':extra+=['art/ctesiphus/preview.html','evidence/faithful-cat-result.json']
        if f=='dromad':extra+=['art/dromad/nude/refinement.json','art/dromad/layered/model.json','evidence/dromad-refined-result.json']
        add('BODY-'+slug(f),'Race/body templates',f,targets=sorted(a for a,r in model['actors'].items() if r['family']==f or r['family']=='human' and f.startswith('human-')),
            links=[base] if base else [],metadata=dict(unmutated_base_entry=base,mutation_rendering='Separate framework; no baked mutant baseline') if base else {},
            variants=['south/front','east/whole-body side','north/back','west mirror','neutral base and separate Qud tint/detail'],artifacts=layers(body)+extra,issues=issues,
            steps=['resolve_race_description_original_sprite_runtime_anatomy','select_actual_core_dlc_or_mod_reference','construct_front',
                'imagegen_side_back_from_front_and_race_facts','correct_anatomy_then_imagegen_refine_composed_views','register_required_layers_and_color_masks',
                'visual_review_anatomy_orientation_palette_all_views','native_body_review'])
    for race,body in sorted(ages['templates'].items()):
        key='BODY-'+slug(race+'-child');add(key,'Race/body templates',race+' child (featureless body with separate clothing)',
            variants=['male/female templates; shared geometry if no supported distinction','south/east/north','west mirror','separate removable clothing'],artifacts=layers(body),
            issues=['Constructed template only. No native age selector established; do not assign an age to residents by guesswork.'],
            steps=['resolve_age_evidence_and_render_reference','construct_featureless_front','generate_other_views','correct_and_refine_composite',
                'register_body_head_and_actual_clothing','visual_review_all_views','record_native_selection_policy_without_changing_demographics'])
        for component in sorted({l['component'] for v in body['views'].values() for l in v}-{'body','head'}):
            add('FIT-'+slug(race+'-child-template-'+component),'Template garments',race+' child / '+component,links=[key],
                artifacts=[l['public_file'] for v in body['views'].values() for l in v if l['component']==component],
                issues=['Unmapped template garment: no actual Qud item identity or native equipped-slot binding established.'])
    for gender in ['male','female']:
        add('BODY-HUMAN-'+gender.upper()+'-OLDER','Race/body templates','human '+gender+' older template',links=['BODY-HUMAN-'+gender.upper()],
            variants=['south/front','east/whole-body side','north/back','west mirror','separate body/head and clothing'],
            issues=['User-requested age variant of the selected shared human family. No native life-stage selector established; do not change NPC demographics.'],
            steps=['resolve_age_evidence_and_render_reference','construct_front_from_shared_human_base','refine_front','generate_other_views',
                   'patch_and_refine_composed_views','register_body_head_and_palette','visual_review_all_views','record_native_selection_policy_without_changing_demographics'])
    for actor in source['actors']:
        natives=sorted(actor['native_instances'],key=lambda n:n['instance'])
        for i,native in enumerate(natives,1):
            f=family(actor['creature'],native);links=['BODY-'+slug(f)]
            for part in native['parts']:
                it=part.get('equipped')
                if it:links.append('FIT-'+slug(f+'-'+re.sub('[^a-z0-9]+','-',it['blueprint'].lower()).strip('-')+'@'+part['type']+'@'+str(part['laterality'])))
            name='Irudad (ElderBob)' if actor['creature']=='ElderBob' else actor['creature']
            if len(natives)>1:name+=' / captured resident '+str(i)
            add('NPC-'+slug(actor['creature'])+('-'+str(i).zfill(2) if len(natives)>1 else ''),
                'Creatures' if actor['race'] in ['cat','catfish'] else 'NPC assemblies',name,targets=[actor['creature']],links=links,
                variants=['south','east','north','west','neutral/Qud palette','actual equipped outfit','native visible/hidden and supported state'],
                metadata=dict(species=actor['race'],captured_gender=native['gender'],captured_instance=native['instance'],
                    source_snapshot=source['runtime_catalogue_sha256'],race_description=actor['race_input'],original_tiles=actor['original_model_tiles'],
                    body_parts_source='art/village/sources.json',native_parts=native['parts']),
                issues=['Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward.'],
                steps=['resolve_individual_race_and_runtime_metadata','verify_body_and_every_equipped_item_dependencies','assemble_without_baking_equipment',
                    'review_anatomy_clothing_attachment_all_directions','review_neutral_and_qud_palette_at_game_scale','native_visibility_equipment_hurt_look_save_review'])
    groups={
        'Furniture':{'Alchemist Table','Argyve Multicabinet','Bed','Bedroll','Book Table','Canvas Folding Chair','Chair','Chest1','Dresser','Floor Cushion','Hammock','Joppa Bookshelf','Mannequin','Metal Workbench','Ornate Table','Table'},
        'Vegetation':{'Brinestalk','Dogthorn Tree','Starapple Tree','Starapple Tree Ripe','Watervine'},
        'Machinery/appliances':{'Broken Industrial Fan','Electric Generator','JoppaOven','Lathe','Loudspeaker','Millstone','Powerless Electrothing','Sewing Machine','Wooden Water Wheel','WoodenMechanicalTransmission'},
        'Terrain/structures':{'BrineBridge','BrinestalkFence','BrinestalkWall','BrinestalkWallWithGearbox','CanvasWall','DirtFloor','DirtPath','Door','Pond','RustedMetalWall'},
        'Signs/shrine':{'ArgyveSign','JoppaMillSign','JoppaNorthSign','JoppaReshephShrine','PepperSign2','TamSign'},
        'Containers':{'Canteen','Random Bottle','Vase','Wine Vase','Woven Basket'},
        'Other props/debris/light':{'Garbage','Painting','Scrap Electronics','Scrap Metal','Torchpost'}}
    for obj in source['scenery']:
        name=obj['blueprint'];category=next(g for g,names in groups.items() if name in names)
        variants=['fixed map view; source palette/coverage and native supported states']
        if name in model['scenery']['walls'] or name=='BrinestalkFence':
            variants=[dict(mask=i,neighbors=[d for bit,d in [(1,'N'),(2,'E'),(4,'S'),(8,'W')] if i&bit]) for i in range(16)]
        if name=='Door':variants=['closed','open; native panel position and occlusion']
        if name=='Pond':variants=['wading/shallow','swimming/deep','connected banks/edges','foreground over liquid']
        if name=='DirtPath':variants=['continuous interior','8-neighbor edge/corner blending']
        if category=='Machinery/appliances':variants+=['operational/motion states: native metadata study still required; do not invent animations']
        current=model['scenery']['entries'].get(name);art=layers(current) if current else []
        linked_files=model['scenery']['walls'].get(name,[])
        if name=='BrinestalkFence':linked_files=[model['scenery']['surfaces'][f] for f in ['fence.png','fence-detail.png']]
        art += [p.relative_to(ROOT).as_posix() for p in (ROOT/'art/village/scenery').glob('*.png') if 'village-'+p.name in linked_files]
        issue=['Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished.']
        if name=='DirtPath':issue+=['User requires the original stone/cobblestone-like path integrated over grass and original Qud palette; reject the historical sandy-road interpretation.']
        add('SCN-'+slug(name),category,name,targets=[name],variants=variants,artifacts=art,issues=issue,
            metadata=dict(description=obj.get('description'),render=obj.get('render'),original_reference=refs.get(name)),
            steps=['resolve_object_description_original_tile_palette_state','select_render_reference_or_document_no_equivalent','construct_faithful_shape',
                'create_required_state_neighbor_variants','refine_materials_and_form','extract_register_color_coverage','visual_review_identity_and_connections_at_game_scale','native_state_review'])
    surfaces=model['scenery']['surfaces']
    for file,subject in [('marsh.png','marsh/grass ground'),('soil.png','bare soil/interior ground'),('sand.png','path surface'),('water-shallow.png','shallow/wading water'),('water-deep.png','deep/swimming water')]:
        filename=surfaces[file];paths=[p.relative_to(ROOT).as_posix() for p in (ROOT/'art/village/scenery').glob('*.png') if 'village-'+p.name==filename]
        add('TILE-'+slug(file[:-4]),'Surface/grass tiles',subject,variants=['seamless material','native palette','edge/depth transitions where applicable'],artifacts=paths,
            issues=['Procedural draft material only; identity, texture scale and transitions must be reviewed through the complete workflow.'])
        if file=='sand.png':entries[-1]['known_issues']+=['Historical filename only: replace the sandy-road interpretation with Qud-colored stone/cobblestone-like paving over grass.']
    for i in [1,2,3]:
        name='Basic Grass '+str(i);add('TILE-GRASS-'+str(i),'Surface/grass tiles',name,targets=[name],
            artifacts=['art/village/scenery/basic-grass.png'] if i==1 else [],metadata=dict(original_reference=refs[name]),
            issues=['Grass 1 traced candidate only; Grass 2/3 have original references but no converted output. Validate variation and vegetation merging.'])
    for obj in baseline['entries']:
        if obj['baseline_selected']:continue
        add('SCOPE-'+slug(obj['blueprint']),'Baseline exclusion review',obj['blueprint'],targets=[obj['blueprint']],disposition='Audit exclusion; do not generate art for a truly invisible widget',
            metadata=dict(original_baseline_decision=obj,visibility_source='Resolved installed Render.Visible=false in retained baseline definitions',
                original_tile='terrain/sw_crack.bmp' if obj['blueprint']=='PondDown' else None),
            issues=['Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior.'],
            steps=['verify_blueprint_visibility_and_any_tile','record_justified_art_exclusion_or_add_conversion_target'])
    return sorted(entries,key=lambda e:(e['category'],e['name'],e['id']))

def validate(data,expected):
    rows=data['entries'];ids=[e['id'] for e in rows];assert len(ids)==len(set(ids)),'Duplicate entry IDs'
    assert set(ids)=={e['id'] for e in expected},'Inventory drift: enumerate and reconcile new/removed targets explicitly'
    index={e['id']:e for e in rows}
    for e in rows:
        fresh=next(x for x in expected if x['id']==e['id'])
        for key in ['category','name','source_targets','related_entries','required_variants','required_steps']:
            assert e[key]==fresh[key],(e['id'],'Inventory/workflow drift',key)
        assert set(e['related_entries'])<=set(ids),(e['id'],'Missing linked entry')
        assert e['status'] in ['UNFINISHED','IN PROGRESS','COMPLETE']
        for artifact in e['historical_artifacts']:assert digest(ROOT/artifact['path'])==artifact['sha256'],('Historical input changed',artifact)
        if e['status']=='COMPLETE':
            if e['category'] in ['Equipment inventory','NPC assemblies','Creatures']:
                assert all(index[k]['status']=='COMPLETE' for k in e['related_entries']),(e['id'],'Related body/fittings are unfinished')
            for step in e['required_steps']:
                passed=[l for l in e['process_log'] if l['step']==step and l.get('result')=='PASS']
                assert passed,(e['id'],'Missing logged acceptance for',step)
                for log in passed:
                    assert all(log.get(k) for k in ['timestamp','action','inputs','outputs','review']),log
                    for item in log['inputs']+log['outputs']:
                        p=(ROOT/item['path']).resolve();assert p.is_relative_to(ROOT) and digest(p)==item['sha256'],item
    active=[e['id'] for e in rows if e['status']=='IN PROGRESS']
    assert len(active)<=1 and data['active_entry']==(active[0] if active else None),'Only one active entry permitted'
    for e in rows:
        if e['status']=='IN PROGRESS':assert e['current_step'] in e['required_steps'],(e['id'],'Current step not recorded')
    assert all(digest(ROOT/p)==h for p,h in data['input_sha256'].items()),'Source inventory changed; explicitly reconcile the ledger before continuing'

def markdown(data):
    rows=data['entries'];counts=Counter(e['category'] for e in rows)
    out=['# Joppa conversion ledger','',f"Reset date: {data['reset_date']}. **Every entry is UNFINISHED at the reset.**",
        '','This ledger supersedes earlier art-completion claims. Native tests establish integration behavior only. Existing sprites, traced contours, generated sheets and previous selections are historical inputs; none receive completion credit.',
        '',f"{len(rows)} entries: 16 resident assemblies (10 blueprints), {counts['Race/body templates']} body/age templates, 20 actual equipment inventory/aggregate records, 33 body/equipment fittings, 2 child-template garments, 57 scenery types, 8 surface/grass targets and 8 exclusion reviews.",
        '', 'The 75 baseline blueprint types are all accounted for: 67 selected visible types plus eight exclusions to recheck. Connectivity masks are enumerated under their owning wall/fence entry, not hidden behind an atlas count. Counts overlap between subjects and fittings; they are not a completion percentage.',
        '', 'Equipment inventory rows identify the 20 unique items and aggregate their fitting records; they do not require generating a second generic outfit. The 33 fitting entries own actual body-specific construction/refinement/extraction. An item aggregate or NPC assembly cannot complete while its linked fittings/body remain unfinished.',
        '',f"Active entry: **{data['active_entry'] or 'none'}**. Overall art work: **unfinished**. Implementation Stage 3: **ACTIVE**.",
        '', '## One-entry execution rule','',
        '1. Select exactly one entry and record it as IN PROGRESS with its current step. Resolve its source identity, description, native metadata and actual reference decision first.',
        '2. Append the conversion process as it happens: timestamp, step, action, exact input hashes, prompt text/file and tool/settings when used, output hashes, corrections/rejections, and review result. Do not manufacture retrospective PASS events from file existence.',
        '3. Body authoring: front construction -> front-guided side/back -> anatomical fixes -> composed refinement -> registered body/head/color masks. Child models are featureless mannequins; removable clothing stays separate at every age. For each equipped piece: fit on the unchanged selected body -> in-context refinement -> isolated extraction -> recomposition/occlusion review in every view.',
        '4. Furniture/vegetation/machinery/tiles follow identity + description + original shape/palette + reference decision -> deliberate reconstruction -> relevant views/states -> refinement -> masks/registration -> visual and native review. A trace/upscale is an input, not the completed conversion.',
        '5. Review neutral/Qud palettes, actual game scale, anatomical count, whole-body orientation, clothing perspective, cuffs, attachment and depth order. Record failures and remedies on that entry. A native batch result never completes unreviewed art entries.',
        '6. Record generation-ready after every authoring step is finished, then close its active generation work and move to the next entry. Native validation waits until all pending conversions are generation-ready. Overall COMPLETE still requires every applicable final acceptance step and evidence; pending native acceptance remains explicit.',
        '', 'The JSON is the editable record; this Markdown is generated from it. `python tools/enumerate_conversion_ledger.py --render` preserves statuses/logs and updates this view. `--check` checks inventory coverage, links, one active entry and completion evidence. The script never generates art or promotes entries automatically.',
        '', 'Creature views/composed refinement and garment in-context refinement must follow the agreed ImageGen-assisted procedure. Record exact prompts and outputs. Deliberate construction remains the shape authority. Record a justified reference decision, including no close equivalent when applicable; installed DLC/mod references remain eligible. Reuse applicable unchanged renderer evidence rather than rerunning a full gameplay suite per entry.',
        '', '## Known defects retained in scope','',
        '- Yrame: patched four-foot body still needs the completed composed workflow; chain mail fit and side-view horn attachment/overlap are wrong.',
        '- Human bodies: the displayed standard human lacks recognizable feet; independently generated named variants also drifted from the shared human proportions.',
        '- Irudad: four arms/hands-face and a short barb-crowned tail are supported by native definitions. The draft misses his hunched, elderly silhouette and a clearly barbed tail tip; named anatomy must remain a documented variation of the shared human base.',
        '- Glowfish: fixed sprite has baked-in magenta/cyan; neutral-base and separate Qud masks remain unfinished.',
        '- Tam: staff proportions/grip require review; earlier body and robe selections are also unfinished under this explicit reset.',
        '- Furniture, vegetation, machines and most scenery are traced source silhouettes, not completed rebuilt/refined objects. Grass variation, continuous textures, banks, paths and linked surfaces need the same per-entry process.',
        '', '## Inventory','']
    def esc(s):return str(s).replace('|','/').replace('\n',' ')
    for category,count in counts.items():
        out += [f'### {category} ({count})','', '| Entry | Subject | Status | Linked entries | Known work remaining |','| --- | --- | --- | --- | --- |']
        for e in rows:
            if e['category']!=category:continue
            out.append('| '+ ' | '.join(map(esc,[e['id'],e['name'],e['status'],', '.join(e['related_entries']) or '-', ' '.join(e['known_issues'])]))+' |')
        out.append('')
    out+=['## Per-entry workflow and artifact index','', 'Each entry below lists all required steps and variants. Historical files are not new process-log entries.','']
    for e in rows:
        out += [f"### {e['id']}: {e['name']}",'',
                'Required steps: '+' -> '.join(e['required_steps'])+'.','',
                'Required views/states: '+('; '.join(json.dumps(v,ensure_ascii=False) if isinstance(v,dict) else v for v in e['required_variants']) or 'source/exclusion review')+'.','',
                'Historical artifacts: '+(', '.join(f"[{a['path']}](../{a['path']})" for a in e['historical_artifacts']) or 'none recorded')+'.','',
                'Current step: '+str(e['current_step'] or ('generation ready; final acceptance pending' if e.get('generation_ready') else 'not started'))+'. Process-log events: '+str(len(e['process_log']))+'.','']
        for log in e['process_log']:
            out += [f"- {log['timestamp']} / {log['step']} / {log.get('result','PENDING')}: {log['action']}",
                    '  Review: '+log.get('review','not recorded'),
                    '  Inputs: '+json.dumps(log.get('inputs',[]),ensure_ascii=False),
                    '  Outputs: '+json.dumps(log.get('outputs',[]),ensure_ascii=False),
                    '  Method/prompt/corrections: '+json.dumps({k:v for k,v in log.items() if k not in ['timestamp','step','result','action','review','inputs','outputs']},ensure_ascii=False),'']
    out+=['## Sources and exclusions','', '[Structured ledger](../evidence/conversion-ledger.json) contains per-entry native metadata, exact hashes, source targets and the log.',
          '', 'Sources: '+', '.join(f'[{p}](../{p})' for p in INPUTS)+'.', '',
          'Race description/body trees, equipped part/laterality and palette references are retained. Captured instance IDs/genders describe one source snapshot, not permanent demographics. Unknown age or mutation state is not guessed. Player anatomy and future random/mod inventory are outside the enumerated resident snapshot; they are not silently counted as converted. Any newly discovered visible target must be added explicitly.',
          '', 'All completion blockers remain internal, actionable unfinished art work: missing full construction/refinement, masks/fit and visual acceptance. No required art is deferred to an unnamed future stage. The active objective authorizes completing the entries one at a time with the [HTML evidence report](conversion-report.html), including Qud-colored stone-like paths integrated over grass.','']
    return '\n'.join(out)

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--date');ap.add_argument('--check',action='store_true');ap.add_argument('--render',action='store_true');a=ap.parse_args()
    expected=enumerate_entries()
    if not DATA.exists():
        if a.check or a.render:ap.error('Ledger does not exist; enumerate it first with --date YYYY-MM-DD')
        if not a.date:ap.error('--date YYYY-MM-DD is required for the explicit reset')
        data=dict(scope='All enumerated Joppa subjects and required fittings/variants; every entry reset unfinished by user instruction',reset_date=a.date,
            art_completion_claims_withdrawn=True,stage='Stage 3 ACTIVE',active_entry=None,
            input_sha256={p:digest(ROOT/p) for p in INPUTS},log_contract=dict(required=['timestamp','step','action','inputs','outputs','review','result'],
            additional_when_applicable=['exact prompt/file hash','tool/settings','anatomical corrections','rejected output and reason','alpha/extraction masks','native screenshot/phase identity'],
            file_record=dict(path='repository-relative evidence path',sha256='exact content hash')),entries=expected)
        DATA.write_bytes((json.dumps(data,indent=2,ensure_ascii=False)+'\n').encode())
    else:data=read('evidence/conversion-ledger.json')
    validate(data,expected);text=markdown(data)
    if a.check:assert DOC.read_text(encoding='utf-8')==text,'Markdown ledger is stale; run --render'
    else:DOC.write_bytes(text.encode())
    print(json.dumps(dict(entries=len(data['entries']),categories=dict(Counter(e['category'] for e in data['entries'])),
        statuses=dict(Counter(e['status'] for e in data['entries'])),active_entry=data['active_entry'],inventory_complete=True),indent=2))

if __name__=='__main__':main()
