# Reproduce the diagnostic experiments

These instructions reproduce the bounded engine probes, not a playable visual
overhaul. Windows, Direct3D11 and the exact inspected builds are required. The
source uses exact IL anchors and rejects a changed Qud assembly. Inspect new game
versions before changing those guards.

## Current ledger-selected integration inputs

The older village package/run below is historical evidence. It does not test
the current conversion ledger. The complete-set adapter is still being wired;
the following commands only prepare its current inputs and compare cast
composition operations with the reviewed authoring images. They do not launch
Qud or grant native acceptance.

```powershell
python -X utf8 -B tools/package_current_village.py --root E:/Temp/qud-transplant-probe-fullset-20261021
python -X utf8 -B tools/package_current_village.py --root E:/Temp/qud-transplant-probe-fullset-20261021 --prepare-cast --cast-version 2
python -X utf8 -B tools/check_current_cast_composition.py --root E:/Temp/qud-transplant-probe-fullset-20261021 --cast-version 2
```

Retain an existing package and its diagnostics; the helpers refuse to overwrite
completed evidence. Use a fresh explicitly owned `E:/Temp/qud-transplant-probe-*`
root for a new reproduction. The staged `selected/package.json` pins every ledger
selection and hashed PNG reference; `selected/cast-v2.json` records the actual
per-view composition operations. Original model/texture bytes remain unchanged.
The initial simple-stack contract and failed diagnostic remain retained beside
the corrected version. See [current integration status](../evidence/current-native-integration-20261021/preparation.json)
for the exact acceptance boundary and remaining native-adapter blocker.

## Inputs

- Your installed Qud and RimWorld copies matching the hashes in
  [integration progress](integration-progress.md).
- The matching installed Vehicle Framework Workshop item `3014915404`, specifically
  `1.6/AssetBundles/shaders_win`, for its UnityFS container/type tree.
- Python 3.12 or 3.13, a private virtual environment, UnityPy 1.25.4 and Pillow
  (the layered/reaction run used Python 3.12.14 and Pillow 13.0.0).
- PowerShell 7. Qud compiles the actual C# source mod at startup; a Unity Editor
  installation is not required.

Do not run while another Qud session is active. Use a fresh PowerShell process so
the launcher's process-local environment variables do not affect later work.
The launcher intentionally requires a task-owned root beginning with
`E:\Temp\qud-transplant-probe-`. No global environment change is necessary.

## Prepare and run

From the repository root, set the paths to your actual installations. `python`
in the first command below must resolve to a compatible Python; use its explicit executable
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

For the full authored-map experiment, after donor packaging run:

```powershell
& $Python probe/package_joppa.py --donor-data $Donor --output (Join-Path $Root 'donor')
if ($LASTEXITCODE -ne 0) { throw 'Joppa texture packaging failed' }
& ./probe/run_probe.ps1 -Root $Root -Game $Qud -Mode joppa
& $Python probe/verify_joppa.py --root $Root
if ($LASTEXITCODE -ne 0) { throw 'Joppa evidence verification failed' }
```

This mode reads the native Joppa map, creates real Qud objects over an explicit
dirt-floor fill, and renders eleven controlled scenarios through the accepted buffer.
It is not normal world generation or a normal character game. It logs missing
world-history dependencies during shrine initialization. See the
[active experiment](joppa-experiment.md) for exact acceptance and limitations.
Serve the repository on loopback and open `comparison.html` to compare the two
retained baseline GPU images; the browser does not generate the scene.

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

## Native gameplay integration

After local donor packaging, use the same isolated root with `-Mode gameplay`.
This creates a real seeded Joppa game and runs native commands, modern inventory,
save/load and three turns through the native scheduler. Verify its fresh outputs:

```powershell
python probe/verify_gameplay.py --root E:/Temp/qud-transplant-probe-joppa-20261019 --output evidence/gameplay-result.json
```

The Python verifier needs Pillow. Runtime C# compilation is handled by Qud; no
separate compiler is needed to launch it. Actual map-camera captures include
native camera effects and field of view but omit separate HUD canvases.

The following is a **visible interactive launch**. Obtain foreground authorization
when operating under a hidden-only restriction:

```powershell
./probe/run_probe.ps1 -Root E:/Temp/qud-transplant-probe-joppa-20261019 -Mode review
```

The review mode reuses the native game loop and rendering connection, disables
automatic input and menu closing, and leaves normal game controls available.
It stays silent, starts windowed at 1280 × 800, and waits at the native main menu.
Select New Game; the diagnostic supplies a native pregen and Joppa starting point.
Save and quit normally to end the session and let the launcher complete its
preservation checks. This path was executed successfully; see
[foreground evidence](../evidence/foreground-review.json). Local `donor/` inputs
are required and are not public assets. Remote-control tools may intercept Escape
and synthetic keyboard shortcuts; the on-screen menu supports mouse save/quit.

## Layered actors and native reactions

After the donor and Joppa packages above, extract the selected human, cat and
chair graphics locally. No raw donor graphics are included in this repository.

```powershell
& $Python probe/package_pawns.py --donor-data $Donor --output (Join-Path $Root 'donor')
if ($LASTEXITCODE -ne 0) { throw 'Pawn texture packaging failed' }
./probe/run_probe.ps1 -Root $Root -Game $Qud -Mode pawns -IntegrationStage 2
& $Python probe/verify_gameplay.py --root $Root --mode pawns --stage 2 --output (Join-Path $Root 'verified.json')
if ($LASTEXITCODE -ne 0) { throw 'Native reaction verification failed' }
```

Stage 1 (the default) reproduces the layered scene without the reaction fixture;
use `-IntegrationStage 1` and `--stage 1` together. Stage 2 adds native movement
facing and real environmental damage to the two isolated actors, asynchronous
GPU start/mid/end readbacks and native lifecycle verification. The visual flash
uses 16/60 seconds; no game turns are added to run it. Downed/dead motion is not
inferred from missing HP. Only explicit physical attributes produce an impact
offset, and an actual attacker/source position supplies its direction.

The fixture relocates existing objects and changes HP only in the isolated game.
It does not supply the player as attacker: that correctly caused native hostility
in a retained failed diagnostic. Unknown native summaries stop with failure
evidence. Keep each run's baseline until the original process has exited and its
preservation result has passed; archive the completed baseline before a new run.

## Reviewed coverage

Extract only the reviewed common-prop and linked-scenery set after the earlier
packages, then run both authored and generated contexts in sequence:

```powershell
& $Python probe/package_coverage.py --donor-data $Donor --output (Join-Path $Root 'donor')
if ($LASTEXITCODE -ne 0) { throw 'Coverage packaging failed' }
./probe/run_probe.ps1 -Root $Root -Game $Qud -Mode joppa -IntegrationStage 3
& $Python probe/verify_joppa.py --root $Root --stage 3 --output (Join-Path $Root 'coverage-authored-verified.json')
if ($LASTEXITCODE -ne 0) { throw 'Authored coverage failed' }
# Retain this run's outputs and baseline before starting the next run.
./probe/run_probe.ps1 -Root $Root -Game $Qud -Mode pawns -IntegrationStage 3
& $Python probe/verify_gameplay.py --root $Root --mode pawns --stage 3 --output (Join-Path $Root 'coverage-gameplay-verified.json')
if ($LASTEXITCODE -ne 0) { throw 'Generated coverage failed' }
```

The launcher copies the public `probe/joppa-coverage.json` contract into the local
root. It is the explicit mapping/decision source; unknown content stays native.
The published stage-3 evidence reconciles both runs and the observed generated
addition. It records the canonical LF contract identity separately from the raw
runtime JSON payload digest because Git normalizes text line endings.


## Faithful ray-cat sample

After the donor, scenery, pawn and worn-graphic packages, freeze the installed
semantic/visual inputs and copy the unmodified generated cat views:

```powershell
& $Python probe/package_apparel.py --donor-data $Donor --output (Join-Path $Root 'donor')
if ($LASTEXITCODE -ne 0) { throw 'Worn texture packaging failed' }
& $Python probe/package_ctesiphus.py --qud-data (Join-Path $Qud 'CoQ_Data') --donor-data $Donor --root $Root
if ($LASTEXITCODE -ne 0) { throw 'Creature reference packaging failed' }
./probe/run_probe.ps1 -Root $Root -Game $Qud -Mode pawns -IntegrationStage 4 -ArtSet ray-cat
& $Python probe/verify_gameplay.py --root $Root --mode pawns --stage 4 --art-set ray-cat --output (Join-Path $Root 'faithful-cat-verified.json')
if ($LASTEXITCODE -ne 0) { throw 'Faithful cat verification failed' }
```

`faithful-cat.json` records Ctesiphus -> Ray Cat -> native race description,
actual donor texture identities/hashes and the original Qud atlas reference.
The source alpha and pixels are unchanged. Per-view anatomical contact/body
landmarks set uniform physical scale; width compensates for Qud's rectangular
cells. The generated image bounding box is not stretched into a cell.

The sample uses native primary color. It has no independent detail mask; a
changed detail color retains the native sprite. Unsupported body/equipment and
post-observation changes also retain native graphics. The ray-cat scenario
checks four real movement directions, visibility, tint, fallback, look targeting,
hurt and save/load through the existing command-driven native session.
