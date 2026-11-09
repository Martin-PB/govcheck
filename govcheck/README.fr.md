# Package de gouvernance GovCheck

**English:** [README.md](README.md)

Ce dossier est la **seule** partie du d`2019`p`2019`t GovCheck destin`2019`e `2021` `2019`tre copi`2019`e dans un autre d`2019`p`2019`t pour le gouverner. Ex`2019`cutez `python3 govcheck/bootstrap.py DOSSIER_CIBLE` (ou copiez govcheck/ tel quel `2021` la racine du d`2019`p`2019`t cible) et suivez la politique de bootstrap.

## Versions de publication ind`2019`pendantes

La release du d`2019`p`2019`t, celle du produit GovCheck et celle du package de gouvernance r`2019`utilisable **govcheck/** sont des identit`2019`s distinctes. Le produit et le package poss`2019`dent des contrats SemVer ind`2019`pendants ; une release du produit peut `2019`pinger une release du package, mais ne lui attribue ni n'incr`2019`mente sa version. La premi`2019`re version cible pr`2019`vue du produit GovCheck est **0.1.0** ; elle n'est ni publi`2019`e ni autoris`2019`e `2021` ce stade. La premi`2019`re version du package r`2019`utilisable est ind`2019`pendante et reste `2021` attribuer jusqu'`2019` sa propre d`2019`cision d'initial publication et `2021` l'existence d'un manifeste de release immuable. Voir l'ADR 0004 et les Architectures 0017`2013`0018 du d`2019`p`2019`t.

## Contenu (arborescence pr`2019`vue)

- specifications/ `2014` sp`2019`cifications normatives de gouvernance (bilingues, anglais par d`2019`faut)
- formal/ `2014` mod`2019`le de cycle de vie (TLA+), registre de transitions, catalogue d'artefacts, sch`2019`mas JSON
- docs/formal/ `2014` documentation du mod`2019`le de cycle de vie et diagramme g`2019`n`2019`r`2019`
- scripts/ `2014` g`2019`n`2019`rateur d`2019`terministe du diagramme et contr`2019`le de drift
- .github/workflows/ `2014` gabarit de workflow CI (synchronis`2019` avec le d`2019`p`2019`t m`2019`ta par un contr`2019`le)
- BOOTSTRAP_GOVERNANCE.md `2014` politique de bootstrap temporaire
- decisions/ `2014` guide et gabarit pour le registre de d`2019`cisions **propre au d`2019`p`2019`t cible** (aucune d`2019`cision de GovCheck ici)
- docs/architecture/ `2014` guide pour les enregistrements d'architecture propres au d`2019`p`2019`t cible

## Deux niveaux

L'historique de gouvernance propre `2021` GovCheck (records d'architecture, ADR, d`2019`lib`2019`rations) vit au niveau m`2019`ta du d`2019`p`2019`t GovCheck et n'est d`2019`lib`2019`r`2019`ment **pas** inclus dans ce package. Voir l'ADR 0003 dans le d`2019`p`2019`t GovCheck.

## V`2019`rifier un d`2019`p`2019`t (premi`2019`re tranche ex`2019`cutable)

`govcheck/check.py` est la premi`2019`re commande ex`2019`cutable de GovCheck. Elle `2019`value un ensemble fixe de r`2019`gles sur l'arborescence d'un d`2019`p`2019`t et produit un rapport JSON d`2019`terministe, ind`2019`pendant de la langue :

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Chaque r`2019`gle renvoie `pass`, `fail` ou `unknown`. Le r`2019`sultat global est `fail` si une r`2019`gle `2019`choue, sinon `unknown` si une r`2019`gle est inconnue, sinon `pass` (fermeture par l'`2019`chec : `unknown` n'est jamais un succ`2019`s). Le code de sortie est 0 uniquement lorsque le r`2019`sultat global est `pass`. Les r`2019`gles couvrent les trois classes d'assurance : d`2019`cidable (pr`2019`sence de la licence, paires de d`2019`cisions bilingues, paires de paquet d`2019`clar`2019`es par le manifeste, int`2019`grit`2019` du catalogue de r`2019`f`2019`rences), attest`2019`e (revue ind`2019`pendante) et non v`2019`rifiable hors ligne (fra`2019`cheur des preuves TLC). Les tests unitaires sont dans `tests/test_govcheck_check.py`.


### Attestations enregistr`2019`es (revue ind`2019`pendante)

En mode git (`--base/--candidate`), la r`2019`gle `independent-review` renvoie `pass` quand un enregistrement JSON dans `docs/attestations/*.json` porte `"decision": "accept"`, le SHA complet exact de la r`2019`vision candidate dans `candidate_rev`, et un `reviewer` distinct de l'auteur du commit candidate. Sinon la r`2019`gle reste `unknown` (fermeture par l'`2019`chec).
