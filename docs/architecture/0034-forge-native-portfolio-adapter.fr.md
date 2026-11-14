# Architecture 0034 — Adaptateur natif de forge (govcheck/forge.py) : miroir du registre et vérification côté forge

**Statut :** proposition d’architecture soumise à revue ; ce document n’implémente aucun code d’adaptateur, aucune configuration de forge, ni aucun contrôle de conformité. Il complète l’[ADR 0006](../decisions/0006-vcs-forge-portability.fr.md) et la [Spécification 0004](../specifications/0004-vcs-collaboration-contracts.fr.md) ; il ne les remplace pas.  
**Langue :** l’anglais est la langue par défaut ; voir la [version anglaise](0034-forge-native-portfolio-adapter.md).

## 1. Sujet et objectif

Définir un adaptateur natif de forge possédé par le dépôt, `govcheck/forge.py`, avec deux rôles :

1. **Miroir du registre :** synchroniser le portefeuille de travail canonique stocké dans le dépôt (`docs/work-portfolio/`, [Architecture 0030](0030-repository-backed-work-portfolio-and-recoverable-history.fr.md)) avec les objets de coordination de la forge hébergeant le dépôt (issues, PR, labels, commentaires).
2. **Vérification côté forge :** lire l’état de vérification de la forge (exécutions de checks CI, règles de branche protégée, checks requis) pour que `govcheck` puisse indiquer si un candidat est couvert par des vérifications partagées, non falsifiables localement.

Tout le contenu canonique reste dans le dépôt : la conception est indépendante de la forge, vise plusieurs forges, et fonctionne sans aucune forge. Lorsqu’une forge est présente, elle ajoute la frontière de vérification partagée que les seuls contrôles locaux ne peuvent pas fournir (Spécification 0004 : les hooks locaux peuvent être contournés par quiconque a accès au système de fichiers ; une application partagée forte exige une forge qui exige des vérifications valides liées à l’état exact du dépôt). La forge vérifie ; elle n’autorise jamais.

## 2. Contexte et motivation

- Les Architectures 0028/0030 font du registre dans le dépôt le tracker canonique ; les issues de la forge sont des adaptateurs/projections, et l’autorité va du registre vers l’adaptateur, jamais l’inverse. La synchronisation est initialement explicite/manuelle ; la dérive est rapportée, pas réconciliée silencieusement.
- L’ADR 0006 (proposé) nomme déjà la troisième couche : « adaptateur de forge : miroir du tracker, CI, identité », avec un pipeline CI portable (seule la syntaxe du workflow change selon la forge). La Spécification 0004 définit les contrats d’adaptateurs et constate qu’aucun adaptateur n’est encore implémenté.
- L’option brain.md (Apache-2.0, npm `@mindmux/brain-md` v0.4.1, dépôt <https://github.com/mindmuxai/brain.md>) a été évaluée puis écartée pour la machine de l’agent : son CLI Node.js sans dépendance (`bin/brain.mjs`, node >= 18) n’y est pas souhaitable. Ce document ne réutilise aucun contenu de brain.md ; toute réutilisation future devra être attribuée dans le [catalogue des références](../references.fr.md).
- L’issue #118 suit l’implémentation de ce document (fille de #63).

## 3. Décision d’architecture

Adopter un unique module d’adaptation limité à la bibliothèque standard, derrière un contrat indépendant de la forge :

1. **Contrat :** `govcheck/forge.py` expose de petites fonctions renvoyant des dicts simples : `list_issues`, `get_issue`, `create_issue`, `update_issue`, `list_labels`, `add_comment`, `list_check_runs`, `get_branch_protection`.
2. **Premier backend :** API REST v3 de GitHub via `urllib.request`, avec pagination et comportement sobre face aux limites de débit (requêtes minimales, pas de boucles d’interrogation).
3. **Identifiants :** jeton lu uniquement depuis l’environnement (`GOVCHECK_FORGE_TOKEN`, avec repli sur `GITHUB_TOKEN`) ; jamais persisté sur disque, dans les journaux ou les rapports ; erreur explicite et expurgée en cas d’absence.
4. **Neutralité :** aucun module hors de `forge.py` n’importe de code spécifique à une forge ; le chemin d’évaluation de `govcheck check` reste hors ligne et en lecture seule, sans jeton, et n’appelle jamais la forge.
5. **Testabilité :** le transport HTTP est injectable, donc les tests unitaires et les tests de contrat tournent entièrement hors ligne en CI avec un opener factice.
6. **Configuration :** type de forge, propriétaire et dépôt via variables d’environnement ou options CLI.
7. **Correspondance registre d’abord :** les IDs GovCheck stables (`govcheck.work.<slug>`) sont canoniques ; les numéros d’issues de la forge ne sont que des mappings d’adaptateur. Toute synchronisation en direct exige des tests d’aller-retour sans perte (ID registre, ID natif, direction des relations, historique) avant usage.
8. **Rôle de vérification :** l’adaptateur lit l’état de vérification de la forge (check runs, branche protégée) pour qu’un rapport `govcheck check --forge` puisse indiquer si le candidat est couvert par des checks requis côté forge. Modifier les règles de protection est une commande explicite et auditée. Le pipeline CI reste portable : mêmes checks, syntaxe de workflow propre à chaque forge (GitHub Actions aujourd’hui ; GitLab CI, Woodpecker, Forgejo Actions, builds.sr.ht, ou hooks locaux ailleurs). Sans forge, la gouvernance s’applique encore localement, mais l’application repose sur la révision main acceptée et son enregistrement de revue/fusion (limitation d’Architecture 0030).

## 4. Contrat de l’adaptateur

| Fonction | Entrée principale | Sortie | Notes |
|---|---|---|---|
| `list_issues(state, labels)` | filtre d’état, filtre de labels | liste de dicts d’issues | paginé ; mapping registre inclus |
| `get_issue(number)` | numéro d’issue | dict de l’issue | corps, labels, état inclus |
| `create_issue(title, body, labels)` | titre, corps, labels | dict de l’issue créée | commandes explicites seules ; reflète un élément du registre |
| `update_issue(number, ...)` | numéro, champs à modifier | dict de l’issue mise à jour | les clôtures sont des résolutions typées, pas des éditions brutes |
| `list_labels()` | aucun | liste de noms de labels | pilote les vérifications de taxonomie |
| `add_comment(number, body)` | numéro d’issue, corps markdown | dict du commentaire | les commentaires sont l’historique de discussion, pas des registres de décision |
| `list_check_runs(ref)` | ref (branche ou SHA) | liste de dicts de check runs | preuve de vérification en lecture seule |
| `get_branch_protection(branch)` | nom de branche | dict de protection | checks requis, règles de revue |

## 5. Sécurité et frontières de gouvernance

- Le chemin de `check` ne mute jamais l’état de la forge et ne requiert jamais de jeton.
- Les écritures (création/mise à jour d’issue, commentaire, changement de protection) n’ont lieu que dans des commandes explicites, l’identité de l’acteur et la justification étant consignées dans la sortie de la commande.
- L’autorité va du registre du dépôt vers la projection sur la forge ; les éditions côté forge n’écrasent jamais silencieusement le registre, et la dérive est rapportée plutôt que réconciliée automatiquement (Architecture 0030 section 7).
- L’adaptateur ne doit pas inférer le statut de candidat, l’engagement, l’approbation ou l’achèvement depuis les labels, états, colonnes de tableau ou même des checks verts : un check vert est une preuve, pas une autorité (Spécification 0004 : les commentaires/réactions ne sont pas des approbations sauf si la politique l’exige ; une capacité d’application manquante est une limitation visible, jamais un pass).
- Déclaration de capacités et taxonomie des échecs selon la Spécification 0004 : distinguer not-found, unsupported, unavailable, stale, conflict, échec d’authentification/autorisation et état malformé ; un échec partiel n’est jamais rapporté comme un succès atomique.
- Les mappings d’export/import doivent préserver les IDs du registre, les IDs natifs de la forge, l’identité du dépôt, la direction des relations et l’historique ; des tests d’aller-retour sont requis avant toute synchro en direct.

## 6. Non-objectifs pour cette tranche

- CLI ou SDK externes (pas de CLI brain.md, pas de dépendance `gh`, pas de runtime Node.js).
- Forges non GitHub (GitLab, Gitea, Codeberg, nest Pijul) : le contrat les permet, cette tranche ne les implémente pas.
- Synchronisation bidirectionnelle automatique entre registre et forge dans cette tranche ; écriture des champs structurés Projects v2.
- Toute mutation depuis `govcheck check`.
- Traiter les checks de la forge comme une autorisation : l’acceptation reste un événement de gouvernance typé enregistré dans le dépôt.

## 7. Vérification

- `python3 -m unittest discover -s tests -v` réussit avec les nouveaux tests unitaires et de contrat hors ligne (transport factice ; négociation de capacités, courses obsolètes, échecs d’authentification, échecs partiels selon la Spécification 0004).
- Un balayage d’imports atteste que `govcheck/forge.py` n’utilise que la bibliothèque standard de Python.
- `govcheck/README.md` et `govcheck/README.fr.md` documentent le contrat et les variables d’environnement.
- Le job CI `govcheck-check` reste vert et hors ligne.

## 8. Références

- [Architecture 0028 — Portefeuille de travail gouverné et frontière avec les gestionnaires d’issues](0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md)
- [Architecture 0030 — Portefeuille de travail dans le dépôt et historique récupérable](0030-repository-backed-work-portfolio-and-recoverable-history.fr.md)
- [ADR 0006 — Portabilité VCS et forge](../decisions/0006-vcs-forge-portability.fr.md)
- [Spécification 0004 — Contrats d’adaptateurs VCS et de collaboration](../specifications/0004-vcs-collaboration-contracts.fr.md)
- [Issue #118 — Adaptateur natif de forge : govcheck/forge.py](https://github.com/Martin-PB/govcheck/issues/118)
- [Issue #63 — Adaptateur GitHub du portefeuille et taxonomie de labels](https://github.com/Martin-PB/govcheck/issues/63)
- [Issue #92 (fermée) — Portabilité inter-forges de la décision GovCheck](https://github.com/Martin-PB/govcheck/issues/92)
- brain.md (évalué, non adopté) : <https://github.com/mindmuxai/brain.md> (Apache-2.0)
- [README du package govcheck](../../govcheck/README.md)

Catalogue de références : [R-104 — formats d'instructions pour agents et workflows natifs au dépôt](../references.fr.md#r-104).
