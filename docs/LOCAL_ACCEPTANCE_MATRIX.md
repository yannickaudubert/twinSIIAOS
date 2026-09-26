# Matrice d'acceptation locale SIIAOS

**Version : 2026-09-26**  
**But : convertir les cadres documentaires en critères testables sur SandY.**

## Règle générale

Aucun critère n'est `PASS` sans Evidence datée.

États :

- `NOT_RUN`
- `PASS`
- `FAIL`
- `BLOCKED`
- `STALE`

## F1 — Vérité machine

| ID | Test | Attendu | Evidence |
|---|---|---|---|
| F1-01 | Inventaire OS/CPU/RAM/GPU/disques | valeurs observées, horodatées | MachineTruth |
| F1-02 | Inventaire WSL2/Docker | versions/états connus | MachineTruth |
| F1-03 | Inventaire repos | path/branch/commit/dirty/upstream | RepoTruth |
| F1-04 | Inventaire services/ports | tous les services structurants classés | Service/Port Registry |
| F1-05 | Inventaire modèles | disponibles/chargés/capabilities | ModelRegistry |
| F1-06 | Inventaire MCP | noms/transports/cibles expurgées | MCPRegistry |
| F1-07 | Secrets | présence/ref uniquement | SecretReference report |
| F1-08 | Aucune mutation | préflight read-only | audit du script |
| F1-09 | Reparse/junction/symlink escape | aucun parcours hors racines autorisées | rapport preflight |
| F1-10 | Truth freshness | toute observation porte date/TTL | EvidenceIndex |

## F1B — Briques admissibles

| ID | Test | Attendu |
|---|---|---|
| F1B-01 | Version exacte | connue pour chaque brique active |
| F1B-02 | Licence | connue et compatible avec son rôle |
| F1B-03 | Documentation | correspond à la version runtime |
| F1B-04 | Healthcheck | défini et exécutable |
| F1B-05 | Backup/restore | procédure connue |
| F1B-06 | Rollback | procédure connue |
| F1B-07 | Alternative | connue pour capacité critique |
| F1B-08 | Non-rôle | explicite |

## F2 — Local-only

| ID | Test | Attendu |
|---|---|---|
| F2-01 | LM Studio health | endpoint local répond |
| F2-02 | Public -> local | autorisé |
| F2-03 | Confidential -> local | autorisé |
| F2-04 | Restricted -> local | autorisé |
| F2-05 | Confidential -> remote | refus |
| F2-06 | Restricted -> remote | refus |
| F2-07 | Local indisponible | aucun fallback cloud silencieux |
| F2-08 | Non-egress | aucune connexion interdite pendant run sensible |
| F2-09 | Provider/model | enregistrés dans OperationRecord/Evidence |
| F2-10 | Classification downgrade | aucun `CONFIDENTIAL -> INTERNAL` silencieux |
| F2-11 | Policy decision log | chaque autorisation/refus est relié à une décision |

## F2A — Autorité et permissions

| ID | Test | Attendu |
|---|---|---|
| F2A-01 | Identity | principal connu |
| F2A-02 | Tenant | mission bornée |
| F2A-03 | Mandate | finalité/périmètre/données/décideur connus |
| F2A-04 | ToolGrant | capacité et opérations bornées |
| F2A-05 | Expiration | droits temporaires expirent |
| F2A-06 | Revocation | ToolGrant révoqué refuse l'action |
| F2A-07 | Persona sans mandat | aucune action outillée |

## F3 — Mémoire et reprise

| ID | Test | Attendu |
|---|---|---|
| F3-01 | ContextPack | sources/provenance/contraintes persistées |
| F3-02 | Scope-before-retrieval | fuite cross-tenant impossible |
| F3-03 | Exact refs | chaque synthèse peut revenir aux sources |
| F3-04 | Index rebuild | index dérivé reconstructible |
| F3-05 | Checkpoint | état durable avant action longue/compaction |
| F3-06 | Reboot | mission retrouvée |
| F3-07 | Resume | prochaine étape correcte |
| F3-08 | No hidden chat state | reprise sans conversation cachée du modèle |

## F3A — Mission engine

| ID | Test | Attendu |
|---|---|---|
| F3A-01 | Idempotency | même clé ne duplique pas l'effet |
| F3A-02 | Retry | retry borné et tracé |
| F3A-03 | Failure | échec explicite, pas de continuation silencieuse |
| F3A-04 | HumanGate | bloque réellement |
| F3A-05 | STOP | bloque réellement |
| F3A-06 | STOP reboot | persiste |
| F3A-07 | Rearm | validation humaine + motif |
| F3A-08 | OperationRecord | créé pour chaque action structurante |
| F3A-09 | STOP export | aucun export/action externe après STOP |
| F3A-10 | STOP bypass | aucun provider/harness ne contourne STOP |

## F3B — MCP / Tools

| ID | Test | Attendu |
|---|---|---|
| F3B-01 | MCP discovery | registry expurgé |
| F3B-02 | Tool allowlist | seul outil explicitement accordé appelable |
| F3B-03 | Denied tool | refus explicite |
| F3B-04 | Secret isolation | secret absent prompt/log |
| F3B-05 | Timeout | action bloquée s'arrête |
| F3B-06 | Evidence | arguments redacted + résultat référencé |
| F3B-07 | STOP during tool call | arrêt/abandon maîtrisé selon capability |

## F4 — Golden Mission

| ID | Étape | Attendu |
|---|---|---|
| F4-01 | Intake | origine enregistrée |
| F4-02 | NeedSpec | résultat et critères définis |
| F4-03 | Classification | tenant + data class |
| F4-04 | ContextPack | sources autorisées |
| F4-05 | Team | Producer/Reviewer/Guardian |
| F4-06 | Routing | provider local sélectionné par policy |
| F4-07 | Production | artifact versionné |
| F4-08 | Contradiction | revue indépendante |
| F4-09 | Evidence | chaîne complète |
| F4-10 | HumanGate | décision humaine persistée |
| F4-11 | Export | artifact exportable sans fuite |
| F4-12 | Economy | temps/ressource/coût enregistrés si disponibles |
| F4-13 | RETEX | méthode générique séparée des données client |
| F4-14 | Reboot | mission reprise |
| F4-15 | Close | rétention/archivage appliqués |

## F5 — Backup / Restore

| ID | Test | Attendu |
|---|---|---|
| F5-01 | Backup canon | snapshot exploitable |
| F5-02 | Backup artifacts | présents + digests |
| F5-03 | Config export | non-secrets exportés |
| F5-04 | Restore isolé | runtime redémarre |
| F5-05 | Mission restore | mission retrouvée |
| F5-06 | Digest compare | données/artifacts conformes |
| F5-07 | Secret refs | réinjectables sans fuite |
| F5-08 | Recovery Evidence | rapport de restauration |

## F6 — Observabilité

| ID | Test | Attendu |
|---|---|---|
| F6-01 | Correlation | mission -> operation -> trace -> evidence |
| F6-02 | Provider/version | visibles |
| F6-03 | Latency | mesurée |
| F6-04 | Resource use | capturée si disponible |
| F6-05 | Policy decision | reliée |
| F6-06 | Errors/retries | observables |
| F6-07 | Redaction | données sensibles non exposées |
| F6-08 | Evidence != telemetry | distinction maintenue |
| F6-09 | Authority trace | principal/tenant/mandate/toolgrant/policy corrélables |
| F6-10 | Classification trace | classe d'entrée et classe effective identiques sauf décision explicite |

## F7 — ARAGORN canary

Non bloquant avant réussite de F1-F6 sur SandY.

| ID | Test | Attendu |
|---|---|---|
| F7-01 | Snapshot transfer | digest vérifié |
| F7-02 | Canary | périmètre explicitement borné |
| F7-03 | SandY outage | reprise définie |
| F7-04 | Split-brain | impossible ou détecté/bloqué |
| F7-05 | Return to SandY | retour contrôlé |
| F7-06 | Rollback | prouvé |

## Gate de promotion V1

La V1 locale est promouvable seulement si :

- tous les tests F1 critiques sont PASS ;
- F1B est complet pour les briques actives ;
- tous les tests F2 sont PASS ;
- F2A est PASS pour la Golden Mission ;
- F3/F3A critiques sont PASS ;
- le chemin MCP utilisé est PASS ;
- F4 complet est PASS ;
- F5 restore est PASS ;
- F6 correlation/evidence est PASS.

Les fonctions avancées peuvent rester `LATER` sans bloquer cette promotion.
