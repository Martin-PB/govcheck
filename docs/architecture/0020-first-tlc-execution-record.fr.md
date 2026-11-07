# 0020 — Première exécution enregistrée de TLC sur le modèle de cycle de vie

**Statut :** exécution enregistrée d'un contrôle mécanique (`MODEL_CHECKED` dans le vocabulaire de [0015](0015-governance-conformance-and-validation-plan.fr.md)) portant uniquement sur le modèle et la configuration enregistrés. Ce n'est ni une preuve sur l'implémentation, ni une revendication de conformité, ni une évidence sur un dépôt gouverné. **English:** [0020](0020-first-tlc-execution-record.md).

## Sujet et périmètre

- Modèle : `formal/tla/GovCheckLifecycle.tla` avec `formal/tla/GovCheckLifecycle.cfg`, dépôt `Martin-PB/govcheck`.
- Outil : `tla2tools.jar` v1.7.4, SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`, téléchargé depuis le miroir SourceForge du projet tlaplus et vérifié par somme de contrôle avant usage.
- Invocation : contrôle d'analyse SANY, puis `tlc2.TLC -config formal/tla/GovCheckLifecycle.cfg formal/tla/GovCheckLifecycle.tla`, exécutés par le workflow `.github/workflows/tla-check.yml`.

## Preuves

- Exécution du workflow sur la pull request [#15](https://github.com/Martin-PB/govcheck/pull/15) (commit de tête `49d9c2d43d10459e2878a1e36e188a38d57d50f0`, 6 novembre 2026) : le job `tlc` a conclu `success` ; le job `diagram-drift` a conclu `success`. Check runs : <https://github.com/Martin-PB/govcheck/pull/15/checks>.
- Le run publie la sortie brute en artefact `tlc-report` (`tlc-report.txt` et `tla2tools.sha256`).

## Limites

- `MODEL_CHECKED` ne couvre que le modèle TLA+ et la configuration TLC enregistrés. Cela n'établit pas la conformité de l'implémentation, et le modèle documente lui-même ses limites d'abstraction dans `docs/formal/lifecycle-model.fr.md`.
- Le résultat est lié à la version exacte de l'outil, à la configuration et à la révision du modèle ci-dessus ; il n'est pas transférable à d'autres révisions.
- Les exécutions antérieures du même workflow sur la PR #10 ont échoué au téléchargement de l'outil (asset mutable de la release v1.8.0) ; ces échecs sont notés ici par honnêteté et ne sont pas des résultats de model checking.

## Références bibliographiques

- [R-05 — modélisation par transitions d'états TLA+ / TLC](../references.fr.md#r-05)
