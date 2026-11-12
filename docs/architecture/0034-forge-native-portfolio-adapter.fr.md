# Architecture 0034 — Adaptateur de portefeuille natif de forge (govcheck/forge.py)

**Statut :** proposition d’architecture soumise à revue ; ce document n’implémente aucun code d’adaptateur, aucune configuration de forge, ni aucun contrôle de conformité.  
**Langue :** l’anglais est la langue par défaut ; voir la [version anglaise](0034-forge-native-portfolio-adapter.md).

## 1. Sujet et objectif

Définir un adaptateur natif de forge possédé par le dépôt, `govcheck/forge.py`, afin que les commandes GovCheck puissent lire, et dans des commandes dédiées explicites écrire, le portefeuille de travail gouverné sur la forge hébergeant le dépôt, sans dépendre d’aucun CLI externe, SDK ou runtime non stdlib.

Ce document applique l’invariant de neutralité de l’adaptateur (#12) de l’[Architecture 0028](0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md) à la couche outillage : les champs et comportements spécifiques à une forge ne doivent pas devenir la sémantique canonique de gouvernance.

## 2. Contexte et motivation

- L’Architecture 0028 fait de GitHub l’adaptateur opérationnel initial, pas le modèle canonique ; l’issue #63 configure le côté GitHub (taxonomie de labels, vues Projects) ; l’issue fermée #92 couvrait déjà la portabilité inter-forges du registre de décision.
- L’option brain.md (Apache-2.0, npm `@mindmux/brain-md` v0.4.1, dépôt <https://github.com/mindmuxai/brain.md>) a été évaluée puis écartée pour la machine de l’agent : son CLI Node.js sans dépendance (`bin/brain.mjs`, node >= 18) n’y est pas souhaitable. Ce document ne réutilise aucun contenu de brain.md ; toute réutilisation future devra être attribuée dans le [catalogue des références](../references.fr.md).
- L’issue #118 suit l’implémentation de ce document.

## 3. Décision d’architecture

Adopter un unique module d’adaptation limité à la bibliothèque standard, derrière un contrat indépendant de la forge :

1. **Contrat :** `govcheck/forge.py` expose de petites fonctions renvoyant des dicts simples : `list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_labels`, `add_comment`.
2. **Premier backend :** API REST v3 de GitHub via `urllib.request`, avec pagination et comportement sobre face aux limites de débit (requêtes minimales, pas de boucles d’interrogation).
3. **Identifiants :** jeton lu uniquement depuis l’environnement (`GOVCHECK_FORGE_TOKEN`, avec repli sur `GITHUB_TOKEN`) ; jamais persisté sur disque, dans les journaux ou les rapports ; erreur explicite et expurgée en cas d’absence.
4. **Neutralité :** aucun module hors de `forge.py` n’importe de code spécifique à une forge ; le chemin d’évaluation de `govcheck check` reste hors ligne et en lecture seule, sans appel à la forge.
5. **Testabilité :** le transport HTTP est injectable, donc les tests unitaires tournent entièrement hors ligne en CI avec un opener factice.
6. **Configuration :** type de forge, propriétaire et dépôt via variables d’environnement ou options CLI.

## 4. Contrat de l’adaptateur

| Fonction | Entrée principale | Sortie | Notes |
|---|---|---|---|
| `list_issues(state, labels)` | filtre d’état, filtre de labels | liste de dicts d’issues | paginé |
| `get_issue(number)` | numéro d’issue | dict de l’issue | corps, labels, état inclus |
| `create_issue(title, body, labels)` | titre, corps, labels | dict de l’issue créée | commandes explicites seules |
| `update_issue(number, ...)` | numéro, champs à modifier | dict de l’issue mise à jour | les clôtures sont des résolutions typées, pas des éditions brutes |
| `list_labels()` | aucun | liste de noms de labels | pilote les vérifications de taxonomie |
| `add_comment(number, body)` | numéro d’issue, corps markdown | dict du commentaire | les commentaires sont l’historique de discussion, pas des registres de décision |

## 5. Sécurité et frontières de gouvernance

- Le chemin de `check` ne mute jamais l’état de la forge et ne requiert jamais de jeton.
- Les écritures (création/mise à jour d’issue, commentaire) n’ont lieu que dans des commandes explicites, l’identité de l’acteur et la justification étant consignées dans la sortie de la commande.
- L’adaptateur ne doit pas inférer le statut de candidat, l’engagement, l’approbation ou l’achèvement depuis les labels, états ou colonnes de tableau (Architecture 0028 section 7) ; il ne fait que transporter des données.
- Les mappings d’export/import doivent préserver les identifiants natifs, l’identité du dépôt, la direction des relations et l’historique (Architecture 0028 section 7).

## 6. Non-objectifs pour cette tranche

- CLI ou SDK externes (pas de CLI brain.md, pas de dépendance `gh`, pas de runtime Node.js).
- Forges non GitHub (GitLab, Gitea, Codeberg) : le contrat les permet, cette tranche ne les implémente pas.
- Écriture des champs structurés Projects v2 ; synchronisation automatique entre forge et registre.
- Toute mutation depuis `govcheck check`.

## 7. Vérification

- `python3 -m unittest discover -s tests -v` réussit avec les nouveaux tests hors ligne (transport factice).
- Un balayage d’imports atteste que `govcheck/forge.py` n’utilise que la bibliothèque standard de Python.
- `govcheck/README.md` et `govcheck/README.fr.md` documentent le contrat et les variables d’environnement.
- Le job CI `govcheck-check` reste vert et hors ligne.

## 8. Références

- [Architecture 0028 — Portefeuille de travail gouverné et frontière avec les gestionnaires d’issues](0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md)
- [Issue #118 — Adaptateur de portefeuille natif de forge : govcheck/forge.py](https://github.com/Martin-PB/govcheck/issues/118)
- [Issue #63 — Adaptateur GitHub du portefeuille et taxonomie de labels](https://github.com/Martin-PB/govcheck/issues/63)
- [Issue #92 (fermée) — Portabilité inter-forges de la décision GovCheck](https://github.com/Martin-PB/govcheck/issues/92)
- brain.md (évalué, non adopté) : <https://github.com/mindmuxai/brain.md> (Apache-2.0)
- [README du package govcheck](../../govcheck/README.md)
