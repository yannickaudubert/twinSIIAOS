import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
TRUTH_SCHEMA = json.loads((ROOT / "contracts" / "truth.schema.json").read_text(encoding="utf-8"))
LINEAGE_SCHEMA = json.loads((ROOT / "contracts" / "source-lineage.schema.json").read_text(encoding="utf-8"))
TRUTH_FIXTURE = json.loads((ROOT / "examples" / "a01" / "truth-record.example.json").read_text(encoding="utf-8"))
LINEAGE_FIXTURE = json.loads((ROOT / "examples" / "a01" / "source-lineage.example.json").read_text(encoding="utf-8"))

truth_validator = Draft202012Validator(TRUTH_SCHEMA, format_checker=FormatChecker())
lineage_validator = Draft202012Validator(LINEAGE_SCHEMA, format_checker=FormatChecker())

class A01TruthLineageTests(unittest.TestCase):
    def assert_valid(self, validator, instance):
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        self.assertEqual([], errors, "\n".join(e.message for e in errors))

    def assert_invalid(self, validator, instance):
        errors = list(validator.iter_errors(instance))
        self.assertTrue(errors, "instance unexpectedly valid")

    def test_positive_truth_fixture(self):
        self.assert_valid(truth_validator, TRUTH_FIXTURE)

    def test_positive_lineage_fixture(self):
        self.assert_valid(lineage_validator, LINEAGE_FIXTURE)

    def test_observed_requires_timestamp_and_ttl(self):
        item = dict(TRUTH_FIXTURE)
        item.pop("observed_at")
        self.assert_invalid(truth_validator, item)

    def test_proven_requires_evidence_and_validated_state(self):
        item = dict(TRUTH_FIXTURE)
        item["truth_status"] = "PROVEN"
        item["evidence_refs"] = []
        item["validation"] = {"status": "checked"}
        self.assert_invalid(truth_validator, item)

    def test_declared_requires_declaration_derivation(self):
        item = dict(TRUTH_FIXTURE)
        item["truth_status"] = "DECLARED"
        item["derivation"] = "inference"
        self.assert_invalid(truth_validator, item)

    def test_proposed_requires_proposal_derivation(self):
        item = dict(TRUTH_FIXTURE)
        item["truth_status"] = "PROPOSED"
        item["derivation"] = "calculation"
        self.assert_invalid(truth_validator, item)

    def test_non_unknown_requires_source(self):
        item = dict(TRUTH_FIXTURE)
        item["source_refs"] = []
        self.assert_invalid(truth_validator, item)

if __name__ == "__main__":
    unittest.main()
