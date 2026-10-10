# Index de capitalisation des sources SIIAOS local

**Version : 2026-09-26**  
**But : préserver la provenance sans recopier aveuglément les anciennes instructions.**

## 1. Règle de capitalisation

Une source historique est classée :

- `ACTIVE_REFERENCE` : contenu toujours valable et repris dans les contrats courants ;
- `PARTIAL_REFERENCE` : contenu utile mais certains paramètres/rôles sont périmés ;
- `SUPERSEDED` : remplacé par une décision plus récente ;
- `EVIDENCE_SOURCE` : contient des observations ou preuves datées ;
- `ARCHIVE` : conserve l'historique sans guider l'exécution actuelle.

## 2. Sources majeures récupérées

### SIIAOS_CONVERGENCE_ET_PASSAGE_ASTRA_2026-09-16.md

**Classe : ACTIVE_REFERENCE + PARTIAL_REFERENCE**

Apports conservés :

- primauté humaine ;
- local-first/fail-closed ;
- modèles remplaçables ;
- interfaces comme projections ;
- multi-tenant ;
- séparation Producer/Reviewer/Guardian ;
- STOP persistant ;
- rollback avant mutation ;
- Capability Resolver partant du besoin ;
- chaîne Mandate/Mission/Context/Evidence/RETEX ;
- gates F0-F8 ;
- Golden Journey consultant ;
- capitalisation sans données client.

Éléments à ne pas recopier sans décision fraîche :

- choix SQLite comme état transactionnel canonique ;
- rôles physiques/forge lorsque contredits par des décisions plus récentes ;
- versions/runtime déclarés au 16 septembre.

### Visual Operating Pack — 23 septembre 2026

**Classe : ACTIVE_REFERENCE**

Apports conservés :

- critère de sortie V1 par Golden Mission ;
- séparation décidé/codé/prouvé/pending/blocked ;
- carte maître ;
- topologie physique ;
- trois portes ;
- neuf Atlas ;
- dépendances des gates ;
- Resource Radar comme système d'admission.

Utilisation : support visuel, pas source de vérité runtime.

### TUTORIEL-SANDY-v0.4.0.md

**Classe : EVIDENCE_SOURCE + PARTIAL_REFERENCE**

Apports conservés :

- découverte LM Studio ;
- inventaire de modèles ;
- choix/load/unload ;
- lecture expurgée de `mcp.json` ;
- appel MCP sous mandat ;
- allowlist d'outils ;
- token non stocké dans `integrations.json` ;
- STOP/réarmement ;
- provenance conversation -> mission.

À revérifier :

- version exacte du runtime ;
- endpoint/port ;
- modèle affiché ;
- état actuel des fichiers/configs ;
- services effectivement présents.

### Dossiers SIIAOS × Hermes — profils agents

**Classe : ACTIVE_REFERENCE + PARTIAL_REFERENCE**

Apports conservés :

- Hermes comme opérateur, pas autorité ;
- tools/MCP scopés ;
- subagents isolés ;
- modèle/provider remplaçable ;
- rôles par niveau/bureau ;
- preuves et HumanGate ;
- skills capitalisables après validation.

À revérifier :

- version Hermes installée ;
- config ;
- skills présents ;
- mémoire active ;
- backends terminal ;
- profils réellement déployés.

### PACK_SIIAOS_Socle_Directeur_2026-09-06 et documents Connaissance/MultiVault/TraceOps

**Classe : ACTIVE_REFERENCE**

Apports conservés :

- RAG pour savoir mouvant ;
- formaliser méthode/skill/tests avant fine-tuning ;
- LoRA seulement après besoin mesuré ;
- décision critique avec sources + humain ;
- mémoire longue avec provenance/temporalité ;
- séparation archive/corpus actif ;
- objets documentaires context/ADR/LEARNINGS/BLOCKERS/ITERATION_LOG/MANIFEST/RUNBOOK.

### SIIAOS_ARCHITECTURE_AI_HANDOFF_2026-08-30.md

**Classe : ACTIVE_REFERENCE**

Apports conservés :

- Capability > application ;
- Capability Router ;
- provider candidates ;
- node placement ;
- adapter ;
- Resource/Tool Experience Hub ;
- registry automatique services/apps ;
- capability advertisement ;
- budgets, sandbox, logs, OperationRecord, preuve, STOP, rollback.

### SIIAOS_CS-00_G0_HERITAGE_ADMISSION_2026-08-30.md

**Classe : EVIDENCE_SOURCE**

Apports conservés :

- différences d'autorité entre lignées ;
- importance des migrations/backup/reprise ;
- OperationRecord hashé/provenance ;
- HumanGate opposable ;
- risques des régressions d'autorité ;
- nécessité de vérifier la succession, pas seulement les tests unitaires.

### SIIAOS_Ephemeral_Interface_Factory_Dossier_Decision_2026-08-28.pdf

**Classe : ACTIVE_REFERENCE**

Apports conservés :

- scope avant index ;
- deny-by-default ;
- destruction vérifiée ;
- control plane canonique ;
- SBOM/version pinning ;
- prompt injection/tool scopes ;
- Evidence append-only ;
- Docker/Postgres first avant complexité ;
- modèle IA hors logique métier déterministe ;
- pas d'exposition admin directe de SandY.

## 3. Sources de code actuelles

### yannickaudubert/YanIA

Rôle actuel : fournisseur de capacités IA/recherche/documentaire/outils/agents/gateway.

Éléments à considérer comme code actuel sur `main` ou branches ouvertes :

- Gateway ;
- Capability Registry ;
- Knowledge Layer relationnelle ;
- PostgreSQL/pgvector ;
- Redis/MinIO/OTEL dans la stack ;
- model-router ;
- audit ;
- outils/agents ;
- migrations Mission Factory sur PR #3 ;
- truth-gate fixes PR #4.

Attention : une PR ouverte ne vaut pas déploiement.

### yannickaudubert/twinSIIAOS

Rôle actuel : convergence, contrats, Radar et documentation canonique en cours.

La branche `docs/siiaos-puzzle-20260925` porte désormais :

- puzzle canonique ;
- contrat documentaire de brique ;
- état courant local ;
- contrat de conception locale ;
- runbook de finalisation ;
- gap ledger ;
- matrice d'acceptation ;
- cet index de capitalisation.

## 4. Politique de remplacement

Lorsqu'une source ancienne est contredite :

1. ne pas la supprimer ;
2. identifier la décision ou preuve qui la remplace ;
3. marquer la section concernée `SUPERSEDED` dans le registre actif ;
4. ne pas transporter automatiquement ses valeurs de configuration ;
5. conserver la provenance pour comprendre l'évolution.

## 5. Règle pour les conversations

Les échanges précédents sont utiles pour retrouver :

- décisions humaines ;
- hypothèses ;
- essais ;
- conventions ;
- corrections ;
- besoins métier.

Ils ne deviennent pas des preuves runtime.

Toute affirmation technique issue d'une conversation doit être soit :

- reprise comme décision ;
- vérifiée sur la machine/dépôt ;
- ou conservée comme `DECLARED/UNKNOWN`.

## 6. Point d'entrée de reprise

Pour reprendre le chantier local, lire dans cet ordre :

1. `SIIAOS_PUZZLE.md`
2. `LOCAL_SYSTEM_CURRENT.md`
3. `LOCAL_DESIGN_CONTRACT.md`
4. `DOCUMENTATION_GAP_LEDGER.md`
5. `LOCAL_FINALIZATION_RUNBOOK.md`
6. `LOCAL_ACCEPTANCE_MATRIX.md`
7. uniquement ensuite, les sources historiques utiles à un point précis.

L'objectif est qu'aucune reprise ne nécessite de relire tout l'historique des conversations.
