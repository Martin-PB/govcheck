# Références externes

**Statut :** registre consolidé des sources externes à l'appui des décisions de conception de GovCheck. L'anglais est la langue par défaut ; la version anglaise est [references](references.md).

Cette page liste les sources académiques et industrielles utilisées pour appuyer les décisions enregistrées dans l'[ADR 0001](../decisions/0001-bootstrap-boundaries.md), l'[ADR 0002](../decisions/0002-study-placement.md), l'[ADR 0003](../decisions/0003-two-level-governance.md), les spécifications 0002-0005 et les enregistrements d'architecture 0006-0021. Chaque entrée nomme le domaine de décision qu'elle soutient. Une source listée éclaire une décision ; elle ne rend aucune proposition implémentée ou approuvée.

## Vocabulaire d'assurance et classes de méthodes (spéc. 0005, enregistrements 0009, 0010, 0021)

- [Spécification SLSA](https://slsa.dev/spec/v1) — vocabulaire des « niveaux » de chaîne logistique ; justifie de réserver « levels » au sous-ensemble empirique dans la spéc. 0005.
- [Portail Common Criteria (ISO/IEC 15408, CC:2022)](https://www.commoncriteriaportal.org/cc/index.cfm) — niveaux d'assurance d'évaluation (EAL) ; cité dans la spéc. 0005 comme un axe « levels » distinct.
- [RTCA DO-178C](https://www.rtca.org/do-178/) — niveaux d'assurance de conception (DAL) pour l'avionique ; troisième axe « levels » distinct.
- [in-toto](https://in-toto.io/) — standard CNCF de métadonnées de chaîne logistique ; candidat pour les relevés d'intégrité (enregistrement 0007).

## Méthodes formelles (ADR 0001, spéc. 0005, enregistrements 0007, 0008, 0009, 0010)

- [Page TLA+ (Leslie Lamport)](https://lamport.org/tla/tla.html) — langage de spécification et model checker TLC ; base des modèles `govcheck.lifecycle` et `govcheck.assurance` (décision D-11).
- [Alloy / Alloy Analyzer](https://alloytools.org/) — model checking relationnel borné (Daniel Jackson) ; candidat dans les enregistrements 0007/0010.
- [Model checker SPIN](https://spinroot.com/spin/Doc/Book_extras/index.html) — model checking PROMELA (Gerard Holzmann) ; cité dans la spéc. 0005.
- [Preuve interactive Lean](https://www.microsoft.com/en-us/research/project/lean/) — assistant de preuve ; candidat pour la logique critique (ADR 0001, enregistrement 0010).
- [Assistant de preuve Coq](https://coq.inria.fr/) — cité dans la spéc. 0005 et l'enregistrement 0007.
- [Isabelle](https://isabelle.in.tum.de/) — assistant de preuve générique ; cité dans la spéc. 0005 et l'enregistrement 0007.
- [Vérificateur Kani pour Rust](https://model-checking.github.io/kani/) — vérification de programmes Rust ; cité dans la spéc. 0005.
- [Verus](https://verus-lang.github.io/verus/guide/) — Rust vérifié ; cité dans la spéc. 0005.
- [Dafny](https://www.microsoft.com/en-us/research/project/dafny-a-language-and-program-verifier-for-functional-correctness/overview/) — langage avec vérification intégrée ; cité dans la spéc. 0005.

## Moteurs de politiques (enregistrement 0010)

- [Open Policy Agent (OPA)](https://www.openpolicyagent.org/) — décisions de politique exécutables ; évalué comme non démonstrateur de théorèmes.
- [Cedar](https://cedarpolicy.com/) — langage de politiques de permissions (AWS) ; évalué de même.

## Versionnement, identité et provenance (enregistrement 0017)

- [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) — vocabulaire de compatibilité pour les contrats publics déclarés.
- [1EdTech Versioning Framework 1.0](https://www.imsglobal.org/spec/versioning/v1) — versionnement séparé des spécifications et artefacts.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/) — ontologie de provenance (entités, activités, agents).
- [DataCite — Versioning](https://support.datacite.org/docs/versioning) — identifiants de version et de concept.
- [Scientific Data (2024), cadre de versionnement des jeux de données](https://www.nature.com/articles/s41597-024-03153-y) — traitement spécifique des révisions de jeux de données.

## Ingénierie des exigences (enregistrement 0013)

- van Lamsde, A. (2009), *Requirements Engineering: From System Goals to UML Models to Software Specifications*, Wiley, ISBN 978-0-470-01270-3 ([page éditeur](https://www.wiley.com/en-ie/Requirements+Engineering%3A+From+System+Goals+to+UML+Models+to+Software+Specifications%2C+1st+Edition-p-9780470012703)) — raffinement d'objectifs façon KAOS/GORE référencé par le métamodèle de gouvernance.

## Gestion de versions (ADR 0001, spéc. 0004, enregistrement 0009)

- [Git](https://git-scm.com/) — première cible d'adaptateur VCS ; identité worktree/index dans la spéc. 0004.
- [Pijul](https://pijul.org/index.html) — VCS distribué fondé sur la théorie des patches ; deuxième cible d'adaptateur, sémantiquement distincte (décision D-05).

## Projets externes évalués comme bancs d'essai (enregistrement 0016 ; selon l'ADR 0002, ce sont des études, pas des dépendances)

- [infinri/Writ](https://github.com/infinri/Writ) — moteur de gouvernance de workflows Claude Code ; évalué au commit `ebdafe5450b201339f81e717ed104e6bcfd3fe3e`.
- [privateer-agent/privateer-agent](https://github.com/privateer-agent/privateer-agent) — distribution de l'agent de codage Pi ; évalué au commit `181a988e443fa6b6b4138fc349d1260c96408ad4`.

## Sources de l'étude d'intégration (ADR 0002 ; étude Cartocortex/MoriNet/SaussuNet)

- [Cartocortex](https://github.com/complexus-lab/cartocortex), [MoriNet](https://github.com/lejeunecedric/MoriNet), [SaussuNet](https://github.com/lejeunecedric/SaussuNet) — les trois dépôts de l'étude d'intégration qui a motivé l'ADR 0002.
- [CRDT (crdt.tech)](https://crdt.tech/) — types de données répliqués sans conflit envisagés pour la coédition temps réel.
- [RFC 5766 (TURN)](https://datatracker.ietf.org/doc/html/rfc5766.html) et STUN (RFC 5389), [WebRTC](https://webrtc.org/) — options de transport étudiées pour la collaboration temps réel.

## Règles de lecture

- Les sources sont citées avec leur URL publique canonique ; les évaluations de dépôts consignent aussi le commit exact examiné.
- Une source éclaire un raisonnement ; elle ne remplace jamais une décision autorisée de GovCheck et ne prouve pas qu'un contrôle est implémenté.
- Toute nouvelle source à l'appui d'une nouvelle décision est ajoutée ici dans le même changement que l'enregistrement de la décision.
