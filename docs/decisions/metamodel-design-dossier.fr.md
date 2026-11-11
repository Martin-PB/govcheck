# Dossier de décision sur le métamodèle GovCheck

**Statut :** dossier de décision soumis à revue ; ce document n'adopte pas le métamodèle définitif.  
**Préparé le :** 2026-11-10.  
**Autorité de décision :** l'autorité normative actuelle de GovCheck, telle qu'enregistrée dans l'Architecture 0023.  
**Version anglaise :** [Metamodel decision dossier](metamodel-design-dossier.md).

## 1. Synthèse exécutive

GovCheck a besoin d'un socle sémantique cohérent pour gouverner un dépôt logiciel sur l'ensemble de son cycle de vie. Il ne s'agit ni d'inventer une ontologie universelle qui remplacerait toutes les normes d'ingénierie, d'assurance, de risque ou de décision, ni d'assembler des documents et outils sans sémantique commune.

La direction candidate est un **graphe sémantique typé, versionné et plusieurs-à-plusieurs**, composé de :

1. un noyau canonique minimal de gouvernance GovCheck ;
2. des modèles sémantiques spécialisés pour les domaines où des normes ou méthodes matures existent ;
3. des contrats et relations explicites entre modèles ;
4. des représentations natives, formats d'échange, validateurs et outils d'analyse derrière des adaptateurs ;
5. une couche épistémique et d'assurance qui enregistre ce qui est affirmé, pourquoi, par quelle méthode, avec quels éléments probants, hypothèses, limites et quelle autorité.

Cette direction est cohérente avec les Architectures 0013 et 0027 et la Spécification 0005, mais ces documents restent des propositions de conception. Le présent dossier rassemble les éléments, options et questions d'arbitrage nécessaires avant adoption.

**Posture recommandée :** adopter les principes architecturaux seulement après revue ; ne pas figer dès maintenant l'ontologie complète, la sérialisation, la technologie de graphe, le langage de règles, la logique, l'assistant de preuve ou le model checker. Définir et valider d'abord un noyau sémantique minimal et ses contrats intermodèles.



**Réévaluation du réemploi des ontologies :** consulter l'[évaluation dédiée](../research/metamodel-ontology-reuse-assessment.fr.md) et sa [version anglaise](../research/metamodel-ontology-reuse-assessment.md). Elle identifie SEON/ReqON comme le meilleur candidat de réemploi trouvé et déconseille une ontologie ad hoc exhaustive au vu des éléments actuels ; un petit noyau de gouvernance avec correspondances explicites reste une option provisoire, non adoptée.

## 2. Décision à prendre

Décider de l'architecture et des frontières du métamodèle GovCheck, notamment :

- ce qui appartient au noyau canonique de gouvernance ;
- quelles sémantiques de domaine restent spécialisées et font autorité dans leur propre périmètre ;
- comment typer, versionner, borner et rendre temporellement applicables objets et relations ;
- comment relier intention, objectifs, besoins des parties prenantes, exigences, décisions, spécifications, propriétés, architecture, modèles, implémentations et assurance ;
- comment représenter affirmations, arguments, hypothèses, observations, éléments probants, tests, model checking, preuves formelles, probabilités et raisonnement flou sans les confondre ;
- comment autorité, provenance, incertitude, invalidation et changement affectent ces relations ;
- comment importer/exporter des modèles externes sans perte sémantique silencieuse ;
- quelles responsabilités relèvent du noyau, des profils optionnels, des adaptateurs ou des outils externes.

Il s'agit d'une décision sur le métamodèle, pas d'une décision imposant toutes les méthodes et tous les outils à chaque dépôt utilisateur.

## 3. Contexte de décision et état du dépôt

### 3.1 Conception déjà présente

Le dépôt contient déjà une architecture candidate substantielle :

- [Architecture 0013 — Métamodèle de gouvernance](../architecture/0013-governance-metamodel.fr.md) distingue objectifs, exigences, normes, propriétés, contrats, éléments d'architecture, modèles, artefacts d'implémentation, méthodes, éléments probants, affirmations, arguments et décisions autorisées. Elle laisse explicitement ouverts le vocabulaire ontologique, la sérialisation, la représentation en graphe et la logique.
- [Architecture 0027 — Normes sémantiques de domaine, modèles de décision et engagements du bootstrap](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.fr.md) propose quatre couches : gouvernance canonique, sémantiques spécialisées, relations intermodèles, adaptateurs/représentations/outils.
- [Spécification 0002 — Modèle canonique de gouvernance](../specifications/0002-canonical-governance-model.fr.md) définit un paquet conceptuel de gouvernance, tout en précisant qu'aucun schéma canonique ni évaluateur n'est implémenté.
- [Spécification 0005 — Assurance, affirmations et éléments probants](../specifications/0005-assurance-model.fr.md) distingue explicitement tests empiriques, model checking, vérification de programmes, preuve de théorèmes, conformité de l'implémentation, fidélité normative et acceptation.
- [Architecture 0022 — Audit des capacités de gouvernance](../architecture/0022-governance-capability-audit.fr.md) décrit les écarts entre conception et implémentation et met en garde contre toute présentation de schémas, résolveurs d'autorité ou évaluateurs proposés comme déjà opérationnels.
- [Architecture 0023 — Autorité de gouvernance du bootstrap](../architecture/0023-bootstrap-governance-authority.fr.md) enregistre le régime d'autorité actuel de GovCheck lui-même. Il ne doit pas être généralisé comme modèle par défaut des dépôts adoptants.

### 3.2 Ancrages de recherche et de backlog

- [Issue #73](https://github.com/Martin-PB/govcheck/issues/73) est l'élément principal de vérification des contrats sémantiques entre intention, exigences, architecture, cycle de vie, assurance et autorité.
- [Issue #69](https://github.com/Martin-PB/govcheck/issues/69) traite les chaînes de justification des claims et la préservation des méthodes, hypothèses et limites.
- [Issue #74](https://github.com/Martin-PB/govcheck/issues/74) traite le statut des références, leur provenance et leur traçabilité vérifiable.
- [Issue #79](https://github.com/Martin-PB/govcheck/issues/79) est le conteneur de portefeuille assurance/évaluation ; ses enfants conservent chacun leur périmètre.
- [Issue #81](https://github.com/Martin-PB/govcheck/issues/81) est le conteneur des méthodes formelles et du cycle de vie.
- [Issue #56](https://github.com/Martin-PB/govcheck/issues/56) compare les mécanismes existants de gouvernance et d'assurance.
- Le registre canonique du travail est [work-items.md](../work-portfolio/work-items.md), avec le contexte dans [work-portfolio/README.md](../work-portfolio/README.md).

Ces éléments sont liés, mais non interchangeables. #73 est le travail principal sur les contrats du métamodèle ; #69, #74, #79 et #81 couvrent des sujets adjacents d'assurance, de références et de formalisation. Ce dossier ne crée pas d'epic en doublon et ne modifie pas silencieusement leur priorité ou statut.

## 4. Critères d'un métamodèle satisfaisant

| ID | Critère | Justification / test |
|---|---|---|
| MM-01 | Préserver les distinctions sémantiques | Intention, besoin, objectif, exigence, contrainte, décision, spécification, propriété, modèle, implémentation, claim, élément probant et acceptation ne doivent pas être ramenés à des nœuds génériques. |
| MM-02 | Relations typées | Chaque relation définit types source/cible, direction, cardinalité, sémantique et qualificatifs ; un lien générique `traces-to` ne suffit pas. |
| MM-03 | Plusieurs-à-plusieurs et non-linéarité | Autoriser sources multiples, soutiens multiples, alternatives, conflits, cycles pertinents et liens partiels/non résolus. |
| MM-04 | Traçabilité bidirectionnelle | Expliquer pourquoi un artefact existe et ce qu'il motive, contraint, réalise ou étaye. |
| MM-05 | Identité et évolution | Identités stables, révisions immuables, succession, provenance, intervalles de validité et invalidation/impact. |
| MM-06 | Contexte et applicabilité | Définir les périmètres par dépôt, composant, étape du cycle de vie, environnement, profil, risque et contexte ; ne pas inférer conformité légale ou sûreté à partir d'étiquettes. |
| MM-07 | Autorité explicite | Séparer auteur, producteur, revue technique, autorité normative, approbation, privilège d'exécution et acceptation du risque. |
| MM-08 | Intégrité épistémique | Préserver affirmation, hypothèse, supposition, observation, élément probant, témoignage, inférence, argument, preuve, contre-évidence, inconnu et limite. |
| MM-09 | Pluralisme des méthodes | Tests, model checking, preuve formelle, inspection, simulation, mesure et observation opérationnelle restent des méthodes/résultats distincts. |
| MM-10 | Intégrité sémantique quantitative | Distinguer probabilité, appartenance floue, non-déterminisme, taux de transition, coûts/récompenses et jugements qualitatifs. |
| MM-11 | Interopérabilité sans perte silencieuse | Cartographier explicitement les normes externes ; signaler constructions non mappées ou ambiguës au lieu de les supprimer. |
| MM-12 | Adoption incrémentale | Les projets sélectionnent profils et capacités applicables ; pas d'échelle universelle de maturité ni d'obligation d'utiliser un outil de preuve. |
| MM-13 | Contrats vérifiables par machine | Définir invariants, vecteurs de conformité, cas négatifs et résultats explicites unknown/unsupported. |
| MM-14 | Explicabilité et reproductibilité | Tout résultat d'évaluation renvoie aux révisions exactes du sujet/modèle/politique, à la méthode, aux entrées, à la version d'outil, aux hypothèses, limites et provenance. |
| MM-15 | Indépendance vis-à-vis d'une chaîne d'outils | Pas de dépendance obligatoire à RDF, une base graphe, Lean, TLA+, un parseur SACM, un service hébergé ou une forge. |

## 5. Architecture sémantique candidate

### 5.1 Quatre couches coopérantes

**A. Noyau canonique de gouvernance GovCheck**

Porte les sémantiques transversales : identité du dépôt/projet ; intention et contexte ; autorités et délégations ; engagements normatifs et applicabilité ; décisions et exceptions ; état du cycle de vie et changements ; identité/révision des artefacts ; approbation et acceptation ; politique de gouvernance et évolution.

**B. Modèles sémantiques spécialisés**

Conservent les sémantiques complètes des domaines lorsque des modèles matures existent. Candidats : SACM pour les cas d'assurance ; GSN et motifs Assurance 2.0 ; DMN pour la logique décisionnelle ; BPMN/CMMN pour processus et dossiers ; RAAML pour l'analyse de risque ; SysML v2/KerML pour l'ingénierie système ; ReqIF pour l'échange d'exigences ; ISO 25010 pour le vocabulaire qualité ; GQM/SMM pour la mesure ; PROV pour la provenance ; SPDX/CycloneDX pour les inventaires logiciels.

Il s'agit de capacités candidates, pas d'engagements d'adoption généraux. Un modèle de domaine reste l'autorité pour ses propres concepts dans le périmètre explicitement adopté.

**C. Couche de relations et contrats intermodèles**

Définit des relations typées et versionnées entre le noyau et les modèles spécialisés, sans aplatir leurs types d'objets. Une correspondance enregistre modèle/version source, modèle/version cible, règle de mapping, couverture, pertes/ambiguïtés, hypothèses, autorité et statut de validation.

**D. Adaptateurs de représentation, d'échange et d'outils**

Portent fichiers natifs, sérialisation, parseurs, validateurs, moteurs de requête/évaluation, éditeurs, import/export et adaptateurs VCS/forge. Une syntaxe ou sérialisation n'est pas le modèle sémantique ; le succès d'un parseur n'est pas une conformité sémantique.

### 5.2 Pourquoi pas un métamodèle universel ?

Une ontologie universelle risque d'effacer les distinctions qui rendent les normes spécialisées utiles, tout en créant un sur-ensemble propriétaire trop vaste à implémenter et valider. Une fédération pure sans noyau commun risque l'incohérence des identités, autorités, périmètres, versions et liens intermodèles. L'architecture en couches vise un noyau de gouvernance restreint tout en préservant les sémantiques spécialisées.

## 6. Familles candidates d'objets sémantiques

Inventaire de découverte, pas hiérarchie de classes définitive. Noms, héritage, cardinalités et champs obligatoires restent à concevoir.

### 6.1 Intention, besoins et ingénierie

- Projet / système / contexte du dépôt
- Partie prenante / acteur / rôle / préoccupation
- Intention / finalité / proposition de valeur
- Besoin / attente / exigence de partie prenante
- Objectif / résultat souhaité
- Mesure / indicateur / métrique / cible
- Exigence / contrainte / obligation / interdiction / permission
- Décision / alternative / justification / hypothèse / risque accepté
- Élément d'architecture / interface / frontière / allocation
- Spécification / contrat / modèle / propriété / invariant
- Artefact d'implémentation / composant / configuration / déploiement

Ne pas supposer une chaîne linéaire unique. Les exigences peuvent provenir du droit, de contrats, de normes, de besoins, d'incidents, de menaces, de défauts, d'interfaces, des opérations et de contraintes d'interopérabilité, pas seulement de l'intention du projet. Objectifs, résultats observables et mesures sont distincts.

### 6.2 Objets épistémiques et d'assurance

- Claim / assertion / hypothèse
- Argument / stratégie d'argumentation / inférence
- Supposition / contexte / justification
- Observation / incident / indicateur / évaluation
- Élément probant / témoignage / témoin / artefact
- Méthode / procédure / outil / configuration
- Résultat de test / inspection / simulation
- Résultat de model checking / contre-exemple / rapport d'états explorés
- Preuve formelle / théorème / axiome / déclaration de base de confiance
- Réfutation / defeater / contre-argument / contradiction
- Inconnu / indécidabilité / sémantique non prise en charge
- Limite / périmètre / fraîcheur / déclaration de confiance
- Décision d'acceptation / risque résiduel

Ces objets doivent être alignés sur SACM lorsque pertinent, sans faire de SACM le métamodèle complet de GovCheck.

### 6.3 Objets quantitatifs et modèles de transition

- Système de transitions / état / prédicat d'état initial / relation de transition
- Sémantique de transition : déterministe, non déterministe, probabiliste, temporisée ou hybride
- Poids de transition typé : probabilité, taux, coût, récompense, priorité ou estimation empirique
- Paramètre / a priori / jeu d'observations / méthode d'estimation
- Spécification d'analyse / propriété / horizon / hypothèses de stratégie
- Résultat d'analyse / témoin / contre-exemple / analyse de sensibilité

Une machine à états finis n'est pas automatiquement probabiliste. Une chaîne de Markov ajoute une hypothèse de Markov et une sémantique de distribution/taux de transition. L'appartenance floue n'est pas une probabilité. Un model checker valide une abstraction fournie, pas sa fidélité au système réel. Voir le compte rendu de recherche et l'entrée R-114 une fois la PR de recherche associée intégrée ; les références mathématiques primaires incluent R-05 et la documentation PRISM/UPPAAL citée dans ce compte rendu.

## 7. Familles candidates de relations

Ne pas créer une arête générique à sémantique surchargée. Familles candidates :

| Famille | Exemples | Sémantique à définir |
|---|---|---|
| Dérivation/raffinement | derives-from, refines, decomposes-into | Autorité source, justification, complétude, relation de raffinement |
| Objectifs/exigences | contributes-to, operationalizes, requires, constrains | Sens, signification de satisfaction, applicabilité |
| Architecture/réalisation | allocated-to, implemented-by, realizes, conforms-to | Allocation vs implémentation vs conformité |
| Décision | selects, rejects, supersedes, justified-by, assumes | Alternatives, autorité, portée et date d'effet |
| Vérification/validation | verified-by, validated-by, evaluated-by | Méthode, sujet, propriété, contexte et résultat |
| Assurance | supports, refutes, challenges, contextualizes, argues-for | Polarité probatoire, inférence, defeaters, structure argumentative |
| Provenance | generated-by, derived-from, attributed-to, sourced-from | Entité/activité/agent, lignée et confiance |
| Gouvernance | authorized-by, delegated-by, applies-to, waives, accepts-risk | Autorité, périmètre, validité, expiration et révocation |
| Temps/évolution | supersedes, invalidates, revalidates, effective-during | Liaison aux révisions, intervalle et propagation d'impact |
| Interopérabilité | maps-to, imports-from, exports-to | Version de mapping, couverture, perte et validation |

Les relations peuvent être plusieurs-à-plusieurs. Des cycles peuvent être légitimes dans certains graphes descriptifs, causaux ou de dépendance ; l'acyclicité doit être spécifiée par famille de relations ou par analyse, pas imposée globalement. La sémantique de chaque relation doit préciser si elle est normative, descriptive, causale, justificative, probatoire ou liée à la provenance.

## 8. Statut épistémique, éléments probants et assurance

Le modèle doit répondre aux questions suivantes : qu'affirme-t-on ; sur quel sujet et périmètre exacts ; pourquoi ; quels éléments soutiennent ou contredisent l'affirmation ; comment chaque élément a-t-il été produit ; quelle inférence est autorisée ; qui en est responsable ; quand est-elle valide ; que reste-t-il d'inconnu ?

Distinctions entre méthodes/résultats non interchangeables :

- **Témoignage/test :** rapporte un comportement observé lors d'exécutions sur des cas et conditions définis ; pas une preuve de théorème.
- **Model checking :** rapporte l'analyse d'un modèle formel au regard de propriétés, avec hypothèses, configuration, bornes, complétude et éventuel contre-exemple.
- **Preuve formelle :** dérivation vérifiée dans un système formel, avec axiomes, hypothèses, imports et base de confiance consignés.
- **Inspection/revue :** jugement expert avec compétence, périmètre, grille et justification.
- **Simulation/mesure/observation de production :** information empirique avec échantillonnage, environnement, instruments, lignée des données et limites.
- **Acceptation :** décision autorisée établissant qu'un prédicat d'acceptation déclaré est satisfait ; pas une preuve de vérité de toutes les affirmations sous-jacentes.

Éviter un indicateur générique `verified` et un champ numérique universel de `confidence`.

## 9. Probabilités, logique floue et modèles de transition

Ces méthodes peuvent être utiles dans des domaines délimités, pas comme fondations universelles.

- La probabilité modélise l'incertitude sur événements/résultats/paramètres. Les résultats bayésiens dépendent des a priori, vraisemblances, qualité des données et hypothèses de dépendance.
- La logique floue modélise l'appartenance graduelle à des concepts imprécis et peut aider pour des exigences vagues ou arbitrages linguistiques. Un degré d'appartenance n'est pas une probabilité.
- Les systèmes de transitions à états finis expriment états et transitions possibles sans nécessiter de probabilités.
- DTMC/CTMC/MDP et automates probabilistes temporisés ajoutent des sémantiques différentes d'aléa, d'action et de temps.
- Les poids de transition doivent être typés : probabilité, taux, coût, récompense, préférence et fréquence empirique ne sont pas interchangeables.
- Incertitude des paramètres, variabilité stochastique et imprécision floue doivent rester séparées.

Recommandation : représenter définitions, paramètres, résultats, provenance et limites des méthodes spécialisées via des profils/adaptateurs optionnels. Ne pas imposer à l'évaluateur central de GovCheck d'implémenter l'inférence bayésienne, floue ou le model checking probabiliste. La question de savoir si GovCheck doit valider les hypothèses spécialisées ou déléguer cette validation à des moteurs de confiance reste ouverte.

## 10. Normes et méthodes externes : comparaison et rôle

Le catalogue central des références est le registre canonique des sources. Cette section résume les rôles et frontières ; elle ne remplace pas les entrées détaillées du catalogue.

| Famille de sources | Apport | Ce qu'elle ne règle pas pour GovCheck |
|---|---|---|
| ISO/IEC/IEEE 15288, 12207, 29148, 15289 | Cycle de vie, processus, exigences et items d'information | Ontologie GovCheck, autorité exacte et sémantique exécutable |
| ISO/IEC/IEEE 42010 ; SysML v2/KerML | Descriptions d'architecture et modèles système | Gouvernance du dépôt et autorité d'approbation |
| KAOS, i*, GRL, Tropos | Relations d'exigences orientées objectifs/acteurs | Assurance complète, provenance et cycle de gouvernance |
| OMG SACM 2.3 / 2.4 Beta 1 ; GSN ; Assurance 2.0 | Claims, arguments, éléments probants, contextes et structures d'assurance | Tous les concepts de cycle de vie, exigences, autorité et gouvernance du dépôt |
| OMG DMN, BPMN, CMMN | Logique de décision, processus et gestion de cas adaptative | Pourquoi une décision est autorisée ou si ses hypothèses sont justifiées |
| OMG RAAML ; ISO 31000 / ISO 23894 ; NIST | Structures et processus d'analyse des risques | Autorité d'acceptation du risque et preuve d'efficacité des mesures |
| W3C PROV-DM/PROV-O ; PPMN | Provenance et lignée | Approbation normative ou vérité du contenu source |
| ReqIF ; OSLC RM | Échange/intégration des exigences | Équivalence sémantique complète entre modèles |
| SPDX ; CycloneDX ; SLSA ; in-toto | Inventaires, provenance et attestations de chaîne logicielle | Correction globale du produit ou gouvernance complète |
| ISO/IEC 25010 ; GQM ; OMG SMM | Caractéristiques qualité et concepts de mesure | Validité universelle des métriques ou acceptation automatique de la qualité |
| NIST SSDF ; NIST SP 800-160 ; AI RMF ; ISO/IEC 42001 | Pratiques de cycle de vie et orientations de risque/gouvernance | Métamodèle GovCheck prêt à l'emploi ou politique exécutable |

### Principales ancres du catalogue

- [R-05 — TLA+ et TLC](../references.fr.md#r-05)
- [R-33–R-34 — Métamodèles et fondations des cas d'assurance](../references.fr.md#r-33)
- [R-44 — KAOS et exigences orientées objectifs](../references.fr.md#r-44)
- [R-51–R-55 — Représentation des connaissances, RDF, SKOS, OWL et SHACL](../references.fr.md#r-51)
- [R-71 — Assurance 2.0](../references.fr.md#r-71)
- [R-73 — OMG SACM 2.4 Beta 1](../references.fr.md#r-73)
- [R-74 — Modèle de décision de projet PEAK](../references.fr.md#r-74)
- [R-88 et R-93 — Vérification des modèles de politique et logique déontique](../references.fr.md#r-88)
- [R-92 — iStar 2.0](../references.fr.md#r-92)
- [R-94–R-98 — Modèles sémantiques OMG, architecture, exigences et qualité ISO](../references.fr.md#r-94)
- [R-102 — Famille W3C PROV](../references.fr.md#r-102)
- [R-114 — Modélisation probabiliste, floue et à transitions](https://github.com/Martin-PB/govcheck/blob/docs/research-assurance-dynamics-2026-11/docs/references.fr.md#r-114) (cataloguée dans la PR de recherche parallèle #105 ; vérifier son intégration avant de considérer cette entrée présente sur la branche par défaut).

Le catalogue indique statut et limites. La présence d'une source ne vaut pas adoption. En particulier, SACM 2.4 Beta 1 est la cible d'ingénierie discutée pour la couverture sémantique et l'interopérabilité SACM, pas une affirmation que la bêta est une norme finale ni que SACM remplace le noyau GovCheck.

## 11. Alternatives architecturales

| Option | Description | Atouts | Risques / faiblesses | Évaluation |
|---|---|---|---|---|
| A. Ontologie GovCheck universelle | Tout domaine dans un système propriétaire unique de classes/relations | Un schéma apparent ; validation centralisée | Aplatissement sémantique, périmètre excessif, duplication propriétaire, fidélité difficile aux normes | Non recommandée |
| B. Documents et liens informels | Documents séparés et liens de traçabilité génériques | Coût initial faible, outils familiers | Sémantique faible, arêtes ambiguës, analyse d'impact et validation machine limitées | Insuffisante comme cible |
| C. Adoption directe d'un métamodèle externe (SACM, RDF/OWL, SysML…) | Un modèle existant devient toute la fondation | Vocabulaire/outils matures dans son domaine | Décalage de périmètre ; force des domaines étrangers dans une sémantique unique ; lacunes d'autorité/cycle de vie | Non recommandée |
| D. Fédération de modèles spécialisés sans noyau commun | Chaque norme indépendante, liens ad hoc | Fidélité locale maximale | Identités, autorités, périmètres, versions et raisonnement intermodèles incohérents | Incomplète |
| E. Noyau canonique restreint + modèles spécialisés + contrats typés + adaptateurs | Architecture en couches du §5 | Équilibre entre gouvernance commune, fidélité spécialisée et adoption incrémentale | Exige une définition rigoureuse des mappings/contrats et la gouvernance des profils | Candidate recommandée |

## 12. Décisions candidates et statut actuel

Cette section sépare les engagements de conception déjà présents dans le dépôt des décisions restant à prendre par l'autorité compétente.

### 12.1 Déjà établis dans la conception du dépôt (vérifier le statut propre à chaque document)

- GovCheck vise la gouvernance du cycle de vie complet d'un dépôt logiciel, pas uniquement la sécurité (Architecture 0027).
- Un modèle canonique de gouvernance est destiné à être l'autorité normative du dépôt gouverné ; les documents lisibles par humains sont des projections contrôlées (Spécification 0002, contrat de conception proposé).
- GovCheck possède son propre régime d'autorité explicite (Architecture 0023) ; les dépôts adoptants définissent le leur.
- Claims, arguments, hypothèses, éléments probants, méthodes, limites et acceptation sont distincts (Spécification 0005).
- Témoignage, model checking, preuve de théorème, conformité de l'implémentation, fidélité normative et acceptation ne doivent pas être confondus (Spécification 0005).
- Les modèles spécialisés conservent leur sémantique de domaine et sont reliés par des relations explicites (Architecture 0027).
- SACM 2.4 Beta 1 est la cible d'ingénierie discutée pour la capacité SACM, avec objectif de couverture sémantique complète et d'interopérabilité (R-73 et Architecture 0027) ; ce n'est pas l'adoption de SACM comme métamodèle global.

Ce sont des énoncés de conception du dépôt, pas des capacités toutes implémentées. Le statut « proposé », « conceptuel » ou « non implémenté » indiqué dans chaque document reste déterminant.

### 12.2 Recommandations provisoires soumises à l'autorité

1. Adopter l'architecture en couches du §5 comme direction privilégiée.
2. Adopter un graphe sémantique typé comme abstraction des relations intermodèles, sans imposer base de graphe ni RDF.
3. Conserver un noyau canonique minimal pour identité, autorité, périmètre, applicabilité, révision, décisions, cycle de vie et contrats intermodèles.
4. Conserver des modèles spécialisés pour assurance, exigences, architecture, risque, décision, mesure, provenance et chaîne logicielle lorsque pertinent.
5. Préserver les distinctions épistémiques et méthodologiques ; ne jamais transformer un test en preuve ni le model checking en preuve de théorème.
6. Autoriser des profils probabilistes, flous et Markov/transitionnels lorsqu'ils sont justifiés ; aucun n'est obligatoire.
7. Reporter sérialisation, langage ontologique, stockage/requête de graphe et langage d'évaluation jusqu'à stabilisation des contrats et cas de conformité.
8. Exiger une déclaration explicite de couverture et de pertes pour chaque adaptateur d'import/export.

Ces recommandations ne sont pas adoptées du seul fait de figurer ici. Elles nécessitent une décision explicite de l'autorité actuelle de GovCheck.

### 12.3 Décisions volontairement ouvertes

- Ontologie exacte, hiérarchie de classes et identifiants canoniques.
- Usage de RDF/OWL/SHACL, JSON-LD, JSON/YAML typé, schémas relationnels ou hybride.
- Langage de requête de graphe éventuel.
- Catalogue exact de relations, cardinalités et règles d'inférence.
- Normes qui deviennent des profils de premier rang et celles qui restent des adaptateurs d'import/export.
- Stratégie de couverture complète SACM 2.4 Beta 1 et gestion des versions futures.
- Sémantiques probabilistes/floues et frontières de validation.
- Frontières des profils Markov/MDP/automates et intégration au model checking quantitatif.
- Formalisation et obligations de preuve du métamodèle lui-même.
- Paquet d'échange canonique, migration et comptabilité des pertes.

## 13. Options de décision et réponse attendue de l'autorité

La revue de l'autorité doit enregistrer l'une des réponses : **approuver**, **approuver sous conditions**, **différer**, **rejeter** ou **demander des éléments supplémentaires**. Elle doit identifier la révision exacte du dossier, l'option retenue, la justification, le périmètre, les conditions, le responsable et le déclencheur de réexamen.

Question centrale :

> GovCheck doit-il adopter un noyau canonique restreint de gouvernance, relié à des modèles sémantiques spécialisés par des contrats typés, versionnés et auditables, plutôt qu'un métamodèle universel ou une approche purement documentaire ?

Réponse recommandée : **approuver sous conditions**, sous réserve :
- d'un vocabulaire minimal du noyau et d'un catalogue de relations revus ;
- d'une matrice de correspondance/couverture pour les premiers profils sélectionnés ;
- de non-objectifs explicites et de l'indépendance vis-à-vis des outils ;
- d'exemples de conformité et de cas négatifs ;
- d'une politique d'interopérabilité/migration qui expose les pertes sémantiques ;
- d'un argument d'assurance du métamodèle et de sa frontière d'implémentation.

Cette recommandation ne vaut pas approbation.

## 14. Backlog et séquence de livraison

Le portefeuille existant reste la source des identités et statuts des travaux. La séquence suivante relie le dossier aux travaux existants sans créer silencieusement de nouveaux engagements.

| Ordre | Travail existant | Contribution attendue | Dépendance / condition de sortie |
|---|---|---|---|
| 1 | [#73 — Contrats intermodèles](https://github.com/Martin-PB/govcheck/issues/73) | Définir types d'objets/relations, sémantique, cardinalités, provenance, autorité, périmètre et validité temporelle ; vérifier les contrats entre cycle de vie, assurance et autorité. | Travail principal du métamodèle ; aucune affirmation de raffinement sans éléments probants. |
| 2 | [#56 — Comparaison de l'écosystème gouvernance/assurance](https://github.com/Martin-PB/govcheck/issues/56) | Comparer capacités réutilisables, interfaces et lacunes à partir de sources académiques/industrielles primaires. | Alimenter une matrice sources/concepts/décisions ; cataloguer les sources EN/FR. |
| 3 | [#69 — Chaîne de justification des claims](https://github.com/Martin-PB/govcheck/issues/69) | Formaliser relations épistémiques et d'assurance, limites entre preuve/test/model checking, hypothèses et defeaters. | Réutiliser le vocabulaire de relations du noyau ; garder les méthodes distinctes. |
| 4 | [#74 — Statut et provenance des références](https://github.com/Martin-PB/govcheck/issues/74) | Rendre statut des sources, adoption, provenance et citations bidirectionnelles vérifiables par machine. | Éviter de confondre présence d'une source et adoption. |
| 5 | [#81 — Modèles formels et cycle de vie](https://github.com/Martin-PB/govcheck/issues/81) | Vérifier invariants intermodèles sélectionnés et contrats temporels/invalidation. | Formaliser après explicitation des sémantiques et hypothèses. |
| 6 | [#79 — Portefeuille évaluation et assurance](https://github.com/Martin-PB/govcheck/issues/79) | Relier métamodèle à l'évaluation, aux éléments probants et à une tranche verticale exécutable. | Ne pas implémenter avant stabilisation des contrats minimaux et statuts. |

Tout travail supplémentaire ne doit être créé que lorsqu'une lacune est confirmée et ne peut être affectée à un élément atomique existant. Lacunes candidates à réexaminer dans #73 : sémantique des types/cardinalités de relations ; contrats de mapping/perte des profils spécialisés ; contrats de profils quantitatifs ; corpus de conformité. Ne pas les décomposer prématurément.

### Jalons proposés

- **M0 — Socle documentaire :** catalogue de sources et audit des conceptions existantes suffisamment complets pour identifier concepts et conflits.
- **M1 — Noyau conceptuel :** familles d'objets/relations typées, identité, périmètre, autorité, provenance et temps spécifiés.
- **M2 — Matrice de correspondance :** comparaison du noyau et des profils candidats avec les normes sélectionnées ; couverture, extensions et pertes consignées.
- **M3 — Contrat épistémique/d'assurance :** claims, méthodes, résultats, éléments probants, hypothèses, defeaters, inconnues et invalidation définis.
- **M4 — Contrats formels :** invariants sélectionnés et cas de test/model checking intermodèles assortis d'hypothèses explicites.
- **M5 — Corpus de conformité et prototype :** validation d'exemples positifs/négatifs et d'au moins un profil de bout en bout sans figer une chaîne d'outils universelle.

## 15. Risques et mesures de maîtrise

| Risque | Conséquence | Mesure |
|---|---|---|
| Débordement ontologique | Modèle universel propriétaire impossible à implémenter | Noyau réduit ; profils spécialisés ; périmètre progressif |
| Choix technologique prématuré | L'outil dicte la sémantique | Définir contrats et exemples avant les outils |
| Perte sémantique des adaptateurs | Fausses affirmations d'équivalence/conformité | Couverture, rapports de perte, tests aller-retour |
| Effondrement épistémique | Tests, preuves, probabilités et opinions confondus | Types de méthodes/résultats et arguments d'assurance |
| Fuite d'autorité | Modèle importé ou outil acquiert une force normative indue | Liens explicites d'adoption et d'autorité |
| Dérive temporelle | Éléments périmés considérés actuels | Liaison aux révisions, intervalles de validité, invalidation |
| Fausse complétude | Liens génériques satisfont les contrôles de traçabilité | Complétude par profil et validation sémantique |
| Évolution des versions de normes | Changement de sens silencieux | Versions épinglées, statuts et décisions de migration |
| Fausse précision quantitative | Scores globaux non étayés | Hypothèses, calibration, sensibilité et limites explicites |

## 16. Définition d'un paquet de métamodèle prêt à décision

Le métamodèle ne doit pas être déclaré prêt à adoption tant que le paquet ne contient pas :

- glossaire et définitions des types d'objets ;
- catalogue des relations typées avec domaines, codomaines, cardinalités et sémantiques ;
- contrats d'identité, révision, provenance, autorité, périmètre et temporalité ;
- distinction entre relations normatives, descriptives, causales, justificatives, probatoires et de provenance ;
- matrices de correspondance sources/concepts et normes/profils ;
- couverture import/export et déclarations de pertes sémantiques ;
- exemples positifs et négatifs de conformité ;
- invariants formels sélectionnés et résultats de validation avec hypothèses/limites ;
- non-objectifs, constructions non prises en charge et questions ouvertes explicites ;
- décision autorisée par l'autorité actuelle de GovCheck ;
- documents EN/FR synchronisés et liens vers les références.

Jusque-là, le métamodèle demeure une proposition en recherche et vérification, pas une spécification normative adoptée.

## 17. Références

Toutes les sources externes doivent être maintenues dans le [catalogue central des références](../references.fr.md), avec couverture EN/FR, identifiants stables, statut de source, limites et citations bidirectionnelles. Ce dossier pointe volontairement vers les ancres du catalogue plutôt que de créer une bibliographie parallèle.

Documents internes de conception : Architectures 0013, 0022, 0023, 0027 ; Spécifications 0002 et 0005 ; ADR dans `docs/decisions/` ; modèles formels dans `docs/formal/` ; registre du portefeuille dans `docs/work-portfolio/`.

