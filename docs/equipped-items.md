# Equipped items: verified native integration

Stage 4 reads actual Qud `BodyPart.Equipped` links. Carrying an item adds no
clothing. Native equipment changes, direction, item tint and save/load determine
the visible layers; no donor pawn simulation runs.

| Native item | Native slot | Temporary donor worn/held art |
| --- | --- | --- |
| Woven Tunic | Body | TribalA, Male template |
| Cloth Robe | Body | Duster, Male template |
| Leather Cloak | Back | Cape, Male template |
| Wide-brimmed Hat | Head | CowboyHat |
| Long Sword | Hand | Longsword |

These are explicitly temporary interpretations. The robe's coat silhouette is
not a faithful final design. One adult Male art template currently fits a bounded
Humanoid body shape; that choice does not change a Qud character's sex or anatomy.
Other equipment/body plans retain the whole native actor, including a tested
unsupported boot and an actual third-arm fixture. Stage 3's 26 replacement-type
count describes base mappings before this additional equipment eligibility check.

An isolated new farmer fixture carried the items, equipped four simultaneously,
removed its hat, swapped its torso garment, changed only the robe tint, moved in
four directions and received real native damage. All six layers shared the
finite reaction and restored their individual colors without advancing a turn.
Actual equipped identities/slots survived native save/load. Existing residents'
equipment was unchanged. Native look, menus, disable/restore and three continuous
turns also passed. See [retained evidence](../evidence/pawns-stage4-result.json).

The Core-owned observation publishes scalar appearance values only. The final
accepted-buffer check detects late equipment/color changes and restores native
presentation rather than rendering a stale outfit. Hidden identities remain
excluded. The diagnostic activates the apparel path after inherited baseline
checks; it then applies eligibility checks to all known visible layered actors.

An initial fixture failed because native unequip stacked its hat into another
stack, invalidating the tracked object. Fixture preparation now uses real native
unequip commands with NoStack and zero diagnostic energy cost. It does not change
normal stacking or resident behavior. A cape texture has compressed alpha values
starting at 3; original pixels are preserved below the donor cutout threshold.

The four public images are unaltered native frames. The comparison's optional
8x browser crop makes the small actor visible without changing image pixels.
Its before image is a donor-rendered body carrying unequipped items, not Qud's
original glyph. Other scenes retain their original-versus-replacement comparison.

Reproduce with local matching installations: run `probe/package_apparel.py` after
the existing donor packages, then `probe/run_probe.ps1 -Mode pawns
-IntegrationStage 4 -Root <owned-local-root>`, followed by
`probe/verify_gameplay.py --mode pawns --stage 4 --root <owned-local-root>`.
Normal profile preservation and original-process completion remain required.
No desktop input or MCP endpoint was needed for this bounded workflow.
