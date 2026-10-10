# Roadmap v0.1.0

## alpha.1

Objectif : fixer les contrats publics avant d'importer du code d'execution.

- README et frontieres publiques ;
- First Day sans scan implicite ;
- contrat de consentement ;
- Capability Passport ;
- separation stricte ARAGORN / public ;
- choix de licence encore ouvert.

## alpha.2

Objectif : introduire les objets canoniques minimaux et des fixtures neutres.

- Actor ;
- Context ;
- Evidence ;
- Capability ;
- ResponsibilityProfile ;
- ObservationRequest ;
- Summit ;
- DeploymentPlan ;
- exemples fictifs ;
- tests JSON Schema.

## alpha.3

Objectif : brancher l'existant sans le copier.

- contrat Adapter ;
- contrat DiscoveryProvider ;
- adapter de lecture vers une instance locale SIIAOS existante ;
- aucun chemin absolu commite ;
- aucun secret ;
- aucun scan automatique.

## alpha.4

Objectif : premiere interface First Day.

- demarrage neutre ;
- contexte declare ;
- choix du perimetre ;
- consentement ;
- affichage des faits qualifies ;
- premier graphe de capacites ;
- aucune action destructive.

## beta.1

Objectif : premiers sommets calcules.

Chaque chemin est evalue selon plusieurs couts :

- temps ;
- effort humain ;
- apprentissage ;
- argent ;
- ressources machine ;
- maintenance ;
- dependance externe ;
- risque ;
- confidentialite ;
- reversibilite.

Le meilleur chemin est contextualise. Ce n'est pas necessairement le chemin avec le moins d'etapes.

## Condition pour 0.1.0 stable

- zero valeur ARAGORN par defaut ;
- First Day fonctionnel sans scan ;
- consentement verifiable ;
- un adapter local read-only ;
- un premier sommet calcule ;
- preuve et rollback documentes ;
- licence du noyau decidee ;
- tests reproductibles sous Windows et Linux ;
- documentation installation / upgrade / uninstall.
