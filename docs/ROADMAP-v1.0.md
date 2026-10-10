# Roadmap optimisee jusqu'a twinSIIAOS v1.0

Statut : trajectoire de reference avant poursuite du code.

## 0. Definition de v1.0

La v1.0 n'est pas l'immeuble complet, ni le Web mondial des capacites, ni une plateforme d'agents universelle.

La v1.0 doit prouver un cycle vertical complet et gouverne :

```text
lancer
  -> ne rien observer sans accord
  -> declarer un besoin
  -> proposer un perimetre d'observation
  -> consentir
  -> decouvrir l'existant
  -> qualifier les faits
  -> construire la carte de capacites
  -> proposer plusieurs chemins vers un sommet
  -> expliquer les compromis
  -> faire valider une action si necessaire
  -> preparer
  -> appliquer une action reversible autorisee
  -> verifier
  -> produire une preuve
  -> enregistrer la capacite acquise ou planifiee
```

Une v1.0 est acceptee seulement si ce cycle fonctionne sur une installation neutre et sur au moins une instance locale reelle, sans utiliser de valeurs ARAGORN comme valeurs generiques.

## 1. Principes d'optimisation

### 1.1 Un seul chemin critique

Le chemin critique est :

`contrats -> runtime neutre -> First Day -> discovery -> graphe -> sommets -> action gouvernee -> preuve -> packaging -> pilote -> v1`

Aucun sous-systeme ne doit etre developpe s'il ne sert pas ce chemin avant v1.

### 1.2 Reutiliser avant d'importer

Avant d'importer du code historique, chaque composant existant est classe :

- `REUSE` : reutilisable presque tel quel ;
- `ADAPT` : utile apres neutralisation ;
- `REFERENCE` : conserve comme source d'enseignement ;
- `ARCHIVE` : historique uniquement ;
- `REJECT` : ne doit pas entrer dans le tronc public.

Les sources prioritaires a examiner sont :

- `siiaos-building-local-game-v2.1-step1` ;
- `SIIAOS-BUILDING-V1-DAY1-HARDENED` ;
- les versions KOS ;
- les Starter Kits ;
- les registres, audits et cockpits locaux existants.

### 1.3 La theorie des sommets n'utilise pas un score unique

Un chemin vers une capacite possede plusieurs couts :

- temps ;
- effort humain ;
- apprentissage ;
- argent ;
- CPU, GPU, RAM et stockage ;
- maintenance ;
- dependance externe ;
- confidentialite ;
- risque ;
- reversibilite ;
- responsabilite conservee ou deleguee.

Resolution :

1. eliminer les chemins interdits ou impossibles par contraintes dures ;
2. conserver les chemins non domines selon leurs couts ;
3. presenter une frontiere de Pareto lisible ;
4. contextualiser l'ordre d'affichage avec le profil de responsabilite ;
5. ne jamais cacher les alternatives valides uniquement parce qu'un score est meilleur.

### 1.4 Pas de nouveau service tant qu'un contrat suffit

Avant v1, pas de base graphe externe, pas de Kafka, pas de Kubernetes, pas d'OPA, pas d'OpenBao obligatoire, pas de nouveau conteneur impose.

Le noyau doit rester petit et pouvoir fonctionner comme un binaire local avec fichiers structures et journal d'evenements.

## Passe 0. 0.1.0-alpha.1 : fondations publiques

Statut : en cours dans PR #1.

### But

Fixer les invariants avant tout import de code executable.

### Taches

- [x] definir la frontiere ARAGORN / twinSIIAOS / commun ;
- [x] definir un First Day sans scan implicite ;
- [x] definir le Capability Passport conceptuel ;
- [x] definir un premier schema de consentement ;
- [x] documenter les regles de promotion public/local ;
- [ ] choisir la licence avant import significatif de code executable.

### Gate de sortie

Aucune execution locale n'est necessaire. Les invariants publics sont comprehensibles et revus.

## Passe 1. 0.1.0-alpha.2 : convergence historique, contrats et CI

### Risque ferme

Eviter de reconstruire ce qui existe deja et eviter de republier des hypotheses ARAGORN.

### Taches d'archeologie

- [ ] inventorier les modules, routes, schemas et fonctions des trunks historiques ;
- [ ] produire `docs/HERITAGE-LEDGER.md` avec `REUSE / ADAPT / REFERENCE / ARCHIVE / REJECT` ;
- [ ] identifier toutes les valeurs ARAGORN ou chemins absolus historiques ;
- [ ] cartographier les anciennes API vers les futurs objets canoniques ;
- [ ] verifier ce qui existe deja pour discovery, preuves, maturite, trajectoires, policy et serious game ;
- [ ] interdire tout import avant classification.

### Contrats minimaux

- [ ] `Context` ;
- [ ] `Need` ;
- [ ] `ObservationRequest` ;
- [ ] `Consent` ;
- [ ] `Fact` avec provenance et statut ;
- [ ] `Evidence` ;
- [ ] `CapabilityPassport` ;
- [ ] `ResponsibilityProfile` ;
- [ ] `Summit` ;
- [ ] `PathCandidate` ;
- [ ] `ActionPlan`.

### Tests et qualite

- [ ] fixtures exclusivement fictives ;
- [ ] validation JSON Schema ;
- [ ] test automatique anti-chemins absolus ;
- [ ] test automatique anti-secrets evidents ;
- [ ] test anti-valeurs ARAGORN dans les fixtures generiques ;
- [ ] CI GitHub minimale ;
- [ ] decision de licence du noyau avant fusion de code historique.

### Gate de sortie

Les contrats sont testables sans ARAGORN. Aucun objet canonique n'a besoin d'une application ou d'une base externe.

## Passe 2. 0.1.0-alpha.3 : runtime neutre minimal

### Risque ferme

Prouver que le logiciel peut demarrer sans observer ni modifier la machine.

### Taches

- [ ] extraire ou reutiliser le minimum pertinent du runtime Go historique ;
- [ ] un seul binaire ;
- [ ] servir l'interface locale depuis le binaire ;
- [ ] `twinSIIAOS version` ;
- [ ] `twinSIIAOS doctor` ;
- [ ] `twinSIIAOS start` ;
- [ ] etat initial `zero permission` ;
- [ ] aucun scan filesystem par defaut ;
- [ ] aucun probe reseau par defaut ;
- [ ] aucun service externe par defaut ;
- [ ] journal local append-only des evenements de gouvernance ;
- [ ] repertoire de donnees configurable ;
- [ ] contrat `Adapter` ;
- [ ] contrat `DiscoveryProvider` ;
- [ ] tests de demarrage neutre Windows ;
- [ ] test headless Linux.

### Gate de sortie

Sur une machine vierge, le binaire demarre, affiche le First Day et ne produit aucune observation machine avant une demande explicite.

## Passe 3. 0.1.0-alpha.4 : First Day vertical read-only

### Risque ferme

Prouver la decouverte utile sans surveillance generale de la machine.

### Taches interface

- [ ] accueil explicatif ;
- [ ] contexte declare ;
- [ ] besoin concret ;
- [ ] profil initial de responsabilite ;
- [ ] proposition de perimetre d'observation ;
- [ ] affichage lisible des exclusions ;
- [ ] consentement grant / revoke / expire ;
- [ ] affichage separe `declared / observed / inferred / proposed / validated` ;
- [ ] carte simple des capacites existantes et manquantes.

### Adapters read-only prioritaires

- [ ] resume OS cible et borne ;
- [ ] fichiers ou dossiers uniquement selectionnes par l'utilisateur ;
- [ ] adapter read-only vers une instance SIIAOS historique existante ;
- [ ] probes loopback de services uniquement apres consentement explicite ;
- [ ] aucun scan de ports generique ;
- [ ] aucun navigateur, session, token ou secret.

### Tests

- [ ] refus de consentement : zero observation ;
- [ ] revocation : arret immediat des observations concernee ;
- [ ] fixture fausse ARAGORN : rejet ;
- [ ] tests semantiques de l'UI, pas seulement HTTP 200 ;
- [ ] provenance visible pour chaque fait.

### Gate de sortie

Le First Day permet de passer d'un systeme ignorant a une premiere carte de capacites reelles sans action destructive.

## Passe 4. 0.2.0-beta.1 : moteur de sommets explicable

### Risque ferme

Eviter qu'une recommandation soit une simple liste d'outils ou un score opaque.

### Modele de graphe minimal

Noeuds :

- besoin ;
- capacite ;
- ressource ;
- competence ;
- service ou outil ;
- action ;
- preuve.

Relations :

- `requires` ;
- `enables` ;
- `alternative_to` ;
- `delegates_to` ;
- `learns` ;
- `uses` ;
- `proves`.

### Resolution

- [ ] contraintes dures ;
- [ ] vecteur de couts ;
- [ ] frontiere de Pareto ;
- [ ] preferences issues du ResponsibilityProfile ;
- [ ] explication de chaque chemin ;
- [ ] visualisation des capacites deja presentes ;
- [ ] visualisation de ce qui manque ;
- [ ] aucun choix automatique irrevisible ;
- [ ] resultat deterministe sur fixtures identiques.

### Premier sommet de reference

Le moteur doit savoir traiter au minimum :

`Je veux utiliser une IA locale deja presente si ma machine en dispose.`

Sur une instance possedant un moteur compatible, la reutilisation doit etre preferee a une nouvelle installation lorsque les contraintes humaines l'autorisent.

Sur une machine qui n'en possede pas, le sommet reste planifiable sans installation automatique.

### Gate de sortie

Pour un meme besoin, le systeme peut presenter plusieurs chemins valides et expliquer leurs compromis.

## Passe 5. 0.3.0-beta.1 : action gouvernee, preuve et rollback

### Risque ferme

Prouver que twinSIIAOS peut agir sans devenir un shell universel ou une automatisation autonome.

### Modes

`OBSERVER -> PROPOSER -> PREPARER -> OPERER`

### Taches

- [ ] contrat `ActionManifest` ;
- [ ] actions strictement allowlistees par adapter ;
- [ ] interdiction du shell arbitraire dans le chemin nominal ;
- [ ] plan lisible avant execution ;
- [ ] validation humaine explicite ;
- [ ] rollback prepare avant action modifiante ;
- [ ] preuve avant/apres ;
- [ ] correlation id entre besoin, plan, validation, action et preuve ;
- [ ] journal d'execution ;
- [ ] bouton d'arret ;
- [ ] reprise apres echec.

### Action generique obligatoire

Au moins une action doit fonctionner sans service externe :

`creer un espace de travail local gouverne dans un emplacement choisi par l'utilisateur`

Elle doit etre reversible et testee.

### Action de reutilisation de reference

Sur ARAGORN ou une fixture compatible, atteindre une capacite existante sans la reinstaller, par exemple un moteur IA local deja present.

### Gate de sortie

Au moins un sommet passe de besoin a capacite verifiee avec validation humaine, preuve et rollback.

## Passe 6. 0.4.0-beta.1 : one-click, installation et trois parcours d'or

### Risque ferme

Prouver que le systeme n'est pas seulement developpable par ses auteurs.

### Packaging Windows prioritaire

- [ ] artefact Windows x64 autonome ;
- [ ] pas de Go requis sur la machine utilisateur ;
- [ ] pas de droits administrateur requis pour le mode standard ;
- [ ] lancement en un clic ;
- [ ] ouverture automatique du First Day ;
- [ ] repertoire de donnees identifiable et exportable ;
- [ ] backup ;
- [ ] upgrade ;
- [ ] rollback version ;
- [ ] uninstall documente ;
- [ ] checksum de release ;
- [ ] SBOM de release si l'outillage retenu reste leger.

### Linux

- [ ] binaire headless ;
- [ ] meme contrats et fixtures ;
- [ ] pas d'exigence d'interface desktop specifique avant v1.

### Trois parcours d'or

1. **Zero permission** : lancer et explorer sans autoriser aucune observation.
2. **Comprendre ma machine** : consentir a un resume borne, obtenir des faits sources et une carte de capacites.
3. **Atteindre un sommet** : calculer un chemin, valider une action reversible, verifier la capacite et produire une preuve.

Un quatrieme parcours de reference est teste sur ARAGORN : reutiliser un service local existant plutot que le reinstaller.

### Gate de sortie

Un utilisateur non developpeur peut lancer le systeme et terminer au moins un parcours d'or sans terminal.

## Passe 7. 0.9.0-rc.1 : PILOT, securite et exploitation

### Risque ferme

Eviter une v1 techniquement fonctionnelle mais non exploitable.

### Matrice de test

- [ ] instance ARAGORN ;
- [ ] profil Windows propre ;
- [ ] Windows avec services locaux deja presents ;
- [ ] Linux headless ;
- [ ] fixtures offline.

### Securite et confidentialite

- [ ] threat model ;
- [ ] revue des permissions ;
- [ ] test de non-exfiltration ;
- [ ] verification zero secret dans les logs ;
- [ ] tests de refus et revocation ;
- [ ] tests de chemins non autorises ;
- [ ] tests de rollback ;
- [ ] separation public/local automatisee en CI.

### Exploitation

- [ ] runbook ;
- [ ] troubleshooting ;
- [ ] sauvegarde/restauration ;
- [ ] upgrade/downgrade ;
- [ ] journal et diagnostic ;
- [ ] budget de ressources mesure et documente ;
- [ ] temps de demarrage mesure ;
- [ ] fonctionnement offline verifie ;
- [ ] aucun nouveau service permanent obligatoire.

### Documentation utilisateur

- [ ] installer ;
- [ ] lancer ;
- [ ] comprendre le consentement ;
- [ ] atteindre une premiere capacite ;
- [ ] corriger une observation ;
- [ ] retirer un droit ;
- [ ] sauvegarder ;
- [ ] mettre a jour ;
- [ ] desinstaller.

### Gate de sortie

Aucun bloqueur critique connu. Les trois parcours d'or sont reproductibles et documentes.

## Passe 8. 1.0.0 : release stable

### Definition of Done

- [ ] demarrage neutre, sans scan ;
- [ ] consentement explicite et revocable ;
- [ ] faits qualifies et sources ;
- [ ] aucun default ARAGORN ;
- [ ] Capability Passport persistant ;
- [ ] Responsibility Profile modifiable ;
- [ ] au moins un adapter local read-only ;
- [ ] adapter de compatibilite vers le tronc historique retenu ;
- [ ] moteur de sommets multi-criteres explicable ;
- [ ] au moins une action generique reversible ;
- [ ] au moins une reutilisation reelle d'une capacite existante sur instance de reference ;
- [ ] preuve, journal, correlation et rollback ;
- [ ] one-click Windows ;
- [ ] mode Linux headless ;
- [ ] installation, upgrade et uninstall documentes ;
- [ ] tests CI ;
- [ ] licence libre du noyau fixee ;
- [ ] release notes et checksums ;
- [ ] aucune donnee personnelle ou infrastructurelle de l'instance de reference dans le depot public.

## Ce qui est volontairement repousse apres v1

Pour proteger le chemin critique, ne font pas partie de v1 sauf besoin indispensable decouvert en cours de test :

- immeuble Godot complet ;
- multi-utilisateur organisationnel complet ;
- federation mondiale ;
- Open Capability Search exhaustif ;
- Hyperveille mondiale integree ;
- calcul distribue entre appareils ;
- orchestration massive d'agents ;
- promotion automatique vers les communs ;
- moteur de policy externe obligatoire ;
- secret manager externe obligatoire ;
- base graphe dediee obligatoire ;
- marketplace de packs ;
- installation automatique d'une grande stack logicielle ;
- SaaS ou cloud obligatoire ;
- application mobile.

Ces fonctions pourront devenir des adapters, des packs ou des couches superieures apres stabilisation du noyau.

## Regle de passage entre les passes

Une passe n'est pas fermee par le nombre de fichiers produits.

Elle est fermee uniquement si :

1. son risque principal est teste ;
2. un test de non-regression existe ;
3. la documentation correspond au comportement reel ;
4. le rollback de la passe est connu ;
5. elle n'introduit pas une dependance structurelle non justifiee ;
6. elle rapproche directement d'un des trois parcours d'or.

Si une tache ne satisfait pas au point 6, elle est candidate au report apres v1.
