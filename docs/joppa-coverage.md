# Joppa rendering coverage

Stage 3 reconciles all 67 selected baseline types. **26 receive temporary replacements; 41 keep native graphics.** This is a reviewed rendering contract, not a finished faithful tileset.

The eight unselected widget/landmark/hidden-terrain definitions remain native. The generated run observed 31 selected types, including one addition: the native humanoid player. Its mapping is limited to the current upright Humanoid player with known visible ground.

[Authoritative specification](joppa-integration-spec.md) · [runtime mapping contract](../probe/joppa-coverage.json) · [verified evidence](../evidence/joppa-stage3-result.json)

## Baseline decisions

| Blueprint | Presentation | Reason |
| --- | --- | --- |
| Alchemist Table | native fallback | Native chemistry glassware and scorched layout lack a matching donor prop. |
| Argyve | temporary replacement | Temporary donor human body/head; native Qud tint, identity and gameplay retained. Faithful individual design remains an art goal. |
| Argyve Multicabinet | native fallback | Preserve the native arrangement of assorted galvanized drawers. |
| ArgyveSign | native fallback | Authored Qud signage retains its native symbol, color and interaction. |
| Bed | temporary replacement | Reviewed temporary donor bed silhouette; native Qud tint and interaction retained. Not faithful finished artwork. |
| Bedroll | temporary replacement | Reviewed temporary donor bedroll silhouette; native Qud tint and interaction retained. Not faithful finished artwork. |
| Book Table | native fallback | Puzzle-box drawers are a different silhouette from the donor dining table. |
| BrineBridge | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| Brinestalk | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| BrinestalkFence | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| BrinestalkWall | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| BrinestalkWallWithGearbox | native fallback | Integrated mechanical attachment is outside the plain wall adapter. |
| Broken Industrial Fan | native fallback | Keep the specific industrial blade/ring silhouette. |
| Canteen | native fallback | Cloth-sheathed aluminum container has no reviewed donor counterpart. |
| Canvas Folding Chair | native fallback | The reviewed wooden dining chair does not depict folding canvas construction. |
| CanvasWall | native fallback | A hung canvas surface has no reviewed donor wall material. |
| Chair | temporary replacement | Reviewed temporary donor chair silhouette; native Qud tint and interaction retained. Not faithful finished artwork. |
| Chest1 | native fallback | A hinged wooden chest has no reviewed donor counterpart; do not substitute a crate or basket. |
| Ctesiphus | temporary replacement | Temporary directional donor cat for the native ray cat; preserve Qud tint. |
| DirtFloor | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| DirtPath | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| Dogthorn Tree | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| Door | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| Dresser | temporary replacement | Reviewed temporary donor dresser silhouette; native Qud tint and interaction retained. Not faithful finished artwork. |
| ElderBob | native fallback | Irudad has four arms, a hand-face and tail; the donor human body is unsuitable. |
| Electric Generator | native fallback | Preserve the handcrank rotor and its native installation silhouette. |
| Floor Cushion | native fallback | Keep the flat buttoned cushion rather than substituting a chair/stool. |
| Garbage | native fallback | Preserve Qud-specific fragments and their native pile silhouette. |
| Glowfish | native fallback | No reviewed donor fish graphic or native luminescence adapter. |
| Hammock | native fallback | No reviewed suspended rope-lattice counterpart. |
| Joppa Bookshelf | temporary replacement | Reviewed temporary donor bookcase silhouette; native Qud tint and interaction retained. Not faithful finished artwork. |
| JoppaFarmerConvert | temporary replacement | Temporary donor human body/head; native Qud tint, identity and gameplay retained. Faithful individual design remains an art goal. |
| JoppaMillSign | native fallback | Authored Qud signage retains its native symbol, color and interaction. |
| JoppaNorthSign | native fallback | Authored Qud signage retains its native symbol, color and interaction. |
| JoppaOven | native fallback | Visual review rejected the modern donor stovetop for the native clay oven; preserve its shape and fire. |
| JoppaReshephShrine | native fallback | Resheph imagery is specific to Qud and must remain recognizable. |
| Lathe | native fallback | A generic machining bench would lose the native lathe form. |
| Loudspeaker | native fallback | Preserve the native speaker and its distinct facing/state. |
| Mannequin | native fallback | An inert fiberglass/wood biped must not be treated as an animated NPC. |
| Mehmet | temporary replacement | Temporary donor human body/head; native Qud tint, identity and gameplay retained. Faithful individual design remains an art goal. |
| Metal Workbench | temporary replacement | Reviewed temporary donor workbench silhouette; native Qud tint and interaction retained. Not faithful finished artwork. |
| Millstone | native fallback | The native circular milling mechanism has no reviewed donor counterpart. |
| Nima Ruda | native fallback | Keep the prominent spiral tail and stinger absent from the donor human. |
| Ornate Table | native fallback | Chromium legs and marble top are not represented by the donor wood table. |
| Painting | native fallback | Preserve native artwork instead of substituting unrelated donor art. |
| PepperSign2 | native fallback | Authored Qud signage retains its native symbol, color and interaction. |
| Pond | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| Powerless Electrothing | native fallback | No reviewed counterpart for this specific ancient device. |
| Random Bottle | native fallback | Preserve the native bottle silhouette and its resolved contents/tint. |
| RustedMetalWall | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| Scrap Electronics | native fallback | Preserve native electronic scrap rather than a generic resource icon. |
| Scrap Metal | native fallback | Preserve native metal fragments rather than a generic resource icon. |
| Sewing Machine | temporary replacement | Reviewed temporary donor tailor silhouette; native Qud tint and interaction retained. Not faithful finished artwork. |
| Starapple Tree | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| Starapple Tree Ripe | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| Table | temporary replacement | Reviewed temporary donor table silhouette; native Qud tint and interaction retained. Not faithful finished artwork. |
| Tam | native fallback | The camelfolk humanoid is neither a donor human nor a donor quadruped camel. |
| TamSign | native fallback | Authored Qud signage retains its native symbol, color and interaction. |
| Torchpost | native fallback | Burning handfire and native light state need their existing presentation. |
| Vase | native fallback | Preserve the native container form rather than a donor plant pot. |
| Warden Yrame | native fallback | The horned body described in Qud is outside the reviewed human/cat anatomy. |
| Watervine | temporary replacement | Explicit known scenery adapter; native appearance, visibility and state gate replacement. |
| WatervineFarmerJoppa | temporary replacement | Temporary donor human body/head; native Qud tint, identity and gameplay retained. Faithful individual design remains an art goal. |
| Wine Vase | native fallback | Preserve the native liquid-container form and contents. |
| Wooden Water Wheel | native fallback | Native mechanical motion has no reviewed donor wheel counterpart. |
| WoodenMechanicalTransmission | native fallback | Native mechanical line/attachment rendering stays intact. |
| Woven Basket | native fallback | Visual review found the installed donor basket graphics depict paired metal bins; preserve the native woven basket. |

## Verified states

The authored-map run checks south/east/north graphics for seven prop families (bed, bedroll, dresser, table, bookcase, workbench and sewing station), unsupported vertical-flip fallback, native door open/close, linked wood/metal walls and fences, the bridge and actual shallow/deep water thresholds. Existing human/cat directions, tint, hidden/late-change fallback and known ground remain in the native generated-game checks.

The same generated-game run verifies actual HP-loss reactions, native movement/facing, targeting, inventory/menu return, disabling, save/load and three native scheduler turns. No OS input or foreground desktop session was used. Upright/injured-upright is the supported actor posture; unsupported anatomy retains native graphics. The mapping policy rejects asleep/prone states, but those postures were not exercised in this run.

## Asset review and limits

Source names alone are insufficient. Visual review rejected the installed paired-bin basket graphics for woven baskets and the modern donor stovetop for Joppa's clay oven. The grayscale fence atlas is selected by its inspected source identity rather than a duplicate blue-tinted texture name. Raw donor resources stay local.

The first prop fixture assumed fixed empty areas and failed in an occupied part of the authored map. It now selects actual clear 2-by-2 cells and separates fixtures. This is isolated diagnostic relocation, not NPC or gameplay placement logic.

Temporary assets retain native tint where supported and have explicit alpha-bound feet, dimensions and directional selection. They do not reproduce every detail, material mask, furniture content or character anatomy. Native graphics preserve the unsupported designs; no individual custom artwork was generated in this stage.
