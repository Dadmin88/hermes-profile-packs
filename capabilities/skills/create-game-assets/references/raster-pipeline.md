# Raster, sprite, tile, background, and UI pipeline

Use this reference for production 2D art and raster textures. Generated output is source material;
dimensions, grids, alpha, anchors, and import settings remain deterministic engineering concerns.

## Sprites and animation

1. Approve one idle/neutral seed at the final view and approximate game scale.
2. Lock canvas size, baseline/ground point, facing, palette, outline, proportions, and costume.
3. For a short animation, request the whole action as one strip or sheet referenced to the seed.
   Independent frame requests drift more. Treat the returned grid as a candidate, not exact data.
4. Slice and normalize frames with one shared scale and one shared anchor—usually bottom-center.
5. If frame 1 must equal a shipped idle pose, restore the exact seed after slicing.
6. Preview as a contact sheet and in motion. Check volume, foot sliding, silhouette, and cadence.

For true pixel art, enforce a real pixel grid after generation. Remove blended pseudo-pixels,
single-pixel noise, excess colors, banding, and inconsistent clusters. Resize only with
nearest-neighbor unless a deliberate preprocessing pass says otherwise.

## Tiles and repeatable textures

- Define tile dimensions and neighbor rules before creating art.
- Produce a base, transitions, corners, isolated pieces, and decoration as one visual family.
- Keep gameplay edges and collision meaning legible; decorative shadows must not imply false walls.
- Test seamless materials in a 3×3 repeat at full size and at minified camera scale.
- Inspect terrain combinations in the engine's autotile/terrain system, not only in a sheet.
- Keep padding/extrusion compatible with the engine/atlas tool to prevent texture bleeding.

## Backgrounds and parallax

- Split sky, far, mid, near, and foreground layers according to intended parallax speed.
- Avoid unique landmarks near horizontal seams when layers must scroll/repeat.
- Preserve a low-contrast playfield behind characters and projectiles.
- Keep focal detail away from HUD safe areas and critical navigation silhouettes.
- Export layers independently with overlap so camera movement cannot expose gaps.

## UI art and icons

- Keep labels, numbers, dynamic copy, focus state, and accessibility text code-native.
- Generate or draw ornament, frames, portraits, and texture—not rasterized functional text.
- Prefer one established icon family. Simple geometric symbols should usually be SVG/vector.
- Provide normal, hover/focus, pressed, disabled, selected, and warning states when art changes.
- Design scalable panels as 9-slice/nine-patch assets; verify corners and borders at several sizes.

## Import checkpoints

**Godot 4.7:** 2D filtering and repeat are not import options. Set
`rendering/textures/canvas_textures/default_texture_filter` to Nearest for a pixel-art project (or
`texture_filter` on one `CanvasItem` subtree), and enable `rendering/2d/snap/snap_2d_transforms_to_pixel`
when sprites shimmer while moving. Enable the `mipmaps/generate` import option only for non-pixel
textures that shrink substantially; set `texture_repeat` (or the 3D material's repeat) only for
textures designed to tile. Verify `Sprite2D`, `TileSet`, atlas regions, and animation frames in the
editor.

**Unity 6.3 LTS:** set Texture Type to Sprite (2D and UI), choose Single/Multiple correctly, set a
consistent Pixels Per Unit, filter mode, compression, mipmaps, mesh type, and sprite slicing.
Disable Read/Write unless runtime pixel access is actually required because it adds memory cost.

**Phaser/PixiJS/web:** keep atlas metadata and image filenames stable; use nearest sampling and
integer camera scaling for pixel art; prevent browser/CSS resizing from introducing blur; inspect
texture bleeding under the real renderer.

## Primary documentation

- [Godot 4.7 Image](https://docs.godotengine.org/en/4.7/classes/class_image.html)
- [Godot 4.7 Texture2D](https://docs.godotengine.org/en/4.7/classes/class_texture2d.html)
- [Unity sprite import settings](https://docs.unity3d.com/Manual/texture-type-sprite.html)
- [Phaser asset concepts](https://docs.phaser.io/phaser/concepts/loader)
- [PixiJS Assets guide](https://pixijs.com/8.x/guides/components/assets)
