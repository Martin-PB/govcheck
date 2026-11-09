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

L'artefact source initial de cet enregistrement est **« Évaluer l’intégration des dépôts.pdf »**, daté du 6 novembre 2026 et composé de 224 pages. Il est conservé dans la bibliothèque du projet et n'est pas copié dans ce dépôt. Ses sources externes, dépôts, pull requests, protocoles, vocabulaires et formats sont préservés dans le catalogue central ; les références directement pertinentes sont liées individuellement ci-dessous.

Les artefacts Cartocortex examinés ont des statuts de preuve distincts : la PR #9 est un panorama documentaire ; la PR #27 est une étude sur le stockage/projection OKF explicitement marquée comme non exécutée ; la PR #28 est un backlog et une étude de transport explicitement non exécutés. Aucun de ces statuts ne prouve qu'un adaptateur, un CRDT, un transport, une synchronisation cloud ou un importeur de format proposé est implémenté ou accepté. Voir [R-62](../references.fr.md#r-62) et [R-69](../references.fr.md#r-69).

L'estimation approximative de 10 à 20 % des sessions nécessitant un relais TURN, reprise dans l'étude de la PR #28, n'était reliée à aucune source de mesure indépendante vérifiable lors de cet audit. Elle est conservée comme hypothèse de planification non validée, et non comme statistique générale WebRTC ou garantie protocolaire ; des mesures de télémétrie en déploiement seraient nécessaires pour la confirmer.

L'étude nomme également B, Z, CSP, iStar et la logique déontique comme formalismes candidats, ainsi que NIST SP 800-192 comme source sur la vérification des modèles/politiques de contrôle d'accès. Ils sont catalogués comme méthodes et alternatives distinctes ; aucun n'est choisi ou adopté par implication.

## Références bibliographiques

L'étude d'intégration et ses sources techniques externes sont cataloguées séparément afin de ne pas confondre étude, implémentation et décision d'adoption :

- [R-03 — Contrôles de branches protégées GitHub](../references.fr.md#r-03)
- [R-05 — Spécification TLA+ et model checking TLC](../references.fr.md#r-05)
- [R-06 — Cadre de provenance in-toto](../references.fr.md#r-06)
- [R-07 — SLSA Build Track](../references.fr.md#r-07)
- [R-08 — OpenSSF Scorecard](../references.fr.md#r-08) · [R-111 — OpenSSF Best Practices Badge](../references.fr.md#r-111)
- [R-09 — Open Policy Agent et langage Rego](../references.fr.md#r-09)
- [R-10 — Langage d'autorisation Cedar et développement guidé par la vérification](../references.fr.md#r-10)
- [R-18 — Évaluation de Writ à partir des sources](../references.fr.md#r-18)
- [R-19 — Évaluation de Privateer à partir des sources](../references.fr.md#r-19)
- [R-20 — Assistant de preuve Lean](../references.fr.md#r-20)
- [R-21 — Conseils de versionnement et de reproductibilité des logiciels de recherche](../references.fr.md#r-21)
- [R-22 — Sémantiques natives de Git/Pijul et hébergement Nest](../references.fr.md#r-22)
- [R-35 — Common Criteria / ISO/IEC 15408 et évaluation EAL](../references.fr.md#r-35)
- [R-36 — RTCA DO-178C / EUROCAE ED-12C et niveaux DAL](../references.fr.md#r-36)
- [R-37 — Modélisation relationnelle Alloy](../references.fr.md#r-37)
- [R-38 — Model checking SPIN / Promela](../references.fr.md#r-38)
- [R-39 — Vérification de programmes Rust Kani](../references.fr.md#r-39)
- [R-40 — Vérification Rust Verus](../references.fr.md#r-40)
- [R-41 — Langage et vérificateur Dafny](../references.fr.md#r-41)
- [R-42 — Assistant de preuve Coq / Rocq](../references.fr.md#r-42)
- [R-43 — Assistant de preuve Isabelle](../references.fr.md#r-43)
- [R-44 — KAOS et ingénierie des exigences orientée objectifs](../references.fr.md#r-44)
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
- [R-104 — Formats d'instructions pour agents et workflows pilotés par les spécifications](../references.fr.md#r-104)
- [R-105 — Recherches sur le policy-as-code, l'assurance continue et la gouvernance des agents](../references.fr.md#r-105)
- [R-106 — Recommandations OWASP pour la sécurité des agents IA et de MCP](../references.fr.md#r-106)
- [R-108 — Graphe de chaîne d'approvisionnement GUAC](../references.fr.md#r-108)
- [R-109 — Spécification OpenSSF Security Insights](../references.fr.md#r-109)
- [R-110 — Référentiel OpenSSF OSPS Baseline](../references.fr.md#r-110)
- [R-111 — Programme OpenSSF Best Practices Badge](../references.fr.md#r-111)
- [R-112 — Politiques Git indépendantes de la forge avec gittuf](../references.fr.md#r-112)
- [R-113 — SLSA Source Track](../references.fr.md#r-113)
- [R-114 — Modèle d'ingénierie GRC Gemara](../references.fr.md#r-114)
- [R-115 — Exigences de soumission de Gerrit](../references.fr.md#r-115)
- [R-116 — OpenSSF Minder](../references.fr.md#r-116)
- [R-117 — OpenSSF Allstar](../references.fr.md#r-117)
- [R-118 — Tests de politiques avec Conftest](../references.fr.md#r-118)
- [R-119 — Langage de contraintes CUE](../references.fr.md#r-119)
- [R-120 — Évaluateur de sécurité/conformité OpenSSF Privateer](../references.fr.md#r-120)
- [R-121 — Attestation récapitulative de vérification SLSA](../references.fr.md#r-121)
- [R-122 — Signature et transparence Sigstore](../references.fr.md#r-122)
- [R-123 — Spécification contractuelle formelle Symboleo](../references.fr.md#r-123)
- [R-124 — Programmation littéraire législative Catala](../references.fr.md#r-124)
- [R-125 — Event Calculus](../references.fr.md#r-125)
- [R-126 — Vérification à l'exécution et surveillance de traces](../references.fr.md#r-126)
- [R-127 — GitHub CODEOWNERS et revue par propriétaires de code](../references.fr.md#r-127)
- [R-128 — Common Expression Language (CEL)](../references.fr.md#r-128)
- [R-129 — Argumentation éliminative](../references.fr.md#r-129)
- [R-130 — Moteur de politiques Kyverno](../references.fr.md#r-130)
- [R-131 — Règles d'approbation des merge requests GitLab](../references.fr.md#r-131)
- [R-132 — Gating de fusion Zuul et Bors](../references.fr.md#r-132)
- [R-133 — Théories formelles des patches](../references.fr.md#r-133)
- [R-134 — Standard Goal Structuring Notation (GSN)](../references.fr.md#r-134)
- [R-135 — Vérification NIST SP 800-192 des politiques de contrôle d'accès](../references.fr.md#r-135)
