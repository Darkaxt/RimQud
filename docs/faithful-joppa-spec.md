# Faithful Joppa art and body specification

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
Refined view registration, body/head segmentation and garment extraction are
internal advancement blockers, not verified by the earlier clothed Tam run.
Stage 3 remains ACTIVE. No tracked deferrals; other village requirements remain.

2026-10-20 priority clarification: the reusable procedure retains available Qud
body/mutation metadata, while mutation-specific visual representation and garment
adaptation are user-postponed. Ordinary race bodies, consistent views, layer
separation and actual equipment are the current priority. Unsupported mutated
shapes retain native graphics. This does not claim the broader named-anatomy
requirements have been authored or verified, and does not close Stage 3.

## Requirements

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
  ages or permission to change NPC demographics. Children are fully clothed.
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
