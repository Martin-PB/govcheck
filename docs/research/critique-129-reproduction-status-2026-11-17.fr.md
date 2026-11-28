# État de reproduction de la critique externe #129 — 2026-11-17

**Cible d'audit initiale :** `f27697dac4ceaa6245b6cd796646d7040b12c9b5` (arbre `3604f0e10765afebef6ea7308f94b488247ba8a8`)  
**Cible d'actualisation du main :** `3228404631bb565fddd6d0fb5a52f75724fe24dd`  
**Arbre du main actualisé :** `92920bfbcf6180c12729fc15e937672a92c7bb09`  
**Chantier parent :** [Issue #130](https://github.com/Martin-PB/govcheck/issues/130)  
**Critique source :** [Issue #129](https://github.com/Martin-PB/govcheck/issues/129)

## 1. Périmètre et catégories de preuve

Ce rapport distingue :

1. l'inspection directe des sources de l'arbre exact de `main` indiqué ci-dessus ;
2. les éléments historiques de GitHub Actions issus de la tête de la PR #133, commit `15372f5ca90f5b454a2ff30fa0c0b0fdddab1639` (qui n'est pas la cible de l'audit) ;
3. une reproduction indépendante hébergée par GitHub Actions sur le `main` actualisé après la fusion des PR #134 et #135 (commit courant de `main` : `8e86027297e2d4259403a48842787851e10c9b08`), exécutée sur le checkout de fusion de la PR #138 `fbbff897bd20d7cecadb9801f1da78d50dda541a` (tête de PR `1535cc078be3d97592ab94bd48db0688e93d607c`). Ce checkout ajoute le workflow d'audit et sa déclaration meta-only dans le contrôle d'alignement des paquets ; il ne modifie pas les modèles formels ni l'implémentation runtime évalués ;
4. la reproduction locale, qui **n'a pas été effectuée**, car cet environnement ne dispose ni d'un checkout ni des toolchains et ne résout pas le DNS de GitHub.

Les contrôles historiques de PR ci-dessous restent uniquement des éléments historiques. La reproduction hébergée sur le main actualisé est documentée en section 9 et est liée à son commit exact de fusion. Ce n'est pas une reproduction locale et elle n'établit pas de raffinement entre les modèles TLA+, le vérificateur Python ou un runtime de production.

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

**Constat sur le filtre de chemins du workflow — résolu sur le main courant :** `.github/workflows/ci-routing-model.yml` inclut désormais `.github/workflows/tla-model-reusable.yml` dans les filtres `push.paths` et `pull_request.paths`. Un changement du runner TLC partagé déclenche donc aussi le contrôle `CICheckRouting` lors d'un push direct. Le modèle a réussi dans la reproduction actuelle (section 9).

Cet inventaire établit l'existence des configurations et des contrôles nommés ; il **n'établit pas** que les bornes sont suffisantes, ni que les modèles se raffinent entre eux ou vers l'implémentation Python. Les huit modèles ont depuis été reproduits sur le checkout de fusion fondé sur le main actualisé, documenté en section 9 ; les limites liées aux bornes finies et à l'absence de raffinement intermodèles/runtime demeurent.

## 6. Corrections préparées pour les deux constats sur les vérificateurs

### 6.1 Échec du contrôle de références de la PR #133 — corrigé et fusionné

La PR [#134](https://github.com/Martin-PB/govcheck/pull/134) a été fusionnée le 2026-11-17 dans le commit `f435128d1a8bab5684b6c55d025e52050437366d`. Elle donne aux documents Markdown rédigés une identité relative à la racine du dépôt, parcourt les Markdown rédigés en excluant les miroirs/cache, applique la règle de correspondance EN/FR avec solution de repli, et ajoute des tests de régression. Le workflow d'intégrité des références et la suite Python complète ont réussi après correction d'une assertion erronée dans un test négatif. Le correctif fait désormais partie du `main` courant.

### 6.2 Reconnaissance des références par l'évaluateur de main — corrigée et fusionnée

La PR [#135](https://github.com/Martin-PB/govcheck/pull/135) a été fusionnée le 2026-11-17 dans le commit actuel de `main` `8e86027297e2d4259403a48842787851e10c9b08`. Elle reconnaît les titres Références numérotés, ajoute des sections avec liens au catalogue dans les décisions 0008/0009 EN/FR, conserve les liens du dossier de métamodèle dans sa section numérotée et ajoute un test de régression. Les workflows d'intégrité des références, d'alignement des paquets et de la tranche GovCheck ont réussi. Les six faux négatifs antérieurs ont disparu. Le résultat global de l'évaluateur sur le checkout d'audit fondé sur le main actualisé est `UNKNOWN`, et non `PASS`, faute d'attestation de revue indépendante ; il s'agit d'une condition distincte et encore non résolue. Le workflow reste report-only.

## 7. Travaux restants et limites ouvertes

La reproduction hébergée indépendante est désormais achevée pour le snapshot des sources du main courant (section 9). Travaux restants :

- **Attestation (6.4) :** concevoir et tester une liaison non circulaire à la révision du candidat et une identité de reviewer authentifiée. Aucune architecture de stockage, signature ou revue native de forge n'est choisie.
- **Mappings partiels (6.6) :** la PR [#137](https://github.com/Martin-PB/govcheck/pull/137) ajoute un contre-exemple vérifié par le noyau Lean montrant que le constructeur actuel accepte un domaine vide, et renforce le mapping vers une preuve de théorème en exigeant un `KernelCheckedDerivation` habité. Son build Lean et son audit d'axiomes réussissent (37 déclarations sous la liste configurée ; le rapport explicite inclut le contre-exemple sans dépendance à des axiomes). La PR n'est pas encore fusionnée. L'éventuelle interdiction des mappings partiels vides reste une décision de contrat.
- **Raffinement intermodèles :** les huit modèles TLA+ restent des spécifications bornées distinctes ; aucune preuve de raffinement intégrée ne relie cycle de vie, autorité, assurance, applicabilité de la gouvernance, reprise du journal et implémentation Python.
- **Reproduction locale :** la reproduction Actions hébergée est achevée, mais une seconde exécution locale n'a pas été réalisée dans cet environnement.
- **Maintenabilité des workflows :** la PR [#138](https://github.com/Martin-PB/govcheck/pull/138) ajoute le workflow d'audit réutilisable de bout en bout ; tous les contrôles sont verts et elle reste ouverte pour revue/fusion.

Aucun de ces constats ne doit être transformé en politique normative sans décision explicite de l'autorité GovCheck compétente.

## 8. Disposition

La critique n'est ni acceptée en bloc ni rejetée. Les sources actuelles étayent plusieurs lacunes importantes d'implémentation et d'enforcement ; d'autres affirmations nécessitent une qualification. La spécification du journal améliore la définition du protocole logique, mais ne l'implémente pas. Les travaux SACM/Lean apportent des tranches formalisées utiles, mais ne ferment pas les obligations de cohérence globale du métamodèle, de raffinement du parseur ou de conformité du runtime.

La reproduction hébergée confirme que les huit configurations TLA+ actuelles se terminent sans contre-exemple TLC sur le checkout de fusion fondé sur le main actualisé, et que les paquets Lean et CSLib se construisent avec leurs toolchains épinglées distinctes. Ces résultats ne prouvent ni l'adéquation des bornes finies, ni la correction des abstractions, ni le raffinement intermodèles, ni la conformité de l'implémentation.

Cet audit n'a modifié aucune spécification normative, décision d'architecture, modèle formel ni politique d'acceptation.

## 9. Reproduction indépendante hébergée sur le main actualisé — 2026-11-17

### Identité exacte des sources et du runner

- `main` avant la PR d'audit : `8e86027297e2d4259403a48842787851e10c9b08` (après fusion des PR #134 et #135).
- Tête de la PR #138 : `1535cc078be3d97592ab94bd48db0688e93d607c`.
- Checkout exact de fusion : `fbbff897bd20d7cecadb9801f1da78d50dda541a`.
- Audit complet : [run 44110921001](https://github.com/Martin-PB/govcheck/actions/runs/44110921001) — **success**.
- Contrôle GovCheck report-only : [run 44110920731](https://github.com/Martin-PB/govcheck/actions/runs/44110920731) — **success**.
- Alignement des paquets : [run 44110920743](https://github.com/Martin-PB/govcheck/actions/runs/44110920743) — **success**.

La PR d'audit ajoute uniquement l'orchestration et une déclaration de workflow meta-only ; elle ne modifie pas les modèles formels ni le code runtime évalués.

### Python et contrôles du dépôt

| Contrôle | Résultat |
|---|---|
| Environnement | CPython 3.12.16 ; Git 2.56.1 |
| Suite Python complète | **91 réussis** |
| Intégrité des références sur tout le dépôt | **PASS — 0 avertissement** |
| Alignement des paquets | **PASS** |
| Tests de la tranche GovCheck | **91 réussis** |
| Évaluateur GovCheck | **overall UNKNOWN** : règles applicables PASS sauf `independent-review`, UNKNOWN faute d'attestation de revue indépendante |

Le résultat `UNKNOWN` de l'évaluateur n'est pas un échec des tests unitaires. Son comportement fail-closed est conservé, mais le workflow reste report-only et ne constitue pas une barrière d'acceptation. Les six faux négatifs antérieurs liés aux sections de sources ont disparu après la PR #135.

### Les huit couples modèle/configuration TLA+

Les huit analyses SANY et exécutions TLC se sont terminées avec succès. Chacune indique « Model checking completed. No error has been found » et zéro état restant dans la file. Identité des outils : TLA+ tools 1.7.4, SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88` ; TLC 2.19 (révision `5a47802`) ; Java Temurin 17.0.21+9. Les nombres sont **générés / distincts** :

| Modèle | États générés / distincts |
|---|---:|
| `CICheckRouting` | 65 536 / 32 768 |
| `GovCheckAssurance` | 11 069 137 / 347 424 |
| `GovCheckAuthority` | 13 / 13 |
| `GovCheckGovernanceApplicability` | 20 785 / 18 067 |
| `GovCheckCanonicalPublication` | 84 307 / 56 895 |
| `GovCheckGovernanceControls` | 2 826 117 / 1 026 484 |
| `GovCheckJournalRecovery` | 178 549 / 38 434 |
| `GovCheckLifecycle` | 132 412 944 / 24 922 992 (4 min 15 s) |

Ces résultats sont bornés aux configurations finies exactes et aux sources du checkout de fusion. Ils ne prouvent ni le comportement non borné, ni l'adéquation des bornes, ni une vivacité générale au-delà des hypothèses explicites de fairness, ni le raffinement vers l'implémentation Python.

### Tranche de cohérence Lean 4.19

- Lean 4.19.0, commit `6caaee842e94` ; `lake build` a réussi.
- Audit d'axiomes configuré : **36 déclarations** sous `GovCheckCoherence.Proofs`, toutes dans la liste `propext, Classical.choice, Quot.sound`.
- `AxiomReport.lean` explicite : 42 déclarations affichées sans dépendance à des axiomes.
- Run : [44110921001](https://github.com/Martin-PB/govcheck/actions/runs/44110921001).

Ce résultat ne concerne que le paquet, la racine de preuve et la liste d'autorisation déclarés ; il ne prouve ni l'absence d'axiomes dans tout le dépôt, ni la conformité de l'implémentation.

### Sonde de compatibilité CSLib isolée

- Lean 4.36.0-rc2, commit `b35cb10cf2ced51a2fd1880cfdbf75c71ab7a35a`.
- CSLib `70e25828d89a3916e41c9d84cfffd7e6093bb1a0` ; Mathlib `887bb849a9f64e1c66499fd5ff8523c864e78941`.
- `lake build CslibCompat` a réussi (**1 779 tâches de build**).
- Avertissement non bloquant : `lakefile.lean:6` utilise `PackageConfig.defaultTargets`, champ non reconnu ; la cible explicite a néanmoins été construite.
- Run : [44110921001](https://github.com/Martin-PB/govcheck/actions/runs/44110921001).

Cela établit la compatibilité build/API de la sonde isolée, pas un raffinement sémantique entre GovCheck et CSLib.

### Correction des nombres d'états historiques et suite

La reproduction indépendante confirme que les nombres historiques du 13 novembre avaient été intervertis entre `GovCheckCanonicalPublication` et `GovCheckJournalRecovery` ; le tableau historique ci-dessus est corrigé.

La PR [#137](https://github.com/Martin-PB/govcheck/pull/137) ajoute un contre-exemple vérifié par le noyau pour les mappings partiels vacants et renforce la proposition du mapping vers une preuve de théorème. Son dernier build Lean 4.19 et son audit d'axiomes ont réussi : [run 44111542642](https://github.com/Martin-PB/govcheck/actions/runs/44111542642). Elle reste ouverte pour revue/fusion et ne modifie pas la sémantique des mappings du main courant.

La PR [#138](https://github.com/Martin-PB/govcheck/pull/138) fournit le workflow d'audit réutilisable ; tous les contrôles sont verts et elle reste ouverte pour revue/fusion.


## 10. Actualisation de l'audit du main courant — cible figée avant exécution

Cette actualisation remplace toute formulation ci-dessus présentant `8e86027297e2d4259403a48842787851e10c9b08` comme révision actuelle de `main`. La cible d'audit est le commit exact `3228404631bb565fddd6d0fb5a52f75724fe24dd`, arbre `92920bfbcf6180c12729fc15e937672a92c7bb09` (fusion de la PR #150). La cible originale de la critique reste `24760fb` ; la reproduction hébergée précédente demeure une preuve historique liée à sa propre révision source.

Le workflow d'audit a été étendu avant exécution pour inclure le neuvième couple TLA+ présent, `GovCheckGovernanceContextBinding`, ainsi que les rapports d'axiomes explicites des tranches de composition des mappings de preuves, de composition des ponts et de sémantique typée du risque, en plus de l'audit de la racine de preuves existante. Cela évite d'omettre silencieusement les artefacts formels ajoutés après l'audit antérieur des huit modèles.

**État de l'exécution :** terminé ; voir la section 11. Le marqueur « en attente » ci-dessus restitue la chronologie de préparation du rapport, pas l'état actuel.


## 11. Reproduction finale sur le main actualisé — 2026-11-17

### Identité exacte

- Parent `main` figé : `3228404631bb565fddd6d0fb5a52f75724fe24dd` ; arbre : `92920bfbcf6180c12729fc15e937672a92c7bb09`.
- Tête de la PR #151 : `422254e3b692e705f1f0788eb22edf52a56b480a` ; checkout exact de fusion audité : `b3e98bba92e626f8ee88fefd06b30e2a2b7c182d`.
- Audit complet : [run 44137752200](https://github.com/Martin-PB/govcheck/actions/runs/44137752200) — **success**. Intégrité des références : [44137752107](https://github.com/Martin-PB/govcheck/actions/runs/44137752107) — **success**. Alignement des paquets : [44137752039](https://github.com/Martin-PB/govcheck/actions/runs/44137752039) — **success**.
- La PR #151 ne modifie que le workflow d'audit et les deux rapports ; aucune implémentation, aucun modèle, aucune proposition Lean ni spécification normative évalués n'ont été modifiés.

### Python et évaluateur exécutable

- CPython 3.12.16 ; Git 2.56.1 ; **97 tests Python réussis**.
- Références sur tout le dépôt : **162 entrées au catalogue, 161 citées, 158 fichiers Markdown, PASS avec 0 avertissement**.
- Évaluateur GovCheck `0.4.0-slice`, sur le candidat `b3e98bba92e626f8ee88fefd06b30e2a2b7c182d` par rapport à `origin/main` : **overall UNKNOWN, code de sortie 1**. Licence, décisions bilingues, paires de manifeste, intégrité des références et présence des sources en PASS. Intégrité du bootstrap et fraîcheur TLA non applicables à ce diff d'audit. `independent-review` est UNKNOWN : aucune attestation humaine, issue d'une identité distincte de l'auteur et liée à la révision candidate, n'a été trouvée ; le rapport recense 20 décisions et zéro attestation.
- Le workflow d'audit capture et téléverse ce résultat sans traiter le code non nul de l'évaluateur comme un échec des tests. **UNKNOWN n'est pas PASS.** Le workflow ordinaire de contrôle GovCheck reste report-only.

### Neuf couples TLA+

Les neuf analyses SANY et exécutions TLC se sont terminées avec « Model checking completed. No error has been found » et zéro état restant dans la file. Outils : TLA+ tools 1.7.4 (SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`), TLC 2.19 révision `5a47802`, Temurin Java 17.0.21+9. Nombres générés/distincts :

| Modèle | États générés / distincts | Résultat |
|---|---:|---|
| CICheckRouting | 65,536 / 32,768 | PASS |
| GovCheckAssurance | 11,069,137 / 347,424 | PASS |
| GovCheckAuthority | 13 / 13 | PASS |
| GovCheckCanonicalPublication | 84,307 / 56,895 | PASS |
| GovCheckGovernanceApplicability | 20,785 / 18,067 | PASS |
| GovCheckGovernanceContextBinding | 486,289 / 486,289 | PASS |
| GovCheckGovernanceControls | 2,826,117 / 1,026,484 | PASS |
| GovCheckJournalRecovery | 178,549 / 38,434 | PASS |
| GovCheckLifecycle | 132,412,944 / 24,922,992 (5 min 07 s) | PASS |

Le neuvième modèle, `GovCheckGovernanceContextBinding`, est désormais inclus dans la matrice d'audit réutilisable ; il a exploré 486 289 états distincts à la profondeur 8. Ces résultats sont des vérifications de modèles bornées, pas des preuves non bornées, une preuve d'adéquation des bornes ou une preuve de raffinement vers le runtime Python.

### Lean 4.19 et CSLib

- Le build du paquet Lean 4.19.0 a réussi. L'audit d'axiomes configuré a couvert **44 déclarations** sous `GovCheckCoherence.Proofs` ; toutes les dépendances étaient dans la liste `propext, Classical.choice, Quot.sound`.
- Quatre rapports explicites ont été exécutés (principal, composition des mappings de preuves, composition des ponts, sémantique typée du risque) : **124 déclarations**, dont **8 dépendent de `propext`** et 116 ne déclarent aucune dépendance à des axiomes. Aucune déclaration du rapport de sémantique du risque ne dépend d'un axiome. Cela ne signifie pas que tout le dépôt est sans axiomes ni que l'implémentation Python satisfait ces propositions.
- Sonde CSLib isolée : Lean 4.36.0-rc2 (commit `b35cb10cf2ced51a2fd1880cfdbf75c71ab7a35a`), CSLib épinglé sur `70e25828d89a3916e41c9d84cfffd7e6093bb1a0` ; `lake build CslibCompat` a réussi (**1 779 tâches**). Cela établit uniquement la compatibilité build/API de la sonde, pas un raffinement sémantique.

### Qualification finale des constats 6.1–6.7

| Constat | Qualification sur le main actualisé | Suite |
|---|---|---|
| 6.1 Modèle canonique exécutable | **Lacune d'implémentation confirmée.** La Specification 0002 reste proposée ; aucun schéma canonique ni évaluateur n'est implémenté. | Nécessite une décision gouvernée distincte sur le format/l'évaluateur ; cet audit ne choisit rien. |
| 6.2 Journal canonique | **Partiellement confirmé.** La Specification 0007 définit un protocole logique détaillé mais reste proposée et non implémentée. Elle n'impose pas de base de données/service physiquement séparé. | Aucun moteur de stockage, service ou format filaire choisi. |
| 6.3 Autorité / séparation des tâches | **Partiellement confirmé, avec nuance.** L'architecture 0023 adopte explicitement une autorité racine unique et accepte l'auto-autorisation comme risque résiduel ; elle ne prétend pas fournir une autorisation à deux personnes. | L'issue existante [#60](https://github.com/Martin-PB/govcheck/issues/60) suit la visibilité du risque résiduel. |
| 6.4 Attestation de revue indépendante | **Faiblesse structurelle confirmée.** L'attestation est lue dans l'arbre candidat, doit contenir le SHA final du candidat (problème d'auto-référence), et l'identité du reviewer est une chaîne libre non authentifiée. | Issue existante [#44](https://github.com/Martin-PB/govcheck/issues/44). |
| 6.5 Enforcement de l'acceptation CI | **Confirmé.** L'évaluateur retourne UNKNOWN/code 1 ; le workflow ordinaire masque l'échec avec `continue-on-error: true` et `|| true`. GitHub indique que `main` n'est pas protégée, que l'application des checks requis est désactivée et qu'aucun ruleset n'existe. Aucun contrôle effectif de la forge ne conditionne le merge au résultat. | L'issue existante [#45](https://github.com/Martin-PB/govcheck/issues/45) suit la frontière d'acceptation portable ; le doublon #152 ouvert entre-temps a été fermé. Aucune protection de branche n'a été modifiée. |
| 6.6 Mapping sémantique partiel | **Limitation contractuelle confirmée, désormais explicite.** `SemanticBridge.partialMapping` admet toujours un domaine vide. La [PR #137](https://github.com/Martin-PB/govcheck/pull/137), fusionnée, ajoute un contre-exemple de domaine vide vérifié par le noyau. Elle remplace aussi l'ancienne conclusion réflexive `proof = proof` par un `KernelCheckedDerivation` non vide contenant une preuve de la proposition cible exacte. | L'interdiction éventuelle des mappings partiels vides reste un choix contractuel non décidé. |
| 6.7 Séparation physique du journal | **L'affirmation physique de la critique n'est pas étayée.** La Specification 0007 sépare les actes logiques mais autorise une transaction technique atomique unique ; elle n'exige pas d'infrastructure séparée. | Aucune architecture de séparation physique imposée. |

### Limites formelles restantes

1. Les invariants de sûreté et l'exploration bornée ne démontrent pas la vivacité générale ni la disponibilité sans hypothèses de fairness/environnement adaptées. Seul `GovCheckJournalRecovery` ajoute explicitement `WF_vars(Recover)`.
2. Les neuf modèles TLA+ restent des modèles bornés distincts. Le modèle de liaison du contexte ajoute une tranche utile, mais aucun raffinement intégré entre modèles ou vers le runtime Python n'est établi.
3. La faiblesse précise de l'égalité réflexive dans `kind_mapping_rule_theorem_proof_requires_derivation` a été corrigée par la PR #137 fusionnée. Les autres résultats Lean restent des projections/conséquences de constructeurs ; les rapports d'axiomes limités ne prouvent pas la conformité du runtime.
4. `govcheck/check.py` implémente toujours huit règles (licence, décisions bilingues, paires de manifeste, références, présence des sources, intégrité du bootstrap, fraîcheur TLA et attestation de revue indépendante). Il n'implémente pas le cycle de vie canonique, le registre d'autorité, le protocole de journal, la sémantique du risque/des décisions ni les contrats complets d'assurance intermodèles.

### Disposition

Les PR #137 (contre-exemple de mapping et théorème renforcé) et #138 (workflow d'audit réutilisable) sont fusionnées. La PR #150 (sémantique typée du risque) est fusionnée. La PR #151 contient uniquement cette actualisation, l'ajout du neuvième modèle TLC, les rapports Lean explicites et la capture de l'évaluateur ; elle est ouverte pour revue et n'a pas été fusionnée. La reproduction hébergée est terminée ; aucune reproduction locale distincte n'a été effectuée. La critique n'est ni acceptée ni rejetée en bloc : des lacunes d'implémentation/enforcement sont confirmées, certaines affirmations sont nuancées et certaines faiblesses formelles ont depuis été corrigées. Aucune spécification normative, aucun régime d'autorité, aucun paramètre de protection de branche ni aucune politique d'acceptation n'a été modifié.


## 12. Actualisation du main courant — 2026-11-28 (tranche ciblée)

**Cible source :** commit `708c7bc16bf40d2ad4537fa6d7328e824a0b7ccf` de `main`, arbre `65ad756ca1d67412d6a3bbbb27274260ee3344b1`. Il s'agit d'une actualisation des sources et d'une reproduction Lean ciblée, pas de la reproduction complète de #130. Cette section remplace les anciennes formulations présentant le snapshot du 17 novembre comme le main courant.

| Constat | Qualification actuelle | Preuve |
|---|---|---|
| 6.4 auto-référence de l'attestation dans l'arbre | La circularité de l'attestation intégrée est **obsolète dans le main courant** ; la disponibilité d'une revue demeure un écart. | `govcheck/check.py:329–334` retourne UNKNOWN pour les attestations dans l'arbre candidat ; lignes 359–362 exigent que revue, assurance, identité d'auteur et politique de confiance soient hors de l'arbre. Les lignes 366, 401–427 et 440–446 lient les preuves détachées au candidat, à la base, au contenu, à la gouvernance, au périmètre et aux octets exacts de l'enveloppe de revue. Tests : `test_in_tree_attestation_never_satisfies_independent_review` et `test_detached_review_config_can_satisfy_rule_when_verifier_confirms`. Le commit historique `24760fb` n'a pas été rejoué directement dans cette tranche. |
| 6.5 enforcement de l'acceptation CI | **Confirmé sur le main courant.** | `.github/workflows/govcheck-check.yml:1,33–36` est report-only, utilise `continue-on-error: true` et `|| true`. Le ruleset actif `Protection Main` (ID `28251664`, lu le 28-11-2026) exige une PR, approvals=0, bloque suppression/force-push et n'a aucun bypass, mais `required_status_checks=[]`. Main est donc protégée par PR sans statut GovCheck de confiance obligatoire ; l'enforcement effectif reste non établi (#45). Aucun paramètre n'a été modifié. |
| 6.6 mapping partiel à domaine vide | **Confirmé sur le main courant.** | `formal/lean/GovCheckCoherence/Mapping.lean:63–66` exige une preuve uniquement pour les membres d'un prédicat de domaine, sans exiger que le domaine soit habité. Le choix `domain := fun _ : True => False` permet d'habiter `SemanticBridge True False .partialMapping` par vacuité : le mapping ne couvre aucun cas source, ce n'est pas une preuve de False. La PR #211 ajoute une reproduction compilable ; l'issue #210 suit la décision contractuelle sans modifier Mapping.lean. |

Les constats 6.1, 6.2, 6.3 et 6.7 ne sont **pas entièrement rejoués sur cette cible** ; leurs qualifications précédentes restent historiques jusqu'à une nouvelle revue constat par constat. Le journal, les attestations détachées, la provenance typée et la protection du ruleset sont des améliorations, mais ne prouvent pas à elles seules l'adoption du modèle canonique, le consensus d'un journal distribué ou un régime d'autorité à deux personnes.

Les limites formelles restent : TLC borné ne prouve pas la vivacité générale ; les modèles TLA+ séparés ne sont pas un raffinement de bout en bout vers Python ; Lean prouve les propositions encodées (y compris le contre-exemple à domaine vide) ; l'évaluateur ordinaire reste report-only. Toutes les exécutions TLC courantes, l'audit Lean/CSLib complet, le commit historique `24760fb` et les autres éléments 6.1–6.7 sont **non reproduits dans cette tranche** et restent ouverts dans #130. Aucune recommandation de la critique n'est adoptée par ce rapport.

La commande Lean ciblée est exécutée par le workflow épinglé `lean-coherence.yml`, depuis `formal/lean` :

```sh
lake env lean GovCheckCoherence/Reproductions/EmptyDomainPartialMapping.lean
```

Les tests Python peuvent être lancés par `python3 -m unittest discover -s tests -p 'test_govcheck_check.py' -v`. La CI de la PR constitue la reproduction hébergée enregistrée pour le nouveau fixture Lean ; aucune reproduction locale avec checkout/toolchain n'a été effectuée.

**Disposition :** le cycle du constat 6.4 est mitigé par les preuves détachées ; le 6.5 demeure une lacune d'enforcement ; le 6.6 est une limitation formelle confirmée suivie dans #210. L'issue #130 reste ouverte pour la matrice complète.
