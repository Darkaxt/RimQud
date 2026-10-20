---
name: qud-creature-conversion
description: Convert a Caves of Qud creature into a source-bound layered sprite through anatomy metadata, an unclothed front design, front-guided side/back generation and controlled refinement. Use for RimQud creature or NPC art authoring; not a renderer transplant or an automatic mod installer.
---

# Qud creature conversion

Create reusable race/body art, then fit actual equipped items separately. Resolve
identity and anatomy before interpreting the tiny sprite. Follow the project's
authoritative specification; this procedure does not authorize installations,
game launches, desktop takeover, publication or a change of project stage.

Current priority is ordinary race/body conversion. Retain available mutation
metadata, but mutation-specific visuals and clothing adaptations are postponed
by the user. Do not build a mutation renderer or block ordinary body authoring
on filling every mutation field. Preserve native art for unsupported shapes.

This is a repository-maintained skill source, not a globally installed skill.
The [conversion ledger](../../docs/conversion-ledger.md) governs current entry
status. All entries were explicitly reset unfinished on 2026-10-20, including
previously selected models. Work one entry at a time and append its actual
inputs/hashes, prompts, corrections, extraction and review evidence as performed.
Historical assets or a passing native batch never complete another entry.
**Generation first:** do not perform native or formal integration validation
until all pending textures, objects, creatures/NPCs and their required equipment
have completed the generation workflow. This applies to scenery as well as bodies.
Follow the gate in section 7; one completed asset is not permission to test it.
Resolve the repository root from this file, two directories above this folder.
Read [the metadata contract](references/metadata-packet.md) when preparing an
input packet and [the Tam example](references/tam-example.md) for the worked case
and evidence boundaries. Use existing exports rather than launching the game
again for already captured metadata.

## 1. Resolve NPC, race and body

Build this input chain:

**NPC/creature → exact blueprint and ancestry → species/race → native description
+ original sprite/palette + runtime body metadata + actual donor reference.**

- Prefer installed version-pinned definitions and the observed runtime object.
  Wiki data supplements them; record its revision/game version and conflicts.
- Keep mechanical body tree, description-based visible features, and authored
  interpretation distinct. A slot name or sprite blob is not proof of anatomy.
- Record attached part IDs/parents, type/variant, laterality, mutation manager,
  natural/default equipment and actually equipped items where available.
  Separate inventory from worn/held gear. Missing exports are unknown, not zero.
- Read the runtime topology after mutations/builders/dismemberment. A wiki limb
  list that excludes mutation-added parts is only a baseline.
- References may come from RimWorld Core, DLC or installed mods. Record the exact
  asset and its role: perspective, outline, shading or anatomical feature. A
  camel reference does not turn Qud camelfolk into an ordinary camel.

## 2. Establish one unclothed front design

Reconstruct the original silhouette using explicit editable geometry where
practical. Combine race description and anatomy with the sprite; do not merely
enlarge ambiguous pixels or invent a species from their appearance.

Create a neutral adult race/body template without clothing, held items or
occupation-specific posture. Keep distinguishing anatomy, palette roles and
compatible presentation. Personal cosmetics follow the project's current scope.
Children require the separate fully clothed authoring policy; this adult nude
reference step does not authorize unclothed child templates.

Treat the estimated shape as an interpretation until checked. Preserve the front
as the design anchor once selected. Avoid generating a new body per named farmer
when they share a race and body plan.

## 3. Propose side and back from that front

Supply ImageGen with the selected front and an explicit **race description and
anatomy summary**. Use the installed image-generation workflow. Request the same
creature at the same physical scale in front, right-facing side and back views.

Label views **FRONT / SOUTH**, **RIGHT SIDE / EAST**, **BACK / NORTH**, below the
shapes. Prefer labels supplied by the review layout; generated text is not a
reliable view identifier. State which full-body view each panel represents.

Check that the entire body turns: feet and limb overlap, muzzle projection,
front/back feature visibility and hump/tail attachment must agree. A front torso
with a sideways head is not a side model. Side/back are proposals for unseen
surfaces, not new canonical race facts.

## 4. Correct anatomy, then refine the composed views

Inspect once for the consequential errors: wrong species, appendage count,
attachment, front/back placement, side-leg orientation, clothing on a bare base,
or changed proportions. Correct the source geometry or make a focused image edit
using the appropriate image-editing workflow. Preserve the unchanged source.

Compose the corrected views and ask for restrained, consistent shading/outline
refinement while keeping anatomy, scale and pose. Do not try to correct a wrong
body by repeatedly asking for a prettier image. If the same invariant keeps
failing, return to the constructed geometry instead of extending a prompt loop.

Keep input/output hashes, exact prompts, selected output and superseded reasons.
Inspect alpha in the actual saved image or browser: RGB values in fully
transparent pixels can make a tool preview misleading. A selected refined sheet
is artwork, not proof of registered layers or native integration.

## 5. Register and split the selected base

Use shared feet-contact, scale and head/neck attachment landmarks across views.
Retain transparent margins; do not independently fit bounding boxes, since ears,
muzzles or humps would change apparent body scale. Respect Qud's rectangular
cells when converting image coordinates to physical render dimensions.

Separate body (including limbs and intrinsic body features) from head/neck, plus
any necessary explicit tint/detail masks. Map actual Qud parts to the existing
supported render contract. RimWorld's ordinary humanlike tree does not supply
standard independent arm/leg nodes; Qud slots are not render bones.

The constructed input masks do **not** automatically segment a refined image.
Re-establish the refined boundaries and registration. Preserve overlap pixels at
the neck seam so independent layers do not expose gaps. Record intentional
occlusion and per-facing layer order. Unsupported anatomy retains native art.

## 6. Fit one garment or held item at a time

Read the actual item's blueprint, description, sprite, palette, equipped part
and laterality. Start with one real equipped item, not a profession costume.

1. Overlay its constructed shape on the selected, registered unclothed body.
2. Refine that item in context, preserving body, camera and contact landmarks.
3. Retrieve an isolated transparent garment/item layer. A flattened dressed image
   does not contain automatically recoverable independent layers; use explicit
   coverage/occlusion masks and inspect the extraction.
4. Recompose over the unchanged body. Reject baked skin, missing fabric, seams,
   changed anatomy or incorrect perspective. A side garment must turn with the
   torso and accommodate actual humps, necks and additional limbs.

Inspect **ownership at every cut edge**, especially cuffs, necklines and limb
openings. A generated isolated garment can retain a hand/body outline or a
closed cuff oval that crosses the real hand when overlaid. Do not treat those
strokes as fabric merely because they are inside the extracted asset. Remove
foreign outlines with explicit, recorded alpha/coverage masks; preserve the
garment's intended outer edge and the unchanged underlying anatomy. Check both
the isolated shape and its recomposition at enlarged and intended game scale,
including side/back views. Keep the unmodified generation and mask provenance.

Apparel art must fit the supported body family. Do not claim donor clothing is
automatically deformed for every Qud mutation. Inventory items remain invisible
until equipped. Laterality controls held-item anchors rather than a universal
hand location.

## 7. Validate only after every pending conversion is generated

Finish generation across the entire requested ledger before beginning native
or formal integration validation. All pending textures/terrain tiles, furniture,
plants, machinery, other objects, creatures/NPC bodies and separate clothing or
equipment must have their required construction, refinement, views/states,
corrections and extraction recorded in the HTML evidence report. A justified
non-art exclusion needs its source-based explanation. A single generated body,
family or small sample does not satisfy this gate.

During generation, inspect the artwork to correct anatomy, perspective, palette,
cut edges and layer ownership; recompose layers and show intended-size previews.
These are authoring steps. Do not turn them into per-asset game launches,
native acceptance batches, simulation/save/load tests, performance tests or
test-harness debugging. Record discovered integration concerns and keep generating.

Record an entry as generation-ready when its authoring steps are finished, then
move to the next generation entry. Keep pending native acceptance explicit;
generation-ready does not mean validated, integrated or overall COMPLETE. Pending
native checks must not force a validation detour before the next generation entry.

Only once every pending conversion is generation-ready, assemble the full set
and run the applicable native facing, contact, visibility, equip/unequip, palette,
hurt, look and save/load checks through the authorized hidden diagnostic.
Reuse applicable renderer evidence and validate the integrated set rather than
rerunning the gameplay suite for every asset. Preserve profiles and user processes.
Keep generation evidence and final native evidence separately identified.

## Output

Deliver the source-bound metadata packet, selected references, editable front,
exact prompts and selected turnaround, registered body/head/tint layers, actual
separate equipment layers, and the contemporaneous HTML process report. Native
evidence belongs to the final validation phase after section 7's gate. Retain unresolved
requirements in the existing project ledger. Stop at the user's requested scope:
documenting this method does not itself authorize generating the next creature.
## Source-bound scenery adaptation

For furniture, plants and terrain, use object blueprint -> native description,
original tile and palette -> coverage/detail geometry -> optional material
refinement -> registered object or connected surface. A donor object is a visual
reference, not an excuse to replace an unfamiliar Qud machine with a generic bench.

Decode the installed shader's mask contract before tracing. In the audited Qud
build, Kobold dual-color output is
`A*((1-R)*foreground + R*detail) + (1-A)*background`: alpha is coverage, opaque
black is primary and opaque white is detail. Do not infer this from a raw mask
thumbnail or assume alpha is a detail channel. Keep source masks local; publish
source identity, hashes, editable conversion geometry and contextual native views.

Use world-continuous ground/water textures and neighbor-mask walls where the
source requires connectivity. Keep liquid depth, open doors and visibility under
native state ownership. Review seamless material scale in the complete village,
not only enlarged isolated tiles. Native glyphs and dynamically painted tile
variants need explicit provenance; they are not automatically non-art exclusions.

For fixed named anatomy, verify appendage count across every view. Two generated
Yrame proposals still had three feet after correction prompts; explicit four-foot
geometry replaced that region. Retain rejected proposals and state why they failed.
This is a fixed authored variant, not a general mutation or clothing resolver.
