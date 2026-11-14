# 0026 — Capacité d'assurance conforme à SACM 2.4 et intégration dans GovCheck

**Statut :** proposition d'architecture soumise à revue. Elle fixe une cible de couverture sémantique et de conformité ; elle ne prétend pas qu'un parseur, un sérialiseur, un évaluateur ou une implémentation SACM 2.4 existe déjà ni qu'une conformité formelle ait été démontrée.  
**Langue :** l'anglais est la version par défaut ; voir la [version anglaise](0026-sacm-24-conformance-and-govcheck-integration.md).

## 1. Décision à examiner

GovCheck devrait pouvoir représenter, préserver, valider et exploiter l'intégralité de la sémantique des dossiers d'assurance définie par la spécification SACM 2.4 Beta 1 épinglée, y compris son métamodèle normatif et les constructions complémentaires explicitement identifiées comme non normatives.

Il s'agit d'un objectif plus fort qu'un adaptateur d'import/export avec pertes. La cible est une **capacité d'assurance de GovCheck conforme à SACM** : chaque concept, relation, multiplicité, contrainte, énumération, règle de paquetage et construction de vue/diagramme prise en charge par SACM doit disposer d'une représentation fidèle dans GovCheck. GovCheck doit également pouvoir exprimer ses propres concepts de gouvernance des dépôts et les relier à SACM sans les forcer dans des classes SACM dont le sens serait différent.

SACM 2.4 Beta 1 a été adoptée comme spécification OMG en cours en septembre 2026 ; SACM 2.3 demeure la version formelle à la date du présent document. La bêta constitue donc une cible de conception épinglée, et non l'affirmation que la version finale 2.4 serait déjà formelle. Le PDF normatif et le métamodèle lisible par machine sont publiés depuis le [catalogue de la spécification SACM de l'OMG](https://www.omg.org/spec/SACM). L'historique des changements 2.4 est disponible dans le [suivi des tickets OMG](https://issues.omg.org/issues/spec/SACM?view=CLOSED).

## 2. Positionnement architectural dans GovCheck

SACM est un métamodèle métier pour les dossiers d'assurance structurés. GovCheck est le système de gouvernance d'un dépôt logiciel pendant tout son cycle de vie. Ces périmètres sont liés, mais ne sont pas interchangeables.

La composition proposée est la suivante :

1. **Fondations canoniques de gouvernance GovCheck** — identité du projet, autorité, objectifs, exigences, règles normatives, applicabilité, profils, cycle de vie, changements, approbations, exceptions, provenance, identité des artefacts et projections contrôlées.
2. **Capacité d'assurance conforme à SACM** — sous-modèle sémantique fidèle aux paquets Foundation, Argumentation, Artifact, Terminology, Packaging et aux constructions View/Diagram applicables, y compris les ajouts de la Beta 1.
3. **Capacités métier GovCheck** — exigences, architecture, implémentation, maintenabilité, tests, méthodes formelles, dépendances, documentation, sécurité, vie privée, sûreté, build/publication, exploitation et maintenance. Chaque capacité peut produire ou consommer des éléments d'assurance sans être réduite à un dossier d'assurance.
4. **Relations intermodèles** — liens explicites, typés et versionnés entre les concepts GovCheck et les éléments SACM.

Le modèle canonique GovCheck reste responsable de la gouvernance du dépôt et de l'autorité. La capacité SACM est responsable de la sémantique d'un dossier d'assurance représenté en SACM. Aucun ne remplace l'autre.

Il ne faut pas faire de chaque artefact GovCheck un Artifact SACM, de chaque exigence un Claim SACM, de chaque constat un Assessment, ni de chaque décision un Argument. Le mapping n'est valide que lorsque les significations correspondent réellement ; sinon, il faut créer une relation explicite ou une extension GovCheck dont la sémantique est déclarée.

## 3. Exigence de couverture : aucune réduction sémantique silencieuse

La cible de conformité est l'intégralité du métamodèle SACM 2.4 Beta 1 épinglé, et non un sous-ensemble choisi arbitrairement. L'inventaire d'implémentation doit être dérivé directement du métamodèle lisible par machine et de la spécification normative OMG, et non de ce seul résumé.

L'audit de couverture doit au minimum prendre en compte :

### 3.1 Foundation et sémantique commune de modélisation

- identité des modèles et éléments SACM, propriété, containment, espace de noms et appartenance aux paquets ;
- classes de base communes, caractère abstrait, héritage et redéfinitions ;
- extrémités d'associations, direction, propriété, multiplicités, ordre, unicité, sous-ensembles et unions ;
- contraintes et sémantique de leur évaluation/validation ;
- noms, valeurs, commentaires, contraintes, références externes et expressions tenant compte des langues ;
- identité du modèle et organisation au niveau du modèle.

Le travail Foundation et d'alignement MOF de SACM 2.4 est déterminant : l'implémentation doit préserver la sémantique réelle des associations et de la propriété, pas seulement sérialiser des noms de classes et des arêtes.

### 3.2 Argumentation

Représenter intégralement le paquet normatif Argumentation, notamment les constructions SACM de claim/assertion, argument, reasoning, inference, evidence, context, relationship, citation/abstraction, defeater et les autres éléments exactement comme les définit le métamodèle épinglé.

Préserver :
- les relations asserted et inferred et leur direction/sémantique exacte ;
- les sujets des claims et le mécanisme de sujet explicite introduit en 2.4 ;
- le contexte des arguments et les éléments complémentaires non normatifs correspondants ;
- les noms et valeurs des raisonnements lorsqu'ils peuvent être distincts ;
- les types d'inférence et la logique/notation déclarées ;
- les defeaters, mécanismes/règles de réfutation et objections non résolues ;
- les références de preuve et de contexte et la sémantique de leurs relations ;
- les descripteurs d'argumentation avancée, dont force, valeurs de vérité et indécidabilité, tout en conservant leur statut non normatif lorsqu'il est spécifié ainsi.

Il ne faut pas remplacer la sémantique argumentative SACM par le graphe de claims conjonctif simplifié actuellement utilisé par GovCheck 0021. L'évaluateur GovCheck peut imposer une politique d'acceptation particulière, mais le modèle d'assurance sous-jacent doit préserver le graphe et la logique SACM plus riches sans perte.

### 3.3 Artifact

Représenter le paquet Artifact dans son intégralité ainsi que ses constructions de cycle de vie et de provenance, notamment les artefacts, références d'artefacts, événements, activités, techniques, participants, ressources et relations Artifact-Asset, conformément à la spécification.

Préserver les cibles exactes des références externes et internes, les emplacements pertinents dans les artefacts externes, les dates et informations temporelles, les relations entre artefacts ainsi que la distinction entre un artefact et une affirmation/preuve à son sujet.

Un fichier du dépôt, une révision Git/Pijul, une exécution de test, un objet de preuve, un build, une publication, une dépendance, un composant déployé ou une observation peut être référencé comme sujet GovCheck. Il ne faut pas le forcer dans une sous-classe Artifact si sa sémantique ne correspond pas. Un binding typé relie son identité stable GovCheck et son identité de révision/instance immuable à la référence SACM correspondante.

### 3.4 Terminology

Représenter les assets terminologiques, catégories, termes, définitions, relations et valeurs multilingues. Préserver les balises de langue et les valeurs d'expression structurées. Le vocabulaire propre à GovCheck et les glossaires métier peuvent être reliés aux éléments terminologiques SACM, sans les redéfinir silencieusement.

### 3.5 Packaging, modularité et réutilisation

Préserver l'identité des modèles/paquets SACM, les types de paquets, la propriété, les imports/dépendances, interfaces et bindings ainsi que toutes les contraintes de paquetage de la version 2.4. Le refactoring des paquets et la suppression/le renommage des constructions 2.3 doivent être reflétés exactement ; il ne faut pas conserver les anciennes sémantiques de paquetage 2.3 comme si elles étaient celles de 2.4.

### 3.6 Assessments, joins, arguments avancés, vues et diagrammes

La bêta 2.4 comprend des constructions et tickets complémentaires concernant :
- **Assessment**, avec notamment identité d'évaluation, évaluations imbriquées, règles et lacunes ;
- **Join**, avec type/règle de combinaison déclaré et sémantique de sélection des sources ;
- **argumentation avancée**, notamment forces d'argument, types d'inférence, valeurs de vérité et indécidabilité ;
- **vues et diagrammes SACM**, notamment structures de diagrammes/éléments de diagramme et informations visuelles.

Les dispositions des tickets OMG identifient certaines de ces constructions comme des éléments complémentaires non normatifs. En particulier, SACM24-105 met à jour la clause de conformité pour inclure le paquetage, les vues/diagrammes et les joins, assessments et arguments avancés non normatifs. GovCheck doit préserver leurs métadonnées de statut et ne doit pas les promouvoir silencieusement en exigences normatives ou en obligations normatives du métamodèle. Lorsque la clause de conformité distingue les éléments normatifs et non normatifs, GovCheck doit implémenter et rapporter ces points de conformité séparément.

La liste des tickets de la bêta fournit une checklist utile pour l'implémentation (les identifiants sont des liens stables dans le [registre des tickets OMG clos](https://issues.omg.org/issues/spec/SACM?view=CLOSED)) :

| Sujet de la bêta | Ticket OMG | Conséquence pour la couverture GovCheck |
|---|---|---|
| Paquet Foundation et concepts de base réutilisables | SACM24-5, SACM24-36 | Préserver la couche Foundation et ses sémantiques d'alignement/incorporation. |
| Alignement MOF et extrémités/multiplicités explicites | SACM24-55, SACM24-59 | Valider propriété, direction, multiplicité, redéfinition, sous-ensemble et espace de noms. |
| Structure et sémantique des packages | SACM24-56, SACM24-18, SACM24-11 | Implémenter le modèle 2.4 ; ne pas conserver les anciennes structures 2.3 comme équivalentes. |
| Sujet explicite des claims | SACM24-83 | Préserver le sujet des claims, y compris les références à des éléments SACM. |
| Contexte de l'argument | SACM24-81 | Préserver les constructions de contexte argumentatif et leur statut non normatif. |
| Concepts d'argumentation avancée | SACM24-77 | Préserver force, type d'inférence, valeur de vérité et indécidabilité. |
| Assessment et assessments imbriqués | SACM24-75 | Préserver identité, règles, lacunes et sous-évaluations. |
| Sémantique des joins | SACM24-76 | Préserver type de jointure, règle et sémantique de sélection des sources. |
| NamedValue typé | SACM24-80 | Préserver les types de valeurs scalaires/structurées sans les aplatir en chaînes. |
| Vues SACM | SACM24-78 | Préserver les vues et leurs liens vers les éléments du modèle sous-jacent. |
| Relations entre artefacts | SACM24-82 | Préserver les cibles et sémantiques précises des relations. |
| Types de déclaration des claims et suppression d'anciennes relations | SACM24-12, SACM24-15 | Préserver exactement le modèle 2.4 des types de déclaration et des relations ; ne pas émuler les constructions 2.3 supprimées. |
| Identité du modèle et changements d'identité | SACM24-17, SACM24-41 | Préserver l'identité du modèle et la sémantique explicite de changement d'identité. |
| Groupement et refactoring des packages | SACM24-16, SACM24-11 | Préserver les règles 2.4 de groupement et de propriété des packages. |
| Références externes et sémantique des références d'artefacts | SACM24-10, SACM24-14 | Préserver les métadonnées de référence externe et la distinction exacte Artifact/ArtifactReference. |
| Valeurs multilingues et expressions | SACM24-6, SACM24-37 | Préserver les valeurs tenant compte des langues et la distinction entre nom d'élément et contenu. |
| Propriété des NamedValue et formes de valeurs supplémentaires | SACM24-72, SACM24-80 | Préserver propriété et valeurs typées sans les aplatir. |
| Sémantique date/heure et durée | SACM24-39, SACM24-79 | Préserver formats de date, sémantique d'occurrence, durée et unités de temps. |
| Complétude des claims/arguments et état de développement | SACM24-73, SACM24-74 | Préserver les constructions/états entirety et needs-development de la bêta tels qu'ils sont définis. |
| Clause de conformité et migration | SACM24-105, SACM24-98 | Séparer les points de conformité et implémenter le parcours de migration 2.3 vers 2.4 documenté. |

## 4. Contrat d'intégration GovCheck–SACM

L'intégration doit reposer sur des mappings explicites et des identités croisées stables, pas sur la similarité des noms de classes.

| Sujet GovCheck | Relation SACM | Règle d'intégration |
|---|---|---|
| Objectif, besoin d'une partie prenante, résultat du projet | Souvent contexte ou artefact référencé ; parfois sujet d'un claim | L'objectif reste l'objet canonique de gouvernance du projet ; le relier au contexte/sujet de claim SACM si cela se justifie. |
| Exigence, norme, obligation de politique | Peut être sujet de claim, contexte ou artefact référencé | Une exigence n'est pas automatiquement un claim. Préserver dans GovCheck sa force normative et son autorité. |
| Propriété, contrat, invariant, modèle | Généralement artefacts référencés et/ou sujets de claims | Préserver la révision exacte de la spécification/du modèle et le périmètre. |
| Source, configuration, build, test, preuve, publication, déploiement | Artifact/ArtifactReference/ArtifactAssetRelationship SACM selon le cas | Lier à l'ID d'artefact GovCheck stable et à la révision ou instance d'exécution immuable. |
| Observation, résultat de test, attestation, résultat de preuve | Peut être AssertedEvidence ou artefact référencé selon sa sémantique | Préserver producteur, méthode, provenance, périmètre, résultat, date, limites et dépendances d'invalidation dans GovCheck. |
| Affirmation et argument d'assurance | Mapping SACM direct | Préserver la structure et la logique SACM complètes. |
| Hypothèse, contexte, defeater, contre-preuve | Constructions SACM de contexte/argumentation lorsque la sémantique convient | Rendre explicites source, responsable, validité, incertitude et conditions de revue/réfutation. |
| Décision PEAK | Décision GovCheck liée, pas un remplacement SACM | Relier les dossiers d'assurance et éléments SACM pertinents ; ne pas modéliser PEAK comme un argument SACM par défaut. |
| Autorisation, approbation, exception, acceptation | Sémantique d'autorité/cycle de vie GovCheck | Les preuves et claims SACM peuvent éclairer la décision, mais ne confèrent pas eux-mêmes l'autorité sur le dépôt. |
| Changement de dépôt, candidat, état VCS | Sujet du cycle de vie GovCheck et artefact référencé SACM | Lier le dossier et ses évaluations au candidat et à la révision de gouvernance exacts. |

Chaque mapping doit déclarer : métaclasses source/cible ; cardinalité ; direction ; mapping d'identité ; préservation sémantique ; pertes autorisées (normalement aucune pour les constructions natives SACM) ; règles de validation ; versions applicables ; provenance.

## 5. Deux axes complémentaires d'identité et de version

GovCheck doit préserver simultanément :
- l'identité logique GovCheck stable, l'identité de révision/instance immuable et l'éventuelle version de contrat (Architecture 0017) ;
- l'identité du modèle/paquet/élément SACM et la version/profil exacts du métamodèle SACM.

Un élément SACM importé conserve son identifiant d'origine et l'identité de son modèle source. Un élément GovCheck qui lui est lié ne doit ni écraser ni usurper cette identité. Révisions, migrations, remplacements et références externes doivent être explicites.

La cible est un aller-retour sans perte pour la version SACM épinglée :
`modèle SACM → représentation GovCheck → modèle SACM`
doit préserver tout élément, relation, valeur, multiplicité, contrainte, paquet, vue/diagramme pris en charge et statut d'extension SACM natif, qu'il soit normatif ou complémentaire. L'ordre ou le formatage de sérialisation ne peut être canonisé que lorsque la spécification le permet ; le contenu sémantique et les identités stables restent inchangés.

Les futurs éléments SACM ou extensions inconnus doivent être préservés comme contenu opaque, typé et versionné, ou provoquer un résultat explicitement non pris en charge/indéterminé. Ils ne doivent jamais être supprimés silencieusement.

## 6. Relation avec les sémantiques d'assurance existantes de GovCheck

La spécification 0005 et l'architecture 0021 définissent déjà des contraintes importantes de GovCheck : liaison au sujet exact, méthode et périmètre, provenance, hypothèses, limites, fraîcheur des preuves, invalidation des dépendances, revue et discipline d'acceptation.

Elles restent valides. Toutefois, l'abstraction TLA+ initiale de l'architecture 0021 utilise actuellement un graphe fini acyclique de claims, une composition conjonctive des preuves et un vocabulaire de statuts limité. Elle exclut explicitement les stratégies argumentatives alternatives et d'autres constructions avancées. Cette abstraction n'est pas la représentation canonique de tous les arguments SACM.

Évolution requise :
1. conserver les responsabilités de 0021 relatives à la fraîcheur, la liaison au sujet, l'invalidation et la revue autorisée ;
2. remplacer l'hypothèse selon laquelle son graphe conjonctif serait le modèle complet de l'argumentation par une projection/politique d'évaluation sur la structure plus riche conforme à SACM ;
3. définir des sémantiques d'évaluation propres aux politiques pour AND/OR/XOR, les joins, defeaters, assessments, types d'inférence et forces, sans prétendre réduire toutes les logiques à un statut booléen unique ;
4. séparer la sémantique brute du modèle SACM de toute politique d'évaluation ou d'acceptation GovCheck ;
5. faire évoluer progressivement le modèle TLA+, en conservant des bornes explicites et en indiquant les constructions SACM abstraites ou hors périmètre de chaque modèle.

Un statut de claim est une évaluation gouvernée relativement à une politique, un sujet, un périmètre, une révision de modèle, des preuves et des hypothèses — pas une valeur de vérité intrinsèque fournie par SACM ou GovCheck.

## 7. Stratégie de conformité et de vérification

La conformité doit être démontrée ; elle ne découle pas du fait qu'un document JSON ressemble à SACM.

### 7.1 Conformité au métamodèle normatif

- Épingler le PDF OMG 2.4 Beta 1 exact, le métamodèle lisible par machine et les artefacts du profil UML par version et digest.
- Générer un inventaire complet des métaclasses/énumérations/associations/contraintes depuis le modèle normatif lisible par machine.
- Vérifier chaque classe, superclasse, propriété, extrémité d'association, multiplicité, contrainte d'ordre/unicité, sous-ensemble/redéfinition, littéral d'énumération, règle de paquetage et contrainte OCL.
- Vérifier les contraintes de modèle/paquet/interface/binding et les identifiants requis.
- Séparer les points de conformité normatifs des constructions complémentaires non normatives.

### 7.2 Sérialisation et aller-retour

- Importer des modèles SACM valides représentatifs et rejeter ou classer explicitement les modèles invalides.
- Exporter vers SACM les dossiers d'assurance natifs GovCheck lorsque le mapping est défini.
- Exiger un aller-retour sans perte pour toutes les constructions natives SACM.
- Préserver extensions inconnues, références externes, valeurs multilingues et métadonnées de vues/diagrammes.
- Tester la migration 2.3 vers 2.4 selon les indications de l'annexe G de l'OMG ; préserver la source originale et la provenance de migration.

### 7.3 Validation sémantique et multidomaine

- Tester que les liens GovCheck vers exigences, révisions de dépôt, exécutions de tests, objets de preuve et décisions ne modifient pas la sémantique SACM.
- Tester qu'une exigence ne devient pas automatiquement un claim, qu'un résultat de contrôle n'est pas automatiquement accepté comme preuve et qu'une évaluation d'assurance n'est pas une autorisation.
- Tester cycles argumentatifs, sémantiques d'inférence non prises en charge, defeaters, preuves contradictoires, contexte manquant, références périmées, sujets non résolus et modèles incomplets.
- Vérifier que la politique d'évaluation signale les cas non pris en charge ou indéterminés au lieu de les simplifier silencieusement.

### 7.4 Rapport de conformité

Un rapport de conformité doit identifier version/digests SACM exacts, révision du modèle/évaluateur GovCheck, métaclasses et contraintes couvertes, constructions exclues/non prises en charge, corpus de test, résultats d'aller-retour et de migration, écarts sémantiques connus et identités du réviseur/de l'autorité. Il ne doit pas déclarer « conforme à SACM » si une construction normative requise n'est pas implémentée ou est représentée avec perte.

## 8. Stratégie de version

- Traiter **SACM 2.4 Beta 1 (septembre 2026)** comme cible d'ingénierie épinglée pour le prototype.
- Conserver la compatibilité d'import SACM 2.3 et un parcours de migration 2.3→2.4 documenté lorsque cela est utile.
- Suivre les changements jusqu'à la formalisation de SACM 2.4. Ne pas suivre silencieusement une URL de bêta mouvante.
- À la publication de la 2.4 finale, comparer son métamodèle lisible par machine et ses clauses de conformité à la bêta épinglée, produire un rapport explicite de migration/impact et mettre à jour le profil pris en charge uniquement par un changement autorisé.
- Préserver la distinction entre éléments SACM normatifs et ajouts complémentaires non normatifs.

## 9. Travaux par étapes

1. **Inventaire du métamodèle :** dériver la matrice complète de couverture Beta 1 depuis le XMI/PDF OMG ; classer les constructions normatives et non normatives.
2. **Mapping sémantique :** relier chaque métaclasse et relation SACM à la capacité d'assurance GovCheck ou à un sous-modèle dédié sans perte ; identifier les liens vers 0002, 0005, 0013, 0017 et 0021.
3. **Profil de conformité :** spécifier identité, sérialisation, épinglage de version, contraintes, comportement face aux extensions inconnues et rapport de conformité.
4. **Prototype :** parseur/sérialiseur et corpus d'aller-retour sans perte ; aucune base graphe ni aucun service hébergé obligatoire.
5. **Intégration formelle :** réviser l'abstraction d'assurance et les propriétés TLA+ pour couvrir certaines sémantiques de composition argumentative et d'invalidation ; expliciter le périmètre de chaque abstraction.
6. **Revue et adoption :** revue humaine de la matrice de couverture sémantique et des preuves d'implémentation avant toute déclaration de conformité normative.

## 10. Décisions qui ne sont volontairement pas prises

Ce document ne sélectionne pas de base graphe, n'impose pas d'outillage UML, n'oblige pas chaque projet GovCheck à rédiger des dossiers SACM, ne fait pas de SACM le métamodèle de toute la gouvernance du dépôt, ne remplace pas les sémantiques d'autorité/cycle de vie/exigences de GovCheck et ne prétend pas à une conformité d'implémentation actuelle. Il fixe comme cible la capacité d'expression et de préservation complète de SACM 2.4 Beta 1 dans la capacité d'assurance de GovCheck.

## 11. Sources primaires

- [Catalogue de la spécification SACM de l'OMG, dont SACM 2.4 Beta 1 et le métamodèle lisible par machine](https://www.omg.org/spec/SACM).
- [Suivi des tickets SACM 2.4 de l'OMG — tickets clos et dispositions](https://issues.omg.org/issues/spec/SACM?view=CLOSED).
- [Suivi des tickets SACM 2.4 de l'OMG — tous les tickets](https://issues.omg.org/issues/spec/SACM?view=ALL).
- [Spécification formelle SACM 2.3 de l'OMG](https://www.omg.org/spec/SACM/2.3).

## 12. Relations avec les documents GovCheck existants

Ce document affine, sans les remplacer :
- Spécification 0002 — autorité et composition canoniques de la gouvernance ;
- Spécification 0005 — vocabulaire d'assurance, classes de méthodes, preuves et confiance ;
- Architecture 0013 — métamodèle de gouvernance global : objectifs/exigences/normes/propriétés/assurance ;
- Architecture 0017 — identité stable, révisions et provenance ;
- Architecture 0021 — fraîcheur, invalidation et discipline d'acceptation ;
- Architecture 0024 — bootstrap de projet et sélection de capacités métier ;
- Architecture 0025 — observations du cycle de vie et traçabilité décisionnelle PEAK.

La capacité SACM doit rester reliée à toutes ces fondations sans absorber leurs responsabilités distinctes.

Catalogue de références : [R-197 — artefacts sources et suivi des problèmes SACM 2.4](../references.fr.md#r-197).
