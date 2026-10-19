# Integration progress — 2026-10-19

## Verified experiments

| Experiment | Observed result | Boundary |
| --- | --- | --- |
| Donor packaging | Six shader records and compressed program hashes unchanged after serializing and re-reading a genuine UnityFS bundle | Local extraction only; no bundle distributed |
| Actual recipient rendering | Six supported shaders, one pass each, eleven 128 × 128 GPU readbacks without magenta errors | Qud built-in pipeline, Direct3D11, tested machine |
| Material inputs | Tint, terrain edge fading and both plant wind variants changed pixels | Not seasonal/lighting/API parity |
| Real scene fixture | Ground, brinestalk wall, watervine, farmer and pond appearances captured | Real Qud objects in a temporary zone, not full Joppa |
| Frame correspondence | Three generations matched submitted/consumed hashes under the existing lock, across distinct producer and Unity threads | MainMenu boot fixture; no gameplay input/view validation |
| Invalidation | Hidden identities omitted, movement reflected, late mutation flagged for original presentation | No arbitrary mod/effect/layer guarantee |

The public [result summary](../evidence/integration-result.json) records measured
pixel differences. [Package metadata](../evidence/package.json) binds the inspected
shader resources to their hashes. Source in `probe/` is identical to the locally
verified experiment source at commit `4f7086a` of the original private study
checkout. That checkout's full history and extracted assets were not imported.

## Inspected builds

| Input | Version | SHA-256 |
| --- | --- | --- |
| Qud `Assembly-CSharp.dll` | 2.0.211.56; Unity 6000.0.77f1 | `cfd20cf1d6126bb64c9362311b9611fe0450589e21d51db00536af32d63150a7` |
| RimWorld `Assembly-CSharp.dll` | 1.6.4871 rev590; Unity 2022.3.35f1 | `5cf1b5be399d5b1c9c56ca72c9d35b4ecf307feacf5859d04ac5a1aa5926356a` |
| RimWorld `resources.assets` | Same installation | `7c0c69bde01910dde60205bc1417cd56a39e27affd2de36735dcedd6facd6155` |
| Vehicle Framework `shaders_win` | Installed 1.6 bundle; Unity 2022.3.61f1 container | `338146d78f42f9dff9917914e9191fbab4e197e6c3c186a415684715eb46d8e8` |

## What is not implemented

There is no replacement renderer submitting a complete Qud scene, playable
overhaul, production material cache, faithful replacement tileset, complete wall
or terrain connectivity, camera/input integration, or arbitrary-mod support.
The captured payload records blueprint identity rather than stable per-instance
actor IDs. Unknown effects, confusion permutations and independently resolved
layers remain unresolved integration questions.

## Preservation and shutdown evidence

The launcher used isolated save/shared/synced paths and disabled Steam integration
with Qud's observed `STEAM:NO` switch. Game assemblies and normal save/options
content hashes stayed unchanged. Nine Unity display preference changes were
restored to their baseline after each launch.

Isolation did not cover every engine diagnostic: native logging and Unity
analytics still touched the normal profile. Across both runs, 14 diagnostic/cache
files were created, 218 removed and three modified; the SDK itself pruned archived
telemetry. This was not a completely untouched normal profile.

The shader probe wrote successful GPU results before quitting during independent
blueprint startup; shutdown logged a loading-thread abort and another shutdown
exception. The later capture probe completed after initialization and exited
cleanly. Both processes exited with code zero. Shader results do not imply clean
startup/shutdown parity for a production mod.

Expendable packages, extracted resources, generated bundle, isolated profile and
compile outputs were removed using a reviewed transactional cleanup. Retained
source, metadata and explicitly requested documentation images remain. No probe
process or persistent normal-profile mod was left active.
