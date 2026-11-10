# ADR 0007 — Sources obligatoires pour les décisions et attestations

**Statut :** adoptée par le responsable du dépôt le 10 novembre 2026. **Anglais :** [0007 (English)](0007-mandatory-sources.md).

## Contexte

Un agent peut énoncer des décisions, des revues ou des affirmations sans preuve. Le catalogue de références (docs/references.md / docs/references.fr.md) indexe déjà les sources externes sous forme d'ancres R-xx avec rétroliens, et scripts/check-reference-integrity.py en assure l'intégrité, mais rien n'obligeait un document de décision à citer une source : un ADR pouvait satisfaire bilingual-decisions et reference-integrity tout en contenant zéro référence. L'issue #33 pose la règle de recherche (blogs et wikis = simples pistes ; sources académiques et standards = preuves) ; les issues #72, #74 et #77 suivent le corpus adversarial, la sémantique de statut des références et l'exigence de justification. Ensemble, elles motivent des sources obligatoires plutôt que conseillées.

## Décision

Ajouter une règle décidable `sources-present` à `govcheck/check.py` (tranche 0.3.0) :

1. Chaque `docs/decisions/*.md` non guide doit contenir un titre `## Références` / `## Références bibliographiques` / `## References` / `## Bibliographic references` suivi, avant le prochain titre `##`, d'au moins un lien de source : une ancre du catalogue de références (`references(.fr)?.md#r-xx`) ou une URL externe `http(s)://`. Les fichiers guides (`README*`, `TEMPLATE*`) sont exemptés.
2. Chaque enregistrement d'attestation dans `docs/attestations/*.json` doit porter une liste `sources` non vide de chaînes : les preuves sur lesquelles le relecteur s'est appuyé.
3. La règle est décidable et fail-closed : sources absentes ou vides = `fail`. Quand il n'y a ni documents de décision ni attestations, la règle n'est pas applicable.

Les fichiers `govcheck/decisions/TEMPLATE*` gagnent un placeholder Références pour que les dépôts cibles commencent conformes. L'ADR 0006 (branche docs/adr-0006-vcs-forge-portability, PR #93) a vu ses sources cataloguées R-109–R-113 lors de sa rédaction, ce qui est exactement le comportement que cette règle rend désormais obligatoire.

## Conséquences

- `govcheck check` rejette désormais hors ligne, en CI et dans tout dépôt cible amorcé avec le package, les décisions sans sources.
- Les agents doivent citer des ancres du catalogue (préféré : garde l'index unique des URL externes) ou des URL explicites ; les URL brutes laissées dans les documents de décision sont signalées par l'outil d'intégrité des références et devraient être cataloguées.
- Les décisions existantes ADR 0001–0005 portent déjà des références et restent conformes.

## Hors périmètre

- Vérifier qu'une source citée étaye réellement l'affirmation (l'adéquation sémantique relève de la revue humaine, enregistrée via les attestations).
- Signature cryptographique des attestations ou des sources.
- Réaudit rétroactif des dossiers d'architecture.

## Références

- [R-03 — Branches protégées et contrôles obligatoires GitHub](../references.fr.md#r-03)
- [R-06 — in-toto : intégrité de la chaîne d'approvisionnement logicielle](../references.fr.md#r-06)
- [R-24 — W3C PROV-O](../references.fr.md#r-24)
- [Intégrité du catalogue de références](reference-integrity.md)
- [ADR 0002 — placement de l'étude](0002-study-placement.fr.md)
- Issues #33 (règle de recherche), #72 (corpus adversarial), #74 (statut des références), #77 (justification)
