# Audit de compatibilité et d'adéquation sémantique de CSLib

**Date de l'audit :** 2026-11-12  
**Catalogue de références :** [R-20 Lean et bibliothèque de formalisation associée](../../references.fr.md#r-20)  
**Dépôt :** [leanprover/cslib](https://github.com/leanprover/cslib)  
**Commit inspecté :** `70e25828d89a3916e41c9d84cfffd7e6093bb1a0`  
**Noyau Lean GovCheck :** Lean 4.19.0

## 1. Conclusion exécutive

CSLib est pertinent pour le problème de formalisation de GovCheck, mais son adéquation la mieux démontrée concerne **la sémantique formelle des systèmes et le raisonnement temporel/sur les transitions**, et non une ontologie prête à l'emploi pour l'alignement d'ontologies ou la gouvernance des éléments probants.

Le HEAD CSLib inspecté n'est pas directement compatible avec le projet Lean actuel de GovCheck : CSLib épingle `leanprover/lean4:v4.36.0-rc2`, tandis que le noyau épistémique GovCheck épingle Lean 4.19.0. CSLib épingle également Mathlib au commit `887bb849a9f64e1c66499fd5ff8523c864e78941`. N'ajoutons pas CSLib comme dépendance du paquet Lean 4.19 sans migration volontaire de chaîne d'outils ou projet de compatibilité isolé.

## 2. Formalisations pertinentes repérées

| Domaine CSLib | Module inspecté | Pertinence pour GovCheck | Limite |
|---|---|---|---|
| Logique temporelle de base (BTL) | `Cslib/Logics/BTL/Basic.lean` | Modalités futur/passé, sémantique de modèles/cadres, relation de satisfaction, propriétés temporelles | BTL est un langage modal temporel de base avec F/P ; il n'est pas automatiquement équivalent à tous les formalismes LTL |
| Séquences infinies | `Cslib/Foundations/Data/OmegaSequence/Temporal.lean` | `Step`, `LeadsTo`, transitivité et propriétés de récurrence/éventualité sur les exécutions infinies | Utile pour les propriétés temporelles du cycle de vie ; nécessite une correspondance explicite avec les traces d'états GovCheck |
| Systèmes de transitions étiquetées | `Cslib/Foundations/Semantics/LTS/Basic.lean` | Transitions d'états, traces finies, bornitude, terminaison, propriétés d'états finis | Bonne base de sémantique opérationnelle ; pas une ontologie de gouvernance |
| Sémantique modale | `Cslib/Logics/Modal/Semantics.lean` | Modèles, cadres, valuations et sémantique de satisfaction | Substrat sémantique formel, pas spécification de mapping pour SACM/OWL/SEON |

Le code BTL laisse explicitement la relation d'accessibilité sans contrainte par défaut : la réflexivité détermine si le présent est inclus, et la transitivité détermine si la relation modélise un écoulement du temps. GovCheck devra donc énoncer et prouver les hypothèses de cadre adaptées à chaque propriété de cycle de vie ; importer BTL ne les fournit pas automatiquement.

## 3. Constat de compatibilité

Au HEAD inspecté :

- Chaîne d'outils Lean CSLib : `leanprover/lean4:v4.36.0-rc2`.
- Dépendance Mathlib CSLib : révision Git exacte `887bb849a9f64e1c66499fd5ff8523c864e78941`.
- Noyau épistémique GovCheck : Lean 4.19.0.

Conséquences :

1. Le HEAD CSLib actuel ne peut pas être importé tel quel dans le paquet Lake GovCheck en Lean 4.19.
2. Une migration vers une version candidate uniquement pour consommer CSLib serait un couplage injustifié à ce stade.
3. Un paquet de compatibilité séparé permettrait de tester CSLib avec sa chaîne d'outils épinglée sans modifier la compilation de confiance du noyau sémantique GovCheck.
4. Il est également possible de rechercher un commit historique CSLib compatible avec Lean 4.19, mais il faut l'identifier dans l'historique et le tester, pas le supposer.

## 4. Analyse préliminaire du socle de confiance

Une recherche préliminaire dans le code du commit inspecté a donné les résultats suivants :

- aucune occurrence indexée de `sorry` ;
- aucune occurrence indexée de `run_tac`, `implemented_by` ou `extern` ;
- les occurrences de `axiom` décrivent principalement des axiomes comme objets des logiques modales/propositionnelles formalisées, et non des axiomes du noyau Lean ;
- les occurrences de `unsafe` se trouvaient dans des commentaires de tests, sans déclaration identifiée ;
- plusieurs déclarations `opaque` sont des marqueurs de types, par exemple `InferenceSystem.Default`, `MLL` et `ND`, et ne constituent pas en elles-mêmes une frontière de preuve non sûre.

Il s'agit d'une recherche préliminaire, pas d'une certification du socle de confiance : la recherche de code GitHub n'est pas un audit statique exhaustif, et les dépendances transitives Mathlib ainsi que les artefacts générés/compilés restent à inspecter. Avant d'importer une définition dans un théorème GovCheck critique, il faudra examiner toute sa fermeture de dépendances transitives et auditer ses axiomes avec `#print axioms` de Lean ou un contrôle reproductible équivalent.

## 5. CSLib résout-il le problème de cohérence du métamodèle ?

Aucun module CSLib inspecté ne fournit les sémantiques spécifiques à GovCheck qui manquent pour :

- classe de méthode probante versus statut du résultat et acceptation ;
- préservation de la provenance et de la révision source entre mappings ;
- classes de couverture sémantique et pertes d'information explicites ;
- préservation de la portée et des hypothèses ;
- absence d'amplification de l'autorité et des délégations ;
- extension conservative ou non-interférence lors de l'ajout de concepts GovCheck aux ontologies sources ;
- fidélité des imports/exports SACM 2.4 Beta 1.

Lean reste l'assistant de preuve et l'environnement de vérification par noyau dans lequel GovCheck peut énoncer ces obligations. CSLib peut fournir des définitions formelles réutilisables pour certaines structures mathématiques et certains mécanismes sémantiques. Il ne remplace pas les contrats de liaison GovCheck.

## 6. Stratégie d'intégration recommandée

N'ajoutons pas encore CSLib au paquet central. À la place :

1. Conserver le petit noyau épistémique sur sa chaîne Lean 4.19 épinglée tant qu'il reste sans dépendance.
2. Créer une expérimentation de compatibilité CSLib séparée et isolée, épinglée au commit CSLib exact et à sa révision Mathlib.
3. Formaliser une propriété de cycle de vie GovCheck dans le noyau GovCheck et une autre dans le cadre BTL ou `ωSequence` de CSLib.
4. Énoncer une relation sémantique explicite entre les deux représentations et prouver la préservation dans les deux sens lorsqu'une équivalence est revendiquée ; sinon déclarer précisément le sens et la couverture.
5. Comparer le résultat CSLib au modèle TLA+ existant. Ne pas considérer la traduction entre TLA+ et Lean/CSLib comme fiable par défaut sans établir sa préservation sémantique.
6. Ce n'est qu'après réussite de l'expérience qu'il faudra décider si CSLib devient une dépendance directe, un back-end de preuve isolé ou une formalisation de référence.

## 7. Conclusion

CSLib doit être considéré comme une bibliothèque candidate sérieuse pour les sémantiques de cycle de vie, les systèmes de transitions, le raisonnement temporel et les théories informatiques connexes. Le HEAD actuel inspecté n'est pas une dépendance directement intégrable au noyau Lean 4.19 de GovCheck et ne fournit pas les garanties de mapping d'ontologies dont GovCheck a besoin.

Une expérimentation de compatibilité épinglée et séparée est désormais présente dans `formal/cslib-compat/` ; elle importe les modules BTL et de séquences temporelles infinies sans modifier la chaîne d'outils du noyau GovCheck. Sa compilation CI a réussi dans [l'exécution 43210543930](https://github.com/Martin-PB/govcheck/actions/runs/43210543930), avec 1 779 tâches et les API BTL/séquences oméga demandées. Il s'agit uniquement d'une compatibilité de compilation et d'API. Il s'agit d'un test de compilation et de disponibilité des API, pas d'une preuve de raffinement sémantique. Ce n'est pas une mise à niveau de la chaîne d'outils du noyau GovCheck et cela ne signifie pas que la logique temporelle suffit à établir la cohérence statique du métamodèle.
