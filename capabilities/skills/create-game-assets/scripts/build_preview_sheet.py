#!/usr/bin/env python3
"""Build a labelled nearest-neighbor contact sheet for raster game assets.

Requires Pillow 10+. Inputs are sorted by path so repeated runs stay stable.
"""

from __future__ import annotations

import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def checkerboard(size: tuple[int, int], tile: int = 12) -> Image.Image:
    image = Image.new("RGBA", size, "#c9c9c9")
    draw = ImageDraw.Draw(image)
    for y in range(0, size[1], tile):
        for x in range(0, size[0], tile):
            if (x // tile + y // tile) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill="#eeeeee")
    return image


def fit_nearest(image: Image.Image, max_size: tuple[int, int]) -> Image.Image:
    source = image.convert("RGBA")
    scale = min(max_size[0] / source.width, max_size[1] / source.height)
    if scale >= 1:
        scale = max(1, math.floor(scale))
    width = max(1, round(source.width * scale))
    height = max(1, round(source.height * scale))
    return source.resize((width, height), Image.Resampling.NEAREST)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("inputs", nargs="+", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--columns", type=int, default=4)
    parser.add_argument("--cell-size", type=int, default=192)
    parser.add_argument("--padding", type=int, default=12)
    args = parser.parse_args()

    if args.columns <= 0 or args.cell_size <= 0 or args.padding < 0:
        parser.error("columns/cell-size must be positive and padding cannot be negative")

    paths = sorted({path.resolve() for path in args.inputs})
    missing = [path for path in paths if not path.is_file()]
    if missing:
        parser.error("missing input(s): " + ", ".join(path.as_posix() for path in missing))

    label_height = 24
    cell_width = args.cell_size + args.padding * 2
    cell_height = args.cell_size + label_height + args.padding * 2
    rows = math.ceil(len(paths) / args.columns)
    sheet = Image.new("RGBA", (cell_width * args.columns, cell_height * rows), "#202124")
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, path in enumerate(paths):
        column, row = index % args.columns, index // args.columns
        left, top = column * cell_width, row * cell_height
        preview = checkerboard((args.cell_size, args.cell_size))
        with Image.open(path) as source:
            fitted = fit_nearest(source, (args.cell_size, args.cell_size))
        x = (args.cell_size - fitted.width) // 2
        y = (args.cell_size - fitted.height) // 2
        preview.alpha_composite(fitted, (x, y))
        sheet.alpha_composite(preview, (left + args.padding, top + args.padding))
        label = path.name
        if len(label) > 30:
            label = label[:27] + "..."
        draw.text(
            (left + args.padding, top + args.padding + args.cell_size + 6),
            label,
            fill="#ffffff",
            font=font,
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    sheet.convert("RGB").save(args.out, quality=95)
    print(f"Wrote {args.out} ({len(paths)} assets, {args.columns} columns)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
