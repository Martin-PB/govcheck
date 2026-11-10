# Intention produit GovCheck — constitution et évolution gouvernées

**Type de document :** intention produit et orientation de conception ; ce document n'est pas un ADR et n'adopte pas de choix d'implémentation.  
**Statut :** capture de l'intention exprimée par le propriétaire, destinée à une analyse d'impact systématique. Le propriétaire du dépôt conserve l'autorité de décision ; les recommandations de ce document ne deviennent pas une politique approuvée du seul fait de leur consignation.  
**Langue :** l'anglais est la langue par défaut ; voir la [version anglaise](product-intent.md).

## 1. Objet de ce document

Ce document capture l'évolution de l'intention produit discutée lors du réexamen du bootstrap du package et du besoin apparent de deux fichiers `AGENTS.md`. Il conserve délibérément le raisonnement depuis la préoccupation initiale jusqu'à son affinage :

1. Le package GovCheck réutilisable et le dépôt de développement de GovCheck ont tous deux besoin d'instructions pour les agents, mais ces instructions ne peuvent pas être identiques : le fichier racine `AGENTS.md` du dépôt GovCheck gouverne le travail sur GovCheck lui-même, tandis que le `AGENTS.md` d'un dépôt gouverné doit refléter la gouvernance approuvée de ce dépôt.
2. Le package ne peut pas fournir un `AGENTS.md` universellement canonique, prêt à être copié. GovCheck fournit tout au plus des structures d'instructions réutilisables, des fragments, une logique de décision et des mécanismes de génération.
3. Le bootstrap ne consiste pas simplement à copier un répertoire ou à rendre des modèles. Il marque le début d'un processus gouverné dans lequel les mainteneurs établissent la gouvernance du dépôt, ses autorités, obligations, attentes d'assurance et capacités applicables.
4. Ce processus est progressif. Il commence par un petit nombre de décisions fondatrices et réexamine les décisions ultérieures lorsque de nouveaux sujets, changements, risques ou éléments d'évidence les rendent pertinents.
5. Les décisions sont contextualisées par des sources, des critères et un raisonnement explicite. GovCheck peut guider la décision de manière déterministe, présenter les éléments bruts ou les mettre à disposition d'un agent assistant ; l'autorité humaine ou organisationnelle habilitée reste responsable de l'approbation.
6. L'autorité de gouvernance peut être distribuée par domaine et catégorie de décision. Les personnes qui réalisent les modifications n'ont pas nécessairement autorité pour affaiblir les exigences auxquelles ces modifications sont évaluées.
7. Le modèle initial de gouvernance est restrictif et fonctionne en échec fermé. Un blocage ne peut être assoupli que par une décision explicite et traçable de l'autorité compétente, dans les limites de son autorité et de son périmètre.

Il s'agit d'une base d'intention produit pour l'analyse d'impact à venir. Ce document ne remplace, ne modifie ni n'approuve implicitement les ADR, spécifications, documents d'architecture, modèles formels ou contrats d'implémentation existants.

## 2. Définition du produit

**GovCheck est un système permettant de constituer, exprimer, justifier, gouverner, appliquer et faire évoluer la gouvernance et l'assurance des dépôts logiciels.**

Il aide les personnes responsables d'un dépôt à :

- établir un modèle de gouvernance propre au dépôt à partir d'un socle initialement restrictif ;
- définir les autorités, rôles, responsabilités, délégations et droits de décision ;
- identifier les décisions requises par le contexte et le cycle de vie du dépôt ;
- découvrir et consulter les sources et connaissances pertinentes au moment de décider ;
- raisonner sur les exigences, propriétés, risques et méthodes d'assurance adaptées ;
- enregistrer les décisions, leur autorité, leur justification, les alternatives, hypothèses, sources, périmètre et validité ;
- traduire les décisions approuvées en obligations applicables et en projections contrôlées destinées aux humains et aux agents ;
- évaluer les changements proposés au regard de ces obligations et des éléments d'évidence requis ;
- gouverner les exceptions, acceptations de risques, mesures compensatoires et modifications de politique ;
- réexaminer les décisions lorsque le contexte, l'architecture, les menaces, les exigences, les éléments d'évidence ou les autorités organisationnelles évoluent.

GovCheck est donc davantage qu'un vérificateur de politiques, un bootstrapper, un générateur de documents, une action CI ou un ensemble d'instructions pour agents. Le contrôle de conformité est une composante importante d'un cycle de vie plus large des décisions et de la gouvernance.

L'objet gouverné est le dépôt et le cycle de vie de son logiciel. Les humains et les agents de codage y contribuent dans le cadre de cette gouvernance. GovCheck n'est pas principalement un bac à sable pour agents, une passerelle d'appels d'outils, un service d'approbation hébergé ou un remplacement de forge.

## 3. Le package fournit un cadre, pas une politique universelle pour les dépôts

Le package GovCheck réutilisable définit les concepts, sémantiques, capacités, sources, mécanismes d'aide à la décision, règles de validation et moyens de génération nécessaires à la construction et à l'exploitation d'un modèle de gouvernance propre à chaque dépôt.

Il ne doit pas prédéterminer pour tous les dépôts :

- la structure des autorités ou la séparation des tâches ;
- les catégories de décisions et seuils d'approbation ;
- les capacités métier ou standards applicables ;
- les méthodes d'assurance pour chaque affirmation ou propriété ;
- l'appétence au risque, l'autorité d'exception ou les conditions de livraison ;
- les flux de travail humains/agents ou le contenu des instructions générées.

Il s'agit de décisions propres à chaque dépôt, soumises aux fondations sémantiques invariantes de GovCheck et aux obligations externes explicitement applicables.

Il n'existe pas de `AGENTS.md` canonique au niveau du package dont le contenu pourrait être copié sans modification comme politique de chaque dépôt gouverné. GovCheck peut fournir des modèles génériques, des fragments réutilisables, des explications et une logique de rendu. Le véritable `AGENTS.md` est une projection propre au dépôt, générée ou contrôlée à partir des décisions de gouvernance approuvées, des capacités sélectionnées, des obligations applicables et des besoins opérationnels des agents.

Les fichiers racine `AGENTS.md` et `AGENTS.fr.md` du dépôt de développement GovCheck restent spécifiques au développement et à la gouvernance de GovCheck. Ils ne doivent pas être confondus avec les modèles ou sorties destinés aux dépôts utilisateurs. Un nom de modèle tel que `AGENTS.md.tmpl` constitue une technique de packaging possible, pas une exigence d'implémentation arrêtée.

Le même principe vaut pour `GOVERNANCE.md`, `SECURITY.md`, `CONTRIBUTING.md`, la configuration CI, les bundles de politiques et les autres projections : ce sont des représentations dérivées ou contrôlées, pas des autorités normatives indépendantes.

## 4. Constitution progressive : le bootstrap est un commencement, pas un processus complet

### 4.1 Inspecter avant de questionner

Pour un dépôt existant, GovCheck doit inspecter l'état observable du dépôt et les éléments de gouvernance disponibles avant de poser des questions. Pour un dépôt nouveau ou vide, il commence avec les informations fournies par ses mainteneurs.

Les résultats d'inspection sont des observations, pas des décisions approuvées. GovCheck doit distinguer les faits observés, les faits déclarés par l'utilisateur, les hypothèses inférées, les inconnues et les choix de gouvernance approuvés. Il ne doit pas convertir silencieusement un flux de travail détecté, une règle de branche, un document ou une configuration d'outil en politique autorisée.

### 4.2 Ne poser initialement que les questions fondatrices

Le parcours initial doit établir ce qui est nécessaire pour fonctionner de manière sûre, sans obliger les utilisateurs à parcourir tous les sujets de gouvernance possibles. Selon le contexte, les questions fondatrices comprennent :

- Qui établit la gouvernance initiale et de quelle autorité dispose cette personne ou instance ?
- Quel est le dépôt gouverné, quelle est sa finalité et dans quel contexte sera-t-il exploité ?
- Qui peut proposer, approuver, examiner ou révoquer les décisions de gouvernance ?
- Quelle frontière initiale d'acceptation des changements doit être protégée ?
- Quels enregistrements, éléments de provenance et preuves minimaux sont requis ?
- Quelles décisions peuvent être différées et quelles opérations doivent rester bloquées tant qu'elles ne sont pas prises ?

Le questionnaire initial exact, ses champs obligatoires et la machine à états du bootstrap restent à concevoir. Une question sans réponse doit rester explicitement sans réponse ; elle ne doit pas recevoir une valeur permissive par défaut.

### 4.3 Décisions progressives déclenchées par les événements

Le modèle de gouvernance doit s'enrichir à mesure que le dépôt et l'organisation évoluent. De nouvelles décisions peuvent être déclenchées, par exemple, par :

- une nouvelle exigence, affirmation, propriété, composant ou domaine ;
- une évolution de l'architecture, du déploiement, de la sensibilité des données ou du contexte de menace ;
- une dépendance, intégration ou interface externe proposée ;
- une lacune d'assurance, un échec, un incident ou une observation contradictoire ;
- une évolution du droit, d'un contrat, d'un standard ou de la publication d'une source applicable ;
- une modification de la structure d'équipe, des autorités, délégations ou responsabilités ;
- une évolution d'une méthode d'assurance, d'un outil de vérification ou de la base de confiance ;
- une opération bloquée parce qu'une décision ou une preuve requise manque.

GovCheck doit identifier les décisions concernées, expliquer pourquoi elles sont nécessaires et demander uniquement celles qui sont pertinentes dans le contexte présent. Il ne doit pas redemander continuellement des décisions déjà couvertes par des règles valides, applicables et approuvées. Il ne doit pas non plus inférer silencieusement une nouvelle décision à partir de comportements passés.

Une décision peut être différée, mais le modèle doit représenter son état, son propriétaire ou autorité, son déclencheur ou sa condition de réexamen, ainsi que les opérations bloquées tant qu'elle reste non résolue.

## 5. L'autorité de décision est distribuée par domaine et catégorie de décision

L'autorité n'est pas nécessairement concentrée chez un mainteneur ou dans un rôle unique. Un dépôt peut déléguer différentes catégories de décisions aux mainteneurs, à l'architecture, à l'assurance qualité, à la sécurité, à l'exploitation, aux responsables produit, à un comité ou à des personnes nommément désignées.

Par exemple, une autorité d'assurance qualité peut décider quelles propriétés exigent des tests empiriques, du model checking, de la vérification de programme, une preuve formelle ou une combinaison de méthodes. Les développeurs peuvent proposer et réaliser les changements et fournir les éléments d'évidence, sans pouvoir affaiblir unilatéralement ces exigences d'assurance. Lorsqu'un changement est soumis, GovCheck l'évalue au regard des décisions QA actuellement applicables.

Le modèle de gouvernance doit pouvoir exprimer au minimum :

- l'objet, le domaine et la catégorie d'une décision ;
- le détenteur de l'autorité (personne, rôle, équipe, comité ou organisation) ;
- les pouvoirs exacts accordés et leurs limites ;
- le périmètre, les conditions et la période d'effet de l'autorité ;
- les délégations et sous-délégations, y compris l'autorisation éventuelle de déléguer à nouveau ;
- les responsabilités de proposition, examen, approbation, rejet, révocation et recours ;
- les contraintes de séparation des tâches et de conflits d'intérêts ;
- le quorum, l'indépendance ou les approbations multiples éventuellement requis ;
- les règles de succession, d'indisponibilité et de révocation d'autorité ;
- la provenance et les éléments démontrant qu'un acteur était habilité au moment de la décision.

L'autorité est une donnée sémantique de gouvernance, pas simplement une permission GitHub, un paramètre de protection de branche, une appartenance à un compte ou une capacité d'agent. Les contrôles de forge peuvent appliquer certaines parties d'une décision, mais ne définissent pas son autorité normative. Un délégataire ne peut pas accorder des pouvoirs qu'il ne possède pas ; une décision ne peut pas être acceptée au seul motif qu'une intégration annonce un succès.

## 6. Les sources et l'aide à la décision contextualisée sont des capacités du produit

### 6.1 Présenter les sources lorsqu'elles sont pertinentes

Le travail de référence de GovCheck n'est pas uniquement une bibliographie interne de conception. Le produit doit pouvoir présenter aux utilisateurs les connaissances et sources pertinentes dans le contexte de la décision examinée.

Les catégories possibles comprennent les standards, lois et règlements, contrats, publications académiques, recommandations gouvernementales, spécifications industrielles, documentations officielles d'outils, dossiers du projet, observations opérationnelles/incidents et éléments d'évidence propres au dépôt. Leur autorité et leur applicabilité diffèrent ; elles ne doivent pas être aplaties dans une liste indifférenciée de citations.

Une vue d'aide à la décision doit exposer, lorsque pertinent :

- la question et la catégorie de décision ;
- les faits, affirmations, exigences et propriétés du dépôt concernés ;
- les passages de sources pertinents et leurs identifiants/révisions stables ;
- le type de source, l'organisme émetteur, la publication/version/date et l'applicabilité ;
- le caractère normatif, contractuel, consultatif, empirique, académique ou simplement informatif ;
- les affirmations ou critères étayés par chaque source et les limites de cet appui ;
- les contradictions, publications remplacées, incertitudes et sources manquantes ;
- les décisions existantes du dépôt et les précédents comparables ;
- les alternatives, conséquences, coûts, hypothèses et incertitudes résiduelles.

Les sources éclairent une décision ; elles ne prennent pas automatiquement la décision et ne confèrent pas d'autorité. L'inscription dans un catalogue ne signifie ni adoption, ni applicabilité, ni preuve de conformité.

### 6.2 Préserver la chaîne de raisonnement dans les deux sens

La traçabilité visée comprend, selon le cas :

`Source → affirmation / observation étayée → critère → recommandation / argument → décision → règle / exigence → propriété → méthode de vérification → preuve → évaluation / acceptation`

Chaque lien doit être explicite au point de distinguer un appui direct d'une interprétation ou d'une inférence. La navigation inverse est tout aussi importante : d'une source vers les décisions et règles qui s'appuient sur elle, et d'un contrôle en échec vers l'exigence, la décision, l'argument et les sources qui le fondent.

Le produit doit préserver l'identité de la source, sa version ou révision, les données de récupération/provenance, le passage ou localisateur pertinent, l'applicabilité, la classification de confiance et la fraîcheur. Une correction ou un remplacement de source doit rendre les décisions affectées identifiables pour réexamen ; il ne doit pas réécrire silencieusement les décisions historiques.

### 6.3 Plusieurs modes d'aide à la décision

GovCheck doit prendre en charge trois modes complémentaires :

1. **Guidage déterministe :** critères explicites, règles, questionnaires et arbres de décision dont la version et la justification sont gouvernées et testables.
2. **Délibération assistée par agent :** un agent reçoit le contexte de décision, la gouvernance applicable, les sources, critères, incertitudes et limites d'autorité ; il peut expliquer les alternatives, poser des questions, comparer les éléments d'évidence et préparer une proposition argumentée.
3. **Décision directe par un expert :** une personne habilitée peut examiner les éléments sous-jacents et enregistrer une décision sans suivre un assistant pas-à-pas ni utiliser un agent.

Un agent peut résumer des sources ou recommander une option, mais doit signaler les incertitudes et limites des sources. Il ne peut pas approuver une décision, sauf si une règle de gouvernance distincte et dûment autorisée lui confère explicitement ce pouvoir dans des conditions contrôlées. L'autorité humaine/organisationnelle reste l'autorité de décision par défaut.

Les arbres de décision et recommandations sont eux-mêmes des artefacts gouvernés : ils nécessitent une identité stable, un versionnement, une provenance des sources, une applicabilité, des limites et une validation. Un arbre de décision ne doit pas déguiser un jugement contestable en fait objectif.

## 7. L'assurance est choisie pour les affirmations et propriétés, pas selon une préférence d'outil ou un niveau de maturité

GovCheck doit partir de ce que le dépôt doit établir, et non d'un outil privilégié ou d'une échelle universelle d'assurance.

Pour chaque affirmation, exigence ou propriété, il doit aider à déterminer quelles méthodes sont adaptées, complémentaires ou insuffisantes. Les méthodes possibles comprennent les tests empiriques, les tests basés sur les propriétés/fuzzing, l'analyse statique, l'inspection, l'observation en fonctionnement, le model checking, la vérification de programme, la démonstration de théorèmes, la conformité implémentation/spécification et les arguments d'assurance structurés.

Pour chaque méthode candidate, il faut expliquer :

- ce qu'elle peut établir et ce qu'elle ne peut pas établir ;
- le sujet auquel le résultat s'applique (modèle, implémentation, processus, artefact ou système opérationnel) ;
- les hypothèses, bornes, environnement et base de confiance ;
- les limites d'exhaustivité et de couverture ;
- les compétences, outils, reproductibilité et coûts de maintenance requis ;
- les éléments d'évidence attendus et la manière dont ils peuvent devenir obsolètes ou être invalidés ;
- les lacunes résiduelles et méthodes complémentaires.

Les méthodes ne sont pas interchangeables. Un test est un témoignage empirique sur des cas exécutés, pas une preuve de théorème. Le model checking produit des résultats sur un modèle, une configuration, des bornes et des hypothèses déclarés ; il ne prouve pas automatiquement la correction de l'implémentation. Une dérivation formelle vérifiée est distincte d'un élément d'évidence de model checking. La vérification de programme et la conformité de l'implémentation nécessitent également leur propre périmètre et argument de confiance explicites. Un argument d'assurance structure les affirmations et les éléments d'évidence, mais ne rend pas vraies des prémisses non étayées.

Aucune méthode formelle n'est obligatoire du seul fait d'utiliser GovCheck, et aucune méthode formelle n'est catégoriquement supérieure pour toutes les affirmations. Un même dépôt peut employer des méthodes différentes pour différentes propriétés ou combiner plusieurs méthodes pour une propriété. La décision et sa justification relèvent de l'autorité affectée à la catégorie de décision concernée.

Une équipe d'assurance qualité constitue une autorité possible pour les exigences de méthodes d'assurance. Elle peut prescrire les éléments d'évidence attendus pour une catégorie de propriétés, indépendamment des développeurs qui réalisent les changements. GovCheck vérifie alors les changements soumis au regard de ces exigences ; il ne demande pas à chaque développeur de les renégocier.

## 8. Échec fermé par défaut ; l'assouplissement est une décision gouvernée explicite

### 8.1 Socle initial restrictif

Le modèle initial de gouvernance doit être aussi restrictif que raisonnablement nécessaire pour éviter toute autorisation implicite. Une information obligatoire absente, ambiguë, contradictoire, obsolète, non prise en charge ou invérifiable ne doit pas être interprétée comme une permission, une approbation, une satisfaction ou une assurance réussie.

Les sémantiques visées comprennent au minimum :

- une autorité non définie n'autorise aucune décision ;
- une approbation manquante ne vaut pas approbation ;
- une décision obligatoire non résolue reste non résolue et bloque les opérations qui en dépendent ;
- une preuve requise manquante ne satisfait pas l'exigence d'évidence ;
- un contrôle absent, en échec, partiel, obsolète ou non pris en charge n'est pas un succès ;
- une hypothèse non enregistrée ne peut pas soutenir silencieusement une affirmation ;
- une évaluation inconnue ou conflictuelle ne peut pas autoriser l'acceptation ;
- une délégation non déclarée ne confère aucun pouvoir ;
- une exception expirée, révoquée, hors périmètre ou liée à un état différent est invalide ;
- l'impossibilité d'effectuer un contrôle requis ne dispense pas à elle seule de l'exigence ;
- une recommandation, réponse d'agent, réussite CI ou permission de forge ne vaut pas approbation, sauf disposition explicite du modèle de gouvernance.

Les états inconnu, non évalué, non applicable, non exécuté, non pris en charge, incomplet, en échec, conflictuel et réussi doivent rester distincts. En particulier, l'absence de décision n'est pas une décision négative, et « non applicable » n'est pas synonyme de satisfait.

### 8.2 Ne bloquer que le périmètre dépendant

L'échec fermé ne signifie pas geler indistinctement tout un dépôt. Une décision manquante ou une exigence non satisfaite doit bloquer l'opération, la transition, l'artefact ou la livraison qui en dépend. Les travaux sans lien de dépendance peuvent continuer lorsque le modèle de gouvernance établit explicitement qu'ils sont indépendants et sûrs.

L'analyse des dépendances et des impacts doit être explicite. Si GovCheck ne peut pas établir qu'une opération est hors du périmètre bloqué, l'incertitude ne doit pas servir à contourner le blocage.

### 8.3 L'assouplissement est une décision gouvernée, jamais un raccourci « ignorer »

Lorsqu'un blocage intervient, GovCheck doit identifier la règle/exigence bloquante, la décision dont elle découle, le périmètre affecté, l'autorité compétente, la condition manquante ou en échec et les conséquences de l'assouplissement. L'autorité peut maintenir le blocage, demander davantage d'éléments d'évidence, accorder une exception bornée, accepter un risque résiduel, exiger des mesures compensatoires, modifier prospectivement la politique ou changer la stratégie d'assurance.

Au moins quatre mécanismes sémantiquement distincts sont nécessaires :

- **Dérogation (waiver) :** exception limitée à une exigence normalement applicable, si cette exigence est dérogeable.
- **Acceptation de risque :** acceptation explicite par le responsable du risque habilité d'un risque résiduel décrit ; cela ne transforme pas une preuve en échec en preuve réussie.
- **Modification de politique :** changement prospectif de la règle générale par l'autorité compétente pour la modifier.
- **Mesure compensatoire :** contrôle alternatif pouvant satisfaire un objectif par un autre mécanisme, avec sa propre évaluation d'adéquation.

Ces mécanismes ne sont pas interchangeables. Remplacer, par exemple, une exigence de preuve par des tests modifie la base d'assurance et laisse d'autres limites ; cela ne doit pas être présenté comme une preuve équivalente.

Tout assouplissement doit enregistrer l'autorité et le fondement de son habilitation, le motif, les exigences/règles exactes, le périmètre du dépôt et des artefacts, la période de validité ou le déclencheur de réexamen, les risques et conséquences, les alternatives étudiées, les sources/arguments d'appui, les mesures compensatoires, les lacunes résiduelles, les approbations requises et les conditions de révocation/expiration. Un assouplissement ne peut dépasser le périmètre ou la durée de l'autorité et ne peut être généralisé silencieusement.

### 8.4 Préserver l'historique et les frontières d'autorité

Les assouplissements n'effacent ni les échecs antérieurs, ni les preuves, ni les décisions. Les modifications de politique sont prospectives, sauf si une règle distincte, explicite et valide en dispose autrement. Les exceptions expirées ou révoquées cessent d'autoriser les opérations futures. Les enregistrements historiques restent accessibles et peuvent nécessiter une requalification distincte.

Aucune personne ou aucun agent ne peut assouplir une exigence sans l'autorité correspondante. Une délégation ne peut dépasser les pouvoirs du délégant. Si l'autorité compétente est indisponible ou ne peut être établie, le comportement restrictif reste en vigueur. Les contraintes de séparation des tâches continuent de s'appliquer aux décisions de dérogation et de modification de politique.

## 9. L'évaluation des changements applique les décisions prises par les autorités compétentes

Un changement proposé est évalué au regard de la révision de gouvernance et des décisions applicables à son contexte exact. GovCheck doit :

1. identifier le changement candidat et les artefacts/propriétés du dépôt affectés ;
2. résoudre les exigences, règles, profils et décisions applicables ;
3. établir l'autorité, le périmètre, la validité et la provenance de ces décisions ;
4. déterminer les contrôles, éléments d'évidence, revues et approbations attendus ;
5. évaluer les éléments fournis au regard de la méthode spécifiée et du sujet/état exact ;
6. rapporter distinctement les états réussi, échec, indéterminé, conflit, non pris en charge et lacune d'évidence ;
7. appliquer le prédicat d'acceptation, y compris les exceptions valides et mesures compensatoires ;
8. identifier toute nouvelle décision qui doit être prise par une autorité compétente.

Les développeurs peuvent proposer des changements aux exigences ou à la stratégie d'assurance, mais ne peuvent pas les affaiblir simplement en modifiant le code, les tests, les documents générés ou la configuration CI. Les changements de gouvernance suivent le cycle de décision gouverné et sont eux-mêmes soumis à autorité, revue et traçabilité.

## 10. Carte des capacités produit

L'intention produit implique au minimum les capacités coopérantes suivantes :

| Capacité | Responsabilité |
|---|---|
| Modélisation de gouvernance | Exprimer les concepts de gouvernance, autorités, rôles, pouvoirs, périmètres, règles, obligations, interdictions, permissions et états du cycle de vie. |
| Découverte du dépôt | Inspecter l'état existant et distinguer observations, affirmations, hypothèses et décisions approuvées. |
| Constitution progressive | Poser des questions contextualisées et établir la gouvernance initiale sans imposer un questionnaire exhaustif au premier lancement. |
| Autorités et délégations | Résoudre qui peut proposer, décider, approuver, déléguer, révoquer ou accepter un risque pour chaque catégorie de décision. |
| Gestion des connaissances et sources | Cataloguer, qualifier, versionner, retrouver et contextualiser les sources et affirmations qui en dérivent. |
| Aide à la décision | Présenter critères, alternatives, arbres de décision, arguments, incertitudes et délibération assistée par agent. |
| Gestion des décisions | Enregistrer propositions, approbations, justifications, hypothèses, validité, réexamen, remplacement et provenance. |
| Gestion de l'assurance | Relier affirmations et propriétés aux méthodes adaptées, éléments d'évidence, hypothèses, limites et fraîcheur. |
| Validation des politiques et modèles | Détecter incohérence, incomplétude, conflit, composition dangereuse, délégation invalide et assouplissement dangereux. |
| Génération/conformité des projections | Générer ou vérifier le `AGENTS.md` propre au dépôt et les autres projections destinées aux humains/agents à partir de la gouvernance approuvée. |
| Conformité des changements | Évaluer les changements et appliquer la frontière d'acceptation au regard des décisions approuvées applicables. |
| Gouvernance des exceptions et risques | Gérer dérogations, acceptations de risque, modifications de politique, mesures compensatoires, expiration et révocation. |
| Historique et audit | Préserver la provenance des décisions et éléments d'évidence et reconstruire le raisonnement ayant conduit à un résultat. |

Il s'agit de responsabilités conceptuelles, pas d'un engagement envers un monolithe, une topologie de services, une structure de commandes ou une architecture de plugins.

## 11. Frontières de confiance et d'autorité

- Le modèle canonique de gouvernance approuvé et versionné du dépôt reste son unique autorité normative, interprétée selon des sémantiques/un évaluateur explicitement identifiés.
- Le métamodèle du produit GovCheck définit ce qui peut être représenté ; il ne choisit pas lui-même toute la politique de chaque dépôt.
- Les mainteneurs et autorités déléguées du dépôt prennent les décisions propres à celui-ci dans les limites de leurs pouvoirs enregistrés.
- Les sources éclairent les décisions, mais ne confèrent pas elles-mêmes l'autorité et ne prouvent pas l'applicabilité.
- Les agents peuvent aider à découvrir, expliquer et proposer ; ils ne peuvent pas approuver ou assouplir silencieusement une politique.
- VCS, forge, CI et résultats de l'exécutable local sont des éléments d'évidence ou des mécanismes d'application dans des frontières de confiance déclarées, pas des substituts à l'autorité normative.
- Les documents lisibles par les humains et les instructions pour agents sont des projections contrôlées ou des explications. Ils ne créent pas de politique concurrente.
- GovCheck ne doit pas revendiquer une implémentation, une application, une preuve ou une conformité qui n'a pas été démontrée pour le périmètre et l'état exacts.

## 12. Relations avec la conception GovCheck existante

Cette intention s'appuie sur les éléments suivants et impose une analyse systématique de leurs impacts :

- ADR 0001 — frontières du bootstrap et gouvernance centrée sur le dépôt ;
- ADR 0003 — package produit versus historique méta propre à GovCheck ;
- Architecture 0012 — autorité normative canonique et conformité documentaire ;
- Architecture 0013 — métamodèle de gouvernance ;
- Architecture 0014 — flux de développement gouverné et responsabilités des acteurs ;
- Architecture 0015 — outil de conformité et plan de validation ;
- Architecture 0018 — gouvernance des versions et autorité d'approbation ;
- Architecture 0021 — affirmations, arguments et fraîcheur des éléments d'évidence ;
- Architecture 0022 — audit des capacités de gouvernance ;
- Architecture 0023 — autorité initiale du bootstrap ;
- Architecture 0024 — bootstrap de projet, choix de gouvernance et profils d'assurance ;
- Architectures 0025–0027 — observations du cycle de vie, capacité SACM, sémantiques métier et modèles de décision ;
- Spécification 0002 — modèle canonique de gouvernance ;
- Spécification 0003 — cycle de vie des changements ;
- Spécification 0005 — modèle d'assurance ;
- Spécification 0006 — applicabilité des révisions de gouvernance ;
- modèles formels du cycle de vie, de l'applicabilité, de la publication, de l'évaluation, des exceptions, des révocations et du journal ;
- catalogue de références et intégrité bidirectionnelle des citations/renvois ;
- bootstrapper du package, modèles, manifestes, projections générées, CI et contrôles de conformité.

Cette liste est un inventaire initial d'impacts, pas l'affirmation que chaque artefact cité est incohérent ou doit être réécrit. Les sémantiques existantes utiles doivent être conservées lorsqu'elles sont compatibles. Les conflits, omissions et concepts dupliqués doivent être identifiés explicitement avant l'implémentation.

## 13. Travaux à venir

Les travaux doivent avancer par étapes contrôlées :

1. **Capture et rapprochement :** conserver cette intention comme document de conception de premier rang et relier chaque affirmation aux décisions, spécifications, architectures, références, issues et codes existants.
2. **Analyse d'impact :** classer les éléments existants comme compatibles, complémentaires, incomplets, conflictuels, remplacés ou nécessitant une décision. Identifier les concepts dupliqués ou manquants et les dérives entre versions anglaise et française.
3. **Modèle conceptuel :** spécifier catégories de décisions, autorités/délégations, sources contextualisées, artefacts d'aide à la décision, questions progressives, choix d'assurance, sémantiques d'échec fermé, blocages ciblés et mécanismes d'assouplissement.
4. **Autorité et sémantiques :** identifier les sujets déjà décidés par le propriétaire, ceux qui sont des propositions de conception et ceux qui nécessitent encore une décision explicite. Ne pas déduire une adoption de ce document d'intention.
5. **Formalisation :** définir les propriétés de sûreté et sémantiques de transition ; sélectionner les méthodes de vérification selon les affirmations et abstractions, sans rendre un outil formel particulier obligatoire pour tous les utilisateurs.
6. **Évolution de l'architecture et des spécifications :** mettre à jour ou remplacer les documents existants avec une justification traçable et des versions bilingues ; conserver le catalogue central unique et l'intégralité des renvois réciproques.
7. **Planification de l'implémentation :** une fois le modèle rapproché, décomposer le travail en issues atomiques et changements respectant les dépendances, puis implémenter par incréments révisables avec éléments d'évidence.

La conception du package/bootstrap et de la génération d'`AGENTS.md` ne doit pas être implémentée isolément avant que ces sémantiques soient comprises.

## 14. Non-objectifs explicites et choix ouverts

Cette intention ne sélectionne pas :

- une sérialisation canonique, une technologie de schéma, un langage d'expression ou un moteur de politiques ;
- un assistant de preuve, model checker ou démonstrateur de théorèmes particulier comme dépendance obligatoire de GovCheck ;
- un framework d'interface interactive, un harnais d'agent, un serveur MCP, un service hébergé ou une autorité distante ;
- un nombre fixe de rôles de gouvernance ou de domaines de décision ;
- un score universel d'assurance ou un niveau de maturité ;
- un arbre de décision universel pour tous les domaines ;
- une politique universelle par défaut pour `AGENTS.md` ;
- l'hypothèse que chaque dépôt nécessite toutes les capacités métier ou toutes les méthodes d'assurance.

Ces sujets nécessitent une conception distincte fondée sur des éléments d'évidence et, lorsqu'ils sont normatifs, des décisions explicites de l'autorité compétente.

## 15. Invariants produit fondateurs à formaliser

Les énoncés suivants sont des propositions d'invariants pour l'analyse d'impact et la formalisation ultérieure. Leur présence consigne une intention ; elle ne signifie pas qu'ils ont déjà été adoptés dans le modèle canonique exécutable ou vérifiés.

1. **Autorité normative unique du dépôt :** aucune projection, aucun agent, aucune configuration CI ni aucun catalogue de sources ne devient silencieusement une autorité de politique concurrente.
2. **Décision liée à l'autorité :** toute décision normative est attribuable à une autorité compétente pour sa catégorie, son périmètre et sa période.
3. **Aucune permission implicite :** absence, ambiguïté, inconnue, échec ou impossibilité ne sont jamais interprétés silencieusement comme permission ou approbation.
4. **Acceptation en échec fermé :** les conditions obligatoires non résolues, conflictuelles, non prises en charge ou non satisfaites ne peuvent conduire à l'acceptation.
5. **Blocage ciblé :** un blocage s'applique à toutes les opérations dépendantes et à aucune opération indépendante, sauf si la dépendance ne peut être exclue de manière sûre.
6. **Assouplissement explicite :** tout assouplissement est une décision valide, traçable, prise par une autorité compétente et bornée par un périmètre, une durée et des conditions.
7. **Aucune escalade d'autorité :** délégations et pouvoirs d'exception ne peuvent dépasser l'autorité qui les accorde.
8. **L'évidence n'est pas la décision :** éléments d'évidence, recommandations, résultats de tests, de model checking, de preuve et décisions d'acceptation restent des types d'enregistrements et des significations distincts.
9. **Non-substituabilité des méthodes :** les méthodes d'assurance conservent leurs sémantiques, hypothèses et limites propres ; une substitution exige une décision explicite et consigne le changement de base d'assurance.
10. **Provenance des sources :** les recommandations et décisions dérivées de sources conservent identité, révision, applicabilité et liens de raisonnement vers ces sources.
11. **Aucune adoption silencieuse :** une recommandation, un modèle, une configuration découverte ou ce document d'intention ne devient pas une politique approuvée sans la décision requise.
12. **Préservation de l'historique :** modifications de politique, dérogations, révocations et requalifications préservent les décisions et éléments d'évidence antérieurs au lieu de réécrire l'historique.
13. **Constitution progressive :** les décisions non résolues restent explicites ; les nouvelles décisions sont demandées lorsqu'elles deviennent pertinentes, tandis que les décisions existantes valides sont réutilisées dans leur périmètre.
14. **Fidélité des projections :** les documents destinés aux humains/agents, générés ou contrôlés, reflètent fidèlement les règles approuvées et ne peuvent ajouter, supprimer ou affaiblir leur contenu normatif.

## 16. Statut et interprétation

Ce document est une déclaration détaillée de l'intention produit et une base de refonte architecturale. Il n'est pas en lui-même un ADR, une politique normative du dépôt, un plan d'implémentation approuvé ou une preuve qu'une capacité existe. Le processus d'autorité de gouvernance actuel reste applicable. Dans l'organisation actuelle du projet, seul le propriétaire du dépôt peut approuver les évolutions de son orientation normative.

Tout changement futur dérivé de cette intention doit préserver la distinction entre décisions du propriétaire, propositions de conception, recommandations, affirmations issues de sources externes, résultats de modèles formels et comportements effectivement implémentés.

## Analyse d'impact

Voir l'[analyse d'impact de l'intention produit](product-intent-impact-analysis.fr.md) ([English](product-intent-impact-analysis.md)) pour la première réconciliation de cette intention avec les ADR, architectures, spécifications et frontières produit existants. Il s'agit d'un audit de travail, pas d'un acte d'adoption.
