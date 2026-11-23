"""Curated native personality pilot: source, materialization, and safety invariants."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import capabilities  # noqa: E402

PILOTS = {
    "agency-backend-engineer": "hermes-agency",
    "academy-cybersecurity-instructor": "hermes-academy",
    "council-parenting-coach": "hermes-council",
}
PROTECTED_CONFIGS = {"agency-orchestrator", "hermes-wear"}


class ProfilePersonalityTests(unittest.TestCase):
    def test_source_name_and_native_registration(self):
        expected = capabilities.source_profiles(ROOT)
        sources = capabilities.load_personalities(ROOT, expected)
        self.assertEqual(set(sources), set(expected))
        self.assertEqual(len(sources), 168)
        self.assertEqual(len({source["description"] for source in sources.values()}), len(sources))
        for name, relative_path in expected.items():
            pack = relative_path.split("/")[0]
            path = ROOT / relative_path

            with self.subTest(name=name):
                cfg = json.loads(
                    (path / "config.yaml").read_text(encoding="utf-8")
                )
                self.assertEqual(cfg["display"]["personality"], name)
                self.assertEqual(set(cfg["agent"]["personalities"]), {name})
                self.assertEqual(cfg["agent"]["personalities"][name], sources[name])
                self.assertNotIn("system_prompt", cfg["agent"])
                self.assertNotIn("model", cfg)
                if name not in PROTECTED_CONFIGS:
                    self.assertNotIn("toolsets", cfg)

    def test_generated_native_config_is_current(self):
        data = capabilities.load_json(ROOT / "capabilities/profiles.json")
        rendered = capabilities.render_outputs(ROOT, data)
        for name, relative_path in capabilities.source_profiles(ROOT).items():
            with self.subTest(name=name):
                file = ROOT / relative_path / "config.yaml"
                self.assertEqual(rendered[file], file.read_bytes())

    def test_existing_restricted_configs_are_preserved(self):
        seeds = capabilities.load_json(ROOT / "capabilities/preserved-config-seeds.json")
        for name in PROTECTED_CONFIGS:
            with self.subTest(name=name):
                path = ROOT / capabilities.source_profiles(ROOT)[name] / "config.yaml"
                cfg = json.loads(path.read_text(encoding="utf-8"))
                original = seeds[name]
                for key, value in original.items():
                    if key != "agent":
                        self.assertEqual(cfg[key], value)
                    else:
                        for setting, original_value in value.items():
                            self.assertEqual(cfg["agent"][setting], original_value)
                self.assertEqual(cfg["display"]["personality"], name)

    def test_all_personalities_are_differentiated_and_role_specific(self):
        sources = capabilities.load_personalities(ROOT, capabilities.source_profiles(ROOT))
        for name, persona in sources.items():
            with self.subTest(name=name):
                self.assertGreater(len(persona["system_prompt"]), 180)
                self.assertGreater(len(persona["description"]), 30)
                self.assertIn("SOUL.md", persona["system_prompt"])
                self.assertNotIn("agent.system_prompt", persona["system_prompt"])

    def test_backend_disabled_mcp_seed_is_retained(self):
        cfg = json.loads(
            (ROOT / "hermes-agency/profiles/agency-backend-engineer/config.yaml").read_text()
        )
        self.assertEqual(set(cfg["mcp_servers"]), {"context7"})
        server = cfg["mcp_servers"]["context7"]
        self.assertIs(server["enabled"], False)
        self.assertIs(server["sampling"]["enabled"], False)
        self.assertIs(server["elicitation"]["enabled"], False)
        self.assertEqual(server["trust"], "untrusted")

    def test_unknown_source_fails_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            folder = Path(temp) / "personalities"
            folder.mkdir()
            (folder / "not-a-public-profile.json").write_text(
                json.dumps({
                    "description": "Something",
                    "system_prompt": "Some " * 100,
                    "tone": "Neutral",
                    "style": "Plain",
                })
            )
            with self.assertRaisesRegex(ValueError, "unknown or unsafe personality"):
                capabilities.load_personalities(Path(temp), capabilities.source_profiles(ROOT))

    def test_invalid_or_extra_personality_fields_fail_closed(self):
        good = capabilities.load_personalities(ROOT, capabilities.source_profiles(ROOT))[
            "agency-backend-engineer"
        ]
        for change in ({"tone": ""}, {"toolsets": ["terminal"]}, {"system_prompt": ""}):
            with self.subTest(change=change), tempfile.TemporaryDirectory() as temp:
                folder = Path(temp) / "personalities"
                folder.mkdir()
                (folder / "agency-backend-engineer.json").write_text(
                    json.dumps({**good, **change})
                )
                with self.assertRaisesRegex(ValueError, "invalid personality"):
                    capabilities.load_personalities(Path(temp), capabilities.source_profiles(ROOT))


if __name__ == "__main__":
    unittest.main()
