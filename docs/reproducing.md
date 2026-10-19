# Reproduce the diagnostic experiments

These instructions reproduce the bounded engine probes, not a playable visual
overhaul. Windows, Direct3D11 and the exact inspected builds are required. The
source uses exact IL anchors and rejects a changed Qud assembly. Inspect new game
versions before changing those guards.

## Inputs

- Your installed Qud and RimWorld copies matching the hashes in
  [integration progress](integration-progress.md).
- The matching installed Vehicle Framework Workshop item `3014915404`, specifically
  `1.6/AssetBundles/shaders_win`, for its UnityFS container/type tree.
- Python 3.13, a private virtual environment, UnityPy 1.25.4 and Pillow.
- PowerShell 7. Qud compiles the actual C# source mod at startup; a Unity Editor
  installation is not required.

Do not run while another Qud session is active. Use a fresh PowerShell process so
the launcher's process-local environment variables do not affect later work.
The launcher intentionally requires a task-owned root beginning with
`E:\Temp\qud-transplant-probe-`. No global environment change is necessary.

## Prepare and run

From the repository root, set the paths to your actual installations. `python`
in the first command below must resolve to Python 3.13; use its explicit executable
path if your default Python differs.

```powershell
$Root = 'E:\Temp\qud-transplant-probe-reproduction'
$Qud = 'D:\Steam\steamapps\common\Caves of Qud'
$Donor = 'D:\Steam\steamapps\common\RimWorld\RimWorldWin64_Data'
$Template = 'D:\Steam\steamapps\workshop\content\294100\3014915404\1.6\AssetBundles\shaders_win'
New-Item -ItemType Directory -Path $Root -Force | Out-Null
$env:TEMP = Join-Path $Root 'tmp'
$env:TMP = $env:TEMP
$env:PIP_CACHE_DIR = Join-Path $Root 'pip-cache'
New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
python -m venv (Join-Path $Root 'venv')
if ($LASTEXITCODE -ne 0) { throw 'Virtual environment creation failed' }
$Python = Join-Path $Root 'venv\Scripts\python.exe'
& $Python -m pip install 'UnityPy==1.25.4' Pillow
if ($LASTEXITCODE -ne 0) { throw 'Dependency installation failed' }
$env:PATH = (Join-Path $Root 'venv\Scripts') + ';' + $env:PATH
& $Python probe/package_donor.py --donor-data $Donor --template $Template --output (Join-Path $Root 'donor')
if ($LASTEXITCODE -ne 0) { throw 'Donor packaging failed' }
& ./probe/run_probe.ps1 -Root $Root -Game $Qud -Mode shader
& ./probe/run_probe.ps1 -Root $Root -Game $Qud -Mode capture
& $Python probe/verify_probe.py --root $Root
if ($LASTEXITCODE -ne 0) { throw 'Probe evidence verification failed' }
```

The packager verifies exact input hashes, replaces six shader records in the
container, saves it, reopens it and checks raw/program hashes. Container packaging
does not recompile the donor shaders. Generated textures and bundles stay local.
Do not use Python optimization (`-O`): experiment checks use assertions.

The launcher creates source/options only in its isolated profile, disables Steam
integration with `STEAM:NO`, starts hidden batch graphics, and waits for actual
process exit. Its explicit root also gates source-mod activation. It does not
install the probe in your normal mod directory.

## Interpretation and recovery

`verify_probe.py` checks actual readbacks, material changes, selected blueprint
identities, invisible/unseen exclusion, actor movement, late mutation detection,
three accepted/consumed frame hashes and preservation. Inspect errors and retained
logs if the process or verification fails; do not infer success from launch alone.

The fixture runs during MainMenu startup with a temporary real Qud game/zone;
it restores the original game context. It is not a saved or generated Joppa run.
`runtime*.json`, launch records and `preservation.json` are local diagnostics and
may contain machine paths, hardware details or profile filenames. Do not publish
them without review.

The normal profile's save/options hashes are checked. Batch graphics may modify
Unity registry display preferences, which the guard restores to its captured
baseline. Native logs and Unity analytics can still change outside the isolated
paths, including cache pruning. See [the recorded effects](integration-progress.md).
Keep the original `profile-before.json` until preservation has been checked.
After an interrupted launcher, inspect and observe the original game process
before performing the guard's `after` operation; do not start a competing run or
restore preferences while the process is still writing them.

Keep needed results, then remove expendable scratch using a reviewed cleanup
workflow. In the original agent environment this was the installed
`transactional-cleanup` helper, with exact-root inventory, signed-manifest
inspection, ticket issuance and apply. Its installation is environment-specific;
it is not bundled or required to render the probe. Never sweep game/profile
directories as experiment cleanup.
