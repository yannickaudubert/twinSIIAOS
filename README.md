# twinSIIAOS

Surface de convergence et d'expérimentation autour du SIIAOS.

## Documentation canonique de convergence

À lire dans cet ordre pour toute reprise locale :

1. [Puzzle canonique SIIAOS](docs/SIIAOS_PUZZLE.md)
2. [État courant du système local](docs/LOCAL_SYSTEM_CURRENT.md)
3. [Contrat de conception locale](docs/LOCAL_DESIGN_CONTRACT.md)
4. [Registre des lacunes documentaires](docs/DOCUMENTATION_GAP_LEDGER.md)
5. [Runbook de finalisation locale SandY](docs/LOCAL_FINALIZATION_RUNBOOK.md)
6. [Matrice d'acceptation locale](docs/LOCAL_ACCEPTANCE_MATRIX.md)
7. [Index de capitalisation des sources](docs/SOURCE_CAPITALIZATION_INDEX.md)
8. [Standard de reprise humaine](docs/HUMAN_TAKEOVER_STANDARD.md)
9. [Guide par langage et type de fichier](docs/LANGUAGE_AND_FILE_DOCUMENTATION_GUIDE.md)
10. [Politique IA de documentation du code](docs/AI_CODE_DOCUMENTATION_POLICY.md)
11. [Modèle FILE_INDEX](docs/FILE_INDEX_TEMPLATE.md)
12. [Contrat documentaire d'intégration](docs/BRICK_INTEGRATION_CONTRACT.md)

## Règle de reprise

Le chantier local ne repart pas d'une nouvelle architecture :

`documentation canonique -> Truth Pack SandY -> écarts -> paramètres -> bindings -> Golden Mission -> restart -> preuve -> promotion`

Toujours distinguer :

`PROPOSÉ != CODÉ != TESTÉ != DÉPLOYÉ != OBSERVÉ != PROUVÉ`

et :

`DesiredState != ObservedState`.

## Sous-surfaces actuelles

- `public-resource-hub/` : démonstrateur public du Resource Radar.
- `resource-radar-v3/` : portail / bridge de découverte et mirroring de ressources.

Ces sous-surfaces ne constituent pas à elles seules le SIIAOS. Elles doivent respecter la boucle d'admission gouvernée et les Truth Gates décrits dans le puzzle canonique.
