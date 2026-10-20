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
| Demographics/size | Native gender resolution; explicit age/life-stage/size fields and their source, if present | Do not infer age from missing fields, height from weight, or visual dimorphism from a gender string. Demographic changes are not art work. |
| Original appearance | Tile and selected variant; atlas rectangle/hash; render string/layer; palette codes and RGB roles; flip/detail properties when available | A dual-color mask is not a normal illustration. Preserve palette roles and distinguish creature tint from equipment tint. |
| Description anatomy | Muzzle, neck, hump, dulla, horns, tail, wings, etc., with source description | Some visible features have no dedicated body part. No mechanical Neck/Hump/Dulla node is required for their art. |
| Donor reference | Exact Core/DLC/mod asset, version/hash, direction and role | Visual convention or anatomical reference is not copied game logic. Note when a reference is an inventory icon instead of a pawn graphic. |
| Authoring map | Proposed physical body; uncertainty; body/head/addon mapping; contact/seam landmarks; coverage masks; per-view layering | This is authored interpretation, not native metadata. A render layer is not an equipment slot or an articulated bone. |
| Apparel occlusion | Workflow version; full contextual material/construction provenance; explicit hidden-fabric completion; per-facing fit/frozen-region controls; editable natural cuff curves and body-over-clothing mask; shared body/frame hashes; body versus equipment tint; actual layer precedence and equipped-item binding | Follow regional-curved-v1. Keep continuous cloth separate from the final visibility mask and derived overlay. Do not regenerate an isolated garment, bake limb-shaped holes into cloth, or redraw bare body above other worn gear. |

## Source hierarchy and conflicts

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
