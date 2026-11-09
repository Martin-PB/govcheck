# Modèles formels

Les travaux formels de GovCheck sont développés progressivement et restent distincts de toute affirmation relative à l’implémentation.

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

- [Spécification 0006 — Applicabilité des révisions de gouvernance](../specifications/0006-governance-revision-applicability.fr.md) · [English](../specifications/0006-governance-revision-applicability.md)
- [Module TLA+](../../formal/tla/GovCheckGovernanceApplicability.tla)
- [Configuration TLC](../../formal/tla/GovCheckGovernanceApplicability.cfg)

Ce modèle borné distinct lie chaque évaluation à la révision de gouvernance effective à sa position d'événement, exige l'autorisation de l'autorité enregistrée à cette position et ne permet la publication qu'à une position ultérieure. Il préserve les liens des décisions historiques et rejette les évaluations périmées lors de l'autorisation. Il ne modélise pas encore les changements/délégations d'autorité, le consensus distribué, l'identité cryptographique, toute la concurrence multi-écrivain ou le raffinement de l'implémentation. Son exécution TLC constitue une preuve relative à cette abstraction finie uniquement.

## Périmètres de vérification CI

La partition des vérifications du dépôt et son modèle formel de routage sont décrits dans [l'Architecture 0029](../architecture/0029-concern-scoped-ci-and-formal-verification-boundaries.fr.md) ([English](../architecture/0029-concern-scoped-ci-and-formal-verification-boundaries.md)). Le modèle de routage CI est `formal/tla/CICheckRouting.tla` ; il n'est vérifié que lorsque ses propres entrées de politique changent. Les modifications documentaires ordinaires ne déclenchent ni ce modèle ni les modèles TLC produit, sauf si elles sont explicitement déclarées comme entrées sémantiques d'un modèle.

## Registre de références

Pour les fondements académiques et industriels, notamment les limites du model checking et la distinction entre provenance, preuve et autorité normative, voir le [registre GovCheck des références sur la gouvernance et l'assurance](../references.fr.md) et sa [version anglaise](../references.md).
