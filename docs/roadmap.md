# Next experiments and eventual release

The [native Joppa experiment](joppa-experiment.md) is now authorized and active.
Its full-map and automated gameplay integration passed. Foreground physical-input
review remains pending before calling the slice playable.
The later art/compatibility work below remains a proposal, not a scheduled release.

## Current gate: foreground review of the integrated Joppa slice

The native map-camera connection now draws the visible Joppa materials and keeps
unmapped content native. Native movement, look, inventory, save/load and a short
continuous game loop are verified. A prepared `review` launch uses normal controls
and silent audio. It has not been launched because foreground use requires the
user's go-ahead. Check physical pointer routing, sustained walking, camera zoom,
HUD/menu visibility and the resulting visual readability before expanding art.

The controlled zone/visibility/disable checks remain valid. No broad FPS or
long-session stability claim follows from the short native run. Those measurements
should follow successful foreground review, before broader compatibility work.

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
