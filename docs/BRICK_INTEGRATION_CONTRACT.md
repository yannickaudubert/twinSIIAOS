# Contrat documentaire d'intégration SIIAOS

Ce fichier définit le format minimal à appliquer aux briques impliquées, impliquantes ou impliquables.

## En-tête minimal

```yaml
siiaos_puzzle_version: "2026-09-25"
integration_status: ACTIVE | CONVERGENCE | CANDIDATE | SURFACE | WORKLOAD | OUT_OF_SCOPE | UNCLASSIFIED
truth_status: PROPOSED | CODED | TESTED | DEPLOYED | OBSERVED | PROVEN
authority: "none by default"
```

## Sections obligatoires

- Rôle dans le SIIAOS
- Ce que la brique implique
- Ce qui peut l'impliquer
- Capabilities fournies
- Capabilities consommées
- Interfaces / contrats
- Données et classes de confidentialité
- Autorités / permissions
- Evidence attendue
- Dépendances / fallbacks
- Non-rôles
- État observé vs cible
- Conditions d'admission / promotion
- Conditions de retrait / rollback
- Liens vers sources et décisions

## Invariants à recopier

- Le SIIAOS n'est pas cette brique.
- Une brique ne devient jamais autorité parce qu'elle sait agir.
- `PROPOSÉ != CODÉ != TESTÉ != DÉPLOYÉ != OBSERVÉ != PROUVÉ`.
- `DesiredState != ObservedState`.
- Source originale, index, RAG, interface et canon sont distincts.
- Une donnée confidentielle ne devient pas transverse par apprentissage implicite.
- Une intégration doit pouvoir être remplacée, exportée ou retirée sans perdre le raisonnement, les sources et les preuves.
