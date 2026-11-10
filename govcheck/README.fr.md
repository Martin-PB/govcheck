# Package de gouvernance GovCheck

**English:** [README.md](README.md)

Ce dossier est la **seule** partie du dépôt GovCheck destinée à être copiée dans un autre dépôt pour le gouverner. Exécutez `python3 govcheck/bootstrap.py DOSSIER_CIBLE` (ou copiez govcheck/ tel quel à la racine du dépôt cible) et suivez la politique de bootstrap.

## Versions de publication indépendantes

La release du dépôt, celle du produit GovCheck et celle du package de gouvernance réutilisable **govcheck/** sont des identités distinctes. Le produit et le package possèdent des contrats SemVer indépendants ; une release du produit peut épingler une release du package, mais ne lui attribue ni n’incrémente sa version. La première version cible prévue du produit GovCheck est **0.1.0** ; elle n’est ni publiée ni autorisée à ce stade. La première version du package réutilisable est indépendante et reste à attribuer jusqu’à sa propre décision d’initial publication et à l’existence d’un manifeste de release immuable. Voir l’ADR 0004 et les Architectures 0017—0018 du dépôt.

## Contenu (arborescence prévue)

- specifications/ — spécifications normatives de gouvernance (bilingues, anglais par défaut)
- formal/ — modèle de cycle de vie (TLA+), registre de transitions, catalogue d’artefacts, schémas JSON
- docs/formal/ — documentation du modèle de cycle de vie et diagramme généré
- scripts/ — générateur déterministe du diagramme et contrôle de drift
- .github/workflows/ — gabarit de workflow CI (synchronisé avec le dépôt méta par un contrôle)
- BOOTSTRAP_GOVERNANCE.md — politique de bootstrap temporaire
- decisions/ — guide et gabarit pour le registre de décisions **propre au dépôt cible** (aucune décision de GovCheck ici)
- docs/architecture/ — guide pour les enregistrements d’architecture propres au dépôt cible

## Deux niveaux

L’historique de gouvernance propre à GovCheck (records d’architecture, ADR, délibérations) vit au niveau méta du dépôt GovCheck et n’est délibérément **pas** inclus dans ce package. Voir l’ADR 0003 dans le dépôt GovCheck.

## Vérifier un dépôt (première tranche exécutable)

`govcheck/check.py` est la première commande exécutable de GovCheck. Elle évalue un ensemble fixe de règles sur l’arborescence d’un dépôt et produit un rapport JSON déterministe, indépendant de la langue :

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Chaque règle renvoie `pass`, `fail` ou `unknown`. Le résultat global est `fail` si une règle échoue, sinon `unknown` si une règle est inconnue, sinon `pass` (fermeture par l’échec : `unknown` n’est jamais un succès). Le code de sortie est 0 uniquement lorsque le résultat global est `pass`. Les règles couvrent les trois classes d’assurance : décidable (présence de la licence, paires de décisions bilingues, paires de paquet déclarées par le manifeste, intégrité du catalogue de références, sources obligatoires sur décisions et attestations), attestée (revue indépendante) et non vérifiable hors ligne (fraîcheur des preuves TLC). Les tests unitaires sont dans `tests/test_govcheck_check.py`.

### Attestations enregistrées (revue indépendante)

En mode git (`--base/--candidate`), la règle `independent-review` renvoie `pass` quand un enregistrement JSON dans `docs/attestations/*.json` porte `"decision": "accept"`, le SHA complet exact de la révision candidate dans `candidate_rev`, et un `reviewer` distinct de l’auteur du commit candidate. Sinon la règle reste `unknown` (fermeture par l’échec).

### Sources obligatoires (ADR 0007)

La règle `sources-present` (décidable) exige que chaque `docs/decisions/*.md` non guide porte une section `## Références` (ou `## References`) contenant au moins un lien de source : une ancre du catalogue de références (`docs/references.fr.md#r-xx`) ou une URL externe. Chaque enregistrement d’attestation dans `docs/attestations/*.json` doit aussi porter une liste `"sources"` non vide de chaînes, listant les preuves sur lesquelles le relecteur s’est appuyé. Les fichiers guides (`README*`, `TEMPLATE*`) sont exemptés. Sans cela, un agent pouvait énoncer une décision sans aucune preuve ; la règle rend « pas de source, pas de décision » vérifiable hors ligne.
