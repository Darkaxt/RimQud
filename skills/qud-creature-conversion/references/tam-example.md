# Tam: worked example and current limits

The input chain is Tam → Dromad → native race description, original shader-mask
sprite, humanoid body tree and actual RimWorld dromedary presentation/anatomy
references. [Structured input](../../../evidence/tam-conversion-input.json).

The native description establishes a long neck, camel-like identity, dulla,
ears and a back hump. The two-legged visual interpretation is supported by the
humanoid template, two hand-bearing arms and plural Feet group. Fine proportions
and unseen surfaces remain authored. There are no separate native Neck, Dulla
or Hump entries in the captured body tree; the named features still need art.

The [wiki limb list](https://wiki.cavesofqud.com/wiki/Tam,_dromad_merchant) matches
the baseline humanoid layout and explicitly excludes mutation-granted limbs.
The viewed infobox identifies game version 2.0.206.57 and reports Fatty Hump;
our installed source is 2.0.211.56, uses blueprint Tam, and its resolved static
declarations do not include that mutation. The original runtime exporter did
not enumerate active mutations: runtime absence is **not** established. Its
attached tree also contains an abstract Thrown Weapon slot omitted by that wiki
list. Preserve these distinctions rather than inventing another physical limb.

## What changed during the example

1. An initial three-view vector construction exposed a common error: the side
   head turned while the garment and later the legs retained a frontal stance.
2. Clothing was removed from the authoring phase. Bare adult body/head sources
   and source coverage masks were prepared first; the supplied clothed user
   refinement image was not used as generation input.
3. A front-guided ImageGen proposal produced more coherent side/back silhouettes.
   Review caught a shortened muzzle in an earlier test and a round/tail-like
   interpretation of the hump. The composed refinement made the upper-back
   mound continuous with the shoulders.
4. The user selected the [refined unclothed base](../../../art/dromad/nude/preview.html).
   Keep its [exact prompts and provenance](../../../art/dromad/nude/refinement.json).
   ImageGen output is retained unchanged. Browser labels identify the views;
   generated text and a misleading RGB preview of transparent background pixels
   are not relied on.
5. The separately generated Cloth Robe retained closed oval sleeve strokes.
   Overlaid on the selected body, those strokes crossed the actual hands; the
   side hand was also obscured. This was an extraction/coverage defect, not a
   reason to regenerate the creature. Explicit alpha cutouts open the lower
   cuffs while keeping the original body and garment source. The mask paths and
   uniform registration are recorded in
   [robe registration](../../../art/dromad/robe-registration.json); inspect the
   [assembled layers](../../../art/dromad/layered/preview.html), not just the
   isolated robe, before accepting the clothing.

## Registered selected base

The selected views use one physical pixel scale and per-view feet contacts.
Explicit masks separate body from head/neck; they were re-established on the
refined image rather than inherited from the constructed source. Body owns arms,
feet and hump; head owns the long neck and dulla. The observed snapshot wears
Cloth Robe and holds Shillelagh; this is not a universal dromad costume. A native
right-hand anchor is recorded for that actual held item.

The isolated robe uses a different image frame, so uniform scale and explicit
collar/hump registration map it onto the body. Source pixels are not stretched
to independent bounding boxes. Only alpha changes at the recorded cuff cutouts;
the selected body and original robe generation remain unchanged.

The [refined native evidence](../../../evidence/dromad-refined-result.json) applies
to this assembly; the [layer inspector](../../../art/dromad/layered/preview.html)
separates enlarged art review from actual unchanged native frames.

An [earlier clothed vector diagnostic](../../../evidence/dromad-result.json)
passed native facing, contact, equip/unequip, separate tint, visibility/fallback,
hurt, look and save/load. It predates the selected refined body and must not be
presented as verification of that newer image or garment-extraction workflow.
Full village Stage 3 remains ACTIVE. The ray-cat sample is unchanged.

The user subsequently clarified that mutation representation is not the current
priority. Preserve known mutation metadata and uncertainty; do not expand this
ordinary-race conversion into mutation-specific art or garment adaptation now.

## Discovery note

The installed image-generation and skill-authoring guidance already cover their
general tasks. Local exact-name discovery found no Qud conversion skill. Public
exact searches for `qud-creature-conversion` and `sprite-turnaround` found no
matching candidate on 2026-10-20. A broad scout suggested
`wheresryan22/anatomy/anatomy`, but its inspected scope is interactive isometric
SVG explainers, not Qud anatomy or creature-layer conversion. It was not adopted
or installed. This repository source captures the specific tested procedure;
it does not claim a new globally discoverable skill is active.
