# Contrat de projection publique

## 1. Projection `radar-public`

Audience : consultants IA, architectes, développeurs, veilleurs, responsables innovation.

Expose :

- identité de la ressource ;
- capacités et approches ;
- état de qualification publiable ;
- position compétitive ;
- maturité, licence et activité ;
- tendances 7/30/90 jours si mesurées ;
- fit agrégé et contexte de test publiable ;
- alternatives, concurrents et remplacements potentiels ;
- gaps connus non sensibles ;
- benchmark résumé ;
- preuves publiables ;
- date de dernière vérification.

N'expose jamais : secrets, chemins locaux nominaux, tokens, données clients, prompts confidentiels, logs bruts sensibles, notes privées, inventaire local complet.

## 2. Projection `consultant-site`

Audience : dirigeants, DSI, responsables transformation, clients et prospects.

Expose une synthèse décisionnelle :

- capacité métier/SI ;
- rôle architectural ;
- quand choisir / quand ne pas choisir ;
- effets organisationnels ;
- enjeux de gouvernance, exploitation et réversibilité ;
- alternatives structurantes ;
- maturité ;
- conclusion issue du Radar lorsque suffisamment qualifiée.

Le site consultant ne doit pas republier tout le bruit de l'Hyperveille.

## 3. Projection `local-siiaos`

Conserve la donnée riche : observations, benchmarks complets, preuves, artefacts, historique, déploiements, performances, coûts, incidents, décisions et éléments non publiables.

## 4. Règle de publication

Aucune promotion publique automatique d'un signal brut.

```text
signal → qualification → test/benchmark si nécessaire → evidence → review humaine → projection → Git → publication
```

## 5. Compatibilité avec le site existant

Le format `StackCatalogData` du repo `site` reste supporté par un exporteur dédié. La migration ne doit pas casser les pages `/stack-open-source/*` existantes.
