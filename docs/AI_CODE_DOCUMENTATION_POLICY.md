# Politique SIIAOS pour les IA qui modifient du code

**Version : 2026-09-26**  
**Statut : règle transverse de travail IA**  
**Référence : HUMAN_TAKEOVER_STANDARD.md**

## 1. Objectif

Toute IA qui lit, écrit, refactore, migre ou génère du code dans un dépôt SIIAOS doit préserver la possibilité de reprise humaine.

La responsabilité documentaire fait partie de la tâche de code.

## 2. Avant toute modification

L'IA doit établir, pour le scope concerné :

- fichier(s) visé(s) ;
- rôle ;
- composant ;
- appelants/consommateurs ;
- dépendances ;
- contrats ;
- données ;
- effets de bord ;
- autorité/sécurité ;
- tests existants ;
- convention du langage ;
- documentation existante ;
- risques de régression ;
- rollback/revert possible.

Si ces informations ne sont pas disponibles, elle doit les marquer `UNKNOWN` et réduire le scope.

## 3. Pendant la modification

L'IA doit :

- préserver les conventions du langage ;
- éviter la magie et les abstractions inutiles ;
- maintenir les types/schémas ;
- conserver ou améliorer les erreurs ;
- ne pas supprimer un commentaire expliquant un invariant sans le remplacer ;
- documenter toute décision non évidente ;
- ajouter/adapter les tests ;
- ne pas déplacer une responsabilité sans mettre à jour l'architecture.

## 4. Après la modification

Mettre à jour selon impact :

- FILE_INDEX ;
- README de composant ;
- API/OpenAPI/schema ;
- variables d'environnement ;
- dépendances ;
- diagrammes ;
- runbook ;
- sécurité ;
- tests ;
- ADR ;
- migration notes ;
- changelog/release note ;
- rollback.

Une modification de code qui rend la documentation fausse est une régression.

## 5. Fichiers nouveaux

Tout nouveau fichier doit recevoir :

- classification ;
- responsabilité ;
- composant ;
- langage/type ;
- test ou justification d'absence ;
- statut generated/non-generated ;
- sécurité ;
- entrée dans FILE_INDEX.

## 6. Fichiers supprimés

Avant suppression :

- retrouver consommateurs ;
- vérifier génération/remplacement ;
- identifier données/artefacts associés ;
- mettre à jour docs/index ;
- documenter migration ;
- garantir rollback lorsque nécessaire.

## 7. Refactoring

Un refactoring doit maintenir ou améliorer :

- comportement ;
- tests ;
- lisibilité ;
- documentation ;
- traçabilité.

Une IA ne doit pas refactorer uniquement pour satisfaire son style préféré.

## 8. Code généré

L'IA doit marquer clairement :

- ce qui est généré ;
- par quel outil/processus ;
- comment reproduire ;
- ce qui peut être édité manuellement.

Elle ne doit pas produire un fichier opaque dont elle seule connaît la génération.

## 9. Dépendances

Toute nouvelle dépendance doit documenter :

- besoin ;
- version ;
- licence ;
- fournisseur/source ;
- pourquoi le standard library/existant ne suffit pas ;
- surface d'attaque ;
- impact build/runtime ;
- alternative ;
- retrait.

## 10. Migrations

Toute migration doit inclure :

- raison ;
- forward path ;
- contrôle ;
- rollback ou irréversibilité ;
- backup ;
- impact ;
- tests.

## 11. Sécurité

L'IA ne doit jamais :

- documenter un secret en clair ;
- déplacer un secret dans un fichier versionné ;
- rendre une permission implicite ;
- ajouter une action destructive sans gate ;
- inventer une politique.

Les changements d'autorité, d'authentification ou de data boundary demandent une validation humaine.

## 12. Langage

L'IA doit appliquer les bonnes pratiques du langage décrites dans `LANGUAGE_AND_FILE_DOCUMENTATION_GUIDE.md`.

Si le langage n'est pas couvert :

1. identifier les conventions officielles/communautaires pertinentes ;
2. documenter la règle retenue ;
3. proposer son ajout au guide transverse ;
4. ne pas inventer une convention arbitraire.

## 13. Rapport de fin de tâche

Toute tâche de code doit produire :

- fichiers lus ;
- fichiers modifiés ;
- comportement changé ;
- comportement inchangé important ;
- documentation mise à jour ;
- tests/checks exécutés ;
- résultats ;
- UNKNOWN restants ;
- risques ;
- rollback.

## 14. Gate

Une IA doit considérer la tâche incomplète si :

- FILE_INDEX devient faux ;
- l'architecture devient fausse ;
- une API change sans documentation ;
- une config change sans documentation ;
- une dépendance apparaît sans justification ;
- un fichier critique n'a plus de test ;
- un humain ne peut plus expliquer le changement à partir du dépôt.

## 15. Règle ultime

L'IA optimise pour :

`capacité humaine future > commodité immédiate de l'agent`.

Elle est un accélérateur de développement, jamais le détenteur exclusif du savoir nécessaire pour maintenir le système.
