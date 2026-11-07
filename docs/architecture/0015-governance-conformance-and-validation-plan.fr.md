# 0015 — Outil de conformité de gouvernance et plan de validation

**Statut :** proposition de capacités et de validation, pas une affirmation d’implémentation. « Outil de conformité de gouvernance » désigne des responsabilités livrées progressivement par le cœur GovCheck et ses adaptateurs. **English:** [0015](0015-governance-conformance-and-validation-plan.md).

## Six responsabilités

1. **Découverte de la gouvernance :** identifier paquet canonique, version, profils, autorité et documentation contrôlée.
2. **Conformité documentaire :** vérifier que les instructions normatives sont des projections autorisées et que l’explicatif n’est pas promu silencieusement en politique.
3. **Traçabilité :** relier le dossier aux identités exactes dépôt/base/candidat, objectifs/exigences/propriétés affectés, décisions et objets natifs VCS/collaboration.
4. **Exécution des contrôles :** résoudre contrôles applicables, prérequis, conditions autorisées, identité/version/configuration outils et limites de ressources ; enregistrer les résultats.
5. **Évaluation de l’assurance :** examiner affirmations au regard des preuves admissibles, hypothèses, fraîcheur, indépendance, exceptions et prédicat d’acceptation.
6. **Autorité/application :** vérifier approbations et appliquer/revalider à la frontière la plus forte disponible, en exposant les limites de contournement.

Ce sont des responsabilités, pas des niveaux de maturité. Inspection/audit locaux sans application partagée doivent être signalés honnêtement.

## Trois sujets de conformité distincts

- **Conformité de l’artefact :** gouvernance, documents, code/configuration et contrôles déclarés possèdent structure et traçabilité requises.
- **Comportement agent/processus :** un agent/harness et flux délégué ont respecté le contrat de tâche lors d’un exercice enregistré.
- **Application opérationnelle :** la frontière déployée empêche l’application interdite et résiste aux contournements, preuves obsolètes, courses et dérogations administratives selon son modèle de menace.

Les contrôles d’artefacts ne qualifient pas tous les agents. La qualification d’un agent ne prouve pas la correction d’un artefact. Un rapport CLI local n’établit pas l’application opérationnelle.

## Dossier d’assurance

Le rapport est un dossier, pas un badge PASS/FAIL ni un score opaque. Il identifie schéma/rapport ; dépôt et VCS natif/capacités ; base/candidat exacts (dirty/index/worktree ou état Pijul natif) ; paquet/révision/profil de gouvernance ; spécification/modèle/build/configuration évaluateur ; affirmations/exigences du périmètre ; contrôles, invocations exactes, outils/versions/digests, environnement, limites et statut ; sortie brute ou référence protégée ; provenance/fraîcheur/invalidations ; hypothèses, réfutations, contradictions, zones non prises en charge et exceptions ; identités/rôles producteur, validateur indépendant et autorité ; décision, sujet exact, date et frontière d’application ; limites de contournement.

Le rapport prouve qu’une évaluation définie a eu lieu, pas que chaque affirmation est vraie.

## Vocabulaire des statuts

Libellés candidats :
- `NOT_EVALUATED`
- `CHECKED` — contrôle mécanique/empirique spécifié exécuté.
- `MODEL_CHECKED` — exploration achevée pour le modèle/configuration enregistrés.
- `PROOF_CHECKED` — vérificateur ayant accepté un objet sous hypothèses enregistrées.
- `CONFORMANCE_ESTABLISHED` — conformité implémentation/spécification justifiée séparément.
- `EXEMPTED` — exception valide approuvée par l’autorité.
- `FAILED`

Ce ne sont ni des notes ni des statuts interchangeables. Ils exigent sujet, périmètre, méthode, preuves, hypothèses et métadonnées d’achèvement. MODEL_CHECKED ne signifie pas conformité de l’implémentation ; EXEMPTED est une décision, pas une preuve. Préserver aussi inconnu, non exécuté, non applicable, non pris en charge, incomplet, obsolète/invalidé et conflit.

## Validation sur dépôts représentatifs

Avant de choisir sérialisation, langage, adaptateur agent ou forge, valider au moins quatre contextes :

| Fixture | Défi |
|---|---|
| Petite bibliothèque | Faible surcharge, local seul, fonctionnalité/correction, gouvernance absente, contrôle obsolète |
| Application avec agents | Agents multiples, revue humaine, découverte, incertitude, pas d’auto-approbation |
| Technologie/VCS inhabituel | Contrôle non pris en charge, état non-Git, préservation identité/conflit Pijul si disponible |
| Projet haute assurance | TLA+/Lean, distinctions preuve/modèle/test, limites de raffinement |

Exécuter les mêmes classes de tâches avec plusieurs agents/harness si possible. Enregistrer révisions, configurations et versions d’outils. Une démonstration ne prouve pas une qualification générale.

## Catalogue de tests d’acceptation (critères futurs)

1. Découvrir gouvernance valide ; signaler absence sans inventer de défauts.
2. IDs dupliqués, références non résolues et constructions normatives non prises en charge échouent ou deviennent indéterminés.
3. Détecter règles obligatoires contradictoires ; l’ordre des fichiers ne tranche pas.
4. Absence d’interdiction ≠ permission.
5. Signaler Markdown ajoutant une obligation non enregistrée.
6. Signaler projection anglais/français obsolète ou divergente.
7. Relier tâche aux objectifs, exigences, propriétés et composants.
8. Contrôle obligatoire absent ≠ succès.
9. Succès d’un test ≠ preuve mathématique ou conformité d’implémentation.
10. Rapport de model checking lié au modèle/configuration et à l’achèvement exacts.
11. Rapport de preuve identifiant noyau, axiomes, imports et obligations admises.
12. Preuve d’un autre candidat/révision/dépendances considérée obsolète.
13. Producteur ne peut approuver sa propre exception ni être unique validateur si séparation requise.
14. Label/commentaire/réaction PR ou CI verte ne crée pas l’acceptation.
15. État Git dirty/index/worktree/sous-modules non réduit à HEAD.
16. Sémantiques patch/canal/graphe/conflit Pijul non remplacées par hypothèses Git.
17. Mutation entre acceptation/application déclenche revalidation ou échec sûr.
18. Contournement local privilégié signalé, non déclaré impossible.
19. Exception limitée, autorisée, motivée, bornée dans le temps ; inconnu ne devient pas preuve.
20. Rapport conserve contradictions, limites, échecs outils et exécutions partielles.

Ces critères n’ont pas été exécutés par ce changement documentaire.

## Frontière produit conservée

- Petit exécutable local et CLI documentée obligatoires.
- Aucun daemon, service hébergé, MCP ou harness obligatoire.
- Interfaces facultatives délèguent à la même sémantique ; pas de second évaluateur normatif.
- Profils déclaratifs sélectionnant obligations/contrôles, pas niveaux selon taille.
- Adaptateurs déclarant exécutable, arguments, prérequis, limites temps/ressources, format résultat et identité outil ; pas de code arbitraire de politique chargé dans le cœur.
- Outils existants build/test/sécurité/formel/VCS gardent leurs rôles ; GovCheck qualifie et enregistre leurs sorties.
- Git et Pijul restent adaptateurs natifs séparés ; hébergement/forge distincts de la sémantique.
- Bootstrap/migration non destructifs : inspecter → planifier → appliquer, migrations versionnées, dérive et retour arrière.

MCP fut envisagé comme interface facultative ; ce n’est pas une dépendance obligatoire. Lean reste candidat pour un cœur critique de preuve étroitement justifié, pas pour tout le produit ni comme dépendance des dépôts gouvernés.

## Proposition de livraison

**v0.1 — Gouvernance locale/dossier :** inspection/bootstrap sûr ; source canonique versionnée ; obligations/interdictions/permissions/dérogations/applicabilité ; plan/décisions ; déclarations et enregistrements de contrôles ; résultats liés au candidat ; documentation contrôlée ; dossier d’assurance local.

**v0.2 — Agents :** CLI stable et opérations machine pour découvrir exigences, démarrer changements, enregistrer décisions, demander exceptions et évaluer dossiers ; AGENTS.md généré/contrôlé ; exercices agents représentatifs ; adaptateurs sans logique normative.

**v0.3 — Application partagée :** intégration forge/équipe de référence (GitHub d’abord seulement si choisi) ; décision avant application liée au candidat ; vérification attestations et invalidation obsolescence ; capacités/contournement admin visibles ; historique décisions/dérogations.

**v0.4 — Assurance formelle :** formaliser sémantique du cœur et composants justifiés ; modèles TLA+ cycle/concurrence et rapports utiles ; prototype Lean pour prédicats/certificats seulement si justifié ; vecteurs de conformité et raffinement ; dossier de release renforcé.

Ne pas retarder une première tranche utile jusqu’à preuve de chaque règle ; ne pas vendre docs/tests/déclarations de modèles comme assurance implémentée.

## Frontières de l’étude écosystème

Les outils discutés occupent des couches différentes :
- Spec Kit et workflows de spécification agent structurent intention/spécification et étapes d’implémentation.
- OPA/Cedar prennent des décisions de politique exécutables, sans établir justesse normative ou impossibilité de contournement.
- in-toto/SLSA traitent provenance/attestations de chaîne logicielle, pas sémantique de gouvernance.
- OpenSSF Scorecard fournit des signaux de posture, pas un dossier d’assurance complet.
- Lean vérifie des dérivations, pas le choix des exigences ni la conformité d’un exécutable non vérifié.
- Writ et Privateer nécessitent une étude technique approfondie dédiée. Aucune conclusion de compatibilité/adoption sans revue des sources/du code.

Comparer selon complémentarité avec les six responsabilités, frontière de confiance étroite, local d’abord, sémantiques Git/Pijul, reproductibilité et limites épistémiques. Aucune pile globale sélectionnée.

## Décisions différées

Commandes CLI/dossier ; composition profils/modèles tâches ; première intégration forge et modèle de menace ; protocole qualification agents/indépendance ; adoption Writ/Privateer ; rôle justifié de Lean ; rétention/confidentialité/stockage protégé. Chacun nécessite ADR/prototype et preuves.


## Références

- [Registre GovCheck des références sur la gouvernance et l'assurance](../references/governance-and-assurance.fr.md) : NIST SSDF, in-toto/SLSA, OpenSSF Scorecard, OPA et Cedar, avec leur périmètre et leurs limites.
- [Version anglaise](../references/governance-and-assurance.md).
