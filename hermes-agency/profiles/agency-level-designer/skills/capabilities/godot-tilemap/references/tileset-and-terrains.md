# TileSet & terrains reference (Godot 4.7)

Depth companion to `godot-tilemap`.

## TileSet sources

A `TileSet` holds one or more **sources**, each with an integer `source_id`:

- **Atlas source** (`TileSetAtlasSource`) — a single texture sliced into a grid of tiles.
  Most common. Tiles are addressed by `atlas_coords: Vector2i` (column, row).
- **Scene collection source** (`TileSetScenesCollectionSource`) — places whole scenes as
  tiles (e.g. a tile that is a particle emitter). `atlas_coords` is always `Vector2i(0,0)`
  and the `alternative_tile` selects the scene.

In code, `set_cell(coords, source_id, atlas_coords, alternative_tile)` fully identifies a
tile. `alternative_tile` selects flips/rotations or alternative tiles you defined.

## Per-tile data layers

Configured in the TileSet editor; each layer applies to every tile you paint data onto:

- **Physics layers** — collision polygons per tile. The TileSet defines layer index +
  collision layer/mask; `TileMapLayer.collision_enabled` toggles them at the node level.
- **Navigation layers** — navigation polygons for pathfinding. Note the docs caution that
  built-in tile navigation has limits; consider baking a `NavigationRegion2D` for large
  maps.
- **Occlusion layers** — light occluder polygons per tile.
- **Custom data layers** — named, typed values (`String`, `int`, `bool`, `Vector2`, ...).
  Read with `tile_data.get_custom_data("name")`. Ideal for gameplay metadata
  (`is_ladder`, `friction`, `damage`, `is_spawn`).

## Terrains (autotiling)

1. In the TileSet, create a **terrain set** (choose a matching mode: Match Corners and
   Sides, Match Corners, or Match Sides).
2. Add one or more **terrains** to that set.
3. Paint terrain **peering bits** onto each tile's edges/corners so Godot knows how tiles
   connect.
4. In the TileMap panel's **Terrains** tab, paint with **Connect** (auto-connect to
   neighbors on the layer) or **Path** (connect only along the current stroke).

From code:

```gdscript
set_cells_terrain_connect(cells, terrain_set, terrain, ignore_empty_terrains)
set_cells_terrain_path(path_cells, terrain_set, terrain, ignore_empty_terrains)
```

Both require the TileSet to have all needed bit combinations defined; missing
combinations yield placeholder/odd tiles.

## Coordinate conversions

```gdscript
local_to_map(local_pos: Vector2) -> Vector2i   # pixel (local) -> cell
map_to_local(cell: Vector2i)     -> Vector2     # cell -> centered local pixel pos
get_neighbor_cell(cell, TileSet.CELL_NEIGHBOR_RIGHT_SIDE)
get_surrounding_cells(cell)                     # all edge neighbors
```

For global coordinates wrap with `to_local()` / `to_global()` (Node2D methods).

## Y-sorting (top-down depth)

Enable `CanvasItem.y_sort_enabled` on the `TileMapLayer` and set per-tile
`y_sort_origin` (and the layer's `y_sort_origin`) so taller tiles and characters overlap
correctly. The rendering quadrant optimization is bypassed for Y-sorted layers (tiles are
grouped by Y instead).

## Runtime tile-data overrides

To vary a tile's data at runtime without editing the shared TileSet, override on a
`TileMapLayer` subclass:

```gdscript
extends TileMapLayer

func _use_tile_data_runtime_update(coords: Vector2i) -> bool:
    return get_cell_atlas_coords(coords) == Vector2i(3, 0)   # only these tiles

func _tile_data_runtime_update(coords: Vector2i, tile_data: TileData) -> void:
    # Duplicate sub-resources before editing — they are shared with the TileSet!
    tile_data.modulate = Color(1, 0.6, 0.6)
```

Call `notify_runtime_tile_data_update()` when the result of `_use_tile_data_runtime_update`
should change. These updates are computationally expensive — restrict them to the few
tiles that need them.

## Migrating from the TileMap node

A deprecated `TileMap` node with N layers becomes N `TileMapLayer` nodes. Godot offers a
"Extract TileMap layers as individual TileMapLayer nodes" tool from the TileMap node's
toolbar. After extraction, update scripts: drop the leading `layer` argument from cell
calls and target the specific `TileMapLayer` node instead.
