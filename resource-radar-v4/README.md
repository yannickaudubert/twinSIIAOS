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

## Shell V4 maintenant versionné

Le premier rendu professionnel est dans `resource-radar-v4/ui/`.

Il ne remplace pas encore la V3 déployée. Il sert à faire évoluer l'interface sous Git sans consommer un déploiement Vercel à chaque commit.

Vues déjà présentes :

- Radar ;
- Capacités ;
- Approches ;
- Paysages ;
- Hyperveille ;
- Acquérir ;
- Méthode ;
- teasers Expert : Fit, Comparateur, Evidence, Architecture, Décisions.

La direction visuelle est volontairement sobre : fond clair, navigation produit B2B, tables, états de preuve, timelines et cartes décisionnelles. La V4 ne reprend pas la DA cyberpunk/néon de la V3.

### Projection réelle et fixture de revue

L'interface lit par défaut :

`projections/radar-public.json`

Ce fichier est initialement vide. L'absence de données reste une absence de données : le shell n'invente pas de qualification.

Pour les seules captures de revue, `?fixture=1` charge :

`ui/fixtures/radar-public.demo.json`

La fixture porte explicitement `fixture: true` et une notice de non-publication. Elle sert à vérifier densité, états, responsive et navigation ; elle ne vaut ni benchmark ni qualification SandY.

## Aperçu visuel sans Vercel

Le workflow `.github/workflows/radar-v4-ui-preview.yml` construit un aperçu **uniquement dans GitHub Actions** :

1. valide les fichiers UI et les deux projections JSON ;
2. lance un serveur HTTP temporaire dans le runner ;
3. installe Chromium via Playwright ;
4. capture Radar desktop, Paysages, Expert Fit et mobile ;
5. publie les PNG et le site statique comme artifact GitHub pendant 14 jours.

Cela devient le cycle normal de chantier :

```text
commit Git
   ↓
Radar V4 CI + UI Preview
   ↓
artifacts / captures GitHub
   ↓
revue
   ↓
plusieurs itérations Git
   ↓
checkpoint montrable
   ↓
preview Vercel ponctuel seulement
```

Vercel reste donc une recette/publication, pas un compilateur déclenché à chaque modification.

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

Le read model du shell est :

- `projections/radar-public.json` — `siiaos.radar-public.v1`.

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
