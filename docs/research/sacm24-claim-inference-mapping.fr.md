# SACM 2.4 Beta 1 — première tranche de mapping sémantique

**Statut :** tranche sémantique source formalisée en Lean ; compilation Lean et audit des axiomes réussis dans [l'exécution 43214838388](https://github.com/Martin-PB/govcheck/actions/runs/43214838388).  
**Référence source :** OMG SACM 2.4 Beta 1, septembre 2026 ; XML normatif du métamodèle daté du 04/05/2026.  
**Catalogue :** [R-73](../references.fr.md#r-73).  
**Formalisation :** [GovCheckCoherence.SACM24](../../formal/lean/GovCheckCoherence/SACM24.lean).

## 1. Pourquoi cette tranche source en premier

SACM 2.4 Beta 1 introduit des sémantiques directement pertinentes pour le modèle épistémique de GovCheck :

- un sujet explicite pour un Claim (issue SACM24-83) ;
- des valeurs étendues de AssertionDeclarationKind et des structures de valeur d'assertion ;
- des valeurs plus riches pour InferenceTypeKind : probable, collective, necessary, sufficient, necessaryAndSufficient et byRule ;
- des points d'extension AssertionRule et InferenceRule pour des sémantiques définies par l'utilisateur ;
- des constructions liées à l'évaluation (issue SACM24-75) et aux arguments avancés (issue SACM24-77).

SACM constitue donc une bonne cible de réfutation : un mapping GovCheck doit préserver les distinctions présentes dans SACM, au lieu d'aplatir tout le contenu des assertions et inférences en un lien générique affirmation/élément probant.

## 2. Une déclaration d'assertion n'est ni un statut d'élément probant ni une preuve de théorème

La tranche Lean modélise les littéraux de AssertionDeclarationKind de SACM :

| Déclaration SACM | Disposition GovCheck | Ce que cela **ne** signifie **pas** |
|---|---|---|
| `asserted` | `asserted` | Ni un test réussi ni une preuve |
| `assumed` | `assumed` | Pas un élément probant de vérité de la proposition |
| `axiomatic` | `axiomaticDeclared` | Pas une preuve de théorème vérifiée par le noyau Lean |
| `byRule` | `ruleDeclared` | Pas validé tant que la règle référencée n'est pas interprétée et vérifiée |

Le mapping est injectif : aucun littéral de déclaration SACM n'est fusionné avec un autre dans une disposition GovCheck.

Les champs optionnels SACM `isTrue`, `assertionValue` et `assertionRule` restent distincts du type de déclaration. Dans la tranche Lean actuelle, les deux derniers sont conservés comme chaînes opaques de contenu/référence source, sans formaliser encore leurs métaclasses SACM complètes. Une valeur booléenne de vérité facultative n'est pas un objet de preuve ; une valeur d'assertion peut être plus riche qu'un booléen ; une référence de règle n'est pas sa sémantique formelle. L'enregistrement Lean conserve ces champs séparément.

**Règle critique de non-promotion :** `axiomatic` dans SACM doit rester un axiome/hypothèse explicitement déclaré par la source dans le registre de confiance. Il ne peut pas être promu en `theoremProof` GovCheck sans terme de preuve Lean indépendant et audit séparé de la base de confiance/des axiomes.

## 3. Sujet du Claim et interprétation formelle

La tranche Lean définit un `SACMElementRef` contenant l'identité source, la métaclasse et la révision du modèle. `SACMClaimInterpretation` lie :

- l'identité exacte du Claim SACM à l'identifiant d'affirmation GovCheck ;
- le sujet SACM explicite facultatif au sujet traduit ;
- la référence du sujet à la révision exacte du modèle source ;
- une proposition Lean fournie séparément comme interprétation formelle.

Il ne s'agit volontairement pas d'une conversion automatique du texte/de la valeur SACM en logique Lean. L'autorité de mapping doit fournir et justifier l'interprétation propositionnelle. Le contrat formel actuel contrôle la préservation de l'identité et du sujet/de la révision, mais ne prouve pas qu'une proposition choisie pour une affirmation en langage naturel est fidèle à son texte. Cela reste un argument d'interprétation et une obligation d'assurance explicites.

## 4. Types d'inférence et directionnalité

Le modèle Lean formalise le fragment déterministe avec sa direction explicite :

| SACM InferenceTypeKind | Liaison formelle | Interprétation |
|---|---|---|
| `sufficient` | `AllPremises premises → conclusion` | Les prémisses conjointes suffisent à la conclusion |
| `necessary` | `conclusion → premise` | La prémisse source est nécessaire à la conclusion |
| `necessaryAndSufficient` | `premise ↔ conclusion` | Les deux directions sont vraies |
| `collective` | `AllPremises premises ↔ conclusion` avec un ensemble de prémisses non vide | L'ensemble des prémisses est conjointement nécessaire et suffisant |
| `byRule` | Identité de règle explicite et terme de preuve | Nécessite une règle formelle interprétée séparément |
| `probable` | Aucun constructeur de liaison classique | Nécessite une sémantique probabiliste ; non pris en charge par ce fragment classique |

Cela évite une erreur de direction fréquente : une inférence SACM nécessaire n'est pas la même implication qu'une inférence suffisante. Le type Lean indexe chaque liaison par le type d'inférence SACM, ce qui empêche d'inverser silencieusement la direction.

Le cas `probable` ne reçoit volontairement aucun constructeur d'implication classique. Il faut fournir un modèle probabiliste, un espace/une mesure de probabilité, les hypothèses de conditionnement et l'interprétation de la force probabiliste SACM avant de formaliser une liaison probabiliste. Assimiler `probable` à une implication ordinaire serait incorrect.

## 5. Ce qui a été vérifié par le noyau

La bibliothèque Lean de cohérence existante importe désormais `GovCheckCoherence.SACM24`. Le rapport d'axiomes inclut des déclarations de théorèmes concernant :

- l'injectivité du mapping des déclarations d'assertion SACM ;
- l'absence de liaison classique pour une inférence probable ;
- la bonne direction des inférences nécessaires et suffisantes ;
- l'équivalence conjointe de l'inférence collective ;
- la préservation de l'identité du Claim et du sujet explicite SACM ;
- l'épinglage de la référence du sujet à la révision exacte du modèle.

L'exécution de compilation/audit des axiomes pour cette extension est en attente. Aucun résultat n'est revendiqué avant la fin de la CI sur le commit contenant ces déclarations.

## 6. Limites et prochaine étape du mapping

Il s'agit d'une petite tranche SACM 2.4, pas d'une conformité SACM complète. Elle ne formalise pas encore tous les constructs Argument, Artifact, Terminology, Package, View, Diagram, Assessment, Strength, AssertionRule ou InferenceRule ; elle ne prouve pas non plus un import/export XML/XMI sans perte.

Suite :
1. lier une vraie fixture XMI/XML SACM 2.4 Beta 1 à la représentation formelle `SACMClaim` et `SACMAssertion` ;
2. lier une relation `AssertedInference` et une relation `AssertedEvidence`, en préservant les identités source/cible et `isCounter` ;
3. ajouter l'identité source explicite des `AssertionRule`/`InferenceRule` et la liaison aux dépendances de preuve ;
4. ajouter une sémantique probabiliste sans la convertir en implication classique ;
5. tester explicitement les métaclasses non prises en charge et les pertes aller-retour.

L'objectif est de prouver d'abord une petite loi de mapping intermodèle réelle, puis de généraliser par métaclasse et association avec des déclarations de couverture — pas de prétendre que l'intégralité du métamodèle SACM est déjà formalisée.
