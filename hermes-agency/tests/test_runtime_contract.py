from __future__ import annotations

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import catalog  # noqa: E402


class RuntimeSourceContractTests(unittest.TestCase):
    def test_static_contract_matches_runtime_catalog(self):
        contract = json.loads(
            (ROOT / "runtime-contract.json").read_text(encoding="utf-8")
        )
        self.assertEqual(
            set(contract),
            {
                "schema_version",
                "agency_name",
                "catalog_schema_version",
                "content_digest_schema",
                "agency_manifest",
                "profile_root",
                "profile_path_template",
                "capability_path_template",
            },
        )
        self.assertEqual(contract["schema_version"], 2)
        self.assertEqual(contract["agency_manifest"], "agency.json")
        self.assertEqual(contract["profile_root"], "profiles")
        self.assertEqual(
            contract["capability_path_template"], "profiles/{name}/skills"
        )

        runtime = catalog.build_catalog()
        self.assertEqual(contract["agency_name"], runtime["agency"]["name"])
        self.assertEqual(
            contract["catalog_schema_version"], runtime["schema_version"]
        )
        self.assertEqual(
            contract["content_digest_schema"], runtime["content_digest_schema"]
        )
        self.assertEqual(
            contract["profile_path_template"],
            runtime["distribution"]["profile_path_template"],
        )

        agency = json.loads((ROOT / contract["agency_manifest"]).read_text(encoding="utf-8"))
        self.assertEqual(agency["name"], contract["agency_name"])
        self.assertEqual(
            agency["distribution"]["profile_root"], contract["profile_root"]
        )
        self.assertEqual(
            agency["distribution"]["profile_path_template"],
            contract["profile_path_template"],
        )
        for profile in runtime["profiles"]:
            capability_path = ROOT / contract["capability_path_template"].format(
                name=profile["name"]
            )
            self.assertTrue(capability_path.is_dir())


if __name__ == "__main__":
    unittest.main()
