# Resource Radar V5 — protocole de simulation d'usages

## Objet

Ce protocole teste la valeur du Radar comme systeme d'aide a la decision. Un test n'est pas considere utile parce qu'un bouton repond : il doit verifier qu'un utilisateur ou une organisation obtient une decision plus explicable, plus frugale et plus fidele a son contexte.

## Axes mesures

1. **Time to understand** — l'utilisateur identifie rapidement le bon point d'entree.
2. **Time to useful action** — il atteint une action ou information exploitable sans detour technologique inutile.
3. **Context fidelity** — la configuration, le workload, la confidentialite et le budget modifient reellement le resultat.
4. **Decision traceability** — une conclusion peut remonter aux profils, observations et preuves.
5. **Avoided waste** — le moteur reutilise l'existant et n'ajoute ni achat ni dependance sans necessite.
6. **TAT perceptif** — comprehension, utilite, confiance, ouverture, autonomie, humanite, risque percu et intention d'usage restent des dimensions independantes.
7. **Uncertainty honesty** — une inconnue reste une inconnue et n'est pas transformee en compatibilite ou incompatibilite.
8. **Progressive disclosure** — le public comprend l'objet ; les conclusions contextualisees restent protegees.
9. **Mobile viability** — les chemins essentiels restent accessibles sur petit ecran.

## Personas initiaux

| Persona | But du test | Contraintes |
|---|---|---|
| SandY simulated | environnement local riche deja equipe | budget incremental 0, local-first, provider externe non structurel |
| Office laptop 8 GB | petite configuration generaliste | CPU, Python, pas de GPU observe |
| Unknown GPU | environnement incompletement observe | la VRAM ne doit jamais etre inventee |
| Novice web | ne connait pas le vocabulaire IA | doit pouvoir partir du besoin |
| Expert / architecte | cherche les preuves et limites | doit remonter aux conditions et a la provenance |
| Mobile user | consultation rapide | navigation et lecture essentielles preservees |

Les personas de test sont synthetiques. Ils ne constituent pas un inventaire materiel probant d'un utilisateur reel.

## Scenarios decisionnels automatises

Les tests Python verifient notamment :

- classification confidentielle a budget zero ;
- preference d'un traitement deterministe lorsque suffisant ;
- refus d'un provider externe interdit ;
- refus d'une option payante hors budget ;
- rejet d'un profil trop gros puis selection d'un substitut local ;
- preservation des preuves du profil retenu ;
- runtime absent = gap reel ;
- GPU non observe = statut unknown, jamais "VRAM insuffisante" ;
- une capacite preferee manquante ne bloque pas les capacites requises ;
- aucune dependance externe n'apparait silencieusement sur un workload confidentiel.

## Parcours navigateur automatises

Playwright verifie :

- novice -> besoin -> Capacites ;
- utilisateur equipe -> ma configuration -> Configuration & execution ;
- recherche d'une ressource connue -> fiche explicative ;
- ressource depreciee -> statut visible ;
- demande de preuve -> gate Expert explicite ;
- mobile -> menu -> vue Execution ;
- projection publique vide -> aucune recommandation inventee ;
- power user -> raccourci "/" -> recherche.

## Etat courant de la campagne

La premiere campagne versionnee couvre maintenant 59 assertions/scenarios repartis entre :
- decisions Estate x Workload x Execution Profile ;
- cas adversariaux de politique, cout, inconnues et stockage ;
- composition multi-capacites ;
- integrite des signaux publics ;
- admission organisationnelle, maturite et HumanGate ;
- regressions de contexte/ontologie recuperees depuis les travaux anterieurs ;
- parcours navigateur Playwright.

## Campagne suivante

La base doit etre etendue progressivement vers 50 a 100 scenarios, sans gonfler artificiellement le nombre. Les prochaines familles prioritaires sont :

- multi-machine / cluster / noeud secondaire ;
- air-gap et donnees restricted ;
- workload tres volumineux avec decomposition/RAG ;
- remplacement d'un SaaS existant vs augmentation/mirror ;
- changement de licence ou archive upstream ;
- conflit entre benchmark fournisseur et benchmark local ;
- stockage presque plein ;
- concurrence de plusieurs workloads ;
- plan qui doit sequencer deux modeles pour tenir en VRAM ;
- echec et reprise du bridge/local runtime ;
- capital numerique dormant et doublons de services ;
- utilisateur qui demande explicitement "le plus gros modele" ou "le plus populaire".

## Gate de release

La V5 ne doit pas etre promue sur Vercel si :

- une politique local-only peut produire un step external_required ;
- budget zero peut produire un cout incremental positif ;
- une ressource inconnue est presentee comme compatible ou incompatible sans observation ;
- une projection publique expose Estate, Workload ou Execution Plan prive ;
- un parcours principal est inaccessible clavier ou mobile ;
- la V3 operationnelle n'est pas preservee ;
- les tests de decision ou les parcours navigateur ne sont pas verts.
