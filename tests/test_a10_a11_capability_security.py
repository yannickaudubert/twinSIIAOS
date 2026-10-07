import copy
import json
from pathlib import Path
import unittest

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
A10 = json.loads((ROOT / "contracts" / "capability-provider-execution.schema.json").read_text(encoding="utf-8"))
A11 = json.loads((ROOT / "contracts" / "security-trust-effect.schema.json").read_text(encoding="utf-8"))

a10 = Draft202012Validator(A10, format_checker=FormatChecker())
a11 = Draft202012Validator(A11, format_checker=FormatChecker())

PROVIDER = {
    "id": "provider:lmstudio-local",
    "name": "Local model runtime",
    "provider_kind": "model_runtime",
    "status": "available",
    "replaceable": True,
    "execution_modes": ["api"],
    "version": "observed-separately",
    "license_ref": None,
    "host_refs": ["host:sandy"],
    "evidence_refs": ["evidence:provider-health"],
    "exit_strategy_ref": "runbook:provider-replacement"
}

CAPABILITY = {
    "id": "capability:reasoning.local",
    "name": "Local reasoning",
    "description": "Governed local reasoning capability.",
    "status": "admitted",
    "maturity": "L3_GOVERNED",
    "required_evidence_level": "runtime",
    "policy_refs": ["policy:local-only-sensitive"],
    "evidence_refs": ["evidence:provider-health"]
}

BINDING = {
    "id": "capability-binding:reasoning-lmstudio",
    "capability_ref": "capability:reasoning.local",
    "provider_ref": "provider:lmstudio-local",
    "status": "active",
    "priority": 10,
    "locality": "local",
    "resource_profile_ref": "resource-profile:sandy-default",
    "policy_refs": ["policy:local-only-sensitive"]
}

EXECUTION = {
    "id": "execution:ex-1",
    "tenant_ref": "tenant:t-1",
    "mission_ref": "mission:m-1",
    "capability_ref": "capability:reasoning.local",
    "binding_ref": "capability-binding:reasoning-lmstudio",
    "actor_identity_ref": "identity:agent-1",
    "mandate_ref": "mandate:md-1",
    "toolgrant_ref": None,
    "human_gate_ref": None,
    "data_class": "CONFIDENTIAL",
    "effect_class": "read",
    "status": "allowed",
    "input_refs": ["context-pack:cp-1"],
    "output_refs": [],
    "evidence_refs": [],
    "created_at": "2026-10-08T00:00:00Z"
}

TRUST = {
    "id": "trust-profile:tp-1",
    "tenant_ref": "tenant:t-1",
    "mission_ref": "mission:m-1",
    "data_class": "CONFIDENTIAL",
    "network_mode": "deny_egress",
    "sandbox_required": True,
    "credential_refs": ["credential-ref:local-runtime"],
    "allowed_endpoint_refs": ["endpoint:loopback-model"],
    "policy_refs": ["policy:local-only-sensitive"]
}

EFFECT = {
    "id": "effect-assessment:ea-1",
    "tenant_ref": "tenant:t-1",
    "mission_ref": "mission:m-1",
    "effect_class": "read",
    "channel": "local",
    "decision": "allow",
    "human_gate_required": False,
    "verification_method": "read-back",
    "idempotency_key": None,
    "compensation_ref": None,
    "human_gate_ref": None,
    "reason_codes": [],
    "evidence_refs": [],
    "evaluated_at": "2026-10-08T00:00:00Z"
}

class A10A11Tests(unittest.TestCase):
    def assert_valid(self, validator, instance):
        errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        self.assertEqual([], errors, "\n".join(e.message for e in errors))

    def assert_invalid(self, validator, instance):
        self.assertTrue(list(validator.iter_errors(instance)), "instance unexpectedly valid")

    def test_a10_positive(self):
        self.assert_valid(a10, {
            "providers": [PROVIDER],
            "capabilities": [CAPABILITY],
            "bindings": [BINDING],
            "execution_envelopes": [EXECUTION]
        })

    def test_l8_capability_requires_evidence(self):
        capability = copy.deepcopy(CAPABILITY)
        capability["maturity"] = "L8_PRODUCTION"
        capability["evidence_refs"] = []
        self.assert_invalid(a10, {
            "providers": [PROVIDER],
            "capabilities": [capability],
            "bindings": [BINDING],
            "execution_envelopes": []
        })

    def test_irreversible_execution_requires_human_gate(self):
        execution = copy.deepcopy(EXECUTION)
        execution["effect_class"] = "irreversible"
        execution["status"] = "waiting_human"
        self.assert_invalid(a10, {
            "providers": [PROVIDER],
            "capabilities": [CAPABILITY],
            "bindings": [BINDING],
            "execution_envelopes": [execution]
        })
        execution["human_gate_ref"] = "humangate:hg-1"
        self.assert_valid(a10, {
            "providers": [PROVIDER],
            "capabilities": [CAPABILITY],
            "bindings": [BINDING],
            "execution_envelopes": [execution]
        })

    def test_sensitive_trust_profile_denies_egress(self):
        self.assert_valid(a11, {"trust_profiles": [TRUST], "effect_assessments": [EFFECT]})
        trust = copy.deepcopy(TRUST)
        trust["network_mode"] = "remote_allowed"
        self.assert_invalid(a11, {"trust_profiles": [trust], "effect_assessments": [EFFECT]})

    def test_compensable_external_effect_requires_idempotency_and_compensation(self):
        effect = copy.deepcopy(EFFECT)
        effect["effect_class"] = "external_compensable"
        effect["channel"] = "remote"
        self.assert_invalid(a11, {"trust_profiles": [], "effect_assessments": [effect]})
        effect["idempotency_key"] = "mission:m-1:publish:1"
        effect["compensation_ref"] = "runbook:revoke-publication"
        self.assert_valid(a11, {"trust_profiles": [], "effect_assessments": [effect]})

    def test_irreversible_effect_requires_human_gate(self):
        effect = copy.deepcopy(EFFECT)
        effect["effect_class"] = "irreversible"
        effect["decision"] = "allow"
        self.assert_invalid(a11, {"trust_profiles": [], "effect_assessments": [effect]})
        effect["decision"] = "require_human_gate"
        effect["human_gate_required"] = True
        effect["human_gate_ref"] = "humangate:hg-1"
        self.assert_valid(a11, {"trust_profiles": [], "effect_assessments": [effect]})

if __name__ == "__main__":
    unittest.main()
