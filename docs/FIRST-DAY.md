# First Day Contract

Version: `0.1.0-alpha.1`

## But

Le First Day est la premiere interaction entre une personne et une instance SIIAOS.

Il ne doit pas supposer qui est la personne, ce qu'elle sait, sa machine, ses services, ses dossiers, ses objectifs ou ses valeurs.

## Etat initial obligatoire

```yaml
identity: unknown
context: minimal
observation_scope: none
execution: disabled
network_discovery: disabled
filesystem_scan: disabled
external_services: disabled
```

## Sequence minimale

### 1. Accueil

Le systeme explique ce qu'il sait et ce qu'il ne sait pas.

Aucune observation profonde n'est lancee.

### 2. Contexte declare

L'utilisateur peut indiquer uniquement ce qui est utile maintenant :

- contexte personnel, professionnel, projet ou organisation ;
- objectif court terme ;
- contraintes ;
- ressources qu'il souhaite declarer ;
- responsabilites qu'il souhaite conserver ou deleguer.

Toutes ces informations sont qualifiees `declared`.

### 3. Proposition d'observation

Le systeme propose un perimetre lisible :

```yaml
observation_request:
  reason: "identifier les capacites deja disponibles"
  targets:
    - operating_system_summary
    - declared_directories
    - selected_services
  exclusions:
    - secrets
    - client_data
    - browser_sessions
  mode: read_only
```

### 4. Consentement

Aucun scan ne commence avant consentement explicite.

Le consentement doit etre :

- limite a un perimetre ;
- revocable ;
- journalise ;
- temporel si necessaire ;
- compréhensible sans connaissance technique.

### 5. Decouverte

Les faits observes sont separes des declarations et hypotheses.

Un fait observe doit contenir au minimum :

```yaml
status: observed
source: adapter-id
timestamp: RFC3339
scope: local
```

### 6. Carte de capacites

Le systeme compare :

- besoin ;
- capacites existantes ;
- capacites manquantes ;
- ressources disponibles ;
- responsabilites choisies ;
- contraintes ;
- alternatives.

### 7. Premier sommet

Un sommet est une capacite utile de haut niveau.

Le systeme propose au moins un chemin gouverne vers ce sommet, sans privilegier automatiquement l'installation de nouveaux logiciels.

### 8. Validation et preuve

Toute action modifiant l'environnement doit passer par :

`observe -> plan -> explain -> validate -> prepare -> apply -> verify -> register`

Le First Day est considere reussi lorsqu'une premiere capacite utile est atteinte ou clairement planifiee, avec une preuve et sans avoir impose une architecture inutile.
