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

L’historique de gouvernance propre à GovCheck (records d’architecture, ADR, délibérations) vit au niveau méta du dépôt GovCheck et n’est délibérément **pas** inclus dans ce p
ackage. Voir l’ADR 0003 dans le dépôt GovCheck.

## Amorcer un dépôt existant (inspect / plan / apply)

`govcheck/bootstrap.py` permet aussi d'adopter GovCheck dans un dépôt existant non vide sans rien détruire :

    python3 govcheck/bootstrap.py inspect CIBLE [--out rapport.json]
    python3 govcheck/bootstrap.py plan CIBLE [--capabilities check,docs] [--out plan.json]
    python3 govcheck/bootstrap.py apply CIBLE [--capabilities check,docs] [--plan plan.json] [--out resultat.json]
    python3 govcheck/bootstrap.py rollback CIBLE [--out resultat.json]

- `inspect` rapporte l'identité du package (étiquette de version et empreinte SHA-256 de l'arborescence du package), indique si la cible existe, est vide et est un dépôt git, quelles parties du package sont déjà présentes et quels chemins entreraient en conflit. Aucune mutation de la cible.
- `plan` produit un plan JSON déterministe d'actions (`create`, `identical`, `conflict`) sans effet de bord ; deux exécutions sur une cible inchangée donnent une sortie identique octet par octet.
- `apply` n'écrit que les actions `create` : les fichiers existants ne sont jamais écrasés, les conflits sont préservés et signalés. Deux applications successives sont idempotentes (la seconde ne crée rien). Avec `--plan`, apply vérifie d'abord que le plan correspond toujours à la cible et échoue sinon (code de sortie 2) : seules les modifications revues sont appliquées.
- L'identité du package est enregistrée dans un marqueur possédé par le package, `.govcheck-bootstrap.json`, à la racine de la cible (version, empreinte, fichiers installés avec leurs empreintes, conflits préservés). `rollback` supprime exactement les fichiers installés dont le contenu correspond encore à l'empreinte enregistrée, puis le marqueur : c'est le chemin de rollback documenté. La mise à niveau consiste à réexécuter `apply` avec un package plus récent : les fichiers modifiés par l'utilisateur ne sont jamais écrasés et apparaissent comme des conflits.
- `--capabi
lities` sélectionne les parties du package à installer (`check`, `decisions`, `docs`, `formal`, `readme`, `scripts`, `workflows` ; par défaut : toutes).

La forme historique `python3 govcheck/bootstrap.py DOSSIER_CIBLE` initialise toujours un dépôt vide et refuse les cibles non vides. Les tests unitaires sont dans `tests/test_govcheck_bootstrap.py`.

## Vérifier un dépôt (première tranche exécutable)

`govcheck/check.py` est la première commande exécutable de GovCheck. Elle évalue un ensemble fixe de règles sur l’arborescence d’un dépôt et produit un rapport JSON déterministe, indépendant de la langue :

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Chaque règle renvoie `pass`, `fail` ou `unknown`. Le résultat global est `fail` si une règle échoue, sinon `unknown` si une règle est inconnue, sinon `pass` (fermeture par l’échec : `unknown` n’est jamais un succès). Le code de sortie est 0 uniquement lorsque le résultat global est `pass`. Les règles couvrent les trois classes d’assurance : décidable (présence de la licence, paires de décisions bilingues, paires de paquet déclarées par le manifeste, intégrité du catalogue de références, sources obligatoires sur décisions et attestations, intégrité du marqueur d’amorçage), attestée (revue indépendante) et non vérifiable hors ligne (fraîcheur des preuves TLC). Les tests unitaires sont dans `tests/test_govcheck_check.py`.

### Attestations enregistrées (revue indépendante)

En mode git (`--base/--candidate`), la règle `independent-review` renvoie `pass` quand un enregistrement JSON dans `docs/attestations/*.json` porte `"decision": "accept"`, le SHA complet exact de la révision candidate dans `candidate_rev`, et un `reviewer` distinct de l’auteur du commit candidate. Sinon la règle reste `unknown` (fermeture par l’échec).

### Sources obligatoires (ADR 0007)

La règle `sources-present` (décidable) exige que chaque `docs/decisions/*.md` non guide porte une section `## Référence
s` (ou `## References`) contenant au moins un lien de source : une ancre du catalogue de références (`docs/references.fr.md#r-xx`) ou une URL externe. Chaque enregistrement d’attestation dans `docs/attestations/*.json` doit aussi porter une liste `"sources"` non vide de chaînes, listant les preuves sur lesquelles le relecteur s’est appuyé. Les fichiers guides (`README*`, `TEMPLATE*`) sont exemptés. Sans cela, un agent pouvait énoncer une décision sans aucune preuve ; la règle rend « pas de source, pas de décision » vérifiable hors ligne.

### Intégrité du marqueur d’amorçage

Quand la racine du dépôt contient le marqueur propriétaire du paquet `.govcheck-bootstrap.json` (écrit par `govcheck/bootstrap.py apply`), la règle `bootstrap-integrity` vérifie que :

- le marqueur est un JSON valide, objet JSON ;
- `tool` vaut `govcheck-bootstrap`, `package_version` est une chaîne non vide et `package_digest` est un SHA-256 hexadécimal minuscules de 64 caractères ;
- `installed` est une liste d’entrées `{path, sha256}` dont chaque chemin est relatif et sûr (pas de chemin absolu, pas d’antislash, aucun segment vide, `.` ou `..`), chaque `sha256` est en hexadécimal minuscules de 64 caractères, et chaque fichier enregistré existe avec exactement ce digest (fichier manquant ou contenu dérivé = échec) ;
- `conflicts` est une liste de chaînes non vides.

Tout problème fait échouer la règle. Sans marqueur à la racine de l’arbre, la règle n’est pas applicable et rapporte `pass` avec `applies: false`.
