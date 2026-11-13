# Conception de l'architecture

L'anglais est la langue par défaut. Chaque document d'architecture possède une version française. L'[index bilingue des registres de décision](../decisions/README.fr.md) ([English](../decisions/README.md)) distingue les décisions de gouvernance des comptes rendus de provenance.

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
- [0022 — Audit des capacités de gouvernance](0022-governance-capability-audit.fr.md) · [English](0022-governance-capability-audit.md)
- [0023 — Décision d'amorçage de l'autorité de gouvernance](0023-bootstrap-governance-authority.fr.md) · [English](0023-bootstrap-governance-authority.md)
- [0024 — Bootstrap de projet, choix de gouvernance et profils de capacités métier](0024-project-bootstrap-and-assurance-profiles.fr.md) · [English](0024-project-bootstrap-and-assurance-profiles.md)
- [0025 — Observations transverses au cycle de vie, traçabilité PEAK et intégration SACM](0025-runtime-observations-peak-and-sacm.fr.md) · [English](0025-runtime-observations-peak-and-sacm.md)
- [0026 — Capacité d'assurance conforme à SACM 2.4 et intégration dans GovCheck](0026-sacm-24-conformance-and-govcheck-integration.fr.md) · [English](0026-sacm-24-conformance-and-govcheck-integration.md)
- [0027 — Référentiels sémantiques métier, modèles de décision et engagements du bootstrap](0027-domain-semantic-standards-decisions-and-bootstrap.fr.md) · [English](0027-domain-semantic-standards-decisions-and-bootstrap.md)
- [0028 — Portefeuille de travaux gouverné et frontière avec les gestionnaires d'issues](0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md) · [English](0028-governed-work-portfolio-and-issue-tracker-boundary.md)
- [0029 — Séparation des préoccupations CI et périmètres de vérification formelle](0029-concern-scoped-ci-and-formal-verification-boundaries.fr.md) · [English](0029-concern-scoped-ci-and-formal-verification-boundaries.md)
- [0030 — Registre du portefeuille gouverné dans le dépôt et historique révisable/récupérable](0030-repository-backed-work-portfolio-and-recoverable-history.fr.md) · [English](0030-repository-backed-work-portfolio-and-recoverable-history.md)
- [0031 — Première exécution TLC du modèle d'applicabilité de la gouvernance](0031-first-tlc-governance-applicability.fr.md) · [English](0031-first-tlc-governance-applicability.md)
- [0032 — Rapport de model checking du modèle de publication canonique](0032-canonical-publication-model-checking.fr.md) · [English](0032-canonical-publication-model-checking.md)
- [0033 — Modèle de contrôle des évaluateurs, exceptions et révocation](0033-governance-evaluator-exception-revocation-model.fr.md) · [English](0033-governance-evaluator-exception-revocation-model.md)
- [0034 — Adaptateur de portefeuille natif de forge (govcheck/forge.py)](0034-forge-native-portfolio-adapter.fr.md) · [English](0034-forge-native-portfolio-adapter.md)
- [0035 — Modèle de durabilité, reprise et rollback du journal canonique](0035-canonical-journal-recovery-model.fr.md) · [English](0035-canonical-journal-recovery-model.md)

L'architecture 0028 définit le cycle de vie du portefeuille et la frontière avec les gestionnaires d'issues. L'architecture 0030 ajoute le registre dans le dépôt, l'identité stable des éléments, les événements logiques préservés, la liaison aux révisions natives du VCS, les règles de migration et les limites explicites du mécanisme initial d'historisation/récupération. Aucun de ces documents ne prétend qu'un moteur de registre, un journal inviolable, une synchronisation automatique ou un service d'application est implémenté.

Les documents 0009–0027 préservent le raisonnement de conception, les distinctions d'assurance, les constats sur les capacités de gouvernance, la décision initiale d'autorité et la proposition de bootstrap guidé. Les documents 0017 et 0018 définissent respectivement la politique adoptée de versionnement des artefacts par catégorie et le processus d'autorité/compatibilité associé. L'ADR 0004 adopte ces politiques. SemVer n'est pas universel et l'application automatisée n'est pas encore implémentée.

## Registre de références

Le [catalogue unique des références](../references.fr.md) ([English](../references.md)) rassemble les sources externes, leurs usages, leurs limites et les renvois vers les documents qui les citent. Suivre le [guide de maintenance de l'intégrité des références](../reference-integrity.md) et exécuter le contrôle hors ligne avant toute modification du catalogue. Une référence n'implique ni adoption ni implémentation.

## Statut

Les documents d'architecture sont des propositions/mémoires de conception, sauf indication contraire dans leur statut individuel. Ils ne prouvent ni contrôles implémentés, ni propriétés de sécurité vérifiées, ni adoption technologique. Lire le statut, le périmètre et les limites de chaque document.

## Réconciliation de l'intention

L'[analyse d'impact de l'intention](../intent-impact-analysis.fr.md) ([English](../intent-impact-analysis.md)) met en correspondance l'orientation produit élargie avec les architectures/spécifications existantes et identifie l'audit complémentaire. Il s'agit d'une analyse de travail, pas d'un acte d'adoption.
