# GovCheck

**Gouvernance formelle des dépôts logiciels, centrée sur le dépôt.**

GovCheck vise à rendre les règles de développement explicites, vérifiables par machine, traçables et applicables au moment de l'acceptation des changements, indépendamment de l'agent, du VCS, de l'hébergement ou de la forge.

> **Bootstrap :** aucun exécutable, moteur canonique, preuve formelle ou mécanisme d'application n'est encore implémenté. Ce dépôt consigne les décisions de conception, pas des garanties opérationnelles.

## Principes

- Le dépôt et son cycle de vie sont l'objet gouverné ; humains et agents sont des contributeurs.
- Un modèle canonique versionné, lisible par machine, sera l'unique autorité normative. Markdown en sera une projection ou une explication contrôlée.
- Le socle formel s'applique à tout dépôt, quelle que soit sa taille.
- Petit exécutable local comme interface principale ; aucun service hébergé, daemon ou serveur MCP obligatoire.
- Git et Pijul sont de première classe, avec leurs sémantiques propres.
- Usages locaux, serveurs d'équipe, hébergements auto-gérés et forges publiques sont dans le périmètre.
- VCS, hébergement, collaboration et acceptation sont des responsabilités séparées.
- Noyau réduit, profils déclaratifs et adaptateurs étroits ; réutilisation des outils existants.
- Bootstrap et migrations selon inspecter → planifier → appliquer, sans écrasement silencieux.

## Langues

L'anglais est la langue par défaut : [README.md](README.md). Cette page est la version française.

## État

Le premier jalon est de définir le contrat canonique, la sémantique du cycle de vie, le vocabulaire d'assurance et les contrats d'adaptateurs avant de choisir le langage d'implémentation.

Voir [ADR 0001 — périmètre et architecture](docs/decisions/0001-bootstrap-boundaries.fr.md) et [la version anglaise](docs/decisions/0001-bootstrap-boundaries.md).

## Licence

Aucune licence n'a été choisie. Aucune permission de réutilisation ou redistribution ne doit être présumée.