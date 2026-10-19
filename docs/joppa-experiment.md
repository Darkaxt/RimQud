# Native Joppa rendering experiment

Authority: the user approved Joppa as the complete sample, using existing
RimWorld textures first, and authorized execution on 2026-10-19. Pause before any
required foreground desktop control. Hidden batch graphics and offscreen
simulation were authorized initially. The user subsequently authorized the
silent isolated foreground review and physical-input/HUD checks with "go ahead".
Desktop interaction is limited to that review; automated game diagnostics stay
within the isolated process.

## Required outcome

- J1: Load the full authored 80 × 25 Joppa map through Qud's native map/object
  APIs in an isolated runtime. Record the map/build hashes and distinguish this
  controlled simulation from a fully generated world or normal character session.
- J2: Connect resolved, accepted Qud cell appearances to locally extracted donor
  materials in the same engine run. Draw the whole village, preserve coordinates,
  use linked donor wall atlas selection and existing terrain/plant shaders, and
  retain original Qud sprites for unmapped/invalidated content, including actors.
  Any background fill or approximate asset mapping must be explicit.
- J3: Produce actual original/replacement full-map GPU images and a comparison
  toggle in the local simulation output. Exercise movement, visibility, late cell
  mutation, disabling replacement, unrelated-view gating and zone re-entry using
  deterministic engine-side operations. Verify frame correspondence and pixels.
- J4: Verify gameplay presentation, targeting, menus and save/load before calling
  the sample playable. Automated checks may satisfy criteria they actually test;
  offscreen geometry checks cannot stand in for real gameplay input validation.
  If foreground control is required, preserve progress and pause before it.
- J5: Preserve installed binaries, saves/settings and existing processes; observe
  the original hidden process through completion. Use one game process at a time,
  task-owned scratch and bounded render resources. Record normal-profile diagnostic
  effects, clean expendable output, document results and commit verified work.
  Synchronize source/docs and contextual evidence to the authorized public repo;
  do not distribute donor bundles, raw textures or a mod release.
- J6 (user refinement): replace the uniform brown presentation with green marsh
  ground and basic grass, merge neighboring liquid surfaces, and distinguish
  shallow from deeper water using actual Qud liquid state and distinct donor
  texture choices. Do not invent deep regions when the native state is shallow.
  Validate the revised full-village output and explicit depth-change scenarios.
- J7 (user refinement): terrain transitions should resemble the supplied RimWorld
  reference, with merged floor materials rather than a bright rim around a hard
  staircase. Use the donor's base/transition material and precedence conventions,
  preserve the authored logical cells and inspect actual GPU output.

## Compact plan

1. **COMPLETE — Full-village offscreen integration (J1-J3, J5).** Native authored
   map → real Qud object rendering → accepted frame → donor materials plus native
   fallback → actual GPU readbacks, deterministic state checks and reviewable
   local comparison. A small patch is an implementation diagnostic, not stage
   completion. Preserve a concise result ledger here.
2. **COMPLETE — Marsh, connected liquids and merged terrain (J5-J7).**
   User reprioritized these visible defects before gameplay verification. Inspect
   native ground/liquid semantics, implement the complete scene correction and
   verify actual full-map readbacks, visibility, connectivity and depth transitions.
3. **COMPLETE — Gameplay lifecycle and targeting verification (J4, J5).**
   Depends on stage 1. Prove actual gameplay-view alignment, targeting, menus and
   save/load using supported internal automation where possible. Pause before any
   necessary foreground action. Desktop permission is not inferred from elapsed
   time or a successful batch run.

Stage 3 implementation contract: reuse the verified material/geometry path in a
transparent render target on Qud's actual map camera. Preserve native tile input
objects and original renderers for fallback; restore owned visibility changes on
new buffers, unrelated views, disabling and disposal. Capture actual map-camera
before/after frames. Exercise adjacent movement through native PlayerTurn command
handling, coordinate-bearing native look input, modern inventory open/close and
native save/load, then verify fresh presentation after each. The isolated command
test supplies an energy budget; it is distinct from a continuous RunGame session
or physical mouse/keyboard validation. No FPS claim without measured evidence.

Acceptance is per complete stage outcome, not per mesh or shader. The existing
publication experiments remain historical evidence; they do not satisfy J2/J4.

Stage 1 reconciliation: native map builder instantiated 996 authored placements,
including the named residents and shrine; all 2000 positions observed. Baseline
mapped 1761 cells with 161 linked brinestalk walls; 239 cells retained original
sprites. All nine generations matched accepted/consumed hashes inside BufferCS.
Actual image checks verified relocation, hidden-region exclusion, late mutation,
zero replacement when disabled/in another view/in another zone, and rendering
after return. Eighteen 1920 × 900 readbacks retained locally. Browser comparison
verified headlessly at 1440 × 1000 and 390 × 844, with drag, keyboard and buttons.

Stage 1 preservation: no game/save/option content changes; Unity display settings
restored. Across two launches, native logs/analytics created 26, removed 2 and
modified 2 diagnostic/cache files. The guard initially rejected the unnumbered
game_log.txt; inspected its Qud log contents, then added that exact filename to
the existing diagnostic classification and reran preservation successfully.
Both hidden processes exited zero and are absent. Source and retained evidence
are intentional outputs. Private packages and inspection scratch remain in use
for stage 2; remove them when no longer needed, including at a desktop pause.

Known scope limits: explicit dirt-floor fill; native shrine initialization logged
three missing-world-history exceptions, not map-placement failures. Other walls,
water and furniture retain original sprites; their dark backgrounds are visible.
Scene construction and PNG readback timings are not gameplay frame-time evidence.
No production caching or general renderer framework introduced.

Stage 2 reconciliation: eleven scenario frames and twenty-two actual GPU images
verified. Baseline maps 1810 cells, keeps 190 original foreground cells, draws 274
grass clumps at native Dirty-painter locations and 51 connected wading-depth
liquid surfaces. Hidden cells expose no liquid identity/geometry. Captured liquid
volumes vary through normal native initialization (473-1500 in this run); none
is swimming depth. A separately labeled 4000-dram fixture selects the deep ramp,
then restores the original volume. Native threshold checks passed at 199, 200,
1999 and 2000 drams. Actual GPU green-ground checks passed at 575 bare centers.

Terrain correction: inspected donor TerrainDef/SectionLayer_Terrain confirmed a
single material for a terrain's solid quad and transition fan, render queues
2000 + precedence, and repeat/trilinear/mip texture sampling. The earlier sample
mixed hard interiors with rough edges and an amplified sand tint. Corrected
those inputs together and inspected the resulting full-map output; the bright
rim is gone and the transition merges with the path interior. No blur shader,
texture painting or change to authored cells was introduced.

Water remains an explicit known-layer adapter using donor ramp textures and the
already tested cutout/fade shaders, not a port of RimWorld's WaterDepth/reflection
pipeline. Native foreground/detail colors over water remain; their background
is made transparent to expose that known visible liquid underlay.

Across all five launches so far, saves/options and installed game content are
unchanged, Unity display preferences restored; diagnostic/cache changes are 63
created, 3 removed, 2 modified. Scoped packages/scratch remain needed for stage 3.
Stage-closure review found no required speculative refactor or new infrastructure.

Stage 3 retains actual gameplay presentation/targeting/menu/save-load behavior.
Native bootstrap diagnostics now create a fully generated Joppa world with a
real player and initialized history through NewGame. The first native build-code
attempt lacked UI-owned gamemode/character-type choices; these are now explicitly
selected in the isolated diagnostic. The native single-button embark message is
acknowledged through its own callback, without OS input; unknown prompts are
recorded and stop the diagnostic. This is bootstrap evidence only: no live donor
presentation, targeting, menus or save/load acceptance had passed at that point.
This initial bootstrap evidence is superseded by the native gameplay checks below.
Tracked deferrals: none. Overall experiment is not complete.

Stage 3 diagnostic interruption: the native-game bootstrap reached Joppa world
generation but did not return from NewGame before the user heard game audio.
Stopped the exact owned batch process and observed its launcher exit. The profile
guard verified no changed saves/settings and restored nine Unity preferences.
The launch profile had muted music/effects but omitted the independent ambient
channel and master volume. All audio categories are now disabled in the isolated
profile, with master/ambient volumes zero and Unity's listener paused. A runtime
assertion checks that suppression before further diagnostics. The subsequent
native bootstrap passed this assertion, recorded all three categories disabled,
master/ambient/listener volumes zero and listener paused, and exited zero. No Qud
process remains. The latest aggregate guard reports 135 created and 3 removed
diagnostic/cache files, no changed saves/settings and nine restored Unity
preferences. This interruption and its correction do not satisfy gameplay,
targeting, menus or save/load acceptance.

Scratch owner: `E:/Temp/qud-transplant-probe-joppa-20261019`; cleanup transaction
`4fab00f509c5f82947297bc94a46dc51`. Expected expendable output: private Python
packages/cache, scoped decompilation diagnostics, extracted donor materials,
compiled diagnostics, isolated profile, logs and intermediate captures. Requested
source, reviewed image evidence and comparison deliverables are retained.

## Stage 3 history — native integration verified; foreground gate initially parked

Implemented and verified through the real map camera: generated Joppa with native
history/player, accepted/consumed frame hashes, mapped native painted ground,
adjacent movement through native commands, coordinate-bearing look input, modern
inventory open/close, replacement disable/re-enable, native save/load and three
continuous turns through RunGame/its native scheduler. Eight phase pairs contain
16 actual 640 × 480 map-camera readbacks. The separate HUD canvases are not in
these images. Desktop/mobile comparison, scene switching, divider drag, keyboard
and buttons passed against the served URL.

Integration fixes were scoped to proven boundaries: use the loaded native UI
presentation shader; suppress replaced native renderers at camera pre-cull after
Qud's LateUpdate can re-enable them; restore on unmatched buffers/views; use
native SaveGame's synchronous-success contract and validate by loading actual
saved state. Native opaque ground-layer pixels match the controlled renderer;
Qud's map-camera effects remain applied. No compensating color/style patch added.

At the earlier pause, the external blocker was J4 physical pointer/keyboard routing, full HUD visibility
and final foreground readability have not been observed. Their actual path
requires opening and operating a game window, outside the standing hidden-only
authorization. Resolve by user authorization for one silent isolated `review`
session, then verify normal walking, mouse look/targeting, zoom, inventory/HUD and
save/quit. The prepared review mode is compiled but unexecuted; it uses the same
presentation and native loop without automatic commands or menu closing. Overall
playable-sample completion and a working-mod claim depend on this gate. Stage 3
was parked BLOCKED; no later implementation stage was ACTIVE. Tracked deferrals:
none. No production FPS or long-session stability claim is made.

Fresh automated run: exit zero, no remaining CoQ process, master/ambient/listener
volumes zero and listener paused; no changed normal saves/settings, nine restored
Unity preferences. Aggregate native diagnostic/cache effects: 219 created,
3 removed, 1 modified. Native shutdown can log a loading-thread abort/platform
shutdown exception; the successful probe/preservation results do not establish
production shutdown parity. See `evidence/gameplay-result.json`.

Stage 3 parking cleanup: discarded the original broad-root inventory because the
root contains requested captures and donor inputs needed for foreground review.
Reviewed all 2,191 entries of exact expendable tooling/profile targets in
transaction `5dcf37b27b3458459d1e4a857cf69f2c`, then applied its signed ticket:
102,214,642 logical bytes removed, no exclusions/errors/residual candidates.
Packages/cache, scoped decompilation, closed browser profile, isolated test
profile and compile intermediates are gone. Requested captures, private run
evidence and `donor/` review inputs remain intentionally. Complete gameplay
evidence is also retained in ignored `local/gameplay-20261019/` and verified there.
The completed run's profile baseline moved with that evidence; the next launch
will capture a fresh baseline rather than restore stale preferences.

Foreground gate resumed: the user explicitly authorized the proposed silent
isolated window and physical-input/HUD check with "go ahead". The authorization
blocker was resolved; stage 3 resumed ACTIVE for the remaining checks below.

## Foreground result and final reconciliation

The actual 1280 × 800 window showed the full HUD, donor terrain and native actors.
Mouse walking moved the player from (37,22) through (39,22) to (43,17). Right-click
selected Warden Yrame; mouse-wheel zoom retained map alignment. The user confirmed
physical I opened inventory, and its native StatusScreensScreen was captured.
Closing inventory restored donor presentation. The on-screen menu also opened
correctly; native Save and Quit wrote a 551,538-byte save, displayed "Game saved!"
and exited zero after mouse acknowledgement. The save's gzip integrity was checked.

Native rendering beneath menus is intentional conservative fallback: unrelated
views restore owned sprite visibility and hide the donor layer; returning to Stage
rebuilds it from an accepted buffer. This is not donor-layer loss during gameplay.
The first review exposed a nullable message in the diagnostic popup hook; fixing
that exact contract removed its exception. Review now enters through the native
main menu and NewGame/RunGame lifecycle, without the loader's direct-game shortcut.

Keyboard coverage is deliberately bounded. Physical I worked; synthetic keys were
visible to Unity's legacy Input but did not trigger the tested native shortcuts.
The user clarified that walking was by pointer. Keyboard movement is unverified.
Physical Escape stopped the desktop-control tool, so its game-menu shortcut is
also unverified. The mouse menu path passed. No input rerouting workaround was
added. These results establish basic input coexistence, not every key binding,
production frame rate or long-session stability.

Fresh preservation checks found no changed normal saves/settings, restored ten
Unity preferences, and recorded 66 created, two removed and one modified normal
diagnostic/cache files across the two foreground attempts. Installed game content
remains unchanged. The original launcher completed and no CoQ process remained.
Reviewed transaction `5a53801542629bddc56811075b6b213f` removed all 28 expendable
profile/scratch entries (983,931 logical bytes), with no errors or exclusions.
The completed profile baseline moved into the private review archive so the next
launch captures fresh preferences. Requested captures and private evidence remain;
donor inputs remain local
for reproducibility and are excluded from publication.

J1-J3 remain verified by the full-village and accepted-frame evidence. J6-J7 remain
verified by the marsh/depth/terrain scenarios. J4 is satisfied by native automated
save/load and targeting plus this bounded foreground workflow. J5 preservation,
observed exit and reviewed cleanup passed; source/docs and contextual evidence
are included in the verified closure commit. No blockers or tracked deferrals.
All three stages are COMPLETE, with no ACTIVE stage. No speculative consolidation or
new rendering abstraction is needed for the specified experiment.

See [foreground evidence](../evidence/foreground-review.json) and the README's
unaltered HUD/menu captures. This closes the specified feasibility sample; it does
not constitute a released overhaul. Remote synchronization is verified separately
at delivery.
