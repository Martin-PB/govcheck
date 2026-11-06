# 0019 — Évolution du catalogue d'artefacts et du manifeste de release

**Statut :** proposition de migration. Elle dépend de la revue/adoption des documents 0017 et 0018 et des schémas d'enregistrement dans formal/schemas. Aucun format actuel n'est modifié.

## 1. Objet

Le document 0017 sépare identité logique, révision immuable, version de contrat facultative, identité de release et identité d'événement. Le document 0018 définit les décisions d'autorité et de compatibilité. Les schémas de décision de version et de relation de dépendance proposent les formes d'enregistrement correspondantes.

Ce document explique comment intégrer ces concepts au catalogue d'artefacts et au manifeste de release sans confondre les versions de sérialisation de ces enregistrements avec les versions des artefacts décrits.

## 2. État actuel

Le fichier formal/artifacts.json contient catalogueVersion: 1, un objet textuel versioningPolicy et un tableau artifacts. Son entrée du modèle de cycle de vie possède un artifactId stable, des chemins source/configuration/documentation, une politique de révision fondée sur l'historique du dépôt et un lien de publication tag/commit.

Le schéma actuel du manifeste de release déclare schemaVersion: 1, lie un tag de release et un commit Git, puis liste chemins, empreintes SHA-256, rôles et métadonnées facultatives de preuve. Il rejette les propriétés inconnues. Le registre des transitions déclare séparément schemaVersion: 1. Ce sont des marqueurs de format propres à chaque document ; des valeurs numériques identiques ne couplent pas leurs formats.

Aucune entrée du catalogue ne déclare de version de contrat. Ne pas en déduire une d'un tag Git, d'un chemin, d'un marqueur de schéma ou d'une release. Une version de contrat exige les conditions de déclaration du §2.2 du document 0017 et l'autorisation prévue par le document 0018.

## 3. Quatre responsabilités d'enregistrement

1. **Catalogue d'artefacts :** identité logique stable, type, titre, chemins maintenus, stratégie de révision et métadonnées facultatives du contrat.
2. **Événement de décision de version :** enregistrement append-only des révisions antérieure/candidate, classification de compatibilité, autorité et résultat.
3. **Relation de dépendance :** relation typée et orientée entre des révisions exactes.
4. **Manifeste de release :** index de publication immuable liant le commit et les octets exacts des artefacts, preuves et enregistrements de gouvernance.

Le catalogue n'est pas un journal d'événements. L'historique des décisions et dépendances ne doit pas être écrasé dans ses champs mutables. Le manifeste enregistre ce qui a été publié ensemble ; il n'approuve pas les versions.

## 4. Entrée de catalogue proposée

Un futur schéma devrait exiger artifactId, kind, title, chemins source/location, revisionPolicy et releaseBinding. Un bloc contract facultatif peut identifier le contrat, son périmètre, les catégories de consommateurs, le sens de compatibilité et le dernier enregistrement de décision autorisé. Il ne doit pas contenir une SemVer modifiable indépendamment : l'événement de décision fait autorité. Une valeur en cache n'est acceptable que si un validateur prouve sa concordance avec cet événement.

Les dépendances restent dans le registre séparé des relations typées ; ne pas dupliquer une liste non typée dans chaque entrée.

Conserver catalogueVersion: 1 tant que le format actuel est utilisé. Ce champ désigne la révision de sérialisation/format du catalogue, et non la version de chaque artefact. Ne pas le renommer schemaVersion pour une simple cohérence de nommage. Une évolution future incompatible exige un schéma et un plan de migration délibérés.

## 5. Frontière du manifeste v2

Le schéma actuel rejette les propriétés supplémentaires. Ajouter des références de contrats ou des enregistrements de gouvernance à v1 serait donc incompatible pour les consommateurs stricts. Ne pas étendre v1 silencieusement.

Une future v2 devrait préserver le noyau v1 et ajouter des références liées par empreinte aux artefacts porteurs de contrat, aux décisions de version et aux relations de dépendance. Elle doit distinguer la version du format de manifeste de chaque version de contrat d'artefact. Une décision référencée doit être incluse ou récupérable de façon immuable ; les références orphelines et identifiants dupliqués doivent être rejetés.

Ne pas ajouter de SemVer globale pour la release du dépôt. Le tag/commit Git reste l'identité de release ; chaque artefact porteur de contrat conserve sa propre version approuvée.

## 6. Séquence de migration

1. Adopter 0017/0018 selon le processus canonique de gouvernance.
2. Adopter les schémas de décision de version et de relation de dépendance et définir les exigences du validateur.
3. Publier les schémas du catalogue et du manifeste avant de modifier les instances.
4. Implémenter des lecteurs acceptant les formats actuels et nouveaux ; les formats majeurs inconnus échouent de manière fermée avec un résultat explicite.
5. Ajouter uniquement les identifiants et métadonnées étayés par le dépôt ; n'inventer aucune version ou approbation historique.
6. Ajouter des dépendances uniquement lorsque les extrémités exactes et la sémantique sont connues ; marquer l'incertitude « revue requise ».
7. Créer des décisions de référence autorisées lorsque les contrats sont réellement approuvés ; ne pas les antidater.
8. Publier le premier manifeste v2 lorsque tous les artefacts et enregistrements référencés sont immuables et résolubles.
9. Conserver les manifestes v1 et l'historique du catalogue. La migration crée de nouveaux enregistrements ; elle ne réécrit pas les anciennes preuves de release.

## 7. Exigences de validation

Un futur validateur devrait vérifier l'unicité des identifiants stables ; la concordance des chemins/empreintes avec la release épinglée ; le lien des métadonnées de contrat à une décision autorisée pour le même artefact/révision ; le périmètre de l'autorité ; la résolution des extrémités de dépendance ; l'unicité et les empreintes des enregistrements de gouvernance ; l'absence de décision bloquée/rejetée/retirée/remplacée utilisée comme autorisation courante ; la fraîcheur des preuves ; et la prise en charge explicite des formats.

Ces contrôles sont structurels et inter-enregistrements. Compatibilité sémantique, légitimité de l'autorité et validité des preuves exigent toujours une évaluation de gouvernance/domaine. Une validation de schéma réussie n'est pas une approbation.

## 8. Choix différés

Ce document ne choisit ni base de données de graphe, ni format de signature, ni SemVer globale de release, ni algorithme automatique d'invalidation. Il ne modifie aucun JSON actuel et n'implémente aucun validateur. Le catalogue étant petit, un registre séparé de relations et des décisions immuables suffisent pour la première implémentation.

## 9. Documents associés

- [Architecture 0017](0017-artifact-identity-revision-and-versioning.fr.md).
- [Architecture 0018](0018-version-governance-and-compatibility-authority.fr.md).
- [Inventaire des schémas formels](../../formal/schemas/README.md).
- [Conception des enregistrements de décision de version et de dépendance](../../formal/schemas/version-governance-records.md).
- [Modèle canonique de gouvernance](../specifications/0002-canonical-governance-model.fr.md).
- [Cycle de vie et acceptation des changements](../specifications/0003-change-lifecycle.fr.md).
- [Assurance, affirmations et preuves](../specifications/0005-assurance-model.fr.md).
