# GovCheck

**Gouvernance formelle des dépôts logiciels, centrée sur le dépôt.**

GovCheck vise à rendre les règles de développement explicites, vérifiables par machine, traçables et applicables à l'acceptation des changements, indépendamment de l'agent, du VCS, de l'hébergement, de la forge ou d'un service distant.

> **État actuel :** les spécifications d'architecture sont prêtes pour revue. GovCheck n'est pas encore implémenté ni formellement vérifié. Les intentions de conception ne sont pas des garanties opérationnelles.

## Principes

- Le dépôt et son cycle de vie sont gouvernés ; humains et agents sont des contributeurs.
- Un modèle canonique versionné est l'unique autorité normative ; Markdown est une projection contrôlée ou une explication.
- Les fondations formelles de gouvernance et d'assurance s'appliquent à tous les dépôts, quelle que soit leur taille.
- Un petit exécutable local est l'interface principale ; aucun service hébergé, daemon ou serveur MCP obligatoire.
- Git et Pijul sont de première classe et sémantiquement distincts.
- Usages locaux, serveurs d'équipe, hébergements auto-gérés et publics sont dans le périmètre.
- VCS, hébergement, collaboration et acceptation sont des responsabilités séparées.
- Les contrôles locaux sont utiles ; l'application partagée relève d'une frontière d'intégration vérifiable indépendamment.
- Préférer un noyau réduit, des profils déclaratifs, des adaptateurs étroits et la réutilisation des outils existants.
- Bootstrap et migration suivent inspecter → planifier → appliquer, sans destruction.

## Langues

L'anglais est la langue par défaut : [README.md](README.md). Cette page est la version française.

## Spécifications d'architecture

Le premier cycle de conception est documenté dans [docs/specifications](docs/specifications/README.md) :
1. Modèle canonique de gouvernance.
2. Cycle de vie et acceptation des changements.
3. Contrats des adaptateurs VCS et collaboration.
4. Assurance, affirmations et preuves.

Chaque spécification existe en anglais et en français. Elles définissent des contrats proposés, pas un comportement implémenté.

Le raisonnement de conception, les distinctions d’assurance, l’audit du modèle de cycle de vie, l’autorité documentaire canonique, le métamodèle, le flux de développement et les évaluations de l’écosystème sont indexés dans [docs/architecture](docs/architecture/README.fr.md).

## Décisions et suite

[ADR 0001](docs/decisions/0001-bootstrap-boundaries.fr.md) consigne les frontières du bootstrap. Restent à décider : langage d'implémentation, format/schéma canonique, langage d'expression, noyau formel, approche cryptographique, licence et stratégie de dépendances. Ces choix doivent faire l'objet d'une analyse comparative explicite avant l'implémentation.

## Licence

Aucune licence n'a été choisie. Aucune permission de réutilisation, modification ou redistribution ne doit être présumée.
