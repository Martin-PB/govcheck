# ADR 0003 — Gouvernance à deux niveaux : niveau méta et package portable

**Statut :** proposé. **English:** [0003](0003-two-level-governance.md).

## Contexte

GovCheck doit se gouverner lui-même (niveau méta : enregistrements d'architecture, registre de décisions, délibérations) tout en fournissant un package de gouvernance prêt à copier pour tout autre dépôt. Copier le dépôt entier mélangerait ces deux niveaux et divulguerait l'historique propre à GovCheck dans les dépôts gouvernés.

## Décision

Séparer le dépôt en deux niveaux :

1. **Niveau méta (racine du dépôt, non copiée)** : l'historique de gouvernance de GovCheck — enregistrements de docs/architecture/, ADR de docs/decisions/, README et fichiers AGENTS racine.
2. **Package portable (governance/, seul dossier copié dans un dépôt gouverné)** : spécifications normatives, modèle formel et schémas, contrôles exécutables (gabarit de workflow CI, script de drift check), politique de bootstrap, et guides/gabarits pour les registres propres au dépôt gouverné.

Règles anti-duplication :

- Le contenu normatif et exécutable a une source unique dans governance/ ; le niveau méta y fait référence par lien, jamais par copie.
- Le decisions/ du package ne contient qu'un guide et un gabarit pour le registre de décisions du dépôt gouverné ; les ADR de GovCheck restent au niveau méta.
- Exception : GitHub exige que les workflows soient à la racine .github/workflows/. Le workflow racine et governance/.github/workflows/tla-check.yml sont maintenus synchronisés par un contrôle, governance/ étant la source canonique.

## Migration

Par phases, pour éviter les conflits avec les PR #11/#12 ouvertes : cet ADR et le squelette du package passent d'abord ; docs/specifications/, docs/formal/, formal/, scripts/, docs/BOOTSTRAP_GOVERNANCE* et le gabarit de workflow CI seront déplacés dans governance/ une fois #11/#12 fusionnées, avec mise à jour des liens internes et ajout du contrôle de synchro du workflow.

## Conséquences

- Gouverner un nouveau dépôt signifie copier exactement un dossier : governance/.
- Le dépôt gouverné tient son propre registre de décisions (guidé par le gabarit du package), indépendant de l'historique de GovCheck.