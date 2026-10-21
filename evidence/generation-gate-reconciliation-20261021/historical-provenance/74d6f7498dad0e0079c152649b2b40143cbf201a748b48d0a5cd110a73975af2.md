---
name: qud-creature-conversion
description: Convert a Caves of Qud creature into a source-bound layered sprite through anatomy metadata, an unclothed front design, front-guided side/back generation and controlled refinement. Use for RimQud creature or NPC art authoring; not a renderer transplant or an automatic mod installer.
---

# Qud creature conversion

**First define the creature without mutations.** Create the reusable unmutated
race body before any named NPC's mutation-specific appearance. Derive ordinary
age/sex/body variants from that base, then fit actual equipped items separately.
Extra mutation-granted arms, feet, heads, tails and other appendages belong to
the separate mutation framework, not a one-off baked body for each NPC.
Resolve
identity and anatomy before interpreting the tiny sprite. Follow the project's
authoritative specification; this procedure does not authorize installations,
game launches, desktop takeover, publication or a change of project stage.

Current priority is ordinary race/body conversion. Retain mutation metadata and
its relationship to the baseline, but do not implement the mutation framework
during generation or block baseline art on that later work. Intrinsic species
anatomy is not removed as a mutation: a cat's normal tail and a dromad's long
neck/hump remain in their race base. Preserve native art for unsupported shapes.

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
- Resolve the unmutated race/body plan separately from the captured individual's
  mutation-altered tree. Do not make Irudad's extra arms/tail, Nima's extra arms
  or Yrame's extra feet the baseline for ordinary humans. Existing named-mutant
  drafts are historical inputs, not reusable race templates. Carry their exact
  mutation and attachment metadata forward to the separate framework.
- Record attached part IDs/parents, type/variant, laterality, mutation manager,
  natural/default equipment and actually equipped items where available.
  Separate inventory from worn/held gear. Missing exports are unknown, not zero.
- Read the runtime topology after mutations/builders/dismemberment. A wiki limb
  list that excludes mutation-added parts is only a baseline.
- References may come from RimWorld Core, DLC or installed mods. Record the exact
  asset and its role: perspective, outline, shading or anatomical feature. A
  camel reference does not turn Qud camelfolk into an ordinary camel.

## 2. Establish one unclothed front design

**Lock the camera before construction or refinement.** Use the actual selected
RimWorld reference's cardinal facing: south is straight front, north straight
back, east a complete right profile, and west the supported mirrored or authored
left profile. No three-quarter body, diagonal stance substituted for a facing,
isometric camera, or independently turned head over a frontal torso. Shading and
normal overlapping anatomy do not change the facing.

Apply this camera contract to furniture and props too. Align their footprint and
principal structural axes north/south or east/west. Use only the fixed, shallow
top visibility/depth established by the actual donor reference; do not invent
strong foreshortening, converging tabletop edges or a display-model camera. A
small shaded bevel is not itself a three-quarter view. A source Qud sprite may
be oblique: preserve its identity, materials, parts, patterns and palette, then
reconstruct those in the target cardinal view rather than tracing its camera.
Intrinsic diagonal parts, leaning books, bent limbs and hanging ropes remain
physical features; they do not authorize rotating the whole object.

Record the chosen facing and reference camera in the source packet and exact
generation prompt. Furniture always requires front/south, side/east and back/north
art, even when Qud currently binds one fixed tile. Other fixed scenery may use
one documented cardinal map view unless its source/state requires more. Authored
furniture views do not establish native four-way rotation or automatic placement.
Reject a mismatched camera during authoring, before registration or clothing
extraction. Record it as unresolved on the entry and withhold generation-ready
credit until corrected/reviewed. Preserve rejected art and previous process logs.

Reconstruct the original silhouette using explicit editable geometry where
practical. Combine race description and anatomy with the sprite; do not merely
enlarge ambiguous pixels or invent a species from their appearance.

Create a neutral adult race/body template without clothing, held items or
occupation-specific posture. Keep distinguishing anatomy, palette roles and
compatible presentation. Personal cosmetics follow the project's current scope.
Child templates use plain, featureless mannequins without detailed anatomy.
Keep their body/head separate from removable clothing just as for adult templates;
do not bake garments into the body. Male/female child labels do not require
inventing body-shape differences unsupported by the selected references.

Treat the estimated shape as an interpretation until checked. Preserve the front
as the design anchor once selected. Avoid generating a new body per named farmer
when they share a race and body plan.

## 3. Propose side and back from that front

Supply ImageGen with the selected front and an explicit **race description and
anatomy summary**. Use the installed image-generation workflow. Request the same
creature at the same physical scale in strict front, complete right profile and
straight back views, with the locked camera above. Labels alone do not establish
those orientations; the actual contours and anatomical overlap must agree.

Label views **FRONT / SOUTH**, **RIGHT SIDE / EAST**, **BACK / NORTH**, below the
shapes. Prefer labels supplied by the review layout; generated text is not a
reliable view identifier. State which full-body view each panel represents.

Check that the entire body turns: feet and limb overlap, muzzle projection,
front/back feature visibility and hump/tail attachment must agree. A front torso
with a sideways head is not a side model. Side/back are proposals for unseen
surfaces, not new canonical race facts.

For furniture, use the selected front construction plus the Qud description,
original sprite, material/part metadata and actual directional RimWorld reference
to generate a complete side and back. Preserve the same object, structural parts,
material regions, physical scale and consistent map-camera elevation; no oblique
turntable view or independently fitted bounds. Use a shared placement pivot and
a common canvas large enough for every facing, with transparent margins. Record
any mapping from that authoring frame to the current native cell explicitly.
West may mirror east only when geometry, markings and attachments permit it;
otherwise record the unresolved asymmetry and author a separate west view.

Review and patch the side/back construction, then refine the coherent composed
views without changing the selected front design. Show each view and its
neutral/tint masks in the report. Label unseen construction as authored where
source evidence is absent. Preserve required cosmetic/occupied/folded states
separately; do not invent native states. All three views are required for furniture
generation-readiness, not just the currently bound facing. Record the extra views
as unbound authoring assets. Whether wall/table context should select a facing
is a later integration decision, not permission to implement placement logic now.

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
Normalize every facing to the same horizontal canvas pivot and ground baseline
before calling the layers generation-ready. Current human canvases are 512 × 1024,
with contact at (256, 950). Translate body, head and masks together; keep render
offsets consistent with that normalized contact. Do not use ImageGen placement,
equal sheet columns or independently centered alpha bounds as registration.
An asymmetric side profile can extend forward while its foot/body anchor remains
fixed. Show center/ground guides in a separate report plate, never in production
textures. Clothing must inherit that body's canvas, scale and anchor.
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

Read the actual item's blueprint, description, original sprite/palette, equipped
part and laterality. Start with one real item, not a profession costume.

For garments, follow [the approved apparel-fitting recipe](references/apparel-fitting.md)
before constructing or extracting a replacement. Its production sequence is:
fixed race/body → one contextual refinement → continuous cloth source →
registered regional fitting where needed → curved body visibility →
independent body/equipment tint → authoring review in every required facing.

ImageGen may refine the item in context. Do not ask it for a second supposedly
exact garment isolation: that redraws proportions and loses registration.
Preserve original body pixels. Classify colored mannequin pixels as ownership
reference, explicitly complete occluded cloth before fitting, and retain full
cloth independently of a final body-over-clothing visibility mask. Neither
closed nor side-connected arm holes are canonical garment alpha.

Use the simplest fit that meets the actual garment/body landmarks: preserve
already good regions, try three bands for broad upper/middle/lower differences,
and use nine cells for independent sleeve/torso adjustment. Use shared boundaries
and one sampling pass; do not restart an unconstrained local mesh. The selected
adult dromad example uses nine-grid front/back cloth, natural curved cuff masks,
and its unchanged accepted profile. Its adult coordinates are not child, human,
boot or hat defaults. Adapt each garment class to its actual coverage.

Draw natural cuff openings as smooth editable curves, following cloth wrapping
around the arm, rather than polygon spurs. Retain complete exposed forearms/hands
and the original body contour. Antialias only geometric mask edges. Keep the
visible front cuff rim and shoulder coverage; no body/background-colored fill,
foreign body lines, limb-shaped destructive cutoffs or blurred artwork.

White mask means original body above garment, black means none, gray is edge
coverage. Body, garment and mask share frame, physical scale, pivot and facing.
Body overlay retains body tint; cloth retains equipment tint. Do not expose bare
hands above gloves or other worn/held gear. Record actual outfit precedence;
authoring masks do not prove support in an unnamed RimWorld mod or native runtime.

Retain exact prompts, output hashes, source completion, fit controls, masks,
mask-off/on and intended-size/palette plates on the one active ledger entry.
Compare techniques using identical generated material; disclose different inputs.
Existing failed drafts stay historical. Readiness invalidated by a workflow change
returns only after that particular entry has been processed and reviewed under
the new version. Native checks stay behind section 7's full-set generation gate.

Held tools/weapons retain their separate identity, directional art, attachment,
slot and laterality workflow. They do not gain sleeve masks or garment deformation.
Mutation overlays likewise remain separate from reusable unmutated body templates.

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
Apply section 2's camera contract before tracing scenery: source-camera fidelity
must not override the target cardinal presentation. Keep terrain in the map
plane, with continuous world scale; do not render a tilted material sample slab.

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

Do not repeat the earlier fixed-mutant-body approach. The historical Yrame
three-foot proposals and four-foot patch illustrate why baseline species art
and mutation assembly must remain separate. Retain rejected proposals as history;
generate the unmutated human race base and leave added feet to the mutation
framework, with their source metadata preserved.
