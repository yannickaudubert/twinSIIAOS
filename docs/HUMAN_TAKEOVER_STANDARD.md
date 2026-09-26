# Standard SIIAOS de reprise humaine du code et des systèmes

**Version documentaire : 2026-09-26**  
**Statut : contrat transverse de réversibilité humaine**  
**Principe d'autorité : l'humain doit pouvoir comprendre, reprendre, modifier, tester, arrêter, restaurer et remplacer le système sans dépendre de l'IA qui l'a produit.**

## 1. Principe fondamental

Un code ou un système n'est pas terminé s'il fonctionne uniquement parce qu'une IA, un auteur historique ou une conversation passée sait comment il fonctionne.

La Definition of Done documentaire est :

`COMPRENDRE -> LOCALISER -> EXPLIQUER -> MODIFIER -> TESTER -> OBSERVER -> RESTAURER -> RETIRER`

Chaque étape doit être réalisable par un humain compétent à partir du dépôt, de la documentation et des preuves disponibles.

## 2. Portée

Ce standard s'applique à :

- dépôts et monorepos ;
- applications ;
- services ;
- workers ;
- bibliothèques ;
- scripts ;
- migrations ;
- configurations ;
- workflows CI/CD ;
- conteneurs ;
- bases et schémas ;
- modèles de données ;
- agents et workflows IA ;
- MCP et connecteurs ;
- interfaces ;
- traitements batch ;
- fichiers documentaires structurants ;
- artefacts générés dont la régénération est nécessaire au fonctionnement.

Il s'applique au code produit par un humain, une IA ou les deux.

## 3. Règle de documentation à quatre niveaux

### Niveau S0 — Système

Chaque système possède une fiche expliquant :

- finalité ;
- utilisateurs ;
- non-objectifs ;
- contexte métier ;
- architecture ;
- frontières ;
- dépendances ;
- flux ;
- données ;
- autorité ;
- sécurité ;
- déploiement ;
- observabilité ;
- backup/restore ;
- rollback ;
- modes dégradés ;
- tests ;
- exploitation ;
- succession / retrait ;
- statut de vérité.

### Niveau S1 — Dépôt

Chaque dépôt doit permettre de répondre immédiatement à :

1. Pourquoi ce dépôt existe-t-il ?
2. Quel système ou quelle capability fournit-il ?
3. Quelles parties sont canoniques, dérivées, générées, historiques ou expérimentales ?
4. Comment le construire ?
5. Comment le lancer ?
6. Comment le tester ?
7. Comment le diagnostiquer ?
8. Comment le sauvegarder/restaurer ?
9. Comment le faire évoluer ?
10. Comment le retirer ou le remplacer ?

Minimum attendu à la racine :

- `README.md`
- `AGENTS.md` ou équivalent de règles IA/humain
- `docs/ARCHITECTURE.md`
- `docs/OPERATIONS.md`
- `docs/SECURITY.md`
- `docs/TESTING.md`
- `docs/DEPENDENCIES.md`
- `docs/FILE_INDEX.md`
- `docs/CHANGE_AND_ROLLBACK.md`

Ces fichiers peuvent être fusionnés dans un dépôt petit, mais toutes les questions doivent rester couvertes.

### Niveau S2 — Composant / répertoire

Tout répertoire significatif possède un point d'entrée qui explique :

- responsabilité ;
- frontières ;
- API/contrats ;
- dépendances entrantes/sortantes ;
- données lues/écrites ;
- effets de bord ;
- tests ;
- règles de modification ;
- principaux fichiers.

Pour un répertoire simple, un `README.md` local suffit.

### Niveau S3 — Fichier individuel

Chaque fichier suivi par Git doit être explicable.

L'explication peut être :

- dans le fichier, via docstring/header approprié ;
- dans `docs/FILE_INDEX.md` ;
- dans un manifeste généré et versionné ;
- ou par combinaison des trois.

Chaque entrée de fichier doit au minimum indiquer :

- chemin ;
- nature ;
- responsabilité ;
- statut : source / config / test / migration / generated / asset / documentation ;
- propriétaire logique ou composant ;
- entrées ;
- sorties ;
- effets de bord ;
- dépendances importantes ;
- contrat/API exposé si applicable ;
- invariants ;
- sécurité / données sensibles ;
- test associé ;
- mode de régénération si généré ;
- risques de modification ;
- statut de documentation.

## 4. Ne pas sur-commenter le code

La reprise humaine ne signifie pas ajouter un commentaire à chaque ligne.

Les commentaires doivent expliquer :

- **pourquoi** ;
- invariants ;
- décisions non évidentes ;
- compromis ;
- conséquences ;
- contraintes externes ;
- sécurité ;
- algorithmes complexes ;
- comportements surprenants.

Ils ne doivent pas paraphraser la syntaxe.

Mauvais :

`// increment counter`

Bon :

`// Keep this counter monotonic: OperationRecord IDs are used to preserve replay order after recovery.`

## 5. Documentation du code public et des frontières

Toute API publique ou frontière inter-composants doit documenter :

- contrat d'entrée ;
- contrat de sortie ;
- erreurs ;
- effets de bord ;
- idempotence ;
- timeout/retry ;
- sécurité ;
- versionnement ;
- compatibilité ;
- exemples minimaux lorsque nécessaire.

Pour une fonction privée évidente, le nom, les types et la structure doivent suffire.

## 6. Règle IA

Avant de modifier un fichier, une IA doit pouvoir expliquer :

1. son rôle ;
2. ses appelants ;
3. ses dépendances ;
4. les tests qui le couvrent ;
5. les invariants à préserver ;
6. la convention du langage ;
7. le rollback ou l'effet d'un revert.

Si l'un de ces éléments est inconnu, l'IA doit l'indiquer et réduire son périmètre au lieu d'inventer.

Après modification, elle doit mettre à jour la documentation concernée lorsque la compréhension, le contrat ou l'exploitation ont changé.

## 7. Human-in-the-loop obligatoire

L'IA peut :

- inventorier ;
- expliquer ;
- proposer ;
- rédiger la documentation ;
- générer des diagrammes ;
- produire des tests ;
- détecter la dette ;
- suggérer des refactorings.

L'humain conserve :

- les décisions d'architecture structurantes ;
- les changements de source de vérité ;
- les migrations destructives ;
- les suppressions ;
- les ruptures d'API ;
- les changements de licence ;
- les changements de sécurité/autorité ;
- la promotion en production.

## 8. États documentaires

Chaque élément peut porter :

- `DOCUMENTED`
- `PARTIAL`
- `UNKNOWN`
- `STALE`
- `GENERATED`
- `SUPERSEDED`
- `NOT_APPLICABLE`

Et séparément son truth status :

`PROPOSED / CODED / TESTED / DEPLOYED / OBSERVED / PROVEN`

Documentation et état runtime ne doivent jamais être confondus.

## 9. Provenance

Une explication doit distinguer :

- comportement déduit du code ;
- comportement couvert par test ;
- comportement observé au runtime ;
- décision humaine ;
- hypothèse ;
- historique obsolète.

Une affirmation générée par une IA n'est pas une preuve indépendante.

## 10. Generated files, lockfiles et assets

Ils ne sont pas dispensés d'explication.

Pour un fichier généré, documenter :

- générateur ;
- source ;
- commande de régénération ;
- version outil ;
- possibilité ou interdiction d'édition manuelle.

Pour un lockfile :

- outil propriétaire ;
- commande normale de mise à jour ;
- politique de commit ;
- rôle dans la reproductibilité.

Pour un asset :

- rôle ;
- source/licence si nécessaire ;
- consommateur ;
- règles de remplacement.

## 11. Tests comme documentation exécutable

Pour chaque comportement critique :

- au moins un test doit montrer le comportement nominal ;
- un test négatif doit couvrir les interdits importants ;
- le nom du test doit décrire le comportement attendu ;
- le lien fichier -> test doit être retrouvable.

Les tests ne remplacent pas la documentation ; ils la corroborent.

## 12. Architecture Decision Records

Toute décision difficile à deviner dans le code doit avoir un ADR :

- contexte ;
- options ;
- décision ;
- raisons ;
- conséquences ;
- alternatives rejetées ;
- conditions de réouverture.

Une IA ne doit pas transformer un compromis local en doctrine globale sans ADR.

## 13. Dette de documentation

La dette documentaire est traitée comme dette technique.

Classes :

- `P0` : sécurité, autorité, données, restore ou comportement critique incompris ;
- `P1` : module actif non reprenable humainement ;
- `P2` : fichier important insuffisamment expliqué ;
- `P3` : amélioration de lisibilité ou exemples.

Un P0 bloque la promotion.

## 14. Gate de revue

Une PR modifiant du code n'est pas complète si elle introduit :

- un nouveau fichier non indexé ;
- une nouvelle dépendance non documentée ;
- une nouvelle variable d'environnement non décrite ;
- une nouvelle migration sans impact expliqué ;
- une nouvelle API sans contrat ;
- un nouveau workflow sans runbook ;
- un nouveau secret sans modèle de gestion ;
- un comportement critique sans test ;
- une rupture de reprise/restore ;
- une complexité que seul l'auteur ou l'IA sait expliquer.

## 15. Handoff humain

Une personne découvrant le système doit pouvoir, depuis le dépôt :

### En 15 minutes

- identifier sa finalité ;
- comprendre les composants ;
- trouver les points d'entrée ;
- voir les risques et dépendances.

### En 2 heures

- lancer l'environnement de développement ;
- exécuter les tests ;
- suivre un flux principal ;
- identifier où modifier un comportement.

### En 1 journée

- effectuer une petite modification ;
- ajouter ou adapter un test ;
- observer le résultat ;
- produire une PR cohérente ;
- revenir en arrière.

### En cas d'incident

- savoir arrêter ;
- diagnostiquer ;
- restaurer ;
- retrouver la dernière preuve saine.

## 16. Critère de succession

Un système est considéré transmissible uniquement si un humain n'ayant pas participé à sa conception peut, sans conversation privée avec l'auteur ou l'IA :

1. reconstruire l'environnement ;
2. comprendre les frontières ;
3. expliquer le chemin critique ;
4. modifier un comportement borné ;
5. lancer les tests ;
6. diagnostiquer un échec ;
7. restaurer les données ;
8. retirer ou remplacer une dépendance.

## 17. Principe final

`AI-assisted != AI-dependent`

Le SIIAOS peut utiliser massivement l'IA pour produire et maintenir le code. Il ne doit jamais créer une dépendance cognitive où l'humain perd la capacité de comprendre et reprendre son propre système.
