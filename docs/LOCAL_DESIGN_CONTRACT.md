# Contrat de conception locale SIIAOS

**Version : 2026-09-26**  
**Statut : cadre de conception à appliquer aux reprises locales**  
**Autorité : aucun composant logiciel par défaut**

## 1. Objectif

Ce contrat évite de redéfinir l'architecture au moment de chaque reprise. Il fixe les invariants et les contrats nécessaires pour concevoir, brancher, tester et promouvoir les capacités locales du SIIAOS.

Il s'applique aux modèles, runtimes, agents, MCP, services, bases, graphes, mémoires, interfaces, workers, connecteurs et composants d'observabilité.

## 2. Principe directeur

Une brique n'est jamais intégrée parce qu'elle existe.

La chaîne minimale est :

`Need -> CapabilityRequirement -> ProviderCandidate -> ResourceFit -> Policy -> Experiment -> Evidence -> Admission -> Binding -> Observation`

Toute intégration doit rester remplaçable derrière un contrat de capacité.

## 3. Objets minimaux à fermer

### 3.1 Identity

Représente un humain, service, agent ou système identifiable.

Champs minimaux :

- `identity_id`
- `identity_kind`
- `tenant_id`
- `status`
- références d'authentification
- provenance

### 3.2 Role

Décrit une fonction ou un rôle opérationnel. Un rôle ne donne pas automatiquement une autorité.

### 3.3 Authority

Décrit les droits effectifs d'un acteur dans un périmètre.

Champs minimaux :

- principal
- tenant
- mission
- scope
- capabilities autorisées
- données autorisées
- durée / expiration
- provenance de la décision

### 3.4 Mandate

Décrit pourquoi une mission ou une action peut être exécutée.

Minimum :

- demandeur ;
- finalité ;
- périmètre ;
- résultat attendu ;
- non-objectifs ;
- classe de données ;
- contraintes ;
- budget ;
- décideur humain ;
- date d'expiration ;
- règles de publication.

### 3.5 PolicyDecision

Chaque action significative doit pouvoir relier la décision de politique qui l'autorise ou la refuse.

### 3.6 ToolGrant

Un agent ou modèle n'obtient jamais un outil entier par défaut.

Un ToolGrant lie :

- mission ;
- actor/agent ;
- capability ;
- outil/provider ;
- opérations permises ;
- données permises ;
- durée ;
- budget ;
- egress ;
- HumanGate requis ;
- condition de révocation.

## 4. Contrat Capability

Une capability décrit un résultat maîtrisé, pas une marque.

Exemples :

- `model.infer`
- `knowledge.search`
- `document.ingest`
- `document.render`
- `repo.inspect`
- `container.inspect`
- `browser.navigate`
- `computer.interact`
- `workflow.run`
- `mcp.call`
- `evidence.verify`

Chaque capability doit pouvoir référencer :

- version du contrat ;
- I/O ;
- classification de données admissible ;
- risque ;
- preuve attendue ;
- coût / budget ;
- latence / performance ;
- sandbox ;
- observabilité ;
- fallback ;
- alternative.

## 5. Contrat Provider

Un provider est un fournisseur remplaçable d'une ou plusieurs capabilities.

Exemples possibles : LM Studio, Ollama, Hermes, Docker, Git, Graphiti, Qdrant, Neo4j, un MCP, une API métier.

Minimum :

- `provider_id`
- `provider_kind`
- version exacte
- host/node
- endpoint ou mécanisme d'accès
- licence
- healthcheck
- capabilities fournies
- data classes autorisées
- dependencies
- secrets refs
- modes de fallback
- backup / restore
- rollback
- preuves de qualification.

Aucun provider n'est source de vérité par défaut.

## 6. Contrat Resource

Le ResourceContract décrit ce qu'une exécution peut consommer.

Minimum :

- node ;
- CPU ;
- RAM ;
- GPU/VRAM ;
- disque ;
- réseau ;
- concurrence ;
- temps maximum ;
- budget ;
- quotas ;
- capacité de spill/cache ;
- contraintes thermiques ou d'alimentation si pertinentes.

Le Resource Steward peut recommander un placement, mais ne modifie pas une policy.

## 7. Routage modèle

Le model-router ne choisit pas seulement un nom de modèle.

Critères de routage :

1. classe de données ;
2. capability demandée ;
3. modality ;
4. qualité observée ;
5. contexte nécessaire ;
6. VRAM/RAM disponible ;
7. latence ;
8. concurrence ;
9. coût ;
10. licence ;
11. risque ;
12. preuve de compatibilité ;
13. disponibilité locale ;
14. fallback autorisé.

Règle fail-closed :

- `CONFIDENTIAL` : local par défaut ;
- `RESTRICTED` : local uniquement ;
- aucune dégradation silencieuse vers un provider distant.

Le modèle actif est découvert au runtime. Aucun nom historique de modèle ne doit devenir une constante canonique.

## 8. Mémoire et contexte

### 8.1 Séparation obligatoire

`Source != SourceRecord != KnowledgeObject != Index != Embedding != Graph != RAG != Summary != CanonicalDecision`

### 8.2 ContextPack

Un ContextPack doit porter au minimum :

- tenant / mission ;
- sources autorisées ;
- décisions ;
- artifacts ;
- memory refs ;
- contraintes ;
- provenance ;
- digests ;
- fraîcheur ;
- politique de rétention ;
- taille/budget contexte.

### 8.3 MemoryProvider

Un MemoryProvider est un provider remplaçable.

Qu'il utilise PostgreSQL, Qdrant, Graphiti, Neo4j, LCM ou un autre moteur, il ne devient jamais l'autorité.

Le contrat mémoire doit assurer :

- scope avant retrieval ;
- isolation tenant ;
- provenance ;
- temporalité ;
- exact refs ;
- suppression / rétention ;
- export ;
- reconstruction des index ;
- détection des contradictions ;
- checkpoint avant compaction destructive.

### 8.4 Graphe

Un graphe peut relier sources, décisions, capacités, missions, personnes et preuves. Il est une projection reconstruisible.

Les choix Graphiti / Neo4j / tables relationnelles / autre moteur doivent être décidés à partir des requêtes réelles, de l'exploitation locale et du coût, pas pour obtenir une nouvelle source de vérité.

## 9. Agents et équipes

### 9.1 Agent

`Agent = Mission + Context + CapabilityGrants + Tools + Resources + Budget + Policies + EvidenceRequirements + Reviewer + ExitConditions`

Une personnalité ne donne aucun droit.

### 9.2 Team minimale pour action structurante

- Producer ;
- Reviewer indépendant ;
- Guardian ;
- vérificateur déterministe lorsque le critère est automatisable.

Par défaut, les droits disparaissent avec la mission.

### 9.3 Hermes et autres harness

Hermes, Codex, OpenCode ou tout autre harness sont des opérateurs interchangeables.

Ils ne possèdent ni :

- l'autorité ;
- le canon ;
- la mémoire commune ;
- les droits persistants ;
- la décision finale.

## 10. MCP, outils, navigateur et computer-use

Tous utilisent le même modèle de contrôle.

Chaîne :

`Mission -> ToolGrant -> Policy -> Preflight -> HumanGate si requis -> ExecutionEnvelope -> Action -> OperationRecord -> Evidence`

### 10.1 MCP

- allowlist d'outils par appel ou mission ;
- secrets hors contexte ;
- arguments tracés avec redaction ;
- résultat typé ;
- timeout ;
- budget ;
- STOP ;
- preuve.

### 10.2 Browser-use

- profil navigateur isolé ;
- domaines / destinations gouvernés ;
- downloads dans espace mission ;
- credentials via coffre, jamais dans le prompt ;
- actions sensibles avec validation humaine ;
- traces et captures selon politique.

### 10.3 Computer-use

Le computer-use est une capability à haut risque.

Par défaut :

- sandbox ou compte OS séparé ;
- pas d'accès au bureau personnel complet ;
- filesystem scope explicite ;
- réseau limité ;
- clipboard contrôlé ;
- HumanGate pour destructive/financial/external publish ;
- replay ou trace exploitable ;
- kill switch.

## 11. ExecutionEnvelope

Toute action exécutable structurante doit recevoir une enveloppe contenant :

- principal ;
- tenant ;
- mission ;
- actor/agent ;
- capability ;
- provider ;
- resource budget ;
- data class ;
- policy decision ;
- tool grants ;
- input refs et digests ;
- timeout ;
- retry policy ;
- idempotency key ;
- rollback ou irréversibilité ;
- evidence requirements ;
- HumanGate state.

## 12. OperationRecord

Un OperationRecord décrit ce qui s'est réellement passé.

Minimum :

- operation id ;
- mission / step ;
- actor ;
- provider ;
- capability ;
- action ;
- started/completed ;
- status ;
- input/output refs ;
- evidence refs ;
- policy refs ;
- resource use ;
- error ;
- rollback ;
- digest.

Il ne doit pas être confondu avec un log technique.

## 13. Evidence

Evidence doit pouvoir être vérifiée indépendamment de l'interface.

Types possibles :

- résultat de test ;
- hash ;
- fichier ;
- capture ;
- log append-only ;
- observation machine ;
- réponse d'une source ;
- attestation humaine ;
- comparaison ;
- métrique ;
- preuve de non-egress.

La télémétrie aide à expliquer ; elle ne remplace pas l'Evidence.

## 14. État et reprise

Chaque mission durable doit supporter :

- checkpoint ;
- état de step ;
- idempotency ;
- retry borné ;
- reprise après redémarrage ;
- blocage explicite ;
- STOP persistant ;
- décision humaine persistée ;
- conservation des evidence refs.

La reprise se fait depuis l'état canonique et les preuves, jamais depuis la seule conversation d'un modèle.

## 15. Stockage

La documentation historique contient plusieurs choix. Ils ne doivent pas être fusionnés silencieusement.

Décision à fermer :

- YanIA utilise PostgreSQL comme stockage durable principal ;
- un ancien contrat de convergence retenait SQLite pour l'état transactionnel canonique.

Le choix final doit être documenté dans un ADR. Il peut retenir plusieurs moteurs par rôle, mais il doit établir une autorité unique par objet.

## 16. Réseau et egress

Par défaut :

- loopback pour services locaux non partagés ;
- LAN uniquement si un besoin explicite le justifie ;
- aucune exposition directe d'administration sur Internet ;
- deny-by-default pour egress des traitements sensibles ;
- inventaire des ports ;
- TLS/auth selon frontière ;
- DNS et proxy observables ;
- test automatisé de non-egress.

## 17. Secrets et credentials

Obligatoire :

- secret hors Git ;
- secret hors prompt ;
- secret hors logs ;
- références opaques dans les contrats ;
- rotation ;
- révocation ;
- scope minimal ;
- coffre ou mécanisme OS adapté ;
- distinction credential humain / service / machine.

Une capacité doit pouvoir utiliser un credential sans nécessairement exposer sa valeur au modèle.

## 18. Observabilité

Corrélation minimale :

`mission_id -> operation_id -> trace_id -> evidence_id`

À enregistrer :

- durée ;
- provider ;
- modèle/version ;
- erreurs ;
- retries ;
- tokens/compute si disponible ;
- ressources ;
- coût ;
- décisions ;
- sorties/artifacts ;
- policy ;
- STOP / HumanGate.

OpenTelemetry est un moyen recommandé, pas le canon.

## 19. Backup, restore, rollback

Toute brique active doit documenter :

- données persistantes ;
- volumes ;
- config ;
- secrets refs ;
- sauvegarde ;
- fréquence ;
- restore ;
- test de restore ;
- rollback logiciel ;
- rollback données ;
- irréversibilités.

Une sauvegarde jamais restaurée n'est pas une preuve de continuité.

## 20. Admission

Une brique ne passe à `ACTIVE` que si sont connus :

- besoin ;
- capability ;
- version exacte ;
- licence ;
- source ;
- digest si applicable ;
- configuration ;
- données ;
- permissions ;
- health ;
- tests ;
- Evidence ;
- observabilité ;
- backup ;
- rollback ;
- alternative / retrait.

## 21. Promotion runtime

`CANDIDATE -> LAB -> TESTED -> CANARY -> ACTIVE`

La promotion exige une Evidence adaptée au risque et peut être annulée.

## 22. UX

Hall, Buildings, cockpits, personas et client rooms sont des projections.

Trois profondeurs :

- Orientation ;
- Pilotage ;
- Inspection.

Une interface qui affiche une capacité non prouvée doit afficher son truth status au lieu de simuler une opérationnalité.

## 23. Définition de conception suffisamment fermée

Le cadre de conception est suffisamment défini lorsque le branchement d'une nouvelle brique ne nécessite plus d'inventer :

- son autorité ;
- son scope ;
- son modèle de données ;
- ses permissions ;
- sa preuve ;
- son healthcheck ;
- son backup ;
- son rollback ;
- sa relation avec les missions ;
- sa place dans le Capability Registry.

À partir de là, les travaux locaux consistent en découverte, configuration, adapter, test et promotion.
