# Capability Passport

Version: `0.1.0-alpha.1`

Un Capability Passport décrit une capacité comme un objet gouvernable. Il ne se limite ni à un logiciel ni à un agent.

## Schéma conceptuel

```yaml
capability:
  id: data.analysis
  title: "Analyser des données"
  purpose: []

  human:
    required_skills: []
    current_maturity: unknown
    learning_paths: []
    responsible_people: []

  technical:
    tools: []
    services: []
    apis: []
    databases: []
    models: []
    infrastructure: []

  governance:
    owner: null
    permissions: []
    secret_refs: []
    licenses: []
    confidentiality: unknown
    cost: unknown
    risks: []
    rollback: []

  lifecycle:
    state: discovered
    evidence: []
    deployment: []
    maintenance: []

  contribution:
    scope: local
    reusable_parts: []
    public_parts: []
    protected_parts: []
```

## États de cycle de vie

`discover -> understand -> learn -> experiment -> prove -> deploy -> adopt -> integrate -> operate -> capitalize -> generalize -> contribute`

Tous les états ne sont pas obligatoires pour chaque capacité, mais toute transition vers un état plus opératoire doit être justifiable par des preuves.

## Capacité effective

Une capacité technique disponible ne suffit pas.

La capacité effective dépend au minimum de :

- capacité humaine ;
- capacité technique ;
- capacité organisationnelle ;
- capacité juridique ;
- capacité opérationnelle.

Le système ne doit pas présenter une capacité comme acquise si l'une de ces dimensions bloque son usage réel.

## Responsabilité

Pour chaque capacité, l'utilisateur peut choisir ce qu'il souhaite :

- gérer lui-même ;
- partager ;
- mutualiser ;
- confier à un tiers ;
- confier à un service propriétaire ;
- ne pas activer.

Ce choix est une décision de responsabilité, pas un jugement moral.
