# SIIAOS Resource Radar V4 — convergence

Cette branche prépare la convergence entre :

- **SandY / SIIAOS local** : source de vérité riche, qualification, benchmark, preuves, exécution et historique ;
- **SIIAOS Resource Radar public** : surface technique vivante, hyperveille, recherche multi-sources, challengers et ressources exploitables ;
- **site consultant Yannick Audubert** : projection décisionnelle et éditoriale pour dirigeants, DSI et consultants.

## Principe directeur

Les deux sites publics ne maintiennent pas leur propre vérité. Ils consomment des **projections** d'un référentiel canonique SIIAOS.

```text
Sources externes
    ↓
Hyperveille
    ↓
Signals / observations
    ↓
SIIAOS Radar Core sur SandY
    ├─ registry
    ├─ knowledge graph
    ├─ capability graph
    ├─ gaps
    ├─ fit assessments
    ├─ benchmarks
    ├─ evidence
    └─ decisions
    ↓
Publication Gate
    ├─ projection radar-public
    └─ projection consultant-site
```

## Ce que V4 ajoute à la V3

La V3 sait déjà rechercher des sources live, résoudre des artefacts, constituer une file de mirroring et envoyer des téléchargements vers un bridge local sécurisé.

V4 garde ces fonctions et ajoute la **qualification architecturale** :

- Capability / Approach / System / Model / Agent / Runtime / Source / Signal / Gap / Benchmark / Evidence / Decision / Workload ;
- états `observed`, `installed`, `tested`, `qualified`, `target`, `candidate`, `deprecated` ;
- positions `champion`, `challenger`, `candidate`, `experimental`, `retired` ;
- fit SIIAOS et fit par contexte ;
- gaps connus et contournements ;
- liens de preuve ;
- blast radius architectural ;
- trajectoire et dynamique d'un projet, pas seulement sa popularité absolue ;
- publication différenciée entre local, Radar public et site consultant.

## Contrats

Le contrat canonique minimal est décrit dans :

- `contracts/resource-record.schema.json`
- `contracts/publication-projection.md`
- `local/SANDY-WORKPLAN.md`

## Règle de souveraineté

Le local reste maître. Vercel est une surface de publication, jamais la base de connaissance interne. Une indisponibilité du Radar public ou du site consultant ne doit pas interrompre Hyperveille, la qualification ou l'exécution locale.

## Réutilisation

Ne pas réécrire la V3. Les fonctions actuelles doivent être reprises comme modules :

1. recherche live multi-sources ;
2. résolution d'artefacts ;
3. file miroir ;
4. génération multi-OS ;
5. bridge local ;
6. hash et manifeste.

V4 enrichit ces fonctions avec le référentiel, les évaluations et les projections.
