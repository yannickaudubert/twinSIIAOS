# ADR-001 — Registre canonique local et projections publiques

## Statut

Proposé — branche `radar-v4-convergence`.

## Contexte

SIIAOS dispose déjà de deux surfaces utiles mais différentes :

1. le Resource Radar, orienté hyperveille, recherche live, artefacts, mirroring et évolution technique ;
2. le site consultant, orienté capacités SI, topologies, arbitrages, maturité, effets organisationnels et décision.

Les deux surfaces doivent s'améliorer mutuellement sans dupliquer leur source de vérité ni coupler leur rythme de publication.

## Décision

Le registre riche reste local-first sur SandY. Il contient les observations, preuves, benchmarks, fits, gaps, signaux, relations et états de qualification.

Les sites ne lisent pas directement ce registre. Ils reçoivent des projections minimales, versionnées et revues dans Git :

- `radar-public.json` : projection technique publique ;
- `consultant-site.json` : enrichissement de fiches déjà éditorialisées sur le site consultant.

Le catalogue éditorial du site consultant reste propriétaire de son texte, de sa structure SEO, de ses topologies et de ses arbitrages. Le Radar ne l'écrase pas ; il l'enrichit par clé stable `projection_keys.consultant_slug`.

## Règles

- Aucun signal brut ne devient automatiquement une recommandation.
- Aucun score ou état ne doit être inventé pour remplir l'interface.
- Une qualification absente reste absente à l'affichage.
- Toute donnée publique dérivée doit avoir une origine canonique et une date de génération.
- `observed`, `installed`, `tested`, `qualified`, `target`, `candidate`, `deprecated` restent distincts.
- `champion`, `challenger`, `candidate`, `experimental`, `retired` expriment une position compétitive, pas un état de preuve.
- Les données privées, clients, chemins locaux, logs bruts et artefacts sensibles ne doivent pas franchir le publication gate.
- Les projections doivent pouvoir être reconstruites depuis le registre local ; elles ne sont jamais la source de vérité.

## Flux cible

```text
Sources externes
      ↓
Hyperveille
      ↓
Signaux / observations
      ↓
Registre canonique SandY
      ├── preuves
      ├── benchmarks
      ├── fit assessments
      ├── gaps
      ├── décisions
      └── relations
      ↓
Publication gate
      ↓
export_projections.py
      ├── consultant-site.json → repo site → preview → revue → Vercel
      └── radar-public.json    → repo Radar → preview → revue → Vercel
```

## Conséquences

### Positives

- Un seul noyau de connaissance riche.
- Les deux interfaces peuvent évoluer à des cadences différentes.
- Les changements sont auditables par Git.
- Le site consultant garde sa cohérence éditoriale.
- Le Radar peut évoluer rapidement sans polluer la production commerciale.
- SandY peut fonctionner même si GitHub ou Vercel sont indisponibles.

### Coûts

- Il faut maintenir les contrats de projection.
- Les correspondances de fiches doivent utiliser des identifiants explicites.
- Un pipeline de validation/export/promotion est nécessaire.

## Non-décisions

Cette ADR ne choisit pas encore la base de données finale du registre local ni un moteur de graphe. Le contrat canonique reste indépendant de ces choix.
