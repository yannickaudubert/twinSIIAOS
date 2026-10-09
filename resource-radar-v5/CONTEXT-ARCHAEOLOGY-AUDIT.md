# Resource Radar V5 — audit d'archéologie de contexte

Date de reprise : 2026-09-27.

## Règle de lecture

Ce fichier distingue :
- **OBSERVE DANS GIT** : présent dans la branche et inspecté ;
- **RECUPERE DES ECHANGES** : contrainte ou concept antérieur retrouvé, utile comme exigence mais pas comme preuve runtime ;
- **CORRIGE** : défaut concret identifié puis modifié dans la V5 ;
- **INCONNU / A REVALIDER** : ne doit pas être promu sans observation ou preuve.

## OBSERVE DANS GIT

- branche de convergence : `radar-v5-saas-augmentation` ;
- PR draft #10 ;
- contrats Resource / Lineage / Observation / Execution ;
- planner déterministe local ;
- CI V5 et workflow UI V5 ;
- Vercel auto-deploy désactivé pour les branches V5 de chantier ;
- branche historique `work/capability-admission-registry` contenant une spec d'admission/maturité et un registre bootstrap.

## Anomalies / régressions trouvées et corrigées

### 1. États de vérité incomplets

**Défaut :** le `ResourceRecord` V5 n'exposait plus explicitement `proven / rejected / watch / unknown`, alors que ces distinctions existaient dans les travaux antérieurs.

**Risque :** réduction silencieuse de l'inconnu ou du rejet à un état générique.

**CORRIGE :**
- états ajoutés au contrat ;
- labels et filtres UI ajoutés ;
- test de non-régression.

### 2. Confusion possible entre dépôt, déploiement, runtime et autorité

**Défaut :** le type de ressource restait trop générique.

**Risque :** déduire un état machine/runtime depuis Git ou traiter une projection comme source d'autorité.

**CORRIGE :**
- kinds `repository / deployment / data_store / authority / registry / projection / peer` ;
- `surface_role` explicite ;
- test de non-régression.

### 3. Observation sans vérité explicite du claim

**Défaut :** une Observation indiquait sa source et confiance mais pas le statut `observed / realised / verified / blocked / unknown` du claim.

**CORRIGE :**
- `claim_status` ;
- environnement `estate/node/runtime/deployment`.

### 4. Faisabilité technique confondue avec admissibilité

**Défaut :** ExecutionPlan pouvait répondre "faisable" sans représenter maturité organisationnelle, risque ou HumanGate.

**CORRIGE :**
- `OrganizationContext` ;
- `AdmissionProfile` ;
- `ExperimentContract` ;
- moteur d'admission séparé ;
- R3/R4 HumanGate obligatoire ;
- organisation autorisée à être plus stricte, par exemple gate dès R2.

### 5. Coût absent interprété comme zéro

**Défaut :** le planner utilisait 0 EUR lorsque `incremental_eur` était absent.

**Risque :** transformer une inconnue économique en option gratuite.

**CORRIGE :** coût absent -> `unknown`.

### 6. Quality floor présent mais non appliqué

**Défaut :** le Workload possédait `quality_floor`, mais le planner pouvait sélectionner un profil sans preuve de ce niveau.

**CORRIGE :**
- `quality_claims` dans ExecutionProfile ;
- quality floor non prouvé -> `unknown` ;
- contrôle limité à la capacité effectivement évaluée.

### 7. Contrôle qualité initialement trop large

**Défaut introduit pendant correction :** un quality floor d'une autre capacité du même profil pouvait contaminer la capacité en cours.

**CORRIGE :** test et contrôle par capability.

### 8. Provider externe insuffisamment borné

**Défaut :** autoriser globalement les providers externes pouvait suffire.

**CORRIGE :**
- local-only ;
- offline-required ;
- classes de données locales ;
- allowlist explicite par workload ;
- budget toujours appliqué.

### 9. Workflow UI Playwright mal câblé

**Défaut :** Chromium était installé mais `@playwright/test` ne l'était pas dans le workspace.

**CORRIGE :** installation explicite du runner ; run ultérieur vert.

### 10. Plan produit V5 encore présenté comme V4 canonique

**Défaut :** `PRODUCT-PREMIUM-UX-WORKPLAN.md` restait intitulé et lu comme plan V4.

**CORRIGE :** marqué baseline héritée, non canonique pour la DoD V5.

## RECUPERE DES ECHANGES ET REINTEGRE

### Configuration first-class
`Observed Estate -> Workload -> Capability composition -> Execution Plan -> Evidence`.

### Maturité multidimensionnelle
Axes : gouvernance, delivery, opérations, observabilité, sécurité, données, usage IA, automatisation, open source, contrôle humain. Pas de score global canonique.

### TAT perceptif
Dimensions indépendantes : compréhension, utilité, confiance, ouverture, autonomie, humanité, risque perçu, intention d'usage.

### Métabolisme numérique
Capacité, flux, production, stock, inertie, réutilisation, capital dormant. Les métriques de valeur restent nulles si elles ne sont pas prouvées.

### HumanGate
La capacité technique n'implique pas l'autorisation opérationnelle. Les risques élevés et mutations sensibles restent soumis à gate humain.

### Capital numérique dormant
Le Radar doit pouvoir mesurer ce qui est possédé mais non exploité et favoriser la réutilisation avant l'achat ou la dépendance externe.

### Chaîne preuve
Signal / Observation / Claim / Evidence / Status doivent rester distingués. Répétition d'une affirmation ou résumé assistant ne constitue pas une preuve indépendante.

## Ancienne branche Capability Admission : précaution

La branche `work/capability-admission-registry` contient une spec utile et des contrats historiques. Son README décrit aussi des moteurs `capability-core/engine.py` et `engine.js`.

Lors de cet audit, ces moteurs ne figurent pas dans le diff de la branche comparé à `main`.

**Conclusion :** utiliser cette branche comme source de concepts et contrats, pas comme preuve qu'un moteur d'admission avait déjà été implémenté ou validé.

## INCONNU / A REVALIDER

- inventaire réel courant de SandY pour produire un Execution Estate prouvé ;
- source exacte et code effectivement servi par la V3 Vercel historique ;
- fonctionnement réel search/resolve/queue/mirror/bridge V3 depuis la future V5 ;
- registre local réel alimentant `radar-public.json` ;
- valeurs réelles de Resource Utilisation Gap, Capability Unlock Potential et Avoided Spend ;
- mesures TAT issues de vrais utilisateurs humains ;
- matérialisation locale du graphe et Evidence Ledger ;
- session Expert révoquable et projection serveur protégée.

## Règle anti-régression retenue

```text
source != observation != claim != evidence != decision
repo != deployment != runtime != authority
technically feasible != organisationally admissible
unknown != zero != false != incompatible
popular != suitable
installed != tested != proven
```
