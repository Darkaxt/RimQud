# Regional garment fitting and curved body visibility

Workflow version: **regional-curved-v1**, approved by the user on 2026-10-20.
This authoring recipe replaces generative garment re-isolation, baked limb
cutouts, whole-image-only fitting as a universal solution, and polygon cuff tops.
It does not require regenerating a usable source or deforming an already good fit.

## Inputs and identity

Resolve actual NPC/creature → unmutated race/body → description, original sprite,
runtime parts and actual equipped item. Read the item's own description, material,
palette, slot/laterality and silhouette. Select the proper registered age/sex/body
family and source-bound donor style reference; body shape is not a profession.
Keep mutation anatomy and outfit precedence explicit, separate from base art.

Lock the body, cardinal camera, physical scale, common canvas and contact. The
current examples use 512×1024 at contact (256,950); these are authoring coordinates,
not a universal native sprite size. West mirrors east only when permitted.

## Context refinement and full cloth preparation

1. Construct one actual garment and overlay it on the registered body. A red
   recoloring of the body may preserve its shading and outlines as a segmentation
   key; keep the untouched body as the authoritative anatomical source.
2. Provide that reference, garment construction and item description for an initial
   contextual refinement. Preserve the exact prompt, input/output and hashes.
   Treat generated body preservation as a proposal, never as registered truth.
   Before extraction, apply section 4's structural inspection to every facing.
   Check actual coverage and connected construction, including straps reaching
   over the full foot height/instep and joining their intended anchors. If the
   refined source is structurally unusable, reject it and reattempt contextual
   generation with explicit corrections; retain both attempts and the decision.
   Do not confuse this with a second call to isolate the item. Persistent failure
   returns to editable construction; extraction/fitting cannot conceal the defect.
3. Derive cloth from that same output programmatically. Do not make a second
   ImageGen call to isolate it: a new drawing changes cuffs, proportions and lines.
   Exclude mannequin RGB, backdrop and body contours from actual visible fabric.
4. Complete cloth concealed by the body **before fitting**. Keying cannot recover
   hidden material. Record authored continuation separately, using visible fabric
   and explicit garment-side envelopes. Inspect closed holes and exterior-connected
   notches. A real neckline remains an opening; a hand-shaped missing region used
   only for draw order does not belong in canonical cloth alpha.

Retain source, reconstructed regions and full transparent cloth. Do not hide a
poor source by showing only its final masked composition. Do not change source
drawings between technique comparisons. An accepted facing may retain its earlier
successful registration while other facings are improved from the same drawing.

## Controlled fitting

Map source garment landmarks to the fixed body's corresponding neckline,
shoulders, cuffs, waist and hem. Preserve already aligned parts and record the
frozen region. A whole-image scale/translation is a useful baseline, not a mandate.

- Three bands: upper region adjusts, middle connects continuously, lower region
  stays at its selected baseline. Use garment landmarks, not equal thirds of a
  mostly transparent canvas. In skirt/trouser classes the relevant regions differ.
- Nine cells: add left sleeve, torso and right sleeve control when shared width
  cannot fit both sleeves. Adjacent cells share boundary coordinates. Keep the
  minimum required freedom; do not invent a generalized mutation-clothing solver.
- Sample the intact source through one coordinate map using appropriate alpha
  handling. Retain full output cloth, frozen-region evidence and all control points.
  Do not cut the bitmap into independently rescaled tiles with disconnected seams.

Inspect exterior fit **and** cuff overlap. Restoring original arm pixels alone
does not establish garment coverage. Existing painted masks may be wrong targets:
distinguish true sleeve coverage from exposed-hand outlines before fitting to them.
Do not cover an entire hand merely to make an inherited coverage-map count zero.

## Body visibility with natural openings

Paint visibility on the fixed unclothed model for that garment class and facing:
T-shirt-like, trousers-like, skirt-like, robe-like, etc. This defines which original
body surfaces render above that item. Aprons, boots, hats, eyewear and gloves need
their own ownership; do not add sleeve machinery to an object without sleeves.

Represent an ordinary cuff as fabric wrapping around an arm: a smooth editable
Bezier cross-section aligned to the actual fitted sleeve opening. Keep continuous
tangents, complete forearm/hand ownership and intended shoulder coverage. Avoid
straight diagonal-plus-horizontal spurs, arbitrary circles or corner-rounding
that ignores the garment. Preserve the front cuff's intended visible ink rim.

Rasterize curves with supersampling/antialiasing. Do not blur body or cloth art to
hide fit errors. White selects original body above cloth, black selects none,
gray represents edge coverage. Clip by actual body alpha so painted regions
cannot invent anatomy. Retain full body, full cloth, semantic mask and any derived
overlay separately. Apply visibility only after complete fitting, with independent
body and equipment tint. Do not draw bare hands over gloves or another held item.

## One-entry evidence and advancement

Log the actual sequence on the currently active clothing entry: source identity,
metadata/reference/construct, contextual output, full cloth reconstruction, fit
controls, curved masks, painted body, full facings, mask-off/on, neutral and Qud
tints, and intended-size view. Reuse accepted generation inputs without inventing
a new ImageGen call. Record which facings or constraints needed no transformation.

Review once for consequential source/fit/palette/ownership errors and correct
them coherently. Do not create a per-edit game test cycle. Mark generation-ready
only when the entry's authoring requirements are satisfied; keep native acceptance
pending. Finish that entry before activating another. Workflow invalidation
preserves all history, removes readiness and requires a new per-entry process log.

## Worked adult dromad evidence

The exact current example is preserved under `art/conversion/fit-dromad-cloth-robe/`:

- `red-key-v1/`: actual contextual source and keying experiment.
- `regional-fit-v1/fit-regions.py`: source completion and three-band/nine-grid
  trials, with `source-packet.json` and per-method control coordinates/results.
- `curved-mask-v1/curve-cuffs.py`: smooth sleeve-opening mask trial, editable SVG
  curves, painted body and identical-cloth old/new comparisons.
- `late-mask-v3/assembly-east.png`: profile the user requested to keep unchanged.

These scripts are worked dromad-specific implementations, not generic launchers.
Their adult arm rectangles, row ranges and sampling windows must not be copied
blindly to other bodies. Reuse the sequence and math with each new registered
body's source packet. The HTML reports show the full input-to-output history;
earlier failed comparisons retain their correction and provenance notes.
