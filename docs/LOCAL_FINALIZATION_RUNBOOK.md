# Runbook de finalisation locale SandY

**Version : 2026-09-26**  
**Statut : préparation de reprise, aucune mutation implicite**  
**Machine principale : SandY**  
**Machine secondaire : ARAGORN**

## 1. But

Transformer la documentation et le code existants en un SIIAOS local réellement opérant, sans réinventer l'architecture pendant l'installation.

Ordre obligatoire :

`Truth Pack -> écarts -> décision -> paramètres -> bindings -> tests -> Golden Mission -> reboot/resume -> preuve -> promotion`

## 2. Phase A — Truth Pack machine

Aucune installation avant ce snapshot.

Capturer :

- OS / build ;
- CPU ;
- RAM ;
- GPU / driver / VRAM ;
- disques / volumes / espace libre ;
- WSL2 ;
- Docker ;
- services ;
- ports ;
- processus structurants ;
- repos et worktrees ;
- branches / commits / propreté ;
- modèles locaux ;
- LM Studio / Ollama éventuel ;
- Hermes / OpenCode / autres harness présents ;
- MCP déclarés ;
- fichiers de configuration pertinents ;
- secrets par présence et référence uniquement ;
- containers / images / volumes ;
- bases ;
- endpoints locaux ;
- interfaces accessibles ;
- tâches/services de démarrage ;
- junctions, symlinks et reparse points dans les racines inventoriées, sans les suivre hors périmètre.

Artefacts attendus :

- `MachineTruth.json`
- `RepoTruth.json`
- `ServiceRegistry.snapshot.json`
- `ModelRegistry.snapshot.json`
- `MCPRegistry.snapshot.json`
- `PortRegistry.snapshot.json`
- `VolumeRegistry.snapshot.json`
- `EvidenceIndex.json`
- `GapLedger.md`

## 3. Phase B — Résolution des contradictions documentaires

Avant configuration :

1. confirmer le stockage autoritaire par type d'objet ;
2. confirmer les dépôts canoniques locaux ;
3. confirmer la forge active ;
4. confirmer les rôles SandY / ARAGORN ;
5. confirmer la version/runtime à promouvoir ;
6. classer les anciennes instructions en ACTIVE / SUPERSEDED / ARCHIVE.

Aucune ancienne configuration n'est appliquée seulement parce qu'elle apparaît dans un tutoriel historique.

## 4. Phase C — Paramètres SandY

Tous les paramètres suivants sont découverts puis enregistrés, jamais supposés.

### 4.1 LM Studio

Capturer :

- endpoint ;
- API OpenAI-compatible ;
- API native ;
- auth active ou non ;
- modèles disponibles ;
- modèles chargés ;
- contexte ;
- parallélisme ;
- GPU offload réel ;
- MCP autorisés ;
- server settings utiles ;
- logs ;
- méthode start/stop ;
- healthcheck.

Historique à revérifier : `127.0.0.1:1235`.

### 4.2 Model Router

Configurer à partir du Truth Pack :

- providers admis ;
- endpoint local ;
- timeout ;
- classes de données ;
- fallback policy ;
- modèles/capabilities ;
- limites contexte ;
- concurrency ;
- refus explicites.

Tests obligatoires :

- public vers local ;
- confidential vers local : accepté ;
- restricted vers local : accepté ;
- confidential vers remote : refus ;
- restricted vers remote : refus ;
- provider local indisponible : pas de fallback cloud silencieux.

### 4.3 Gateway / YanIA

Vérifier :

- auth mode ;
- tenant/org model ;
- DB ;
- migrations ;
- MinIO/object store ;
- Redis si utilisé ;
- services Python ;
- capability registry ;
- tool/agent routes ;
- audit ;
- health endpoints.

### 4.4 Stockages

Pour chaque store :

- rôle canonique ou dérivé ;
- chemin/volume ;
- schéma/version ;
- taille ;
- owner ;
- ACL ;
- backup ;
- restore ;
- retention ;
- migration ;
- health.

### 4.5 Hermes et harness agentiques

Capturer :

- version exacte ;
- install path ;
- profiles ;
- skills ;
- MCP ;
- model providers ;
- terminal backend ;
- subagent behavior ;
- memory behavior ;
- config files ;
- logs ;
- STOP/kill mechanisms.

Ne promouvoir aucune nouvelle version sans lab isolé et preuve.

## 5. Phase D — Réseau

Produire une matrice :

| Service | Bind observé | Bind cible | LAN requis | Egress | Auth | TLS | Evidence |
|---|---|---|---|---|---|---|---|

Règles :

- loopback par défaut ;
- LAN seulement par besoin explicite ;
- aucune console admin exposée Internet ;
- egress sensible deny-by-default ;
- DNS/proxy intégrés au test de non-egress.

## 6. Phase E — Secrets

Inventorier uniquement les références.

Pour chaque credential :

- owner ;
- consumer ;
- purpose ;
- scope ;
- store ;
- rotation ;
- revocation ;
- expiration ;
- exposé au modèle : oui/non.

Objectif : `exposé au modèle = non` sauf justification explicite et bornée.

## 7. Phase F — Capability Bindings

Pour chaque capability nécessaire au Golden Journey, produire :

| Capability | Provider | Node | Version | Data classes | ToolGrant | Health | Evidence | Fallback |
|---|---|---|---|---|---|---|---|---|

Minimum initial :

- model.infer ;
- knowledge.search ;
- document.ingest ;
- document.retrieve ;
- repo.inspect ;
- tool.call ;
- mcp.call ;
- artifact.store ;
- evidence.record ;
- mission.resume.

## 8. Phase G — Mémoire / contexte

Fermer un chemin minimal avant sophistication.

### 8.1 ContextPack

Test :

- créer un besoin ;
- rattacher sources ;
- attacher contraintes ;
- attacher provenance ;
- calculer digests ;
- conserver tenant/mission.

### 8.2 Retrieval

Prouver :

- scope avant retrieval ;
- exact refs ;
- absence de fuite inter-tenant ;
- fallback si embeddings indisponibles ;
- reconstruction possible de l'index.

### 8.3 Reprise

Après redémarrage :

- retrouver mission ;
- retrouver ContextPack ;
- retrouver dernière step ;
- retrouver Evidence ;
- continuer sans historique caché du modèle.

Graphiti / Neo4j / Qdrant / LCM ne sont branchés qu'après ce chemin minimal si leur capability est justifiée.

## 9. Phase H — Tool / MCP Gate

Par défaut :

1. mission créée ;
2. ToolGrant émis ;
3. HumanGate si requis ;
4. outil allowlisté ;
5. paramètres contrôlés ;
6. secret non exposé ;
7. action exécutée ;
8. OperationRecord créé ;
9. Evidence attachée ;
10. sortie réinjectée dans la mission.

Test négatif obligatoire : un persona/chat sans mission ne peut pas déclencher un MCP d'action.

## 10. Phase I — STOP

Tester réellement :

- STOP depuis cockpit ou API ;
- persistance après redémarrage ;
- refus des nouvelles exécutions ;
- lecture toujours disponible si policy le permet ;
- réarmement humain ;
- motif de réarmement ;
- aucun export, publication ou action externe pendant STOP ;
- aucun harness/provider ne contourne STOP ;
- trace Evidence.

## 11. Phase J — Golden Mission

Scénario minimal :

1. créer NeedSpec ;
2. classer les données ;
3. créer ContextPack ;
4. créer Mission ;
5. assigner Team ;
6. résoudre capability/provider ;
7. utiliser modèle local ;
8. produire artifact ;
9. contradiction/review ;
10. enregistrer OperationRecords ;
11. attacher Evidence ;
12. HumanGate ;
13. livrer/exporter ;
14. produire RETEX ;
15. redémarrer ;
16. reprendre ;
17. clôturer.

Critère : aucun passage ne dépend d'une donnée cachée uniquement dans la conversation du modèle.

## 12. Phase K — Preuve de non-egress

Le test doit vérifier au minimum :

- provider sélectionné ;
- classe de données d'entrée et classe effective ;
- preuve d'absence de downgrade silencieux ;
- endpoint ;
- DNS ;
- connexions sortantes du runtime ;
- absence de fallback distant ;
- logs/correlation id ;
- résultat de policy.

La preuve doit être attachée à la mission ou au test d'acceptation.

## 13. Phase L — Backup / Restore

Pour la première capacité client locale :

1. sauvegarder état canonique ;
2. sauvegarder sources/artefacts ;
3. sauvegarder config non-secrète ;
4. sauvegarder références de secrets ;
5. arrêter ;
6. restaurer dans environnement propre/isolé ;
7. vérifier health ;
8. reprendre la mission ;
9. comparer digests ;
10. produire Evidence.

## 14. Phase M — ARAGORN

Seulement après SandY.

Tests :

- recevoir un artefact ou snapshot autorisé ;
- vérifier digest ;
- démarrer en canary si prévu ;
- simuler indisponibilité SandY ;
- reprendre le périmètre explicitement prévu ;
- éviter split-brain ;
- retourner à SandY ;
- prouver le rollback.

## 15. Phase N — Promotion

Une brique ou un binding est promu uniquement si :

- version exacte connue ;
- licence admissible ;
- health vert ;
- tests verts ;
- Evidence disponible ;
- sécurité vérifiée ;
- backup/restore connu ;
- rollback connu ;
- owner connu ;
- dépendances connues ;
- alternative connue si critique.

## 16. Definition of Done V1 locale

Un dossier client `CONFIDENTIAL` peut être :

- importé ;
- isolé ;
- indexé/recherché ;
- traité par modèle local ;
- utilisé dans une mission multi-étapes ;
- relié aux sources et preuves ;
- validé humainement ;
- exporté ;
- repris après reboot ;
- archivé/supprimé selon policy ;
- restauré depuis backup ;
- démontré sans provider distant.

## 17. Ce qui vient après seulement

Après la V1 prouvée :

- Graphiti/Neo4j plus riche ;
- LCM/RLM avancés ;
- vLLM/LMCache ;
- computer-use généraliste ;
- federation plus large ;
- Client Rooms externes ;
- agents plus autonomes ;
- optimisation multi-GPU/nœuds ;
- productisation installable.

Leur absence ne bloque pas la fermeture de la première verticale.
