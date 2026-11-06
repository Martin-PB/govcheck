# ADR 0002 : Placement des études et évaluations comparatives

- **Statut :** accepté pour le bootstrap ; toute modification exige un ADR de remplacement.
- **Date :** 2026-11-06
- **Périmètre :** où placer les études, évaluations et analyses comparatives d'outils ou méthodes externes dans un dépôt gouverné.

## Contexte

La conception de GovCheck elle-même est issue d'études (évaluation d'intégration de Cartocortex/MoriNet/SaussuNet, évaluation de Writ et Privateer dans le record d'architecture 0016). Un dépôt gouverné doit dire où vont ces études pour qu'elles ne soient ni perdues ni prises pour des règles normatives ou des comportements implémentés.

## Décision

Les études, évaluations et analyses comparatives sont des **records d'architecture** placés dans docs/architecture/ sous forme de records numérotés séquentiellement et bilingues (anglais par défaut, version française), avec un statut explicite (étude / proposition / évaluation) et un périmètre/limites. Elles ne sont jamais présentées comme des contrôles implémentés, des propriétés vérifiées ou des règles normatives. Les rapports de vérification, contre-exemples et preuves générées sont des artefacts de release attachés aux releases, pas des fichiers source portant des noms spécifiques à une release. GovCheck applique cette règle à lui-même : le record 0016 est une évaluation, pas un contrôle.

## Conséquences

- Toute nouvelle étude prend le prochain numéro libre dans docs/architecture/.
- Le README d'architecture les indexe avec leur statut.
- Le contenu normatif reste dans docs/specifications/ et docs/decisions/.

English: [ADR 0002](0002-study-placement.md).
