# Décision et risque assumé comme dimensions transversales de la gouvernance

**Statut :** clarification de recherche pour les issues [#73](https://github.com/Martin-PB/govcheck/issues/73) et [#131](https://github.com/Martin-PB/govcheck/issues/131) ; ni métamodèle ni décision d'architecture adoptés. **Date :** 2026-11-13.

## 1. Correction : le chemin de traçabilité n'est pas une chaîne de cycle de vie qui se termine par une décision

La séquence

`Intention → Exigence → Propriété → Modèle → Implémentation → Vérification de conformité → Assurance`

peut constituer un chemin de traçabilité utile. Ce n'est ni un cycle de vie universel strictement linéaire, ni une séquence qui devrait se terminer par `Décision`.

La structure sémantique de GovCheck est un graphe typé, plusieurs-à-plusieurs et évolutif. Ses nœuds et relations peuvent être créés, révisés, contestés, invalidés, remplacés ou laissés sans résolution. Les exigences et décisions peuvent aussi provenir du droit, de normes, de contrats, de besoins des parties prenantes, de contraintes d'architecture, d'observations opérationnelles, de défauts, d'incidents, de menaces, d'obligations d'interopérabilité et d'autres sources — pas uniquement d'une intention initiale.

La décision est un objet de gouvernance transversal de premier rang. Elle peut intervenir à n'importe quel endroit du graphe : établir ou réviser une intention ; sélectionner, raffiner ou rejeter des exigences ; choisir des propriétés ou des modèles ; autoriser, contraindre ou rejeter une implémentation ; accepter ou rejeter des résultats de vérification ; accepter, qualifier ou refuser un argument d'assurance ; autoriser une publication ou un déploiement ; suspendre, révoquer ou déclencher une réévaluation. Les décisions peuvent également gouverner les relations entre artefacts, pas seulement les artefacts eux-mêmes.

Le graphe doit donc représenter le contexte de décision, l'autorité, la portée, la justification, les alternatives, les conditions, les conséquences, la date d'effet, la révision de gouvernance applicable, la provenance et les conditions de réexamen/révocation. Une décision n'est pas synonyme d'approbation ou de succès : elle peut consigner un désaccord, une contradiction non résolue, un report, un rejet, une acceptation conditionnelle ou une acceptation explicite du risque.

## 2. L'assurance n'est pas une décision, et une décision n'est pas une preuve

Distinguer :

- **Éléments probants/assurance :** ce qui est étayé, par quelle méthode, relativement à quelle affirmation, sous quelles hypothèses et limites.
- **Décision :** ce qu'un acteur autorisé choisit ou s'engage à faire dans un contexte déclaré.
- **Autorité :** pourquoi cet acteur est habilité à prendre cette décision, pour cette portée et cette période.
- **Acceptation du risque :** engagement autorisé concernant l'exposition et les conséquences qui subsistent ; elle n'efface pas le risque et ne renforce pas les éléments probants.

Une décision peut s'appuyer sur une assurance forte et néanmoins accepter un risque résiduel. Elle peut aussi conduire à poursuivre malgré une assurance incomplète, mais les éléments manquants, hypothèses, désaccords, incertitudes et expositions acceptées doivent rester explicites. Une autorisation ne peut transformer un test en preuve de théorème, un résultat de model checking en conformité de l'implémentation, ni une hypothèse non étayée en connaissance.

Une décision peut modifier l'objet même qui fait l'objet de l'assurance. Ce changement peut invalider des modèles, éléments probants, mappings, approbations ou décisions antérieures ; ces dépendances et obligations de réévaluation doivent être explicites et situées dans le temps.

## 3. Le risque et le risque assumé sont des objets de premier rang

Ne pas représenter le risque par un booléen tel que `accepted_risk: true`, une simple note libre ou un score numérique universel. Distinguer au minimum :

1. Un scénario de risque ou résultat défavorable incertain.
2. Les conséquences et objectifs/actifs/parties prenantes affectés.
3. Les observations, expériences, éléments probants et provenance des sources.
4. Les hypothèses, inconnues, désaccords et limites du modèle.
5. La méthode d'analyse/évaluation du risque et son domaine d'applicabilité.
6. Les estimations quantitatives ou qualitatives, avec leur sémantique et leur incertitude.
7. Les options de traitement, contrôles, mesures d'atténuation et exposition résiduelle.
8. Une décision qui accepte, rejette, transfère, tolère, atténue ou reporte cette exposition.
9. L'autorité, la portée, la justification, les conditions, la période de validité, les déclencheurs de réexamen et les règles de révocation/expiration de cette décision.

L'objet risque et son évaluation doivent avoir une identité et une version propres. Une décision référence la révision exacte de l'évaluation du risque qu'elle a prise en compte. Une réévaluation peut produire une nouvelle évaluation sans réécrire le fondement historique d'une décision antérieure.

PEAK signifie **Problem, Experience, Assumptions, Knowledge**. Ces quatre entrées alimentent un processus de décision qui produit deux résultats distincts : la **solution** et le **risque assumé** (ce qui pourrait ne pas fonctionner comme prévu). Le risque assumé n'est pas un ajout facultatif ni seulement le risque résiduel après les contrôles ; il fait partie du dossier de décision dès le départ. Les quatre entrées et les deux résultats doivent rester consultables séparément :

| Élément PEAK | Rôle dans le dossier de décision |
|---|---|
| Problem | Le problème à résoudre, y compris exigences et contraintes |
| Experience | L'expérience antérieure pertinente et son applicabilité |
| Assumptions | Ce qui est tenu pour vrai sans éléments probants suffisants, et ce qui est délibérément exclu de l'examen |
| Knowledge | Les faits et connaissances contextuelles réellement disponibles au moment de la décision |
| Solution | La réponse/l'approche choisie |
| Assumed Risk | Ce qui pourrait ne pas fonctionner comme prévu, y compris l'exposition que le décideur accepte consciemment de prendre |

Ne pas confondre trois notions : le **risque assumé PEAK** (second résultat explicite du processus de décision), l'**évaluation du risque** (analyse distincte pouvant estimer vraisemblances, conséquences et incertitudes) et l'**acceptation du risque** (disposition autorisée concernant l'exposition). Le **risque résiduel** constitue encore une autre notion : l'exposition qui subsiste après des traitements ou contrôles spécifiés. Un risque assumé PEAK peut ne pas être quantifié, ne pas encore avoir été atténué et faire ultérieurement l'objet d'une évaluation ou d'un traitement. Le dossier de décision doit préserver le risque assumé initial même lorsque des évaluations ou contrôles ultérieurs le modifient. PEAK aide donc à structurer le problème, l'expérience, les hypothèses et les connaissances, tout en exigeant que le décideur explicite à la fois son choix et ce qui pourrait échouer. Il ne doit pas être fusionné artificiellement avec SACM, la modélisation des menaces ou le métamodèle GovCheck dans son ensemble. PEAK apporte une perspective de raisonnement sur les décisions et risques ; SACM apporte une perspective de dossier d'assurance ; aucun des deux ne fournit à lui seul l'autorité de gouvernance.

## 4. Préserver les distinctions mathématiques et épistémiques

Le métamodèle ne doit pas fusionner :

- **Vérité ou satisfaction classique/formelle :** relativement à un langage, une sémantique, un modèle et des hypothèses déclarés.
- **Probabilité :** incertitude portant sur des événements, résultats ou paramètres, avec une interprétation explicitée.
- **Appartenance floue :** degré d'appartenance d'un objet à un concept vague ; un degré d'appartenance de 0,8 n'est pas une probabilité de 80 %.
- **Non-déterminisme :** ensemble de transitions ou de choix possibles sans distribution probabiliste implicite.
- **Taux de transition :** taux dépendant du temps, pas une probabilité pour un intervalle non spécifié.
- **Coût, récompense/utilité, priorité, préférence et fréquence empirique :** grandeurs typées de significations et d'unités différentes.
- **Confiance dans un argument :** jugement épistémique/d'évaluation dont la sémantique et la méthode doivent être déclarées ; ce n'est automatiquement ni une probabilité ni une force de preuve.
- **Inconnu ou non quantifiable :** absence de connaissance justifiée ; ne jamais convertir silencieusement en zéro, valeur médiane, succès ou score.

Pour les évaluations probabilistes, préserver l'événement, les hypothèses conditionnelles, la population, l'horizon temporel, la provenance des données et paramètres, la méthode d'estimation, les dépendances, la distribution/l'intervalle, la sensibilité et la validité. Pour les évaluations floues, préserver le concept linguistique, la fonction d'appartenance, la base de règles, les jugements experts et leur validation. Dans les deux cas, conserver ce que la méthode n'établit pas.

Une formule telle que probabilité × impact peut être utile dans une méthode et une échelle de risque données, mais elle n'est pas une définition universelle du risque. Toute agrégation entre unités, scénarios, incertitudes ou jugements de valeur différents exige un modèle de décision explicite et justifié ; GovCheck ne doit pas en inventer un.

## 5. Conséquences pour le graphe sémantique et les contrats formels

Relations candidates :

- `informsDecision`, `justifiesDecision`, `authorizesDecision`, `constrainsDecision`, `supersedesDecision`, `revokesDecision` ;
- `identifiesRisk`, `evaluatesRisk`, `treatsRisk`, `acceptsRisk`, `reassessesRisk` ;
- `supports`, `challenges`, `assumes`, `dependsOn`, `invalidates`, `isApplicableUnder`.

Ces noms sont illustratifs, pas un vocabulaire adopté. Chaque relation exige une signature typée, une direction, une sémantique, des cardinalités, une provenance, des exigences d'autorité, une portée et une validité temporelle. Le graphe peut contenir des cycles lorsqu'ils sont justifiés ; aucune contrainte générale d'acyclicité n'est impliquée.

## 5.1 Frontières candidates entre objets typés

La séparation suivante constitue un contrat de modélisation candidat, pas une sérialisation choisie ni une hiérarchie finale de classes :

| Objet candidat | Responsabilité | À ne pas confondre avec |
|---|---|---|
| `DecisionRecord` | Identité/révision, type/statut de décision, contexte, autorité, portée, justification, alternatives, conditions, positions d'effet/expiration, provenance et remplacement/révocation | Une approbation de PR, un résultat CI ou un booléen sans qualification |
| `DecisionInputs` | Entrées PEAK Problem, Experience, Assumptions et Knowledge, chacune avec source et contexte temporel | Un score de confiance indifférencié |
| `DecisionSolution` | Réponse choisie et alternatives/contraintes retenues | Une preuve que la solution fonctionne |
| `AssumedRisk` | Énoncé PEAK explicite de ce qui pourrait ne pas fonctionner comme prévu | Une probabilité quantifiée, un risque résiduel ou une acceptation formelle du risque |
| `RiskScenario` | Événement/état défavorable incertain, description causale/contextuelle et conséquences | L'estimation de sa vraisemblance |
| `RiskAssessment` | Analyse d'un scénario selon une méthode, avec modèle, hypothèses, données, paramètres, horizon, résultats et limites | Le scénario lui-même ou l'autorité de l'accepter |
| `RiskTreatment` | Évitement, réduction, transfert/partage, surveillance, contingence et exposition résiduelle résultante | Un enregistrement de décision, sauf s'il porte l'autorité et la justification requises |
| `RiskAcceptance` | Disposition autorisée, circonscrite et limitée dans le temps concernant une exposition spécifiée, liée aux révisions exactes de l'évaluation et de la politique | Une preuve que le risque est absent ou acceptable dans tout contexte |

Un enregistrement de décision peut référencer zéro ou plusieurs hypothèses, éléments de connaissance, alternatives, solutions et énoncés de risque assumé. Un énoncé de risque assumé peut concerner plusieurs scénarios ; un scénario peut être évalué par plusieurs méthodes ou dans plusieurs contextes. Ces cardinalités doivent être justifiées par les cas d'usage, pas fixées prématurément.

La chaîne d'identité essentielle n'est pas un pipeline linéaire unique. C'est un ensemble de références typées :

- décision → entrées exactes et révisions sources ;
- décision → solution choisie et résultats explicites de risque assumé ;
- scénario de risque → une ou plusieurs évaluations ;
- évaluation → révisions exactes du modèle, des données, paramètres, hypothèses et méthode/outil ;
- traitement → révisions du scénario et de l'évaluation auxquelles il répond ;
- acceptation → exposition résiduelle exacte, autorité, révision de politique, portée et intervalle de validité ;
- observation/réévaluation ultérieure → décision/évaluation antérieure qu'elle conteste ou dont elle déclenche le réexamen.

Une sortie de risque assumé PEAK peut exister avant toute analyse quantitative. Une évaluation probabiliste ou floue ultérieure enrichit le dossier mais ne doit pas écraser ce qui avait été assumé initialement. Une acceptation du risque peut viser une exposition résiduelle après traitement ; c'est un acte autorisé distinct.

### Exemples négatifs que le modèle doit rejeter

- Traiter une appartenance floue de 0,8 comme une probabilité d'événement de 80 %.
- Traiter une estimation probabiliste absente comme une probabilité nulle.
- Traiter un taux de transition comme une probabilité sans intervalle temporel ni sémantique de conversion.
- Traiter une transition non déterministe non pondérée comme équiprobable.
- Traiter un score de confiance expert comme une preuve de théorème ou une probabilité calibrée sans interprétation justifiée.
- Traiter un risque assumé PEAK enregistré comme s'il avait déjà été évalué ou formellement accepté.
- Traiter l'acceptation d'un risque comme un élément prouvant que le scénario ne peut pas se produire.
- Réutiliser une acceptation expirée/révoquée après modification de sa portée, de la politique, de l'évaluation ou des hypothèses.

Obligations formelles candidates, selon pertinence :

- une décision ne peut acquérir autorité, portée ou durée par un mapping sémantique ;
- l'acceptation du risque ne peut impliquer que le risque est absent, le scénario impossible ou l'estimation prouvée ;
- probabilité, appartenance floue, non-déterminisme, taux, coûts et confiance ne peuvent être échangés par une conversion non typée ;
- une évaluation ou décision est liée aux révisions exactes de son modèle, paramètres, éléments probants, hypothèses et politique gouvernante ;
- les changements de ces dépendances invalident ou déclenchent le réexamen des évaluations et décisions concernées selon des règles déclarées ;
- la justification historique d'une décision et l'exposition acceptée restent consultables après remplacement, expiration ou révocation.

Ce sont des obligations candidates à préciser dans #73 et #131, pas des affirmations selon lesquelles le code GovCheck actuel les impose déjà.

## 6. Recherche et références existantes

Cet addendum précise sans la remplacer la [recherche sur l'assurance sémantique et les modèles de transition](semantic-assurance-and-transition-models-2026-11.fr.md). Préserver notamment la distinction qui y est déjà documentée entre probabilité, appartenance floue, non-déterminisme, taux de transition, coûts et récompenses. Voir le catalogue [R-193](../references.fr.md#r-193) pour les sources sur les modèles probabilistes, flous et de transition, et [R-74](../references.fr.md#r-74) pour la source du modèle de décision PEAK.

## 7. Statut et frontières

Ce document est une clarification de recherche. Il n'adopte ni sérialisation canonique, ni calcul universel du risque, ni moteur probabiliste/flou, ni PEAK, ni SACM, ni modèle de décision particulier, ni métamodèle GovCheck normatif. Il ne modifie pas le régime d'autorité actuel. Les propositions doivent être spécifiées, confrontées aux sémantiques sources et soumises au processus de gouvernance du dépôt avant toute adoption normative.
