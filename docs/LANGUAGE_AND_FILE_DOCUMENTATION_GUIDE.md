# Guide SIIAOS de documentation par langage et type de fichier

**Version : 2026-09-26**  
**But : garantir une documentation de reprise humaine adaptée aux langages et formats réellement employés.**

## 1. TypeScript / JavaScript

### Bonnes pratiques attendues

- types explicites aux frontières ;
- éviter `any` sauf justification documentée ;
- fonctions courtes et nommées selon l'intention ;
- effets de bord isolés ;
- erreurs typées ;
- async/await lisible ;
- dépendances injectées ou explicites ;
- validation runtime aux entrées non fiables ;
- éviter logique métier cachée dans UI/framework hooks.

### Documentation

Documenter particulièrement :

- exports publics ;
- API HTTP ;
- événements ;
- configuration ;
- side effects ;
- appels réseau ;
- accès base/fichier ;
- règles d'auth/authz ;
- retry/timeout ;
- state management ;
- cache.

Pour TypeScript, préférer les types comme documentation exécutable, complétés par JSDoc lorsque le **pourquoi** ou le contrat n'est pas évident.

### React / TSX

Chaque composant significatif doit expliciter :

- responsabilité UX ;
- props ;
- source des données ;
- mutations ;
- états loading/empty/error/unauthorized ;
- accessibilité ;
- effets ;
- dépendance au serveur/client ;
- tests.

Ne pas cacher une règle métier critique dans un composant visuel.

## 2. Python

### Bonnes pratiques attendues

- PEP 8 ;
- type hints aux frontières ;
- docstrings pour modules/classes/fonctions publiques ;
- gestion explicite des exceptions ;
- context managers pour ressources ;
- pas de mutable defaults ;
- configuration hors code ;
- dépendances pinées selon politique du projet ;
- séparation I/O / logique métier ;
- tests pytest lisibles.

### Docstrings

Style recommandé : Google ou NumPy, mais un seul style cohérent par dépôt.

Documenter :

- purpose ;
- Args ;
- Returns ;
- Raises ;
- side effects ;
- sécurité ;
- exemples si l'usage n'est pas évident.

### FastAPI / API

Documenter :

- modèle de requête ;
- auth ;
- codes retour ;
- erreurs métier ;
- idempotence ;
- data class ;
- appel à provider externe/local ;
- timeout.

## 3. Rust

### Bonnes pratiques attendues

- `rustfmt` ;
- `clippy` ;
- Result/Option explicites ;
- pas de `unwrap()` en chemin de production sans justification ;
- ownership et lifetimes simples quand possible ;
- unsafe minimal et documenté ;
- erreurs avec contexte ;
- modules à responsabilité claire ;
- invariants encodés dans les types quand raisonnable.

### Documentation

Utiliser :

- `//!...` pour modules/crates ;
- `///...` pour API publique ;
- `# Safety` obligatoire pour unsafe public ;
- `# Errors`, `# Panics`, `# Examples` lorsque pertinents.

Toute section unsafe doit expliquer :

- invariant mémoire ;
- pourquoi safe Rust ne suffit pas ;
- conditions de sûreté ;
- test ou preuve.

## 4. SQL

### Chaque migration doit expliquer

- intention métier ;
- tables/colonnes/index touchés ;
- compatibilité arrière ;
- volumétrie/lock potentiel ;
- transformation des données ;
- rollback ou irréversibilité ;
- impact applicatif ;
- ordre d'exécution ;
- test associé.

### Bonnes pratiques

- noms explicites ;
- contraintes en base pour invariants critiques ;
- FK lorsque appropriées ;
- index justifiés par requêtes ;
- transactions pour changements atomiques ;
- migrations idempotentes uniquement si volontaire ;
- aucune suppression destructive sans stratégie de sauvegarde.

Le schéma est une API durable : une IA ne doit jamais traiter une migration comme un détail interne.

## 5. PowerShell

### Bonnes pratiques attendues

- fonctions avec verbes approuvés ;
- `[CmdletBinding()]` pour scripts opératoires importants ;
- paramètres typés ;
- `-WhatIf` / `-Confirm` pour mutations appropriées ;
- `Set-StrictMode` lorsque compatible ;
- gestion explicite de `$ErrorActionPreference` ;
- paths avec `Join-Path` ;
- pas de secrets dans les sorties ;
- encodage et quoting maîtrisés.

### Help-based documentation

Pour scripts importants, utiliser comment-based help :

- `.SYNOPSIS`
- `.DESCRIPTION`
- `.PARAMETER`
- `.EXAMPLE`
- `.INPUTS`
- `.OUTPUTS`
- `.NOTES`

Documenter clairement si un script est READ_ONLY, MUTATING ou DESTRUCTIVE.

## 6. Shell / Bash

### Bonnes pratiques

- shebang ;
- `set -euo pipefail` lorsque compatible et compris ;
- variables quotées ;
- éviter parsing fragile de `ls` ;
- trap/cleanup ;
- exit codes documentés ;
- commandes destructives protégées ;
- compatibilité POSIX ou Bash explicitée.

Documenter :

- environnement attendu ;
- outils requis ;
- fichiers touchés ;
- idempotence ;
- rollback ;
- privilèges.

## 7. Dockerfile

Chaque Dockerfile doit expliquer ou rendre évident :

- base image et raison ;
- version/digest selon niveau de reproductibilité ;
- build stages ;
- utilisateur non-root si possible ;
- ports ;
- volumes ;
- healthcheck ;
- fichiers copiés ;
- secrets build/runtime ;
- entrypoint/cmd ;
- dépendances système ;
- stratégie d'update.

Éviter les images `latest` pour les composants structurants.

## 8. Docker Compose

Documenter :

- rôle de chaque service ;
- dépendances ;
- réseaux ;
- volumes ;
- binds ;
- ports hôte ;
- secrets/env ;
- healthchecks ;
- ordre de démarrage ;
- données persistantes ;
- restore ;
- profils.

Un compose n'est pas auto-documentant.

## 9. YAML / YML

Applicable à CI, config, manifests, corpus structurés.

Documenter :

- schéma ;
- propriétaire ;
- valeurs autorisées ;
- defaults ;
- secrets interdits ;
- générateur éventuel ;
- validation ;
- consommateurs.

Pour GitHub Actions :

- trigger ;
- permissions ;
- secrets ;
- artefacts ;
- caches ;
- environnements ;
- conditions ;
- conséquences d'échec.

Permissions minimales obligatoires.

## 10. JSON

Un JSON structurant doit avoir :

- schéma JSON Schema ou type équivalent si durable ;
- version de schéma ;
- producteur ;
- consommateur ;
- règles de compatibilité ;
- statut généré ou éditable ;
- exemples sans secrets.

Les JSON de données runtime ne doivent pas être documentés comme configuration si ce n'est pas leur rôle.

## 11. TOML

Documenter :

- outil consommateur ;
- sections ;
- versions ;
- dépendances ;
- features ;
- valeurs locales vs publiables ;
- commande de validation.

Pour `pyproject.toml` / `Cargo.toml`, expliquer les dépendances non triviales et les features structurantes.

## 12. HTML

Pour pages ou shells applicatifs :

- finalité ;
- données injectées ;
- scripts associés ;
- formulaires/actions ;
- accessibilité ;
- sécurité CSP/injection si applicable ;
- génération statique ou runtime.

Préférer HTML sémantique.

## 13. CSS

Documenter au niveau architecture plutôt que chaque règle :

- design tokens ;
- conventions de nommage ;
- responsive strategy ;
- thèmes ;
- variables globales ;
- zones sensibles ;
- overrides exceptionnels.

Un hack CSS non évident doit être commenté avec sa raison et sa condition de suppression.

## 14. Markdown

La documentation Markdown doit porter :

- titre ;
- objectif ;
- statut ;
- date/version lorsque périssable ;
- source/provenance ;
- ce qui est normatif vs informatif ;
- liens vers artefacts.

Ne pas laisser plusieurs documents concurrents sans statut de supersession.

## 15. Variables d'environnement

Chaque variable doit être enregistrée dans un catalogue :

- nom ;
- consommateur ;
- type ;
- obligatoire ;
- valeur par défaut ;
- secret oui/non ;
- exemple non sensible ;
- environnement ;
- effet ;
- validation ;
- dépréciation.

`.env.example` ne suffit pas s'il n'explique pas la sémantique.

## 16. Fichiers de configuration

Chaque config doit préciser :

- source de vérité ;
- override precedence ;
- reload ou restart requis ;
- portée ;
- sécurité ;
- validation ;
- fallback ;
- exemple.

## 17. Tests

### Tests unitaires

Doivent expliquer les invariants locaux.

### Tests d'intégration

Doivent documenter les frontières et fixtures.

### E2E

Doivent correspondre aux Golden Journeys réels.

### Tests sécurité/négatifs

Doivent couvrir explicitement :

- refus d'autorité ;
- isolation tenant ;
- non-egress ;
- STOP ;
- secret redaction ;
- inputs invalides ;
- retry/failure.

## 18. Migrations de données

En plus du SQL :

- source ;
- destination ;
- mapping ;
- données perdues ou normalisées ;
- contrôle avant/après ;
- reprise en cas d'interruption ;
- sauvegarde ;
- métriques de succès.

## 19. API et protocoles

Documenter avec OpenAPI/JSON Schema/protobuf ou contrat équivalent lorsque possible.

Le contrat doit inclure :

- version ;
- auth ;
- permissions ;
- rate limits ;
- timeout ;
- erreurs ;
- idempotence ;
- pagination ;
- data classification ;
- compatibilité.

## 20. Fichiers générés

Header ou index externe obligatoire :

`GENERATED — DO NOT EDIT — source: ... — command: ...`

Si un fichier généré est édité manuellement, le système doit considérer cela comme une dette ou une erreur.

## 21. Binaires / médias / assets

L'index doit documenter :

- type ;
- finalité ;
- source ;
- licence/droits ;
- hash si critique ;
- consommateur ;
- régénération/remplacement.

## 22. Bonnes pratiques transverses

Quel que soit le langage :

- simplicité avant magie ;
- interfaces explicites ;
- erreurs visibles ;
- sécurité deny-by-default ;
- tests déterministes ;
- pas de secret en code ;
- dépendances minimales ;
- versions maîtrisées ;
- logs structurés ;
- code mort retiré ou marqué ;
- TODO avec issue/rationale, pas TODO éternel ;
- dépréciation explicite ;
- compatibilité documentée ;
- rollback pensé avant mutation.

## 23. Revue IA spécifique au langage

Avant commit, l'IA doit produire ou vérifier :

- formatter ;
- linter ;
- type checker/compile ;
- tests ;
- security/static analysis disponible ;
- docs publiques ;
- FILE_INDEX ;
- dépendances ;
- changelog/ADR si nécessaire.

Le jeu exact de commandes dépend du dépôt et doit être documenté dans `docs/TESTING.md`.
