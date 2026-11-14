# Évaluation du réemploi des ontologies et de CSLib pour GovCheck

**Statut :** complément de recherche ; recommandation provisoire, non adoptée. **Date :** 2026-11-11.  
**Version anglaise :** [Ontology reuse and CSLib assessment](metamodel-ontology-reuse-assessment.md).  
**Dossier parent :** [Dossier de décision sur le métamodèle GovCheck](../decisions/metamodel-design-dossier.fr.md).

## 1. Conclusion

Les éléments étudiés ne justifient **pas** la création immédiate d'une ontologie GovCheck exhaustive et autonome. Il existe déjà un réseau d'ontologies d'ingénierie logicielle (SEON), ainsi que des modèles établis pour les exigences, l'assurance, la provenance, les rôles, les politiques, les décisions, l'architecture, le cycle de vie et les artefacts logiciels.

La direction la mieux étayée consiste à **réutiliser les modèles existants dans leurs périmètres**, à ne définir un **petit vocabulaire de gouvernance propre à GovCheck** que lorsqu'une lacune sémantique est démontrée, puis à relier les modèles par des correspondances et contrats de conformité explicites et versionnés. CSLib est une bibliothèque candidate de formalisation/preuve, non une ontologie canonique, un format d'échange ou un moteur RDF/SHACL. Son éventuelle non-adoption ne rend pas facultative l'obligation de preuve : toute correspondance sémantique utilisée dans un raisonnement GovCheck doit être formellement démontrée par une chaîne de vérification de confiance, que les définitions proviennent de CSLib, d'une autre bibliothèque ou d'une formalisation GovCheck minimale.

Cela ne signifie pas « aucun modèle GovCheck ». GovCheck doit définir la sémantique de gouvernance du dépôt et les contrats intermodèles ; il faut les déduire d'une analyse de lacunes plutôt que tout inventer. La PR #106 n'est pas fusionnée et ce rapport n'adopte aucun métamodèle.

## 2. Candidat de réemploi le plus pertinent : SEON

Le *Software Engineering Ontology Network* (SEON) est la découverte la plus directement pertinente. Son réseau publié comprend :

- **SPO** : processus logiciels, activités, ressources, personnes, artefacts et procédures ;
- **ReqON** : exigences logicielles de référence (RSRO), exigences orientées objectifs (GORO), processus de développement des exigences (RDPO) et exigences à l'exécution (RRO) ;
- **SwO** : concepts du domaine logiciel ;
- **ROoST** : tests logiciels ; **QAPO** : processus d'assurance qualité ; **RSMO** : mesure logicielle ;
- d'autres ontologies de conception, codage, gestion de projet et gestion de configuration ;
- **UFO** comme ontologie fondationnelle pour ancrer les distinctions du réseau.

SEON se présente comme un réseau d'ontologies de référence avec des mécanismes d'intégration et une sémantique cohérente entre concepts et relations. C'est un point de départ nettement meilleur que de réinventer tous les concepts du cycle de vie, des exigences et de l'ingénierie.

**Réserve de maturité :** le site public affiche la version 1.0.5 et une documentation qui semble dater de plusieurs années. Cette passe n'a pas établi la maintenance active, l'uniformité des licences, la conformité des implémentations ni l'aptitude opérationnelle comme dépendance obligatoire. SEON est donc une référence de grande valeur et un candidat d'alignement, à valider avant adoption.

SEON ne règle pas à lui seul l'autorité normative propre au dépôt, la délégation/révocation, l'adoption des décisions, l'expiration des exceptions, l'application indépendante de la forge, ni toutes les distinctions entre tests, rapports de model checking, preuves de théorèmes, risques acceptés et observations réelles.

Sources : [R-115](../references.fr.md#r-115), [SEON](https://dev.nemo.inf.ufes.br/seon/SEON.html), [ReqON](https://dev.nemo.inf.ufes.br/seon/ReqON.html), [SPO](https://dev.nemo.inf.ufes.br/seon/SPO.html).

Sources du catalogue associées : [R-04](../references.fr.md#r-04) · [R-33](../references.fr.md#r-33) · [R-34](../references.fr.md#r-34) · [R-71](../references.fr.md#r-71) · [R-73](../references.fr.md#r-73) · [R-88](../references.fr.md#r-88) · [R-92](../references.fr.md#r-92) · [R-93](../references.fr.md#r-93) · [R-94](../references.fr.md#r-94) · [R-95](../references.fr.md#r-95) · [R-96](../references.fr.md#r-96) · [R-97](../references.fr.md#r-97) · [R-98](../references.fr.md#r-98) · [R-99](../references.fr.md#r-99) · [R-100](../references.fr.md#r-100) · [R-102](../references.fr.md#r-102) · [R-115](../references.fr.md#r-115) · [R-116](../references.fr.md#r-116) · [R-117](../references.fr.md#r-117) · [R-118](../references.fr.md#r-118) · [R-119](../references.fr.md#r-119) · [R-120](../references.fr.md#r-120)

## 3. Cartographie de couverture : réutiliser sans confondre

| Besoin | Candidats existants | Couverture réutilisable | Limite / lacune |
|---|---|---|---|
| Intentions, objectifs, exigences | SEON ReqON/RSRO/GORO/RDPO ; ISO/IEC/IEEE 29148 ; ReqIF ; OSLC RM | Concepts, produits de travail, échange et traçabilité des exigences | Aucun ne couvre tout le cycle intention-assurance ni l'autorité de dépôt |
| Cycle de vie et produits de travail | SEON SPO ; OMG Essence ; ISO/IEC/IEEE 15288 | Processus, activités, artefacts et noyau d'ingénierie indépendant des méthodes | Les états/al­phas ne sont pas automatiquement des décisions de gouvernance ou des preuves de conformité |
| Affirmations, arguments et preuves | SACM 2.4 Beta 1 (cible d'ingénierie) ; SACM 2.3 formel | Structures de dossiers d'assurance, affirmations, raisonnement, références de preuves | SACM n'est pas tout le modèle de gouvernance ; distinguer versions bêta et formelles |
| Provenance | W3C PROV/PROV-O | Entités, activités, agents, dérivation, attribution, génération | La provenance ne prouve pas vérité, intégrité, suffisance ou autorisation |
| Organisations et rôles | W3C ORG ; agents PROV-O | Organisations, rôles et attribution | ORG ne couvre pas entièrement contrôle, responsabilité, habilitation et délégation propre au dépôt |
| Permissions et devoirs | W3C ODRL ; logique déontique ; politiques exécutables | Permissions, interdictions, devoirs et règles de politique typés | ODRL n'est pas un système complet de gouvernance ou de résolution d'autorité |
| Décisions et motivation | OMG BMM ; DMN | Motivation, objectifs, exigences et logique de décision | Un modèle de décision ne donne pas l'autorité de l'adopter |
| Architecture et comportement | ISO/IEC/IEEE 42010 ; SysML v2/KerML ; TLA+ | Description d'architecture, modèles structurels/comportementaux et propriétés | Modèles spécialisés ; leur analyse ne prouve pas la fidélité au réel |
| Représentation/validation des ontologies | OWL 2, RDF, SKOS, SHACL ; OMG ODM | Langage d'ontologie, graphes, correspondances de vocabulaires, contraintes et mappings | RDF/OWL n'est pas une condition d'interopérabilité ; SHACL n'est pas une preuve de théorème |
| Artefacts et chaîne logicielle | SPDX, CycloneDX | Métadonnées de composants, dépendances, paquets et builds | Un format valide ne prouve pas exhaustivité, sûreté ou conformité des licences |
| Sémantique formelle et preuve | Lean et CSLib | Définitions typées, sémantique opérationnelle, systèmes de transition, logiques et théorèmes formalisés | CSLib n'est ni une ontologie métier, ni un moteur RDF/SHACL, ni un pont automatique du code vers une preuve |

Cette cartographie ne prétend pas que tous les candidats sont adoptés ni qu'ils sont de même nature. Elle couvre ontologies, métamodèles, formats d'échange, normes, langages de modélisation, politiques et bibliothèques de preuve ; leurs rôles doivent rester distincts.

## 4. CSLib : capacités et limites

Le dépôt officiel présente CSLib comme une bibliothèque Lean de formalisation des théories et outils de l'informatique, avec des API réutilisables pour la formalisation, la vérification logicielle et le logiciel certifié. Son organisation publiée comprend fondations et structures de données ; sémantique opérationnelle et systèmes de transition étiquetés (LTS) ; bisimilarité et équivalence de traces ; logiques de Hoare et temporelle linéaire ; langages/calculs Boole, CCS, lambda et pi ; automates et calculabilité.

CSLib peut servir à **formaliser certaines sémantiques GovCheck** : système de transition du cycle de vie, propriété temporelle, relation de raffinement ou théorème sur un contrat intermodèle fini. Les consignes de contribution recommandent explicitement de réutiliser les abstractions existantes comme LTS au lieu de les dupliquer.

En revanche, CSLib ne fournit pas :
- une ontologie prête à l'emploi des intentions, objectifs, exigences, décisions, autorités, preuves ou dossiers d'assurance ;
- un magasin RDF/OWL, moteur SPARQL, outil d'alignement SKOS ou validateur SHACL ;
- un format d'échange de dépôt lisible par les humains/agents, ni la préservation automatique des artefacts natifs SACM XML/XMI ;
- une chaîne achevée et entièrement fondationnelle qui transforme du code courant arbitraire en sémantique Lean vérifiée.

La voie Boole évolue encore. Sa documentation indique que les traductions de sources peuvent initialement être ad hoc et considérées comme fiables ; la preuve de préservation sémantique est un objectif de plus long terme et le backend par plongement profond n'est pas entièrement fondationnel. Une preuve établit un théorème à partir des définitions, axiomes et hypothèses fournis ; elle ne prouve pas que le modèle représente fidèlement le dépôt, la politique, le déploiement ou le monde réel.

**Recommandation :** ne pas rendre CSLib obligatoire maintenant. Si un contrat important ne peut être contrôlé par des tests de schéma/contrat, réaliser un petit prototype Lean/CSLib derrière un adaptateur facultatif. Épingler sa révision et documenter chaîne d'outils, imports, axiomes, hypothèses et base de confiance.

Sources : [R-118](../references.fr.md#r-118), [dépôt CSLib](https://github.com/leanprover/cslib), [organisation](https://github.com/leanprover/cslib/blob/main/ORGANISATION.md), [guide de contribution](https://github.com/leanprover/cslib/blob/main/CONTRIBUTING.md), [feuille de route](https://www.cslib.io/roadmap/).

## 5. Ontologie, métamodèle, contraintes et bibliothèque de preuve : rôles différents

- **Ontologie/vocabulaire de domaine :** concepts et relations d'un domaine, par exemple SEON ou PROV-O.
- **Métamodèle :** constructions et règles structurelles pour définir des modèles, par exemple SACM, ReqIF ou SysML.
- **Format d'échange :** structure d'interopérabilité, par exemple ReqIF XML ; la syntaxe ne constitue pas toute la sémantique.
- **Langage de contraintes :** validation d'instances, par exemple SHACL sur des graphes RDF.
- **Langage de décision/politique :** expression/évaluation de décisions ou permissions, par exemple DMN ou ODRL.
- **Bibliothèque de preuve formelle :** définitions et théorèmes vérifiés, par exemple CSLib en Lean.

L'Ontology Definition Metamodel (ODM) de l'OMG est pertinent comme méthode : il définit des métamodèles, profils et correspondances entre normes d'ontologie et de modélisation, notamment UML/MOF. Il ne s'agit pas d'une ontologie de cycle de vie GovCheck prête à l'emploi. OWL 2 exprime des ontologies formelles ; RDF fournit des graphes ; SKOS permet les schémas de concepts et leurs correspondances ; SHACL valide les graphes contre des contraintes déclarées. Ces technologies peuvent constituer un profil d'implémentation, mais GovCheck ne doit ni confondre sa sémantique avec RDF ni imposer cette pile avant décision.

Sources : [R-116](../references.fr.md#r-116), [R-117](../references.fr.md#r-117), [OWL 2](https://www.w3.org/TR/owl-overview/), [SKOS](https://www.w3.org/TR/skos-reference/), [SHACL](https://www.w3.org/TR/shacl/), [OMG ODM](https://www.omg.org/spec/ODM/).

## 6. Candidat recommandé : fédérer d'abord, étendre sur preuve de besoin

Le noyau GovCheck candidat pourrait couvrir les lacunes suivantes : périmètre du dépôt et identité/révision des artefacts ; autorité normative, rôle, délégation, portée, période d'effet, révocation et succession ; décision, alternative, justification, adoption, exception, acceptation du risque résiduel et expiration ; applicabilité exacte d'une politique/modèle/décision ; contrat de correspondance versionné avec couverture, ambiguïté et pertes ; statuts d'évaluation (réussi, échoué, indéterminé, non pris en charge, non évalué, périmé) ; invalidation/révalidation après changement.

Ce sont des lacunes candidates, pas une hiérarchie approuvée. Chaque concept doit être justifié par une question de compétence et une comparaison démontrant que réemploi, profil ou correspondance ne suffisent pas.

Chaque correspondance doit déclarer les versions exactes des modèles et artefacts, l'identité de la règle et l'autorité responsable, la relation exacte revendiquée (équivalence, inclusion, raffinement, traduction, préservation partielle ou traçabilité seule), les constructions mappées/non mappées/transformées, les hypothèses, pertes et comportements aller-retour, les sémantiques formelles et l'énoncé du théorème, l'artefact de preuve, le vérificateur de confiance et les dépendances du socle de confiance, ainsi que la période de validité et les conditions d'invalidation.

Une correspondance utilisée dans un raisonnement GovCheck n'est admissible qu'après démonstration formelle vérifiée de la relation revendiquée. Une proposition non démontrée peut être conservée comme recherche non résolue, mais ne peut pas servir de prémisse établie. Ne jamais convertir silencieusement « inconnu » en « faux », « non applicable », « réussi » ou « prouvé », ni inférer une équivalence à partir des seuls libellés.

## 7. Options et recommandation

| Option | Évaluation |
|---|---|
| A. Inventer une ontologie GovCheck exhaustive | **Non recommandée actuellement** : duplication, maintenance coûteuse, dérive sémantique et fausses équivalences |
| B. Relier les modèles existants sans sémantique propre à GovCheck | Insuffisant seul : autorité, applicabilité, révisions, validité des mappings et statuts d'évaluation restent flous |
| C. Petit noyau + fédération de modèles + contrats typés | **Candidat recommandé à l'arbitrage** : réemploi des sémantiques spécialisées et contrat minimal de gouvernance/interopérabilité |
| D. Faire de CSLib/Lean l'ontologie canonique | Non recommandé ; un profil facultatif de vérification formelle peut être utile |

## 8. Backlog et critères de sortie

Pas de nouvel épique. Réutiliser :
1. **#56 :** comparer SEON/ReqON, ODM, composants W3C, OSLC RM et CSLib.
2. **#73 :** définir questions de compétence, matrice de couverture, sémantique des correspondances et fixtures positives/adversariales.
3. **#74 :** conserver source/version, maturité, licence, artefact machine et citations réciproques.
4. **#79 :** distinguer test, model checking, preuve, observation et acceptation.
5. **#81 :** prototyper Lean/CSLib uniquement si justifié par rapport aux tests exécutables.

Critères de sortie : chaque concept est classé comme réutilisé, profilé, mappé, géré par adaptateur, lacune propre démontrée ou hors périmètre ; les modèles natifs sont préservés ; le contenu non pris en charge est signalé ; les mappings ont contrats versionnés et fixtures adversariales ; l'autorité approuve explicitement les limites du noyau. Aucune technologie d'ontologie ni aucun outil de preuve n'est imposé par cette recherche.

## 9. Traçabilité

Catalogue central : [R-115 SEON/ReqON](../references.fr.md#r-115), [R-116 OWL/RDF/SKOS/SHACL](../references.fr.md#r-116), [R-117 OMG ODM](../references.fr.md#r-117), [R-118 CSLib](../references.fr.md#r-118), [R-119 Essence](../references.fr.md#r-119), [R-120 OSLC RM](../references.fr.md#r-120). Sources existantes : SACM (R-04, R-33–R-34, R-71, R-73), modèles d'ingénierie/domaine (R-92, R-94–R-100), PROV (R-102) et politiques/logique (R-88, R-93).

Documents internes : [Architecture 0013](../architecture/0013-governance-metamodel.md), [Architecture 0027](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [Spécification 0002](../specifications/0002-canonical-governance-model.md), [Spécification 0005](../specifications/0005-assurance-model.md), [dossier de décision](../decisions/metamodel-design-dossier.fr.md).

Catalogue de références : [R-200 — SEON/ReqON/SPO](../references.fr.md#r-200) ; [R-201 — OMG ODM](../references.fr.md#r-201) ; [R-123 — CSLib](../references.fr.md#r-123).
