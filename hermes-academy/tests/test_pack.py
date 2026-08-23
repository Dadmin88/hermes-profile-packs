import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class AcademyPackTests(unittest.TestCase):
    def setUp(self):
        self.manifest = json.loads((ROOT / "academy.json").read_text(encoding="utf-8"))
        self.shared_skill_names = {
            s["name"] for s in self.manifest.get("shared_skills", [])
        }

    def test_namespace_count_and_categories(self):
        profiles = self.manifest["profiles"]
        self.assertEqual(self.manifest["profile_count"], len(profiles))
        self.assertEqual(sum(self.manifest["categories"].values()), len(profiles))
        self.assertTrue(all(p["name"].startswith("academy-") for p in profiles))

    def test_v02_faculty_and_skill_targets(self):
        profiles = self.manifest["profiles"]
        self.assertEqual(self.manifest["version"], "0.2.0")
        self.assertEqual(len(profiles), 30)
        self.assertEqual(sum(len(profile["jobs"]) for profile in profiles), 120)

        expected_second_wave = {
            "academy-physics-professor",
            "academy-chemistry-professor",
            "academy-biology-professor",
            "academy-statistics-professor",
            "academy-data-science-professor",
            "academy-philosophy-professor",
            "academy-law-professor",
            "academy-theology-religious-studies-professor",
            "academy-education-professor",
            "academy-cybersecurity-instructor",
            "academy-cloud-systems-instructor",
            "academy-project-management-instructor",
            "academy-automotive-instructor",
            "academy-culinary-arts-instructor",
            "academy-music-instructor",
        }
        names = {profile["name"] for profile in profiles}
        self.assertTrue(expected_second_wave.issubset(names))

    def test_broad_science_chair_is_preserved_with_specialist_preference(self):
        names = {profile["name"] for profile in self.manifest["profiles"]}
        self.assertIn("academy-natural-sciences-professor", names)
        self.assertIn("academy-natural-sciences-professor", self.manifest["routing"]["broad_chairs"])
        specialist_preferences = self.manifest["routing"]["specialist_preferences"]
        self.assertEqual(specialist_preferences["physics"], "academy-physics-professor")
        self.assertEqual(specialist_preferences["chemistry"], "academy-chemistry-professor")
        self.assertEqual(specialist_preferences["biology"], "academy-biology-professor")

    def test_every_specialist_preference_targets_installed_faculty(self):
        names = {profile["name"] for profile in self.manifest["profiles"]}
        for topic, profile_name in self.manifest["routing"]["specialist_preferences"].items():
            self.assertIn(profile_name, names, topic)

    def test_every_job_has_skill(self):
        """Profile-owned jobs must match non-shared skills in the filesystem."""
        for profile in self.manifest["profiles"]:
            root = ROOT / "profiles" / profile["name"] / "skills"
            all_skills = {p.parent.name for p in root.glob("*/SKILL.md")}
            # Exclude shared skills — they are a separate distribution mechanism
            own_skills = all_skills - self.shared_skill_names
            self.assertEqual(set(profile["jobs"]), own_skills, profile["name"])

    def test_profiles_are_intentionally_isolated(self):
        for profile in self.manifest["profiles"]:
            self.assertTrue((ROOT / "profiles" / profile["name"] / ".no-bundled-skills").is_file(), profile["name"])

    def test_no_runtime_state_files(self):
        forbidden = {"auth.json", ".env", "state.db", "projects.db", "gateway.pid"}
        found = {p.name for p in (ROOT / "profiles").rglob("*") if p.is_file() and p.name in forbidden}
        self.assertFalse(found, sorted(found))


if __name__ == "__main__":
    unittest.main()
