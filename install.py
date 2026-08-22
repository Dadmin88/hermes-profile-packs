#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PACKS = {
    "agency": ROOT / "hermes-agency" / "install.py",
    "hermes-agency": ROOT / "hermes-agency" / "install.py",
    "council": ROOT / "hermes-council" / "install.py",
    "hermes-council": ROOT / "hermes-council" / "install.py",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Install profiles from Hermes Profile Packs.")
    parser.add_argument("pack", nargs="?", help="agency or council")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="arguments forwarded to the pack installer")
    parser.add_argument("--list-packs", action="store_true")
    ns = parser.parse_args()

    if ns.list_packs:
        print("agency   agency-*   Professional multidisciplinary work")
        print("council  council-*  Personal support and life stewardship")
        return 0
    if not ns.pack:
        parser.error("choose a pack or use --list-packs")
    installer = PACKS.get(ns.pack)
    if installer is None:
        parser.error(f"unknown pack: {ns.pack}")
    return subprocess.run([sys.executable, str(installer), *ns.args]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
