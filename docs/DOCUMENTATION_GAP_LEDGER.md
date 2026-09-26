# Registre des lacunes documentaires et décisions locales

**Version : 2026-09-26**  
**But : identifier uniquement ce qui reste à définir, décider ou prouver avant finalisation locale.**

## Légende

- `CLOSED` : cadre suffisamment défini ; ne pas rouvrir sans contradiction prouvée.
- `DECISION` : choix d'architecture encore à ratifier.
- `CONTRACT` : contrat à formaliser pour éviter les interprétations locales.
- `PROOF` : conception suffisante, preuve runtime manquante.
- `BINDING` : provider/paramètre local à découvrir et raccorder.
- `LATER` : utile après V1 ; ne bloque pas la première verticale.

## 1. Gouvernance

| Sujet | Statut | État |
|---|---|---|
| Primauté humaine | CLOSED | Documentée et répétée dans les contrats |
| HumanGate | CLOSED/PROOF | Contrat et code partiel présents ; preuve Golden Mission attendue |
| STOP persistant | CLOSED/PROOF | Exigence stabilisée ; test runtime frais requis |
| Producer / Reviewer / Guardian | CLOSED | Modèle d'équipe stabilisé |
| DesiredState vs ObservedState | CLOSED | Invariant canonique |
| Truth statuses | CLOSED | Normaliser la terminologie dans les outils |
| Identity != Role != Authority | CLOSED/CONTRACT | Invariant fixé ; schéma exécutable à fermer |
| Mandate / ToolGrant / PolicyDecision | CONTRACT | Contrats applicatifs encore incomplets dans YanIA |
| ChangeSet / rollback | CLOSED/PROOF | Doctrine fixée ; appliquer aux mutations locales |

## 2. Topologie et runtime

| Sujet | Statut | État |
|---|---|---|
| SandY principal | CLOSED/PROOF | Décision stabilisée ; snapshot frais à régénérer |
| ARAGORN secondaire/canary | CLOSED/PROOF | Rôle cible fixé ; test réel plus tard |
| Galaxy/Galaxy Book | DECISION | Ne pas attribuer de rôle par inférence |
| Forge active GitHub | CLOSED/PROOF | Utilisée dans le travail courant ; comparer au local |
| Vercel | CLOSED | Surface Web, jamais autorité |
| WSL2/Docker | PROOF | Présence historique ; état actuel à sonder |
| Ports / services | PROOF | Inventaire read-only requis |
| Démarrage automatique | BINDING | À inventorier puis documenter |

## 3. Stockage et canon

| Sujet | Statut | État |
|---|---|---|
| Une autorité par objet | CLOSED | Invariant |
| PostgreSQL YanIA | PROOF | Documenté par le repo |
| SQLite historique comme canon transactionnel | DECISION | Contradiction avec YanIA à résoudre |
| Object storage | BINDING | MinIO/S3-compatible documenté ; état SandY à vérifier |
| Redis | BINDING | Présent dans architecture YanIA ; rôle réel à confirmer |
| DuckDB analytique | LATER | Option dérivée, non bloquante |
| Evidence Ledger append-only | CONTRACT | Modèle exigé, implémentation unifiée à fermer |

## 4. Modèles et inférence

| Sujet | Statut | État |
|---|---|---|
| LM Studio fournisseur local immédiat | CLOSED/PROOF | Historique solide ; health actuel requis |
| Endpoint 127.0.0.1:1235 | PROOF | Valeur historique, jamais constante canonique |
| Model Router fail-closed | CLOSED/PROOF | Code/tests sur branches YanIA ; déploiement à prouver |
| Noms de modèles | BINDING | Découverte runtime obligatoire |
| vLLM | LATER | Benchmark après baseline |
| LMCache/APC | LATER | Après benchmark |
| Ollama | BINDING/LATER | Provider possible si réellement présent/utile |

## 5. Mémoire, connaissance et graphe

| Sujet | Statut | État |
|---|---|---|
| Source/index/RAG/canon séparés | CLOSED | Doctrine fixée |
| ContextPack | CLOSED/PROOF | Contrat + code partiel |
| Knowledge Layer YanIA | CLOSED/PROOF | Déjà codée en partie sur main |
| MemoryProvider commun | CONTRACT | Interface à formaliser |
| Scope avant retrieval | CLOSED/PROOF | Invariant ; tests négatifs requis |
| Exact refs / provenance | CLOSED/PROOF | Exigence stabilisée |
| Graphiti | BINDING/LATER | Provider potentiel, pas canon |
| Neo4j | BINDING/LATER | Provider potentiel, pas canon |
| Qdrant | BINDING/LATER | Provider potentiel, pas canon |
| LCM/hermes-lcm | LATER | Lab après fermeture mémoire minimale |
| Checkpoint avant compaction | CONTRACT | À intégrer au moteur durable de mission |
| Memory Debt Sweeper | LATER | Après writeback/reprise minimum |

## 6. Agents et orchestration

| Sujet | Statut | État |
|---|---|---|
| Mission Factory | CLOSED/PROOF | PR YanIA #3 |
| NeedSpec | CLOSED/PROOF | PR YanIA #3 |
| OperationRecord | CLOSED/PROOF | PR YanIA #3 |
| Evidence refs | CLOSED/PROOF | PR YanIA #3 |
| Resume read-only | CLOSED | Existe, mais ne constitue pas moteur |
| Moteur durable mission | CONTRACT | Queue/checkpoint/retry/idempotence à fermer |
| Hermes opérateur | CLOSED/PROOF | Rôle défini ; version/config actuelles à sonder |
| OpenCode/Codex/autres harness | CLOSED | Providers remplaçables |
| Budgets / quotas agents | CONTRACT | Schéma commun à finaliser |
| Exit conditions | CONTRACT | À encoder dans mission/team |

## 7. Outils, MCP, browser et computer-use

| Sujet | Statut | État |
|---|---|---|
| MCP sous mandat | CLOSED/PROOF | Tutoriel v0.4 documente un câblage antérieur |
| MCP allowlist | CLOSED/PROOF | Contrat établi |
| Secrets hors prompt | CLOSED/PROOF | Invariant |
| Capability Broker commun | CONTRACT | Manquant dans le tutoriel v0.4 |
| Git connector local | BINDING | À brancher sous policy |
| Docker connector local | BINDING | À brancher sous policy |
| Obsidian/AppFlowy/Grist | BINDING/LATER | Selon usages réels |
| Browser-use | CONTRACT/LATER | Contrat de sandbox défini ; provider à choisir plus tard |
| Computer-use | CONTRACT/LATER | Haut risque ; ne bloque pas V1 |

## 8. Sécurité

| Sujet | Statut | État |
|---|---|---|
| local-first / fail-closed | CLOSED | Invariant |
| Classes PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED | CLOSED | Stabilisé |
| Non-egress | PROOF | Test machine automatisé manquant |
| Loopback par défaut | CLOSED/PROOF | Doctrine fixée ; binds réels à vérifier |
| Exposition Internet admin interdite | CLOSED | Invariant |
| Secret store | DECISION/BINDING | Mécanisme local exact à arrêter |
| Rotation/révocation | CONTRACT | Runbook à produire avec le choix de coffre |
| Prompt injection / source trust | CONTRACT | Policy/tool mediation à expliciter dans tests |
| Tenant isolation | CLOSED/PROOF | Design présent ; tests négatifs obligatoires |

## 9. Observabilité et preuve

| Sujet | Statut | État |
|---|---|---|
| Audit events | CLOSED/PROOF | YanIA les utilise |
| Claim -> Evidence -> Citation -> Source | CLOSED | YanIA main |
| OperationRecord | CLOSED/PROOF | PR #3 |
| OpenTelemetry | BINDING | Collector documenté ; wiring réel à vérifier |
| correlation mission/operation/trace/evidence | CONTRACT | À normaliser |
| Evidence vs telemetry | CLOSED | Séparation fixée |
| Evidence retention/redaction | CONTRACT | À finaliser |

## 10. Backup / restore / continuité

| Sujet | Statut | État |
|---|---|---|
| Rollback obligatoire | CLOSED | Invariant |
| Backup par brique | PROOF | Documentation locale fraîche à produire |
| Restore testé | PROOF | Gate bloquant avant client réel |
| Reprise mission après reboot | PROOF | Gate F3 |
| ARAGORN canary/rollback | LATER/PROOF | Après SandY V1 |
| Split-brain protection | CONTRACT/LATER | Nécessaire avant fédération |

## 11. Juridique / licences

| Sujet | Statut | État |
|---|---|---|
| Licence exacte par dépendance | CLOSED/PROOF | Règle fixée, inventaire à produire |
| Gate licence twinSIIAOS | DECISION | Issue #2 ouverte |
| SBOM | PROOF/LATER | Requis avant productisation |
| THIRD_PARTY_NOTICES | PROOF/LATER | Requis avant release |
| LegalCapabilityManifest | CONTRACT/LATER | Déjà spécifié dans issue #2 |
| Anti-capture / modèle de licence noyau | DECISION | À ratifier humainement |

## 12. UX / surfaces

| Sujet | Statut | État |
|---|---|---|
| Interface = projection | CLOSED | Invariant |
| Hall/Building/Cockpit | CLOSED | Grammaire de projection, pas canon |
| Truth status visible | CONTRACT | À généraliser |
| Local cockpit | PROOF | Câblages historiques, version active à vérifier |
| Client Room | LATER | Après V1 locale |
| Ephemeral Interface Factory | LATER | Cadre déjà documenté |

## 13. Radar / Hyperveille

| Sujet | Statut | État |
|---|---|---|
| Une chaîne d'admission commune | CLOSED | Source -> signal -> qualification -> preuve -> admission |
| Resource Radar comme projection | CLOSED | Pas de deuxième canon |
| V3 réellement déployée reproductible | PROOF | Issue Radar l'identifie comme préalable |
| V4 shell | PROOF | Travaux versionnés, intégration live restante |
| Bridge local | PROOF | À tester depuis SandY |
| Capability Graph feed | CONTRACT | À brancher sans transformer le Radar en autorité |

## 14. Golden Mission

| Sujet | Statut | État |
|---|---|---|
| Parcours fonctionnel | CLOSED | Étapes déjà définies |
| Tests exacts | CONTRACT | À automatiser |
| Provider local réel | PROOF | À exécuter |
| Non-egress | PROOF | À attacher |
| HumanGate | PROOF | À exécuter |
| Artifact/Evidence | PROOF | À exécuter |
| Reboot/resume | PROOF | À exécuter |
| RETEX | PROOF | À exécuter |
| Archive/retention | CONTRACT/PROOF | À fermer |

## 15. Résultat du gap analysis

Le système ne manque plus d'un métamodèle général.

Les lacunes bloquantes restantes pour la V1 sont concentrées dans six groupes :

1. **Truth Pack machine frais** ;
2. **autorité/stockage + Identity/Authority/Mandate/ToolGrant** ;
3. **moteur durable Mission/Checkpoint/Retry/Resume** ;
4. **Capability/Provider/Resource bindings réels** ;
5. **sécurité opérationnelle : secrets, réseau, non-egress** ;
6. **backup/restore + Golden Mission + reboot proof**.

Graphiti, Neo4j, LCM, vLLM, LMCache, browser-use généralisé et federation ne doivent pas retarder ces six fermetures.
