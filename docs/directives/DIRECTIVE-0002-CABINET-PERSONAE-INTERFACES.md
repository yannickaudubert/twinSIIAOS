# DIRECTIVE-0002 — Cabinet personae and interface contract

Status: ACTIVE
Purpose: ensure SIIAOS interfaces support real augmented-cabinet work rather than decorating technical subsystems.

## 1. Stable operational roles

The cabinet may compile specialist personae, but the stable operational roles remain:

- Observer — establishes what is actually known or unknown;
- Integrator — connects existing capabilities without creating a second authority;
- Producer — creates a bounded deliverable or action result;
- Contradictor — attacks assumptions, missing evidence and hidden coupling;
- Reviewer — checks quality, fitness and consistency;
- Guardian — checks authority, privacy, security and reversibility;
- Archivist — preserves provenance, decisions, supersession and validity;
- Coordinator — compiles the temporary team around the mission.

Specialist lenses such as Cartographe, Juriste, Stratège, Gouverneur de Réversibilité, Ingénieur Frontières, Gardien Identités/Rôles, Détecteur de Signaux Faibles, Tisseur Territorial, Pédagogue, Chef de Partition and Forgeron Modules map onto these operational roles. They are reusable expertise profiles, not sovereign agents.

## 2. Required mission envelope

Every persona/role must receive a bounded mission envelope containing at least:

- tenant and mission identity;
- need and expected result;
- ContextPack with permitted sources;
- known unknowns;
- applicable policy and mandate references;
- allowed capabilities/tools;
- forbidden actions;
- evidence expectations;
- reviewer / HumanGate rule;
- output destination and retention rule.

A persona without this envelope is advisory only.

## 3. Common output contract

Each substantial agentic output should expose, directly or through linked records:

- context;
- sources/provenance;
- assumptions and unknowns;
- analysis or transformation performed;
- risks and contradictions;
- proposed result;
- evidence;
- human validation state when required;
- reversibility / rollback;
- validity or review horizon.

## 4. Interface obligations

### Hall
Must orient a human toward needs, missions and capabilities. It must not expose internal technical complexity as the primary mental model.

### Mission Workbench
Must show mission context, current state, unknowns, team/roles, evidence, pending gates, outputs and next governed action.

### Research Studio
Must separate source, claim, evidence, inference and contradiction. It must preserve unknowns instead of forcing an answer.

### Decision Room
Must show mandate, alternatives, supporting and contradicting evidence, consequences, decision digest and HumanGate. It is the preferred surface for irreversible or externally committing choices.

### Deliverable Studio
Must distinguish draft, reviewed output and immutable record. A polished document is not automatically an approved record.

### Client Room
Must be a filtered projection of explicitly admitted objects. It must never expose a complete private vault or another tenant's context.

### Building / City
May help humans understand teams, capabilities and flows. It must remain a reconstructible projection and never become the source of authority.

## 5. Persona review gates for an interface

Before an interface is accepted:

- Cartographer/Observer: can I see what exists, what is inferred and what is missing?
- Archivist: can I recover provenance, version, decision and supersession?
- Jurist/Guardian: can I see authority, purpose, tenant and sensitive-data boundaries?
- Reversibility Governor: can I identify rollback, stop and exit paths?
- Boundary Engineer/Integrator: is the interface coupled to one provider or can it consume contracts?
- Contradictor: can the interface represent disagreement and UNKNOWN?
- Reviewer: is there a visible acceptance criterion and evidence?
- Pedagogue: can a non-technical user understand the consequence of the next action?
- Producer/Forger: can the user actually finish a useful mission without dropping to an unrelated tool?
- Coordinator/Chef de Partition: can temporary roles be composed without creating permanent autonomous staff?

An interface that fails one of these questions must either close the gap or explicitly declare the limitation.
