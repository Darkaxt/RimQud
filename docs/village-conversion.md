# Source-bound Joppa conversion

**Status correction, 2026-10-20:** this document describes historical integration
drafts, not completed art. The user reset every subject to unfinished. See the
[conversion ledger](conversion-ledger.md) for the authoritative per-entry process
and outstanding work. Native rendering evidence does not accept the artwork.

This pass covers the captured starting village: **16 residents, 10 actor
blueprints and 57 selected environment types**. The player keeps native graphics.
It is a bounded Qud-side adapter using selected donor shaders and flat directional
layers, not transplantation of the complete RimWorld pawn tree.

## Coverage

| Native subject | Reusable body / specific treatment |
| --- | --- |
| Argyve, Mehmet, Joppa convert, seven watervine farmers | Shared male/female human templates; actual native gender, separately fitted equipped items |
| Irudad (`ElderBob`) | Four-arm body, hands-face and tail; ordinary head separate; actual robes, spectacles, walking stick and sandals |
| Nima Ruda | Four-arm body and coiled stinger; actual apron, hat, sandals, pestle and floating glowsphere |
| Warden Yrame | Explicit four-foot geometry; actual chain mail, horns, vibro blade and fore-pair boots |
| Tam | Selected dromad body/head/neck/dulla and extracted robe retained; staff enlarged about the same grip |
| Ctesiphus | Accepted ray-cat pixels retained unchanged |
| Glowfish | Catfish with native magenta/cyan palette, whiskers and four fins; three registered views |
| 54 isolated scenery types | Original coverage/detail converted to editable contours; linked walls/fence, door and bridge use connected geometry |
| DirtFloor, DirtPath, Pond | Continuous source-palette surfaces; native grass coverage and liquid depth |

[Source packets](../art/village/sources.json) retain native description, race,
original tile/color, actual equipment and runtime part tree. The
[reference index](../evidence/village-reference-index.json) records 90 resolved
private original references, including equipment and grass. Raw atlases,
assemblies, donor textures and decompilation remain private.

Male/female human bodies are shared templates, not occupation poses. Adult
dromads reuse the selected body across genders; no source establishes distinct
sexual morphology. Fully clothed human/dromad child templates have explicit
shorter-torso/larger-head proportions. They remain unbound authoring variants
because selected actors expose no established age selector. No demographics
were changed and animal juvenile forms were not invented.

## Procedure and interpretation

1. Resolve identity, race description, original sprite/palette, attached body
   topology and equipped items from pinned installed data.
2. Construct the unclothed adult front; supply race facts and actual donor
   presentation references for front-guided side/back proposals.
3. Correct consequential anatomy errors. Two Yrame proposals still had three
   feet; deterministic four-foot geometry replaced that region.
4. Register contact/neck/hand landmarks and split body/head. Limbs and intrinsic
   named features are body pixels, not new articulated render nodes.
5. Fit one actual item at a time as separate primary/detail geometry. Tam keeps
   the individually refined/extracted robe. Other items use explicit SVG.
   Garment edges exclude copied hands and closed cuff ovals. Back face-accessory
   views are empty.
6. For scenery, decode primary/detail coverage, trace editable contours, add
   restrained materials, register contact and use native neighbor/state data.
7. Review the assembled village and verify relevant state boundaries in a
   coherent native batch, rather than a full regression per asset.

The installed Kobold dual-color pixel shader was checked directly:
`A*((1-R)*foreground + R*detail) + (1-A)*background`. Alpha is coverage; opaque
black is primary and opaque white is detail. A raw mask thumbnail is not a
normal colored illustration. The extraction helper and skill record this rule.

Original shapes, palette roles and description facts are references; unseen
surfaces, neutral human proportions and fixed named-anatomy poses are authored
interpretations. Scenery stays close to Qud's glyph silhouettes; this first pass
does not claim the richness of a fully painted furniture set.

## Native evidence

[Verification](../evidence/village-result.json) binds tested source, packaged
contract and unchanged images. The batch rendered all residents and selected
environment types. It verified four facings, contact/scale, independent equipment
colors, real native Body-slot unequip/equip, hidden actors, late equipment and
unsupported-topology fallback, native look, one-HP hurt without simulation advance,
and equipment-preserving save/load.

Generated ponds are wading depth. One isolated pond was temporarily changed to
native swimming depth, rendered with the deep texture, then restored. Full-map
visibility uses Qud's diagnostic switch scoped to the batch. Facing fixtures
relocate residents to clear cells; they do not prove new locomotion animation.
Normal saves/settings were unchanged and Unity preferences restored.

The [gallery](../art/village/preview.html) separates enlarged assemblies from
unchanged native before/after frames. At 1280px it has five cast and eight scenery
columns; narrow screens use two and three. Controls remain keyboard accessible.
The model retains preparation-time status strings as a frozen native input;
current status is in the evidence, artwork manifest and specification ledger.

## Reproduction

Use the existing private task root with pinned source exports, selected generated
sheets and locally extracted donor resources. Its Python runtime needs Pillow,
UnityPy, resvg-py 0.5.0 and VTracer 0.6.15. Helpers in `tools/` take
`--root <owned-private-root>`:

- `prepare_village_conversion.py`: initial packets/fronts; do not reset selected
  briefs during a routine rebuild.
- `extract_village_references.py`: atlas rectangles and correct original masks.
- `register_village_bodies.py`: turnarounds and explicit masks.
- `build_village_equipment.py`, `build_village_scenery.py`,
  `build_village_age_templates.py`: registered separate art.
- `package_village.py`: native filenames and public layer provenance.

Run `probe/run_probe.ps1 -Root <owned-private-root> -Mode pawns
-IntegrationStage 4 -ArtSet village`, then `probe/verify_village.py --root
<owned-private-root> --output evidence/village-result.json`. The launcher refuses
an existing Qud process, uses a silent isolated batch profile and waits for exit.
A rebuild resets preparation statuses; evidence must match its exact contract.

Unknown anatomy, equipment, species, fixed-art palette or unsupported posture
retains native graphics. Generic mutation garments, personal overlays, arbitrary
mod conversion and a full donor render tree remain outside this pass.
