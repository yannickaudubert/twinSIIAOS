# SandY — plan de travail Radar Core

Objectif : faire de SandY la source de vérité opérationnelle du Radar SIIAOS sans dépendre de Vercel, tout en réutilisant la V3 et le catalogue déjà publié sur le site consultant.

## 0 — préflight obligatoire sur SandY

Avant toute création de dossier :

- inventorier les clones Git existants et leurs branches ;
- rechercher un éventuel `radar-core`, `twinSIIAOS`, `resource-radar` ou équivalent déjà présent ;
- vérifier l'emplacement réel du SIIAOS local ;
- ne jamais écraser ou déplacer un actif existant automatiquement ;
- produire un rapport de préflight versionnable.

La cible `D:\SIIAOS\radar-core` ci-dessous reste une **cible**, pas un fait observé.

## A — conserver la V3 fonctionnelle

Conserver sans régression :

- recherche live multi-sources ;
- résolution d'artefacts ;
- file de mirroring ;
- génération de commandes multi-OS ;
- manifeste JSON ;
- bridge localhost + token ;
- séparation téléchargement / installation ;
- SHA-256 ;
- contrôle de la racine de destination.

La V4 est une extension de la V3, pas un remplacement réécrit.

## B — créer le Radar Core local

Arborescence cible proposée :

```text
D:\SIIAOS\radar-core\
  registry\
    resources\
    approaches\
    capabilities\
  signals\
  observations\
  benchmarks\
  evidence\
  decisions\
  gaps\
  projections\
  manifests\
  inbox\
  reports\
  logs\
```

Chaque ressource doit disposer d'un `id` canonique stable. Les correspondances avec les interfaces publiques sont explicites dans `projection_keys`, notamment `consultant_slug` : pas de rapprochement automatique sur le seul nom.

## C — protocole bridge V4

Étendre le bridge sans exécution shell arbitraire :

- `GET /health` : santé et version, sans exposer le chemin local complet ;
- `GET /tasks` : téléchargements ;
- `POST /batch` : téléchargement V3 ;
- `POST /ingest/manifest` : déposer un manifeste dans une inbox locale ;
- `GET /registry/summary` : statistiques non sensibles ;
- `POST /observations` : accepter des observations structurées ;
- `GET /exports/radar-public` : servir la dernière projection publique générée ;
- `GET /exports/consultant-site` : servir l'enrichissement compatible site consultant.

Garde-fous à ajouter :

- CORS limité au domaine Radar de production et aux origines localhost de développement ;
- token requis pour toute opération autre que santé minimale ;
- plafond du nombre d'items par batch ;
- limite de taille configurable par artefact ;
- limite de concurrence ;
- refus par défaut des cibles loopback, link-local et réseaux privés pour les URLs de téléchargement afin d'éviter qu'une ressource publique fasse du bridge un proxy interne ;
- allowlist/override explicite si une source privée locale doit être autorisée ;
- téléchargement atomique `.part` puis renommage ;
- hash SHA-256 vérifié lorsqu'il est fourni ;
- journal d'événement et manifeste de résultat ;
- aucun endpoint d'exécution de commande.

## D — modèle canonique

Valider chaque ressource contre `contracts/resource-record.schema.json`.

Premiers objets à importer :

1. systèmes déjà présents dans `StackCatalogData` du site consultant ;
2. 41 sources connues de la V3 ;
3. résultats de recherche live **après qualification**, pas l'intégralité du bruit brut ;
4. ressources effectivement installées/testées sur SandY ;
5. capability gaps issus des travaux SIIAOS ;
6. approches architecturales concurrentes lorsqu'une innovation remet en cause plusieurs briques à la fois.

Ne jamais déduire `tested` ou `qualified` d'une simple présence dans un catalogue.

## E — produire les projections

Le script stdlib `local/export_projections.py` produit :

```text
projections/consultant-site.json
projections/radar-public.json
projections/export-report.json
```

Exemple de lancement une fois les chemins réels confirmés :

```powershell
py .\resource-radar-v4\local\export_projections.py `
  --registry "D:\SIIAOS\radar-core\registry" `
  --out "D:\SIIAOS\radar-core\projections" `
  --fit-context sandy
```

`consultant-site.json` n'écrit pas les textes éditoriaux du site. Il ne fournit que l'enrichissement de qualification lié par `consultant_slug`.

## F — Git bridge et promotion

Flux cible :

```text
SandY local
   ↓
validation des contrats
   ↓
export des projections
   ↓
diff local
   ↓
branche Git
   ↓
CI + preview
   ↓
revue humaine
   ↓
merge
   ↓
Vercel
```

Ne jamais publier directement le registre riche de SandY vers Vercel.

Le repo `site` reçoit seulement la projection consultant dans :

```text
content/stack-catalog/radar-qualification.json
```

Le site superpose cette projection à son catalogue éditorial existant au moment de la lecture.

## G — boucle bidirectionnelle site ↔ Radar

Le site consultant apporte au Radar :

- capacités SI ;
- topologies ;
- décisions d'architecture ;
- effets organisationnels ;
- cas d'usage et limites éditorialisées.

Le Radar apporte au site :

- état de preuve ;
- position champion/challenger/candidate ;
- fit contextualisé ;
- date de dernière vérification ;
- plateformes réellement testées ;
- résumé de benchmark ;
- gaps connus ;
- tendance ;
- nombre de preuves publiables.

Aucun des deux produits ne devient la base de l'autre : ils projettent le même noyau et s'enrichissent par contrats.

## H — premier benchmark d'intégration

Lot initial : 10 ressources déjà présentes dans le catalogue consultant.

Pour chacune :

1. associer un `id` canonique et `projection_keys.consultant_slug` ;
2. distinguer ce qui est seulement observé de ce qui est installé/testé ;
3. ajouter un fit SandY uniquement s'il existe une observation ou un test ;
4. lier preuves et benchmark ;
5. produire les deux projections ;
6. vérifier le diff ;
7. vérifier l'absence de régression du site ;
8. vérifier l'affichage enrichi du Radar ;
9. vérifier qu'une ressource `never_publish`, locale privée ou client-specific ne fuit dans aucun export.

## I — critères de sortie du lot 1

Le lot est acceptable seulement si :

- la V3 n'a perdu aucune fonction ;
- les projections sont reproductibles ;
- une donnée absente n'est pas affichée comme vraie ;
- le site fonctionne avec une projection vide ;
- les deux projections sont reconstructibles depuis le registre ;
- aucun chemin local, token, log brut ou donnée client n'est exposé ;
- rollback = retrait de la projection / retour au commit précédent, sans migration destructive du catalogue éditorial.
