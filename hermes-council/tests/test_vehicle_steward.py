import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROFILE = ROOT / "profiles" / "council-vehicle-steward"
EXPECTED_SKILLS = {
    "vehicle-records",
    "maintenance-planning",
    "repair-and-service-review",
    "vehicle-ownership-planning",
}


class VehicleStewardTests(unittest.TestCase):
    def test_manifest_and_distribution_contract(self):
        manifest = json.loads((ROOT / "council.json").read_text(encoding="utf-8"))
        matches = [p for p in manifest["profiles"] if p["name"] == "council-vehicle-steward"]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["category"], "stewardship")
        self.assertEqual(set(matches[0]["jobs"]), EXPECTED_SKILLS)
        self.assertTrue((PROFILE / ".no-bundled-skills").is_file())
        self.assertIn("name: council-vehicle-steward", (PROFILE / "distribution.yaml").read_text(encoding="utf-8"))

    def test_four_portable_skills_with_frontmatter(self):
        found = {path.parent.name for path in (PROFILE / "skills").glob("*/SKILL.md")}
        self.assertEqual(found, EXPECTED_SKILLS)
        for name in EXPECTED_SKILLS:
            body = (PROFILE / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(body.startswith(f"---\nname: {name}\ndescription: "), name)

    def test_provenance_and_no_unsafe_authority(self):
        records = (PROFILE / "skills" / "vehicle-records" / "SKILL.md").read_text(encoding="utf-8").lower()
        planning = (PROFILE / "skills" / "maintenance-planning" / "SKILL.md").read_text(encoding="utf-8").lower()
        soul = (PROFILE / "SOUL.md").read_text(encoding="utf-8").lower()
        for term in ("booked", "documented completed", "unknown", "evidence"):
            self.assertIn(term, records)
        for term in ("manufacturer", "units", "unknown"):
            self.assertIn(term, planning)
        for term in ("do not diagnose", "safe-to-drive", "explicit user authorization", "recall"):
            self.assertIn(term, soul)


if __name__ == "__main__":
    unittest.main()
