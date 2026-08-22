import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AcademyPackTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "academy.json").read_text(encoding="utf-8"))

    def test_namespace_count_and_categories(self):
        profiles = self.manifest["profiles"]
        self.assertEqual(self.manifest["profile_count"], len(profiles))
        self.assertEqual(sum(self.manifest["categories"].values()), len(profiles))
        self.assertTrue(all(p["name"].startswith("academy-") for p in profiles))

    def test_every_job_has_skill(self):
        for profile in self.manifest["profiles"]:
            root = ROOT / "profiles" / profile["name"] / "skills"
            skills = {p.parent.name for p in root.glob("*/SKILL.md")}
            self.assertEqual(set(profile["jobs"]), skills, profile["name"])

    def test_profiles_are_intentionally_isolated(self):
        for profile in self.manifest["profiles"]:
            self.assertTrue((ROOT / "profiles" / profile["name"] / ".no-bundled-skills").is_file(), profile["name"])

    def test_no_runtime_state_files(self):
        forbidden = {"auth.json", ".env", "state.db", "projects.db", "gateway.pid"}
        found = {p.name for p in (ROOT / "profiles").rglob("*") if p.is_file() and p.name in forbidden}
        self.assertFalse(found, sorted(found))


if __name__ == "__main__":
    unittest.main()
