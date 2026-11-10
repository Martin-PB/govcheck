# Modèles formels

Les travaux formels de GovCheck sont développés progressivement et restent distincts de toute affirmation relative à l’implémentation. Ils s'appuient sur [R-05 — TLA+ et TLC](../references.fr.md#r-05) et [R-22 — Sémantiques natives de Git et Pijul](../references.fr.md#r-22).

## Cycle de vie

- [Modèle du cycle de vie — français](lifecycle-model.fr.md)
- [Lifecycle model — anglais](lifecycle-model.md)
- [Diagramme généré du cycle de vie](lifecycle-diagram.mmd)
- [Registre des transitions](../../formal/lifecycle-transitions.json)
- [Générateur et contrôle de dérive](../../scripts/render-lifecycle-diagram.py)
- [Module TLA+](../../formal/tla/GovCheckLifecycle.tla)
- [Configuration TLC](../../formal/tla/GovCheckLifecycle.cfg)
- [Catalogue des artefacts stables](../../formal/artifacts.json)
- [Schéma du manifeste de preuves de release](../../formal/schemas/release-manifest.schema.json)

Le modèle de cycle de vie est un artefact source dont l'identifiant logique stable est `govcheck.lifecycle`. Ses révisions sont suivies dans Git. Un tag de release fige l'arbre source et le commit exacts ; il n'impose pas de créer des copies des fichiers sources portant le nom de chaque release. Les rapports de vérification générés et leur manifeste sont joints à la release GitHub correspondante.

Le diagramme est généré depuis `formal/lifecycle-transitions.json`. Le registre contient des libellés explicatifs et relie chaque transition affichée à un opérateur TLA+ de premier niveau. Exécuter `python3 scripts/render-lifecycle-diagram.py` pour le régénérer, ou ajouter `--check` pour détecter une dérive. Le contrôle vérifie la couverture des noms d'opérateurs et la fraîcheur du fichier généré ; il **n'analyse pas la sémantique TLA+** et ne prouve pas que les gardes/effets explicatifs décrivent fidèlement les opérateurs. Toute modification d'une transition doit donc faire l'objet d'une revue conjointe du modèle et du registre.

Le premier modèle couvre un changement abstrait, l’évaluation liée à un tuple, la publication de preuves, les approbations autorisées, l’acceptation, l’application du candidat exact, la mutation des entrées et les décisions terminales.

**Statut de vérification :** spécification et configuration TLC ajoutées ; aucune exécution TLC ni aucun résultat de preuve ne sont revendiqués. Consulter le document du modèle pour les limites de l’abstraction et les raffinements nécessaires.


## Autorité de gouvernance

- [Décision d'amorçage de l'autorité — français](../architecture/0023-bootstrap-governance-authority.fr.md)
- [Bootstrap authority decision — anglais](../architecture/0023-bootstrap-governance-authority.md)
- [Modèle TLA+ de transition d'autorité](../../formal/tla/GovCheckAuthority.tla)
- [Configuration TLC](../../formal/tla/GovCheckAuthority.cfg)

Le modèle est une abstraction à transitions bornées du régime initial à racine unique. Il vérifie l'attribution historique des amendements à l'autorité immédiatement précédente, la continuité de la chaîne autorité/révision, la cohérence de l'état courant avec le dernier enregistrement et la propriété temporelle append-only (l'historique antérieur reste un préfixe exact après chaque transition). Il n'encode pas de positions d'entrée en vigueur : il ne vérifie donc ni l'effet prospectif ni la préservation de la validité des décisions antérieures. Il abstrait l'identité des principaux et ne modélise pas les délégations, l'identité cryptographique, la validité en temps réel, le cycle de vie des dérogations ni l'intégration au validateur de gouvernance des versions. Le fixture TLC fini ne prouve pas l'application en production.

## Applicabilité des révisions de gouvernance

- [Premier enregistrement d'exécution TLC — Architecture 0031](../architecture/0031-first-tlc-governance-applicability.fr.md) · [English](../architecture/0031-first-tlc-governance-applicability.md)

- [Spécification 0006 — Applicabilité des révisions de gouvernance](../specifications/0006-governance-revision-applicability.fr.md) · [English](../specifications/0006-governance-revision-applicability.md)
- [Module TLA+](../../formal/tla/GovCheckGovernanceApplicability.tla)
- [Configuration TLC](../../formal/tla/GovCheckGovernanceApplicability.cfg)

Ce modèle borné distinct lie chaque évaluation à la révision de gouvernance effective à sa position d'événement, exige l'autorisation de l'autorité enregistrée à cette position et ne permet la publication qu'à une position ultérieure. Il préserve les liens des décisions historiques et rejette les évaluations périmées lors de l'autorisation. Il ne modélise pas encore les changements/délégations d'autorité, le consensus distribué, l'identité cryptographique, toute la concurrence multi-écrivain ou le raffinement de l'implémentation. Son exécution TLC constitue une preuve relative à cette abstraction finie uniquement.

## Publication canonique de la gouvernance

- [Compte rendu d'arbitrage sur l'applicabilité — français](../decisions/0008-governance-applicability-arbitration-session.fr.md) · [English](../decisions/0008-governance-applicability-arbitration-session.md)
- [Module TLA+ de publication canonique](../../formal/tla/GovCheckCanonicalPublication.tla)
- [Configuration TLC](../../formal/tla/GovCheckCanonicalPublication.cfg)
- [Résultat TLC consigné — Architecture 0032](../architecture/0032-canonical-publication-model-checking.fr.md)
- [Entrée du catalogue stable des artefacts](../../formal/artifacts.json) — `govcheck.canonical-publication`

Ce modèle de conception borné sépare l'évaluation du candidat, l'autorisation et la publication. L'autorisation est liée à la révision et à la position de tête évaluées ; la publication n'ajoute au journal que si cette base est toujours courante. Il exprime l'unicité des identités de révision, la continuité des prédécesseurs, une publication par prédécesseur canonique, la liaison autorisation/évaluation, l'autorisation préalable à la publication et l'exclusion des bases périmées. La configuration TLC demande également la propriété temporelle append-only. **Statut de vérification corrigé :** le modèle et la configuration exacts ont réussi TLC ; consulter l'Architecture 0032 pour la révision vérifiée et le résultat fini. Les lacunes d'implémentation restantes ne sont pas couvertes par ce modèle.


## Contrôles des évaluateurs, exceptions et révocation

- [Module TLA+](../../formal/tla/GovCheckGovernanceControls.tla)
- [Configuration TLC](../../formal/tla/GovCheckGovernanceControls.cfg)
- [Architecture 0033 — résultat TLC](../architecture/0033-governance-evaluator-exception-revocation-model.fr.md)
- [Catalogue stable des artefacts](../../formal/artifacts.json) — `govcheck.governance-controls`

Ce modèle borné conserve l'évaluateur reconnu par la gouvernance antérieure comme seul évaluateur faisant autorité ; le remplaçant proposé ne produit que des résultats comparatifs. Il distingue `Pass`, `Fail`, `Unknown` et `Conflict`, bloque les deux derniers, borne et revalide les exceptions dérogeables, exclut les exigences non dérogeables, enregistre la révocation prospective et préserve les décisions historiques avec requalification séparée. SANY 2.1 et TLC 2.19 ont réussi sur la tête de PR vérifiée `86713a99574c085ee5a41a71e70f93ab7ce4a831` (checkout CI `1f387b8f6019db545ccd50d55fd9c7cc0d704d80`) : 2 826 117 états générés, 1 026 484 distincts, zéro restant, profondeur 12 ; les neuf invariants et `AppendOnly` ont réussi. Ce résultat ne couvre pas le stockage durable, la reprise après panne, les adaptateurs VCS, le consensus distribué ni le raffinement de l'implémentation.

## Périmètres de vérification CI

La partition des vérifications du dépôt et son modèle formel de routage sont décrits dans [l'Architecture 0029](../architecture/0029-concern-scoped-ci-and-formal-verification-boundaries.fr.md) ([English](../architecture/0029-concern-scoped-ci-and-formal-verification-boundaries.md)). Le modèle de routage CI est `formal/tla/CICheckRouting.tla` ; il n'est vérifié que lorsque ses propres entrées de politique changent. Les modifications documentaires ordinaires ne déclenchent ni ce modèle ni les modèles TLC produit, sauf si elles sont explicitement déclarées comme entrées sémantiques d'un modèle.

## Registre de références

Pour les fondements académiques et industriels, notamment les limites du model checking et la distinction entre provenance, preuve et autorité normative, voir le [registre GovCheck des références sur la gouvernance et l'assurance](../references.fr.md) et sa [version anglaise](../references.md).


## Durabilité et reprise du journal canonique

- [Architecture 0034 — modèle et limites](../architecture/0034-canonical-journal-recovery-model.fr.md) · [English](../architecture/0034-canonical-journal-recovery-model.md)
- [Module TLA+](../../formal/tla/GovCheckJournalRecovery.tla)
- [Configuration TLC](../../formal/tla/GovCheckJournalRecovery.cfg)
- [Catalogue stable des artefacts](../../formal/artifacts.json) — `govcheck.journal-recovery`

Le modèle distingue l'état volatil en attente du journal durable append-only. L'ajout durable constitue le point de commit ; la reprise rejoue jusqu'à la tête durable. Un rollback ajoute un nouvel événement et une nouvelle révision dont le contenu est restauré depuis une position antérieure. Les observations de répliques Git/Pijul sont des positions passives de provenance/réplication et ne peuvent établir l'ordre normatif. Le modèle est borné et ne spécifie pas un moteur de stockage ni ne prouve la sûreté après panne d'une implémentation. La vérification TLC est en attente de la fin du workflow enregistré.
