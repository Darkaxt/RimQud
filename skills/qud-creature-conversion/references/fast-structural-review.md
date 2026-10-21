# Fast independent structural review

Run after every ImageGen refinement or correction result, including retries,
before extraction, fitting or generation-ready credit. This is a short art
inspection, not native/game validation. Do not turn it into an open-ended audit
or a new approval gate.

Use a fresh agent without the authoring conversation. Give it only the asset ID,
exact image paths/hashes, source-supported anatomy/parts, authored per-view fit
contract, required views/states, unchanged manual/body reference, and intended
display size. Include the refined image as a target; do not give the author's
pass/fail explanation or suggest that the newest attempt is better. Use the
same model as the main agent at Low reasoning effort when required by standing
policy, with at most one active reviewer. The reviewer must not edit, regenerate,
delegate or expand scope. Preserve launch identity and actual configuration;
never invent an independent review that did not run.

The reviewer must view the actual pixels, including every required facing and
state. Inspect a relevant close-up when a suspected defect is unclear. Look for:

- anatomy/part count and body-family fidelity;
- actual emergence and contact surfaces, rather than a point inside alpha;
- complete continuous geometry and taper behind occluders;
- skull/body clearance for non-root segments and physically consistent overlap;
- fore/aft direction, roots, tips, near/far surfaces and self-occlusion across views;
- garment openings, strap endpoints, grips, detached fragments and foreign lines;
- cardinal camera, scale/pivot, edge/crop integrity and unintended backgrounds;
- neutral/tint separation and source identity, when visible evidence permits it.
- for environmental art: connected seams, unintended ground rectangles or mattes,
  stone/foliage density at intended size, and plant contact/scale in composition.

For example, a horn can have a root point inside the skull yet look like a flat
tube resting on it. A rear curl can show two unrelated-looking fragments despite
a mathematically continuous hidden centerline. Require the visible contact and
occluding contours to explain that geometry. Similar symmetric front/back
silhouettes and one visible horn in exact profile can be physically valid; do not
flag those alone. Do not invent native anatomy from absent metadata.

Return a compact finding list: asset, view/state, approximate region, concrete
observation, confidence, severity, evidence image and correction principle. State
what remains ambiguous and whether extraction/registration may proceed. A clear
image with no observed issue is a bounded screening result, not a guarantee.

The main author reads the report and checks each flagged area. Record each
finding as **FIX NOW**, **NEEDS CLOSER INSPECTION**, **MINOR POLISH**, or
**NOT SUBSTANTIATED**, with evidence and reasoning. FIX NOW covers source identity,
anatomy, broken attachment/continuity/coverage, impossible camera/depth and
material/frame defects that would propagate into current conversion work.
Unresolved serious or uncertain structural findings withhold readiness until
resolved. Minor cosmetic suggestions can remain outside the current correction
scope, but must not conceal required work. A required later correction needs a
named owning stage and verification criterion under the project specification.

Save the report, reviewed hashes and main-agent dispositions in the conversion
ledger and HTML evidence. Reuse a review only for unchanged reviewed bytes and
relevant context. Corrected outputs receive a fresh review. Never regenerate
automatically merely because a reviewer proposed a change; the main author owns
source interpretation, triage, fixes and final acceptance.

For an explicitly requested retrospective sweep, inventory selected texture sets
and their components, resolve shared dependencies by content hash, and review in
small bounded batches. Index superseded/rejected history separately; do not
silently count it as currently accepted art. Account for every current set,
including sets with no observed findings, missing evidence and assets not yet
created. Do not claim visual review of a component only because a script found
its file or an agent read its metadata. A batch contact image can establish broad
coverage; uncertain details require inspection at sufficient size.
