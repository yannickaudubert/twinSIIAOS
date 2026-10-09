# Resource Radar V4 — chantier produit Free → Expert

Date : 2026-09-03  
Statut : architecture cible / chantier lancé

## 1. Rôle du Radar dans l'offre

Le Resource Radar n'est pas la page commerciale principale et ne doit pas dupliquer le site consultant.

- **Radar Free** : découvrir, chercher, observer, ouvrir les sources, suivre les signaux et comprendre le paysage.
- **Radar Expert** : comparer dans un contexte professionnel, afficher les preuves SIIAOS, challenger une solution, construire une décision.
- **Site consultant** : expliquer la valeur du conseil, vendre le Pass, qualifier la mission, gérer le circuit administratif.

Le même Pass commercial doit, à terme, ouvrir les deux projections Expert sans créer deux achats ou deux comptes indépendants.

## 2. Invariants de migration depuis la V3

La V4 conserve les capacités opérationnelles utiles de la V3 :

- recherche multi-sources ;
- résolution d'artefacts ;
- source officielle ;
- téléchargement / mirroring ;
- file de ressources ;
- commandes multi-OS ;
- bridge local ;
- hash et manifeste.

La refonte d'interface ne doit pas supprimer ces fonctions pour faire une simple landing page marketing.

## 3. Architecture des surfaces

### Free

Navigation cible :

1. `Radar` — signaux et recherche live ;
2. `Capacités` — paysage par problème plutôt que par fournisseur ;
3. `Approches` — RAG, long context, document VLM, computer-use, durable workflows, etc. ;
4. `Paysages` — options comparables et familles de technologies ;
5. `Hyperveille` — nouveautés, vitesse, accélération, risques, trous dans la raquette ;
6. `Acquérir` — resolve, download, mirror, bridge ;
7. `Méthode` — comment le SIIAOS qualifie sans promouvoir automatiquement un signal.

### Expert

8. `Fit` — contexte matériel, organisationnel, réglementaire et mission ;
9. `Comparateur` — matrice contextualisée ;
10. `Evidence` — tests, benchmarks, vérifications, dates ;
11. `Architecture` — impact, dépendances, remplacements, topologies ;
12. `Décisions` — panier de choix, rejet, justification ;
13. `Session` — temps restant, contexte, notes et restitution.

## 4. Frontière de valeur

### Toujours gratuit

- recherche ;
- ressources ;
- sources officielles ;
- type, catégorie, date et métadonnées publiques ;
- activité/tendance générale ;
- lecture des capacités ;
- méthode de qualification ;
- fonctions publiques de mirroring lorsque juridiquement et techniquement permises.

### Expert 8 h

- fit contextualisé ;
- champion / challengers qualifiés ;
- pourquoi oui / pourquoi non ;
- tests et preuves internes publiables ;
- limites observées ;
- coûts / ressources / exploitation ;
- impact architectural ;
- architecture recommandée ;
- trajectoire de migration ;
- comparaisons sauvegardées ;
- décisions de session ;
- rapport final.

Le verrou n'est jamais posé artificiellement sur une information upstream déjà publique. La valeur Expert correspond à la qualification, au contexte, à l'analyse et au travail de conseil.

## 5. CTA du Radar

Le Radar ne doit pas afficher une popup commerciale dès la première recherche.

CTA déclenchés aux moments de décision :

- `Comparer pour mon contexte`
- `Voir pourquoi cette solution est retenue ou écartée`
- `Ouvrir les preuves SIIAOS`
- `Construire une architecture`
- `Ajouter à ma décision`

Utilisateur non authentifié : le CTA explique la valeur puis renvoie vers la page canonique du Pass sur le site consultant.

Utilisateur avec Pass : le CTA ouvre la vue Expert correspondante.

## 6. Marketing commun

Message de fond :

> Le Radar trouve. Le SIIAOS qualifie. Le conseil transforme les signaux en décisions.

Sous-message :

> Ne payez pas pour voir plus de liens. Payez pour réduire l'incertitude d'une décision technique.

Offre :

- 600 EUR HT ;
- 8 heures consécutives ;
- professionnel ;
- ponctuel ;
- sans renouvellement automatique ;
- exécution agentique future hors forfait et mesurée séparément.

Les prix et conditions sont exposés par le site consultant ; le Radar utilise un lien canonique et n'embarque pas une seconde logique commerciale divergente.

## 7. Identité et design

La V4 abandonne le style cyberpunk / gradient / néon de la V3 pour les vues professionnelles.

Direction :

- fond clair ou neutre professionnel ;
- typographie de produit B2B ;
- densité d'information contrôlée ;
- tableaux, matrices, graphes et timelines ;
- palette restreinte ;
- états de preuve et de maturité avant couleurs décoratives ;
- responsive sans transformer l'outil en landing page.

Le Radar doit ressembler à un outil d'urbanisme / intelligence technologique, pas à une démonstration générative.

## 8. Accès Expert

Architecture cible :

```text
client -> site consultant -> demande -> Still Portage -> validation
                                            |
                                            v
                                      émission locale
                                            |
                                     SIIAOS PASS 8 h
                                      /           \
                              site session     radar session
```

Règles :

- aucun secret de signature dans le navigateur ;
- aucune PII dans un token portable ;
- validation serveur puis cookie HttpOnly propre à chaque domaine ;
- scopes explicites ;
- expiration 8 h ;
- révocation côté registre local ;
- journal d'activation ;
- absence de token dans les URLs, analytics ou logs publics.

## 9. Juridique et confidentialité

Le Radar public renvoie vers les documents canoniques du site consultant :

- mentions légales ;
- conditions d'utilisation des contenus ;
- politique de confidentialité ;
- cookies/analytics ;
- conditions commerciales du Pass.

Une bannière/notice spécifique doit rappeler :

- les ressources externes restent soumises à leurs licences ;
- le signal Radar n'est pas une recommandation automatique ;
- les données Premium et benchmarks ont une date / niveau de preuve ;
- ne jamais coller de secrets ou documents client dans une recherche publique.

## 10. Instrumentation

Événements autorisés sans PII :

- `radar_search`
- `radar_resource_open`
- `expert_teaser_seen`
- `expert_compare_clicked`
- `expert_evidence_clicked`
- `premium_landing_outbound`
- `pass_session_active`
- `expert_comparison_created`
- `decision_saved`
- `session_report_exported`

Jamais dans analytics : email, organisation, token, texte de mission, prompt client, document, URL privée ou valeur de secret.

## 11. Lots

### R4-A — reversion de la V3 déployée

- capturer le code effectivement servi par Vercel ;
- identifier la source de build ;
- la remettre sous Git avant refonte ;
- conserver un snapshot V3 reproductible.

### R4-B — shell V4 professionnel

- nouvelle DA ;
- navigation Free / Expert ;
- composants états de preuve ;
- CTA contextuels ;
- footer légal canonique.

### R4-C — projection réelle

- consommer `radar-public.json` ;
- afficher états, positions et dates ;
- supporter absence de qualification sans données fictives.

### R4-D — Expert

- session validée ;
- fit ;
- comparateur ;
- evidence ;
- décisions ;
- rapport.

### R4-E — bridge SandY

- test réel du bridge V4 ;
- preflight ;
- observations ;
- export des projections ;
- publication gate.

## 12. Definition of Done V4 commerciale

La V4 n'est pas considérée prête tant que :

- la V3 est reversionnée ;
- les capacités resolve/mirror/bridge sont conservées ;
- le registre réel SandY alimente une projection ;
- la frontière Free/Expert est testée ;
- l'accès Expert 8 h est révocable ;
- les documents légaux sont canoniques ;
- aucune PII n'est présente dans les tokens/analytics ;
- aucune recommandation n'est affichée sans preuve et date ;
- CI + preview + revue humaine sont vertes.
