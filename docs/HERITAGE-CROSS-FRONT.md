# Cross-front heritage ledger

Status: ACTIVE CONVERGENCE LEDGER
Updated: 2026-10-05

Purpose: preserve useful historical work while preventing a second canon during Front A/B/C convergence.

| Asset | Historical location | Decision | Reason / migration |
|---|---|---|---|
| Mission Factory | YanIA PR #3 | KEEP + ADAPT | Preserve NeedSpec, ContextPack, Mission and route/store behavior. Rebind authority/evidence semantics to Front A ABI instead of its historical local types. |
| Mission lifecycle state machine | YanIA PR #6 | KEEP | Draft→qualified→planned→dry_run→waiting_gate→ready→running→verifying→succeeded/failed→retex remains useful. Gate semantics must reference canonical HumanGate/Decision records. |
| Historical OperationRecord | YanIA PR #3 | ADAPT | Preserve append-only execution history and evidence refs. Replace org/actor/operator shortcuts with explicit tenant, mission, actor identity, mandate/toolgrant/humangate refs from A08. |
| Historical Knowledge Admission | YanIA PR #6 | KEEP + ADAPT | Preserve quarantine/review rules, source/provenance requirements and contradiction blocking. Canon admission remains a HumanGate + Decision/Record event, never an automatic memory write. |
| Pre-machine Golden Mission | YanIA PR #6 | KEEP AS TEST | Preserve adversarial verification, unknown resource fit, remote denial and gate behavior. It is an integration/regression proof, not the definition of the canon. |
| Front B Golden Business Journey | YanIA PR #7 | KEEP + ADAPT | Preserve discovery→pre-audit→twin→methods→governance→epistemic→knowledge/radar→deliverable→impact. Outputs remain derived until admitted through Front A. |
| YanIA packages/contracts research EvidenceItem | YanIA main / PR #3 | KEEP AS COMPATIBILITY | Useful for research UI citation grouping, but it is not A08 Evidence. Rename/qualify at boundaries and never promote it as canonical evidence. |
| Front B local HumanGate | YanIA PR #7 | RETIRE AS CANON | Keep only as temporary compatibility input. Canonical human approval is A05 HumanGate with principal/tenant/mission/digest/evidence. |
| Front C module registry | YanIA PR #10 | KEEP | UI modules remain projections. Decision Room must consume canonical mandate/gate/evidence read models. |
| Legacy YanIA final-state ADR | YanIA ADR-0001 | SUPERSEDED | Provider stack remains reusable, but no provider or packages/contracts package is canonical authority. |

## Canonical migration spine

`NeedSpec -> ContextPack -> Mission -> compiled Team -> Action -> A08 OperationRecord/Evidence -> A05 HumanGate when required -> A09 Decision/Record -> Deliverable -> RETEX`

## Non-negotiable

Historical code can be reused without inheriting historical authority assumptions.

Any future import from the stacked SandY PR lineage (#2/#3/#4/#6) must be classified here before being promoted into a current Front branch.
