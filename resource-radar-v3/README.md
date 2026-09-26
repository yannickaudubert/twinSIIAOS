# SIIAOS Resource Radar V3

V3 operationnelle du portail public AgorIA / SIIAOS pour hyperveille et ressources IA.

## Capacites

- Catalogue public de 41 sources.
- Recherche live multi-sources : Hugging Face models/datasets, Civitai, GitHub, arXiv, OpenRouter.
- Resolution d'artefacts : fichiers HF, fichiers/version Civitai, ZIP GitHub, PDF arXiv.
- File de mirroring persistante dans le navigateur.
- Generation de commandes : PowerShell, CMD, Linux Bash, macOS zsh, WSL, POSIX/BSD, Python, Docker.
- Export manifeste JSON.
- Bridge local Python sans dependance : telechargement direct source -> disque, localhost uniquement, token, SHA-256.

## Production

https://siiaos-resource-radar.vercel.app

## Securite / gouvernance

Le bridge ne permet pas l'execution de commandes arbitraires. Il accepte uniquement des telechargements HTTP(S) vers un repertoire racine choisi au lancement. Le telechargement est distinct de l'installation/activation.

## Relation au SIIAOS

**Statut : ACTIF comme surface Radar, admission des ressources toujours gouvernée.** Découvrir, résoudre ou télécharger un artefact ne l'installe pas et ne lui accorde aucune autorité. Les sorties du Radar alimentent une boucle de qualification et d'expérimentation ; elles ne modifient pas directement le canon ou le runtime.

Voir le [puzzle canonique SIIAOS](../docs/SIIAOS_PUZZLE.md).
