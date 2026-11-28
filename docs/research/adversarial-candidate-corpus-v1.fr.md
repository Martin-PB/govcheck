# Corpus de candidats adversariaux — version 1.1.0

**Statut :** catalogue versionné 1.1.0 avec pointeurs vers les tests existants ; il ne prétend ni que chaque attaque possède une fixture exécutable, ni que la frontière d'acceptation est déployée.  
**Instantané source :** révision du corpus v1.1.0 `d25e417f41eb67619cc6a9df285cdb89b317dd70` ; la base v1.0.0 avait été auditée sur `451d1e1ff929946274edba8e844e08d74fdd306f`.  
**Parent :** [Issue #72](https://github.com/Martin-PB/govcheck/issues/72).  
**English:** [Adversarial candidate corpus](adversarial-candidate-corpus-v1.md).  
**Manifeste lisible par machine :** [`formal/adversarial-candidate-corpus-v1.json`](../../formal/adversarial-candidate-corpus-v1.json).

## 1. Objet et interprétation

Ce corpus enregistre des scénarios positifs, adversariaux, de frontière et non encore testés pour l'évaluateur et les adaptateurs d'acceptation. Il ne les réduit volontairement pas à un score générique d'attaque. Chaque cas précise :

- l'attaque ou la condition de frontière ;
- le résultat attendu ;
- la manière dont le contexte candidat et base/politique est lié ;
- le test/modèle/document existant qui fournit l'élément probant ;
- le statut de couverture et la limite résiduelle.

Le corpus distingue `tested-unit`, `tested-integration`, `model-only`, `planned` et `not-demonstrated`. Un pointeur vers un test ne signifie pas que ce test a été relancé dans cette modification. Un cas uniquement modélisé n'est pas un test de l'implémentation. Un audit de configuration ne prouve pas qu'une forge rejette une mise à jour réelle.

## 2. Liaison et provenance

Le manifeste épingle l'instantané source à partir duquel ses pointeurs de test initiaux ont été audités. Les tests unitaires peuvent utiliser des valeurs synthétiques déterministes de candidat/base ou générer des clés de signature et politiques éphémères. Les tests d'intégration Git local créent des identifiants de commits temporaires exacts et lient les décisions au tuple ancien/nouveau/référence à l'exécution. Dans chaque cas, le test doit exercer les valeurs exactes qu'il a générées ou déclarées ; un résultat de test ne doit pas être généralisé à un autre candidat ou à une autre politique.

Ce corpus ne contient volontairement aucun digest partagé de politique de confiance de production. Les clés éphémères et politiques de test sont du matériel de test, pas des racines de confiance GovCheck. Toutes les entrées déclarent `deploymentStatus: not-demonstrated` : même un test d'intégration Git isolé ne démontre pas que le même gate est installé sur une forge de production.

## 3. Carte initiale de couverture

| Plage de cas | Domaine | Éléments probants existants | Statut actuel |
|---|---|---|---|
| AC-001–AC-003 | Décision d'acceptation, digest du rapport, liaison du candidat, distinction PASS/risque | `tests/test_acceptance_decision.py` | Tests unitaires |
| AC-004–AC-005 | Signature DSSE, rôle/principal du signataire, expiration/révocation de clé | `tests/test_attestation_verify.py` | Tests unitaires avec clés synthétiques |
| AC-006–AC-009 | Résultats du gate, tuple/pins exacts, références protégées et voie de risque explicite | `tests/test_govcheck_git_pre_receive.py` | Tests unitaires |
| AC-010–AC-011 | Décision périmée et comportement réel d'un receive Git bare local | `tests/test_pre_receive_acceptance_integration.py`, `tests/test_govcheck_git_pre_receive_integration.py` | Tests d'intégration isolés |
| AC-012–AC-013 | Configuration du ruleset forge et références non applicables | `tests/test_govcheck_forge.py`, `tests/test_govcheck_git_pre_receive.py` | Tests unitaires ; configuration seulement |
| AC-014–AC-015 | Concurrence du journal et parsing JSON canonique | `tests/test_journal.py` | Tests unitaires |
| AC-016 | Abstraction de frontière d'acceptation enforced/advisory/bypass admin | `formal/tla/GovCheckAcceptanceBoundary.tla` et configurations | Modèle uniquement |
| AC-017 | Symétrie des filtres de chemins, routage des workflows réutilisables, syntaxe de chemins non prise en charge et routage des entrées de modèles | `tests/test_ci_workflow_routing_audit.py` | Tests unitaires sur fixtures de dépôt synthétiques ; pas un gate de forge |
| AC-018–AC-019 | Rejeu d'un rapport TLC périmé ; injection de `sorry`/axiome Lean | Aucun test exécutable propre au corpus | Planifié |
| AC-020 | Rejet réel d'une référence protégée GitHub et bypass | Recherche sur la frontière d'acceptation ; vérification de la configuration réelle encore requise | Non démontré ; suivi par #45 |
| AC-023 | Workflow report-only non obligatoire comme check d'acceptation dans le ruleset réel | Workflow et instantané du ruleset | Non démontré ; liste des checks requis vide ; suivi par #45 |
| AC-021 | Bypass de l'enforcement distant Pijul/Nest | Recherche plateforme uniquement | Planifié ; aucun adaptateur distant d'enforcement |
| AC-022 | Exécution hostile de contrôles fournis par le dépôt, exfiltration de secrets et épuisement de ressources | Architecture 0006 ; issue candidate #218 | Planifié ; aucun sandbox sélectionné |

Le manifeste lisible par machine constitue la source des identifiants de cas et des pointeurs de preuve exacts. AC-017 référence désormais les tests de routage synthétiques : asymétrie des filtres PR/push, workflows réutilisables absents ou non routés, syntaxe non prise en charge, globs non justifiés et routage des entrées de modèles. Ces tests ne prouvent pas l'existence d'un gate GitHub obligatoire. AC-023 enregistre la lacune distincte : le workflow report-only n'est pas un check obligatoire dans le ruleset actuel. `tests/test_adversarial_candidate_corpus.py` vérifie l'identité/version du manifeste, l'unicité des IDs, les sémantiques requises, l'existence des fichiers de preuve et les noms des méthodes de test Python référencées. Ce test d'intégrité n'exécute pas lui-même les attaques sous-jacentes.

## 4. Limites importantes

1. **Aucune revendication d'enforcement en production.** Le prototype de hook Git local n'est ni une GitHub App ni un gate de fusion hébergé réel.
2. **Aucun relecteur indépendant synthétisé.** Les clés de test et principaux des fixtures n'établissent pas l'existence d'un relecteur humain indépendant.
3. **Aucun enforcement général Pijul.** Un hook local n'est pas une frontière d'acceptation distante obligatoire.
4. **Aucun sandbox de code projet arbitraire.** Isolation d'exécution, minimisation des secrets et budgets de ressources restent des travaux candidats dans #218.
5. **Aucune suite complète d'attaques sur les preuves formelles pour l'instant.** Les rapports de model checking périmés et les preuves Lean contenant des axiomes interdits restent des cas planifiés.

## 5. Incréments suivants

- Transformer AC-018–AC-019 en fixtures liées à des candidats exacts, avec résultats fail/unknown attendus et provenance explicite ; étendre AC-017 aux chemins d'altération non couverts par l'audit de routage.
- Étendre le corpus aux chemins d'attaque et hypothèses de confiance précis de l'Architecture 0006.
- Lier tout nouveau rapport de test à la révision du corpus, à la version des outils/tests, au candidat/base exacts, à la politique applicable et à l'identité du vérificateur.
- N'ajouter une expérience de frontière forge réelle que lorsque sa configuration requise et son environnement de test sont explicitement autorisés et disponibles.

Ce catalogue n'adopte aucune nouvelle règle normative, ne modifie pas la configuration de protection de branche et ne prétend pas qu'un cas planifié est déjà testé.
