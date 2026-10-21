# Terrain, liquids and vegetation

Apply these contracts to new or revised RimQud environmental art and, when
separately authorized, its renderer binding. Preserve the selected source design
and native state ownership. An adapter fault calls for an adapter correction,
not automatic texture regeneration. Keep rejected captures and exact inputs.

## Bind the material to the actual shader

Record whether each source is a glyph mask, neutral albedo, detail/tint mask,
intrinsic opacity, connected boundary coverage, or foreground silhouette. Record
the destination shader, coordinate space, repeat period, image size, filtering,
color space, blend mode and layer order. Inspect the pinned shader or existing
proven binding rather than guessing from property names or a PNG thumbnail.

For the audited RimWorld donor `Custom/Terrain hard` / `Custom/Terrain fade`
binding, UV comes from **mesh-local XZ / 16**, not the supplied mesh UV channel.
The fade fragment multiplies sampled RGBA by vertex color and material tint.
Keep the full repeating material; the current selected fields are 1024 pixels over
16 cells. Do not supply independently cropped cell textures, clamp them, fit their
bounds to each quad, or assume changing the UV channel changes this shader.
Keep local mesh coordinates in logical cells; apply Qud's rectangular cell aspect
and map-axis transform through the mesh transform, preserving physical placement
and material scale together. Reinspect this contract for another shader/version;
these numbers are evidence for this binding, not universal terrain constants.

Keep intrinsic texture alpha (stone gaps, ripples) separate from the connected
boundary mask. For this fade shader, boundary coverage drives mesh vertex alpha;
sampled texture alpha remains intact. Resolve curved edges at intended display
size and preserve neighbor continuity. Do not sample fine stone opacity onto a
coarse boundary grid, multiply the same mask twice, or replace partial ripple
opacity with an opaque cutout threshold. Use explicit base/detail/foreground
precedence and mip/filter settings suitable for the actual displayed scale.

## Share ground; keep plants separate

Use one world-continuous, source-tinted substrate beneath dry converted cells,
including cells containing vegetation, paths or props. Drawing a different opaque
ground albedo only on grass-marked cells produces rectangular color patches even
when every native background color is identical. Apply the selected ground field
consistently; retain source-supported terrain distinctions and overlay masks.

Plant textures contain the plant silhouette with transparent surroundings. Do
not bake a green matte, ground tile, proxy, or preview background into them.
Choose the plant shader and physical scale from the actual reference/category;
retain the full registered frame and enlarge about its authored ground contact,
not its bounding-box center. The reviewed Joppa POC uses scale 2 for trees and
scale 1 for crops/reeds; do not apply the tree multiplier to all vegetation or
interpret it as a universal physical size. Check contact, sorting and nearby
props together at intended display size.

For a future revision of Joppa's cobblestone path, preserve the original loose
stones with generous grass-filled gaps rather than closely packed paving.
Record stone size, spacing/density and world scale in the editable construction.
The user explicitly kept the present cobblestone artwork for the current test;
this preference does not authorize regenerating that set now.

## Liquid identity and lighting

Use native open-volume, component/primary-liquid, depth and frozen-state metadata
to decide support. Do not infer liquid identity from blue pixels or use a fixed
numeric water proportion as a general eligibility rule. The observed Joppa pond
is water 600 / salt 400 brine. The current water-primary water/salt binding shares
Qud's b/B palette with fresh water; other mixtures and frozen surfaces retain
native rendering unless separately supported. Keep eligibility distinct from
purity, and preserve native objects above a supported liquid underlay.

Apply the same presentation lighting to converted and retained native graphics;
otherwise fallback water can appear self-lit against a darkened converted map.
Preserve native palette, local light, clock and visibility ownership. Label any
adapter night tint as an approximation; it is not proof of a transplanted lighting
system. Keep water-base and ripple opacity independent and blend each once.

## Review and integration evidence

During authoring, inspect connected patches and plant/ground compositions at
intended size for seams, isolated squares, inconsistent backgrounds, excessive
texture density, wrong contact/scale and damaged transparency. Record the shader
contract even when the integration phase is pending. Keep generating until the
complete requested set passes the generation gate; do not launch the game for
each texture or treat a single asset preview as native acceptance.

After that gate, use the authorized complete-set integration to compare actual
day/night and native-fog captures, including the earlier POC when relevant. Check
the material dimensions/repeat, boundary coverage, native liquid components,
plant scale/contact, retained fallbacks and the actual served report assets.
If a fog mod is used, verify the exact installed shader/provenance and rendered
mask, keep donor bundles private, and let Qud own sight/exploration. A rendering
shader does not authorize importing the mod's AI or revealing hidden objects.
