# 0024 — Bootstrap de projet, choix de gouvernance et profils d'assurance

**Statut :** proposition de conception produit et architecture soumise à revue ; ce document n'implémente ni assistant interactif, ni schéma de profil, ni moteur de modèles, ni commande de modification de dépôt.  
**Langue :** l'anglais est la langue par défaut ; voir le [document anglais](0024-project-bootstrap-and-assurance-profiles.md).

## 1. Objectif

Un nouveau dépôt ne devrait pas commencer par une arborescence générique et entièrement peuplée. GovCheck doit guider le responsable du projet dans des décisions importantes de gouvernance et d'assurance, expliquer les compromis, puis préparer une structure de dépôt correspondant aux choix réellement effectués.

Le bootstrap a trois responsabilités :

1. **Décider :** recueillir le contexte et expliquer les options de gouvernance et d'assurance, leurs conséquences, coûts et limites.
2. **Planifier :** traduire les décisions explicites en un plan de dépôt déterministe et révisable.
3. **Appliquer :** créer uniquement la structure sélectionnée, sans écraser le contenu existant ni modifier silencieusement la politique normative.

Il s'agit d'un assistant à la création de projet, pas simplement d'un générateur de répertoires ni d'un questionnaire attribuant une note de maturité.

## 2. Relation avec les fondations existantes

Cette conception complète, sans les modifier silencieusement, l'ADR 0001, la spécification 0002 (modèle canonique de gouvernance), la spécification 0005 (assurance, affirmations et preuves) et l'architecture 0015 (outil de conformité de gouvernance et plan de validation).

La distinction suivante est obligatoire :

- **Les fondations de gouvernance GovCheck sont invariantes.** Chaque dépôt gouverné possède une identité/profil canonique de gouvernance, des sémantiques explicites d'applicabilité et de décision, et la capacité d'enregistrer affirmations d'assurance, preuves, provenance et incertitude. Les profils peuvent ajouter des contraintes, jamais supprimer ces fondations.
- **Les méthodes d'assurance du projet sont configurables.** Un projet peut sélectionner des tests empiriques, de l'analyse statique, du model checking, de la vérification de programmes, de la preuve de théorèmes, des travaux de conformité de l'implémentation, ou des combinaisons adaptées à ses affirmations. Ne sélectionner aucune méthode formelle propre au projet est valide.
- **Une méthode n'est pas un niveau de maturité.** Ne pas classer les dépôts en bronze/argent/or ou assurance faible/moyenne/élevée selon leur taille. Le choix des méthodes dépend des affirmations, des risques, du domaine et des conséquences. Différentes affirmations d'un même dépôt peuvent nécessiter différentes méthodes.
- **Aucune méthode de preuve n'est présumée supérieure pour toutes les affirmations.** Tests, analyse statique, model checking, vérification de programmes et preuve de théorèmes établissent des choses différentes. Le bootstrap doit expliquer ce que chaque méthode peut ou ne peut pas établir, ses hypothèses, son coût opérationnel et sa charge de maintenance.

Ainsi, un projet qui ne sélectionne aucune vérification formelle conserve les fondations de gouvernance et d'assurance de GovCheck, mais ne reçoit pas de répertoires, configurations ou chaînes d'outils Lean, TLA+, sources de preuves ou compilation de preuves propres au projet, simplement pour faire bonne figure.

## 3. Parcours de décision guidé

La CLI est l'interface initiale principale, conformément à l'ADR 0001. Elle doit être utilisable de manière interactive par une personne et de manière non interactive par scripts/agents au moyen de réponses explicites et lisibles par machine. Une interface graphique pourra ultérieurement consommer le même modèle de décision ; elle ne devra pas créer un second évaluateur de politique.

Le dialogue doit être progressif et contextuel, pas une liste plate d'options sans explication.

### 3.1 Contexte du projet

Recueillir uniquement les faits influençant les recommandations ou les obligations générées, avec des états explicites « inconnu/non fourni » :

- objectif du projet, utilisateurs et contexte opérationnel ;
- type de logiciel et composants critiques ;
- sensibilité des données et exposition de sécurité ;
- conséquences d'une défaillance et attentes de reprise ;
- contraintes légales, contractuelles, sectorielles ou organisationnelles applicables, lorsqu'elles sont déclarées par le responsable ;
- modèle de déploiement et de mise à jour ;
- contributeurs, autorité décisionnelle, capacité de revue et collaboration externe ;
- contexte VCS et hébergement/collaboration (Git ou Pijul ; local, hébergé en équipe, auto-hébergé ou public).

GovCheck ne doit pas déduire une conformité légale ou une acceptation du risque à partir d'une simple étiquette de projet. Les recommandations doivent identifier les faits et hypothèses dont elles dépendent.

### 3.2 Décisions de gouvernance

Expliquer et permettre au responsable de décider, selon le cas :

- autorité et délégation : personne, mainteneurs nommés, équipe ou organisation ;
- approbation des changements et séparation des tâches ;
- enregistrements de décisions et circonstances qui les rendent nécessaires ;
- exigences et attentes de traçabilité ;
- politique de contribution et de revue ;
- autorité des exceptions/dérogations, périmètre, expiration et mesures compensatoires ;
- attentes de publication, provenance et conservation des preuves ;
- gouvernance de sécurité et réponse aux incidents.

Un choix tel que « projet individuel » ne doit pas impliquer automatiquement que tous les changements sont auto-approuvés si le responsable choisit une revue indépendante. Autorité et revue sont deux décisions distinctes.

### 3.3 Affirmations d'assurance et méthodes

Commencer par les propriétés que le projet souhaite établir, pas par une liste d'outils. Pour chaque affirmation ou famille d'affirmations, demander quelles preuves seraient convaincantes et proportionnées.

| Famille de méthodes | Ce qu'elle peut étayer | Limite importante à expliquer |
|---|---|---|
| Tests unitaires/d'intégration | Comportement observé pour les cas et chemins exécutés | N'établit pas le comportement hors des cas testés |
| Tests fondés sur les propriétés/fuzzing | Comportement sur des entrées générées ou fuzzées | L'échantillonnage n'est pas une preuve mathématique |
| Analyse statique/vérification de types | Détection ou exclusion de classes de défauts ciblées sous les hypothèses de l'outil | N'établit pas tout le comportement à l'exécution |
| Model checking (ex. TLA+/TLC) | Propriétés d'un modèle explicite dans son espace d'états, ses bornes et hypothèses | N'établit pas à lui seul la conformité de l'implémentation |
| Vérification de programmes (ex. Dafny, Verus, Kani) | Propriétés spécifiées d'un programme dans le cadre du vérificateur et de ses hypothèses de confiance | Portée et socle de confiance dépendent de l'outil et du langage |
| Preuve de théorèmes (ex. Lean, Coq, Isabelle) | Dérivations acceptées par un noyau logique spécifié et ses hypothèses | Ne choisit pas les bonnes exigences et ne prouve pas la correction d'une implémentation non reliée |
| Conformité implémentation/spécification | Relation justifiée entre implémentation et spécification | Exige un argument explicite de raffinement/conformité et des preuves |

Les méthodes peuvent être combinées. Par exemple, des tests peuvent valider le comportement d'intégration tandis que TLA+ explore des propriétés de concurrence ; aucun résultat ne remplace l'autre. Un assistant de preuve n'est pas automatiquement approprié à une logique métier ordinaire, et une suite de tests verte ne doit jamais être décrite comme une preuve formelle.

L'utilisateur peut explicitement sélectionner **aucune vérification formelle propre au projet**. Ce n'est ni un échec ni une réduction des fondations de gouvernance GovCheck. Le profil résultant enregistre cette décision et son périmètre afin que des affirmations ultérieures ne laissent pas entendre que des propriétés formelles ont été établies.

### 3.4 Qualité des recommandations

Pour chaque recommandation, afficher :

- le fait du projet, l'affirmation ou la conséquence qui l'a déclenchée ;
- la méthode ou le contrôle proposé ;
- ce qu'il peut établir et ce qu'il ne peut pas établir ;
- la charge attendue de maintenance/outillage et les dépendances ;
- les hypothèses, incertitudes et éventuelles décisions humaines encore nécessaires.

Les recommandations sont consultatives, sauf si une contrainte légale/contractuelle applicable ou une politique de projet autorisée rend un contrôle obligatoire. GovCheck doit distinguer le choix du responsable, la recommandation de GovCheck et l'obligation normative.

### 3.5 Assurance guidée par les menaces et traçabilité

Le bootstrap doit relier le contexte du projet et les choix d'assurance à une analyse explicite des menaces et des risques. Il ne doit pas demander de sélectionner des outils isolément.

Maintenir des relations typées et traçables entre, au minimum :

- actifs et intérêts métier/opérationnels ;
- objectifs de sécurité et de sûreté ;
- sources/acteurs de menace, capacités et motivations lorsqu'elles sont connues ;
- événements et scénarios de menace ;
- techniques, préconditions et chemins d'attaque, frontières de confiance traversées ;
- vulnérabilités, faiblesses et conditions d'exposition ;
- mesures préventives, détectives, de réponse et de récupération ;
- instances de mise en œuvre/configuration des mesures et responsables ;
- affirmations d'assurance, hypothèses, preuves, limites et décisions de revue ;
- risques résiduels, décisions de traitement, propriétaires du risque et déclencheurs de réexamen.

Employer une terminologie précise dans l'interface. Une **menace** est une cause potentielle de dommage ; un **scénario de menace** décrit comment une source/un événement de menace pourrait affecter un actif dans un contexte donné ; un **chemin d'attaque** est une séquence réalisable à travers des composants, privilèges ou frontières de confiance ; une **vulnérabilité/faiblesse** est une condition pouvant permettre ou amplifier un événement. Ces notions sont liées, mais ne doivent pas être réduites à un seul champ binaire.

Le graphe de traçabilité doit fonctionner dans les deux sens. Depuis un scénario de menace, l'utilisateur peut examiner les chemins, faiblesses, mesures, activités de vérification, preuves, risques résiduels et décisions responsables. Depuis une mesure ou une preuve, il peut voir quels scénarios et affirmations elle traite, sous quelles hypothèses et dans quel périmètre. Une mesure sans objectif ni scénario déclaré appelle une justification ; elle n'est pas automatiquement invalide, car elle peut relever de la défense en profondeur ou répondre à une obligation extérieure au jeu de menaces actuel.

La couverture n'est pas un pourcentage unique et ne doit pas être présentée comme une preuve de sécurité. Faire notamment ressortir :
- les scénarios sans traitement proposé ;
- les chemins sans mesure efficace à une ou plusieurs étapes critiques ;
- les mesures planifiées mais non mises en œuvre ;
- les mesures mises en œuvre mais non testées ou autrement assurées ;
- les preuves ne couvrant pas le déploiement/la configuration concernés ;
- les affirmations dont les hypothèses ne sont pas vérifiées ou étayées ;
- les preuves périmées, incomplètes, contestées ou produites par un composant non fiable ;
- les risques acceptés sans responsable compétent, justification, périmètre ou condition de réexamen.

Une mesure n'est pas « efficace » simplement parce qu'elle est documentée ou générée par le bootstrap. Distinguer les états proposés, mis en œuvre, configurés, testés/observés, revus indépendamment et surveillés en exploitation. Un test de mesure n'étaye que le périmètre et les conditions effectivement testés.

### 3.6 Hypothèses, inférences et limites

Tout argument d'assurance doit rendre son raisonnement inspectable :

- **Hypothèse :** prémisse tenue pour acquise dans un argument délimité, avec source, responsable, périmètre, confiance, période de validité et conditions de réfutation/réexamen.
- **Preuve :** observation, résultat de test, analyse, attestation ou démonstration produit dans des conditions déclarées.
- **Inférence :** raisonnement explicite reliant hypothèses et preuves à une affirmation.
- **Conclusion :** affirmation délimitée étayée par cet argument, et non garantie plus large.
- **Limite/inconnu :** ce qui n'a pas été examiné, n'est pas établi ou dépend d'une prémisse non résolue.

Montrer à l'utilisateur ce qui est supposé et ce qui peut en être déduit. Par exemple : « En supposant que le noyau de l'hôte et le compte administrateur soient fiables, cette politique de sandbox restreint les accès déclarés du worker au système de fichiers et au réseau » est nettement plus limité que « le worker est confiné ». Si l'administrateur de l'hôte fait partie du modèle de menace, le même argument n'établit aucune protection contre cet adversaire.

Les hypothèses ne sont jamais silencieusement promues au rang de faits. Leur provenance et leur niveau de confiance doivent être visibles ; les hypothèses critiques devraient être associées à des actions de validation ou à une acceptation explicite par un responsable du risque autorisé. Inconnu ne signifie pas faux, et une hypothèse non vérifiée ne peut pas être affichée comme une preuve établie. Le bootstrap doit identifier le socle de confiance et les dépendances externes de chaque méthode d'assurance : runners de contrôle, compilateurs, model checkers, noyaux de preuve, systèmes de build, fournisseurs d'identité et points d'application, selon le cas.

Le model checking ou la preuve de théorèmes peuvent établir des propriétés d'un modèle ou d'une dérivation sous les hypothèses et la formalisation retenues. Ils n'établissent pas automatiquement que le modèle couvre toutes les menaces pertinentes, que l'implémentation est conforme au modèle, que le déploiement correspond à la configuration analysée ou que les hypothèses restent vraies en exploitation. Tests, analyse statique, supervision opérationnelle et attestations externes ont leurs propres périmètres et dépendances de confiance. L'interface doit montrer cette chaîne plutôt que classer les méthodes par prestige.

## 4. Évaluation et traitement des risques

Le risque est contextuel et gradué, pas une propriété booléenne. GovCheck ne doit pas assimiler « une menace existe » à « le risque est inacceptable », ni « aucune menace n'est enregistrée » à « le système est sûr ».

Pour chaque scénario, permettre une évaluation documentée de :
- vraisemblance/plausibilité, avec fondement et incertitude de l'estimation ;
- impact selon les dimensions pertinentes (confidentialité, intégrité, disponibilité, sûreté, vie privée, finances, droit, opérations ou réputation) ;
- exposition, capacité de l'attaquant, préconditions et opportunité ;
- mesures existantes et efficacité démontrée dans leur périmètre ;
- risque inhérent avant mesures et risque résiduel après mesures ;
- confiance dans l'évaluation et inconnues importantes.

Ne pas imposer une fausse précision numérique. Les projets peuvent employer des échelles qualitatives, ordinales calibrées ou des méthodes quantitatives lorsqu'elles sont défendables. L'échelle choisie, ses définitions, règles d'agrégation et incertitudes doivent être explicites et versionnées. Éviter de multiplier des étiquettes ordinales arbitraires et de présenter le résultat comme un score de risque mathématiquement significatif. Les évaluations servent à prioriser les décisions ; elles ne sont pas des mesures objectives de la vérité.

Pour chaque risque, guider le responsable parmi les options de traitement :
- **éviter :** modifier ou supprimer l'activité, l'actif ou l'exposition à l'origine du risque ;
- **réduire/atténuer :** introduire ou améliorer des mesures, puis évaluer leur mise en œuvre et leur efficacité ;
- **transférer/partager :** répartir une partie des conséquences financières ou opérationnelles par contrat ou service, en précisant que la responsabilité et toutes les conséquences ne sont pas nécessairement transférées ;
- **accepter/conserver :** conserver consciemment le risque résiduel dans le cadre d'une décision autorisée.

L'acceptation n'est pas le choix par défaut en l'absence de mesures. Enregistrer le propriétaire du risque, l'autorité décisionnaire, la justification, les actifs/scénarios concernés, le niveau et l'incertitude du risque résiduel, les mesures compensatoires, le périmètre, la date, l'échéance ou date de revue et les déclencheurs de réévaluation (évolution d'architecture/dépendances/menaces, incident, nouvelle exposition, échec d'une mesure, changement d'hypothèse ou obligation réglementaire). Une acceptation peut être limitée dans le temps ou conditionnelle. Une personne ne peut accepter que dans les limites de son autorité enregistrée et de sa délégation. GovCheck ne doit déduire aucune acceptation du silence, d'une coche verte, d'une fusion ou de l'absence de remédiation.

L'outil doit aider à comparer les options de traitement, leurs coûts, leur charge opérationnelle et l'exposition résiduelle. Il peut recommander des mesures supplémentaires ou une escalade, mais doit distinguer conseil, obligation et décision autorisée sur le risque. Un risque résiduel élevé peut être consciemment accepté lorsque l'autorité le permet ; l'interface ne doit ni le masquer ni présenter le projet comme sans risque. Inversement, une évaluation faible ou incertaine ne doit pas servir à écarter un scénario rare mais aux conséquences graves sans justification explicite.

L'acceptation du risque ne fait pas disparaître une menace, ne valide pas une mesure et ne transforme pas une affirmation non étayée en affirmation étayée. Elle enregistre une décision gouvernée d'opérer avec une exposition résiduelle connue. Le statut d'assurance et le traitement du risque doivent donc rester distincts, mais reliés.

## 5. Profil et arborescence générée

Le résultat est un profil de projet lisible par machine et versionné, accompagné d'un plan de bootstrap déterministe. Le profil enregistre les capacités sélectionnées, les non-sélections explicites lorsque pertinentes, les justifications, le contexte/hypothèses, l'autorité et les révisions du profil/schéma. Il ne constitue pas une seconde source normative : les règles normatives restent dans le paquet canonique de gouvernance.

Le générateur s'appuie sur des déclarations de capacités et leurs dépendances plutôt que sur un modèle monolithique. Correspondance indicative :

| Capacité sélectionnée | Contenu candidat généré |
|---|---|
| Socle de gouvernance (toujours) | configuration/profil canonique, explication/projection de gouvernance, points d'entrée pour décisions et cycle de vie des changements |
| Enregistrements de décisions | `docs/decisions/` et modèle de décision |
| Traçabilité des exigences | `requirements/`, conventions d'ID stable et métadonnées de traçabilité |
| Tests unitaires/d'intégration | `tests/`, structure de tests sélectionnée et commandes documentées |
| Tests fondés sur les propriétés | structure de tests de propriétés et configuration d'outils |
| Analyse statique | configuration de l'analyseur sélectionné et déclarations de contrôles |
| Model checking TLA+ | `formal/tla/`, squelette de modèle/configuration et invocation épinglée |
| Preuve de théorèmes Lean | `formal/lean/`, squelette de projet/chaîne d'outils et commande de vérification |
| Autre vérification de programme | uniquement sources/configuration du vérificateur choisi et commande reproductible |
| Modélisation des menaces | `security/threat-models/` et modèle de périmètre de menace |
| Provenance des publications | structure de manifeste de publication/preuves et instructions de provenance |

Ce tableau est indicatif, pas un contrat figé de répertoires. La correspondance finale doit être maintenue dans un catalogue de modèles versionné, avec dépendances explicites, conflits, propriété des fichiers générés et comportement de migration.

Règles :

1. Ne pas créer de répertoire, chaîne d'outils, workflow ou README fictif propre à une méthode si celle-ci n'est pas sélectionnée.
2. Ne pas créer de répertoire `formal/` vide si aucune méthode formelle propre au projet n'est sélectionnée.
3. Les fondations partagées de preuve et de provenance appartiennent au socle gouvernance/assurance ; les schémas ou exécuteurs de preuves propres à une méthode ne sont inclus que s'ils sont nécessaires.
4. Une capacité sélectionnée doit générer un point de départ utilisable et documenté — pas un répertoire vide laissant croire qu'un contrôle opérationnel existe.
5. Ne jamais prétendre qu'un squelette généré constitue une suite de tests, une preuve, un contrôle de sécurité ou une barrière CI fonctionnels avant configuration et exécution.
6. Les noms de répertoires sont des détails d'implémentation. Les identifiants stables de capacité du profil et les relations typées entre artefacts font autorité pour la planification.

## 6. Dépendances et composition des capacités

Les capacités forment un graphe de dépendances typées, pas un ensemble de booléens indépendants. Exemples :

- une capacité de model checking TLA+ dépend d'un artefact modèle, d'une configuration, d'une invocation TLC épinglée et d'un contrat d'enregistrement du résultat ;
- la preuve de théorèmes Lean dépend d'une déclaration de projet/chaîne d'outils Lean, de sources de preuve, de l'épinglage des dépendances et d'une commande reproductible de vérification ;
- une capacité de traçabilité exigence-vers-test dépend d'identités stables d'exigences/affirmations et de relations typées vers les preuves ;
- une capacité de provenance de publication dépend de l'identité exacte de la source/publication et d'un enregistrement manifeste/preuve.

Le résolveur doit détecter les dépendances manquantes, sélections incompatibles, combinaisons non prises en charge et cycles. Il doit en expliquer la raison et proposer une résolution ; il ne doit pas activer silencieusement des capacités supplémentaires. Une capacité peut déclarer séparément des prérequis obligatoires, recommandations facultatives et conflits.

Aucune méthode formelle propre au projet n'est un prérequis du socle de gouvernance.

## 7. Cycle de vie du bootstrap : inspecter → décider → planifier → revoir → appliquer → vérifier

Le bootstrap doit préserver le cycle non destructif de l'ADR 0001 et rendre explicite l'étape de décision :

1. **Inspecter :** identifier le VCS, les fichiers existants, les métadonnées du projet et le profil GovCheck existant, le cas échéant. Préserver les sémantiques natives Git/Pijul.
2. **Décider :** mener le dialogue guidé ou valider les réponses fournies. Les réponses inconnues restent inconnues ; ne pas deviner.
3. **Planifier :** résoudre les dépendances des capacités et produire un plan déterministe de fichiers/opérations, comprenant justifications, omissions, conflits et outils requis.
4. **Revoir :** présenter l'arborescence proposée et chaque fichier à créer, modifier, préserver ou ignorer. Expliquer séparément les changements normatifs.
5. **Appliquer :** exiger une confirmation explicite ; ne jamais écraser les fichiers non détenus par GovCheck. Les conflits avec des fichiers existants arrêtent l'opération ou exigent une fusion examinée séparément.
6. **Vérifier :** valider le profil/schéma, les projections générées, les fichiers attendus, la fermeture des dépendances et les contrôles locaux disponibles. Signaler honnêtement les contrôles non exécutés.

Le plan doit permettre aperçu/dry-run, sortie lisible par machine, régénération déterministe, réexécution idempotente et empreinte stable du plan. L'application d'un même profil au même état inspecté doit produire le même plan. Un profil modifié produit un nouveau plan et un diff de migration ; il ne doit pas supprimer automatiquement du contenu généré antérieurement ou appartenant à l'utilisateur.

Pour les dépôts existants, le bootstrap est un assistant de migration, pas une commande de remise à zéro. Il doit détecter la dérive et préserver les modifications utilisateur. Tout nettoyage destructeur exige une opération distincte et explicite, soumise à revue.

## 8. Évolution après le bootstrap

Le profil n'est pas le résultat définitif d'un questionnaire. Un projet peut ensuite ajouter ou retirer des capacités lorsque ses affirmations, risques, équipe ou contexte de déploiement évoluent.

Une modification de profil doit :

- créer un enregistrement de décision/changement lié à une révision ;
- présenter les ajouts, suppressions et obligations modifiées ;
- identifier les artefacts générés devenus inutilisés, obsolètes ou invalides ;
- préserver l'historique et le contenu appartenant à l'utilisateur ;
- exiger une revue avant de supprimer des fichiers ou d'affaiblir des obligations ;
- réévaluer les affirmations/preuves affectées selon le modèle de fraîcheur de l'Architecture 0021.

Retirer une méthode formelle du profil actif n'efface pas les anciennes preuves ou décisions. Cela ne modifie l'applicabilité et les attentes d'acceptation futures que par une décision autorisée et prospective.

## 9. Esquisse de CLI et interface machine

Les noms exacts des commandes restent ouverts, mais le parcours devrait prendre en charge des équivalents de :

- `govcheck init` — démarrer le bootstrap guidé ;
- `govcheck init --answers <file>` — décisions non interactives validées par schéma ;
- `govcheck plan` — inspecter et afficher le plan déterministe ;
- `govcheck apply` — appliquer un plan revu ;
- `govcheck profile show|validate` — inspecter et valider le profil actif ;
- `govcheck plan --format json` — plan lisible par machine pour scripts/agents.

Il s'agit d'esquisses d'interface, pas de commandes implémentées ni d'un contrat CLI approuvé. La syntaxe exacte, la sérialisation et le schéma du profil nécessitent une spécification et un prototype séparés.

## 10. Scénarios d'acceptation du premier prototype

Un prototype devrait démontrer au minimum :

1. Une petite bibliothèque locale sélectionnant socle de gouvernance, tests unitaires/intégration et analyse statique, sans arborescence `formal/`.
2. Un projet sélectionnant explicitement aucun test et aucune méthode formelle propre au projet ; le plan explique la conséquence et ne crée aucun répertoire correspondant.
3. Un service concurrent/distribué sélectionnant tests et TLA+ ; l'arborescence générée contient un point d'entrée utilisable pour le modèle/configuration/vérification.
4. Un composant orienté preuve sélectionnant Lean ; l'arborescence inclut une chaîne d'outils épinglée et un point d'entrée reproductible de vérification des preuves.
5. Un dépôt existant avec du contenu utilisateur dans `tests/` ou `formal/` ; l'aperçu détecte les conflits et l'application les préserve.
6. Une modification de profil ajoutant ou retirant une capacité ; le plan de migration préserve les preuves historiques et ne supprime jamais silencieusement les fichiers source.
7. Un risque/contexte de projet inconnu ; les recommandations exposent l'incertitude plutôt que de sélectionner silencieusement un profil d'assurance élevé ou faible.
8. Les mêmes réponses et le même état inspecté produisent une sortie de plan identique octet pour octet.
9. Les contextes Git et Pijul préservent leurs identités et sémantiques d'état natives.
10. Les réponses fournies par machine sont validées ; identifiants de capacité inconnus, dépendances manquantes et décisions contradictoires échouent de manière fermée avec explications exploitables.
11. Les scénarios de menace sont traçables dans les deux sens à travers chemins d'attaque, faiblesses, mesures, affirmations d'assurance, hypothèses, preuves et décisions de risque résiduel.
12. Le prototype distingue les mesures non évaluées, non traitées, planifiées, mises en œuvre, testées, revues et surveillées ; il expose les chemins non couverts et les hypothèses non étayées.
13. Le risque ne peut être accepté que par un responsable autorisé, avec justification, périmètre, évaluation résiduelle et conditions de revue/expiration ; l'acceptation ne modifie jamais le statut des preuves.

## 11. Séquence de livraison

1. Examiner ce modèle de décision et harmoniser la terminologie avec les spécifications 0002/0005 et les architectures 0013/0015/0021.
2. Définir les identifiants stables de capacités, le schéma de profil, la sémantique des dépendances et le contrat du catalogue de modèles.
3. Prototyper une CLI locale avec inspecter/réponses/planifier uniquement ; ne pas encore modifier les dépôts.
4. Ajouter application sûre, détection de conflits, idempotence et comportement de migration.
5. Valider des fixtures représentatives Git/Pijul, petites/grandes, tests uniquement et méthodes formelles.
6. Ajouter projections/documentation générées et adaptateurs facultatifs forge/CI seulement après stabilisation des sémantiques locales.

Ne pas commencer par une grande interface graphique, un service hébergé, un serveur MCP obligatoire, une place de marché de plugins ou un modèle universel de projet. L'exécutable local reste l'interface principale.

## 12. Limites et statut

Ce document définit une expérience proposée et ses propriétés de sûreté. Il ne sélectionne ni langage d'implémentation, ni format de sérialisation, ni syntaxe CLI concrète, ni framework de test, assistant de preuve, model checker, catalogue de répertoires ou profil de projet par défaut. Il ne prétend pas qu'une fonctionnalité de bootstrap existe déjà.

L'architecture doit être conciliée avec l'autorité canonique de gouvernance existante avant qu'un profil ne devienne normatif. Une arborescence générée ne constitue pas une preuve de conformité de gouvernance ; la vérification doit évaluer le profil réel, les fichiers, outils, exécutions et l'état exact du dépôt.
