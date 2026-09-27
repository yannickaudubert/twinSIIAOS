# ADR-005 — Réponse complexe et routage de mobilisation

## Statut

Accepted for implementation on `radar-v5-saas-augmentation`.

## Problème

Le Resource Radar V5 ne peut pas s'arrêter à une fiche ressource ou à un Execution Plan. Ses réponses sont par nature contextuelles et peuvent révéler :

- une solution réalisable immédiatement en self-service local ;
- un besoin d'arbitrage ou d'expertise humaine ;
- une mission de transformation ou de delivery ;
- un besoin multidisciplinaire ;
- une situation territoriale ou collective ;
- un manque de preuve qui interdit encore toute mobilisation.

Le routage ne doit jamais devenir un tunnel commercial automatique.

## Décision

La réponse V5 suit quatre couches :

```text
Facts / Evidence
      ↓
Contextual Analysis
      ↓
Execution + Admission
      ↓
Mobilization Routes
```

Les routes canoniques sont :

1. `siiaos_local` — self-service, agents, outils, modèles et services locaux ;
2. `yannick_consultant` — arbitrage, expertise, relation, diagnostic, engagement ou décision dans son périmètre ;
3. `cabinet_augmente` — mission structurée, delivery, transformation, POC/MVP, administration et capitalisation portés par le cabinet augmenté ;
4. `agoria_collective` — mobilisation fédérée d'un ou plusieurs domaines humains autonomes, avec mandat, pilote, contributeurs, droits et responsabilités explicites ;
5. `no_activation` — preuve, contexte ou autorité insuffisante ; le Radar doit d'abord demander/produire l'information manquante.

## Invariants

### R1 — self-service avant mobilisation commerciale

Une capacité déjà disponible localement et admissible ne doit pas être transformée artificiellement en mission payante.

### R2 — faisabilité n'est pas autorité

Un plan techniquement faisable ne donne pas le droit de l'exécuter ni de mobiliser un tiers.

### R3 — mobilisation minimale

Le routeur doit proposer le plus petit périmètre humain suffisant. AgorIA n'implique pas quatre personnes : un seul domaine peut suffire.

### R4 — AgorIA reste fédérée

AgorIA ne devient ni le backend, ni le runtime, ni l'autorité du SIIAOS ou du cabinet. Le Radar propose une route ; l'activation exige un mandat.

### R5 — cabinet augmenté distinct de Yannick consultant

`yannick_consultant` concerne expertise, arbitrage, relation et engagements personnels. `cabinet_augmente` concerne une mission structurée pouvant mobiliser systèmes, agents, delivery et opérations.

### R6 — preuve de la raison de mobilisation

Toute route autre que `siiaos_local` doit exposer :
- ce qui manque au self-service ;
- les capacités humaines ou organisationnelles nécessaires ;
- le niveau de mandat attendu ;
- les données partageables et celles qui restent locales ;
- le HumanGate éventuel.

### R7 — pas de score global de complexité

La complexité reste multidimensionnelle : technique, organisation, finance, droit/réglementaire, sécurité, données, changement humain, territoire/écosystème, urgence. Une dimension forte peut suffire à changer la route.

### R8 — pas d'activation automatique

Une route est une proposition. Contacter, engager, partager un ContextPack ou créer une mission nécessite l'autorité correspondante.

## Chaîne cible

```text
Need / Question
  -> Radar Response
  -> Evidence + Unknowns
  -> Execution Feasibility
  -> Organisational Admission
  -> Mobilization Routing
  -> HumanGate / Mandate
  -> Mission
  -> Team / Agents / Tools
  -> Operations
  -> Evidence / RETEX
```

## Frontières

### SIIAOS local
Peut observer, analyser, simuler, préparer, exécuter dans ses permissions et produire des preuves.

### Yannick consultant
Intervient lorsque jugement professionnel, relation, arbitrage, engagement, représentation ou mandat personnel sont requis.

### Cabinet augmenté
Transforme le besoin en mission structurée et mobilise la fabrique agentique / delivery / administration du cabinet.

### AgorIA
Fédère des capacités humaines autonomes. Le Radar décrit les domaines nécessaires, jamais une mobilisation implicite de personnes nommées.

## Gate de release

La V5 ne peut pas être considérée prête si :
- un cas self-service suffisant déclenche une route cabinet/AgorIA sans justification ;
- une route AgorIA ne porte pas de mandat ;
- une route externe publie un contexte privé par défaut ;
- une situation unknown déclenche une mission comme si elle était qualifiée ;
- les raisons de routage ne sont pas auditables.
