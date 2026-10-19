# Joppa rendering integration specification

Authority: already_authorized. On 2026-10-19 the user instructed execution with
Specification-Gated Implementation, pausing only when desktop testing is needed.
Earlier instructions select actual RimWorld human/animal placeholders, applicable
hurt reactions and a fourth step making NPCs wear actual equipped Qud items.
This document governs this implementation; the earlier feasibility experiment
remains a separately completed, narrower result.

## Required behavior

- P1: Render a real generated Joppa game through Qud's native camera with locally
  sourced RimWorld human and animal graphics, a prop and connected scenery.
  Establish transparent body/head composition, direction, scale, feet/pivots,
  ground beneath foreground objects and depth ordering among mapped content.
  Preserve native input targets and original fallback for unsupported appearances.
- P2: Capture native selected appearances and known visible supporting layers
  once, publish only with the accepted buffer generation, and respect visibility,
  late changes, tint/detail/flip changes and source-instance identity. Never rerun
  Cell.Render or expose hidden identities. Rebuild presentation after load.
- P3: Drive hurt flash/offset from actual Qud damage, and direction/movement from
  Qud state. Effects are visual; they neither advance turns nor import donor AI,
  health/jobs or TickManager. A reaction can finish while Qud waits for input.
  Keep supported posture states explicit; injured does not imply downed/dead.
- P4: Expand from the first scene to Joppa's observed NPC/item coverage. Reconcile
  the 67 selected blueprint types in the retained controlled baseline and the
  generated-game additions; record each replacement and required appearance
  variants. Raw instantiated widgets/landmarks are not automatically art targets.
  Donor placeholders are explicit, and unknown content stays native. Do not count
  repeated terrain cells as distinct converted assets. Use existing appropriate
  donor resources first; custom art, when required, is one subject at a time with
  original sprite/description references, preserving recognizable Qud design.
- P5: Make NPCs visibly wear a bounded explicit selection of actually equipped
  Qud clothing/armor, initially using appropriate donor worn-apparel graphics.
  Read equipment/body slots rather than inventory ownership. Support at least a
  torso garment, outer garment and head item, plus the mapped held-item case.
  Respect facing, fit, layer order and relevant tint. Verify equip/remove/swap,
  movement, hurt and native save/load. Unsupported equipment/anatomy has an
  explicit native fallback. Do not mutate real NPC equipment to manufacture a
  result; isolated diagnostic fixtures may change their own equipment.
- P6: Use isolated, silent profiles and one owned game process; preserve installed
  binaries, user saves/settings and unrelated processes. Observe each original
  launch to actual completion, restore preferences and clean expendable scratch.
  Use existing native commands for required testing. An in-game MCP endpoint is
  authorized only if needed by a concrete acceptance check; it is not itself a
  deliverable. No arbitrary sleeps, kill deadlines or repeated desktop takeover.
- P7: Verify actual engine images plus native gameplay/state, including movement,
  targeting, visibility, menu return, disable/restore and save/load. Reuse valid
  unchanged prior evidence; new rendering paths require fresh integration checks.
  Pause before a required desktop-only check, identifying its unmet criterion.
  No separate speculative performance gate or unsupported FPS claim.
- P8: Maintain source, acceptance ledger and sanitized contextual captures in the
  authorized public RimQud repository. Verify, commit and synchronize completed
  work. Donor textures/bundles, decompiled source and private profiles stay local.
  No external mod release is authorized by this implementation request.

## Compact staged plan and acceptance ledger

There is exactly one ACTIVE implementation stage. Each acceptance unit below is
a complete integrated workflow; source/package/unit checks are diagnostics only.

| Stage | Status | Requirements | Acceptance outcome |
| --- | --- | --- | --- |
| 1. Layered NPC/prop scene | COMPLETE | P1, P2, P6-P8 | Generated Joppa shows one layered human, one animal and a prop with correct ground, direction, transparency, mapped overlap and native input binding; actual camera pairs plus visibility/late-change/fallback checks pass. |
| 2. Native reactions and lifecycle | NOT STARTED | P2, P3, P6-P8 | Real Qud movement/damage drives facing and a finite visible hurt reaction; targeting, menus, save/load and return work with the new scene; no simulation authority transferred. |
| 3. Joppa coverage | NOT STARTED | P1, P2, P4, P6-P8 | Every selected baseline blueprint and observed generated addition has a reviewed explicit rendering decision; known eligible content receives its mapped replacement, required state variants pass, and unsupported content retains verified fallback. |
| 4. Visible equipped items | NOT STARTED | P2, P3, P5-P8 | A native NPC fixture actually equips/removes/swaps supported torso/outer/head/held items; correct layers/facing/tint react to those changes and survive movement, damage and save/load. |

Stage 1 reconciliation: [fresh engine evidence](../evidence/pawns-stage1-result.json)
passed the full layered scene and native workflow. Twenty-one paired 1280 x 800
map-camera captures exercised human east/west, cat east/north, tint, known ground,
mapped overlap, hidden-source exclusion, late-change fallback, native NPC look,
menus, disabling, save/load and three continuous native turns. Native colliders
and coordinate bindings remained enabled. Visual inspection confirmed body/head
composition and the directional cat. Fixtures relocate existing objects only in
the isolated generated game; captures omit separate HUD canvases.

The first captures exposed a diagnostic camera-layout transition: source render
target composition was correct, but startup projection differed between phases.
Captures now wait for the native LetterboxCamera delay/refresh state to complete
and record per-frame camera coordinates. Tint verification checks red-pixel gain,
not merely differences caused by native CRT effects. No cosmetic correction was
added. One attempted baseline renewal was refused by the preservation guard before
game launch; completed evidence was archived rather than bypassing that guard.

The original launchers completed with zero exit codes and no CoQ process remained.
Normal saves/settings were unchanged; twelve Unity preferences were restored.
The last two runs share their retained preservation baseline (26 created, two
removed and one modified native diagnostic/cache files). A cross-volume baseline
archive attempt failed; the old baseline stayed intact and was used for the final
run. It is retained with the run evidence and will be archived before stage 2.
Source identities and selected image hashes were verified before publication.
Tooling/private donor inputs remain needed by stage 2; expendable scratch is owned
by cleanup transaction `01f2f4761b43f93f2655004ff20ae467` for final cleanup or a pause.

Stage-closure refactoring assessment: the existing accepted-buffer/material path
remains in use. The added known-layer/pose adapter and body/head composition serve
this scene and the required apparel stage; no separate RPC framework or renderer
was introduced. No acceptance-blocking consolidation was found.

Stage 1 remaining acceptance: none. Stages 2-4 remain required and incomplete.

Tracked deferrals: none. Stage 4 is a named requirement, not permission to weaken
earlier acceptance. Overall completion requires all stages and final reconciliation.

## Design boundary

Reuse the existing accepted-buffer observer, donor material/quad conventions,
native camera and native command diagnostics. Separate presentation of known
ground from known foreground. Add only the actor/prop data and owned render state
required for this scene; preserve native fallback for unrecognized state changes.
Do not transplant high-level Pawn/Map/Thing classes or create a general renderer,
RPC framework or arbitrary-mod resolver in anticipation of future use.

Continuous visual effects need a visual lifetime, not additional game turns.
Equipment presentation will consume native body-slot state at stage 4; body/head
composition established in stage 1 must support that actual later requirement.

Desktop acceptance: deferred until evidence shows a required check cannot be done
through native commands and captures. This is a workflow constraint, not a tracked
deferral of a current-stage acceptance criterion.
