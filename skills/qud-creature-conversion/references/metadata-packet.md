# Metadata to carry into each conversion

Capture available facts, their source and the distinction between static
blueprint defaults and an observed individual. Use null/unknown where the source
does not supply a value. Do not add a new runtime service merely to fill a packet.

| Group | Useful fields | Meaning and constraints |
| --- | --- | --- |
| Provenance | Game version; assembly/definition hashes; blueprint file; capture identifier; wiki URL/revision and declared game version | Bind metadata to a version and snapshot. Instance/part IDs are local to that game, not stable race identifiers. |
| Identity | Blueprint; inheritance chain; species tag/native species; display name; race and individual descriptions | Resolve an NPC to a reusable race/body family. Inherited descriptions can differ from old wiki text. |
| Body tree | Anatomy template; attached part IDs and parent IDs; type; variant; laterality; primary/preferred flags if exported; mutation manager; dependency/support relations where available | Preserve structure, not only counts. An extra arm attached to a head differs from an arm attached to a torso. Record the export's actual field coverage. |
| Missing parts | Dismembered parts, manager and regrowth state when exported | An attached-only tree does not prove no historical dismemberment. Unknown states remain unknown. |
| Mutations/builders | Resolved static declarations; runtime active mutation types/levels; body-altering builders | Mutation level is not appendage count. A runtime tree is required for actual added parts. Static absence is not proof of no runtime mutation. |
| Natural equipment | Default behavior blueprint and instantiated natural item, occupied part, mutation-granted equipment | Horns, stingers and similar features may occupy real slots. Do not treat them as ordinary inventory garments. |
| Equipped items | Actual blueprint/instance; equipped part ID/type/laterality; description; sprite; foreground/detail colors | Deduplicate items spanning parts. Inventory is a separate list; random starting gear is not a guaranteed outfit. |
| Weapon handedness | Inherited Physics.UsesTwoSlots; explicit UsesSlots; occupied parts for the same item; captured actor-specific GetSlotsRequiredFor result | Keep static and runtime requirements distinct; modifiers may change slot demand. A single exported Hand link does not establish one-handed grip. Unknown runtime demand stays unknown. |
| Weapon size and grips | Native dimensions/size fields when present; descriptive lengths; source proportions; actual donor graphic drawSize; authored canonical physical size, blade/head and handle measures; primary/supporting grip landmarks | Distinguish one-handed/two-handed size and grip classes at minimum. Weight/strength/class are context, not length. Use registered world mapping to retain the same item's size across bodies. Record authored estimates and exceptions; keep scale separate from pose/angle. |
| Demographics/size | Native gender resolution; explicit age/life-stage/size fields and their source, if present | Do not infer age from missing fields, height from weight, or visual dimorphism from a gender string. Demographic changes are not art work. |
| Original appearance | Tile and selected variant; atlas rectangle/hash; render string/layer; palette codes and RGB roles; flip/detail properties when available | A dual-color mask is not a normal illustration. Preserve palette roles and distinguish creature tint from equipment tint. |
| Description anatomy | Muzzle, neck, hump, dulla, horns, tail, wings, etc., with source description | Some visible features have no dedicated body part. No mechanical Neck/Hump/Dulla node is required for their art. |
| Donor reference | Exact Core/DLC/mod asset, version/hash, direction and role | Visual convention or anatomical reference is not copied game logic. Note when a reference is an inventory icon instead of a pawn graphic. |
| Blender object and fit proxy | Editable model/script/version; source controls; body-model hash and custom proxy; physical units; cameras; silhouettes/landmarks in all required views; raw/full/visibility/material passes; manual finish; optional AI candidate and actual selection | Blender-first for new/revised non-body assets; bodies remain ImageGen-led. Keep original body authoritative, full item intact and Qud tint separate. Preserve usable existing art provisionally until full-generation integrated testing; no blanket reset. |
| Furniture proportions and camera | Actual directional textures and transparent margins; GraphicClass; drawSize; footprint/size; per-facing render mapping; source-supported or authored width/depth; camera elevation; relevant component thickness; apparatus volume and occlusion | Carry the same dimensions into construction and the exact refinement prompt, with provenance or an authored-estimate label. Compare views in one physical frame before refinement. An upright Qud icon does not establish hidden depth; a cardinal map view is not automatically an edge-on elevation. Correct shared geometry when profile compression is unsupported. No universal end/front width ratio, independent side-panel compression or imported donor footprint. |
| Authoring map | Proposed physical body; uncertainty; body/head/addon mapping; contact/seam landmarks; coverage masks; per-view layering | This is authored interpretation, not native metadata. A render layer is not an equipment slot or an articulated bone. |
| Per-view item fit contract | Body/item hashes and frame/scale; anatomical surface or coverage boundary; root/contact/grip extent; exit direction; visible/hidden regions and depth; body/item feature ownership; west policy; source facts versus estimates; manual/refined comparison and evidence image per facing | Record before construction/refinement using prose, annotated art or equivalently labeled controls. Each view must depict the same attachment. Coordinate-inside-alpha alone does not prove a connected visible root. Record failures and required corrections before extraction; material refinement cannot waive structural failure. |
| Apparel occlusion | Workflow version; full contextual material/construction provenance; explicit hidden-fabric completion; per-facing fit/frozen-region controls; editable natural cuff curves and body-over-clothing mask; shared body/frame hashes; body versus equipment tint; actual layer precedence and equipped-item binding | Follow regional-curved-v1. Keep continuous cloth separate from the final visibility mask and derived overlay. Do not regenerate an isolated garment, bake limb-shaped holes into cloth, or redraw bare body above other worn gear. |

## Source hierarchy and conflicts

Record the selected visual body family separately from the mechanical anatomy
template, with original-sprite evidence and the reason that family applies.
Human/Humanoid presentation applies to confirmed human-based races, not every
creature with familiar slots. For a remodeled mutant, identify which ordinary
body regions are reused and which require separate replacement art; appendage
count alone does not establish torso shape or joint placement. Distinguish
source facts, visible silhouette interpretation and explicit user art direction.

Use runtime state for the observed actor, resolved installed definitions for
defaults, and version-labelled wiki facts as supplements. Keep disagreements
visible rather than silently replacing a live actor with a wiki template.

For example, one plural `Feet` part is not one physical foot. The humanoid
template's paired-feet interpretation is supported by its body plan and the
type's `Mobility=2`; it does not enumerate left/right Foot nodes. The quadruped
template separately lists four Foot parts plus dependent grouped-feet slots.
`Hands`, `Floating Nearby`, `Missile Weapon` and `Thrown Weapon` also do not each
represent an additional visible appendage.

## Reuse existing project exports

- [Observed resident catalogue](../../../evidence/joppa-creature-catalogue.json)
  records species, descriptions, normalized body variants, equipment and original
  model/donor-reference identities. It is an input study, not native art evidence.
- [Installed anatomy study](../../../evidence/joppa-anatomy-study.json) records
  definitions, palette, age/body types and rendering limitations.
- [Tam input example](../../../evidence/tam-conversion-input.json) retains a
  full observed part tree, natural/equipped items, static declarations, metadata
  gaps, wiki conflict notes and the distinction between mechanics and visible
  shape. Its runtime capture predates the selected artwork.

Those links are relative to this reference file within the repository. Keep raw
game assemblies, atlases and decompiled classes private; source metadata/hashes
and contextual captures are sufficient for the public procedure.
