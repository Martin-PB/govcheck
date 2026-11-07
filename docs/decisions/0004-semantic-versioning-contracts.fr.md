# ADR 0004 — Versionnement sémantique du produit GovCheck et du package de gouvernance

**Statut :** proposé à l'adoption ; consigne la décision explicite du propriétaire du projet d'adopter SemVer par catégorie le 07-11-2026. **English:** [0004](0004-semantic-versioning-contracts.md).

## Contexte

GovCheck doit adopter le versionnement sémantique, mais pas une version globale unique pour chaque fichier, modèle, décision, test, preuve, rapport ou publication. L'Architecture 0017 définit déjà une politique de compatibilité par catégorie ; l'Architecture 0018 définit l'autorité et le processus de décision. Les deux documents se présentent encore comme des propositions, ce qui ne reflète plus la décision du projet d'adopter le versionnement sémantique.

Le dépôt contient également deux livrables distincts : le produit GovCheck et le package de gouvernance réutilisable situé sous **govcheck/**. L'ADR 0003 décrit leurs rôles respectifs de produit et de méta-historique. Leurs versions ne doivent pas être confondues.

## Décision

1. **Adopter SemVer 2.0.0 comme standard de versionnement de GovCheck partout où un contrat de compatibilité déclaré donne un sens à MAJOR.MINOR.PATCH.** Les règles d'applicabilité et de compatibilité par catégorie de l'Architecture 0017 sont adoptées. SemVer n'est pas un mécanisme universel de révision des artefacts.
2. **Maintenir deux contrats de publication indépendants :**
   - **govcheck.product** : le produit GovCheck et ses interfaces publiques déclarées.
   - **govcheck.governance-package** : le package réutilisable **govcheck/** et ses interfaces de gouvernance/package déclarées.
   Ils possèdent des séquences de versions et des évaluations de compatibilité indépendantes. Une release du produit peut épingler une release du package, mais une version n'implique ni n'incrémente jamais l'autre.
3. **Utiliser des identifiants SemVer complets.** **0.1** peut servir d'abréviation informelle dans une discussion ; ce n'est pas un identifiant de release complet. Un identifiant complet comporte trois composantes numériques, par exemple **0.1.0**. Cet ADR ne déclare pas **0.1.0** comme release publiée ; cette valeur est uniquement consignée comme première version cible prévue du produit.
4. **Respecter la sémantique pré-1.0.** Tant qu'un contrat n'a pas atteint 1.0.0, il est en développement initial et son API publique n'est pas promise stable au sens de SemVer. Les changements incompatibles d'un contrat pré-1.0 déjà déclaré doivent néanmoins être explicites, documentés et reflétés par un incrément MINOR ; ils ne doivent pas être dissimulés dans une release PATCH.
5. **Préserver les régimes par catégorie de l'Architecture 0017.** SemVer s'applique à un contrat de produit/package/API/schéma/modèle/profil/ensemble de règles uniquement lorsque ses consommateurs, son périmètre, ses garanties, sa relation de compatibilité et son autorité d'approbation sont déclarés. Les règles individuelles, ADR, décisions, exceptions, approbations, exécutions de tests, exécutions de preuves, observations, éléments de preuve, rapports et manifestes ne reçoivent pas SemVer individuellement par défaut ; ils conservent des identités stables, des révisions/instances immuables et leur provenance.
6. **Séparer tous les axes de versionnement.** Les tags/commits Git identifient les releases/révisions du dépôt. SemVer du produit/package identifie les contrats de compatibilité. **schemaVersion** et **catalogueVersion** JSON identifient leurs formats de sérialisation/registre respectifs. Ces notions ne sont pas interchangeables.
7. **Exiger une décision explicite d'initial publication.** Ne pas déduire une première version d'une branche, d'un commit, d'une date, du répertoire du package, d'un marqueur de schéma ou d'une ancienne étiquette informelle. Ne pas inventer d'historique de versions ni d'approbations rétroactives. Lier chaque version publiée à une révision immuable et à un manifeste de release.
8. **Appliquer le processus de gouvernance de l'Architecture 0018.** Chaque incrément est évalué par rapport au contrat publié précédemment approuvé et à ses consommateurs déclarés. Une incertitude de compatibilité est **undetermined**, jamais un PATCH automatique. L'autorisation suit le régime d'autorité limité au sujet défini dans l'[Architecture 0023](../architecture/0023-bootstrap-governance-authority.fr.md) ; les permissions de dépôt, de fusion et de CI ne confèrent pas à elles seules d'autorité normative.
9. **Maintenir l'alignement du package réutilisable et du méta-historique GovCheck.** Toute modification normative du package doit mettre à jour le contrat générique du package et l'enregistrement correspondant au niveau méta GovCheck dans la même pull request, sans copier les décisions propres à GovCheck dans les dépôts gouvernés.

## Conséquences

- À la fusion de cet ADR, les Architectures 0017 et 0018 seront adoptées comme politiques de versionnement catégoriel et de gouvernance des versions ; cet ADR résoudra leur ancien statut de proposition.
- La Spécification 0002 distingue désormais explicitement le contrat du package de gouvernance réutilisable et le contrat de release du produit GovCheck. Cela n'adopte pas l'intégralité du modèle canonique de gouvernance et ne prétend pas qu'un évaluateur existe.
- Les valeurs existantes **catalogueVersion: 1**, **schemaVersion: 1**, les tags Git et les révisions historiques conservent leur signification actuelle. Aucune valeur existante n'est renommée ni convertie rétroactivement en SemVer.
- La première version cible prévue du produit GovCheck est **0.1.0** ; elle n'est ni publiée ni autorisée à ce stade. Le package de gouvernance réutilisable possède une séquence indépendante et aucune version ne lui est attribuée ici. Chaque première release exige sa propre décision d'initial publication, un contrat déclaré, l'approbation de l'autorité et un lien immuable vers la publication.
- Les schémas de décision de version/dépendance et leur validateur constituent un travail d'implémentation distinct. Leur validité structurelle ne peut établir la compatibilité sémantique ni l'autorité.
- La PR #21 a été fusionnée. Son enregistrement [Architecture 0023](../architecture/0023-bootstrap-governance-authority.fr.md) figure désormais dans main et fournit le fondement d'autorité pour la revue de cet ADR.

## Références

- [Architecture 0017 — Identité, révision et politique de versionnement](../architecture/0017-artifact-identity-revision-and-versioning.fr.md).
- [Architecture 0018 — Gouvernance des versions, compatibilité et autorité d'approbation](../architecture/0018-version-governance-and-compatibility-authority.fr.md).
- [Architecture 0019 — Évolution du catalogue d'artefacts et du manifeste de release](../architecture/0019-catalogue-and-release-manifest-migration.fr.md).
- [Spécification 0002 — Modèle canonique de gouvernance](../specifications/0002-canonical-governance-model.fr.md).
- [ADR 0003 — Gouvernance à deux niveaux](0003-two-level-governance.fr.md).
- [R-14 — Semantic Versioning 2.0.0](../references.fr.md#r-14).
- [R-15 — Tags Git et releases GitHub](../references.fr.md#r-15).
- [R-23 — Cadre de versionnement 1EdTech](../references.fr.md#r-23).
