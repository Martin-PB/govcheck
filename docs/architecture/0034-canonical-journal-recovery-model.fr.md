# Architecture 0034 — Modèle de durabilité, reprise et rollback du journal canonique

**Statut :** modèle de conception TLA+ borné ; vérifié par SANY/TLC pour la configuration finie exacte. Il ne s'agit ni d'une preuve d'implémentation ni d'une adoption normative. Ce document ne constitue ni une affirmation d'implémentation, ni une adoption normative, ni une preuve de durabilité opérationnelle. **English:** [0034](0034-canonical-journal-recovery-model.md).

## 1. Objet

Ce modèle isole la frontière de persistance laissée ouverte par les modèles de publication canonique et de contrôles de gouvernance. Il examine les conséquences d'un ajout durable, d'une panne avant ou après cet ajout, de la reprise à partir du journal durable, d'un rollback comme nouvel événement et des observations de répliques VCS.

Il encode les choix de conception sélectionnés par le propriétaire et consignés dans la session d'arbitrage 0008 : le journal logique fait autorité sur l'ordre normatif ; Git, Pijul et les autres VCS fournissent des observations de transport et de provenance ; un rollback ajoute une nouvelle révision sans réécrire l'historique. Il ne réouvre pas ces choix et ne les adopte pas formellement.

## 2. Modèle

- Module : [GovCheckJournalRecovery.tla](../../formal/tla/GovCheckJournalRecovery.tla)
- Configuration : [GovCheckJournalRecovery.cfg](../../formal/tla/GovCheckJournalRecovery.cfg)
- Identifiant stable : `govcheck.journal-recovery`
- Miroir du package : `govcheck/formal/tla/GovCheckJournalRecovery.tla` et `.cfg`

Le modèle fini contient un journal durable append-only, un enregistrement en attente volatil, un marqueur de position appliquée, un indicateur de panne et les positions observées par chaque réplique. `CommitDurably` est le point de commit du journal. Une panne abandonne uniquement un enregistrement non commité. La reprise recalcule la position appliquée depuis la tête du journal durable. Un rollback ajoute un nouvel événement et une nouvelle révision dont le contenu provient d'une position antérieure du journal.

Les observations des répliques sont limitées aux positions présentes dans le journal ; elles ne peuvent ni ajouter, ni réordonner, ni sélectionner, ni faire avancer la tête normative. Une observation Git/Pijul relève donc de la provenance ou de la réplication, pas de la publication de gouvernance.

## 3. Propriétés vérifiées

- `TypeOK` : les valeurs d'état restent dans les domaines finis déclarés.
- `AppendOnly` : chaque transition conserve le journal antérieur comme préfixe exact.
- `UniqueEventAndRevisionIds` : les identités d'événement et de révision ne sont jamais réutilisées.
- `PositionAndPredecessorContinuity` : les positions augmentent d'une unité et chaque événement désigne la révision immédiatement précédente.
- `RollbackRestoresContentAsNewEvent` : le contenu restauré provient d'un état antérieur du journal, mais le rollback possède une nouvelle position et une nouvelle identité.
- `VCSObservationIsNonAuthoritative` : une observation de réplique ne peut dépasser la tête canonique.
- `AppliedStateIsDurable` : l'état appliqué ne peut dépasser la tête du journal durable.

## 4. Modèle de panne et limites

Il s'agit d'une petite abstraction finie à transitions, pas d'une spécification de moteur de stockage. Elle modélise un rédacteur sérialisé et un journal ; elle ne modélise ni écritures déchirées, ni ordre des opérations du système de fichiers, ni sommes de contrôle, quorum/consensus, acteurs byzantins, corruption disque, sauvegarde/restauration, gestion des clés, rédacteurs concurrents, protocoles de réconciliation de répliques divergentes ou véritable adaptateur Git/Pijul. Les observations de répliques sont volontairement passives et ne prouvent pas l'authenticité de la provenance.

L'action de reprise est une opération abstraite de rejeu jusqu'à la tête. Elle ne prouve pas qu'une implémentation concrète peut reconstruire tout état matérialisé ni que les effets externes sont idempotents. Les domaines bornés de contenus, révisions et événements n'établissent aucune correction non bornée.

Les résultats TLC, lorsqu'ils seront disponibles, constitueront uniquement des éléments de model checking pour le module et la configuration exacts. Ils ne seront ni preuve de théorème, ni vérification de l'implémentation, ni assurance de production.



## 6. Éléments de vérification TLC

Le module et la configuration exacts ont réussi SANY 2.1 et TLC 2.19 sur la tête de PR #99 `a5c9845b1df7a36c9b1f23af0a28bdabdd4300f3` (checkout de fusion CI consigné dans le workflow [42848709804](https://github.com/Martin-PB/govcheck/actions/runs/42848709804)).

- Blob Git du module : `f99b33f510f3350f7ee1dc2ecc4b13a216d64ab6`.
- Blob Git de la configuration : `43102a4fc3c17a0656ccfe71d34642457d85737a`.
- Résultat : 178 549 états générés, 38 434 distincts, zéro restant ; profondeur complète du graphe : 9.
- Les six invariants configurés et la propriété temporelle `AppendOnly` ont réussi ; aucun contre-exemple n'a été trouvé.
- Job : `129943126960` ; artefact du rapport ID `13778403717`, SHA-256 du ZIP `0fe3148982524a25336674718505b02fd786953bd000d9b06ae016ec4987d00b`.
- Chaîne d'outils : tla2tools v1.7.4 (SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`), SANY 2.1, TLC 2.19, Temurin Java 17.0.21+9, quatre workers.

Il s'agit d'éléments de model checking finis pour ces identités exactes de source et de configuration. Ce n'est ni une preuve de théorème, ni une vérification de l'implémentation, ni une preuve de durabilité d'un moteur de stockage. Le modèle vérifie des propriétés de sûreté et l'historique append-only ; il n'affirme pas la reprise éventuelle sous équité. L'autorisation et les contrôles d'évaluateur sont abstraits par les modèles amont de gouvernance/publication et ne sont pas revérifiés ici.



Revalidation de la tête finale de PR : les mêmes blobs du module et de la configuration ont été revérifiés sur la tête finale documentation/package `8ace02658a9f349db57e937c697e66c7b779aaa8` dans le [workflow 42849634866](https://github.com/Martin-PB/govcheck/actions/runs/42849634866), job `129946416981`. Le résultat est identique : 178 549 états générés / 38 434 distincts, zéro restant, profondeur 9 ; les six invariants et `AppendOnly` ont réussi. Artefact du rapport de la tête finale ID `13778459512`, SHA-256 `8ce7414863ef57725e7ae36e3055d10edb21571feb62c35d9fae68228a96b94c`. Les huit vérifications configurées de la PR ont toutes réussi sur cette tête finale.

## 5. Contrat et références associés

Ce modèle complète la [Spécification 0006](../specifications/0006-governance-revision-applicability.fr.md), l'[Architecture 0032](0032-canonical-publication-model-checking.fr.md) et l'[Architecture 0033](0033-governance-evaluator-exception-revocation-model.fr.md). Ses fondements conceptuels sont catalogués sous [R-05 — TLA+ et TLC](../references.fr.md#r-05) et [R-22 — sémantiques natives de Git et Pijul](../references.fr.md#r-22).

Il ne prétend pas que le journal, la procédure de reprise ou les adaptateurs VCS sont implémentés.
