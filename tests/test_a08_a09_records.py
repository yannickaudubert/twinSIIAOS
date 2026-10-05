import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
A08 = json.loads((ROOT / "contracts" / "evidence-operation-record.schema.json").read_text(encoding="utf-8"))
A09 = json.loads((ROOT / "contracts" / "decision-adr-case.schema.json").read_text(encoding="utf-8"))

a08 = Draft202012Validator(A08, format_checker=FormatChecker())
a09 = Draft202012Validator(A09, format_checker=FormatChecker())

EVIDENCE = {
    "id": "evidence:ev-1",
    "tenant_ref": "tenant:t-1",
    "mission_ref": "mission:m-1",
    "kind": "test_result",
    "claim_refs": ["claim:1"],
    "source_refs": ["source:1"],
    "digest": "a" * 64,
    "captured_at": "2026-10-05T07:00:00Z",
    "captured_by_identity_ref": "identity:human-1",
    "lineage_refs": ["lineage:1"]
}

OPERATION = {
    "id": "operation:op-1",
    "tenant_ref": "tenant:t-1",
    "mission_ref": "mission:m-1",
    "actor_identity_ref": "identity:agent-1",
    "mandate_ref": "mandate:md-1",
    "toolgrant_ref": "toolgrant:tg-1",
    "human_gate_ref": None,
    "action": "validate-contracts",
    "status": "succeeded",
    "started_at": "2026-10-05T07:00:00Z",
    "completed_at": "2026-10-05T07:01:00Z",
    "input_refs": ["record:r-1"],
    "output_refs": ["record:r-2"],
    "evidence_refs": ["evidence:ev-1"],
    "error_code": None
}

DECISION = {
    "id": "decision:d-1",
    "tenant_ref": "tenant:t-1",
    "mission_ref": "mission:m-1",
    "title": "Adopt governed golden journey",
    "status": "approved",
    "decided_by_identity_ref": "identity:human-1",
    "mandate_ref": "mandate:md-1",
    "human_gate_ref": "humangate:hg-1",
    "evidence_refs": ["evidence:ev-1"],
    "rationale": "Reviewed evidence and explicit approval",
    "decided_at": "2026-10-05T07:02:00Z",
    "supersedes_decision_ref": None
}

class A08A09Tests(unittest.TestCase):
    def assert_valid(self, validator, instance):
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        self.assertEqual([], errors, "\n".join(e.message for e in errors))

    def assert_invalid(self, validator, instance):
        self.assertTrue(list(validator.iter_errors(instance)), "instance unexpectedly valid")

    def test_a08_positive(self):
        self.assert_valid(a08, {"evidence": [EVIDENCE], "operations": [OPERATION]})

    def test_successful_operation_requires_evidence(self):
        op = copy.deepcopy(OPERATION)
        op["evidence_refs"] = []
        self.assert_invalid(a08, {"evidence": [EVIDENCE], "operations": [op]})

    def test_a09_positive(self):
        self.assert_valid(a09, {
            "decisions": [DECISION],
            "adrs": [{
                "id": "adr:a-1",
                "tenant_ref": "tenant:t-1",
                "mission_ref": "mission:m-1",
                "title": "Use explicit Front C module registry",
                "status": "accepted",
                "decision_ref": "decision:d-1",
                "context": "UI projections must not become a competing canon.",
                "consequences": ["Modules carry explicit governance metadata."],
                "recorded_at": "2026-10-05T07:03:00Z"
            }],
            "cases": [{
                "id": "case:c-1",
                "tenant_ref": "tenant:t-1",
                "mission_ref": "mission:m-1",
                "title": "First A-B-C integration journey",
                "state": "decided",
                "opened_at": "2026-10-05T06:50:00Z",
                "closed_at": None,
                "evidence_refs": ["evidence:ev-1"],
                "decision_refs": ["decision:d-1"]
            }]
        })

    def test_decision_requires_human_gate_and_evidence(self):
        decision = copy.deepcopy(DECISION)
        decision.pop("human_gate_ref")
        decision["evidence_refs"] = []
        self.assert_invalid(a09, {"decisions": [decision], "adrs": [], "cases": []})

if __name__ == "__main__":
    unittest.main()
