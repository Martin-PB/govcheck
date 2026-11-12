# Recherche d'applicabilité de GovCheck : constructivisme, irréductibilité et modélisation systémique

**Identifiant de recherche :** STUDY-003-APP  
**Statut :** évaluation d'applicabilité transversale provisoire ; non normative. Aucune capacité produit n'est déclarée implémentée et aucune modification du métamodèle n'est adoptée.

## Objet

Cette note traduit les trois sessions de [STUDY-003](le-moigne-colloquium.fr.md) en questions relatives à l'adéquation et aux limites de GovCheck. Elle ne transforme pas le colloque en spécification produit. Il faut distinguer (1) ce que suggère la recherche, (2) ce que l'outil de gouvernance de dépôt pourrait raisonnablement soutenir, (3) ce qui exige d'autres méthodes ou preuves externes et (4) ce qui reste une question de conception ouverte.

## Évaluation préliminaire de l'adéquation

### Contextes dans lesquels GovCheck pourrait être bien adapté

Le rôle visé de GovCheck dans la gouvernance des dépôts est pertinent lorsqu'un projet doit rendre explicites et traçables :

- les finalités et points de vue qui sous-tendent intentions, objectifs, exigences, modèles et décisions ;
- le périmètre, les hypothèses, frontières, exclusions et dépendances d'un modèle de gouvernance ou d'assurance ;
- les relations entre modèles, affirmations, arguments, preuves, résultats de vérification et décisions autorisées ;
- les changements de modèles et d'hypothèses dans le temps, y compris leurs effets sur les preuves antérieures ;
- les incertitudes non résolues, inconnues connues, interactions non modélisées et risques résiduels acceptés ;
- plusieurs modèles partiels pour différents sujets, sans supposer qu'une représentation unique est exhaustive.

Il s'agit de domaines d'adéquation candidats déduits de l'orientation produit existante. Ce ne sont pas des affirmations selon lesquelles toutes ces capacités sont déjà implémentées.

### Contextes où GovCheck peut aider sans suffire seul

Certains besoins exigent des approches complémentaires :

- **Enquête et délibération entre parties prenantes :** un dépôt peut préserver points de vue, décisions et traçabilité, mais ne peut pas faciliter à lui seul des échanges difficiles ni garantir une participation réelle. Des méthodes comme la SSM ou la recherche collaborative peuvent être nécessaires.
- **Modélisation métier/système :** GovCheck peut gouverner identité, hypothèses, périmètre, revue et preuves d'un modèle ; des outils spécialisés et une expertise métier peuvent être nécessaires pour construire et valider les modèles substantiels.
- **Adéquation empirique :** tests, observations, études de terrain, mesures opérationnelles et évaluations expertes sont nécessaires pour apprécier si un modèle convient au phénomène et à l'usage visé.
- **Évaluation de la complexité et de l'incertitude :** le projet doit identifier la forme d'incertitude ou d'irréductibilité pertinente. Une étiquette générique « complexité » ne suffit pas.
- **Vérification formelle :** preuve et model checking peuvent valider des affirmations formelles précises sous des hypothèses déclarées ; ils ne valident pas à eux seuls l'abstraction, sa frontière, la légitimité de la finalité ou la vérité des hypothèses externes.

### Contextes où GovCheck seul serait inadapté

GovCheck ne doit pas être présenté comme suffisant lorsque le besoin réel consiste à :

- produire une représentation complète ou définitive de la réalité ;
- résoudre des désaccords entre parties prenantes sans processus délibératif ;
- garantir que toutes les interactions émergentes ou inconnues inconnues ont été modélisées ;
- remplacer expertise scientifique/métier ou observation empirique ;
- prouver qu'un modèle formel représente fidèlement un système sociotechnique ;
- transformer un jugement incertain ou contesté en fait objectif par le seul fait de l'enregistrer.

La bonne explication produit doit préciser la partie que GovCheck peut soutenir, les méthodes/preuves complémentaires nécessaires, l'incertitude résiduelle et l'autorité responsable de l'acceptation du risque.

## Audit candidat au regard des concepts GovCheck existants

Cette correspondance est volontairement une liste de contrôle de recherche, pas une nouvelle ontologie.

| Préoccupation conceptuelle | Domaines GovCheck existants à examiner | Question d'audit |
|---|---|---|
| Finalité, point de vue, observateur | intention, objectif, partie prenante/autorité, décision | Le point de vue et l'usage visé peuvent-ils être explicites sans confondre auteur d'une affirmation et autorité décisionnelle ? |
| Identité et périmètre du modèle | identité/révision d'artefact, applicabilité, spécification | Un modèle peut-il déclarer version, périmètre, exclusions, environnement et contexte d'usage ? |
| Hypothèses et incertitude | modèle d'assurance, affirmations/arguments, risque | Hypothèses, inconnues, type d'incertitude et limites acceptées peuvent-ils être représentés distinctement ? |
| Validité du modèle | méthode de vérification, preuve, affirmation d'assurance | La cohérence formelle peut-elle être distinguée de l'adéquation empirique/pragmatique ? |
| Pluralité des modèles | modèles par préoccupation, artefacts liés, applicabilité | Plusieurs modèles peuvent-ils traiter différents aspects sans unification forcée ? |
| Évolution et rétroaction | cycle de changement, fraîcheur des preuves, applicabilité des révisions | Les changements de modèles peuvent-ils invalider ou imposer la revue des preuves et décisions dépendantes ? |
| Irréductibilité | concepts de risque/hypothèse/limitation/exception | Les éléments irréductibles peuvent-ils être enregistrés sans créer un vague « score de complexité » ? |
| Délibération et légitimité | autorité, revue, décision, argument | GovCheck peut-il préserver qui a participé, qui a décidé et sous quel mandat ? |

## Proposition de texte explicatif destiné aux utilisateurs

> GovCheck vise les projets qui ont besoin d'une gouvernance explicite et traçable des changements de dépôt, exigences, décisions, modèles et preuves d'assurance. Il peut aider à rendre visibles les hypothèses, frontières des modèles, responsabilités et risques non résolus. Il ne remplace ni expertise métier, ni délibération des parties prenantes, ni validation empirique, ni outils spécialisés de modélisation des systèmes. La vérification formelle peut établir des propriétés d'un modèle défini sous des hypothèses déclarées ; elle ne prouve pas à elle seule que ce modèle représente intégralement le système réel. Selon le projet, GovCheck peut donc constituer une couche centrale de gouvernance, un complément utile à d'autres méthodes ou une solution insuffisante lorsqu'elle est utilisée seule.

Cette formulation est uniquement une proposition issue de la recherche. Elle devra être confrontée au périmètre produit implémenté avant toute publication comme documentation produit.

## Questions pour une décision ultérieure

1. Le point de vue/finalité/contexte doit-il être un concept de premier rang, ou peut-il être représenté par les métadonnées et relations existantes ?
2. Quelles informations minimales sont nécessaires pour déclarer le contexte de validité d'un modèle ?
3. Comment l'évolution d'un modèle doit-elle affecter la fraîcheur des preuves et les décisions antérieures ?
4. GovCheck doit-il prendre en charge des liens vers des modèles systémiques externes, plutôt que devenir lui-même un environnement de modélisation systémique ?
5. Comment distinguer incertitude épistémique, incertitude stochastique, limites computationnelles, dépendances inconnues et absence de contrôlabilité ?
6. Quelles preuves suffisent à affirmer qu'un modèle est adapté à une décision particulière ?
7. Quels mécanismes garantissent que plusieurs perspectives de parties prenantes restent visibles sans rendre toutes les affirmations contradictoires également autorisées ?

## Statut décisionnel

Aucune décision n'est prise ici. Aucune issue ni tâche d'implémentation n'est créée par cette recherche seule. Les décisions futures devront citer STUDY-003 et les entrées exactes du catalogue utilisées, recensées dans le [dossier source](le-moigne-colloquium.fr.md), consigner les contre-arguments et identifier l'autorité décisionnelle compétente.

## Catalogue central des références

Voir [R-176](../references.fr.md#r-176), [R-178](../references.fr.md#r-178), [R-180](../references.fr.md#r-180) et [R-182](../references.fr.md#r-182).
