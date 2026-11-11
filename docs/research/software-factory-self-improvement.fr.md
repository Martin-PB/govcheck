# How to Build a Software Factory That Improves Itself — analyse de la conférence

**Statut :** analyse de source non normative. Ce document analyse la conférence fournie et les sources complémentaires ; il n'adopte ni produit, ni architecture, ni workflow, ni concept de métamodèle, ni exigence.
**Préparé le :** 2026-11-11.

## Source et méthode

Zach Lloyd (Warp), [« How to Build a Software Factory That Improves Itself »](https://youtu.be/nKjPBAw_N_0), conférence présentée à AI Engineer ; cataloguée en [R-162](../references.fr.md#r-162).

L'analyse s'appuie sur la présentation et sa transcription horodatée, puis confronte ses affirmations à la [documentation officielle de Warp Factories](https://docs.warp.dev/factories/) ([R-163]), à l'étude randomisée de METR sur des développeurs open source expérimentés ([R-164]) et au profil NIST de gestion des risques liés à l'IA générative ([R-165]). Les références existantes au SSDF, aux protections de branches GitHub, à l'isolation des agents et à DORA sont mobilisées lorsqu'elles apportent un contexte pertinent ([R-02](../references.fr.md#r-02), [R-03](../references.fr.md#r-03), [R-79](../references.fr.md#r-79), [R-148](../references.fr.md#r-148)).

Il s'agit d'une analyse critique ciblée, non d'une évaluation indépendante de Warp ni d'une revue systématique de littérature. L'intervenant est le fondateur d'un fournisseur qui présente son propre produit. La documentation produit établit la conception et les affirmations du fournisseur, pas les propriétés opérationnelles de manière indépendante.

## 8. Analyse détaillée de la conférence

### 8.1 Reconstruction de l'argument présenté

La conférence n'est pas simplement une démonstration commerciale d'agents distants. Elle défend une proposition cohérente de modèle opérationnel :

1. **Passer du prompting interactif au développement automatisé (01:12–03:08).** Dans le modèle actuel décrit par Lloyd, chaque ingénieur exécute individuellement des agents sur son ordinateur. L'ingénieur devient un goulot d'étranglement ; les configurations sont fragmentées, les dépenses difficiles à maîtriser et un agent compromis peut hériter de privilèges locaux comparables à ceux de l'utilisateur connecté.
2. **Traiter la factory comme une boucle de travail à l'échelle de l'entreprise (03:08–04:03).** Les humains soumettent le travail ; les agents peuvent assurer le triage, collaborer à la spécification, implémenter et effectuer une vérification par interaction avec l'interface utilisateur. L'organisation définit la répartition du travail entre humains et agents, puis mesure et améliore ce modèle opérationnel.
3. **Traiter la factory comme une infrastructure, pas comme un coéquipier IA (04:03–05:15).** Elle devrait être ouverte à différents modèles et harnesses, adaptable à l'infrastructure existante et précisément définie dans du code versionné. Cette définition comprend les workflows, les skills, les MCP, les lieux d'exécution et les configurations associées.
4. **Préserver la maîtrise des données, du calcul et de l'inférence (05:15–06:55).** Lloyd présente la souveraineté IA comme une préoccupation des grandes entreprises : maîtriser les entrées et sorties, envisager sa propre infrastructure et son propre calcul, et conserver le choix du fournisseur d'inférence. Il distingue aussi les ingénieurs produit, qui livrent de la valeur client via la factory, des ingénieurs de la factory, qui améliorent les skills, le contexte, le choix des modèles et la factory elle-même.
5. **Rendre les exécutions observables (07:51–11:57).** La démonstration présente des vues sur l'automatisation, le cycle time et les dépenses, ainsi que l'accès aux exécutions individuelles et à leurs artefacts. La définition de la factory est adossée à un dépôt contenant définitions d'agents, automatisations, benchmarks, lieux d'exécution, skills et webhooks. L'objectif est de rendre le processus opérationnel inspectable et modifiable comme du code.
6. **Évaluer les exécutions et réinjecter les échecs dans le système (12:01–14:42).** Des évaluateurs fondés sur des LLM examinent les exécutions selon des critères, notamment un exemple de détection de tests redondants. Les motifs d'échec agrégés peuvent conduire à des propositions de modification de la configuration ou des skills, soumises sous forme de pull request. L'exemple mentionne un motif observé 37 fois et une proposition demandant aux agents de lire davantage de skills positifs avant l'implémentation.
7. **Construire des benchmarks sur les tâches de l'organisation (14:42–17:15).** Plutôt que de s'appuyer uniquement sur des benchmarks publics, les équipes devraient constituer un corpus représentatif de tâches historiques et les rejouer avec différentes configurations de modèles. Les résultats de coût et de qualité peuvent guider le routage des modèles pour le code et la stack réels de l'équipe.
8. **Maintenir une discipline de vérification et d'économie (17:15–fin).** Dans les questions-réponses, Lloyd recommande le développement piloté par spécification et la vérification par interaction avec l'interface pour absorber le volume de PR et réduire la charge de revue. Pour le budget, il suggère de mesurer le coût par PR et la part consacrée à l'évaluation et aux benchmarks, puis d'extrapoler. Il estime que cela devient particulièrement utile autour de dix ingénieurs ou davantage ; c'est une heuristique pratique, pas un seuil universel.

### 8.2 Les apports réellement intéressants de la proposition

- **La factory est elle-même un système à gouverner.** Prompts, rôles d'agents, permissions d'outils, skills, workflows, évaluateurs, tâches de benchmark et lieux de déploiement ne sont pas de simples détails de configuration : ils influencent les propriétés du logiciel produit et méritent identité, historique de révision, revue et preuves.
- **La boucle opérationnelle est explicite.** Exécution → trace/artefacts → évaluation → analyse des échecs → proposition de modification du workflow → revue/tests → nouvelle exécution. C'est un cycle de vie intéressant à modéliser, y compris lorsque la boucle elle-même est défectueuse.
- **Les preuves issues des tâches locales comptent.** Les classements de benchmarks publics ne démontrent pas la performance attendue sur un dépôt, un langage, une architecture, un profil de risque ou un processus de revue particuliers. Un corpus local, versionné et soigneusement sélectionné peut répondre à une question plus circonscrite et plus utile, à condition d'en exposer les limites.
- **Le coût doit être rapporté aux résultats.** Le coût par PR est plus informatif que la seule dépense en tokens, mais uniquement si son dénominateur et son périmètre sont définis : PR acceptées ou rejetées, retries, temps humain de spécification et de revue, exécutions échouées, reprises, vérification, incidents et maintenance peuvent modifier l'interprétation.
- **Les responsabilités humaines et agentiques doivent être conçues.** La distinction entre ingénierie produit et ingénierie de la factory rend visible la maintenance du système de production comme un travail à part entière, avec responsables, compétences et obligations d'assurance.
- **La souveraineté recouvre des choix concrets.** Maîtrise des données, localisation du calcul, fournisseur d'inférence, rétention, sous-traitants et possibilité de sortie peuvent être spécifiés et évalués séparément, au lieu d'être résumés par l'étiquette vague « auto-hébergé ».

### 8.3 Hypothèses et limites que la conférence ne démontre pas

La présentation est une proposition industrielle faite par le fondateur d'un fournisseur qui y démontre son propre produit. C'est une source primaire utile pour comprendre sa philosophie de conception et un exemple concret d'implémentation, mais pas une évaluation indépendante du produit ou de l'approche générale.

En particulier, la conférence ne démontre pas :

- que déplacer les exécutions dans une factory cloud est nécessairement plus sûr qu'un worker local ou auto-hébergé correctement isolé ;
- que les garanties du fournisseur concernant sandbox, secrets, isolation entre clients, journalisation ou suppression sont effectives parce que la configuration de la factory les déclare ;
- que l'enregistrement exhaustif des exécutions est compatible avec la confidentialité, le moindre privilège, la minimisation des données, les obligations légales de rétention et la protection des identifiants et données clients ;
- qu'un juge LLM distingue de manière fiable un bon travail d'ingénierie d'un mauvais, ni que ses erreurs sont indépendantes de celles du générateur ;
- que le score choisi mesure réellement la propriété recherchée. L'exemple des tests redondants est une heuristique : supprimer des tests peut améliorer ce score tout en diminuant l'assurance ;
- qu'un benchmark historique est représentatif, exempt de contamination, résistant au surapprentissage ou stable lorsque le dépôt et la distribution des tâches évoluent ;
- que le rejeu d'interactions enregistrées avec des modèles et outils mesure à tous égards le comportement d'un fournisseur vivant et changeant ;
- qu'une modification proposée à la factory améliore effectivement la production, plutôt que le benchmark ou le score de l'évaluateur ;
- que cycle time, taux d'automatisation, coût par PR et correction peuvent être optimisés indépendamment sans déplacer le travail ou le risque vers les reviewers, opérateurs ou utilisateurs.

Une boucle d'auto-amélioration n'est donc pas automatiquement une boucle d'amélioration de la qualité. Elle peut amplifier une métrique défectueuse, un biais d'évaluation, une fuite du benchmark ou un diagnostic erroné. Chaque transition de la boucle nécessite provenance et contrôle approprié, idéalement indépendant.

### 8.4 Conséquences pour GovCheck — reprendre les questions, pas l'architecture produit

La conférence devrait inciter GovCheck à traiter le **système de production comme un objet d'assurance à part entière**, mais elle ne signifie pas que GovCheck doit devenir une factory cloud ou exploiter lui-même des agents.

Cette distinction est particulièrement importante parce que GovCheck vise un bootstrap agnostique des forges, orienté dépôt et reposant sur un petit exécutable local. Un dépôt peut décrire et valider son propre contrat de gouvernance ainsi que les artefacts qu'une factory doit fournir. Sans intégration et autorité de confiance, il ne peut pas garantir le comportement à l'exécution d'une factory externe. Un schéma propre à Warp, un agencement MCP, une exécution cloud ou un score fournisseur ne doivent pas devenir une exigence générique de GovCheck.

Les questions utiles à intégrer à l'audit du dépôt sont :

- **Identité de la factory :** une exécution peut-elle être reliée à une révision immuable des workflows, rôles d'agents, skills, permissions d'outils, définitions d'évaluateurs et corpus de benchmark ?
- **Identité d'exécution :** les preuves identifient-elles le harness effectif, le modèle/fournisseur/version, l'image du runner, le profil d'isolation, les permissions d'outils, la configuration pertinente et le lieu d'exécution ? Lesquels sont simplement déclarés par le runner, lesquels sont attestés indépendamment ?
- **Traçabilité du cycle de vie :** l'exécution peut-elle être reliée à l'intention/requête initiale, au triage, à la spécification, à la révision d'implémentation, aux tests, à la revue, à la vérification et à la décision de release, sans confondre activité d'agent et autorisation ?
- **Validité de l'évaluation :** les critères de notation sont-ils explicites, versionnés et liés à des affirmations ou exigences ? Les juges sont-ils calibrés, échantillonnés, confrontés à des preuves indépendantes et empêchés de devenir silencieusement l'unique oracle ?
- **Gouvernance des benchmarks :** qui choisit les tâches, résultats attendus et niveaux de difficulté ? Comment les tâches sensibles sont-elles protégées ? Les ajouts/retraits et versions du corpus sont-ils revus ? Comment évalue-t-on fuite, représentativité et surapprentissage ?
- **Gouvernance de l'amélioration :** une proposition d'auto-amélioration emprunte-t-elle le même chemin de contrôle des changements, revue, tests et assurance que toute autre modification sensible à la gouvernance ? Le système peut-il modifier son propre évaluateur ou son benchmark sans autorisation indépendante ?
- **Affirmations économiques et de qualité :** les dénominateurs, exclusions, incertitudes, imputations de coûts, efforts de revue, reprises et résultats en aval sont-ils enregistrés afin qu'un tableau de bord ne transforme pas une télémétrie partielle en affirmation injustifiée de productivité ?
- **Autorité humaine :** les personnes qui spécifient, relisent, approuvent, acceptent les risques et exploitent la factory sont-elles distinguables dans les preuves ? Un point de contrôle humain enregistré correspond-il à une permission effectivement imposée ?
- **Sortie et portabilité :** l'organisation peut-elle exporter ses définitions, preuves d'exécution et données de benchmark, remplacer modèle/harness/fournisseur et continuer à interpréter les preuves anciennes après migration ?

Ce sont des questions candidates pour l'audit, pas un nouveau schéma obligatoire de factory. Il faut d'abord les relier aux concepts GovCheck et aux issues ouvertes.

### 8.5 Distinction essentielle : gouverner une factory et imposer ses garanties

Un dépôt peut imposer qu'une définition de factory soit versionnée, valide au regard d'un schéma, revue et associée à une exécution. Il peut vérifier une attestation signée ou interroger une API de forge/fournisseur. Il peut refuser une affirmation de release si une preuve requise est absente ou périmée, lorsque la politique adoptée le prévoit.

Il ne peut pas déduire de la présence d'un fichier YAML que le service distant l'a exécuté fidèlement. Il ne peut pas rendre un reviewer compétent, garantir l'efficacité de l'isolation d'un fournisseur ou prouver qu'un benchmark est représentatif en vérifiant simplement la présence de fichiers de benchmark. Il s'agit de preuves externes, de préconditions organisationnelles ou de risques résiduels.

La factory peut aussi être un dépôt gouverné distinct. GovCheck peut alors amorcer et gouverner ce dépôt avec le même modèle général ; il ne doit pas supposer silencieusement que le dépôt du produit a autorité sur le dépôt d'infrastructure de la factory, le compte cloud ou l'organisation.

### 8.6 Chaîne de preuves suggérée pour une amélioration de factory

Une chaîne de traçabilité candidate, à confronter au métamodèle existant plutôt qu'à ajouter immédiatement comme nouveau schéma, est :

`FactoryRevision → Run → TraceAndArtifacts → EvaluationResult → FailureFinding → ImprovementProposal → ReviewedChange → VerifiedFactoryRevision`

Chaque lien nécessite identité stable et provenance. Le résultat d'évaluation doit préciser son critère et son évaluateur ; la proposition d'amélioration doit identifier les constats qui l'étayent ; le changement revu doit identifier la décision humaine/de l'autorité ; et la vérification ultérieure doit utiliser un corpus de tâches et un environnement identifiés. Un benchmark réussi est une preuve concernant les cas testés, pas une preuve d'amélioration générale.

### 8.7 Appréciation générale

L'apport le plus fort de la conférence est le déplacement de l'unité d'analyse : de l'agent de codage individuel vers le système gouverné qui configure, exécute, observe, évalue et améliore le travail agentique. GovCheck devrait prendre ce déplacement au sérieux lorsqu'il audite le cycle de vie des dépôts et l'exhaustivité de l'assurance.

La partie la plus fragile est la confiance implicite selon laquelle l'exécution cloud centralisée, la notation par LLM et l'auto-amélioration produiraient un développement plus sûr ou plus productif. Ce sont des hypothèses à tester, pas des garanties. La contribution de GovCheck doit être de rendre explicites les affirmations, preuves, autorités, frontières et risques résiduels — sans imposer une factory cloud, un fournisseur, un modèle, un harness ou une structure organisationnelle.

## Positionnement dans la recherche

Cette conférence constitue une entrée du programme plus large de recherche sur l'ingénierie logicielle assistée par IA et l'applicabilité de GovCheck. Ses observations doivent être confrontées aux autres conférences fournies, aux études académiques et aux normes avant toute recommandation transversale sur le produit. L'évaluation d'applicabilité est conservée séparément dans [Applicabilité de GovCheck et frontières externes](govcheck-applicability-and-boundaries.fr.md).

## Traçabilité

Nouvelles références : [R-162](../references.fr.md#r-162), [R-163](../references.fr.md#r-163), [R-164](../references.fr.md#r-164), [R-165](../references.fr.md#r-165). Références de contexte : [R-02](../references.fr.md#r-02), [R-03](../references.fr.md#r-03), [R-79](../references.fr.md#r-79), [R-148](../references.fr.md#r-148). Aucune source de ce document n'est adoptée comme exigence GovCheck.
