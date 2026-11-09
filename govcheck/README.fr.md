# Package de gouvernance GovCheck

**English:** [README.md](README.md)

Ce dossier est la **seule** partie du d\u00e9p\u2019t GovCheck destin\u00e9e \u2019 \u2019tre copi\u00e9e dans un autre d\u00e9p\u2019t pour le gouverner. Ex\u00e9cutez `python3 govcheck/bootstrap.py DOSSIER_CIBLE` (ou copiez govcheck/ tel quel \u00e0 la racine du d\u00e9p\u2019t cible) et suivez la politique de bootstrap.

## Versions de publication ind\u00e9pendantes

La release du d\u00e9p\u2019t, celle du produit GovCheck et celle du package de gouvernance r\u00e9utilisable **govcheck/** sont des identit\u00e9s distinctes. Le produit et le package poss\u00e8dent des contrats SemVer ind\u00e9pendants ; une release du produit peut \u2019pinger une release du package, mais ne lui attribue ni n’incr\u00e9mente sa version. La premi\u00e8re version cible pr\u00e9vue du produit GovCheck est **0.1.0** ; elle n’est ni publi\u00e9e ni autoris\u00e9e \u00e0 ce stade. La premi\u00e8re version du package r\u00e9utilisable est ind\u00e9pendante et reste \u00e0 attribuer jusqu’\u2019 sa propre d\u00e9cision d’initial publication et \u00e0 l’existence d’un manifeste de release immuable. Voir l’ADR 0004 et les Architectures 0017\u20140018 du d\u00e9p\u2019t.

## Contenu (arborescence pr\u00e9vue)

- specifications/ \u2014 sp\u00e9cifications normatives de gouvernance (bilingues, anglais par d\u00e9faut)
- formal/ \u2014 mod\u00e8le de cycle de vie (TLA+), registre de transitions, catalogue d’artefacts, sch\u00e9mas JSON
- docs/formal/ \u2014 documentation du mod\u00e8le de cycle de vie et diagramme g\u00e9n\u00e9r\u00e9
- scripts/ \u2014 g\u00e9n\u00e9rateur d\u00e9terministe du diagramme et contr\u00f4le de drift
- .github/workflows/ \u2014 gabarit de workflow CI (synchronis\u00e9 avec le d\u00e9p\u2019t m\u00e9ta par un contr\u00f4le)
- BOOTSTRAP_GOVERNANCE.md \u2014 politique de bootstrap temporaire
- decisions/ \u2014 guide et gabarit pour le registre de d\u00e9cisions **propre au d\u00e9p\u2019t cible** (aucune d\u00e9cision de GovCheck ici)
- docs/architecture/ \u2014 guide pour les enregistrements d’architecture propres au d\u00e9p\u2019t cible

## Deux niveaux

L’historique de gouvernance propre \u00e0 GovCheck (records d’architecture, ADR, d\u00e9lib\u00e9rations) vit au niveau m\u00e9ta du d\u00e9p\u2019t GovCheck et n’est d\u00e9lib\u00e9r\u00e9ment **pas** inclus dans ce package. Voir l’ADR 0003 dans le d\u00e9p\u2019t GovCheck.

## V\u00e9rifier un d\u00e9p\u2019t (premi\u00e8re tranche ex\u00e9cutable)

`govcheck/check.py` est la premi\u00e8re commande ex\u00e9cutable de GovCheck. Elle \u00e9value un ensemble fixe de r\u00e8gles sur l’arborescence d’un d\u00e9p\u2019t et produit un rapport JSON d\u00e9terministe, ind\u00e9pendant de la langue :

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Chaque r\u00e8gle renvoie `pass`, `fail` ou `unknown`. Le r\u00e9sultat global est `fail` si une r\u00e8gle \u00e9choue, sinon `unknown` si une r\u00e8gle est inconnue, sinon `pass` (fermeture par l’\u00e9chec : `unknown` n’est jamais un succ\u00e8s). Le code de sortie est 0 uniquement lorsque le r\u00e9sultat global est `pass`. Les r\u00e8gles couvrent les trois classes d’assurance : d\u00e9cidable (pr\u00e9sence de la licence, paires de d\u00e9cisions bilingues, paires de paquet d\u00e9clar\u00e9es par le manifeste, int\u00e9grit\u00e9 du catalogue de r\u00e9f\u00e9rences), attest\u00e9e (revue ind\u00e9pendante) et non v\u00e9rifiable hors ligne (fra\u00eecheur des preuves TLC). Les tests unitaires sont dans `tests/test_govcheck_check.py`.

### Attestations enregistr\u00e9es (revue ind\u00e9pendante)

En mode git (`--base/--candidate`), la r\u00e8gle `independent-review` renvoie `pass` quand un enregistrement JSON dans `docs/attestations/*.json` porte `"decision": "accept"`, le SHA complet exact de la r\u00e9vision candidate dans `candidate_rev`, et un `reviewer` distinct de l’auteur du commit candidate. Sinon la r\u00e8gle reste `unknown` (fermeture par l’\u00e9chec).
