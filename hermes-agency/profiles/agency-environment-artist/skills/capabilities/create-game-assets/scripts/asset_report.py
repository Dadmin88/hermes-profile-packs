#!/usr/bin/env python3
"""Inspect raster game assets and enforce simple production constraints.

Requires Pillow 10+. The command exits 1 when an explicit constraint fails and
otherwise prints either a compact table or JSON suitable for build tooling.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from PIL import Image


def parse_size(value: str) -> tuple[int, int]:
    try:
        width_text, height_text = value.lower().split("x", 1)
        width, height = int(width_text), int(height_text)
    except (ValueError, AttributeError) as exc:
        raise argparse.ArgumentTypeError("size must look like WIDTHxHEIGHT") from exc
    if width <= 0 or height <= 0:
        raise argparse.ArgumentTypeError("size dimensions must be positive")
    return width, height


def alpha_stats(image: Image.Image) -> dict[str, Any]:
    has_alpha = "A" in image.getbands() or "transparency" in image.info
    if not has_alpha:
        return {
            "has_alpha": False,
            "alpha_min": 255,
            "alpha_max": 255,
            "transparent_pixels": 0,
            "content_bounds": [0, 0, image.width, image.height],
        }

    alpha = image.convert("RGBA").getchannel("A")
    extrema = alpha.getextrema()
    histogram = alpha.histogram()
    return {
        "has_alpha": True,
        "alpha_min": extrema[0],
        "alpha_max": extrema[1],
        "transparent_pixels": histogram[0],
        "content_bounds": list(alpha.getbbox() or (0, 0, 0, 0)),
    }


def inspect(path: Path, max_colors: int | None) -> dict[str, Any]:
    with Image.open(path) as image:
        image.load()
        # getcolors() returns None only when the count EXCEEDS maxcolors, so asking for
        # max_colors + 1 lets an over-limit image come back as a list one entry too long.
        limit = max_colors or 65535
        colors = image.convert("RGBA").getcolors(maxcolors=limit + 1)
        if colors is not None and len(colors) > limit:
            colors = None
        result: dict[str, Any] = {
            "path": path.as_posix(),
            "format": image.format,
            "mode": image.mode,
            "width": image.width,
            "height": image.height,
            "bytes": path.stat().st_size,
            "color_count": len(colors) if colors is not None else f">{limit}",
        }
        result.update(alpha_stats(image))
        return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="Raster image files to inspect")
    parser.add_argument("--expect-size", type=parse_size, metavar="WIDTHxHEIGHT")
    parser.add_argument(
        "--require-alpha",
        action="store_true",
        help="fail unless the image has an alpha channel with at least one transparent pixel",
    )
    parser.add_argument("--max-colors", type=int)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    if args.max_colors is not None and args.max_colors <= 0:
        parser.error("--max-colors must be positive")

    reports: list[dict[str, Any]] = []
    failed = False
    for path in args.paths:
        problems: list[str] = []
        if not path.is_file():
            reports.append({"path": path.as_posix(), "problems": ["file does not exist"]})
            failed = True
            continue
        try:
            report = inspect(path, args.max_colors)
        except (OSError, ValueError) as exc:
            reports.append({"path": path.as_posix(), "problems": [f"cannot read image: {exc}"]})
            failed = True
            continue

        if args.expect_size and (report["width"], report["height"]) != args.expect_size:
            problems.append(
                f"size is {report['width']}x{report['height']}; expected "
                f"{args.expect_size[0]}x{args.expect_size[1]}"
            )
        if args.require_alpha and not report["has_alpha"]:
            problems.append("image has no alpha channel")
        elif args.require_alpha and report["alpha_min"] == 255:
            # An RGBA file with every pixel opaque usually means a baked background
            # (often a fake checkerboard) rather than real transparency.
            problems.append("alpha channel is fully opaque; no pixel is transparent")
        if args.max_colors is not None and isinstance(report["color_count"], str):
            problems.append(f"image has more than {args.max_colors} colors")
        report["problems"] = problems
        reports.append(report)
        failed = failed or bool(problems)

    if args.as_json:
        print(json.dumps({"ok": not failed, "assets": reports}, indent=2))
    else:
        for report in reports:
            if "width" not in report:
                print(f"FAIL {report['path']}: {', '.join(report['problems'])}")
                continue
            state = "PASS" if not report["problems"] else "FAIL"
            print(
                f"{state} {report['path']} {report['width']}x{report['height']} "
                f"{report['mode']} colors={report['color_count']} alpha={report['has_alpha']}"
            )
            for problem in report["problems"]:
                print(f"  - {problem}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
