# 0025 — Observations transverses au cycle de vie, traçabilité décisionnelle PEAK et interopérabilité SACM

**Statut :** recherche et recommandation d'architecture proposées à revue. Ce document propose des liens sémantiques ; il ne prétend pas qu'une collecte opérationnelle, un processus PEAK, un import/export SACM ou une réévaluation automatisée soient implémentés.  
**Langue :** l'anglais est la version par défaut ; voir la [version anglaise](0025-runtime-observations-peak-and-sacm.md).

## 1. Objet et périmètre

GovCheck a vocation à gouverner un dépôt logiciel pendant tout son cycle de vie : de l'intention du projet et de sa structure initiale aux exigences, à l'architecture, à l'implémentation, aux tests, à la vérification, aux revues, à l'acceptation des changements, aux publications, à l'exploitation, à la maintenance et, finalement, au retrait. Son objet est le dépôt gouverné et l'évolution de l'état du projet — pas la seule sécurité, ni une méthode d'ingénierie particulière.

Selon le projet, les sujets gouvernés peuvent notamment inclure :

- objectifs, besoins des parties prenantes, exigences fonctionnelles et non fonctionnelles ;
- architecture, interfaces, contraintes de conception et dette technique ;
- pratiques d'implémentation, qualité du code et maintenabilité ;
- tests, analyses statiques et dynamiques, model checking, vérification de programmes et preuve de théorèmes ;
- dépendances, chaîne d'approvisionnement, reproductibilité et intégrité des builds ;
- sécurité, vie privée, sûreté et résilience opérationnelle ;
- documentation, licences, obligations légales ou réglementaires ;
- gestion des changements, revues, approbations, publications, support et maintenance.

Aucun projet n'est tenu d'adopter tous ces sujets ni toutes ces méthodes. Leur applicabilité et leur profondeur dépendent du contexte déclaré, du profil, des obligations et des décisions autorisées du projet. GovCheck doit rendre explicites les sélections, omissions, inconnues et leurs conséquences, plutôt que d'imposer une pile d'ingénierie universelle.

Ce document traite de trois besoins liés mais distincts :

1. relier les observations issues du cycle de vie du dépôt et, le cas échéant, de l'exploitation du système au modèle gouverné du projet ;
2. utiliser **PEAK** pour rendre traçables les éléments d'entrée, le raisonnement, la solution et le risque assumé d'une décision ;
3. définir comment l'intégralité du métamodèle de dossiers d'assurance SACM est représentée et gouvernée comme une capacité dédiée de GovCheck, et comment elle se relie au modèle plus large de gouvernance des dépôts.

PEAK et SACM ne répondent pas au même problème et ne sont pas des alternatives l'un à l'autre. Aucun des deux ne constitue GovCheck dans son ensemble.

## 2. Fondations GovCheck à préserver

Ce travail étend l'architecture existante ; il ne doit pas créer un modèle de gouvernance parallèle.

- **Spécification 0002** définit le paquet canonique de gouvernance : identifiants stables des règles, règles typées, périmètre, applicabilité, composition, exceptions, profils et projections documentaires contrôlées.
- **Spécification 0003** définit le cycle de vie des changements du dépôt indépendamment de Git, Pijul, d'une forge ou d'un produit CI. Les décisions lient des états exacts de base/candidat et de gouvernance ; acceptation et application sont distinctes.
- **Spécification 0005** distingue affirmations, arguments, preuves, hypothèses, contexte, limites, classes de méthodes et acceptation. Tests, model checking, preuve de théorèmes, conformité de l'implémentation et fidélité normative ne sont pas interchangeables.
- **Architecture 0013** fournit le vocabulaire conceptuel général reliant objectifs, exigences, normes, propriétés, contrats, modèles, artefacts d'implémentation, méthodes, preuves, affirmations, arguments et décisions autorisées.
- **Architectures 0017 et 0021** traitent l'identité/révision des artefacts, la liaison des preuves, leur fraîcheur, l'invalidation des dépendances et les arguments d'assurance.
- **Architecture 0024** propose un bootstrap guidé et non destructif dans lequel les projets sélectionnent des capacités et des méthodes d'assurance adaptées à leur contexte.

Ces documents décrivent un socle général de gouvernance des dépôts. La sécurité et la modélisation des menaces sont des capacités métier importantes parmi d'autres ; elles ne sont pas le principe organisateur de toutes les autres capacités.

## 3. PEAK : tracer le raisonnement qui conduit à une décision

PEAK est utilisé ici dans son sens d'analyse de décision : **Problem, Experience, Assumptions et Knowledge** sont explicités comme éléments d'entrée d'une décision ; le processus consigne la **Solution** retenue et l'**Assumed Risk** [R-74](../references.fr.md#r-74).

Une décision GovCheck peut exposer ces dimensions sans les transformer en quatre silos de données isolés :

| Dimension PEAK | Question de traçabilité | Liens GovCheck possibles |
|---|---|---|
| **P — Problem** | Quel problème faut-il résoudre, dans quel périmètre et sous quelles contraintes ? | Objectif, exigence, problème, changement, artefact concerné, besoin d'une partie prenante |
| **E — Experience** | Quelle expérience pertinente éclaire la décision ? | Décisions antérieures, incidents, défauts, historique des tests, expérience de maintenance, retours d'exploitation et expertise |
| **A — Assumptions** | Quelles prémisses sont utilisées et sous quelles conditions ? | Hypothèses explicites avec responsable, périmètre, justification, validité, confiance et conditions de revue/réfutation |
| **K — Knowledge** | Quelles informations sont disponibles pour les décideurs ? | Spécifications, architecture, mesures, résultats de tests, preuves, faits sur les dépendances, observations, normes et autres éléments admissibles |
| **Solution** | Quelle option a été retenue, et pourquoi ? | Alternative retenue, alternatives rejetées, justification, plan d'implémentation ou de suivi |
| **Assumed Risk** | Quelle incertitude ou exposition est consciemment conservée par ce choix ? | Arbitrages, risque résiduel, incertitude, conditions, responsable redevable et déclencheurs de revue |

PEAK n'est ni un mécanisme d'autorisation, ni une formule de risque, ni une notation de dossier d'assurance, ni un modèle du cycle de vie d'un dépôt. GovCheck doit fournir la gouvernance de la décision : identité, autorité, périmètre, participants, date, justification, liens vers les preuves, validité, revue et remplacement.

La même structure PEAK peut éclairer des décisions d'architecture, de maintenabilité, de stratégie de test, de mise à niveau des dépendances, de préparation d'une publication, de traitement de sécurité ou de gouvernance du projet. Son emploi doit être proportionné à l'importance et aux conséquences de la décision ; il ne doit pas devenir une formalité obligatoire pour chaque choix trivial.

Une décision et un dossier d'assurance répondent à des questions différentes. Un enregistrement de décision explique ce qui a été examiné et choisi, y compris le risque assumé. Un dossier d'assurance explique pourquoi une affirmation délimitée devrait être crue, à partir d'un argument, d'hypothèses et de preuves. Une décision peut s'appuyer sur plusieurs dossiers d'assurance ; un dossier d'assurance peut éclairer plusieurs décisions. Leurs liens sont plusieurs-à-plusieurs et doivent être liés au contexte et aux révisions concernés.

## 4. Les observations comme retour d'information sur le cycle de vie

GovCheck devrait pouvoir relier les observations à l'état exact du dépôt/projet ainsi qu'aux exigences, hypothèses, affirmations, méthodes, décisions et risques qu'elles peuvent affecter. Les sources d'observation ne se limitent pas à la télémétrie de production.

Exemples :

- échec de test, tendance de régression, test instable ou évolution de la couverture ;
- constat d'analyse statique ou nouveau problème de maintenabilité ;
- échec de reproductibilité d'un build ou changement de chaîne d'outils ;
- publication d'une dépendance, annonce de fin de support, avis de vulnérabilité ou changement de licence ;
- constat de revue, changement rejeté, rapport de défaut ou incident de support ;
- dérive documentaire ou divergence entre spécification et implémentation ;
- contre-exemple d'un modèle formel, obligation de preuve non satisfaite ou changement d'une dépendance de preuve ;
- alerte d'exécution, dérive de déploiement, dégradation de service ou incident de sécurité.

Ces observations peuvent remettre en cause une hypothèse, indiquer qu'une exigence n'est pas satisfaite, invalider une preuve, révéler un nouveau risque ou déclencher la revue d'une décision. Elles n'ont pas toutes la même valeur probante. Un échec de test ne prouve pas automatiquement un défaut général ; un avertissement d'analyse statique n'est pas automatiquement une vulnérabilité confirmée ; une variation de métrique ne constitue pas à elle seule une violation de gouvernance ; une alerte d'exécution n'est pas automatiquement un incident confirmé.

### 4.1 Cycle général de retour

1. **Observer :** enregistrer un événement ou une observation provenant d'un outil, d'un artefact du dépôt, d'un réviseur, d'un opérateur ou d'une source externe.
2. **Lier :** identifier le dépôt, l'artefact, la révision, l'environnement, la méthode et la fenêtre temporelle exacts.
3. **Évaluer la qualité :** enregistrer provenance, intégrité, complétude, couverture, état de la source/de l'outil, incertitude et limites.
4. **Interpréter :** relier l'observation aux exigences, propriétés, affirmations, hypothèses, dépendances, risques et décisions applicables.
5. **Dériver un constat ou une hypothèse :** préserver la distinction entre observation brute, interprétation, cause suspectée et conclusion confirmée.
6. **Évaluer l'impact :** identifier les preuves, affirmations, approbations, plans ou décisions qui peuvent nécessiter revalidation ou revue.
7. **Décider :** laisser l'autorité compétente choisir d'enquêter, corriger, différer, accepter une déviation circonscrite, modifier une exigence ou prendre une autre mesure autorisée.
8. **Vérifier la réponse :** enregistrer les preuves de suivi et déterminer si le résultat attendu a été obtenu.

Ce cycle est indépendant du domaine. L'interprétation spécifique relève de la méthode ou de la capacité concernée. Par exemple, le retour vers le modèle de menace constitue un parcours spécialisé : des observations de sécurité en exploitation peuvent remettre en cause des hypothèses de menace ou l'efficacité des mesures, mais elles ne réécrivent pas silencieusement le modèle de menace et n'autorisent pas une remédiation. Les recommandations de surveillance continue, les travaux sur la certification à l'exécution et un exemple industriel de modélisation des menaces à l'exécution illustrent ce parcours propre à la sécurité [R-75](../references.fr.md#r-75) [R-76](../references.fr.md#r-76) [R-72](../references.fr.md#r-72). Les travaux ACCESS illustrent également l'utilisation de données d'exécution dans l'évolution de dossiers d'assurance fondés sur SACM [R-70](../references.fr.md#r-70). Le même schéma général s'applique à la qualité, à la maintenabilité, aux tests, aux dépendances, aux preuves et à la gouvernance des publications.

### 4.2 Enregistrements d'observation et de preuve

Ne pas surcharger un même enregistrement avec l'observation brute, son interprétation et la conclusion d'assurance. Une séparation utile est :

**Enregistrement d'événement/observation**
- identité stable et révision du schéma ;
- source/producteur, identité et version de l'outil ou du capteur ;
- dates de l'événement, de l'observation et de l'ingestion, si pertinentes ;
- liaison au sujet exact : dépôt, artefact, commit/révision, configuration, environnement et périmètre ;
- méthode, invocation/configuration et résultat brut ou référence immuable/empreinte ;
- provenance, intégrité, complétude, couverture et état de la source ;
- incertitude, limites, classification/vie privée et métadonnées de conservation ;
- liens vers les artefacts, exigences, affirmations, hypothèses, risques et décisions associés.

**Enregistrement dérivé de constat/évaluation/preuve**
- identifiants exacts des observations d'entrée et révision de la transformation/méthode ;
- méthode d'interprétation et producteur/réviseur responsable ;
- constat, hypothèse ou conclusion, avec alternatives et contre-preuves ;
- périmètre, exigences, propriétés, affirmations, mesures ou décisions affectés ;
- incertitude, limites, statut et conditions d'invalidation/réévaluation.

Une observation peut être utilisée comme preuve, mais elle n'est pas automatiquement admissible pour toute affirmation. Les sémantiques de la Spécification 0005 et de l'Architecture 0021 déterminent si une preuve est pertinente, suffisamment fiable, actuelle et dans le périmètre.

## 5. SACM : une capacité complète d'assurance intégrée à GovCheck

SACM (Structured Assurance Case Metamodel) définit un métamodèle structuré pour les dossiers d'assurance. GovCheck devrait prendre en charge l'intégralité du périmètre sémantique de SACM 2.4 Beta 1 comme capacité d'assurance dédiée, et non comme un simple adaptateur d'échange limité. L'architecture 0026 définit la cible : couverture complète du métamodèle normatif SACM et préservation fidèle des constructions complémentaires explicitement non normatives, avec version épinglée et conformité démontrée [R-34](../references.fr.md#r-34) [R-73](../references.fr.md#r-73).

SACM n'est pas un concurrent de PEAK. PEAK aide à exposer les éléments de raisonnement et le risque assumé derrière une décision ; SACM représente des arguments d'assurance structurés. GovCheck peut utiliser les deux à des fins différentes tout en conservant ses propres sémantiques de gouvernance des dépôts. Les décisions PEAK peuvent référencer des dossiers et éléments SACM, et les claims SACM peuvent référencer des objectifs, exigences, révisions et preuves GovCheck au moyen de liens typés explicites. Les recherches sur l'ingénierie des dossiers d'assurance soulignent également l'importance des réfutations possibles, des contre-preuves et de la force des preuves — des sujets pertinents pour l'évaluation des arguments par GovCheck, que SACM soit ou non utilisé comme format d'échange [R-71](../references.fr.md#r-71).

### 5.1 Périmètre de la capacité SACM

| Construction SACM | Usage potentiel dans GovCheck |
|---|---|
| AssuranceCasePackage | Regrouper un dossier d'assurance structuré et ses références |
| Claim / Assertion | Représenter des affirmations délimitées et des états explicites : assumée, affirmée, à étayer ou réfutée |
| ArgumentReasoning / AssertedInference | Représenter le raisonnement et les relations d'inférence |
| AssertedEvidence / AssertedContext | Relier preuves et prémisses contextuelles à l'argumentation |
| ArtifactReference / Artifact | Référencer des artefacts exacts du dépôt, spécifications, configurations, rapports et résultats |
| Event / Activity / Technique / Participant / Resource | Décrire des événements pertinents du cycle de vie des artefacts et le contexte de production des preuves |
| TerminologyPackage | Échanger une terminologie contrôlée |
| Interfaces et bindings de packages | Relier des dossiers d'assurance modulaires |

Ces constructions peuvent réduire la quantité de mécanismes propres aux dossiers d'assurance que GovCheck devrait inventer. Elles n'établissent pas qu'une affirmation est vraie, qu'une preuve est fraîche, qu'une décision est autorisée ou qu'une implémentation est conforme à une spécification. Ces significations dépendent toujours des règles propres à GovCheck sur le périmètre, la provenance, l'autorité, le cycle de vie et l'évaluation.

### 5.2 Frontière et composition avec GovCheck

La distinction de périmètre est architecturale ; il ne s'agit ni d'une comparaison ni d'un classement. SACM gouverne la sémantique de la capacité « dossier d'assurance » ; GovCheck gouverne le dépôt et l'ensemble de son cycle de vie.

SACM ne définit pas la gouvernance complète d'un dépôt logiciel pendant son cycle de vie. Il ne fournit pas à lui seul l'autorité des règles canoniques de GovCheck, le cycle de vie des changements et de leur acceptation, le bootstrap et la sélection des capacités, la gouvernance des artefacts et versions, l'autorité et les délégations des acteurs, ni les politiques et méthodes propres aux domaines sélectionnés par un projet.

SACM ne définit pas non plus toutes les sémantiques métier dont les projets peuvent avoir besoin : politique de maintenabilité, stratégie et adéquation des tests, cycle de vie des dépendances, gouvernance des builds/publications, scénarios de menace, obligations de vie privée ou réponse opérationnelle. Il peut représenter des arguments d'assurance portant sur ces sujets, mais il ne fournit pas leurs modèles métier ni leurs politiques de décision.

Les constructions SACM sont donc des éléments de premier ordre dans la capacité d'assurance, tandis que les concepts GovCheck transverses restent de premier ordre dans leurs propres domaines. Les mappings doivent préserver les distinctions entre claims, hypothèses, preuves, inférences, observations, exigences, constats, décisions et autorité. L'architecture 0026 définit la cible de couverture SACM complète et le contrat d'intégration entre modèles.

### 5.3 SACM 2.4 Beta 1 comme cible d'ingénierie épinglée

L'OMG répertorie SACM 2.4 Beta 1 (septembre 2026) comme version en cours, tandis que 2.3 reste formelle [R-73](../references.fr.md#r-73). La bêta introduit ou clarifie l'alignement Foundation/MOF, la sémantique des packages, les sujets explicites des claims, le contexte argumentatif, les assessments, les joins, les descripteurs d'argumentation avancée, les valeurs nommées typées et les vues/diagrammes. Le suivi des tickets distingue également les changements du métamodèle normatif des constructions complémentaires non normatives.

GovCheck devrait épingler le PDF Beta 1 exact et le métamodèle lisible par machine pour son prototype, préserver les distinctions de statut normatif et suivre la version finale 2.4 au moyen d'une migration explicite. La couverture complète et la stratégie de conformité sont spécifiées dans l'architecture 0026.

## 6. Architecture sémantique GovCheck : un socle commun, plusieurs domaines

L'architecture doit être **multidomaine et orientée capacités**, et non centrée sur la sécurité ni construite autour d'un métamodèle externe unique.

Le modèle canonique de gouvernance GovCheck reste responsable des règles, de l'autorité, de l'applicabilité, du cycle de vie, des décisions et de la conformité. Les capacités métier ajoutent les concepts, relations, méthodes et exigences de preuve typés qui leur sont nécessaires. Un profil de projet sélectionne les capacités applicables et leurs dépendances ; il ne remplace pas le socle commun de gouvernance.

Exemples de domaines de capacité :

- **Produit et exigences :** besoins des parties prenantes, objectifs, exigences fonctionnelles, critères d'acceptation et traçabilité.
- **Architecture et conception :** composants, interfaces, contraintes, décisions d'architecture et dette technique.
- **Implémentation et maintenabilité :** propriété du code, contraintes de qualité, complexité, modularité, constats de maintenabilité et remédiation.
- **Tests et validation :** plans et cas de test, suites, environnements, couverture, résultats, régressions et arguments d'adéquation.
- **Méthodes formelles et preuves :** modèles, propriétés, hypothèses, exécutions de model checking, obligations de preuve, artefacts de preuve et relations de conformité.
- **Dépendances et chaîne d'approvisionnement :** identité et versions des dépendances, provenance, licences, vulnérabilités, état du support et décisions de mise à niveau.
- **Sécurité, vie privée et sûreté :** actifs, menaces, chemins d'attaque, mesures, exigences de vie privée, dangers et décisions de traitement.
- **Documentation et conformité :** projections normatives, couverture documentaire, obligations, attestations et enregistrements de revue.
- **Build, publication et exploitation :** reproductibilité, artefacts, manifestes de publication, état de déploiement, observations de service, support et retrait.

Ces domaines sont des frontières candidates, pas une taxonomie fixe et obligatoire. Certains projets les regrouperont ; d'autres auront besoin de domaines supplémentaires. Le modèle doit permettre des définitions de capacités explicites et des extensions versionnées sans que chaque domaine invente ses propres identités, provenance, décisions et sémantiques de cycle de vie incompatibles.

Les concepts transverses devraient inclure :

- identité stable, révision et état du cycle de vie ;
- objectif, exigence, règle, propriété et contrat ;
- acteur, rôle, autorité, délégation et approbation ;
- artefact, dépendance, relation et liaison au sujet exact ;
- méthode, exécution, observation, constat et preuve ;
- hypothèse, incertitude, limite et contre-preuve ;
- affirmation, argument, évaluation, risque et décision ;
- applicabilité, validité, fraîcheur, invalidation et réévaluation ;
- provenance, historique d'audit et projection documentaire contrôlée.

Les relations typées relient le socle commun aux enregistrements métier : derivesFrom, refines, constrains, appliesTo, implementedBy, verifiedBy, testedBy, evidencedBy, supports, refutes, assumes, dependsOn, affects, invalidates, supersedes, reviewedBy et authorizedBy. Des relations propres à un domaine (par exemple threatens, mitigatedBy ou regresses) ne sont ajoutées qu'avec une sémantique explicite.

### 6.1 Vues et interopérabilité

- **Vue PEAK :** exposer le Problem, l'Experience, les Assumptions et le Knowledge qui éclairent une décision, puis sa Solution et son Assumed Risk.
- **Capacité d'assurance SACM :** représenter et valider l'intégralité du métamodèle SACM épinglé ; préserver les constructions complémentaires non normatives et fournir un import/export/aller-retour sans perte des sémantiques natives SACM. Les liens vers le cycle de vie et les artefacts métier GovCheck restent explicites.
- **Vues métier :** présenter les exigences, artefacts, méthodes, preuves et décisions pertinents pour les tests, la maintenabilité, les preuves formelles, les dépendances, la sécurité ou toute autre capacité sélectionnée.
- **Vue cycle de vie :** montrer comment intention du projet, exigences, architecture, implémentation, vérification, acceptation, publication, exploitation et maintenance s'articulent dans le temps.
- **Vue de retour opérationnel :** montrer les observations, constats dérivés, hypothèses/affirmations/décisions affectées et réévaluations nécessaires.

Ces vues sont des projections des enregistrements gouvernés, pas des sources de vérité concurrentes. Modifier une vue doit produire des changements GovCheck explicites et validés, avec l'autorité requise.

## 7. Invariants transverses

1. Toute observation, tout résultat et toute décision est lié à son sujet exact, sa révision, sa méthode, son périmètre et sa provenance.
2. Les observations brutes et décisions historiques sont préservées ; les corrections et réinterprétations créent des enregistrements liés au lieu de réécrire silencieusement l'historique.
3. Une observation n'est pas automatiquement un fait, un constat, une preuve pour une affirmation donnée ou une décision autorisée.
4. Hypothèses, preuves, inférences, conclusions, incertitudes et limites restent distinguables dans tous les domaines.
5. Une méthode n'établit que ce que permettent son périmètre, ses entrées, sa configuration, son exécution et son socle de confiance déclarés.
6. La fraîcheur et l'invalidation des preuves suivent les dépendances déclarées ; un changement d'artefact, d'exigence, d'outil, d'environnement ou d'hypothèse déclenche la réévaluation appropriée, pas une remise à zéro globale et indifférenciée.
7. Un résultat absent n'est pas un résultat positif. Inconnu, non applicable, non exécuté, non pris en charge, incomplet, échoué et réussi restent distincts.
8. Une métrique ou un score agrégé ne doit pas masquer les preuves, hypothèses, incertitudes ou significations propres au domaine sous-jacents.
9. Une décision enregistre son autorité, sa justification, son périmètre, ses alternatives, sa validité et ses conditions de revue. PEAK peut rendre son raisonnement lisible, mais ne confère aucune autorité.
10. Les conclusions propres à un domaine ne modifient pas silencieusement les règles canoniques de gouvernance. Les changements normatifs suivent le cycle de vie gouverné.
11. La capacité SACM de GovCheck doit préserver chaque construction du métamodèle SACM épinglé et signaler toute sémantique non prise en charge ; aucune construction normative SACM ne peut être supprimée ou simplifiée silencieusement.
12. Les règles propres à la sécurité — par exemple revue du modèle de menace et acceptation du risque — s'appliquent dans leur domaine déclaré et ne deviennent pas des règles universelles pour des préoccupations sans rapport.

## 8. Recommandations et travaux par étapes

### Recommandations

- Conserver le modèle de gouvernance et de cycle de vie de l'ensemble du dépôt comme principe organisateur de GovCheck.
- Traiter les capacités métier comme composables et sélectionnables ; ne rendre obligatoires pour chaque projet ni la sécurité, ni les méthodes formelles, ni les tests, ni aucune discipline unique.
- Utiliser PEAK comme méthode de raisonnement et de traçabilité des décisions lorsque leur importance le justifie. Ne pas le comparer à SACM.
- Se conformer au métamodèle SACM dans la capacité dédiée aux dossiers d'assurance. Ne pas étendre le périmètre de SACM jusqu'à remplacer la gouvernance globale, l'autorité ou le cycle de vie des dépôts de GovCheck.
- Préserver la distinction entre gouvernance normative, méthodes métier, preuves, arguments d'assurance et décisions autorisées.
- Garder un modèle extensible et neutre vis-à-vis des méthodes. Préférer des adaptateurs et mappings explicites plutôt que de forcer chaque discipline dans un standard externe unique.

### Séquence proposée

1. **Cartographie des capacités du dépôt :** rapprocher la liste des domaines des spécifications, architectures, catalogue d'artefacts et capacités de bootstrap existants. Identifier recouvrements, omissions, dépendances et responsabilités.
2. **Mapping sémantique transverse :** relier les concepts communs des documents 0002/0003/0005/0013/0017/0021 aux enregistrements propres aux domaines sans dupliquer identité, provenance, autorité ou cycle de vie.
3. **Enregistrement de décision et vue PEAK :** définir les liens entre Problem, Experience, Assumptions, Knowledge, alternatives, Solution, Assumed Risk, autorité et réévaluation ultérieure.
4. **Contrats observation/constat :** définir des enregistrements généraux d'événement/observation et de constat/preuve dérivé, avec liaison au sujet exact, provenance, incertitude, vie privée et invalidation.
5. **Parcours de retour par domaine :** spécifier comment les observations mettent à jour l'évaluation pertinente — maintenabilité, adéquation des tests, état des dépendances ou hypothèses de menace — sans modifier silencieusement les règles normatives.
6. **Prototype de conformité SACM :** dériver l'inventaire complet du métamodèle Beta 1, implémenter la matrice de couverture sémantique et tester l'import/représentation/export/aller-retour sans perte. Relier les dossiers d'assurance aux objectifs, exigences, artefacts, preuves, changements et décisions GovCheck par des mappings typés explicites.
7. **Modèles formels et tests :** vérifier les propriétés communes de cycle de vie telles que l'autorité, l'invalidation, la revue et l'acceptation, puis ajouter des propriétés propres aux domaines lorsque cela se justifie.
8. **Intégration au bootstrap :** exposer les capacités métier et leurs dépendances dans le profil guidé, avec sélection, omission, migration et comportement non destructif explicites.

## 9. Limites et décisions non prises

Ce document ne finalise pas une taxonomie universelle des domaines, ne sélectionne ni base graphe ni sérialisation, ne prescrit pas un score unique de qualité/risque, ne rend pas PEAK obligatoire pour chaque décision, ne fait pas de SACM le métamodèle de toute la gouvernance du dépôt et ne prétend pas que la collecte d'observations ou la réévaluation automatisée soient implémentées. Il ne rend obligatoires ni la sécurité ni la vérification formelle pour chaque dépôt.

La question centrale est de savoir comment GovCheck peut gouverner un dépôt pendant tout son cycle de vie tout en permettant à différents domaines et méthodes d'ingénierie de coexister : des sémantiques communes d'identité, d'autorité, de provenance, de décision et de cycle de vie, avec des modèles et exigences de preuve propres aux domaines lorsque cela est réellement nécessaire. PEAK contribue à la traçabilité décisionnelle ; SACM fournit le métamodèle des dossiers d'assurance dans son domaine. Aucun ne remplace l'architecture globale de gouvernance GovCheck.
