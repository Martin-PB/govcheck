# Audit de couverture sémantique du métamodèle GovCheck — état initial au 13/11/2026

**Statut :** audit d'ingénierie et de recherche de l'état actuel du dépôt ; ne constitue ni un métamodèle adopté, ni une déclaration de conformité, ni une décision normative.  
**Périmètre :** issue [#73](https://github.com/Martin-PB/govcheck/issues/73), recherches existantes sur le réemploi des ontologies, prototype de cohérence Lean, tranche de mapping SACM 2.4 Beta 1 et modèles de cycle de vie/assurance/autorité.  
**Version anglaise :** [GovCheck metamodel semantic-coverage audit](metamodel-semantic-coverage-audit.md).

## 1. Constat exécutif

GovCheck dispose déjà d'un paysage sémantique documentaire substantiel et de plusieurs artefacts formels utiles. Il ne possède **pas encore** de métamodèle inter-domaines complet et exécutable par machine, ni d'intégration sémantique démontrée des ontologies candidates.

Les couvertures existantes les plus solides sont :
- un petit vocabulaire Lean qui sépare méthode de production, nature épistémique et statut du résultat ;
- un contrat typé de correspondance portant des preuves ;
- une tranche SACM 2.4 Beta 1 qualifiée par la vue source pour Claim/Assertion/inférences ;
- des modèles TLA+ distincts pour le cycle de vie, l'assurance, l'autorité, l'applicabilité de la gouvernance et le journal ;
- une stratégie documentée de réemploi de SEON/ReqON, SACM, PROV-O, des référentiels d'exigences et d'architecture, de modèles de décision et d'autres sémantiques spécialisées.

Le principal constat de cet audit est un **défaut de frontière de preuve dans l'ancienne API Lean de mapping**. Son ancien type `SemanticBridge` acceptait les constructeurs `approximate`, `traceabilityOnly` et `unsupported` sans théorème reliant les propositions source et cible. Ces valeurs pouvaient néanmoins être intégrées dans `EvidenceMapping`. Son ancien `KindMappingRule.transport` permettait également de transporter une étiquette `theoremProof` sans terme de preuve pour la proposition cible.

Cette PR ferme ces deux voies au niveau des types :
- `EvidenceMapping` opérationnel n'admet désormais que l'équivalence, la préservation directionnelle saine ou la préservation partielle sur un domaine déclaré, chacune avec son obligation de preuve correspondante ;
- les candidats approximatifs, limités à la traçabilité ou non pris en charge sont représentés séparément par `MappingProposal`, qui ne contient aucun pont sémantique et ne peut pas être un `EvidenceMapping` ;
- toute correspondance dont la cible est de nature `theoremProof` exige un terme de preuve Lean de la proposition cible exacte, y compris lorsque l'enregistrement source portait déjà l'étiquette `theoremProof`.

Il s'agit d'une correction de la **frontière de types du prototype**, pas d'une preuve qu'une ontologie source, un importateur, un exportateur ou une implémentation de production de GovCheck est correct.

## 2. Vocabulaire de statut employé dans cet audit

| Statut | Signification |
|---|---|
| **Formalisé (localement)** | Une définition ou un théorème indépendant de la source existe dans le paquet Lean/TLA+ actuel. |
| **Vérifié par model checking** | Un modèle/schéma de transition fini a été exploré ; les conclusions restent bornées par ce modèle. |
| **Cible documentée** | Un standard, une ontologie ou un modèle métier est identifié et sa couverture souhaitée est décrite, mais il n'est ni implémenté ni démontré. |
| **Mapping candidat** | Une relation sémantique possible a été identifiée ; elle ne devient pas une prémisse opérationnelle avant la preuve de la relation exacte. |
| **Pas encore couvert** | Aucune représentation formelle adéquate ni correspondance vérifiée n'a été trouvée dans l'état du dépôt examiné. |
| **Conflit de source / non résolu** | Les sources divergent ou leur sémantique/identité n'est pas encore établie ; les deux vues doivent être conservées. |

Ces étiquettes décrivent les éléments présents dans le dépôt, pas un classement des standards externes. Une cible documentée n'est pas une adoption ; un model checking réussi n'est pas une preuve de théorème ; un théorème Lean sur une proposition fournie ne prouve pas que cette proposition interprète fidèlement un artefact source.

## 3. Matrice de couverture

| Domaine sémantique | Base existante dans le dépôt | Couverture actuelle | Lacune principale |
|---|---|---|---|
| **Intention, besoins des parties prenantes, objectifs et résultats** | Enregistrement de l'intention et analyse d'impact ; ISO/IEC/IEEE 15288/29148 ; ingénierie des systèmes NASA ; GORE/iStar ; étude de réemploi SEON/ReqON. | Cible documentée et recherche existante. | Aucun système complet de types canoniques ni sémantique formelle de ces concepts et de leurs relations plusieurs-à-plusieurs. Aucun mapping vérifié des modèles source d'exigences/objectifs vers un domaine sémantique GovCheck commun. |
| **Exigences et contraintes** | Recherche sur les exigences ; candidats ReqIF et OSLC ; ISO/IEC/IEEE 29148 ; ReqON/SEON. | Cible documentée. | Aucun fixture d'instance source, parseur, inventaire exhaustif des constructions ni contrat de préservation démontré. Une exigence n'est pas automatiquement un objectif, une affirmation, une règle ou une décision. |
| **Décisions, justification et risque accepté** | Recherche PEAK et Architecture 0025 ; candidats DMN/BMM ; comptes rendus de décision et modèles d'autorité de gouvernance. | Cible documentée ; certaines transitions de gouvernance sont vérifiées par model checking. | Aucun pont sémantique formel de PEAK/DMN vers les décisions, hypothèses, connaissances, alternatives et risques acceptés GovCheck. La logique de décision ne confère pas à elle seule l'autorité d'adopter un résultat. |
| **Architecture, spécifications et modèles système** | ISO/IEC/IEEE 42010 ; SysML v2/KerML ; Architecture 0027 ; modèles TLA+ du cycle de vie et de la gouvernance. | Cible documentée ; certaines propriétés de transition sont vérifiées par model checking. | Aucun inventaire complet des constructions des modèles/architectures ni preuve de correspondance entre descriptions d'architecture, spécifications, implémentation et gouvernance du dépôt. |
| **Affirmations, arguments et éléments probants d'assurance** | SACM 2.3 comme base formelle ; SACM 2.4 Beta 1 comme cible ; recherches Assurance 2.0 et ACCESS ; Architecture 0021. | Formalisation partielle : épistémologie des éléments probants et tranche SACM Claim/Assertion/inférences. | Pas de couverture SACM complète, pas d'échange natif d'instances sans perte, pas de preuve que les affirmations en langage naturel sont fidèlement interprétées, ni de traitement formel complet des réfutations, évaluations, artefacts, terminologies, packages, vues et diagrammes. |
| **Épistémologie des éléments probants** | `Evidence.lean`, `Mapping.lean`, schéma JSON des éléments probants et modèle d'assurance. | Formalisé localement : classe de méthode, nature épistémique et statut du résultat sont distincts ; toute cible de nature preuve de théorème exige un terme de preuve exact. | Le schéma de production n'expose toujours pas de champ explicite de nature épistémique ni d'objet de dérivation typé. Les métadonnées de dépendances de preuve ne sont pas encore liées mécaniquement à la fermeture transitive complète du terme de preuve. |
| **Provenance et identité des artefacts** | Candidat famille PROV ; catalogue des artefacts ; liaison des révisions exactes des modèles source/cible en Lean ; Spécification 0007 du protocole VCS. | Formalisation partielle et cible documentée. | Pas de mapping PROV-O source prouvé, pas de conformité démontrée d'importateur/exportateur de production et pas de théorème complet de préservation/composition de la provenance au fil des transformations. |
| **Autorité, permissions et force normative** | Architecture 0023 ; modèles TLA+ de contrôle/applicabilité de la gouvernance ; candidats logique déontique et ODRL. | Modèles de transition de gouvernance existants, avec éléments de model checking borné. | Pas d'intégration sémantique complète entre autorité/délégation, modalités déontiques, modèles de politiques externes et décisions propres aux domaines. Un mapping ne doit jamais amplifier l'autorité. |
| **Cycle de vie, fraîcheur et invalidation des changements** | `GovCheckLifecycle.tla`, `GovCheckAssurance.tla`, modèles d'applicabilité/publication/contrôle/journal ; Spécifications 0006/0007. | Plusieurs modèles finis distincts ont été vérifiés par model checking. | Pas de preuve de raffinement/composition vérifiée par machine reliant les modèles TLA+ à la sémantique de mapping Lean ou à une implémentation de production. |
| **Représentation des ontologies et cohérence logique** | Recherches OWL 2, RDF, SKOS, SHACL et ODM ; étude de réemploi des ontologies. | Cible documentée et outils candidats. | Pas de couche sémantique commune épinglée, pas d'exécution de cohérence d'ontologie source enregistrée comme élément probant GovCheck, pas de théorème d'extension conservative/non-interférence et pas d'alignement inter-ontologies démontré. |
| **Qualité logicielle, tests, risques et chaîne d'approvisionnement** | ISO/IEC 25010, RAAML, UTP, SPDX, CycloneDX, NIST et modèles OMG d'ingénierie. | Candidats documentés de capacités spécialisées. | Pas d'inventaire formel de couverture de bout en bout ni de mappings démontrés pour ces modèles spécialisés. Ils doivent rester des capacités sémantiques distinctes plutôt que d'être réduits à des objets génériques d'exigence ou de preuve. |
| **Infrastructure de sémantique formelle** | Noyau Lean 4.19 ; paquet isolé de compatibilité CSLib ; TLA+/TLC. | Le noyau Lean et la compatibilité d'API/compilation CSLib ont des résultats distincts. | La compatibilité CSLib n'est pas une preuve de raffinement sémantique GovCheck↔CSLib. Aucun outil ni formalisme n'a été choisi comme moteur universel du métamodèle. |

## 4. Réutiliser les sources n'est pas les intégrer sémantiquement

L'étude de réemploi des ontologies du dépôt distingue correctement plusieurs familles d'artefacts :
- **ontologies/vocabulaires de domaine**, tels que SEON/ReqON et PROV-O ;
- **métamodèles**, tels que SACM, ReqIF et SysML ;
- **formats d'échange/sérialisation**, qui peuvent préserver la syntaxe sans préserver le sens ;
- **langages de contraintes/validation**, tels que SHACL ;
- **modèles de décision et de processus**, tels que DMN, BPMN et BMM ;
- **bibliothèques de preuve formelle**, telles que CSLib.

Ces familles ne sont pas des « ontologies » interchangeables. Leurs constructions, sémantiques, autorités, cycles de vie et règles de conformité diffèrent. GovCheck doit préserver chaque modèle source sous son identité/révision et son profil sémantique déclarés, puis ajouter des mappings explicites uniquement pour les relations effectivement justifiées.

En particulier :
- SEON/ReqON est un candidat de réemploi de grande valeur, pas encore une dépendance démontrée ni une ontologie complète de gouvernance de dépôt.
- SACM est une capacité spécialisée d'assurance, pas l'ensemble du métamodèle GovCheck.
- PEAK contribue un modèle d'examen des décisions ; ce n'est ni un métamodèle de dossier d'assurance ni un mécanisme d'autorisation.
- PROV décrit la provenance ; la provenance ne prouve ni vérité, ni suffisance, ni autorité.
- La cohérence OWL et la conformité SHACL répondent à des questions différentes de la préservation sémantique en Lean.
- CSLib apporte des sémantiques formelles réutilisables ; ce n'est pas un moteur d'alignement d'ontologies.

Voir l'[évaluation du réemploi des ontologies](metamodel-ontology-reuse-assessment.fr.md), l'[architecture des standards sémantiques de domaine](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.fr.md) et la [recherche sur l'assurance sémantique et les modèles de transition](semantic-assurance-and-transition-models-2026-11.fr.md).

## 5. Correction de la frontière formelle dans cette modification

### 5.1 Avant

L'ancien `SemanticBridge` comportait des constructeurs :
- `approximate`, qui acceptait une relation arbitraire et des chaînes de limites, sans établir de propriété de préservation ;
- `traceabilityOnly`, qui n'établissait aucune relation entre propositions ;
- `unsupported`, qui n'établissait aucune relation entre propositions.

Comme `EvidenceMapping` acceptait ces trois valeurs dans son champ `semanticBridge`, le système de types n'empêchait pas de prendre ces enregistrements pour des correspondances sémantiques opérationnelles.

L'ancien `KindMappingRule.transport` admettait aussi toute nature épistémique, y compris `theoremProof`, sans exiger de terme de preuve de la proposition cible.

### 5.2 Après

Le type de couverture opérationnelle est volontairement plus étroit :
- **equivalent :** preuve de `source ↔ target` ;
- **soundDirectional :** preuve de `source → target` ;
- **partialMapping :** domaine source déclaré et preuve que toute proposition source de ce domaine implique la proposition cible.

Le type de proposition conserve séparément :
- **approximate** ;
- **traceabilityOnly** ;
- **unsupported**.

Une proposition peut être enregistrée, étudiée, révisée ou rejetée. Ce n'est pas un `EvidenceMapping`, elle ne contient pas de `SemanticBridge` et ne peut pas être consommée par l'interface de mapping typée actuelle comme prémisse établie.

Une cible de nature `theoremProof` ne peut être construite que par `deriveTheoremProof`, qui transporte un terme de preuve de la proposition cible exacte. Le constructeur générique de transport de nature exclut explicitement `theoremProof`.

### 5.3 Ce que cela ne démontre toujours pas

- que la proposition Lean fournie pour une affirmation source est une interprétation fidèle de sa sémantique native ou en langage naturel ;
- que les implémentations de parseur/importateur/sérialiseur/exportateur ne construisent que des valeurs de mapping valides ;
- que les chaînes décrivant prémisses, hypothèses, identité/version du noyau correspondent à la fermeture complète des dépendances du terme de preuve ;
- que les mappings se composent tout en préservant leurs propriétés déclarées ;
- que la restriction de portée, la non-amplification de l'autorité et l'extension conservative tiennent pour des modèles arbitraires ;
- qu'un modèle TLA+ raffine un modèle Lean ou une implémentation de production ;
- qu'une ontologie ou un métamodèle complet est cohérent.

Le théorème prouve la proposition représentée par son type Lean sous le noyau de confiance Lean et les axiomes importés. Il n'authentifie pas automatiquement l'interprétation source, les données sources, l'autorité ou l'implémentation.

## 6. SACM 2.4 Beta 1 : tranche verticale actuelle et travail source restant

Le module existant `GovCheckCoherence.SACM24` formalise une tranche limitée, qualifiée par la vue source :
- le texte PDF et le métamodèle XML normatif restent des vues source distinctes ;
- la vue sélectionnée lie le format natif et le champ d'identité (`gid` versus `elementId`) ;
- les littéraux de déclaration propres à chaque vue sont contrôlés au lieu d'être fusionnés silencieusement ;
- `axiomatic` reste une déclaration, pas une preuve de théorème ;
- les inférences necessary, sufficient, necessary-and-sufficient et collective disposent de ponts formels orientés correctement ;
- `probable` ne dispose d'aucun pont d'implication classique ;
- l'identité du Claim et son sujet explicite sont liés à la révision exacte du modèle source.

Cela ne fournit **ni conformité complète à SACM 2.4 ni fidélité d'instances sources**. Le prochain travail spécifique à SACM doit épingler et comparer les artefacts officiels PDF/XML, résoudre les conflits restants de multiplicité/valeur/héritage, obtenir un fixture d'instance portable, puis seulement lier de vraies relations `AssertedInference`/`AssertedEvidence` et leurs indicateurs de contre-preuve.

## 7. Travaux résiduels priorisés

| Priorité | Travail | Condition de sortie |
|---|---|---|
| **P0** | Prouver que l'API de mapping ne peut admettre ni proposition sémantique non démontrée ni preuve de théorème fondée sur une simple étiquette. | Compilation Lean et audit des axiomes réussis sur l'API resserrée ; théorèmes négatifs couvrant la promotion d'un témoignage ou d'un résultat de model checking. |
| **P1** | Compléter une tranche verticale SACM réelle, issue de la source. | Fixture source épinglé, identité explicite du parseur/vue, mapping typé et obligations de preuve pour Claim, AssertedInference et AssertedEvidence ; champs/pertes non pris en charge rapportés. |
| **P1** | Spécifier le contrat intermodèles cycle de vie/assurance/autorité. | Relations exactes, direction, portée, hypothèses, autorité et révisions liées explicitement ; responsabilités TLA+ et Lean séparées ; composition/raffinement revendiqués uniquement lorsqu'ils sont démontrés. |
| **P2** | Auditer SEON/ReqON et les modèles d'exigences/architecture/décision construction par construction. | Révisions sources, licence et maturité établies ; matrice indiquant constructions préservées, transformées, non prises en charge et contradictoires ; chaque mapping opérationnel possède son obligation de preuve exacte. |
| **P2** | Définir la provenance des dépendances de preuve et des hypothèses. | Rapports de preuve liés à la fermeture transitive des dépendances, aux axiomes importés, au noyau/à la chaîne d'outils Lean et aux révisions exactes des modèles source/cible. |
| **P2** | Définir la composition des mappings et l'extension conservative. | Lois de composition et affirmations de non-interférence/conservativité précisément formulées et vérifiées par machine pour les profils déclarés. |
| **P3** | Décider du rôle de CSLib dans l'architecture de preuve. | Au moins une propriété utile du cycle de vie GovCheck est reliée à une formalisation CSLib épinglée par une relation démontrée ; sinon, conserver uniquement le réemploi isolé. |

## 8. Disposition et frontière d'autorité

Cet audit est un état de référence d'ingénierie et un livrable de recherche pour l'issue #73. Il :
- n'adopte pas un métamodèle GovCheck complet ;
- ne choisit pas CSLib, Lean, OWL, RDF ou une sérialisation comme technologie universelle ;
- ne revendique aucune conformité à SEON, SACM, ReqIF, SysML, PROV-O ou à un autre modèle externe ;
- ne transforme pas un mapping candidat non démontré en relation opérationnelle ;
- ne modifie pas l'autorité normative et ne ferme pas l'issue #73.

La correction actuelle restreint ce que le prototype Lean peut représenter comme mapping sémantique *opérationnel*. C'est une amélioration de sûreté de la frontière de preuve, pas une adoption normative du métamodèle plus large.

## 9. Références

- [R-20 — Lean et frontière du noyau de preuve](../references.fr.md#r-20)
- [R-34 — OMG SACM 2.3](../references.fr.md#r-34)
- [R-73 — OMG SACM 2.4 Beta 1](../references.fr.md#r-73)
- [R-74 — Modèle PEAK de décision de projet](../references.fr.md#r-74)
- [R-115 — Processus de cycle de vie ISO/IEC/IEEE 15288](../references.fr.md#r-115)
- [R-116 — Ingénierie des exigences ISO/IEC/IEEE 29148](../references.fr.md#r-116)
- [R-128 — Audit indépendant de l'impact d'implémentation SACM 2.4 Beta 1](../references.fr.md#r-128)
- [Évaluation du réemploi des ontologies et de CSLib](metamodel-ontology-reuse-assessment.fr.md)
- [Standards sémantiques de domaine, modèles de décision et engagements de bootstrap](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.fr.md)
- [Méthodes formelles et évaluation de la chaîne d'outils](metamodel-coherence-verification.fr.md)
