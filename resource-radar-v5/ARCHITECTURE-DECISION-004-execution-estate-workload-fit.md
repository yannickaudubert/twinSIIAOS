# ADR-004 — Execution Estate, Workload et plan d'execution

## Statut

Accepted for implementation on `radar-v5-saas-augmentation`.

## Contexte

Les versions precedentes du Radar qualifiaient surtout une ressource puis ajoutaient son `fit` dans un contexte. Cette logique est insuffisante pour un SIIAOS local-first : la configuration deja disponible chez l'utilisateur doit etre une entree structurante du raisonnement, pas une verification tardive.

Deux machines identiques n'offrent pas la meme capacite reelle si l'une dispose deja de runtimes, modeles, services, corpus, automatisations, graphes, politiques et preuves locales. Inversement, une fiche technique indiquant un besoin de VRAM superieur a la configuration ne suffit pas a conclure qu'une capacite est impossible : quantification, offload, decomposition, batching, RAG, outils deterministes et composition de briques peuvent rendre la charge faisable.

## Decision

V5 introduit une couche de decision d'execution composee de quatre contrats de premier rang :

1. **Execution Estate** — photographie datee des ressources réellement mobilisables par un utilisateur, une organisation, une machine ou un cluster ;
2. **Execution Profile** — exigences prouvees d'une ressource dans un mode d'execution donne ;
3. **Workload** — charge a accomplir, contraintes et capacites requises ;
4. **Execution Plan** — composition concrete Estate × Workload × Resources, avec gaps, substitutions, dependances externes et preuves.

Ces objets ne remplacent pas Resource Record / Lineage Edge / Observation. Ils les completent. Le graphe de ressources reste le catalogue canonique ; la couche d'execution transforme ce catalogue en plans faisables dans un contexte reel.

## Pipeline V5

```text
observe estate
  -> normalize resources
  -> describe workload
  -> decompose required capabilities
  -> match execution profiles
  -> compose candidate plans
  -> identify gaps
  -> search substitutions
  -> benchmark when needed
  -> preserve evidence
  -> qualify / reject plan
```

La compatibilite materielle n'est donc jamais assimilee a elle seule a la faisabilite d'une capacite.

## Invariants

### R1 — configuration avant recommandation

Une recommandation contextualisee ne peut pas etre qualifiee sans `estate_id` et `workload_id`.

### R2 — aucun score global artificiel

Le plan expose la faisabilite, les contraintes, le headroom mesure ou estime, les gaps et les preuves. Il ne produit pas un score universel qui masquerait les arbitrages.

### R3 — cout incremental explicite

Le budget disponible pour une charge est porte par le Workload. Un plan doit indiquer son cout incremental attendu. Lorsque le budget est zero, toute brique payante est soit exclue, soit marquee comme dependance externe optionnelle non necessaire au fonctionnement nominal.

### R4 — local-first testable

`local_first` et `external_provider_dependency_allowed` sont des politiques explicites. Une solution disant fonctionner localement doit pouvoir etre testee sans provider externe lorsque ces politiques l'exigent.

### R5 — preuves par mode d'execution

Les exigences RAM/VRAM/runtime et les performances varient selon quantification, backend, version, contexte et workload. Elles vivent donc dans Execution Profile avec leurs `evidence_ids`, jamais comme une verite unique attachee au nom du produit.

### R6 — configuration sensible

Un Execution Estate peut contenir des noms de machines, chemins, reseaux, services ou politiques internes. Sa visibilite est `local_private` par defaut. Aucune projection publique ne publie automatiquement un estate utilisateur.

### R7 — composition avant achat

Avant de declarer un gap non couvert, le moteur doit tester les substitutions raisonnables : outil deterministe, modele plus petit, quantification, RAG, decomposition, execution sequentielle, offload, autre runtime deja disponible ou composition de plusieurs ressources.

## Consequences produit

Le Radar peut desormais repondre a :

- que puis-je deja faire avec ce que je possede ?
- quelles capacites sont dormantes ?
- quelles ressources sont reellement compatibles avec mon contexte ?
- quelles briques peuvent etre combinees pour satisfaire la charge ?
- qu'est-ce qui manque reellement apres substitutions ?
- quelles dependances externes sont indispensables, optionnelles ou evitables ?

La V5 publique doit donc distinguer :

- **information publique sur les ressources** ;
- **configuration locale ou client** ;
- **qualification contextualisee** ;
- **plan d'execution prouve**.

## Gate de release

Une V5 ne peut pas etre consideree release candidate tant que :

1. les quatre contrats sont versionnes et testes ;
2. l'UI V5 expose clairement la logique Configuration -> Charge -> Execution ;
3. la CI empeche la fuite d'un Execution Estate prive vers `radar-public` ;
4. au moins un plan d'execution est produit a partir d'une configuration observee et d'un workload reel ;
5. les fonctions operationnelles V3 restent disponibles ou sont explicitement bloquees hors cut-over.
