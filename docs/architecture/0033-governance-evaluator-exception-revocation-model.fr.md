# Architecture 0033 — Modèle de contrôle des évaluateurs, exceptions et révocation

**Statut :** élément de preuve par model checking enregistré pour une abstraction de contrôle TLA+ bornée. Ce document ne constitue ni une adoption normative, ni une preuve d'implémentation, ni une preuve d'application en production.

## 1. Sujet et objectif

Ce document décrit le modèle de contrôle borné [GovCheckGovernanceControls](../../formal/tla/GovCheckGovernanceControls.tla), introduit pour formaliser certains résultats de la séance d'arbitrage 0008 autorisée par le propriétaire. Il complète le modèle de publication canonique de l'Architecture 0032 ; il ne le remplace pas.

Le modèle couvre cinq sujets :

1. l'évaluateur reconnu par la révision de gouvernance antérieure reste le seul évaluateur faisant autorité ; un remplaçant proposé ne peut produire que des résultats comparatifs/en parallèle ;
2. les résultats d'évaluation restent distincts : `Pass`, `Fail`, `Unknown` et `Conflict` ; unknown et conflict bloquent l'autorisation ;
3. les exceptions explicites sont justifiées, limitées dans le temps, révocables, réservées aux exigences dérogeables et revalidées lors de la publication ; les exigences non dérogeables ne peuvent faire l'objet d'une exception ;
4. la révocation de l'autorité est prospective et bloque les publications suivantes sans supprimer les décisions antérieures ;
5. la requalification historique est représentée par un enregistrement append-only distinct faisant référence à la décision d'origine.

L'évaluation, l'autorisation et la publication restent trois actes logiques distincts dans le modèle de publication canonique sous-jacent. Ce modèle ne les fusionne pas en un acte normatif unique.

## 2. Modèle et configuration exacts

- **Module TLA+ :** `formal/tla/GovCheckGovernanceControls.tla`
- **Configuration TLC :** `formal/tla/GovCheckGovernanceControls.cfg`
- **Git blob — module :** `b237fa3bc939c711f0510c4aeca1346c8e50264f`
- **Git blob — configuration :** `9e8f48d409eeb31adaf22890bbb8ff90674aa96a`
- **Tête de PR vérifiée :** `86713a99574c085ee5a41a71e70f93ab7ce4a831`
- **Checkout CI de fusion :** `1f387b8f6019db545ccd50d55fd9c7cc0d704d80`
- **Exécution du workflow TLC :** [42825118727](https://github.com/Martin-PB/govcheck/actions/runs/42825118727)
- **Job TLC :** `129860312738`
- **Outils TLA :** tla2tools v1.7.4, SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`
- **SANY :** 2.1
- **TLC :** 2.19
- **Java :** Temurin 17.0.21+9

## 3. Propriétés vérifiées

Le module et la configuration exacts ont réussi SANY et TLC. TLC a rapporté :

- **2 826 117** états générés ;
- **1 026 484** états distincts ;
- **0** état restant ;
- profondeur du graphe complet : **12** ;
- aucune violation d'invariant ni de propriété temporelle.

Les neuf invariants configurés ont réussi :

1. `TypeOK` — les variables d'état restent dans les types finis configurés ;
2. `UniquePublishedRevisions` — les enregistrements de publication ne réutilisent pas une identité de révision publiée ;
3. `PublicationUsesPriorAuthority` — la base d'autorisation et la révision résultante sont distinctes ;
4. `ShadowCannotAuthorize` — les évaluations faisant autorité identifient l'évaluateur antérieur ;
5. `UnknownAndConflictBlock` — ni unknown ni conflict ne peuvent soutenir une autorisation ;
6. `NonDerogableNeverExcepted` — une exception active ne peut viser une exigence non dérogeable ;
7. `RevocationIsProspective` — une révocation est associée à une position logique ultérieure ;
8. `HistoricalDecisionsPreserved` — les enregistrements de requalification continuent de référencer la décision de gouvernance d'origine ;
9. `NoStaleAuthorization` — l'autorisation conserve l'identité et la position de base capturées par l'évaluation.

La propriété temporelle `AppendOnly` a également réussi. Elle vérifie que le journal, l'historique des évaluations comparatives, l'historique des décisions et l'historique des requalifications ne font que croître par ajout, sans réécrire leurs préfixes existants.

## 4. Bornes délibérées et limites de l'abstraction

Il s'agit d'un modèle de conception fini, pas d'une preuve d'un protocole général non borné. L'instance TLC utilise volontairement :

- deux valeurs de contenu candidates et deux valeurs de révision de gouvernance ;
- un identifiant d'évaluation faisant autorité et un identifiant d'autorisation ;
- un identifiant d'exception ;
- au plus un résultat comparatif/en parallèle et une requalification historique ;
- une progression du temps logique bornée.

En conséquence, cette exécution **n'établit pas** la concurrence entre publications multiples, une séquence complète de rollback, une succession arbitraire d'évaluateurs, l'identité cryptographique, la délégation, un enregistrement structuré complet d'acceptation du risque, l'expiration en temps réel, le stockage durable du journal, la reprise après panne, la réconciliation de répliques distribuées, la correction des adaptateurs Git/Pijul ni le raffinement de l'implémentation. L'[Architecture 0035](0035-canonical-journal-recovery-model.fr.md) complémentaire vérifie uniquement une abstraction bornée de reprise/rollback à rédacteur unique ; la [Spécification 0007](../specifications/0007-canonical-governance-journal-protocol.fr.md) proposée définit des obligations de protocole, mais ne constitue ni une implémentation ni une vérification de l'ensemble de la spécification. Ces sujets restent des obligations d'ingénierie et de formalisation suivies dans l'issue #86.

Le résultat sur cet espace d'états fini constitue un élément de preuve par model checking pour ces identités exactes de source et de configuration uniquement. Il ne s'agit ni d'une preuve de théorème, ni d'une preuve que le code de production raffine le modèle, ni d'un acte d'adoption normative. Les onze choix sélectionnés par le propriétaire restent des entrées sélectionnées ; l'adoption formelle relève exclusivement de l'autorité du propriétaire du projet.

## 5. Références

- [R-05 — Modélisation des transitions d'état avec TLA+ et TLC](../references.fr.md#r-05)
- [Spécification 0006 — applicabilité des révisions de gouvernance](../specifications/0006-governance-revision-applicability.fr.md)
- [Spécification 0007 — protocole du journal canonique et des adaptateurs VCS](../specifications/0007-canonical-governance-journal-protocol.fr.md)
- [Architecture 0032 — rapport de model checking du modèle de publication canonique](0032-canonical-publication-model-checking.fr.md)
- [Architecture 0035 — modèle de reprise du journal canonique](0035-canonical-journal-recovery-model.fr.md)
- [Compte rendu de séance 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md)
- [Issue #86 — obligations d'ingénierie sur l'applicabilité de la gouvernance](https://github.com/Martin-PB/govcheck/issues/86)
