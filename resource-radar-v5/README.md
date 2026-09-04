# SIIAOS Resource Radar V5 — graph, lineage et supply-chain

V5 part de la V4 de convergence et conserve ses principes : **SandY / SIIAOS local reste la source de verite**, les surfaces publiques ne publient que des projections explicitement autorisees.

V5 ajoute une couche manquante : le Radar ne traite plus les ressources comme une liste d'objets independants. Il les represente comme un **graphe vivant de provenance, filiation, dependances, preuves, execution et usages**.

## Branche de travail et regle de publication

Branche de chantier :

`radar-v5-graph-convergence`

Regle :

```text
V4 convergence figee
        |
        v
V5 travail Git uniquement
        |
        +--> contrats / schemas
        +--> adapters / ingestion
        +--> tests / audits
        +--> UI / captures GitHub Actions
        |
        v
candidate V5 complete
        |
        v
UN SEUL preview Vercel de recette
        |
        +--> validation
        |
        v
convergence site consultant + site SIIAOS
```

Aucun commit de chantier V5 ne doit etre pousse vers le site consultant ni servir de publication publique. Vercel reste un **gate de recette**, pas l'environnement de developpement.

## Principe directeur V5

Chaque fait du Radar doit pouvoir repondre a cinq questions :

1. **Quoi ?** — quelle ressource, version ou capacite ?
2. **D'ou ?** — quelle source et quelle genealogie ?
3. **Pourquoi le croire ?** — quelle preuve, observation ou methode ?
4. **Dans quel contexte ?** — quel runtime, materiel, workload, client ou contrainte ?
5. **Peut-on le publier ?** — quelle visibilite et quelle projection ?

Une relation n'est jamais une verite nue. Elle porte au minimum :

- `source` ;
- `observed_at` ;
- `confidence` ;
- `method` ;
- `evidence_ids` ;
- `visibility`.

Cela permet de distinguer une relation declaree par un auteur, inferee automatiquement, importee d'un standard, observee en execution ou verifiee localement sur SandY.

## Graphe canonique

```text
External sources
   |
   +-- Hugging Face / Genmod
   +-- GitHub / ecosyste.ms / deps.dev
   +-- SPDX / CycloneDX
   +-- Croissant
   +-- OpenLineage
   +-- OpenAlex / Software Heritage
   +-- OSV / OpenSSF
   +-- Sigstore / provenance
   |
   v
Observations + Evidence
   |
   v
SIIAOS Canonical Graph
   |
   +-- Resource nodes
   +-- Lineage edges
   +-- Dependency edges
   +-- Dataset / training edges
   +-- Scientific links
   +-- Security / license signals
   +-- Runtime observations
   +-- Benchmarks / fit / decisions
   |
   v
Publication Gate
   +-- radar-public
   +-- consultant-site
   +-- local-only
```

## Model Lineage Passport

Pour les modeles IA, V5 construit un passeport compose au minimum de :

- identite, revision, hash, auteur et organisation ;
- famille et modele racine ;
- relations `finetune`, `adapter`, `merge`, `distillation`, `quantization`, `conversion` ;
- datasets declares ou detectes ;
- licences modele / donnees / code ;
- formats et runtimes ;
- exigences RAM / VRAM / CPU / GPU / NPU lorsqu'elles sont prouvees ;
- benchmarks publics et benchmarks SandY clairement separes ;
- signaux de securite et de supply-chain ;
- niveau d'ouverture : open source, open weights, source available, autre ;
- preuves et niveau de confiance de chaque relation ;
- fit par contexte SIIAOS.

## Standards et sources a federer

V5 prevoit des adapters, sans rendre le coeur dependant d'un fournisseur :

- CNIL Genmod : genealogie modeles / datasets ;
- Hugging Face metadata et model cards ;
- SPDX 3.x AI/Dataset profiles ;
- CycloneDX AI/ML-BOM ;
- Croissant pour la provenance des datasets ;
- OpenLineage pour les executions et transformations reelles ;
- MLflow pour nos runs, benchmarks et versions locales ;
- ecosyste.ms et deps.dev pour le graphe OSS ;
- OSV et OpenSSF Scorecard pour securite / hygiene projet ;
- Software Heritage pour les identifiants sources persistants ;
- OpenAlex pour la filiation scientifique ;
- Sigstore / attestations pour la provenance verifiable.

Les adapters sont **remplacables**. Le schema canonique SIIAOS est la frontiere stable.

## Contrats V5

V5 conserve les contrats V4 et introduit :

- `contracts/lineage-edge.schema.json` — relation graphe avec provenance et preuve ;
- `contracts/observation.schema.json` — observation horodatee issue d'une source ou d'un test ;
- `ARCHITECTURE-DECISION-002-lineage-supply-chain-graph.md` — architecture et regles de federation.

Le schema `resource-record.schema.json` reste le contrat du noeud. Les relations complexes sortent du noeud et deviennent des objets de premier rang afin d'eviter un JSON monolithique impossible a auditer.

## Vues produit V5

V5 conserve les vues V4 et ajoute progressivement :

- **Genealogie** : parents, descendants et transformations ;
- **Supply-chain** : code, packages, modeles, datasets, artefacts et attestations ;
- **Evidence graph** : pourquoi une affirmation est affichee ;
- **Openness** : niveau d'ouverture et contraintes de licence ;
- **Security posture** : vulnerabilites, hygiene, provenance et alertes ;
- **Scientific lineage** : papiers, auteurs, citations et implementations ;
- **Runtime reality** : ce qui a reellement ete installe, execute et mesure localement ;
- **Impact / remplacement** : dependances et composants qu'une nouvelle ressource peut remplacer ou simplifier.

## Phases de chantier

### V5.0 — baseline

- copie immuable de la V4 dans `resource-radar-v5/` ;
- branche dediee ;
- aucune publication Vercel.

### V5.1 — contrats graphe

- edge + observation ;
- identifiants canoniques ;
- provenance, preuve, confiance et visibilite ;
- compatibilite ascendante avec les projections V4.

### V5.2 — ingestion

- adapters externes ;
- normalisation ;
- deduplication ;
- conservation de la source brute et de la date d'observation.

### V5.3 — materialisation locale

- graphe local interrogeable ;
- stockage des preuves ;
- raccordement aux benchmarks et runs SandY ;
- aucune dependance obligatoire au cloud.

### V5.4 — experience Radar

- vues genealogie / supply-chain / preuves ;
- parcours humain simple avant profondeur experte ;
- export de passeports et BOM.

### V5.5 — qualification et recette

- tests de schemas ;
- audits humains / UX ;
- tests des projections ;
- verification qu'aucune donnee locale protegee ne fuit dans les projections publiques.

### V5.6 — release candidate

Une fois seulement la V5 complete et verte :

1. gel du commit candidat ;
2. generation des artefacts GitHub ;
3. preview Vercel ponctuel ;
4. recette fonctionnelle et visuelle ;
5. convergence avec `yannickaudubert/site` et la future surface SIIAOS ;
6. promotion uniquement apres validation.

## Invariants

- **local-first** : SandY continue de fonctionner sans Vercel ;
- **evidence-first** : une inference reste une inference ;
- **no fake data** : les fixtures ne deviennent jamais des preuves ;
- **projection-first** : les sites publics ne lisent pas la base locale brute ;
- **standards-aware, vendor-neutral** : on ingere les standards sans leur abandonner notre modele ;
- **version before deploy** : Git est la memoire du chantier, Vercel uniquement la recette finale.
