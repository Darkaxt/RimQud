# Diagnostic source

Start with [reproduction instructions](../docs/reproducing.md).

| File | Responsibility |
| --- | --- |
| `package_donor.py` | Hash-pinned local extraction/container packaging; re-read output verification |
| `RenderingProbe.cs` | Qud bootstrap, offscreen material rendering, PNG readbacks and completion |
| `SceneCapture.cs` | Narrow real-render hooks, fixture and frame correspondence |
| `manifest.json` | Isolated source-mod metadata |
| `run_probe.ps1` | Build guard, isolated profile, hidden launch, actual process-exit observation |
| `profile_guard.py` | Profile hashes and registry baseline restoration |
| `verify_probe.py` | Full retained private-run evidence verification |

The public repository contains selected sanitized evidence and documentation
images. `verify_probe.py` expects a complete locally reproduced run directory,
including its private diagnostics and all eleven readbacks; it does not operate
on the reduced public `evidence/` directory.
