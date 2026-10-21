param(
    [string]$Root = 'E:\Temp\qud-transplant-probe-20261019',
    [ValidateSet('shader','capture','joppa','gameplay','review','pawns')][string]$Mode = 'shader',
    [ValidateRange(1,4)][int]$IntegrationStage = 1,
    [switch]$CatalogueOnly,
    [ValidateSet('donor','ray-cat','dromad','dromad-refined','village','current')][string]$ArtSet = 'donor',
    [string]$Game = 'D:\Steam\steamapps\common\Caves of Qud'
)
$ErrorActionPreference='Stop'
if($ArtSet -eq 'current' -and ($Mode -ne 'pawns' -or $IntegrationStage -ne 4 -or -not (Test-Path -LiteralPath (Join-Path $Root 'selected/runtime/contract.json')))) {
    throw 'Current art requires the exact prepared runtime contract and pawns stage4.'
}
if(($IntegrationStage -eq 2 -or $IntegrationStage -eq 4) -and $Mode -ne 'pawns' -or
   $IntegrationStage -eq 3 -and $Mode -notin @('pawns','joppa')) {
    throw 'Stages 2/4 require pawns mode; stage 3 requires pawns or joppa mode.'
}
if($ArtSet -eq 'ray-cat' -and ($Mode -ne 'pawns' -or $IntegrationStage -ne 4 -or -not (Test-Path -LiteralPath (Join-Path $Root 'faithful-cat.json')))) {
    throw 'Ray-cat art requires its packaged contract and pawns stage 4.'
}
$existing = Get-CimInstance Win32_Process -Filter "Name = 'CoQ.exe'"
if($ArtSet -in @('dromad','dromad-refined') -and ($Mode -ne 'pawns' -or $IntegrationStage -ne 4 -or -not (Test-Path -LiteralPath (Join-Path $Root "$ArtSet.json")))) {
    throw 'Dromad sample requires its packaged contract and pawns stage 4.'
}
if ($existing) { throw 'A Qud process already exists; preserve it and do not launch a competing probe.' }
if($ArtSet -eq 'village' -and ($Mode -ne 'pawns' -or $IntegrationStage -ne 4 -or -not (Test-Path -LiteralPath (Join-Path $Root 'village.json')))) {
    throw 'Village art requires its packaged source contract and pawns stage 4.'
}
$assembly=Join-Path $Game 'CoQ_Data\Managed\Assembly-CSharp.dll'
if ((Get-FileHash -LiteralPath $assembly).Hash -ne 'CFD20CF1D6126BB64C9362311B9611FE0450589E21D51DB00536AF32D63150A7') {
    throw 'Qud build differs from the audited input; inspect the hooks before running.'
}
$rootFull = [IO.Path]::GetFullPath($Root)
if (-not $rootFull.StartsWith('E:\Temp\qud-transplant-probe-', [StringComparison]::OrdinalIgnoreCase)) {
    throw 'The probe requires its explicit task-owned E: scratch directory.'
}
if($Mode -eq 'joppa' -and (Get-FileHash -LiteralPath (Join-Path $Game 'CoQ_Data\StreamingAssets\Base\Joppa.rpm')).Hash -ne '581053CD370DFEE27BB855CCB5870DE7A782898B05A0377D6B79AC28BF956951') {
    throw 'Joppa map differs from the inspected input.'
}
$profile = Join-Path $Root 'profile'
$local = Join-Path $profile 'Local'
$synced = Join-Path $profile 'Synced'
$mod = Join-Path $local 'Mods\RenderingTransplantProbe'
New-Item -ItemType Directory -Path $mod,$synced -Force | Out-Null
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'RenderingProbe.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'SceneCapture.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'JoppaSimulation.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'JoppaRenderer.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'GameplayProbe.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'PawnPresentation.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'JoppaCoverage.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'NativeApparel.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'CtesiphusArt.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'DromadArt.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'VillageArt.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'CurrentArt.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'CaiFog.cs') -Destination $mod
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'joppa-coverage.json') -Destination $Root
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'manifest.json') -Destination $mod
@{
    OptionEnableMods='Yes'; OptionAllowCSMods='Yes'; OptionOutputModAssembly='No';
    OptionHarmonyDebug='No'; OptionMasterVolume='0'; OptionMusicVolume='0'; OptionSoundVolume='0'
    OptionAmbientVolume='0'; OptionMusic='No'; OptionSound='No'; OptionAmbient='No'
    OptionDisplayFullscreen='No'
    OptionDisplayScanlines='No'; OptionDisplayVignette='No'
    OptionDisableFloorTextureObjects='No'
} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $local 'PlayerOptions.json') -Encoding utf8NoBOM
$env:QUDEXPERIMENT_ROOT=$rootFull
$env:QUDEXPERIMENT_MODE=$Mode
$env:QUDEXPERIMENT_STAGE="$IntegrationStage"
$env:QUDEXPERIMENT_ART=$ArtSet
$env:QUDEXPERIMENT_CATALOGUE=if($CatalogueOnly){"1"}else{"0"}
$env:TEMP=Join-Path $Root 'tmp'
$env:TMP=$env:TEMP
New-Item -ItemType Directory -Path $env:TEMP -Force | Out-Null
$baseline=Join-Path $Root 'profile-before.json'
if (-not (Test-Path -LiteralPath $baseline)) {
    & python (Join-Path $PSScriptRoot 'profile_guard.py') before --root $Root
    if ($LASTEXITCODE -ne 0) { throw 'Profile baseline failed' }
}
$screenWidth=if($Mode -in @('review','pawns')){'1280'}else{'640'}
$screenHeight=if($Mode -in @('review','pawns')){'800'}else{'480'}
$launchArgs=@('-batchmode','-force-d3d11','-screen-width',$screenWidth,'-screen-height',$screenHeight,'-screen-fullscreen','0',
    '-savepath',$profile,'-sharedpath',$local,'-syncedpath',$synced,
    '-logFile',(Join-Path $Root "unity-$Mode.log"),'STEAM:NO','NOMETRICS','probe')
if($Mode -eq 'review'){$launchArgs=$launchArgs | Where-Object {$_ -ne '-batchmode'}}
$windowStyle=if($Mode -eq 'review'){'Normal'}else{'Hidden'}
# review is an explicitly selected interactive launch; do not run it during a hidden-only session.
$process=Start-Process -FilePath (Join-Path $Game 'CoQ.exe') -WorkingDirectory $Game -ArgumentList $launchArgs -WindowStyle $windowStyle -PassThru
@{pid=$process.Id;start=$process.StartTime.ToUniversalTime().ToString('o');mode=$Mode;integrationStage=$IntegrationStage;artSet=$ArtSet;catalogueOnly=[bool]$CatalogueOnly;arguments=$launchArgs} |
    ConvertTo-Json | Set-Content -LiteralPath (Join-Path $Root "launch-$Mode.json") -Encoding utf8NoBOM
Write-Output "Probe process $($process.Id) launched; waiting for its actual exit."
$process.WaitForExit()
$process.Refresh()
$exit=$process.ExitCode
Write-Output "Probe process exited: $exit"
& python (Join-Path $PSScriptRoot 'profile_guard.py') after --root $Root
if ($LASTEXITCODE -ne 0) { throw 'Normal profile preservation check failed' }
if ($exit -ne 0) { throw "Probe failed with exit code $exit; inspect its retained diagnostics." }
