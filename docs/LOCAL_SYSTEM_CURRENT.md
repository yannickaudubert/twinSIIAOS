# État courant du SIIAOS local

**Version documentaire : 2026-09-26**  
**Statut : convergence documentaire**  
**Portée : SandY, ARAGORN, YanIA, twinSIIAOS, runtime local, capacités, mémoire, agents, preuves et reprise**  
**Règle : ce document ne constitue pas une preuve runtime.**

## 1. Hiérarchie documentaire

La hiérarchie active est :

1. mandat humain explicite ;
2. décisions et policies validées ;
3. preuves machine datées ;
4. contrats canoniques SIIAOS ;
5. état des dépôts et artefacts ;
6. projections, interfaces et index ;
7. déclarations historiques et conversations ;
8. modèles et fournisseurs.

Les deux documents de base restent :

- `docs/SIIAOS_PUZZLE.md` ;
- `docs/BRICK_INTEGRATION_CONTRACT.md`.

Les documents historiques sont des sources de capitalisation. Ils ne prennent pas automatiquement le pas sur les décisions et preuves plus récentes.

## 2. Topologie cible actuellement retenue

- **SandY** : nœud local principal IA / SI / compute.
- **ARAGORN** : nœud secondaire, complément, canary et rollback.
- **Redmi** : terminal / surface d'accès.
- **Galaxy / Galaxy Book** : rôle non figé tant qu'il n'est pas décidé et prouvé.
- **GitHub** : forge et CI.
- **Vercel** : surface de démonstration Web ; ne constitue ni le canon ni le runtime local.

Les anciennes topologies où ARAGORN est présenté comme hub principal ou où Forgejo est la forge active doivent être considérées comme historiques jusqu'à preuve contraire.

## 2.1. Registre de supersession topologique

Des décisions contradictoires ont existé dans les échanges de septembre. Elles doivent être conservées comme historique, pas comme vérités concurrentes.

- 22 septembre : plusieurs échanges avaient repositionné ARAGORN comme canon/hub et SandY comme compute distant.
- 23 septembre : la topologie a été reconsolidée avec SandY comme nœud principal local et ARAGORN comme second nœud.
- 25 septembre : cette topologie a été confirmée comme canon courant : **SandY principal ; ARAGORN secondaire/recovery/canary/rollback**.

La règle active est donc la topologie du 25 septembre. Toute instruction antérieure qui inverse ces rôles est `SUPERSEDED`.

## 3. Vérité d'implémentation

Toujours distinguer deux axes.

### Axe A — cycle d'implémentation

`PROPOSÉ -> CODÉ -> TESTÉ -> DÉPLOYÉ -> OBSERVÉ -> PROUVÉ`

### Axe B — qualité de la source

`PROUVÉ / OBSERVÉ / DÉCLARÉ / PROPOSÉ / ÉCHOUÉ / INCONNU`

Ces axes ne doivent plus être mélangés. Un composant peut par exemple être `TESTÉ` dans GitHub mais `INCONNU` sur SandY.

## 4. État GitHub vérifié

### twinSIIAOS

- PR #9 `docs: establish canonical SIIAOS puzzle and brick contract` : **ouverte, draft, non mergée**.
- Elle contient le puzzle canonique, le contrat documentaire de brique et les frontières Radar.
- Issue #8 `SANDY-LOCAL-001` : backlog de convergence local.
- Issue #2 : gate licence, attribution et redistribution toujours ouverte.

### YanIA

- PR #2 `SandY local-only operational baseline` : **ouverte, draft** ; introduit le profil local-only, le preflight et le refus du cloud pour les classes sensibles. Le head historique de cette PR a une CI en échec.
- PR #3 `SandY governed Mission Factory slice` : **ouverte, draft** ; implémente la tranche `NeedSpec -> ContextPack -> Mission -> Team -> OperationRecord -> Evidence -> HumanGate -> Resume`. CI du head : succès.
- PR #4 `close SandY truth-gate gaps` : **ouverte, draft** ; corrige les truth gates et valide lint/tests/build exact head ainsi que les tests de policy du model-router. CI : succès.
- PR #5 : documentation d'intégration SIIAOS uniquement ; CI observée en échec pendant `setup-node`, sans preuve que le contenu documentaire soit fautif.

Aucune de ces PR ouvertes ne doit être assimilée à un déploiement sur SandY.

## 5. Capacités déjà documentées ou codées

### Cœur de mission

Déjà documenté et, dans YanIA PR #3, partiellement codé :

`NeedSpec -> ContextPack -> Mission -> Team -> OperationRecord -> Evidence -> HumanGate -> Resume`

La projection `/resume` est explicitement en lecture seule : elle ne constitue pas encore un moteur d'exécution durable.

### Local-only

Déjà documenté et codé dans la branche YanIA concernée :

- classes `public / internal / confidential / restricted` ;
- refus d'un endpoint distant pour les données sensibles ;
- cloud fallback désactivé par défaut ;
- endpoint LM Studio local comme fournisseur immédiat ;
- preflight SandY destiné à produire une preuve machine.

La preuve machine actuelle reste à régénérer localement.

### Knowledge / graph

YanIA contient déjà une Knowledge Layer relationnelle : notes, versions, liens, backlinks, nœuds/edges de graphe, canvas, indexation et recherche. Le graphe reste une projection reconstruisible et non une autorité.

Graphiti, Neo4j, Qdrant, LCM ou un autre moteur peuvent fournir des capacités, mais aucune de ces technologies ne devient le canon par son seul branchement.

### Capability Registry

YanIA expose déjà un Capability Registry natif. Le besoin restant n'est pas de créer un nouveau catalogue, mais de fermer le contrat `Capability -> Provider -> Resource -> Policy -> Evidence`.

### MCP / outils locaux

Le tutoriel SandY v0.4.0 documente un chemin où :

- LM Studio est découvert localement ;
- les modèles sont inventoriés ;
- `mcp.json` est lu de manière expurgée ;
- un MCP n'est exécuté qu'après mission et validation humaine ;
- la liste des outils autorisés est explicitement bornée pour l'appel.

Ce document est une preuve documentaire d'un câblage antérieur ; l'état actuel doit être réobservé sur SandY.

### Agents / Hermes

Hermes est traité comme un opérateur / fournisseur de capacité agentique remplaçable. Les profils, skills, MCP, sous-agents, budgets, STOP et preuves ont déjà été largement décrits. La version réellement installée, les capacités réellement actives et les bindings actuels restent à inventorier avant promotion.

## 5.1. Non-objectifs de la reprise locale

La phase de finalisation ne doit pas introduire par défaut :

- un nouvel orchestrateur ;
- Kubernetes ;
- un dixième Atlas ;
- un nouveau canon ;
- un nouveau dépôt d'autorité ;
- une nouvelle mémoire globale ;
- une nouvelle couche logicielle portant le nom d'une machine.

Toute nouvelle brique reste `DISCOVERY/LAB` tant qu'elle ne résout pas un besoin non couvert et ne passe pas la chaîne d'admission.

## 6. Ce qui ne doit plus être redéfini

Les cadres suivants sont suffisamment stabilisés pour guider la conception locale :

- primauté humaine ;
- local-first / fail-closed ;
- modèle remplaçable ;
- `Identity != Role != Authority` ;
- mission-bound rights ;
- HumanGate ;
- séparation Producteur / Reviewer / Guardian ;
- STOP persistant ;
- `DesiredState != ObservedState` ;
- interfaces comme projections ;
- séparation Source / Index / Embedding / Graphe / RAG / Synthèse / Décision ;
- isolation tenant / client ;
- provenance et Evidence ;
- rollback avant mutation ;
- admission d'une brique par preuve, licence et capacité ;
- Radar / Hyperveille comme chaîne d'admission, pas comme canon ;
- SandY principal, ARAGORN secondaire.

## 7. Ce qui reste à fermer avant reprise d'exécution

Les sujets suivants ne demandent pas une nouvelle architecture générale ; ils demandent une décision, un contrat plus précis ou une preuve locale :

1. autorité de stockage : ancien choix SQLite versus PostgreSQL déjà utilisé par YanIA ;
2. mapping exécutable `Identity / Authority / Mandate / Policy / ToolGrant` ;
3. moteur durable de mission : queue, checkpoint, idempotence, retry, reprise et état après reboot ;
4. contrat commun Capability / Provider / Resource / Model / Tool ;
5. contrat mémoire et contexte unifié, avec rôle exact des projections Graphiti/Neo4j/Qdrant/LCM ;
6. coffre de secrets et cycle de credentials ;
7. matrice réseau, ports, egress, LAN et surfaces exposées ;
8. preuve automatique de non-egress ;
9. backup / restore / rollback par brique et test de restauration ;
10. corrélation Audit / OperationRecord / Evidence / OpenTelemetry ;
11. contrat générique MCP / browser / computer-use et sandbox ;
12. gate licence/SBOM/redistribution ;
13. paramètres runtime exacts de SandY et modèles effectivement disponibles ;
14. tests Golden Journey réellement exécutables ;
15. refus de tout downgrade silencieux de classification (par exemple `CONFIDENTIAL -> INTERNAL`) ;
16. preuve qu'un STOP bloque également les exports/actions externes ;
17. protection des collecteurs/preflights contre l'évasion via symlink/junction/reparse point ;
18. Cognitive ABI / ResultEnvelope commun lorsque plusieurs engines cognitifs deviennent mobilisables.

## 8. Principe de reprise

La reprise ne part pas d'une nouvelle architecture.

Elle part de :

`documentation canonique -> Truth Pack SandY -> écarts -> paramètres -> bindings -> Golden Mission -> restart -> preuve -> promotion`

Tant que le Truth Pack machine n'est pas frais, tout paramètre de runtime reste `INCONNU` ou `DÉCLARÉ`.

## 9. Sources à conserver comme patrimoine daté

À exploiter sans les traiter comme instructions courantes par défaut :

- `SIIAOS_CONVERGENCE_ET_PASSAGE_ASTRA_2026-09-16.md` ;
- Visual Operating Pack du 23 septembre 2026 ;
- `TUTORIEL-SANDY-v0.4.0.md` ;
- dossiers de conception mémoire / MultiVault / TraceOps ;
- dossiers Hermes / profils agents ;
- handoffs et matrices d'héritage d'août 2026.

Leur contenu utile doit être repris dans les contrats actifs ; leurs choix remplacés doivent être marqués obsolètes plutôt que maintenus en concurrence.
