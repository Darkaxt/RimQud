# Joppa conversion ledger

Reset date: 2026-10-20. **Every entry is UNFINISHED at the reset.**

This ledger supersedes earlier art-completion claims. Native tests establish integration behavior only. Existing sprites, traced contours, generated sheets and previous selections are historical inputs; none receive completion credit.

156 entries: 16 resident assemblies (10 blueprints), 12 body/age templates, 20 actual equipment inventory/aggregate records, 33 body/equipment fittings, 2 child-template garments, 57 scenery types, 8 surface/grass targets and 8 exclusion reviews.

The 75 baseline blueprint types are all accounted for: 67 selected visible types plus eight exclusions to recheck. Connectivity masks are enumerated under their owning wall/fence entry, not hidden behind an atlas count. Counts overlap between subjects and fittings; they are not a completion percentage.

Equipment inventory rows identify the 20 unique items and aggregate their fitting records; they do not require generating a second generic outfit. The 33 fitting entries own actual body-specific construction/refinement/extraction. An item aggregate or NPC assembly cannot complete while its linked fittings/body remain unfinished.

Active entry: **BODY-HUMAN-FEMALE-OLDER**. Overall art work: **unfinished**. Implementation Stage 3: **ACTIVE**.

## One-entry execution rule

1. Select exactly one entry and record it as IN PROGRESS with its current step. Resolve its source identity, description, native metadata and actual reference decision first.
2. Append the conversion process as it happens: timestamp, step, action, exact input hashes, prompt text/file and tool/settings when used, output hashes, corrections/rejections, and review result. Do not manufacture retrospective PASS events from file existence.
3. Body authoring: front construction -> front-guided side/back -> anatomical fixes -> composed refinement -> registered body/head/color masks. Child models are featureless mannequins; removable clothing stays separate at every age. For each equipped piece: fit on the unchanged selected body -> in-context refinement -> isolated extraction -> recomposition/occlusion review in every view.
4. Furniture/vegetation/machinery/tiles follow identity + description + original shape/palette + reference decision -> deliberate reconstruction -> relevant views/states -> refinement -> masks/registration -> visual and native review. A trace/upscale is an input, not the completed conversion.
5. Review neutral/Qud palettes, actual game scale, anatomical count, whole-body orientation, clothing perspective, cuffs, attachment and depth order. Record failures and remedies on that entry. A native batch result never completes unreviewed art entries.
6. Record generation-ready after every authoring step is finished, then close its active generation work and move to the next entry. Native validation waits until all pending conversions are generation-ready. Overall COMPLETE still requires every applicable final acceptance step and evidence; pending native acceptance remains explicit.

The JSON is the editable record; this Markdown is generated from it. `python tools/enumerate_conversion_ledger.py --render` preserves statuses/logs and updates this view. `--check` checks inventory coverage, links, one active entry and completion evidence. The script never generates art or promotes entries automatically.

Creature views/composed refinement and garment in-context refinement must follow the agreed ImageGen-assisted procedure. Record exact prompts and outputs. Deliberate construction remains the shape authority. Record a justified reference decision, including no close equivalent when applicable; installed DLC/mod references remain eligible. Reuse applicable unchanged renderer evidence rather than rerunning a full gameplay suite per entry.

## Known defects retained in scope

- Yrame: patched four-foot body still needs the completed composed workflow; chain mail fit and side-view horn attachment/overlap are wrong.
- Human bodies: the displayed standard human lacks recognizable feet; independently generated named variants also drifted from the shared human proportions.
- Irudad: four arms/hands-face and a short barb-crowned tail are supported by native definitions. The draft misses his hunched, elderly silhouette and a clearly barbed tail tip; named anatomy must remain a documented variation of the shared human base.
- Glowfish: fixed sprite has baked-in magenta/cyan; neutral-base and separate Qud masks remain unfinished.
- Tam: staff proportions/grip require review; earlier body and robe selections are also unfinished under this explicit reset.
- Furniture, vegetation, machines and most scenery are traced source silhouettes, not completed rebuilt/refined objects. Grass variation, continuous textures, banks, paths and linked surfaces need the same per-entry process.

## Inventory

### Baseline exclusion review (8)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| SCOPE-DAYLIGHTWIDGET | DaylightWidget | UNFINISHED | - | Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior. |
| SCOPE-DIRTY | Dirty | UNFINISHED | - | Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior. |
| SCOPE-LANDMARKJOPPAARGYVEWORKSHOP | LandmarkJoppaArgyveWorkshop | UNFINISHED | - | Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior. |
| SCOPE-LANDMARKJOPPAIRUDADHUT | LandmarkJoppaIrudadHut | UNFINISHED | - | Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior. |
| SCOPE-LANDMARKJOPPAMILL | LandmarkJoppaMill | UNFINISHED | - | Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior. |
| SCOPE-LANDMARKJOPPATAMTENT | LandmarkJoppaTamTent | UNFINISHED | - | Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior. |
| SCOPE-LANDMARKJOPPAWATERVINE | LandmarkJoppaWatervine | UNFINISHED | - | Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior. |
| SCOPE-PONDDOWN | PondDown | UNFINISHED | - | Unfinished exclusion review. Confirm no independent visible tile/state is being omitted; preserve native behavior. |

### Body/equipment fittings (33)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| FIT-DROMAD-CLOTH-ROBE-BODY-0 | dromad / Cloth Robe / Body / laterality 0 | UNFINISHED | ITEM-CLOTH-ROBE, BODY-DROMAD | Earlier isolated/refined robe and cuff masks exist; re-audit every view under the reset. No completion credit carried forward. |
| FIT-DROMAD-SHILLELAGH-HAND-2 | dromad / Shillelagh / Hand / laterality 2 | UNFINISHED | ITEM-SHILLELAGH, BODY-DROMAD | User reported staff too small. Later shaft enlargement has not been accepted as resolution; review proportions and grip in every view. |
| FIT-HUMAN-FEMALE-CLOTH-ROBE-BODY-0 | human-female / Cloth Robe / Body / laterality 0 | UNFINISHED | ITEM-CLOTH-ROBE, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-FEMALE-IRON-VINEREAPER-HAND-2 | human-female / Iron Vinereaper / Hand / laterality 2 | UNFINISHED | ITEM-IRON-VINEREAPER, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-FEMALE-POCKETED-VEST-BODY-0 | human-female / Pocketed Vest / Body / laterality 0 | UNFINISHED | ITEM-POCKETED-VEST, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-FEMALE-SANDALS-FEET-0 | human-female / Sandals / Feet / laterality 0 | UNFINISHED | ITEM-SANDALS, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-FEMALE-STEEL-UTILITY-KNIFE-HAND-2 | human-female / Steel Utility Knife / Hand / laterality 2 | UNFINISHED | ITEM-STEEL-UTILITY-KNIFE, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-FEMALE-TELESCOPIC-MONOCLE-FACE-0 | human-female / Telescopic Monocle / Face / laterality 0 | UNFINISHED | ITEM-TELESCOPIC-MONOCLE, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-FEMALE-WIDE-BRIMMED-HAT-HEAD-0 | human-female / Wide-brimmed Hat / Head / laterality 0 | UNFINISHED | ITEM-WIDE-BRIMMED-HAT, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-FEMALE-WOVEN-TUNIC-BODY-0 | human-female / Woven Tunic / Body / laterality 0 | UNFINISHED | ITEM-WOVEN-TUNIC, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-FEMALE-WRENCH-HAND-1 | human-female / Wrench / Hand / laterality 1 | UNFINISHED | ITEM-WRENCH, BODY-HUMAN-FEMALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-CLOTH-ROBE-BODY-0 | human-male / Cloth Robe / Body / laterality 0 | UNFINISHED | ITEM-CLOTH-ROBE, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-IRON-VINEREAPER-HAND-2 | human-male / Iron Vinereaper / Hand / laterality 2 | UNFINISHED | ITEM-IRON-VINEREAPER, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-POCKETED-VEST-BODY-0 | human-male / Pocketed Vest / Body / laterality 0 | UNFINISHED | ITEM-POCKETED-VEST, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-SANDALS-FEET-0 | human-male / Sandals / Feet / laterality 0 | UNFINISHED | ITEM-SANDALS, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-STEEL-UTILITY-KNIFE-HAND-2 | human-male / Steel Utility Knife / Hand / laterality 2 | UNFINISHED | ITEM-STEEL-UTILITY-KNIFE, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-TELESCOPIC-MONOCLE-FACE-0 | human-male / Telescopic Monocle / Face / laterality 0 | UNFINISHED | ITEM-TELESCOPIC-MONOCLE, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0 | human-male / Wide-brimmed Hat / Head / laterality 0 | UNFINISHED | ITEM-WIDE-BRIMMED-HAT, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-WOVEN-TUNIC-BODY-0 | human-male / Woven Tunic / Body / laterality 0 | UNFINISHED | ITEM-WOVEN-TUNIC, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-HUMAN-MALE-WRENCH-HAND-1 | human-male / Wrench / Hand / laterality 1 | UNFINISHED | ITEM-WRENCH, BODY-HUMAN-MALE | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-IRUDAD-BLACK-ROBES-BODY-0 | irudad / Black Robes / Body / laterality 0 | UNFINISHED | ITEM-BLACK-ROBES, BODY-IRUDAD | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-IRUDAD-SANDALS-FEET-0 | irudad / Sandals / Feet / laterality 0 | UNFINISHED | ITEM-SANDALS, BODY-IRUDAD | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-IRUDAD-SPECTACLES-FACE-0 | irudad / Spectacles / Face / laterality 0 | UNFINISHED | ITEM-SPECTACLES, BODY-IRUDAD | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-IRUDAD-WALKING-STICK-HAND-6 | irudad / Walking Stick / Hand / laterality 6 | UNFINISHED | ITEM-WALKING-STICK, BODY-IRUDAD | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-NIMA-FLOATING-GLOWSPHERE-FLOATING-NEARBY-0 | nima / Floating Glowsphere / Floating Nearby / laterality 0 | UNFINISHED | ITEM-FLOATING-GLOWSPHERE, BODY-NIMA | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-NIMA-LEATHER-APRON-BODY-0 | nima / Leather Apron / Body / laterality 0 | UNFINISHED | ITEM-LEATHER-APRON, BODY-NIMA | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-NIMA-PESTLE-HAND-6 | nima / Pestle / Hand / laterality 6 | UNFINISHED | ITEM-PESTLE, BODY-NIMA | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-NIMA-SANDALS-FEET-0 | nima / Sandals / Feet / laterality 0 | UNFINISHED | ITEM-SANDALS, BODY-NIMA | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-NIMA-WIDE-BRIMMED-HAT-HEAD-0 | nima / Wide-brimmed Hat / Head / laterality 0 | UNFINISHED | ITEM-WIDE-BRIMMED-HAT, BODY-NIMA | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-YRAME-CHAIN-MAIL-BODY-0 | yrame / Chain Mail / Body / laterality 0 | UNFINISHED | ITEM-CHAIN-MAIL, BODY-YRAME | Known defect: generic garment does not fit Yrame correctly. |
| FIT-YRAME-HORNS-HEAD-0 | yrame / Horns / Head / laterality 0 | UNFINISHED | ITEM-HORNS, BODY-YRAME | Known defect: the same frontal pair is drawn for every view; side attachment and overlap are wrong. |
| FIT-YRAME-LEATHER-BOOTS-FEET-16 | yrame / Leather Boots / Feet / laterality 16 | UNFINISHED | ITEM-LEATHER-BOOTS, BODY-YRAME | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |
| FIT-YRAME-VIBRO-BLADE-HAND-2 | yrame / Vibro Blade / Hand / laterality 2 | UNFINISHED | ITEM-VIBRO-BLADE, BODY-YRAME | Generic SVG candidate: no completed one-item in-context refinement/extraction/recomposition log. |

### Containers (5)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| SCN-CANTEEN | Canteen | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-RANDOM-BOTTLE | Random Bottle | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-VASE | Vase | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-WINE-VASE | Wine Vase | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-WOVEN-BASKET | Woven Basket | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |

### Creatures (2)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| NPC-CTESIPHUS | Ctesiphus | UNFINISHED | BODY-RAY-CAT | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-GLOWFISH | Glowfish | UNFINISHED | BODY-GLOWFISH | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |

### Equipment inventory (20)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| ITEM-BLACK-ROBES | Black Robes | UNFINISHED | FIT-IRUDAD-BLACK-ROBES-BODY-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-CHAIN-MAIL | Chain Mail | UNFINISHED | FIT-YRAME-CHAIN-MAIL-BODY-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-CLOTH-ROBE | Cloth Robe | UNFINISHED | FIT-HUMAN-MALE-CLOTH-ROBE-BODY-0, FIT-HUMAN-FEMALE-CLOTH-ROBE-BODY-0, FIT-DROMAD-CLOTH-ROBE-BODY-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-FLOATING-GLOWSPHERE | Floating Glowsphere | UNFINISHED | FIT-NIMA-FLOATING-GLOWSPHERE-FLOATING-NEARBY-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-HORNS | Horns | UNFINISHED | FIT-YRAME-HORNS-HEAD-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-IRON-VINEREAPER | Iron Vinereaper | UNFINISHED | FIT-HUMAN-MALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-FEMALE-IRON-VINEREAPER-HAND-2 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-LEATHER-APRON | Leather Apron | UNFINISHED | FIT-NIMA-LEATHER-APRON-BODY-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-LEATHER-BOOTS | Leather Boots | UNFINISHED | FIT-YRAME-LEATHER-BOOTS-FEET-16 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-PESTLE | Pestle | UNFINISHED | FIT-NIMA-PESTLE-HAND-6 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-POCKETED-VEST | Pocketed Vest | UNFINISHED | FIT-HUMAN-MALE-POCKETED-VEST-BODY-0, FIT-HUMAN-FEMALE-POCKETED-VEST-BODY-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-SANDALS | Sandals | UNFINISHED | FIT-HUMAN-MALE-SANDALS-FEET-0, FIT-HUMAN-FEMALE-SANDALS-FEET-0, FIT-IRUDAD-SANDALS-FEET-0, FIT-NIMA-SANDALS-FEET-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-SHILLELAGH | Shillelagh | UNFINISHED | FIT-DROMAD-SHILLELAGH-HAND-2 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-SPECTACLES | Spectacles | UNFINISHED | FIT-IRUDAD-SPECTACLES-FACE-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-STEEL-UTILITY-KNIFE | Steel Utility Knife | UNFINISHED | FIT-HUMAN-MALE-STEEL-UTILITY-KNIFE-HAND-2, FIT-HUMAN-FEMALE-STEEL-UTILITY-KNIFE-HAND-2 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-TELESCOPIC-MONOCLE | Telescopic Monocle | UNFINISHED | FIT-HUMAN-MALE-TELESCOPIC-MONOCLE-FACE-0, FIT-HUMAN-FEMALE-TELESCOPIC-MONOCLE-FACE-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-VIBRO-BLADE | Vibro Blade | UNFINISHED | FIT-YRAME-VIBRO-BLADE-HAND-2 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-WALKING-STICK | Walking Stick | UNFINISHED | FIT-IRUDAD-WALKING-STICK-HAND-6 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-WIDE-BRIMMED-HAT | Wide-brimmed Hat | UNFINISHED | FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-FEMALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-NIMA-WIDE-BRIMMED-HAT-HEAD-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-WOVEN-TUNIC | Woven Tunic | UNFINISHED | FIT-HUMAN-MALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-FEMALE-WOVEN-TUNIC-BODY-0 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |
| ITEM-WRENCH | Wrench | UNFINISHED | FIT-HUMAN-MALE-WRENCH-HAND-1, FIT-HUMAN-FEMALE-WRENCH-HAND-1 | Existing fits are historical candidates. Item completion requires its listed body-specific fittings; a generic garment is not a completed conversion. |

### Furniture (16)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| SCN-ALCHEMIST-TABLE | Alchemist Table | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-ARGYVE-MULTICABINET | Argyve Multicabinet | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-BED | Bed | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-BEDROLL | Bedroll | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-BOOK-TABLE | Book Table | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-CANVAS-FOLDING-CHAIR | Canvas Folding Chair | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-CHAIR | Chair | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-CHEST1 | Chest1 | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-DRESSER | Dresser | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-FLOOR-CUSHION | Floor Cushion | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-HAMMOCK | Hammock | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-JOPPA-BOOKSHELF | Joppa Bookshelf | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-MANNEQUIN | Mannequin | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-METAL-WORKBENCH | Metal Workbench | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-ORNATE-TABLE | Ornate Table | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-TABLE | Table | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |

### Machinery/appliances (10)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| SCN-BROKEN-INDUSTRIAL-FAN | Broken Industrial Fan | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-ELECTRIC-GENERATOR | Electric Generator | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-JOPPAOVEN | JoppaOven | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-LATHE | Lathe | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-LOUDSPEAKER | Loudspeaker | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-MILLSTONE | Millstone | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-POWERLESS-ELECTROTHING | Powerless Electrothing | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-SEWING-MACHINE | Sewing Machine | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-WOODEN-WATER-WHEEL | Wooden Water Wheel | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-WOODENMECHANICALTRANSMISSION | WoodenMechanicalTransmission | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |

### NPC assemblies (14)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| NPC-ARGYVE | Argyve | UNFINISHED | BODY-HUMAN-MALE, FIT-HUMAN-MALE-POCKETED-VEST-BODY-0, FIT-HUMAN-MALE-TELESCOPIC-MONOCLE-FACE-0, FIT-HUMAN-MALE-STEEL-UTILITY-KNIFE-HAND-2, FIT-HUMAN-MALE-WRENCH-HAND-1, FIT-HUMAN-MALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-ELDERBOB | Irudad (ElderBob) | UNFINISHED | BODY-IRUDAD, FIT-IRUDAD-BLACK-ROBES-BODY-0, FIT-IRUDAD-SPECTACLES-FACE-0, FIT-IRUDAD-WALKING-STICK-HAND-6, FIT-IRUDAD-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-JOPPAFARMERCONVERT | JoppaFarmerConvert | UNFINISHED | BODY-HUMAN-FEMALE, FIT-HUMAN-FEMALE-CLOTH-ROBE-BODY-0, FIT-HUMAN-FEMALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-FEMALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-FEMALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-MEHMET | Mehmet | UNFINISHED | BODY-HUMAN-MALE, FIT-HUMAN-MALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-MALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-MALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-NIMA-RUDA | Nima Ruda | UNFINISHED | BODY-NIMA, FIT-NIMA-LEATHER-APRON-BODY-0, FIT-NIMA-WIDE-BRIMMED-HAT-HEAD-0, FIT-NIMA-PESTLE-HAND-6, FIT-NIMA-SANDALS-FEET-0, FIT-NIMA-FLOATING-GLOWSPHERE-FLOATING-NEARBY-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-TAM | Tam | UNFINISHED | BODY-DROMAD, FIT-DROMAD-CLOTH-ROBE-BODY-0, FIT-DROMAD-SHILLELAGH-HAND-2 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-WARDEN-YRAME | Warden Yrame | UNFINISHED | BODY-YRAME, FIT-YRAME-CHAIN-MAIL-BODY-0, FIT-YRAME-HORNS-HEAD-0, FIT-YRAME-VIBRO-BLADE-HAND-2, FIT-YRAME-LEATHER-BOOTS-FEET-16 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-WATERVINEFARMERJOPPA-01 | WatervineFarmerJoppa / captured resident 1 | UNFINISHED | BODY-HUMAN-MALE, FIT-HUMAN-MALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-MALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-MALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-WATERVINEFARMERJOPPA-02 | WatervineFarmerJoppa / captured resident 2 | UNFINISHED | BODY-HUMAN-FEMALE, FIT-HUMAN-FEMALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-FEMALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-FEMALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-FEMALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-WATERVINEFARMERJOPPA-03 | WatervineFarmerJoppa / captured resident 3 | UNFINISHED | BODY-HUMAN-FEMALE, FIT-HUMAN-FEMALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-FEMALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-FEMALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-FEMALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-WATERVINEFARMERJOPPA-04 | WatervineFarmerJoppa / captured resident 4 | UNFINISHED | BODY-HUMAN-FEMALE, FIT-HUMAN-FEMALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-FEMALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-FEMALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-FEMALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-WATERVINEFARMERJOPPA-05 | WatervineFarmerJoppa / captured resident 5 | UNFINISHED | BODY-HUMAN-MALE, FIT-HUMAN-MALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-MALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-MALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-WATERVINEFARMERJOPPA-06 | WatervineFarmerJoppa / captured resident 6 | UNFINISHED | BODY-HUMAN-MALE, FIT-HUMAN-MALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-MALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-MALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |
| NPC-WATERVINEFARMERJOPPA-07 | WatervineFarmerJoppa / captured resident 7 | UNFINISHED | BODY-HUMAN-MALE, FIT-HUMAN-MALE-WOVEN-TUNIC-BODY-0, FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0, FIT-HUMAN-MALE-IRON-VINEREAPER-HAND-2, FIT-HUMAN-MALE-SANDALS-FEET-0 | Reused bodies/equipment are dependencies; do not generate a baked profession costume. No accepted assembly carried forward. |

### Other props/debris/light (5)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| SCN-GARBAGE | Garbage | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-PAINTING | Painting | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-SCRAP-ELECTRONICS | Scrap Electronics | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-SCRAP-METAL | Scrap Metal | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-TORCHPOST | Torchpost | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |

### Race/body templates (12)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| BODY-DROMAD | dromad | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. |
| BODY-DROMAD-CHILD | dromad child (featureless body with separate clothing) | UNFINISHED | - | Constructed template only. No native age selector established; do not assign an age to residents by guesswork. |
| BODY-GLOWFISH | glowfish | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. Known defect: magenta/cyan are baked into fixed-color pixels; palette-off is not neutral. Establish neutral base and separate Qud color masks. Existing east-guided turnaround is not evidence of the complete agreed front-first process. |
| BODY-HUMAN-CHILD | human child (featureless body with separate clothing) | UNFINISHED | - | Constructed template only. No native age selector established; do not assign an age to residents by guesswork. |
| BODY-HUMAN-FEMALE | human-female | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. Shared-human-base consistency must be reviewed across named human variants; independent turnarounds allowed unsupported proportion drift. The standard human shown in the gallery has tapered leg stubs without recognizable feet; construct and review feet and contact in every orientation. |
| BODY-HUMAN-MALE | human-male | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. Shared-human-base consistency must be reviewed across named human variants; independent turnarounds allowed unsupported proportion drift. The standard human shown in the gallery has tapered leg stubs without recognizable feet; construct and review feet and contact in every orientation. |
| BODY-IRUDAD | irudad | UNFINISHED | BODY-HUMAN-MALE-OLDER | Existing art/registration and native checks are historical only; restart the logged workflow. Latest user rule: reuse the unmutated human base; do not bake individual mutations into a new race body. Preserve mutation metadata for the separate framework. The named mutation assembly remains unfinished. Native second arm pair/hands-face is supported, but the upright mannequin omits the described hunched back and elderly proportions. Reconstruct the elder silhouette from sprite plus full description. Native description explicitly specifies a short barb-crowned tail and the blueprint includes Stinger. The displayed smooth curled tail does not clearly preserve the barbed tip; review against description in all views. The initial constructed torso shared human geometry, but independently generated/registered turnarounds drifted in torso, leg and head proportions. Derive from the selected shared human base and record each source-supported age/anatomy change. |
| BODY-NIMA | nima | UNFINISHED | BODY-HUMAN-FEMALE | Existing art/registration and native checks are historical only; restart the logged workflow. Latest user rule: reuse the unmutated human base; do not bake individual mutations into a new race body. Preserve mutation metadata for the separate framework. The named mutation assembly remains unfinished. |
| BODY-RAY-CAT | ray-cat | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. |
| BODY-YRAME | yrame | UNFINISHED | BODY-HUMAN-FEMALE | Existing art/registration and native checks are historical only; restart the logged workflow. Latest user rule: reuse the unmutated human base; do not bake individual mutations into a new race body. Preserve mutation metadata for the separate framework. The named mutation assembly remains unfinished. ImageGen three-foot proposals were rejected; four-foot geometry was patched afterward without a completed composed refinement. |
| BODY-HUMAN-FEMALE-OLDER | human female older template | IN PROGRESS | BODY-HUMAN-FEMALE | User-requested age variant of the selected shared human family. No native life-stage selector established; do not change NPC demographics. |
| BODY-HUMAN-MALE-OLDER | human male older template | UNFINISHED | BODY-HUMAN-MALE | User-requested age variant of the selected shared human family. No native life-stage selector established; do not change NPC demographics. |

### Signs/shrine (6)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| SCN-ARGYVESIGN | ArgyveSign | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-JOPPAMILLSIGN | JoppaMillSign | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-JOPPANORTHSIGN | JoppaNorthSign | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-JOPPARESHEPHSHRINE | JoppaReshephShrine | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-PEPPERSIGN2 | PepperSign2 | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-TAMSIGN | TamSign | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |

### Surface/grass tiles (8)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| TILE-GRASS-1 | Basic Grass 1 | UNFINISHED | - | Grass 1 traced candidate only; Grass 2/3 have original references but no converted output. Validate variation and vegetation merging. |
| TILE-GRASS-2 | Basic Grass 2 | UNFINISHED | - | Grass 1 traced candidate only; Grass 2/3 have original references but no converted output. Validate variation and vegetation merging. |
| TILE-GRASS-3 | Basic Grass 3 | UNFINISHED | - | Grass 1 traced candidate only; Grass 2/3 have original references but no converted output. Validate variation and vegetation merging. |
| TILE-SOIL | bare soil/interior ground | UNFINISHED | - | Procedural draft material only; identity, texture scale and transitions must be reviewed through the complete workflow. |
| TILE-WATER-DEEP | deep/swimming water | UNFINISHED | - | Procedural draft material only; identity, texture scale and transitions must be reviewed through the complete workflow. |
| TILE-MARSH | marsh/grass ground | UNFINISHED | - | Procedural draft material only; identity, texture scale and transitions must be reviewed through the complete workflow. |
| TILE-SAND | path surface | UNFINISHED | - | Procedural draft material only; identity, texture scale and transitions must be reviewed through the complete workflow. Historical filename only: replace the sandy-road interpretation with Qud-colored stone/cobblestone-like paving over grass. |
| TILE-WATER-SHALLOW | shallow/wading water | UNFINISHED | - | Procedural draft material only; identity, texture scale and transitions must be reviewed through the complete workflow. |

### Template garments (2)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| FIT-DROMAD-CHILD-TEMPLATE-TUNIC | dromad child / tunic | UNFINISHED | BODY-DROMAD-CHILD | Unmapped template garment: no actual Qud item identity or native equipped-slot binding established. |
| FIT-HUMAN-CHILD-TEMPLATE-TUNIC | human child / tunic | UNFINISHED | BODY-HUMAN-CHILD | Unmapped template garment: no actual Qud item identity or native equipped-slot binding established. |

### Terrain/structures (10)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| SCN-BRINEBRIDGE | BrineBridge | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-BRINESTALKFENCE | BrinestalkFence | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-BRINESTALKWALL | BrinestalkWall | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-BRINESTALKWALLWITHGEARBOX | BrinestalkWallWithGearbox | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-CANVASWALL | CanvasWall | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-DIRTFLOOR | DirtFloor | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-DIRTPATH | DirtPath | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. User requires the original stone/cobblestone-like path integrated over grass and original Qud palette; reject the historical sandy-road interpretation. |
| SCN-DOOR | Door | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-POND | Pond | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-RUSTEDMETALWALL | RustedMetalWall | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |

### Vegetation (5)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| SCN-BRINESTALK | Brinestalk | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-DOGTHORN-TREE | Dogthorn Tree | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-STARAPPLE-TREE | Starapple Tree | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-STARAPPLE-TREE-RIPE | Starapple Tree Ripe | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
| SCN-WATERVINE | Watervine | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |

## Per-entry workflow and artifact index

Each entry below lists all required steps and variants. Historical files are not new process-log entries.

### SCOPE-DAYLIGHTWIDGET: DaylightWidget

Required steps: verify_blueprint_visibility_and_any_tile -> record_justified_art_exclusion_or_add_conversion_target.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCOPE-DIRTY: Dirty

Required steps: verify_blueprint_visibility_and_any_tile -> record_justified_art_exclusion_or_add_conversion_target.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCOPE-LANDMARKJOPPAARGYVEWORKSHOP: LandmarkJoppaArgyveWorkshop

Required steps: verify_blueprint_visibility_and_any_tile -> record_justified_art_exclusion_or_add_conversion_target.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCOPE-LANDMARKJOPPAIRUDADHUT: LandmarkJoppaIrudadHut

Required steps: verify_blueprint_visibility_and_any_tile -> record_justified_art_exclusion_or_add_conversion_target.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCOPE-LANDMARKJOPPAMILL: LandmarkJoppaMill

Required steps: verify_blueprint_visibility_and_any_tile -> record_justified_art_exclusion_or_add_conversion_target.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCOPE-LANDMARKJOPPATAMTENT: LandmarkJoppaTamTent

Required steps: verify_blueprint_visibility_and_any_tile -> record_justified_art_exclusion_or_add_conversion_target.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCOPE-LANDMARKJOPPAWATERVINE: LandmarkJoppaWatervine

Required steps: verify_blueprint_visibility_and_any_tile -> record_justified_art_exclusion_or_add_conversion_target.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCOPE-PONDDOWN: PondDown

Required steps: verify_blueprint_visibility_and_any_tile -> record_justified_art_exclusion_or_add_conversion_target.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### FIT-DROMAD-CLOTH-ROBE-BODY-0: dromad / Cloth Robe / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/dromad/layered/robe-east.png](../art/dromad/layered/robe-east.png), [art/dromad/layered/robe-north.png](../art/dromad/layered/robe-north.png), [art/dromad/layered/robe-south.png](../art/dromad/layered/robe-south.png).

Current step: not started. Process-log events: 0.

### FIT-DROMAD-SHILLELAGH-HAND-2: dromad / Shillelagh / Hand / laterality 2

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/dromad-shillelagh-east.png](../art/village/equipment/dromad-shillelagh-east.png), [art/village/equipment/dromad-shillelagh-north.png](../art/village/equipment/dromad-shillelagh-north.png), [art/village/equipment/dromad-shillelagh-south.png](../art/village/equipment/dromad-shillelagh-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-CLOTH-ROBE-BODY-0: human-female / Cloth Robe / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-cloth-robe-body-0-item-detail-east.png](../art/village/equipment/human-female-cloth-robe-body-0-item-detail-east.png), [art/village/equipment/human-female-cloth-robe-body-0-item-detail-north.png](../art/village/equipment/human-female-cloth-robe-body-0-item-detail-north.png), [art/village/equipment/human-female-cloth-robe-body-0-item-detail-south.png](../art/village/equipment/human-female-cloth-robe-body-0-item-detail-south.png), [art/village/equipment/human-female-cloth-robe-body-0-item-east.png](../art/village/equipment/human-female-cloth-robe-body-0-item-east.png), [art/village/equipment/human-female-cloth-robe-body-0-item-north.png](../art/village/equipment/human-female-cloth-robe-body-0-item-north.png), [art/village/equipment/human-female-cloth-robe-body-0-item-south.png](../art/village/equipment/human-female-cloth-robe-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-IRON-VINEREAPER-HAND-2: human-female / Iron Vinereaper / Hand / laterality 2

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-iron-vinereaper-hand-2-item-detail-east.png](../art/village/equipment/human-female-iron-vinereaper-hand-2-item-detail-east.png), [art/village/equipment/human-female-iron-vinereaper-hand-2-item-detail-north.png](../art/village/equipment/human-female-iron-vinereaper-hand-2-item-detail-north.png), [art/village/equipment/human-female-iron-vinereaper-hand-2-item-detail-south.png](../art/village/equipment/human-female-iron-vinereaper-hand-2-item-detail-south.png), [art/village/equipment/human-female-iron-vinereaper-hand-2-item-east.png](../art/village/equipment/human-female-iron-vinereaper-hand-2-item-east.png), [art/village/equipment/human-female-iron-vinereaper-hand-2-item-north.png](../art/village/equipment/human-female-iron-vinereaper-hand-2-item-north.png), [art/village/equipment/human-female-iron-vinereaper-hand-2-item-south.png](../art/village/equipment/human-female-iron-vinereaper-hand-2-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-POCKETED-VEST-BODY-0: human-female / Pocketed Vest / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-pocketed-vest-body-0-item-detail-east.png](../art/village/equipment/human-female-pocketed-vest-body-0-item-detail-east.png), [art/village/equipment/human-female-pocketed-vest-body-0-item-detail-south.png](../art/village/equipment/human-female-pocketed-vest-body-0-item-detail-south.png), [art/village/equipment/human-female-pocketed-vest-body-0-item-east.png](../art/village/equipment/human-female-pocketed-vest-body-0-item-east.png), [art/village/equipment/human-female-pocketed-vest-body-0-item-north.png](../art/village/equipment/human-female-pocketed-vest-body-0-item-north.png), [art/village/equipment/human-female-pocketed-vest-body-0-item-south.png](../art/village/equipment/human-female-pocketed-vest-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-SANDALS-FEET-0: human-female / Sandals / Feet / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-sandals-feet-0-item-detail-east.png](../art/village/equipment/human-female-sandals-feet-0-item-detail-east.png), [art/village/equipment/human-female-sandals-feet-0-item-detail-north.png](../art/village/equipment/human-female-sandals-feet-0-item-detail-north.png), [art/village/equipment/human-female-sandals-feet-0-item-detail-south.png](../art/village/equipment/human-female-sandals-feet-0-item-detail-south.png), [art/village/equipment/human-female-sandals-feet-0-item-east.png](../art/village/equipment/human-female-sandals-feet-0-item-east.png), [art/village/equipment/human-female-sandals-feet-0-item-north.png](../art/village/equipment/human-female-sandals-feet-0-item-north.png), [art/village/equipment/human-female-sandals-feet-0-item-south.png](../art/village/equipment/human-female-sandals-feet-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-STEEL-UTILITY-KNIFE-HAND-2: human-female / Steel Utility Knife / Hand / laterality 2

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-steel-utility-knife-hand-2-item-detail-east.png](../art/village/equipment/human-female-steel-utility-knife-hand-2-item-detail-east.png), [art/village/equipment/human-female-steel-utility-knife-hand-2-item-detail-north.png](../art/village/equipment/human-female-steel-utility-knife-hand-2-item-detail-north.png), [art/village/equipment/human-female-steel-utility-knife-hand-2-item-detail-south.png](../art/village/equipment/human-female-steel-utility-knife-hand-2-item-detail-south.png), [art/village/equipment/human-female-steel-utility-knife-hand-2-item-east.png](../art/village/equipment/human-female-steel-utility-knife-hand-2-item-east.png), [art/village/equipment/human-female-steel-utility-knife-hand-2-item-north.png](../art/village/equipment/human-female-steel-utility-knife-hand-2-item-north.png), [art/village/equipment/human-female-steel-utility-knife-hand-2-item-south.png](../art/village/equipment/human-female-steel-utility-knife-hand-2-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-TELESCOPIC-MONOCLE-FACE-0: human-female / Telescopic Monocle / Face / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-telescopic-monocle-face-0-item-detail-east.png](../art/village/equipment/human-female-telescopic-monocle-face-0-item-detail-east.png), [art/village/equipment/human-female-telescopic-monocle-face-0-item-detail-south.png](../art/village/equipment/human-female-telescopic-monocle-face-0-item-detail-south.png), [art/village/equipment/human-female-telescopic-monocle-face-0-item-east.png](../art/village/equipment/human-female-telescopic-monocle-face-0-item-east.png), [art/village/equipment/human-female-telescopic-monocle-face-0-item-south.png](../art/village/equipment/human-female-telescopic-monocle-face-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-WIDE-BRIMMED-HAT-HEAD-0: human-female / Wide-brimmed Hat / Head / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-wide-brimmed-hat-head-0-item-detail-east.png](../art/village/equipment/human-female-wide-brimmed-hat-head-0-item-detail-east.png), [art/village/equipment/human-female-wide-brimmed-hat-head-0-item-detail-north.png](../art/village/equipment/human-female-wide-brimmed-hat-head-0-item-detail-north.png), [art/village/equipment/human-female-wide-brimmed-hat-head-0-item-detail-south.png](../art/village/equipment/human-female-wide-brimmed-hat-head-0-item-detail-south.png), [art/village/equipment/human-female-wide-brimmed-hat-head-0-item-east.png](../art/village/equipment/human-female-wide-brimmed-hat-head-0-item-east.png), [art/village/equipment/human-female-wide-brimmed-hat-head-0-item-north.png](../art/village/equipment/human-female-wide-brimmed-hat-head-0-item-north.png), [art/village/equipment/human-female-wide-brimmed-hat-head-0-item-south.png](../art/village/equipment/human-female-wide-brimmed-hat-head-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-WOVEN-TUNIC-BODY-0: human-female / Woven Tunic / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-woven-tunic-body-0-item-detail-east.png](../art/village/equipment/human-female-woven-tunic-body-0-item-detail-east.png), [art/village/equipment/human-female-woven-tunic-body-0-item-detail-north.png](../art/village/equipment/human-female-woven-tunic-body-0-item-detail-north.png), [art/village/equipment/human-female-woven-tunic-body-0-item-detail-south.png](../art/village/equipment/human-female-woven-tunic-body-0-item-detail-south.png), [art/village/equipment/human-female-woven-tunic-body-0-item-east.png](../art/village/equipment/human-female-woven-tunic-body-0-item-east.png), [art/village/equipment/human-female-woven-tunic-body-0-item-north.png](../art/village/equipment/human-female-woven-tunic-body-0-item-north.png), [art/village/equipment/human-female-woven-tunic-body-0-item-south.png](../art/village/equipment/human-female-woven-tunic-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-FEMALE-WRENCH-HAND-1: human-female / Wrench / Hand / laterality 1

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-female-wrench-hand-1-item-east.png](../art/village/equipment/human-female-wrench-hand-1-item-east.png), [art/village/equipment/human-female-wrench-hand-1-item-north.png](../art/village/equipment/human-female-wrench-hand-1-item-north.png), [art/village/equipment/human-female-wrench-hand-1-item-south.png](../art/village/equipment/human-female-wrench-hand-1-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-CLOTH-ROBE-BODY-0: human-male / Cloth Robe / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-cloth-robe-body-0-item-detail-east.png](../art/village/equipment/human-male-cloth-robe-body-0-item-detail-east.png), [art/village/equipment/human-male-cloth-robe-body-0-item-detail-north.png](../art/village/equipment/human-male-cloth-robe-body-0-item-detail-north.png), [art/village/equipment/human-male-cloth-robe-body-0-item-detail-south.png](../art/village/equipment/human-male-cloth-robe-body-0-item-detail-south.png), [art/village/equipment/human-male-cloth-robe-body-0-item-east.png](../art/village/equipment/human-male-cloth-robe-body-0-item-east.png), [art/village/equipment/human-male-cloth-robe-body-0-item-north.png](../art/village/equipment/human-male-cloth-robe-body-0-item-north.png), [art/village/equipment/human-male-cloth-robe-body-0-item-south.png](../art/village/equipment/human-male-cloth-robe-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-IRON-VINEREAPER-HAND-2: human-male / Iron Vinereaper / Hand / laterality 2

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-iron-vinereaper-hand-2-item-detail-east.png](../art/village/equipment/human-male-iron-vinereaper-hand-2-item-detail-east.png), [art/village/equipment/human-male-iron-vinereaper-hand-2-item-detail-north.png](../art/village/equipment/human-male-iron-vinereaper-hand-2-item-detail-north.png), [art/village/equipment/human-male-iron-vinereaper-hand-2-item-detail-south.png](../art/village/equipment/human-male-iron-vinereaper-hand-2-item-detail-south.png), [art/village/equipment/human-male-iron-vinereaper-hand-2-item-east.png](../art/village/equipment/human-male-iron-vinereaper-hand-2-item-east.png), [art/village/equipment/human-male-iron-vinereaper-hand-2-item-north.png](../art/village/equipment/human-male-iron-vinereaper-hand-2-item-north.png), [art/village/equipment/human-male-iron-vinereaper-hand-2-item-south.png](../art/village/equipment/human-male-iron-vinereaper-hand-2-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-POCKETED-VEST-BODY-0: human-male / Pocketed Vest / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-pocketed-vest-body-0-item-detail-east.png](../art/village/equipment/human-male-pocketed-vest-body-0-item-detail-east.png), [art/village/equipment/human-male-pocketed-vest-body-0-item-detail-south.png](../art/village/equipment/human-male-pocketed-vest-body-0-item-detail-south.png), [art/village/equipment/human-male-pocketed-vest-body-0-item-east.png](../art/village/equipment/human-male-pocketed-vest-body-0-item-east.png), [art/village/equipment/human-male-pocketed-vest-body-0-item-north.png](../art/village/equipment/human-male-pocketed-vest-body-0-item-north.png), [art/village/equipment/human-male-pocketed-vest-body-0-item-south.png](../art/village/equipment/human-male-pocketed-vest-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-SANDALS-FEET-0: human-male / Sandals / Feet / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-sandals-feet-0-item-detail-east.png](../art/village/equipment/human-male-sandals-feet-0-item-detail-east.png), [art/village/equipment/human-male-sandals-feet-0-item-detail-north.png](../art/village/equipment/human-male-sandals-feet-0-item-detail-north.png), [art/village/equipment/human-male-sandals-feet-0-item-detail-south.png](../art/village/equipment/human-male-sandals-feet-0-item-detail-south.png), [art/village/equipment/human-male-sandals-feet-0-item-east.png](../art/village/equipment/human-male-sandals-feet-0-item-east.png), [art/village/equipment/human-male-sandals-feet-0-item-north.png](../art/village/equipment/human-male-sandals-feet-0-item-north.png), [art/village/equipment/human-male-sandals-feet-0-item-south.png](../art/village/equipment/human-male-sandals-feet-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-STEEL-UTILITY-KNIFE-HAND-2: human-male / Steel Utility Knife / Hand / laterality 2

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-steel-utility-knife-hand-2-item-detail-east.png](../art/village/equipment/human-male-steel-utility-knife-hand-2-item-detail-east.png), [art/village/equipment/human-male-steel-utility-knife-hand-2-item-detail-north.png](../art/village/equipment/human-male-steel-utility-knife-hand-2-item-detail-north.png), [art/village/equipment/human-male-steel-utility-knife-hand-2-item-detail-south.png](../art/village/equipment/human-male-steel-utility-knife-hand-2-item-detail-south.png), [art/village/equipment/human-male-steel-utility-knife-hand-2-item-east.png](../art/village/equipment/human-male-steel-utility-knife-hand-2-item-east.png), [art/village/equipment/human-male-steel-utility-knife-hand-2-item-north.png](../art/village/equipment/human-male-steel-utility-knife-hand-2-item-north.png), [art/village/equipment/human-male-steel-utility-knife-hand-2-item-south.png](../art/village/equipment/human-male-steel-utility-knife-hand-2-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-TELESCOPIC-MONOCLE-FACE-0: human-male / Telescopic Monocle / Face / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-telescopic-monocle-face-0-item-detail-east.png](../art/village/equipment/human-male-telescopic-monocle-face-0-item-detail-east.png), [art/village/equipment/human-male-telescopic-monocle-face-0-item-detail-south.png](../art/village/equipment/human-male-telescopic-monocle-face-0-item-detail-south.png), [art/village/equipment/human-male-telescopic-monocle-face-0-item-east.png](../art/village/equipment/human-male-telescopic-monocle-face-0-item-east.png), [art/village/equipment/human-male-telescopic-monocle-face-0-item-south.png](../art/village/equipment/human-male-telescopic-monocle-face-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-WIDE-BRIMMED-HAT-HEAD-0: human-male / Wide-brimmed Hat / Head / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-wide-brimmed-hat-head-0-item-detail-east.png](../art/village/equipment/human-male-wide-brimmed-hat-head-0-item-detail-east.png), [art/village/equipment/human-male-wide-brimmed-hat-head-0-item-detail-north.png](../art/village/equipment/human-male-wide-brimmed-hat-head-0-item-detail-north.png), [art/village/equipment/human-male-wide-brimmed-hat-head-0-item-detail-south.png](../art/village/equipment/human-male-wide-brimmed-hat-head-0-item-detail-south.png), [art/village/equipment/human-male-wide-brimmed-hat-head-0-item-east.png](../art/village/equipment/human-male-wide-brimmed-hat-head-0-item-east.png), [art/village/equipment/human-male-wide-brimmed-hat-head-0-item-north.png](../art/village/equipment/human-male-wide-brimmed-hat-head-0-item-north.png), [art/village/equipment/human-male-wide-brimmed-hat-head-0-item-south.png](../art/village/equipment/human-male-wide-brimmed-hat-head-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-WOVEN-TUNIC-BODY-0: human-male / Woven Tunic / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-woven-tunic-body-0-item-detail-east.png](../art/village/equipment/human-male-woven-tunic-body-0-item-detail-east.png), [art/village/equipment/human-male-woven-tunic-body-0-item-detail-north.png](../art/village/equipment/human-male-woven-tunic-body-0-item-detail-north.png), [art/village/equipment/human-male-woven-tunic-body-0-item-detail-south.png](../art/village/equipment/human-male-woven-tunic-body-0-item-detail-south.png), [art/village/equipment/human-male-woven-tunic-body-0-item-east.png](../art/village/equipment/human-male-woven-tunic-body-0-item-east.png), [art/village/equipment/human-male-woven-tunic-body-0-item-north.png](../art/village/equipment/human-male-woven-tunic-body-0-item-north.png), [art/village/equipment/human-male-woven-tunic-body-0-item-south.png](../art/village/equipment/human-male-woven-tunic-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-MALE-WRENCH-HAND-1: human-male / Wrench / Hand / laterality 1

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/human-male-wrench-hand-1-item-east.png](../art/village/equipment/human-male-wrench-hand-1-item-east.png), [art/village/equipment/human-male-wrench-hand-1-item-north.png](../art/village/equipment/human-male-wrench-hand-1-item-north.png), [art/village/equipment/human-male-wrench-hand-1-item-south.png](../art/village/equipment/human-male-wrench-hand-1-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-IRUDAD-BLACK-ROBES-BODY-0: irudad / Black Robes / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/irudad-black-robes-body-0-item-detail-east.png](../art/village/equipment/irudad-black-robes-body-0-item-detail-east.png), [art/village/equipment/irudad-black-robes-body-0-item-detail-north.png](../art/village/equipment/irudad-black-robes-body-0-item-detail-north.png), [art/village/equipment/irudad-black-robes-body-0-item-detail-south.png](../art/village/equipment/irudad-black-robes-body-0-item-detail-south.png), [art/village/equipment/irudad-black-robes-body-0-item-east.png](../art/village/equipment/irudad-black-robes-body-0-item-east.png), [art/village/equipment/irudad-black-robes-body-0-item-north.png](../art/village/equipment/irudad-black-robes-body-0-item-north.png), [art/village/equipment/irudad-black-robes-body-0-item-south.png](../art/village/equipment/irudad-black-robes-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-IRUDAD-SANDALS-FEET-0: irudad / Sandals / Feet / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/irudad-sandals-feet-0-item-detail-east.png](../art/village/equipment/irudad-sandals-feet-0-item-detail-east.png), [art/village/equipment/irudad-sandals-feet-0-item-detail-north.png](../art/village/equipment/irudad-sandals-feet-0-item-detail-north.png), [art/village/equipment/irudad-sandals-feet-0-item-detail-south.png](../art/village/equipment/irudad-sandals-feet-0-item-detail-south.png), [art/village/equipment/irudad-sandals-feet-0-item-east.png](../art/village/equipment/irudad-sandals-feet-0-item-east.png), [art/village/equipment/irudad-sandals-feet-0-item-north.png](../art/village/equipment/irudad-sandals-feet-0-item-north.png), [art/village/equipment/irudad-sandals-feet-0-item-south.png](../art/village/equipment/irudad-sandals-feet-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-IRUDAD-SPECTACLES-FACE-0: irudad / Spectacles / Face / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/irudad-spectacles-face-0-item-east.png](../art/village/equipment/irudad-spectacles-face-0-item-east.png), [art/village/equipment/irudad-spectacles-face-0-item-south.png](../art/village/equipment/irudad-spectacles-face-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-IRUDAD-WALKING-STICK-HAND-6: irudad / Walking Stick / Hand / laterality 6

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/irudad-walking-stick-hand-6-item-east.png](../art/village/equipment/irudad-walking-stick-hand-6-item-east.png), [art/village/equipment/irudad-walking-stick-hand-6-item-north.png](../art/village/equipment/irudad-walking-stick-hand-6-item-north.png), [art/village/equipment/irudad-walking-stick-hand-6-item-south.png](../art/village/equipment/irudad-walking-stick-hand-6-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-NIMA-FLOATING-GLOWSPHERE-FLOATING-NEARBY-0: nima / Floating Glowsphere / Floating Nearby / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-detail-east.png](../art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-detail-east.png), [art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-detail-north.png](../art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-detail-north.png), [art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-detail-south.png](../art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-detail-south.png), [art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-east.png](../art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-east.png), [art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-north.png](../art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-north.png), [art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-south.png](../art/village/equipment/nima-floating-glowsphere-floating nearby-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-NIMA-LEATHER-APRON-BODY-0: nima / Leather Apron / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/nima-leather-apron-body-0-item-detail-east.png](../art/village/equipment/nima-leather-apron-body-0-item-detail-east.png), [art/village/equipment/nima-leather-apron-body-0-item-detail-south.png](../art/village/equipment/nima-leather-apron-body-0-item-detail-south.png), [art/village/equipment/nima-leather-apron-body-0-item-east.png](../art/village/equipment/nima-leather-apron-body-0-item-east.png), [art/village/equipment/nima-leather-apron-body-0-item-north.png](../art/village/equipment/nima-leather-apron-body-0-item-north.png), [art/village/equipment/nima-leather-apron-body-0-item-south.png](../art/village/equipment/nima-leather-apron-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-NIMA-PESTLE-HAND-6: nima / Pestle / Hand / laterality 6

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/nima-pestle-hand-6-item-east.png](../art/village/equipment/nima-pestle-hand-6-item-east.png), [art/village/equipment/nima-pestle-hand-6-item-north.png](../art/village/equipment/nima-pestle-hand-6-item-north.png), [art/village/equipment/nima-pestle-hand-6-item-south.png](../art/village/equipment/nima-pestle-hand-6-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-NIMA-SANDALS-FEET-0: nima / Sandals / Feet / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/nima-sandals-feet-0-item-detail-east.png](../art/village/equipment/nima-sandals-feet-0-item-detail-east.png), [art/village/equipment/nima-sandals-feet-0-item-detail-north.png](../art/village/equipment/nima-sandals-feet-0-item-detail-north.png), [art/village/equipment/nima-sandals-feet-0-item-detail-south.png](../art/village/equipment/nima-sandals-feet-0-item-detail-south.png), [art/village/equipment/nima-sandals-feet-0-item-east.png](../art/village/equipment/nima-sandals-feet-0-item-east.png), [art/village/equipment/nima-sandals-feet-0-item-north.png](../art/village/equipment/nima-sandals-feet-0-item-north.png), [art/village/equipment/nima-sandals-feet-0-item-south.png](../art/village/equipment/nima-sandals-feet-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-NIMA-WIDE-BRIMMED-HAT-HEAD-0: nima / Wide-brimmed Hat / Head / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/nima-wide-brimmed-hat-head-0-item-detail-east.png](../art/village/equipment/nima-wide-brimmed-hat-head-0-item-detail-east.png), [art/village/equipment/nima-wide-brimmed-hat-head-0-item-detail-north.png](../art/village/equipment/nima-wide-brimmed-hat-head-0-item-detail-north.png), [art/village/equipment/nima-wide-brimmed-hat-head-0-item-detail-south.png](../art/village/equipment/nima-wide-brimmed-hat-head-0-item-detail-south.png), [art/village/equipment/nima-wide-brimmed-hat-head-0-item-east.png](../art/village/equipment/nima-wide-brimmed-hat-head-0-item-east.png), [art/village/equipment/nima-wide-brimmed-hat-head-0-item-north.png](../art/village/equipment/nima-wide-brimmed-hat-head-0-item-north.png), [art/village/equipment/nima-wide-brimmed-hat-head-0-item-south.png](../art/village/equipment/nima-wide-brimmed-hat-head-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-YRAME-CHAIN-MAIL-BODY-0: yrame / Chain Mail / Body / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/yrame-chain-mail-body-0-item-detail-east.png](../art/village/equipment/yrame-chain-mail-body-0-item-detail-east.png), [art/village/equipment/yrame-chain-mail-body-0-item-detail-north.png](../art/village/equipment/yrame-chain-mail-body-0-item-detail-north.png), [art/village/equipment/yrame-chain-mail-body-0-item-detail-south.png](../art/village/equipment/yrame-chain-mail-body-0-item-detail-south.png), [art/village/equipment/yrame-chain-mail-body-0-item-east.png](../art/village/equipment/yrame-chain-mail-body-0-item-east.png), [art/village/equipment/yrame-chain-mail-body-0-item-north.png](../art/village/equipment/yrame-chain-mail-body-0-item-north.png), [art/village/equipment/yrame-chain-mail-body-0-item-south.png](../art/village/equipment/yrame-chain-mail-body-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-YRAME-HORNS-HEAD-0: yrame / Horns / Head / laterality 0

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/yrame-horns-head-0-item-detail-east.png](../art/village/equipment/yrame-horns-head-0-item-detail-east.png), [art/village/equipment/yrame-horns-head-0-item-detail-north.png](../art/village/equipment/yrame-horns-head-0-item-detail-north.png), [art/village/equipment/yrame-horns-head-0-item-detail-south.png](../art/village/equipment/yrame-horns-head-0-item-detail-south.png), [art/village/equipment/yrame-horns-head-0-item-east.png](../art/village/equipment/yrame-horns-head-0-item-east.png), [art/village/equipment/yrame-horns-head-0-item-north.png](../art/village/equipment/yrame-horns-head-0-item-north.png), [art/village/equipment/yrame-horns-head-0-item-south.png](../art/village/equipment/yrame-horns-head-0-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-YRAME-LEATHER-BOOTS-FEET-16: yrame / Leather Boots / Feet / laterality 16

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/yrame-leather-boots-feet-16-item-detail-east.png](../art/village/equipment/yrame-leather-boots-feet-16-item-detail-east.png), [art/village/equipment/yrame-leather-boots-feet-16-item-detail-north.png](../art/village/equipment/yrame-leather-boots-feet-16-item-detail-north.png), [art/village/equipment/yrame-leather-boots-feet-16-item-detail-south.png](../art/village/equipment/yrame-leather-boots-feet-16-item-detail-south.png), [art/village/equipment/yrame-leather-boots-feet-16-item-east.png](../art/village/equipment/yrame-leather-boots-feet-16-item-east.png), [art/village/equipment/yrame-leather-boots-feet-16-item-north.png](../art/village/equipment/yrame-leather-boots-feet-16-item-north.png), [art/village/equipment/yrame-leather-boots-feet-16-item-south.png](../art/village/equipment/yrame-leather-boots-feet-16-item-south.png).

Current step: not started. Process-log events: 0.

### FIT-YRAME-VIBRO-BLADE-HAND-2: yrame / Vibro Blade / Hand / laterality 2

Required steps: source_identity_description_slot_laterality -> select_correct_body_and_references -> construct_and_overlay_one_item -> imagegen_refine_in_context_on_unchanged_body -> retrieve_isolated_item_and_masks -> recompose_check_cuffs_attachment_occlusion_all_views -> review_game_scale_and_palette -> native_equipment_state_review.

Required views/states: south; east; north; west mirror/handedness review.

Historical artifacts: [art/village/equipment/yrame-vibro-blade-hand-2-item-detail-east.png](../art/village/equipment/yrame-vibro-blade-hand-2-item-detail-east.png), [art/village/equipment/yrame-vibro-blade-hand-2-item-detail-north.png](../art/village/equipment/yrame-vibro-blade-hand-2-item-detail-north.png), [art/village/equipment/yrame-vibro-blade-hand-2-item-detail-south.png](../art/village/equipment/yrame-vibro-blade-hand-2-item-detail-south.png), [art/village/equipment/yrame-vibro-blade-hand-2-item-east.png](../art/village/equipment/yrame-vibro-blade-hand-2-item-east.png), [art/village/equipment/yrame-vibro-blade-hand-2-item-north.png](../art/village/equipment/yrame-vibro-blade-hand-2-item-north.png), [art/village/equipment/yrame-vibro-blade-hand-2-item-south.png](../art/village/equipment/yrame-vibro-blade-hand-2-item-south.png).

Current step: not started. Process-log events: 0.

### SCN-CANTEEN: Canteen

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/canteen-body.png](../art/village/scenery/canteen-body.png), [art/village/scenery/canteen-detail.png](../art/village/scenery/canteen-detail.png).

Current step: not started. Process-log events: 0.

### SCN-RANDOM-BOTTLE: Random Bottle

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/random-bottle-body.png](../art/village/scenery/random-bottle-body.png), [art/village/scenery/random-bottle-detail.png](../art/village/scenery/random-bottle-detail.png).

Current step: not started. Process-log events: 0.

### SCN-VASE: Vase

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/wine-vase-body.png](../art/village/scenery/wine-vase-body.png), [art/village/scenery/wine-vase-detail.png](../art/village/scenery/wine-vase-detail.png).

Current step: not started. Process-log events: 0.

### SCN-WINE-VASE: Wine Vase

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/wine-vase-body.png](../art/village/scenery/wine-vase-body.png), [art/village/scenery/wine-vase-detail.png](../art/village/scenery/wine-vase-detail.png).

Current step: not started. Process-log events: 0.

### SCN-WOVEN-BASKET: Woven Basket

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/woven-basket-detail.png](../art/village/scenery/woven-basket-detail.png).

Current step: not started. Process-log events: 0.

### NPC-CTESIPHUS: Ctesiphus

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-GLOWFISH: Glowfish

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-BLACK-ROBES: Black Robes

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-CHAIN-MAIL: Chain Mail

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-CLOTH-ROBE: Cloth Robe

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-FLOATING-GLOWSPHERE: Floating Glowsphere

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-HORNS: Horns

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-IRON-VINEREAPER: Iron Vinereaper

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-LEATHER-APRON: Leather Apron

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-LEATHER-BOOTS: Leather Boots

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-PESTLE: Pestle

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-POCKETED-VEST: Pocketed Vest

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-SANDALS: Sandals

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-SHILLELAGH: Shillelagh

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-SPECTACLES: Spectacles

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-STEEL-UTILITY-KNIFE: Steel Utility Knife

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-TELESCOPIC-MONOCLE: Telescopic Monocle

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-VIBRO-BLADE: Vibro Blade

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-WALKING-STICK: Walking Stick

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-WIDE-BRIMMED-HAT: Wide-brimmed Hat

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-WOVEN-TUNIC: Woven Tunic

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### ITEM-WRENCH: Wrench

Required steps: resolve_item_identity_description_palette -> verify_every_body_fitting_log -> record_item_acceptance_from_all_fittings.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCN-ALCHEMIST-TABLE: Alchemist Table

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/alchemist-table-body.png](../art/village/scenery/alchemist-table-body.png), [art/village/scenery/alchemist-table-detail.png](../art/village/scenery/alchemist-table-detail.png).

Current step: not started. Process-log events: 0.

### SCN-ARGYVE-MULTICABINET: Argyve Multicabinet

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/argyve-multicabinet-body.png](../art/village/scenery/argyve-multicabinet-body.png), [art/village/scenery/argyve-multicabinet-detail.png](../art/village/scenery/argyve-multicabinet-detail.png).

Current step: not started. Process-log events: 0.

### SCN-BED: Bed

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/bed-body.png](../art/village/scenery/bed-body.png), [art/village/scenery/bed-detail.png](../art/village/scenery/bed-detail.png).

Current step: not started. Process-log events: 0.

### SCN-BEDROLL: Bedroll

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/bedroll-body.png](../art/village/scenery/bedroll-body.png), [art/village/scenery/bedroll-detail.png](../art/village/scenery/bedroll-detail.png).

Current step: not started. Process-log events: 0.

### SCN-BOOK-TABLE: Book Table

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/book-table-body.png](../art/village/scenery/book-table-body.png), [art/village/scenery/book-table-detail.png](../art/village/scenery/book-table-detail.png).

Current step: not started. Process-log events: 0.

### SCN-CANVAS-FOLDING-CHAIR: Canvas Folding Chair

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/canvas-folding-chair-body.png](../art/village/scenery/canvas-folding-chair-body.png), [art/village/scenery/canvas-folding-chair-detail.png](../art/village/scenery/canvas-folding-chair-detail.png).

Current step: not started. Process-log events: 0.

### SCN-CHAIR: Chair

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/chair-body.png](../art/village/scenery/chair-body.png), [art/village/scenery/chair-detail.png](../art/village/scenery/chair-detail.png).

Current step: not started. Process-log events: 0.

### SCN-CHEST1: Chest1

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/chest1-body.png](../art/village/scenery/chest1-body.png), [art/village/scenery/chest1-detail.png](../art/village/scenery/chest1-detail.png).

Current step: not started. Process-log events: 0.

### SCN-DRESSER: Dresser

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/dresser-body.png](../art/village/scenery/dresser-body.png), [art/village/scenery/dresser-detail.png](../art/village/scenery/dresser-detail.png).

Current step: not started. Process-log events: 0.

### SCN-FLOOR-CUSHION: Floor Cushion

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/floor-cushion-body.png](../art/village/scenery/floor-cushion-body.png), [art/village/scenery/floor-cushion-detail.png](../art/village/scenery/floor-cushion-detail.png).

Current step: not started. Process-log events: 0.

### SCN-HAMMOCK: Hammock

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/hammock-body.png](../art/village/scenery/hammock-body.png), [art/village/scenery/hammock-detail.png](../art/village/scenery/hammock-detail.png).

Current step: not started. Process-log events: 0.

### SCN-JOPPA-BOOKSHELF: Joppa Bookshelf

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/joppa-bookshelf-body.png](../art/village/scenery/joppa-bookshelf-body.png), [art/village/scenery/joppa-bookshelf-detail.png](../art/village/scenery/joppa-bookshelf-detail.png).

Current step: not started. Process-log events: 0.

### SCN-MANNEQUIN: Mannequin

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/mannequin-body.png](../art/village/scenery/mannequin-body.png), [art/village/scenery/mannequin-detail.png](../art/village/scenery/mannequin-detail.png).

Current step: not started. Process-log events: 0.

### SCN-METAL-WORKBENCH: Metal Workbench

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/metal-workbench-body.png](../art/village/scenery/metal-workbench-body.png).

Current step: not started. Process-log events: 0.

### SCN-ORNATE-TABLE: Ornate Table

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/ornate-table-body.png](../art/village/scenery/ornate-table-body.png), [art/village/scenery/ornate-table-detail.png](../art/village/scenery/ornate-table-detail.png).

Current step: not started. Process-log events: 0.

### SCN-TABLE: Table

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/table-body.png](../art/village/scenery/table-body.png).

Current step: not started. Process-log events: 0.

### SCN-BROKEN-INDUSTRIAL-FAN: Broken Industrial Fan

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/broken-industrial-fan-body.png](../art/village/scenery/broken-industrial-fan-body.png), [art/village/scenery/broken-industrial-fan-detail.png](../art/village/scenery/broken-industrial-fan-detail.png).

Current step: not started. Process-log events: 0.

### SCN-ELECTRIC-GENERATOR: Electric Generator

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/electric-generator-body.png](../art/village/scenery/electric-generator-body.png), [art/village/scenery/electric-generator-detail.png](../art/village/scenery/electric-generator-detail.png).

Current step: not started. Process-log events: 0.

### SCN-JOPPAOVEN: JoppaOven

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/joppaoven-body.png](../art/village/scenery/joppaoven-body.png), [art/village/scenery/joppaoven-detail.png](../art/village/scenery/joppaoven-detail.png).

Current step: not started. Process-log events: 0.

### SCN-LATHE: Lathe

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/lathe-body.png](../art/village/scenery/lathe-body.png), [art/village/scenery/lathe-detail.png](../art/village/scenery/lathe-detail.png).

Current step: not started. Process-log events: 0.

### SCN-LOUDSPEAKER: Loudspeaker

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/loudspeaker-body.png](../art/village/scenery/loudspeaker-body.png), [art/village/scenery/loudspeaker-detail.png](../art/village/scenery/loudspeaker-detail.png).

Current step: not started. Process-log events: 0.

### SCN-MILLSTONE: Millstone

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/millstone-body.png](../art/village/scenery/millstone-body.png), [art/village/scenery/millstone-detail.png](../art/village/scenery/millstone-detail.png).

Current step: not started. Process-log events: 0.

### SCN-POWERLESS-ELECTROTHING: Powerless Electrothing

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/powerless-electrothing-body.png](../art/village/scenery/powerless-electrothing-body.png), [art/village/scenery/powerless-electrothing-detail.png](../art/village/scenery/powerless-electrothing-detail.png).

Current step: not started. Process-log events: 0.

### SCN-SEWING-MACHINE: Sewing Machine

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/sewing-machine-body.png](../art/village/scenery/sewing-machine-body.png), [art/village/scenery/sewing-machine-detail.png](../art/village/scenery/sewing-machine-detail.png).

Current step: not started. Process-log events: 0.

### SCN-WOODEN-WATER-WHEEL: Wooden Water Wheel

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/wooden-water-wheel-body.png](../art/village/scenery/wooden-water-wheel-body.png), [art/village/scenery/wooden-water-wheel-detail.png](../art/village/scenery/wooden-water-wheel-detail.png).

Current step: not started. Process-log events: 0.

### SCN-WOODENMECHANICALTRANSMISSION: WoodenMechanicalTransmission

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states; operational/motion states: native metadata study still required; do not invent animations.

Historical artifacts: [art/village/scenery/woodenmechanicaltransmission-body.png](../art/village/scenery/woodenmechanicaltransmission-body.png), [art/village/scenery/woodenmechanicaltransmission-detail.png](../art/village/scenery/woodenmechanicaltransmission-detail.png).

Current step: not started. Process-log events: 0.

### NPC-ARGYVE: Argyve

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-ELDERBOB: Irudad (ElderBob)

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-JOPPAFARMERCONVERT: JoppaFarmerConvert

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-MEHMET: Mehmet

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-NIMA-RUDA: Nima Ruda

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-TAM: Tam

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-WARDEN-YRAME: Warden Yrame

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-WATERVINEFARMERJOPPA-01: WatervineFarmerJoppa / captured resident 1

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-WATERVINEFARMERJOPPA-02: WatervineFarmerJoppa / captured resident 2

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-WATERVINEFARMERJOPPA-03: WatervineFarmerJoppa / captured resident 3

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-WATERVINEFARMERJOPPA-04: WatervineFarmerJoppa / captured resident 4

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-WATERVINEFARMERJOPPA-05: WatervineFarmerJoppa / captured resident 5

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-WATERVINEFARMERJOPPA-06: WatervineFarmerJoppa / captured resident 6

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### NPC-WATERVINEFARMERJOPPA-07: WatervineFarmerJoppa / captured resident 7

Required steps: resolve_individual_race_and_runtime_metadata -> verify_body_and_every_equipped_item_dependencies -> assemble_without_baking_equipment -> review_anatomy_clothing_attachment_all_directions -> review_neutral_and_qud_palette_at_game_scale -> native_visibility_equipment_hurt_look_save_review.

Required views/states: south; east; north; west; neutral/Qud palette; actual equipped outfit; native visible/hidden and supported state.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCN-GARBAGE: Garbage

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/garbage-body.png](../art/village/scenery/garbage-body.png).

Current step: not started. Process-log events: 0.

### SCN-PAINTING: Painting

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/painting-body.png](../art/village/scenery/painting-body.png), [art/village/scenery/painting-detail.png](../art/village/scenery/painting-detail.png).

Current step: not started. Process-log events: 0.

### SCN-SCRAP-ELECTRONICS: Scrap Electronics

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/scrap-metal-body.png](../art/village/scenery/scrap-metal-body.png), [art/village/scenery/scrap-metal-detail.png](../art/village/scenery/scrap-metal-detail.png).

Current step: not started. Process-log events: 0.

### SCN-SCRAP-METAL: Scrap Metal

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/scrap-metal-body.png](../art/village/scenery/scrap-metal-body.png), [art/village/scenery/scrap-metal-detail.png](../art/village/scenery/scrap-metal-detail.png).

Current step: not started. Process-log events: 0.

### SCN-TORCHPOST: Torchpost

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/torchpost-detail.png](../art/village/scenery/torchpost-detail.png).

Current step: not started. Process-log events: 0.

### BODY-DROMAD: dromad

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/dromad/layered/body-east.png](../art/dromad/layered/body-east.png), [art/dromad/layered/body-north.png](../art/dromad/layered/body-north.png), [art/dromad/layered/body-south.png](../art/dromad/layered/body-south.png), [art/dromad/layered/head-detail-east.png](../art/dromad/layered/head-detail-east.png), [art/dromad/layered/head-detail-south.png](../art/dromad/layered/head-detail-south.png), [art/dromad/layered/head-east.png](../art/dromad/layered/head-east.png), [art/dromad/layered/head-north.png](../art/dromad/layered/head-north.png), [art/dromad/layered/head-south.png](../art/dromad/layered/head-south.png), [art/dromad/layered/model.json](../art/dromad/layered/model.json), [art/dromad/nude/refinement.json](../art/dromad/nude/refinement.json), [evidence/dromad-refined-result.json](../evidence/dromad-refined-result.json).

Current step: not started. Process-log events: 0.

### BODY-DROMAD-CHILD: dromad child (featureless body with separate clothing)

Required steps: resolve_age_evidence_and_render_reference -> construct_featureless_front -> generate_other_views -> correct_and_refine_composite -> register_body_head_and_actual_clothing -> visual_review_all_views -> record_native_selection_policy_without_changing_demographics.

Required views/states: male/female templates; shared geometry if no supported distinction; south/east/north; west mirror; separate removable clothing.

Historical artifacts: [art/village/age-templates/dromad/body-east.png](../art/village/age-templates/dromad/body-east.png), [art/village/age-templates/dromad/body-north.png](../art/village/age-templates/dromad/body-north.png), [art/village/age-templates/dromad/body-south.png](../art/village/age-templates/dromad/body-south.png), [art/village/age-templates/dromad/head-east.png](../art/village/age-templates/dromad/head-east.png), [art/village/age-templates/dromad/head-north.png](../art/village/age-templates/dromad/head-north.png), [art/village/age-templates/dromad/head-south.png](../art/village/age-templates/dromad/head-south.png), [art/village/age-templates/dromad/tunic-east.png](../art/village/age-templates/dromad/tunic-east.png), [art/village/age-templates/dromad/tunic-north.png](../art/village/age-templates/dromad/tunic-north.png), [art/village/age-templates/dromad/tunic-south.png](../art/village/age-templates/dromad/tunic-south.png).

Current step: not started. Process-log events: 0.

### BODY-GLOWFISH: glowfish

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/glowfish/body-east.png](../art/village/bodies/glowfish/body-east.png), [art/village/bodies/glowfish/body-north.png](../art/village/bodies/glowfish/body-north.png), [art/village/bodies/glowfish/body-south.png](../art/village/bodies/glowfish/body-south.png), [art/village/bodies/glowfish/model.json](../art/village/bodies/glowfish/model.json), [art/village/bodies/glowfish/turnaround-prompt.txt](../art/village/bodies/glowfish/turnaround-prompt.txt), [art/village/bodies/glowfish/turnaround.png](../art/village/bodies/glowfish/turnaround.png).

Current step: not started. Process-log events: 0.

### BODY-HUMAN-CHILD: human child (featureless body with separate clothing)

Required steps: resolve_age_evidence_and_render_reference -> construct_featureless_front -> generate_other_views -> correct_and_refine_composite -> register_body_head_and_actual_clothing -> visual_review_all_views -> record_native_selection_policy_without_changing_demographics.

Required views/states: male/female templates; shared geometry if no supported distinction; south/east/north; west mirror; separate removable clothing.

Historical artifacts: [art/village/age-templates/human/body-east.png](../art/village/age-templates/human/body-east.png), [art/village/age-templates/human/body-north.png](../art/village/age-templates/human/body-north.png), [art/village/age-templates/human/body-south.png](../art/village/age-templates/human/body-south.png), [art/village/age-templates/human/head-east.png](../art/village/age-templates/human/head-east.png), [art/village/age-templates/human/head-north.png](../art/village/age-templates/human/head-north.png), [art/village/age-templates/human/head-south.png](../art/village/age-templates/human/head-south.png), [art/village/age-templates/human/tunic-east.png](../art/village/age-templates/human/tunic-east.png), [art/village/age-templates/human/tunic-north.png](../art/village/age-templates/human/tunic-north.png), [art/village/age-templates/human/tunic-south.png](../art/village/age-templates/human/tunic-south.png).

Current step: not started. Process-log events: 0.

### BODY-HUMAN-FEMALE: human-female

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/human-female/body-east.png](../art/village/bodies/human-female/body-east.png), [art/village/bodies/human-female/body-north.png](../art/village/bodies/human-female/body-north.png), [art/village/bodies/human-female/body-south.png](../art/village/bodies/human-female/body-south.png), [art/village/bodies/human-female/brief.json](../art/village/bodies/human-female/brief.json), [art/village/bodies/human-female/front.png](../art/village/bodies/human-female/front.png), [art/village/bodies/human-female/front.svg](../art/village/bodies/human-female/front.svg), [art/village/bodies/human-female/head-east.png](../art/village/bodies/human-female/head-east.png), [art/village/bodies/human-female/head-north.png](../art/village/bodies/human-female/head-north.png), [art/village/bodies/human-female/head-south.png](../art/village/bodies/human-female/head-south.png), [art/village/bodies/human-female/model.json](../art/village/bodies/human-female/model.json), [art/village/bodies/human-female/turnaround-prompt.txt](../art/village/bodies/human-female/turnaround-prompt.txt), [art/village/bodies/human-female/turnaround.png](../art/village/bodies/human-female/turnaround.png).

Current step: generation ready; final acceptance pending. Process-log events: 10.

- 2026-10-20T01:05:15.310631+00:00 / resolve_race_description_original_sprite_runtime_anatomy / PASS: Resolved female humans from the captured JoppaFarmerConvert and watervine farmer instances, retaining source descriptions, ancestry, body trees and actual equipment.
  Review: Inspected the packet and reference plate. The body plan is Humanoid with paired feet, two hands and one head; no race-wide nude description exists. Captured gender does not establish mandatory morphology or a life stage.
  Inputs: [{"path": "art/village/sources.json", "sha256": "b0a2de847e29d251f500f81fc25aa3eacec393b4af78370c2a490e9f2706ec22", "role": ""}, {"path": "evidence/joppa-creature-catalogue.json", "sha256": "de8affadee7f4260a8ec68a81e6d6e5f7c98c627a7b29ddcbae3668c6cfd4a79", "role": ""}, {"path": "evidence/village-reference-index.json", "sha256": "cc00cbf6f72d5d4134efb3879d83b30988fcec4ae822cec8a340b072024ca149", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/source-packet.json", "sha256": "0949e4f13981fe60ebc6eb57acc6766066efe506dbcee1b432e274d2a9a1476e", "role": ""}, {"path": "art/conversion/body-human-female/v1/source-comparison.png", "sha256": "24f7a962826da30dfcf88a8fffcadfc3127c2db3c02058fe65b8eed0217e8377", "role": ""}]
  Method/prompt/corrections: {"phase": "Original shapes and captured female human anatomy"}

- 2026-10-20T01:05:15.310896+00:00 / select_actual_core_dlc_or_mod_reference / PASS: Selected exact installed Core Naked_Female_south and Female_Average_Normal_south, retaining the completed male base as the common design family.
  Review: Viewed the actual donor torso and head. Their role is body-type presentation and clean game shading; Qud identity and separate gear remain authoritative.
  Inputs: [{"path": "art/conversion/body-human-female/v1/source-packet.json", "sha256": "0949e4f13981fe60ebc6eb57acc6766066efe506dbcee1b432e274d2a9a1476e", "role": ""}, {"path": "art/conversion/body-human-male/v1/model.json", "sha256": "62eb59d1943b8f64bdcb2503f171bcb6c908e1d72eb24e882de2ef4cfe1a701e", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/source-comparison.png", "sha256": "24f7a962826da30dfcf88a8fffcadfc3127c2db3c02058fe65b8eed0217e8377", "role": ""}]
  Method/prompt/corrections: {"phase": "Female donor convention and shared human reference"}

- 2026-10-20T01:05:15.311216+00:00 / construct_front / PASS: Retained shared human head, arms, hands and explicit bare feet, with a modest authored torso/hip variation based on the donor convention.
  Review: Viewed rendered front: one head, two arms/hands, two legs and two feet; relaxed neutral mannequin. The body variation is an authoring convention, not claimed as native anatomical fact.
  Inputs: [{"path": "art/conversion/body-human-female/v1/source-packet.json", "sha256": "0949e4f13981fe60ebc6eb57acc6766066efe506dbcee1b432e274d2a9a1476e", "role": ""}, {"path": "tools/construct_female_base.py", "sha256": "8c4b08513cbdfa7715b55f585b54d136de7e403135211708dcf2d7ab6c655fc0", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/constructed-front.svg", "sha256": "01c73dd1765553f6b1f56c6c7709a75e9685ae80a112f87bc2c980d78e987ccb", "role": ""}, {"path": "art/conversion/body-human-female/v1/constructed-front.png", "sha256": "b3aad5f65861f16406e12255a9b10ab5766509eb285a7bc7f66e3e4106c73a16", "role": ""}]
  Method/prompt/corrections: {"phase": "Manual front derived from the shared human geometry", "tool": "Python + resvg_py 0.5.0", "settings": "512x1024 transparent editable SVG"}

- 2026-10-20T01:08:28.559814+00:00 / construct_front / RECORDED: Refined the manually constructed shared-family female front. Retained the returned image as an intermediate proposal; its false ankle-cuff lines need correction.
  Review: One head/two arms/hands/two legs and feet retained. Front body belongs to the shared human family. Ankle seams resemble shoe cuffs; request removal with the selected male bare feet as reference in the next proposal.
  Inputs: [{"path": "art/conversion/body-human-female/v1/constructed-front.png", "sha256": "b3aad5f65861f16406e12255a9b10ab5766509eb285a7bc7f66e3e4106c73a16"}, {"path": "art/conversion/body-human-female/v1/source-comparison.png", "sha256": "24f7a962826da30dfcf88a8fffcadfc3127c2db3c02058fe65b8eed0217e8377"}, {"path": "art/conversion/body-human-female/v1/refine-front-prompt.txt", "sha256": "96fc8e9bd14d775cd87fa88f82f1bc82edf44a4c6e4087e7f16cefb5e1398335"}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/refined-front.png", "sha256": "570f48928a16d3384180d56116ac141857caad39796c705e5eeebf0f46820d17"}]
  Method/prompt/corrections: {"phase": "Refined front proposal and foot correction identified", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-9aa37c6c-880b-4b1d-8370-985dac5a807e.png"}

- 2026-10-20T01:10:00.052485+00:00 / imagegen_side_back_from_front_and_race_facts / PASS: Generated female front/side/back from its refined front and the selected male turnaround; explicitly corrected the ankle cuffs and retained modest ordinary contour differences.
  Review: Viewed all three: feet now read as bare feet, side torso/limbs turn together, rear view has heels. No new appendages or cosmetics. Subtle torso/hip curves remain within the shared human design.
  Inputs: [{"path": "art/conversion/body-human-female/v1/refined-front.png", "sha256": "570f48928a16d3384180d56116ac141857caad39796c705e5eeebf0f46820d17"}, {"path": "art/conversion/body-human-male/v1/registered-assembly.png", "sha256": "20883b2586c0045436f258a90e8411eea6909762cda532a6b379fcb3d6e3393a"}, {"path": "art/conversion/body-human-female/v1/secondary-views-prompt.txt", "sha256": "0099a62b1f1d2de86294ccea5f59514076777e0014febbe2f341aef075ecdf2d"}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/secondary-views.png", "sha256": "eff784118096bc294f2eba9274a8a1ae43e0328956a68be7e15df5338c0482e3"}]
  Method/prompt/corrections: {"phase": "Secondary views with the shared male family reference", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-483147ec-540c-40cb-bf57-9418f100a760.png"}

- 2026-10-20T01:10:00.054166+00:00 / correct_anatomy_then_imagegen_refine_composed_views / RECORDED: Removed generated labels, cleared invisible background RGB/low-alpha fringe, converted to equal-channel grayscale and translated feet onto one baseline.
  Review: Viewed the patched sheet. Side foot/arm overlap is coherent; head and body turn, and no ankle cuff remains. No anatomical-count correction needed. Next is the required composed refinement.
  Inputs: [{"path": "art/conversion/body-human-female/v1/secondary-views.png", "sha256": "eff784118096bc294f2eba9274a8a1ae43e0328956a68be7e15df5338c0482e3"}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/patched-views.png", "sha256": "c57b0dbf0143011fe47046f46bf6a4792542791063c6d2db518a6f706636a696"}, {"path": "art/conversion/body-human-female/v1/patch-decisions.json", "sha256": "652463eaedbf66f24d01596f1038a4860902b22907664aa2787be0d6f91cafc1"}]
  Method/prompt/corrections: {"phase": "Patched view registration and neutral source", "tool": "Python Pillow", "settings": {"alpha_clear_below": 16, "alpha_restore_from": 240, "foot_baseline": 950}}

- 2026-10-20T01:12:14.088652+00:00 / correct_anatomy_then_imagegen_refine_composed_views / PASS: Refined the composed patched sheet once, retaining the same human family and modest curves.
  Review: Viewed output: coherent front/side/back, no cuff seams, extra appendages, clothes or cosmetics. Side limb occlusion and foot direction are retained; rear view uses heels.
  Inputs: [{"path": "art/conversion/body-human-female/v1/patched-views.png", "sha256": "c57b0dbf0143011fe47046f46bf6a4792542791063c6d2db518a6f706636a696", "role": ""}, {"path": "art/conversion/body-human-female/v1/refine-patched-prompt.txt", "sha256": "a4d168928b69250f6cedf55f8034044819896e38512221ecb3aea83a86995f43", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/refined-patched-views.png", "sha256": "4e3727c571a2bc475ec0651cfeabee226dd6ad9b48798920a506625641f403b2", "role": ""}]
  Method/prompt/corrections: {"phase": "Refined patched female views", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-6b44fa51-9e8c-45ff-98c7-7cc675355b02.png"}

- 2026-10-20T01:12:14.091040+00:00 / register_required_layers_and_color_masks / PASS: Registered the selected views, cleared invisible RGB, neutralized source shading and split body/head using explicit neck masks with two-pixel body underlap.
  Review: Inspected the recomposed registered image: no neck gaps or cropped hands/feet. Body contains painted limbs; head is separate. No garment or foreign hand outline is baked into an equipment layer. Native use waits for the complete generated set.
  Inputs: [{"path": "art/conversion/body-human-female/v1/refined-patched-views.png", "sha256": "4e3727c571a2bc475ec0651cfeabee226dd6ad9b48798920a506625641f403b2", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/model.json", "sha256": "64dc8143e6d213f6573671a98d5c3dca81208534ecb16b2f31374b0077a1dfc5", "role": ""}, {"path": "art/conversion/body-human-female/v1/registered-assembly.png", "sha256": "35c294224ef070f93701c3212bf7bca823c96c4d06430c0f165a3282d2cb817f", "role": ""}, {"path": "art/conversion/body-human-female/v1/body-south.png", "sha256": "fd424b78b7fb2e45529000f0cc46f53f6eeb55cf5bef87d492ee47db26123f7f", "role": "body / south"}, {"path": "art/conversion/body-human-female/v1/head-south.png", "sha256": "a25fd8f5cf18d52c1ca6a62119dd187da14f8e80b56a6a1e63c02d65602d614b", "role": "head / south"}, {"path": "art/conversion/body-human-female/v1/body-mask-south.png", "sha256": "8dc764e0fb398c7704dcd6235ec00091bcd00bd2d01c3c653b7aa296b334df5d", "role": "body-mask / south"}, {"path": "art/conversion/body-human-female/v1/head-mask-south.png", "sha256": "2c5543c572e49d68cf5bcdaa63aaf42608dd475a1bf89eaa0c8d0ece6a72775f", "role": "head-mask / south"}, {"path": "art/conversion/body-human-female/v1/body-east.png", "sha256": "e1cc2a73198e89fdad1d69751c6852f3fa1e607966c2e621807e22bd9807a56d", "role": "body / east"}, {"path": "art/conversion/body-human-female/v1/head-east.png", "sha256": "c561948d9d19baf6bfa3ece091fb6880f300693f4ae16eaf2561c52f4a3a21d0", "role": "head / east"}, {"path": "art/conversion/body-human-female/v1/body-mask-east.png", "sha256": "68f914b723a56991070b7d4d64caed35942316b0365ffbbca85ebac7ee925b9c", "role": "body-mask / east"}, {"path": "art/conversion/body-human-female/v1/head-mask-east.png", "sha256": "1cd4862169d2b89586983fb122d62c2a9a77e2f00fb521639d56c0f4685e1652", "role": "head-mask / east"}, {"path": "art/conversion/body-human-female/v1/body-north.png", "sha256": "e4c78a288b316853441baf9602b147559e0079b67b27ef391604ac0762b6be0e", "role": "body / north"}, {"path": "art/conversion/body-human-female/v1/head-north.png", "sha256": "b03fbfc93d172d41ff6986f977bc6abb06af0f537b15d3d28130108b665931d3", "role": "head / north"}, {"path": "art/conversion/body-human-female/v1/body-mask-north.png", "sha256": "1f16c2a9d09fafe0e5bff980fb554ff42b170d3b7bde24b0b1aac5fb2055c886", "role": "body-mask / north"}, {"path": "art/conversion/body-human-female/v1/head-mask-north.png", "sha256": "3fa7e08fbe406f06379710b2875636f10a68182ce2ac48f403bf63024345a259", "role": "head-mask / north"}]
  Method/prompt/corrections: {"phase": "Separate female body/head layers and masks", "tool": "Python Pillow", "settings": {"canvas": [512, 1024], "native_body_height": 1.21, "head_mask_top_y": 210, "neck_mask_bottom_y": 242, "body_underlap_pixels": 2}}

- 2026-10-20T01:12:14.091388+00:00 / visual_review_anatomy_orientation_palette_all_views / PASS: Reviewed the registered assembly and intended-size authoring previews. Finished this entry's generation work without native testing.
  Review: Same family as the male human, with modest contour variation. Blank head, two arms/hands, two legs and distinct bare feet. Side turns coherently; rear feet are heels; west mirrors east. Clothing remains separate and its fitting entries are pending.
  Inputs: [{"path": "art/conversion/body-human-female/v1/model.json", "sha256": "64dc8143e6d213f6573671a98d5c3dca81208534ecb16b2f31374b0077a1dfc5", "role": ""}, {"path": "art/conversion/body-human-female/v1/registered-assembly.png", "sha256": "35c294224ef070f93701c3212bf7bca823c96c4d06430c0f165a3282d2cb817f", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-female/v1/game-scale-review.png", "sha256": "d2de21d2e81012f7823f238a30b798c08e969761b88fa65c49a380d4acbfdf20", "role": ""}]
  Method/prompt/corrections: {"phase": "Female base generation-ready"}

- 2026-10-20T01:31:42.340273+00:00 / register_required_layers_and_color_masks / PASS: Translated all body/head/mask layers together to contact (256, 950), preserving v1, dimensions and exact visible source pixels. Replaced facing-dependent horizontal offsets with the shared canvas pivot.
  Review: Viewed all four facings with center/ground guides. Front/back align on the canvas center; side and mirrored side keep the same contact while retaining profile asymmetry. No cut limbs or displaced neck joins. Native movement acceptance remains pending.
  Inputs: [{"path": "art/conversion/body-human-female/v1/model.json", "sha256": "64dc8143e6d213f6573671a98d5c3dca81208534ecb16b2f31374b0077a1dfc5"}, {"path": "tools/center_human_registration.py", "sha256": "16beef95e1ebeee0d7329f250b568c49a1264704c7bebdbefc72ae184ab64cff"}, {"path": "art/conversion/body-human-female/v1/body-south.png", "sha256": "fd424b78b7fb2e45529000f0cc46f53f6eeb55cf5bef87d492ee47db26123f7f"}, {"path": "art/conversion/body-human-female/v1/body-mask-south.png", "sha256": "8dc764e0fb398c7704dcd6235ec00091bcd00bd2d01c3c653b7aa296b334df5d"}, {"path": "art/conversion/body-human-female/v1/head-south.png", "sha256": "a25fd8f5cf18d52c1ca6a62119dd187da14f8e80b56a6a1e63c02d65602d614b"}, {"path": "art/conversion/body-human-female/v1/head-mask-south.png", "sha256": "2c5543c572e49d68cf5bcdaa63aaf42608dd475a1bf89eaa0c8d0ece6a72775f"}, {"path": "art/conversion/body-human-female/v1/body-east.png", "sha256": "e1cc2a73198e89fdad1d69751c6852f3fa1e607966c2e621807e22bd9807a56d"}, {"path": "art/conversion/body-human-female/v1/body-mask-east.png", "sha256": "68f914b723a56991070b7d4d64caed35942316b0365ffbbca85ebac7ee925b9c"}, {"path": "art/conversion/body-human-female/v1/head-east.png", "sha256": "c561948d9d19baf6bfa3ece091fb6880f300693f4ae16eaf2561c52f4a3a21d0"}, {"path": "art/conversion/body-human-female/v1/head-mask-east.png", "sha256": "1cd4862169d2b89586983fb122d62c2a9a77e2f00fb521639d56c0f4685e1652"}, {"path": "art/conversion/body-human-female/v1/body-north.png", "sha256": "e4c78a288b316853441baf9602b147559e0079b67b27ef391604ac0762b6be0e"}, {"path": "art/conversion/body-human-female/v1/body-mask-north.png", "sha256": "1f16c2a9d09fafe0e5bff980fb554ff42b170d3b7bde24b0b1aac5fb2055c886"}, {"path": "art/conversion/body-human-female/v1/head-north.png", "sha256": "b03fbfc93d172d41ff6986f977bc6abb06af0f537b15d3d28130108b665931d3"}, {"path": "art/conversion/body-human-female/v1/head-mask-north.png", "sha256": "3fa7e08fbe406f06379710b2875636f10a68182ce2ac48f403bf63024345a259"}]
  Outputs: [{"path": "art/conversion/body-human-female/v2/body-south.png", "sha256": "a16d522e0f330d76bd3136914eba9c7173ad5598d24f660072a463c3ce7de902"}, {"path": "art/conversion/body-human-female/v2/body-mask-south.png", "sha256": "15fc68744fbe010dcbd9fa07470ae4f83382fed45f1be9682d2abf76fae34a6a"}, {"path": "art/conversion/body-human-female/v2/head-south.png", "sha256": "faa3bc3220fe2db08794e0e6b77b7c2795757468306249a13121e8530a5585b8"}, {"path": "art/conversion/body-human-female/v2/head-mask-south.png", "sha256": "85cea5822341c4c591a8c2a511315408b29db4d8447fb041244f3467aba30c45"}, {"path": "art/conversion/body-human-female/v2/selected-south.png", "sha256": "4be9af44baa01447c0dfaa23abe8c93cd98218aafd681885987c793d62b039e6"}, {"path": "art/conversion/body-human-female/v2/body-east.png", "sha256": "10c46567247cf069b63f68ae546c9b247149a7ab2d141516c85f4e94b24f1dc7"}, {"path": "art/conversion/body-human-female/v2/body-mask-east.png", "sha256": "3599d2f6d099570b72aeb381a7bfe03aaa9ef0b055cd3c2b04bbace68341d22e"}, {"path": "art/conversion/body-human-female/v2/head-east.png", "sha256": "2ba5b17a0e1afd5ff7b2752c21f2b7effe0cdd715dd2de297c9cd891956ee511"}, {"path": "art/conversion/body-human-female/v2/head-mask-east.png", "sha256": "f17c12f4a0b3e8b1c9863313d7464633a671bcb1e7b3643774f421ec0ee226d9"}, {"path": "art/conversion/body-human-female/v2/selected-east.png", "sha256": "a71914893266ae414176d760e0e1560b399834469f840f3d2cc2e2c5bd7e5762"}, {"path": "art/conversion/body-human-female/v2/body-north.png", "sha256": "f56d658f1e9cb36f9b1f44766ab8e5d95157a83009a848730e8927fd832d3d30"}, {"path": "art/conversion/body-human-female/v2/body-mask-north.png", "sha256": "475ef61e238fd6fa6492d20f33538194175cdd9990b48e97d50b3b83c8026846"}, {"path": "art/conversion/body-human-female/v2/head-north.png", "sha256": "894d6930977186ca62f3bcf681242ee3f8131fbcff7136cb8f927dc459eec637"}, {"path": "art/conversion/body-human-female/v2/head-mask-north.png", "sha256": "7a58309fefcef7f53abf9b6744b2077ee59b029fda7b482df54d9795e0b1c3a9"}, {"path": "art/conversion/body-human-female/v2/selected-north.png", "sha256": "62c7e1757d8301a8528f3c298a60e9dcc8ce2a7664871e287236a8db69104979"}, {"path": "art/conversion/body-human-female/v2/model.json", "sha256": "d98a479b61e27de71f0a616e400a53ea88ddcff1adce25ea90056e83c140c09b"}, {"path": "art/conversion/body-human-female/v2/registration-decisions.json", "sha256": "b5ef422bf378d890349ac22a708d389a93a68659728d2b5bca511db7ad5fba1d"}, {"path": "art/conversion/body-human-female/v2/registration-comparison.png", "sha256": "b91dddc5eac7c2bc72dc6008ffcc91aa7df706aa3b608981d4800e0dfc972a9a"}]
  Method/prompt/corrections: {"phase": "Shared centered canvas registration v2"}

### BODY-HUMAN-MALE: human-male

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/human-male/body-east.png](../art/village/bodies/human-male/body-east.png), [art/village/bodies/human-male/body-north.png](../art/village/bodies/human-male/body-north.png), [art/village/bodies/human-male/body-south.png](../art/village/bodies/human-male/body-south.png), [art/village/bodies/human-male/brief.json](../art/village/bodies/human-male/brief.json), [art/village/bodies/human-male/front.png](../art/village/bodies/human-male/front.png), [art/village/bodies/human-male/front.svg](../art/village/bodies/human-male/front.svg), [art/village/bodies/human-male/head-east.png](../art/village/bodies/human-male/head-east.png), [art/village/bodies/human-male/head-north.png](../art/village/bodies/human-male/head-north.png), [art/village/bodies/human-male/head-south.png](../art/village/bodies/human-male/head-south.png), [art/village/bodies/human-male/model.json](../art/village/bodies/human-male/model.json), [art/village/bodies/human-male/turnaround-prompt.txt](../art/village/bodies/human-male/turnaround-prompt.txt), [art/village/bodies/human-male/turnaround.png](../art/village/bodies/human-male/turnaround.png).

Current step: generation ready; final acceptance pending. Process-log events: 13.

- 2026-10-20T00:49:23.267686+00:00 / resolve_race_description_original_sprite_runtime_anatomy / PASS: Resolved Argyve, Mehmet and captured male watervine farmers to reusable human anatomy. Preserved individual descriptions, attached native body trees, actual gear, source hashes and uncertainty.
  Review: Inspected the exact metadata and contextual source plate. Two arms, two hands and paired feet; no native race-wide appearance prose. The original clothed sprite is not a nude anatomy diagram.
  Inputs: [{"path": "art/village/sources.json", "sha256": "b0a2de847e29d251f500f81fc25aa3eacec393b4af78370c2a490e9f2706ec22", "role": "Observed native definitions and parts"}, {"path": "evidence/joppa-creature-catalogue.json", "sha256": "de8affadee7f4260a8ec68a81e6d6e5f7c98c627a7b29ddcbae3668c6cfd4a79", "role": "Source-bound species catalogue"}, {"path": "evidence/village-reference-index.json", "sha256": "cc00cbf6f72d5d4134efb3879d83b30988fcec4ae822cec8a340b072024ca149", "role": "Original sprite identities"}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/source-packet.json", "sha256": "4cf5319cc280332acf3f9fcae315c1e298868cee108f972d656685c93fce57d6", "role": "Exact source packet and authored anatomy contract"}, {"path": "art/conversion/body-human-male/v1/source-comparison.png", "sha256": "75421f2e6f2bdaac37601f124f2058094440b4315b6c4b70b7f181a8ef1f1a1b", "role": "Annotated Qud original shapes alongside donor conventions"}]
  Method/prompt/corrections: {"phase": "Original shape and body metadata"}

- 2026-10-20T00:49:23.267847+00:00 / select_actual_core_dlc_or_mod_reference / PASS: Selected installed Core Naked_Male_south and Male_Average_Normal_south for presentation only. Verified the extracted PNG hashes against the recorded catalogue; DLC/mod references remain eligible for subjects that need them.
  Review: Viewed donor torso/head reference. Ordinary donor humanlike body has no independent rendered arms/legs; this Qud body keeps them painted into the body graphic. No donor race substitution.
  Inputs: [{"path": "art/conversion/body-human-male/v1/source-packet.json", "sha256": "4cf5319cc280332acf3f9fcae315c1e298868cee108f972d656685c93fce57d6", "role": "Exact donor IDs/hashes and role"}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/source-comparison.png", "sha256": "75421f2e6f2bdaac37601f124f2058094440b4315b6c4b70b7f181a8ef1f1a1b", "role": "Contextual source/reference comparison"}]
  Method/prompt/corrections: {"phase": "RimWorld reference decision"}

- 2026-10-20T00:49:23.268142+00:00 / construct_front / PASS: Constructed original editable adult front with two visible arms/hands, paired legs and explicit rounded bare feet. Preserved the non-detailed neutral mannequin convention; personal cosmetics and occupation gear remain separate.
  Review: Viewed the rendered PNG: one head, two arms/hands, two legs and two distinct feet. Foot overlap/ankle contours still require the refinement review. This passes construction only, not final body or native acceptance.
  Inputs: [{"path": "art/conversion/body-human-male/v1/source-packet.json", "sha256": "4cf5319cc280332acf3f9fcae315c1e298868cee108f972d656685c93fce57d6", "role": "Anatomy and design contract"}, {"path": "tools/construct_human_base.py", "sha256": "c0edbb92f78c930c49a4328137a7606706b2ff1bfd49c3669b743de15f0cf1dc", "role": "Exact geometry and plate construction method"}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/constructed-front.svg", "sha256": "618d5e12a3c6fdfec84456655ea1a3217d60cdb4168ce7722b6c56ce47c0c84c", "role": "Editable source geometry"}, {"path": "art/conversion/body-human-male/v1/constructed-front.png", "sha256": "f4ccc3be23caca549954021f28af47086157e46fb225f868a5f6c6ccf0e3fd15", "role": "Rendered manual front suggestion"}]
  Method/prompt/corrections: {"phase": "Manual front suggestion", "tool": "Python + resvg_py 0.5.0", "settings": "512x1024 transparent SVG render; deterministic authored geometry"}

- 2026-10-20T00:50:32.619990+00:00 / construct_front / PASS: Refined only the constructed front with built-in ImageGen, using the manual front and the inspected source/reference plate.
  Review: Viewed full output: one blank head, two arms/hands, two legs and distinct short bare feet with toes. Foot stubs corrected. Neutral low-chroma gray; exact alpha inspected. No clothes or personal cosmetics. Front selected as the next view-generation anchor, not final native art.
  Inputs: [{"path": "art/conversion/body-human-male/v1/constructed-front.png", "sha256": "f4ccc3be23caca549954021f28af47086157e46fb225f868a5f6c6ccf0e3fd15"}, {"path": "art/conversion/body-human-male/v1/source-comparison.png", "sha256": "75421f2e6f2bdaac37601f124f2058094440b4315b6c4b70b7f181a8ef1f1a1b"}, {"path": "art/conversion/body-human-male/v1/refine-front-prompt.txt", "sha256": "508479e64f8cd2a5600b6ee7f4c15aa55558ea6aef0dd02a7e4ef5b01ee5b87c"}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/refined-front.png", "sha256": "68948433e0d49fcae6e6cb6de75c8ee3e7bf102f2b1114479ffd5e8063f2eafd"}]
  Method/prompt/corrections: {"phase": "Refined front suggestion", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-9e08c9ab-9d61-47ee-a74a-eb3571e45f4e.png"}

- 2026-10-20T00:52:22.047183+00:00 / imagegen_side_back_from_front_and_race_facts / PASS: Generated the same adult body in front, right-facing side and back using only the reviewed refined front plus explicit anatomy facts.
  Review: Viewed the raw sheet. Side body/legs/foot rotate coherently and far limbs are occluded. Back has no face features or front toes. Proposal changes the front slightly and low-chroma fill/alpha still require controlled cleanup.
  Inputs: [{"path": "art/conversion/body-human-male/v1/refined-front.png", "sha256": "68948433e0d49fcae6e6cb6de75c8ee3e7bf102f2b1114479ffd5e8063f2eafd", "role": ""}, {"path": "art/conversion/body-human-male/v1/secondary-views-prompt.txt", "sha256": "abd015f6e250f394157c669fee5aa6f1d3acf71be795c419c885e92c0bdace86", "role": ""}, {"path": "art/conversion/body-human-male/v1/source-packet.json", "sha256": "4cf5319cc280332acf3f9fcae315c1e298868cee108f972d656685c93fce57d6", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/secondary-views.png", "sha256": "f75108d6aad2e2be1a2b7a5b3beb6ffb22e317774716307fd13600de6b36308f", "role": "Raw proposed turnaround, including generated labels"}]
  Method/prompt/corrections: {"phase": "Secondary views proposed from the front", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-bf36edf1-fb52-468f-96b5-34557aca3c02.png"}

- 2026-10-20T00:52:22.049107+00:00 / correct_anatomy_then_imagegen_refine_composed_views / RECORDED: Restored selected front, cleared labels, normalized neutral grayscale and alpha, and aligned foot contact. No anatomy-count patch was necessary; the side silhouette supports occluded far limbs.
  Review: Inspected patched sheet: feet visible in every applicable direction, genuine side profile, no background or labels in sprite panels. Back head/torso breadth consistency is explicitly requested in the composed refinement.
  Inputs: [{"path": "art/conversion/body-human-male/v1/refined-front.png", "sha256": "68948433e0d49fcae6e6cb6de75c8ee3e7bf102f2b1114479ffd5e8063f2eafd", "role": ""}, {"path": "art/conversion/body-human-male/v1/secondary-views.png", "sha256": "f75108d6aad2e2be1a2b7a5b3beb6ffb22e317774716307fd13600de6b36308f", "role": ""}, {"path": "tools/patch_human_turnaround.py", "sha256": "84208fe5367aad46134dc12b41a88bc44656aebf11e2c8de2100783a21317dcb", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/patched-views.png", "sha256": "4ec47fba8771fb45c8f22bd00a2ace36c9ba97001132dee1a24464c72d57bfc6", "role": "Patched front / side / back"}, {"path": "art/conversion/body-human-male/v1/patch-decisions.json", "sha256": "e56bd97b0ab68c42a1f6aae9aeb09636d3438d284e0c1f2f201e27b2998d2c00", "role": "Exact patch regions and registration decisions"}]
  Method/prompt/corrections: {"phase": "Patched views before composed refinement", "tool": "Python Pillow", "settings": {"alpha_clear_below": 16, "alpha_restore_from": 240, "neutral": "equal RGB luminance", "foot_baseline": 930}}

- 2026-10-20T00:55:48.198028+00:00 / correct_anatomy_then_imagegen_refine_composed_views / PASS: Refined the composed patched sheet once, preserving count, directions and bare feet; selected its coherent three-view result.
  Review: Viewed the complete returned sheet: one head/two arms/hands/two legs/feet; side is a full-body profile and back shows heels rather than front toes. Front/back head and torso remain the same body family. Raw transparent pixels carry irrelevant background RGB; registration explicitly clears it.
  Inputs: [{"path": "art/conversion/body-human-male/v1/patched-views.png", "sha256": "4ec47fba8771fb45c8f22bd00a2ace36c9ba97001132dee1a24464c72d57bfc6", "role": ""}, {"path": "art/conversion/body-human-male/v1/refine-patched-prompt.txt", "sha256": "cf04ed7b85464b4dc080bae2d7807b1852cef602b4946db67079e724453e558f", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/refined-patched-views.png", "sha256": "5678c33fb1561c1c1f88a89c07fc5605aa9433e97023bd3c0bf321ea4b14cc25", "role": "Raw composed refinement"}]
  Method/prompt/corrections: {"phase": "Refined patched views", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-20ed3e12-9f2f-43b4-bb61-88d4fdfd1523.png"}

- 2026-10-20T00:55:48.200669+00:00 / register_required_layers_and_color_masks / PASS: Registered selected views to physical contact, converted source to true grayscale, split body/head with explicit masks and a two-pixel body underlap. Prepared an isolated native contract.
  Review: Viewed registered assembly and normal-size authoring sheet. Recomposition preserves the body and neck; no separate limb nodes added. Source pixels have equal RGB channels, with body/head under native foreground tint. Historical clothing remains unaccepted and is not regenerated by this body entry.
  Inputs: [{"path": "art/conversion/body-human-male/v1/refined-patched-views.png", "sha256": "5678c33fb1561c1c1f88a89c07fc5605aa9433e97023bd3c0bf321ea4b14cc25", "role": ""}, {"path": "tools/register_human_base.py", "sha256": "c246de68cf5c364d589062ce6e8e670bafbc491ab9b9b41e0f36753d78657676", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/model.json", "sha256": "62eb59d1943b8f64bdcb2503f171bcb6c908e1d72eb24e882de2ef4cfe1a701e", "role": "Exact layer registration and palette contract"}, {"path": "art/conversion/body-human-male/v1/registered-assembly.png", "sha256": "20883b2586c0045436f258a90e8411eea6909762cda532a6b379fcb3d6e3393a", "role": "Recomposed registered front / side / back"}, {"path": "art/conversion/body-human-male/v1/body-mask-south.png", "sha256": "0c15a4c60887019c8b12466a1dce728928ede488409997784c9842f92b323934", "role": "body ownership mask / south"}, {"path": "art/conversion/body-human-male/v1/head-mask-south.png", "sha256": "91ab4a405e9611f8a388429ac1ee81ea6654fe511b051d805021a50877112d68", "role": "head ownership mask / south"}, {"path": "art/conversion/body-human-male/v1/body-mask-east.png", "sha256": "d48a0b98139f37e38d67ccc9ebca99f4b01f598ae2dac8aff23679e7fd4ac742", "role": "body ownership mask / east"}, {"path": "art/conversion/body-human-male/v1/head-mask-east.png", "sha256": "442f20d565ab7c3c89e4c726229b2c302caa0274356314ffd609308746b13ef2", "role": "head ownership mask / east"}, {"path": "art/conversion/body-human-male/v1/body-mask-north.png", "sha256": "946f68c27c39d659f7c7e7e49c6a83ef923cf79a739af15202544307a3ce7750", "role": "body ownership mask / north"}, {"path": "art/conversion/body-human-male/v1/head-mask-north.png", "sha256": "4422afeba5826c44683aeeb7630fd2fd310b79f0fe6bf26589919014caaf7b85", "role": "head ownership mask / north"}]
  Method/prompt/corrections: {"phase": "Registered body, head and explicit masks", "tool": "Python Pillow", "settings": {"body_height_world": 1.21, "head_body_underlap_pixels": 2, "body_contains_limbs": true}}

- 2026-10-20T00:55:48.201291+00:00 / visual_review_anatomy_orientation_palette_all_views / RECORDED: Reviewed the same registered model at 48x96 and 2x nearest display; native captures are still pending.
  Review: Feet remain visible and side foot points right. No shoulder/neck holes or extra hands. The entry remains IN PROGRESS until the real native body evidence and current bindings are reviewed.
  Inputs: [{"path": "art/conversion/body-human-male/v1/model.json", "sha256": "62eb59d1943b8f64bdcb2503f171bcb6c908e1d72eb24e882de2ef4cfe1a701e", "role": ""}, {"path": "art/conversion/body-human-male/v1/registered-assembly.png", "sha256": "20883b2586c0045436f258a90e8411eea6909762cda532a6b379fcb3d6e3393a", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/game-scale-review.png", "sha256": "dfcd88d79635ba81e432ed2340917c121264ea1d4526655b66d5953f38d822d8", "role": "Authoring-scale review, not native footage"}]
  Method/prompt/corrections: {"phase": "Authoring-scale review before native acceptance"}

- 2026-10-20T01:00:03.908420+00:00 / native_body_review / FAIL: Ran isolated hidden native Qud with the registered human body. Four-facing captures rendered, but the existing diagnostic rejected a completed hurt reaction for missing its narrow midpoint window; save/load was not reached.
  Review: Failure inspected. Actual hurt start/end exist; no claim of a passing batch or save/load. Diagnostic is corrected without changing animation timing, then a new isolated run will verify completion.
  Inputs: [{"path": "art/conversion/body-human-male/v1/native-contract.json", "sha256": "cd588e2e566d2a816a733c67d187670742fc14dfddc6f6d1dbdabb320ce68d4b"}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/native-attempt-01.json", "sha256": "db4fd1f1529749bb9c634601352b1ec02ad15b520a74add9b809a9d640331f3d"}]
  Method/prompt/corrections: {"phase": "Native attempt 01: retained diagnostic failure"}

- 2026-10-20T01:02:52.068448+00:00 / native_body_review / DEFERRED UNTIL ALL GENERATED: User requires generation of all pending textures, objects and creatures before native validation. The already-running second probe exited; no new probe will be started. Reverted the diagnostic code change and retained the existing generated artwork.
  Review: No validation acceptance or completion credit assigned. Resume generation and its visual corrections. Native checks remain pending until the all-conversions gate.
  Inputs: []
  Outputs: []
  Method/prompt/corrections: {"phase": "Validation deferred by user instruction"}

- 2026-10-20T01:05:15.309900+00:00 / visual_review_anatomy_orientation_palette_all_views / PASS: Concluded visual authoring review of the registered neutral model, including explicit feet and whole-body side orientation. Native acceptance is intentionally pending until all conversions are generated.
  Review: Body/head layers recompose without a neck gap. Two arms/hands and paired feet are retained; east is a genuine profile, north has rear heels, west uses the documented east mirror. Equal RGB channels preserve neutral source tint. Clothing fitting belongs to the separate fitting entries.
  Inputs: [{"path": "art/conversion/body-human-male/v1/model.json", "sha256": "62eb59d1943b8f64bdcb2503f171bcb6c908e1d72eb24e882de2ef4cfe1a701e", "role": ""}, {"path": "art/conversion/body-human-male/v1/registered-assembly.png", "sha256": "20883b2586c0045436f258a90e8411eea6909762cda532a6b379fcb3d6e3393a", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male/v1/game-scale-review.png", "sha256": "dfcd88d79635ba81e432ed2340917c121264ea1d4526655b66d5953f38d822d8", "role": ""}]
  Method/prompt/corrections: {"phase": "Authoring complete: shared human male base"}

- 2026-10-20T01:31:29.305480+00:00 / register_required_layers_and_color_masks / PASS: Translated body, head and segmentation masks together to contact (256, 950) on unchanged 512 x 1024 canvases. Preserved v1 and replaced compensating horizontal render offsets with a common canvas pivot. No resizing or native testing.
  Review: Viewed front, side, back and mirrored west with guides: shared horizontal center and ground contact, complete hands/feet and unchanged head/body joins. Exact source pixels inside art bounds survive translation; full-canvas mask padding clips only outside visible art. Side profile retains natural asymmetry.
  Inputs: [{"path": "art/conversion/body-human-male/v1/model.json", "sha256": "62eb59d1943b8f64bdcb2503f171bcb6c908e1d72eb24e882de2ef4cfe1a701e"}, {"path": "tools/center_human_registration.py", "sha256": "16beef95e1ebeee0d7329f250b568c49a1264704c7bebdbefc72ae184ab64cff"}, {"path": "art/conversion/body-human-male/v1/body-south.png", "sha256": "10f4f1aed4788afe28e3a9af63b4efa3d52c2286022075a9fd2d30bea298f061"}, {"path": "art/conversion/body-human-male/v1/body-mask-south.png", "sha256": "0c15a4c60887019c8b12466a1dce728928ede488409997784c9842f92b323934"}, {"path": "art/conversion/body-human-male/v1/head-south.png", "sha256": "eebe09d48114fce7ce76d08afa684200f9912573e4268437b9efa5e10bfc777a"}, {"path": "art/conversion/body-human-male/v1/head-mask-south.png", "sha256": "91ab4a405e9611f8a388429ac1ee81ea6654fe511b051d805021a50877112d68"}, {"path": "art/conversion/body-human-male/v1/body-east.png", "sha256": "31c4f1e51880a225275c38389f6ac31d8512317c8787ede7c33e184692659dd5"}, {"path": "art/conversion/body-human-male/v1/body-mask-east.png", "sha256": "d48a0b98139f37e38d67ccc9ebca99f4b01f598ae2dac8aff23679e7fd4ac742"}, {"path": "art/conversion/body-human-male/v1/head-east.png", "sha256": "8ff86ae187d5cf612b48fb4938469f09f037ec066da4def773c529dabf31e29b"}, {"path": "art/conversion/body-human-male/v1/head-mask-east.png", "sha256": "442f20d565ab7c3c89e4c726229b2c302caa0274356314ffd609308746b13ef2"}, {"path": "art/conversion/body-human-male/v1/body-north.png", "sha256": "ca8d56852784783c4900311d66bda6da2d0afe9f2167e8285f4012f48e524b69"}, {"path": "art/conversion/body-human-male/v1/body-mask-north.png", "sha256": "946f68c27c39d659f7c7e7e49c6a83ef923cf79a739af15202544307a3ce7750"}, {"path": "art/conversion/body-human-male/v1/head-north.png", "sha256": "5fade74e67ccef9c2d93b267716e21f4185f6c628239eda44c708127d129a0e6"}, {"path": "art/conversion/body-human-male/v1/head-mask-north.png", "sha256": "4422afeba5826c44683aeeb7630fd2fd310b79f0fe6bf26589919014caaf7b85"}]
  Outputs: [{"path": "art/conversion/body-human-male/v2/body-south.png", "sha256": "37833fb63565d9af0e01fa1f5f2986de097761bc0b534a6ed2aebc042cd96b57"}, {"path": "art/conversion/body-human-male/v2/body-mask-south.png", "sha256": "95f3d42db6b738ad0a8f16a33211ae545ae230ea8f6e72abb49c5da478b61fbe"}, {"path": "art/conversion/body-human-male/v2/head-south.png", "sha256": "9ed0324137804609c9c0e8b430af17d3d2c90f645669f4f9844e2a67903a7b05"}, {"path": "art/conversion/body-human-male/v2/head-mask-south.png", "sha256": "0b71145761180ce50a5fe2d07f6264a34091ffa8642620f7c88965d3b12a1cd7"}, {"path": "art/conversion/body-human-male/v2/selected-south.png", "sha256": "16f2266b29a1fcccb5a44bcf5b8cfea4953fa1ce7e595724cfca9873ee971bd1"}, {"path": "art/conversion/body-human-male/v2/body-east.png", "sha256": "10c7b8fbc8118fd46e208c093d4d975eefcbb36c1e74b7840f6de67f0e26f860"}, {"path": "art/conversion/body-human-male/v2/body-mask-east.png", "sha256": "3608d456aad367c705c6177bbee7b04887f9da8747eb6bab9f088c4ac9fc90c7"}, {"path": "art/conversion/body-human-male/v2/head-east.png", "sha256": "a27cc8e70ed2e46845ea844b748af133a34eb8ebb660fbc1816815cd74d18fa0"}, {"path": "art/conversion/body-human-male/v2/head-mask-east.png", "sha256": "eacc182e21ac26760405cc02a623beaf4b199c12cee72592422df6cbceabfba6"}, {"path": "art/conversion/body-human-male/v2/selected-east.png", "sha256": "24705a71b541a8b416a12ca12a0b7587e4b31082c94a5dbdefd44f0f272a2f56"}, {"path": "art/conversion/body-human-male/v2/body-north.png", "sha256": "328499003f02e2d3e4d4792c2e53ac8522896afa3050da5f18a3d6c505de32ee"}, {"path": "art/conversion/body-human-male/v2/body-mask-north.png", "sha256": "178c8866f8bba7baaea91180f6faf229784bfeba720c810eaa019b725603d5d0"}, {"path": "art/conversion/body-human-male/v2/head-north.png", "sha256": "6025b82030de0122cc32787913ce6fce720d88c8131963a477dfee8d335bb7ee"}, {"path": "art/conversion/body-human-male/v2/head-mask-north.png", "sha256": "cd78bb7e39a7f7626a5ac7da9df8d0e067ec560e4ea0b69a8b605e29c62d780c"}, {"path": "art/conversion/body-human-male/v2/selected-north.png", "sha256": "4fe07f85bc1f472241a2c22d089b8c4bdf70dc168ca916c077c463140a36cd8c"}, {"path": "art/conversion/body-human-male/v2/model.json", "sha256": "a9b6a4b5fab6115794251297bc91dc0e8fce30c2be9835704807b2ab73d535d4"}, {"path": "art/conversion/body-human-male/v2/registration-decisions.json", "sha256": "a34709e348b21b170c753fdb35a87d50bd2cf76d4362305cc5d11eef6bd8d87a"}, {"path": "art/conversion/body-human-male/v2/registration-comparison.png", "sha256": "db04fd4395d5268029e9fed095bd208d050350e7ba1b5b7fd966ac810b881c3f"}]
  Method/prompt/corrections: {"phase": "Shared centered canvas registration v2"}

### BODY-IRUDAD: irudad

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/irudad/body-east.png](../art/village/bodies/irudad/body-east.png), [art/village/bodies/irudad/body-north.png](../art/village/bodies/irudad/body-north.png), [art/village/bodies/irudad/body-south.png](../art/village/bodies/irudad/body-south.png), [art/village/bodies/irudad/brief.json](../art/village/bodies/irudad/brief.json), [art/village/bodies/irudad/front.png](../art/village/bodies/irudad/front.png), [art/village/bodies/irudad/front.svg](../art/village/bodies/irudad/front.svg), [art/village/bodies/irudad/head-east.png](../art/village/bodies/irudad/head-east.png), [art/village/bodies/irudad/head-north.png](../art/village/bodies/irudad/head-north.png), [art/village/bodies/irudad/head-south.png](../art/village/bodies/irudad/head-south.png), [art/village/bodies/irudad/model.json](../art/village/bodies/irudad/model.json), [art/village/bodies/irudad/refinement-prompt.txt](../art/village/bodies/irudad/refinement-prompt.txt), [art/village/bodies/irudad/turnaround-draft.png](../art/village/bodies/irudad/turnaround-draft.png), [art/village/bodies/irudad/turnaround-prompt.txt](../art/village/bodies/irudad/turnaround-prompt.txt), [art/village/bodies/irudad/turnaround.png](../art/village/bodies/irudad/turnaround.png).

Current step: not started. Process-log events: 0.

### BODY-NIMA: nima

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/nima/body-east.png](../art/village/bodies/nima/body-east.png), [art/village/bodies/nima/body-north.png](../art/village/bodies/nima/body-north.png), [art/village/bodies/nima/body-south.png](../art/village/bodies/nima/body-south.png), [art/village/bodies/nima/brief.json](../art/village/bodies/nima/brief.json), [art/village/bodies/nima/front.png](../art/village/bodies/nima/front.png), [art/village/bodies/nima/front.svg](../art/village/bodies/nima/front.svg), [art/village/bodies/nima/head-east.png](../art/village/bodies/nima/head-east.png), [art/village/bodies/nima/head-north.png](../art/village/bodies/nima/head-north.png), [art/village/bodies/nima/head-south.png](../art/village/bodies/nima/head-south.png), [art/village/bodies/nima/model.json](../art/village/bodies/nima/model.json), [art/village/bodies/nima/refinement-prompt.txt](../art/village/bodies/nima/refinement-prompt.txt), [art/village/bodies/nima/turnaround-draft.png](../art/village/bodies/nima/turnaround-draft.png), [art/village/bodies/nima/turnaround-prompt.txt](../art/village/bodies/nima/turnaround-prompt.txt), [art/village/bodies/nima/turnaround.png](../art/village/bodies/nima/turnaround.png).

Current step: not started. Process-log events: 0.

### BODY-RAY-CAT: ray-cat

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/ctesiphus/east-albedo.png](../art/ctesiphus/east-albedo.png), [art/ctesiphus/north-albedo.png](../art/ctesiphus/north-albedo.png), [art/ctesiphus/preview.html](../art/ctesiphus/preview.html), [art/ctesiphus/south-albedo.png](../art/ctesiphus/south-albedo.png), [evidence/faithful-cat-result.json](../evidence/faithful-cat-result.json).

Current step: not started. Process-log events: 0.

### BODY-YRAME: yrame

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/yrame/body-east.png](../art/village/bodies/yrame/body-east.png), [art/village/bodies/yrame/body-north.png](../art/village/bodies/yrame/body-north.png), [art/village/bodies/yrame/body-south.png](../art/village/bodies/yrame/body-south.png), [art/village/bodies/yrame/brief.json](../art/village/bodies/yrame/brief.json), [art/village/bodies/yrame/four-feet-east.png](../art/village/bodies/yrame/four-feet-east.png), [art/village/bodies/yrame/four-feet-east.svg](../art/village/bodies/yrame/four-feet-east.svg), [art/village/bodies/yrame/four-feet-north.png](../art/village/bodies/yrame/four-feet-north.png), [art/village/bodies/yrame/four-feet-north.svg](../art/village/bodies/yrame/four-feet-north.svg), [art/village/bodies/yrame/four-feet-south.png](../art/village/bodies/yrame/four-feet-south.png), [art/village/bodies/yrame/four-feet-south.svg](../art/village/bodies/yrame/four-feet-south.svg), [art/village/bodies/yrame/front.png](../art/village/bodies/yrame/front.png), [art/village/bodies/yrame/front.svg](../art/village/bodies/yrame/front.svg), [art/village/bodies/yrame/head-east.png](../art/village/bodies/yrame/head-east.png), [art/village/bodies/yrame/head-north.png](../art/village/bodies/yrame/head-north.png), [art/village/bodies/yrame/head-south.png](../art/village/bodies/yrame/head-south.png), [art/village/bodies/yrame/model.json](../art/village/bodies/yrame/model.json), [art/village/bodies/yrame/refinement-prompt.txt](../art/village/bodies/yrame/refinement-prompt.txt), [art/village/bodies/yrame/turnaround-draft.png](../art/village/bodies/yrame/turnaround-draft.png), [art/village/bodies/yrame/turnaround-prompt.txt](../art/village/bodies/yrame/turnaround-prompt.txt), [art/village/bodies/yrame/turnaround-rejected-three-feet.png](../art/village/bodies/yrame/turnaround-rejected-three-feet.png).

Current step: not started. Process-log events: 0.

### SCN-ARGYVESIGN: ArgyveSign

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/argyvesign-body.png](../art/village/scenery/argyvesign-body.png), [art/village/scenery/argyvesign-detail.png](../art/village/scenery/argyvesign-detail.png).

Current step: not started. Process-log events: 0.

### SCN-JOPPAMILLSIGN: JoppaMillSign

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/peppersign2-body.png](../art/village/scenery/peppersign2-body.png), [art/village/scenery/peppersign2-detail.png](../art/village/scenery/peppersign2-detail.png).

Current step: not started. Process-log events: 0.

### SCN-JOPPANORTHSIGN: JoppaNorthSign

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/joppanorthsign-body.png](../art/village/scenery/joppanorthsign-body.png), [art/village/scenery/joppanorthsign-detail.png](../art/village/scenery/joppanorthsign-detail.png).

Current step: not started. Process-log events: 0.

### SCN-JOPPARESHEPHSHRINE: JoppaReshephShrine

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/joppareshephshrine-body.png](../art/village/scenery/joppareshephshrine-body.png), [art/village/scenery/joppareshephshrine-detail.png](../art/village/scenery/joppareshephshrine-detail.png).

Current step: not started. Process-log events: 0.

### SCN-PEPPERSIGN2: PepperSign2

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/peppersign2-body.png](../art/village/scenery/peppersign2-body.png), [art/village/scenery/peppersign2-detail.png](../art/village/scenery/peppersign2-detail.png).

Current step: not started. Process-log events: 0.

### SCN-TAMSIGN: TamSign

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/tamsign-body.png](../art/village/scenery/tamsign-body.png), [art/village/scenery/tamsign-detail.png](../art/village/scenery/tamsign-detail.png).

Current step: not started. Process-log events: 0.

### TILE-GRASS-1: Basic Grass 1

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: source/exclusion review.

Historical artifacts: [art/village/scenery/basic-grass.png](../art/village/scenery/basic-grass.png).

Current step: not started. Process-log events: 0.

### TILE-GRASS-2: Basic Grass 2

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### TILE-GRASS-3: Basic Grass 3

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: source/exclusion review.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### TILE-SOIL: bare soil/interior ground

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: seamless material; native palette; edge/depth transitions where applicable.

Historical artifacts: [art/village/scenery/surface-soil.png](../art/village/scenery/surface-soil.png).

Current step: not started. Process-log events: 0.

### TILE-WATER-DEEP: deep/swimming water

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: seamless material; native palette; edge/depth transitions where applicable.

Historical artifacts: [art/village/scenery/surface-water-deep.png](../art/village/scenery/surface-water-deep.png).

Current step: not started. Process-log events: 0.

### TILE-MARSH: marsh/grass ground

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: seamless material; native palette; edge/depth transitions where applicable.

Historical artifacts: [art/village/scenery/surface-marsh.png](../art/village/scenery/surface-marsh.png).

Current step: not started. Process-log events: 0.

### TILE-SAND: path surface

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: seamless material; native palette; edge/depth transitions where applicable.

Historical artifacts: [art/village/scenery/surface-sand.png](../art/village/scenery/surface-sand.png).

Current step: not started. Process-log events: 0.

### TILE-WATER-SHALLOW: shallow/wading water

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: seamless material; native palette; edge/depth transitions where applicable.

Historical artifacts: [art/village/scenery/surface-water-shallow.png](../art/village/scenery/surface-water-shallow.png).

Current step: not started. Process-log events: 0.

### FIT-DROMAD-CHILD-TEMPLATE-TUNIC: dromad child / tunic

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: source/exclusion review.

Historical artifacts: [art/village/age-templates/dromad/tunic-east.png](../art/village/age-templates/dromad/tunic-east.png), [art/village/age-templates/dromad/tunic-north.png](../art/village/age-templates/dromad/tunic-north.png), [art/village/age-templates/dromad/tunic-south.png](../art/village/age-templates/dromad/tunic-south.png).

Current step: not started. Process-log events: 0.

### FIT-HUMAN-CHILD-TEMPLATE-TUNIC: human child / tunic

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: source/exclusion review.

Historical artifacts: [art/village/age-templates/human/tunic-east.png](../art/village/age-templates/human/tunic-east.png), [art/village/age-templates/human/tunic-north.png](../art/village/age-templates/human/tunic-north.png), [art/village/age-templates/human/tunic-south.png](../art/village/age-templates/human/tunic-south.png).

Current step: not started. Process-log events: 0.

### SCN-BRINEBRIDGE: BrineBridge

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/brinebridge-detail.png](../art/village/scenery/brinebridge-detail.png).

Current step: not started. Process-log events: 0.

### SCN-BRINESTALKFENCE: BrinestalkFence

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: {"mask": 0, "neighbors": []}; {"mask": 1, "neighbors": ["N"]}; {"mask": 2, "neighbors": ["E"]}; {"mask": 3, "neighbors": ["N", "E"]}; {"mask": 4, "neighbors": ["S"]}; {"mask": 5, "neighbors": ["N", "S"]}; {"mask": 6, "neighbors": ["E", "S"]}; {"mask": 7, "neighbors": ["N", "E", "S"]}; {"mask": 8, "neighbors": ["W"]}; {"mask": 9, "neighbors": ["N", "W"]}; {"mask": 10, "neighbors": ["E", "W"]}; {"mask": 11, "neighbors": ["N", "E", "W"]}; {"mask": 12, "neighbors": ["S", "W"]}; {"mask": 13, "neighbors": ["N", "S", "W"]}; {"mask": 14, "neighbors": ["E", "S", "W"]}; {"mask": 15, "neighbors": ["N", "E", "S", "W"]}.

Historical artifacts: [art/village/scenery/fence-detail.png](../art/village/scenery/fence-detail.png), [art/village/scenery/fence.png](../art/village/scenery/fence.png), [art/village/scenery/rustedmetalwall-detail.png](../art/village/scenery/rustedmetalwall-detail.png), [art/village/scenery/woodenmechanicaltransmission-body.png](../art/village/scenery/woodenmechanicaltransmission-body.png).

Current step: not started. Process-log events: 0.

### SCN-BRINESTALKWALL: BrinestalkWall

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: {"mask": 0, "neighbors": []}; {"mask": 1, "neighbors": ["N"]}; {"mask": 2, "neighbors": ["E"]}; {"mask": 3, "neighbors": ["N", "E"]}; {"mask": 4, "neighbors": ["S"]}; {"mask": 5, "neighbors": ["N", "S"]}; {"mask": 6, "neighbors": ["E", "S"]}; {"mask": 7, "neighbors": ["N", "E", "S"]}; {"mask": 8, "neighbors": ["W"]}; {"mask": 9, "neighbors": ["N", "W"]}; {"mask": 10, "neighbors": ["E", "W"]}; {"mask": 11, "neighbors": ["N", "E", "W"]}; {"mask": 12, "neighbors": ["S", "W"]}; {"mask": 13, "neighbors": ["N", "S", "W"]}; {"mask": 14, "neighbors": ["E", "S", "W"]}; {"mask": 15, "neighbors": ["N", "E", "S", "W"]}.

Historical artifacts: [art/village/scenery/brinestalkwallwithgearbox-body.png](../art/village/scenery/brinestalkwallwithgearbox-body.png), [art/village/scenery/brinestalkwallwithgearbox-detail.png](../art/village/scenery/brinestalkwallwithgearbox-detail.png), [art/village/scenery/wall-brinestalk-detail.png](../art/village/scenery/wall-brinestalk-detail.png), [art/village/scenery/wall-brinestalk.png](../art/village/scenery/wall-brinestalk.png).

Current step: not started. Process-log events: 0.

### SCN-BRINESTALKWALLWITHGEARBOX: BrinestalkWallWithGearbox

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: {"mask": 0, "neighbors": []}; {"mask": 1, "neighbors": ["N"]}; {"mask": 2, "neighbors": ["E"]}; {"mask": 3, "neighbors": ["N", "E"]}; {"mask": 4, "neighbors": ["S"]}; {"mask": 5, "neighbors": ["N", "S"]}; {"mask": 6, "neighbors": ["E", "S"]}; {"mask": 7, "neighbors": ["N", "E", "S"]}; {"mask": 8, "neighbors": ["W"]}; {"mask": 9, "neighbors": ["N", "W"]}; {"mask": 10, "neighbors": ["E", "W"]}; {"mask": 11, "neighbors": ["N", "E", "W"]}; {"mask": 12, "neighbors": ["S", "W"]}; {"mask": 13, "neighbors": ["N", "S", "W"]}; {"mask": 14, "neighbors": ["E", "S", "W"]}; {"mask": 15, "neighbors": ["N", "E", "S", "W"]}.

Historical artifacts: [art/village/scenery/brinestalkwallwithgearbox-body.png](../art/village/scenery/brinestalkwallwithgearbox-body.png), [art/village/scenery/brinestalkwallwithgearbox-detail.png](../art/village/scenery/brinestalkwallwithgearbox-detail.png), [art/village/scenery/wall-brinestalk-detail.png](../art/village/scenery/wall-brinestalk-detail.png), [art/village/scenery/wall-brinestalk.png](../art/village/scenery/wall-brinestalk.png).

Current step: not started. Process-log events: 0.

### SCN-CANVASWALL: CanvasWall

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: {"mask": 0, "neighbors": []}; {"mask": 1, "neighbors": ["N"]}; {"mask": 2, "neighbors": ["E"]}; {"mask": 3, "neighbors": ["N", "E"]}; {"mask": 4, "neighbors": ["S"]}; {"mask": 5, "neighbors": ["N", "S"]}; {"mask": 6, "neighbors": ["E", "S"]}; {"mask": 7, "neighbors": ["N", "E", "S"]}; {"mask": 8, "neighbors": ["W"]}; {"mask": 9, "neighbors": ["N", "W"]}; {"mask": 10, "neighbors": ["E", "W"]}; {"mask": 11, "neighbors": ["N", "E", "W"]}; {"mask": 12, "neighbors": ["S", "W"]}; {"mask": 13, "neighbors": ["N", "S", "W"]}; {"mask": 14, "neighbors": ["E", "S", "W"]}; {"mask": 15, "neighbors": ["N", "E", "S", "W"]}.

Historical artifacts: [art/village/scenery/rustedmetalwall-detail.png](../art/village/scenery/rustedmetalwall-detail.png), [art/village/scenery/wall-canvas-detail.png](../art/village/scenery/wall-canvas-detail.png), [art/village/scenery/wall-canvas.png](../art/village/scenery/wall-canvas.png), [art/village/scenery/woodenmechanicaltransmission-body.png](../art/village/scenery/woodenmechanicaltransmission-body.png).

Current step: not started. Process-log events: 0.

### SCN-DIRTFLOOR: DirtFloor

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCN-DIRTPATH: DirtPath

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: continuous interior; 8-neighbor edge/corner blending.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCN-DOOR: Door

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: closed; open; native panel position and occlusion.

Historical artifacts: [art/village/scenery/door-body.png](../art/village/scenery/door-body.png), [art/village/scenery/door-detail.png](../art/village/scenery/door-detail.png).

Current step: not started. Process-log events: 0.

### SCN-POND: Pond

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: wading/shallow; swimming/deep; connected banks/edges; foreground over liquid.

Historical artifacts: none recorded.

Current step: not started. Process-log events: 0.

### SCN-RUSTEDMETALWALL: RustedMetalWall

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: {"mask": 0, "neighbors": []}; {"mask": 1, "neighbors": ["N"]}; {"mask": 2, "neighbors": ["E"]}; {"mask": 3, "neighbors": ["N", "E"]}; {"mask": 4, "neighbors": ["S"]}; {"mask": 5, "neighbors": ["N", "S"]}; {"mask": 6, "neighbors": ["E", "S"]}; {"mask": 7, "neighbors": ["N", "E", "S"]}; {"mask": 8, "neighbors": ["W"]}; {"mask": 9, "neighbors": ["N", "W"]}; {"mask": 10, "neighbors": ["E", "W"]}; {"mask": 11, "neighbors": ["N", "E", "W"]}; {"mask": 12, "neighbors": ["S", "W"]}; {"mask": 13, "neighbors": ["N", "S", "W"]}; {"mask": 14, "neighbors": ["E", "S", "W"]}; {"mask": 15, "neighbors": ["N", "E", "S", "W"]}.

Historical artifacts: [art/village/scenery/rustedmetalwall-detail.png](../art/village/scenery/rustedmetalwall-detail.png), [art/village/scenery/wall-metal-detail.png](../art/village/scenery/wall-metal-detail.png), [art/village/scenery/wall-metal.png](../art/village/scenery/wall-metal.png), [art/village/scenery/woodenmechanicaltransmission-body.png](../art/village/scenery/woodenmechanicaltransmission-body.png).

Current step: not started. Process-log events: 0.

### SCN-BRINESTALK: Brinestalk

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/brinestalk-body.png](../art/village/scenery/brinestalk-body.png), [art/village/scenery/brinestalk-detail.png](../art/village/scenery/brinestalk-detail.png).

Current step: not started. Process-log events: 0.

### SCN-DOGTHORN-TREE: Dogthorn Tree

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/dogthorn-tree-body.png](../art/village/scenery/dogthorn-tree-body.png), [art/village/scenery/dogthorn-tree-detail.png](../art/village/scenery/dogthorn-tree-detail.png).

Current step: not started. Process-log events: 0.

### SCN-STARAPPLE-TREE: Starapple Tree

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/starapple-tree-ripe-body.png](../art/village/scenery/starapple-tree-ripe-body.png), [art/village/scenery/starapple-tree-ripe-detail.png](../art/village/scenery/starapple-tree-ripe-detail.png).

Current step: not started. Process-log events: 0.

### SCN-STARAPPLE-TREE-RIPE: Starapple Tree Ripe

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/starapple-tree-ripe-body.png](../art/village/scenery/starapple-tree-ripe-body.png), [art/village/scenery/starapple-tree-ripe-detail.png](../art/village/scenery/starapple-tree-ripe-detail.png).

Current step: not started. Process-log events: 0.

### SCN-WATERVINE: Watervine

Required steps: resolve_object_description_original_tile_palette_state -> select_render_reference_or_document_no_equivalent -> construct_faithful_shape -> create_required_state_neighbor_variants -> refine_materials_and_form -> extract_register_color_coverage -> visual_review_identity_and_connections_at_game_scale -> native_state_review.

Required views/states: fixed map view; source palette/coverage and native supported states.

Historical artifacts: [art/village/scenery/watervine-body.png](../art/village/scenery/watervine-body.png), [art/village/scenery/watervine-detail.png](../art/village/scenery/watervine-detail.png).

Current step: not started. Process-log events: 0.

### BODY-HUMAN-FEMALE-OLDER: human female older template

Required steps: resolve_age_evidence_and_render_reference -> construct_front_from_shared_human_base -> refine_front -> generate_other_views -> patch_and_refine_composed_views -> register_body_head_and_palette -> visual_review_all_views -> record_native_selection_policy_without_changing_demographics.

Required views/states: south/front; east/whole-body side; north/back; west mirror; separate body/head and clothing.

Historical artifacts: none recorded.

Current step: construct_front_from_shared_human_base. Process-log events: 0.

### BODY-HUMAN-MALE-OLDER: human male older template

Required steps: resolve_age_evidence_and_render_reference -> construct_front_from_shared_human_base -> refine_front -> generate_other_views -> patch_and_refine_composed_views -> register_body_head_and_palette -> visual_review_all_views -> record_native_selection_policy_without_changing_demographics.

Required views/states: south/front; east/whole-body side; north/back; west mirror; separate body/head and clothing.

Historical artifacts: none recorded.

Current step: generation ready; final acceptance pending. Process-log events: 12.

- 2026-10-20T01:13:36.283910+00:00 / resolve_age_evidence_and_render_reference / PASS: Recorded the requested older human variant, original Qud age reference, actual adult donor references, and the source hierarchy.
  Review: Inspected the plate and packet. Irudad supplies explicit old-face/hunched-back prose, but extra arms/tail are individual mutations, not generic aging. No distinct aged donor torso or native age selector is established; age variation is authored.
  Inputs: [{"path": "art/village/sources.json", "sha256": "b0a2de847e29d251f500f81fc25aa3eacec393b4af78370c2a490e9f2706ec22"}, {"path": "art/conversion/body-human-male/v1/model.json", "sha256": "62eb59d1943b8f64bdcb2503f171bcb6c908e1d72eb24e882de2ef4cfe1a701e"}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/source-packet.json", "sha256": "61ff9a57a6aedd1e37d94fd406471b17c57563406c3bb10e1da161e0ce78d49c"}, {"path": "art/conversion/body-human-male-older/v1/source-comparison.png", "sha256": "ca0dfc9f63529505d8b023644c4b4d96c37295d62c31a3f260daaa5f5554f903"}]
  Method/prompt/corrections: {"phase": "Human age reference and metadata"}

- 2026-10-20T01:13:36.284216+00:00 / construct_front_from_shared_human_base / PASS: Adjusted the shared human editable torso to softened shoulders and midsection, retaining head, limbs, bare feet and presentation.
  Review: Viewed the manually constructed front. Same human family and anatomy; no clothes, personal hair/eyes, mutation appendages or profession pose. This is an age-related authoring suggestion, not a new native demographic.
  Inputs: [{"path": "art/conversion/body-human-male/v1/constructed-front.svg", "sha256": "618d5e12a3c6fdfec84456655ea1a3217d60cdb4168ce7722b6c56ce47c0c84c"}, {"path": "tools/construct_older_human.py", "sha256": "4fc047dad3df73b87888cb21f577119fd32c6b8c9f9585f16a5dc17a3fea9c28"}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/constructed-front.svg", "sha256": "791064bc6d2b431546cb76f5bb6ca7559fa8cdf177db02168115ec7a7aae3726"}, {"path": "art/conversion/body-human-male-older/v1/constructed-front.png", "sha256": "cd8d98e4ddc6630c2690102caa390e05c3143b354289fe8931c985717ab9ea61"}]
  Method/prompt/corrections: {"phase": "Manual older male front"}

- 2026-10-20T01:15:01.250159+00:00 / refine_front / REJECTED: Generated a first refined older front from the construction and shared male reference. Rejected it because the returned shoulder/pectoral shading reads more athletic and did not establish the intended age variation.
  Review: Anatomy/feet were retained, but the age brief was missed. Do not select this as an older human. Make one focused correction to the shoulder/torso planes and age-specific head/neck planes while preserving the family.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/constructed-front.png", "sha256": "cd8d98e4ddc6630c2690102caa390e05c3143b354289fe8931c985717ab9ea61"}, {"path": "art/conversion/body-human-male/v1/registered-assembly.png", "sha256": "20883b2586c0045436f258a90e8411eea6909762cda532a6b379fcb3d6e3393a"}, {"path": "art/conversion/body-human-male-older/v1/refine-front-prompt.txt", "sha256": "0975fe314a99cd0a757354578e978d37cb1a524948c7b5601e0e25cd7d3a5d83"}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/refined-front-rejected-athletic.png", "sha256": "28ccdc1f87d2f7b397e5d7aa6eb03b47ee3665000282ed00aed03516ccd0b27f"}]
  Method/prompt/corrections: {"phase": "Rejected older front: athletic shading replaced age cues", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-6b8f614b-4793-4af2-a2c9-2819b04cafc2.png"}

- 2026-10-20T01:16:05.936592+00:00 / refine_front / PASS: Applied one focused correction to the rejected athletic proposal, keeping the manually constructed human family and adding restrained age-related neck/cheek planes and a softer torso.
  Review: Viewed output: softer sloped shoulders, relaxed abdomen and subtle neck/cheek creases. One blank head, two arms/hands and two bare feet remain; no hair, eyes, clothing or mutation appendages. Selected as the older front anchor.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/refined-front-rejected-athletic.png", "sha256": "28ccdc1f87d2f7b397e5d7aa6eb03b47ee3665000282ed00aed03516ccd0b27f"}, {"path": "art/conversion/body-human-male-older/v1/constructed-front.png", "sha256": "cd8d98e4ddc6630c2690102caa390e05c3143b354289fe8931c985717ab9ea61"}, {"path": "art/conversion/body-human-male-older/v1/correct-front-prompt.txt", "sha256": "273b5517b12a8d5c0e0d227fffe84e8433bb5cdbb0c409f8a08cbb64b0ba9352"}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/refined-front.png", "sha256": "a93caed2d577514bb9ddfed2995e21eb24628a23f88cdf55a678f814883750ec"}]
  Method/prompt/corrections: {"phase": "Corrected older front selected", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-05187bf1-22dc-465e-adfa-ff406142a03e.png"}

- 2026-10-20T01:17:47.418140+00:00 / generate_other_views / PASS: Generated secondary views from the corrected older front and explicit shared-family/age anatomy.
  Review: Viewed three directions: the side has restrained rounded upper back and forward head, with whole-body rotation and occluded far limbs. Rear head and heels read as back view. No mutation appendages or clothing.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/refined-front.png", "sha256": "a93caed2d577514bb9ddfed2995e21eb24628a23f88cdf55a678f814883750ec"}, {"path": "art/conversion/body-human-male-older/v1/secondary-views-prompt.txt", "sha256": "2768f17a31ce5a3e73b7d5701a23eda287fa978bc8207295e2056ad5edf9b6ae"}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/secondary-views.png", "sha256": "2e6b4836f357633b88632addb595456e79d5d9bf4286be1bb1ca14142be9a7a2"}]
  Method/prompt/corrections: {"phase": "Older male side/back proposals", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-df595590-120e-40dd-9f65-33acce761693.png"}

- 2026-10-20T01:17:47.419567+00:00 / patch_and_refine_composed_views / RECORDED: Cleaned generated labels/alpha, restored neutral source and aligned contacts before composed refinement.
  Review: Contact/neutrality patches only; no count or attachment error required rebuilding. Preserve the age cues during the composed refinement.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/secondary-views.png", "sha256": "2e6b4836f357633b88632addb595456e79d5d9bf4286be1bb1ca14142be9a7a2"}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/patched-views.png", "sha256": "7b063168fc5524907ce0618c3da466734fb11b95b8e04fc2952c2171b3409b4c"}, {"path": "art/conversion/body-human-male-older/v1/patch-decisions.json", "sha256": "8106a89eb5139c5bfa243a80cda6dabd78d310700fd53b8eb91542c0699dc454"}]
  Method/prompt/corrections: {"phase": "Patched older views"}

- 2026-10-20T01:20:19.682356+00:00 / patch_and_refine_composed_views / RECORDED: Caught that the proposal did not use equal columns: the front right hand crossed x512, and the back left hand began before x1024. Preserved v1 and replaced its segmentation with inspected full-figure regions.
  Review: Viewed the corrected composed sheet: each panel now owns its complete figure, including both front/back hands. Scale unchanged; baseline aligned. V1 is retained as rejected segmentation evidence and must not be registered.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/secondary-views.png", "sha256": "2e6b4836f357633b88632addb595456e79d5d9bf4286be1bb1ca14142be9a7a2"}, {"path": "art/conversion/body-human-male-older/v1/patched-views.png", "sha256": "7b063168fc5524907ce0618c3da466734fb11b95b8e04fc2952c2171b3409b4c"}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/patched-views-v2.png", "sha256": "bb834dcdf1ff70551feb6e619a524bf2214487fea633e6bbff64976fd412da41"}, {"path": "art/conversion/body-human-male-older/v1/patch-decisions-v2.json", "sha256": "a0612b3283dd2c776aa58a3ff256f920bb26e0fbde87dac7ab8509db46b0e038"}]
  Method/prompt/corrections: {"phase": "Corrected unequal view boundaries before refinement"}

- 2026-10-20T01:22:51.195852+00:00 / patch_and_refine_composed_views / PASS: Refined the correctly separated v2 composed sheet, keeping the unmutated human family, mild older stance and complete hands/feet.
  Review: Viewed all directions. Retains relaxed torso, older neck/knee planes, slight forward head and rounded upper back in side view. Same one head/two arms/hands/two legs/feet; no added mutations, clothing or personal cosmetics.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/patched-views-v2.png", "sha256": "bb834dcdf1ff70551feb6e619a524bf2214487fea633e6bbff64976fd412da41", "role": ""}, {"path": "art/conversion/body-human-male-older/v1/refine-patched-prompt.txt", "sha256": "c939a8abf0a02536b60be586bfe40847c7fc9462cf02cd00e51f4bbe74d42a93", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/refined-patched-views.png", "sha256": "0a42be20267db6c7ed48eafd2e919dcd2f8877088858039a716b84309474e279", "role": ""}]
  Method/prompt/corrections: {"phase": "Refined corrected older-male views", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-c7229443-7fe3-402e-a763-ef2a4c06fb22.png"}

- 2026-10-20T01:22:51.199193+00:00 / register_body_head_and_palette / PASS: Registered the selected complete-figure views at the shared physical human height, with grayscale source, separate head/neck masks and two-pixel body underlap.
  Review: Viewed the recomposition: no missing hands/feet or neck gaps. Intrinsic age planes remain in the body/head art. No mutation appendages are baked into this reusable race variant.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/refined-patched-views.png", "sha256": "0a42be20267db6c7ed48eafd2e919dcd2f8877088858039a716b84309474e279", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/model.json", "sha256": "1dc629200b2a9ae71466230a4e130d2709fecc8441f162a45dc5729007bcbded", "role": ""}, {"path": "art/conversion/body-human-male-older/v1/registered-assembly.png", "sha256": "d4ae5a06f783eadb19586886209978a84b3aa0ac7f42baca6f88fd193e964618", "role": ""}, {"path": "art/conversion/body-human-male-older/v1/body-south.png", "sha256": "d40f6caeaffa194d223c96fe7a652e228464c7f133e62c6e997caf1c819f51e6", "role": "body / south"}, {"path": "art/conversion/body-human-male-older/v1/head-south.png", "sha256": "c625aa2cf9a2f968d4f0d4d9c5b78a7d399180b4347df30b28758c229b53edda", "role": "head / south"}, {"path": "art/conversion/body-human-male-older/v1/body-mask-south.png", "sha256": "9121d6f63dfac84ff2b45667220b2e9fb5e52f2abf127a509f0a9dc8cb929d2e", "role": "body-mask / south"}, {"path": "art/conversion/body-human-male-older/v1/head-mask-south.png", "sha256": "7d401843cb09cd8fb3e0b0e2674800e999d0b40c8a389d4683e36a8294e9dc49", "role": "head-mask / south"}, {"path": "art/conversion/body-human-male-older/v1/body-east.png", "sha256": "8dc37ee37a1ff2f9eb0efb42124e1da27f0c1efee004ca32cf831e55ff8cd438", "role": "body / east"}, {"path": "art/conversion/body-human-male-older/v1/head-east.png", "sha256": "177c7e9ebe7693125d918c4dacb9cb7893e0e395be5968fee9c2f9b3fcba3ba9", "role": "head / east"}, {"path": "art/conversion/body-human-male-older/v1/body-mask-east.png", "sha256": "d185b9f68316bf22f51c7b29d75ba7625d46c373034fa74a27999e9f5e22cf30", "role": "body-mask / east"}, {"path": "art/conversion/body-human-male-older/v1/head-mask-east.png", "sha256": "84b3dd4bf3bd026e7dc034e6766b4f1f3764c730871e60d281dce237850eea98", "role": "head-mask / east"}, {"path": "art/conversion/body-human-male-older/v1/body-north.png", "sha256": "8dc54232a51a0dd928147fb1d3123011fde595289f67bae32bc6a18afd387d17", "role": "body / north"}, {"path": "art/conversion/body-human-male-older/v1/head-north.png", "sha256": "a1086c735aa423f41b3a892e4cc045f657ab045d258eabc485f2b4e8fb1927e1", "role": "head / north"}, {"path": "art/conversion/body-human-male-older/v1/body-mask-north.png", "sha256": "32ebe6a168b6f62e45ae7716b1195f650d59c591b51ae470b28b3e6a65aa756b", "role": "body-mask / north"}, {"path": "art/conversion/body-human-male-older/v1/head-mask-north.png", "sha256": "abcab997a3c75c19e963532dd595a4b6131cb86e84b5bede865d6943feae5372", "role": "head-mask / north"}]
  Method/prompt/corrections: {"phase": "Registered older body/head and explicit masks", "tool": "Python Pillow", "settings": {"canvas": [512, 1024], "physical_height": 1.21, "head_mask_top_y": 210, "neck_bottom_y": 248, "body_underlap_pixels": 2}}

- 2026-10-20T01:22:51.199710+00:00 / visual_review_all_views / PASS: Reviewed the registered views and intended-size authoring preview, including complete hands after correcting the unequal-column proposal.
  Review: Front/back feet and hands remain visible; side is a whole-body profile with occluded far limbs. Grayscale source supports Qud foreground tint and separate clothing colors. Generation-ready only; native acceptance remains pending.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/model.json", "sha256": "1dc629200b2a9ae71466230a4e130d2709fecc8441f162a45dc5729007bcbded", "role": ""}, {"path": "art/conversion/body-human-male-older/v1/registered-assembly.png", "sha256": "d4ae5a06f783eadb19586886209978a84b3aa0ac7f42baca6f88fd193e964618", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/game-scale-review.png", "sha256": "db5dd88863880015c08d04422302f675d84aaadb04e96a7d7cd2e23dbaa25209", "role": ""}]
  Method/prompt/corrections: {"phase": "Older male authoring ready"}

- 2026-10-20T01:22:51.199884+00:00 / record_native_selection_policy_without_changing_demographics / PASS: Recorded this as an authored older-human variant without assigning a numerical age or changing villagers. It may supply Irudad's unmutated baseline later; his mutation metadata stays separate.
  Review: No native age selector is assumed. Mutation appendages and actual equipped items remain separate from the reusable older human base.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/source-packet.json", "sha256": "61ff9a57a6aedd1e37d94fd406471b17c57563406c3bb10e1da161e0ce78d49c", "role": ""}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v1/model.json", "sha256": "1dc629200b2a9ae71466230a4e130d2709fecc8441f162a45dc5729007bcbded", "role": ""}]
  Method/prompt/corrections: {"phase": "Age template selection policy"}

- 2026-10-20T01:32:06.245907+00:00 / register_body_head_and_palette / PASS: Translated body/head/masks together to contact (256, 950), keeping the original size, age shape and head/body segmentation. Preserved the previous registration and its evidence.
  Review: Viewed front, east, back and mirrored west with center/ground guides: identical anchor, no clipping, complete hands/feet and unchanged neck join. Side lean remains part of the authored older shape. Exact source pixels preserved. No native tests run.
  Inputs: [{"path": "art/conversion/body-human-male-older/v1/model.json", "sha256": "1dc629200b2a9ae71466230a4e130d2709fecc8441f162a45dc5729007bcbded"}, {"path": "tools/center_human_registration.py", "sha256": "16beef95e1ebeee0d7329f250b568c49a1264704c7bebdbefc72ae184ab64cff"}, {"path": "art/conversion/body-human-male-older/v1/body-south.png", "sha256": "d40f6caeaffa194d223c96fe7a652e228464c7f133e62c6e997caf1c819f51e6"}, {"path": "art/conversion/body-human-male-older/v1/body-mask-south.png", "sha256": "9121d6f63dfac84ff2b45667220b2e9fb5e52f2abf127a509f0a9dc8cb929d2e"}, {"path": "art/conversion/body-human-male-older/v1/head-south.png", "sha256": "c625aa2cf9a2f968d4f0d4d9c5b78a7d399180b4347df30b28758c229b53edda"}, {"path": "art/conversion/body-human-male-older/v1/head-mask-south.png", "sha256": "7d401843cb09cd8fb3e0b0e2674800e999d0b40c8a389d4683e36a8294e9dc49"}, {"path": "art/conversion/body-human-male-older/v1/body-east.png", "sha256": "8dc37ee37a1ff2f9eb0efb42124e1da27f0c1efee004ca32cf831e55ff8cd438"}, {"path": "art/conversion/body-human-male-older/v1/body-mask-east.png", "sha256": "d185b9f68316bf22f51c7b29d75ba7625d46c373034fa74a27999e9f5e22cf30"}, {"path": "art/conversion/body-human-male-older/v1/head-east.png", "sha256": "177c7e9ebe7693125d918c4dacb9cb7893e0e395be5968fee9c2f9b3fcba3ba9"}, {"path": "art/conversion/body-human-male-older/v1/head-mask-east.png", "sha256": "84b3dd4bf3bd026e7dc034e6766b4f1f3764c730871e60d281dce237850eea98"}, {"path": "art/conversion/body-human-male-older/v1/body-north.png", "sha256": "8dc54232a51a0dd928147fb1d3123011fde595289f67bae32bc6a18afd387d17"}, {"path": "art/conversion/body-human-male-older/v1/body-mask-north.png", "sha256": "32ebe6a168b6f62e45ae7716b1195f650d59c591b51ae470b28b3e6a65aa756b"}, {"path": "art/conversion/body-human-male-older/v1/head-north.png", "sha256": "a1086c735aa423f41b3a892e4cc045f657ab045d258eabc485f2b4e8fb1927e1"}, {"path": "art/conversion/body-human-male-older/v1/head-mask-north.png", "sha256": "abcab997a3c75c19e963532dd595a4b6131cb86e84b5bede865d6943feae5372"}]
  Outputs: [{"path": "art/conversion/body-human-male-older/v2/body-south.png", "sha256": "b25c2a6a9b69d6f79f02b4f16b1080c72dac476218ddeb2d274ad52e18080f4b"}, {"path": "art/conversion/body-human-male-older/v2/body-mask-south.png", "sha256": "63a25ef4f65b169d23fb5bcf5a03ab8fecb942c2a437599dc101924411fd1d71"}, {"path": "art/conversion/body-human-male-older/v2/head-south.png", "sha256": "a51dae7026a931ec698ce81105853096618a64cf60d513251dae89ac33ccc869"}, {"path": "art/conversion/body-human-male-older/v2/head-mask-south.png", "sha256": "7c313cf6dffc1c74f4def1d126b433ef38e23275089ecaf68208c0ef93feb73b"}, {"path": "art/conversion/body-human-male-older/v2/selected-south.png", "sha256": "4003d3a7e8ebe80de3146b346f271674ff9989805dc19deeee570f6a5b55b506"}, {"path": "art/conversion/body-human-male-older/v2/body-east.png", "sha256": "b02e62e26817d3b0ed9fbf0e4b58ea7ed19839d5617b688ebcc1967e761f4ee1"}, {"path": "art/conversion/body-human-male-older/v2/body-mask-east.png", "sha256": "cf968b40f96aeb4499c998ed67f4ef9a7a239703cd34bdad782f6d7dc2d33883"}, {"path": "art/conversion/body-human-male-older/v2/head-east.png", "sha256": "fc213613028b8be93f39a5857cd0755830ca0c332483b2ab74ed936cd15905ae"}, {"path": "art/conversion/body-human-male-older/v2/head-mask-east.png", "sha256": "3dbc3e537cb869d06253e55f8ee9092ae60e36bd1248fd5750ff7c28cfda6ba9"}, {"path": "art/conversion/body-human-male-older/v2/selected-east.png", "sha256": "d0a10e7cc510a0bb8949f7699304e10b74033c38862e145521c29559ed740fa6"}, {"path": "art/conversion/body-human-male-older/v2/body-north.png", "sha256": "3e13cf2dc56c96f3c9dc5e513edfc5494c788ff86a3dba7522f9e50e4756b800"}, {"path": "art/conversion/body-human-male-older/v2/body-mask-north.png", "sha256": "e416ab62c176bc0de75b67f5135d9016b9b33eac6ca638794aae596c299ecd72"}, {"path": "art/conversion/body-human-male-older/v2/head-north.png", "sha256": "771f0b0d627c71b28aaa95f23e404f406a0dce0db0a48c273ec7d4be6454442a"}, {"path": "art/conversion/body-human-male-older/v2/head-mask-north.png", "sha256": "b552c1ce29633802fca437003493f949f4cb5e2bb3592c0e3e749be2acd9366a"}, {"path": "art/conversion/body-human-male-older/v2/selected-north.png", "sha256": "18f21eec1e2ba53057f222ddbd07fe370389664ebd648299d82552a2120a5db1"}, {"path": "art/conversion/body-human-male-older/v2/model.json", "sha256": "07bee6d989188dff1e551a89d2f1e0752026e1ba6b5693f64665d5d174db1369"}, {"path": "art/conversion/body-human-male-older/v2/registration-decisions.json", "sha256": "4470036b2b635e32b0eea7d35eccbd30628396a5792909928ab3d1bae45c1cbc"}, {"path": "art/conversion/body-human-male-older/v2/registration-comparison.png", "sha256": "31a39a0be4ca5b1ea6d36cf65be29a8b05c5a7fc2e4019c7072903a9ccb0e262"}]
  Method/prompt/corrections: {"phase": "Shared centered canvas registration v2"}

## Sources and exclusions

[Structured ledger](../evidence/conversion-ledger.json) contains per-entry native metadata, exact hashes, source targets and the log.

Sources: [art/village/sources.json](../art/village/sources.json), [art/village/model.json](../art/village/model.json), [art/village/age-templates.json](../art/village/age-templates.json), [evidence/village-reference-index.json](../evidence/village-reference-index.json), [evidence/joppa-creature-catalogue.json](../evidence/joppa-creature-catalogue.json), [probe/joppa-coverage.json](../probe/joppa-coverage.json).

Race description/body trees, equipped part/laterality and palette references are retained. Captured instance IDs/genders describe one source snapshot, not permanent demographics. Unknown age or mutation state is not guessed. Player anatomy and future random/mod inventory are outside the enumerated resident snapshot; they are not silently counted as converted. Any newly discovered visible target must be added explicitly.

All completion blockers remain internal, actionable unfinished art work: missing full construction/refinement, masks/fit and visual acceptance. No required art is deferred to an unnamed future stage. The active objective authorizes completing the entries one at a time with the [HTML evidence report](conversion-report.html), including Qud-colored stone-like paths integrated over grass.
