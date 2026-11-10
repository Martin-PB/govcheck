# ADR 0006 — Portabilité VCS/forge de la décision GovCheck

**Statut :** proposé ; consigne l'analyse de transposabilité du 10 novembre 2026 répondant à la question du responsable : « notre décision est-elle transposable facilement à l'écosystème Pijul, voire hors de GitHub ? » En attente de décision explicite du responsable. **Anglais :** [0006 (English)](0006-vcs-forge-portability.md).

## Contexte

La conception adoptée repose sur quatre piliers : (1) le portefeuille de travaux gouverné, adossé au dépôt, est la source de vérité, les issues de la forge n'étant qu'un adaptateur de coordination (Architectures 0028, 0030) ; (2) une frontière d'acceptation contrôlée par des humains : aucune fusion sans approbation explicite du mainteneur, et une évaluation fail-closed où unknown n'est jamais un succès (`govcheck check`, PR #38 et #87) ; (3) des attestations de revue indépendante enregistrées dans `docs/attestations/*.json` et liées à la révision candidate exacte (SHA git complet de 40 hexadécimales dans `candidate_rev`) ; (4) le paquet à deux niveaux `govcheck/` (ADR 0003).

La tranche exécutable actuelle (`govcheck/check.py`, v0.2.0-slice) est couplée à git et GitHub en trois points : elle appelle la CLI git (`diff --name-only base...candidate`, `rev-parse`, `log -1 --format=...`), les attestations épinglent un SHA-1 de 40 hexadécimales, et le pipeline de dogfooding est un workflow GitHub Actions (`.github/workflows/govcheck-check.yml`, meta-only ; CI hébergée autorisée dans l'issue #88).

Les principes du projet (README) engagent déjà à être « indépendant de l'agent de codage, du système de gestion de versions, du fournisseur d'hébergement, de la forge » et énoncent que « Git et Pijul sont de première classe et sémantiquement distincts » ; la Spécification 0004 définit les contrats d'adaptateurs VCS et de collaboration. Cet ADR répond à la question de savoir si les piliers adoptés tiennent au-delà de git/GitHub, et ce qui doit changer.

## Décision (proposée)

Maintenir strictement séparées trois couches :

1. **Cœur agnostique de VCS/forge, transposable tel quel.** Le paquet `govcheck/`, les paires déclarées par le manifeste (ADR 0003), les règles décidables (`license-present`, `bilingual-decisions`, `manifest-pairs`, `reference-integrity`), la sémantique fail-closed (fail > unknown > pass ; code de sortie 0 uniquement sur pass), le rapport JSON et les attestations dans `docs/attestations/`. La frontière d'acceptation humain/agent est une politique écrite, pas du code.
2. **Adaptateur VCS : interface étroite, une implémentation par VCS.** `check.py` résout les révisions via un `VcsAdapter` à exactement trois opérations : `list_changed(base, candidate) -> [chemins]`, `resolve_rev(rev) -> rev_id`, `author_of(rev) -> identité`. `GitAdapter` est l'implémentation de référence aujourd'hui. Un `PijulAdapter` se mappe sur `pijul diff --channel <CHANNEL>`, `pijul log --output-format json` et `pijul change <HASH>`. La liaison des attestations se généralise d'un SHA nu de 40 hexadécimales à une référence de révision typée `{"vcs": "git" | "pijul" | ..., "rev": "<id natif>"}`.
3. **Adaptateur de forge : miroir du tracker, CI, identité.** Le tracker reste le portefeuille adossé au dépôt ; l'adaptateur de forge ne fait que refléter la coordination (issues/PR/discussions) et exécuter la CI. Le pipeline de CI lui-même (tests unitaires bloquants + `govcheck check` en report-only + artefact de rapport) est portable ; seule la syntaxe du workflow change (GitHub Actions, GitLab CI, Forgejo Actions ou Woodpecker, builds.sr.ht, ou hooks locaux).

### Matrice de transposabilité

| Élément | git + GitHub (aujourd'hui) | Autres forges git | Pijul | Fossil / Mercurial |
|---|---|---|---|---|
| Paquet `govcheck/`, règles décidables, fail-closed, rapport JSON | tel quel | tel quel | tel quel | tel quel |
| Attestations `docs/attestations/*.json` | tel quel | tel quel | schéma : `candidate_rev` devient `{vcs, rev}` typé | même changement de schéma |
| Frontière d'acceptation humaine (politique) | tel quel | tel quel | tel quel | tel quel |
| Accès aux révisions dans `check.py` | CLI git | CLI git | `pijul diff --channel`, `pijul log --output-format json`, `pijul change` | `fossil diff --from` / `fossil info` ; équivalents `hg` |
| Tracker comme source de vérité | API issues/PR + protection de branche | issues/MR GitLab + approbations ; API Gitea/Forgejo compatible GitHub | discussions de la nest ; pas de required-check natif | tickets Fossil ; revue par patches SourceHut |
| Check bloquant + refus démontré | required status check | pipeline obligatoire / approbation de MR | job CI de la nest + règle explicite du channel | CI externe + statut du ticket |
| Workflow CI | YAML Actions | GitLab CI / Woodpecker / Forgejo Actions / builds.sr.ht | Woodpecker ou CI externe | CI externe |
| Identité | login de la forge | login de la forge / commits signés | clés SSH | utilisateur Fossil / SSH |

### Spécificités de Pijul

- Pijul est fondé sur les patches, pas sur les commits : il n'y a pas de SHA-1. Les changes ont des identifiants base32 (ex. `TQU67HU5...`), adressables par préfixe non ambigu ; `pijul change <HASH>` affiche l'auteur et la date.
- Les channels sont l'analogue des branches mais sont mutables (rebasables) : une attestation doit épingler l'identifiant exact du change, jamais le nom du channel, exactement comme le mode git épingle le SHA du commit.
- `pijul diff --channel <CHANNEL>` compare à un autre channel (ou à la copie de travail) ; `pijul log --output-format json` fournit un historique lisible par machine.
- nest.pijul.com héberge code, discussions et jobs CI, mais n'a pas de « required status check sur une pull request » à la GitHub : le pattern du check bloquant se traduit par un job CI de la nest plus une règle explicite dans les discussions du channel.
- L'identité est fondée sur les clés SSH, pas sur un login.

## Conséquences

- `check.py` conserve sa CLI (`--tree/--base/--candidate/--out`) et détecte le VCS (git aujourd'hui ; `--vcs pijul` explicite plus tard) ; le cœur ne doit pas importer de code spécifique à un VCS hors de l'adaptateur.
- Schéma d'attestation v2 : `candidate_rev` devient `{"vcs": ..., "rev": ...}` ; la chaîne legacy de 40 hexadécimales reste acceptée pendant la tranche 0.x pour compatibilité ascendante.
- L'interface d'adaptateur est volontairement limitée à trois opérations : chaque VCS supplémentaire est un nouvel adaptateur, jamais un changement du cœur.
- Cet ADR n'implique aucune migration de ce dépôt : il rend la conception portable, il ne déplace pas le projet.
- Fonctionne sans aucune forge : `govcheck check --tree .` s'exécute en local et les attestations du dépôt restent valides ; seul le miroir de coordination externe disparaît, et le portefeuille adossé au dépôt est déjà le tracker canonique.

## Hors périmètre (travaux à suivre)

- Implémenter `PijulAdapter` (l'issue #58 explore déjà la sémantique de collaboration git/Pijul ; la Spécification 0004 définit les contrats).
- Choisir ou ajouter une seconde forge pour ce dépôt.
- Migrer le dépôt govcheck lui-même vers Pijul, Fossil ou Mercurial.
- Mécanismes de sign-off des contributions (DCO) et signature cryptographique des attestations.

## Références

- [Spécification 0004 — Contrats d'adaptateurs VCS et collaboration](../specifications/0004-vcs-collaboration-contracts.fr.md)
- [ADR 0003 — Gouvernance à deux niveaux](0003-two-level-governance.fr.md) ; [ADR 0005 — Licence (Pijul déjà listé comme outil GPL externe)](0005-license-apache-2-0-with-individual-attribution.fr.md)
- [Architecture 0028 — Portefeuille gouverné et frontière avec le tracker d'issues](../architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md)
- [Manuel Pijul — channels](https://pijul.org/manual/workflows/channels.html) ; [pijul diff](https://pijul.org/manual/reference/diff.html) ; [pijul change](https://pijul.org/manual/reference/change.html)
- [Discourse Pijul — `pijul log --output-format json`](https://discourse.pijul.org/t/how-to-efficiently-query-dependencies-for-all-changes/862)
- [nest.pijul.com](https://nest.pijul.com/)
- [GitLab Docs — SLSA niveau 3](https://docs.gitlab.com/ci/pipeline_security/slsa/level_3/)
- [Woodpecker CI — configuration Forgejo](https://woodpecker-ci.org/docs/next/administration/configuration/forges/forgejo)
- [SourceHut](https://sourcehut.org/) ; [Interface web Fossil](https://fossil-scm.org/home/doc/2026-06-23/www/webui.wiki)
- Issues #58 (sémantique git/Pijul), #88 (autorisation de CI hébergée), #92 (issue de suivi de cet ADR)
