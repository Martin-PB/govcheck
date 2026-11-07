# 0009 — Mémoire de conception GovCheck et registre consolidé des décisions

**Statut :** mémoire de conception consolidée ; elle consigne les décisions et propositions discutées les 5 et 6 novembre 2026. Elle ne transforme pas chaque proposition en fonctionnalité implémentée ou en règle déjà approuvée.  
**Langue :** l’anglais est la langue par défaut ; la version anglaise est [ici](0009-govcheck-design-discussion-record.md).  
**Références :** ADR 0001 ; spécifications 0002 à 0005 ; architectures 0006 à 0008 ; modèle formel `govcheck.lifecycle`.

## 1. Objet, provenance et règles de lecture

Ce document rassemble la discussion de conception de GovCheck dans une mémoire durable du dépôt. Il conserve le raisonnement, les décisions, les contraintes, les questions non résolues et les suites à donner qui seraient autrement dispersés entre les messages et les descriptions de pull requests. Il s’agit d’une synthèse, pas d’une transcription verbatim. Lorsqu’une décision ultérieure remplace une piste antérieure, la décision actuelle est indiquée ; l’alternative précédente n’est conservée que lorsqu’elle explique l’évolution de la conception.

Le statut épistémique est explicite :

- **Décision** : frontière produit ou choix architectural tranché pendant la discussion.
- **Contrat proposé** : objectif de conception documenté pour revue, et non garantie implémentée.
- **Artefact actuel** : fichier ou modèle présent dans le dépôt.
- **Vérification observée** : contrôle réellement exécuté, avec son périmètre déclaré.
- **Question ouverte** : aucune décision n’a été prise ; une implémentation ne doit pas choisir silencieusement à la place du projet.

L’historique Git et les PR restent la référence pour les changements de sources. Ce document explique leur raison d’être et leur cohérence ; il ne remplace pas les spécifications et ne modifie pas silencieusement leur sémantique normative.

## 2. Définition du produit et frontières

GovCheck est un système de gouvernance logicielle centré sur le dépôt : il gouverne un dépôt logiciel et le cycle de vie des changements qui lui sont proposés. Les développeurs et les agents de programmation sont des contributeurs soumis à la gouvernance du dépôt ; GovCheck n’est pas d’abord un système de gouvernance des agents eux-mêmes.

GovCheck n’est pas :
- un bac à sable pour agents ni une passerelle d’appels d’outils ;
- un plan de contrôle hébergé ou un SaaS obligatoire ;
- un serveur MCP obligatoire, un démon résident ou un service réseau ;
- un remplacement des systèmes de build, tests, scanners, CI ou outils VCS des projets ;
- un agrégat de scanners dont les résultats constitueraient à eux seuls la gouvernance.

L’interface principale visée est un petit exécutable local, utilisable par des personnes, scripts, tâches CI et agents capables d’appeler des commandes locales. Il doit produire des résultats exploitables par machine. Le fonctionnement exclusivement local est un mode de déploiement complet et de première classe. L’application d’une politique partagée ou distante est une capacité d’intégration facultative, pas une condition préalable du cœur.

Aucun modèle à trois niveaux fondé sur la taille du dépôt ne doit être introduit. Les fondations formelles de gouvernance et d’assurance s’appliquent à tous les dépôts. Les profils et politiques propres à chaque projet peuvent faire varier les obligations, preuves et commandes d’exécution applicables ; ils ne suppriment pas les fondations sémantiques communes.

## 3. Autorité normative et documentation

Le système visé possède une seule autorité normative : un modèle canonique de gouvernance, versionné et lisible par machine, interprété par GovCheck. Les fichiers Markdown tels que `AGENTS.md`, `GOVERNANCE.md`, `SECURITY.md` et `CONTRIBUTING.md` sont des projections contrôlées ou des documents explicatifs. Ils ne doivent pas devenir des sources concurrentes de règles normatives.

Le modèle canonique doit pouvoir exprimer :
- l’identité du paquet et sa version sémantique ;
- des identifiants de règles stables et immuables ;
- des règles typées et leur force normative explicite ;
- des périmètres d’applicabilité et des paramètres typés ;
- des relations explicites : dépendance, raffinement, remplacement et incompatibilité ;
- des profils de dépôt et des exceptions bornées ;
- des métadonnées de projection pour les documents humains générés ou contrôlés.

Les types de règles doivent distinguer au minimum obligations, interdictions, permissions, invariants/contraintes, exigences de preuve, exigences de processus/approbation et recommandations. Une recommandation est explicitement non normative. L’absence d’interdiction ne vaut pas permission. La précédence est une relation partielle explicite, jamais l’ordre des fichiers ou une règle « le dernier gagne ».

Un identifiant de règle n’est jamais recyclé. Toute évolution sémantique exige revue et traçabilité ; les règles retirées restent adressables via des tombstones ou des relations de remplacement. Contradictions, précédences ambiguës, périmètres mal formés, sémantiques non prises en charge et références non résolues sont des erreurs de gouvernance. Une indétermination obligatoire bloque l’acceptation.

L’anglais est la langue de présentation par défaut. Les versions françaises doivent préserver le sens normatif et le statut. Une divergence de traduction est une non-conformité documentaire, pas une seconde source de politique.

## 4. Séparer VCS, hébergement, collaboration et acceptation

Quatre dimensions doivent rester indépendantes :

1. **Contrôle de version :** Git, Pijul et d’éventuels futurs VCS.
2. **Hébergement :** local, hébergement d’équipe, auto-hébergement ou hébergement public.
3. **Collaboration :** travail individuel ou partagé, revue, échange de patches et demandes d’intégration.
4. **Acceptation/application :** décision de gouvernance et opération appliquant un candidat accepté.

Le cœur de gouvernance ne doit dépendre d’aucune forge. Les adaptateurs d’hébergement et de collaboration pourront viser GitHub, GitLab, Forgejo, Gitea, Nest ou de futurs systèmes, y compris des déploiements locaux et opérés par une équipe. Une forge peut transporter des revues et appliquer une barrière d’intégration uniquement dans la limite de ses capacités déclarées.

Une branche Git, un commit, un worktree, une pull request, un patch Pijul, un canal ou une demande Nest ne sont pas le changement GovCheck lui-même. Ce sont des objets natifs exposés par des adaptateurs. Une PR/MR est un objet de collaboration, pas le dossier de changement ni l’autorité d’acceptation.

### 4.1 Git

L’identité Git doit tenir compte d’autre chose que HEAD lorsque le candidat inclut du contenu indexé, modifié ou non suivi. Les descripteurs doivent distinguer l’identité commit/tree des instantanés index/worktree et prendre en compte les sous-modules. Un commit ne doit pas être présenté comme le candidat complet si l’arbre de travail diffère.

### 4.2 Pijul

Pijul est de première classe et sémantiquement distinct ; ce n’est pas un mode de compatibilité Git. Il faut préserver les identités et dépendances des patches, l’identité et l’état des canaux, la sémantique du graphe et les conflits natifs. Ne pas aplatir Pijul en commits/branches synthétiques et ne pas déduire ses conflits natifs d’un outil de fusion textuelle sans rapport. Si un adaptateur ne peut établir une propriété requise, il doit signaler « non pris en charge » ou « indéterminé », jamais un succès.

### 4.3 Application locale et partagée

Les hooks et wrappers locaux peuvent être contournés par un utilisateur ayant accès au système de fichiers ou des privilèges administrateur. Un exécutable local ne peut empêcher universellement les modifications directes, le remplacement de l’exécutable ou le contournement des hooks. L’acceptation locale doit néanmoins appliquer le même prédicat et déclarer ses limites d’application.

Une application forte et partagée exige une autorité d’équipe de confiance ou une intégration de forge vérifiant, à la frontière d’intégration, une décision liée au candidat exact du dépôt et à la révision de gouvernance. L’absence de capacité de blocage ou le contournement par un administrateur doit être visible, jamais transformé silencieusement en succès.

## 5. Cycle de vie canonique d’un changement

Un changement est une proposition identifiée de faire passer un dépôt d’un état de base exact à un état candidat exact. Son identité lie au minimum :

`(dépôt, base, candidat, révision/sémantique de gouvernance, révision de spécification, identifiant du changement)`

Le cycle de vie abstrait est :

`Proposed → Prepared → Evaluated → Reviewable → Accepted → Applied`

Les états supplémentaires incluent `Stale`, `Rejected`, `Withdrawn` et `Superseded`. Les implémentations peuvent ajouter des sous-états sans remettre en cause ces distinctions.

Séparations fondamentales :
- l’évaluation n’est pas l’approbation ;
- la preuve n’est pas l’approbation ;
- l’approbation n’est pas l’acceptation ;
- l’acceptation n’est pas l’application ;
- un résultat de modèle n’est pas une conformité de l’implémentation ;
- l’accusé d’application d’un adaptateur doit identifier le candidat exact appliqué.

Chaque transition est un événement auditable explicite comprenant acteur, date, motif, provenance et références avant/après. Aucune transition n’est déduite d’un nom de branche, d’un label de PR, d’un statut CI, d’un commentaire, d’une réaction ou d’un message de chat. L’autorité d’approbation vient de la gouvernance et d’une identité vérifiable, pas des conventions d’une forge.

### 5.1 Fraîcheur des preuves et acceptation

Une preuve est liée au sujet exact et à ses dépendances pertinentes : empreintes de base/candidat, révisions de gouvernance et de spécification, versions de l’évaluateur/des outils, configuration, hypothèses, environnement et faits externes. Si une dépendance déclarée change, les preuves et approbations concernées deviennent obsolètes pour le nouveau tuple. Les preuves historiques restent dans l’audit ; elles ne sont ni effacées ni réutilisées silencieusement.

L’acceptation est dérivée, pas un indicateur modifiable. Elle exige :
- les identités exactes du dépôt, de la base, du candidat, de la gouvernance et de la spécification ;
- l’évaluation de toutes les obligations obligatoires applicables ;
- aucune défaillance bloquante, contradiction ou indétermination/non-prise en charge ;
- des preuves valides liées au tuple courant et à ses dépendances ;
- des approbations authentiques d’acteurs autorisés, en nombre et rôles requis ;
- des exceptions valides, limitées, dans leur périmètre et non expirées ;
- un adaptateur capable d’identifier le candidat et de vérifier son application exacte.

`Accepted` est une décision concernant un candidat exact. `Applied` est une opération VCS/collaboration ultérieure. L’adaptateur doit revérifier les préconditions et confirmer que le candidat exact accepté a été appliqué. Une mutation concurrente ou une course TOCTOU doit échouer de manière sûre.

## 6. Vocabulaire d’assurance : bannir le « vérifié » générique

GovCheck doit indiquer précisément ce qu’une méthode établit, pour quel sujet et périmètre, et sous quelles hypothèses. Les classes suivantes ne sont pas interchangeables :

| Classe | Ce qu’elle peut établir | Ce qu’elle n’établit pas à elle seule |
|---|---|---|
| Exécution empirique (tests, builds, linters, scans) | Résultat observé pour les entrées et l’environnement exécutés | Correction générale, validité du modèle ou preuve |
| Model checking | Propriétés d’un modèle formel dans ses bornes, sa configuration et ses hypothèses | Conformité de l’implémentation au modèle |
| Preuve par théorème | Dérivation acceptée par une logique/un noyau donné, relativement aux axiomes et imports | Pertinence de l’exigence ou du modèle choisi, ni implémentation du code |
| Conformité de l’implémentation | Relation justifiée entre comportement implémenté et spécification/modèle | Approbation normative de la spécification |
| Fidélité normative | Traçabilité des règles approuvées vers propriétés formelles, tests et projections documentaires | Vérité des preuves externes ou correction de toute implémentation |
| Acceptation | Décision de gouvernance pour un candidat exact selon un prédicat défini | Vérité universelle de toutes les affirmations ou absence de tout défaut |

Les tests sont des **témoignages** : ils attestent qu’une exécution donnée a produit un résultat observé. Le model checking valide un modèle dans les hypothèses et limites explorées. Une preuve par théorème est valide relativement à sa logique, son noyau, ses axiomes et ses imports. La conformité entre modèle et implémentation exige sa propre relation de raffinement explicite et ses propres preuves. Ces distinctions doivent être conservées dans les noms, schémas, rapports et interfaces.

Les enregistrements de preuve doivent lier les identifiants de revendication/règle, l’identité du sujet, les empreintes exactes du dépôt et de son état, les révisions gouvernance/spécification/modèle, la méthode et le périmètre, l’outil/sa version/la configuration/l’invocation, l’environnement et les hypothèses, le résultat brut ou sa référence protégée, le résultat/la date/le producteur/la provenance, les limites et les dépendances d’invalidation. Un simple code retour ne prouve que le résultat de cette invocation.

Pour TLA+/TLC, consigner la révision du modèle, la configuration/les constantes, les réductions, l’équité, les bornes, la version de l’outil, les nombres d’états/transitions, le statut d’achèvement et les contre-exemples. Une exécution bornée ne doit pas être qualifiée d’exhaustive. Pour la preuve par théorème, consigner la logique, la version du noyau/vérificateur, les axiomes, théorèmes importés, obligations admises et fonctionnalités non sûres ou oracles. Pour la conformité, identifier les révisions de l’implémentation et de la spécification, la frontière d’abstraction et la relation de raffinement.

## 7. Modèle de menace et frontières de confiance

La conception prend en compte les contributeurs et agents malveillants ou compromis, le contenu de dépôt malveillant, les dépendances/outils de build compromis, les identités falsifiées ou révoquées, les forges/serveurs d’équipe compromis, les faits externes obsolètes, les parseurs/évaluateurs/adaptateurs défectueux, les erreurs opérateur, les courses et les échecs partiels.

Les actifs à protéger comprennent la gouvernance canonique et son historique ; l’identité du dépôt et du candidat ; les dossiers de changement et approbations ; les preuves et leur provenance ; les clés et identités ; les binaires/configurations de l’évaluateur et des adaptateurs ; les décisions d’acceptation ; ainsi que les données privées et secrets rencontrés par les contrôles.

Les objectifs de sécurité sont l’intégrité, l’authenticité/l’autorité, la liaison à l’état exact, la fraîcheur, la disponibilité, la confidentialité et l’auditabilité.

Les frontières de confiance sont :
1. les entrées normatives, non fiables avant analyse et validation ;
2. le parseur, canonicaliseur, évaluateur et moteur de composition des règles, qui forment le TCB central ;
3. les scripts/contrôles du projet et leurs dépendances, potentiellement malveillants ;
4. les adaptateurs VCS interprétant les états natifs ;
5. les producteurs/vérificateurs de preuves, signatures et faits externes ;
6. l’opérateur/administrateur local, qui peut contourner les contrôles locaux ;
7. l’autorité d’acceptation partagée et ses administrateurs/identifiants ;
8. les projections Markdown générées, susceptibles de dérive et non normatives.

Les traitements sûrs requis incluent le rejet des encodages ambigus et clés dupliquées ; la gestion explicite des périmètres et conflits ; des limites de parsing et d’évaluation ; la protection contre les échappements de chemins et liens symboliques ; des preuves liées à l’état exact et résistantes au rejeu ; le recalcul des empreintes du candidat avant application ; des approbations authentifiées et autorisées avec politique de révocation ; le signalement explicite des capacités/erreurs d’adaptateur ; l’exécution à privilèges minimaux des contrôles projet ; le stockage des preuves respectueux de la confidentialité et la rédaction des secrets ; et des vérifications compare-and-swap/préconditions contre les courses.

GovCheck seul ne peut garantir un fonctionnement inviolable, hermétique ou « zero trust ». Une signature peut établir intégrité/provenance uniquement sous des hypothèses de gestion des clés ; elle ne prouve ni correction, ni autorité, ni vérité. Une barrière de forge n’est pas indépendante si un administrateur peut la désactiver. Ces limites doivent être explicites.

## 8. Stratégie de formalisation et de conformité

Les fondations formelles sont communes à tous les dépôts. La première cible formelle est le cycle de vie des changements et le prédicat d’acceptation, pas un modèle complet de chaque VCS, forge, parseur, système de fichiers ou scénario de menace.

Le modèle de cycle de vie doit rester petit et fini. Des modèles/contrats séparés conviennent à la composition des règles, à la sémantique Git/Pijul, à la concurrence et aux menaces. Ne pas construire un modèle monolithique dont l’espace d’états devient ingérable.

Les cibles de sûreté communes comprennent : correction des types ; solidité de l’acceptation ; application du candidat exact ; absence d’acceptation obsolète ; liaison des preuves et approbations ; absence d’approbation/application implicite ; historique append-only ; discipline des états terminaux ; et « inconnu n’est pas succès ». La vivacité est conditionnelle à l’action des acteurs, à la stabilisation des entrées, à la disponibilité des adaptateurs et à un ordonnancement équitable. Ne pas revendiquer de progression inconditionnelle.

Les vecteurs de conformité doivent être indépendants du langage et contenir les descripteurs et identités initiaux, les acteurs/autorités, la séquence d’actions, les preuves/dépendances, la transition et le motif attendus, les ajouts d’historique attendus et le résultat d’acceptation/application. Les familles minimales couvrent : chemin nominal ; preuves obligatoires manquantes ou indéterminées ; preuve obsolète après mutation du candidat ou de la gouvernance ; approbation non autorisée ou liée au mauvais candidat ; candidat appliqué différent ; mutation concurrente entre acceptation et application ; décisions terminales ; limite du mode local ; état Git dirty ; et préservation du graphe/patch/conflit natif Pijul.

## 9. Artefact formel actuel : `govcheck.lifecycle`

La PR #4 a ajouté le premier modèle TLA+ borné `formal/tla/GovCheckLifecycle.tla`, sa configuration TLC, des explications bilingues, un registre de transitions, un diagramme Mermaid généré, un générateur/contrôleur Python, un catalogue d’artefacts stables et un schéma de manifeste de release. La PR a été fusionnée dans `main` le 6 novembre 2026.

Le modèle lie un changement abstrait au tuple :

`(baseId, candidateId, governanceId, specId)`

Ses variables couvrent la phase, les identités du tuple, le tuple évalué, les résultats des obligations, les preuves, les approbations, le tuple accepté, le candidat appliqué et l’historique des événements. Ses actions sont `Prepare`, `PublishEvidence`, `Evaluate`, `Approve`, `Accept`, `Apply`, `ChangeInputs`, `Reject`, `Withdraw` et `Supersede`.

La configuration TLC utilise deux valeurs par dimension d’identité, deux acteurs, deux obligations et une limite d’historique de 12. Cette limite sert uniquement à garder fini l’espace d’états exploré ; ce n’est pas une politique de rétention en production.

Invariants d’état configurés :
- `TypeOK` : les variables restent dans leurs domaines déclarés.
- `AcceptanceSoundness` : Accepted est lié au tuple courant, à l’évaluation courante, aux obligations réussies et au nombre requis d’approbations.
- `ApplicationSoundness` : Applied identifie exactement le candidat du tuple accepté/courant.
- `NoStaleEvaluation` : Reviewable, Accepted et Applied ne reposent pas sur l’évaluation d’un ancien tuple.
- `EvidenceBinding` : Reviewable exige une preuve pour toutes les obligations modélisées.
- `ApprovalBinding` : les états accepted/applied ne contiennent que des approbations d’acteurs autorisés.
- `NoImplicitApplication` : aucune identité de candidat appliqué n’existe avant Applied.
- `HistoryNonEmpty` : l’événement initial de création reste présent.

La propriété temporelle `TerminalDiscipline` indique que Applied, Rejected, Withdrawn et Superseded ne peuvent plus effectuer de transition sortante. Le module énonce également des obligations de théorème à partir de `Spec` ; leur présence dans le source ne signifie pas qu’un prouveur les a déchargées.

### 9.1 Limites du modèle à conserver visibles

L’abstraction actuelle traite une preuve publiée comme suffisante et réussie. Elle n’établit pas la véracité, la provenance, les dépendances de fraîcheur, la révocation ou la vérification indépendante des preuves. `Fail` existe dans le domaine des résultats, mais aucune transition actuelle ne le produit. La concurrence, l’indisponibilité des adaptateurs, les adaptateurs malveillants, l’authenticité cryptographique, les mécanismes internes de Git, la sémantique native de Pijul et les courses du système de fichiers ne sont pas modélisés. La séquence d’événements est append-only dans les actions modélisées, mais il n’existe pas encore de propriété temporelle séparée d’intégrité de l’historique ni de métadonnées acteur/motif complètes. `ChangeInputs` est désactivée après les états terminaux, y compris Applied ; la politique de remédiation/réouverture après application reste à décider.

Le registre de transitions et le diagramme Mermaid sont des métadonnées explicatives. TLA+ est l’autorité sémantique. Le contrôleur Python vérifie la couverture structurelle des actions/opérateurs et la fraîcheur du fichier généré ; il n’analyse pas la sémantique TLA+ et ne prouve pas que les gardes/effets du registre décrivent fidèlement le modèle.

### 9.2 Statut des vérifications lors de la PR

Le rapport de PR documentait la réussite des contrôles structurels : parsing du registre JSON, couverture des dix actions de `Next`, définitions des opérateurs de premier niveau, bornes d’historique sur les actions modifiant l’état et cohérence du diagramme/rendu. Il ne revendiquait **pas** l’exécution du générateur dans un checkout, de TLC ou SANY, une preuve par théorème, une conformité de l’implémentation ou l’exécution de GitHub Actions. Ces tâches restent distinctes et ne découlent pas de la fusion.

Avant de qualifier le modèle de « model-checked », l’exécuter avec une version TLA+ Tools/TLC épinglée et consigner les empreintes exactes de l’outil et de la configuration, le statut d’achèvement, les états/transitions explorés et tout contre-exemple. Même une exécution TLC bornée réussie n’établit pas la conformité de l’implémentation.

## 10. Versionnement des artefacts et des releases

Les artefacts sources conservent des chemins stables ; Git enregistre leurs révisions. Un tag de release identifie le commit/arbre exact. Ne pas créer de copies sources `-v1`, `-v2` uniquement parce qu’une release est publiée.

Les identifiants logiques stables `artifactId` survivent aux renommages ; mettre à jour le catalogue dans le même changement lorsqu’un chemin évolue. Les rapports de vérification générés sont des artefacts propres à une release, joints à la GitHub Release correspondante, et non des sources renommées. Un manifeste lie tag/commit, identifiant d’artefact, chemin, empreinte du contenu, outil/version, empreinte de configuration, statut d’exécution et nombres de résultats disponibles. Ne jamais fabriquer un rapport ou un statut si l’exécution n’a pas eu lieu.

L’identifiant initial du modèle de cycle de vie est `govcheck.lifecycle`. Son catalogue est `formal/artifacts.json` ; le schéma du manifeste est `formal/schemas/release-manifest.schema.json`.

## 11. Choix technologiques volontairement différés

Aucun langage d’implémentation, format de sérialisation canonique, technologie de schéma, langage d’expression des règles, noyau formel, format cryptographique, licence ou ensemble obligatoire de dépendances n’a été choisi. Les familles de candidats du document d’architecture 0007 comprennent Rust, Go, OCaml, Haskell, Kotlin/JVM et Python ; JSON/JSON Schema, sous-ensembles YAML, TOML, CBOR et encodages canoniques ; prédicats typés fixes ou DSL restreint ; TLA+, Alloy, PlusCal et prouveurs de théorèmes ; hashes, attestations signées et mécanismes de transparence ; packaging d’un exécutable local ; adaptateurs de forge ; intégration native Pijul.

Les candidats doivent d’abord satisfaire les critères éliminatoires : préserver les sémantiques Git/Pijul ; fonctionner localement sans service hébergé/démon/MCP ; fournir une évaluation déterministe et bornée avec états inconnus/erreurs explicites ; éviter l’exécution arbitraire de politiques du dépôt ; permettre une distribution reproductible ; préserver les distinctions d’assurance. Les scores pondérés viennent après les critères éliminatoires et les preuves. « Inconnu » n’est ni un succès ni un zéro supposé.

## 12. Registre des décisions

| ID | Décision / contrainte | Statut |
|---|---|---|
| D-01 | GovCheck gouverne les dépôts et leur cycle de vie, pas les appels d’outils des agents | Tranché dans l’ADR 0001 |
| D-02 | Une autorité normative canonique lisible par machine ; Markdown est une projection/explication | Tranché comme contrat de conception |
| D-03 | Les fondations formelles s’appliquent à toute taille de dépôt ; aucun niveau d’assurance par taille | Tranché |
| D-04 | Petit exécutable local ; aucun MCP, démon ou service hébergé obligatoire | Tranché |
| D-05 | Git et Pijul sont de première classe, natifs et sémantiquement distincts | Tranché |
| D-06 | VCS, hébergement, collaboration et acceptation/application sont séparés | Tranché |
| D-07 | Anglais par défaut avec documentation française parallèle | Tranché |
| D-08 | Inconnu/non pris en charge/indéterminé ne satisfait pas une obligation obligatoire | Tranché comme objectif |
| D-09 | Tests, model checking, preuve par théorème, conformité, fidélité normative et acceptation sont distincts | Tranché |
| D-10 | Chemins sources et identifiants d’artefacts stables ; releases liées aux commits exacts et manifestes de preuves générées | Établi par la PR #4 |
| D-11 | TLA+ sert au premier modèle de cycle de vie ; cela ne présélectionne pas toute la pile formelle | Artefact initial actuel ; stratégie globale encore ouverte |
| D-12 | Aucun langage, format de sérialisation, DSL, format crypto, licence ou dépendance obligatoire choisi | Ouvert volontairement |

## 13. Questions ouvertes et suites ordonnées

Les points suivants ne sont pas résolus par cette mémoire et doivent faire l’objet d’ADR/spécifications ciblés et de preuves :

1. **Données et sémantique canoniques :** sérialisation, octets canoniques, gestion des clés dupliquées, évolution de schéma, versionnement sémantique et représentation typée des règles.
2. **Composition des règles :** précédence/raffinement précis, détection des contradictions, composition des profils, sémantique des exceptions et évaluation déterministe.
3. **Cycle de vie des preuves :** provenance, fraîcheur des dépendances, révocation, vérification indépendante, distinctions échec/inconnu/non pris en charge/non exécuté et confidentialité/rétention.
4. **Identités et approbations :** identité des acteurs, autorité, signatures, rotation/révocation des clés, invalidation des approbations et politique de rôles/seuils.
5. **Raffinement du cycle de vie :** contrôles explicitement échoués, réouverture/remédiation après application, intégrité de l’historique et champs acteur/motif, concurrence et équité.
6. **Vérification formelle :** version TLA+ Tools épinglée, exécution SANY/TLC, revue des contre-exemples, raffinements du modèle et cibles de preuve par théorème séparées si justifiées.
7. **Conformité de l’implémentation :** sémantique de référence exécutable, format de vecteurs indépendant du langage, relation de raffinement et harnais de tests.
8. **Adaptateurs VCS :** descripteurs exacts de l’état Git dirty/sous-modules et contrats natifs Pijul patch/canal/graphe/conflits, validés séparément.
9. **Frontière d’exécution :** privilèges minimaux, limites de ressources/temps, scripts projet malveillants, gestion des sorties et masquage des secrets.
10. **Application partagée :** négociation des capacités forge/équipe, protocole de barrière lié à l’état exact, visibilité des contournements et confiance envers les administrateurs.
11. **Distribution et maintenance :** packaging de l’exécutable local, builds reproductibles, plateformes supportées, licence et politique de dépendances.
12. **Fidélité documentaire :** génération/contrôle des projections, cohérence des traductions et traçabilité des identifiants de règles vers spécifications, modèles, tests et preuves de release.

Ordre recommandé : affiner les identités sémantiques et hypothèses sur les preuves ; valider le modèle de cycle de vie actuel avec un outillage TLC épinglé ; ajouter les vecteurs de conformité et les états échec/inconnu explicites ; modéliser séparément concurrence et frontières d’adaptateurs ; prototyper sérialisation canonique et sémantique de l’évaluateur ; puis comparer les technologies d’implémentation et de packaging sur des contrats désormais testables. Ne pas développer de nombreuses intégrations avant d’avoir clarifié la sémantique du cœur et la frontière de conformité.

## 14. Cartographie du dépôt

- `docs/decisions/0001-bootstrap-boundaries.md` : frontières produit acceptées et ADR de bootstrap.
- `docs/specifications/0002-canonical-governance-model.md` : contrat du modèle normatif.
- `docs/specifications/0003-change-lifecycle.md` : cycle de vie et acceptation.
- `docs/specifications/0004-vcs-collaboration-contracts.md` : adaptateurs Git/Pijul et collaboration.
- `docs/specifications/0005-assurance-model.md` : revendications, preuves et vocabulaire d’assurance.
- `docs/architecture/0006-threat-and-trust-model.md` : modèle de menace et frontières de confiance.
- `docs/architecture/0007-technology-decision-framework.md` : critères et méthode de comparaison technologique.
- `docs/architecture/0008-formalization-and-conformance.md` : plan de formalisation et conformité.
- `docs/formal/lifecycle-model.md` et `.fr.md` : explication du modèle de cycle de vie actuel.
- `formal/tla/GovCheckLifecycle.tla` et `.cfg` : modèle et configuration TLC.
- `formal/lifecycle-transitions.json`, `docs/formal/lifecycle-diagram.mmd`, `scripts/render-lifecycle-diagram.py` : registre explicatif, diagramme généré et contrôleur de dérive structurelle.
- `formal/artifacts.json`, `formal/schemas/release-manifest.schema.json` : identité des artefacts et manifeste de preuves de release.

- `docs/architecture/0010-assurance-proof-and-conformance.fr.md` : distinctions entre assurance, preuves, preuve formelle et conformité.
- `docs/architecture/0011-lifecycle-model-assertion-audit.fr.md` : audit du source du modèle TLA+ actuel.
- `docs/architecture/0012-normative-authority-and-documentation.fr.md` : autorité canonique et projections documentaires contrôlées.
- `docs/architecture/0013-governance-metamodel.fr.md` : objectifs, exigences, normes, propriétés et traçabilité de l’assurance.
- `docs/architecture/0014-governed-development-workflow.fr.md` : flux des tâches, responsabilités et qualification des agents.
- `docs/architecture/0015-governance-conformance-and-validation-plan.fr.md` : responsabilités de conformité, tests d’acceptation futurs et séquencement.

- `docs/architecture/0016-writ-privateer-assessment.fr.md` : évaluation de Writ et Privateer à partir de leurs sources, de leurs couches produit distinctes, limites de sécurité et rôles possibles comme fixtures de test.

## 15. Gestion des évolutions de cette mémoire

Ce document est une mémoire de conception et un index de décisions, pas une seconde spécification normative. Si une décision évolue, modifier d’abord l’ADR/la spécification/le modèle concerné, puis mettre à jour cette mémoire et sa version anglaise. Ne pas modifier silencieusement les décisions historiques : les remplacer par un ADR daté ou une révision explicite de spécification. Maintenir le statut d’implémentation et les affirmations de vérification alignés sur les preuves réellement présentes dans le dépôt.

## Références bibliographiques

- [R-05 — Modélisation par transitions d'états TLA+ / TLC](../references.fr.md#r-05)
- [R-18 — Évaluation de Writ comme fixture de workflow d'agent](../references.fr.md#r-18)
- [R-19 — Évaluation de Privateer comme fixture de workflow d'agent](../references.fr.md#r-19)
- [R-22 — Sémantiques natives Git et Pijul](../references.fr.md#r-22)
- [R-29 — Modélisation relationnelle et analyse Alloy](../references.fr.md#r-37)
