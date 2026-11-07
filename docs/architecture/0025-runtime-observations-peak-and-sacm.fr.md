# 0025 — Observations en production, traçabilité des décisions PEAK et étude de SACM

**Statut :** étude et recommandation d'architecture soumises à revue ; ce document n'implémente ni pipeline d'observations en production, ni moteur de décision PEAK, ni sérialiseur SACM, ni mise à jour opérationnelle du modèle de menace.  
**Langue :** le français est présenté ici ; voir la [version anglaise](0025-runtime-observations-peak-and-sacm.md).

## 1. Conclusion exécutive

GovCheck devrait relier les observations de production, l'évolution du modèle de menace, les arguments d'assurance et les décisions gouvernées sur le risque au moyen d'un modèle sémantique commun et typé. PEAK et SACM sont des apports complémentaires, pas des ontologies concurrentes :

- **PEAK** est une grille d'analyse de décision : Problem, Experience, Assumptions et Knowledge sont examinés comme entrées d'un processus de décision ; celui-ci produit une solution et un risque assumé [R-74](../references.fr.md#r-74).
- **SACM** est un métamodèle structuré de dossier d'assurance pour les affirmations, l'argumentation, les références aux preuves, les artefacts et la terminologie [R-34](../references.fr.md#r-34).
- **GovCheck** doit conserver les sémantiques métier que ni PEAK ni SACM ne fournissent seuls : menaces, chemins d'attaque, contrôles, observations opérationnelles, fraîcheur des preuves, traitement du risque, autorité et décisions d'acceptation.

**Recommandation :** ne faire de PEAK ni de SACM l'ontologie canonique de gouvernance de GovCheck. Utiliser PEAK comme vue de projection des décisions gouvernées. Utiliser SACM comme représentation candidate d'interopérabilité et de dossier d'assurance, avec un profil/une extension GovCheck et un mapping qui préserve les pertes éventuelles. Conserver SACM 2.3 comme base formelle actuelle de compatibilité tout en évaluant la bêta 2.4 ; ne pas figer le modèle interne sur cette bêta.

Une observation peut modifier ce que nous savons du système et remettre en cause une hypothèse ; elle ne prouve pas à elle seule une attaque, n'établit pas un scénario de menace, ne détermine pas l'acceptabilité du risque et n'autorise pas une mesure de mitigation.

## 2. Fondations GovCheck existantes

Cette proposition doit étendre les concepts existants, pas les dupliquer :

- L'architecture 0013 distingue déjà objectifs, exigences, normes, propriétés, contrats, modèles, artefacts d'implémentation, méthodes, témoins/éléments probants, affirmations, arguments et décisions/autorité. Elle impose des relations typées plutôt que des inférences fondées sur la proximité documentaire.
- La spécification 0005 et le schéma proposé d'enregistrement des preuves séparent l'enregistrement d'une preuve de l'affirmation qu'il peut étayer/réfuter, de l'argument qui l'interprète et de la décision d'acceptation. Un enregistrement lie une observation, une exécution ou une dérivation à des sujets exacts, une méthode, un contexte, une provenance, des limites et des dépendances d'invalidation.
- L'architecture 0021 définit affirmations, arguments, preuves, hypothèses, dépendances et décisions ; elle distingue le résultat d'une preuve de son admissibilité, de sa fraîcheur et de son authenticité. Elle impose de conserver les preuves historiques immuables et de créer de nouvelles observations lors d'une revalidation.
- L'architecture 0017 distingue un élément probant/une observation comme instance/événement immuable, et non comme artefact logique versionné en SemVer.
- L'architecture 0006 fournit les fondations du modèle de menace et de confiance ; l'architecture 0024 introduit l'assurance guidée par les menaces et le traitement des risques.

Ces fondations apportent déjà une grande partie du substrat sémantique nécessaire. Le lien manquant le plus important est un cycle de vie de l'observation opérationnelle de première classe et une projection explicite des entrées et sorties de décision.

## 3. PEAK : traçabilité des décisions, pas une nouvelle ontologie d'assurance

Le modèle de décision PEAK présenté par Hoover, Rosso-Llopart et Taran identifie quatre dimensions d'entrée :

| Élément PEAK | Signification | Projection GovCheck |
|---|---|---|
| **P — Problem** | Le problème à résoudre, avec exigences et contraintes | Question de décision, système/actif concerné, intérêts des parties prenantes, périmètre, objectifs et contraintes |
| **E — Experience** | Compétences et expérience apportées à la décision | Incidents antérieurs pertinents, historique opérationnel, retours d'expérience, expertise et provenance/contexte de ces éléments |
| **A — Assumptions** | Prémisses acceptées pour la décision | Enregistrements d'hypothèses explicites, avec responsable, périmètre, justification, confiance, validité, possibilité de surveillance et conditions de réfutation/réexamen |
| **K — Knowledge** | Environnement et faits disponibles pour les décideurs | Faits d'architecture/configuration versionnés, normes, renseignement sur les menaces, observations et preuves admissibles |

Le processus produit au minimum :
- **Solution :** l'alternative retenue, le plan d'action/de mise en œuvre, les alternatives rejetées et la justification.
- **Assumed risk / risque assumé :** l'exposition et l'incertitude acceptées en choisissant cette alternative, y compris le risque résiduel et ses conditions.

PEAK ne prescrit ni schéma, ni modèle d'autorisation, ni formule de risque, ni vocabulaire de menace. Il doit donc être représenté comme une **vue de décision** sur les objets natifs de GovCheck, et non en créant quatre silos d'enregistrements P/E/A/K déconnectés.

### 3.1 Exigences pour l'enregistrement d'une décision

Une décision gouvernée devrait être liée à :
- l'énoncé du problème, son périmètre, les sujets concernés et les contraintes ;
- les alternatives examinées, y compris ne rien faire/différer le cas échéant ;
- l'expérience et les connaissances pertinentes, avec sources et dates ;
- les hypothèses utilisées, y compris celles qui restent non résolues ou contestées ;
- les bénéfices attendus, coûts, compromis, incertitudes et conséquences ;
- la solution retenue et ses conditions de mise en œuvre ;
- le traitement du risque et l'énoncé du risque résiduel ;
- le décideur, le fondement de son autorité, les réviseurs, la justification et la date de décision ;
- le périmètre, la validité/expiration, la date de revue et les déclencheurs de réévaluation ;
- les preuves et observations qui confirmeront, contesteront ou invalideront ultérieurement la décision.

La décision est un événement immuable. Un contexte modifié, une nouvelle preuve ou une autorité différente crée une nouvelle évaluation/décision ou un événement de remplacement ; cela ne réécrit pas la justification historique. L'acceptation du risque est une disposition explicite et autorisée, pas une affirmation que le risque est absent ou que le système est sûr.

### 3.2 PEAK et l'assurance répondent à des questions différentes

PEAK demande : **quelles entrées ont éclairé cette décision, quelle solution a été retenue et quel risque a été assumé ?**

Un dossier d'assurance demande : **quelle affirmation est formulée, pourquoi devrait-on y croire, quelles preuves et hypothèses la soutiennent et qu'est-ce qui pourrait la réfuter ?**

Une décision peut référencer plusieurs dossiers d'assurance. Un dossier d'assurance peut éclairer plusieurs décisions. La relation doit rester plusieurs-à-plusieurs et liée au temps/contexte.

## 4. Les observations de production comme retour vers les modèles de menace et d'assurance

Les recommandations NIST sur la surveillance continue relient explicitement la visibilité permanente sur les actifs, menaces, vulnérabilités et efficacité des contrôles aux décisions de risque [R-75](../references.fr.md#r-75). Les travaux de Rushby sur la certification à l'exécution vont plus loin : les hypothèses utilisées dans un argument d'assurance peuvent être explicitées et surveillées en production ; les observations peuvent révéler des hypothèses violées ou des comportements anormaux [R-76](../references.fr.md#r-76). La recherche ACCESS démontre une approche fondée sur SACM dans laquelle les artefacts d'ingénierie et les dossiers d'assurance évoluent ensemble et où l'assurance peut être évaluée à partir de données d'exécution [R-70](../references.fr.md#r-70). Ericsson fournit un exemple industriel de télémétrie en production alimentant l'évolution des modèles de menace et l'analyse des contrôles [R-72](../references.fr.md#r-72).

GovCheck devrait prendre en charge cette boucle de retour :

1. **Observer :** collecter un événement/une observation brute provenant d'un capteur, moniteur, opérateur ou source externe identifié.
2. **Lier :** identifier le système, le déploiement/la configuration, le composant, la fenêtre temporelle et le contexte de collecte exacts.
3. **Évaluer la qualité de l'observation :** établir provenance de la source, intégrité, qualité de l'horloge, couverture, santé de la collecte, complétude et incertitude.
4. **Interpréter :** corréler l'observation avec les actifs, frontières de confiance, menaces existantes, chemins d'attaque, faiblesses, contrôles et hypothèses.
5. **Formuler une hypothèse :** enregistrer un indicateur candidat, une anomalie, un changement d'exposition, un scénario de menace ou une dégradation de contrôle. Conserver les explications alternatives et les contre-preuves.
6. **Évaluer l'impact :** déterminer quelles hypothèses, affirmations, mesures de contrôle, évaluations de risque et décisions d'acceptation pourraient être contestées ou invalidées.
7. **Décider :** un acteur autorisé choisit l'investigation, la surveillance, la mitigation, la récupération, la réévaluation du risque ou l'absence d'action, avec justification.
8. **Valider la réponse :** capturer les observations ultérieures montrant si l'action a modifié l'exposition ou l'efficacité des contrôles ; préserver le contexte avant/après.

La boucle doit être déclenchée par les événements, mais ne doit pas s'auto-autoriser. Une détection automatisée peut proposer une hypothèse ou une réponse. Elle ne doit pas modifier silencieusement le modèle de menace normatif, déclarer un incident confirmé, accepter le risque résiduel ou appliquer une mesure lourde de conséquences sans l'autorité et la politique applicables.

### 4.1 Ne pas fusionner les étapes sémantiques

| Étape | Signification | À ne pas confondre avec |
|---|---|---|
| Événement | Quelque chose qui est rapporté comme s'étant produit | Un fait vérifié ou une attaque |
| Observation | Enregistrement lié à une source de ce qu'un collecteur/opérateur a perçu | L'interprétation de ces données |
| Indicateur/anomalie | Caractéristique ou écart dérivé des observations | Une menace confirmée |
| Hypothèse | Explication candidate, par exemple scénario de menace ou défaillance de contrôle | Une explication causale démontrée |
| Évaluation | Analyse raisonnée de la plausibilité, de l'impact, de l'efficacité des contrôles et de l'incertitude | Une observation brute ou une décision autorisée |
| Incident/constat confirmé | Conclusion atteinte selon une procédure explicite d'investigation/confirmation | Un soupçon généré par un modèle |
| Décision | Choix autorisé concernant le traitement ou l'exploitation | L'évaluation elle-même |

L'absence d'alerte ne constitue pas une preuve d'absence, sauf si la couverture des capteurs, la santé de la collecte, la logique de détection et la fenêtre temporelle pertinente étayent cette inférence. Un capteur bruité ou compromis peut produire des observations trompeuses. Une observation de production peut contester une hypothèse de conception, mais aussi révéler une condition bénigne non modélisée.

### 4.2 Enregistrement d'observation : enveloppe sémantique minimale

L'enregistrement de preuve existant convient aux observations utilisées comme preuves d'affirmations, mais il ne devrait pas être surchargé en devenant l'unique schéma de télémétrie/événement brut. Envisager deux types d'enregistrements liés :

**Enregistrement d'événement/observation opérationnelle**
- identifiant stable de l'événement/de l'observation et version du schéma ;
- identité, version et configuration de la source/du capteur/collecteur, ainsi que provenance et confiance ;
- heure de l'événement, heure observée, heure d'ingestion, source/qualité de l'horloge et métadonnées d'ordre/corrélation ;
- liaison exacte au sujet : actif logique, instance de déploiement, composant, révision de configuration et environnement ;
- type d'observation, méthode de collecte, périmètre, contenu brut ou référence immuable avec empreinte ;
- état d'intégrité/authenticité, complétude, couverture, angles morts connus et preuve de santé de collecte ;
- incertitude/confiance et limites, sans prétendre qu'un nombre de confiance est étalonné ;
- classification vie privée/données, politique d'accès, conservation et métadonnées de caviardage ;
- liens vers événements, observations, incidents, affirmations, hypothèses, menaces et contrôles connexes.

**Enregistrement d'évaluation/de preuve dérivée**
- identifiants exacts des observations d'entrée et révision de la transformation/du modèle/de la règle ;
- méthode d'inférence (règle, modèle statistique, évaluation d'analyste, corrélation ou investigation) ;
- hypothèse candidate, explications alternatives et contre-preuves ;
- périmètre, hypothèses, incertitude, limites et état du résultat ;
- affirmations, scénarios de menace, chemins d'attaque, contrôles et décisions potentiellement affectés ;
- exigences de revue/d'autorité et événements d'invalidation/réévaluation résultants.

Cette séparation préserve le témoignage brut et rend l'interprétation reproductible. Une évaluation dérivée ne réécrit jamais son observation source. L'enregistrement de preuve existant peut référencer les deux comme artefacts probants et lier le soutien/la réfutation de l'affirmation résultante à des révisions exactes.

## 5. SACM 2.3 : ce qu'il apporte à GovCheck

SACM 2.3 est nettement plus riche qu'une simple liste d'affirmations et de preuves. Le métamodèle officiel définit quatre points de conformité principaux et sépare les packages de dossier d'assurance, d'argumentation, d'artefacts et de terminologie [R-34](../references.fr.md#r-34).

### 5.1 Constructions utiles

| Construction SACM 2.3 | Apport | Utilisation GovCheck |
|---|---|---|
| AssuranceCasePackage | Conteneur échangeable de premier niveau pour argumentation, artefacts et terminologie | Regrouper un dossier d'assurance gouverné et son vocabulaire/références d'artefacts |
| Claim / Assertion | Propositions explicites, y compris états déclaré/assumé/à étayer/axiomatique/réfuté | Représenter les affirmations d'assurance et les états explicites non développés/réfutés |
| ArgumentReasoning | Description du raisonnement sous-jacent aux relations | Préserver la justification de l'inférence et la méthode argumentative |
| AssertedInference | Relier prémisses et conclusions | Mapper les arêtes d'inférence typées |
| AssertedEvidence | Relier les références d'artefacts aux affirmations/à l'argumentation | Mapper le soutien ou la contre-preuve d'une affirmation |
| AssertedContext | Attacher des prémisses contextuelles | Mapper contexte système, hypothèses et contraintes |
| ArtifactReference / Artifact | Référencer des preuves et artefacts d'ingénierie externes | Lier artefacts, configurations, modèles, rapports et observations GovCheck exacts |
| Event | Enregistrer des événements du cycle de vie d'un artefact | Représenter potentiellement les événements de cycle de vie et les observations, avec extensions GovCheck |
| Activity / Technique / Participant / Resource | Décrire travaux, méthodes, acteurs et ressources tangibles | Représenter le contexte de production des preuves et les participants de provenance |
| ArtifactAssetRelationship | Relier des artefacts par des relations nommées et décrites | Fournir un pont général entre relations d'artefacts |
| TerminologyPackage | Définir termes et expressions contrôlés | Publier le vocabulaire GovCheck et les correspondances PEAK/SACM |
| Interfaces/bindings de packages | Échange modulaire et relations entre packages | Séparer les dossiers d'assurance par projet/composant et les lier explicitement |

Le modèle n'est pas seulement une notation graphique : il dispose d'une représentation XMI normative exploitable par machine. SACM 2.3 inclut explicitement Event pour les événements du cycle de vie d'un artefact et ArtifactAssetRelationship pour les liens entre artefacts. Son vocabulaire de déclaration des affirmations distingue les affirmations assumées, affirmées, à étayer, axiomatiques et réfutées. Ces caractéristiques en font un candidat sérieux pour l'interopérabilité et la représentation structurée des arguments.

### 5.2 En quoi SACM est plus riche que la proposition GovCheck actuelle

SACM apporte des structures explicites et mûres de dossier d'assurance que la proposition actuelle 0013/0021 de GovCheck ne définit pas complètement :
- packages de dossiers d'assurance modulaires réutilisables, interfaces et bindings de packages ;
- packages distincts de terminologie, d'artefacts et d'argumentation ;
- types explicites d'affirmations/relations d'inférence/preuve/contexte ;
- états explicites de réfutation/contre-preuve et d'argument incomplet/à étayer ;
- concepts de première classe pour artefacts, événements, activités, techniques, participants et ressources ;
- format d'échange publié et points de conformité.

GovCheck ne devrait pas recréer ces concepts à la légère. Un mapping ou une implémentation devrait réutiliser leurs sémantiques lorsqu'elles conviennent, et documenter les différences délibérées.

### 5.3 Ce que SACM 2.3 ne fournit pas à GovCheck

SACM est un métamodèle de dossier d'assurance, pas une ontologie complète de sécurité, de risque opérationnel ou de gouvernance. En particulier, il ne fournit pas à lui seul :

- un modèle de menace métier : capacités adverses, sources de menace, techniques, chemins d'attaque, préconditions, exposition et sémantique des vulnérabilités ;
- un cycle de vie des contrôles de sécurité : planifié, implémenté, configuré, testé, revu indépendamment, surveillé, dégradé et retiré ;
- un contrat de télémétrie d'exécution avec identité du capteur, qualité de l'horloge, couverture de collecte, intégrité, classification vie privée et conservation des événements bruts ;
- une distinction définie entre événement, observation, indicateur, hypothèse, menace évaluée, incident confirmé et risque ;
- la sémantique d'évaluation et de traitement du risque, l'acceptation du risque résiduel, le propriétaire responsable, l'autorité d'approbation, l'expiration et les déclencheurs de réévaluation ;
- le modèle complet d'entrées de décision PEAK et la traçabilité entre résultat de décision et risque assumé ;
- la liaison exacte sujet/révision de GovCheck, la fraîcheur des preuves, l'invalidation des dépendances et la sémantique d'acceptation du cycle de vie ;
- la vérification de provenance cryptographique, la politique de confiance ou le comportement d'application.

Les Event et ArtifactAssetRelationship génériques de SACM sont des points d'extension utiles, pas des substituts à ces sémantiques métier. De même, une déclaration de Claim assumed n'est pas un enregistrement complet de gouvernance d'hypothèse avec propriétaire, périmètre, validité, moniteur, critères de réfutation et conséquences.

### 5.4 SACM 2.4 Beta modifie l'évaluation

À la date de ce document, OMG répertorie SACM 2.4 Beta 1 (septembre 2026) comme une bêta en cours, tandis que 2.3 reste la version formelle [R-73](../references.fr.md#r-73). Le suivi des tickets de la bêta montre des changements proposés/résolus qui répondent à plusieurs lacunes importantes de 2.3, notamment :
- valeurs structurées typées et données liées à la force des preuves (SACM24-80) ;
- constructions liées à l'évaluation (SACM24-75) ;
- jointures pour combiner affirmations/preuves (SACM24-76) ;
- références à un concept entier (SACM24-73) ;
- marqueur needsDevelopment (SACM24-74) ;
- structure des packages et propriété des domaines (SACM24-56) ;
- cibles d'inférence/de preuve plus précises (SACM24-82).

C'est significatif : certains éléments qui pourraient autrement devenir des extensions GovCheck sont déjà étudiés dans la révision de SACM elle-même. Mais les résolutions de tickets d'une bêta ne constituent pas un contrat normatif final. GovCheck devrait suivre l'évolution de 2.4 et réévaluer son choix lorsqu'une version formelle et son modèle lisible par machine seront publiés.

## 6. Architecture sémantique proposée

Utiliser un **graphe métier GovCheck** comme couche sémantique faisant autorité, avec des adaptateurs/projections PEAK et SACM.

### 6.1 Concepts métier fondamentaux

Conserver au minimum des identités stables et des relations typées pour :

- **Contexte système :** projet, actif, composant, instance de déploiement, environnement, instantané de configuration et frontière de confiance.
- **Modèle de menace :** source/acteur de menace, capacité, événement de menace, scénario, technique/chemin d'attaque, précondition, faiblesse, exposition et conséquence.
- **Contrôle :** définition du contrôle, instance d'implémentation/configuration, responsable, état du cycle de vie, test/évaluation et statut de surveillance.
- **Témoignage opérationnel :** événement, observation, capteur/collecteur, indicateur, anomalie, hypothèse, incident/constat et évaluation dérivée.
- **Assurance :** affirmation, sous-affirmation, argument/raisonnement, hypothèse, preuve, contre-preuve/élément réfutant, méthode, périmètre, limite, revue et statut d'assurance.
- **Risques et décisions :** évaluation du risque, option de traitement, risque résiduel, décision d'acceptation, autorité, propriétaire, alternatives, justification, validité, expiration et déclencheur de réévaluation.
- **Provenance :** producteur/participant, activité, outil, source, horodatage, révisions exactes, empreinte, intégrité/authenticité, dérivation et remplacement.

### 6.2 Relations typées importantes

Le vocabulaire de relations devrait inclure au minimum :

- observedOn, collectedBy, derivedFrom, correlatedWith ;
- indicates, hypothesizes, confirms, refutes, challenges ;
- threatens, enables, requiresPrecondition, followsAttackStep ;
- mitigatedBy, implementedAs, configuredBy, testedBy, monitoredBy ;
- supports, refutes, contextualizes, assumes, inferredFrom ;
- affectsClaim, invalidatesEvidence, invalidatesReview, triggersReassessment ;
- assessedBy, treatedBy, acceptsResidualRisk, authorizedBy ;
- supersedes, derivedFrom, revalidates.

Les relations doivent avoir leur propre identité, provenance, périmètre et, le cas échéant, intervalle de validité. Une arête générique non typée ou une étiquette textuelle ne suffit pas pour une interprétation normative.

### 6.3 Règles de projection

- **Projection PEAK :** afficher une décision et ses entrées liées Problem, Experience, Assumptions et Knowledge, puis sa Solution et son Assumed Risk. Chaque élément affiché renvoie à l'identité et à la révision canoniques GovCheck.
- **Projection SACM :** mapper affirmations, raisonnements, inférences, preuves, contextes, artefacts et terminologie dans des packages SACM. Préserver les sémantiques propres à GovCheck dans une extension/profil avec espace de noms ou des enregistrements liés explicites. Les tests aller-retour doivent détecter toute sémantique perdue ou affaiblie.
- **Projection du modèle de menace :** afficher les scénarios et chemins d'attaque de conception à côté des indicateurs/hypothèses dérivés des observations, en distinguant clairement possibilités modélisées, faits observés et constats confirmés.
- **Projection opérationnelle :** montrer l'instantané courant du système/déploiement, la couverture des observations, l'état des contrôles, les hypothèses en attente, les affirmations d'assurance affectées et les décisions à réexaminer.

La projection n'est pas la source de vérité. Une modification par l'utilisateur dans une vue PEAK ou SACM doit produire des changements explicites dans le domaine GovCheck, avec validation et contrôle d'autorité.

## 7. Invariants sémantiques et contraintes de sûreté

1. Les observations brutes sont immuables ; les corrections ou réinterprétations créent de nouveaux enregistrements liés à l'original.
2. Une observation n'est pas automatiquement un fait, un indicateur, une hypothèse, un incident, une menace ou une évaluation du risque.
3. Une hypothèse conserve les explications alternatives, le fondement du niveau de confiance, l'incertitude et les contre-preuves.
4. L'absence d'observation n'implique pas l'absence de menace, sauf si la couverture de surveillance et la santé des capteurs étayent cette inférence.
5. Les hypothèses sont des prémisses gouvernées de première classe, distinctes des preuves et du risque assumé.
6. Les hypothèses surveillables sont liées à des prédicats explicites, une identité de moniteur, une couverture et une politique de réponse ; toutes les hypothèses ne sont pas surveillables.
7. Une hypothèse violée ne conteste que les affirmations/décisions dont la clôture argumentative en dépend ; l'impact doit être tracé, pas deviné globalement.
8. Une mise à jour du modèle de menace est versionnée et revue. Une observation peut proposer un nouveau scénario ou réviser sa plausibilité, mais ne modifie pas silencieusement la référence normative.
9. L'efficacité d'un contrôle est circonscrite au déploiement, à la configuration, à la méthode et à la fenêtre temporelle testés/observés.
10. Une décision d'acceptation du risque n'améliore pas le statut d'assurance, ne valide pas un contrôle et n'efface pas les contre-preuves.
11. Une action en production exige une politique et une autorité explicites ; recommandations et prédictions ne sont pas des autorisations.
12. Les décisions, observations, évaluations et états d'assurance historiques restent auditables après remplacement ou invalidation.

## 8. Recommandation d'adoption et travaux par étapes

### Recommandation

- Conserver le graphe métier GovCheck et les sémantiques d'autorité de gouvernance comme éléments canoniques.
- Adopter PEAK comme **vue de traçabilité des décisions** pour les décisions importantes de gouvernance/sécurité/risque, pas comme ontologie séparée ou règle de décision automatique.
- Traiter SACM 2.3 comme première **cible d'interopérabilité** pour les structures de dossier d'assurance, pas comme métamodèle complet de GovCheck.
- Suivre SACM 2.4 Beta 1 et éviter de finaliser les mappings sur les domaines actuellement modifiés avant la publication d'une version formelle 2.4.
- Ajouter des sémantiques de profil/extension GovCheck uniquement lorsque la base SACM ne peut pas représenter le sens métier requis ; maintenir des mappings explicites qui préservent les pertes éventuelles.

### Séquence proposée

1. **Spécification de mapping sémantique :** mapper 0013/0021 et les enregistrements de preuve GovCheck vers PEAK et SACM 2.3 ; consigner les concepts et cardinalités non mappés.
2. **Contrat d'observation :** définir un schéma versionné d'observation/événement opérationnel distinct de l'enregistrement de preuve/évaluation dérivée ; inclure provenance, sujet exact, horloge/couverture, intégrité, incertitude et vie privée.
3. **Contrat de retour vers le modèle de menace :** définir la transition observation → indicateur/hypothèse → proposition de modèle de menace → revue → mise à jour versionnée.
4. **Contrat de décision :** définir les liens des entrées PEAK, alternatives, solution, risque assumé/résiduel, autorité, expiration et déclencheurs de réévaluation.
5. **Prototype d'interopérabilité SACM :** importer/exporter un dossier d'assurance représentatif ; tester affirmations, hypothèses, contextes, contre-preuves, artefacts, événements, bindings de packages et extensions GovCheck pour détecter les pertes aller-retour.
6. **Vérifications formelles :** modéliser invalidation/réévaluation et autorisation des décisions séparément de la détection. Ne pas fusionner tout le raisonnement de menace à l'exécution dans un seul modèle sujet à l'explosion d'états.
7. **Pilote opérationnel :** commencer avec des observations synthétiques, puis une source de télémétrie non sensible et de périmètre limité. Ne pas automatiser de mitigation conséquente avant d'avoir démontré gestion des faux positifs, rollback, autorisation et préservation des preuves.

## 9. Limites et décisions non prises

Ce document n'adopte pas SACM comme ontologie canonique de GovCheck, ne sélectionne pas de base de données graphe, ne prescrit pas de score de risque, ne définit pas de plateforme de télémétrie de production, n'autorise pas de remédiation autonome et ne prétend pas que la modélisation des menaces à l'exécution est implémentée. PEAK reste un cadre d'analyse de décision ; SACM reste un métamodèle de dossier d'assurance. Leurs rôles sont volontairement distincts.

La question de conception immédiate n'est pas « quel modèle unique remplace tous les autres ? » mais « quelles sémantiques canoniques permettent de projeter les mêmes faits et décisions gouvernés dans des vues menace, opérationnelle, PEAK et SACM sans perdre provenance, incertitude, autorité ni signification ? »
