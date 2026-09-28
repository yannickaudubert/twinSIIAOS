---
name: systematic-debugging
description: Imposer un diagnostic root-cause-first avant de proposer une correction lorsqu'un bug, test, workflow, intégration, runtime, machine ou service se comporte mal. Utiliser sur échec de test, comportement inattendu, divergence entre environnements, panne n8n/MCP/agent, incident multi-composants ou succession de corrections infructueuses. Tracer les frontières entre dépôt, déploiement, runtime et environnement réel, formuler une hypothèse falsifiable, tester une variable à la fois puis vérifier le symptôme d'origine. Ne pas déclencher pour une architecture greenfield sans panne observée.
---

# Déboguer systématiquement

## Règle

Ne pas proposer de correctif avant d'avoir établi au moins une observation concrète du problème et une hypothèse sur sa cause.

Séparer explicitement :

- état souhaité ;
- état du dépôt ;
- état déployé ;
- état runtime ;
- machine, service ou environnement concerné.

Ne jamais déduire l'identité ou l'état d'une machine, d'un dépôt ou d'un service à partir d'un contexte ancien lorsque cela change le diagnostic.

## Workflow

### 1. Capturer le symptôme

- Nommer ce qui échoue et où.
- Lire l'erreur complète, les codes et les traces disponibles.
- Reproduire si possible.
- Si le problème n'est pas reproductible, collecter davantage de données au lieu de deviner.

### 2. Localiser la frontière défaillante

Pour un système multi-composants, tracer l'entrée et la sortie de chaque frontière pertinente :

`source -> workflow -> service -> runtime -> stockage -> retour`

Comparer les mêmes données, versions et paramètres des deux côtés de la frontière.

### 3. Comparer un état qui marche et un état qui échoue

Chercher les différences de version, configuration, dépendances, permissions, données, ressources et environnement. Ne pas éliminer une différence sans preuve.

### 4. Formuler une hypothèse falsifiable

Écrire une cause candidate précise et la raison qui la rend plausible. Définir le plus petit test capable de la réfuter ou de la confirmer.

Tester une variable à la fois.

### 5. Corriger la cause

N'appliquer qu'un changement correspondant à l'hypothèse établie. Éviter les améliorations opportunistes « tant qu'on y est » qui brouillent le diagnostic.

Si plusieurs correctifs successifs échouent ou déplacent le problème, arrêter l'empilement de patches et réexaminer l'architecture, le couplage ou les hypothèses de base.

### 6. Vérifier la résolution

Rejouer le symptôme d'origine, puis les régressions pertinentes. Utiliser le skill `verification-before-completion` avant de déclarer l'incident résolu.

## Cas multi-environnements

Quand le même flux produit des résultats différents dans ChatGPT, n8n, CLI, MCP, SandY ou un autre SI :

1. comparer exactement le même payload ;
2. comparer version/commit/configuration ;
3. comparer transport et sérialisation ;
4. comparer variables d'environnement et permissions ;
5. comparer runtime et dépendances ;
6. seulement ensuite modifier la logique.

## Statut et RETEX

Une hypothèse rejetée reste rejetée ; ne pas la réécrire rétroactivement comme si elle avait été correcte.

Pour un incident opérationnel utile à capitaliser, conserver le symptôme, la cause démontrée, la preuve, le correctif et les conditions de réapparition.

Pour l'origine et la méthode d'adaptation, consulter `references/provenance.md` uniquement si nécessaire.
