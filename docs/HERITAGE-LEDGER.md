# Heritage Ledger

Version de travail : Passe 1, `0.1.0-alpha.2`.

Objectif : classer l'existant avant tout import de code dans twinSIIAOS.

## Regles de classement

- `REUSE` : peut etre repris presque tel quel apres verification.
- `ADAPT` : valeur forte mais neutralisation ou reduction necessaire.
- `REFERENCE` : doctrine, methode ou idee a conserver, implementation non retenue.
- `ARCHIVE` : conserve comme historique et preuve de trajectoire.
- `REJECT` : ne doit pas entrer dans le noyau public v1.

## 1. siiaos-building-local-game-v2.1-step1

Classe globale : `ADAPT` avec plusieurs modules candidats `REUSE`.

### Forces

- runtime Go local ;
- `go.mod` sans dependance externe ;
- serveur HTTP local ;
- interface Web statique ;
- 39 routes exposees ;
- modeles existants de capacites, preuves, risques, mesures, trajectoires, mandats, opportunites et twins ;
- scanner, control plane, world model et couche v2 separes en packages ;
- scripts Windows existants ;
- tests et rapports historiques.

### Contaminations identifiees

Au moins 23 fichiers contiennent des faits ou chemins ARAGORN, notamment :

- `config/paths.json` ;
- `services/local-agent/internal/scanner/config.go` ;
- `services/local-agent/internal/control/control.go` ;
- `data/runtime/*` ;
- plusieurs documents d'audit ARAGORN.

`config/paths.json` contient notamment des racines `D:/`, `D:/github`, `D:/Obsidian`, le profil `ARAGORN`, des caracteristiques materiel et une liste de services locaux historiques.

### Decision par composant

| Composant | Classe | Decision |
|---|---|---|
| `services/local-agent/cmd` | ADAPT | Conserver le principe du binaire Go unique. Refaire le bootstrap en etat zero-permission. |
| `internal/server` | ADAPT | Reprendre le serveur local et le service des assets apres reduction des routes. |
| `internal/scanner/types.go` | ADAPT | Banque de types utile. Mapper vers les objets canoniques nouveaux. |
| `internal/scanner/config.go` | REJECT en l'etat | Defaults ARAGORN et observation implicite incompatibles avec First Day. |
| `internal/scanner/scan.go` | ADAPT | Garder les fonctions de decouverte seulement derriere `ObservationRequest + Consent`. |
| `internal/scanner/probe.go` | ADAPT | Probes uniquement cibles et explicitement consentis. |
| `internal/scanner/context_audit.go` | REFERENCE/ADAPT | Logique de synthese utile, mais les faits historiques ne doivent jamais devenir des defaults. |
| `internal/control` | ADAPT | Capacites, risques, preuves et actions sont utiles. Neutraliser les hypotheses locales. |
| `internal/v2` | REFERENCE | Conserver les concepts de model catalog et trajectoire, sans figer le futur noyau dessus. |
| `internal/world` | REFERENCE | Sert de source pour futures integrations monde/Hyperveille, hors chemin critique v1. |
| `apps/web` | REFERENCE | UI historique utile pour inventaire de vues, pas comme First Day final. |
| `config/capability-catalog.json` | ADAPT | Source de vocabulaire et seeds, a requalifier en fixtures generiques. |
| `config/schemas/*` | ADAPT | Reprendre seulement les schemas utiles apres harmonisation avec les contrats v1. |
| `data/runtime/*` | ARCHIVE | Donnees d'instance, interdites dans les fixtures publiques. |
| scripts `one-click` | REFERENCE | Le parcours operatoire est utile, mais pas le build a chaque lancement. |
| binaires fournis | ARCHIVE | Ne pas importer comme source canonique. Reproduire les builds par CI. |

## 2. SIIAOS-BUILDING-V1-DAY1-HARDENED

Classe globale : `REFERENCE`, avec plusieurs morceaux `ADAPT`.

### Forces

- politique read-only/simulation explicite ;
- interdiction d'actions selon mission ;
- admission de ressources CPU/RAM ;
- probes HTTP limitees au loopback ;
- separation planner/policy/discovery/state ;
- threat model ;
- tests de policy/planner/API ;
- Godot traite comme vue et non source de verite.

### Limites

- second control plane Python/FastAPI ;
- dependances lourdes par rapport au noyau Go ;
- risque de double autorite d'execution ;
- implementation non necessaire pour v1 si les contrats sont portes en Go.

### Decision par composant

| Composant | Classe | Decision |
|---|---|---|
| `policy.py` | ADAPT | Porter les invariants dans le noyau Go et les tests. |
| `planner.py` | ADAPT | Reprendre ordre des taches, gates et simulation, pas le runtime Python. |
| provider loopback guard | REUSE conceptuel | Regle a reproduire dans les adapters HTTP. |
| resource admission | ADAPT | Integrer comme contraintes dures du moteur de sommets/actions. |
| `models.py` | REFERENCE | Source de modelisation pour Mission/Task/State. |
| tests | ADAPT | Convertir les scenarios utiles en tests Go/fixtures contractuelles. |
| FastAPI control plane | REJECT pour noyau v1 | Ne pas introduire un second serveur. |
| Godot minimal | ARCHIVE/REFERENCE | Apres v1 ou comme projection optionnelle. |
| scripts PowerShell doctor/smoke | REFERENCE | Reprendre les scenarios de verification dans packaging futur. |

## 3. SIIAOS-KOS-v1.0.1-stabilized

Classe globale : `REFERENCE` forte, avec certains invariants `REUSE conceptuel`.

### Forces

- ADR explicites ;
- formats ouverts ;
- SQLite comme index reconstructible ;
- espaces separes ;
- objets stables ;
- jobs tracables ;
- separation lectures/ecritures pour agents ;
- packaging, doctor, backup, integrite et update documentes.

### Decision

| Element | Classe | Decision |
|---|---|---|
| ADR-001 noyau sans app centrale | REUSE conceptuel | Les interfaces restent des vues. |
| ADR-002 formats ouverts | REUSE conceptuel | Markdown/YAML/JSON/JSONL + SQLite si utile. |
| ADR-003 SQLite index calcule | REUSE conceptuel | Source canonique reconstructible, SQLite non autoritaire. |
| ADR-006 espaces separes | REUSE conceptuel | Devient une exigence du Context/Space. |
| ADR-007 objet SIIAOS | ADAPT | Inspirer les IDs stables et relations. |
| ADR-008 jobs tracables | REUSE conceptuel | Toute action/observation longue doit etre tracable et relancable. |
| ADR-014 outils agents gouvernes | REUSE conceptuel | Lecture/ecriture separees, journalisation obligatoire. |
| ADR-015 packaging stable | REUSE conceptuel | Doctor, backup, update, integrity, release manifest. |
| runtime Python/Jinja/FastAPI | REJECT pour noyau v1 | Eviter le deuxieme runtime. |
| scripts documentaires | REFERENCE | Reprendre les comportements necessaires sans multiplier les outils. |
| donnees de demo/index/report | ARCHIVE | Fixtures nouvelles et neutres uniquement. |

## 4. ARAGORN_SIIAOS_Starter_Kit_v0.1.1

Classe globale : `ARCHIVE/REFERENCE`.

### Forces

- installer ;
- doctor/status ;
- backup/reset ;
- verification d'integrite ;
- workflows de validation humaine ;
- theorie des sommets deja presente dans le corpus.

### Limites bloquantes v1

- Docker Compose obligatoire ;
- Postgres ;
- Graphify ;
- worker Python ;
- API Go separee ;
- Grist ;
- Vault `Corpus_Audubert` avec contenus personnels et doctrinaux historiques.

### Decision

Ne pas importer le kit. Extraire seulement les scenarios operatoires et les idees de doctor, backup, integrite et validation humaine.

## 5. siiaos-codex-convergence-pack

Classe globale : `ARCHIVE/REFERENCE`.

Ce pack est une archive genealogique precieuse des versions V1, V1.1, V1.2, V1.3 et V2. Il sert a comprendre la trajectoire, verifier qu'une fonction n'a pas deja existe et documenter les decisions.

Il ne doit pas etre importe dans le runtime ni distribue avec la v1.

## 6. Synthese de convergence

Le futur noyau v1 doit combiner :

1. **Runtime** : la frugalite et le binaire Go de `v2.1-step1`.
2. **Gouvernance d'execution** : les gates, simulation et guards de Day1-Hardened.
3. **Memoire et exploitation** : les ADR, formats ouverts, journalisation et packaging du KOS.
4. **Experience utilisateur** : le First Day et les Capability Passports de twinSIIAOS.
5. **Non-repetition** : le convergence-pack reste la genealogie consultable.

Il ne doit importer aucun systeme historique en bloc.

## 7. Decisions de non-import avant v1

Sauf preuve nouvelle, ne pas introduire dans le noyau :

- FastAPI ;
- uvicorn ;
- Pydantic ;
- Jinja ;
- Graphify ;
- Postgres ;
- Grist ;
- Docker obligatoire ;
- Godot obligatoire ;
- base graphe externe ;
- service de secrets externe ;
- moteur de policy externe.

Ces briques pourront revenir comme adapters ou projections optionnelles.

## 8. Prochaine action

Construire la matrice `heritage API -> objet canonique` puis les schemas de `Context`, `Need`, `Fact`, `Evidence`, `CapabilityPassport`, `ResponsibilityProfile`, `ObservationRequest`, `Summit`, `PathCandidate` et `ActionPlan`.
