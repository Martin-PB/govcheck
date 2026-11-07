# Package de gouvernance GovCheck

**English:** [README.md](README.md)

Ce dossier est la **seule** partie du dépôt GovCheck destinée à être copiée dans un autre dépôt pour le gouverner. Exécutez `python3 govcheck/bootstrap.py DOSSIER_CIBLE` (ou copiez govcheck/ tel quel à la racine du dépôt cible) et suivez la politique de bootstrap.

## Versions de publication indépendantes

La release du dépôt, celle du produit GovCheck et celle du package de gouvernance réutilisable **govcheck/** sont des identités distinctes. Le produit et le package possèdent des contrats SemVer indépendants ; une release du produit peut épingler une release du package, mais ne lui attribue ni n'incrémente sa version. Aucune première version du produit ou du package n'est déclarée avant la décision d'initial publication et l'existence d'un manifeste de release immuable. Voir l'ADR 0004 et les Architectures 0017–0018 du dépôt.


## Contenu (arborescence prévue)

- specifications/ — spécifications normatives de gouvernance (bilingues, anglais par défaut)
- formal/ — modèle de cycle de vie (TLA+), registre de transitions, catalogue d'artefacts, schémas JSON
- docs/formal/ — documentation du modèle de cycle de vie et diagramme généré
- scripts/ — générateur déterministe du diagramme et contrôle de drift
- .github/workflows/ — gabarit de workflow CI (synchronisé avec le dépôt méta par un contrôle)
- BOOTSTRAP_GOVERNANCE.md — politique de bootstrap temporaire
- decisions/ — guide et gabarit pour le registre de décisions **propre au dépôt cible** (aucune décision de GovCheck ici)
- docs/architecture/ — guide pour les enregistrements d'architecture propres au dépôt cible

## Deux niveaux

L'historique de gouvernance propre à GovCheck (records d'architecture, ADR, délibérations) vit au niveau méta du dépôt GovCheck et n'est délibérément **pas** inclus dans ce package. Voir l'ADR 0003 dans le dépôt GovCheck.