# Codex / SandY - mission de réconciliation locale - 2026-10-09

**Dépôt :** `yannickaudubert/twinSIIAOS`  
**Branche de référence GitHub examinée :** `main`  
**Priorité :** P0 - normes, Radar et interfaces publiques  
**Statut :** INSTRUCTIONS / NON EXÉCUTÉES - état distant inspecté le 2026-10-09.

> Ce fichier missionne Codex installé localement sur SandY. Sa présence sur GitHub ne lance pas Codex, ne prouve pas qu'un clone est présent et n'autorise aucune mutation sur SandY. Respecter d'abord les directives AGENTS.md du dépôt, les décisions humaines applicables et les permissions effectivement accordées.

## 0 bis. Interoperabilite du relais (ajout 2026-10-09)
Un protocole de relais local prive, de delegation de modeles et de gates DevSecOps est documente le 2026-10-09 dans IrinA (depot PRIVE). En conserver ici seulement les principes publics generiques : outputs LLM non fiables, preuves source-ref, permission explicite, resume/rollback, redaction et non-egress. Ne pas divulguer les details de la machine ou les chemins des depots prives. Chercher les contrats existants et eviter tout nouveau canon.

## 1. Rôle confirmé ou déclaré du dépôt
Contrats publics, documentation de convergence, Radar/ressources ; ni machine, ni backend runtime, ni autorité opérationnelle.

## 2. Sources de référence GitHub
- [Resource Hub](public-resource-hub/README.md)
- [Resource Radar V3](resource-radar-v3/README.md)

## 3. Constats à date - GitHub ≠ SandY
- **Référence constatée ou documentée :** La racine GitHub main du 2026-10-09 contient `.gitattributes`, `public-resource-hub/` et `resource-radar-v3/`.
- **Référence constatée ou documentée :** `public-resource-hub` se présente comme une démo publique aux sources curées, non comme un pipeline de production prouvé.
- **Référence constatée ou documentée :** Le README Radar V3 décrit un bridge Python localhost pour téléchargements et des commandes multi-OS, mais la documentation ne prouve pas son installation locale.
- **Référence constatée ou documentée :** Le répertoire `docs/`, cité ailleurs comme support de standards SIIAOS, n'est pas visible dans main GitHub. Vérifier l'historique, les autres branches et SandY avant d'inventer ou de recréer des standards.

## 4. Mission Codex - inspection locale et écarts
1. Découvrir les copies locales, worktrees, branches et remotes ; inventorier les documents publics existants, les prototypes et tout décalage avec GitHub.
2. Comparer le Radar V3 et le Hub aux versions réellement disponibles sur SandY, vérifier sans démarrage non autorisé l'état des éventuels services locaux.
3. Distinguer démonstration browser, bibliothèque de sources, bridge localhost, registry gouverné et Hyperveille staging : ne fusionner aucun de ces rôles par simple similitude.
4. Vérifier la provenance, licences, endpoints et capacités du bridge, son confinement local, ses limites de téléchargement et sa réversibilité.
5. Retrouver les standards HUMAN_TAKEOVER / FILE_INDEX / AI_CODE_DOCUMENTATION via historique/branches/archives avant toute correction de référence.
6. Proposer les contrats publics manquants et un plan d'admission documenté ; ne pas publier de noms de dépôts privés, chemins machines, inventaires réseau ni secrets.

## 5. Tronc commun de reconnaissance
1. Chercher le dépôt local par URL de remote et identité Git ; ne jamais supposer que les chemins d'une autre machine valent pour SandY.
2. En cas de clone présent : relever sans modifier `git status --porcelain=v1`, branche, HEAD, remotes expurgés de tokens, worktrees, commits non poussés, différences avec références distantes, sous-modules et fichiers ignorés importants (noms seulement).
3. Si le dépôt est absent : noter `ABSENT_LOCAL`, ses conséquences et les options ; NE PAS cloner d'office et ne pas interpréter absence locale comme abandon de projet.
4. Vérifier l'existant local : services/processus, Docker/Compose/WSL, montages, volumes, ports, logs synthétisés et dépendances seulement si concernés, sans déclencher ni redémarrer de services.
5. Classer chaque objet `DÉCLARÉ / CODÉ / TESTÉ / DÉPLOYÉ / OBSERVÉ / PROUVÉ / INCONNU`, dater les preuves et préciser leur emplacement. Distinguer `DesiredState` de `ObservedState`.
6. Évaluer architecture, dépendances, risques, rollback, critères d'acceptation et preuves attendues avant toute proposition de modification opératoire.

## 6. Gel opératoire et garde-fous spécifiques
- Sur SandY, seules la documentation, l'inspection en lecture seule et les vérifications non destructives compatibles avec l'environnement sont autorisées par défaut ; aucune installation, mise à jour, migration ni reconfiguration de service avant validation de l'état et des gates.
- Aucun `git reset --hard`, `git clean -fd`, merge/rebase automatique, `docker compose up/down`, `docker system prune`, écrasement de .env/volumes/données, exposition réseau ou publication par simple lecture de cette mission.
- Ne jamais copier de secrets, valeurs .env, données clients, identité d'utilisateur final ni journaux sensibles dans GitHub ; produire un rapport privé et expurgé.
- Aucun téléchargement/mirroring ni activation d'outil sans validation des sources, licences, sécurité et décision de promotion.
- Ce dépôt public ne doit contenir aucune configuration locale sensible, identité client, secret ni inventaire d'infrastructure privée.
- Ne pas recréer Hyperveille ou un runtime concurrent. Réconcilier l'existant avant toute proposition.
- Ne pas interpréter l'étiquette 'V3 opérationnelle' du README comme une preuve d'exploitation sur SandY.

## 7. Livrable local attendu de Codex
Créer dans un espace de rapports **local privé** (hors commit automatique) un dossier daté pour ce dépôt avec :
- `inventory.md` : chemins réels observés sur SandY, branche/HEAD, composants trouvés, services et données, sources et preuves.
- `gap-matrix.md` : `attendu / déclaré GitHub / observé SandY / contradiction / criticité / propriétaire`.
- `plan.md` : corrections ordonnées P0-P3, prérequis, tests, risques, rollback, gate humaine.
- `evidence.json` : métadonnées expurgées (date, commande de lecture/test, code retour, identifiants de version, lien vers trace locale sécurisée).
- `handoff.md` : prochain ordre opératoire, blockers, éléments à ne pas toucher et décision humaine attendue.
Ne déclarer `READY` qu'après résultats de tests et preuve de reprise ; ne jamais affirmer qu'une consigne écrite équivaut à un test. Si rien n'est exécutable, renseigner `NON_OBSERVÉ` et les causes.

## 8. Commande de reprise pour l'opérateur
Depuis Codex sur SandY : « Lis `CODEX_SANDY_2026-10-09.md` dans ce dépôt (ou sur sa branche `main` si nécessaire), effectue l'inventaire read-only et écris le rapport privé. N'installe ni ne déploie rien sans la gate définie. »
