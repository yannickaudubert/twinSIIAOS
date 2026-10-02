# Resource Radar V4 — contrat d'explicabilité et d'usage humain

Date : 2026-09-03
Statut : contrat produit / UX de référence

## Finalité

Le Resource Radar ne doit pas devenir un GitHub, un Hugging Face ou un catalogue de liens avec davantage de filtres. Sa valeur tient à la capacité de rendre un écosystème technique **compréhensible, comparable et actionnable** pour un humain qui doit apprendre, explorer, qualifier ou décider.

Le produit doit toujours répondre à cinq questions, dans cet ordre :

1. **Qu'est-ce que c'est ?**
2. **À quel problème cela répond-il ?**
3. **Avec quoi faut-il réellement le comparer ?**
4. **Que savons-nous, et avec quel niveau de preuve ?**
5. **Que dois-je faire ensuite dans mon contexte ?**

## Lecture par niveaux

Chaque ressource importante doit pouvoir être lue à trois profondeurs.

### 30 secondes

- nature de l'objet ;
- problème résolu ;
- rôle architectural ;
- état de preuve ;
- licence / ouverture ;
- date de dernière vérification ;
- alternatives comparables ;
- principal point d'attention.

### 5 minutes

- ce que la ressource fait et ne fait pas ;
- cas d'usage ;
- dépendances ;
- forces et limites ;
- options alternatives ;
- preuves disponibles ;
- conséquences d'intégration ;
- acquisition / source officielle.

### Expert / mission

- fit contextualisé ;
- critères pondérés ;
- coûts et exploitation ;
- sécurité, conformité, souveraineté et réversibilité ;
- benchmark contextualisé ;
- architecture cible ;
- trajectoire de migration ;
- décision justifiée ;
- rapport de session.

## Frontière Free / Expert

### Free doit rester réellement utile

Le gratuit permet :

- chercher et explorer ;
- comprendre le vocabulaire ;
- lire les sources ;
- distinguer capacité, approche et implémentation ;
- comprendre le rôle d'une ressource ;
- connaître son état public, sa licence, son activité et sa fraîcheur ;
- voir les alternatives réellement comparables ;
- voir les preuves publiables et leur absence ;
- comprendre les limites générales ;
- acquérir ou ouvrir la source lorsque cela est possible ;
- apprendre la méthode de qualification.

### Expert doit réduire l'incertitude d'une décision

Le payant n'est pas « plus de liens ». Il ajoute :

- fit pour le contexte réel du client ;
- critères et pondérations adaptés ;
- pourquoi retenir / pourquoi écarter ;
- champion / challengers contextualisés ;
- preuves SIIAOS détaillées publiables ;
- risques d'exploitation ;
- coût / ressources / compétences ;
- impact sur l'architecture existante ;
- scénarios et trajectoires ;
- décisions sauvegardées et justifiées ;
- restitution de mission.

## Vocabulaire obligatoire

Les termes suivants doivent être définis dans le produit dès qu'ils apparaissent :

- capacité ;
- approche ;
- implémentation / système ;
- signal ;
- état de preuve ;
- evidence / preuve ;
- observé ; installé ; testé ; qualifié ; cible ; candidat ; déprécié ;
- champion ; challenger ; candidat ; expérimental ; retiré ;
- fit ;
- gap ;
- benchmark ;
- tendance 30 j ;
- dernière vérification ;
- blast radius / impact architectural ;
- open source ; open core ; source available ; propriétaire ;
- self-hosted ; local ; cloud ;
- projection publique ;
- provenance.

Aucun terme interne SIIAOS ne doit être exposé sans définition utile au visiteur.

## Règles de microcopy

- préférer « dernière vérification » à « freshness » ;
- préférer « adéquation à votre contexte » à « fit » dans les titres, tout en gardant le terme de lexique ;
- préférer « preuve » à « evidence » dans le texte courant ;
- préférer « impact architectural » à « blast radius » dans l'interface ;
- expliquer les acronymes à la première occurrence ;
- ne jamais transformer stars, activité ou release en recommandation ;
- ne jamais présenter « candidat » comme un jugement négatif : il s'agit d'un état à examiner ;
- afficher explicitement « preuve locale absente » lorsqu'elle n'existe pas ;
- rendre les dates visibles à côté des conclusions qui peuvent vieillir.

## Modes d'entrée

Le produit doit permettre d'entrer par l'intention, pas uniquement par le nom d'une technologie :

1. « Je connais déjà une solution » → recherche directe → fiche.
2. « J'ai un problème à résoudre » → capacité → approches → paysage → ressources.
3. « J'hésite entre plusieurs options » → paysage → comparateur.
4. « Je dois expliquer ou justifier un choix » → preuve → architecture → décision.
5. « Je veux installer / tester » → ressource → source → acquisition / bridge.

## Hiérarchie d'une fiche ressource

Une fiche doit présenter successivement :

1. **En 30 secondes** ;
2. **Ce que c'est / ce que ce n'est pas** ;
3. **Pourquoi la regarder** ;
4. **Rôle dans l'architecture** ;
5. **Alternatives comparables** ;
6. **Forces / limites** ;
7. **Preuves et niveau de confiance** ;
8. **Provenance et fraîcheur** ;
9. **Acquisition / source** ;
10. **Expert : adéquation, risques, architecture et décision contextualisées**.

## Critères d'efficience humaine

Une vue n'est pas terminée tant qu'elle ne respecte pas :

- un objectif compréhensible en moins de 10 secondes ;
- un prochain geste évident ;
- pas de tableau illisible sur mobile ;
- pas de badge sans légende ;
- pas de score sans définition ;
- pas de conclusion sans date ni niveau de preuve ;
- pas de verrou Expert sur une information upstream publique ;
- pas de faux contenu pour remplir un écran vide ;
- navigation clavier et focus visibles ;
- largeur et densité compatibles avec une lecture professionnelle prolongée.

## Tests de revue

Chaque lot UI doit être capturé et relu au minimum sur :

- desktop 1440 px ;
- mobile 390 px ;
- page d'entrée ;
- liste Radar ;
- fiche ressource ;
- guide ;
- lexique ;
- teaser Expert.

La revue doit vérifier : compréhension, lisibilité, charge cognitive, précision du vocabulaire, frontière Free/Expert et absence de données fictives présentées comme réelles.
