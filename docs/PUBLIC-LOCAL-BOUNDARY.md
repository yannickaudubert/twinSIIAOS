# Public / Local Boundary

Version: `0.1.0-alpha.1`

## Objectif

Empêcher qu'une instance locale, ses habitudes, ses chemins ou ses données deviennent implicitement le modèle d'un autre utilisateur.

## Local uniquement par défaut

Ne doivent jamais être publiés automatiquement :

- noms de machines ;
- chemins absolus ;
- utilisateurs système ;
- secrets, jetons, clés et identifiants ;
- données clientes ;
- contenus personnels ;
- inventaires réseau détaillés ;
- journaux contenant des données privées ;
- configurations révélant une infrastructure sensible ;
- faits observés sur ARAGORN présentés comme valeurs génériques.

## Public possible après distillation

Peuvent devenir publics après revue :

- contrats et schémas ;
- méthodes ;
- interfaces génériques ;
- tests sans données sensibles ;
- exemples fictifs ;
- adapters sans secrets ;
- Capability Passports génériques ;
- documentation de déploiement reproductible ;
- retours d'expérience anonymisés ;
- règles de gouvernance ;
- preuves synthétiques non sensibles.

## Règle de promotion

```text
LOCAL
  -> candidate
  -> redact
  -> generalize
  -> verify provenance
  -> verify license
  -> human review
  -> PUBLIC
```

Aucune étape ne peut être sautée par un agent.

## ARAGORN

ARAGORN est une instance de référence et un terrain de validation, pas un jeu de valeurs par défaut.

Les informations historiques ARAGORN doivent vivre dans un espace d'instance non distribué ou dans des fixtures explicitement marquées comme fictives.
