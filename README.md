# RimQud

Research toward a **high-contrast, Qud-faithful visual overhaul** using selected
RimWorld rendering techniques and locally sourced rendering resources. Qud keeps
its own simulation and controls.

**Current result: two prerequisite experiments passed separately.** One loaded
six unchanged RimWorld shaders into Qud's Unity runtime and rendered small test
planes. The other captured selected Qud appearances and paired submitted display
buffers with Unity consumption. **The captured Qud scene has not been drawn with
the donor shaders. There is no shader-rendered Joppa screenshot or playable
overhaul yet.**

## Actual shader experiment: the complete visual output

These are all eleven original, unaltered **128 × 128 GPU readbacks** from the
executed shader probe. An offscreen camera inside Qud rendered a simple plane
using a locally extracted RimWorld shader and test texture. These images were
not AI-generated. They show material compatibility and input effects; they are
not screenshots of a replacement scene in Qud's gameplay view.

| Shader / input change | Baseline | Changed input | Pixels changed |
| --- | --- | --- | ---: |
| Terrain hard: material tint | ![Terrain hard baseline, actual engine readback](docs/images/terrain-hard-base.png) | ![Terrain hard with green tint, actual engine readback](docs/images/terrain-hard-tint.png) | 7,744 |
| Terrain fade: vertex alpha | ![Terrain fade baseline, actual engine readback](docs/images/terrain-fade-base.png) | ![Terrain fade edge, actual engine readback](docs/images/terrain-fade-edge.png) | 7,740 |
| Terrain fade rough: vertex alpha with alpha-add texture | ![Terrain fade rough baseline, actual engine readback](docs/images/terrain-rough-base.png) | ![Terrain fade rough edge, actual engine readback](docs/images/terrain-engine-test.png) | 7,534 |
| Plant cutout: sway input | ![Plant cutout baseline, actual engine readback](docs/images/plant-engine-test.png) | ![Plant cutout with changed sway, actual engine readback](docs/images/plant-wind-engine-test.png) | 3,463 |
| Plant transparent: sway input | ![Plant transparent baseline, actual engine readback](docs/images/plant-transparent-base.png) | ![Plant transparent with changed sway, actual engine readback](docs/images/plant-transparent-wind.png) | 3,746 |

The sixth shader, `Custom/Cutout`, was tested with one wall-atlas sample:

![Cutout material on a single test plane, actual engine readback](docs/images/cutout-engine-test.png)

The wall sample establishes that the cutout material draws. It does not establish
connected wall geometry, correct wall-neighbor selection or a finished wall style.
Likewise, the plant pairs compare two sway values; they do not demonstrate a
complete animated vegetation system.

All six shaders reported supported with one pass and produced pixels without
magenta error pixels in Qud's Unity 6000.0.77f1 built-in pipeline on Direct3D11.
The retained [render measurements](evidence/shader-renders.json) and
[result summary](evidence/integration-result.json) record these tests.

## Separate scene-capture experiment

A second launch used real Qud ground, wall, vegetation, actor and liquid objects
in a controlled temporary zone. It tested hidden-object exclusion, actor movement
and a late buffer mutation. Three frame generations matched between the producer
and Unity consumer under the existing buffer lock.

That fixture ran during MainMenu startup with Qud's original presentation.
Its output was diagnostic data, not a donor-shader image of the fixture. It does
not yet prove gameplay view/input integration or a generic layered scene.

The next integration test is to connect these two pieces and draw a small known
Qud scene with the donor materials during gameplay. Full-scene rendering,
terrain/wall connectivity and mod compatibility remain to be demonstrated.

## Earlier HTML concepts

The previous AI-generated art sheets and before/after browser mockups are
preserved in [the archived HTML visual study](docs/html-visual-study.md).
They illustrate possible art directions and are unrelated to the shader test's
rendered output shown above.

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
