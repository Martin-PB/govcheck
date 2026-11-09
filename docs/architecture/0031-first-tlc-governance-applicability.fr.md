# 0031 — Première exécution TLC du modèle d'applicabilité de la gouvernance

**Statut :** enregistrement d'exécution pour la [Spécification 0006](../specifications/0006-governance-revision-applicability.fr.md) proposée. Ce document consigne uniquement un résultat de model checking ; il n'adopte pas la spécification et n'établit pas la conformité d'une implémentation. **English:** [0031](0031-first-tlc-governance-applicability.md).

## 1. Objet

Consigner la première exécution SANY/TLC achevée du modèle distinct d'applicabilité des révisions de gouvernance. Ce modèle traite la lacune temporelle identifiée par l'[Architecture 0023](0023-bootstrap-governance-authority.fr.md) : le modèle initial de transition d'autorité n'encodait pas les positions d'effet et ne préservait pas l'applicabilité historique des décisions.

## 2. Sujet exact

- **Dépôt :** `Martin-PB/govcheck`
- **PR :** [#90 — Spécifier l'applicabilité temporelle des révisions de gouvernance](https://github.com/Martin-PB/govcheck/pull/90)
- **Branche :** `work/governance-revision-applicability`
- **Commit source :** `3a8d0176bff8783e25103a4603bb4eea06664cee`
- **Commit de fusion de test contrôlé par le runner :** `e226461` (fusion du commit source dans la base `d04a6dd02d5bdda0b40e4aa740475a8e554e63d7`)
- **Modèle :** `formal/tla/GovCheckGovernanceApplicability.tla`
- **SHA du blob modèle :** `43743eac208f9faf9a844ae35c55ceb6e2b74239`
- **Configuration :** `formal/tla/GovCheckGovernanceApplicability.cfg`
- **SHA du blob configuration :** `54d7387bfe577c5bd9152c7427fc5410c4a00db2`
- **Workflow :** [TLC — modèle d'applicabilité des révisions de gouvernance](https://github.com/Martin-PB/govcheck/actions/runs/42659943881)
- **Job :** `129308483397`
- **Artefact :** [Rapport SANY/TLC et empreinte de l'outil](https://github.com/Martin-PB/govcheck/actions/runs/42659943881/artifacts/13693473469)

## 3. Outils et configuration

- SANY : version 2.1 (24 février 2014).
- TLC : version 2.19 (8 août 2024, révision `5a47802`).
- Java : Temurin 17.0.21+9.
- tla2tools : v1.7.4 épinglée ; SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`.
- Workers TLC : 4.
- Configuration : 2 principaux, 3 révisions de gouvernance, 2 candidats, 3 identifiants d'évaluation, 3 identifiants de décision, historique borné à 3 ; révision de genèse `gov0`, principal racine `alice`.

Cette configuration finie permet au plus deux amendements après la genèse et trois enregistrements d'évaluation/décision. Acteurs et révisions sont des valeurs abstraites du modèle, pas des identités de production.

## 4. Résultat

**Model checked — configuration finie**

- L'analyse syntaxique et le traitement sémantique SANY se sont achevés avec succès.
- TLC a terminé avec : **« Model checking completed. No error has been found. »**
- **20 785 états générés ; 18 067 états distincts ; 0 état restant dans la file.**
- Les invariants configurés et la propriété temporelle `AppendOnly` se sont achevés sans contre-exemple.

Les invariants vérifiés couvrent le typage, l'unicité des révisions, la continuité prédécesseur/position d'effet, l'autorisation par l'autorité applicable à la position de décision, l'utilisation de la révision antérieure applicable, l'absence d'auto-autorisation, la publication strictement postérieure à l'autorisation, la préservation des liaisons historiques et la liaison entre évaluation et décision. La propriété temporelle vérifie la préservation par préfixe des historiques de gouvernance et de décisions.

## 5. Première tentative échouée et correction

La première tentative TLC sur le commit source `eba2a74ec790c013e65f4301a203063d22885943` a échoué après la réussite de SANY. TLC a révélé un défaut d'expression dans le modèle : une expression `CHOOSE` sélectionnait un indice d'évaluation/décision, puis le modèle tentait de lire directement un champ d'enregistrement sur cet entier. Le modèle a été corrigé pour indexer explicitement la séquence correspondante. L'exécution réussie ci-dessus porte sur le commit corrigé `3a8d0176...`.

Cette correction est préservée dans l'historique de la branche ; l'exécution échouée n'est pas présentée comme un succès.

## 6. Interprétation et limites

Il s'agit d'une **preuve issue du model checking**, pas d'une preuve de théorème. TLC a exploré le graphe complet des états atteignables de ce modèle/configuration finis sans trouver de violation des propriétés configurées. Cela ne prouve pas :
- la correction pour des historiques, ensembles de principaux, candidats ou révisions non bornés ;
- l'authenticité cryptographique, la garde des clés ou la liaison d'identité ;
- le consensus distribué ou l'ordre d'événements tolérant aux pannes ;
- toute la concurrence multi-écrivain, la récupération après interruption ou chaque cycle de révocation/dérogation ;
- le raffinement ou la conformité d'une future implémentation ;
- une application impossible à contourner par Git, Pijul, une forge ou une frontière de déploiement ;
- la correction ou l'adoption de la politique normative elle-même.

Le modèle maintient volontairement l'autorité racine constante. Succession/délégation et récupération d'urgence exigent des décisions et extensions distinctes. Le mécanisme canonique d'ordre des événements et le protocole de publication persistante restent également ouverts.

## 7. Documents liés

- [Spécification 0006 — Applicabilité des révisions de gouvernance](../specifications/0006-governance-revision-applicability.fr.md)
- [Spécification 0003 — Cycle de vie des changements](../specifications/0003-change-lifecycle.fr.md)
- [Architecture 0023 — Décision d'amorçage de l'autorité](0023-bootstrap-governance-authority.fr.md)
- [Issue #86 — Travail de spécification technique](https://github.com/Martin-PB/govcheck/issues/86)
- [Issue #41 — Décision d'autorité parente](https://github.com/Martin-PB/govcheck/issues/41)
