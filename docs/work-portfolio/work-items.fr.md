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

- #41 est le fil de décision sur la révision de gouvernance applicable ; #86 porte la spécification technique associée. Le compte rendu bilingue 0008 consigne les onze choix explicitement arrêtés par l'autorité racine ; ils constituent les entrées de conception du travail technique et ne sont pas redemandés. Leur adoption normative reste un acte réservé à cette même autorité. Les spécifications 0003/0006, les modèles d'applicabilité et de publication canonique sont intégrés et vérifiés (Architectures 0031/0032 ; PR #96). Un premier modèle borné distinct est maintenant vérifié (Architecture 0033) : autorité de l'évaluateur antérieur, évaluation comparative uniquement pour un remplaçant, `Pass`/`Fail`/`Unknown`/`Conflict`, exceptions bornées/révocables, exigences non dérogeables, révocation prospective et requalification historique. Le chantier restant porte sur l'extension au-delà de l'instance à une évaluation/autorisation, la concurrence multi-publication, le rollback complet, l'acceptation du risque, le stockage durable, la reprise après panne et les adaptateurs Git/Pijul/répliques. #41 n'est pas adopté par ce travail technique.
- #33 reste un candidat atomique, sans décomposition artificielle.
- #46 est considéré terminé à la suite de la PR #39 fusionnée et de l'ADR 0005 ; sa clôture GitHub est différée jusqu'à l'acceptation de la migration du registre.
- #61 est un doublon historique remplacé par #62.
- #75 reste ouvert jusqu'à la décision formelle d'adoption de l'architecture 0028 et du registre.
- Les issues historiques #23, #26, #30, #35 et #37 restent liées comme provenance. Leur fermeture antérieure ne signifie pas que toutes leurs recommandations ont été adoptées.

## Règles de migration

Les issues #40 et #78–#85 restent ouvertes comme vues de navigation/coordination. Les issues individuelles restent des adaptateurs de coordination pendant la transition. Aucun contenu, commentaire ou historique source n'est supprimé. La clôture d'une issue exige une résolution typée et un lien vers le résultat, successeur ou enregistrement canonique ; l'import seul ne suffit pas.

La priorité, l'ouverture, l'assignation, la colonne Projects et la relation parent/enfant ne confèrent jamais d'autorisation. Le registre du dépôt est l'autorité documentaire ; une modification GitHub ne le remplace pas silencieusement.

Les modifications du registre doivent passer par une branche/canal de changement, une revue d'un candidat exact et un événement ajouté au journal. Le journal est append-only par politique, mais son application automatique, la réplication indépendante et les protections anti-altération ne sont pas encore implémentées.


## Mise à jour de l'étude des relations — issue #73 — 2026-11-10

Le périmètre de l'issue #73 couvre explicitement les contrats sémantiques entre intention du dépôt, besoins/attentes des parties prenantes, objectifs/résultats, exigences/contraintes, décisions/justifications, architecture/spécifications, réalisation, vérification/validation, assurance et autorité. Le travail reste un candidat P2 nécessitant une spécification ; cette précision ne vaut ni autorisation d'exécution ni adoption normative. Voir l'[étude des relations intention-assurance](../research/intent-relationship-model-survey.fr.md) dans la branche de travail dépendante.
