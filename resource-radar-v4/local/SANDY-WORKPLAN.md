# SandY — plan de travail Radar Core

Objectif : faire de SandY la source de vérité opérationnelle du Radar SIIAOS sans dépendre de Vercel.

## Phase A — conserver la V3 fonctionnelle

- récupérer `siiaos_bridge.py` V3 ;
- conserver le port localhost et le token ;
- conserver la séparation téléchargement / installation ;
- conserver SHA-256 et racine de destination contrôlée ;
- ne pas casser les commandes multi-OS ni le manifeste actuel.

## Phase B — créer le Radar Core local

Arborescence cible proposée :

```text
D:\SIIAOS\radar-core\
  registry\
  signals\
  observations\
  benchmarks\
  evidence\
  decisions\
  gaps\
  projections\
  manifests\
  logs\
```

Le chemin est une cible proposée : vérifier l'état réel de SandY avant création et éviter tout doublon avec les dossiers SIIAOS déjà existants.

## Phase C — protocole bridge V4

Ajouter au bridge sans exécution shell arbitraire :

- `GET /health` : santé et version ;
- `GET /tasks` : téléchargements ;
- `POST /batch` : téléchargement V3 ;
- `POST /ingest/manifest` : déposer un manifeste dans une inbox locale ;
- `GET /registry/summary` : statistiques non sensibles ;
- `POST /observations` : accepter des observations structurées ;
- `GET /exports/radar-public` : générer/servir la projection publique ;
- `GET /exports/consultant-site` : générer/servir l'export compatible site.

Aucun endpoint ne doit permettre d'exécuter une commande arbitraire.

## Phase D — modèle canonique

Valider chaque ressource contre `contracts/resource-record.schema.json`.

Premiers objets à ingérer :

1. les systèmes du `StackCatalogData` du site consultant ;
2. les 41 sources de la V3 ;
3. les résultats de recherche live qualifiés ;
4. les ressources effectivement testées sur SandY ;
5. les capability gaps identifiés dans le travail SIIAOS.

## Phase E — projections

Générer :

```text
projections/radar-public.json
projections/consultant-stack.json
projections/local-summary.json
```

Le second doit rester compatible avec le modèle du repo `yannickaudubert/site` pendant la migration.

## Phase F — Git bridge

SandY travaille localement puis propose des changements versionnés via Git.

Flux cible :

```text
SandY → export → branche Git → contrôles → revue humaine → merge → Vercel
```

Ne pas publier directement les données locales riches vers Vercel.

## Phase G — premier benchmark d'intégration

Test minimal :

- choisir 10 ressources déjà présentes dans la stack consultant ;
- enrichir avec état, fit, gaps et preuve ;
- produire les deux projections ;
- vérifier absence de régression sur le site ;
- vérifier affichage enrichi sur Radar V4 ;
- vérifier qu'une ressource privée n'apparaît dans aucune projection publique.
