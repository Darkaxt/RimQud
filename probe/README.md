# Diagnostic source

Start with [reproduction instructions](../docs/reproducing.md).

| File | Responsibility |
| --- | --- |
| `package_donor.py` | Hash-pinned local extraction/container packaging; re-read output verification |
| `RenderingProbe.cs` | Qud bootstrap, offscreen material rendering, PNG readbacks and completion |
| `SceneCapture.cs` | Narrow real-render hooks, fixture and frame correspondence |
| `JoppaSimulation.cs` | Native authored map, complete accepted-frame capture and deterministic state scenarios |
| `JoppaRenderer.cs` | Donor meshes/materials, native sprite fallback and full-map offscreen GPU output |
| `GameplayProbe.cs` | Native map-camera presentation, bounded gameplay checks and separate foreground review mode |
| `verify_gameplay.py` | Fresh native-input, view, save/load, continuous-turn and image verification |
| `package_joppa.py` | Small additional hash-pinned local texture selection |
| `verify_joppa.py` | Full-scene frame, pixel, invalidation and preservation acceptance checks |
| `manifest.json` | Isolated source-mod metadata |
| `run_probe.ps1` | Build guard, isolated profile, hidden launch, actual process-exit observation |
| `profile_guard.py` | Profile hashes and registry baseline restoration |
| `verify_probe.py` | Full retained private-run evidence verification |

The public repository contains selected sanitized evidence and documentation
images. `verify_probe.py` expects a complete locally reproduced run directory,
including its private diagnostics and all eleven readbacks; it does not operate
on the reduced public `evidence/` directory.

Hidden launches disable music, effects and ambient audio in their isolated
profile, set master/ambient volumes to zero, and pause Unity's audio listener.
The runtime asserts and records that state. No normal audio preferences are
changed. `gameplay` exercises the native session automatically. `review` launches
a visible interactive session with the same presentation and silent audio; run it
only when foreground use is authorized. Physical-input review is still pending.
