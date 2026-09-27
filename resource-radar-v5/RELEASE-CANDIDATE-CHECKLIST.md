# Resource Radar V5 — Release Candidate checklist

## Etat du chantier

Branche de convergence : `radar-v5-saas-augmentation`.

Regle : aucun cut-over Vercel tant que les gates P0 ne sont pas tous prouves. Les branches de chantier V5 sont explicitement bloquees dans `ui/vercel.json`.

## P0 — bloque la release

- [x] contrats Lineage Edge / Observation ;
- [x] contrats SaaS augmentation et controle ;
- [x] ADR configuration-first ;
- [x] `execution-estate.schema.json` ;
- [x] `execution-profile.schema.json` ;
- [x] `workload.schema.json` ;
- [x] `execution-plan.schema.json` ;
- [x] `organization-context.schema.json` + `admission-profile.schema.json` + HumanGate deterministe ;
- [x] contrats TAT perceptif et metabolisme numerique ;
- [x] etats de verite PROUVE / REJETE / WATCH / INCONNU restaures ;
- [x] distinction repository / deployment / runtime / data_store / authority restauree ;
- [x] CI : presence et invariants des contrats d'execution ;
- [x] CI : anti-fuite du contexte d'execution dans la projection publique ;
- [x] Vercel : auto-deploy des branches V5 interdit ;
- [x] UI : premiere vue Configuration & execution ;
- [ ] reversionner la V3 effectivement servie et identifier sa source de build ;
- [ ] raccorder la recherche live multi-sources V3 au shell V5 ;
- [ ] raccorder `/api/resolve` ;
- [ ] rendre queue / mirror / manifeste operables depuis la V5 ;
- [ ] tester le bridge local depuis SandY ;
- [ ] produire un premier Execution Estate observe depuis SandY ;
- [ ] produire un premier Workload reel ;
- [ ] produire et verifier un premier Execution Plan a budget incremental zero ;
- [ ] generer un `radar-public.json` reel issu du registre local ;
- [ ] verifier qu'aucune fixture ne peut etre confondue avec une projection publiee.

## P1 — qualite et produit

- [x] workflow GitHub UI V5 dedie ;
- [x] protocole de simulation d'usages versionne ;
- [x] premiers personas synthetiques Estate/Workload ;
- [x] 60 assertions/scenarios automatises (decision, adversarial, composition, admission, signal public, anti-regression de contexte) ;
- [x] 8 parcours navigateur Playwright, verifies apres correction du runner ;
- [ ] adapter `audit_human_ux.py` aux vues V5 et a la terminologie V5 ;
- [x] ajouter captures desktop/mobile de la vue Execution ;
- [ ] ajouter vues Genealogie / Supply-chain / Evidence graph ;
- [ ] rendre Hyperveille evenementielle : release, archive, licence, permissions, faille, rupture d'approche ;
- [ ] materialiser les relations et observations dans un stockage local interrogable ;
- [ ] brancher les profils d'execution aux ressources et benchmarks ;
- [x] marquer le plan produit V4 herite comme baseline non canonique et pointer vers les artefacts V5 ;
- [ ] verifier accessibilite clavier/mobile de toutes les vues V5.

## Expert / publication protegee

- [ ] session Expert revocable ;
- [ ] projection Expert servie cote serveur ;
- [ ] aucune conclusion client, estate, workload ou execution plan prive dans Git/Vercel public ;
- [ ] documents legaux et confidentialite canoniques ;
- [ ] aucune PII dans analytics/tokens.

## Gate Release Candidate

La RC peut etre gelee uniquement lorsque :

1. V3 operationnelle est preservee ;
2. V5 CI et UI Preview sont verts ;
3. un Estate + Workload + Execution Plan reels sont prouves ;
4. la projection publique reelle est revue ;
5. la frontiere public / Expert / local est testee ;
6. le commit RC est fige.

Ensuite seulement :

`Git RC -> un preview Vercel -> recette fonctionnelle + visuelle -> promotion du meme artefact`.

Aucun redeploiement de developpement ne doit remplacer cette sequence.
