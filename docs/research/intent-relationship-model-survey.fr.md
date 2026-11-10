# Étude : relations formelles de l'intention à l'assurance

- **Statut :** analyse de recherche et de conception ; non normative.
- **Élément de travail :** [issue #73](https://github.com/Martin-PB/govcheck/issues/73).
- **Dépend de :** [ADR 0009 — document d'intention du dépôt et nomenclature canonique](../decisions/0009-intent-record-and-authority.fr.md).
- **Objet :** établir l'état de l'art académique et industriel et un vocabulaire candidat de relations avant toute adoption d'un métamodèle GovCheck.
- **Autorité :** ce rapport n'adopte aucune relation, cardinalité, propriété obligatoire, sérialisation, notation ou outil.

## 1. Conclusions principales

Les normes et travaux de recherche examinés ne fournissent **pas** un métamodèle universel de bout en bout couvrant l'intention du dépôt, les besoins des parties prenantes, objectifs/résultats, exigences, décisions, architecture/spécifications, implémentation, vérification/validation et assurance.

Ils proposent plutôt des modèles partiels complémentaires :

- les normes de cycle de vie décrivent des processus et échanges d'information ;
- les normes d'ingénierie des exigences définissent les informations, la dérivation, l'allocation et la traçabilité des exigences ;
- les méthodes orientées objectifs relient préoccupations et objectifs des parties prenantes aux exigences et alternatives opérationnelles ;
- les normes de description d'architecture relient parties prenantes, préoccupations, points de vue, modèles, correspondances et justifications architecturales ;
- les recherches sur la justification des décisions relient exigences, contraintes, hypothèses, alternatives, choix et conséquences ;
- les normes de modélisation et d'échange représentent des éléments de modèle et des relations typées ;
- les normes de dossiers d'assurance structurent affirmations, arguments, hypothèses, contexte et preuves ;
- les vocabulaires de provenance décrivent dérivation, attribution, activités, agents et invalidation ;
- les recherches sur la traçabilité montrent que la traçabilité pré-exigences et le maintien des liens entre artefacts évolutifs restent difficiles.

La conclusion la plus solide n'est donc pas « adopter la norme X comme graphe GovCheck ». C'est : **GovCheck a besoin d'un graphe de relations typées, plusieurs-à-plusieurs et versionnées, avec des sémantiques explicites, tout en permettant des profils et mappings externes spécialisés.**

Une arête générique `traces-to` ne suffit pas. Une chaîne linéaire rigide ne suffit pas non plus : les exigences peuvent provenir de lois, normes, risques, incidents ou contraintes d'architecture ; les décisions peuvent créer ou modifier des exigences ; les affirmations d'assurance peuvent concerner plusieurs niveaux ; les observations en exploitation peuvent contester des hypothèses antérieures.

## 2. Périmètre et terminologie

Cette étude considère les familles de concepts suivantes. Elles doivent rester distinctes, même si une méthode externe en regroupe certaines.

| Concept | Sens de travail dans cette étude |
|---|---|
| Intention | Déclaration durable de la raison d'être du dépôt, du problème/contexte, des frontières, parties prenantes ou bénéficiaires, résultats visés, hypothèses et questions ouvertes. |
| Besoin / attente d'une partie prenante | Préoccupation, besoin ou attente exprimé par une partie intéressée ; il peut être incomplet, contradictoire ou non validé. |
| But / objectif | État ou condition souhaité qui affine l'intention ; les objectifs peuvent être qualitatifs, contradictoires, décomposables ou seulement partiellement opérationnalisables. |
| Résultat | Effet ou résultat observable permettant d'évaluer la valeur ou la validité d'un objectif. |
| Exigence | Énoncé gouverné d'une capacité, condition, contrainte ou qualité nécessaire ; son origine peut être interne ou externe. |
| Décision | Sélection, interprétation, contrainte, report, exception ou modification autorisée parmi des alternatives, avec justification et conséquences. |
| Élément d'architecture | Composant, relation, frontière, interface, élément de déploiement ou autre élément de l'architecture du système. |
| Spécification | Description structurée des propriétés, comportements, interfaces ou contraintes requis ou visés. Son existence documentaire ne la rend pas automatiquement normative. |
| Propriété | Prédicat ou condition concernant un artefact, modèle, implémentation ou exécution, avec périmètre et hypothèses déclarés. |
| Implémentation / réalisation | Artefact ou activité concret destiné à réaliser une conception ou satisfaire une exigence. |
| Vérification / validation | Activités distinctes : la vérification évalue la conformité aux conditions spécifiées ; la validation évalue l'adéquation à l'usage visé et aux résultats attendus par les parties prenantes. |
| Affirmation d'assurance | Assertion concernant un système, processus, propriété ou état de gouvernance et nécessitant un argument adapté à sa nature. |
| Argument / justification | Raisonnement qui explique, justifie, décompose ou conteste une décision ou une affirmation d'assurance. |
| Élément d'évidence | Artefact ou observation utilisé pour étayer ou contester une assertion. Un résultat de test est un témoignage/élément d'évidence, pas une preuve ; le model checking est une évidence de validation de modèle, pas une preuve de théorème. |
| Provenance | Information sur qui/quoi a produit, modifié, dérivé, révisé ou invalidé un artefact ou une assertion, quand et à partir de quelles entrées. |

Un même mot peut avoir des sens différents selon les méthodes. Le métamodèle GovCheck devra définir ses propres termes et mappings plutôt que supposer qu'une homonymie implique une équivalence sémantique.

## 3. Résultats académiques et industriels

### 3.1 Cycle de vie et ingénierie des exigences

**ISO/IEC/IEEE 15288:2023** fournit un cadre de processus du cycle de vie, de la conception au retrait, applicable de manière itérative et récursive. Elle ne prescrit ni modèle de cycle de vie unique ni structure documentaire de dépôt. Elle confirme que exigences, réalisation, vérification, validation et exploitation appartiennent au cycle de vie entier, pas à une séquence ponctuelle.

**ISO/IEC/IEEE 29148:2018** fournit des processus et éléments d'information d'ingénierie des exigences. Sa pertinence porte notamment sur la dérivation, l'allocation, la validation, la vérification et la traçabilité des exigences. Le DIS de troisième édition visible en 2026 est un projet en enquête, pas une norme internationale adoptée.

Le **NASA Systems Engineering Handbook** rend explicites attentes des parties prenantes, ConOps, exigences, décisions de conception, vérification et validation et insiste sur la traçabilité bidirectionnelle. Il soutient la navigation ascendante et descendante, les contrôles de cohérence et la réconciliation itérative, plutôt qu'une transformation à sens unique.

Les recherches sur la **traçabilité pré-exigences** sont particulièrement pertinentes. La revue systématique de Mucha, Kaufmann et Riehle publiée en 2024 examine 77 articles de 1992 à 2022 et identifie les liens entre exigences et origines, par exemple entretiens de parties prenantes, comptes rendus de réunion et systèmes historiques. Les auteurs signalent que ce domaine a reçu moins d'attention que la traçabilité postérieure aux exigences. C'est un avertissement direct contre un graphe qui commencerait seulement au nœud « exigence ».

Une autre revue systématique de 2018 sur les technologies de traçabilité des exigences analyse 114 articles (2006–2016), évalue 83 études empiriques et identifie dix défis ainsi que plusieurs catégories de technologies. Elle confirme que la traçabilité est une capacité difficile du cycle de vie, qui exige une méthode explicite et évaluée, et pas simplement des hyperliens.

### 3.2 Objectifs, intention et résultats

Les approches d'ingénierie des exigences orientée objectifs (**GORE**) telles que **KAOS, iStar, GRL et Tropos** partagent des capacités : objectifs, raffinements ET/OU, tâches ou opérationnalisation, acteurs et dépendances. Elles diffèrent par leurs priorités : définition formelle des objectifs, objectifs qualitatifs/softgoals, dépendances entre acteurs et raisonnement orienté agents.

La réflexion 2026 sur la cartographie systématique de 246 publications GORE relève à la fois des capacités de modélisation communes et des obstacles persistants à l'adoption industrielle, ainsi qu'une évaluation empirique inégale. GovCheck doit donc étudier et mapper sélectivement ces concepts, sans imposer une notation GORE particulière.

Cette recherche soutient au moins trois relations distinctes :
- l'intention motive ou cadre les objectifs ;
- les objectifs se raffinent en sous-objectifs et peuvent être opérationnalisés par des exigences/tâches ;
- les résultats fournissent une base pour évaluer si les objectifs ont été atteints.

Un objectif n'est pas automatiquement une exigence ; une exigence n'est pas automatiquement un résultat mesurable. Les objectifs qualitatifs et contradictoires doivent rester représentables.

### 3.3 Architecture, spécification et justification des décisions

**ISO/IEC/IEEE 42010:2022** spécifie la structure et l'expression des descriptions d'architecture. Elle distingue l'architecture elle-même de sa description et définit des concepts et relations entre parties prenantes, préoccupations, points de vue, vues, types de modèles et correspondances. Elle reconnaît également les justifications architecturales et les décisions, mais ne prescrit ni méthode de modélisation, ni notation, ni processus, ni format de stockage.

**SysML v2** est une source candidate de relations typées entre exigences, structure, comportement, analyse et vérification. C'est un langage de modélisation des systèmes, pas un métamodèle de gouvernance de dépôt.

**ReqIF 1.2** fournit un format normalisé d'échange des exigences et un schéma lisible par machine. Il est utile pour échanger objets d'exigence, relations et attributs associés, mais ne définit pas les sémantiques complètes de l'intention, de l'autorité ou du cycle de vie d'assurance GovCheck.

Les recherches sur les décisions d'architecture sont particulièrement importantes, car les décisions ne sont pas simplement une étape après les exigences :
- le modèle AREL (Architecture Rationale and Elements Linkage) relie exigences, contraintes et hypothèses aux éléments d'architecture au moyen des décisions et justifications, pour soutenir l'analyse d'impact ;
- les travaux formels sur la sémantique des décisions d'architecture identifient des relations explicites entre éléments de décision ;
- les études empiriques rapportent que les praticiens valorisent les justifications de conception mais rencontrent des obstacles à leur capture systématique ;
- un cadre de 2024 sur les caractéristiques, spécifications et preuves de conception souligne que raisons, alternatives, compromis et argumentation font partie de la justification.

Cela soutient la représentation d'une décision comme objet avec contexte, alternatives, sélection, justification, autorité, conséquences et liens vers les artefacts affectés. Une décision peut satisfaire, contraindre, réinterpréter, différer, déroger ou créer des exigences. Ce n'est pas simplement une arête entre une exigence et une spécification.

### 3.4 Dossiers d'assurance et éléments d'évidence

**OMG SACM 2.3** fournit un métamodèle normalisé pour affirmations, argumentation, références d'artefacts, preuves, contexte et raisonnement. **GSN v3** fournit un standard communautaire de structuration des arguments d'ingénierie, notamment objectifs/affirmations, stratégies, contextes, hypothèses, justifications et solutions/éléments d'évidence.

Ces structures d'assurance sont complémentaires, pas des métamodèles complets du cycle de vie. GovCheck ne doit pas déduire qu'un élément d'évidence prouve une affirmation du seul fait qu'un lien existe. Argument, méthode, périmètre, hypothèses, provenance, fraîcheur et réfutation éventuelle restent pertinents.

L'assurance n'est pas non plus simplement le dernier nœud d'une chaîne linéaire. Des affirmations peuvent concerner l'adéquation de l'intention, la couverture des exigences, l'acceptabilité d'une décision, les propriétés d'architecture, le comportement de l'implémentation, la performance opérationnelle ou le processus de gouvernance lui-même.


### 3.6 Mesure des objectifs et qualité du produit

Le paradigme **Goal-Question-Metric (GQM)** fournit une méthode rigoureuse pour relier les objectifs à des questions qui opérationnalisent l'évaluation, puis à des mesures/observations interprétées dans leur contexte. Il soutient l'observabilité des résultats sans réduire chaque objectif à un KPI universel : questions et modèle de mesure doivent dériver de l'objectif et du contexte.

**ISO/IEC 25010:2023** fournit un modèle de qualité du produit dont les caractéristiques peuvent éclairer exigences qualité, objectifs de conception, objectifs de test, critères qualité, critères d'acceptation et mesures sur le cycle de vie. C'est une taxonomie de qualité, pas un modèle d'objectifs ; les caractéristiques doivent être sélectionnées et interprétées pour le produit et ses parties prenantes.

### 3.7 L'ingénierie de sécurité comme test du modèle de relations

**NIST SP 800-160 Vol. 1 Rev. 1** traite l'ingénierie de sécurité des systèmes comme une discipline du cycle de vie reliant besoins de protection et préoccupations des parties prenantes aux exigences de sécurité, risques, architecture/conception, implémentation, vérification, validation et assurance. C'est un test de résistance utile pour GovCheck car les exigences de sécurité peuvent dériver des menaces, risques et contextes opérationnels, pas uniquement de l'intention produit. Le modèle de relations doit préserver ces origines et les décisions d'autorité/risque qui acceptent ou traitent ces risques.

### 3.8 Processus d'architecture, éléments d'information et gestion de configuration

**ISO/IEC/IEEE 42020:2019** complète ISO 42010 en définissant les processus de gouvernance/gestion d'architecture et d'architecture tout au long du cycle de vie architectural. Les décisions et changements d'architecture deviennent ainsi des activités de cycle de vie de premier rang.

**ISO/IEC/IEEE 15289:2019** spécifie la finalité et le contenu des éléments d'information du cycle de vie. Elle organise ces éléments par types génériques de documents et par finalité, sans définir de nom de fichier ni de support universel. C'est pertinent pour la séparation GovCheck entre identité sémantique d'un artefact et nom de fichier : un nom canonique est une convention du dépôt, pas automatiquement une exigence dérivée d'une norme. L'édition 2019 a été confirmée courante en 2025, tandis qu'un projet de révision est actif.

**ISO 10007:2017** fournit des lignes directrices de gestion de configuration de la conception au retrait, notamment identification de configuration, maîtrise des modifications, comptabilisation d'état et audit. Cela soutient la liaison des relations, spécifications et éléments d'évidence à des baselines et révisions explicites, tout en préservant l'historique des changements.

### 3.5 Échange de relations et provenance

**OASIS OSLC Requirements Management 2.1** représente les relations vers d'autres ressources comme des propriétés/triples RDF. Cela démontre l'intérêt de prédicats explicites et de liens de ressources interopérables, tout en restant une spécification d'intégration pour les ressources de gestion des exigences, pas une sémantique complète de la gouvernance du cycle de vie.

**W3C PROV-O** fournit des classes et propriétés de provenance pour entités, activités et agents, notamment dérivation, attribution, association, génération, usage et invalidation. C'est une couche de provenance utile. Il ne faut pas la confondre avec les sémantiques métier des objectifs, exigences, décisions ou affirmations d'assurance.

Ces sources suggèrent de séparer :
1. la relation métier (par exemple, une exigence dérive d'un objectif) ;
2. la provenance de l'assertion selon laquelle cette relation existe (qui l'a affirmée, à partir de quelle source et avec quelle méthode) ;
3. l'applicabilité temporelle de cette relation à une révision du dépôt ou de gouvernance.


### 3.9 Ingénierie de la sûreté et dossiers de sécurité

Les pratiques de sécurité fonctionnelle fournissent un autre exemple fort de cycle de vie. Le guide du Health and Safety Executive britannique décrit la dérivation d'exigences de réduction du risque à partir de l'analyse des dangers/risques, leur allocation à des systèmes instrumentés de sécurité ou autres mesures, la spécification et la conception du système, sa validation, puis son exploitation, sa maintenance, sa modification et son retrait. Il montre pourquoi les relations d'origine, allocation, vérification/validation et changement opérationnel doivent être connectées. Ce domaine est spécialisé et ne doit pas devenir un processus obligatoire pour tout dépôt logiciel.

Une revue systématique de 2021 portant sur **51 articles de dossiers d'assurance de sécurité** constate que ces dossiers structurent arguments et éléments d'évidence pour raisonner sur la posture de sécurité d'un système, mais que le soutien aux praticiens, la validation et l'outillage restent immatures. Cela avertit que l'existence d'une notation GSN/SACM ne résout pas à elle seule la construction ou la maintenance des dossiers d'assurance.

### 3.10 Alignement des objectifs au-delà d'un dépôt unique

**GQM+Strategies** étend le raisonnement Goal-Question-Metric en explicitant les liens entre objectifs organisationnels, stratégies, objectifs logiciels, facteurs contextuels, hypothèses, scénarios et objectifs de mesure. C'est pertinent lorsqu'un dépôt contribue à un système ou une finalité organisationnelle plus large. GovCheck ne doit pas supposer que chaque dépôt possède une hiérarchie d'objectifs commerciaux ; les concepts transférables utiles sont l'explicitation du contexte, des hypothèses et de l'alignement traçable des objectifs.

## 4. Familles de relations candidates

Le vocabulaire suivant est une proposition de recherche à discuter, pas un vocabulaire GovCheck adopté. Les noms et directions ne doivent être finalisés qu'après analyse sémantique et exemples.

| Famille | Relation candidate | Source → cible typiques | Sens et précautions |
|---|---|---|---|
| Motivation | `motivates` | Intention / besoin → objectif | La source donne finalité ou raison de l'objectif ; n'implique pas son adoption. |
| Décomposition | `refines` | Objectif → sous-objectif ; exigence → sous-exigence | Précise ou décompose le sens ; une acyclicité peut être exigée dans une hiérarchie de raffinement. |
| Opérationnalisation | `operationalizedBy` | Objectif → exigence / tâche / capacité opérationnelle | Indique comment poursuivre un objectif ; ne prouve pas sa réalisation. |
| Origine / dérivation | `derivedFrom` | Exigence → objectif / besoin / règlement / risque / norme / incident / décision | Enregistre l'origine ; plusieurs origines sont permises et les origines externes ne passent pas nécessairement par l'intention. |
| Allocation | `allocatedTo` | Exigence → élément d'architecture / sous-système | Attribue responsabilité ou périmètre ; n'établit pas la satisfaction. |
| Décision | `addresses` | Décision → préoccupation / exigence / risque / objectif | Indique ce à quoi répond la décision. |
| Sélection | `selects` / `rejects` | Décision → alternative | Enregistre alternatives sélectionnées et rejetées ; alternatives et compromis doivent rester identifiables. |
| Contrainte | `constrains` | Décision / contrainte → spécification / élément d'architecture | Limite les choix de conception permis ; autorité et applicabilité doivent être explicites. |
| Justification | `justifiedBy` | Décision → justification / argument | Relie le choix au raisonnement, aux preuves, hypothèses et conséquences. |
| Spécification | `specifiedBy` | Exigence / propriété → élément de spécification | Indique où une exigence/propriété est décrite ; ne prouve pas l'implémentation. |
| Réalisation | `realizedBy` | Exigence / spécification → implémentation / élément système | Identifie une réalisation prévue ; la satisfaction reste évaluée séparément. |
| Satisfaction | `satisfiedBy` | Exigence / propriété → implémentation / élément système | Affirme une relation de satisfaction avec un statut d'évaluation défini ; ne doit pas être déduite de la seule réalisation. |
| Vérification | `verifiedBy` | Exigence / propriété / spécification → cas / méthode / résultat de vérification | Contrôle la conformité aux conditions spécifiées ; méthode et résultat sont distincts. |
| Validation | `validatedBy` | Objectif / résultat / usage prévu → cas de validation / observation | Évalue l'adéquation à l'usage prévu ou l'atteinte des résultats ; n'est pas interchangeable avec la vérification. |
| Décomposition d'assurance | `decomposedInto` | Affirmation → sous-affirmations | Structure un argument d'assurance ; les sémantiques dépendent du profil d'assurance retenu. |
| Soutien par évidence | `supportedBy` | Affirmation → argument / élément d'évidence | Enregistre un soutien dans un périmètre déclaré ; l'existence du lien n'est pas une preuve. |
| Contestation | `challengedBy` | Affirmation / décision → contre-argument / contre-évidence | Préserve réfutations et éléments invalidants au lieu de cacher les contradictions. |
| Hypothèse | `dependsOnAssumption` | Affirmation / décision / modèle → hypothèse | Rend explicite le caractère conditionnel ; les hypothèses peuvent être contestées ou invalidées. |
| Provenance | `generatedBy`, `derivedFrom`, `attributedTo` | Artefact / assertion → activité / entrée / agent | Enregistre production et dérivation ; mapping possible vers PROV-O. |
| Changement temporel | `invalidatedBy`, `supersededBy` | Relation / artefact → événement de changement / successeur | Préserve la vérité historique et enregistre l'applicabilité prospective ; ne supprime jamais silencieusement l'historique. |

### 4.1 Familles de relations à ne pas confondre

- `realizedBy` n'est pas `satisfiedBy`.
- `satisfiedBy` n'est pas `verifiedBy`.
- `verifiedBy` n'est pas `validatedBy`.
- `supportedBy` n'est pas `provedBy`.
- `justifiedBy` n'est pas `authorizedBy`.
- `derivedFrom` n'est pas `approvedBy`.
- `tracesTo` peut être utile pour la navigation, mais ne remplace pas un prédicat sémantique typé.

## 5. Enregistrement de relation candidat

Une relation peut nécessiter sa propre identité et ses métadonnées, plutôt qu'un hyperlien sans qualification. Champs candidats à étudier :

- identifiant stable de relation et type de relation ;
- identités du sujet et de l'objet, avec types déclarés ;
- révisions du dépôt/de gouvernance du sujet et de l'objet ;
- statut de l'assertion (proposée, acceptée, rejetée, contestée, invalidée, remplacée) ;
- auteur/agent ayant formulé l'assertion, fondement d'autorité et événement d'approbation lorsque requis ;
- source de provenance, méthode et justification ;
- intervalle de validité ou condition d'applicabilité ;
- périmètre, hypothèses, qualificatifs et confiance/incertitude si pertinent ;
- preuve ou argument soutenant l'assertion ;
- événement de changement et historique de remplacement/invalidation.

Le statut d'une assertion relationnelle ne doit pas être confondu avec le statut de ses extrémités. Une exigence peut rester acceptée alors qu'une allocation proposée est rejetée ; une décision peut rester historiquement valide alors que son applicabilité courante est remplacée.

## 6. Propriétés et contraintes globales candidates

Ces éléments sont des hypothèses à formaliser ultérieurement, pas des invariants adoptés :

1. **Extrémités typées :** chaque type de relation définit les types source et cible permis.
2. **Origine explicite :** chaque exigence acceptée possède une classe d'origine et une origine traçable, ou une déclaration explicite indiquant que l'origine est inconnue ou non résolue.
3. **Complétude des décisions :** une décision acceptée identifie préoccupation/contexte, autorité, résultat, justification et artefacts affectés ; la profondeur de l'analyse des alternatives peut être proportionnée et doit être déclarée.
4. **Aucune implication sémantique par simple proximité :** réalisation n'implique pas satisfaction ; satisfaction n'implique pas vérification ; vérification n'implique pas validation ; soutien par évidence n'implique pas preuve.
5. **Séparation de l'autorité :** une relation ou un élément d'évidence ne peut conférer une autorité par sa seule existence.
6. **Liaison à une révision :** les affirmations de satisfaction, vérification, validation et assurance sont liées à une révision exacte du sujet, à une méthode et à un périmètre d'entrées.
7. **Préservation historique :** invalidation et remplacement sont enregistrés comme nouveaux événements ; les relations antérieurement acceptées restent consultables.
8. **Propagation d'impact :** la modification d'un objet amont déclenche une analyse d'impact de ses descendants pertinents, mais n'invalide pas automatiquement tous les descendants sans règles propres aux relations.
9. **Complétude par profil :** les liens requis dépendent du type d'objet, du profil d'assurance, du risque et du contexte de cycle de vie ; aucune règle universelle de complétude tous-vers-tous.
10. **Règles de cycle propres aux relations :** certaines relations (décomposition/raffinement, par exemple) peuvent exiger l'acyclicité ; le graphe global ne doit pas être supposé acyclique car dépendances et justifications peuvent légitimement former des cycles.
11. **Navigation bidirectionnelle :** chaque relation affirmée est navigable depuis ses deux extrémités, avec la même identité et les mêmes sémantiques.
12. **Provenance des assertions :** le système distingue une relation affirmée d'une relation candidate inférée ou produite par un outil.

## 7. Contre-exemples et scénarios indispensables

Un modèle complet doit gérer au moins les cas suivants :

- Une exigence dérive directement d'un règlement ou d'une norme externe, sans chemin direct intention-exigence.
- Une exigence de sécurité dérive d'une analyse de menace/risque ou d'une observation d'incident.
- Un objectif est opérationnalisé par plusieurs exigences ; une exigence contribue à plusieurs objectifs.
- Deux objectifs entrent en conflit et une décision sélectionne un compromis en enregistrant alternatives rejetées et risque résiduel accepté.
- Une décision crée une nouvelle contrainte ou exigence au lieu de simplement résoudre une exigence existante.
- Une exigence est allouée à plusieurs éléments d'architecture ; un élément contribue à plusieurs exigences.
- Une spécification décrit une exigence, mais l'implémentation ne la réalise pas encore.
- Une implémentation réalise une exigence, mais la vérification échoue.
- Un test réussit, mais ne valide pas le résultat visé.
- Une preuve formelle couvre un modèle abstrait, pas l'implémentation.
- Un résultat de model checking valide un modèle borné sous hypothèses, mais ne prouve ni un théorème ni un raffinement d'implémentation.
- Une affirmation d'assurance est soutenue par une évidence qui devient périmée ou est contestée par un incident en production.
- Une relation est valide pour une révision de gouvernance et pas pour une autre.
- Un graphe de dépendances contient un cycle tandis que son sous-graphe de raffinement reste acyclique.
- Une décision acceptée est prise par l'autorité compétente sans revue indépendante sous un régime à autorité unique ; le risque résiduel doit rester visible.

## 8. Mappings externes et limites

| Modèle externe | Mapping potentiel | Ce qu'il ne fournit pas |
|---|---|---|
| ISO 29148 | Exigences, dérivation, allocation, traçabilité de vérification/validation | Sémantiques complètes du graphe intention/décision/assurance |
| GORE (KAOS/iStar/GRL/Tropos) | Objectifs, raffinements, tâches, acteurs, dépendances, softgoals | Gouvernance universelle de dépôt, autorité et assurance |
| ISO 42010 | Parties prenantes, préoccupations, points de vue, vues, modèles, correspondances, justification d'architecture | Processus d'architecture ou format de dépôt imposé |
| SysML v2 | Exigences et relations de modèles système | Modèle d'autorité et de provenance GovCheck |
| ReqIF | Échange d'objets d'exigence et d'attributs | Sémantiques d'intention et d'assurance, autorité des décisions |
| OSLC RM | Liens inter-ressources et intégration d'outils du cycle de vie | Sémantique complète des relations hors domaine RM |
| SACM / GSN | Affirmations, structures d'argument, contexte, hypothèses, évidence | Dérivation amont complète et traçabilité d'implémentation |
| PROV-O | Provenance entité/activité/agent, dérivation et invalidation | Sens métier des exigences, décisions ou affirmations d'assurance |

Un profil de mapping doit déclarer équivalence sémantique, sens plus étroit/large, constructions non prises en charge et pertes d'information. La compatibilité de sérialisation n'est pas une compatibilité sémantique.

## 9. Séquence de conception proposée

1. Stabiliser un glossaire et les frontières conceptuelles.
2. Extraire les sémantiques exactes des relations de chaque source externe et noter accords et divergences.
3. Définir les types de nœuds et signatures de relations candidates, avec cardinalités et qualificatifs temporels.
4. Définir statut/autorité/provenance comme dimensions orthogonales, pas comme étiquettes relationnelles surchargées.
5. Définir profils de complétude et conditions diagnostiques.
6. Créer des scénarios de conformité positifs et négatifs.
7. Modéliser les contrats essentiels de cycle de vie et d'assurance dans un formalisme adapté, choisi selon les affirmations et sans imposer un outil.
8. Comparer les mappings externes et exécuter des tests de détection des pertes.
9. Proposer seulement ensuite une spécification GovCheck et une décision d'architecture à soumettre au propriétaire.

## 10. Limites de la recherche

Cette étude est une revue ciblée, pas une revue systématique de toutes les bases bibliographiques pertinentes. Elle utilise des normes sélectionnées, spécifications officielles, revues systématiques et études évaluées par les pairs identifiées comme directement pertinentes. La prochaine itération devra élargir la recherche à la théorie de la décision, la mesure des objectifs/résultats, l'ingénierie de sécurité, l'assurance de cybersécurité, la provenance des données, la gestion de configuration, l'ingénierie système basée sur les modèles et les pratiques de gestion de produit.

Aucune relation ou propriété candidate de ce document n'est normative. Aucun format externe n'est choisi comme sérialisation canonique GovCheck. Aucun raffinement formel ou assurance d'implémentation n'est revendiqué.

## Reference catalogue links

- [R-114](../references.fr.md#r-114)
- [R-115](../references.fr.md#r-115)
- [R-116](../references.fr.md#r-116)
- [R-117](../references.fr.md#r-117)
- [R-118](../references.fr.md#r-118)
- [R-119](../references.fr.md#r-119)
- [R-120](../references.fr.md#r-120)
- [R-121](../references.fr.md#r-121)
- [R-123](../references.fr.md#r-123)
- [R-124](../references.fr.md#r-124)
- [R-125](../references.fr.md#r-125)
- [R-126](../references.fr.md#r-126)
- [R-127](../references.fr.md#r-127)
- [R-128](../references.fr.md#r-128)
- [R-129](../references.fr.md#r-129)
- [R-130](../references.fr.md#r-130)
- [R-131](../references.fr.md#r-131)
- [R-132](../references.fr.md#r-132)
- [R-133](../references.fr.md#r-133)
- [R-134](../references.fr.md#r-134)
- [R-135](../references.fr.md#r-135)
- [R-136](../references.fr.md#r-136)
- [R-137](../references.fr.md#r-137)
- [R-138](../references.fr.md#r-138)
- [R-139](../references.fr.md#r-139)
- [R-140](../references.fr.md#r-140)
- [R-141](../references.fr.md#r-141)

## 11. Évaluation de la couverture et lacunes restantes

### 11.1 Carte de couverture

| Préoccupation | Principales sources couvertes | Évaluation |
|---|---|---|
| Intention du dépôt et contexte d'origine | Pratique d'intention Anthropic ; attentes des parties prenantes NASA ; revue de traçabilité pré-exigences | Bonne couverture conceptuelle ; le nom de fichier n'est pas une norme normative. |
| Processus de cycle de vie et éléments d'information | ISO 15288, 42020, 15289 | Bonne couverture des processus/documentation ; pas de métamodèle unifié du graphe. |
| Objectifs et résultats | GORE ; GQM ; GQM+Strategies ; ISO 25010 | Méthodes candidates bien couvertes ; évaluation des résultats dépend du contexte. |
| Exigences et traçabilité | ISO 29148 ; ReqIF ; OSLC RM ; revues de traçabilité | Couverture normative et académique forte ; maintenance automatisée et traçabilité pré-exigences restent difficiles. |
| Architecture et spécifications | ISO 42010/42020 ; SysML v2 | Bonne couverture des descriptions d'architecture et modèles ; pas de sémantique de gouvernance de dépôt. |
| Décisions et justifications | Guide ADR britannique ; AREL ; sémantique formelle des décisions ; cadre de justification de conception | Approches complémentaires multiples ; pas de métamodèle décisionnel universel unique. |
| Assurance et éléments d'évidence | SACM ; GSN ; NIST SSE ; revue des dossiers d'assurance de sécurité ; guide de sécurité fonctionnelle | Bonne couverture spécialisée ; outillage de construction/maintenance des dossiers encore immature. |
| Provenance et applicabilité temporelle | PROV-O ; lignes directrices de gestion de configuration | Bons concepts de provenance/configuration ; mapping vers autorité et révisions du dépôt à définir par GovCheck. |
| Qualité, risque et sécurité | ISO 25010 ; NIST SP 800-160 ; cycle de vie de sécurité fonctionnelle | Bons exemples de qualité/sécurité ; profils propres aux domaines nécessaires. |

### 11.2 Domaines encore insuffisamment couverts

Le corpus actuel est assez large pour dériver un modèle candidat de relations, mais il ne constitue **pas une revue systématique exhaustive de la littérature**. Les lacunes restantes comprennent :

- théorie formelle de la décision, analyse multicritère, ingénierie de la valeur et calcul explicite des compromis ;
- facteurs humains, conception centrée utilisateur, accessibilité et participation des parties prenantes au-delà du ConOps d'ingénierie des systèmes ;
- confidentialité, gouvernance des données, assurance des systèmes IA/agents et assurance de la chaîne d'approvisionnement logicielle ;
- autres domaines de sûreté (ferroviaire, aéronautique, dispositifs médicaux, nucléaire) et relations de certification/assurance propres à ces secteurs ;
- obligations légales/réglementaires et sémantique des sources normatives externes ;
- pratiques de gestion de produits/services pour dépôts non commerciaux, de recherche, d'infrastructure et internes ;
- ingénierie système basée sur les modèles au-delà de SysML v2, y compris cadres d'architecture et profils web sémantique/données liées ;
- sémantique formelle des assertions relationnelles, raisonnement défaisable, incertitude, contraintes déontiques et changements d'autorité.

La prochaine passe de recherche devra sélectionner ces domaines en fonction de la portée généraliste de GovCheck, identifier sources primaires et revues systématiques, et consigner pourquoi un domaine est inclus, reporté ou hors périmètre. Il ne s'agit pas de collecter indistinctement toutes les normes sectorielles.

### 11.3 Méthode de recherche et d'inclusion

Il s'agit d'une recherche ciblée interdisciplinaire, pas d'une revue systématique enregistrée. Les domaines recherchés comprennent ingénierie du cycle de vie, traçabilité des exigences, GORE, description/processus d'architecture, justification des décisions, dossiers d'assurance, provenance, gestion de configuration, mesure de la qualité, ingénierie de sécurité et sûreté fonctionnelle. Les sources ont été priorisées dans cet ordre : normes courantes et spécifications officielles ; guides officiels gouvernementaux/agences ; revues systématiques de littérature ; recherches évaluées par les pairs ; enfin documents de pratique industrielle lorsqu'ils éclairent directement la question du document d'intention.

La recherche suffit à montrer qu'aucune norme externe unique ne couvre le graphe complet des relations et à identifier les grandes familles complémentaires. Elle ne suffit pas à revendiquer une couverture exhaustive de toutes les disciplines pertinentes ou normes propres à chaque domaine.
