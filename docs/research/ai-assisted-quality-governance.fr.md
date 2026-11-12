# Qualité logicielle assistée par IA, maintenabilité et gouvernance de l'ingénierie : revue de recherche

**Statut :** dossier non normatif soumis à la revue du responsable du dépôt. Aucune architecture, exigence, métrique, méthode ou outil n'est adopté.
**Préparé le :** 2026-11-11.

## Sources fournies pour examen

- [AI-Friendly Code: The Missing Link for Speed with Quality — Adam Tornhill, GOTO Copenhagen 2026](https://youtu.be/ciRTdOIhNCc) — [R-157](../references.fr.md#r-157).
- [Vidéo d'identifiant hP2vfBcQhfk](https://youtu.be/hP2vfBcQhfk) — métadonnées/contenu non vérifiés indépendamment ; conservée en [R-160](../references.fr.md#r-160).
- [How to Use Test-Driven Development with AI Agents — Emily Bache / Modern Software Engineering](https://youtu.be/a6HYpocKwXU) — [R-158](../references.fr.md#r-158).
- [Vidéo d'identifiant cZ_PqBpZygY](https://youtu.be/cZ_PqBpZygY) — métadonnées/contenu non vérifiés indépendamment ; conservée en [R-161](../references.fr.md#r-161).
- [What the Top Companies Do Differently With AI Coding — Martin Harrysson et Prakhar Dixit, McKinsey / AI Engineer](https://youtu.be/21tuT-e4NVo) — [R-159](../references.fr.md#r-159).

**Travaux GovCheck liés :** [#73](https://github.com/Martin-PB/govcheck/issues/73) contrats formels ; [#74](https://github.com/Martin-PB/govcheck/issues/74) provenance ; [#79](https://github.com/Martin-PB/govcheck/issues/79) évaluation et assurance ; [#81](https://github.com/Martin-PB/govcheck/issues/81) cycle de vie formel ; [#83](https://github.com/Martin-PB/govcheck/issues/83) état de l'art ; [#84](https://github.com/Martin-PB/govcheck/issues/84) collaboration multi-agents et attribution ; [#86](https://github.com/Martin-PB/govcheck/issues/86) applicabilité des évaluations aux révisions.

## 1. Évaluation synthétique

La question commune est de savoir comment augmenter le débit de changements assistés par IA sans confondre code généré, correction, maintenabilité, satisfaction des exigences et acceptation justifiée.

La piste principale pour GovCheck est une chaîne auditable : **intention et exemples des parties prenantes → exigences/spécification → changement d'implémentation → éléments de vérification → argument d'assurance → décision autorisée → observations après livraison et réévaluation**. Cette chaîne doit préserver les distinctions entre tests, analyse statique, model checking, preuve de théorème, revue humaine et acceptation d'un risque résiduel.

**Recommandation provisoire :** auditer le métamodèle, le modèle d'assurance, le cycle de vie, l'applicabilité aux révisions et l'attribution avant de proposer des changements. Les pistes incluent les affirmations de qualité dépendantes du contexte, les oracles de test/acceptation explicites et leur indépendance, la fraîcheur des preuves, la maintenabilité longitudinale et la responsabilité organisationnelle. Ce dossier ne démontre pas que ces capacités sont absentes. Aucun seuil CodeHealth, workflow TDD, méthode EXACT, schéma de sous-agents, produit fournisseur ou modèle organisationnel n'est proposé comme obligatoire.

## 2. Méthode et limites

Cette revue ciblée n'est pas systématique. Les études évaluées par les pairs étayent des conclusions bornées par leurs méthodes et jeux de données ; les expériences de praticiens fournissent des hypothèses utiles mais exigent l'examen des références, des oracles et de la reproductibilité ; les entretiens industriels décrivent des pratiques sans établir à eux seuls la causalité. Les métriques de fournisseurs sont des signaux, pas des définitions universelles de la qualité.

Les deux liens non résolus, R-160 et R-161, sont conservés sans attribution de contenu. Le dossier n'est pas exhaustif à leur égard tant que les titres et contenus n'ont pas été vérifiés directement.

## 3. Recherche académique

### 3.1 Santé du code et refactoring par IA

L'article FORGE 2026 de Borg, Hagatulah, Tornhill et Söderberg étudie le refactoring par IA sur 5 000 solutions Python de programmation compétitive. Il rapporte une association entre CodeHealth et la préservation sémantique mesurée par les suites de tests, avec des taux de rupture plus faibles pour plusieurs modèles de taille moyenne sur du code plus sain. Les effets dépendent du modèle et de la tâche ; certains écarts ne sont pas statistiquement significatifs. Voir [R-152](../references.fr.md#r-152).

Cela motive l'étude de la maintenabilité et de la compréhensibilité comme facteurs de risque/contexte, mais ne valide pas une métrique comme seuil universel d'acceptation. Le corpus, la tâche, la sélection des défauts et l'oracle sont circonscrits ; réussir les tests ne prouve pas l'équivalence au-delà des propriétés testées.

### 3.2 Données nuancées sur la maintenabilité ultérieure

L'étude préenregistrée *Echoes of AI* porte sur 151 participants, dont 95 % de développeurs professionnels. Dans sa tâche ultérieure randomisée, elle ne trouve pas de différence systématique claire de temps ou de qualité entre le code assisté par IA et le code sans IA dans le contexte étudié. Voir [R-153](../references.fr.md#r-153). Cela ne prouve pas l'absence de risque ; cela invite à ne pas présumer que l'assistance IA dégrade nécessairement la maintenabilité.

### 3.3 Contexte et provenance à grande échelle

Une étude préliminaire ESEM 2026 analyse plus de 10 000 développeurs et 400 000 diffs chez Meta. Elle suit le code suggéré par IA au travers des modifications, revues et intégrations et identifie des facteurs de confusion, dont la centralité du code, la taille du changement, les tests et l'ancienneté de l'auteur. Voir [R-154](../references.fr.md#r-154). Cela soutient l'explicitation du contexte et de la provenance, pas le transfert de seuils propres à une organisation.

### 3.4 Pull requests produites par des agents et revue humaine

Une étude de 567 PR produites avec Claude Code dans 157 dépôts open source rapporte que 83,8 % ont été fusionnées, tandis que 45,1 % des PR fusionnées ont nécessité d'autres changements. Voir [R-155](../references.fr.md#r-155).

GovCheck devrait distinguer producteur, révision soumise, modifications du réviseur, révision intégrée exacte et acceptation autorisée. Le taux de fusion n'est pas une mesure de correction ; l'auteur agentique ne confère aucune autorité décisionnelle.

## 4. Recherche de praticiens : exemples, TDD et rétroaction

Le compte rendu d'Emily Bache sur EXACT décrit l'example mapping collaboratif, une liste de tests en langage naturel, la boucle red/green/refactor, le TDD prédictif et des expériences avec un sous-agent dédié au refactoring. Le laboratoire utilise des katas et des suites d'acceptation cachées au modèle. Les auteurs rapportent des avantages dans leurs expériences, mais les résultats et coûts varient selon le modèle et le workflow. Voir [R-156](../references.fr.md#r-156) et [la vidéo R-158](../references.fr.md#r-158).

Séparation des responsabilités potentiellement utile :
1. Les parties prenantes clarifient l'intention par des exemples.
2. Les exigences et exemples d'acceptation sont explicités.
3. L'agent d'implémentation travaille dans une boucle de rétroaction contrôlée.
4. Les prédictions de test sont comparées aux résultats réels.
5. Un oracle d'acceptation non montré au générateur peut améliorer l'évaluation si son indépendance et sa couverture sont comprises.
6. Un agent de refactoring propose des changements, mais ne peut autoriser lui-même leur acceptation.

Ces résultats ne prouvent pas que TDD, example mapping ou agents multiples améliorent toujours la qualité. Les tests cachés ne vérifient que les propriétés qu'ils encodent ; ils ne remplacent ni l'analyse des exigences, ni l'évaluation des risques, ni la preuve, ni le model checking, ni la revue autorisée. La conférence [AI-Friendly Code](https://youtu.be/ciRTdOIhNCc) est enregistrée en [R-157](../references.fr.md#r-157) et doit être examinée avec, et non à la place de, l'article empirique.

## 5. Pratiques organisationnelles

L'entretien McKinsey « What the Top Companies Do Differently With AI Coding » est catalogué en [R-159](../references.fr.md#r-159). Il invite à examiner normes d'ingénierie, formation, sélection des tâches, boucles de rétroaction, capacité de revue, responsabilité et mesure des résultats. Comme entretien industriel, ses affirmations doivent être reliées aux données et méthodes sous-jacentes avant tout usage normatif.

DORA 2025, déjà catalogué en [R-148](../references.fr.md#r-148), fournit un contrepoint : l'IA tend à amplifier les forces et faiblesses existantes du système de livraison. L'évaluation pourrait considérer tâche, dépôt, équipe, workflow, pipeline d'intégration et résultats après livraison, en précisant l'entité visée par chaque affirmation. Ne pas assimiler la maturité au nombre d'agents, aux lignes générées, au débit de PR, au taux de fusion ou à un score unique.

## 6. Implications candidates à auditer dans GovCheck

| Sujet | Capacité à rechercher | Travaux existants à auditer |
|---|---|---|
| Chaîne intention-preuve | Tracer intention, objectifs, exigences, exemples, spécifications, implémentation, vérification, argument et décision sans confondre leurs types | #73 ; Architecture 0013 ; Spécification 0005 |
| Oracle de test | Enregistrer provenance, périmètre, couverture, indépendance du générateur et angles morts | #79 ; Spécification 0005 |
| Dimensions de qualité | Distinguer correction, maintenabilité, sécurité, fiabilité, complexité, performance et évolutivité | #73 ; #79 |
| Contexte/provenance | Enregistrer tâche, dépôt/révision, dépendances, version modèle/outil, contributions agent/humain et configuration | #74 ; #84 ; #86 |
| Applicabilité des preuves | Lier les preuves aux révisions exactes/dépendances ; définir quand elles deviennent périmées ou partiellement applicables | #69 ; #79 ; #81 ; #86 |
| Qualité longitudinale | Relier les contrôles aux défauts, incidents, reprises, maintenance et réévaluations ultérieurs | #79 ; #81 ; #83 |
| Workflow agentique | Traiter attribution et collaboration comme provenance, jamais comme autorisation | #58 ; #59 ; #84 |
| Affirmations organisationnelles | Déclarer population, contexte, référence, mesures, incertitude et décideur | #79 ; #83 |
| Autorité d'acceptation | Séparer contrôles réussis, auto-évaluation, mécanismes de fusion, revue humaine et décision autorisée | Architecture 0023 ; #73 ; #84 |

Relier chaque piste à des définitions, règles, modèles et tests précis ; la classer comme **couverte, partiellement couverte, absente, contradictoire ou non implémentée**. L'absence d'une mention dans un document ne prouve pas à elle seule une lacune du métamodèle.

## 7. Distinctions d'assurance à préserver

- **Résultat de test :** comportement observé sur un jeu de tests et un environnement spécifiés ; élément probant dans ce périmètre, pas preuve de tout comportement.
- **Analyse statique :** résultat d'un outil selon son modèle/configuration ; périmètre et faux positifs/faux négatifs comptent.
- **Model checking :** exploration d'un système de transitions/configuration déclaré, bornée par le modèle et l'espace d'états exploré.
- **Preuve de théorème :** dérivation vérifiée relativement à des définitions et un noyau/vérificateur de confiance ; elle établit uniquement l'énoncé formel prouvé.
- **Revue/attestation humaine :** affirmation attribuable dans un processus déclaré, pas automatiquement indépendante ou infaillible.
- **Argument d'assurance :** raisonnement reliant affirmations, preuves, hypothèses et réfutations ; sa qualité dépend de la pertinence de l'argument.
- **Risque accepté/décision :** acte de gouvernance autorisé, pas preuve technique du seul fait de l'approbation.

Example mapping, TDD et tests d'acceptation cachés peuvent clarifier la spécification et l'évaluation sans effacer ces distinctions épistémiques.

## 8. Scénarios adversariaux pour une vérification future

Non implémentés ni exécutés dans cette PR de recherche ; à rapprocher des travaux existants avant d'ajouter des fixtures.

- **AQ-01 — Oracle vert mais incorrect :** les tests visibles passent mais omettent une exigence ou encodent le mauvais comportement.
- **AQ-02 — Couplage générateur/oracle :** le même agent produit implémentation et tests à partir d'une interprétation erronée commune.
- **AQ-03 — Surinterprétation de tests cachés :** une suite indépendante détecte des défauts puis est présentée à tort comme preuve de correction totale.
- **AQ-04 — Substitution de métrique :** un seuil CodeHealth/complexité devient une prétendue preuve de correction ou de sécurité.
- **AQ-05 — Confusion de contexte :** les résultats sont attribués à l'IA sans tenir compte de la difficulté, centralité, expérience, sélection de revue ou taille du changement.
- **AQ-06 — Preuve périmée :** un résultat antérieur est réutilisé après un changement pertinent de dépendance, hypothèse, politique ou implémentation.
- **AQ-07 — Auto-acceptation du refactoring :** un agent accepte son propre résultat sans contrôles indépendants ou autorité requis.
- **AQ-08 — PR modifiée par le réviseur :** provenance et preuves pointent vers le commit initial plutôt que la révision intégrée.
- **AQ-09 — Gain immédiat, régression durable :** le temps d'implémentation baisse mais maintenance, reprises ou résultats opérationnels ne sont pas mesurés.
- **AQ-10 — Généralisation organisationnelle abusive :** une étude de cas devient règle universelle sans population, référence, incertitude ni limites d'applicabilité.

Le comportement attendu est de préserver type d'affirmation, périmètre, provenance, incertitude et autorité. Un test positif ne doit pas devenir silencieusement une preuve ; une approbation valide ne doit pas être présentée comme preuve technique.

## 9. Étapes proposées pour revue

1. Auditer la chaîne intention/exigences/assurance, le cycle de vie, l'applicabilité aux révisions et l'attribution avant d'ajouter des concepts.
2. Relier exemples et spécifications de test aux exigences et affirmations ; vérifier si oracle et producteur de preuves sont représentés séparément.
3. Vérifier si dimensions de qualité et contexte sont exprimables sans métrique propriétaire ou cadre organisationnel unique.
4. Vérifier si les règles d'invalidation couvrent les changements pertinents de révision, outil, dépendance, hypothèse et environnement.
5. Réutiliser #73, #74, #79, #81, #83, #84 et #86 ; ne pas créer d'epic en doublon.
6. Examiner directement R-160 et R-161 et actualiser leurs entrées si leurs métadonnées/contenus deviennent accessibles.
7. Si l'audit démontre une lacune réelle, proposer une modification limitée et explicite ainsi que des fixtures adversariales. Garder le dossier non normatif jusqu'à adoption par le responsable autorisé.

## 10. Recommandation

**La recherche justifie un audit, pas une refonte immédiate du métamodèle.** La question centrale est de savoir si GovCheck peut exprimer une chaîne d'assurance complète, précise sur le plan épistémique et sensible aux révisions, de l'intention et des exemples jusqu'à l'acceptation autorisée et aux retours ultérieurs.

Les métriques de santé du code, le TDD, l'example mapping, le refactoring agentique, les suites de tests cachées et les pratiques organisationnelles sont des techniques dont les affirmations doivent être évaluées dans leur contexte. Aucune ne devrait devenir obligatoire simplement parce qu'elle figure dans une vidéo ou une étude. GovCheck devrait pouvoir les représenter lorsqu'un dépôt les choisit et enregistrer leurs hypothèses, preuves et limites.

## 11. Traçabilité

Nouvelles entrées : [R-152](../references.fr.md#r-152), [R-153](../references.fr.md#r-153), [R-154](../references.fr.md#r-154), [R-155](../references.fr.md#r-155), [R-156](../references.fr.md#r-156), [R-157](../references.fr.md#r-157), [R-158](../references.fr.md#r-158), [R-159](../references.fr.md#r-159), [R-160](../references.fr.md#r-160), [R-161](../references.fr.md#r-161). Référence existante : [R-148 — DORA 2025](../references.fr.md#r-148). Issues liées : #73, #74, #79, #81, #83, #84, #86.