# Next experiments and eventual release

The [native Joppa experiment](joppa-experiment.md) now has full-map, automated
gameplay and bounded foreground acceptance evidence. Mouse walking, NPC targeting,
zoom, physical I opening inventory, HUD, native menus and save/quit passed.
The later art/compatibility work below remains a proposal, not a scheduled release.

## Next proposed gate: measured gameplay stability

The native map-camera connection now draws the visible Joppa materials and keeps
unmapped content native. Native movement, look, inventory, save/load and a short
continuous game loop are verified. The authorized silent foreground review also
passed its bounded workflow. Keyboard movement and the Escape menu shortcut
remain unverified; physical Escape was intercepted by the remote-control tool.
The native on-screen menu worked. Menus intentionally show Qud's original
presentation, and donor rendering returns when gameplay resumes.

The controlled zone/visibility/disable checks remain valid. No broad FPS or
long-session stability claim follows from the short native run. A bounded measured
walk, repeated menu/save-load transitions and memory/frame-cost observations are
the next proposed experiment before broader compatibility or a released mod.

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
