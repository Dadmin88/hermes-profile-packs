"""Focused safety tests for reviewed, selective profile source synchronization."""
from __future__ import annotations

import json
from pathlib import Path
import stat
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from reviewed_profile_sync import (apply, build, fingerprint, print_diff, rollback,
                                  safe_parts, summary)  # noqa: E402


class ReviewedSyncTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.source = base / "source"
        self.installed = base / "installed"
        self.backups = base / "private-backups"
        self.source.mkdir()
        self.installed.mkdir()
        (self.source / "capabilities").mkdir()
        (self.source / "capabilities/profiles.json").write_text(json.dumps({
            "profiles": [{"profile": "agency-example",
                          "path": "hermes-agency/profiles/agency-example"}]
        }))
        self.upstream = self.source / "hermes-agency/profiles/agency-example"
        self.upstream.mkdir(parents=True)
        (self.upstream / "distribution.yaml").write_text("name: agency-example\nversion: 0.3.0\n")
        (self.upstream / "SOUL.md").write_text("New reviewed upstream role\n")
        skill = self.upstream / "skills/workflow"
        (skill / "references").mkdir(parents=True)
        (skill / "SKILL.md").write_text("---\nname: workflow\ndescription: Reviewed process\n---\nDo steps\n")
        (skill / "references/guide.md").write_text("A new reviewed reference\n")
        self.profile = self.installed / "agency-example"
        (self.profile / "skills/workflow").mkdir(parents=True)
        (self.profile / "distribution.yaml").write_text(
            f"name: agency-example\nversion: 0.1.0\nsource: {self.upstream}\n"
        )
        (self.profile / "SOUL.md").write_text("Important local SOUL addition\n")
        (self.profile / "skills/workflow/SKILL.md").write_text("My locally customized skill\n")
        (self.profile / "skills/my-own").mkdir()
        (self.profile / "skills/my-own/SKILL.md").write_text("Keep this personal skill\n")
        (self.profile / "config.yaml").write_text("model: my-choice\n")

    def test_preview_exposes_conflicts_without_writing(self):
        units, skip = build(self.source, self.installed, "agency-example", [])
        report = summary(units, skip, False)
        self.assertEqual(report["matched_profiles"], 1)
        self.assertEqual(report["units_seen"], 2)
        self.assertEqual(report["files"]["replace"], 2)
        self.assertEqual(report["files"]["add"], 1)
        self.assertEqual((self.profile / "SOUL.md").read_text(),
                         "Important local SOUL addition\n")
        self.assertEqual((self.profile / "skills/my-own/SKILL.md").read_text(),
                         "Keep this personal skill\n")

    def test_explicit_approved_skill_only_sync_and_guarded_rollback(self):
        units, skipped = build(self.source, self.installed, "agency-example",
                               ["skills/workflow"])
        self.assertFalse(skipped)
        approved = fingerprint(units)
        result = apply(units, self.source, self.installed, self.backups, approved)
        self.assertEqual(result["status"], "applied")
        self.assertEqual(result["changed"], 2)
        self.assertEqual((self.profile / "skills/workflow/SKILL.md").read_bytes(),
                         (self.upstream / "skills/workflow/SKILL.md").read_bytes())
        self.assertEqual((self.profile / "skills/workflow/references/guide.md").read_text(),
                         "A new reviewed reference\n")
        self.assertEqual((self.profile / "SOUL.md").read_text(),
                         "Important local SOUL addition\n")
        self.assertEqual((self.profile / "config.yaml").read_text(), "model: my-choice\n")
        self.assertEqual((self.profile / "skills/my-own/SKILL.md").read_text(),
                         "Keep this personal skill\n")
        saved = self.backups / result["backup_id"]
        self.assertEqual(stat.S_IMODE(saved.stat().st_mode), 0o700)
        self.assertEqual(stat.S_IMODE((saved / "0000.bak").stat().st_mode), 0o600)
        restoration = rollback(self.installed, self.backups, result["backup_id"])
        self.assertEqual(restoration["files"], 2)
        self.assertEqual((self.profile / "skills/workflow/SKILL.md").read_text(),
                         "My locally customized skill\n")
        self.assertFalse((self.profile / "skills/workflow/references/guide.md").exists())

    def test_plan_hash_rejects_drift(self):
        units, _ = build(self.source, self.installed, "agency-example",
                         ["skills/workflow"])
        approved = fingerprint(units)
        (self.profile / "skills/workflow/SKILL.md").write_text("changed again\n")
        with self.assertRaisesRegex(ValueError, "changed since approval"):
            apply(units, self.source, self.installed, self.backups, approved)
        self.assertFalse(self.backups.exists())

    def test_rollback_wont_overwrite_later_local_edit(self):
        units, _ = build(self.source, self.installed, "agency-example",
                         ["SOUL.md"])
        result = apply(units, self.source, self.installed, self.backups,
                       fingerprint(units))
        (self.profile / "SOUL.md").write_text("edited after sync\n")
        with self.assertRaisesRegex(ValueError, "destination changed"):
            rollback(self.installed, self.backups, result["backup_id"])
        self.assertEqual((self.profile / "SOUL.md").read_text(), "edited after sync\n")

    def test_reject_symlinked_destination(self):
        original = self.profile / "skills/workflow/SKILL.md"
        original.unlink()
        original.symlink_to(self.profile / "SOUL.md")
        with self.assertRaisesRegex(ValueError, "symlinked"):
            build(self.source, self.installed, "agency-example", ["skills/workflow"])

    def test_unmatched_source_is_skipped_without_mutation(self):
        (self.profile / "distribution.yaml").write_text(
            "name: agency-example\nsource: /some/unrelated/source\n")
        result, skipped = build(self.source, self.installed, None, [])
        self.assertEqual(result, [])
        self.assertEqual(skipped["not_installed_or_unmatched"], 1)
        with self.assertRaisesRegex(ValueError, "source differs"):
            build(self.source, self.installed, "agency-example", ["SOUL.md"])

    def test_invalid_path_cannot_escape_profile(self):
        for name in ("skills/../SOUL.md", "/etc/passwd", "skills/a/../../x",
                     "skills/a", "skills//a/SKILL.md"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                safe_parts(name)


if __name__ == "__main__":
    unittest.main()
