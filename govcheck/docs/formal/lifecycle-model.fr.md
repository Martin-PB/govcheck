# Modèle du cycle de vie GovCheck — TLA+

**Statut :** première spécification bornée ; elle n'a pas encore été vérifiée par model checking. Ce modèle est une première formalisation exécutable candidate du document d'architecture, pas une implémentation ni une preuve du comportement en production.

## Identité et versionnement

Ce modèle possède l'identifiant logique stable `govcheck.lifecycle`. Son fichier source est `formal/tla/GovCheckLifecycle.tla` ; son chemin n'est pas un numéro de release. L'historique Git conserve ses révisions. Un tag de release identifie le commit exact du dépôt contenant la version utilisée pour cette release. Il ne faut pas créer une copie ni renommer ce fichier à chaque publication.

L'explication bilingue conserve elle aussi un chemin stable. La révision exacte utilisée par une release est identifiée par son tag et son commit, et non par un suffixe `v1` dans le nom du fichier.

## Périmètre

Le modèle couvre un changement abstrait et le tuple exact d'identités :

`(baseId, candidateId, governanceId, specId)`.

Il représente les preuves associées à un ensemble fini d'obligations obligatoires, les approbations d'acteurs autorisés, l'acceptation, l'application du candidat exact, la mutation des entrées, les décisions terminales et une séquence d'événements append-only.

Il ne modélise volontairement ni les mécanismes internes de Git, ni la sémantique des patches/canaux Pijul, ni l'authenticité cryptographique, ni les courses du système de fichiers, ni le comportement d'une forge, ni l'implémentation d'un adaptateur.

## État et transitions

Le cycle de vie est également représenté dans le [diagramme d'états généré](lifecycle-diagram.mmd). Son registre de transitions et son générateur sont référencés dans l'[index des modèles formels](README.fr.md). Le diagramme est explicatif, pas normatif : le module TLA+ reste l'autorité sémantique.

- `phase` : phase du cycle de vie.
- `evaluatedTuple` : tuple exact qui a été évalué.
- `evidence` : obligations pour lesquelles un enregistrement de preuve a été publié sur le tuple courant.
- `evidenceOutcomes` : dernier résultat publié pour chaque obligation.
- `outcomes` : résultats liés à la dernière évaluation. `PublishEvidence(obligation, outcome)` peut publier `Pass`, `Fail`, `Unknown`, `Unsupported`, `NotRun` ou `Incomplete`. Une preuve absente produit `Unknown`. Le cycle n'atteint `Reviewable` que si chaque obligation possède une preuve et si chaque résultat vaut `Pass` ; tout autre résultat laisse le cycle dans `Evaluated` et interdit l'acceptation. La publication ou le remplacement d'une preuve efface les approbations antérieures et impose une nouvelle évaluation/revue. Cela modélise la propagation des statuts, pas la véracité ni la suffisance de la preuve.
- `approvals` : ensemble des acteurs autorisés ayant approuvé le tuple courant.
- `acceptedTuple` : tuple exact accepté.
- `appliedCandidateId` : identité du candidat déclaré appliqué.
- `history` : séquence étendue par chaque action modifiant l'état. Sa longueur est bornée par `HistoryLimit` (12 dans la configuration TLC) afin de conserver un espace d'états fini ; une fois cette limite atteinte, les actions modifiant l'état ne sont plus activables. Il s'agit d'une borne d'exploration, pas d'une politique de rétention en production.

Les transitions sont `Prepare`, `PublishEvidence`, `Evaluate`, `Approve`, `Accept`, `Apply`, `ChangeInputs`, `Reject`, `Withdraw` et `Supersede`.

## Invariants d'état configurés pour TLC

| Invariant | Ce qu'il vérifie |
|---|---|
| `TypeOK` | Chaque variable d'état reste dans son domaine déclaré. |
| `AcceptanceSoundness` | Un changement accepté est lié au tuple courant, à une évaluation courante, à des obligations réussies et au nombre requis d'approbations. |
| `ApplicationSoundness` | Applied signifie que le candidat appliqué enregistré est exactement celui du tuple accepté et du tuple courant. |
| `NoStaleEvaluation` | Les états Reviewable, Accepted et Applied ne peuvent pas reposer sur l'évaluation d'un ancien tuple. |
| `EvidenceBinding` | Reviewable exige une preuve et un résultat `Pass` pour chacune des obligations modélisées sur l'évaluation courante. |
| `EvaluationOutcomeBinding` | Evaluated et les phases suivantes utilisent le résultat publié pour chaque obligation prouvée ; une preuve absente reste `Unknown`. |
| `FailedOrUnresolvedEvidenceBlocksAcceptance` | Tout résultat différent de `Pass` interdit les phases Accepted et Applied. |
| `ApprovalBinding` | Les états Accepted et Applied ne contiennent que des approbations provenant de l'ensemble configuré des acteurs autorisés. |
| `NoImplicitApplication` | Avant la phase Applied, aucune identité de candidat appliqué n'est enregistrée. |
| `NoApprovalInPreparedPhase` | La phase Prepared ne conserve aucune approbation antérieure à une nouvelle publication de preuve. |
| `HistoryNonEmpty` | La séquence d'événements contient son événement initial de création. |

La configuration TLC vérifie également la propriété temporelle `TerminalDiscipline` : une fois une phase terminale atteinte (`Applied`, `Rejected`, `Withdrawn` ou `Superseded`), le changement ne peut plus en sortir.

Le module TLA+ énonce également les obligations de théorème correspondantes à partir de `Spec`. La configuration TLC est bornée à deux valeurs par dimension d'identité, deux acteurs, deux obligations et au maximum 12 événements d'historique.

## Limites importantes et raffinements suivants

1. La véracité des preuves, leur provenance, les dépendances de fraîcheur, la révocation et la vérification indépendante restent abstraites. Le modèle accepte une valeur `Pass` publiée en entrée ; il ne vérifie pas cette valeur.
2. Le modèle propage maintenant les résultats explicites `Fail`, `Unknown`, `Unsupported`, `NotRun` et `Incomplete`. Il n'intègre pas encore toute la richesse des statuts et méthodes du modèle de preuve défini dans la spécification 0005.
3. Le modèle ne représente pas encore les opérations concurrentes, l'indisponibilité d'un adaptateur, les courses TOCTOU ou un adaptateur malveillant.
4. La séquence d'événements est étendue par les actions modélisées, mais cette version ne définit pas encore une propriété temporelle distincte d'intégrité de l'historique ni les métadonnées acteur/motif pour chaque événement.
5. `ChangeInputs` est désactivée après les phases terminales, y compris Applied. Une politique de production pour la remédiation/réouverture après application exige une décision séparée.
6. Aucun résultat TLC n'est revendiqué. Avant de considérer ce modèle comme vérifié, l'exécuter avec une version TLC épinglée et consigner la version exacte de l'outil, la configuration, les nombres d'états/transitions explorés, le statut d'achèvement et tout contre-exemple.

## Reproductibilité et preuves de release

Exécuter TLC sur `GovCheckLifecycle.tla` avec `GovCheckLifecycle.cfg`, en utilisant une distribution TLA+ Tools locale et épinglée. Une exécution bornée réussie ne constitue ni une preuve de conformité de l'implémentation, ni une preuve de théorème, ni une démonstration de fidélité normative.

Une release peut joindre un rapport de vérification généré et un manifeste de release. Ce manifeste doit identifier le tag et le commit de release, l'identifiant stable de l'artefact, son chemin exact et son empreinte, la version de TLC et des outils, l'empreinte de la configuration, le statut d'exécution et les nombres d'états/transitions lorsqu'ils sont disponibles. Les rapports générés sont des livrables de release, pas des fichiers source renommés manuellement. Le format du manifeste est défini dans `formal/schemas/release-manifest.schema.json` ; le catalogue des artefacts stables se trouve dans `formal/artifacts.json`.
