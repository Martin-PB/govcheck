# Analyse d'impact de l'intention produit — constitution et cycle de vie de la gouvernance

**Statut :** audit de conception de travail destiné à la revue des mainteneurs ; ce document n'est ni un ADR, ni un acte d'adoption, ni un contrat d'implémentation.  
**Document parent :** [Intention produit GovCheck](product-intent.fr.md). **English:** [Product-intent impact analysis](product-intent-impact-analysis.md).

## 1. Constat exécutif

L'intention produit élargie ne nécessite pas d'abandonner les fondations existantes. Les architectures 0013–0015 et 0021–0027, ainsi que les spécifications 0002–0006, anticipent déjà une grande partie des concepts et comportements requis : gouvernance canonique, bootstrap progressif, méthodes d'assurance sélectionnables, autorité et délégation circonscrites, traçabilité des sources, sémantiques métier, évaluation en échec fermé, exceptions bornées et conformité des changements.

La lacune principale est leur intégration. Ces éléments restent dispersés dans des documents de statuts et de maturités différents. Ils ne constituent pas encore un modèle produit intégré, adopté et exécutable. La prochaine phase doit réconcilier sémantiques, autorités et dépendances du cycle de vie avant d'implémenter un nouveau questionnaire ou de réécrire le bootstrapper.

GovCheck doit être compris comme un **système de constitution de gouvernance, d'aide à la décision, d'assurance et de conformité du cycle de vie**. Le bootstrap en est le premier processus guidé de constitution, pas un questionnaire plat exécuté une seule fois. Les décisions sont catégorisées par domaine, confiées à des autorités compétentes, éclairées par des sources contextualisées et réexaminées lorsque des changements pertinents invalident leur fondement.

## 2. Discipline de statut

Cette analyse distingue :
- **Décision consignée :** décision explicite avec sa base d'autorité (notamment l'architecture 0023 pour l'autorité racine actuelle de GovCheck et l'ADR 0004 pour la gouvernance des versions).
- **Conception proposée :** contenu d'architecture/spécification en attente de l'acte d'adoption applicable.
- **Capacité implémentée ou vérifiée :** uniquement ce que démontrent les artefacts et éléments d'exécution du dépôt. Un document de conception ou un rapport de model checking ne démontre pas une capacité opérationnelle.
- **Constat d'impact :** compatibilité, lacune, ambiguïté ou précision nécessaire identifiée par comparaison avec l'intention produit.

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

Sources internes principales : ADR 0001, 0003 et 0007 ; architectures 0012–0015, 0018 et 0021–0027 ; spécifications 0002–0006 ; document parent d'intention produit. Le statut propre de chaque source détermine la force avec laquelle elle étaye une conclusion.

Les références externes restent dans le catalogue unique docs/references.md : autorité/séparation des tâches (R-01–R-03), dossiers d'assurance/SACM (R-04, R-33–R-34, R-71, R-73), provenance des preuves (R-06–R-08), évaluation/vérification des politiques (R-09, R-10, R-88), PEAK (R-74), conventions d'instructions agents (R-104), sémantiques métier (R-94–R-103) et modalités normatives (R-93). Aucun catalogue concurrent n'est créé et une citation n'implique pas l'adoption comme dépendance.

Ce document est une base d'analyse d'impact. Il ne modifie aucune décision, n'adopte aucun contrat proposé, n'attribue pas d'autorité à une équipe QA au sein de GovCheck, ne sélectionne aucune technologie et ne prétend à aucune implémentation/vérification. L'autorité racine actuelle de GovCheck demeure celle de l'architecture 0023. Chaque utilisateur choisit sa propre structure d'autorité au moyen de décisions de bootstrap autorisées. Actualiser cet audit à mesure de l'inspection des artefacts. Tout changement normatif nécessite toujours la décision d'autorité et l'acte d'adoption applicables.
