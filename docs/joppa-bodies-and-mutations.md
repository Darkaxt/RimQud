# Joppa bodies, ages and mutation clothing study

This is an installed-source study, not new-model gameplay evidence. The
[reproducible inventory](../evidence/joppa-anatomy-study.json) reconciles all 67
selected baseline types and ten actor blueprints. It records installed assembly
and definition hashes. The existing generated-game evidence adds the player;
the player's body is not a new village race. Static definitions cannot replace
the runtime body tree after mutation, dismemberment, builders or regeneration.

## Inhabitants and necessary visual families

| Inhabitant | Installed species / anatomy | Defining visual requirements | Gender evidence |
| --- | --- | --- | --- |
| Argyve | human / Humanoid | Powdered mushroom-shaped beard, tinker's pockets and scrap | male tag |
| Mehmet | human / Humanoid | Bent farmer posture, turquoise eyes, work-worn hands | male tag |
| Watervine farmers | human / Humanoid | Kufiya, vinereaper; six RandomTile candidates | randomized male/female |
| Mechanimist convert | human / Humanoid | Resewn cowl, sack habit, copper-bound watervine | randomized male/female |
| Irudad (`ElderBob`) | human / HumanoidWithHandsFace | Hunched elder, second arm pair forming a hands-face, barbed tail | male tag |
| Nima Ruda | human / Humanoid plus mutations | Extra arms, great jeweled spiral tail/stinger, apothecary identity | female tag |
| Warden Yrame | human / Humanoid plus mutations | Hind/forelegs, great horn tines, rime-veined hands | female tag |
| Tam | dromad / Humanoid | Long camel-like neck, decorated dulla, ringed ears, hump | male tag |
| Ctesiphus | cat / Quadruped | Phosphorescent purple ray cat; native pale-gray detail role | male tag |
| Glowfish | catfish / Fish | Small luminous fish visible through water | neuterperson tag |

These establish four species families: human, dromad, cat and catfish. Mutated
humans remain human; Yrame is not declared a separate cervitaur race. Nima and
Irudad both declare MultipleArms, Stinger and Chimera. Yrame declares MultipleLegs,
Horns, FreezingRay and Regeneration. A Humanoid base does not mean ordinary limbs.
Mehmet removes the inherited RandomTile builder: the inventory checks that removal.

The selected actor definitions contain no explicit age field in the inspected
Age/LifeStage/Child/Juvenile keys. Descriptions identify Irudad as old and Nima
as late middle-aged; this does not establish a generic numerical age system or
prove that no children exist elsewhere. Child models will be authored templates,
not smaller substitutions for named adult residents. For human/dromad families,
author adult male, adult female and fully clothed child templates. For cats/fish,
male/female may share a silhouette where the references provide no dimorphism;
author a juvenile variant without inventing gender-specific anatomy. Preserve
native fixed/random gender independently of which art template is displayed.

## What the installed donor actually supplies

`BodyTypes.xml` defines Male, Female, Thin, Hulk and Fat adult shape families.
`LifeStages.xml` separately defines human baby, child, teenager and adult stages,
including child body/head factors. Child is not a sixth body-type suffix in that
file. Age needs an explicit render contract; shrinking an adult garment alone
does not establish correct child proportions or fit.

`RimWorld.ApparelGraphicRecordGetter.TryGetGraphicApparel` chooses a worn path
with a body-type suffix for ordinary garments, with exceptions for overhead,
eye-cover and packs. It loads directional `Graphic_Multi`, uses apparel draw
color, and can select CutoutComplex for masked graphics. `PawnRenderNode_Apparel`
consumes that graphic; body-apparel workers handle visibility, layer/offset and
pack adjustments. This is useful proven composition, but it does not synthesize
sleeves or deform clothing around arbitrary limb topology. Merely importing an
alien body or installing a race mod does not establish compatible garment art.
No workshop runtime was imported or enabled for this study.

## Qud mutation consequences

| Native case | Source behavior inspected | Consequence for presentation |
| --- | --- | --- |
| MultipleArms | Rank/Pairs and AddMoreArms create Arm/Hand and dependent Hands parts; mutation level changes attack chance | Level 10 is not ten extra arms. Read resulting parts and laterality; provide matching sleeves and held-item anchors. |
| MultipleLegs | AddMoreLegs adds/relateralizes Feet groups and requests re-equipping | Feet can represent a pair/group. Slot count is not a literal count of individual visible legs. |
| Chimera | Mutations.AddChimericBodyPart chooses a weighted part type and attachment point, adds usual child parts and changes laterality/names | Counts alone lose topology. An arm on a head differs from another arm at a shoulder. No finite atlas covers every combination. |
| TwoHeaded | Adds Head and Face parts with managed laterality | Hats/face gear bind to actual head slots, not one global hat layer. |
| Stinger | Adds/reuses a Tail and creates default/equipped mutation equipment | Tail art and native natural equipment must remain visible; it is not an inventory cloak. |
| Horns | Regrows mutation equipment on a native head slot | Respect Qud's actual occupied slot. Do not automatically draw an incompatible hat over horns. |
| Wings / Carapace | Native default-equipment mutations generate equipment and use the relevant body slot | Read actual natural/default equipment and native restrictions; a cape/torso texture is not automatically valid. |
| Dismemberment / regeneration | BodyPart has attached/dismembered state; mutation parts have managers | Rebuild appearance on actual topology changes. Suppress the missing limb and its gear; do not keep a baked complete body. |

The source inspection used the installed hash-pinned assemblies. Decompiled
classes remain private: MultipleArms, MultipleLegs, Chimera, Mutations, Anatomies,
Stinger, Horns, TwoHeaded, Wings, Carapace and BodyPart on the recipient; apparel
getter and body/apparel render-node workers on the donor. Source audit is not a
claim that all these variants have been exercised in the engine. The previous
Stage 4 verified an actual added arm falling back natively, not mutation rendering.

## Bounded approach for this village

Start with authored body templates for these known inhabitants and their actual
generated anatomy. Keep torso/head, appendages and removable equipment separate.
Use per-facing contact points and explicit front/behind order. Separate garment
torso panels from sleeves only for a real required multi-arm outfit; the first
case is Irudad or Nima, not a generic rig for hypothetical species.

Select supported topology from native part type, parent path, laterality,
attachment/missing state and default/equipped item identity. Deduplicate the same
item occupying several slots by instance identity, while allowing different copies
of the same item on different limbs. Aggregate Hands/Feet slots need authored
visual interpretation. A changed body must not keep a previously accepted outfit.
The current Stage 4 guard deliberately supports a much narrower body-count case;
it is not this future topology implementation.

For random mutations outside an authored supported arrangement, retain the native
actor and gear rather than silently dropping appendages. Broad procedural limb
assembly would be a separate implementation decision with a real case and its own
acceptance evidence. This study requires no new simulation, skinning framework,
runtime race provider or MCP server.

## Art contract and next acceptance

Work one subject per generation using its original sprite plus a short description
brief. Preserve silhouette, foreground/detail roles and strong contrast; avoid
brown color grading across the village. Use transparent directional sprites with
consistent canvas, feet/contact baseline and scale. Terrain/walls additionally
need repeatable surfaces and required neighbor/state variants. Keep source art,
generated concept, reviewed sprite and native integrated result separately labeled.

First prove one faithful subject through the existing native scene before
generating the remaining inventory. Review the result at normal game scale, with
native tint/visibility and relevant states, then reuse the established contract.
Do not equate a beautiful atlas or model sheet with a finished in-game tileset.

Palette correction: the installed Display.txt defines `m` as `#B154CF` and `y`
as `#B1C9C3`. These are actual palette values, not ANSI color-name assumptions.
The first blue-violet/gold-eye draft was corrected before native integration.
