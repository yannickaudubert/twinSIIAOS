# Contrat de projection et frontière Free / Expert

## 1. Projection `radar-public` — gratuite et réellement publique

Audience : consultants IA, architectes, développeurs, veilleurs, responsables innovation et visiteurs en phase d'exploration.

Cette projection peut être servie statiquement et inspectée par n'importe quel navigateur. Elle ne doit donc contenir **aucune donnée que l'on prétendrait ensuite protéger uniquement par l'interface**.

Expose :

- identité de la ressource ;
- nature / type ;
- résumé public ;
- source et dépôt officiels ;
- capacités et approches ;
- état de preuve publiable (`observed`, `installed`, `tested`, `qualified`...) ;
- maturité publique ;
- licence / régime d'ouverture ;
- activité et date de dernière vérification ;
- tendances publiques si mesurées ;
- gaps connus non sensibles ;
- relations générales non sensibles (`depends_on`, `enables`, `replaces`, `competes_with`) ;
- indication qu'un benchmark ou des preuves existent, sans exposer leur contenu protégé.

N'expose pas :

- fit contextualisé ou scores d'adéquation ;
- champion / challengers contextualisés ;
- benchmark détaillé ou conclusion propriétaire de benchmark ;
- pondérations client ;
- architecture recommandée pour une mission ;
- coûts et hypothèses client ;
- trajectoire de migration client ;
- décisions de session ;
- secrets, chemins locaux nominaux, tokens, données clients, prompts confidentiels, logs bruts sensibles, notes privées ou inventaire local complet.

Le Free doit rester utile : comprendre l'objet, son rôle, ses limites générales, sa provenance, son état de preuve et les alternatives comparables ne doit pas nécessiter un Pass.

## 2. Projection `radar-expert` — protégée

Audience : détenteur d'un Pass Expert valide.

Cette projection **ne doit jamais être publiée comme fichier statique public dans Git/Vercel**. Elle est délivrée après validation de session côté serveur et doit pouvoir être filtrée par mission, droits et niveau de publication.

Peut exposer, lorsque publiable :

- fit contextualisé ;
- critères et pondérations ;
- champion / challengers dans le contexte de mission ;
- pourquoi retenir / pourquoi écarter ;
- benchmarks détaillés publiables ;
- preuves SIIAOS contextualisées ;
- limites observées ;
- coûts / ressources / exploitation ;
- impact architectural contextualisé ;
- architecture recommandée ;
- trajectoire de migration ;
- décisions et justifications de session ;
- éléments de restitution.

Le jeton portable ou le navigateur ne contient jamais les données sensibles de mission. Le serveur valide le droit, puis renvoie uniquement la projection autorisée.

## 3. Projection `consultant-site`

Audience : dirigeants, DSI, responsables transformation, clients et prospects.

Expose une synthèse éditoriale et décisionnelle compatible avec la surface publique du site consultant :

- capacité métier/SI ;
- rôle architectural ;
- quand regarder / quand ne pas regarder ;
- effets organisationnels ;
- enjeux généraux de gouvernance, exploitation et réversibilité ;
- alternatives structurantes ;
- maturité ;
- conclusion issue du Radar uniquement lorsque cette conclusion est volontairement publiable.

Le site consultant ne republie ni tout le bruit de l'Hyperveille ni le contenu protégé d'une mission Expert.

## 4. Projection `local-siiaos`

Conserve la donnée riche : observations, benchmarks complets, preuves, artefacts, historique, déploiements, performances, coûts, incidents, décisions, données de session et éléments non publiables.

## 5. Règle de publication

Aucune promotion publique automatique d'un signal brut.

```text
signal
  → qualification
  → test / benchmark si nécessaire
  → preuve
  → revue humaine
  → classification de visibilité
      ├─ radar-public
      ├─ radar-expert protégé
      ├─ consultant-site
      └─ local-only
  → publication
```

## 6. Règle anti-faux-paywall

Une donnée upstream déjà publique ne devient pas « Premium » parce que l'interface la masque.

La valeur Expert doit porter sur :

- le contexte ;
- la qualification ;
- l'interprétation ;
- les preuves de terrain ;
- la comparaison pondérée ;
- l'architecture ;
- la décision ;
- la restitution.

## 7. Compatibilité avec le site existant

Le format `StackCatalogData` du repo `site` reste supporté par un exporteur dédié. La migration ne doit pas casser les pages `/stack-open-source/*` existantes.
