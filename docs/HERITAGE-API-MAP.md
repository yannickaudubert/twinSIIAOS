# Heritage API Map

Passe 1, `0.1.0-alpha.2`.

Ce document cartographie la surface API historique de `siiaos-building-local-game-v2.1-step1` vers le modele twinSIIAOS v1.

## 1. Routes a reprendre directement ou presque

| Route historique | Cible v1 | Decision |
|---|---|---|
| `/api/capabilities` | `CapabilityPassport[]` | ADAPT |
| `/api/proofs` | `Evidence[]` | ADAPT |
| `/api/risks` | `Fact/Risk` | ADAPT |
| `/api/measurements` | `Evidence/Measurement` | ADAPT |
| `/api/state` | `RuntimeState` | ADAPT |
| `/api/events` | `EventJournal` | ADAPT |
| `/api/config` | `RuntimeConfig` | ADAPT, aucun default machine |
| `/api/context-audit` | `Context + Fact[]` | ADAPT fortement |
| `/api/recommendations` | `PathCandidate[]` | REFERENCE, remplacer la logique de recommandation |
| `/api/trajectories` | `PathCandidate / Journey` | ADAPT |
| `/api/mandates` | `ActionPlan / Mandate` | ADAPT |
| `/api/opportunities` | `SummitCandidate` | REFERENCE |
| `/api/twins` | `AdapterObservation` | ADAPT |
| `/api/search` | `LocalSearchAdapter` | REFERENCE, hors noyau minimum |

## 2. Routes a conserver comme compatibilite historique

Ces routes peuvent vivre plus tard dans un adapter `legacy-building-v2`, mais ne doivent pas definir le modele canonique :

- `/api/command` ;
- `/api/building` ;
- `/api/serious-game` ;
- `/api/stacks` ;
- `/api/hybrid-library` ;
- `/api/probabilities` ;
- `/api/v2` ;
- `/api/v2/models` ;
- `/api/v2/examples` ;
- `/api/v2/schemas` ;
- `/api/queue-policy` ;
- `/api/clients` ;
- `/api/teams` ;
- `/api/routines` ;
- `/api/pipelines`.

Decision : `REFERENCE/ADAPTER`, pas de duplication dans le noyau v1.

## 3. Routes interdites en demarrage neutre

Les fonctions suivantes ne doivent jamais etre appelees avant consentement :

- `/api/rescan` ;
- `/api/probe` ;
- `/api/processes` ;
- `/api/schedules` ;
- toute recherche de fichiers ou service non explicitement selectionne.

Le futur runtime doit imposer la gate :

`ObservationRequest -> Consent(granted) -> Adapter -> Fact(observed)`.

## 4. Routes de preparation/execution historiques

- `/api/prepare/hermes` ;
- `/api/prepare/odysseus` ;
- `/api/prepare/codex-obsidian-audit` ;
- `/api/actions` ;
- `/api/control`.

Decision : `REFERENCE` jusqu'a la Passe 5.

Aucune execution historique ne sera importee avant l'existence des objets :

- `ActionPlan` ;
- `Approval` ;
- `Evidence` ;
- `RollbackPlan` ;
- `CorrelationID`.

## 5. Mapping de types historiques

| Type historique | Objet v1 | Commentaire |
|---|---|---|
| `Snapshot` | `RuntimeSnapshot` | Derive de faits consentis seulement. |
| `HostInfo` | `Fact` | Ne jamais devenir une identite permanente. |
| `Service` | `Fact + Resource` | Service observe, puis eventuellement capacite. |
| `Project` | `ContextResource` | Attache a un espace explicite. |
| `Vault` | `ContextResource` | Jamais scanne sans selection. |
| `ToolObservation` | `Fact` | Provenance obligatoire. |
| `MaturityProfile` | `CapabilityMaturity` | Multidimensionnel, jamais score absolu unique. |
| `SuggestedCapability` | `SummitCandidate` | Proposition, pas fait. |
| `SuggestedStack` | `PathCandidate` | Alternative de composition. |
| `Capability` control | `CapabilityPassport` | A enrichir avec humain/gouvernance/preuves. |
| `Risk` | `Risk` | Doit pointer vers faits et preuves. |
| `Proof` | `Evidence` | Renommage canonique. |
| `ActionProposal` | `ActionPlan` | Passage par validation humaine. |
| `Measurements` | `MeasurementEvidence` | Historique, source et unite obligatoires. |
| `Trajectory` | `PathCandidate/Journey` | A separer entre chemin vers sommet et parcours temporel. |
| `Mandate` | `Mandate` | Conserver l'idee de perimetre/droits/duree. |

## 6. Principe de compatibilite

Le noyau v1 ne promet pas la compatibilite binaire avec `v2.1-step1`.

Il promet une compatibilite semantique par adapter :

```text
legacy API / files
      -> legacy adapter read-only
      -> canonical Fact / Evidence / CapabilityPassport
      -> twinSIIAOS v1
```

Cela permet de reutiliser ARAGORN sans faire de son historique le schema universel.
