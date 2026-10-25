from pathlib import Path
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1] / "hermes-wear"

class WearDistributionTests(unittest.TestCase):
    def test_distribution_contains_only_portable_source(self):
        allowed = {"SOUL.md", "config.yaml", "distribution.yaml", "README.md", ".no-bundled-skills", "skills/wrist-interactions/SKILL.md"}
        actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob("*") if p.is_file()}
        self.assertEqual(allowed, actual)
        for name in actual:
            self.assertFalse((ROOT / name).is_symlink())
            text = (ROOT / name).read_text()
            self.assertNotIn("/home/", text)
            self.assertNotRegex(text, r"100(?:\.[0-9]{1,3}){3}|192\.168\.")
    def test_identity_and_tool_boundary(self):
        manifest = yaml.safe_load((ROOT / "distribution.yaml").read_text())
        self.assertEqual("hermes-wear", manifest["name"])
        config = yaml.safe_load((ROOT / "config.yaml").read_text())
        self.assertNotIn("model", config)
        for tools in config["platform_toolsets"].values():
            self.assertEqual(["memory", "session_search"], tools)
        self.assertEqual("off", config["tools"]["tool_search"]["enabled"])
