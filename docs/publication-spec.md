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

**ACTIVE — Prepare, verify and publish the documented research repository (R1-R5).**

Acceptance requires all five requirements above. The repository checker, reviewed
tree and remote read-back provide evidence. Existing engine evidence remains
applicable to byte-identical probe sources; repository publication does not
require another game launch.

Remaining: prepare content, inspect/check it, commit, create/push the public repo,
and read back its README, images and default-branch commit.

Blockers: none external. Missing acceptance work keeps this stage ACTIVE.
Tracked deferrals: none. Future renderer work is outside this requested deliverable.
