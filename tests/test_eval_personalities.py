"""Isolated native personality selection checks (no provider or production files)."""
from __future__ import annotations

import sys
import types
from unittest import TestCase
from unittest.mock import patch

from evals.native_worker import resolve_distribution_personality


class NativePersonalitySelectionTests(TestCase):
    @staticmethod
    def stub():
        native = types.ModuleType("hermes_cli.personality")

        def normalize(value):
            name = str(value or "").strip().lower()
            return "" if name in {"", "none", "default", "neutral"} else name

        def active(cfg):
            name = normalize((cfg.get("display") or {}).get("personality"))
            catalog = (cfg.get("agent") or {}).get("personalities") or {}
            return name if name in catalog else ""

        def resolve(cfg):
            name = active(cfg)
            if name:
                record = cfg["agent"]["personalities"][name]
                return "\n".join(v for v in (record.get("system_prompt", ""),
                    "Tone: " + record["tone"] if record.get("tone") else "",
                    "Style: " + record["style"] if record.get("style") else "") if v)
            return (cfg.get("agent") or {}).get("system_prompt", "")

        native.normalize_personality_name = normalize
        native.active_personality_name = active
        native.resolve_ephemeral_system_prompt = resolve
        return native

    def resolve(self, cfg):
        with patch.dict(sys.modules, {"hermes_cli.personality": self.stub()}):
            return resolve_distribution_personality(cfg)

    def test_curated_personality_is_resolved(self):
        cfg = {"agent": {"personalities": {"council-parenting-coach": {
            "system_prompt": "Support the parent directly.",
            "tone": "Warm and frank", "style": "Situation first"}}},
            "display": {"personality": "council-parenting-coach"}}
        name, overlay = self.resolve(cfg)
        self.assertEqual(name, "council-parenting-coach")
        self.assertIn("Support the parent directly.", overlay)
        self.assertIn("Tone: Warm and frank", overlay)
        self.assertIn("Style: Situation first", overlay)

    def test_neutral_selection_does_not_activate_curated_overlay(self):
        cfg = {"agent": {"personalities": {"council-parenting-coach": {
            "system_prompt": "Curated text"}}}, "display": {"personality": "none"}}
        self.assertEqual(self.resolve(cfg), ("", ""))

    def test_manual_prompt_remains_when_no_personality_selected(self):
        cfg = {"agent": {"system_prompt": "Manually specified guidance"}, "display": {}}
        self.assertEqual(self.resolve(cfg), ("", "Manually specified guidance"))

    def test_unknown_named_personality_fails_closed(self):
        cfg = {"agent": {"personalities": {}}, "display": {"personality": "made-up"}}
        with self.assertRaisesRegex(RuntimeError, "unknown or unavailable"):
            self.resolve(cfg)

    def test_selected_personality_with_empty_render_fails_closed(self):
        cfg = {"agent": {"personalities": {"empty": {"system_prompt": ""}}},
               "display": {"personality": "empty"}}
        with self.assertRaisesRegex(RuntimeError, "empty overlay"):
            self.resolve(cfg)

    def test_malformed_display_fails_closed(self):
        with self.assertRaisesRegex(RuntimeError, "must be a mapping"):
            self.resolve({"display": ["unexpected"]})


if __name__ == "__main__":
    import unittest
    unittest.main()
