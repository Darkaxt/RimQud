# Blender-to-2D objects and body-fit proxies

Workflow version: **blender-first-v1**, selected by the user on 2026-10-21 after
the Yrame horn trial. Prioritize quality silhouette, volume, attachment, coverage
and consistent views. RimWorld-style readability generally needs simple shading
and clear borders rather than complex texture. Native Qud identity, palette and
all existing fit/registration/review requirements remain authoritative.

## Scope and transition

Use Blender by default for new or revised weapons, tools, natural equipment such
as horns, garments/armor/footwear, furniture, machinery, props and other objects,
including vegetation. Ground/liquid/connected tiles may use an appropriate
map-plane mesh and material; do not invent a raised slab or unnecessary facings.
Bodies retain the front-guided ImageGen process. A body proxy is a fitting aid,
not permission to replace accepted 2D body art or create a new race design.

Finish the current generation, including confirmed serious defects, before the
full-set in-game test. Keep existing usable art provisional; do not invalidate or
rebuild every object solely because the default technique changed. After the
integrated test, prioritize further replacements by visible shape/fit problems at
actual play distance. This transition does not waive a known defect, missing
source step, required view/state, or final native acceptance.

## Construct and render

1. Resolve original Qud sprite, complete metadata, palette roles, actual equipment
   slot/laterality and the exact RimWorld reference. Source dimensions take
   precedence; distinguish authored hidden depth and attachment estimates.
2. Model the complete object in Blender, including hidden continuations. Preserve
   an editable `.blend` plus construction controls/script and Blender version.
   Use one physical size and source-bound proportions, including handedness,
   handle length, grips and supporting-hand span. Avoid elaborate textures ahead
   of a correct shape. Do not replace Blender with another custom rasterizer.
   Save models in the persistent project asset directory, not only temporary
   storage or a disposable cache. Index each version in the project's Blender
   shape ledger with `.blend`/controls/script hashes, body/source dependencies,
   camera/material settings, approval state and the exact version to resume.
   Keep previous versions and resume the latest usable model for corrections;
   do not restart modeling merely because the rendered texture was rejected.
3. For worn/attached equipment, create or reuse a recipient fit proxy bound to the
   accepted body model hash, age/body variant, landmarks and mutation anatomy.
   Match the custom silhouette jointly in all required views, common scale,
   pivot and foot contact. Include the relevant head/ears, arms/hands, hump,
   feet/instep/heel and other coverage surfaces. Unknown depth is authored.
   Reuse this proxy for subsequent complements on that exact body version;
   recheck it when the body changes. Child proxies remain featureless mannequins.
4. Fit the object to the proxy: straps wrap over the full instep and meet sole
   anchors; garments cover the intended shoulder/hump/limbs; roots emerge from
   the intended surface; grips contact the actual hand. Give the model enough
   overlap and thickness. An interior root point or intersection test alone does
   not prove that a root visually grows from the skull. Inspect the visible
   emergence, not just the hidden mesh intersection.
5. Render required views/states with fixed orthographic cameras and the established
   shallow map elevation. Use shared dimensions and calibrated image/world
   mapping; never independently resize facing bounds. Front/back and side views
   must come from actual model rotation, including near/far occlusion. Furniture
   requires south/east/north. West follows real symmetry/handedness. Additional
   three-quarter model screenshots are diagnostics, not replacement facings.
6. Keep full item-only transparent renders separate from proxy/depth/visibility
   passes and contextual proofs. Retain semantic tint/material masks independently
   from body ownership. Proxy pixels are never part of production body art.
   Recompose over the original 2D body; inspect any proxy/sprite mismatch,
   particularly ears, cuffs and foot height. Do not erase cloth to encode depth.

## Finish without losing the shape

Prefer simple Blender materials/toon shading, grooves and rendered contours
(for example Freestyle), then limited manual pixel work for edge cleanup,
black borders or a source-supported mark. Save direct renders before edits.
Make line weight readable at intended size. Lighting must not bake unrelated
colors into neutral equipment; retain Qud primary/detail tint ownership.

ImageGen may compare a restrained 2D texture/style treatment of those already
rendered views. Preserve exact inputs/prompt/output. Do not ask it to reconstruct
new side/back geometry or isolate the object in a second call. Run the mandatory
fresh structural review after each actual refinement, and have the main author
disposition its findings. Compare silhouette, roots/grips, overlap, thickness,
grooves and markings against direct renders at matched scale. A smoother drawing
is not automatically a better asset.

If refinement loses important details, changes geometry/registration or repaints
the recipient, retain the direct Blender-to-2D source and finish manually. Never
transfer refined body pixels. If the Blender source itself has structural faults,
fix the model; manual outlines or a prettier texture cannot approve that fault.
Skipping ImageGen needs a recorded selection reason, not an invented call/pass.

## Evidence and completion

Show actual images for: source/metadata/reference; editable model and fit proxy;
raw cardinal renders; contextual fit; outline/material finishing; any ImageGen
candidate; review, rejection/selection and resulting masks/assembly. Save hashes,
camera/scale parameters, model version, exact prompts and the chosen source in
the entry's lazy HTML report. Label a stage not performed rather than fabricating
an image. These are authoring checks. Native/game validation still waits for all
pending ledger entries to satisfy the full generation gate.
