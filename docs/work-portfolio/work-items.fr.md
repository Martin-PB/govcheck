# Registre des éléments de travail GovCheck

**Statut :** import initial soumis à revue. Les éléments importés sont des candidats, sauf indication explicite contraire. Le registre du dépôt est canonique ; les numéros d'issues GitHub sont des correspondances d'adaptateur et des références de provenance. Les identifiants stables suivent la forme govcheck.work.<slug> et ne sont jamais réutilisés.

La [version anglaise du registre](work-items.md) contient l'inventaire détaillé, les résultats attendus, les classifications, les dispositions et les correspondances vers les issues sources. Les descriptions et discussions d'origine restent conservées sur GitHub pendant la transition ; elles constituent des sources de provenance, pas des décisions adoptées.

## Portefeuilles thématiques

| Identifiant | Domaine | Vue GitHub conservée |
|---|---|---|
| govcheck.portfolio.governance | Gouvernance, autorité, décisions | [#78](https://github.com/Martin-PB/govcheck/issues/78) |
| govcheck.portfolio.assurance | Tranche verticale, évaluation, assurance | [#79](https://github.com/Martin-PB/govcheck/issues/79) |
| govcheck.portfolio.enforcement | Enforcement, CI, opérations | [#80](https://github.com/Martin-PB/govcheck/issues/80) |
| govcheck.portfolio.formal | Modèles formels et cycle de vie | [#81](https://github.com/Martin-PB/govcheck/issues/81) |
| govcheck.portfolio.bootstrap | Bootstrap, paquet, distribution | [#82](https://github.com/Martin-PB/govcheck/issues/82) |
| govcheck.portfolio.research | Références, état de l'art, provenance | [#83](https://github.com/Martin-PB/govcheck/issues/83) |
| govcheck.portfolio.collaboration | Collaboration multi-agents et attribution | [#84](https://github.com/Martin-PB/govcheck/issues/84) |
| govcheck.portfolio.quality | Schémas, fixtures, qualité documentaire | [#85](https://github.com/Martin-PB/govcheck/issues/85) |

## Dispositions importantes

- #41 est le fil de décision sur la révision de gouvernance applicable ; #86 porte la formalisation technique. Le compte rendu bilingue 0008 consigne les onze choix explicitement sélectionnés par le propriétaire ; ils restent des entrées de conception arrêtées, mais leur adoption normative est un acte distinct réservé à cette même autorité. Les PR #90, #96 et #98 sont intégrées dans `main` (Architectures 0031–0033). Le modèle de reprise/rollback de l'Architecture 0035 et la Spécification 0007 proposée sont maintenant préparés dans la PR de remplacement [#123](https://github.com/Martin-PB/govcheck/pull/124), empilée sur le dossier du métamodèle [#122](https://github.com/Martin-PB/govcheck/pull/122). La PR #122 établit le principe selon lequel toute correspondance sémantique utilisée dans un raisonnement doit être formellement démontrée ; la Spécification 0007 applique cette exigence à l'identité commune de candidats VCS. Les modèles restent des abstractions finies distinctes ; les limites restantes incluent le multi-écrivain distribué, la durabilité d'un stockage concret, les adaptateurs VCS exécutables, la résolution des conflits, la fraîcheur complète des preuves, l'acceptation structurée du risque, les tests de conformité et le raffinement de l'implémentation. #41 n'est pas adopté par ce travail technique.
- #33 reste un candidat atomique, sans décomposition artificielle.
- #46 est considéré terminé à la suite de la PR #39 fusionnée et de l'ADR 0005 ; sa clôture GitHub est différée jusqu'à l'acceptation de la migration du registre.
- #61 est un doublon historique remplacé par #62.
- #75 reste ouvert jusqu'à la décision formelle d'adoption de l'architecture 0028 et du registre.
- Les issues historiques #23, #26, #30, #35 et #37 restent liées comme provenance. Leur fermeture antérieure ne signifie pas que toutes leurs recommandations ont été adoptées.

## Règles de migration

Les issues #40 et #78–#85 restent ouvertes comme vues de navigation/coordination. Les issues individuelles restent des adaptateurs de coordination pendant la transition. Aucun contenu, commentaire ou historique source n'est supprimé. La clôture d'une issue exige une résolution typée et un lien vers le résultat, successeur ou enregistrement canonique ; l'import seul ne suffit pas.

La priorité, l'ouverture, l'assignation, la colonne Projects et la relation parent/enfant ne confèrent jamais d'autorisation. Le registre du dépôt est l'autorité documentaire ; une modification GitHub ne le remplace pas silencieusement.

Les modifications du registre doivent passer par une branche/canal de changement, une revue d'un candidat exact et un événement ajouté au journal. Le journal est append-only par politique, mais son application automatique, la réplication indépendante et les protections anti-altération ne sont pas encore implémentées.


## Issue #86 — mise à jour de l'avancement technique — 2026-11-10

Les onze choix sélectionnés par l'autorité racine restent des entrées techniques arrêtées ; aucune nouvelle délibération ni adoption normative n'est impliquée. La PR #98 ajoute le modèle borné des évaluateurs, exceptions et révocation (Architecture 0033). La PR #99 ajoute le modèle distinct de durabilité, reprise et rollback du journal canonique (Architecture 0035) : le modèle fini exact a réussi SANY/TLC avec 178 549 états générés / 38 434 distincts, zéro restant, six invariants et `AppendOnly` (WP-EVT-000012). Ces résultats n'établissent ni l'implémentation ni la durabilité en production. Restent notamment la conception et l'implémentation réelles du journal/persistance, l'intégration compare-and-append, les sémantiques de stockage résistantes aux pannes, les adaptateurs de provenance Git/Pijul et la réconciliation des répliques divergentes, les tests de conformité exécutables et les éléments de raffinement. #86 reste ouverte.


## Issue #86 — contrat de protocole du journal proposé — 2026-11-10

Une Spécification 0007 bilingue et indépendante des technologies est proposée dans la PR #100. Elle définit l'identité et l'enveloppe des événements du journal, compare-and-append, le commit durable et les nouvelles tentatives idempotentes, la reprise après panne, la distinction des actes d'évaluation/autorisation/publication, les adaptateurs VCS limités à la provenance, la réconciliation des répliques, le vocabulaire des résultats bloquants et douze scénarios sémantiques de conformité. Elle ne sélectionne volontairement ni moteur de stockage, ni sérialisation, ni schéma de hachage/signature, ni produit de consensus, ni VCS ou forge. Le contrat reste proposé à la revue et n'est pas adopté normativement. Il doit guider les fixtures exécutables de conformité et les travaux d'implémentation ultérieurs ; #86 reste ouverte.


## Issue #86 — précisions proposées après revue — 2026-11-10

La PR [#104](https://github.com/Martin-PB/govcheck/pull/104), empilée sur la PR #100, traite des lacunes relevées dans le protocole de journal proposé : identité explicite du périmètre sans fixer la cardinalité dépôt/domaine, liaison de la genèse à l'ancre de confiance, propriétés minimales d'intégrité/authenticité, sémantique exacte et rétention des clés d'idempotence, ainsi que références primaires [R-194](../references.fr.md#r-194), [R-195](../references.fr.md#r-195) et [R-196](../references.fr.md#r-196). Elle corrige aussi la description EN/FR de l'Architecture 0035 sur la différence entre l'hypothèse d'équité et les propriétés de vivacité effectivement vérifiées. Il s'agit uniquement de précisions techniques ; la Spécification 0007 reste proposée et aucune adoption normative ni implémentation n'est revendiquée. #86 reste ouverte.

## Réconciliation de l'intégration #41 / #86 — 2026-11-11

- **#41 :** reste ouverte au stade `needs-decision`. Les onze choix figurent dans le [compte rendu 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md) comme choix de séance ; aucune adoption normative n'est intervenue et l'Architecture 0023 n'est pas modifiée.
- **#86 :** reste ouverte au stade `in-progress`. La PR [#90](https://github.com/Martin-PB/govcheck/pull/90) est fusionnée dans `main` au commit `5af21e58ef597480061a2712aaf94a3e2980ba7f`), la PR [#96](https://github.com/Martin-PB/govcheck/pull/96) au commit `934000a73aa0f34acd9b692b072d29b7877a8f2b`), et la PR [#98](https://github.com/Martin-PB/govcheck/pull/98) au commit `a9ea85796e9864296bef4c0ff33d174d63dc3b75`.
- **PR #99 :** GitHub la marque fusionnée dans l'ancienne branche `work/issue-86-governance-controls-model`, pas dans `main`. Sa tête `e9a57ad63f223a2d934e9ec44f272b4684499dbd` diverge de `main` (48 commits en avance, 1 en retard ; base commune `502e43d4ea55a4a5beec07573dab80c69a6796a0`). Le modèle de reprise/rollback n'était donc pas intégré à `main`.
- **Propositions empilées :** la PR [#100](https://github.com/Martin-PB/govcheck/pull/100) reste ouverte/non-draft, basée sur `work/issue-86-journal-recovery-model` ; la PR [#104](https://github.com/Martin-PB/govcheck/pull/104) reste ouverte/non-draft, basée sur `work/issue-86-journal-protocol-spec`. Aucune des deux n'est fusionnée dans `main`.
- **Dernière validation enregistrée de la PR #104 :** l'exécution [42891011411](https://github.com/Martin-PB/govcheck/actions/runs/42891011411) a échoué au contrôle hors ligne d'intégrité des références (17 erreurs, 8 avertissements) ; l'alignement du package et le contrôle GovCheck report-only ont réussi. Les défauts portaient sur l'index thématique et les backlinks R-194 à R-196, le backlink [R-107](../references.fr.md#r-107) obsolète, les mentions non liées et l'écart de citations EN/FR. Le présent candidat corrige ces défauts documentaires. Aucune nouvelle exécution Actions n'a été déclenchée.
- **Candidat courant :** la [PR #107](https://github.com/Martin-PB/govcheck/pull/107) est ouverte, non-draft, cible `main` et est actuellement mergeable ; la branche `work/issue-41-formalization-reconciliation` transporte les artefacts #99/#100/#104 et réconcilie les documents bilingues, modèles, références et registre. Aucune issue n'est fermée, aucune adoption normative n'est inférée et aucune implémentation n'est revendiquée.
- **Références du protocole :** [R-194](../references.fr.md#r-194), [R-195](../references.fr.md#r-195) et [R-196](../references.fr.md#r-196).


## Source SACM — provenance du digest

La première capture source-native du métamodèle OMG SACM 2.4 Beta 1 réutilise la valeur de comparaison SHA-256 publiée par l'audit indépendant [R-128](../references.fr.md#r-128). Le workflow GovCheck l'a vérifiée sur les 524 243 octets téléchargés depuis l'URL officielle (exécution [43443933268](https://github.com/Martin-PB/govcheck/actions/runs/43443933268)). La branche d'implémentation est [PR #126](https://github.com/Martin-PB/govcheck/pull/126) ; l'inventaire MOF/XMI et les correspondances dérivées de la source restent à réaliser.
