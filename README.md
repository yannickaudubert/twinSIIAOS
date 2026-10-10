# twinSIIAOS

`twinSIIAOS` est le tronc public et generique du travail SIIAOS autour du jumeau numerique contextuel, des capacites humaines et numeriques, et de leur mise en action gouvernee.

Version courante : `0.1.0-alpha.1`.

## Principe

Le systeme ne part pas d'une liste d'outils. Il part d'une personne, d'un contexte, d'un besoin et des responsabilites qu'elle souhaite conserver ou deleguer.

Le premier jour doit donc respecter l'ordre suivant :

1. accueil sans scan implicite ;
2. contexte minimal declare par l'utilisateur ;
3. objectif ou besoin concret ;
4. choix des responsabilites ;
5. proposition explicite du perimetre d'observation ;
6. consentement humain ;
7. decouverte des capacites existantes ;
8. calcul d'un premier chemin vers une capacite utile ;
9. preuve ;
10. capitalisation eventuelle.

## Separation des mondes

- **ARAGORN** : instance locale reelle, laboratoire et machine de Yannick. Elle peut contenir des chemins, services, secrets, traces et donnees qui ne doivent jamais etre publies par defaut.
- **twinSIIAOS** : contrats, documentation, schemas, exemples anonymises, interfaces generiques et code reproductible.
- **Commun mondial** : ce qui peut etre publie apres distillation, qualification de provenance, licence et validation humaine.

## Regles cardinales

- aucun scan profond au premier lancement ;
- aucune donnee ARAGORN en valeur par defaut ;
- aucune action irreversible sans validation humaine ;
- aucune promotion automatique vers un commun ;
- chaque fait doit etre qualifie : `declared`, `observed`, `inferred`, `proposed`, `validated` ;
- chaque capacite doit pouvoir decrire preuves, couts, risques, dependances et rollback ;
- reutiliser l'existant avant d'ajouter une brique ;
- une interface n'est jamais la source de verite ; elle projette des objets canoniques.

## Arborescence initiale

```text
contracts/       schemas publics
examples/        exemples neutres
 docs/           doctrine operatoire, First Day, ADR, roadmap
```

Le code d'execution ne sera importe qu'apres verification des frontieres, suppression des valeurs historiques ARAGORN et definition d'un contrat d'adaptation avec les surfaces locales existantes.

## Statut de licence

Le depot est public, mais la licence libre definitive du noyau n'est pas encore choisie. Aucune release executable canonique ne doit etre annoncee avant cette decision. Voir `docs/LICENSE-DECISION.md`.

## Auteur et gouvernance

Conception d'origine : Yannick Audubert.

Les contributions IA, methodologiques ou editoriales sont des contributions au projet et ne revendiquent aucune copropriete sur l'architecture d'origine.
