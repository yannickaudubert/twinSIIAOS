# ADR-001 - Convergence de l'heritage vers twinSIIAOS v1

Statut : accepte pour la Passe 1.

## Contexte

Plusieurs lignages SIIAOS existent deja : Building V1/V2, Day1-Hardened, KOS, Starter Kits, cockpits et packs de convergence. Ils contiennent des fonctions utiles mais aussi des implementations concurrentes, des donnees d'instance ARAGORN et plusieurs runtimes.

Importer un pack entier recreerait une architecture parallele au lieu de converger.

## Decision

### 1. Un seul runtime canonique avant v1

Le noyau executable cible reste un binaire Go local, inspire du `local-agent` de `siiaos-building-local-game-v2.1-step1`.

Aucun second control plane Python/FastAPI n'est introduit dans le noyau v1.

### 2. L'heritage est traduit, pas copie

Chaque fonction historique traverse la chaine :

`inspect -> classify -> neutralize -> map -> test -> import`

Une fonction non classee n'entre pas dans le noyau.

### 3. Zero permission avant observation

Les scanners et probes historiques ne sont jamais actifs par default.

Toute observation passe par :

`ObservationRequest -> Consent -> Adapter -> Fact -> Evidence`.

### 4. ARAGORN est une instance de reference

Les chemins, ports, services, materiels et donnees historiques ARAGORN ne sont jamais des defaults publics.

Ils servent uniquement aux tests d'integration locaux ou a des documents historiques explicitement classes.

### 5. Les meilleures idees restent distribuees

- Building V2 : runtime Go et surface operatoire.
- Day1-Hardened : gates, simulation, loopback guard et admission de ressources.
- KOS : formats ouverts, index reconstructible, espaces, jobs tracables et packaging.
- Starter Kit : scenarios doctor/backup/integrite et genealogie de la theorie des sommets.

Le noyau v1 compose ces invariants sans importer les piles entieres.

### 6. L'interface n'est pas la source de verite

Les objets canoniques et le journal doivent rester lisibles sans interface specifique.

Les vues Web, Godot, Backstage ou futures interfaces ne sont que des projections.

## Consequences positives

- reduction du nombre de runtimes ;
- moins de dependances ;
- pas de migration forcee de l'existant ARAGORN ;
- compatibilite future par adapters ;
- meilleur chemin vers un one-click autonome ;
- tests de neutralite possibles avant toute integration locale.

## Consequences negatives

- certaines fonctions historiques devront etre reecrites ou adaptees ;
- la compatibilite avec les anciennes routes n'est pas immediate ;
- l'architecture public v1 n'embarque pas tout l'immeuble historique.

Ces couts sont acceptes car ils evitent la dette d'une federation prematuree de plusieurs control planes.

## Regle de retour

Cette decision peut etre reouverte uniquement si une fonction necessaire a l'un des trois parcours d'or ne peut raisonnablement etre fournie par le runtime Go ou par un adapter externe optionnel.
