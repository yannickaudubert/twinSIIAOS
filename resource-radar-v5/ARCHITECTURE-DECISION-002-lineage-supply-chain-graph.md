# ADR-002 — Lineage, provenance et supply-chain graph

## Statut

Accepted for V5 implementation.

## Contexte

La V4 modelise correctement les ressources, leurs capacites, leur etat, leur fit, leurs preuves et leurs projections. Elle reste cependant trop centree sur le noeud : `depends_on`, `replaces` ou `competes_with` sont encore essentiellement des listes de references.

Pour les modeles IA, datasets et composants OSS, une relation possede sa propre histoire : source, date, methode, confiance, preuve, version et politique de publication. La genealogie des modeles, les AI-BOM/SBOM, la provenance scientifique, les vulnerabilites et les observations runtime exigent donc que la relation devienne un objet de premier rang.

## Decision

V5 adopte trois objets canoniques separes :

1. **Resource Record** — l'objet identifie et ses proprietes relativement stables ;
2. **Lineage Edge** — une relation entre deux objets, avec provenance et preuve ;
3. **Observation** — un fait horodate brut ou derive, qui peut alimenter un noeud, une relation, un benchmark ou une decision.

Le stockage physique peut etre Neo4j, fichiers JSON/JSONL, SQLite ou autre. Aucun moteur n'est inscrit dans les contrats. Les contrats sont la frontiere stable.

## Regles

### R1 — source obligatoire

Toute relation publiee doit avoir une provenance. Une relation sans source peut exister comme brouillon local mais ne franchit pas le Publication Gate.

### R2 — inference explicite

`inferred` n'est jamais transforme silencieusement en `declared` ou `verified`.

### R3 — evidence chain

Une relation peut pointer vers plusieurs `evidence_ids`. Les decisions et scores doivent pouvoir remonter a leurs preuves puis, lorsque disponible, a l'observation brute.

### R4 — temporalite

Le graphe n'est pas suppose eternellement vrai. Les observations portent `observed_at` et eventuellement `expires_at`; une nouvelle observation peut `supersede` une precedente.

### R5 — publication par objet

Noeuds, relations et observations possedent leur propre niveau de visibilite. Le fait qu'un modele soit public ne rend pas publics nos benchmarks locaux, un client, un chemin local ou une decision interne.

### R6 — standards comme adapters

SPDX, CycloneDX, Croissant, OpenLineage ou les metadonnees Hugging Face sont ingeres par adapters. Le domaine SIIAOS ne reproduit pas aveuglement un standard externe et ne depend pas de son cycle de version.

### R7 — identifiants stables

Lorsque possible, les adapters conservent les identifiants amont (`repo`, revision, digest, SWHID, DOI, package URL, model id) comme aliases/projection keys, tout en emettant un identifiant SIIAOS stable.

## Relations prioritaires V5

### Genealogie IA

- `derived_from`
- `finetuned_from`
- `adapter_of`
- `merged_from`
- `distilled_from`
- `quantized_from`
- `converted_from`
- `trained_on`
- `evaluated_on`

### Supply-chain

- `implemented_by`
- `depends_on`
- `contains`
- `produces`
- `consumes`
- `signed_by`
- `attested_by`
- `archived_as`

### Connaissance / exploitation

- `cites`
- `observed_running_on`
- `replaces`
- `competes_with`
- `enables`

## Federation cible

```text
HF / CNIL -----------+
CycloneDX / SPDX ----+
Croissant -----------+
OpenLineage / MLflow-+--> adapters --> observations --> canonical graph
GitHub/ecosyste.ms --+
OSV/OpenSSF ---------+                         |
OpenAlex / SWH ------+                         +--> evidence
Sigstore ------------+                         +--> decisions
                                               +--> projections
```

## Consequences positives

- genealogie et supply-chain interrogables sans denormaliser les ressources ;
- comparaison entre declaration fournisseur et verification locale ;
- historique des changements ;
- meilleur audit RGPD/licence/securite ;
- possibilite de produire un Model Lineage Passport ou un AI-BOM compose ;
- separation stricte entre savoir public, savoir interne et savoir client.

## Couts / risques

- besoin de deduplication et resolution d'identite ;
- volume de relations potentiellement tres superieur au nombre de ressources ;
- contradictions entre sources ;
- necessite d'un modele de confiance et de fraicheur ;
- les standards externes evoluent.

Ces couts sont acceptes parce que V5 vise une intelligence de dependances et de transformation, pas un simple catalogue.

## Gate de deploiement

La branche de travail n'est pas un environnement de publication. Le cycle recommande est : Git -> tests -> captures/artifacts GitHub -> iterations -> commit release candidate -> un preview Vercel de recette -> convergence consultant/SIIAOS -> promotion validee.
