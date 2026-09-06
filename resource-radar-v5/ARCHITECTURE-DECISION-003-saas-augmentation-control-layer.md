# ADR-003 — Augmentabilite SaaS, couche de controle et extensions navigateur

## Statut

Accepted for implementation on `radar-v5-saas-augmentation`.

## Contexte

Le Resource Radar V5 sait deja representer des ressources, leurs dependances, leurs preuves, leur filiation et leurs observations runtime. Il manquait cependant une lecture explicite des solutions proprietaires deja utilisees par une organisation : un SaaS peut etre pertinent et conserve, tout en etant augmente, interface, double localement ou rendu reversible.

La fouille ChatGPT / Tampermonkey a montre qu'un besoin fonctionnel peut etre couvert par plusieurs couches : application officielle, plugin, API, SDK, webhook, MCP, CLI, export, sauvegarde, extension navigateur, userscript, userstyle, sidecar ou miroir local. Ces mecanismes ne doivent pas devenir un second catalogue separe du Radar.

## Decision

La greffe respecte les trois objets canoniques V5 :

1. **Resource Record** — le SaaS, le plugin, le userscript, le connecteur ou le sidecar reste une ressource normale ;
2. **Lineage Edge** — la relation vers la ressource cible devient une relation explicite (`augments`, `interfaces_with`, `mirrors`, `backs_up`, etc.) ;
3. **Observation** — la decouverte, l'analyse de permissions, le risque, un test isole ou une verification runtime restent des faits dates et sourcables.

Aucun quatrieme type canonique n'est introduit.

## Strategie par SaaS

Le Radar peut associer plusieurs strategies simultanees :

- `use` — conserver le service tel quel ;
- `augment` — enrichir l'interface ou les fonctions ;
- `interface` — utiliser API, SDK, webhook, MCP, CLI ou connecteur ;
- `mirror` — doubler donnees, metadonnees ou artefacts sous controle local ;
- `archive` — conserver une trace exploitable hors du SaaS ;
- `hybridize` — repartir les fonctions entre SaaS et briques locales/open source ;
- `replace` — preparer ou executer une migration ;
- `exit_ready` — maintenir formats, exports et procedure de sortie testables.

Une alternative n'est donc plus seulement un remplacant. Elle peut etre un complement, une passerelle, un miroir, un frontend, un backend, une sauvegarde ou un plan de sortie.

## Ordre de preference des mecanismes

Le Radar privilegie les surfaces supportees avant les interceptions fragiles :

```text
official app / plugin
  -> UI extension
  -> API / SDK
  -> webhook / events
  -> MCP / agents
  -> CLI
  -> export / backup
  -> local mirror / sidecar
  -> browser extension
  -> userscript / userstyle
  -> DOM hook en dernier recours
```

## Sources userscripts

Les catalogues sont des **adapters**, jamais des autorites metier. Le premier graphe de sources comprend :

- Userscript.Zone ;
- Greasy Fork ;
- OpenUserJS ;
- GitHub / Gist ;
- ScriptCat ;
- GitLab ;
- Userstyles.org ;
- Userscripts.org Mirror comme archive ;
- Sleazy Fork en quarantaine par defaut pour les usages entreprise.

La provenance originale, les metadonnees, le hash du code et la date d'observation sont conserves.

## Gate de securite userscript

La decouverte n'installe et n'execute jamais un script. Le screening statique inspecte au minimum :

- `@match` / `@include` ;
- `@grant` ;
- `@connect` ;
- `@require` / `@resource` ;
- `unsafeWindow` ;
- acces cookies, session ou tokens ;
- `eval`, `new Function` et execution dynamique ;
- dependances distantes mutables ;
- hash SHA-256 du code acquis.

Les secrets/tokens, l'evaluation dynamique non justifiee et l'acces session/cookies a risque entrainent un blocage ou une reecriture avant tout test. Les essais se font dans un profil navigateur isole.

## Profils associes aux Resource Records

Deux profils optionnels enrichissent un Resource Record sans modifier le canon :

- `control_profile` pour la solution/SaaS : augmentabilite, reversibilite, gouvernance, controle SIIAOS, lock-in et strategies ;
- `augmentation` pour la brique d'augmentation : mecanisme, cible, provenance catalogue, permissions, hash, risque, statut de revue et action recommandee.

Les schemas de ces profils sont des contrats auxiliaires. Le `resource-record.schema.json` reste le contrat canonique du noeud.

## Publication

Le detail des permissions, des destinations reseau, des constats de securite, des chemins locaux et des decisions de mission reste local/protege par defaut.

Une projection publique peut exposer, apres decision explicite, une synthese de strategie ou de controle. Elle ne doit jamais publier automatiquement le metadata brut d'un userscript ni transformer une observation communautaire en recommandation.

## Integration Hyperveille

Cette extension ne cree pas une seconde Hyperveille. Les adapters alimentent observations et ressources du graphe existant. L'Hyperveille peut signaler une nouvelle version, un changement de permissions, une disparition, une faille ou une alternative ; le Radar qualifie ensuite l'impact et les options.

## Gate Git / Vercel

La regle V5 est conservee : Git est le chantier et la memoire ; tests et artefacts precede tout deploiement ; Vercel reste un preview ponctuel de recette une fois le candidat coherent. Aucun deploiement public n'est declenche par la simple decouverte d'une augmentation.
