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

## Still required before this selected base is integrated

Register the selected views and split the refined body from head/neck. The
constructed source masks do not automatically apply to the new output. Then fit
and isolate one actual equipped garment at a time. The observed snapshot wears
Cloth Robe and holds Shillelagh; this is not a universal dromad costume.

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
