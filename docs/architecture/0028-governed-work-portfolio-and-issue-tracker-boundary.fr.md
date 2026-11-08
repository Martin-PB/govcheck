# 0028 — Portefeuille de travaux gouverné et frontière avec les gestionnaires d'issues

**Statut :** proposition d'architecture soumise à revue ; ce document ne prétend pas qu'un registre de backlog, une configuration GitHub Projects, une automatisation de workflow ou un contrôle de conformité soit implémenté.  
**Langue :** l'anglais est la langue par défaut ; voir la [version anglaise](0028-governed-work-portfolio-and-issue-tracker-boundary.md).

## 1. Objectif

Définir comment GovCheck découvre, qualifie, conserve, priorise, autorise, exécute et clôt les travaux proposés sans confondre un enregistrement dans un gestionnaire d'issues avec une décision, une exigence, un engagement ou un résultat réalisé.

Cette architecture est indépendante des outils. GitHub Issues et Projects constituent le premier adaptateur opérationnel, et non le modèle canonique de gouvernance. Une autre forge, une interface locale ou un futur adaptateur doit préserver les mêmes sémantiques.

Le problème récurrent auquel répond cette architecture est la confusion entre la création d'une issue et l'acceptation de sa proposition, entre l'attribution d'une priorité et l'autorisation du travail, ou entre la clôture d'une issue et la preuve du résultat attendu.

## 2. Décision d'architecture

Adopter un **portefeuille de travaux gouverné en trois étapes** :

1. **Intake (entrée) :** un signal ou sujet est enregistré pour qualification. Il n'est pas encore admis dans le backlog conservé.
2. **Backlog candidat :** le sujet a été examiné et explicitement conservé comme candidat à un travail futur. Cette conservation n'autorise pas son exécution.
3. **Travail engagé :** un élément délimité a été autorisé et suffisamment spécifié pour entrer dans un plan d'exécution.

Il s'agit d'états de gouvernance, pas de trois bases de données ou dépôts obligatoires. Ils peuvent être présentés sous forme de vues d'un même gestionnaire d'issues, à condition que l'état et l'historique de ses transitions soient explicites et auditables.

Une issue GitHub peut servir :
- d'enregistrement d'entrée ;
- de dossier de coordination d'un candidat ;
- de dossier de coordination d'un travail engagé ;
- de conteneur parent reliant des travaux indépendamment traçables.

L'issue n'est pas la représentation canonique d'une décision, d'une exigence, d'une affirmation d'assurance, d'un élément de preuve, d'un résultat d'implémentation ou d'un événement d'acceptation. Ceux-ci restent des artefacts typés du projet, liés par des identités et révisions stables.

## 3. Concepts et frontières

| Concept | Signification | Représentation canonique |
|---|---|---|
| Signal | Observation, demande, idée, signalement de défaut, question ou recommandation externe | Observation source ou enregistrement d'entrée |
| Sujet de travail | Sujet nécessitant une qualification ou une action éventuelle | Entrée du portefeuille gouverné |
| Élément de travail | Résultat délimité à produire et vérifier | Enregistrement de travail ; une issue peut le coordonner |
| Décision | Choix, rejet, report ou contrainte autorisés | Décision / ADR avec autorité et périmètre |
| Exigence | Condition normative ou contractuelle | Spécification ou règle de gouvernance versionnée |
| Plan | Proposition ordonnée et dépendante pour réaliser le travail | Plan versionné ou dossier d'exécution |
| Preuve | Information admissible pour une affirmation et un périmètre donnés | Enregistrement de preuve ou référence d'artefact immuable |
| Résultat | Modification produite ou résultat vérifié | Commit, PR, release, rapport ou autre artefact versionné |
| Acceptation | Détermination autorisée au regard d'un candidat exact et de la gouvernance applicable | Événement d'acceptation lié aux identités exactes |

Une issue peut pointer vers chacun de ces objets ; elle ne doit pas les fusionner dans un corps de texte ou un fil de commentaires. Les commentaires constituent l'historique des discussions, pas des décisions faisant autorité, sauf si une règle explicite de gouvernance définit un événement de décision typé et attribuable.

Une issue parente est un conteneur organisationnel. Elle ne devient pas automatiquement une epic dont les enfants hériteraient de la priorité, de l'autorité ou de l'acceptation. Les travaux enfants conservent leur propre périmètre, critères, état et traçabilité.

## 4. Cycle de vie du portefeuille

### 4.1 Entrée (intake)

Tout contributeur peut soumettre un signal, sous réserve de la politique du dépôt. L'entrée doit préserver :
- l'origine, le déclarant/producteur et la date de création ;
- le fait observé ou demandé, séparé clairement de son interprétation ;
- les liens sources et éléments de preuve fournis, avec provenance et limites ;
- le projet/domaine concerné lorsqu'il est connu ;
- les liens vers les doublons ou sujets similaires ;
- l'incertitude et les informations manquantes.

L'entrée est volontairement permissive. Un signalement incomplet ou non vérifié peut être enregistré sans être présenté comme un défaut, un risque, une exigence ou un engagement confirmé.

### 4.2 Qualification

Une décision de triage classe le sujet au minimum dans l'une des catégories suivantes :
- conserver pour recherche ou investigation ;
- conserver comme candidat de travail ;
- scinder en sujets livrables indépendamment ;
- fusionner/lier comme doublon ou sujet connexe ;
- différer dans l'attente de preuves ou d'une décision ;
- rejeter comme hors périmètre, invalide ou sans intérêt suffisant ;
- clôturer car déjà couvert, remplacé ou devenu sans objet.

La résolution, sa justification, l'autorité lorsqu'elle est requise et les liens vers les enregistrements résultants doivent être conservés. Le rejet n'est pas une suppression ; un nouveau signal peut rouvrir la question avec de nouveaux éléments.

### 4.3 Backlog candidat

Un candidat est conservé pour une éventuelle exécution future. Il doit préciser, de manière proportionnée :
- le résultat visé et son bénéficiaire/problème ;
- le périmètre et les exclusions explicites ;
- la compréhension actuelle, les hypothèses et les questions ouvertes ;
- la nature du travail et les domaines concernés ;
- les livrables attendus et les conditions observables d'achèvement ;
- les dépendances, contraintes et risques connus ;
- les décisions, exigences, documents d'architecture et preuves pertinents ;
- pourquoi il reste candidat et les éléments qui conduiraient à le réexaminer.

Un candidat peut rester volontairement insuffisamment spécifié lorsque la recherche ou une décision constitue précisément le travail. Il ne doit pas être présenté artificiellement comme prêt à être implémenté.

### 4.4 Engagement et exécution

Un candidat ne devient un travail engagé qu'au moyen d'une autorisation explicite de l'autorité compétente, conformément au régime de gouvernance du projet. L'engagement requiert une unité d'exécution délimitée avec :
- un résultat et un périmètre définis ;
- des critères d'acceptation/achèvement ;
- les exigences et décisions applicables résolues, ou explicitement listées comme prérequis ;
- des dépendances et un séquencement suffisamment compris ;
- une approche de vérification/preuve proportionnée à l'impact ;
- les acteurs responsables, rôles de revue/approbation et contraintes ;
- une fenêtre d'exécution ou un contexte de planification si le projet en utilise un.

L'engagement est distinct de l'assignation d'une issue, de son ajout à un Project, de l'attribution d'une priorité, d'un milestone ou du déplacement vers une colonne « In progress ». Les opérations de l'outil ne représentent un engagement que si une transition de gouvernance définie et attribuable les autorise.

Une modification du périmètre, des exigences, des dépendances, de l'identité du candidat ou de l'autorité de gouvernance peut invalider l'engagement ou renvoyer le sujet en qualification. L'historique est conservé ; l'invalidation n'efface pas l'autorisation antérieure.

## 5. Décomposition et relations entre travaux

Scinder un sujet lorsqu'il contient des résultats livrables indépendamment, des décisions distinctes, des autorités différentes, des vérifications sensiblement différentes ou des travaux pouvant être acceptés séparément. Conserver un seul élément lorsque ses parties ne peuvent pas être livrées ou acceptées de manière pertinente indépendamment.

Modéliser explicitement les relations, avec une direction lorsque leur sémantique l'exige :
- `derived-from` / `reported-by` ;
- `refines` / `decomposes-into` ;
- `depends-on` / `blocks` ;
- `related-to` / `duplicates` ;
- `implements` / `satisfies` ;
- `changes` / `supersedes` ;
- `verified-by` / `evidenced-by` ;
- `authorized-by` / `accepted-by`.

Une relation doit identifier la révision ou l'événement pertinent lorsque sa cible mutable rend un simple lien ambigu. Les cycles de dépendances doivent être détectés ; les cycles dans de simples relations « related-to » ne sont pas intrinsèquement erronés. Une relation parent-enfant n'implique aucune dépendance, sauf indication explicite.

Le portefeuille doit assurer une traçabilité bidirectionnelle :
- de l'objectif, de la décision, de l'exigence ou du constat vers le candidat, le travail engagé, la modification et la vérification ;
- de chaque élément de travail et résultat livré vers sa justification, son autorité, son périmètre et la gouvernance applicable.

## 6. Classification, étape et priorité

Les dimensions de classification répondent à des questions différentes et ne doivent pas être confondues.

### 6.1 Nature du travail

Utiliser une nature principale par élément de travail actif :
- décision ;
- audit ;
- recherche ;
- spécification ;
- implémentation ;
- vérification ;
- intégration ;
- maintenance.

La documentation est normalement un livrable d'une de ces natures, pas une nature universelle. N'introduire une classe « documentation » distincte que si le projet démontre un workflow documentaire gouverné indépendamment.

### 6.2 Domaine

Utiliser zéro ou plusieurs domaines lorsque cela facilite réellement la navigation (par exemple gouvernance, assurance, autorité, évaluation, bootstrap, méthodes formelles, distribution, références, intégrations ou opérations). Éviter un label par document d'architecture, outil ou standard externe.

### 6.3 Étape

L'étape représente la maturité du portefeuille ou l'état d'exécution, pas l'acceptation normative :
- needs-triage ;
- needs-evidence ;
- needs-decision ;
- needs-specification ;
- ready ;
- in-progress ;
- blocked ;
- validation.

Une transition d'étape doit être étayée par le dossier de travail. « Done » est représenté par la clôture et une résolution enregistrée, pas par un label d'étape permanent. L'acceptation d'une décision constitue un événement distinct.

### 6.4 Priorité

La priorité exprime l'urgence/la valeur relative dans un contexte de planification déclaré. Elle ne représente ni l'effort, ni la confiance, ni la maturité, ni la seule gravité, ni l'autorisation. Si la priorité ne peut pas être justifiée, la laisser non attribuée dans l'attente du triage plutôt que d'inventer P2.

Utiliser une petite échelle ordonnée (P0–P3) uniquement avec des critères publiés et une revue périodique. P0 est réservé aux menaces immédiates sur l'intégrité de la gouvernance, la sûreté/sécurité ou un jalon critique ; P1 à un prérequis ou blocage matériel ; P2 au travail planifié ordinaire ; P3 à une amélioration différable. Les changements de priorité exigent une justification et préservent l'historique.

### 6.5 Facettes risque et décision

Les labels de risque signalent une attention transverse importante (par exemple sécurité, changement incompatible, gouvernance, perte de données, dépendance externe) ; ils ne remplacent pas un enregistrement ou une évaluation du risque.

Les facettes de décision (normative, architecture, technologie, politique, périmètre) ne s'appliquent que lorsqu'une véritable décision est attendue. Une recherche susceptible d'éclairer une décision future n'est pas automatiquement un travail de décision.

## 7. Adaptateur GitHub Issues et Projects

GitHub est le premier adaptateur. Utiliser :
- **Issues** pour l'entrée et la coordination des travaux, les discussions, références et décompositions ;
- **Projects** pour les vues du portefeuille, le regroupement, le tri, la planification et les champs structurés ;
- **labels** pour les dimensions de classification stables et réutilisables ;
- **milestones/itérations** uniquement pour des fenêtres de planification ou regroupements de livrables explicites ;
- **PR, commits et releases** pour les identités de modifications/résultats, reliées aux éléments de travail.

Préférer les champs structurés de Projects pour l'étape du portefeuille, la priorité, la fenêtre cible, la responsabilité et l'engagement lorsqu'ils sont disponibles. Les labels conviennent mieux à la classification multidimensionnelle et au filtrage qu'à l'encodage de chaque fait de workflow mutable. Les préfixes de labels GitHub sont des conventions, pas des types mutuellement exclusifs imposés ; toute règle « une valeur par famille » doit être contrôlée par le processus ou l'automatisation.

L'adaptateur ne doit pas déduire :
- le statut de candidat de la seule ouverture d'une issue ;
- l'engagement d'une priorité, d'un assigné, d'un milestone ou de l'appartenance à un Project ;
- l'approbation d'une revue de PR sans autorité de gouvernance et lien au candidat exact ;
- l'achèvement ou l'assurance de la clôture d'une issue ;
- la vérité normative de commentaires, labels ou colonnes de tableau.

L'adaptateur doit préserver les liens stables et, si possible, les identifiants natifs ainsi que l'identité du dépôt. La portabilité exige un mapping d'export/import qui ne perde ni identité, ni direction des relations, ni historique des décisions, ni provenance, ni justification des transitions d'état.

## 8. Clôture, remplacement et historique

Un élément peut être clôturé avec une résolution typée :
- livré et vérifié selon les critères énoncés ;
- décision prise (avec lien vers l'enregistrement de décision) ;
- rejeté/hors périmètre ;
- doublon (avec lien vers l'élément canonique) ;
- remplacé (avec lien vers le successeur) ;
- devenu sans objet ;
- retiré par son auteur/autorité.

« Livré » exige des liens vers les résultats réels et les preuves de vérification adaptées à l'affirmation. Cela ne signifie pas automatiquement que la modification a été acceptée, publiée ou déployée : ce sont des événements distincts du cycle de vie.

La réouverture qualifie de nouveau des circonstances modifiées ou de nouvelles preuves ; elle ne réécrit pas l'ancienne résolution. Les éléments remplacés restent adressables. La conservation et la confidentialité suivent la politique du dépôt ; ne pas conserver de contenu sensible dans des issues publiques lorsqu'un stockage de preuves contrôlé est requis.

## 9. Invariants de gouvernance

Les exigences d'architecture suivantes sont proposées pour une spécification et des contrôles de conformité ultérieurs :

1. **La création n'est pas l'acceptation :** une entrée ne crée aucune obligation d'exécution.
2. **La priorité n'est pas l'autorité :** priorité et planification n'autorisent aucune action normative ou opérationnelle.
3. **Ouvert ne signifie pas backlog :** l'état ouvert d'une issue n'établit pas sa conservation comme candidat.
4. **Candidat ne signifie pas engagement :** un travail conservé n'est pas une exécution autorisée.
5. **L'engagement est explicite :** l'autorisation identifie acteur/autorité, périmètre, date et révision de gouvernance.
6. **L'inconnu reste visible :** périmètre, justification, autorité, dépendances ou critères manquants restent inconnus/bloquants, jamais implicitement satisfaits.
7. **La décision est un artefact typé :** une décision importante ne se déduit pas d'une discussion ou d'une fusion.
8. **La traçabilité est bidirectionnelle :** travaux et résultats pointent vers leur justification ; celle-ci pointe vers les travaux et preuves.
9. **La clôture n'est pas une preuve :** la résolution et les preuves du résultat sont distinctes.
10. **L'historique est préservé par ajout :** changements d'état/priorité, décisions, invalidations et résolutions restent attribuables.
11. **La décomposition est sémantique :** la parenté n'implique ni dépendance, ni autorité partagée, ni acceptation héritée.
12. **Neutralité de l'adaptateur :** les champs et comportements propres à une forge ne deviennent pas des sémantiques canoniques.

## 10. Politique opérationnelle et cadence de revue

Au triage, identifier le sujet, sa provenance, la nature du travail, le domaine, la prochaine information/décision nécessaire et la disposition provisoire. Ne pas imposer de priorité avant de disposer d'un contexte suffisant.

Lors du raffinement du backlog, réexaminer la valeur du candidat, sa justification, les doublons, sa décomposition, ses dépendances, les hypothèses périmées, les décisions préalables et la pertinence de le conserver. Un candidat sans résultat plausible ni déclencheur de réexamen doit être clôturé ou reformulé.

Avant engagement, vérifier les conditions de préparation de la §4.4. Pendant l'exécution, contrôler les dérives de périmètre, les changements de dépendances, les blocages et la fraîcheur des preuves. À la clôture, enregistrer une résolution typée et relier les résultats.

La cadence est définie par le projet ; cette architecture n'impose ni Scrum, ni sprints, ni story points, ni vélocité, ni estimations, ni méthode de planification particulière. Les petits projets peuvent utiliser une revue manuelle légère. L'automatisation ne doit faire respecter que des invariants déterministes et ne doit pas fabriquer des jugements sémantiques.

## 11. Application aux discussions actuelles de GovCheck

Les issues d'analyse récentes illustrent la nécessité de séparer l'entrée de l'engagement :

- **Issue #23 — « Analyse Claude » :** entrée/candidat analytique concernant des lacunes conceptuelles et des pistes de recherche. Ses recommandations ne sont pas toutes des exigences acceptées. Ne conserver que les sujets délimités après rapprochement avec les spécifications 0005/0015 et les architectures 0022–0027 ; éviter de maintenir une issue parapluie permanente à la place de travaux traçables.
- **Issue #26 — « perplexity » :** entrée analytique proposant une séquence d'exécution plus concrète. Sa liste de backlog n'est pas un plan autorisé. La question P0 de la révision de gouvernance de base exige une décision explicite et une spécification avant tout engagement d'implémentation dépendant.

Les discussions et commentaires restent des matériaux sources. Cette architecture ne transforme pas rétroactivement leurs recommandations en politique approuvée et ne prétend pas que les labels, champs Projects ou automatisations ont été configurés.

## 12. Séquence d'adoption et d'implémentation

1. Examiner et autoriser cette architecture ; rapprocher sa terminologie des spécifications 0002–0005 et architectures 0013–0015, 0022–0027.
2. Définir les enregistrements minimaux de travail et de transition dans le modèle canonique de gouvernance ; décider quels champs sont normatifs et lesquels relèvent des métadonnées d'adaptateur.
3. Configurer les champs et vues GitHub Projects comme adaptateur ; créer des labels uniquement pour les dimensions de classification stables.
4. Qualifier un échantillon représentatif d'issues ouvertes, dont #23 et #26, sans supposer que toutes les issues ouvertes appartiennent au backlog conservé.
5. Ajouter des contrôles déterministes sur la classification obligatoire, les combinaisons d'étapes invalides, les liens manquants et les preuves de transition seulement après spécification de leurs sémantiques.
6. Tester l'export/import et un second adaptateur ou jeu de données neutre pour démontrer que le modèle n'est pas façonné par GitHub.
7. Ajouter des modèles formels ou tests de mutation uniquement pour les propriétés de transition et de concurrence identifiées comme importantes ; ne pas prétendre que cette architecture est elle-même formellement vérifiée.

## 13. Hors périmètre et limites

Ce document ne choisit pas une méthode de gestion de produit, n'impose pas Scrum, ne prescrit pas d'estimation, ne crée pas de nouvelle base de données, n'exige pas de base graphe, ne rend pas GitHub normatif, ne définit pas un schéma complet de gestion de projet, n'autorise aucune issue actuelle et ne prétend pas qu'un moteur de backlog est implémenté. Il ne remplace ni le cycle de vie des changements, ni le cadre de décision, ni le modèle d'assurance, ni les politiques d'identité/versionnement des artefacts.
