# Audit sémantique des correspondances entre relations du métamodèle typé

**Statut :** audit sémantique fondé sur les sources d'un crosswalk de recherche ; ni métamodèle canonique, ni profil normatif de mapping, ni décision d'adoption.  
**Cible de l'audit :** main au commit `3490c1b576bb155723818a43b24482a6015e9ff5`.  
**Parent :** [Issue #73](https://github.com/Martin-PB/govcheck/issues/73).  
**English:** [Semantic mapping audit](semantic-mapping-audit-2026-11-28.md).  
**Crosswalk candidat :** [Typed metamodel relation candidate](typed-metamodel-relation-candidate.md).

## 1. Conclusion exécutive

Le crosswalk bilingue fusionné dans la PR #217 constitue un **catalogue candidat fondé sur les sources** utile. Il ne prouve pas que les relations des standards sources sont sémantiquement équivalentes aux noms de relations candidats de GovCheck.

L'audit identifie plusieurs non-équivalences récurrentes :

- une **relation d'argumentation affirmée** n'est pas une preuve de théorème ;
- une **relation de support probatoire** ne prouve ni la suffisance ni la vérité de la preuve ;
- une **dérivation de provenance** n'est pas un raffinement sémantique, une dérivation logique ou une implication ;
- un **lien d'échange de besoins** peut être générique et dépendre du type source ;
- une **activité ou relation de vérification de modèle** n'est pas en elle-même un résultat de vérification réussi ;
- une **validation de Resource Shape** établit une conformité structurelle, pas la validité d'une assurance ou d'une autorité.

Le comportement sûr par défaut consiste à préserver les éléments, types, directions, contraintes d'extrémités et identifiants de version natifs de la source. Une relation GovCheck doit rester une correspondance candidate tant qu'un profil de mapping épinglé par version n'énonce pas sa règle sémantique, son domaine/codomaine, ses hypothèses, ses pertes d'information et ses obligations de preuve. Aucune relation de cet audit n'est promue dans le métamodèle canonique.

## 2. Niveaux de correspondance

| Niveau | Signification | Affirmation permise |
|---|---|---|
| L0 — préservation source | Conserver payload natif, type, direction, extrémités et version. | « Cet élément source a été importé/préservé. » |
| L1 — lien générique | Préserver un lien de navigation/interopérabilité sans lui attribuer de sémantique GovCheck. | « Ces ressources sont liées dans la source. » |
| L2 — correspondance sémantique candidate | Proposer une relation GovCheck typée en conservant la relation native et la justification du mapping. | « Il s'agit d'un mapping candidat pour cette version/profil source. » |
| L3 — mapping opérationnel | Règle de mapping épinglée par version, contraintes d'extrémités/domaine, portée et preuves requises définies et validées. | « Ce mapping est opérationnel dans le profil et la portée déclarés. » |
| L4 — preuve ou autorité | Un objet de preuve distinct ou une décision autorisée établit une affirmation/action précise. | Seule la preuve ou décision exacte est revendiquée ; elle ne se déduit pas de L0–L3. |

L3 n'implique pas automatiquement L4. Un mapping peut être structurellement et sémantiquement bien défini sans prouver que l'affirmation mappée est vraie. Une relation affirmée n'est pas un fait vérifié indépendamment.

## 3. Résultats sémantiques par source

| Relation / construction source | Sens natif et contraintes | Traitement GovCheck sûr | Non-équivalence / garde nécessaire |
|---|---|---|---|
| SACM 2.3 — AssertedInference | Relation d'inférence déclarée par un utilisateur entre assertions/claims. Elle enregistre que l'auteur de l'argument affirme un lien inférentiel. | Préserver comme relation de structure argumentative ; mapping candidat vers une relation d'inférence argumentative qualifiée. | Ce n'est ni un théorème Lean, ni une preuve d'implication logique, ni une inférence validée indépendamment. Préserver types source/cible, direction et version SACM. |
| SACM 2.3 — AssertedEvidence | Déclaration qu'un artefact, cité par ArtifactReference, fournit des informations aidant à établir un claim. SACM 2.3 inclut une contrainte OCL imposant ArtifactReference comme source. | Relation candidate de support probatoire, en conservant distincts artefact référencé et claim. | N'établit ni authenticité, pertinence, suffisance, fraîcheur ni vérité de la preuve. La relation elle-même est une affirmation de l'auteur de l'argument. |
| SACM 2.3 — AssertedContext | Relation qui fournit le contexte dans lequel un élément d'argumentation est interprété. | Préserver comme relation de contexte typée ; mapping candidat vers une association contextuelle. | N'est pas automatiquement une hypothèse, justification, prémisse, contrainte ou acceptation de risque. Préserver types et direction des extrémités natives. |
| SACM 2.3 — ArgumentReasoning | Élément descriptif facultatif expliquant le raisonnement associé à des relations affirmées. | Préserver comme annotation/référence de raisonnement, pas comme objet de preuve. | Le suivi d'issues OMG relève une ambiguïté sur le lien diagrammatique entre ArgumentReasoning et AssertedRelationship/AssertedInference. Tant qu'elle n'est pas résolue, ne pas déduire une arête normative de la seule proximité graphique. |
| GSN v3 — SupportedBy | Lien de notation argumentative entre éléments GSN structurant le soutien d'un goal par des sous-goals/solutions/strategies. | Relation candidate de support argumentatif, en préservant types d'éléments et direction du lien GSN. | N'est ni implication formelle, ni terme de preuve, ni garantie de validité de l'argument de soutien. |
| GSN v3 — InContextOf | Lien contextuel utilisé pour les éléments de contexte, d'hypothèse ou de justification dans un argument GSN. | Préserver le type concret d'élément GSN et son rôle contextuel. | Ne pas fusionner contexte, hypothèse et justification dans une relation GovCheck unique sans règle de mapping typée. |
| SysML v2 — SatisfyRequirementUsage | Relation de modèle typée exprimant une affirmation de satisfaction entre un requirement et un sujet/élément de modèle. | Affirmation candidate de satisfaction en conservant requirement, sujet, révision du modèle et portée déclarée. | La relation de modèle ne démontre pas à elle seule la satisfaction et ne fournit pas de preuve de test/preuve formelle. Ce n'est pas une décision d'acceptation. |
| SysML v2 — VerificationCase / verdict | Un cas de vérification possède un sujet et un objectif ; son verdict distingue Pass, Fail, Inconclusive et Error. | Mapper l'enregistrement de vérification comme preuve avec méthode, sujet, exigences, hypothèses et verdict. | Ne pas fusionner Inconclusive ou Error avec Pass/Fail. Une relation de modèle vers un cas de vérification n'est ni le verdict ni sa preuve. |
| ReqIF 1.2 — SpecRelation / SpecRelationType | SpecRelation relie deux instances SpecObject et référence un SpecRelationType. Le standard laisse la relation générique ; les restrictions de types source/cible proposées ont été écartées pour compatibilité. | Préserver type de relation et extrémités comme données d'échange natives. | Ne pas inférer satisfies, derives, refines ou supports de la seule existence d'une SpecRelation ou d'une étiquette lisible par l'humain. |
| PROV-O — wasDerivedFrom | Dérivation de provenance : transformation, mise à jour ou construction d'une entité à partir d'une entité préexistante. | Mapper uniquement vers une filiation de provenance entre entités. | Ce n'est ni dérivation sémantique d'une exigence, ni dérivation de preuve, raffinement ou implication. |
| PROV-O — wasGeneratedBy / used / wasAttributedTo | Relations de provenance entre Entity, Activity et Agent décrivant génération, utilisation et attribution. | Mapper vers événements/agents de provenance avec identifiants source exacts. | Ne constitue ni autorisation normative, ni résultat de vérification, ni preuve de correction. |
| OSLC Core 3.0 — liens de ressources | Les ressources linked-data et liens de domaine fournissent interopérabilité et navigation ; la sémantique est définie par le vocabulaire du domaine OSLC concerné. | Préserver les liens propres à la source ; ne mapper les liens typés que si la spécification de domaine définit leur sens. | Un URI générique ne constitue ni sémantique d'assurance, ni autorité, ni suffisance de preuve. |
| OSLC Resource Shape | Déclare contraintes et descriptions de propriétés des ressources ; permet la validation structurelle des ressources échangées. | Mapper vers une preuve de validation de shape/profil, avec version de shape et résultat de validation. | La conformité à une shape n'établit ni vérité sémantique, ni adéquation d'assurance, ni autorisation. |

### 3.1 SACM 2.3 exige une attention particulière

SACM 2.3 distingue AssertedInference, AssertedEvidence et AssertedContext comme spécialisations d'AssertedRelationship. Leurs sémantiques sources diffèrent :

- AssertedInference enregistre une relation inférentielle affirmée entre assertions.
- AssertedEvidence enregistre qu'un artefact référencé est réputé aider à établir un claim ; sa source est contrainte à ArtifactReference.
- AssertedContext fournit un contexte d'interprétation.
- ArgumentReasoning décrit un raisonnement ; ce n'est pas en soi la preuve ni la relation affirmée.

Le suivi d'issues OMG relève une ambiguïté entre la prose décrivant les sources d'AssertedInference et la structure des types au niveau profil/machine-readable, ainsi qu'une ambiguïté diagrammatique concernant ArgumentReasoning. Ce contenu du suivi d'issues ne constitue pas un amendement normatif. Le profil de mapping doit préserver la structure native SACM 2.3 et enregistrer l'ambiguïté ; il ne doit pas la résoudre silencieusement dans GovCheck.

### 3.2 ReqIF 1.2 montre pourquoi les liens génériques doivent rester génériques

ReqIF SpecRelation relie SpecObject à SpecObject et porte un SpecRelationType. L'issue OMG REQIF12-3 proposait des contraintes de types source/cible sur SpecRelationType, mais la proposition a été écartée pour éviter une modification cassante du schéma XML et préserver l'interopérabilité. Un importeur GovCheck ne peut donc pas supposer qu'une SpecRelation possède des extrémités sémantiques typées parce qu'un outil affiche une étiquette telle que « derive », « satisfy » ou « refine ». Il faut préserver la définition native du type de relation et le profil de l'outil.

### 3.3 Les verdicts de vérification SysML doivent rester distincts

SysML v2 distingue Pass, Fail, Inconclusive et Error comme verdicts de vérification. GovCheck doit préserver ces quatre états et le contexte de vérification. Inconclusive n'est pas Pass ; Error ne prouve pas que le sujet échoue à l'exigence. Un mapping vers le vocabulaire d'évaluation GovCheck nécessite une règle de conversion explicite et doit conserver le verdict original.

## 4. Audit des familles de relations candidates GovCheck

| Relation candidate | Statut du mapping | Obligation minimale avant usage opérationnel |
|---|---|---|
| derives | **Pas une relation universelle.** Distinguer dérivation logique/d'exigence et filiation d'entités PROV-O. | Déclarer le type de dérivation, types source/cible, règle/justification, direction et présence éventuelle d'une preuve de la proposition dérivée. |
| refines | **Candidat uniquement.** Des étiquettes similaires entre standards n'établissent pas un raffinement sémantique. | Définir relation et profil ; propriétés préservées, hypothèses, domaine de couverture et preuve/témoignage requis. |
| supports | **À subdiviser selon la sémantique source.** Support argumentatif, support probatoire et inférence logique diffèrent. | Préserver sous-type, extrémités preuve/claim, direction, standard source et caractère seulement affirmé ou évalué indépendamment. |
| satisfies | **Affirmation, pas preuve.** Les liens de satisfaction SysML sont des assertions de modèle. | Identifier exigence, sujet, configuration, portée, critère et preuve adaptée à la méthode ; décision séparée. |
| verifies | **Relation probatoire qualifiée par la méthode.** Cas de vérification et verdict sont des artefacts distincts. | Enregistrer méthode, outil/version, sujet, exigence/objectif, hypothèses, verdict et digest de preuve. |
| assumes | **Dépend du rôle source.** Contexte, hypothèse, justification et risque accepté ne sont pas interchangeables. | Préserver type source, propriétaire, portée, rationale, revue/expiration et éventuelle décision distincte d'acceptation du risque. |
| wasDerivedFrom | **Provenance uniquement.** | Rester dans la filiation Entity/Activity/Agent ; ne jamais remplacer dérivation sémantique ou preuve. |
| justifies | **Candidat uniquement.** Une relation de rationale n'autorise pas elle-même une décision. | Préserver rationale et preuves ; exiger une décision d'autorité authentifiée distincte pour adoption/publication. |

## 5. Enregistrement de profil de mapping requis

Pour chaque mapping de relation source vers GovCheck, exiger :

1. standard source, version exacte, identifiant d'élément/relation et définition native ;
2. types d'extrémités, multiplicités, direction, contraintes et règles OCL/shape pertinentes ;
3. force sémantique : affirmée, normative, descriptive, observée, dérivée ou prouvée ;
4. relation GovCheck candidate et son domaine/codomaine, y compris partialité et conditions de couverture ;
5. fonction de mapping, hypothèses, pertes d'information et comportement aller-retour ;
6. preuves requises, obligations de preuve et proposition/propriété exacte établie ;
7. fixtures positives, négatives et contre-exemples liées à la version exacte du profil/source ;
8. préservation du payload source et rapport des constructions non prises en charge/non mappées ;
9. enregistrement séparé d'autorisation/adoption si le mapping devient normatif.

Si la sémantique d'une relation source est ambiguë ou si une obligation de mapping n'est pas prouvée, préserver la relation native et classer la correspondance GovCheck comme candidate/unknown. Ne pas la convertir silencieusement en relation typée opérationnelle.

## 6. Lien avec le contre-exemple Lean de mapping partiel

L'issue #210 constate qu'un mapping partiel peut être vacuement vrai lorsque son domaine déclaré est vide. La composition doit également être traitée : deux domaines partiels non vides peuvent avoir une intersection vide, et un premier mapping directionnellement sound ne fournit pas nécessairement un antécédent pour un témoin du domaine du second.

Un futur profil de mapping opérationnel doit donc porter un témoin de domaine habité ou une preuve de couverture typée séparément ; la composition doit exiger un témoin explicite du domaine composé. C'est une obligation de preuve, pas une propriété déductible de deux mappings d'entrée. Les options de conception et tests de régression sont consignés dans #210 ; cet audit n'adopte aucune modification de l'API Lean.

## 7. Disposition

- Le crosswalk de la PR #217 reste un catalogue de recherche fondé sur les sources, pas le métamodèle canonique GovCheck.
- La préservation native source est le défaut pour toutes les relations importées.
- Les liens génériques (ReqIF SpecRelation, liens OSLC génériques) ne doivent pas recevoir de sémantique GovCheck sans profil source spécifique.
- Les relations d'argumentation/preuve (SACM, GSN) ne doivent pas être promues en preuve ou vérité.
- Les relations de provenance (PROV-O) ne doivent pas être confondues avec dérivation/raffinement sémantique.
- Les relations de satisfaction/vérification de modèle (SysML) doivent rester distinctes des verdicts probatoires et décisions d'autorité.
- L'issue #73 reste ouverte jusqu'à ce que les obligations de mapping relation par relation et les fixtures négatives soient complètes. Aucun ontologie ou standard n'est adopté par ce rapport.

## 8. Sources

- [R-04 — GSN Community Standard v3](../references.fr.md#r-04)
- [R-24 — W3C PROV](../references.fr.md#r-24)
- [R-34 — SACM 2.3](../references.fr.md#r-34)
- [R-73 — SACM 2.4 Beta](../references.fr.md#r-73)
- [R-95 — Sources SysML et ReqIF](../references.fr.md#r-95)
- [R-102 — W3C PROV-O](../references.fr.md#r-102)
- [R-234 — OSLC Core](../references.fr.md#r-234) et [R-235 — OSLC Resource Shape](../references.fr.md#r-235)
- [R-243 — Suivi d'issues SACM 2.3](../references.fr.md#r-243)
- [R-244 — Issue ReqIF 1.2 sur les types source/cible](../references.fr.md#r-244)
- [R-245 — Issue SysML 2.1 sur la grammaire de satisfaction d'exigence](../references.fr.md#r-245)
- [Issue #210 — domaine du mapping partiel Lean](https://github.com/Martin-PB/govcheck/issues/210)
