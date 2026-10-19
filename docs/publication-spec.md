# RimQud repository publication specification

Authority: the user requested a new public RimQud repository containing the
previous audits, integration progress and generated images in its README.
Publication is already authorized. A future working-mod release is an aspiration,
not part of this publication's acceptance criteria.

## Required outcome

- R1: Create a new public Darkaxt/RimQud repository with independent, sanitized
  history. Preserve the existing local visual-study project and its history.
- R2: Document all four audits, actual engine results, reproducible probe source,
  remaining integration limits and a bounded next experiment.
- R3: Embed the retained generated images and comparison screenshots directly in
  README, clearly distinguishing concepts from actual engine readbacks.
- R4: Publish no extracted game atlases, textures, compiled shaders, game binaries,
  private profiles, credentials or machine-specific diagnostic dumps. Explicitly
  document image provenance and third-party ownership.
- R5: Verify local content, source-copy identity and image/link integrity before
  committing; verify public visibility, remote commit and README/image delivery.
  Do not claim a finished visual-overhaul mod or publish a release.

## Single-stage plan and reconciliation

**COMPLETE — Prepare, verify and publish the documented research repository (R1-R5).**

Acceptance requires all five requirements above. The repository checker, reviewed
tree and remote read-back provide evidence. Existing engine evidence remains
applicable to byte-identical probe sources; repository publication does not
require another game launch.

Verified 2026-10-19:

- R1: a separate new repository was created at
  https://github.com/Darkaxt/RimQud; GitHub reports PUBLIC, isFork=false, default
  branch main. The original local study repository remains unchanged.
- R2: four audits, current engine results/limits, reproduction instructions and
  proposed next experiment are documented. All seven copied probe source files
  match the Git objects in the verified local experiment commit 4f7086a.
- R3: the public GitHub-rendered README contains seven image elements. All seven
  anonymous public image downloads match local SHA-256 hashes, and the public
  README source matches the local file. Captions distinguish concepts/readbacks.
- R4: reviewed the complete public tree and history. Only original source/docs,
  selected metadata and the seven manifested documentation images are included.
  The publication checker validates allowed file types, local links, image hashes,
  JSON/Python syntax and absence of selected private-path/credential patterns.
  PowerShell parser validation and staged whitespace validation passed.
- R5: initial publication commit was read back from origin/main and matched local
  HEAD. The closure record is synchronized and read back in the final delivery
  check. No game relaunch was needed for identical diagnostic sources; this is
  repository verification, not new gameplay validation. No release was created.

Stage-closure review: no new rendering abstraction or runtime behavior introduced.
The publication checker serves the current public-tree acceptance criteria.

Remaining acceptance work: none. Blockers: none. Tracked deferrals: none.
Future renderer work is outside this requested deliverable.
