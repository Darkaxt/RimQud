# Joppa conversion ledger

Reset date: 2026-10-20. **Every entry is UNFINISHED at the reset.**

This ledger supersedes earlier art-completion claims. Native tests establish integration behavior only. Existing sprites, traced contours, generated sheets and previous selections are historical inputs; none receive completion credit.

156 entries: 16 resident assemblies (10 blueprints), 12 body/age templates, 20 actual equipment inventory/aggregate records, 33 body/equipment fittings, 2 child-template garments, 57 scenery types, 8 surface/grass targets and 8 exclusion reviews.

The 75 baseline blueprint types are all accounted for: 67 selected visible types plus eight exclusions to recheck. Connectivity masks are enumerated under their owning wall/fence entry, not hidden behind an atlas count. Counts overlap between subjects and fittings; they are not a completion percentage.

Equipment inventory rows identify the 20 unique items and aggregate their fitting records; they do not require generating a second generic outfit. The 33 fitting entries own actual body-specific construction/refinement/extraction. An item aggregate or NPC assembly cannot complete while its linked fittings/body remain unfinished.

Active entry: **FIT-DROMAD-CHILD-TEMPLATE-TUNIC**. Overall art work: **unfinished**. Implementation Stage 3: **ACTIVE**.

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
| BODY-HUMAN-FEMALE-OLDER | human female older template | UNFINISHED | BODY-HUMAN-FEMALE | User-requested age variant of the selected shared human family. No native life-stage selector established; do not change NPC demographics. |
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
| FIT-DROMAD-CHILD-TEMPLATE-TUNIC | dromad child / tunic | IN PROGRESS | BODY-DROMAD-CHILD | Unmapped template garment: no actual Qud item identity or native equipped-slot binding established. |
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

Current step: generation ready; final acceptance pending. Process-log events: 12.

- 2026-10-20T02:08:30.483483+00:00 / resolve_race_description_original_sprite_runtime_anatomy / PASS: Resolved Tam through Dromad ancestry; carried native race/individual descriptions, complete attached part IDs/parents/laterality, natural/actual equipment, source version/hashes and metadata gaps.
  Review: Read the source packet and viewed original glyph. Humanoid baseline supports two hands and paired feet, while description supplies long neck, dulla and upper-back hump. Runtime mutation list, age and race-wide dimorphism remain unknown; no four-legged camel substitution.
  Inputs: [{"path": "evidence/tam-conversion-input.json", "sha256": "2dfd8529d919dc160e4dcf05e546d4e8fd5c84340bfe6cac4a3ceb9c8b5ff4fc"}, {"path": "evidence/village-reference-index.json", "sha256": "cc00cbf6f72d5d4134efb3879d83b30988fcec4ae822cec8a340b072024ca149"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/source-packet.json", "sha256": "0f0de31f0629223665e998790882de647d147569c78a4de7d754e115ed4a0709"}]
  Method/prompt/corrections: {"phase": "Dromad identity, description and observed body tree"}

- 2026-10-20T02:08:30.483865+00:00 / select_actual_core_dlc_or_mod_reference / PASS: Selected installed Core Dromedary front/side/back assets for muzzle, hump, perspective, outline and shading conventions.
  Review: Viewed actual donor front/side and the contextual three-direction plate; all source PNG hashes matched the catalogue. Donor quadruped legs/tail are not copied into the Qud humanoid race.
  Inputs: [{"path": "evidence/joppa-creature-catalogue.json", "sha256": "de8affadee7f4260a8ec68a81e6d6e5f7c98c627a7b29ddcbae3668c6cfd4a79"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/source-comparison.png", "sha256": "e4a310f131c608f85f17d4a9eb01f06d0486cc2445f1886830b601dfa57c7fe5"}]
  Method/prompt/corrections: {"phase": "Actual RimWorld dromedary references"}

- 2026-10-20T02:08:30.484056+00:00 / construct_front / PASS: Reused the earlier editable body/head geometry as source only, composing it with one transform onto the common centered canvas. No historical art acceptance carried forward.
  Review: Viewed whole front: camel-like head, long neck/dulla, hump, two arms/hands and paired rounded feet. No robe, staff, jewelry or markings. Neck and foot fine shape remain authored; next is restrained front refinement.
  Inputs: [{"path": "art/dromad/nude/body-south.svg", "sha256": "c017414ec56f0671adcaaca2cb6f4dad42879911b1d42daa44b080a52f5c9873"}, {"path": "art/dromad/nude/head-south.svg", "sha256": "ca87c5895fe7eb827c92cae1e0716ee4016bf22868ff9940f09815069d589030"}, {"path": "tools/construct_dromad_front.py", "sha256": "c49052e1b1a572f5b11f502c6ffbbbedc0eec883bd6f2d87daf3b7e4edaa56d6"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/constructed-front.svg", "sha256": "a2641fded3aed5e5122481e1c58c817fd781b65b8262967e43978fde3b7c12c5"}, {"path": "art/conversion/body-dromad/v1/constructed-front.png", "sha256": "3677a61c4d6f12336d1cbe727c99792a0b0ff124f6d74c412d5017a92cf0ce64"}]
  Method/prompt/corrections: {"phase": "Reconstructed editable dromad front in the shared frame"}

- 2026-10-20T02:09:41.098057+00:00 / construct_front / PASS: Refined the constructed front with the native original/description and installed dromedary reference plate.
  Review: Viewed the complete front. Preserves compact bipedal camelfolk, long neck/dulla, ears/muzzle, integrated body/hump and two hands/feet. No gear or personal adornment. Source foot guide bars remain and will be removed during composed refinement; exact grayscale and contact registration follow.
  Inputs: [{"path": "art/conversion/body-dromad/v1/constructed-front.png", "sha256": "3677a61c4d6f12336d1cbe727c99792a0b0ff124f6d74c412d5017a92cf0ce64"}, {"path": "art/conversion/body-dromad/v1/source-comparison.png", "sha256": "e4a310f131c608f85f17d4a9eb01f06d0486cc2445f1886830b601dfa57c7fe5"}, {"path": "art/conversion/body-dromad/v1/refine-front-prompt.txt", "sha256": "f0a63ca46c098027385bf907eb13a3d0dc97c83d1c67bbb9d9512573f23e8b8d"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/refined-front.png", "sha256": "df23e042c0f627dddf66c2090025a7985e8874fcd07a094c09bc957e16083a11"}]
  Method/prompt/corrections: {"phase": "Refined dromad front selected", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-8b350434-bcdf-4617-b23e-360a80c19a9d.png"}

- 2026-10-20T02:13:27.517602+00:00 / imagegen_side_back_from_front_and_race_facts / RECORDED: Generated secondary views from the selected dromad front and actual donor camel profile, with explicit humanoid race anatomy.
  Review: Viewed projecting camel muzzle, long neck, profile feet/limb overlap and continuous side upper-back hump. Rear proposal has an extra rounded lobe beside the neck; correct it to one integrated hump before selecting. Foot guide bars removed.
  Inputs: [{"path": "art/conversion/body-dromad/v1/refined-front.png", "sha256": "df23e042c0f627dddf66c2090025a7985e8874fcd07a094c09bc957e16083a11"}, {"path": "art/conversion/body-dromad/v1/secondary-views-prompt.txt", "sha256": "95ec5c17fc7514d1573883a776e51d29fd6325326ff3e11a1536fd2ddc73b31c"}, {"path": "art/conversion/body-dromad/v1/source-packet.json", "sha256": "0f0de31f0629223665e998790882de647d147569c78a4de7d754e115ed4a0709"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/secondary-views.png", "sha256": "9f74ec4cb06116cc7a6c106871e1587ef5d0429fa28d9fa818507f7cf5dbcb8c"}]
  Method/prompt/corrections: {"phase": "Front-guided dromad side/back proposals", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2, "private_reference": "dromedary-reference-east.png; exact source/hash in source-packet.json"}, "generation_file": "exec-e74fe33f-d6ba-405a-b174-b8ac24e6531b.png"}

- 2026-10-20T02:13:27.519897+00:00 / correct_anatomy_then_imagegen_refine_composed_views / REJECTED: Prepared a first frame/palette patch using rectangular view bands, then inspected connected silhouettes.
  Review: Source figures overlap in horizontal range: rear silhouette begins at x1047 while the profile extends to x1043. A column band steals or includes pixels from another figure at different heights. Replace it with connected-silhouette ownership.
  Inputs: [{"path": "art/conversion/body-dromad/v1/secondary-views.png", "sha256": "9f74ec4cb06116cc7a6c106871e1587ef5d0429fa28d9fa818507f7cf5dbcb8c"}, {"path": "art/conversion/body-dromad/v1/prepare-views-rejected-panels.py", "sha256": "431fe0d8d39c9fd042db1895bb41848099b0b4e76a09fd7cd122cf1c73f015f8"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/patched-views-rejected-panels.png", "sha256": "ae9c5b93e39e1faa995f6364c2cacd650693eeb25c15ca997468ae8dc62a7baa"}]
  Method/prompt/corrections: {"phase": "Rejected panel-boundary segmentation"}

- 2026-10-20T02:13:27.521619+00:00 / correct_anatomy_then_imagegen_refine_composed_views / RECORDED: Separated each whole figure by its connected alpha silhouette, cleaned invisible/low-alpha RGB and neutralized grayscale. Used one .84 scale and translated complete figures to centered foot contacts, preserving long profile muzzle.
  Review: Ownership masks retain whole figures rather than splitting columns. Rear extra upper-back lobe is explicitly pending the targeted composed refinement; no final anatomy acceptance yet.
  Inputs: [{"path": "art/conversion/body-dromad/v1/secondary-views.png", "sha256": "9f74ec4cb06116cc7a6c106871e1587ef5d0429fa28d9fa818507f7cf5dbcb8c"}, {"path": "art/conversion/body-dromad/v1/prepare-views.py", "sha256": "f4d636cc84a0169e70e8c27a6e5a34fbcf07d674da9941ae83185b6195dd8441"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/patched-views.png", "sha256": "bef036de226c6f464a732614ee2657784529d4d6542a19a93aca418aa774199d"}, {"path": "art/conversion/body-dromad/v1/patch-decisions.json", "sha256": "5fbb9a61ccf17bbccc2001fe528a2feeb6892de6af723203f604cd111bfa10d4"}, {"path": "art/conversion/body-dromad/v1/source-selection-south.png", "sha256": "61fb34d15b2ce233a309f68556333242cdd0bc485878fb6ef68f33bf8f9dc7bf"}, {"path": "art/conversion/body-dromad/v1/source-selection-east.png", "sha256": "41ca3059d468ec31386f2b81ee2da0a5396748935a853e180dce6827ed2d9fce"}, {"path": "art/conversion/body-dromad/v1/source-selection-north.png", "sha256": "ee3d83cf59e76c719d6c728f1832c7db6466368fa70175a8deb79f3d350dcacb"}]
  Method/prompt/corrections: {"phase": "Complete-figure ownership, neutral source and common anchors"}

- 2026-10-20T02:18:04.980364+00:00 / correct_anatomy_then_imagegen_refine_composed_views / PASS: Refined the neutral, ownership-separated sheet with a focused rear upper-back correction while preserving the selected front/profile.
  Review: Viewed all views: rear extra lobe removed, one continuous central upper-back mound. Profile retains the projecting muzzle, long neck/dulla and properly turned feet; no tail, extra appendages or clothing. Foot guide bars removed.
  Inputs: [{"path": "art/conversion/body-dromad/v1/patched-views.png", "sha256": "bef036de226c6f464a732614ee2657784529d4d6542a19a93aca418aa774199d"}, {"path": "art/conversion/body-dromad/v1/refine-patched-prompt.txt", "sha256": "4df95d58d75335a1f86596b96b1101e576fe83d4bcdfd2b2e6d6aa27ddb66206"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/refined-patched-views.png", "sha256": "a946adad77a02bf3567d1d8f7f83e0d8f26d9c2bb6629d4a127b7ec215730b3c"}]
  Method/prompt/corrections: {"phase": "Selected composed refinement: one rear hump", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-6fdeece5-7c94-4575-86f3-a6e2326b04e7.png"}

- 2026-10-20T02:18:04.981758+00:00 / imagegen_side_back_from_front_and_race_facts / PASS: Selected the corrected front/profile/rear proposal, keeping native humanoid counts and camel-specific description anatomy.
  Review: A genuine whole-body profile and rear view are now present. Unseen surfaces remain authored interpretation; no donor quadruped anatomy or tail was substituted.
  Inputs: [{"path": "art/conversion/body-dromad/v1/refined-front.png", "sha256": "df23e042c0f627dddf66c2090025a7985e8874fcd07a094c09bc957e16083a11"}, {"path": "art/conversion/body-dromad/v1/source-packet.json", "sha256": "0f0de31f0629223665e998790882de647d147569c78a4de7d754e115ed4a0709"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/refined-patched-views.png", "sha256": "a946adad77a02bf3567d1d8f7f83e0d8f26d9c2bb6629d4a127b7ec215730b3c"}]
  Method/prompt/corrections: {"phase": "Secondary directions selected after correction"}

- 2026-10-20T02:18:04.983269+00:00 / register_required_layers_and_color_masks / REJECTED: Inspected first body/head/detail ownership masks before accepting registration.
  Review: The straight profile neck boundary assigned the outer edge of the projecting dulla to the body. Reject that ownership split; union the full dulla outline into head/neck before deriving body coverage.
  Inputs: [{"path": "art/conversion/body-dromad/v1/refined-patched-views.png", "sha256": "a946adad77a02bf3567d1d8f7f83e0d8f26d9c2bb6629d4a127b7ec215730b3c"}, {"path": "art/conversion/body-dromad/v1/register-layers-rejected-dulla-edge.py", "sha256": "03823231a34f8e954076f5f630bea8e0fe390d09d693587f48c41014c019f4ff"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/ownership-rejected-dulla-edge.png", "sha256": "8776f32228f7845852d05a32681dd36b5b2a7bf964d49fe88d44ca82978bef18"}]
  Method/prompt/corrections: {"phase": "Rejected head ownership at projecting dulla edge"}

- 2026-10-20T02:18:04.984176+00:00 / register_required_layers_and_color_masks / PASS: Re-established masks on the actual refined image. Used connected whole-figure selection, one .84 image scale, shared contact (256, 950), head ownership including the complete dulla and two-source-pixel body underlap. Kept distinct source/refined selection masks to preserve logged provenance.
  Review: Viewed neutral recomposition and colored ownership: body owns hump/painted limbs, head owns the complete neck/dulla. No back dulla layer rendered. Dulla detail region is authored, not asserted as a proven original-color location. Every production layer is grayscale; all facings use identical centered anchors. Physical height 1.4 is an explicit authoring choice, not native metadata.
  Inputs: [{"path": "art/conversion/body-dromad/v1/refined-patched-views.png", "sha256": "a946adad77a02bf3567d1d8f7f83e0d8f26d9c2bb6629d4a127b7ec215730b3c"}, {"path": "art/conversion/body-dromad/v1/register-layers.py", "sha256": "4a95ce852c5a9fada0685b7a5860e16f987670ee2ac81fa607032aa365b07b5b"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/model.json", "sha256": "570e35bd698e21f5ab0fcfe89f9886ef8bf70276cd6efdbc90227dc071d57c15"}, {"path": "art/conversion/body-dromad/v1/registration-decisions.json", "sha256": "28d1b21eb580dd31dee1807e9cee25567c6490b11ccf0cf02543cba7359aec81"}, {"path": "art/conversion/body-dromad/v1/registration-comparison.png", "sha256": "de546996093ebdf5b60a6eac960e17a512959690859a87c7e67e664cd36398dc"}, {"path": "art/conversion/body-dromad/v1/ownership-comparison.png", "sha256": "2ce666657ec8b30247e04c108e9a868fa885e4bd1cc747b14b68d5c2ce4e1e50"}, {"path": "art/conversion/body-dromad/v1/body-south.png", "sha256": "0a7ff06446a4e8c5243b9c30b144b6a9f352dda0f796f126a7a969cfb25bbedc"}, {"path": "art/conversion/body-dromad/v1/head-south.png", "sha256": "51905c4151f6adbf88714f9f9d5a40f385a71d9fd252133054653d8b6fc996a4"}, {"path": "art/conversion/body-dromad/v1/head-detail-south.png", "sha256": "1c6b410c0764bd0892c19d46ff24d2546392343fd0d7993755e682b373a80d5f"}, {"path": "art/conversion/body-dromad/v1/body-mask-south.png", "sha256": "9c54b5c720d4ecff3bad080b005eb67e4a035f35fa2dc9f2c0ac40d152703b7c"}, {"path": "art/conversion/body-dromad/v1/head-mask-south.png", "sha256": "91af9578ee8b25be3e6e69343adba91982478b01413ac1e1bf123f1068c43000"}, {"path": "art/conversion/body-dromad/v1/head-detail-mask-south.png", "sha256": "54a21bb060c7c68d7f837a2d8d3b784ba44800901fc87c5f260ed05025700667"}, {"path": "art/conversion/body-dromad/v1/refined-selection-south.png", "sha256": "1d72d26f5412010d62b4ea096b7ba941c9e794581965df4b2ec297fcfd5b63d8"}, {"path": "art/conversion/body-dromad/v1/body-east.png", "sha256": "5f918d3d71c345d88ccd3530571110d33f70c2984cbe028f31e44d09019feb75"}, {"path": "art/conversion/body-dromad/v1/head-east.png", "sha256": "aef704589190def62ef6376c528f7fb90c0fe74d837bbb4581d3aa299ecafa0e"}, {"path": "art/conversion/body-dromad/v1/head-detail-east.png", "sha256": "26a83da099933f63b451bd098ca3c561cc5587c5d1c25e6f78da9e05ac3ee7c2"}, {"path": "art/conversion/body-dromad/v1/body-mask-east.png", "sha256": "7eb8fb731cfea20006a8f3c6089404915d4f1d9b6ecd482fe68bbe6ed9425390"}, {"path": "art/conversion/body-dromad/v1/head-mask-east.png", "sha256": "05d9217d15c6f6025b894e60ae596608ac2a2bd11820bb8d77cdced776836c55"}, {"path": "art/conversion/body-dromad/v1/head-detail-mask-east.png", "sha256": "9d6a3534cb9c405ef1961285b419a463e5608bae9edae706a1d0587297f28bbe"}, {"path": "art/conversion/body-dromad/v1/refined-selection-east.png", "sha256": "030bac3c2342992cd2fe26640d0c93aa6c1f3f362be5e2c883f85bc81cd9c117"}, {"path": "art/conversion/body-dromad/v1/body-north.png", "sha256": "c97b1b02983c1f299c22c35cf1b55034fd1a6c65246d698b80dbe84d28e94872"}, {"path": "art/conversion/body-dromad/v1/head-north.png", "sha256": "d467695c9dad915efef6c428d19142257d9f914f20f797e336e6b01972f346d3"}, {"path": "art/conversion/body-dromad/v1/head-detail-north.png", "sha256": "2acc469cc3de6a04146417767c4c3312adc41d8b3d9270af3094068c2a66832d"}, {"path": "art/conversion/body-dromad/v1/body-mask-north.png", "sha256": "04bade47e250144bd80f93e7f419c73a44ee30c9c333a7bcd5f7b6760fbbd9fb"}, {"path": "art/conversion/body-dromad/v1/head-mask-north.png", "sha256": "6fbd15b478fb0ca9ba95c405def53a669a39d10b1267193c174f6d1df3cac5c6"}, {"path": "art/conversion/body-dromad/v1/head-detail-mask-north.png", "sha256": "52848c292a9768d088119562c36fcd5fa3ca7b485fba3187cf50e4c6aa8b4988"}, {"path": "art/conversion/body-dromad/v1/refined-selection-north.png", "sha256": "3f924de1b2e46850c06cf73047f80e90e252616323ffbb073e83dae7240d48f6"}]
  Method/prompt/corrections: {"phase": "Centered dromad layers and separate neutral detail region"}

- 2026-10-20T02:18:04.986653+00:00 / visual_review_anatomy_orientation_palette_all_views / PASS: Reviewed four facings and intended-size authoring previews of the same registered neutral model.
  Review: Readable long-necked bipedal camelfolk, continuous hump, elongated side muzzle and paired bare feet. No clothing/staff/jewelry baked into the base. Shared contact and separate neutral detail retained. Native acceptance and actual clothing/staff fittings remain pending the all-conversions gate.
  Inputs: [{"path": "art/conversion/body-dromad/v1/model.json", "sha256": "570e35bd698e21f5ab0fcfe89f9886ef8bf70276cd6efdbc90227dc071d57c15"}, {"path": "art/conversion/body-dromad/v1/registration-comparison.png", "sha256": "de546996093ebdf5b60a6eac960e17a512959690859a87c7e67e664cd36398dc"}]
  Outputs: [{"path": "art/conversion/body-dromad/v1/game-scale-review.png", "sha256": "5be89c1849baf9a53d392db9befcd392be64727d7368a17785639c973724908b"}, {"path": "art/conversion/body-dromad/v1/selected-south.png", "sha256": "1d1eaded3fcc976dff381ef05c70317565eaabe0b9a0dd558a3c1b5c64aaf694"}, {"path": "art/conversion/body-dromad/v1/selected-east.png", "sha256": "4e25b4f69b77b132f0b55aaeaf0cf7669661ec4f02c19c1ccf3dc3f889e56caf"}, {"path": "art/conversion/body-dromad/v1/selected-north.png", "sha256": "12a7f74eba51adb597e0ab1add7f42dbc347fc78f3896287d73e191f08c0f955"}]
  Method/prompt/corrections: {"phase": "Dromad base generation-ready"}

### BODY-DROMAD-CHILD: dromad child (featureless body with separate clothing)

Required steps: resolve_age_evidence_and_render_reference -> construct_featureless_front -> generate_other_views -> correct_and_refine_composite -> register_body_head_and_palette -> visual_review_all_views -> record_native_selection_policy_without_changing_demographics.

Required views/states: male/female templates; shared geometry if no supported distinction; south/east/north; west mirror; separate removable clothing.

Historical artifacts: [art/village/age-templates/dromad/body-east.png](../art/village/age-templates/dromad/body-east.png), [art/village/age-templates/dromad/body-north.png](../art/village/age-templates/dromad/body-north.png), [art/village/age-templates/dromad/body-south.png](../art/village/age-templates/dromad/body-south.png), [art/village/age-templates/dromad/head-east.png](../art/village/age-templates/dromad/head-east.png), [art/village/age-templates/dromad/head-north.png](../art/village/age-templates/dromad/head-north.png), [art/village/age-templates/dromad/head-south.png](../art/village/age-templates/dromad/head-south.png), [art/village/age-templates/dromad/tunic-east.png](../art/village/age-templates/dromad/tunic-east.png), [art/village/age-templates/dromad/tunic-north.png](../art/village/age-templates/dromad/tunic-north.png), [art/village/age-templates/dromad/tunic-south.png](../art/village/age-templates/dromad/tunic-south.png).

Current step: generation ready; final acceptance pending. Process-log events: 9.

- 2026-10-20T02:20:24.309587+00:00 / resolve_age_evidence_and_render_reference / PASS: Carried the complete dromad race description/body tree, original glyph, donor dromedary references and explicit unknowns into the child template. Added actual Biotech child torso as a life-stage presentation reference only.
  Review: Read packet and viewed reference plate. No canonical juvenile dromad, age selector or sex-specific geometry is established. Child hump/dulla development is unknown; small family features are an authored choice, not native biological proof. Male/female labels share geometry.
  Inputs: [{"path": "art/conversion/body-dromad/v1/source-packet.json", "sha256": "0f0de31f0629223665e998790882de647d147569c78a4de7d754e115ed4a0709"}, {"path": "art/conversion/body-dromad/v1/model.json", "sha256": "570e35bd698e21f5ab0fcfe89f9886ef8bf70276cd6efdbc90227dc071d57c15"}, {"path": "evidence/joppa-creature-catalogue.json", "sha256": "de8affadee7f4260a8ec68a81e6d6e5f7c98c627a7b29ddcbae3668c6cfd4a79"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/source-packet.json", "sha256": "95ce9f3839ead77ff4392aeeb6f29782dcb54784a2b61bf04cf6a8392f5aa0a2"}, {"path": "art/conversion/body-dromad-child/v1/source-comparison.png", "sha256": "7866f94d2a3bcee566e4aff4336977e3b9663f6b7fa13f636261f5bb1a4cc013"}]
  Method/prompt/corrections: {"phase": "Child camelfolk metadata and reference limits"}

- 2026-10-20T02:20:24.310046+00:00 / construct_featureless_front / PASS: Constructed a compact torso and relatively larger head from the race source geometry, removing foot guide bars and personal face marks. Kept a continuous long neck, muzzle, dulla and hump.
  Review: Viewed full front: ordinary humanoid counts with species silhouette retained. Smooth mannequin without eyes, personal marks, clothing or staff. Native age/demographics unchanged. This is a construction suggestion pending refinement.
  Inputs: [{"path": "tools/construct_dromad_child_front.py", "sha256": "1dda7cd134124f8792af9c5acf4b8870a348b58609b7720a9ab1b534b6b88896"}, {"path": "art/dromad/nude/body-south.svg", "sha256": "c017414ec56f0671adcaaca2cb6f4dad42879911b1d42daa44b080a52f5c9873"}, {"path": "art/dromad/nude/head-south.svg", "sha256": "ca87c5895fe7eb827c92cae1e0716ee4016bf22868ff9940f09815069d589030"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/constructed-front.svg", "sha256": "c888d28b56421b878fd1f48846a151e2ad97a1720ffbda1737ce4dcfaf076d3b"}, {"path": "art/conversion/body-dromad-child/v1/constructed-front.png", "sha256": "6e652bc3a61508d203e2bcd7f80094bc0c8a7ee54d786e2c6725bc09c075141b"}]
  Method/prompt/corrections: {"phase": "Editable featureless child dromad front"}

- 2026-10-20T02:21:35.080701+00:00 / construct_featureless_front / PASS: Refined the child front with the selected adult race model as a family-style reference only.
  Review: Viewed complete smooth mannequin: compact two-handed/two-footed body, relatively larger structural head/ears/muzzle, long neck/dulla and hump. No eyes, nostrils, personal marks, gear or detailed anatomy. Juvenile proportions remain authored, not a canonical age claim.
  Inputs: [{"path": "art/conversion/body-dromad-child/v1/constructed-front.png", "sha256": "6e652bc3a61508d203e2bcd7f80094bc0c8a7ee54d786e2c6725bc09c075141b"}, {"path": "art/conversion/body-dromad/v1/selected-south.png", "sha256": "1d1eaded3fcc976dff381ef05c70317565eaabe0b9a0dd558a3c1b5c64aaf694"}, {"path": "art/conversion/body-dromad-child/v1/refine-front-prompt.txt", "sha256": "a49106f37c85bff760fd570c2cc79a18945ed8008bf5db234ec4a39e2c76d21d"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/refined-front.png", "sha256": "e7b0d5a3a896e64c2ec3cf5d8c449d4e17797d196a4d0f3764126f220ba9d406"}]
  Method/prompt/corrections: {"phase": "Refined featureless child camelfolk front selected", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-c002ecf0-c3e9-49a7-a000-cca79b27b95e.png"}

- 2026-10-20T02:23:29.119693+00:00 / generate_other_views / PASS: Generated secondary directions from the selected child front and adult profile as a species-family reference.
  Review: Viewed all directions: whole-body profile, paired feet/occluded far limbs, camel muzzle and long neck; rear has no front dulla or face features. One rear hump is present, but its spherical shading should blend more naturally into the shoulders in composed refinement.
  Inputs: [{"path": "art/conversion/body-dromad-child/v1/refined-front.png", "sha256": "e7b0d5a3a896e64c2ec3cf5d8c449d4e17797d196a4d0f3764126f220ba9d406"}, {"path": "art/conversion/body-dromad/v1/selected-east.png", "sha256": "4e25b4f69b77b132f0b55aaeaf0cf7669661ec4f02c19c1ccf3dc3f889e56caf"}, {"path": "art/conversion/body-dromad-child/v1/secondary-views-prompt.txt", "sha256": "4cf01ff26331d7e3680ee2b19adcc6a1ae36e02f85e82fa6f47eb68fa414b8f7"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/secondary-views.png", "sha256": "9c58361c34b8f75b42cfdc6471c0538ef5c5c4daef0f556db91ccd1207caa947"}]
  Method/prompt/corrections: {"phase": "Front-guided child dromad profile/rear proposals", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-939e1d50-0c07-415f-b1ef-7b38a6b9fcb4.png"}

- 2026-10-20T02:23:29.122151+00:00 / correct_and_refine_composite / RECORDED: Selected complete connected figures, cleared low-alpha/invisible RGB and neutralized grayscale. Applied one common .78 scale, then whole-figure translation to the shared contact without independent facing fitting.
  Review: Figure ownership retains whole muzzles, ears, hands and feet. Compact proportions and structural features retained. Rear hump shading blend remains the targeted composed-refinement item; no native acceptance claimed.
  Inputs: [{"path": "art/conversion/body-dromad-child/v1/secondary-views.png", "sha256": "9c58361c34b8f75b42cfdc6471c0538ef5c5c4daef0f556db91ccd1207caa947"}, {"path": "art/conversion/body-dromad-child/v1/prepare-views.py", "sha256": "12d2ee6ecace1987f2166fb35f06d76f3c8e082fa7e6db081b07997b4f6d91c1"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/patched-views.png", "sha256": "9ff5201b358399fa855db5c7b9cdca330301a1d56711758afa8643e98d62b8fe"}, {"path": "art/conversion/body-dromad-child/v1/patch-decisions.json", "sha256": "db2d49cd05d4fc15ad7813b8638d932cb14a0618160cb37c132edd452c4e83b2"}, {"path": "art/conversion/body-dromad-child/v1/source-selection-south.png", "sha256": "b1b15defa915ccc84e7d0d48f20d2c4084b0efdefa8a86b8abd76eff74e480fb"}, {"path": "art/conversion/body-dromad-child/v1/source-selection-east.png", "sha256": "7b8d9780c1a5c98bbb313fa777a599cb9dcdbacae7a04f3d7d811605b7824363"}, {"path": "art/conversion/body-dromad-child/v1/source-selection-north.png", "sha256": "7770214bbfdf3b0eeca30c341c47e4ac1054adf170a7c2373015721c342ea2ce"}]
  Method/prompt/corrections: {"phase": "Complete silhouette selection and neutral centered frames"}

- 2026-10-20T02:27:45.046844+00:00 / correct_and_refine_composite / PASS: Refined the neutral patched views with a focused organic rear-hump shading blend while retaining the compact family design.
  Review: Viewed all three: smooth blank mannequin, structural camel muzzle/ears, long neck/dulla, coherent whole-body side and one shoulder-integrated rear hump. No face marks, clothing, tail or extra appendages. Juvenile forms remain authored interpretation.
  Inputs: [{"path": "art/conversion/body-dromad-child/v1/patched-views.png", "sha256": "9ff5201b358399fa855db5c7b9cdca330301a1d56711758afa8643e98d62b8fe"}, {"path": "art/conversion/body-dromad-child/v1/refine-patched-prompt.txt", "sha256": "ffe2b4bd42dc866ddc3afa6bf40b5abc717dcdbf839463aeb4d14a46f23eb780"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/refined-patched-views.png", "sha256": "85311116fb01ce60c0fff28573ad7424eb9a4c0a1213b23b40ea0b58d5c80a09"}]
  Method/prompt/corrections: {"phase": "Selected composed child dromad refinement", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-bacbf565-ae73-487d-bf69-774b7e10ff0e.png"}

- 2026-10-20T02:27:45.048054+00:00 / register_body_head_and_palette / PASS: Re-established masks on the actual 1489 x 1056 refinement. Used complete connected silhouettes, one .84 image scale and shared contact (256, 950). Head owns the full long-neck/dulla outline; body owns hump/painted limbs, with two-source-pixel underlap. Detail remains separate neutral coverage.
  Review: Viewed neutral assembly and colored ownership: complete muzzles/ears/hands/feet and neck contour, no neck gap. All production RGB is neutral; no rear dulla layer rendered. Source and refined selection masks are separate evidence. Clothing is not accepted by this body step.
  Inputs: [{"path": "art/conversion/body-dromad-child/v1/refined-patched-views.png", "sha256": "85311116fb01ce60c0fff28573ad7424eb9a4c0a1213b23b40ea0b58d5c80a09"}, {"path": "art/conversion/body-dromad-child/v1/register-layers.py", "sha256": "6fd900a2d1f18a9f36c91f40904b66617c593a185cda4d7eddc8166234f38601"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/model.json", "sha256": "32f94245623581bfbbd45d1385f55cf1e4a74ab143f036906cfe34c9c43628d5"}, {"path": "art/conversion/body-dromad-child/v1/registration-decisions.json", "sha256": "99153376dff3158f5a5307b83e82a8999f665fcf812b0aef055502d1df135de3"}, {"path": "art/conversion/body-dromad-child/v1/registration-comparison.png", "sha256": "f81a14963e11cc6c97a79f0ebe8750e792fb002b9e96414e77875b8dc5db8639"}, {"path": "art/conversion/body-dromad-child/v1/ownership-comparison.png", "sha256": "b24a730e915ee0a1cc8b5b07737334dcbddfa70954a9d338c9520258f377ee9e"}, {"path": "art/conversion/body-dromad-child/v1/body-south.png", "sha256": "ff5622736e308c278eec00ad2df64037b32b578b32d017c0113f456c8841f7f2"}, {"path": "art/conversion/body-dromad-child/v1/head-south.png", "sha256": "af99746d35bc93499b5a5da2f009cc1cde791c999cdca0ef94384c7f2499f0dd"}, {"path": "art/conversion/body-dromad-child/v1/head-detail-south.png", "sha256": "5bbfc050ca208a00e6b9dd74592f333b42700b5c965d30fdf7da596b272e9130"}, {"path": "art/conversion/body-dromad-child/v1/body-mask-south.png", "sha256": "7a11f9d064d90d27bcec8f93eee46bc5b975b9b568ae8e71c4b6226b90e74025"}, {"path": "art/conversion/body-dromad-child/v1/head-mask-south.png", "sha256": "5253485f7b69cf00a24d55c48826f049f6094e855c7a3283a1de1202b626a8e4"}, {"path": "art/conversion/body-dromad-child/v1/head-detail-mask-south.png", "sha256": "ceec238da9716bd84f52da3fd30a71a3812c17b7fb02ef6459cfd633baaab66a"}, {"path": "art/conversion/body-dromad-child/v1/refined-selection-south.png", "sha256": "2f4fd53d7cb25786357b0d8a1d575ec0318898764a75de29a714b4185d3d858c"}, {"path": "art/conversion/body-dromad-child/v1/body-east.png", "sha256": "9f4387129f2ce8e06438f31f3f4d67652a2021af8b5c6a9e9c61e7f88e70414c"}, {"path": "art/conversion/body-dromad-child/v1/head-east.png", "sha256": "9315c16da2d8e38e6d582082d7b05f3a40d1827d218e92ec0c8c4201cdde2573"}, {"path": "art/conversion/body-dromad-child/v1/head-detail-east.png", "sha256": "d679fbddab85401c1aee40a4a2e32566c77e588b414f26acaf51772419da462f"}, {"path": "art/conversion/body-dromad-child/v1/body-mask-east.png", "sha256": "6a6f072fc268cf1f4e8b53725ce1480864804176be5e8440edff26cee7da0d85"}, {"path": "art/conversion/body-dromad-child/v1/head-mask-east.png", "sha256": "4eeabba27823a1ed7dbd205cbeac67e73051f7d251fd83b8311ba781b4078f74"}, {"path": "art/conversion/body-dromad-child/v1/head-detail-mask-east.png", "sha256": "773606e70c3e3bb47cbdf8257bca656e2bb8a19f4f706e594d68ede7b35ddada"}, {"path": "art/conversion/body-dromad-child/v1/refined-selection-east.png", "sha256": "46feb31a7ea96069f8806fdb5fba9f7a4fbd3c5e8a567074a7ed88aaf5516ba9"}, {"path": "art/conversion/body-dromad-child/v1/body-north.png", "sha256": "b95bf2c80a7560e37c82ab47614039024312a2808f201b526a946c0cac52e2af"}, {"path": "art/conversion/body-dromad-child/v1/head-north.png", "sha256": "f73424a7e50dcbbe364a9715fd55a5bb13f3a79594e546ca2945a1065a9334d1"}, {"path": "art/conversion/body-dromad-child/v1/head-detail-north.png", "sha256": "2acc469cc3de6a04146417767c4c3312adc41d8b3d9270af3094068c2a66832d"}, {"path": "art/conversion/body-dromad-child/v1/body-mask-north.png", "sha256": "976ce09bed9e151ebf90d1b05a7caa2a5cc3185c0a7e0b6e940d8db5a9ea1bf1"}, {"path": "art/conversion/body-dromad-child/v1/head-mask-north.png", "sha256": "0ff572ebc00e09baef7ba74100ce3845ddf92c10690fb830c1d23cf6b3888a75"}, {"path": "art/conversion/body-dromad-child/v1/head-detail-mask-north.png", "sha256": "52848c292a9768d088119562c36fcd5fa3ca7b485fba3187cf50e4c6aa8b4988"}, {"path": "art/conversion/body-dromad-child/v1/refined-selection-north.png", "sha256": "a0bc1d8d1b0509ad4ae206a5be4496b1515a4e96a8a612fa98750e8028bdf0cc"}]
  Method/prompt/corrections: {"phase": "Centered child dromad layers and ownership"}

- 2026-10-20T02:27:45.050266+00:00 / visual_review_all_views / PASS: Reviewed front, whole-body profile, rear, mirrored west and intended-size authoring previews.
  Review: Same family as adult, compact smooth body and blank face, paired simple feet and proper profile overlap. Identical centered contact and fixed component frame. Male/female labels share geometry; no unsupported body difference invented. Generation-ready only.
  Inputs: [{"path": "art/conversion/body-dromad-child/v1/model.json", "sha256": "32f94245623581bfbbd45d1385f55cf1e4a74ab143f036906cfe34c9c43628d5"}, {"path": "art/conversion/body-dromad-child/v1/registration-comparison.png", "sha256": "f81a14963e11cc6c97a79f0ebe8750e792fb002b9e96414e77875b8dc5db8639"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/game-scale-review.png", "sha256": "2df17adc3e7ce87f3ad836b9dc63c2dcfaa366484774916c769593b3b1289f25"}, {"path": "art/conversion/body-dromad-child/v1/selected-south.png", "sha256": "089fe4d83f08ac294e553feedbf38e14e8b6ebfcc46faee2d2d1615541a93cd5"}, {"path": "art/conversion/body-dromad-child/v1/selected-east.png", "sha256": "3984f807e31296597f88023161d484aacd506772b9893a3630dd5cc2abc704a9"}, {"path": "art/conversion/body-dromad-child/v1/selected-north.png", "sha256": "6e71f8f97d966f6bf451b33c12ecc69c269400337f7d8f95ed10e19788ff1cac"}]
  Method/prompt/corrections: {"phase": "Child dromad body authoring ready"}

- 2026-10-20T02:27:45.050877+00:00 / record_native_selection_policy_without_changing_demographics / PASS: Recorded authored child-scale variant without assigning an age or new equipment to Tam. Preserved canonical juvenile/dulla-development uncertainty and the full baseline source metadata.
  Review: Physical height .98 is an authoring choice, not native evidence. No child age selector or observed child outfit is assumed. FIT-DROMAD-CHILD-TEMPLATE-TUNIC still owns separate garment work; native acceptance waits for all conversions.
  Inputs: [{"path": "art/conversion/body-dromad-child/v1/source-packet.json", "sha256": "95ce9f3839ead77ff4392aeeb6f29782dcb54784a2b61bf04cf6a8392f5aa0a2"}]
  Outputs: [{"path": "art/conversion/body-dromad-child/v1/model.json", "sha256": "32f94245623581bfbbd45d1385f55cf1e4a74ab143f036906cfe34c9c43628d5"}]
  Method/prompt/corrections: {"phase": "Juvenile template selection and separate garment policy"}

### BODY-GLOWFISH: glowfish

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/glowfish/body-east.png](../art/village/bodies/glowfish/body-east.png), [art/village/bodies/glowfish/body-north.png](../art/village/bodies/glowfish/body-north.png), [art/village/bodies/glowfish/body-south.png](../art/village/bodies/glowfish/body-south.png), [art/village/bodies/glowfish/model.json](../art/village/bodies/glowfish/model.json), [art/village/bodies/glowfish/turnaround-prompt.txt](../art/village/bodies/glowfish/turnaround-prompt.txt), [art/village/bodies/glowfish/turnaround.png](../art/village/bodies/glowfish/turnaround.png).

Current step: not started. Process-log events: 0.

### BODY-HUMAN-CHILD: human child (featureless body with separate clothing)

Required steps: resolve_age_evidence_and_render_reference -> construct_featureless_front -> generate_other_views -> correct_and_refine_composite -> register_body_head_and_palette -> visual_review_all_views -> record_native_selection_policy_without_changing_demographics.

Required views/states: male/female templates; shared geometry if no supported distinction; south/east/north; west mirror; separate removable clothing.

Historical artifacts: [art/village/age-templates/human/body-east.png](../art/village/age-templates/human/body-east.png), [art/village/age-templates/human/body-north.png](../art/village/age-templates/human/body-north.png), [art/village/age-templates/human/body-south.png](../art/village/age-templates/human/body-south.png), [art/village/age-templates/human/head-east.png](../art/village/age-templates/human/head-east.png), [art/village/age-templates/human/head-north.png](../art/village/age-templates/human/head-north.png), [art/village/age-templates/human/head-south.png](../art/village/age-templates/human/head-south.png), [art/village/age-templates/human/tunic-east.png](../art/village/age-templates/human/tunic-east.png), [art/village/age-templates/human/tunic-north.png](../art/village/age-templates/human/tunic-north.png), [art/village/age-templates/human/tunic-south.png](../art/village/age-templates/human/tunic-south.png).

Current step: generation ready; final acceptance pending. Process-log events: 9.

- 2026-10-20T01:45:04.251439+00:00 / resolve_age_evidence_and_render_reference / PASS: Bound the child template to captured unmutated human anatomy, original clothed Qud human glyphs and installed Biotech child torso references.
  Review: Viewed actual donor child torso and contextual source plate. Donor child body provides proportions/shading, not an articulated anatomy. No child resident or sex-specific anatomy is established; both template labels share geometry. Separate garment entries retain the full clothing workflow.
  Inputs: [{"path": "art/conversion/body-human-male/v1/source-packet.json", "sha256": "4cf5319cc280332acf3f9fcae315c1e298868cee108f972d656685c93fce57d6"}, {"path": "art/conversion/body-human-female/v1/source-packet.json", "sha256": "0949e4f13981fe60ebc6eb57acc6766066efe506dbcee1b432e274d2a9a1476e"}, {"path": "evidence/joppa-creature-catalogue.json", "sha256": "de8affadee7f4260a8ec68a81e6d6e5f7c98c627a7b29ddcbae3668c6cfd4a79"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/source-packet.json", "sha256": "dea67080f65ad1ada0e3de98e465f7046deb3d94f92e019a60bb8cd464f13cc0"}, {"path": "art/conversion/body-human-child/v1/source-comparison.png", "sha256": "7303b69862b929edc78a6ab999631202ddadc1d5e23e709afc8f67206be407b4"}]
  Method/prompt/corrections: {"phase": "Human body facts and actual child reference"}

- 2026-10-20T01:45:04.251973+00:00 / construct_featureless_front / PASS: Constructed a smooth child-proportion mannequin with a relatively larger head, short limbs and distinct feet, keeping ordinary human part counts.
  Review: Viewed editable front and render. One blank head, two arms/hands, two legs/feet; no anatomical detail or garment baked into the body. Foot contours will be refined to remove the construction ankle seam.
  Inputs: [{"path": "tools/construct_child_human.py", "sha256": "b6ecfdfcbafa025ad99b8b31a51a0b7fde8bcea174be36d267510c1757c2579d"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/constructed-front.svg", "sha256": "40f73a0071f7d67a51a2cc4a732ca095b8832eeaf90e65be93aa53bd9c9e8c04"}, {"path": "art/conversion/body-human-child/v1/constructed-front.png", "sha256": "c486b08813e1ccd8522bcdd186ced3037a58842c9936b3c6f6d7c757c7eb09a6"}]
  Method/prompt/corrections: {"phase": "Manual featureless child front"}

- 2026-10-20T01:45:58.648622+00:00 / construct_featureless_front / PASS: Refined the manual front with its annotated original/donor comparison plate.
  Review: Viewed the complete blank-headed compact mannequin. Same simple human limb counts, larger relative head and seamless foot forms; no anatomical detail, clothes, accessories or personal cosmetics. Selected as the secondary-view anchor.
  Inputs: [{"path": "art/conversion/body-human-child/v1/constructed-front.png", "sha256": "c486b08813e1ccd8522bcdd186ced3037a58842c9936b3c6f6d7c757c7eb09a6"}, {"path": "art/conversion/body-human-child/v1/source-comparison.png", "sha256": "7303b69862b929edc78a6ab999631202ddadc1d5e23e709afc8f67206be407b4"}, {"path": "art/conversion/body-human-child/v1/refine-front-prompt.txt", "sha256": "6acda85d7ddc383c79f5ca58dc426961f8e2e180a97706b8150b15142e3888b6"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/refined-front.png", "sha256": "b651e3e81fa4e0c8aef1e35b7884aad99c6d3983e7a1e8ab0c774016be0f085e"}]
  Method/prompt/corrections: {"phase": "Selected refined featureless front", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-bcb1d989-35b1-4f13-b720-f3d2033f60de.png"}

- 2026-10-20T01:47:25.875760+00:00 / generate_other_views / PASS: Generated a three-direction proposal from the selected featureless front and explicit ordinary humanoid body facts.
  Review: Viewed complete figures: relative head size and short limbs remain consistent. Side is a whole-body profile with occluded far limbs; back has rear heels and no face. No clothes, cosmetics, mutation appendages or anatomical details.
  Inputs: [{"path": "art/conversion/body-human-child/v1/refined-front.png", "sha256": "b651e3e81fa4e0c8aef1e35b7884aad99c6d3983e7a1e8ab0c774016be0f085e"}, {"path": "art/conversion/body-human-child/v1/secondary-views-prompt.txt", "sha256": "0edb44f78087ebe38d4114f6ccb400a618b0a320b38edc406ea8dc81eea921fc"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/secondary-views.png", "sha256": "fb8708e57eb986106efe162a564533729853bc347e2401685d7bd2a55c973b09"}]
  Method/prompt/corrections: {"phase": "Child side and rear proposals", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-b4066096-e887-4598-b056-99c1062665cd.png"}

- 2026-10-20T01:47:25.877456+00:00 / correct_and_refine_composite / RECORDED: Used inspected complete-figure regions, cleaned low-alpha/invisible RGB and neutralized grayscale. Scaled every view by the same 0.79 factor and translated whole figures to the common centered contact; added report-only direction labels.
  Review: No anatomy/count repair was needed. This patch records palette and frame placement before the required composed refinement; visual selection follows inspection.
  Inputs: [{"path": "art/conversion/body-human-child/v1/secondary-views.png", "sha256": "fb8708e57eb986106efe162a564533729853bc347e2401685d7bd2a55c973b09"}, {"path": "art/conversion/body-human-child/v1/prepare-views.py", "sha256": "57967b3e1307a4c49ab038adfa6e28f52b5944c826ba6c639ca63178e7d81521"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/patched-views.png", "sha256": "5bfa28e78412e2aee9b3a6fb51b565e62fb303158898db986e1fca60720914ac"}, {"path": "art/conversion/body-human-child/v1/patch-decisions.json", "sha256": "cb5e2c663cd23303dfcef17cdacca17fb64390542f72f47092a00b9d97ac92d0"}, {"path": "art/conversion/body-human-child/v1/patched-south.png", "sha256": "811607058bbeadcf97c71f3c045a62dae56aaef4077ef9ab10dba33b4eb98f08"}, {"path": "art/conversion/body-human-child/v1/patched-east.png", "sha256": "bef407c213d25fba66ec963ca61fa9c3429c74cb79c2f1a36bbb98e95eea3af6"}, {"path": "art/conversion/body-human-child/v1/patched-north.png", "sha256": "54f0d5f292112501377995320116aec2b7671ca3f60df51e4222047c099e1c8a"}]
  Method/prompt/corrections: {"phase": "Patched neutral child views in a shared frame"}

- 2026-10-20T01:49:12.047037+00:00 / correct_and_refine_composite / PASS: Refined the patched sheet conservatively, retaining the larger relative head and short simple limbs.
  Review: Viewed the complete front, whole-body side and rear. Smooth featureless surfaces, compact family proportions, correct head/torso rotation and rear heels. No anatomical detail, garments, personal features or mutation appendages.
  Inputs: [{"path": "art/conversion/body-human-child/v1/patched-views.png", "sha256": "5bfa28e78412e2aee9b3a6fb51b565e62fb303158898db986e1fca60720914ac"}, {"path": "art/conversion/body-human-child/v1/refine-patched-prompt.txt", "sha256": "7a6635fff0b01d71805eb485dec1c408214eabca5b0e35f2da1ed74a2760ef6e"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/refined-patched-views.png", "sha256": "cb30f6c8841cfb77d641910321f88705c31f931d5485a8cf01d6ac1449b2d7eb"}]
  Method/prompt/corrections: {"phase": "Refined corrected child turnaround", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-500fa2eb-064b-450d-9682-b723986c3189.png"}

- 2026-10-20T01:49:12.048065+00:00 / register_body_head_and_palette / PASS: Authored masks on the actual 1490 x 1056 refinement and registered whole views/layers to contact (256, 950). Kept one physical pixel scale, separate head/neck, painted body limbs and neutral grayscale. Both template labels point to the same geometry.
  Review: Viewed all-view recomposition and colored ownership. Complete hands/feet, head owns neck, shoulders belong to body, no seam gap or clipped figure. Identical centered anchors. Clothing remains separate and unaccepted in FIT-HUMAN-CHILD-TEMPLATE-TUNIC.
  Inputs: [{"path": "art/conversion/body-human-child/v1/refined-patched-views.png", "sha256": "cb30f6c8841cfb77d641910321f88705c31f931d5485a8cf01d6ac1449b2d7eb"}, {"path": "art/conversion/body-human-child/v1/register-layers.py", "sha256": "ddf06bcf67a9862e61d5694a891218aaef2de402b6845a10e976e2119ac855a9"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/model.json", "sha256": "77b2b615a62c4bd0166b644c85e924686d57b4829dbc7cdaee125059483c5665"}, {"path": "art/conversion/body-human-child/v1/registration-decisions.json", "sha256": "e17b633c8a4d6a63348a91d59ec6c71cd86bdcba63c31f610b3c356276649afa"}, {"path": "art/conversion/body-human-child/v1/ownership-comparison.png", "sha256": "9b6a6906af4715c5a8c2347c5731d8bc7355045e1b086299370f0c67edab51d4"}, {"path": "art/conversion/body-human-child/v1/registration-comparison.png", "sha256": "946ed8fbd17eeede747c863e0438b7399b91036632e91c0dbc4a2e1c73293b71"}, {"path": "art/conversion/body-human-child/v1/body-south.png", "sha256": "a783e5d2987771e803e8299aacce0ddc5b50910dfa6b98022716388d8cdf9bc4"}, {"path": "art/conversion/body-human-child/v1/head-south.png", "sha256": "89058c508cce09ac97baba77a15b135dbb30a9f931725d36229c6366c4a2c51b"}, {"path": "art/conversion/body-human-child/v1/body-mask-south.png", "sha256": "325faf501e1b78aceee53975a7d59fad16958f1026b24ade5aaf5697e6ffecb2"}, {"path": "art/conversion/body-human-child/v1/head-mask-south.png", "sha256": "e600bb713f40b0f07d6d45092c639e2adbb29ef144d9e629228c031fca6cfc2c"}, {"path": "art/conversion/body-human-child/v1/body-east.png", "sha256": "20a0d8298c1ddf78767140e4db9f7af4ab9921de8918d551ba124b58cf2eb084"}, {"path": "art/conversion/body-human-child/v1/head-east.png", "sha256": "a901fff8585e83dcd3d4ab6bdb2534e2d6550490d7126803e0be50fb98ba9c30"}, {"path": "art/conversion/body-human-child/v1/body-mask-east.png", "sha256": "de858f7e112950e55bf93251783a8c31821739277d7ea54e23a3beb0cab3c70c"}, {"path": "art/conversion/body-human-child/v1/head-mask-east.png", "sha256": "765cba5b34a7316079679ca0f2486e9bc879359a69091b9c171b45b0f8ec003a"}, {"path": "art/conversion/body-human-child/v1/body-north.png", "sha256": "0325738b8d176d7c84641fcc3c54d6ec49bd650a1062d2eba40afcb380cd99b3"}, {"path": "art/conversion/body-human-child/v1/head-north.png", "sha256": "fec24773d3497d14c1c5f8725faac7e0f1b5a46be8a72408a784cea3e063b21a"}, {"path": "art/conversion/body-human-child/v1/body-mask-north.png", "sha256": "2bfca07a3360204fa50bb1f95cb2704c424130dd31e815484aa3285e28c4df86"}, {"path": "art/conversion/body-human-child/v1/head-mask-north.png", "sha256": "ca04204b0a63495fe627a2ff05078c40239fcc920a0bdb0905905f98189a91f5"}]
  Method/prompt/corrections: {"phase": "Centered child body/head and ownership masks"}

- 2026-10-20T01:49:12.049669+00:00 / visual_review_all_views / PASS: Reviewed front, east, back, mirrored west and intended-size authoring previews.
  Review: The compact featureless shape is readable at intended size, with smooth foot forms and coherent profile. Male/female templates share geometry because the source does not establish a required difference. Generation-ready body only; separate garment and native acceptance remain pending.
  Inputs: [{"path": "art/conversion/body-human-child/v1/model.json", "sha256": "77b2b615a62c4bd0166b644c85e924686d57b4829dbc7cdaee125059483c5665"}, {"path": "art/conversion/body-human-child/v1/registration-comparison.png", "sha256": "946ed8fbd17eeede747c863e0438b7399b91036632e91c0dbc4a2e1c73293b71"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/game-scale-review.png", "sha256": "366235d9ff3d0a33ea449515503934c65a52473a058a4bd0cc5a861d0e6ee132"}, {"path": "art/conversion/body-human-child/v1/selected-south.png", "sha256": "58b9c9becf365ac984a1d48f57aa04b6d2c228487f45846202a6fddd0aa5aae4"}, {"path": "art/conversion/body-human-child/v1/selected-east.png", "sha256": "2d477ce453ed8c39923d7c5c8263b7479942443839de94a0e87a10336104a4e2"}, {"path": "art/conversion/body-human-child/v1/selected-north.png", "sha256": "8cc3b5623073e471edd5ecd1685b1aeea12ad4f3ce942b66cef2a47115ed193c"}]
  Method/prompt/corrections: {"phase": "Child human body authoring ready"}

- 2026-10-20T01:49:12.050237+00:00 / record_native_selection_policy_without_changing_demographics / PASS: Recorded an authored child-size family without changing any villager, inferring a child resident or inventing a native age selector.
  Review: No demographics or runtime body/equipment selection changed. The .88 physical height is an explicit authoring choice. Separate removable clothing fitting and native batch acceptance still required.
  Inputs: [{"path": "art/conversion/body-human-child/v1/source-packet.json", "sha256": "dea67080f65ad1ada0e3de98e465f7046deb3d94f92e019a60bb8cd464f13cc0"}]
  Outputs: [{"path": "art/conversion/body-human-child/v1/model.json", "sha256": "77b2b615a62c4bd0166b644c85e924686d57b4829dbc7cdaee125059483c5665"}]
  Method/prompt/corrections: {"phase": "Child selection policy and separate clothing requirement"}

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

Current step: construct_shape. Process-log events: 4.

- 2026-10-20T02:30:30.102304+00:00 / source_identity_description_metadata / RECORDED: Selected Woven Tunic and retained exact original glyph/palette/description plus captured Body attachment IDs and laterality from its existing source packet.
  Review: Read the item/body source packets. No child-dromad outfit or age selector is inferred; this is a removable authored fitting. Base body/head/dulla and contact remain fixed.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-packet.json", "sha256": "d2e65664d4c5d53d41ba6018733f10526ea33dc7b191e78f2fa537fda36fcf4a"}, {"path": "art/conversion/body-dromad-child/v1/model.json", "sha256": "32f94245623581bfbbd45d1385f55cf1e4a74ab143f036906cfe34c9c43628d5"}]
  Outputs: [{"path": "art/conversion/fit-dromad-child-woven-tunic/v1/source-packet.json", "sha256": "f4dbdd2f99bea2ff1b3d7b25db587ff8b82cc5590d2587b8aaa918083c0638c7"}, {"path": "art/conversion/fit-dromad-child-woven-tunic/v1/source-comparison.png", "sha256": "d0908c92414609e45044483a64bb935f4471f03eb28bba8ee245a1ec816b2a67"}]
  Method/prompt/corrections: {"phase": "Real Qud tunic identity and attachment evidence"}

- 2026-10-20T02:30:30.102871+00:00 / original_and_render_reference_decision / RECORDED: Prepared a contextual comparison of original Qud Woven Tunic, the fixed child dromad and our selected human-tunic flax/rope design.
  Review: The material design may be shared, while the long-neck/hump/profile geometry requires its own construction and coverage. Actual donor creature/child references remain linked; no human garment fit is accepted for dromads.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-packet.json", "sha256": "d2e65664d4c5d53d41ba6018733f10526ea33dc7b191e78f2fa537fda36fcf4a"}, {"path": "art/conversion/body-dromad-child/v1/model.json", "sha256": "32f94245623581bfbbd45d1385f55cf1e4a74ab143f036906cfe34c9c43628d5"}]
  Outputs: [{"path": "art/conversion/fit-dromad-child-woven-tunic/v1/source-packet.json", "sha256": "f4dbdd2f99bea2ff1b3d7b25db587ff8b82cc5590d2587b8aaa918083c0638c7"}, {"path": "art/conversion/fit-dromad-child-woven-tunic/v1/source-comparison.png", "sha256": "d0908c92414609e45044483a64bb935f4471f03eb28bba8ee245a1ec816b2a67"}]
  Method/prompt/corrections: {"phase": "Source item, fixed species base and selected material design"}

- 2026-10-20T02:31:46.335611+00:00 / source_identity_description_metadata / PASS: Reviewed the resolved Woven Tunic packet and contextual source/base/material plate before garment construction.
  Review: Real Qud item, exact coarse-flax/hemp-rope description and Body/laterality 0 attachment evidence retained. Child-dromad fitting remains authored and ungenerated; no new outfit/age assignment inferred.
  Inputs: [{"path": "art/conversion/fit-dromad-child-woven-tunic/v1/source-packet.json", "sha256": "f4dbdd2f99bea2ff1b3d7b25db587ff8b82cc5590d2587b8aaa918083c0638c7"}]
  Outputs: [{"path": "art/conversion/fit-dromad-child-woven-tunic/v1/source-comparison.png", "sha256": "d0908c92414609e45044483a64bb935f4471f03eb28bba8ee245a1ec816b2a67"}]
  Method/prompt/corrections: {"phase": "Source item and fixed-body packet reviewed"}

- 2026-10-20T02:31:46.335993+00:00 / original_and_render_reference_decision / PASS: Selected the existing source-bound flax/rope treatment as a material reference, with the actual child-dromad donor/metadata references linked through its body packet.
  Review: Viewed original glyph, fixed camelfolk body and selected tunic material. Human garment placement will not be reused as a dromad fit. Long neck, hump and painted near arm require their own garment coverage.
  Inputs: [{"path": "art/conversion/fit-dromad-child-woven-tunic/v1/source-packet.json", "sha256": "f4dbdd2f99bea2ff1b3d7b25db587ff8b82cc5590d2587b8aaa918083c0638c7"}, {"path": "art/conversion/body-dromad-child/v1/source-packet.json", "sha256": "95ce9f3839ead77ff4392aeeb6f29782dcb54784a2b61bf04cf6a8392f5aa0a2"}]
  Outputs: [{"path": "art/conversion/fit-dromad-child-woven-tunic/v1/source-comparison.png", "sha256": "d0908c92414609e45044483a64bb935f4471f03eb28bba8ee245a1ec816b2a67"}]
  Method/prompt/corrections: {"phase": "Material reuse and species-specific fit boundary reviewed"}

### FIT-HUMAN-CHILD-TEMPLATE-TUNIC: human child / tunic

Required steps: source_identity_description_metadata -> original_and_render_reference_decision -> construct_shape -> create_required_views_states -> correct_errors_and_refine -> extract_register_palette_masks -> visual_review_all_views_at_game_scale -> native_review_applicable_states.

Required views/states: source/exclusion review.

Historical artifacts: [art/village/age-templates/human/tunic-east.png](../art/village/age-templates/human/tunic-east.png), [art/village/age-templates/human/tunic-north.png](../art/village/age-templates/human/tunic-north.png), [art/village/age-templates/human/tunic-south.png](../art/village/age-templates/human/tunic-south.png).

Current step: generation ready; final acceptance pending. Process-log events: 14.

- 2026-10-20T01:51:31.357715+00:00 / source_identity_description_metadata / RECORDED: Selected Woven Tunic, preserved its original tile/palette and exact coarse-flax/hemp-rope description, and bound the authored fitting to the unchanged child body.
  Review: Exact original reference hash matched. This resolves the previously generic template garment identity; no child was observed wearing it and no native child selector is assumed. Construction, refinement, extraction and fitting are still unfinished.
  Inputs: [{"path": "art/village/sources.json", "sha256": "b0a2de847e29d251f500f81fc25aa3eacec393b4af78370c2a490e9f2706ec22"}, {"path": "evidence/village-reference-index.json", "sha256": "cc00cbf6f72d5d4134efb3879d83b30988fcec4ae822cec8a340b072024ca149"}, {"path": "art/conversion/body-human-child/v1/model.json", "sha256": "77b2b615a62c4bd0166b644c85e924686d57b4829dbc7cdaee125059483c5665"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-packet.json", "sha256": "d2e65664d4c5d53d41ba6018733f10526ea33dc7b191e78f2fa537fda36fcf4a"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/source-comparison.png", "sha256": "118cc089221ad07315473e921b5929e9af527ad1ce5a3f757a34c5a05df82ffc"}]
  Method/prompt/corrections: {"phase": "Resolved the template tunic to an actual Qud item"}

- 2026-10-20T01:52:15.589851+00:00 / source_identity_description_metadata / PASS: Read the resolved source packet and captured adult Body attachments, preserving part IDs, laterality and item variants.
  Review: Eight captured Woven Tunic attachments use Body/laterality 0. Their plain, painted and feathered descriptions remain in the packet. Child fitting is authored and no child equipment assignment is assumed.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-packet.json", "sha256": "d2e65664d4c5d53d41ba6018733f10526ea33dc7b191e78f2fa537fda36fcf4a"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-comparison.png", "sha256": "118cc089221ad07315473e921b5929e9af527ad1ce5a3f757a34c5a05df82ffc"}]
  Method/prompt/corrections: {"phase": "Reviewed actual item and native attachment metadata"}

- 2026-10-20T01:52:15.590222+00:00 / original_and_render_reference_decision / PASS: Viewed the exact original item glyph beside the fixed child model and actual Biotech child torso.
  Review: Qud original and coarse-flax/hemp-rope description determine garment identity. The donor torso is used for compact presentation only, not as an invented garment or articulated model. Construction and separate in-context refinement/extraction still pending.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-packet.json", "sha256": "d2e65664d4c5d53d41ba6018733f10526ea33dc7b191e78f2fa537fda36fcf4a"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-comparison.png", "sha256": "118cc089221ad07315473e921b5929e9af527ad1ce5a3f757a34c5a05df82ffc"}]
  Method/prompt/corrections: {"phase": "Original Qud tunic and child presentation reference"}

- 2026-10-20T01:54:57.424034+00:00 / construct_shape / REJECTED: Constructed the source-bound short-sleeved flax tunic and waist rope over the fixed model. Caught a floating neckline rectangle and covered side forearm/hand before refinement.
  Review: Reject as final fitting. Collar subtraction was incorrect; the side garment also requires explicit painted-limb occlusion. Preserve the source construction and correct these issues.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-packet.json", "sha256": "d2e65664d4c5d53d41ba6018733f10526ea33dc7b191e78f2fa537fda36fcf4a"}, {"path": "art/conversion/body-human-child/v1/model.json", "sha256": "77b2b615a62c4bd0166b644c85e924686d57b4829dbc7cdaee125059483c5665"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/construct-garment-rejected-coverage.py", "sha256": "9d870873691f7101a04413747c4e77f596edbd1ea627a3f1f1e3d18cbc579b35"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-fit-rejected-coverage.png", "sha256": "cc2d806d7c56a7993ad6223b8ae8baa44dfeb64990fae463fe2ecbe7b8dd15af"}]
  Method/prompt/corrections: {"phase": "Rejected construction: collar and side coverage"}

- 2026-10-20T01:54:57.424843+00:00 / construct_shape / RECORDED: Replaced the neckline rectangle with a continuous garment boundary and added an explicit side-arm garment cutout. Kept the same original body/head pixels.
  Review: Viewed recomposition. Floating collar removed and side hand visible. This is the editable suggestion; the rough side-arm boundary still needs in-context cloth refinement before extraction/fit acceptance.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-packet.json", "sha256": "d2e65664d4c5d53d41ba6018733f10526ea33dc7b191e78f2fa537fda36fcf4a"}, {"path": "art/conversion/body-human-child/v1/model.json", "sha256": "77b2b615a62c4bd0166b644c85e924686d57b4829dbc7cdaee125059483c5665"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/construct-garment.py", "sha256": "ac0c3813aafbf43e165d9af53a1cd0b5c77a051fab7ca1a6f9fd7d22217aaead"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-fit-comparison.png", "sha256": "3b7a6dc33717daca80e7580714488dfdf90bf74bcddd41187bf350841324863a"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-isolated-comparison.png", "sha256": "7099d8c5c9df54859135ca701dc0d26dd82b368f0199f72798e969eb015182d6"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-side-arm-cutout.png", "sha256": "74536ac06b5564efcf53ff999856952a0ec2bdcb19a90d7c78b33cfcd15f8d9b"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-south.svg", "sha256": "6d4e28700bcac187514b72300e01003c40b511b5fc8c0302f17e6e108824be12"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-east.svg", "sha256": "727ee601e800e8fc39a045f551b0dc627db26d4e29c108cedaf838a6a20193fd"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-north.svg", "sha256": "37baf0460be36aacd69d657c581d9fd225ea5b7e53450bb300196927bef85345"}]
  Method/prompt/corrections: {"phase": "Corrected editable garment suggestion"}

- 2026-10-20T01:54:57.425773+00:00 / create_required_views_states / RECORDED: Constructed directional tunic geometry and waist rope for the same fixed child body, using a true profile sleeve and rear neckline.
  Review: All three complete clothing views supplied for in-context refinement. West will mirror east; front knot is absent from the rear. This does not accept the rough cut edge.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/construct-garment.py", "sha256": "ac0c3813aafbf43e165d9af53a1cd0b5c77a051fab7ca1a6f9fd7d22217aaead"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-south.png", "sha256": "518a076a2b04491765d224cbc87a9e6ba23bcd29c57bd40bf7df696388bce493"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-east.png", "sha256": "32d03233b67257b8f71d5d7e5c390098944c15031d6c49b7248c0b500fb49606"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-north.png", "sha256": "9283075586d0c90afda269034de183e1a15a43e0a2605331eb4b381d8d29542a"}]
  Method/prompt/corrections: {"phase": "Distinct front, profile and rear garment construction"}

- 2026-10-20T01:56:34.393181+00:00 / correct_errors_and_refine / RECORDED: Refined the single flax tunic and rope on the mannequin across front, profile and rear views.
  Review: Viewed cloth: coherent profile sleeve, forearm/hand visible, no floating collar, rope cinches waist and rear omits front knot. The generator also reframed the figures, so this image is a cloth design proposal; generated body pixels will not replace the fixed body. Extraction/registration must recover separate apparel in the original frame.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-fit-comparison.png", "sha256": "3b7a6dc33717daca80e7580714488dfdf90bf74bcddd41187bf350841324863a"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/refine-context-prompt.txt", "sha256": "b826b3076e8c8976376e58d2f936a3243fa60ae29bc296974b339e7311957a41"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/refined-context.png", "sha256": "13e1fc9b74f8efaed669359ad70dc2ab5811c8bdec78d024215550ffbef3f66e"}]
  Method/prompt/corrections: {"phase": "Woven Tunic refined in context", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-c972bb79-354c-448f-80ed-7a372aedf85c.png"}

- 2026-10-20T02:01:43.115339+00:00 / extract_register_palette_masks / RECORDED: Retrieved the refined tunic alone, using the garment-only construction as placement/topology reference.
  Review: Viewed isolated front/profile/back: no mannequin pixels or hand outlines. The service reframed the item and filled sleeve interiors; it omitted the profile arm cutout. Separate coverage/registration correction is required before fitting acceptance.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/refined-context.png", "sha256": "13e1fc9b74f8efaed669359ad70dc2ab5811c8bdec78d024215550ffbef3f66e"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-isolated-comparison.png", "sha256": "7099d8c5c9df54859135ca701dc0d26dd82b368f0199f72798e969eb015182d6"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/isolate-garment-prompt.txt", "sha256": "39f420b795685eb9f068c55f118744c2c108f8a0cfe57f50ab5857c09f2f375d"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/isolated-proposal.png", "sha256": "5e42e5a47e93c7b990c7c53a91bff46a6e5379d6fcb0115bd2771aab3518de55"}]
  Method/prompt/corrections: {"phase": "Isolated clothing proposal", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-b39fdc7e-788a-4855-89ef-02406b1574a7.png"}

- 2026-10-20T02:01:43.117601+00:00 / extract_register_palette_masks / REJECTED: Registered the isolated cloth using one common scale and explicit anchors, then inspected its recomposition.
  Review: The front/back cuff cuts extended down the torso and removed cloth at its sides. Reject this mask placement; restrict those cuts to the actual sleeve region. Keep the side near-arm cutout.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/isolated-proposal.png", "sha256": "5e42e5a47e93c7b990c7c53a91bff46a6e5379d6fcb0115bd2771aab3518de55"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/register-garment-rejected-wide-cuts.py", "sha256": "7497274bd53ad6deeadff6dc9ea010fc3691504740521a61060d0c30cdb0809e"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/assembly-rejected-wide-cuts.png", "sha256": "a83ec71b196f4a8ea244ca644724691fd44bd9aad06ceb53f075239550a7f2cc"}]
  Method/prompt/corrections: {"phase": "Rejected first coverage cuts: side notches"}

- 2026-10-20T02:01:43.118882+00:00 / construct_shape / PASS: Selected the constructed short-sleeved flax/rope-waist design after the in-context refinement and corrected fitting review.
  Review: Viewed final recomposition: the source-bound plain tunic, short sleeves and rope cinch are retained, with a real profile sleeve and front-only knot. Earlier construction defects remain documented; final independent layer is the selected garment.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/source-packet.json", "sha256": "d2e65664d4c5d53d41ba6018733f10526ea33dc7b191e78f2fa537fda36fcf4a"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/construct-garment.py", "sha256": "ac0c3813aafbf43e165d9af53a1cd0b5c77a051fab7ca1a6f9fd7d22217aaead"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-south.svg", "sha256": "6d4e28700bcac187514b72300e01003c40b511b5fc8c0302f17e6e108824be12"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-east.svg", "sha256": "727ee601e800e8fc39a045f551b0dc627db26d4e29c108cedaf838a6a20193fd"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/constructed-north.svg", "sha256": "37baf0460be36aacd69d657c581d9fd225ea5b7e53450bb300196927bef85345"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/assembly-comparison.png", "sha256": "272ce1e35a220debce26e450a6f3295b56d0670a01779c487feef248fe5f164d"}]
  Method/prompt/corrections: {"phase": "Source-bound garment design retained"}

- 2026-10-20T02:01:43.119442+00:00 / create_required_views_states / PASS: Reviewed the selected front, side and back garment layers plus mirrored west over the fixed base.
  Review: Distinct directional fabric and neckline/rope views; no frontal shirt reused on the side. Rear omits the front knot. West is the documented east mirror; no native equipment state has been tested.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/isolated-proposal.png", "sha256": "5e42e5a47e93c7b990c7c53a91bff46a6e5379d6fcb0115bd2771aab3518de55"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/registration-decisions.json", "sha256": "000426e3101e031c0576a17c6d4add442d734dad599ae58166e8c4faedc76cd9"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/tunic-south.png", "sha256": "cba96fe1fe9d5a537028772e76f5c36a934e8cb4050294554b82aef444d256c5"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/tunic-east.png", "sha256": "16ac0451fbe5f2105f7a1a6fa7b3f35c74f9b74757fb87c044dfd83f0a67b5ed"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/tunic-north.png", "sha256": "fd92a757b11a158872b2babfaf6b25bd5359281b90f8892b238f6a19e834656d"}]
  Method/prompt/corrections: {"phase": "Directional garment views selected"}

- 2026-10-20T02:01:43.120729+00:00 / correct_errors_and_refine / PASS: Retained the in-context flax refinement and isolated garment, then corrected sleeve/near-arm coverage for the original fixed body.
  Review: Viewed all four facings: rope and fabric retain the refined design; no floating collar or side notches remain. Generated body pixels are excluded. The side forearm/hand and front/back hands remain the unchanged body artwork.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/refined-context.png", "sha256": "13e1fc9b74f8efaed669359ad70dc2ab5811c8bdec78d024215550ffbef3f66e"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/isolated-proposal.png", "sha256": "5e42e5a47e93c7b990c7c53a91bff46a6e5379d6fcb0115bd2771aab3518de55"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/register-garment.py", "sha256": "dfbd40280e855f41e0b5425da30384e24d1487fe6337cee5c8b2079d4039fd4e"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/assembly-comparison.png", "sha256": "272ce1e35a220debce26e450a6f3295b56d0670a01779c487feef248fe5f164d"}]
  Method/prompt/corrections: {"phase": "Refined cloth and corrected fitting selected"}

- 2026-10-20T02:01:43.122725+00:00 / extract_register_palette_masks / PASS: Neutralized isolated cloth to equal-channel grayscale; used common scale .54 and explicit per-view neck anchors. Authored sleeve/near-arm cuts, preserving all underlying body/head pixels. Reused existing item/equipment palette role and body->item->head layer order.
  Review: Inspected isolation and recomposition. The item contains fabric/rope only, no head/skin/hands/feet. Recorded alpha cuts prevent garment material/strokes from covering the actual forearm/hand. Source palette foreground &y/detail y uses a single independent equipment tint; native acceptance remains pending.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/isolated-proposal.png", "sha256": "5e42e5a47e93c7b990c7c53a91bff46a6e5379d6fcb0115bd2771aab3518de55"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/register-garment.py", "sha256": "dfbd40280e855f41e0b5425da30384e24d1487fe6337cee5c8b2079d4039fd4e"}, {"path": "art/conversion/body-human-child/v1/model.json", "sha256": "77b2b615a62c4bd0166b644c85e924686d57b4829dbc7cdaee125059483c5665"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/model.json", "sha256": "8f537f326efe47aac7047850ef7e73e60d39feb214b1cdb98c7cb7058ad71cea"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/registration-decisions.json", "sha256": "000426e3101e031c0576a17c6d4add442d734dad599ae58166e8c4faedc76cd9"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/registered-isolated-comparison.png", "sha256": "daa39426ed24278752fbdc918ccd13f11f254034b7836a3c8030319e49498854"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/coverage-cut-south.png", "sha256": "672928709c0f196d4139b52d8153ae2799b2bb443fd41104b8e75ebd445074e2"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/coverage-cut-east.png", "sha256": "7ebb68df5398969db990d8f457e085c0f7762cba4cf3d37d41150d742bb848ed"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/coverage-cut-north.png", "sha256": "672928709c0f196d4139b52d8153ae2799b2bb443fd41104b8e75ebd445074e2"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/tunic-south.png", "sha256": "cba96fe1fe9d5a537028772e76f5c36a934e8cb4050294554b82aef444d256c5"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/tunic-east.png", "sha256": "16ac0451fbe5f2105f7a1a6fa7b3f35c74f9b74757fb87c044dfd83f0a67b5ed"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/tunic-north.png", "sha256": "fd92a757b11a158872b2babfaf6b25bd5359281b90f8892b238f6a19e834656d"}]
  Method/prompt/corrections: {"phase": "Registered independent neutral clothing and coverage masks"}

- 2026-10-20T02:01:43.124433+00:00 / visual_review_all_views_at_game_scale / PASS: Reviewed enlarged and intended-size assembly, including front/profile/rear and mirrored west, with the fixed centered body.
  Review: Cloth reads as a separate tunic at intended size. Hands/feet remain visible; front rope knot differs from rear. Body/head source and their anchors are unchanged. This is generation-ready only; actual equip/unequip, palette selection and visibility checks wait for all conversions.
  Inputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/model.json", "sha256": "8f537f326efe47aac7047850ef7e73e60d39feb214b1cdb98c7cb7058ad71cea"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/assembly-comparison.png", "sha256": "272ce1e35a220debce26e450a6f3295b56d0670a01779c487feef248fe5f164d"}]
  Outputs: [{"path": "art/conversion/fit-human-child-woven-tunic/v1/game-scale-review.png", "sha256": "5e785054d36b150a17581f24f5ca2699087ea03573602bc7b583567d68b5f46c"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/assembled-south.png", "sha256": "f9de506041764af281b56fe1dd8e4600b976ba30d5dfeb79555cb4ce92604efb"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/assembled-east.png", "sha256": "05c879f04e0b78ed7942401949b4f58d378590cb69fd652b4510ff7a8817fff2"}, {"path": "art/conversion/fit-human-child-woven-tunic/v1/assembled-north.png", "sha256": "48cdf45d08693cbd48af484ba64f993a5c93e60fe26a2af2039549d813d9a295"}]
  Method/prompt/corrections: {"phase": "Child Woven Tunic authoring ready"}

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

Current step: generation ready; final acceptance pending. Process-log events: 10.

- 2026-10-20T01:35:46.927092+00:00 / resolve_age_evidence_and_render_reference / PASS: Resolved the authored older-female variant from the shared unmutated human base, original clothed female Qud glyphs and exact installed Core female torso/head references. Used Irudad only as an explicit old-age prose reference.
  Review: Viewed source/reference plate and read packet. Humanoid baseline has one head, two arms/hands and paired feet. No canonical older-female villager or age-specific donor torso is established. Mutations stay separate; no demographic reassignment.
  Inputs: [{"path": "art/village/sources.json", "sha256": "b0a2de847e29d251f500f81fc25aa3eacec393b4af78370c2a490e9f2706ec22"}, {"path": "art/conversion/body-human-female/v1/source-packet.json", "sha256": "0949e4f13981fe60ebc6eb57acc6766066efe506dbcee1b432e274d2a9a1476e"}, {"path": "art/conversion/body-human-female/v2/model.json", "sha256": "d98a479b61e27de71f0a616e400a53ea88ddcff1adce25ea90056e83c140c09b"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/source-packet.json", "sha256": "2af7e8861f73a39c111df6d66b8fda1cadb3d18d87dec450cdd564fcea51ede6"}, {"path": "art/conversion/body-human-female-older/v1/source-comparison.png", "sha256": "df977725c2c44829b0f085c5d3cd867102a5ef13c224948fc692fb7ae7571d82"}]
  Method/prompt/corrections: {"phase": "Source metadata, age evidence and actual donor reference"}

- 2026-10-20T01:35:46.927654+00:00 / construct_front_from_shared_human_base / PASS: Reviewed the preserved editable front constructed from shared female geometry, softening shoulders/torso while retaining the same head, hands, feet and family proportions.
  Review: Viewed the complete front: ordinary unmutated human mannequin, two arms/hands/legs and distinct bare feet. Age shape is an authored suggestion, ready for restrained refinement.
  Inputs: [{"path": "art/conversion/body-human-female/v1/constructed-front.svg", "sha256": "01c73dd1765553f6b1f56c6c7709a75e9685ae80a112f87bc2c980d78e987ccb"}, {"path": "tools/construct_older_human.py", "sha256": "4fc047dad3df73b87888cb21f577119fd32c6b8c9f9585f16a5dc17a3fea9c28"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/constructed-front.svg", "sha256": "a290240e6217088687b5b95d883c7592707fdc6f80fd8d18e842db23577add86"}, {"path": "art/conversion/body-human-female-older/v1/constructed-front.png", "sha256": "adff0e5bbf57e5fb57f4912c8f5bce90eceb38cb72712383fe5aaae603625810"}]
  Method/prompt/corrections: {"phase": "Manual older-female front"}

- 2026-10-20T01:36:44.721183+00:00 / refine_front / PASS: Refined the constructed older front with the selected adult female as the shared-family reference.
  Review: Viewed full returned front: same human family, softer shoulder/neck planes and relaxed abdomen, one blank head, two arms/hands and paired bare feet. No added mutation appendages, cosmetics, clothing or ankle cuffs. Age interpretation remains restrained rather than a new native demographic.
  Inputs: [{"path": "art/conversion/body-human-female-older/v1/constructed-front.png", "sha256": "adff0e5bbf57e5fb57f4912c8f5bce90eceb38cb72712383fe5aaae603625810"}, {"path": "art/conversion/body-human-female/v2/selected-south.png", "sha256": "4be9af44baa01447c0dfaa23abe8c93cd98218aafd681885987c793d62b039e6"}, {"path": "art/conversion/body-human-female-older/v1/refine-front-prompt.txt", "sha256": "be3ac0bcc6b228a2d6f8ae28f13141a4aeea0e12ca82978c7bc7e1e1b5dbaa58"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/refined-front.png", "sha256": "16b652fb75489439d569d1690da1da65001191f0d201f828189d7eb5cd9ee50f"}]
  Method/prompt/corrections: {"phase": "Refined older-female front selected", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 2}, "generation_file": "exec-234688e9-5b39-4400-9f31-ab00ed5c18de.png"}

- 2026-10-20T01:38:58.833156+00:00 / generate_other_views / PASS: Generated secondary views from the selected front plus explicit unmutated race facts and restrained age posture.
  Review: Viewed all three directions: the side rotates torso, arms, legs and feet, with mildly rounded upper back and forward head. Rear shows heels and no face. No mutation appendages or clothes. Apparent background glow is RGB in transparent pixels; alpha cleanup and registration follow.
  Inputs: [{"path": "art/conversion/body-human-female-older/v1/refined-front.png", "sha256": "16b652fb75489439d569d1690da1da65001191f0d201f828189d7eb5cd9ee50f"}, {"path": "art/conversion/body-human-female-older/v1/secondary-views-prompt.txt", "sha256": "6899915d37815091b6ac3639c54bc4ddcc383813f51c300164c60a89e9cf4c44"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/secondary-views.png", "sha256": "61adcf8ef78cbf1aeb4e029b16437ec8797cb85d262c5337e00de6ab23d5dc4b"}]
  Method/prompt/corrections: {"phase": "Older-female whole-body side and rear proposals", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-326c6176-3ac0-4470-bdd1-5e0bec1a651e.png"}

- 2026-10-20T01:38:58.834984+00:00 / patch_and_refine_composed_views / RECORDED: Separated complete figures using inspected unequal source regions, cleared low-alpha background RGB and neutralized gray. Applied one common 0.97 scale to all views to preserve margin, then translated each whole figure to the shared anchor. Added report-only direction labels.
  Review: Viewed patched sheet: complete hands/feet and coherent whole-body side orientation. No count or attachment correction needed. Ground contacts measured from actual alpha bounds replace approximate placements; composed refinement must preserve these shapes.
  Inputs: [{"path": "art/conversion/body-human-female-older/v1/secondary-views.png", "sha256": "61adcf8ef78cbf1aeb4e029b16437ec8797cb85d262c5337e00de6ab23d5dc4b"}, {"path": "art/conversion/body-human-female-older/v1/prepare-views.py", "sha256": "c233c5a896dfe9d5403e6238aab1a447b132974755afae9a0a1c1f8911b148de"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/patched-views.png", "sha256": "9e04a6d8ba76b4218a62216eaf9d6ef3ccfdded2d00c05c7e414149fd2546b8e"}, {"path": "art/conversion/body-human-female-older/v1/patch-decisions.json", "sha256": "6182ca973c9e017cbe65547b43b38649eb669bb5104c5cfe58775ea206f4c5a2"}, {"path": "art/conversion/body-human-female-older/v1/patched-south.png", "sha256": "23d550eb316aeddc8daa4caaaf4011bd2691ae09f6917777a96ac4ca2e545df9"}, {"path": "art/conversion/body-human-female-older/v1/patched-east.png", "sha256": "af232463a8a5568841d4f7e948a37cc813ef03b2f91e6ee8309daf8c7372ccf9"}, {"path": "art/conversion/body-human-female-older/v1/patched-north.png", "sha256": "379a366618f8903f8f17e0313b951fcd69c3dbbb1e69e8a47ad24fdc6476db46"}]
  Method/prompt/corrections: {"phase": "Neutral source, inspected view regions and centered contacts"}

- 2026-10-20T01:40:07.964781+00:00 / patch_and_refine_composed_views / FAIL: Submitted the patched sheet for restrained composed refinement. The service rejected its output and returned no image.
  Review: No image was available to inspect or accept. Preserve the failed attempt and use one simpler featureless drawing-mannequin brief.
  Inputs: [{"path": "art/conversion/body-human-female-older/v1/patched-views.png", "sha256": "9e04a6d8ba76b4218a62216eaf9d6ef3ccfdded2d00c05c7e414149fd2546b8e"}, {"path": "art/conversion/body-human-female-older/v1/refine-patched-prompt.txt", "sha256": "52f4cf4a0a14399bd878a2bed2c92aa3f437d2767dddf74dd7909bed2030695a"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/refine-patched-attempt-01.json", "sha256": "4d4081ba720ecc2df098610213bec11cebbd72fe5336b9031acb2634f509dda3"}]
  Method/prompt/corrections: {"phase": "Composed refinement attempt rejected by image service", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}}

- 2026-10-20T01:42:38.273778+00:00 / patch_and_refine_composed_views / PASS: Refined the patched neutral drawing-mannequin sheet with a simpler featureless brief after the rejected attempt.
  Review: Viewed all three complete figures. Same blank-headed human family and restrained older stance; side rotates the full body, back has heels. No clothing, mutation appendages or personal cosmetics. Selected for registration.
  Inputs: [{"path": "art/conversion/body-human-female-older/v1/patched-views.png", "sha256": "9e04a6d8ba76b4218a62216eaf9d6ef3ccfdded2d00c05c7e414149fd2546b8e"}, {"path": "art/conversion/body-human-female-older/v1/refine-patched-prompt-02.txt", "sha256": "9235f52d293736bdaf1d0fdaf9aa99a6f7a8b26b18c95ccff79d3f7f75d40a40"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/refined-patched-views.png", "sha256": "8123b887c86527a7aa6d6732d11d8c368bd1cc9f53469b3b188478806e064492"}]
  Method/prompt/corrections: {"phase": "Selected composed refinement", "tool": "image_gen.imagegen", "settings": {"transparent_background": true, "referenced_images": 1}, "generation_file": "exec-da2f40b0-bde2-44bd-91c8-7f8016a391f9.png"}

- 2026-10-20T01:42:38.275170+00:00 / register_body_head_and_palette / PASS: Inspected the actual 1489 x 1056 output rather than assuming equal panel dimensions. Authored neck masks with two-pixel body underlap, neutralized source and translated complete figures/layers to contact (256, 950). One physical pixel scale across every view and component.
  Review: Viewed centered four-facing recomposition and colored ownership. Head owns neck, body owns shoulders and painted limbs. No missing hands/feet or neck gaps; all views share identical canvas/contact without independent rescaling. Native acceptance remains pending.
  Inputs: [{"path": "art/conversion/body-human-female-older/v1/refined-patched-views.png", "sha256": "8123b887c86527a7aa6d6732d11d8c368bd1cc9f53469b3b188478806e064492"}, {"path": "art/conversion/body-human-female-older/v1/register-layers.py", "sha256": "eba2644b2a2ab95c24c339cef9235c27392e464bd9cbdfe7dd8d33752058d669"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/model.json", "sha256": "c638d348c491a9081d26626d1d8fd818d7630a37d43cdf10c9d0cdf7b5dff20a"}, {"path": "art/conversion/body-human-female-older/v1/registration-decisions.json", "sha256": "92f2e0343373f1f0f5f60aa533416047ef88e2f31e3fd5c877f90d02c7bd39e5"}, {"path": "art/conversion/body-human-female-older/v1/registration-comparison.png", "sha256": "ae56c2d39bbf36476532f3dda161d94e0a2a2ee65ec060f39b7cea852f6859de"}, {"path": "art/conversion/body-human-female-older/v1/ownership-comparison.png", "sha256": "b9a423588d09072697b78b740aed9f1e829c304d534c67ba85e5baba064de4a0"}, {"path": "art/conversion/body-human-female-older/v1/body-south.png", "sha256": "fee2ace6f86247b88e1a04bd2017041fdb137657e9fee1b0df6be2227080438e"}, {"path": "art/conversion/body-human-female-older/v1/head-south.png", "sha256": "dab51b03bbead1d1bf13f368017c0dc0304cdde8b7aac22d33e582e0da837572"}, {"path": "art/conversion/body-human-female-older/v1/body-mask-south.png", "sha256": "a0e16d3a13c0031d5bd59459ce1578238698fa6294cd2d8b3baa4332eca44ec2"}, {"path": "art/conversion/body-human-female-older/v1/head-mask-south.png", "sha256": "78dddb0d7b17e1d2386869b590279bb6465f6ba54572c261646054eb9ee861d4"}, {"path": "art/conversion/body-human-female-older/v1/body-east.png", "sha256": "e6a027848a4a15617d82f002db4ef34240322563af76d7224965881f551967da"}, {"path": "art/conversion/body-human-female-older/v1/head-east.png", "sha256": "04c68556f739af461fe4b15559f8988b5a276343ab52e5daf137c93a1b2ab937"}, {"path": "art/conversion/body-human-female-older/v1/body-mask-east.png", "sha256": "c4f9d76778fe74acf229fa541d84bd4ccaaee8075e14f0065992a87158e34fa9"}, {"path": "art/conversion/body-human-female-older/v1/head-mask-east.png", "sha256": "d3cc2f85be31fa7b4f9283aa6e107d24100efe37389d9d5ac564acf409ad9ba3"}, {"path": "art/conversion/body-human-female-older/v1/body-north.png", "sha256": "7ee31b00c29ed5d962b6c6b09f574f5b81478fe82c8396faedd056d9dbdb9069"}, {"path": "art/conversion/body-human-female-older/v1/head-north.png", "sha256": "3b99f22e1bd75583f362b3b6a813f88fe5d878e934425f90112f1291aff5e505"}, {"path": "art/conversion/body-human-female-older/v1/body-mask-north.png", "sha256": "135c2237a1c2a2c0fe9809d18d2f55957ea99a93d89574216cf6cd926b780452"}, {"path": "art/conversion/body-human-female-older/v1/head-mask-north.png", "sha256": "996c080cd9d185f8c22c87669c7257e03617d883ac6fbc93e8c20a05791985e9"}]
  Method/prompt/corrections: {"phase": "Registered centered body/head with explicit ownership masks"}

- 2026-10-20T01:42:38.277298+00:00 / visual_review_all_views / PASS: Reviewed registered front, side, rear, mirrored west and the same model at intended authoring size.
  Review: Complete silhouette, neutral grayscale and consistent centered anchor. Mild older side lean is retained; clothing remains separate. Generation-ready only, with no native game launch or integration acceptance.
  Inputs: [{"path": "art/conversion/body-human-female-older/v1/model.json", "sha256": "c638d348c491a9081d26626d1d8fd818d7630a37d43cdf10c9d0cdf7b5dff20a"}, {"path": "art/conversion/body-human-female-older/v1/registration-comparison.png", "sha256": "ae56c2d39bbf36476532f3dda161d94e0a2a2ee65ec060f39b7cea852f6859de"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/game-scale-review.png", "sha256": "778986ae4bb422133a83ecbf378d6c12fbfef26778ed3c858f8c11ac667753a0"}, {"path": "art/conversion/body-human-female-older/v1/selected-south.png", "sha256": "2cad4799e9dcb6932dee991f4fcb0f7deeec0831f66bc859f826e5a948a20766"}, {"path": "art/conversion/body-human-female-older/v1/selected-east.png", "sha256": "cb6af0e66c93b5532b57cc6016a9a18ff549d22146f089550e1db8c5ff107ca1"}, {"path": "art/conversion/body-human-female-older/v1/selected-north.png", "sha256": "0d92231c33190ecc42f0dac53919e3ad889a661c152b3655a79b253c4046c836"}]
  Method/prompt/corrections: {"phase": "Older female authoring ready"}

- 2026-10-20T01:42:38.277991+00:00 / record_native_selection_policy_without_changing_demographics / PASS: Recorded the requested older female as an authored variant, without changing any captured villager or inventing a native age selector.
  Review: No canonical older-female resident is inferred. Base has no mutations; ordinary clothing fittings and separate mutation representation remain their own requirements.
  Inputs: [{"path": "art/conversion/body-human-female-older/v1/source-packet.json", "sha256": "2af7e8861f73a39c111df6d66b8fda1cadb3d18d87dec450cdd564fcea51ede6"}]
  Outputs: [{"path": "art/conversion/body-human-female-older/v1/model.json", "sha256": "c638d348c491a9081d26626d1d8fd818d7630a37d43cdf10c9d0cdf7b5dff20a"}]
  Method/prompt/corrections: {"phase": "Age-template selection policy"}

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
