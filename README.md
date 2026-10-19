# RimQud

Research toward a **high-contrast, Qud-faithful visual overhaul** using selected
RimWorld rendering techniques and locally sourced rendering resources. Qud keeps
its own simulation and controls.

**Current result:** six unchanged RimWorld shaders rendered inside Qud's engine,
and a controlled scene-capture experiment paired three submitted frames with
Unity consumption. This repository contains diagnostic source and evidence;
there is no playable overhaul release yet.

## The visual studies

These are the retained images from the initial HTML study. The slider compares
Qud's original presentation on the left with an illustrative replacement on the
right. These screenshots are **browser simulations**, not in-game transplants.
The generated sprites are early style studies: walls, roads and several NPCs
still need work, and the two directions are less distinct than intended.

### RimWorld-inspired study

![Early Joppa browser comparison with Qud on the left and the RimWorld-inspired concept on the right](docs/images/rimworld-comparison.png)

Original generated sprite sheet used by this study:

![AI-generated RimWorld-inspired Qud concept sprite sheet](docs/images/rimworld-concepts.png)

### Stoneshard-inspired study

![Early Joppa browser comparison with Qud on the left and the Stoneshard-inspired concept on the right](docs/images/stoneshard-comparison.png)

Original generated sprite sheet used by this study:

![AI-generated Stoneshard-inspired Qud concept sprite sheet](docs/images/stoneshard-concepts.png)

The intended art direction has since become clearer: preserve Qud's colors,
silhouettes and identity, converting individual assets deliberately. These generic
concept sheets are visual exploration, not an approved final tileset. Connected
terrain, readable wall faces and natural roads matter before broader coverage.

## What actually ran in Qud

The following 128 × 128 images are actual GPU readbacks from the isolated Qud
engine probe, using locally extracted RimWorld shaders and test textures.
They establish material loading and rendering, not full-scene quality.

| Rough terrain alpha transition | Plant, baseline | Same plant, changed wind input |
| --- | --- | --- |
| ![Actual Qud-engine terrain shader test](docs/images/terrain-engine-test.png) | ![Actual Qud-engine plant shader test](docs/images/plant-engine-test.png) | ![Actual Qud-engine plant wind shader test](docs/images/plant-wind-engine-test.png) |

- Six donor shaders loaded, reported supported and produced pixels in Qud's
  Unity 6000.0.77f1 built-in pipeline using Direct3D11.
- Terrain tint/fading and plant wind inputs changed the output; eleven readbacks
  contained no magenta error pixels.
- A real Qud object fixture exercised ground, wall, vegetation, actor and liquid
  appearances, hidden-object exclusion, actor movement and a late buffer mutation.
- Three frame generations matched between producer and Unity consumer under the
  existing buffer lock. The fixture ran during MainMenu startup, not gameplay.

This supports a selective rendering transplant. It does **not** establish that
the entire RimWorld renderer can be dropped into Qud: their high-level rendering
classes depend on different maps, definitions, lifecycle and visibility rules.

## Findings and source

- [Four extraction/integration audits](docs/audits.md)
- [Verified integration progress and limits](docs/integration-progress.md)
- [Reproduce the isolated experiments](docs/reproducing.md)
- [Bounded next steps and release conditions](docs/roadmap.md)
- [Probe source](probe/) and [retained evidence](evidence/)
- [Image provenance](docs/images/provenance.json) and [third-party notices](THIRD_PARTY.md)

No game assemblies, extracted texture atlases or shader bundles are distributed.
Reproduction requires your own matching local installations. The source is pinned
to the inspected builds and is a diagnostic, not a normal-profile mod installer.

RimQud is independent and unaffiliated with Freehold Games, Ludeon Studios or
Ink Stains Games. Original glue code and documentation are under the
[MIT license](LICENSE); that license does not cover third-party game content
visible in documentation screenshots/readbacks.
