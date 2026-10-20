# Joppa conversion ledger

Reset date: 2026-10-20. **Every entry is UNFINISHED at the reset.**

This ledger supersedes earlier art-completion claims. Native tests establish integration behavior only. Existing sprites, traced contours, generated sheets and previous selections are historical inputs; none receive completion credit.

154 entries: 16 resident assemblies (10 blueprints), 10 body/age templates, 20 actual equipment inventory/aggregate records, 33 body/equipment fittings, 2 unmapped child-template garments, 57 scenery types, 8 surface/grass targets and 8 exclusion reviews.

The 75 baseline blueprint types are all accounted for: 67 selected visible types plus eight exclusions to recheck. Connectivity masks are enumerated under their owning wall/fence entry, not hidden behind an atlas count. Counts overlap between subjects and fittings; they are not a completion percentage.

Equipment inventory rows identify the 20 unique items and aggregate their fitting records; they do not require generating a second generic outfit. The 33 fitting entries own actual body-specific construction/refinement/extraction. An item aggregate or NPC assembly cannot complete while its linked fittings/body remain unfinished.

Active entry: **none**. Overall art work: **unfinished**. Implementation Stage 3: **ACTIVE**.

## One-entry execution rule

1. Select exactly one entry and record it as IN PROGRESS with its current step. Resolve its source identity, description, native metadata and actual reference decision first.
2. Append the conversion process as it happens: timestamp, step, action, exact input hashes, prompt text/file and tool/settings when used, output hashes, corrections/rejections, and review result. Do not manufacture retrospective PASS events from file existence.
3. For adults: front construction -> front-guided side/back -> anatomical fixes -> composed refinement -> registered body/head/color masks. Child references remain fully clothed. For each equipped piece: fit on the unchanged selected body -> in-context refinement -> isolated extraction -> recomposition/occlusion review in every view.
4. Furniture/vegetation/machinery/tiles follow identity + description + original shape/palette + reference decision -> deliberate reconstruction -> relevant views/states -> refinement -> masks/registration -> visual and native review. A trace/upscale is an input, not the completed conversion.
5. Review neutral/Qud palettes, actual game scale, anatomical count, whole-body orientation, clothing perspective, cuffs, attachment and depth order. Record failures and remedies on that entry. A native batch result never completes unreviewed art entries.
6. Mark COMPLETE only after every required step has a passing logged result and matching evidence. Then move to the next entry. A necessary pause leaves this entry UNFINISHED with the exact blocker/resolution; it does not quietly disappear.

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

### Race/body templates (10)

| Entry | Subject | Status | Linked entries | Known work remaining |
| --- | --- | --- | --- | --- |
| BODY-DROMAD | dromad | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. |
| BODY-DROMAD-CHILD | dromad child (fully clothed template) | UNFINISHED | - | Constructed template only. No native age selector established; do not assign an age to residents by guesswork. |
| BODY-GLOWFISH | glowfish | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. Known defect: magenta/cyan are baked into fixed-color pixels; palette-off is not neutral. Establish neutral base and separate Qud color masks. Existing east-guided turnaround is not evidence of the complete agreed front-first process. |
| BODY-HUMAN-CHILD | human child (fully clothed template) | UNFINISHED | - | Constructed template only. No native age selector established; do not assign an age to residents by guesswork. |
| BODY-HUMAN-FEMALE | human-female | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. Shared-human-base consistency must be reviewed across named human variants; independent turnarounds allowed unsupported proportion drift. The standard human shown in the gallery has tapered leg stubs without recognizable feet; construct and review feet and contact in every orientation. |
| BODY-HUMAN-MALE | human-male | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. Shared-human-base consistency must be reviewed across named human variants; independent turnarounds allowed unsupported proportion drift. The standard human shown in the gallery has tapered leg stubs without recognizable feet; construct and review feet and contact in every orientation. |
| BODY-IRUDAD | irudad | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. Native second arm pair/hands-face is supported, but the upright mannequin omits the described hunched back and elderly proportions. Reconstruct the elder silhouette from sprite plus full description. Native description explicitly specifies a short barb-crowned tail and the blueprint includes Stinger. The displayed smooth curled tail does not clearly preserve the barbed tip; review against description in all views. The initial constructed torso shared human geometry, but independently generated/registered turnarounds drifted in torso, leg and head proportions. Derive from the selected shared human base and record each source-supported age/anatomy change. |
| BODY-NIMA | nima | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. |
| BODY-RAY-CAT | ray-cat | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. |
| BODY-YRAME | yrame | UNFINISHED | - | Existing art/registration and native checks are historical only; restart the logged workflow. ImageGen three-foot proposals were rejected; four-foot geometry was patched afterward without a completed composed refinement. |

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
| TILE-SAND | path surface | UNFINISHED | - | Procedural draft material only; identity, texture scale and transitions must be reviewed through the complete workflow. |
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
| SCN-DIRTPATH | DirtPath | UNFINISHED | - | Only traced/enlarged source contours or preliminary surfaces exist. Full source-to-design/refinement/visual conversion remains unfinished. |
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

### BODY-DROMAD-CHILD: dromad child (fully clothed template)

Required steps: resolve_age_evidence_and_render_reference -> construct_fully_clothed_front -> generate_other_views -> correct_and_refine_composite -> register_body_head_and_actual_clothing -> visual_review_all_views -> record_native_selection_policy_without_changing_demographics.

Required views/states: fully clothed south/east/north; west mirror.

Historical artifacts: [art/village/age-templates/dromad/body-east.png](../art/village/age-templates/dromad/body-east.png), [art/village/age-templates/dromad/body-north.png](../art/village/age-templates/dromad/body-north.png), [art/village/age-templates/dromad/body-south.png](../art/village/age-templates/dromad/body-south.png), [art/village/age-templates/dromad/head-east.png](../art/village/age-templates/dromad/head-east.png), [art/village/age-templates/dromad/head-north.png](../art/village/age-templates/dromad/head-north.png), [art/village/age-templates/dromad/head-south.png](../art/village/age-templates/dromad/head-south.png), [art/village/age-templates/dromad/tunic-east.png](../art/village/age-templates/dromad/tunic-east.png), [art/village/age-templates/dromad/tunic-north.png](../art/village/age-templates/dromad/tunic-north.png), [art/village/age-templates/dromad/tunic-south.png](../art/village/age-templates/dromad/tunic-south.png).

Current step: not started. Process-log events: 0.

### BODY-GLOWFISH: glowfish

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/glowfish/body-east.png](../art/village/bodies/glowfish/body-east.png), [art/village/bodies/glowfish/body-north.png](../art/village/bodies/glowfish/body-north.png), [art/village/bodies/glowfish/body-south.png](../art/village/bodies/glowfish/body-south.png), [art/village/bodies/glowfish/model.json](../art/village/bodies/glowfish/model.json), [art/village/bodies/glowfish/turnaround-prompt.txt](../art/village/bodies/glowfish/turnaround-prompt.txt), [art/village/bodies/glowfish/turnaround.png](../art/village/bodies/glowfish/turnaround.png).

Current step: not started. Process-log events: 0.

### BODY-HUMAN-CHILD: human child (fully clothed template)

Required steps: resolve_age_evidence_and_render_reference -> construct_fully_clothed_front -> generate_other_views -> correct_and_refine_composite -> register_body_head_and_actual_clothing -> visual_review_all_views -> record_native_selection_policy_without_changing_demographics.

Required views/states: fully clothed south/east/north; west mirror.

Historical artifacts: [art/village/age-templates/human/body-east.png](../art/village/age-templates/human/body-east.png), [art/village/age-templates/human/body-north.png](../art/village/age-templates/human/body-north.png), [art/village/age-templates/human/body-south.png](../art/village/age-templates/human/body-south.png), [art/village/age-templates/human/head-east.png](../art/village/age-templates/human/head-east.png), [art/village/age-templates/human/head-north.png](../art/village/age-templates/human/head-north.png), [art/village/age-templates/human/head-south.png](../art/village/age-templates/human/head-south.png), [art/village/age-templates/human/tunic-east.png](../art/village/age-templates/human/tunic-east.png), [art/village/age-templates/human/tunic-north.png](../art/village/age-templates/human/tunic-north.png), [art/village/age-templates/human/tunic-south.png](../art/village/age-templates/human/tunic-south.png).

Current step: not started. Process-log events: 0.

### BODY-HUMAN-FEMALE: human-female

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/human-female/body-east.png](../art/village/bodies/human-female/body-east.png), [art/village/bodies/human-female/body-north.png](../art/village/bodies/human-female/body-north.png), [art/village/bodies/human-female/body-south.png](../art/village/bodies/human-female/body-south.png), [art/village/bodies/human-female/brief.json](../art/village/bodies/human-female/brief.json), [art/village/bodies/human-female/front.png](../art/village/bodies/human-female/front.png), [art/village/bodies/human-female/front.svg](../art/village/bodies/human-female/front.svg), [art/village/bodies/human-female/head-east.png](../art/village/bodies/human-female/head-east.png), [art/village/bodies/human-female/head-north.png](../art/village/bodies/human-female/head-north.png), [art/village/bodies/human-female/head-south.png](../art/village/bodies/human-female/head-south.png), [art/village/bodies/human-female/model.json](../art/village/bodies/human-female/model.json), [art/village/bodies/human-female/turnaround-prompt.txt](../art/village/bodies/human-female/turnaround-prompt.txt), [art/village/bodies/human-female/turnaround.png](../art/village/bodies/human-female/turnaround.png).

Current step: not started. Process-log events: 0.

### BODY-HUMAN-MALE: human-male

Required steps: resolve_race_description_original_sprite_runtime_anatomy -> select_actual_core_dlc_or_mod_reference -> construct_front -> imagegen_side_back_from_front_and_race_facts -> correct_anatomy_then_imagegen_refine_composed_views -> register_required_layers_and_color_masks -> visual_review_anatomy_orientation_palette_all_views -> native_body_review.

Required views/states: south/front; east/whole-body side; north/back; west mirror; neutral base and separate Qud tint/detail.

Historical artifacts: [art/village/bodies/human-male/body-east.png](../art/village/bodies/human-male/body-east.png), [art/village/bodies/human-male/body-north.png](../art/village/bodies/human-male/body-north.png), [art/village/bodies/human-male/body-south.png](../art/village/bodies/human-male/body-south.png), [art/village/bodies/human-male/brief.json](../art/village/bodies/human-male/brief.json), [art/village/bodies/human-male/front.png](../art/village/bodies/human-male/front.png), [art/village/bodies/human-male/front.svg](../art/village/bodies/human-male/front.svg), [art/village/bodies/human-male/head-east.png](../art/village/bodies/human-male/head-east.png), [art/village/bodies/human-male/head-north.png](../art/village/bodies/human-male/head-north.png), [art/village/bodies/human-male/head-south.png](../art/village/bodies/human-male/head-south.png), [art/village/bodies/human-male/model.json](../art/village/bodies/human-male/model.json), [art/village/bodies/human-male/turnaround-prompt.txt](../art/village/bodies/human-male/turnaround-prompt.txt), [art/village/bodies/human-male/turnaround.png](../art/village/bodies/human-male/turnaround.png).

Current step: not started. Process-log events: 0.

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

## Sources and exclusions

[Structured ledger](../evidence/conversion-ledger.json) contains per-entry native metadata, exact hashes, source targets and the log.

Sources: [art/village/sources.json](../art/village/sources.json), [art/village/model.json](../art/village/model.json), [art/village/age-templates.json](../art/village/age-templates.json), [evidence/village-reference-index.json](../evidence/village-reference-index.json), [evidence/joppa-creature-catalogue.json](../evidence/joppa-creature-catalogue.json), [probe/joppa-coverage.json](../probe/joppa-coverage.json).

Race description/body trees, equipped part/laterality and palette references are retained. Captured instance IDs/genders describe one source snapshot, not permanent demographics. Unknown age or mutation state is not guessed. Player anatomy and future random/mod inventory are outside the enumerated resident snapshot; they are not silently counted as converted. Any newly discovered visible target must be added explicitly.

All completion blockers remain internal, actionable unfinished art work: missing full construction/refinement, masks/fit and visual acceptance. No required art is deferred to an unnamed future stage. This request establishes the ledger; it does not resume asset generation.
