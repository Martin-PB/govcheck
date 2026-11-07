# 0027 — Référentiels sémantiques métier, modèles de décision et engagements du bootstrap

**Statut :** proposition d'architecture et de conception produit soumise à revue. Elle établit une cible de découverte et d'intégration ; elle n'adopte pas tous les standards cités, n'implémente aucun parseur ou moteur et ne revendique aucune conformité.
**Langue :** l'anglais est la langue par défaut ; voir le [document anglais](0027-domain-semantic-standards-decisions-and-bootstrap.md).

## 1. Objectif

GovCheck gouverne un dépôt logiciel pendant tout son cycle de vie. Son périmètre comprend l'intention du projet, les exigences, l'architecture, l'implémentation, la maintenabilité, les tests, la vérification et les preuves, les dépendances et la chaîne d'approvisionnement, la sécurité, la vie privée, la sûreté, la documentation, la conformité, le build et les publications, l'exploitation, la maintenance et le retrait.

Le bootstrap guidé doit donc faire davantage que sélectionner des outils ou générer des répertoires. Il doit aider le responsable du projet à prendre des engagements explicites et révisables concernant :

- les domaines du cycle de vie et de l'ingénierie applicables ;
- les méthodes et processus de décision utilisés dans ces domaines ;
- les standards, métamodèles, vocabulaires et formats d'échange adoptés, avec leurs versions exactes ;
- le modèle sémantique faisant autorité pour chaque catégorie d'artefact ou de décision ;
- les relations entre ces modèles, le modèle canonique de gouvernance GovCheck et les autres modèles ;
- les obligations de conformité, validation, provenance et migration qui en découlent ;
- les personnes autorisées à approuver, déroger, examiner ou modifier chaque engagement.

Le résultat est un **profil sémantique de projet** gouverné et versionné, pas un score de maturité ni un catalogue obligatoire de tous les standards possibles.

## 2. Principe d'architecture : un système de gouvernance, plusieurs sémantiques spécialisées

GovCheck ne doit pas remplacer les modèles métier éprouvés par un métamodèle universel propriétaire. Il ne doit pas non plus aplatir des concepts métier distincts en enregistrements génériques au seul motif qu'ils participent au même cycle de vie.

L'architecture comporte quatre couches coopérantes :

1. **Gouvernance canonique GovCheck :** identité et intention du projet ; autorité et délégation ; objectifs et exigences ; applicabilité ; décisions et exceptions ; cycle de vie des changements ; identité et révision des artefacts ; approbations ; politiques ; gouvernance du dépôt dans son ensemble.
2. **Capacités sémantiques spécialisées :** modèles complets et versionnés pour les domaines disposant d'un standard adapté ou d'une méthode bien définie (par exemple SACM pour l'assurance, DMN pour la logique décisionnelle, RAAML pour l'analyse des risques ou SysML v2 pour la modélisation système).
3. **Relations intermodèles :** liens explicites, typés et tenant compte des versions entre objets, sans confondre leurs significations ni transférer implicitement l'autorité.
4. **Adaptateurs, représentations et outils :** fichiers de modèles natifs, formats d'échange, validateurs, évaluateurs, éditeurs et outils externes. Un format de sérialisation n'est pas en soi le modèle sémantique ; un adaptateur ne remplace pas la couverture sémantique.

Chaque modèle adopté reste une référence pour les concepts qu'il définit dans son périmètre déclaré. GovCheck demeure responsable de la gouvernance du dépôt et des décisions explicites d'adoption, d'applicabilité, d'autorité et de cycle de vie du projet.

## 3. Décisions à prendre lors du bootstrap d'un projet

Le bootstrap doit découvrir les décisions pertinentes dans le contexte du projet. Il ne doit pas imposer à chaque projet un questionnaire exhaustif. Pour chaque décision, prévoir au minimum les états : **sélectionné**, **non applicable** (avec justification), **différé** (avec responsable et échéance/condition de revue) et **inconnu/non évalué**. Ne jamais transformer silencieusement un état inconnu en faux, non applicable ou accepté.

### 3.1 Contexte et intention du projet

- finalité, résultats attendus, parties prenantes, utilisateurs et environnement opérationnel ;
- type de produit/système/logiciel, frontières, composants et services externes ;
- criticité et conséquences d'une défaillance ;
- catégories de données, sensibilité, vie privée et exposition de sécurité ;
- modèle de déploiement, de mise à jour, de support et de retrait ;
- obligations légales, réglementaires, contractuelles, sectorielles et organisationnelles déclarées par un responsable compétent ;
- population de contributeurs, modèle de collaboration, VCS, hébergement et frontières de confiance.

Une étiquette de projet ou un profil ne doit pas servir à déduire la conformité légale, l'acceptabilité d'un risque, la criticité ou l'autorité sans faits justificatifs et décision responsable.

### 3.2 Gouvernance et autorité

- responsable du projet et personnes pouvant définir ou modifier une politique normative ;
- autorité décisionnelle, délégation, séparation des tâches et revue indépendante ;
- exigences d'approbation des changements et publications ;
- politique d'exigences et de traçabilité ;
- autorité des exceptions/dérogations, périmètre, justification, expiration et mesures compensatoires ;
- propriété du risque et autorité d'acceptation du risque ;
- attentes de conservation des preuves, provenance et publication ;
- voies de contestation, recours, escalade et modification des politiques.

Autorité, privilège d'exécution, capacité technique, revue et approbation sont distincts. Un outil ou une identité CI ne doit pas acquérir une autorité normative du seul fait qu'il peut écrire dans le dépôt ou fusionner un changement.

### 3.3 Domaines d'ingénierie et du cycle de vie

Le catalogue de capacités doit au minimum évaluer l'applicabilité des domaines suivants :

| Domaine | Décisions de bootstrap et sorties possibles |
|---|---|
| Exigences et besoins des parties prenantes | Types et sources d'exigences, identités stables, baselines, allocation, traçabilité, changements et stratégie de vérification. |
| Architecture et conception | Cadre de description d'architecture, parties prenantes/préoccupations, points de vue/vues, types de modèles, décisions de conception, interfaces et contraintes. |
| Implémentation et maintenabilité | Conventions de code/build, analyse statique, typage, mesures de complexité et maintenabilité, dette technique et politique de remédiation. |
| Tests et vérification | Niveaux de test, conception des tests, tests fondés sur les modèles, interprétation de couverture, analyses statique/dynamique, vérification formelle si justifiée, revue indépendante. |
| Assurance et preuves | Claims, arguments, preuves, contextes, hypothèses, defeaters, évaluation, fraîcheur, provenance et conformité. |
| Risques, sûreté et sécurité | Méthode de risque, analyses de dangers/menaces, objectifs de sûreté/sécurité, mesures, risque résiduel, supervision et acceptation autorisée. |
| Vie privée et gouvernance des données | Inventaire/classification des données, finalités, conservation, accès, risque relatif à la vie privée et obligations de preuve. |
| Dépendances et chaîne d'approvisionnement | Identité des composants, SBOM, licences, provenance, avis/vulnérabilités, attestations, entrées de build et assurance fournisseur. |
| Documentation et conformité | Documents d'information requis, documents contrôlés, références normatives, obligations de conformité, enregistrements et cycles de revue. |
| Build, publication et déploiement | Reproductibilité, provenance du build, attestations d'artefacts, identité de publication, configuration de déploiement et retour arrière. |
| Exploitation et maintenance | Observabilité, incidents, objectifs de service, sauvegarde/reprise, maintenance, déclencheurs de réévaluation et retrait. |
| Connaissances et décisions | Décisions, justification, expérience, hypothèses, connaissances, incertitude, leçons apprises et risques assumés. |
| Processus et collaboration | Rôles humains/agents, flux de travail, approbations, transmissions, gestion de cas, escalade et protocoles de collaboration. |
| Mesure et amélioration | Définitions de métriques, méthodes de mesure, unités, références initiales, interprétation, objectifs qualité et décisions d'amélioration. |

La sécurité est un domaine spécialisé parmi d'autres, pas le modèle universel. Les méthodes formelles sont également choisies en fonction des claims et du contexte ; aucune capacité de méthode formelle n'est obligatoire pour tous les projets.

### 3.4 Engagements de méthode, standard et modèle

Pour chaque domaine applicable, le bootstrap doit établir :

- le problème, le claim, le besoin ou le résultat visé par la méthode ;
- la méthode choisie et les alternatives considérées ;
- le standard/métamodèle/vocabulaire et sa version/profil exacts ;
- son statut (formel, projet, bêta, retiré, organisationnel ou défini par le projet) ;
- le périmètre d'adoption et les exclusions explicites ;
- les formats natifs et d'échange/sérialisation ;
- la chaîne d'outils, les validateurs, évaluateurs et leurs hypothèses de confiance ;
- la cible de conformité et les preuves requises pour la revendiquer ;
- le responsable, l'autorité d'approbation et la périodicité de revue ;
- les dépendances, conflits, politique de migration et déclencheurs de mise à jour ;
- les liens typés vers les objets de gouvernance GovCheck et les autres modèles adoptés.

La présence d'un standard dans le catalogue ne vaut pas adoption. L'adoption d'un standard n'implique pas que chaque projet doive utiliser toutes ses fonctionnalités facultatives. La capacité d'un outil à lire un fichier ne prouve ni la complétude sémantique ni la conformité.

## 4. Standards et méthodes sémantiques candidats

La liste suivante est un inventaire initial de découverte, volontairement large ; ce n'est ni une décision d'adoption ni l'affirmation que tous les candidats ont la même maturité. Le catalogue devra être maintenu avec sources primaires, version/statut, artefacts lisibles par machine, périmètre, contraintes de licence/accès, maturité des implémentations, lacunes connues et date de dernière revue.

| Domaine | Candidat | Nature et rôle potentiel dans GovCheck | Limite / statut à vérifier |
|---|---|---|---|
| Dossiers d'assurance | OMG SACM | Modèle sémantique complet des dossiers d'assurance : claims, arguments, preuves, artefacts, terminologie, contextes et constructions de soutien. | Capacité d'assurance dédiée ; cible de couverture sémantique complète, pas modèle de gouvernance du dépôt. Épingler la version exacte ; 2.4 Beta 1 est une cible d'ingénierie, 2.3 reste formelle au moment de la recherche. |
| Logique décisionnelle | OMG DMN | DRG, tables de décision, expressions et logique FEEL ; rend la logique explicite, inspectable et potentiellement exécutable. | Modélise comment un résultat est déterminé, pas la justification complète, l'autorité ni l'approbation du cycle de vie. DMN 1.6 formelle ; 1.7 Beta 1 dans le catalogue OMG de septembre 2026. |
| Orchestration des processus | OMG BPMN | Notation/modèle standard des activités, événements, passerelles, messages, rôles/couloirs et flux de processus. | Modélise le déroulement du travail ; ne remplace ni la logique DMN ni l'autorité GovCheck. BPMN 2.0.2 est formel. N'impose aucun moteur de workflow. |
| Gestion adaptative de cas | OMG CMMN | Modèle de cas pour le travail centré sur l'information, moins prédéterminé, où les travailleurs du savoir décident des prochaines actions. | Potentiellement adapté aux enquêtes, incidents, exceptions et revues d'assurance ; distinct du flux de processus plus prédéfini de BPMN. CMMN 1.1 est formel. |
| Justification des décisions | PEAK | Problem, Experience, Assumptions et Knowledge alimentent une décision ; l'enregistrement expose Solution et Assumed Risk. | Raisonnement et traçabilité décisionnels, pas langage exécutable de tables de décision ni métamodèle de dossier d'assurance. Garder PEAK distinct de DMN et SACM. |
| Analyse des risques | OMG RAAML | Modélisation structurée de méthodes d'analyse des risques, avec profils/bibliothèques pour FMEA/AMDEC, FTA, STPA et analyses de sûreté/sécurité apparentées. | Sémantique d'analyse des risques, pas autorité ni acceptation du risque. RAAML 1.1 formelle ; 1.2 Beta 1 figure au catalogue OMG de septembre 2026. |
| Ingénierie des exigences | ISO/IEC/IEEE 29148 ; OMG ReqIF | Processus/informations d'ingénierie des exigences ; ReqIF prend en charge l'échange structuré d'exigences. | 29148 est un guide de processus/informations, ReqIF un format d'échange ; aucun des deux ne fournit à lui seul toute l'autorité GovCheck et le cycle de vie décisionnel. Vérifier l'édition/statut de 29148 (un DIS de troisième édition était listé en 2026). |
| Description d'architecture | ISO/IEC/IEEE 42010 | Structure de description d'architecture, parties prenantes, préoccupations, points de vue, vues, types de modèles et exigences de cadre. | Cadre de description, pas langage universel unique de modélisation d'architecture. 42010:2022 est publiée. |
| Modélisation système | OMG SysML v2 et KerML | Modélisation textuelle/graphique précise des exigences, structures, comportements, analyses et vérifications, avec interopérabilité par API. | Langage étendu d'ingénierie système ; potentiellement excessif pour des dépôts logiciels ordinaires. SysML 2.0 formel (catalogue septembre 2025). |
| Modélisation des tests | OMG UML Testing Profile 2 (UTP 2) | Spécification de tests fondée sur les modèles et artefacts de test structurés liés aux modèles système et exigences. | Distinguer UTP 2 de l'ancien UTP 1.x ; la page OMG liste UTP 2.3 Beta 1, maturité et support d'implémentation à examiner. |
| Qualité produit | ISO/IEC 25010:2023 | Caractéristiques/sous-caractéristiques de qualité produit utilisées pour spécifier, mesurer et évaluer la qualité. | Vocabulaire/modèle qualité, pas processus complet de management qualité ni système de métriques. |
| Mesure | OMG SMM et/ou modèles de mesure propres au projet | Candidat pour représenter les mesures, méthodes de mesure et résultats de façon structurée. | Traiter SMM comme candidat à une étude complémentaire des sources, du statut et des implémentations ; ne pas en faire une dépendance adoptée avant cette étude. |
| Provenance | OMG PPMN ; famille W3C PROV | Modèles de provenance/filiation des entités, activités, agents, dérivations et responsabilités entre artefacts et processus. | PPMN et PROV sont des candidats complémentaires, pas des substituts présumés. Le catalogue OMG liste PPMN 1.0 formel (septembre 2026) ; W3C PROV comprend PROV-DM, PROV-O, PROV-XML et les contraintes. |
| Inventaire de chaîne d'approvisionnement | SPDX ; CycloneDX | Inventaires machine-readable de composants logiciels, licences, relations, vulnérabilités, services et informations de chaîne d'approvisionnement. | Choisir selon les cas d'usage et l'écosystème ; une SBOM ne prouve ni la sûreté d'un composant ni une provenance complète. SPDX 3.0 est la version courante dans son catalogue ; épingler séparément la version CycloneDX. |
| Développement sécurisé | NIST SSDF (SP 800-218) | Pratiques et résultats de développement sécurisé sur le cycle de vie logiciel. | Référentiel de pratiques, pas métamodèle complet lisible par machine ni langage de politique exécutable. |
| Conformité open source | OpenChain ISO/IEC 5230 ; ISO/IEC 18974 | Exigences de processus pour la conformité des licences open source et l'assurance de sécurité. | Standards organisationnels/de processus ; adoption et revendications de certification nécessitent des preuves distinctes. |
| Gouvernance sémantique et contraintes | RDF, OWL 2, SKOS, SHACL, JSON-LD, W3C PROV | Vocabulaires, ontologies, contraintes et représentations de données liées pour l'intégration sémantique multidomaine. | À utiliser lorsque les sémantiques de graphe/ontologie apportent une valeur réelle ; ne pas imposer de base de graphe RDF. |
| Motivation métier et règles | OMG BMM, SBVR et DMN | Motivation/objectifs/influenceurs, vocabulaire/règles métier et logique décisionnelle. | Couches complémentaires ; ne pas confondre motivation, autorité normative, vocabulaire et logique décisionnelle exécutable. |

Cet inventaire est volontairement extensible. Il doit être enrichi par des recherches domaine par domaine plutôt que traité comme une liste fermée. Les standards candidats doivent être comparés selon leur portée sémantique, maturité, ouverture, artefacts lisibles par machine, interopérabilité, écosystème d'implémentation, charge de maintenance et adéquation au cycle de vie GovCheck — pas selon leur notoriété.

## 5. PEAK, DMN, BPMN, CMMN et SACM : complémentaires, pas concurrents

Ces modèles peuvent concerner une même décision gouvernée tout en répondant à des questions différentes.

| Modèle | Question principale | Responsabilité GovCheck qu'il peut soutenir |
|---|---|---|
| PEAK | Pourquoi cette décision a-t-elle été prise, sur la base de quel Problem, Experience, Assumptions et Knowledge, et quelle Solution et quel Assumed Risk ont été consignés ? | Justification lisible par un humain, traçabilité épistémique, incertitude et enregistrement du risque assumé. |
| DMN | Étant donné des entrées et exigences décisionnelles déclarées, quel résultat découle des règles/expressions spécifiées ? | Logique décisionnelle explicite, testable et potentiellement exécutable, décisions dépendantes et tables de décision. |
| BPMN | Quelles activités, événements, rôles, transmissions et branches de processus conduisent du déclencheur au résultat ? | Description des processus/workflows, routage des approbations et séquencement opérationnel. |
| CMMN | Comment gérer un cas d'informations, tâches et jugement humain évolutifs lorsque l'étape suivante n'est pas entièrement prédéterminée ? | Enquêtes, incidents, exceptions, revues d'assurance et gestion adaptative de cas. |
| SACM | Quel claim d'assurance est formulé, quel argument le soutient, quelles preuves/contextes/hypothèses sont impliqués et comment est-il évalué ? | Dossier d'assurance structuré et sémantique complète de ses arguments/preuves. |
| Gouvernance GovCheck | Qui est autorisé à décider ou approuver, quelle politique s'applique, quel est le sujet/révision gouverné et quel effet de cycle de vie la décision produit-elle ? | Autorité normative, applicabilité, approbation, exception, changement et contrôle du cycle de vie du dépôt. |

### 5.1 Exemple : sélection d'un profil de gouvernance au bootstrap

Supposons que GovCheck doive déterminer si un dépôt doit activer une capacité de gouvernance de la vie privée.

- **DMN** peut modéliser les exigences décisionnelles et les règles à partir d'entrées déclarées comme la classification des données, la finalité du traitement, l'exposition et la juridiction déclarée. Son résultat est une recommandation ou un résultat d'applicabilité calculé selon les hypothèses du modèle.
- **PEAK** consigne le problème, l'expérience pertinente, les hypothèses et les connaissances, la solution choisie, l'incertitude et le risque assumé. Il explique pourquoi le responsable compétent accepte ou rejette la recommandation.
- **GovCheck** lie la décision au projet et à la révision du profil, vérifie l'autorité du décideur, enregistre l'approbation et gouverne son effet sur le dépôt.
- **BPMN**, si utile, décrit le processus de collecte du contexte, d'exécution de la décision, de revue, d'obtention de l'approbation et d'application du profil.
- **SACM**, lorsqu'une assurance est nécessaire, structure l'argument et les preuves soutenant des claims sur le profil obtenu ou ses contrôles.

Aucun modèle n'assume silencieusement la responsabilité d'un autre. Un résultat DMN n'est pas une approbation ; un enregistrement PEAK n'est pas une autorisation ; l'achèvement d'une tâche BPMN n'est pas une preuve ; une évaluation SACM n'est pas une permission de modifier la politique du dépôt.

### 5.2 Exemple : acceptation d'un changement

Un changement peut déclencher une décision DMN sur les revues requises selon le type de changement, les actifs touchés, le risque et la politique. BPMN peut décrire la séquence de revue et d'approbation. PEAK peut consigner une décision non routinière ou un compromis accepté. SACM peut soutenir les claims d'assurance concernant le système modifié. GovCheck lie l'ensemble au candidat de changement et à la révision exacts, vérifie l'autorité et enregistre le résultat normatif d'acceptation.

### 5.3 Ne pas sur-automatiser

DMN peut être exécutable, mais toute décision ne doit pas être automatisée. Certaines décisions exigent jugement humain, délibération, négociation ou acceptation responsable de l'incertitude. Un modèle DMN peut renvoyer « évaluation humaine requise », « informations insuffisantes » ou « escalade ». Le modèle doit rendre explicites les entrées manquantes et hypothèses.

BPMN est un modèle de processus, pas une obligation d'installer ou d'exécuter un moteur de workflow. CMMN est un modèle de cas, pas une raison de transformer chaque interaction de gouvernance en système de gestion de cas. GovCheck peut initialement valider et publier ces modèles sans les exécuter.

## 6. Relations intermodèles typées

L'intégration intermodèles doit être explicite et typée. Une similitude d'étiquettes n'établit aucune équivalence sémantique.

Exemples de relations :

- un objectif de projet GovCheck **motive** une exigence ;
- une exigence **contraint** un élément d'architecture ;
- une décision DMN **détermine/recommande** un résultat d'applicabilité à partir d'entrées déclarées ;
- un enregistrement PEAK **justifie** une décision responsable et consigne hypothèses/risque assumé ;
- un processus BPMN **orchestre** les activités de collecte des entrées, d'évaluation des décisions et d'obtention des approbations ;
- un cas CMMN **organise** des preuves, tâches et jugements évolutifs ;
- une analyse RAAML **identifie/évalue** un scénario de risque ou danger selon une méthode déclarée ;
- une mesure de maîtrise **réduit/répond à** un scénario de risque ;
- un test ou une mesure **évalue** une propriété ou une mesure de maîtrise dans un périmètre déclaré ;
- un claim SACM **affirme** une proposition délimitée et son argument **est étayé par** des preuves ;
- un enregistrement PPMN/PROV **dérive de / a été produit par / a été attribué à** des entités, activités et agents précis ;
- un enregistrement de composant SPDX/CycloneDX **identifie** un composant ou une relation de chaîne d'approvisionnement.

Chaque type de relation doit définir les sortes de source et cible, cardinalités, direction, versions applicables, provenance, comportement de cycle de vie et effets d'invalidation/réévaluation. Aucun lien intermodèle ne peut silencieusement :
- transformer une observation en incident, risque, preuve ou approbation ;
- transformer une recommandation en obligation ;
- transformer un résultat DMN en décision autorisée ;
- transformer un risque assumé en risque accepté ;
- transformer un claim d'assurance en exigence ;
- transférer l'autorité normative de GovCheck à un modèle ou outil externe.

## 7. Profil sémantique du projet et artefacts du dépôt

Le bootstrap doit produire un profil lisible par machine et versionné comprenant :

- le contexte du projet et les inconnues explicites ;
- les domaines sélectionnés, non applicables et différés ;
- les modèles/standards adoptés, versions exactes et statuts ;
- le périmètre et les sélections de fonctionnalités/profils de chaque modèle ;
- les formats natifs et d'échange ;
- les obligations de validation/conformité et références de chaîne d'outils ;
- l'autorité, la propriété, les revues et la politique de changement ;
- le registre des mappings et relations intermodèles ;
- les dépendances/conflits et règles de migration ;
- les justifications et liens vers les décisions (dont PEAK lorsque utilisé) ;
- les exigences de preuve/provenance et l'identité de révision du profil.

Le dépôt peut exposer les artefacts natifs des modèles à côté des données canoniques de gouvernance GovCheck, par exemple :

```text
governance/
  profile/
  decisions/
  mappings/
models/
  assurance/       # modèles SACM, si sélectionnés
  decisions/       # modèles DMN, si sélectionnés
  processes/       # modèles BPMN, si sélectionnés
  cases/           # modèles CMMN, si sélectionnés
  risks/           # modèles RAAML, si sélectionnés
  architecture/    # descriptions 42010 / modèles SysML, si sélectionnés
  requirements/    # ReqIF ou autre représentation sélectionnée
  provenance/      # représentations PPMN / PROV, si sélectionnées
supply-chain/
  sbom/
quality/
  measures/
  test-models/
```

Cet exemple est indicatif, pas un contrat d'arborescence fixe. Les identifiants stables des capacités/modèles du profil et les métadonnées de propriété font autorité pour la planification. Un projet ne doit pas recevoir de répertoires vides ni prétendre à des intégrations simplement parce qu'un standard figure au catalogue.

Pour chaque modèle adopté, GovCheck doit viser le maintien d'artefacts natifs consommables par les outils lorsque le standard définit un format d'échange ou de sérialisation. L'import/export doit préserver l'intégralité de la sémantique de la version adoptée ; la cible de conformité et le schéma/métamodèle lisible par machine doivent être épinglés. Cela suit le principe de SACM 0026 : couverture sémantique complète, et non conservation opaque comme substitut à la compréhension.

## 8. Conformité, versions et cycle de vie

Pour chaque modèle adopté, distinguer :

1. **Couverture sémantique :** GovCheck sait représenter et comprendre toutes les constructions du périmètre adopté.
2. **Conformité de sérialisation/échange :** les fichiers sont valides selon les schémas/métamodèles et règles de sérialisation exacts.
3. **Conformité comportementale :** tout évaluateur ou moteur d'exécution suit le comportement spécifié par le standard.
4. **Fidélité aller-retour :** import/export préserve identités et sémantique.
5. **Interopérabilité des outils :** des outils indépendants peuvent consommer et échanger les artefacts.
6. **Adoption par le projet :** le projet a explicitement adopté le modèle et déclaré son périmètre.
7. **Usage opérationnel :** le projet utilise réellement le modèle et ses contrôles/processus.

Ne pas déduire un niveau d'un autre. Un fichier syntaxiquement valide ne prouve pas une couverture sémantique complète ; un rapport de conformité ne prouve pas que le projet a correctement appliqué le modèle.

Chaque mise à jour de version doit être une migration gouvernée explicite : comparer les artefacts normatifs et lisibles par machine, identifier changements sémantiques et dépréciations, produire un plan de migration, préserver les entrées originales et leur provenance, rapporter compatibilité/pertes et exiger une approbation avant de changer le profil actif. Les versions bêta/projet doivent être étiquetées comme telles et ne pas être présentées comme des standards formels.

Le projet peut adopter un modèle à la fois, en différer d'autres ou utiliser des méthodes propres au projet lorsqu'aucun standard adapté n'existe. GovCheck doit préserver la justification et le périmètre de ces choix et permettre leur réévaluation ultérieure.

## 9. Séquence de recherche et d'implémentation

1. **Inventaire des décisions de bootstrap :** étendre l'Architecture 0024 avec les domaines et dimensions d'engagement de ce document ; définir la sémantique inconnu/non applicable/différé.
2. **Catalogue de standards :** créer un catalogue versionné avec sources primaires, statut, artefacts lisibles par machine, périmètre, mappings, écosystème d'implémentation et date de revue.
3. **Matrices de couverture sémantique :** pour chaque standard sélectionné, inventorier toutes les constructions et contraintes et les relier à des concepts GovCheck de première classe, comme exigé pour SACM dans l'Architecture 0026.
4. **Prototype de modèle de décision :** évaluer la structure d'enregistrement PEAK avec les modèles DMN ; démontrer une décision de bootstrap avec entrées, règles, justification, autorité et approbation explicites. Ne pas imposer de moteur DMN au cœur.
5. **Évaluation des modèles de processus :** déterminer si BPMN et/ou CMMN apporte de la valeur aux workflows GovCheck réels avant de sélectionner un runtime ou moteur.
6. **Contrat de relations intermodèles :** définir liens typés, identité, provenance, invalidation et sémantique du cycle de vie.
7. **Interopérabilité des artefacts natifs :** valider des modèles représentatifs avec des outils indépendants et tester les aller-retours.
8. **Adoption gouvernée :** seule une décision explicite du projet peut activer un standard/version/profil comme référence normative pour ce dépôt.

## 10. Décisions volontairement laissées ouvertes

Ce document n'adopte pas DMN, BPMN, CMMN, RAAML, SysML, UTP, PPMN, ReqIF, SPDX, CycloneDX ni aucun autre candidat pour tous les dépôts. Il ne choisit aucun moteur d'exécution, moteur de workflow, base de graphe, sérialisation universelle, pile d'ontologies ou méthode formelle obligatoire. Il ne rend pas PEAK exécutable et ne remplace pas PEAK par DMN. Il établit l'architecture et les questions de bootstrap nécessaires pour prendre ces décisions délibérément et avec traçabilité.

## 11. Références primaires et instantanés de version/statut

Les sources primaires suivantes ont été consultées lors de la préparation de ce document. Les versions/statuts sont un instantané de recherche daté, pas un engagement à suivre une URL « latest » mouvante :

- [Catalogue des spécifications OMG](https://www.omg.org/specifications/) — DMN 1.6 formel et 1.7 Beta 1 ; RAAML 1.1 formel et 1.2 Beta 1 ; PPMN 1.0 formel ; SACM 2.3 formel et 2.4 Beta 1 ; BPMN 2.0.2 formel ; CMMN 1.1 formel ; SysML 2.0 formel.
- [OMG DMN 1.6](https://www.omg.org/spec/DMN/1.6/) et [DMN 1.7 Beta 1](https://www.omg.org/spec/DMN/).
- [OMG BPMN](https://www.omg.org/spec/BPMN/) et [OMG CMMN](https://www.omg.org/cmmn/index.htm).
- [OMG RAAML 1.2 Beta 1](https://www.omg.org/spec/RAAML/1.2/Beta1) et [RAAML 1.1](https://www.omg.org/spec/RAAML/1.1).
- [OMG SysML v2](https://www.omg.org/spec/SysML/) et [présentation de SysML v2](https://www.omg.org/sysml/sysmlv2/).
- [OMG UTP 2](https://www.omg.org/spec/UTP2).
- [OMG PPMN](https://www.omg.org/spec/PPMN/).
- [ISO/IEC/IEEE 42010:2022](https://www.iso.org/standard/74393.html), [ISO/IEC/IEEE 29148](https://www.iso.org/standard/94091.html) et [ISO/IEC 25010:2023](https://www.iso.org/standard/78176.html).
- [Spécifications SPDX](https://spdx.dev/use/specifications/), [CycloneDX](https://cyclonedx.org/specification/) et [NIST SSDF SP 800-218](https://csrc.nist.gov/pubs/sp/800/218/final).
- [Vue d'ensemble W3C PROV](https://www.w3.org/TR/prov-overview/).

## 12. Relations avec les documents GovCheck existants

Ce document affine et relie, sans les remplacer :

- Spécification 0002 — autorité et composition canoniques de la gouvernance ;
- Spécification 0005 — assurance, claims, preuves, méthodes et confiance ;
- Architecture 0013 — métamodèle de gouvernance du dépôt ;
- Architecture 0017 — identité, révision et versionnement des artefacts ;
- Architecture 0021 — claims d'assurance, arguments, fraîcheur et invalidation ;
- Architecture 0024 — bootstrap guidé et profils de capacités métier ;
- Architecture 0025 — observations du cycle de vie et relations PEAK/SACM ;
- Architecture 0026 — couverture sémantique complète et interopérabilité native SACM.

La règle directrice est : **les modèles spécialisés conservent leurs sémantiques propres ; GovCheck gouverne leur adoption, leur autorité, leur cycle de vie et leurs relations typées.**
