"""Distribution-level preload invariants for Academy Continuing Education."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ACADEMY_ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ACADEMY_ROOT / "academy.json").read_text(encoding="utf-8"))


def _manifest_list(path: Path, key: str) -> list[str]:
    values: list[str] = []
    active = False
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line == f"{key}:":
            active = True
            continue
        if active and raw_line and not raw_line[0].isspace():
            break
        if active:
            stripped = raw_line.strip()
            if stripped.startswith("- "):
                values.append(stripped[2:].strip().strip('"\''))
    return values


class AcademyDistributionPreloadTests(unittest.TestCase):
    def test_dean_preloads_faculty_routing(self):
        profile = ACADEMY_ROOT / "profiles" / "academy-dean"
        self.assertEqual(
            _manifest_list(profile / "distribution.yaml", "preload_skills"),
            ["faculty-routing"],
        )
        self.assertTrue((profile / "skills" / "faculty-routing" / "SKILL.md").is_file())

    def test_every_faculty_profile_preloads_teach_profile(self):
        names = [p["name"] for p in MANIFEST["profiles"] if p["name"] != "academy-dean"]
        self.assertEqual(len(names), 29)
        for name in names:
            profile = ACADEMY_ROOT / "profiles" / name
            with self.subTest(profile=name):
                self.assertEqual(
                    _manifest_list(profile / "distribution.yaml", "preload_skills"),
                    ["teach-profile"],
                )
                self.assertTrue((profile / "skills" / "teach-profile" / "SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
