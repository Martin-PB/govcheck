# Architecture 0034 — Modèle de durabilité, reprise et rollback du journal canonique

**Statut :** modèle de conception TLA+ borné ; vérification en attente. Ce document ne constitue ni une affirmation d'implémentation, ni une adoption normative, ni une preuve de durabilité opérationnelle. **English:** [0034](0034-canonical-journal-recovery-model.md).

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

## 3. Propriétés visées

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

## 5. Contrat et références associés

Ce modèle complète la [Spécification 0006](../specifications/0006-governance-revision-applicability.fr.md), l'[Architecture 0032](0032-canonical-publication-model-checking.fr.md) et l'[Architecture 0033](0033-governance-evaluator-exception-revocation-model.fr.md). Ses fondements conceptuels sont catalogués sous [R-05 — TLA+ et TLC](../references.fr.md#r-05) et [R-22 — sémantiques natives de Git et Pijul](../references.fr.md#r-22).

Il ne prétend pas que le journal, la procédure de reprise ou les adaptateurs VCS sont implémentés.
