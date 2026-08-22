from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENCY = json.loads((ROOT / "agency.json").read_text(encoding="utf-8"))


def _yaml_scalar(value: str) -> str:
    value = value.strip()
    if value.startswith('"'):
        parsed = json.loads(value)
        if not isinstance(parsed, str):
            raise ValueError("manifest scalar must be a string")
        return parsed
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1].replace("''", "'")
    return value


def _manifest_identity(path: Path) -> dict[str, str]:
    wanted = {"name", "version"}
    result: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line or raw_line[0].isspace() or ":" not in raw_line:
            continue
        key, value = raw_line.split(":", 1)
        if key in wanted:
            result[key] = _yaml_scalar(value)
    return result


class DistributionIdentityTests(unittest.TestCase):
    def test_every_profile_distribution_matches_agency_release_identity(self):
        agency_version = AGENCY["version"]
        profile_root = ROOT / AGENCY["distribution"]["profile_root"]
        for profile in AGENCY["profiles"]:
            name = profile["name"]
            manifest_path = profile_root / name / "distribution.yaml"
            with self.subTest(profile=name):
                manifest = _manifest_identity(manifest_path)
                self.assertEqual(manifest.get("name"), name)
                self.assertEqual(manifest.get("version"), agency_version)

    def test_routing_contract_uses_stable_profile_identity(self):
        distribution = AGENCY["distribution"]
        routing = AGENCY["routing"]
        self.assertEqual(distribution["format"], "hermes-profile-distribution")
        self.assertEqual(distribution["profile_identity_field"], "name")
        self.assertEqual(distribution["profile_path_template"], "profiles/{name}")
        self.assertEqual(routing["selection_order"], ["professional-profile", "eligible-node"])
        self.assertEqual(routing["live_presence_owner"], "hermes-fleet")
        self.assertEqual(routing["missing_presence_behavior"], "fleet-locate-or-place")


if __name__ == "__main__":
    unittest.main()
