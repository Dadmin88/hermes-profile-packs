from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1] / "hermes-wear"
SKILLS = {
    "wrist-interactions", "glanceable-answers", "voice-transcript-repair",
    "quick-capture", "reminders-and-time", "action-confirmations",
    "background-task-tracking", "reconnection-recovery",
    "wear-memory-privacy", "watch-context-safety",
    "watch-capability-discovery", "watch-device-context", "watch-tool-results",
}

class WearDistributionTests(unittest.TestCase):
    def test_distribution_contains_only_portable_source(self):
        allowed = {"SOUL.md", "config.yaml", "distribution.yaml", "README.md", ".no-bundled-skills", "DEVICE_AWARENESS.md",
                   "examples/device-capabilities.example.json", "examples/location-ok.example.json",
                   "examples/location-permission-required.example.json"}
        allowed.update(f"skills/{name}/SKILL.md" for name in SKILLS)
        actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
        self.assertEqual(allowed, actual)
        for name in actual:
            path = ROOT / name
            self.assertFalse(path.is_symlink())
            text = path.read_text()
            self.assertNotIn("/home/", text)
            self.assertNotIn("API_SERVER_KEY=", text)
            self.assertNotIn("sk-proj-", text)

    def test_identity_and_tool_boundary(self):
        manifest = yaml.safe_load((ROOT / "distribution.yaml").read_text())
        self.assertEqual("hermes-wear", manifest["name"])
        self.assertEqual("1.1.0", manifest["version"])
        config = yaml.safe_load((ROOT / "config.yaml").read_text())
        self.assertNotIn("model", config)
        expected = ["memory", "session_search", "skills", "web"]
        for toolsets in config["platform_toolsets"].values():
            self.assertEqual(expected, toolsets)
        disabled = set(config["agent"]["disabled_toolsets"])
        restricted = {"terminal", "file", "browser", "code_execution",
                      "delegation", "cronjob", "computer_use", "image_gen", "tts"}
        self.assertTrue(restricted <= disabled)
        self.assertFalse(set(expected) & disabled)
        self.assertEqual("off", config["tools"]["tool_search"]["enabled"])
        self.assertTrue((ROOT / ".no-bundled-skills").exists())

    def test_skills_have_matching_frontmatter(self):
        for name in SKILLS:
            with self.subTest(name=name):
                text = (ROOT / "skills" / name / "SKILL.md").read_text()
                self.assertTrue(text.startswith("---\n"))
                header, body = text.split("---\n", 2)[1:]
                frontmatter = yaml.safe_load(header)
                self.assertEqual(name, frontmatter["name"])
                self.assertTrue(frontmatter["description"])
                self.assertGreater(len(body), 250)

    def test_device_context_fixtures(self):
        import json
        examples = ROOT / "examples"
        caps = json.loads((examples / "device-capabilities.example.json").read_text())
        ok = json.loads((examples / "location-ok.example.json").read_text())
        denied = json.loads((examples / "location-permission-required.example.json").read_text())
        self.assertTrue(all(x["synthetic"] for x in (caps, ok, denied)))
        self.assertEqual("hermes-wear.capabilities.v1", caps["schema"])
        self.assertEqual("hermes-wear.tool-result.v1", ok["schema"])
        self.assertEqual("watch.location.current", ok["tool"])
        self.assertEqual("ok", ok["status"])
        self.assertIn("accuracy_m", ok["data"])
        self.assertEqual("permission_required", denied["status"])
        self.assertNotIn("latitude", denied.get("data", {}))
        self.assertIn("Never persist", (ROOT / "DEVICE_AWARENESS.md").read_text())

    def test_risk_sensitive_contracts(self):
        soul = (ROOT / "SOUL.md").read_text()
        self.assertIn("cannot create device features or tools", soul)
        self.assertIn("backend-enforced approval", soul)
        reminder = (ROOT / "skills/reminders-and-time/SKILL.md").read_text()
        capture = (ROOT / "skills/quick-capture/SKILL.md").read_text()
        recovery = (ROOT / "skills/reconnection-recovery/SKILL.md").read_text()
        self.assertIn("No reminder was set", reminder)
        self.assertIn("not saved", capture)
        self.assertIn("Never blindly resubmit", recovery)

if __name__ == "__main__":
    unittest.main()
