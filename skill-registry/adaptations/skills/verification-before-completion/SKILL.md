---
name: verification-before-completion
description: Imposer une vérification fraîche et adaptée avant toute affirmation de succès, correction, déploiement, publication, intégration ou achèvement. Utiliser dès que ChatGPT, Codex ou un agent est sur le point de dire qu'un travail est terminé, fonctionnel, corrigé, déployé, publié, intégré ou validé, après une mutation de code/document/workflow, après un rapport de succès d'un sous-agent, ou avant de clôturer une étape. Ne pas déclencher pour un simple brainstorming ou une réponse factuelle sans affirmation d'état de travail.
---

# Vérifier avant de conclure

## Principe

Ne jamais transformer une impression, une intention, un diff ou un rapport d'agent en preuve de réussite.

Distinguer systématiquement :

- `DEMANDE` : résultat attendu ;
- `PROPOSÉ` : solution ou changement envisagé ;
- `OBSERVÉ` : état constaté directement ;
- `RÉALISÉ` : mutation effectivement effectuée ;
- `VÉRIFIÉ` : résultat contrôlé par une preuve adaptée ;
- `BLOQUÉ` : condition empêchant la suite ;
- `INCONNU` : information non établie.

## Gate avant toute affirmation positive

Avant de dire qu'un travail est terminé, corrigé, fonctionnel, déployé, publié, intégré ou validé :

1. Identifier le critère exact que l'affirmation suppose.
2. Identifier la preuve qui démontrerait ce critère dans l'environnement concerné.
3. Produire ou lire cette preuve avec l'outil réellement disponible.
4. Vérifier le résultat complet et les erreurs pertinentes.
5. Comparer la preuve aux corrections et exigences déjà applicables.
6. Formuler l'état réel, même s'il est partiel ou négatif.

Si la preuve manque, dire ce qui est `RÉALISÉ` et ce qui reste `INCONNU À VÉRIFIER`. Ne pas combler le manque par une estimation.

## Adapter la preuve au type de travail

- **Code/tests** : exécuter le test, build ou linter réellement pertinent et lire son statut de sortie.
- **Web/interface** : vérifier le comportement dans le navigateur ou runtime demandé ; un build seul ne prouve pas l'expérience utilisateur.
- **Document/artefact** : confirmer l'existence du fichier, son ouverture/parsage et les critères de contenu ou de rendu demandés.
- **Déploiement** : distinguer commit poussé, build, déploiement et runtime observé. Git ne prouve jamais à lui seul l'état déployé.
- **Action externe** : exiger la réponse du système cible ou une trace équivalente.
- **Sous-agent** : considérer son « succès » comme une affirmation à vérifier indépendamment.

## Préserver les corrections autoritaires

Une correction explicite de l'utilisateur remplace l'état antérieur qu'elle corrige dans son périmètre. Avant de conclure, vérifier que le résultat n'a pas réintroduit une ancienne hypothèse ou version.

Une réponse antérieure de l'assistant n'est jamais une preuve indépendante.

## Éviter la vérification de façade

Ne pas lancer des tests sans rapport avec l'affirmation uniquement pour produire un signal vert. Une preuve doit pouvoir falsifier la conclusion envisagée.

Ne pas dire « tout est bon » lorsque seule une sous-partie est vérifiée. Nommer la frontière exacte : code, dépôt, build, déploiement, runtime, contenu, interface ou autre.

## Sortie attendue

Terminer avec trois éléments au maximum quand le contexte le permet :

- ce qui est effectivement fait ;
- la preuve qui le démontre ;
- le blocage ou l'inconnu résiduel éventuel.

Pour l'origine et la méthode d'adaptation, consulter `references/provenance.md` uniquement si la provenance du skill est pertinente.
