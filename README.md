# RimQud

Research toward a **high-contrast, Qud-faithful visual overhaul** using selected
RimWorld rendering techniques and locally sourced rendering resources. Qud keeps
its own simulation and controls.

**Current result: donor rendering is connected to Qud's actual gameplay map
camera in a fully generated Joppa game.** Native movement, look targeting, modern
inventory, save/load and three continuous native turns passed isolated automated
checks. Foreground review also verified mouse walking, NPC targeting, zoom,
physical I opening inventory, the full HUD and mouse-driven save/quit. This is
an experimental integration, not a released overhaul.

**Earlier coverage was narrow:** the controlled baseline replaced 10 of 67 selected
blueprint types; 57 types, including NPCs and furniture, retain native sprites.
Repeated ground/path cells account for much of that apparent coverage.
The [staged implementation](docs/joppa-integration-spec.md) has now passed its
first layered human/animal/prop scene. Hurt reactions, wider coverage and visibly
equipped Qud apparel remain subsequent stages.

## Layered NPC/prop integration — stage 1

Actual 1280 × 800 native map-camera captures from generated Joppa. The isolated
fixture relocates an existing farmer, Ctesiphus and chair near the player. Humans
use separate donor body/head layers; the cat uses directional donor graphics.
Known native ground stays beneath them, and mapped foregrounds sort by contact
row. Qud's colors, camera effects and original fallback remain. Separate HUD
canvases are omitted from these readbacks.

![Generated Joppa pawn fixture with original sprites](docs/images/joppa-pawns-original.png)

![Same accepted pawn fixture with donor humans, cat and chair](docs/images/joppa-pawns-replacement.png)

[Stage 1 verification](evidence/pawns-stage1-result.json) covers direction, tint,
visibility, late changes, overlap and native targeting/save-load behavior.
These are temporary NPC graphics, not a faithful completed tileset. No hurt or
apparel animation is claimed by this stage.

## Foreground review

Unaltered captures of the actual 1280 × 800 game window, including its native HUD:

![Actual Joppa foreground gameplay and HUD](docs/images/joppa-foreground-hud.jpg)

Opening a native menu deliberately restores Qud's original presentation; the
donor layer returns when gameplay resumes. This conservative fallback also
applies to inventory and NPC context menus.

![Native game menu with original-render fallback](docs/images/joppa-foreground-menu.jpg)

[Foreground evidence](evidence/foreground-review.json) distinguishes direct
observations from user-confirmed physical input. Keyboard movement and the
Escape menu shortcut remain unverified: Escape stopped the remote-control tool.
Synthetic shortcuts did not activate native commands, although physical I did.
Long-session stability and FPS have not been established.

## Actual gameplay-view integration

These unaltered 640 × 480 readbacks use Qud's own map camera after a native save/load
round trip, including native field of view and camera effects. They omit separate
HUD canvases. The donor layer shares the native tile coordinates; existing input
objects and unmapped native sprites remain in place. Qud's painted bare ground
is mapped directly without adding floor objects to the generated world.

![Actual Joppa gameplay map camera, original](docs/images/joppa-gameplay-original.png)

![Same actual gameplay frame with donor presentation](docs/images/joppa-gameplay-replacement.png)

The donor layer clears for look/inventory views, disabling and unmatched buffers.
Native renderer suppression is applied before the map camera draws, after Qud's
own sprite updates. Save/load rebuilds from the newly accepted native frame.
[Verified gameplay evidence](evidence/gameplay-result.json) records the bounded
automated checks; the separate foreground evidence above covers basic controls.

## Full native-map Joppa experiment

These are actual 1920 × 900 GPU captures from the same accepted Qud frame.
The first uses Qud's resolved sprites. The second maps 1,810 cells to donor
materials and retains original sprites for 190 unmapped cells, including NPCs
and furniture. Ground, paths, grass, crops, reeds, trees, water, doors and 161
brinestalk wall cells use donor materials; walls use linked atlas selection.
The current capture includes 274 grass clumps at native ground-paint locations
and 51 connected shallow-water cells.

![Actual native-map Joppa original presentation](docs/images/joppa-original.png)

![Actual native-map Joppa with donor materials and original fallback](docs/images/joppa-replacement.png)

[Local draggable comparison](comparison.html) — download/serve this repository
to use it; GitHub displays HTML source. [Experiment and acceptance](docs/joppa-experiment.md)
and [verified result summary](evidence/joppa-result.json).

Qud's map builder created the 996 authored placements from `Joppa.rpm` over an
explicit dirt-floor fill. This is not normal seeded-world generation; shrine
initialization logged missing world-history data. The renderer preserves native
fallback sprites, including their visible dark tile backgrounds.

Eleven accepted/consumed frames tested liquid depth changes, actor relocation, visibility changes, late
mutation, replacement disabling, view gating, another zone and return. Offscreen
captures include scene creation and PNG readback; their timings are not gameplay
frame times. The later gameplay checks above use a separately generated world.

The path interior and its transition use the same donor fade-rough material,
precedence and texture sampling. The initial hard-interior/rough-edge mismatch
caused the visible bright rim and was corrected. Open water uses Qud's wading
and swimming thresholds with distinct donor ramp textures; this is a connected
liquid adapter, not the complete RimWorld animated water pipeline.

## Earlier isolated shader experiment

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

The later full-map experiment above connects these two pieces in a controlled
simulation. The later native-game experiment connects it to the map camera;
broader mod compatibility remains unverified. These fixtures remain for provenance.

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
