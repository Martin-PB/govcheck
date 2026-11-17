# Architecture 0036 — Modèle de liaison du contexte des révisions de gouvernance

**Statut :** élément de preuve par model checking fini pour un contrat borné de liaison intermodèle du contexte. Ce document ne constitue ni une adoption normative, ni une preuve d'implémentation, ni une preuve d'application en production.

## 1. Sujet et objectif

Ce document décrit [GovCheckGovernanceContextBinding](../../formal/tla/GovCheckGovernanceContextBinding.tla), un modèle TLA+ distinct lié à l'issue #86. Il renforce la tranche d'applicabilité temporelle en liant chaque révision de gouvernance au contexte exact d'autorité/évaluateur/spécification/profil dans lequel les évaluations et décisions ont lieu.

Le modèle traite comme identités/révisions distinctes dans un contexte de gouvernance :

- la révision de la politique d'autorité (distincte de l'identité du principal racine) ;
- l'identité et la révision de l'évaluateur ;
- l'identité et la révision de la spécification ;
- l'identité et la révision du profil d'assurance.

Une évaluation enregistre sa révision de gouvernance de base exacte, son jeton de contexte, les identifiants de base/candidat du cycle de vie et l'identité/révision de la spécification. L'autorisation n'est possible que tant que la révision de gouvernance capturée et le contexte complet restent courants. La décision conserve ce contexte exact ainsi que la proposition de gouvernance/contexte résultante. La publication n'établit le contexte résultant qu'à une position logique strictement ultérieure.

## 2. Modèle et configuration exacts

- **Module TLA+ :** `formal/tla/GovCheckGovernanceContextBinding.tla`
- **Configuration TLC :** `formal/tla/GovCheckGovernanceContextBinding.cfg`
- **Git blob — module :** `8a0ae668dab8eb279ed55b39649a326689b5cdac`
- **Git blob — configuration :** `c04a9104c604517c421e765bf22d247b9815a813`
- **Tête de PR vérifiée :** `fdd6eb3a4d93d15d32e7d837ad25604898e9845d`
- **Exécution du workflow TLC :** [44131092595](https://github.com/Martin-PB/govcheck/actions/runs/44131092595)
- **Job TLC :** `134208042142`
- **Outils TLA :** tla2tools v1.7.4, SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`
- **SANY :** 2.1
- **TLC :** 2.19
- **Java :** Temurin 17

Le workflow TLC réutilisable a réussi l'analyse syntaxique/sémantique SANY et le model checking TLC. TLC a rapporté :

- **486 289** états générés ;
- **486 289** états distincts ;
- **0** état restant ;
- profondeur du graphe complet : **8** ;
- aucune violation d'invariant ni de propriété temporelle.

Les douze invariants configurés ont réussi : `TypeOK`, `UniqueGovernanceRevisions`, `GovernanceChainIsContinuous`, `OnlyApplicableAuthorityCanAuthorize`, `DecisionUsesApplicablePriorGovernance`, `EvaluationUsesApplicableContext`, `DecisionUsesApplicableContext`, `EvaluationAuthorizationBinding`, `NoSelfAuthorization`, `PublishedOnlyAfterAuthorization`, `HistoricalDecisionsRemainBound` et `CurrentContextMatchesHead`. La propriété temporelle `AppendOnly` a également réussi.

## 3. Obligations de liaison intermodèle exercées

Le modèle vérifie les relations suivantes :

1. La révision de gouvernance applicable à la position logique d'une évaluation est celle enregistrée dans le tuple d'évaluation du cycle de vie.
2. Le contexte de base de l'évaluation se résout vers la révision exacte d'autorité, l'identité/révision d'évaluateur, l'identité/révision de spécification et l'identité/révision de profil sélectionnées par cette révision de gouvernance.
3. La décision d'autorisation est prise par le principal d'autorité applicable à sa position de décision et conserve les liaisons exactes de base, candidat, gouvernance et contexte de l'évaluation.
4. Un candidat modifiant la gouvernance ne peut pas s'autoriser lui-même : la révision de gouvernance résultante n'est pas applicable à la position de décision.
5. Le contexte résultant n'est publié qu'après la décision d'autorisation et ne devient effectif qu'à une position d'événement ultérieure.
6. Les décisions historiques restent liées au contexte applicable au moment où elles ont été prises, même après la publication d'un contexte ultérieur.
7. Les historiques de gouvernance, d'évaluations et de décisions sont append-only.

Le jeton de contexte possède deux interprétations finies dans cette instance TLC. Il s'agit d'un jeu de test borné, pas d'un format de sérialisation ou d'un schéma de contexte de production sélectionné.

## 4. Limites délibérées

Il s'agit d'un contrat de liaison intermodèle, pas d'une machine à états entièrement intégrée :

- Il n'importe/n'instancie pas les modules complets `GovCheckAuthority`, `GovCheckLifecycle`, `GovCheckCanonicalPublication`, `GovCheckGovernanceControls` et `GovCheckJournalRecovery`. Ceux-ci restent des abstractions finies distinctes.
- Le principal racine est fixe. Le jeton de révision d'autorité représente une modification de la sémantique de l'autorité ; il ne modélise ni succession du principal racine, ni délégation, ni identité cryptographique, ni chaîne d'autorité complète.
- Le modèle enregistre les identifiants de base/candidat du cycle de vie, mais ne maintient pas lui-même une variable mutable de tête du dépôt et ne prouve pas le comportement des adaptateurs Git/Pijul. L'obsolescence de tête capturée et la publication à gagnant unique sont traitées par le modèle de publication canonique distinct.
- L'exécution comparative d'évaluateurs, les exceptions, la résolution de `unknown`/`conflict`, la révocation, le rollback, la reprise après panne, la durabilité du stockage et le consensus distribué restent dans leurs modèles distincts ou parmi les obligations non implémentées.
- Les deux interprétations de contexte codées en dur ne définissent ni manifeste général, ni sérialisation, ni évolution de schéma, ni mécanisme de compatibilité.

Le résultat est un élément de preuve par model checking pour ce modèle/configuration finis exacts uniquement. Il ne s'agit ni d'une preuve de théorème, ni d'un raffinement de l'implémentation, ni d'un enforcement opérationnel, ni d'une assurance cryptographique, ni d'une adoption normative.

## 5. Relation avec la Spécification 0006

Ce modèle fournit une tranche bornée exécutable pour les obligations de liaison d'identité de la Spécification 0006 : la révision d'autorité, l'identité/révision de l'évaluateur, l'identité/révision de la spécification et l'identité/révision du profil doivent être capturées lors de l'évaluation et préservées jusqu'à l'autorisation ; un contexte résultant ne devient applicable qu'après publication. Il ne clôt pas les obligations restantes de la spécification concernant le modèle de confiance/défaillance du journal canonique, la sérialisation du manifeste, l'ajout atomique durable, le cycle de vie des clés, la réconciliation des adaptateurs VCS, le résolveur/persistance intégrés, les suites de conformité exécutables ou le raffinement de l'implémentation.

## 6. Références

- [Spécification 0006 — applicabilité des révisions de gouvernance](../specifications/0006-governance-revision-applicability.fr.md)
- [Compte rendu de séance 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md)
- [Architecture 0023 — décision d'autorité initiale](0023-bootstrap-governance-authority.fr.md)
- [Architecture 0031 — premier modèle d'applicabilité](0031-first-tlc-governance-applicability.fr.md)
- [Architecture 0032 — modèle de publication canonique](0032-canonical-publication-model-checking.fr.md)
- [Architecture 0033 — modèle d'évaluateur, d'exception et de révocation](0033-governance-evaluator-exception-revocation-model.fr.md)
- [Architecture 0035 — modèle de reprise et rollback du journal](0035-canonical-journal-recovery-model.fr.md)
- [R-05 — modélisation des transitions d'état avec TLA+ et TLC](../references.fr.md#r-05)
- [R-17 — métadonnées de gouvernance typées et relations traçables](../references.fr.md#r-17)
- [R-22 — sémantique native de Git et Pijul](../references.fr.md#r-22)
