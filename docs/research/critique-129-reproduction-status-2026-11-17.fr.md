# État de reproduction de la critique externe #129 — 2026-11-17

**Cible de l'audit :** `main` au commit `f27697dac4ceaa6245b6cd796646d7040b12c9b5`  
**Arbre :** `3604f0e10765afebef6ea7308f94b488247ba8a8`  
**Chantier parent :** [Issue #130](https://github.com/Martin-PB/govcheck/issues/130)  
**Critique source :** [Issue #129](https://github.com/Martin-PB/govcheck/issues/129)

## 1. Périmètre et catégories de preuve

Ce rapport distingue :

1. l'inspection directe des sources de l'arbre exact de `main` indiqué ci-dessus ;
2. les éléments historiques de GitHub Actions issus de la tête de la PR #133, commit `15372f5ca90f5b454a2ff30fa0c0b0fdddab1639` (qui n'est pas la cible de l'audit) ;
3. la reproduction locale indépendante, qui **n'a pas encore été achevée**.

Aucun workflow GitHub Actions n'a été déclenché pour ce rapport. Les contrôles historiques de la PR ont été consultés sans être relancés. Aucun résultat historique de la PR n'est présenté comme une vérification du `main` courant.

## 2. Constats sur les sources de main

| Point de la critique | Qualification actuelle | Éléments source |
|---|---|---|
| 6.1 Modèle canonique exécutable | **Lacune d'implémentation confirmée.** La Specification 0002 indique toujours qu'il s'agit d'une architecture proposée et précise explicitement qu'aucun schéma ni évaluateur n'est implémenté. Les garanties décrites sont des objectifs, pas des garanties opérationnelles. | `docs/specifications/0002-canonical-governance-model.md`, ligne 3 et ligne 60. |
| 6.2 Journal canonique | **Partiellement confirmé ; la critique doit être nuancée.** La Specification 0007 définit désormais un contrat sémantique indépendant des technologies : append, compare-and-append, commit durable, récupération après crash, retry idempotent, observation des répliques et réconciliation VCS. Elle reste explicitement proposée, non adoptée et non implémentée. | `docs/specifications/0007-canonical-governance-journal-protocol.md`, lignes 3, 7, 11, 68–87. |
| 6.3 Autorité / séparation des rôles | **Partiellement confirmé.** La conception distingue l'autorisation normative, l'évaluation/revue technique et l'exécution, mais ne garantit pas une séparation entre deux personnes dans tous les déploiements ; un principal racine unique reste une hypothèse explicite de confiance au bootstrap. Il ne faut pas présenter la revue indépendante facultative comme une règle universelle à deux personnes. | `docs/architecture/0023-bootstrap-governance-authority.md` ; voir aussi le [triage source-level](critique-129-source-triage.fr.md). |
| 6.4 Attestation de revue indépendante | **Faiblesse structurelle confirmée dans la tranche exécutable actuelle.** `rule_independent_review` lit `docs/attestations/*.json`, compare `candidate_rev` au SHA exact du candidat et compare une chaîne libre `reviewer` à la chaîne de l'auteur Git. L'attestation est lue dans l'arbre candidat lui-même. Un fichier inclus dans un commit ne peut normalement pas contenir le SHA de ce même commit sans problème d'auto-référence/de point fixe. La comparaison de chaînes n'authentifie pas le reviewer. | `govcheck/check.py`, lignes 282–299 ; SHA candidat et auteur alimentés lignes 385–393. |
| 6.5 Enforcement de l'acceptation CI | **Confirmé.** Le workflow de la tranche GovCheck est explicitement en mode report-only. Les tests unitaires bloquent, mais l'étape d'évaluation utilise `continue-on-error: true` et se termine par `|| true`. Un évaluateur fail-closed ne constitue donc pas, à lui seul, une barrière CI d'acceptation. | `.github/workflows/govcheck-check.yml`, lignes 1, 37–42. |
| 6.6 Mapping sémantique partiel | **Confirmé.** `SemanticBridge.partialMapping` accepte un prédicat `domain : source → Prop` et ne prouve la cible que pour les membres de ce domaine. Il n'exige pas qu'un membre du domaine existe. Par exemple, avec source `True`, cible `False` et domaine `fun _ => False`, l'obligation du constructeur est satisfaite de manière vacante. Ce n'est pas une dérivation de False à partir de True ; c'est un mapping sans cas source couvert. | `formal/lean/GovCheckCoherence/Mapping.lean`, lignes 63–66. |
| 6.7 Séparation physique du journal | **L'affirmation de la critique sur une infrastructure physiquement distincte n'est pas étayée par la spécification actuelle.** La Specification 0007 sépare les actes logiques d'évaluation, d'autorisation et de publication, tout en permettant leur exécution dans une même transaction technique atomique. Elle définit l'append durable comme point de commit, sans imposer une base de données ou un service séparé. | `docs/specifications/0007-canonical-governance-journal-protocol.md`, lignes 68–72 et 84–96. |

### Contre-exemple minimal pour le point 6.6

Le constructeur accepte :

`SemanticBridge.partialMapping (source := True) (target := False) (domain := fun _ => False) (by intro h hd; exact False.elim hd)`

Le second argument est valide parce qu'il n'existe aucun `h : True` pour lequel le domaine déclaré est satisfait. Il manque actuellement un témoin de non-vacuité tel que `∃ h, domain h`. L'obligation d'imposer un domaine non vide à tout mapping partiel relève d'une décision de contrat ; le type actuel n'exprime pas cette condition.

### Identité et révision de l'attestation

Le format actuel confond trois préoccupations distinctes :

- **liaison à une révision :** quel candidat exact est revu ;
- **authentification du reviewer :** qui a émis l'attestation ;
- **transport/stockage de l'attestation :** comment l'associer au candidat sans exiger que le candidat contienne son propre identifiant final de commit.

Le code actuel ne vérifie qu'une approximation par chaînes des deux premières et stocke l'enregistrement dans l'arbre candidat. Une attestation détachée/signée, une identité de revue native de la forge ou un objet d'attestation gouverné séparément pourraient résoudre le cycle ; le choix de l'une de ces solutions relève d'une décision d'architecture et n'est pas fait silencieusement ici.

## 3. Contrôles existants sur la cible exacte `main`

GitHub possède déjà trois contrôles déclenchés par push et attachés au commit exact de l'audit `f27697dac4ceaa6245b6cd796646d7040b12c9b5` (2026-11-14). Ces enregistrements existants ont été consultés ; ils n'ont pas été relancés pour ce rapport.

| Contrôle | Résultat | Interprétation |
|---|---|---|
| Intégrité des références | **PASS — 0 avertissement** | Le vérificateur du catalogue central et de ses backlinks a réussi sur ce commit exact de `main`. |
| Alignement des paquets | **success** | Le contrôle d'alignement paquet/template déclaré par manifeste a réussi. |
| Tranche GovCheck | **job success**, avec **84 tests unitaires réussis** | La suite bloquante de tests unitaires a réussi. Cependant, la sortie JSON/standard de l'évaluateur indique **overall FAIL**, car il ne reconnaît pas de section References admissible dans six documents de décision/dossier. Il s'agit en partie d'un faux négatif du validateur : les documents 0008 et 0009 contiennent déjà des liens pertinents vers le catalogue dans leur traçabilité/métadonnées, mais pas sous un titre reconnu ; le dossier de métamodèle possède un titre `## 17. References` numéroté, mais le validateur n'accepte que les titres non numérotés et arrête l'extraction de cette section avant la sous-section séparée contenant les liens sources. L'étape est report-only (`continue-on-error` et `|| true`) ; la conclusion positive du workflow ne signifie donc pas que le candidat a passé l'évaluateur. |

Les six documents signalés par l'évaluateur sont :

- `0008-governance-applicability-arbitration-session.md` et son équivalent français ;
- `0009-intent-record-and-authority.md` et son équivalent français ;
- `metamodel-design-dossier.md` et son équivalent français.

**Nuance importante :** ces six constats révèlent une limite de reconnaissance des sections par l'évaluateur, et non six documents dépourvus de sources. Les comptes rendus 0008 possèdent les liens vers le catalogue dans leur section de traçabilité ; les ADR 0009 les possèdent dans leur ligne de métadonnées References. Le dossier de métamodèle contient déjà `## 17. Références`, mais le validateur rejette les titres numérotés et les liens vers le catalogue se trouvent sous le titre suivant `## Liens complets vers le catalogue des sources`. Une branche de correction reconnaît désormais les titres numérotés et rend les sources existantes visibles pour la règle ; voir la section 6.

Enregistrements existants :

- [Intégrité des références sur le commit audité](https://github.com/Martin-PB/govcheck/actions/runs/43591371080/job/132436604521)
- [Tranche GovCheck sur le commit audité](https://github.com/Martin-PB/govcheck/actions/runs/43591371057/job/132436604528)
- [Alignement des paquets sur le commit audité](https://github.com/Martin-PB/govcheck/actions/runs/43591371071/job/132436604617)

Le jeu de contrôles attaché à ce `main` exact ne contient aucun run Lean ni TLC. Les résultats historiques de la PR #133 ci-dessous ne doivent pas se substituer à ces contrôles manquants.
## 4. Contrôles historiques sur la PR #133 (pas une vérification du main courant)

Les contrôles suivants existaient déjà pour la tête de la PR #133, commit `15372f5ca90f5b454a2ff30fa0c0b0fdddab1639`. Ils ont été exécutés le 14 novembre 2026 et ne constituent que des éléments sur cette révision de la PR.

| Contrôle | Résultat | Interprétation |
|---|---|---|
| Tests unitaires Python dans `govcheck-check` | **90 réussis** | L'étape bloquante de tests unitaires a réussi sur le checkout de merge de la PR. |
| Évaluateur GovCheck dans le même job | **overall FAIL**, alors que la conclusion du job est success | L'évaluateur n'a pas reconnu de section References admissible dans six documents de décision/dossier (voir la nuance sur la reconnaissance des sections ci-dessus). L'étape report-only a masqué le code de sortie non nul de l'évaluateur, ce qui confirme la lacune d'enforcement du point 6.5. |
| Validateur de gouvernance de version | **13 réussis** | Suite ciblée, pas reproduction complète de #130. |
| Cohérence Lean | **job success** | L'audit d'axiomes configuré a respecté sa politique. Le journal indique aussi `propext` pour plusieurs déclarations SACM ; il ne faut donc pas résumer le résultat par « tout le développement Lean est sans axiome ». |
| Alignement des paquets | **success** | Le contrôle d'alignement paquet/template a réussi sur le checkout de la PR. |
| Capture des sources OMG épinglées | **success** | Le contrôle de capture/digest a réussi sur le checkout de la PR. |
| Intégrité des références | **failure** | Le vérificateur a planté avec `ValueError` : `formal/lean/README.md` est hors de `docs/`, alors que `logical_doc` appelle `path.relative_to(DOCS)` pendant la résolution d'un backlink du catalogue. |

Exécutions historiques pertinentes :

- [Échec reference-integrity](https://github.com/Martin-PB/govcheck/actions/runs/43587576876/job/132425268063)
- [Tests Python et évaluateur report-only](https://github.com/Martin-PB/govcheck/actions/runs/43587576725/job/132425267482)
- [Cohérence Lean et rapport d'axiomes](https://github.com/Martin-PB/govcheck/actions/runs/43587576783/job/132425267822)
- [Validateur de gouvernance de version](https://github.com/Martin-PB/govcheck/actions/runs/43587576734/job/132425267700)
- [Alignement des paquets](https://github.com/Martin-PB/govcheck/actions/runs/43587576727/job/132425267693)
- [Capture des sources OMG](https://github.com/Martin-PB/govcheck/actions/runs/43587576732/job/132425267619)

Aucun run TLC des huit couples modèle/configuration TLA+ courants ne faisait partie de ces six contrôles de la PR #133. Les chemins modifiés par la PR n'apportaient donc pas de preuve fraîche de model checking pour la cible de cet audit.

## 5. Limites formelles qui demeurent

1. **Sûreté et vivacité :** les invariants et l'exploration bornée d'états n'établissent pas, sans hypothèses de fairness et hypothèses environnementales adaptées, le progrès éventuel ou la disponibilité.
2. **Tranches TLA+ séparées :** les modèles de journal, cycle de vie, autorité, assurance, applicabilité/contrôles de gouvernance et routage CI sont des modèles de conception bornés distincts. La Specification 0007 dit elle-même qu'ils constituent des éléments de conception composables, pas un modèle intégré de l'implémentation. Aucune relation de raffinement de bout en bout vers le vérificateur Python ou un runtime de production n'est établie.
3. **Force des théorèmes Lean :** le théorème générique `kind_mapping_rule_theorem_proof_requires_derivation` conclut à l'existence d'une dérivation accompagnée de `derivation.proof = derivation.proof`. Cette égalité est réflexive ; le contenu utile est le témoin existentiel transporté par le constructeur. Le théorème n'établit pas indépendamment une propriété sémantique supplémentaire de la dérivation. Les noms et les affirmations doivent rester alignés sur la proposition réellement démontrée.
4. **Périmètre exécutable :** le `govcheck/check.py` actuel contient huit règles : présence de licence, décisions bilingues, paires de manifeste, intégrité des références, présence des sources, intégrité du bootstrap, fraîcheur des preuves TLA et attestation de revue indépendante. Il n'implémente pas le cycle de vie canonique, le registre d'autorité, le protocole de journal, la sémantique des risques/décisions ni les contrats complets d'assurance intermodèles.


### Inventaire actuel des modèles/configurations TLA+ (inspection des sources uniquement)

L'arbre courant contient huit couples `.tla`/`.cfg`. Le workflow réutilisable épingle TLA+ tools 1.7.4 par SHA-256 et utilise Java 17 ; il exécute SANY avant TLC et conserve les sorties des modèles comme artefacts. Les workflows spécifiques routent les huit couples via cinq points d'entrée (routage CI, assurance, autorité, applicabilité/contrôles/publication/récupération de gouvernance et cycle de vie).

| Modèle | Configuration finie | Propriétés nommées dans la configuration |
|---|---|---|
| `CICheckRouting` | 15 catégories de changements ; politique de routage uniquement | TypeOK ; absence de déclenchement par documentation sans rapport ; isolation cycle de vie/assurance/autorité ; invalidation par runner partagé ; couverture de chaque modèle. |
| `GovCheckAssurance` | 2 affirmations, 2 éléments probants, 2 dépendances, 2 versions, 2 acteurs ; `MaxTime=2` | 7 invariants sur la bonne formation du graphe, la liaison de revue, la cohérence des affirmations, le soutien/snapshot d'acceptation et la révocation ; propriété temporelle `AcceptedDiscipline`. |
| `GovCheckAuthority` | 2 principaux, 3 révisions ; historique limité à 4 | TypeOK ; modification par l'autorité courante, continuité de chaîne, absence de réutilisation de révision ; `HistoryIsAppendOnly`. |
| `GovCheckCanonicalPublication` | 2 principaux, 3 révisions de gouvernance, 2 candidats, 3 identifiants d'évaluation et 3 d'autorisation | TypeOK ; unicité des révisions, continuité des prédécesseurs, une publication par position, liaison évaluation/autorisation, point d'effet, autorisation et absence de publication périmée ; `AppendOnly`. |
| `GovCheckGovernanceApplicability` | 2 principaux, 3 révisions de gouvernance, 2 candidats, 3 évaluations et 3 décisions ; historique limité à 3 | TypeOK ; unicité/continuité de l'historique, autorité applicable, décision sous gouvernance antérieure, absence d'auto-autorisation, publication autorisée, liaison historique et liaison évaluation/autorisation ; `AppendOnly`. |
| `GovCheckGovernanceControls` | 3 principaux, 2 révisions, 2 contenus candidats, 1 évaluation, 1 autorisation, 1 exception | TypeOK ; unicité des révisions, autorité antérieure, restriction de l'évaluateur parallèle, blocage unknown/conflict, non-dérogabilité, révocation prospective, préservation historique et absence d'autorisation périmée ; `AppendOnly`. |
| `GovCheckJournalRecovery` | 2 contenus, 2 identifiants de révision, 2 identifiants d'événement, `MaxEvents=2`, répliques Git et Pijul | TypeOK ; unicité des événements/révisions, continuité position/prédécesseur, rollback comme nouvel événement, observation VCS non autoritative et état appliqué durable ; `AppendOnly`. |
| `GovCheckLifecycle` | 2 acteurs, 1 approbation requise, historique limité à 12 ; 2 bases, candidats, révisions de gouvernance et spécifications ; 2 types d'obligation | 12 invariants portant sur les types, la sûreté d'acceptation/application, la fraîcheur, les liaisons de preuve/résultat/approbation, l'absence d'application implicite et la discipline de blocage ; propriété temporelle `TerminalDiscipline`. |


### Dernières exécutions TLC réussies observées (historiques, pas sur le SHA audité)

Les huit couples de modèles configurés possèdent chacun au moins une exécution TLC historique réussie dans l'historique des workflows de la branche main. Les journaux indiquent TLC 2.19 (révision `5a47802`), Java 17.0.21+9, « Model checking completed. No error has been found » et zéro état restant dans la file. Les nombres d'états ci-dessous sont **générés / distincts** :

| Modèle | Date et commit source du run | États générés / distincts | Exécution existante |
|---|---|---:|---|
| `CICheckRouting` | 2026-11-08, `0f3e402d` | 65 536 / 32 768 | [TLC routage](https://github.com/Martin-PB/govcheck/actions/runs/42486714556) |
| `GovCheckAssurance` | 2026-11-08, `0f3e402d` | 11 069 137 / 347 424 | [TLC assurance](https://github.com/Martin-PB/govcheck/actions/runs/42486714637) |
| `GovCheckLifecycle` | 2026-11-08, `0f3e402d` | 132 412 944 / 24 922 992 | [TLC cycle de vie](https://github.com/Martin-PB/govcheck/actions/runs/42486714619) |
| `GovCheckAuthority` | 2026-11-10, `934000a7` | 13 / 13 | [TLC autorité](https://github.com/Martin-PB/govcheck/actions/runs/42816437925) |
| `GovCheckGovernanceApplicability` | 2026-11-13, `6c70d4f1` | 20 785 / 18 067 | [Workflow TLC applicabilité](https://github.com/Martin-PB/govcheck/actions/runs/43435417792) |
| `GovCheckCanonicalPublication` | 2026-11-13, `6c70d4f1` | 178 549 / 38 434 | [Workflow TLC publication](https://github.com/Martin-PB/govcheck/actions/runs/43435417792) |
| `GovCheckGovernanceControls` | 2026-11-13, `6c70d4f1` | 2 826 117 / 1 026 484 | [Workflow TLC contrôles](https://github.com/Martin-PB/govcheck/actions/runs/43435417792) |
| `GovCheckJournalRecovery` | 2026-11-13, `6c70d4f1` | 84 307 / 56 895 | [Workflow TLC reprise du journal](https://github.com/Martin-PB/govcheck/actions/runs/43435417792) |

Il s'agit d'éléments historiques de model checking significatifs, plus solides que la simple présence de fichiers de configuration. Ils restent toutefois attachés à trois révisions antérieures des sources, pas à `f27697d` ; ils ne démontrent pas que les modèles/configurations exacts du main courant ont été vérifiés, ni le raffinement vers l'implémentation ou une assurance globale.


### Derniers builds Lean et CSLib observés (historiques)

- **Cohérence Lean :** succès le 2026-11-13 au commit `2ae091f5` ([run](https://github.com/Martin-PB/govcheck/actions/runs/43442307871)). Le journal installe Lean 4.19.0, indique le succès de `lake build` et audite 36 déclarations sous `GovCheckCoherence.Proofs` avec la liste d'autorisation configurée `propext, Classical.choice, Quot.sound`. Cela constitue une preuve pour cette révision des sources et cette racine/liste d'audit, pas une affirmation d'absence d'axiomes dans tout le dépôt.
- **Compatibilité CSLib :** succès le 2026-11-12 au commit `056203bf` ([run](https://github.com/Martin-PB/govcheck/actions/runs/43243377685)). Le paquet isolé `CslibCompat` a été construit avec Lean 4.36.0-rc2, CSLib `70e25828` et Mathlib `887bb849` (1779 tâches de build). Cela établit la compatibilité API/build de cette sonde, pas une preuve de raffinement sémantique entre GovCheck et CSLib.
- **Extension Lean de la PR #133 :** le run sur la tête de la PR du 2026-11-14 a également réussi ([run](https://github.com/Martin-PB/govcheck/actions/runs/43587576783)) ; sa sortie d'audit mentionne `propext` pour certaines déclarations de faits source SACM, dans la liste d'autorisation configurée. Il ne s'agit pas d'un build du `main` courant.

Aucun contrôle Lean ou CSLib n'est attaché au commit exact audité `f27697d`. Ces runs historiques ne doivent pas être confondus avec une reproduction sur cette cible.

L'inspection des hypothèses de fairness apporte une nuance importante : seul `GovCheckJournalRecovery` ajoute explicitement `WF_vars(Recover)` ; les sept autres définitions de `Spec` utilisent `Init /\ [][Next]_vars` sans hypothèse explicite `WF_` ou `SF_`. Les propriétés temporelles configurées ne doivent donc pas être reformulées comme des garanties générales de progrès pour des actions auxquelles aucune hypothèse de fairness ne s'applique.

**Constat sur le filtre de chemins du workflow :** `.github/workflows/ci-routing-model.yml` inclut `.github/workflows/tla-model-reusable.yml` dans `pull_request.paths`, mais l'omet de `push.paths`. Un push direct sur `main` qui modifie le runner TLC partagé ne déclenche donc pas le modèle `CICheckRouting`, alors que les autres workflows d'entrée des modèles incluent le workflow réutilisable dans leurs deux filtres. Il s'agit d'une lacune ciblée de couverture, pas d'un indice d'erreur du modèle lui-même. Une correction d'une ligne est préparée sur [`work/fix-ci-routing-reusable-push-trigger`](https://github.com/Martin-PB/govcheck/tree/work/fix-ci-routing-reusable-push-trigger) ; elle n'a été ni exécutée ni fusionnée.

Cet inventaire établit l'existence des configurations et des contrôles nommés ; il **n'établit pas** que SANY/TLC a réussi sur le SHA audité, que les bornes sont suffisantes, ni que les modèles se raffinent entre eux ou vers l'implémentation Python. Le jeu de contrôles attaché au main exact ne contient aucun résultat TLC ; les huit modèles restent à reproduire dans #130.

## 6. Corrections préparées pour les deux constats sur les vérificateurs

### 6.1 Échec du contrôle de références de la PR #133

Une branche distincte, [`work/fix-reference-integrity-repo-wide-markdown`](https://github.com/Martin-PB/govcheck/tree/work/fix-reference-integrity-repo-wide-markdown), a été créée depuis la tête de la PR #133. Elle contient :

- une identité de document relative à la racine du dépôt, afin que les backlinks vers `formal/lean/README.md` ne déclenchent plus `ValueError` ;
- la découverte des fichiers Markdown rédigés dans le dépôt, en excluant le miroir du paquet installé `govcheck/` et les répertoires générés/cache, afin que les sources externes à `docs/` participent au contrôle réciproque des citations ;
- cinq tests de régression, dont un scénario de dépôt temporaire de bout en bout vérifiant un backlink vers un document formel externe à travers le validateur du catalogue.

Cette correction est **préparée mais non exécutée**. Elle n'a pas été fusionnée dans la PR #133 et aucun workflow Actions n'a été déclenché. La branche part de l'ancienne tête de la PR #133, pas du `main` courant ; l'intégration doit d'abord tenir compte de la divergence de la PR par rapport à sa base actuelle. Aucun statut vert n'est revendiqué.


### 6.2 Reconnaissance des références par l'évaluateur de main

Une seconde branche, [`work/fix-govcheck-sources-present-rule`](https://github.com/Martin-PB/govcheck/tree/work/fix-govcheck-sources-present-rule), part du `main` courant et corrige les six constats de section de sources de l'évaluateur report-only :

- accepter les titres Markdown numérotés, par exemple `## 17. References`, comme sections de références ;
- ajouter des sections explicites de références au catalogue dans les décisions 0008 et 0009 EN/FR, en réutilisant leurs sources R-05/R-22/R-194–R-196 et R-114–R-122 déjà présentes ;
- conserver la liste complète des liens au catalogue du dossier de métamodèle à l'intérieur de sa section Références numérotée en transformant le titre suivant en sous-titre ;
- ajouter un test de régression pour un titre de références numéroté.

L'expression régulière exacte a fait l'objet d'une vérification locale isolée sur cinq formes de titres (anglais/français, numérotés ou non) ; il ne s'agit **pas** de l'exécution de la suite de tests du dépôt. La branche n'a pas été exécutée comme candidat complet, n'a pas été fusionnée et n'a déclenché aucun workflow Actions.

## 7. Reproductions restantes

Le livrable demandé par #130 n'est pas terminé. Il reste à :

- obtenir un checkout local de la cible exacte de l'audit et consigner les versions réelles de Git, Python, Java, TLC et Lean ;
- exécuter la suite Python complète sur le `main` courant, au lieu de s'appuyer uniquement sur le run historique de la PR #133 ;
- exécuter SANY/TLC sur les huit couples modèle/configuration, en enregistrant checksum de l'outil, version Java, états, bornes, invariants et propriétés temporelles ;
- construire et auditer le paquet Lean 4.19.0 épinglé sur les sources formelles exactes de la cible ; examiner le rapport d'axiomes complet, pas seulement la racine configurée ;
- construire et examiner séparément `formal/cslib-compat` avec sa toolchain Lean 4.36.0-rc2 ;
- ajouter des tests exécutables de non-régression sur la révision/authentification des attestations et la non-vacuité des mappings partiels, une fois le contrat visé arbitré ;
- ne classifier les constats restants de la critique qu'après ces reproductions.

**État d'exécution de ce rapport :** inspection des sources et lecture de résultats GitHub existants, plus une seule vérification isolée d'expression régulière Python. L'environnement local disponible fournit Python 3.13.5 et OpenJDK 21.0.12.1 ; aucun exécutable `lean`, `lake` ou `tlc` n'est installé, et la résolution DNS de `github.com` est indisponible, ce qui empêche d'obtenir un clone complet et les dépendances épinglées. Aucun test unitaire du dépôt, run TLC, build Lean, audit d'axiomes ou nouveau run Actions n'a été effectué. Aucun crédit Actions n'a été consommé.

## 8. Disposition

La critique n'est ni acceptée en bloc ni rejetée en bloc. Les sources actuelles étayent plusieurs lacunes importantes d'implémentation et d'enforcement ; d'autres affirmations nécessitent une qualification. La spécification du journal améliore la définition du protocole logique, mais ne l'implémente pas. Les travaux SACM/Lean apportent des tranches formalisées utiles, mais ne ferment pas les obligations de cohérence globale du métamodèle, de raffinement du parseur ou de conformité du runtime.

Cet audit n'a modifié aucune spécification normative, décision d'architecture, modèle formel ni politique d'acceptation.
