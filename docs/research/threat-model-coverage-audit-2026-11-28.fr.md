# Audit de couverture du modèle de menace — 2026-11-28

**Statut :** audit de couverture fondé sur les sources ; ce n'est ni un nouveau modèle de menace, ni une certification de sécurité, ni une décision d'adoption.  
**Cible de l'audit :** `main`, commit de fusion `451d1e1ff929946274edba8e844e08d74fdd306f`.  
**Travail parent :** [#70 — audit de couverture du modèle de menace](https://github.com/Martin-PB/govcheck/issues/70).  
**English:** [Threat-model coverage audit](threat-model-coverage-audit-2026-11-28.md).

## 1. Résultat exécutif

L'Architecture 0006 reste une base pertinente pour les menaces et les frontières de confiance. Ses catégories restent utiles, mais sa mention selon laquelle *aucun contrôle de sécurité n'est implémenté* n'est plus exacte pour décrire le dépôt : plusieurs prototypes bornés existent désormais pour la vérification de signatures détachées, les décisions d'acceptation authentifiées, un gate Git local pre-receive et un journal local durable.

Ces implémentations ne constituent toutefois **ni une frontière de sécurité complète ni une frontière généralement déployée**. Il faut distinguer :

1. une menace ou un traitement est décrit dans l'Architecture 0006 ;
2. un mécanisme existe dans le code ;
3. un test exerce une propriété déclarée ;
4. le mécanisme est installé et appliqué dans un déploiement réel face à l'adversaire concerné.

L'audit identifie plusieurs exemples aux niveaux 2–3, mais n'établit pas le niveau 4 pour la véritable frontière de fusion GitHub du dépôt. Le prototype Git pre-receive local est testé sur un dépôt bare isolé ; il ne constitue pas le mécanisme d'application de GitHub. L'audit en lecture seule des rulesets rapporte uniquement la conformité de configuration et indique explicitement qu'il ne démontre pas le rejet réel d'une mise à jour de référence protégée.

Cet audit est une inspection des sources sur la révision exacte de `main` indiquée ci-dessus. Il n'a pas déclenché Actions, exécuté la suite de tests, lancé TLC ni compilé Lean. Les références aux fichiers de test établissent l'existence et le périmètre des cas de test, pas leur réussite lors d'une nouvelle exécution dans le cadre de cet audit.

## 2. Classification

- **Documenté :** la menace ou le traitement visé apparaît dans l'Architecture 0006 ou un document de conception lié.
- **Implémenté :** du code existe pour au moins un profil borné.
- **Testé :** un test nommé exerce la propriété déclarée. Cet audit ne prétend pas avoir relancé ce test.
- **Démontré en opération :** le contrôle est installé et a effectivement bloqué le chemin réel de publication du déploiement. C'est la catégorie la plus forte ; elle n'est pas déduite de tests unitaires ou d'une inspection de configuration.
- **Lacune / risque résiduel :** contrôle absent, périmètre incomplet, déploiement non vérifié ou adversaire situé hors de la frontière de confiance du mécanisme.

## 3. Matrice de couverture

| Menace / objectif de l'Architecture 0006 | Éléments du dépôt | Évaluation de couverture | Risque résiduel / suite |
|---|---|---|---|
| Affaiblissement ou suppression d'une règle de gouvernance | Changements de source par PR ; protection de branche configurée par le mainteneur ; prototype Git pre-receive dans `scripts/govcheck-git-pre-receive` ; Architecture 0037 | **Partiel ; prototype testé.** Le hook Git peut rejeter les mises à jour de références protégées lorsqu'il est installé sur un serveur bare contrôlé. Le chemin réel d'acceptation GitHub n'est pas démontré par ce hook. | #45 reste ouvert : vérifier le ruleset réel, les checks de confiance obligatoires, les restrictions de push direct, le bypass administrateur et un rejet réel. La configuration GitHub exacte n'a pas été relue en direct pendant cet audit. |
| Règles ambiguës ou contradictoires | `govcheck/check.py` renvoie des résultats distincts pass/fail/unknown ; la décision d'acceptation et le gate rejettent fail/unknown/conflict | **Partiel.** Les résultats fail-closed existent dans la tranche exécutable et l'adaptateur d'acceptation. | Cela ne démontre pas l'existence d'un résolveur générique complet des conflits de politiques ni la couverture de toutes les règles normatives. |
| Confusion de portée / masquage par profil | La décision d'acceptation lie dépôt, candidat, base, référence protégée, révision de gouvernance et portée ; le gate contrôle le dépôt et la référence épinglés | **Partiel ; liaison bornée implémentée.** | La priorité, l'héritage des profils et les fondations non dérogeables ne sont pas démontrés comme intégralement appliqués par un évaluateur canonique unique. |
| Expression de politique malveillante | L'Architecture 0006 recommande les données plutôt que le code ; aucun langage général d'expression n'est sélectionné | **Contrainte de conception uniquement.** La tranche n'exige actuellement aucun langage arbitraire de politique. | Si un langage exécutable ou des expressions fournies par le dépôt sont introduits, ils nécessiteront une analyse distincte de langage borné et d'exécution. |
| Traversée de chemins / échappement par symlink | `attestation_verify.py` rejette les chemins de politique de confiance, de clé et de vérificateur situés dans l'arbre contrôlé par le candidat, y compris après résolution | **Partiel ; contrôles de chemins ciblés implémentés.** | Cela ne prouve pas la sûreté globale des chemins pour toutes les commandes, archives, outils de build ou adaptateurs VCS. |
| Différentiel parseur / canonicalisation | Le vérificateur détaché rejette les clés JSON dupliquées, les flottants et les valeurs non finies ; le journal définit `govcheck.jcs-safe-integer/v1`, rejette clés dupliquées/flottants et utilise l'ordre des propriétés UTF-16 | **Partiel ; profils stricts implémentés.** | Le même contrat de canonicalisation n'est pas établi pour chaque consommateur JSON (dont la première tranche de vérification). Des vecteurs de conformité inter-implémentations et des limites de taille/profondeur restent pertinents. |
| Rejeu de preuves | La Spécification 0010 lie une décision signée à la révision/digest exacts du candidat, à la base, la référence, la politique, la portée, le vérificateur et au digest du rapport d'évaluation ; le vérificateur DSSE contrôle signature et rôle | **Implémenté dans le profil local facultatif.** | Le fournisseur n'est pas activé automatiquement. Les horodatages de confiance et la vérification historique après expiration/révocation d'une clé ne sont pas fournis. |
| Mutation du candidat après approbation / preuve périmée | Le gate Git reçoit le tuple exact ancien/nouveau/référence ; le vérificateur contrôle candidat, base, politique, portée et digest du rapport ; les tests d'intégration incluent le rejet d'une décision périmée | **Implémenté et testé en intégration dans un dépôt Git isolé.** | Le candidat/base réel de fusion GitHub et le chemin de référence protégée après fusion ne sont pas liés à cet adaptateur local aujourd'hui. |
| Approbation falsifiée / attribution du signataire | Architecture 0039 ; vérificateur DSSE Ed25519 facultatif utilisant OpenSSL épinglé par l'opérateur, digests de clés publiques, identifiants de clés, principaux et rôles | **Implémenté comme fournisseur facultatif ; des fixtures cryptographiques synthétiques existent.** | Une signature valide prouve la possession d'une clé configurée, pas l'identité réelle, l'emploi ou l'indépendance d'une personne. La garde de la politique de confiance par l'opérateur reste critique. |
| Clé de signature compromise ou révoquée | La politique de confiance gère intervalles de validité et état de révocation ; politique, clé et exécutable OpenSSL sont épinglés par digest | **Partiel.** Le vérificateur contrôle la validité/révocation configurée. | Aucun cycle complet d'émission, garde, rotation, réponse à incident ou horodatage de confiance n'est fourni. L'opérateur peut modifier la racine de confiance et le digest attendu. |
| Adaptateur VCS incorrect ou perte de sémantique | Hook Git pre-receive et `git_acceptance_gate.py` ; test d'intégration créant un dépôt bare Git isolé et exerçant les push acceptés/rejetés | **Partiel ; prototype Git testé.** | Aucun adaptateur distant/serveur Pijul obligatoire n'est implémenté ou démontré. Un hook Pijul local n'équivaut pas à un enforcement distant. |
| Bypass de forge / checks facultatifs | `govcheck/forge.py audit-ruleset` lit portée du ruleset, checks/source requis et configuration de bypass ; la recherche sur l'acceptation indique explicitement `boundary_demonstrated=false` | **Audit en lecture seule implémenté ; enforcement non démontré.** | L'audit d'un ruleset n'est pas un gate de fusion. #45 reste le travail canonique. Les règles de protection et checks obligatoires doivent être inspectés en direct et le bypass testé ; cet audit ne prétend pas que la configuration GitHub actuelle impose GovCheck. |
| Scripts de contrôle / dépendances du projet malveillants | L'Architecture 0006 identifie scripts/builds/scanners du projet comme non fiables et exige une politique d'exécution explicite, le moindre privilège et des limites de ressources | **Lacune confirmée.** Le gate d'acceptation sépare son vérificateur de confiance de l'arbre candidat, mais ne sandboxe pas les commandes arbitraires de build/test/scanner contrôlées par le projet. | Nouveau travail candidat [#218](https://github.com/Martin-PB/govcheck/issues/218) sur isolation, exposition des secrets et budgets de ressources, sans sélectionner un sandbox universel. |
| Épuisement de ressources | Le journal SQLite utilise un délai d'attente borné ; certains parseurs appliquent un traitement strict des entrées | **Partiel / non général.** | Aucun budget global de temps, mémoire, processus, disque, réseau ou sortie n'est démontré pour les contrôles et parsers non fiables. Suivi par #218. |
| Fuite de secrets | L'adaptateur forge lit les tokens depuis l'environnement et indique qu'ils ne sont pas persistés dans rapports/journaux ; le workflow de contrôle utilise `contents: read` | **Partiel.** | Aucune preuve complète de non-exposition des secrets par des commandes de projet arbitraires, sous-processus, sorties de tests, artefacts ou actions tierces. Suivi par #218 et la revue spécifique des workflows. |
| TOCTOU / mise à jour concurrente | Journal SQLite : transaction `BEGIN IMMEDIATE`, compare-and-append avec tête attendue, idempotence et reçus durables ; gate Git : tuple exact de mise à jour de référence | **Implémenté et couvert par des tests ciblés.** | L'intégrité du journal local n'authentifie pas les acteurs et ne résiste pas à un administrateur privilégié de la base. Une course réelle de fusion forge n'est pas démontrée. |
| Administrateur forge/serveur compromis | L'Architecture 0006 traite explicitement l'accès admin/local et le bypass forge comme limites de confiance ; gate et politique sont installés hors de l'arbre candidat | **Menace documentée ; limite explicite.** | Un administrateur serveur peut remplacer le hook/runtime ou modifier la configuration. Un administrateur GitHub ou acteur de bypass peut modifier les règles. Aucun contrôle indépendant ne supprime actuellement cette hypothèse de confiance. |
| Auditabilité / intégrité de l'historique | Journal SQLite à chaîne de hachage, triggers d'immutabilité des événements/reçus, vérification de chaîne et reçus durables ; Architecture 0038 | **Implémenté comme profil d'intégrité local.** | Une chaîne de hachage n'est ni authentification d'acteur ni stockage inviolable. Un administrateur privilégié peut réécrire la base et recalculer la chaîne en l'absence de point de contrôle externe fiable. |

## 4. Conclusions consolidées

### 4.1 Progrès réel

Le dépôt a dépassé l'affirmation initiale de l'Architecture 0006 selon laquelle aucun contrôle de sécurité n'existe :

- **Vérification de preuves détachées :** un vérificateur DSSE/Ed25519 facultatif contrôle la structure du payload canonique, les liaisons exactes, les identifiants/rôles de clés, leur validité/révocation et les digests épinglés d'OpenSSL et des clés (Architecture 0039 ; `govcheck/attestation_verify.py`).
- **Décision d'acceptation :** la Spécification 0010 sépare le résultat d'évaluation d'une décision d'autorité authentifiée et lie cette décision au candidat, à la base, la politique, la portée, au vérificateur et au digest du rapport exacts.
- **Prototype d'enforcement Git :** un hook pre-receive côté serveur délègue à un gate installé hors du dépôt et épinglé par digest ; les tests d'intégration isolés exercent l'acceptation de PASS et le rejet de décisions UNKNOWN/périmées ou non concordantes.
- **Journal local :** le profil SQLite fournit append transactionnel, contrôle de concurrence par tête attendue, nouvelle tentative idempotente, reçus durables et vérification de chaîne (Architecture 0038).

Ce sont des incréments d'implémentation bornés, pas la preuve que chaque déploiement de dépôt les a installés.

### 4.2 Lacunes principales

1. **Aucune frontière GitHub d'enforcement démontrée.** Le dépôt possède un auditeur de ruleset en lecture seule et un prototype de serveur Git local, mais pas de GitHub App/source de check démontrée comme obligatoire pour le candidat exact de fusion, aucun test réel de rejet d'une référence protégée sur GitHub, ni test complet de bypass. Le suivi reste #45.
2. **Aucun contrat de sandbox pour les contrôles fournis par le dépôt.** Le modèle de menace nomme ce risque, mais le code n'établit pas l'isolation, la minimisation des secrets ou les budgets de ressources pour les scripts/outils de build du projet. Ce point est désormais suivi comme issue candidate #218.
3. **Cycle de vie de la racine de confiance incomplet.** L'association clé-principal, l'état de révocation et les digests épinglés existent, mais la garde des clés, leur rotation, la réponse à compromission et les horodatages historiques fiables restent à la charge du déploiement. Continuer sous #44 et les travaux associés à la politique de confiance.
4. **Aucun enforcement Pijul distant.** Le prototype Git ne doit pas être généralisé à Pijul ni à tous les adaptateurs VCS.
5. **Aucune protection contre un administrateur totalement privilégié.** La base locale, le gate, la politique de confiance, les règles de forge et le runtime serveur restent dans des hypothèses explicites de confiance administrative.

### 4.3 Aucun relecteur indépendant inventé

La situation actuelle à contributeur unique reste un risque résiduel matériel, pas une raison de fabriquer une approbation. Une signature cryptographique d'une clé affectée à un rôle ne crée pas une revue indépendante, sauf si la clé est réellement contrôlée par un principal autorisé distinct. Voir #60 et #71.

## 5. Disposition des travaux

| Travail | Résultat de l'audit |
|---|---|
| #44 — attestations interopérables | Continuer : cycle de vie de la racine de confiance, identité réelle et sémantique des revues indépendantes détachées restent ouverts. |
| #45 — frontière d'acceptation | Continuer : enforcement GitHub réel et démonstrations de bypass/rejet restent ouverts. |
| #60 — risque résiduel d'autorité unique | Le maintenir explicite ; ne pas prétendre à une séparation des tâches. |
| #70 — cet audit | Matrice de couverture achevée par cette proposition ; ne fermer qu'après revue/fusion du rapport et mise à jour de l'issue avec les suites restantes. |
| #72 — corpus de candidats adversariaux | Continuer : utiliser les catégories ci-dessus pour ajouter des fixtures positives/négatives liées au candidat exact. |
| #218 — isolation d'exécution | Nouvel élément candidat de backlog pour la lacune confirmée sur sandbox/ressources/exposition des secrets. |

## 6. Périmètre et limites

Ce rapport n'est ni un test d'intrusion, ni une revue de sécurité indépendante, ni une certification, ni une preuve formelle de correction de l'implémentation, ni une confirmation de la configuration réelle de la forge. Il ne modifie pas les hypothèses de menace de l'Architecture 0006, n'adopte aucune politique d'enforcement, n'active aucun sandbox, ne change pas la protection de branche et n'affirme pas que le gate local est déployé.

Les distinctions de statut de ce rapport doivent être conservées dans la documentation ultérieure : documenté, implémenté, testé et démontré en opération sont des affirmations distinctes.

## 7. Éléments du dépôt examinés

- [Architecture 0006 — Modèle de menace et de confiance](../architecture/0006-threat-and-trust-model.fr.md) et son équivalent anglais.
- [Architecture 0037 — Frontière d'acceptation et adaptateurs d'enforcement](../architecture/0037-acceptance-boundary-and-enforcement-adapters.fr.md).
- [Architecture 0038 — Profil d'implémentation du journal canonique local](../architecture/0038-local-canonical-journal-implementation.fr.md).
- [Architecture 0039 — Vérification DSSE détachée et politique de confiance épinglée](../architecture/0039-detached-dsse-trust-policy.fr.md).
- [Spécification 0008 — Attestations d'assurance interopérables](../specifications/0008-interoperable-assurance-attestations.fr.md).
- [Spécification 0009 — Attestations de revue indépendante](../specifications/0009-independent-review-attestations.fr.md).
- [Spécification 0010 — Décisions d'acceptation authentifiées](../specifications/0010-authenticated-acceptance-decisions.fr.md).
- [Recherche sur l'enforcement à la frontière d'acceptation](acceptance-boundary-enforcement-2026-11.fr.md).
- Sources : `govcheck/attestation_verify.py`, `govcheck/git_acceptance_gate.py`, `govcheck/forge.py`, `govcheck/journal.py`, `scripts/govcheck-git-pre-receive`.
- Tests : `tests/test_attestation_verify.py`, `tests/test_git_acceptance_gate.py`, `tests/test_pre_receive_acceptance_integration.py`, tests du journal.
- [Registre des travaux](../work-portfolio/work-items.md), issues #44, #45, #60, #70, #72 et #218.
