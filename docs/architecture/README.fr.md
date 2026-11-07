# Conception de l'architecture

L'anglais est la langue par défaut. Chaque document d'architecture possède une version française.

- [0006 — Modèle de menace et de confiance](0006-threat-and-trust-model.fr.md) · [English](0006-threat-and-trust-model.md)
- [0007 — Cadre de décision technologique](0007-technology-decision-framework.fr.md) · [English](0007-technology-decision-framework.md)
- [0008 — Plan de formalisation et de conformité](0008-formalization-and-conformance.fr.md) · [English](0008-formalization-and-conformance.md)
- [0009 — Mémoire de conception GovCheck et registre des décisions](0009-govcheck-design-discussion-record.fr.md) · [English](0009-govcheck-design-discussion-record.md)
- [0010 — Assurance, témoignage, preuve et conformité](0010-assurance-proof-and-conformance.fr.md) · [English](0010-assurance-proof-and-conformance.md)
- [0011 — Modèle de cycle de vie : audit des assertions](0011-lifecycle-model-assertion-audit.fr.md) · [English](0011-lifecycle-model-assertion-audit.md)
- [0012 — Autorité normative canonique et conformité documentaire](0012-normative-authority-and-documentation.fr.md) · [English](0012-normative-authority-and-documentation.md)
- [0013 — Métamodèle de gouvernance](0013-governance-metamodel.fr.md) · [English](0013-governance-metamodel.md)
- [0014 — Flux de développement gouverné et responsabilités](0014-governed-development-workflow.fr.md) · [English](0014-governed-development-workflow.md)
- [0015 — Outil de conformité de gouvernance et plan de validation](0015-governance-conformance-and-validation-plan.fr.md) · [English](0015-governance-conformance-and-validation-plan.md)
- [0016 — Évaluation de Writ et Privateer fondée sur leurs sources](0016-writ-privateer-assessment.fr.md) · [English](0016-writ-privateer-assessment.md)
- [0017 — Identité, révision et politique de versionnement des artefacts](0017-artifact-identity-revision-and-versioning.fr.md) · [English](0017-artifact-identity-revision-and-versioning.md)
- [0018 — Gouvernance des versions, compatibilité et autorité d'approbation](0018-version-governance-and-compatibility-authority.fr.md) · [English](0018-version-governance-and-compatibility-authority.md)
- [0019 — Évolution du catalogue d'artefacts et du manifeste de release](0019-catalogue-and-release-manifest-migration.fr.md) · [English](0019-catalogue-and-release-manifest-migration.md)
- [0020 — Première exécution enregistrée de TLC sur le modèle de cycle de vie](0020-first-tlc-execution-record.fr.md) · [English](0020-first-tlc-execution-record.md)
- [0021 — Affirmations, arguments et fraîcheur des preuves](0021-assurance-claims-and-freshness.fr.md) · [English](0021-assurance-claims-and-freshness.md)
- [0024 — Bootstrap de projet, choix de gouvernance et profils de capacités métier](0024-project-bootstrap-and-assurance-profiles.fr.md) · [English](0024-project-bootstrap-and-assurance-profiles.md)
- [0025 — Observations transverses au cycle de vie, traçabilité PEAK et intégration SACM](0025-runtime-observations-peak-and-sacm.fr.md) · [English](0025-runtime-observations-peak-and-sacm.md)
- [0026 — Capacité d'assurance conforme à SACM 2.4 et intégration dans GovCheck](0026-sacm-24-conformance-and-govcheck-integration.fr.md) · [English](0026-sacm-24-conformance-and-govcheck-integration.md)

Les documents 0009–0026 préservent le raisonnement de conception, les distinctions d'assurance et la proposition de bootstrap guidé. Le document 0024 décrit un bootstrap non destructif permettant de sélectionner les capacités métier et méthodes adaptées au projet ; il ne constitue pas une fonctionnalité implémentée. Le document 0025 replace les observations dans l'ensemble du cycle de vie et de ses domaines d'ingénierie, et distingue la traçabilité décisionnelle PEAK de la sémantique d'assurance SACM. Le document 0026 propose une couverture sémantique complète de SACM 2.4 Beta 1 comme capacité d'assurance dédiée de GovCheck, avec mappings intermodèles explicites et tests de conformité. Cela ne fait pas de SACM le métamodèle de gouvernance du dépôt dans son ensemble ; la proposition reste soumise à revue et implémentation. Le document 0021 propose une sémantique des claims, arguments, dépendances et invalidations ; elle reste à vérifier formellement et à relier au cycle de vie. Le document 0019 propose une migration progressive du catalogue et du manifeste de release ; il reste une proposition, pas un contrôle implémenté ni une règle normative approuvée. Les documents 0017 et 0018 proposent respectivement une politique de versionnement des artefacts par catégorie et le processus d'autorité/compatibilité associé. Ils n'imposent pas SemVer universellement et ne transforment pas les propositions en contrôles implémentés ou règles normatives approuvées.

## Statut

Ces documents sont des propositions et mémoires de conception, sauf indication contraire. Ils ne prouvent ni contrôles implémentés, ni propriétés de sécurité vérifiées, ni adoption technologique. Lire statut, périmètre et limites de chaque document.
