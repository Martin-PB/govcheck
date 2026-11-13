# Journal des événements du portefeuille — index français

Le journal canonique des événements est conservé dans [Portfolio event journal](events.md). Il s'agit d'un registre append-only : cette page française est un point d'accès documentaire, et non une copie parallèle du journal. Les événements, leur ordre et leur historique de correction restent définis par le fichier canonique.

## Références mobilisées

- [R-05 — TLA+ et TLC](../references.fr.md#r-05)
- [R-107 — Emplacement et syntaxe des workflows GitHub Actions](../references.fr.md#r-107) : modèles formels et éléments de model checking mentionnés dans les événements.
- [R-22 — Sémantiques natives des VCS](../references.fr.md#r-22) : distinction entre les sémantiques des systèmes de contrôle de version et l'ordre du journal canonique.
- [R-194 — Linéarisabilité](../references.fr.md#r-194) : point de linéarisation des ajouts concurrents.
- [R-195 — Journalisation anticipée ARIES](../references.fr.md#r-195) : distinction entre commit durable et reprise.
- [R-196 — RFC 9110, idempotence](../references.fr.md#r-196) : nouvelle tentative après perte de réponse.

Pour consulter les entrées, leur provenance et leurs limites, se reporter au [journal canonique](events.md).

## WP-EVT-000019 — Rebasage des candidats d'intégration du métamodèle et du journal

- **Sujets :** `govcheck.work.intermodel-contract-conformance` et `govcheck.work.governance-revision-temporal-applicability`
- **Type d'événement :** `integration-review-rebased`
- **Date d'enregistrement :** 2026-11-13
- **Acteur/provenance :** instruction du responsable du dépôt de poursuivre jusqu'à ce que les deux PR soient prêtes ; consultations GitHub des branches, PR, comparaisons et vérifications.
- **Dossier du métamodèle :** la PR de remplacement [#122](https://github.com/Martin-PB/govcheck/pull/122), branche `review/metamodel-proof-carrying-mappings`, est directement fondée sur le `main` actuel. Elle consigne l'obligation universelle selon laquelle toute correspondance sémantique utilisée dans un raisonnement GovCheck doit disposer d'une démonstration formelle vérifiée par machine de la relation exacte revendiquée. Elle n'impose pas l'équivalence de modèles arbitraires et ne sélectionne ni assistant de preuve universel ni mode d'installation chez les adoptants.
- **Intégration du journal :** la PR de remplacement [#123](https://github.com/Martin-PB/govcheck/pull/123), branche `review/canonical-journal-proof-carrying`, est empilée sur la branche du métamodèle. Le modèle de reprise du journal reçoit le numéro Architecture 0035, puisque l'Architecture 0034 est déjà attribuée à l'adaptateur de portefeuille natif de forge. La Spécification 0007 exige désormais une correspondance porteuse de preuve avant de lier des représentations natives VCS à une identité commune de candidat ; un condensat de contenu identique n'est pas traité comme une preuve d'équivalence sémantique.
- **Dépendance/ordre :** la PR #122 doit être fusionnée avant la PR #123. La base de la PR #123 devra être redirigée vers `main` après la fusion de #122.
- **PR historiques :** #106 et #107 sont respectivement remplacées par #122 et #123 ; leurs branches et historiques de revue sont conservés. La fermeture des PR remplacées est distincte de la fusion des remplacements.
- **Frontière normative :** aucune des deux PR de remplacement, ses vérifications, sa revue ou sa fusion éventuelle n'adopte le métamodèle complet, la Spécification 0007 ni les onze résultats d'arbitrage. #41/#86 restent ouvertes à leurs stades existants.
- **Limites connues :** le résultat TLA+ du journal reste un élément de model checking borné pour son modèle/configuration finis exacts, pas une preuve de raffinement de l'implémentation, de consensus distribué ou de durabilité opérationnelle. L'obligation de preuve des mappings est une exigence de conception ; toutes les classes de correspondance ne sont pas encore implémentées ni démontrées par le prototype.
