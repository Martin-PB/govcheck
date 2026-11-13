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
- `--capabilities` sélectionne les parties du package à installer (`check`, `forge`, `decisions`, `docs`, `formal`, `readme`, `scripts`, `workflows` ; par défaut : toutes).

La forme historique `python3 govcheck/bootstrap.py DOSSIER_CIBLE` initialise toujours un dépôt vide et refuse les cibles non vides. Les tests unitaires sont dans `tests/test_govcheck_bootstrap.py`.

## Vérifier un dépôt (première tranche exécutable)

`govcheck/check.py` est la première commande exécutable de GovCheck. Elle évalue un ensemble fixe de règles sur l’arborescence d’un dépôt et produit un rapport JSON déterministe, indépendant de la langue :

    python3 govcheck/check.py --tree . [--out report.json]
    python3 govcheck/check.py --tree . --base main --candidate HEAD

Chaque règle renvoie `pass`, `fail` ou `unknown`. Le résultat global est `fail` si une règle échoue, sinon `unknown` si une règle est inconnue, sinon `pass` (fermeture par l’échec : `unknown` n’est jamais un succès). Le code de sortie est 0 uniquement lorsque le résultat global est `pass`. Les règles couvrent les trois classes d’assurance : décidable (présence de la licence, paires de décisions bilingues, paires de paquet déclarées par le manifeste, intégrité du catalogue de références, sources obligatoires sur décisions et attestations, intégrité du marqueur d’amorçage), attestée (revue indépendante) et non vérifiable hors ligne (fraîcheur des preuves TLC). Les tests unitaires sont dans `tests/test_govcheck_check.py`.

### Attestations enregistrées (revue indépendante)

En mode git (`--base/--candidate`), la règle `independent-review` renvoie `pass` quand un enregistrement JSON dans `docs/attestations/*.json` porte `"decision": "accept"`, le SHA complet exact de la révision candidate dans `candidate_rev`, et un `reviewer` distinct de l’auteur du commit candidate. Sinon la règle reste `unknown` (fermeture par l’échec).

### Sources obligatoires (ADR 0007)

La règle `sources-present` (décidable) exige que chaque `docs/decisions/*.md` non guide porte une section `## Références` (ou `## References`) contenant au moins un lien de source : une ancre du catalogue de références (`docs/references.fr.md#r-xx`) ou une URL externe. Chaque enregistrement d’attestation dans `docs/attestations/*.json` doit aussi porter une liste `"sources"` non vide de chaînes, listant les preuves sur lesquelles le relecteur s’est appuyé. Les fichiers guides (`README*`, `TEMPLATE*`) sont exemptés. Sans cela, un agent pouvait énoncer une décision sans aucune preuve ; la règle rend « pas de source, pas de décision » vérifiable hors ligne.

### Intégrité du marqueur d’amorçage

La règle `bootstrap-integrity` (décidable) contrôle le marqueur possédé par le package `.govcheck-bootstrap.json` écrit par `govcheck/bootstrap.py apply` à la racine de la cible. Sans marqueur, la règle ne s’applique pas (pass, non applicable). Avec le marqueur, celui-ci doit être un objet JSON avec `"tool": "govcheck-bootstrap"`, un `"package_version"` non vide, un `"package_digest"` en SHA-256 hexadécimal minuscule de 64 caractères, une liste `"installed"` d’entrées `{path, sha256}` et une liste `"conflicts"` de chaînes non vides. Chaque chemin installé doit être relatif et sûr (pas de chemin absolu, pas de barre oblique inversée, pas de segment `.`/`..`/vide), et chaque fichier installé doit encore exister avec exactement l’empreinte SHA-256 enregistrée. Toute violation de schéma, fichier manquant ou dérive de contenu fait échouer la règle. Le marqueur est un document du dépôt, pas un sceau inviolable : il détecte la dérive accidentelle, pas un éditeur malveillant.


## Adaptateur de forge (govcheck/forge.py)

govcheck/forge.py est l'adaptateur natif de forge (Architecture 0034 du dépôt GovCheck) à deux rôles : un **miroir du registre** qui projette le portefeuille de travail canonique du dépôt sur les issues, labels et commentaires de la forge, et une **vérification côté forge** qui lit les exécutions de checks CI et la protection de branche pour qu'un rapport puisse indiquer si une révision candidate est couverte par des vérifications partagées, non falsifiables localement. La forge vérifie, elle n'autorise jamais : un check vert est une preuve, pas une autorité. La commande check reste hors ligne, en lecture seule et sans token, et n'appelle jamais l'adaptateur.

    python3 govcheck/forge.py list-issues [--state open] [--labels a,b]
    python3 govcheck/forge.py get-issue --number N
    python3 govcheck/forge.py list-labels
    python3 govcheck/forge.py check-runs --ref REF
    python3 govcheck/forge.py branch-protection [--branch main]
    python3 govcheck/forge.py create-issue --title T [--body B] [--labels a,b] [--registry-id govcheck.work.slug]
    python3 govcheck/forge.py update-issue --number N [--title T] [--state open|closed]
    python3 govcheck/forge.py comment --number N --body B
    python3 govcheck/forge.py capabilities

La configuration vient uniquement de l'environnement : GOVCHECK_FORGE (défaut github), GOVCHECK_FORGE_OWNER, GOVCHECK_FORGE_REPO, et le token GOVCHECK_FORGE_TOKEN (repli GITHUB_TOKEN). Les tokens ne sont jamais écrits sur disque, dans les logs ou dans les rapports, et les messages d'erreur ne les contiennent jamais. Les écritures (create-issue, update-issue, comment) exigent un token et ne sont que des commandes explicites ; check ne modifie jamais la forge. L'adaptateur n'utilise que la bibliothèque standard (REST GitHub v3 d'abord) avec un transport injectable, donc les tests unitaires tournent entièrement hors ligne ; les échecs sont typés (not-found, unsupported, unavailable, stale, conflict, auth, malformed) et un échec partiel n'est jamais rapporté comme un succès atomique. Les ids de registre (govcheck.work.<slug>) restent canoniques ; des tests d'aller-retour sans perte sont requis avant toute synchronisation en direct. Les tests unitaires sont dans tests/test_govcheck_forge.py. La capacité de bootstrap forge installe forge.py seul.
