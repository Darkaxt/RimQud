# Next experiments and eventual release

The [native Joppa experiment](joppa-experiment.md) is now authorized and active.
Its full-map offscreen stage passed; actual gameplay verification remains active.
The later art/compatibility work below remains a proposal, not a scheduled release.

## Next bounded experiment: one playable patch of terrain

Use the proven loading route and resolved Qud buffer association to draw one known
terrain/wall/plant cluster during actual gameplay. Keep the original presentation
for unmapped or invalidated cells. Reuse inspected mesh/transition/link algorithms
with explicit scene inputs; avoid bringing in RimWorld map classes or simulation.

Acceptance should cover entering/leaving the zone, walking, visibility changes,
mouse targeting, menus, save/load, and disabling the mod. Verify actual visual
output and frame timing before expanding coverage. This would answer the principal
remaining question: whether the known material and capture pieces can participate
in a stable playable scene without obscuring Qud's information.

## Art after the playable slice

Convert a small set of original sprites individually, preserving recognizable
silhouettes, palette roles and strong contrast. Establish useful wall front/corner
geometry and irregular terrain transitions. Review at normal gameplay zoom.
The existing generated atlases are concept evidence, not the finished art brief.

## Compatibility after the mapping contract works

Third-party content needs either explicit mappings or a trustworthy appearance
contract. Unmapped content must remain legible using the original presentation.
Demonstrate one real third-party example before expanding adapters. Do not infer
compatibility merely because a mod uses Qud's normal blueprint system.

## Conditions for a working-mod release

A release would require a verified playable slice, clear supported-build/API
boundaries, repeatable installation/removal, provenance for distributable assets,
and actual gameplay/lifecycle verification. Donor resources must stay locally
resolved unless separate distribution permission exists. Release publication
requires the user's authority for that delivery, and no release is created here.
