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

## Références bibliographiques

L'étude d'intégration et ses sources techniques externes sont cataloguées séparément afin de ne pas confondre étude, implémentation et décision d'adoption :

- [R-18 — Évaluation de Writ à partir des sources](../references.fr.md#r-18)
- [R-19 — Évaluation de Privateer à partir des sources](../references.fr.md#r-19)
- [R-37 — Fondements des CRDT](../references.fr.md#r-37)
- [R-38 — Yjs et Yrs](../references.fr.md#r-38)
- [R-39 — Automerge](../references.fr.md#r-39)
- [R-40 — CRDT Loro](../references.fr.md#r-40)
- [R-41 — Transports WebRTC](../references.fr.md#r-41)
- [R-42 — ICE, STUN et TURN](../references.fr.md#r-42)
- [R-43 — Open Knowledge Format (OKF) v0.2](../references.fr.md#r-43)
- [R-44 — RDF 1.1](../references.fr.md#r-44)
- [R-45 — SKOS](../references.fr.md#r-45)
- [R-46 — OWL 2](../references.fr.md#r-46)
- [R-47 — SHACL](../references.fr.md#r-47)
- [R-48 — Termes de métadonnées Dublin Core](../references.fr.md#r-48)
- [R-49 — Ontologie bibliographique BIBO](../references.fr.md#r-49)
- [R-50 — DCAT 3](../references.fr.md#r-50)
- [R-51 — W3C Web Annotation](../references.fr.md#r-51)
- [R-52 — ActivityStreams 2.0](../references.fr.md#r-52)
- [R-53 — Ontologie P-Plan](../references.fr.md#r-53)
- [R-54 — Dépôts et PR #27/#28 Cartocortex, MoriNet et SaussuNet](../references.fr.md#r-54)
- [R-55 — Formats d'échange de cartes mentales et de graphes](../references.fr.md#r-55)
- [R-56 — API de stockage cloud et interopérabilité S3](../references.fr.md#r-56)
- [R-57 — Accès aux fichiers du navigateur, persistance locale et WebAssembly](../references.fr.md#r-57)
- [R-58 — Découverte de pairs Hyperswarm et HyperDHT](../references.fr.md#r-58)
