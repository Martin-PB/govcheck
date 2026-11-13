# Changements concurrents d'agents et gouvernance des dépôts : état de la recherche

**Statut :** dossier de recherche non normatif soumis à revue. Aucune architecture, politique, workflow ou outil n'est adopté ici.
**Préparé le :** 2026-11-11.
**Déclencheur :** Patrick Debois et Tessl, « Your Team's Agents Are All Shipping to the Same Code at Once » : https://youtu.be/fTUinMqA1XQ
**Travaux liés :** [collaboration multi-agents et attribution #84](https://github.com/Martin-PB/govcheck/issues/84), [contrats sémantiques et métamodèle #73](https://github.com/Martin-PB/govcheck/issues/73), [provenance des références #74](https://github.com/Martin-PB/govcheck/issues/74), [évaluation et assurance #79](https://github.com/Martin-PB/govcheck/issues/79), [modèles formels et cycle de vie #81](https://github.com/Martin-PB/govcheck/issues/81).

## 1. Évaluation exécutive

La vidéo est un déclencheur utile pour la recherche, mais ne suffit pas à justifier à elle seule une modification de GovCheck. Son problème central — plusieurs agents effectuant des changements simultanés — rejoint les recherches sur les modifications concurrentes, les conflits de fusion, les interférences sémantiques, les files de fusion, la provenance et les effets du développement assisté par IA.

**Conclusion provisoire :** GovCheck devrait pouvoir représenter et évaluer le travail concurrent, les interactions entre changements, le périmètre et l'actualité des résultats de vérification, ainsi que l'autorité nécessaire à l'intégration. Avant de modifier le métamodèle, il faut auditer si le cycle de vie, l'applicabilité des révisions, l'assurance, la provenance et les contrats VCS existants couvrent déjà ces préoccupations. Ce rapport identifie des lacunes candidates, pas des défauts d'implémentation confirmés.

Le problème ne se limite pas aux agents : il existe aussi avec les équipes humaines, la refactorisation automatisée, les branches de publication, les mises à jour de dépendances, le code généré et les systèmes indépendants. Le modèle canonique ne doit présupposer aucun harness d'agents, forge, VCS, file de fusion ou fournisseur CI particulier.

## 2. Méthode et limites de la recherche

Il s'agit d'une revue ciblée fondée sur les sources, pas d'une revue systématique enregistrée. Elle privilégie les articles évalués par les pairs et les documentations primaires officielles, précise la pertinence et les limites de chaque source et évite de traiter une fonctionnalité produit ou une association empirique comme une garantie universelle.

Thèmes : modifications concurrentes et qualité des fusions ; conflits sémantiques non révélés textuellement ; détection et résolution ; files de fusion et validation de changements combinés ; provenance et autorité dans le développement assisté par IA ; effets organisationnels de l'IA.

La couverture n'est pas exhaustive. Certaines études portent sur des langages, dépôts, organisations ou jeux de données précis ; leurs chiffres ne doivent pas être généralisés sans qualification. La documentation d'un fournisseur décrit le comportement prévu d'un produit, pas une preuve indépendante de sa configuration correcte ou de son adéquation.

## 3. Résultats académiques

### 3.1 Les modifications concurrentes sont un signal de gouvernance, pas seulement un conflit textuel

- **ConE — Concurrent Edit Detection Tool** étudie six grands dépôts Microsoft sur six mois et indique que les fichiers modifiés concurremment dans plusieurs pull requests sont plus susceptibles d'introduire des bogues. L'outil proposé détecte proactivement les chevauchements. Cela justifie d'enregistrer les travaux qui se chevauchent et de déclencher une revue ciblée ; cela ne signifie pas que tout chevauchement est un conflit ou qu'un détecteur prouve la correction. [DOI ACM/IEEE 10.1145/3478019](https://doi.org/10.1145/3478019).
- **An empirical investigation into merge conflicts and software quality** analyse 143 projets open source, 556 911 commits et 36 122 commits de fusion ; 19,32 % des fusions de l'échantillon produisent des conflits. L'étude rapporte une association plus forte avec les bogues pour le code impliqué dans des conflits sémantiques. Ces observations sont propres au jeu de données, pas un multiplicateur de risque universel. [PDF de l'article](https://ics.uci.edu/~iftekha/pdf/J4.pdf).
- **ConflictBench** construit un jeu de données de conflits de fusion Java et compare cinq outils, révélant les limites des outils actuels et des différences d'applicabilité. La réussite d'un outil doit rester distincte de la correction sémantique. [Journal of Systems and Software, 2024](https://www.sciencedirect.com/science/article/pii/S0164121224001298).
- **Lightweight Semantic Conflict Detection with Static Analysis** étudie les conflits sémantiques dynamiques pouvant subsister après une fusion textuelle réussie. L'évaluation rapporte F1 0,50 et exactitude 0,60 sur 99 unités expérimentales. Ces métriques modestes imposent de traiter le détecteur comme une source d'éléments probants faillible, non comme un arbitre faisant autorité. [ICSE Companion 2024, DOI 10.1145/3639478.3643118](https://doi.org/10.1145/3639478.3643118).
- **Predicting merge conflicts considering social and technical assets** étudie la prédiction des conflits à partir de facteurs sociaux et techniques, soulignant l'importance du contexte de coordination et de dépendance au-delà des lignes modifiées. [Empirical Software Engineering](https://link.springer.com/article/10.1007/s10664-023-10395-8).

### 3.2 La résolution automatique est une proposition, pas une acceptation

Les recherches sur la résolution par recherche et par synthèse montrent que certains motifs peuvent être traités automatiquement ou avec assistance, mais la couverture reste partielle et dépend des classes de conflits et des jeux d'évaluation.
- Paulino, « Towards a Feasible Evaluation Function for Search-Based Merge Conflict Resolution » (2026), analyse 9 998 fragments de conflit de 1 062 projets open source et évalue une approche sur un sous-ensemble. La similarité avec les versions antérieures est une heuristique, pas un critère de correction sémantique. [ACM TOSEM DOI 10.1145/3748256](https://doi.org/10.1145/3748256).
- Pan et al., « Can Program Synthesis be Used to Learn Merge Conflict Resolutions? An Empirical Analysis » (ICSE 2021), rapporte des résultats utiles pour une classe bornée de conflits C++ de Microsoft Edge. Cela ne justifie pas de faire confiance à toute résolution générée par un agent. [Microsoft Research](https://www.microsoft.com/en-us/research/publication/can-program-synthesis-be-used-to-learn-merge-conflict-resolutions-an-empirical-analysis/).

Conséquence pour GovCheck : conserver la provenance de la résolution, les entrées, l'outil/version, la révision produite, les contrôles, hypothèses et incertitudes résiduelles. L'algorithme de résolution ne doit pas s'octroyer l'autorité d'acceptation.

### 3.3 L'IA amplifie le système d'ingénierie environnant

La recherche DORA 2025 de Google s'appuie sur plus de 100 heures de travail qualitatif et près de 5 000 réponses de professionnels. Elle décrit l'IA comme un amplificateur des forces et faiblesses organisationnelles existantes : le nombre d'agents ou la vitesse de génération ne garantit pas une livraison fiable. [Rapport DORA 2025](https://dora.dev/research/2025/dora-report/) · [Google Research](https://research.google/pubs/dora-2025-state-of-ai-assisted-software-development-report/).

Une revue de littérature 2025 sur les systèmes multi-agents LLM pour l'ingénierie logicielle synthétise architectures collaboratives, bénéfices, limites et lacunes. Elle cartographie le domaine, mais ne prouve pas la fiabilité d'un workflow particulier. [ACM TOSEM DOI 10.1145/3712003](https://doi.org/10.1145/3712003).

## 4. Pratiques industrielles

### 4.1 Les files de fusion vérifient une révision combinée précise

La file de fusion GitHub crée des branches temporaires combinant une pull request avec la base courante et les changements précédemment en attente, puis exige des contrôles sur cet état combiné. Un contrôle sur une pull request isolée et un contrôle sur un groupe de fusion sont deux exécutions distinctes portant sur des révisions différentes. La file est propre à GitHub et ne doit pas devenir l'abstraction canonique de GovCheck. [GitHub : gestion d'une file de fusion](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-a-merge-queue).

Concept généralisable : un **candidat d'intégration** identifie l'état de base exact, l'ensemble ordonné des changements, la résolution et la configuration sur lesquels les contrôles ont été exécutés. L'assurance ne s'applique qu'à ce candidat et à ses hypothèses déclarées.

### 4.2 Les contrôles de concurrence relèvent de la politique opérationnelle

Une file peut limiter les builds concurrents, grouper les changements, optimiser le débit ou attendre les contrôles. Ces contrôles sont utiles, mais GovCheck doit représenter leurs contraintes et résultats sans imposer une file ou un ordonnancement particulier. Un dépôt peu actif peut intégrer directement ; un dépôt à fort débit peut utiliser une validation progressive ou spéculative.

### 4.3 La provenance est complémentaire, pas suffisante

GovCheck catalogue déjà in-toto et SLSA ([R-06](../references.fr.md#r-06)/[R-07](../references.fr.md#r-07)), et traite séparément identité des artefacts, révisions et actualité des éléments probants. Ces systèmes peuvent identifier comment un artefact a été produit ; ils ne prouvent pas à eux seuls qu'il satisfait l'intention du dépôt ou que l'acteur avait autorité pour l'accepter.

## 5. Conséquences candidates pour GovCheck

Ces éléments issus de la recherche sont à auditer, et non des exigences adoptées.

| Préoccupation | Représentation ou invariant candidat | Concepts existants à auditer d'abord |
|---|---|---|
| Coordination | Travail, périmètre, artefacts attendus, dépendances, provenance du producteur, état du cycle de vie | Portefeuille de travaux ; attribution #59 ; cycle de vie |
| Travail concurrent | Relation de chevauchement entre périmètres ou artefacts modifiés, pour une révision/heure déclarée | Contrats VCS ; cycle de vie des changements |
| Taxonomie des conflits | Conflits textuels, structurels, dépendance/build, comportement/sémantique, exigences/décisions et politiques ; limites des détecteurs | Relations de conflit/contradiction ; architecture 0013 |
| Candidat d'intégration | Révision de base exacte, changements ordonnés, résolution, configuration et chaîne d'outils | Identité/versionnement ; adaptateur VCS |
| Applicabilité de l'assurance | Révision du sujet, entrées, hypothèses, méthode, version d'outil, périmètre et statut exacts | Spécification 0005 ; applicabilité des révisions ; fraîcheur |
| Invalidation | Changement de dépendance, hypothèse, politique, base, résolution ou outil invalide les résultats concernés selon des règles explicites | GovCheckAssurance.tla ; GovCheckLifecycle.tla ; architectures 0021/0033 |
| Autorité d'acceptation | Autorisation d'intégration et acceptation du risque distinctes de l'auteur, de la mécanique de fusion, d'une CI verte ou d'une résolution automatique | Architecture 0023 ; modèles d'autorité/exception |
| Retour d'expérience | Observations en production déclenchant incident, affirmation, changement d'exigence, réévaluation ou remédiation | Références [R-70](../references.fr.md#r-70), [R-72](../references.fr.md#r-72), [R-75](../references.fr.md#r-75) et [R-76](../references.fr.md#r-76) |

### 5.1 La validité individuelle n'implique pas la validité combinée

Pour deux changements c1 et c2, la réussite de contrôles locaux ne prouve pas que leur composition satisfait un invariant partagé. GovCheck ne doit pas inférer :
- fusion textuelle possible ⇒ compatibilité sémantique ;
- build réussi ⇒ exigences satisfaites ;
- tests réussis ⇒ théorème prouvé ;
- conformité des changements isolés ⇒ conformité de leur combinaison ;
- file de fusion terminée ⇒ acceptation normative autorisée ;
- agent ou outil producteur ⇒ autorité de décision.

L'exemple d'unité monétaire de la vidéo est un bon cas adversarial : un changement modifie l'interprétation ou la représentation d'un montant, un autre modifie un consommateur ou un rapport. Chacun peut réussir ses tests isolés alors que la combinaison viole une exigence sémantique commune.

### 5.2 L'actualité des éléments probants dépend des révisions

Un enregistrement d'assurance doit identifier son sujet et ses dépendances pertinentes. Si la base, une dépendance, politique, hypothèse, mapping, résolution ou outil change, GovCheck doit déterminer quels résultats restent applicables et lesquels sont périmés. Il faut tester ce point contre les modèles temporels existants, pas créer un modèle parallèle sans lacune démontrée.

### 5.3 La détection stratifiée doit préserver l'incertitude

Une séquence pratique peut combiner détection VCS/textuelle ; contrôles structurels, de dépendances et de build ; tests et analyse statique ; contrats/invariants et model checking ; preuve formelle lorsqu'une spécification adaptée existe ; revue humaine et acceptation explicite des ambiguïtés/risques résiduels.

Ce n'est pas une échelle universelle de maturité et cela n'impose pas toutes les méthodes à chaque dépôt. La méthode requise dépend de l'affirmation, du risque et de la politique d'assurance déclarée. Les limites de faux positifs et faux négatifs doivent être conservées.

## 6. Scénarios adversariaux proposés

Ils pourraient devenir des fixtures des travaux de vérification existants ; ils ne sont ni implémentés ni exécutés à ce stade.

- **CC-01 — Unité sémantique incohérente :** deux changements passant isolément les tests utilisent des unités ou échelles monétaires différentes ; la combinaison viole un invariant.
- **CC-02 — Vérification périmée :** A est testé sur la base B ; C modifie une dépendance ou politique pertinente ; le résultat ancien de A est réutilisé à tort.
- **CC-03 — Dérive d'interface :** les contrats producteur et consommateur changent indépendamment, sans conflit textuel mais avec des significations incompatibles.
- **CC-04 — Décisions de politique concurrentes :** plusieurs travaux changent la même règle de manière incompatible ; la fusion ne tranche pas l'autorité normative.
- **CC-05 — Provenance de résolution automatique :** un résolveur modifie les fragments en conflit, mais la révision résultante n'enregistre ni son identité, ni ses entrées, ni les contrôles postérieurs.
- **CC-06 — Faux positif de chevauchement :** les changements touchent le même fichier mais des régions indépendantes ; le système bloque uniquement à cause du chevauchement.
- **CC-07 — Échec de détection :** aucun conflit textuel ou avertissement n'apparaît, mais le changement composé viole le comportement attendu.
- **CC-08 — Fusion verte non autorisée :** tous les contrôles réussissent, mais l'approbation ou l'autorité déléguée requise est absente/révoquée.
- **CC-09 — Workflow non-Git :** les changements sont coordonnés avec Pijul ou une forge par patches/email ; la sémantique ne dépend pas des identifiants de PR GitHub.
- **CC-10 — Retour de production :** une observation opérationnelle invalide une hypothèse/affirmation et déclenche analyse d'impact et réévaluation.

Résultat attendu : distinguer réussi/échoué/inconclusif/non pris en charge/périmé, préserver provenance et périmètre, sans transformer la détection en autorité ou l'élément probant en preuve.

## 7. Invariants candidats à formaliser

Ils exigent des définitions précises avant model checking ou preuve.

- **INV-CC-01 Périmètre :** chaque candidat d'intégration identifie état de base, changements constitutifs, résolution et configuration pertinente.
- **INV-CC-02 Pas d'assurance périmée :** l'acceptation ne s'appuie pas sur un résultat connu comme périmé selon les règles déclarées de dépendance/invalidation.
- **INV-CC-03 Composition :** l'acceptation exige une assurance applicable au candidat combiné, pas seulement à ses composants.
- **INV-CC-04 Autorité :** la mécanique de fusion ou résolution automatique ne remplace pas une autorisation requise et encore valide.
- **INV-CC-05 Pas de promotion épistémique :** fusion textuelle, build ou tests réussis ne deviennent pas silencieusement une preuve.
- **INV-CC-06 Provenance :** résolutions automatiques et contrôles identifient entrées pertinentes, producteur/outil et révision exacte.
- **INV-CC-07 Portabilité :** la sémantique canonique ne dépend pas d'identifiants ou de comportements propres à GitHub.
- **INV-CC-08 Pas de verrou universel :** le chevauchement est un signal à analyser, pas une preuve d'incompatibilité ni une raison universelle de bloquer.

TLA+/TLC peut convenir au cycle de vie, à la concurrence, à la révocation et à l'actualité dans des espaces d'états explicites. Lean ou un autre assistant de preuve peut convenir aux affirmations statiques de préservation sémantique lorsque les définitions sont précises. Tests et analyse statique fournissent des éléments probants bornés. Aucune méthode ne prouve tous les invariants ; le model checking reste limité au système modélisé et à la configuration explorée.

## 8. Prochaines étapes recommandées, sous réserve de revue

1. Auditer les Architectures 0013, 0014, 0021, 0022, 0023, 0028, 0032 et 0033 ; les Spécifications 0002, 0003, 0005 et 0006 ; et les modèles formels existants de cycle de vie/assurance.
2. Relier chaque invariant candidat aux concepts, règles, modèles et tests existants ; classer couvert, partiel, absent, contradictoire ou non implémenté, avec références exactes.
3. Réutiliser l'issue #84 et les enfants #58/#59 pour collaboration et attribution ; relier les contrats sémantiques à #73, l'actualité à #69/#79/#81, la provenance à #74/#83. Ne pas créer d'epic en doublon.
4. Seulement si l'audit démontre une lacune, proposer une modification limitée du modèle canonique ou un contrat de collaboration indépendant du VCS. Files, verrous, protocoles d'agents et fournisseurs CI restent des adaptateurs/politiques.
5. Ajouter les sources confirmées au catalogue bilingue avec identifiants stables et liens retour exacts. Valider les liens et backlinks sur la tête finale de PR.
6. Garder ce rapport non normatif. Toute adoption d'exigences, d'architecture ou d'outils demeure une décision distincte de l'autorité habilitée.

## 9. Recommandation

Traiter le travail concurrent d'agents comme un cas d'usage important pour tester l'adéquation du modèle générique de GovCheck, pas comme sa finalité exclusive. L'amélioration candidate la plus forte est une assurance sensible à la composition et aux révisions : quel changement combiné exact a été vérifié, selon quelles hypothèses et dépendances, et si l'autorité actuelle l'a accepté.

Ce rapport ne recommande aucun verrou, file de fusion, framework d'agents, forge, service CI, ontologie ou outil de preuve obligatoire.

## 10. Références et traçabilité

Les entrées proposées sont [R-142](../references.fr.md#r-142), [R-143](../references.fr.md#r-143), [R-144](../references.fr.md#r-144), [R-145](../references.fr.md#r-145), [R-146](../references.fr.md#r-146), [R-147](../references.fr.md#r-147), [R-148](../references.fr.md#r-148), [R-149](../references.fr.md#r-149), [R-150](../references.fr.md#r-150) et [R-151](../references.fr.md#r-151) du catalogue central. Documents liés : [Architecture 0013](../architecture/0013-governance-metamodel.fr.md), [Architecture 0021](../architecture/0021-assurance-claims-and-freshness.fr.md), [Architecture 0022](../architecture/0022-governance-capability-audit.fr.md), [Architecture 0023](../architecture/0023-bootstrap-governance-authority.fr.md), [Architecture 0028](../architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md), [Architecture 0033](../architecture/0033-governance-evaluator-exception-revocation-model.fr.md), [Spécification 0005](../specifications/0005-assurance-model.fr.md), et travaux [#84](https://github.com/Martin-PB/govcheck/issues/84), [#73](https://github.com/Martin-PB/govcheck/issues/73), [#74](https://github.com/Martin-PB/govcheck/issues/74), [#79](https://github.com/Martin-PB/govcheck/issues/79), [#81](https://github.com/Martin-PB/govcheck/issues/81).
