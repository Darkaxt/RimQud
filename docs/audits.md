# Four audit findings

These audits inspected the installed game builds before the runtime experiments.
They investigated rendering only; importing either game's mechanics was outside
scope. Method names below are evidence pointers into locally installed assemblies,
not a distribution of decompiled game source.

## 1. Donor extraction

RimWorld's lowest-level drawing algorithms are comparatively shallow. The
high-level classes are coupled to its world state.

| Candidate | Useful behavior | Dependencies to separate |
| --- | --- | --- |
| `Verse.Printer_Plane.PrintPlane/GetUVs` | Quad winding, rotation, vertex colors, UV payload and altitude bias | Donor material/mesh conventions |
| `LayerSubMesh.FinalizeMesh` | Unity vertices, triangles, colors, UV0/UV1 and normals | Submission ownership and lifecycle |
| `MapDrawLayer` | Material grouping and `Graphics.DrawMesh` submission | Map bounds and donor lifecycle |
| `SectionLayer_Terrain.Regenerate` | Terrain quad and eight-neighbor alpha transition fan | Terrain grids, precedence, edifices, snow, sand, pollution and foundations |
| `Graphic_Linked` | Four-bit neighbor selection | Donor Things, maps, link grids and definitions |
| `MaterialAtlasPool` | Sixteen submaterials in a 4 × 4 atlas; scale 0.1875 and inset 1/32 | Atlas layout must match the material |
| `Plant.Print` | Scatter, growth, flip and wind vertex inputs | Donor definitions, randomness, atlases and wind manager |

`ContentFinder` and `ShaderDatabase` are global game loaders rather than isolated
filesystem APIs. Loading the whole donor `Assembly-CSharp.dll` would introduce
game dependencies and collide with Qud's assembly of the same simple name.

Conclusion: preserve the selected rendering algorithms with explicit Qud inputs.
A whole-assembly transplant is not supported by the audit.

## 2. Recipient integration

Qud has its own core thread. `GameManager` initializes the Unity-side UI queue
and grid, then consumes `CurrentBuffer` under `BufferCS`. Source mods compile via
`ModInfo.TryBuildAssembly`, and Harmony patches are applied by its mod loader.

`Cell.Render` resolves visibility, light, solid/radar selection and layer effects;
it also causes side effects such as `Seen()`. Calling it again solely to inspect
the scene would change behavior. `ConsoleChar.Set` contains resolved appearance
but not a generic object identity or complete independently drawable layers.

`ConsoleChar.Copy` preserves particular sound/imposter extras, not an arbitrary
capture payload. `TextConsole.ProcessBufferExtra` expects Qud's specific extra
type. A generic side-channel needs its own correct frame association.

Qud's default tile-center transform uses a screen-oriented grid, approximately
`(-640 + 16x + 8, 300 - 24y - 12, 100 - z)`. RimWorld's planes use world XZ.
Camera/coordinate conversion, menu ownership and input alignment require explicit
integration. Sharing Unity does not make these conventions interchangeable.

## 3. Shader portability

The donor shader records are compiled Direct3D11 programs, not recoverable original
ShaderLab/HLSL source. The inspected shader records have no external dependencies.

| Shader | Source object ID | Important inputs |
| --- | --- | --- |
| `Custom/Terrain hard` | 3602 | Position, main texture, tint |
| `Custom/Terrain fade` | 3604 | Position and vertex alpha/color |
| `Custom/Terrain fade rough` | 3761 | Fade inputs plus alpha-add texture |
| `Custom/Cutout` | 3633 | Position, vertex color, UV.xy, texture transform |
| `Custom/Plant cutout` | 3622 | UV.xyz, vertex wind exposure, sway and fall-color globals |
| `Custom/Plant transparent` | 3620 | Plant inputs without the same fall globals |

Terrain mapping uses world positions. Plant vertices encode phase in UV.z and
wind exposure in alpha. A supported shader alone does not prove those inputs or
seasonal globals are faithfully supplied.

At audit time the loadable-bundle route was unresolved. The later experiment
resolved it: a genuine Vehicle Framework UnityFS container/type tree accepted
the six byte-identical shader records, and the resulting bundle rendered in Qud.
The compiled shader programs were preserved, not rewritten or recompiled.

## 4. Scene capture

The selected object in `Cell.Render` is available after radar selection and before
its `Render` access. Generic render callbacks do not necessarily identify the
winner: a `FinalRender` receiver can differ from the object whose appearance wins.

Later `Zone.Paint`, effects, particles, confusion, sidebar rendering and Unity
extras can change the final buffer without retaining source provenance. An
`AfterRenderCallback` is not universally the final display boundary. Confusion can
move/recolor appearances and invalidate source-position associations.

Capture must observe the real invocation and publish at the accepted buffer-copy
boundary. Buffer identity alone is insufficient because the producer reuses it;
generations and invalidation are necessary. Unknown/changed cells require original
presentation or an explicit adapter, not guessed hidden identities.

The experiment verified two narrowly anchored IL hooks and cross-thread pairing
in a controlled fixture. It did not establish a generic layered scene contract.

## Combined assessment

Selective reuse has positive runtime evidence for shader loading and bounded
scene capture. The later [native Joppa experiment](joppa-experiment.md) adds
full-map offscreen drawing, linked walls, terrain transitions and a bounded native
gameplay/foreground workflow. Production stability, Qud-faithful replacement
assets and third-party compatibility remain unverified or unimplemented;
see the [roadmap](roadmap.md).
