# ADR 0003 — Gouvernance à deux niveaux : package produit et historique méta

**Statut :** proposé. **English:** [0003](0003-two-level-governance.md).

## Contexte

GovCheck est lui-même du code en développement. Le dépôt doit donc servir deux usages à la fois : (1) fournir un package de gouvernance copiable dans tout nouveau dépôt, et (2) conserver l'historique vivant de la gouvernance propre à GovCheck (records, ADR, délibérations, spécificités).

## Décision

Maintenir deux niveaux vivants, mis à jour ensemble dans la même pull request :

1. **Package produit (`govcheck/`) :** le code de gouvernance livrable. Il évolue à chaque PR et, à tout commit, doit former un ensemble cohérent et autonome pour un nouveau dépôt : spécifications, modèle formel et schémas, contrôles exécutables (gabarit de workflow CI, drift check), politique de bootstrap, guide et gabarits de registre de décisions. Il ne contient aucun historique propre à GovCheck. Un script de bootstrap dans le package (`govcheck/bootstrap.py`) génère l'arborescence du dépôt cible à partir du package.
2. **Niveau méta (racine du dépôt) :** les documents vivants de GovCheck avec leurs spécificités — records de docs/architecture/, ADR de docs/decisions/, README et fichiers AGENTS racine. Ce niveau trace pourquoi et comment le package évolue.

Règle de duplication : quand une PR modifie un document normatif, les deux niveaux sont mis à jour dans cette même PR — version générique dans govcheck/ (pour les dépôts gouvernés) et version vivante spécifique au niveau méta. Un contrôle CI vérifie que les deux restent structurellement alignés (mêmes sections de gabarit), sans exiger un contenu identique. Exception : GitHub exige les workflows à la racine .github/workflows/, le workflow racine est donc généré depuis le gabarit du package par le contrôle de synchro.

## Migration

Par phases : cet ADR, le squelette du package et le script de bootstrap passent d'abord (PR #20). Les fichiers normatifs existants (docs/specifications/, docs/formal/, formal/, scripts/, docs/BOOTSTRAP_GOVERNANCE*, gabarit CI) sont ensuite dupliqués dans govcheck/ en versions génériques, les copies méta restant à la racine ; liens internes mis à jour ; contrôle d'alignement structurel ajouté.

## Conséquences

- Mettre en place la gouvernance dans un nouveau dépôt = exécuter le script de bootstrap du package (ou copier govcheck/), qui produit toute l'arborescence.
- Le niveau méta reste l'historique autoritaire de GovCheck lui-même et n'est jamais copié dans les dépôts gouvernés.

## Références bibliographiques

- [R-107 — Emplacement et syntaxe des workflows GitHub Actions](../references.fr.md#r-107)
