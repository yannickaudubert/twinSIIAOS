# ADR — Gate licence, attribution et redistribution

Statut : **DRAFT / GATE ACTIVE**  
Date : 2026-09-18

## Décision

Le noyau SIIAOS n'est pas considéré comme libre/open source au sens OSI tant qu'une licence définitive n'a pas été arrêtée. Le dépôt public reste consultable, mais aucune hypothèse de réutilisation commerciale générale ne doit être déduite de cette visibilité.

La trajectoire retenue à ce stade est **source-available / anti-capture**, avec possibilité de licences différentes selon les actifs.

## Principe

Chaque architecture SIIAOS doit associer à son graphe technique un graphe juridique et de redistribution :

```
Capability
 -> Provider
 -> Package / Model / Dataset / Skill / MCP / Harness
 -> License
 -> Required notices
 -> Redistribution duties
 -> Source-disclosure duties
 -> Commercial-use constraints
 -> Compatibility
 -> User-facing consequences
```

Une architecture techniquement valide mais juridiquement inconnue ou incompatible est **non déployable**.

## Invariants

1. Les obligations amont ne sont jamais supprimées par une surcouche SIIAOS.
2. Les notices, copyrights et obligations de citation restent attachés aux composants concernés.
3. Le système distingue les droits sur :
   - code SIIAOS ;
   - dépendances tierces ;
   - modèles ;
   - datasets ;
   - contenus ;
   - configurations ;
   - artefacts générés.
4. L'utilisateur reçoit les impacts juridiques avant validation d'une projection ou d'un déploiement.
5. Une obligation inconnue sur une dépendance critique provoque un état `legal_status=blocked`.
6. Toute exception commerciale est explicite, versionnée et non rétroactive.
7. Le SIIAOS doit pouvoir générer un SBOM, un THIRD_PARTY_NOTICES et un manifeste juridique lisible machine.
8. Les composants libres conservent leurs propres licences ; le SIIAOS ne les « re-licencie » pas.

## Classification minimale

Chaque composant doit exposer :

- `license_id`
- `license_family`
- `copyright_holder`
- `source_url`
- `attribution_required`
- `notice_required`
- `source_disclosure_required`
- `network_source_disclosure_required`
- `redistribution_required`
- `commercial_use`
- `modified_distribution`
- `patent_terms`
- `trademark_terms`
- `data_or_model_terms`
- `compatibility_status`
- `reviewed_at`
- `evidence_refs`

## Projection utilisateur

Avant activation d'une composition, l'interface doit pouvoir expliquer :

- ce que l'utilisateur peut faire ;
- ce qu'il ne peut pas faire ;
- ce qu'il doit citer ;
- ce qu'il doit redistribuer ;
- ce qu'il doit publier ;
- quelles obligations changent en cas d'usage commercial ;
- quelles dépendances imposent des conditions supplémentaires ;
- quelles alternatives existent si ces obligations ne conviennent pas.

## Modèles de licence à étudier

Aucun choix final n'est pris ici. Les familles à comparer incluent :
- source-available restrictive ;
- PolyForm Small Business ;
- BSL 1.1 ;
- double licence ;
- AGPL/GPL/MPL pour certains modules ;
- Apache/MIT/BSD pour protocoles, schémas ou briques volontairement placées dans les communs.

## Condition de promotion

Aucune release canonique ne franchit la gate tant que le manifeste juridique du lot n'est pas calculable, explicable et testé.
