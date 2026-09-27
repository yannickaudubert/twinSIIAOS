import unittest

from validate_handoff import validate_handoff


def route(name):
    human = name in {"yannick_consultant","cabinet_augmente","agoria_collective"}
    return {
        "route": name,
        "mandate": {"required": human, "human_gate": human},
        "context_boundary": {
            "shareable_fields": ["need","public_facts"],
            "local_only_fields": ["estate","client_secrets"]
        }
    }


def pack():
    return {
        "decision_state": {"execution":"feasible","admission":"eligible"},
        "share_policy": {
            "shareable_fields":["need","public_facts"],
            "excluded_fields":["estate","client_secrets"],
            "human_approval_required": True
        }
    }


def mission(name="cabinet_augmente", state="proposed"):
    return {
        "route":name,
        "human_gate":True,
        "state":state
    }


class GovernedHandoffTests(unittest.TestCase):
    def test_73_local_route_cannot_create_mission(self):
        r = validate_handoff(route("siiaos_local"), None, mission())
        self.assertFalse(r["valid"])

    def test_74_no_activation_cannot_create_mission(self):
        r = validate_handoff(route("no_activation"), None, mission())
        self.assertFalse(r["valid"])

    def test_75_human_route_requires_context_pack(self):
        r = validate_handoff(route("cabinet_augmente"))
        self.assertFalse(r["valid"])
        self.assertTrue(any("ContextPack" in e for e in r["errors"]))

    def test_76_valid_human_proposal_with_filtered_context_is_allowed(self):
        r = validate_handoff(route("cabinet_augmente"), pack(), mission())
        self.assertTrue(r["valid"])

    def test_77_agoria_context_share_requires_human_approval(self):
        p = pack()
        p["share_policy"]["human_approval_required"] = False
        r = validate_handoff(route("agoria_collective"), p, mission("agoria_collective"))
        self.assertFalse(r["valid"])

    def test_78_shareable_and_local_only_overlap_is_blocked(self):
        rt = route("cabinet_augmente")
        rt["context_boundary"]["shareable_fields"].append("estate")
        r = validate_handoff(rt, pack(), mission())
        self.assertFalse(r["valid"])

    def test_79_unknown_execution_cannot_be_qualified_handoff(self):
        p = pack()
        p["decision_state"]["execution"] = "unknown"
        r = validate_handoff(route("cabinet_augmente"), p, mission())
        self.assertFalse(r["valid"])

    def test_80_unknown_admission_cannot_be_qualified_handoff(self):
        p = pack()
        p["decision_state"]["admission"] = "unknown"
        r = validate_handoff(route("cabinet_augmente"), p, mission())
        self.assertFalse(r["valid"])

    def test_81_active_mission_cannot_be_created_by_validator(self):
        r = validate_handoff(route("cabinet_augmente"), pack(), mission(state="active"))
        self.assertFalse(r["valid"])

    def test_82_human_route_without_mission_remains_valid_proposal_with_warning(self):
        r = validate_handoff(route("yannick_consultant"), pack(), None)
        self.assertTrue(r["valid"])
        self.assertTrue(r["warnings"])


if __name__ == "__main__":
    unittest.main()
