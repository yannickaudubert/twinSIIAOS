# Passe 1 - Statut de convergence

Version : `0.1.0-alpha.2`.

## Objectif

Fermer le risque de reconstruction inutile avant import du runtime.

## Fait

- [x] audit de `siiaos-building-local-game-v2.1-step1` ;
- [x] audit de `SIIAOS-BUILDING-V1-DAY1-HARDENED` ;
- [x] audit de `SIIAOS-KOS-v1.0.1-stabilized` ;
- [x] audit de `ARAGORN_SIIAOS_Starter_Kit_v0.1.1` ;
- [x] utilisation du `siiaos-codex-convergence-pack` comme genealogie ;
- [x] classement `REUSE / ADAPT / REFERENCE / ARCHIVE / REJECT` ;
- [x] identification des defaults et donnees ARAGORN dans le tronc historique ;
- [x] cartographie de 39 routes historiques ;
- [x] mapping API historique vers objets canoniques ;
- [x] decision : un seul runtime Go canonique avant v1 ;
- [x] decision : pas de FastAPI/Python control plane dans le noyau v1 ;
- [x] schema canonique initial `core.schema.json` ;
- [x] fixture First Day neutre ;
- [x] CI anti-contamination sur `contracts/` et `examples/` ;
- [x] premiere execution CI reussie ;
- [x] ADR de convergence.

## Gate restant

- [ ] licence libre du noyau decidee et documentee.

Suivi : issue GitHub #2.

## Tests encore a renforcer avant fermeture definitive alpha.2

- [ ] validation semantique complete des fixtures contre JSON Schema ;
- [ ] fixtures invalides pour verifier le refus ;
- [ ] test des references croisees entre besoin, sommet, chemin et action ;
- [ ] test de stabilite des identifiants ;
- [ ] test de provenance obligatoire pour les faits observes.

Ces tests peuvent etre ajoutes sans modifier l'architecture et ne bloquent pas la decision de convergence.

## Conclusion de passe

La convergence technique est suffisamment claire pour preparer la Passe 2, mais aucun code executable historique ne doit encore etre importe tant que la licence du noyau n'est pas tranchee.

Le candidat runtime est le `local-agent` Go de Building v2.1, a extraire par fonctions et non par copie du repertoire complet.

Les premiers morceaux a porter en Passe 2 seront uniquement :

1. demarrage local ;
2. serveur d'assets ;
3. configuration neutre ;
4. journal d'evenements ;
5. contrats Adapter / DiscoveryProvider ;
6. aucune observation avant consentement.
