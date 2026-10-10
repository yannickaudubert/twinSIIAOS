# Puzzle canonique SIIAOS

**Version documentaire : 2026-09-25**  
**Statut : architecture cible / contrat de convergence**  
**Règle de vérité : une architecture cible n'est pas un runtime prouvé.**

## Définition

Le SIIAOS est un système local-first qui transforme une situation humaine réelle en missions gouvernées, assemble les capacités humaines, logicielles et IA nécessaires, produit des résultats vérifiables, puis transforme l'expérience obtenue en connaissance réutilisable sans retirer à l'humain son autorité, ses données ni sa capacité de reprendre la main.

Le SIIAOS n'est pas un chatbot, un modèle, un agent, un orchestrateur, un RAG, un Vault, une machine ou une interface. Ces éléments peuvent fournir des capacités au système ; aucun ne possède seul son autorité ou son canon.

## Ordre d'autorité

```text
mandat humain explicite
  > politiques et registres validés
  > sources primaires et preuves datées
  > systèmes canoniques
  > projections / index / RAG / interfaces
  > modèles et fournisseurs externes
```

Probabilité, puissance de calcul, disponibilité technique ou capacité d'action ne créent jamais une autorisation.

## États de vérité

Toujours distinguer :

`PROPOSÉ != CODÉ != TESTÉ != DÉPLOYÉ != OBSERVÉ != PROUVÉ`

Et :

`DesiredState != ObservedState`

Un état runtime doit être relié à une preuve machine datée.

## Boucle complète

```text
Situation réelle
 -> NeedSpec
 -> ContextPack
 -> Mandat / Policy / Authority
 -> Mission
 -> Capability composition
 -> Team / Workflow
 -> Execution Envelope
 -> Action
 -> OperationRecord
 -> Evidence
 -> HumanGate
 -> Livrable
 -> Effets observés
 -> RETEX
 -> KnowledgeAdmission
 -> Method / Template / Recipe / Skill / Anti-skill / Test
 -> ChangeSet
 -> nouvel état observé
 -> nouvelle boucle
```

## Objets structurants

- **Identity** : qui ou quoi est impliqué.
- **Authority** : qui a le droit de faire quoi.
- **Mandate** : pourquoi une action est autorisée.
- **Policy** : quelles règles s'imposent.
- **TransitionGate** : ce qui autorise le passage à l'étape suivante.
- **NeedSpec** : le besoin réellement qualifié.
- **ContextPack** : sources, historique, contraintes, données autorisées et contexte.
- **Capability** : ce qu'un humain, logiciel, modèle, service ou système sait effectivement faire.
- **ResourceContract** : ressources, limites et dépendances mobilisables.
- **Mission** : résultat attendu, critères, budget, risques et preuves.
- **Decision** : arbitrage, motif, autorité et alternatives.
- **OperationRecord** : ce qui a effectivement été exécuté.
- **Evidence** : ce qui permet de le vérifier.
- **KnowledgeAdmission** : ce qui peut entrer dans le patrimoine commun.
- **DesiredState / ObservedState / ChangeSet** : cible, réalité constatée et modification proposée.

## Les Atlas

Les Atlas sont des projections du même système, pas des bases de vérité concurrentes :

1. Infrastructure & Topology
2. Software, Runtime & Capabilities
3. Cognitive Fabric
4. Data, Memory & Knowledge
5. Identities, Humans, Agents & Authorities
6. Governance, Policies & Compliance
7. Security & Trust
8. Mission Factory & Workflows
9. Evidence, Observability & Operations

Une interface, un Building, un cockpit ou un Hall représente ces objets ; il ne les possède pas.

## Profils et surfaces

Le même système doit pouvoir être projeté pour un particulier, artisan, expert métier, consultant, développeur, chercheur, manager, dirigeant, auditeur, collectivité, territoire, citoyen ou agent IA.

Ce qui change par profil : vocabulaire, droits, contexte, capacités visibles, profondeur, workflow, confidentialité et exigences de preuve.

`Identity != Role != Authority`

## Hall / Buildings / Cockpits

Le Hall est une porte d'entrée et d'orientation.  
Les Buildings, étages, bureaux, Teams et cockpits sont des projections UX.  
Ils ne sont ni le canon, ni l'autorité, ni un orchestrateur souverain.

## Agents et équipes cognitives

```text
Agent =
Mission
+ Skills
+ Context
+ Permissions
+ Tools
+ Resources
+ Budget
+ Policies
+ Evidence requirements
+ Reviewer
+ Exit conditions
```

Une personnalité n'accorde aucun droit.

Chaîne de contrôle privilégiée :

```text
Producteur -> Reviewer indépendant -> Guardian
 -> vérification déterministe -> synthèse responsable -> HumanGate
```

## Cognitive Fabric

Toujours distinguer :

`MODEL != RUNTIME != COGNITIVE ENGINE != AGENT != TOOL != CAPABILITY`

Un fournisseur ou un modèle est remplaçable derrière des contrats. Le routage doit pouvoir tenir compte du besoin, des données, de la confidentialité, du hardware, du coût, de la latence, de la qualité observée, du risque et des preuves.

## Data, Memory & Knowledge

```text
Source originale
 != SourceRecord
 != KnowledgeObject
 != Index
 != Embedding
 != Graphe
 != RAG
 != Synthèse
 != Décision canonique
```

Les index, embeddings et RAG sont reconstruisibles. Les sources, décisions, droits, temporalités et provenances doivent rester auditables.

## Vaults et VaultOps

Les Vaults séparent les patrimoines par propriétaire, finalité, confidentialité, droits, provenance, rétention, règles RAG, export et succession.

**VaultOps désigne les pratiques et opérations de gestion de ces patrimoines ; ce n'est pas une couche logicielle autonome.**

## Capability / Resource Fabric

La question n'est pas « quels logiciels avons-nous ? » mais « quelles capacités maîtrisées pouvons-nous réellement mobiliser ? ».

Une Capability doit pouvoir être reliée à son fournisseur, sa version, son hôte, sa licence, ses données autorisées, ses dépendances, son coût, ses risques, ses tests, son niveau de maturité, son observabilité et son mécanisme de repli.

## Radar / Hyperveille

```text
Source
 -> signal
 -> qualification
 -> NeedSpec
 -> alternatives
 -> licence / sécurité / TCO
 -> expérimentation bornée
 -> preuve
 -> reviewer
 -> HumanGate
 -> admission / rejet / veille
 -> observation en exploitation
```

`Trouvé != compatible != sûr != admis != installé != opérationnel`

Un dépôt public GitHub ne devient jamais automatiquement une brique du SIIAOS.

## Sécurité et frontières

Principes transverses :

```text
confiance != autorisation
connexion != intégration
intégration != possession
possession != autorité
capacité != permission
conversation != exécution
```

Les données clients, personnelles, confidentielles ou secrètes restent dans leur périmètre d'autorité. Un RETEX transverse peut mutualiser une méthode abstraite sans aspirer les données sources.

## Local-first

Local-first ne signifie pas « tout hors ligne ». Cela signifie qu'aucun fournisseur distant ne doit devenir une dépendance structurelle irréversible pour comprendre, gouverner, exporter, restaurer ou reprendre le système.

Le niveau de calcul doit suivre une escalade frugale :

```text
baseline simple
 -> modèle existant
 -> RAG / outils
 -> adaptation légère
 -> LoRA / spécialisation
 -> entraînement spécialisé
 -> calcul lourd si le besoin mesuré le justifie
```

## Production et apprentissage

Deux boucles restent entremêlées :

```text
Production : Besoin -> Mission -> Capacités -> Exécution -> Preuve -> Livrable
Apprentissage : Observation -> RETEX -> Connaissance -> Méthode/Capability -> amélioration
```

Un livrable réussi peut produire une recipe réutilisable ; les données du contexte initial ne deviennent pas automatiquement communes.

## Topologie physique

Les noms de machines ne sont jamais des noms de couches logicielles.

- **SandY** : nœud local principal de compute / IA / SI dans la cible actuelle, sous réserve de preuves runtime fraîches.
- **ARAGORN** : machine physique ASUS TUF, nœud secondaire / complément / canary / rollback dans la cible actuelle.
- **Redmi** : terminal utilisateur / surface d'accès.
- **Galaxy / Galaxy Book** : rôle non figé tant qu'il n'est pas prouvé et décidé.
- GitHub, Vercel et les fournisseurs cloud restent des surfaces ou capacités externes ; ils ne constituent pas l'autorité du SIIAOS.

## Contrat documentaire d'une brique

Toute brique active, candidate ou exposée au SIIAOS doit documenter :

1. son **statut** : ACTIF, CONVERGENCE, CANDIDAT, SURFACE, WORKLOAD, HORS PÉRIMÈTRE ou NON CLASSÉ ;
2. son **rôle local** ;
3. ce qu'elle **implique** ;
4. ce qui peut **l'impliquer** ;
5. les **capabilities** qu'elle fournit ou consomme ;
6. ses **interfaces et contrats** ;
7. les **données** qu'elle lit/écrit et leurs classes ;
8. les **autorités et permissions** nécessaires ;
9. les **preuves** attendues pour déclarer une capacité opérationnelle ;
10. ses **dépendances et fallbacks** ;
11. ses **non-rôles** explicites ;
12. son **état de vérité** actuel.

Aucune proximité de nom, de technologie ou de dépôt ne vaut admission.

## Definition of Done globale

Une architecture SIIAOS n'est considérée opérable que lorsque les gates concernés sont prouvés : runtime observé, Golden Mission, traitement local des données requises, contrats canoniques, isolation, Evidence, observabilité, sécurité, restauration, rollback, Radar gouverné, Delivery, RETEX et succession.

Le chantier n'est donc plus d'inventer des couches supplémentaires par défaut. Il consiste à faire progresser les éléments de `DesiredState` vers `ObservedState -> Evidence -> PROUVÉ`.
