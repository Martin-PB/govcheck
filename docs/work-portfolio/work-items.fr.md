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

- #41 est le fil de décision sur la révision de gouvernance applicable ; #86 en porte le travail de spécification technique associé.
- #33 reste un candidat atomique, sans décomposition artificielle.
- #46 est considéré terminé à la suite de la PR #39 fusionnée et de l'ADR 0005 ; sa clôture GitHub est différée jusqu'à l'acceptation de la migration du registre.
- #61 est un doublon historique remplacé par #62.
- #75 reste ouvert jusqu'à la décision formelle d'adoption de l'architecture 0028 et du registre.
- Les issues historiques #23, #26, #30, #35 et #37 restent liées comme provenance. Leur fermeture antérieure ne signifie pas que toutes leurs recommandations ont été adoptées.

## Règles de migration

Les issues #40 et #78–#85 restent ouvertes comme vues de navigation/coordination. Les issues individuelles restent des adaptateurs de coordination pendant la transition. Aucun contenu, commentaire ou historique source n'est supprimé. La clôture d'une issue exige une résolution typée et un lien vers le résultat, successeur ou enregistrement canonique ; l'import seul ne suffit pas.

La priorité, l'ouverture, l'assignation, la colonne Projects et la relation parent/enfant ne confèrent jamais d'autorisation. Le registre du dépôt est l'autorité documentaire ; une modification GitHub ne le remplace pas silencieusement.

Les modifications du registre doivent passer par une branche/canal de changement, une revue d'un candidat exact et un événement ajouté au journal. Le journal est append-only par politique, mais son application automatique, la réplication indépendante et les protections anti-altération ne sont pas encore implémentées.
