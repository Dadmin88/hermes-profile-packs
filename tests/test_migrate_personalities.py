"""Bounded regression coverage for the install-side personality migration."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from migrate_personalities import atomic_write, digest, load_yaml, plan, render, restore, store_backup


def persona(name="agency-game-designer"):
    return json.loads((ROOT / "personalities" / (name + ".json")).read_text())


class PersonalityMigrationTests(unittest.TestCase):
    def test_json_preserves_unrelated_settings(self):
        source = {"model": {"default": "my-model"}, "mcp_servers": {"pix": {"enabled": False}},
                  "_config_version": 7}
        before = (json.dumps(source) + "\n").encode()
        after, action = render(before, "agency-game-designer", persona())
        updated = load_yaml(after.decode())
        self.assertEqual(source["model"], updated["model"])
        self.assertEqual(source["mcp_servers"], updated["mcp_servers"])
        self.assertEqual(updated["_config_version"], 7)
        self.assertEqual(updated["display"]["personality"], "agency-game-designer")
        self.assertEqual(updated["agent"]["personalities"]["agency-game-designer"], persona())
        self.assertEqual(action, "activate")
        again, status = render(after, "agency-game-designer", persona())
        self.assertIsNone(again)
        self.assertIn("already", status)

    def test_yaml_preserves_comments_and_display_options(self):
        before = b"# owned header\nmodel:\n  default: local\n\ndisplay:\n  theme: dark\n# owned footer\n"
        after, _ = render(before, "agency-game-designer", persona())
        self.assertIn(b"# owned header", after)
        self.assertIn(b"# owned footer", after)
        self.assertIn(b"theme: dark", after)
        result = load_yaml(after.decode())
        self.assertEqual(result["model"], {"default": "local"})
        self.assertEqual(result["display"]["theme"], "dark")
        self.assertEqual(result["display"]["personality"], "agency-game-designer")

    def test_manual_prompt_and_existing_personality_selection_are_respected(self):
        before = b"agent:\n  system_prompt: 'my own instructions'\ndisplay:\n  personality: teacher\n"
        after, action = render(before, "agency-game-designer", persona())
        cfg = load_yaml(after.decode())
        self.assertEqual(cfg["agent"]["system_prompt"], "my own instructions")
        self.assertEqual(cfg["display"]["personality"], "teacher")
        self.assertIn("preserve", action)
        conflicting = json.dumps({"agent": {"personalities": {"agency-game-designer": {
            "description": "local owned preset"}}}}).encode()
        candidate, why = render(conflicting, "agency-game-designer", persona())
        self.assertIsNone(candidate)
        self.assertIn("different", why)

    def test_source_plan_creates_only_matching_installed_configs(self):
        with tempfile.TemporaryDirectory() as tmp:
            installed = Path(tmp) / "profiles"
            installed.mkdir()
            (installed / "agency-game-designer").mkdir()
            (installed / "network-chuck").mkdir()
            entries, skipped = plan(ROOT, installed)
            self.assertEqual([entry["profile"] for entry in entries], ["agency-game-designer"])
            self.assertEqual(skipped, [])
            self.assertIsNone(entries[0]["old"])
            self.assertTrue(entries[0]["new"])

    def test_private_backup_and_guarded_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            installed = Path(tmp) / "profiles"
            folder = installed / "agency-game-designer"
            folder.mkdir(parents=True)
            cfg = folder / "config.yaml"
            original = b"model: private-choice\n"
            cfg.write_bytes(original)
            entries, _ = plan(ROOT, installed)
            backup = store_backup(entries, Path(tmp) / "backups")
            self.assertTrue((backup / "agency-game-designer.yaml").is_file())
            self.assertEqual((backup / "agency-game-designer.yaml").stat().st_mode & 0o777, 0o600)
            entry = entries[0]
            atomic_write(cfg, entry["new"], entry["mode"])
            self.assertEqual(digest(cfg.read_bytes()), entry["sha_after"])
            self.assertEqual(restore(installed, backup), ["agency-game-designer"])
            self.assertEqual(cfg.read_bytes(), original)
            atomic_write(cfg, b"model: user changed it\n")
            with self.assertRaisesRegex(ValueError, "config changed"):
                restore(installed, backup)


if __name__ == "__main__":
    unittest.main()
