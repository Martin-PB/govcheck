# STUDY-004 — Spécifications multi-métiers, pluralité des points de vue et délibération formelle

**Statut :** recherche et orientation de conception à instruire. Ce dossier ne constitue ni une décision d'architecture, ni une exigence adoptée, ni une autorisation d'implémentation.

## 1. Origine et intention

Ce dossier conserve fidèlement l'orientation formulée dans la conversation du 11 novembre 2026 : un dépôt gouverné par GovCheck doit pouvoir recevoir des spécifications provenant de sources, disciplines et métiers différents, en préserver le sens et la provenance, puis fournir un moyen formel et calculable de mettre ces spécifications en relation — y compris lorsque leurs concepts, définitions, périmètres ou affirmations divergent ou se contredisent.

Le but n'est pas d'imposer une convergence sémantique ni de fabriquer prématurément un vocabulaire commun. Il s'agit de donner aux métiers une matière structurée, traçable et analysable pour discuter, comprendre les conséquences des divergences et permettre à l'autorité compétente de prendre une décision informée. Une fois la décision prise, ses conséquences autorisées peuvent être traduites en exigences, spécifications cibles, décisions de conception et travaux de réalisation, avec une filiation explicite vers les sources et l'arbitrage.

Exemple déclencheur : « prospect », « client », « opportunité », « compte » ou « tiers » peuvent désigner des réalités partiellement recouvrantes ou différentes selon le marketing, les ventes, la gestion contractuelle et la comptabilité. Inversement, un même objet ou acteur peut être nommé différemment selon le métier. Ces écarts ne sont pas nécessairement des erreurs : ils peuvent refléter des finalités, des découpages, des temporalités, des responsabilités ou des périmètres distincts.

## 2. Orientation centrale à étudier

> GovCheck doit permettre d'ingérer, préserver, structurer, mettre en relation et confronter des spécifications hétérogènes, afin de fournir une matière formelle, traçable et calculable à la délibération des parties prenantes et à la décision de l'autorité compétente. Les décisions adoptées doivent ensuite pouvoir être transformées en exigences, spécifications et travaux de réalisation, tout en conservant leur filiation avec les sources et les arbitrages dont elles résultent.

Cette orientation est une proposition de capacité à étudier, pas une décision déjà adoptée.

## 3. Cycle fonctionnel envisagé

### 3.1 Ingestion de sources diverses

Sources potentielles : documents métier, exigences réglementaires et normatives, contrats, conventions, modèles de données, ontologies, processus, spécifications fonctionnelles et techniques, documents d'outils externes et contributions de parties prenantes.

L'ingestion doit distinguer et préserver :
- la source originale, son identité, sa provenance, son auteur/émetteur, son autorité et sa version ;
- le contenu extrait ou importé ;
- la représentation structurée construite dans GovCheck ;
- les transformations, normalisations et interprétations appliquées ;
- les informations perdues, ambiguës, non comprises ou non représentées ;
- les liens entre chaque élément structuré et son emplacement dans la source.

Principe de précaution : aucune ingestion ne doit faire disparaître silencieusement une information ni faire passer une interprétation automatique pour une validation métier. La conservation du document source et la traçabilité des transformations sont des sujets à examiner, y compris pour les formats non textuels et les mises à jour de sources.

### 3.2 Préservation du contexte et du point de vue

Une spécification peut devoir déclarer, selon sa nature :
- métier, discipline, communauté ou fonction concernée ;
- auteur, producteur, sponsor et autorité d'approbation ;
- finalité, préoccupations et décisions qu'elle vise à soutenir ;
- périmètre, population, objets, processus et contexte temporel ;
- vocabulaire, définitions, conventions et unités ;
- hypothèses, contraintes, exclusions et limites de validité ;
- statut, version, date d'effet et relations avec les versions précédentes.

Ces dimensions sont des questions de recherche, pas une liste obligatoire de métadonnées pour chaque document. Le modèle doit éviter de réduire un point de vue à l'identité de son auteur : il peut être collectif, institutionnel, disciplinaire, situé ou contesté.

### 3.3 Structuration sans fusion

L'outillage devrait permettre de représenter les éléments significatifs des spécifications sans exiger qu'ils soient tous convertis immédiatement dans un modèle canonique unique. Il faut pouvoir conserver les formulations et concepts sources, puis leur associer des représentations structurées et des interprétations explicites.

Une même réalité peut être découpée différemment selon les métiers. Il ne s'agit donc pas toujours de synonymes à aligner : les objets, événements, rôles, états, frontières et critères d'identité peuvent différer.

### 3.4 Mise en relation et analyse

Relations candidates à examiner, sans les adopter comme vocabulaire normatif :
- identité ou équivalence déclarée, dans un contexte explicite ;
- correspondance exacte ou partielle ;
- proximité, recouvrement ou intersection ;
- spécialisation et généralisation ;
- traduction ou projection d'un concept vers un autre vocabulaire ;
- dépendance, présupposition ou dérivation ;
- complémentarité ;
- différence de périmètre, de temporalité ou de finalité ;
- incompatibilité, contradiction ou conflit ;
- absence de correspondance connue, ambiguïté ou relation non déterminée.

Les traductions métier ne doivent pas être de simples tables de synonymes. Une traduction peut être partielle, asymétrique, conditionnelle et contextuelle. Elle devrait pouvoir préciser le concept source et le concept cible, le contexte de validité, les éléments conservés, les pertes ou raffinements, les hypothèses, les règles de transformation, la provenance et l'autorité ayant validé cette traduction.

Il faut distinguer au minimum :
- même terme, significations différentes ;
- termes différents, réalité ou concept partiellement commun ;
- concepts qui se recouvrent sans être équivalents ;
- différences de découpage du domaine ;
- contradiction logique sous des hypothèses et périmètres identiques ;
- divergence apparente due à des contextes, temporalités ou finalités différents.

### 3.5 Matière formelle et calculable pour la délibération

Les relations et divergences devraient pouvoir alimenter, selon les besoins, des graphes de concepts et de dépendances, matrices de correspondance, analyses de couverture, ensembles d'affirmations incompatibles, hypothèses, conséquences, lacunes et questions non résolues.

Les traitements automatisés pourraient détecter des candidats à la correspondance, des incohérences, des dépendances ou des conflits. Ils doivent exposer les règles, hypothèses, versions, limites et éléments justificatifs de leurs résultats.

Distinction impérative : un conflit calculé n'est pas encore un conflit métier qualifié ; une contradiction détectée sous une interprétation ne démontre pas que les sources sont globalement incompatibles ; une absence de conflit détecté ne prouve pas la cohérence complète. Le calcul prépare et éclaire la discussion, il ne remplace pas le jugement des métiers.

### 3.6 Délibération, autorité et décision

Les parties prenantes doivent pouvoir examiner les spécifications sources, les correspondances, les divergences, les arguments, les conséquences et les incertitudes. Les désaccords ne doivent pas être effacés automatiquement ni traités tous comme des anomalies.

Une décision devrait préserver :
- l'autorité compétente, son mandat et le périmètre de compétence ;
- les parties prenantes consultées et les positions exprimées ;
- les sources, versions, éléments et analyses considérés ;
- les interprétations et hypothèses retenues ;
- les options, conséquences et compromis examinés ;
- les options rejetées et leurs motifs ;
- les risques acceptés, conditions et limites ;
- les désaccords ou questions restant ouverts ;
- le caractère conditionnel, temporaire, révisable ou définitif de la décision.

La décision ne réécrit pas rétroactivement les documents sources et ne déclare pas nécessairement qu'un métier avait tort. Elle établit ce qui est autorisé ou retenu dans un contexte de gouvernance donné.

### 3.7 Dérivation vers la réalisation et assurance

Une décision adoptée peut conduire à des exigences, spécifications cibles, règles métier, contrats d'interface, modèles, décisions d'architecture et travaux de réalisation. Ces artefacts ne sont pas nécessairement produits en une seule étape et ne sont pas identiques à la décision.

La filiation doit rester consultable : artefact dérivé → décision → arbitrage et arguments → analyses et relations → spécifications sources et versions. Les vérifications et éléments d'assurance doivent préciser quelles interprétations, exigences, périmètres et hypothèses ils couvrent. Un test concluant pour une interprétation de « client » ne démontre pas automatiquement une autre interprétation.

## 4. Deux espaces liés, à ne pas confondre

L'orientation suggère de distinguer analytiquement :

1. **Espace de pluralité et de confrontation** : sources originales, spécifications importées, points de vue, vocabulaires, interprétations, alignements, divergences, contradictions, analyses et délibérations.
2. **Espace de gouvernance et de réalisation** : autorités, décisions adoptées, exigences et spécifications dérivées, travaux, implémentations et assurances.

Ils doivent être fortement reliés, mais ne doivent pas être fusionnés. Une source ingérée n'est pas automatiquement adoptée ; une correspondance calculée n'est pas automatiquement validée ; un conflit détecté n'est pas automatiquement une non-conformité ; une décision n'est pas une preuve de bonne réalisation.

Cette séparation est une hypothèse d'architecture à examiner, pas une structure déjà décidée.

## 5. Principes de prudence et limites

- Ne pas imposer une ontologie universelle ni une convergence sémantique par défaut.
- Ne pas confondre terme, concept, objet du domaine, représentation et identifiant.
- Ne pas assimiler traduction, correspondance, équivalence et identité.
- Ne pas confondre incohérence logique, désaccord métier, différence de périmètre et conflit de gouvernance.
- Ne pas laisser un algorithme décider de la légitimité d'un point de vue ou de l'autorité d'un arbitrage.
- Ne pas transformer une spécification importée en exigence approuvée.
- Ne pas perdre les formulations sources, leur provenance, leur version ou les transformations appliquées.
- Ne pas prétendre qu'un modèle formel exhauste le domaine réel.
- Ne pas faire de GovCheck un outil universel de modélisation ontologique ou de facilitation métier : il pourrait gouverner les sources, relations, traductions, décisions et assurances, en s'appuyant au besoin sur des outils spécialisés.

## 6. Questions de recherche

1. Quels formats et mécanismes d'ingestion permettent une conservation fidèle, une extraction structurée et une traçabilité des transformations ?
2. Quelles structures existantes représentent correctement point de vue, préoccupation, contexte, spécification, vocabulaire et autorité ?
3. Comment représenter plusieurs modèles de domaine et découpages sémantiques sans les réduire à un modèle canonique ?
4. Quels formalismes expriment les alignements exacts, partiels, contextuels, asymétriques et contestables ?
5. Comment distinguer formellement équivalence, implication, compatibilité, contradiction, chevauchement et absence de correspondance ?
6. Comment détecter les contradictions sans produire de faux positifs dus aux différences de contexte, de temps, de modalité ou de périmètre ?
7. Comment associer chaque résultat calculé à ses règles, hypothèses, versions, preuves et limites ?
8. Comment gouverner la validation et l'évolution des traductions métier ?
9. Comment organiser une délibération multi-acteurs, conserver les désaccords et rattacher les décisions à l'autorité compétente ?
10. Comment dériver des décisions des artefacts de réalisation sans perdre la filiation avec les sources et arbitrages ?
11. Comment relier ce dispositif au métamodèle existant, aux exigences, intentions, objectifs, décisions, modèles, arguments, affirmations et assurances ?
12. Quelles capacités relèvent de GovCheck, de formats d'échange, d'outils spécialisés ou de processus organisationnels externes ?
13. Quelles conditions d'applicabilité, prérequis et limites GovCheck devrait-il expliquer aux organisations qui ont plusieurs métiers ou spécifications hétérogènes ?

## 7. Familles de travaux à examiner

Le dossier doit comparer au minimum :
- Domain-Driven Design, bounded contexts, context mapping et traductions entre modèles ;
- architecture viewpoints/views et description des préoccupations des parties prenantes ;
- registres de métadonnées et sémantique des données (dont ISO/IEC 11179) ;
- alignement d'ontologies, SKOS, OWL et limites de ces formalismes ;
- modèles conceptuels pluriels et délibération (dont Soft Systems Methodology) ;
- exigences multi-parties prenantes, goal-oriented requirements et gestion des conflits ;
- SACM et argumentation structurée pour relier affirmations, arguments, éléments et décisions ;
- formats de spécification et standards sectoriels, y compris les mécanismes de provenance, versionnement et évolution.

Les références R-187 à R-192 sont des points de départ bibliographiques à vérifier et approfondir ; leur inscription ne vaut ni adoption ni preuve qu'elles répondent à tous les besoins.

## 8. Relations avec les autres recherches

- **STUDY-003** fournit le contexte épistémologique : pluralité des points de vue, limites des modèles, irréductibilité et validité située. STUDY-004 transforme ces questions en hypothèse de capacité d'ingestion, de mise en relation et de délibération.
- **STUDY-001** éclaire qualité, tests, TDD et assurance du développement.
- **STUDY-002** éclaire applicabilité, frontières d'enforcement et prérequis externes.
- Les recherches existantes sur ontologies, interopérabilité sémantique, cohérence du métamodèle et SACM sont à réexaminer ; STUDY-004 ne doit pas dupliquer leurs résultats mais identifier ce qui manque pour le cycle complet décrit ici.

## 9. Statut et discipline décisionnelle

- Cette étude enregistre une orientation importante exprimée par l'utilisateur ; elle n'est pas une décision formelle d'adoption.
- Aucun nouveau concept du métamodèle, format canonique, langage, moteur de raisonnement ou outil d'alignement n'est adopté.
- Aucun travail d'implémentation n'est créé par ce dossier.
- Toute décision ultérieure devra citer STUDY-004 et les entrées R exactes, expliciter les options et contre-arguments, les limites d'applicabilité, l'autorité compétente et les conséquences sur le modèle existant.
- Le critère de réussite central de la recherche est de permettre une confrontation formelle et calculable sans imposer une convergence sémantique artificielle, puis de préserver la filiation entre sources, délibération, décision, réalisation et assurance.

## Références

Catalogue central : [R-187](../references.fr.md#r-187) · [R-188](../references.fr.md#r-188) · [R-189](../references.fr.md#r-189) · [R-190](../references.fr.md#r-190) · [R-191](../references.fr.md#r-191) · [R-192](../references.fr.md#r-192). Voir également les références R-51–R-61, R-83–R-86, R-115–R-127 et R-178–R-182.
