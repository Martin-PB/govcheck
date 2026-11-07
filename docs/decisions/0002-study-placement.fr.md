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

## Artefact source et frontière des preuves

L'artefact source initial de cet enregistrement est **« Évaluer l’intégration des dépôts.pdf »**, daté du 6 novembre 2026 et composé de 224 pages. Il est conservé dans la bibliothèque du projet et n'est pas copié dans ce dépôt. Ses sources externes, dépôts, pull requests, protocoles, vocabulaires et formats sont indexés en [R-35–R-69 et R-77–R-87](../references.fr.md) dans le catalogue central.

Les artefacts Cartocortex examinés ont des statuts de preuve distincts : la PR #9 est un panorama documentaire ; la PR #27 est une étude sur le stockage/projection OKF explicitement marquée comme non exécutée ; la PR #28 est un backlog et une étude de transport explicitement non exécutés. Aucun de ces statuts ne prouve qu'un adaptateur, un CRDT, un transport, une synchronisation cloud ou un importeur de format proposé est implémenté ou accepté. Voir [R-62](../references.fr.md#r-62) et [R-69](../references.fr.md#r-69).

L'estimation approximative de 10 à 20 % des sessions nécessitant un relais TURN, reprise dans l'étude de la PR #28, n'était reliée à aucune source de mesure indépendante vérifiable lors de cet audit. Elle est conservée comme hypothèse de planification non validée, et non comme statistique générale WebRTC ou garantie protocolaire ; des mesures de télémétrie en déploiement seraient nécessaires pour la confirmer.

## Références bibliographiques

L'étude d'intégration et ses sources techniques externes sont cataloguées séparément afin de ne pas confondre étude, implémentation et décision d'adoption :

- [R-18 — Évaluation de Writ à partir des sources](../references.fr.md#r-18)
- [R-19 — Évaluation de Privateer à partir des sources](../references.fr.md#r-19)
- [R-45 — Fondements des CRDT](../references.fr.md#r-45)
- [R-46 — Yjs et Yrs](../references.fr.md#r-46)
- [R-47 — Automerge](../references.fr.md#r-47)
- [R-48 — CRDT Loro](../references.fr.md#r-48)
- [R-49 — Transports WebRTC](../references.fr.md#r-49)
- [R-50 — ICE, STUN et TURN](../references.fr.md#r-50)
- [R-51 — Open Knowledge Format (OKF) v0.2](../references.fr.md#r-51)
- [R-52 — RDF 1.1](../references.fr.md#r-52)
- [R-53 — SKOS](../references.fr.md#r-53)
- [R-54 — OWL 2](../references.fr.md#r-54)
- [R-55 — SHACL](../references.fr.md#r-55)
- [R-56 — Termes de métadonnées Dublin Core](../references.fr.md#r-56)
- [R-57 — Ontologie bibliographique BIBO](../references.fr.md#r-57)
- [R-58 — DCAT 3](../references.fr.md#r-58)
- [R-59 — W3C Web Annotation](../references.fr.md#r-59)
- [R-60 — ActivityStreams 2.0](../references.fr.md#r-60)
- [R-61 — Ontologie P-Plan](../references.fr.md#r-61)
- [R-62 — Dépôts et PR #27/#28 Cartocortex, MoriNet et SaussuNet](../references.fr.md#r-62)
- [R-63 — Formats d'échange de cartes mentales et de graphes](../references.fr.md#r-63)
- [R-64 — API de stockage cloud et interopérabilité S3](../references.fr.md#r-64)
- [R-65 — Accès aux fichiers du navigateur, persistance locale et WebAssembly](../references.fr.md#r-65)
- [R-66 — Découverte de pairs Hyperswarm et HyperDHT](../references.fr.md#r-66)
- [R-67 — WebDAV, Model Context Protocol et conventions de wiki Markdown](../references.fr.md#r-67)
- [R-68 — Dépôts de l'écosystème GovCheck associés et examinés](../references.fr.md#r-68)
- [R-69 — Inventaire des sources sur les formats de cartes mentales et l'interopérabilité](../references.fr.md#r-69)
- [R-77 — Gouvernance des politiques et des outils MCP](../references.fr.md#r-77)
- [R-78 — NIST OSCAL et Continuous Compliance Framework](../references.fr.md#r-78)
- [R-79 — Sandboxing et isolation à l'exécution des agents](../references.fr.md#r-79)
- [R-80 — Protocole Matrix et client Element X](../references.fr.md#r-80)
- [R-81 — Métamoteur SearXNG](../references.fr.md#r-81)
- [R-82 — Conversion de documents Microsoft MarkItDown](../references.fr.md#r-82)
- [R-83 — sérialisation de données liées JSON-LD 1.1](../references.fr.md#r-83)
- [R-84 — syntaxe Turtle de RDF 1.1](../references.fr.md#r-84)
- [R-85 — ontologie SIOC des communautés en ligne](../references.fr.md#r-85)
- [R-86 — vocabulaire Schema.org DigitalDocument](../references.fr.md#r-86)
- [R-87 — transport et découverte pair-à-pair WebTorrent dans le navigateur](../references.fr.md#r-87)
- [R-88 — vérification et test des politiques/modèles de contrôle d'accès NIST SP 800-192](../references.fr.md#r-88)
- [R-89 — méthode B et Atelier B](../references.fr.md#r-89)
- [R-90 — notation de spécification formelle Z](../references.fr.md#r-90)
- [R-91 — Communicating Sequential Processes et FDR](../references.fr.md#r-91)
- [R-92 — modélisation des exigences orientée objectifs iStar 2.0](../references.fr.md#r-92)
- [R-93 — logique déontique et modalités normatives](../references.fr.md#r-93)
