# Joppa integration completeness and art sequencing

The completed feasibility experiment proves that selected donor materials can
draw inside Qud and coexist with a bounded native gameplay workflow. It does not
establish a complete rendering integration or a finished Joppa overhaul.

The user's next concern is integration completeness before broad art production.
Faithful art is authorized if useful, subject to individual conversion using the
original sprite and available description, preserving the original design.
The user subsequently selected actual RimWorld human/animal graphics as temporary
NPC assets, including applicable hurt reactions, and requested a fourth step for
NPCs visibly wearing the Qud items they actually equip. This replaces faithful
custom NPC art as an immediate prerequisite; it remains the eventual art goal.
Integration comes first. No bulk image generation has started.

## Evidence from the existing implementation

[Coverage inventory](../evidence/joppa-coverage.json) reconciles the controlled
baseline's 2,000 cells with its instantiated and selected blueprint identities:

| Measure | Result | Meaning |
| --- | ---: | --- |
| Instantiated blueprint types | 75 | Includes widgets, landmarks and objects obscured by another selected object |
| Blueprint types selected for display | 67 | One controlled full-map snapshot, not all runtime appearances |
| Selected types receiving replacement rendering | 10 | Ground, path, brinestalk wall, door, water, crops/reeds and three tree types |
| Selected types keeping native rendering | 57 | Includes NPCs, furniture, machinery, canvas/rusted walls and fences |
| Replacement cells | 1,810 | Mostly repeated ground/path/vegetation; not 1,810 converted assets |
| Native fallback cells | 190 | Correct preservation, not completed replacement coverage |

The three tree blueprints share the generic donor plant path; mapped does not
mean individually faithful. The baseline includes eight farmers and named
residents, all still native. A generated game adds player and potentially other
appearances. Doors, lighting, crop states, colors and stacked objects can require
more than one appearance per blueprint. Consequently, 67 is not a final tileset
size, and 75 is not a promise that all those types need images.

Source boundaries inspected:

- `JoppaSimulation.Kind` recognizes a small explicit set. `Leave` records one
  selected object plus native appearance and a known liquid/painted-ground adapter.
  This is not a generic inventory of every drawable layer in a cell.
- `JoppaRenderer.Draw` chooses a soil/marsh underlay from the mapped kind, then
  draws selected terrain, wall, door or vegetation geometry. Adding an actor to
  that branch would not establish its real ground-under-object behavior.
- `Quad` has atlas selection, fixed geometry conventions and plant sway inputs;
  it has no authored actor/prop asset contract for pivots, footprints, appearance
  variants, transparent margins or overlapping foregrounds.
- The accepted buffer carries foreground/background/detail colors and flips,
  but most donor mappings use white or fixed material tints. Full preservation of
  native appearance states has not been demonstrated for replacement actors/props.
- Water uses a known-layer adapter, not RimWorld's complete water pipeline.
  Unknown late changes, unrelated views and unsupported content fall back to Qud.
- The actual native map camera/HUD/input, bounded save/load and menu restoration
  have positive evidence. Broad effects, remembered/unseen presentation and
  arbitrary content compatibility do not follow from those checks.

## Recommended next implementation outcome

Complete the rendering path needed for Joppa before producing its whole tileset.
There is no need to transplant every RimWorld rendering subsystem: Qud's own
simulation, field of view, interaction and HUD remain authoritative. Required
rendering behavior should determine which donor routines are reused.

The next implementation should demonstrate one cohesive scene containing temporary
RimWorld human/animal graphics, a prop and connected scenery through the actual
game camera:

1. Preserve the accepted-frame visibility and appearance contract while carrying
   the known visible ground and foreground needed for that scene. Do not rerun
   native rendering or reveal hidden object identities.
2. Load the selected transparent assets with explicit scale, pivot,
   footprint and appearance-state mapping. Preserve native ground under them,
   foreground ordering, actor movement, outlines/contrast and click coordinates.
3. Verify overlap near walls/plants, an appearance/state change, visibility,
   interaction, save/load and native fallback together. A standalone rendered
   sprite or a successful image-generation call is not this integrated result.

Use locally installed RimWorld humans and animals for the first NPCs, clearly
labeled as placeholders. Use original Qud references for any custom prop artwork.
The runtime mapping must allow later faithful art to replace the placeholder
graphics without changing Qud simulation or equipment semantics.

This is a recommendation for the next bounded implementation specification,
not a claim that those missing paths are already implemented. No new performance
gate is required: observe responsiveness during the relevant workflow and
investigate only a concrete defect or resource-growth symptom.

## Faithful art requirements retained from the user

For each displayed item/NPC and each required appearance variant:

- Identify the actual blueprint and resolved appearance; use original tile,
  native foreground/detail colors and available description as references.
- Generate one subject at a time. Preserve silhouette, species/body plan,
  clothing, equipment, recognizable details and palette roles. Do not replace
  Qud characters with generic RimWorld pawns or invent details absent from the
  references. Record uncertainty when the original is ambiguous.
- Keep a consistent viewpoint, lighting, contrast, asset footprint and pivot;
  retain genuine transparency. Review at the real gameplay size, beside its
  original reference, and inside Joppa.
- Track generated, visually reviewed and integrated status separately. Inventory
  observed Joppa content and its required states before claiming complete coverage.
  Keep unsupported content native until its replacement is actually verified.

Original reference assets remain local. Published contextual comparisons and
generated assets must retain provenance and third-party ownership notices.

The old feasibility stages remain complete under their original limited criteria.
This inventory identifies the next scope; it does not retroactively turn the
feasibility sample into a complete overhaul.


## Four-step integration sequence, revised by the user

The previous feasibility stages remain complete. The user has now authorized
execution. The [authoritative implementation specification](joppa-integration-spec.md)
owns current stage status and acceptance; the ordered scope below remains the
design rationale. Stages 1-3 are COMPLETE and stage 4 is NOT STARTED.

1. **COMPLETE — Layered NPC/prop scene.** Use actual locally extracted RimWorld
   human and animal graphics to demonstrate bodies, direction, transparency,
   scale/pivots, true ground underneath and overlap with Joppa scenery. Preserve
   native visibility and input coordinates. Custom faithful NPC generation is
   not a prerequisite.
2. **COMPLETE — Native state and reaction integration.** Bind hurt feedback
   to actual Qud damage; adapt applicable donor flash/offset behavior. Movement,
   facing and supported posture changes follow Qud state. Verify targeting,
   visibility, movement and save/load together. Keep Qud health, AI, jobs and
   turn progression authoritative. A matching texture alone is not animation.
3. **COMPLETE — Joppa coverage.** Expand verified mappings to observed Joppa
   NPCs/items and required states. NPCs may keep the approved donor placeholders.
   Custom Qud artwork remains an individual reference-based conversion process.
   Track mapped, visually reviewed and integrated coverage separately; unknown
   content stays native.
4. **NOT STARTED — Visible equipped items.** Map a bounded initial selection of
   Qud clothing/armor to existing RimWorld worn-apparel graphics. Read the items
   actually equipped and their body slots, not items merely carried in inventory.
   Compose body, head, clothing/armor and held-item layers in the correct visual
   order and facing, with body-type fit and relevant tinting. Verify equip,
   remove and swap, movement/turning, hurt reactions and save/load on NPCs without
   changing their gameplay equipment. Unsupported items/body plans retain explicit
   fallback; do not invent worn garments. Faithful Qud apparel art can replace the
   donor mappings later.

Step 4 is separately requested scope, not a deferral excusing an incomplete
prior step. Its supported-item selection and fallback must be explicit. It does
not promise automatic rendering of every item or arbitrary anatomy.

## Donor pawn/apparel audit

The installed hash-pinned RimWorld assembly was inspected directly. This is
source evidence, not executed NPC rendering; see
[audit metadata](../evidence/pawn-rendering-audit.json).

- `DamageFlasher` records health-harming damage, interpolates a material color
  and expires its flash after 16 donor simulation ticks.
- `Pawn_DrawTracker.Notify_DamageApplied` forwards to a jitter handler and pawn
  renderer. Images alone do not provide these reactions. The adapter must use
  Qud events and an appropriate visual lifetime, without a RimWorld tick manager.
- `PawnDownedWiggler` depends on donor downed/dead/awake state and ticks. Reuse only
  behavior with an explicit corresponding Qud state; injured, downed and dead
  are not interchangeable.
- `ApparelGraphicRecordGetter` selects a worn graphic, body-type suffix where
  applicable, directional `Graphic_Multi` and apparel draw color. Item/inventory
  icons are different assets from graphics rendered on a body.
- Apparel composition also uses body/head render-node ordering. Optional masked
  apparel can request a different shader. The six previously tested shaders do
  not establish complete pawn/apparel compatibility.

Decompiled donor source remains private and is removed after this inspection.
No pawn animation or equipped-apparel integration was implemented by this audit.
