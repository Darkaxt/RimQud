# Faithful Joppa art and body specification

Current status correction (2026-10-20): **Stage 3 is ACTIVE and every asset is
unfinished**, including previously selected Tam/Ctesiphus. The user explicitly
reset completion after identifying incomplete scenery and Yrame clothing/horns.
The [conversion ledger](conversion-ledger.md) enumerates all subjects and required
variants, with one active entry and a complete contemporaneous process log.
Earlier completion/reconciliation statements below are historical and withdrawn
as art acceptance. Native checks retain only their measured integration meaning.

Authority: already_authorized. The user requested a new tileset close to Qud's
original art, proper models for the village's races including male/female/child
variants, and a study of mutations/variable appendages against RimWorld clothing.
Earlier constraints remain: high contrast, Qud colors, recognizable item design,
one subject at a time using original sprite and description references.
Current art direction clarification: use an appropriate actual RimWorld animal
sprite as the proportion/viewpoint/outline/shading reference. Qud identity and
palette remain authoritative; Ctesiphus uses the small donor cat, not a panther.
The user resumed implementation after QA and confirmed this required input chain:
creature -> race -> race description + actual RimWorld reference + original Qud
model. References may come from installed vanilla, DLC or mods. Continue
without desktop takeover; pause only for a necessary desktop-only acceptance.
The four stages in [the integration specification](joppa-integration-spec.md) are
separately complete. This specification governs the newly requested outcome.

2026-10-20 authorized direction correction: explicit editable geometry is the
production source for creatures and apparel. ImageGen is optional for textures
or object concepts, not the creature construction engine. Leave the accepted
ray cat unchanged. The current Stage 3 sample is Tam: reconstruct one adult
dromad from native race description and original sprite, using donor references
for presentation. Deliver separate body (including limbs/hump), head/long-neck,
fitted equipped Cloth Robe and held Shillelagh graphics in south/east/north views;
west mirrors east. This does not create standard arm/leg render nodes. Record
authored interpretation where the tiny original does not settle anatomy.
Acceptance for this sample is the real layered Tam inside native Joppa, correct
direction/contact and actual equip/unequip, supported palette, native look and
save/load, with one focused hidden integration run. No per-asset full regression.
This sample does not close Stage 3 or remove its remaining village requirements.

Latest user correction (2026-10-20): the current authoring phase produces the
unclothed adult dromad first. Do not use the user's clothed refinement image as
input. A constructed unclothed model may undergo ImageGen refinement, keeping
the source anatomy, views and registration as constraints. Subsequent clothing
is one item at a time: overlay on the refined unclothed reference, refine, and
retrieve a separate garment. Preserve explicit body/garment coverage masks and
check extraction; a flattened generated composite does not automatically supply
independent layers. Existing clothed Tam native evidence is a retained earlier
diagnostic, not acceptance of this revised authoring process. Stop clothing
authoring while the unclothed model is being established. All remains within
the single ACTIVE Stage 3; its full village criteria remain unchanged.

The user's subsequent authoring sequence supersedes constructing all three views
independently: establish the front design, supply that front to ImageGen for side
and back proposals, inspect and patch anatomical/perspective errors, then refine
the composed three-orientation sheet. Labels belong under the views. Race facts
remain binding: elongated camel muzzle, long neck/dulla and upper-back hump.
Do not turn the hump into a tail or medallion, or bare feet into shoes. Inspect
the source shapes before regeneration; no repeated native tests for these art
drafts. The final selected sheet must be registered and split into separate
body/head components before it can qualify as integrated race art.

Current authoring checkpoint: the user selected the front-derived, refined
unclothed turnaround on 2026-10-20 ("I love the result"). The selected image,
exact input/prompts and limits are retained under art/dromad/nude. Native source
identity is resolved; interpretation of unseen surfaces remains explicit.
Refined view registration, body/head segmentation and garment extraction were
subsequently verified through the separate selected-base native run below.
The earlier vector-only run remains historical evidence for its own model.
Stage 3 remains ACTIVE. No tracked deferrals; other village requirements remain.

2026-10-20 priority clarification: the reusable procedure retains available Qud
body/mutation metadata, while mutation-specific visual representation and garment
adaptation are user-postponed. Ordinary race bodies, consistent views, layer
separation and actual equipment are the current priority. Unsupported mutated
shapes retain native graphics. This does not claim the broader named-anatomy
requirements have been authored or verified, and does not close Stage 3.

## Requirements

2026-10-20 ledger execution objective: complete all enumerated entries one at a
time. The HTML conversion report must show contemporaneous evidence for original
shape, metadata, actual Core/DLC/mod rendering reference, constructed suggestion,
refined front, secondary views, consequential patches, composed refinement,
layer/mask extraction, and actual separate clothing integration where applicable.
Furniture, plants, machinery and props follow the same source-first procedure;
omit extra views only with a shape/state-specific reason. Environmental materials
must preserve Qud's original palette and design: the path should read as
stone/cobblestone-like paving integrated over grass, not the previous sandy road.
Keep rejected outputs and uncertainty visible. Start with the shared human male
base; do not start another ledger entry until its complete workflow is accepted.

Subsequent user correction: generation takes priority across the entire pending
ledger. Complete an entry's authoring workflow before moving to the next generation
entry; native validation must wait until all pending textures, objects,
creatures/NPCs and required clothing/equipment are generation-ready. Visual
inspection and correction remain authoring work. Do not launch per-entry native
tests or debug their harness during generation. Generation readiness and native
acceptance remain distinct; A5 stays required for final Stage 3 closure after the
complete generated set is assembled. This sequencing supersedes the earlier
per-sample native checkpoints for the current conversion pass.

Human variant request: retain the selected human turnaround as the common visual
family for adult male/female, child male/female and older male/female templates.
Children are featureless mannequins, not detailed anatomy studies. Keep removable
clothing separate for every age; the earlier blanket fully-clothed authoring
constraint is withdrawn by the user's clarification. Child male/female variants
may share body geometry when references do not support meaningful differences.
These are authoring variants, not permission to infer or change villagers' ages.

Latest creature workflow rule: first create the reusable unmutated race body;
derive ordinary age/sex variants from it. Individual mutation-granted limbs,
heads, tails and similar changes belong to a separate mutation framework and
must not be baked into a named NPC's baseline body. Preserve their exact native
metadata. Intrinsic species anatomy remains in the race base. This supersedes
the earlier fixed Irudad/Nima/Yrame body-authoring approach. Mutation appearance
and its clothing fit remain explicit unfinished requirements; this generation
pass does not implement that framework or claim those NPC assemblies complete.

2026-10-20 unattended continuation: the user requested finishing the conversion
of the starting village's NPCs/creatures and bringing environment textures/tiles
as close as possible to Qud's original look, palette and design. Reuse the same
source-first workflow for scenery: object identity -> native description, tile,
palette and connectivity/state metadata -> rendering reference -> editable
construction -> optional refinement -> registered layers/neighbor variants ->
native batch review. Continue within ACTIVE Stage 3, hidden command-driven tests
only, with source/art/evidence synchronization. The dromad's held staff needs a
larger visual proportion. Preserve the accepted ray cat.

For the known village cast, fixed authored variants may represent their captured
named anatomy (Irudad's hands-face/tail, Nima's arms/spiral stinger, Yrame's four
feet and equipped horns). This serves existing A4 rather than implementing a
general mutation resolver. Unknown changed topology retains native art. Personal
cosmetic customization remains outside this first conversion; no profession pose
is baked into a shared human body. Age/sex templates do not change demographics.

- A1: Inventory actual Joppa art targets and inhabitants from the installed,
  hash-pinned Qud definitions and retained generated-game evidence. Separate
  mechanical body slots, visible anatomy, gender and age. Do not infer species
  or anatomy from a humanoid equipment layout. Identify random builders and
  mutations which make a static blueprint insufficient.
- A2: Study actual donor body-type, age and apparel graphic selection alongside
  Qud equipment/body mutation semantics. Record specific limitations and a bounded
  recommended approach for multiple limbs/heads, tails, horns, wings, missing
  limbs and layered garments. This requirement is a study; it does not authorize
  replacing Qud's equipment rules or implementing arbitrary mutation rendering.
- A3: Create an original, consistent Joppa tileset for the selected visible art
  targets, with per-subject references, prompts, output provenance and a coverage
  ledger. Preserve characteristic shapes and palette roles. Internal widgets
  without independent visible art are documented exclusions, not missing sprites.
  Work one subject at a time. Generated concepts are not installed game results.
- A4: Create layered 2D body models for the village's confirmed visual families,
  including supported adult and child body/head variants where applicable.
  Body/head selection follows actual species, body-type, head-type and life-stage
  rules; humanlike clothing/equipment remains separate. Occupation and prose
  posture do not define a body sprite. Hair, eyes, beards and personal overlays
  are explicitly postponed by the user beyond this initial conversion scope.
  Necessary species/mutation anatomy must remain represented using a supported
  body graphic or addon arrangement, without assuming separate limb nodes. New age/sex
  templates are authored variants, not evidence that the village contains those
  ages or permission to change NPC demographics. Child bodies are featureless
  mannequins with separate removable clothing, following the clarification above.
  Preserve all visible appendages; unknown runtime shapes retain native graphics.
- A5: Integrate the new art through the existing native rendering path. Respect
  direction, contact pivots, layer order, native visibility, palette/tint and
  actual equipment. Verify normal-scale native captures, relevant state changes,
  hurt, native look and save/load. Retain explicit native fallback for unconverted
  or unsupported states. No new general renderer or donor simulation.
- A6: Preserve user profiles/processes, use hidden command-driven testing and
  owned E-drive scratch, clean expendable output, maintain public source/docs/
  contextual evidence and verified commits/synchronization. Raw game resources
  and decompilation remain local. No external mod release is authorized.

## Stages

Exactly one stage may be ACTIVE. No stage is complete on concept art alone when
its acceptance requires native integration.

| Stage | Status | Requirements | Acceptance |
| --- | --- | --- | --- |
| 1. Native body and clothing study | COMPLETE | A1, A2, A6 | Source-bound inventory covers observed inhabitants and selected art targets; gender/age uncertainty and runtime anatomy changes are explicit; mutation/clothing findings and concrete art/body contracts are recorded and checked against installed sources. |
| 2. First faithful tile in native Joppa | COMPLETE | A3, A5, A6 | One referenced subject is generated, visually reviewed at intended scale, packaged, used in the actual native scene and verified with relevant direction/tint/lifecycle behavior. This establishes the art contract without broadening the renderer. |
| 3. Complete village tiles and bodies | ACTIVE | A3-A6 | Every selected visible target has completed faithful art or an explicitly justified non-art exclusion; required body-family age/sex variants and named anatomy are authored; the integrated native village and supported equipment/lifecycle states pass, and all source/assets/evidence are reconciled and synchronized. |

Stage 1 QA reconciliation: the source-bound inventory now includes installed
Biotech Baby/Child body types, alongside Core adult types and life-stage geometry.
The actual Humanlike render-tree definitions confirm separate body/head and
appearance/apparel roots, without standard arm/leg nodes. The source inventory
and required palette values were freshly regenerated and checked. The study now
records the user's template/clothing/overlay split and distinguishes the current
Qud-side adapter from execution of the donor pawn rendering/animation pipeline.
A1/A2/A6 study acceptance is reconciled; remaining blockers/deferrals: none.

Stage 2 reconciliation: Ctesiphus -> Ray Cat -> native race description,
actual three-view donor cat references and the original Qud sprite are frozen
in the packaged record. The generated views run in actual Qud. Native four-way
movement, uniform physical scale/contact, primary tint, visibility, hurt, look,
save/load, changed-detail fallback and late extra-foot fallback passed; see
[verified evidence](../evidence/faithful-cat-result.json). Generated pixels and
public native readbacks remain unchanged. The initial rectangular-cell squeeze
was rejected and corrected in the cell/world conversion. The neutral base has
no independent detail mask; its count-based body guard is not arbitrary topology
support. Those limits are explicit, without claiming the full donor render tree.
Owned isolated profiles were cleaned through the reviewed helper transaction;
source and private reproduction evidence remain preserved. Stage-closure design
review found no required refactor for this bounded tile. A3/A5/A6 acceptance for
this stage is satisfied; blockers/deferrals: none.

Stage 2 source, documentation and native evidence are synchronized at df768dd.
Stage 3 is ACTIVE: the user selected a deterministic adult dromad/Tam sample next;
the remaining human variants, other species and mutation arrangements remain required.
Remaining criteria are full selected art coverage, authored required body variants,
native batch visual/integration acceptance and final reconciliation. These are
internal advancement blockers while this stage is implemented. No tracked deferrals.
Per the user's efficiency correction, subsequent art-only replacements reuse
unchanged renderer behavior evidence. Generate one subject at a time, review
native visuals in batches by body family, and rerun behavior checks only when
relevant integration code changes. A3-A6 still require the complete village
coverage and native integration; there is no per-NPC full-regression gate.

Stage 3 selected Tam reconciliation (2026-10-20): the approved unclothed sheet is
registered at one physical pixel scale, with per-facing feet contacts and explicit
body/head/neck/dulla masks. The actual Cloth Robe was refined in context, returned
as a separate garment and registered without stretching its views. Recorded
alpha cutouts remove closed cuff strokes which crossed the unchanged hands.
Shillelagh uses the actual Right Hand (laterality 2); unsupported handedness or
equipment retains native graphics. Arms, hands and feet remain pixels in the
body texture, not articulated limb models. The renderer uses flat directional
layers; this sample does not claim drop-in donor PawnRenderTree compatibility.

[The selected-base native evidence](../evidence/dromad-refined-result.json)
verifies four-way facing, measured layer contact/scale, actual equip/unequip,
independent native palette roles, visibility, late equipment/topology fallback,
native look, hurt without simulation advance and save/load. Source RGB retention,
complete body/head mask coverage and alpha-only garment extraction were checked.
The hidden run exited successfully and restored Unity preferences; normal saves
and settings were unchanged. Full native frames and the public layer inspector
are separate evidence from the enlarged authoring preview.

This satisfies the bounded Tam sample's A3/A4/A5 acceptance. Stage 3 stays ACTIVE:
other selected village targets, required body-family age/sex variants and their
integrated batch acceptance remain internal advancement blockers. Their resolution
requires authoring and integrating those subjects; full-village completion cannot
be claimed until that work passes. No tracked deferrals. The extraction rule is
recorded in the repository conversion skill. Scope review found no need for a
new rig, general renderer or mutation-clothing framework for this sample.

Stage 3 current reconciliation (2026-10-20): the former full-village art
completion claim is withdrawn. The native batch measured rendering integration
for the historical candidates; it did not establish the agreed per-subject
construction, refinement, extraction, perspective, neutral palette or visual fit.

All 154 ledger entries start UNFINISHED, including Tam and Ctesiphus. Exactly one
entry may be IN PROGRESS. Every conversion must log its actual source inputs,
reference choice, prompts/tool settings, output hashes, corrections/rejections,
mask extraction, all-view visual review and applicable native evidence as those
steps occur. A passing batch cannot automatically complete other entries.
Stages 1/2 above are historical study/demonstration milestones, not completion
credit for the reset art entries. The subsequent ledger execution objective above
authorizes conversion and its HTML evidence report, one entry at a time.

A3/A4/A5 advancement blockers (internal):

| Blocker | Unmet requirement and reason | Resolution | Dependent acceptance |
| --- | --- | --- | --- |
| ART-01 | A3/A5: furniture, vegetation, machinery, surfaces and tiles are mostly traces/drafts; source-to-design/refinement and visual acceptance are missing. | Complete the logged workflow for every corresponding entry, including relevant states and connections. | Full tileset/environment acceptance. |
| ART-02 | A4/A5: no body receives reset completion credit; Yrame has patched anatomy without the completed composed refinement; Glowfish has baked colors instead of a neutral/masked base. | Complete and review each body/age entry through the agreed procedure. | NPC assemblies and their clothing fits. |
| ART-03 | A3/A4/A5: generic equipment shapes skipped per-body in-context refinement/extraction; Yrame chain mail/horns and Tam staff have known fit/proportion issues. | Complete each fitting individually, then its equipment aggregate and NPC assembly. | Dressed NPC/creature conversion. |
| ART-04 | A3/A6: earlier green checks measured native bindings, not art completion. | Keep historical evidence labelled; require each ledger step's contemporaneous log and verified outputs before completion. | Truthful final reconciliation. |

Stage 3 remains ACTIVE. These are implementable advancement blockers, not a parked
BLOCKED stage. No required work is moved to an unnamed future stage. The ledger
records exact remaining work; arbitrary mutation systems and personal cosmetics
retain their explicitly agreed separate scope. User profiles, historical native
evidence and prior assets remain preserved. Documentation/publication of the
ledger does not satisfy the unfinished conversion objective.

Human registration correction (2026-10-20): normalize the authored human facing
canvases to 512 × 1024 with common contact (256, 950), translating body/head/masks
together without resizing. Per-facing silhouette placement from ImageGen is not
a stable authoring anchor. Preserve old evidence; identify the current registered
version and show center/ground guides separately from production layers. Clothing
inherits the registered family frame. This is art generation/registration work;
native movement acceptance still waits for the all-conversions generation gate.

Child body entries follow the user's featureless-mannequin/separate-clothing
instruction: author and register body/head/palette first. Their existing linked
template-garment entries own actual garment identity, in-context refinement,
extraction and fitting; none of that work is removed or accepted by the body entry.
The earlier combined child-body registration step is named accordingly in the
enumerator. Age selection remains authored and must not alter resident demographics.
