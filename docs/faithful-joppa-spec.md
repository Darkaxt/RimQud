# Faithful Joppa art and body specification

Authority: already_authorized. The user requested a new tileset close to Qud's
original art, proper models for the village's races including male/female/child
variants, and a study of mutations/variable appendages against RimWorld clothing.
Earlier constraints remain: high contrast, Qud colors, recognizable item design,
one subject at a time using original sprite and description references.
Current art direction clarification: use an appropriate actual RimWorld animal
sprite as the proportion/viewpoint/outline/shading reference. Qud identity and
palette remain authoritative; Ctesiphus uses the small donor cat, not a panther. Continue
without desktop takeover; pause only for a necessary desktop-only acceptance.
The four stages in [the integration specification](joppa-integration-spec.md) are
separately complete. This specification governs the newly requested outcome.

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
  including adult male, adult female and child templates where applicable.
  Named inhabitants retain their defining anatomy and identity. New age/sex
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
| 2. First faithful tile in native Joppa | BLOCKED | A3, A5, A6 | One referenced subject is generated, visually reviewed at intended scale, packaged, used in the actual native scene and verified with relevant direction/tint/lifecycle behavior. This establishes the art contract without broadening the renderer. |
| 3. Complete village tiles and bodies | NOT STARTED | A3-A6 | Every selected visible target has completed faithful art or an explicitly justified non-art exclusion; required body-family age/sex variants and named anatomy are authored; the integrated native village and supported equipment/lifecycle states pass, and all source/assets/evidence are reconciled and synchronized. |

Stage 1 reconciliation: [the installed-source inventory](../evidence/joppa-anatomy-study.json)
reconciles all 67 selected types and ten actor blueprints. Hash-pinned donor/
recipient definitions and private class inspections establish the documented
[body and clothing findings](joppa-bodies-and-mutations.md). Explicit checks
confirm species, named mutations, removed RandomTile behavior, absence of the
inspected actor age fields, donor body-type garment selection and Chimera
attachment topology. The contract separates native state from authored age/sex
variants; source evidence is not called a runtime mutation test. No implementation
of general mutation rendering is implied. A1/A2/A6 study acceptance passes.
Stage 1 remaining/blockers/deferrals: none. Source/evidence publication checks pass.

Stage 2 is BLOCKED and parked at the user's explicit request to pause once the
Ctesiphus model is finished, before discussion of the NPC conversion pipeline.
The [directional artwork](../art/ctesiphus/preview.html) and exact generation
prompts are saved. Actual RimWorld cat samples now guide shape and rendering
style; semantic identity comes from Qud lineage/description and the installed
palette, not interpretation of a tiny glyph. Ornate first drafts were rejected.

Blocked requirement: A5 / stage-2 actual native integration, pivots, physical
scale, independent detail color and lifecycle evidence remain unverified. This is
an external execution constraint: the user requested a pause before the next
integration step. Resume after the pipeline discussion and user continuation.
The artwork is not called an integrated tile. Stage 3 remains NOT STARTED; no
stage is ACTIVE during this requested pause. Tracked deferrals: none; unfinished
stage-2 acceptance remains with stage 2.
