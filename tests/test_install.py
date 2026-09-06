from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("profile_installer", ROOT / "install.py")
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def make_repo(self, root: Path) -> None:
        packs = {
            "schema_version": 1,
            "packs": [
                {
                    "name": "hermes-agency",
                    "path": "hermes-agency",
                    "namespace": "agency-*",
                    "manifest": "hermes-agency/agency.json",
                    "purpose": "Professional work.",
                },
                {
                    "name": "hermes-council",
                    "path": "hermes-council",
                    "namespace": "council-*",
                    "manifest": "hermes-council/council.json",
                    "purpose": "Personal support.",
                },
                {
                    "name": "hermes-academy",
                    "path": "hermes-academy",
                    "namespace": "academy-*",
                    "manifest": "hermes-academy/academy.json",
                    "purpose": "Teaching.",
                },
            ],
        }
        (root / "packs.json").write_text(json.dumps(packs), encoding="utf-8")
        manifests = {
            "agency": {
                "name": "hermes-agency",
                "version": "1",
                "orchestrator": "agency-orchestrator",
                "backbone_profiles": ["agency-backend-engineer", "agency-orchestrator"],
                "profiles": [
                    {
                        "name": "agency-orchestrator",
                        "display_name": "Agency Orchestrator",
                        "category": "leadership",
                    },
                    {
                        "name": "agency-backend-engineer",
                        "display_name": "Backend Engineer",
                        "category": "engineering",
                    },
                    {
                        "name": "agency-frontend-engineer",
                        "display_name": "Frontend Engineer",
                        "category": "engineering",
                    },
                    {
                        "name": "agency-security-engineer",
                        "display_name": "Security Engineer",
                        "category": "engineering",
                    },
                ],
            },
            "council": {
                "name": "hermes-council",
                "version": "1",
                "orchestrator": "council-steward",
                "profiles": [
                    {
                        "name": "council-steward",
                        "display_name": "Council Steward",
                        "category": "coordination",
                        "description": "Routes personal requests.",
                    },
                    {
                        "name": "council-fitness-coach",
                        "display_name": "Fitness Coach",
                        "category": "body",
                        "description": "Plans sustainable workouts and recovery.",
                    },
                    {
                        "name": "council-finance-coach",
                        "display_name": "Finance Coach",
                        "category": "stewardship",
                        "description": "Budget and personal finance planning.",
                    },
                ],
            },
            "academy": {
                "name": "hermes-academy",
                "version": "1",
                "orchestrator": "academy-dean",
                "profiles": [
                    {
                        "name": "academy-dean",
                        "display_name": "Academy Dean",
                        "category": "coordination",
                        "role": "Routes learners.",
                    },
                    {
                        "name": "academy-cybersecurity-instructor",
                        "display_name": "Cybersecurity Instructor",
                        "category": "technology",
                        "role": "Teaches defensive cybersecurity and threat modeling.",
                        "jobs": ["security-concept-lesson"],
                    },
                    {
                        "name": "academy-project-management-instructor",
                        "display_name": "Project Management Instructor",
                        "category": "professional",
                        "role": "Teaches project planning and management.",
                    },
                ],
            },
        }
        for key, manifest in manifests.items():
            pack_dir = root / f"hermes-{key}"
            (pack_dir / "profiles").mkdir(parents=True)
            (pack_dir / f"{key}.json").write_text(json.dumps(manifest), encoding="utf-8")
            (pack_dir / "install.py").write_text("print('ok')\n", encoding="utf-8")
            for profile in manifest["profiles"]:
                profile_dir = pack_dir / "profiles" / profile["name"]
                profile_dir.mkdir()
                description = (
                    profile.get("description")
                    or profile.get("role")
                    or f"{profile['display_name']} profile"
                )
                (profile_dir / "distribution.yaml").write_text(
                    f'name: {profile["name"]}\ndescription: "{description}"\n',
                    encoding="utf-8",
                )
                (profile_dir / "SOUL.md").write_text("test\n", encoding="utf-8")

    def test_catalog_uses_manifests_and_distribution_descriptions(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            packs, profiles = installer.load_catalog(root)
            self.assertEqual(set(packs), {"agency", "council", "academy"})
            backend = next(p for p in profiles if p.name == "agency-backend-engineer")
            self.assertEqual(backend.description, "Backend Engineer profile")
            self.assertGreater(backend.source_bytes, 0)

    def test_recommendation_prefers_academy_when_user_wants_to_learn_security(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            _, profiles = installer.load_catalog(root)
            ranked = installer.recommend_profiles(profiles, "learn cybersecurity", limit=3)
            self.assertEqual(ranked[0][0].name, "academy-cybersecurity-instructor")

    def test_recommendation_prefers_agency_for_building_web_software(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            _, profiles = installer.load_catalog(root)
            ranked = installer.recommend_profiles(profiles, "build a web app", limit=4)
            self.assertTrue(ranked)
            self.assertEqual(ranked[0][0].pack, "agency")
            self.assertIn(
                ranked[0][0].name,
                {"agency-backend-engineer", "agency-frontend-engineer"},
            )

    def test_reverse_engineer_routing_cases_recommend_expected_owner_via_cli(self):
        routing = json.loads(
            (ROOT / "hermes-agency" / "evals" / "routing.json").read_text(
                encoding="utf-8"
            )
        )
        cases = {
            case["id"]: case
            for case in routing["cases"]
            if case["id"].startswith("reverse-engineer-")
        }
        expected_ids = {
            "reverse-engineer-ownership",
            "reverse-engineer-red-team-boundary",
            "reverse-engineer-security-review-boundary",
            "reverse-engineer-integration-boundary",
            "reverse-engineer-mobile-boundary",
            "reverse-engineer-security-operations-boundary",
        }
        self.assertEqual(set(cases), expected_ids)

        for case_id in sorted(expected_ids):
            case = cases[case_id]
            with self.subTest(case=case_id):
                result = subprocess.run(
                    [
                        sys.executable,
                        str(ROOT / "install.py"),
                        "--pack",
                        "agency",
                        "--recommend",
                        case["task"],
                        "--limit",
                        "1",
                        "--json",
                    ],
                    cwd=ROOT,
                    text=True,
                    capture_output=True,
                    check=False,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(
                    payload["recommendations"][0]["name"],
                    case["expected_profile"],
                )

    def test_category_selection_is_exact_and_sparse(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            _, profiles = installer.load_catalog(root)
            selected = installer.resolve_selection(
                profiles,
                explicit_names=None,
                category_specs=["council:body"],
                select_all=False,
                pack_filter=None,
            )
            self.assertEqual([p.name for p in selected], ["council-fitness-coach"])

    def test_explicit_selection_deduplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.make_repo(root)
            _, profiles = installer.load_catalog(root)
            selected = installer.resolve_selection(
                profiles,
                explicit_names=["agency-backend-engineer,agency-backend-engineer"],
                category_specs=None,
                select_all=False,
                pack_filter=None,
            )
            self.assertEqual([p.name for p in selected], ["agency-backend-engineer"])

    def test_index_parser_supports_ranges(self):
        self.assertEqual(installer._parse_indices("1,3-4", 5), [0, 2, 3])
        self.assertEqual(installer._parse_indices("", 3, blank_means_all=True), [0, 1, 2])

    def test_agent_help_documents_safe_two_step_flow(self):
        payload = installer.agent_help_payload()
        self.assertIn("--recommend", payload["recommend"])
        self.assertIn("--dry-run", payload["dry_run"])
        self.assertIn("--yes", payload["install_profiles"])


if __name__ == "__main__":
    unittest.main()
