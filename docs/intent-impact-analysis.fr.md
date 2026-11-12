# Analyse d'impact de l'intention — constitution et cycle de vie de la gouvernance

**Statut :** audit de conception de travail destiné à la revue des mainteneurs ; ce document n'est ni un ADR, ni un acte d'adoption, ni un contrat d'implémentation.  
**Document parent :** [Intention GovCheck](intent.fr.md). **English:** [Intent impact analysis](intent-impact-analysis.md).

## 1. Constat exécutif

L'intention élargie ne nécessite pas d'abandonner les fondations existantes. Les architectures 0013–0015 et 0021–0027, ainsi que les spécifications 0002–0006, anticipent déjà une grande partie des concepts et comportements requis : gouvernance canonique, bootstrap progressif, méthodes d'assurance sélectionnables, autorité et délégation circonscrites, traçabilité des sources, sémantiques métier, évaluation en échec fermé, exceptions bornées et conformité des changements.

La lacune principale est leur intégration. Ces éléments restent dispersés dans des documents de statuts et de maturités différents. Ils ne constituent pas encore un modèle produit intégré, adopté et exécutable. La prochaine phase doit réconcilier sémantiques, autorités et dépendances du cycle de vie avant d'implémenter un nouveau questionnaire ou de réécrire le bootstrapper.

GovCheck doit être compris comme un **système de constitution de gouvernance, d'aide à la décision, d'assurance et de conformité du cycle de vie**. Le bootstrap en est le premier processus guidé de constitution, pas un questionnaire plat exécuté une seule fois. Les décisions sont catégorisées par domaine, confiées à des autorités compétentes, éclairées par des sources contextualisées et réexaminées lorsque des changements pertinents invalident leur fondement.

## 2. Discipline de statut

Cette analyse distingue :
- **Décision consignée :** décision explicite avec sa base d'autorité (notamment l'architecture 0023 pour l'autorité racine actuelle de GovCheck et l'ADR 0004 pour la gouvernance des versions).
- **Conception proposée :** contenu d'architecture/spécification en attente de l'acte d'adoption applicable.
- **Capacité implémentée ou vérifiée :** uniquement ce que démontrent les artefacts et éléments d'exécution du dépôt. Un document de conception ou un rapport de model checking ne démontre pas une capacité opérationnelle.
- **Constat d'impact :** compatibilité, lacune, ambiguïté ou précision nécessaire identifiée par comparaison avec l'intention.

Il s'agit d'un premier audit sémantique, pas encore d'un audit ligne à ligne de chaque fichier d'implémentation, modèle, test, issue, workflow CI et traduction.

## 3. Fondations existantes à préserver

| Document | Contribution existante | Impact |
|---|---|---|
| ADR 0001 | Gouvernance centrée sur le dépôt, autorité normative unique, exécutable local, séparation VCS/forge, Git et Pijul distincts. | Compatible. Préciser la constitution progressive plutôt qu'une installation d'arbre fixe. |
| ADR 0003 | Séparation du package produit générique et de l'historique méta propre à GovCheck. | Compatible en principe. Définir le package comme source de modèles, connaissances et mécanismes de génération, pas comme politique universelle ou arbre à copier aveuglément. |
| ADR 0007 | Enregistrement obligatoire des sources pour les décisions de conception de GovCheck. | Compatible. Étendre la provenance des sources à chaque dépôt utilisateur et à chaque décision pertinente. |
| Architecture 0012 | Autorité canonique, projections contrôlées, identifiants de règles et détection de dérive. | Compatible. Ajouter l'autorité par catégorie et les recommandations contextualisées issues des sources. |
| Architecture 0013 | Objectifs, exigences, normes, propriétés, contrats, modèles, méthodes, preuves, affirmations, arguments, décisions et justification PEAK. | Fondation centrale. Faire des délégations d'autorité et des sources qualifiées des objets liés de premier ordre. |
| Architecture 0014 | Contributeur, réviseur, évaluateur, autorisateur et dossier de changement gouverné. | Compatible. Circonscrire les pouvoirs par catégorie de décision et action, pas seulement par étape du workflow. |
| Architecture 0015 | Découverte, conformité documentaire, traçabilité, contrôles, assurance et autorité/application. | Compatible mais incomplet comme carte produit : constitution et aide à la décision doivent être explicites. |
| Architecture 0018 + ADR 0004 | Identité/versionnement par catégorie et autorité d'approbation. | Fondation adoptée ; préserver. Ne pas confondre versionnement d'artefact et autorité politique. |
| Architecture 0021 | Affirmations, arguments, preuves, dépendances, invalidation et fraîcheur. | Compatible. Relier choix/substitution de méthode à l'autorité, la justification et les conséquences. |
| Architecture 0022 | Écart entre vocabulaire de conception et autorité/évaluateur machine lisible adopté. | Toujours pertinent ; actualiser son état de référence à la lumière de l'intention élargie. |
| Architecture 0023 | Une autorité racine actuelle pour GovCheck ; délégation uniquement par évolution gouvernée explicite. | Décision existante pour GovCheck. Ne pas imposer cette structure à propriétaire unique aux utilisateurs. |
| Architecture 0024 | Bootstrap progressif, contexte, choix de gouvernance, domaines/méthodes sélectionnables, inspecter-planifier-appliquer. | Très forte convergence. Étendre le dialogue aux décisions ultérieures déclenchées par les changements. |
| Architecture 0025 | Observations du cycle de vie, justification PEAK et intégration SACM. | Compatible. PEAK, SACM et autorité GovCheck restent distincts. |
| Architecture 0026 | Capacité SACM 2.4 dédiée et objectif de couverture sémantique. | Capacité spécialisée compatible ; pas le métamodèle universel de GovCheck. |
| Architecture 0027 | Modèles métier spécialisés et engagements sémantiques progressifs ; distinctions DMN/BPMN/CMMN/SACM. | Fondation centrale pour des arbres de décision gouvernés, explicables et propres aux domaines. |
| Spécifications 0002–0006 | Modèle canonique, cycle de vie, adaptateurs, assurance et applicabilité temporelle de l'autorité. | Contrats proposés compatibles ; ajouter les liens explicites aux catégories de décision, sources et déclencheurs. |

## 4. Intégration sémantique nécessaire

### 4.1 Constitution progressive et cycle de décision

L'architecture 0024 rejette déjà le questionnaire plat et exhaustif. L'intention exige un cycle continu :
1. Poser uniquement les questions fondatrices nécessaires à l'identité du dépôt et à une autorité initiale sûre.
2. Distinguer décisions, éléments différés, inconnus et non-applicables.
3. Lors d'un changement, détecter les décisions nouvelles qu'exigent les propriétés, domaines, risques, obligations ou changements de gouvernance concernés.
4. Demander la décision manquante à l'autorité compétente, en réutilisant les décisions valides déjà en vigueur.
5. Réexaminer les décisions lorsque hypothèses, sources, périmètres, validité ou dépendances changent.

Concepts nécessaires : déclencheur, catégorie, état, responsable, autorité compétente, échéance/condition de revue, applicabilité, remplacement, déclencheur de réexamen et dépendance à une décision non résolue.

### 4.2 Autorité par catégorie et délégation

Les documents existants fournissent une grande partie du vocabulaire, mais GovCheck a besoin d'un mécanisme cohérent de résolution d'autorité. Une simple étiquette de rôle ne suffit pas. Chaque délégation doit identifier :
- principal/groupe ;
- catégories de décision et actions autorisées (proposer, évaluer, décider, approuver, déléguer, révoquer, accepter un risque) ;
- périmètres dépôt, artefact, domaine et organisation ;
- période de validité et révision de gouvernance effective ;
- contraintes, séparation des tâches et combinaisons interdites ;
- profondeur de délégation et droit éventuel de sous-déléguer ;
- délégant, base d'autorisation, provenance, révocation et remplacement.

L'exemple QA est un cas de validation nécessaire : une autorité QA peut fixer la méthode d'assurance ou les preuves minimales pour une classe de propriétés, tandis que les développeurs proposent et réalisent les changements de code. Les développeurs ne peuvent pas affaiblir l'exigence par le code, les tests ou la CI. À la soumission, GovCheck résout la décision QA applicable et évalue la conformité. Ce modèle ne doit pas devenir l'unique organisation codée en dur.

L'architecture 0023 gouverne uniquement l'autorité racine actuelle de GovCheck. Chaque dépôt utilisateur constitue sa propre organisation d'autorité au moyen de ses décisions de bootstrap autorisées.

### 4.3 Sources comme entrées de décision contextualisées

Le catalogue central de GovCheck est le registre de recherche/provenance de la conception de GovCheck. Il ne remplace pas les registres de sources propres aux dépôts gouvernés.

Une fiche source doit conserver identité stable, éditeur/auteur, titre, type et localisateur ; révision exacte et dates ; section pertinente ; affirmation ou critère soutenu ; conditions d'applicabilité et périmètre ; limites, incertitudes, conflits et sources remplaçantes ; liens vers questions, options, branches, affirmations, arguments, décisions et exigences.

Au moment de décider, GovCheck présente les sources pertinentes au contexte, explique pourquoi chacune est montrée et ce qu'elle étaye ou non, puis conserve la révision exacte utilisée. Une source informe mais n'accorde pas l'autorité et ne prouve pas l'applicabilité. Découverte, qualification, interprétation, recommandation et décision autorisée sont des étapes distinctes. Les agents peuvent aider à résumer et comparer, mais ne transforment pas leur synthèse en approbation.

### 4.4 Arbres de décision et délibération assistée

Les arbres doivent être des artefacts versionnés et révisables, non des heuristiques cachées. Ils définissent sémantique des questions/réponses, prérequis et branches, options et conséquences, liens aux sources/affirmations, chemins inconnu/conflit/non-applicable/différé, autorité compétente, explication de branche, versions et tests.

Un arbre peut recommander ou réduire les options. Il ne décide pas, sauf autorisation explicite d'une règle déterministe par la gouvernance applicable. Un agent est un assistant facultatif de délibération. Le même modèle doit être utilisable par humains, CLI, scripts et autres interfaces.

### 4.5 Choix de méthode d'assurance par affirmation/propriété

La spécification 0005 distingue déjà exécution empirique, model checking, vérification de programme, preuve de théorème, conformité de l'implémentation, fidélité normative et acceptation. Préserver ces significations non interchangeables.

Pour chaque affirmation/propriété, l'enregistrement du choix doit lier proposition exacte, sujet, périmètre et conséquence d'échec ; obligations et risques applicables ; hypothèses et frontières d'abstraction ; méthodes candidates et ce qu'elles établissent ; admissibilité, indépendance, coût, faisabilité et contraintes d'outillage ; incertitude résiduelle ; autorité compétente ; déclencheurs de réévaluation.

Ne pas redemander une décision de test/preuve à chaque changement. Réutiliser une décision valide tant que son périmètre et ses hypothèses restent applicables. La rouvrir si elle est absente, invalidée, contradictoire, hors périmètre ou matériellement affectée. Remplacer une preuve par des tests n'est pas une équivalence : le test reste un témoignage empirique ; le model checking porte sur le modèle et les bornes consignés ; la vérification de preuve porte sur une dérivation sous hypothèses ; la conformité de l'implémentation exige sa propre relation et ses propres éléments.

### 4.6 Échec fermé et assouplissement gouverné

L'intention concorde avec les sémantiques d'échec fermé des spécifications 0002, 0003 et 0006 et de l'architecture 0024. Appliquer une règle commune au bootstrap, à la résolution de décisions, à l'assurance, à l'évaluation des changements et à leur application :
- une information obligatoire absente, inconnue, ambiguë, contradictoire, périmée, non prise en charge ou invérifiable n'accorde jamais de permission ;
- une preuve manquante ne satisfait jamais une exigence ;
- sortie d'agent, recommandation de source, succès CI ou permission de forge ne constituent pas une décision d'autorité ;
- les conditions non résolues bloquent les opérations dépendantes, pas les travaux indépendants dont l'indépendance est établie ;
- l'incertitude sur les dépendances ne permet pas de contourner le blocage.

Le rapport de blocage identifie condition, règle et décision source, périmètre et dépendances affectés, autorité compétente, lacune de preuve et voies licites.

Quatre mécanismes restent distincts :
1. **Dérogation :** exception bornée à une exigence dérogeable.
2. **Acceptation du risque :** acceptation autorisée d'un risque résiduel décrit ; elle ne transforme pas une preuve échouée en preuve réussie.
3. **Modification de politique :** changement prospectif par l'autorité compétente.
4. **Mesure compensatoire :** moyen alternatif dont l'adéquation est évaluée séparément.

Tout assouplissement est explicite, autorisé, motivé, circonscrit, limité dans le temps/soumis à revue, lié aux sources et révocable. Les échecs et preuves antérieurs restent dans l'historique. Aucun « ignorer », force-pass ou repli silencieux générique n'est acceptable.

## 5. Frontières à ne pas confondre

| Ambiguïté potentielle | Résolution nécessaire |
|---|---|
| Modèle canonique unique face à plusieurs standards métier | Une autorité GovCheck gouverne les décisions et engagements du dépôt ; les modèles métier spécialisés conservent leurs sémantiques et sont liés, non aplatis. |
| Package générique face à l'AGENTS.md utilisateur | Le package fournit contrats de projection, modèles et générateurs ; la gouvernance approuvée par l'utilisateur détermine le contenu. Aucune politique universelle canonique d'AGENTS.md utilisateur n'existe dans le package. |
| Autorité racine GovCheck face aux autorités QA/sécurité/release des utilisateurs | L'architecture 0023 ne concerne que GovCheck. Chaque utilisateur constitue sa propre autorité. |
| Fondations formelles face à la preuve formelle optionnelle | Chaque dépôt possède des sémantiques explicites d'affirmation, décision, provenance et incertitude ; aucun outil de preuve/model checker particulier n'est obligatoire pour chaque propriété. |
| Échec fermé face à l'adoption progressive | Les décisions inconnues restent inconnues et ne bloquent que les actions dépendantes ; la constitution par étapes évite d'exiger toutes les décisions dès le premier lancement. |
| Recommandation d'arbre face à l'autorité | Arbres et agents expliquent/recommandent ; seul un acteur autorisé ou une politique déterministe explicitement autorisée décide. |
| Catalogue central face aux sources des projets | Conserver le catalogue de conception de GovCheck et permettre des registres propres à chaque dépôt gouverné. |
| Bootstrap face aux évolutions ultérieures d'assurance | Le bootstrap établit les engagements initiaux ; les changements ultérieurs utilisent le même cycle de décision et les mêmes contrôles d'autorité. |

## 6. Impacts sur le package, le bootstrap et AGENTS.md

Le package ne doit pas livrer un AGENTS.md universel prétendant prescrire les choix de gouvernance de chaque utilisateur. Il doit fournir métamodèle et sémantiques de décision génériques ; mécanismes de qualification des sources et références initiales clairement distinguées des sources utilisateur ; modèles de décision versionnés et ressources d'aide par domaine ; descriptions des méthodes d'assurance et critères de sélection ; sémantiques d'échec fermé et d'assouplissement ; contrats de projection et règles de génération ; mécanismes déterministes de bootstrap et migration.

Le bootstrap doit inspecter la gouvernance existante (ou établir le contexte d'un dépôt vide), recueillir les décisions fondatrices minimales, identifier l'autorité compétente et ses pouvoirs initiaux, présenter les sources contextualisées, enregistrer décisions et incertitudes, dériver un plan déterministe limité aux capacités applicables, montrer les collisions avant application, générer AGENTS.md propre au dépôt et AGENTS.fr.md si choisi, préserver le contenu utilisateur et enregistrer les révisions du package/modèle/source/générateur.

À chaque changement ultérieur, le même moteur détermine si une nouvelle décision est nécessaire, qui en est responsable et quelle décision existante reste applicable. Ce n'est pas un sous-système de questionnaire indépendant.

Les AGENTS.md et AGENTS.fr.md racine de GovCheck restent les instructions méta destinées aux contributeurs de GovCheck ; ils ne sont pas copiés comme instructions des dépôts utilisateurs.

## 7. Cibles de formalisation

Avant l'implémentation, dériver et vérifier au minimum :
- résolution d'autorité unique ou résultat inconnu/conflit ;
- décision prise uniquement par une autorité valide pour catégorie, action, périmètre et période ;
- délégation ne dépassant ni pouvoirs ni validité du délégant ;
- absence d'autorisation implicite en cas d'inconnu/manque ;
- décisions obligatoires non résolues bloquant toutes et seulement les opérations dépendantes ;
- recommandation jamais confondue avec décision ;
- révisions et applicabilité des sources préservées dans les décisions ;
- chemin d'arbre déterministe et explicable pour des entrées figées ;
- choix de méthode lié à une affirmation/propriété et à l'autorité compétente ;
- substitution de méthode préservant les différences sémantiques et ses limites modifiées ;
- invalidation des preuves propagée aux affirmations/décisions dépendantes ;
- assouplissement typé, autorisé, borné et révocable ;
- modification de politique prospective sauf règle temporelle explicite valide ;
- projections fidèles à la gouvernance approuvée ;
- changement accepté et état appliqué identifiant le même candidat exact.

Ce sont des cibles, pas l'affirmation que les modèles TLA+ actuels les couvrent. Mettre en correspondance les modèles existants de cycle de vie, applicabilité, assurance, publication et journal ; consigner recouvrements, lacunes et frontières.

## 8. Audit du dépôt encore nécessaire

Inspecter, sans présumer :
1. tous les ADR et registres de décision/provenance, statuts, bases d'autorité et références ;
2. architectures 0006–0032 et leurs deux versions linguistiques ;
3. spécifications 0002–0006 et versions françaises ;
4. tous les modèles formels/TLA+, configurations, assertions, sorties TLC et limites ;
5. schémas, registres de versions, décisions, manifestes et métadonnées de publication ;
6. package govcheck, bootstrapper, modèles, capacités et tests ;
7. scripts racine, contrôles d'alignement package/intégrité des références et workflows générés ;
8. issues ouvertes, portefeuille de travaux gouverné et PR, doublons et dépendances inclus ;
9. catalogue central et backlinks ;
10. instructions agents racine/package et statut de projection.

Pour chaque artefact, consigner identité/chemin, statut, affirmations, sources, dépendances, version linguistique, correspondance avec l'intention, classe de compatibilité, lacune/conflit, action proposée, autorité nécessaire et preuve de vérification attendue.

## 9. Séquence recommandée

1. Terminer l'audit des artefacts et de la dérive bilingue.
2. Construire une matrice de traçabilité de chaque exigence de l'intention vers documents, sources, modèles, code, tests et travaux.
3. Réconcilier le métamodèle : catégories de décision, délégations, qualification des sources, aide à la décision, choix d'assurance, blocages circonscrits et assouplissements.
4. Mettre à jour architectures/spécifications dans l'ordre des dépendances, avec statuts explicites et backlinks.
5. Étendre modèles formels et tests ; consigner contre-exemples et propriétés non couvertes.
6. Définir les frontières schéma canonique/évaluateur et les choix technologiques uniquement s'ils sont justifiés.
7. Refondre bootstrap et génération des projections selon les contrats approuvés.
8. Décomposer l'implémentation en travaux atomiques gouvernés et PR révisables avec preuves CI.

Ne pas commencer par un grand questionnaire interactif ou une réécriture isolée des modèles AGENTS.md. Rendre d'abord cohérentes les sémantiques de décision et d'autorité.

## 10. Sources et limites

Sources internes principales : ADR 0001, 0003 et 0007 ; architectures 0012–0015, 0018 et 0021–0027 ; spécifications 0002–0006 ; document parent d'intention. Le statut propre de chaque source détermine la force avec laquelle elle étaye une conclusion.

Les références externes restent dans le catalogue unique docs/references.md : autorité/séparation des tâches (R-01–R-03), dossiers d'assurance/SACM (R-04, R-33–R-34, R-71, R-73), provenance des preuves (R-06–R-08), évaluation/vérification des politiques (R-09, R-10, R-88), PEAK (R-74), conventions d'instructions agents (R-104), sémantiques métier (R-94–R-103) et modalités normatives (R-93). Aucun catalogue concurrent n'est créé et une citation n'implique pas l'adoption comme dépendance.

Ce document est une base d'analyse d'impact. Il ne modifie aucune décision, n'adopte aucun contrat proposé, n'attribue pas d'autorité à une équipe QA au sein de GovCheck, ne sélectionne aucune technologie et ne prétend à aucune implémentation/vérification. L'autorité racine actuelle de GovCheck demeure celle de l'architecture 0023. Chaque utilisateur choisit sa propre structure d'autorité au moyen de décisions de bootstrap autorisées. Actualiser cet audit à mesure de l'inspection des artefacts. Tout changement normatif nécessite toujours la décision d'autorité et l'acte d'adoption applicables.

### 6.1 Implémentation du bootstrap observée (main actuel)

Le bootstrapper actuel possède déjà un parcours pour les dépôts existants ; il serait inexact de le décrire comme limité aux dépôts vides. La CLI expose inspect, plan, apply et rollback. Inspect/plan sont en lecture seule ; apply crée les fichiers manquants, préserve les collisions de contenu différent, est idempotent et enregistre un marqueur de package contenant version/digest, capacités sélectionnées et digests des fichiers installés ; rollback ne supprime que les fichiers inchangés enregistrés comme installés. Le mode historique à un argument est explicitement réservé aux cibles vides et refuse les cibles non vides.

Il s'agit toutefois encore d'un **mécanisme d'installation de fichiers et de sélection de capacités**, pas de la constitution progressive de gouvernance décrite dans l'intention. L'ensemble des capacités est actuellement une liste fixe (readme, check, decisions, docs, formal, scripts, workflows) ; en l'absence d'argument, elles sont toutes sélectionnées. Le bootstrap ne conduit pas encore de questionnaire contextuel, ne découvre/qualifie pas les sources propres au projet, n'établit pas l'autorité et les délégations du dépôt, n'enregistre pas les décisions différées/inconnues/non applicables, ne choisit pas les méthodes d'assurance par affirmation/propriété, ne génère pas un AGENTS.md utilisateur à partir des décisions approuvées et ne déclenche pas le réexamen des décisions lors des évolutions ultérieures. Le rapport inspect décrit aussi une présence élémentaire du système de fichiers/de Git et les collisions, pas un inventaire sémantique de l'intention, des exigences, risques, propriétés ou de la gouvernance existante.

**Classification d'impact :** préserver inspecter-planifier-appliquer/rollback et les protections contre les collisions comme infrastructure utile. Faire évoluer l'entrée du plan : d'une liste fixe de capacités sélectionnées manuellement vers une projection déterministe des décisions de gouvernance contextualisées et approuvées. Ne pas remplacer le comportement d'installation sûr par un questionnaire avant d'avoir spécifié le modèle de décision, les règles d'autorité et le contrat de migration. Le README du package et l'ADR 0003 décrivent actuellement la copie de govcheck/ telle quelle ; cela doit être réconcilié avec la constitution générée propre au dépôt et avec le caractère exclusivement méta des instructions racine de GovCheck.

## 11. Correspondance avec le portefeuille de travaux gouverné existant

L'intention doit être intégrée au portefeuille de travaux maintenu dans le dépôt ; les issues GitHub sont des adaptateurs de coordination/navigation et leur existence n'autorise pas en elle-même l'exécution. Les éléments ouverts suivants sont directement concernés et doivent être rapprochés de la matrice d'impact avant toute création de nouveaux travaux :

- [#78 — Gouvernance, autorité et décisions](https://github.com/Martin-PB/govcheck/issues/78), avec les enfants #41 (applicabilité des révisions), #60 (risque de séparation des tâches sous autorité unique), #67 (autorisation de la CI hébergée), #71 (évaluation future des autorités à seuil/quorum), #75 (adoption du portefeuille) et #86 (applicabilité temporelle de la gouvernance). L'intention élargit particulièrement le besoin de délégations par catégorie et de résolution d'autorité ; elle n'autorise pas en elle-même un régime multi-autorités pour GovCheck.
- [#79 — Évaluation et assurance](https://github.com/Martin-PB/govcheck/issues/79), comprenant #52 (causes d'unknown et politique de résolution), #68 (nature de vérifiabilité), #69 (argumentation des claims), #72 (corpus adversarial) et #43/#44 (implémentation verticale et attestations). C'est le domaine naturel du choix de méthode par affirmation/propriété et des sémantiques d'assurance non interchangeables.
- [#81 — Modèles formels et cycle de vie](https://github.com/Martin-PB/govcheck/issues/81), comprenant [#73](https://github.com/Martin-PB/govcheck/issues/73) (contrats intermodèles) et [#86](https://github.com/Martin-PB/govcheck/issues/86) (applicabilité temporelle de l'autorité). La délégation, la provenance des sources et les assouplissements circonscrits nécessitent une couverture explicite des modèles ou des exclusions déclarées.
- [#82 — Bootstrap, package et distribution](https://github.com/Martin-PB/govcheck/issues/82), comprenant [#62](https://github.com/Martin-PB/govcheck/issues/62) (inspect/plan/apply pour dépôts existants). Le bootstrap actuel possède déjà les mécanismes non destructifs décrits plus haut ; la lacune produit restante concerne la constitution guidée par les décisions, pas la simple prise en charge des dépôts existants.
- [#83 — Références et provenance](https://github.com/Martin-PB/govcheck/issues/83), comprenant [#74](https://github.com/Martin-PB/govcheck/issues/74) (statut machine-vérifiable et provenance des références). Étendre ce travail avec soin : le catalogue de conception de GovCheck et le registre contextualisé d'un utilisateur sont liés, mais distincts.
- [#84 — Collaboration multi-agents et attribution](https://github.com/Martin-PB/govcheck/issues/84) : pertinent pour la délibération assistée facultative et l'attribution, mais un agent reste non autoritaire sauf délégation explicite d'un pouvoir borné.
- [#85 — Schémas, fixtures et qualité documentaire](https://github.com/Martin-PB/govcheck/issues/85) : domaine approprié pour les contrats de schémas/fixtures et l'intégrité documentaire bilingue.

Cette analyse ne duplique pas ces éléments du portefeuille et ne modifie pas automatiquement leur périmètre. Il faut inspecter leurs enregistrements canoniques dans le dépôt, leur statut, leurs dépendances et leur autorisation avant toute modification. L'analyse d'impact doit alimenter leur traçabilité, pas créer un backlog parallèle.

## 12. Couverture des modèles formels observée dans le dépôt

L'inventaire formel montre que plusieurs comportements demandés possèdent déjà des modèles bornés distincts. La nouvelle intention doit conduire à étendre et composer ces modèles, pas à créer une machine à états monolithique de gouvernance.

| Modèle / document | Préoccupation déjà modélisée | Éléments explicitement non couverts par l'intention élargie |
|---|---|---|
| GovCheckAuthority.tla / Architecture 0023 | Autorité initiale unique, attribution des amendements, continuité autorité/révision, historique append-only. | Identité du principal abstraite ; pas de pouvoirs par catégorie, de délégations, de sémantique de prise d'effet, de cycle de vie des exceptions ni de constitution configurable par utilisateur. |
| GovCheckGovernanceApplicability.tla / Spécification 0006 / Architecture 0031 | Évaluation liée à la révision de gouvernance effective à une position d'événement ; publication ultérieure ; liaison historique des décisions ; rejet des évaluations périmées. | Changements/délégations d'autorité, consensus distribué, identité cryptographique, concurrence multi-écrivains complète et raffinement de l'implémentation. |
| GovCheckGovernanceControls.tla / Architecture 0033 | Évaluateur précédent faisant autorité pendant un remplacement ; distinction Pass/Fail/Unknown/Conflict ; dérogations bornées pour exigences dérogeables ; révocation et historique append-only. | Autorité complète par catégorie, justification issue des sources, arbres de décision contextualisés, choix de méthode par claim et application au niveau de l'implémentation. |
| GovCheckAssurance.tla / Architecture 0021 | Graphe fini acyclique de claims, fermeture d'argument conjonctive, dépendances/fraîcheur des preuves, révocation/expiration, revue indépendante et instantané d'acceptation. | Vérité externe, provenance cryptographique, décharge des hypothèses, stratégies d'argument alternatives, délibération sur le choix de méthode et raffinement de l'implémentation. |
| GovCheckLifecycle.tla / Spécification 0003 | Cycle de vie du changement et transitions gardées pour les identités exactes des candidats/gouvernance. | Le modèle ne résout pas à lui seul les délégations d'autorité ni le lien sémantique complet avec les modèles d'assurance et de publication ; voir issue #73. |
| GovCheckCanonicalPublication.tla / Architecture 0032 | Liaison entre évaluation, autorisation et publication ; exclusion des bases périmées ; publication append-only. | Organisation complète des autorités/délégations utilisateur, aide à la décision fondée sur les sources et garanties de production des adaptateurs/concurrence. |
| CICheckRouting.tla / Architecture 0029 | Routage CI par préoccupation et séparation des charges de vérification. | Ne décide pas en soi de la politique d'assurance du dépôt et n'autorise pas le choix des méthodes. |

Cette couverture s'appuie sur l'index des modèles formels et sur les limites qu'il déclare. Une réussite TLC est un élément d'évidence relatif à l'abstraction finie enregistrée. Elle n'établit ni l'application en production, ni l'adéquation sémantique d'une décision, ni le raffinement de l'implémentation, ni des propriétés hors modèle. Le contrat intermodèles de l'[issue #73](https://github.com/Martin-PB/govcheck/issues/73) et le travail sur l'autorité temporelle de l'[issue #86](https://github.com/Martin-PB/govcheck/issues/86) sont des points d'intégration particulièrement importants.
## 10. Comparaison académique et industrielle externe

Cette première comparaison éclaire le prochain travail sur le métamodèle. Elle n'adopte aucun cycle de vie, aucune notation ni aucun outil externe.

| Source | Contribution établie | Pertinence pour GovCheck | Limite |
|---|---|---|---|
| Anthropic, AI-native SDLC Playbook (2026), `intent.md` | Une intention lisible et versionnée conserve le problème d'origine, le résultat attendu, les utilisateurs/systèmes, les contraintes et questions ouvertes, puis alimente la spécification. | Précédent de nommage et conceptuel proche du document d'intention au niveau du dépôt. | Playbook industriel, pas standard universel de format. Anthropic utilise aussi des intentions pour des changements ; celle de GovCheck a une portée temporelle plus large. |
| ISO/IEC/IEEE 15288:2023 | Cadre de processus du cycle de vie, de la conception au retrait, appliqué de manière itérative et récursive. | Traite intention, exigences, décisions, réalisation et assurance comme préoccupations du cycle de vie, pas du seul bootstrap. | Ne prescrit ni modèle de cycle de vie, ni méthode, approche de modélisation ou nom de document. |
| ISO/IEC/IEEE 29148:2018 ; DIS édition 3 | Processus et éléments d'information d'ingénierie des exigences ; dérivation, allocation, validation, vérification et traçabilité bidirectionnelle. | Distingue besoins/attentes et exigences et soutient les liens de dérivation et d'allocation. | L'édition 2018 restait courante après la revue 2024 ; le DIS 2026 est un projet en enquête, pas une norme adoptée. |
| NASA Systems Engineering Handbook | Attentes des parties prenantes, ConOps, exigences, conception, vérification et validation sont réconciliés de façon itérative ; traçabilité bidirectionnelle entre niveaux. | Soutient cohérence et traçabilité ascendante/descendante entre attentes, exigences, conception et vérification. | Guide d'ingénierie des systèmes propre à un domaine, pas schéma universel de dépôt. |
| GORE : KAOS, iStar, GRL, Tropos | Les objectifs motivent les exigences ; modèles de raffinements ET/OU, opérationnalisation, acteurs, dépendances, objectifs qualité et compromis. | Relations plus riches entre intention/objectifs, acteurs, alternatives, contraintes et exigences. | La réflexion 2026 sur l'étude systématique rapporte des obstacles persistants à l'adoption industrielle et une évaluation empirique inégale ; aucune notation unique ne doit être imposée. |
| OMG SysML v2.0 | Modélisation normalisée des exigences, comportements, structures, analyses et vérifications, avec relations de modèle et API. | Vocabulaire candidat pour les relations typées dériver/satisfaire/vérifier/raffiner/allouer et l'échange de modèles. | Langage de modélisation des systèmes, pas métamodèle de gouvernance GovCheck ni format d'échange obligatoire. |
| OMG SACM 2.3 | Métamodèle normalisé d'assurance pour affirmations, argumentation, références d'artefacts, preuves, contexte et raisonnement. | Utile pour le sous-graphe d'assurance. | Ne définit pas le cycle complet intention-exigences-décisions-spécifications. |
| UK Government ADR Framework (2025) | Les registres consignent contexte, décision et conséquences au niveau d'autorité approprié. | Soutient des décisions d'architecture séparées, autorisées, motivées et assorties de conséquences. | Un ADR consigne un choix ; il ne prouve pas qu'il satisfait l'intention ou les exigences. |
| `INTENT.md` d'IntentDocs | Format ouvert publié regroupant présentation produit, personas, releases, stories et critères d'acceptation. | Point de comparaison utile pour une convention existante `INTENT.md`. | Son modèle regroupé n'est pas adopté, GovCheck séparant intention, exigences et éléments d'acceptation. |

### 10.1 Premiers constats sur les relations

Les sources ne justifient pas une chaîne linéaire unique. Elles soutiennent un graphe typé, plusieurs-à-plusieurs, versionné, avec des sémantiques relationnelles et événements de cycle de vie distincts. Le prochain modèle formel doit au minimum étudier :

- **Intention ↔ besoins/attentes des parties prenantes :** une intention peut synthétiser plusieurs besoins ; les attentes peuvent être contradictoires, incertaines ou non validées.
- **Intention / besoins → objectifs et résultats :** les objectifs raffinent la finalité en états recherchés ; les résultats nécessitent des indicateurs observables ou scénarios de validation sans métrique numérique universelle.
- **Objectifs → exigences :** les exigences peuvent dériver des objectifs, obligations externes, risques, normes ou contraintes de conception ; les exigences auto-dérivées doivent être identifiées.
- **Exigences ↔ décisions :** les décisions peuvent créer, sélectionner, contraindre, interpréter, différer, déroger ou modifier les exigences ; une exigence peut motiver plusieurs décisions concurrentes.
- **Décisions ↔ architecture/spécifications :** les décisions sélectionnent ou contraignent les alternatives de conception ; les spécifications décrivent comportements/propriétés requis ou visés. Une décision peut affecter plusieurs spécifications et inversement.
- **Exigences / spécifications / propriétés → vérification et validation :** la vérification contrôle les caractéristiques spécifiées ; la validation demande si le bon système et les résultats visés ont été obtenus.
- **Affirmations → arguments → éléments d'évidence/résultats :** les dossiers d'assurance structurent affirmations et raisonnements ; l'évidence n'étaye les affirmations que dans son périmètre, ses hypothèses, sa provenance et sa fraîcheur.
- **Implémentation / exploitation ↔ observations et déclencheurs de changement :** observations à l'exécution, incidents et changements de contexte peuvent contester les hypothèses, invalider l'évidence et déclencher le réexamen de l'intention, des objectifs, exigences ou décisions.

Il s'agit de familles de relations candidates issues de la recherche, pas d'un vocabulaire GovCheck adopté ni d'un modèle de cardinalité.

### 10.2 Lacunes de recherche avant l'adoption d'un modèle formel de relations

1. Distinguer finalité/intention, besoin, attente, objectif, résultat, exigence, contrainte, décision, justification, élément d'architecture, spécification, propriété, affirmation, argument, méthode, cas de vérification, élément d'évidence et acceptation.
2. Définir direction, cardinalité, composition, provenance, validité temporelle et autorité de chaque relation ; ne pas utiliser une arête générique `traces-to` pour toutes les significations.
3. Modéliser alternatives, conflits, contribution/satisfaction, raffinement, dérivation, allocation, réalisation, justification, approbation, vérification, validation, soutien par évidence, réfutation et invalidation.
4. Diagnostiquer liens manquants, affirmations non étayées, exigences orphelines, objectifs sans opérationnalisation, décisions sans artefacts affectés et preuves sans affirmations.
5. Préserver navigation inverse et analyse d'impact : de l'évidence vers l'affirmation/exigence/décision/objectif/intention qu'elle étaye, et d'une intention ou source modifiée vers les descendants potentiellement affectés.
6. Comparer GORE, ISO 29148/15288, SysML v2, SACM/GSN et pratiques industrielles ADR/SDLC avant de choisir les sémantiques GovCheck ou les mappings externes.

Cette analyse n'adopte à elle seule aucune relation, aucun champ obligatoire, aucune notation formelle ni aucun métamodèle externe.


## Reference catalogue links

- [R-01](./references.fr.md#r-01)
- [R-03](./references.fr.md#r-03)
- [R-04](./references.fr.md#r-04)
- [R-06](./references.fr.md#r-06)
- [R-08](./references.fr.md#r-08)
- [R-09](./references.fr.md#r-09)
- [R-10](./references.fr.md#r-10)
- [R-33](./references.fr.md#r-33)
- [R-34](./references.fr.md#r-34)
- [R-71](./references.fr.md#r-71)
- [R-73](./references.fr.md#r-73)
- [R-74](./references.fr.md#r-74)
- [R-88](./references.fr.md#r-88)
- [R-93](./references.fr.md#r-93)
- [R-94](./references.fr.md#r-94)
- [R-103](./references.fr.md#r-103)
- [R-104](./references.fr.md#r-104)
- [R-114](./references.fr.md#r-114)
- [R-115](./references.fr.md#r-115)
- [R-116](./references.fr.md#r-116)
- [R-117](./references.fr.md#r-117)
- [R-118](./references.fr.md#r-118)
- [R-119](./references.fr.md#r-119)
- [R-120](./references.fr.md#r-120)
- [R-121](./references.fr.md#r-121)
