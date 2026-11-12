# Prototype de cohérence du métamodèle — compte rendu d'exécution

**Statut :** première tranche exécutable compilée ; abstraction de cycle de vie vérifiée par model checking borné.  
**Date :** 2026-11-12.  
**Travaux liés :** issue [#73](https://github.com/Martin-PB/govcheck/issues/73), [contrat du prototype dans la PR #106](https://github.com/Martin-PB/govcheck/blob/docs/metamodel-decision-dossier-2026-11/docs/research/metamodel-coherence-prototype-contract.fr.md), [recherche de vérification dans la PR #106](https://github.com/Martin-PB/govcheck/blob/docs/metamodel-decision-dossier-2026-11/docs/research/metamodel-coherence-verification.fr.md).

## 1. Ce qui a réellement été exécuté

### Noyau épistémique Lean

- Source : `formal/lean/GovCheckEpistemic/Evidence.lean`
- Chaîne d'outils : Lean 4.19.0, épinglée dans `formal/lean/lean-toolchain`.
- Workflow : `Lean epistemic core`.
- Exécution réussie : [43209380453](https://github.com/Martin-PB/govcheck/actions/runs/43209380453).
- Résultat : `lake update` et `lake build` terminés avec succès.

Le noyau sépare la classe de méthode de l'état du résultat et représente une correspondance comme un transport conservant la classe ou comme une dérivation distincte de type preuve de théorème, appuyée par un objet explicite `KernelCheckedDerivation`. Les déclarations vérifiées établissent la préservation de la classe lors du transport, les voies admissibles vers un résultat de preuve de théorème et la préservation du statut.

**Limite de portée :** ce résultat vérifié par le noyau concerne les définitions de ce module Lean. Il ne prouve ni que ces définitions constituent la sémantique définitive de GovCheck, ni qu'un mapping SACM est correct, ni qu'un importateur/exportateur est conforme au modèle.

### Modèle TLA+ de fraîcheur des éléments probants

- Source : `formal/tla/GovCheckEvidenceFreshness.tla`
- Configuration : `formal/tla/GovCheckEvidenceFreshness.cfg`
- Chaîne d'outils : SANY 2.1, TLC 2.19, tla2tools 1.7.4 (empreinte vérifiée), Temurin Java 17.
- Exécution réussie : [43209535512](https://github.com/Martin-PB/govcheck/actions/runs/43209535512).
- Résultat : SANY a analysé le modèle ; TLC n'a trouvé aucun contre-exemple dans l'espace d'états fini configuré.
- Exploration : 132 états générés, 20 états distincts, 0 restant, profondeur 4.
- Invariants contrôlés : `TypeOK`, `AcceptedImpliesFresh`, `NonPassingEvidenceCannotBeAccepted`.

Il s'agit d'un élément probant de model checking borné pour une abstraction à deux révisions, pas d'une preuve de théorème ni d'une preuve de conformité de l'implémentation.

## 2. Un contre-exemple utile a été découvert puis corrigé

La première exécution TLC a révélé un véritable défaut du modèle : `ReevaluateEvidence` pouvait modifier le résultat d'un élément déjà accepté en `Failed` tout en conservant `accepted = TRUE`. TLC a produit la trace suivante :

1. l'élément initial à la révision v0 est Passed ;
2. la révision source passe à v1 ;
3. l'élément est réévalué à v1 et reste Passed ;
4. l'élément est accepté ;
5. une nouvelle évaluation le passe à Failed sans annuler l'acceptation.

L'invariant `NonPassingEvidenceCannotBeAccepted` a échoué. La transition a été corrigée pour que toute réévaluation efface la décision d'acceptation précédente. L'exécution TLC suivante s'est terminée sans contre-exemple.

Cette séquence illustre la distinction recherchée : la première exécution n'était pas « une preuve échouée », mais un contre-exemple de model checking borné révélant une incohérence dans le modèle de transitions. L'exécution corrigée apporte uniquement un élément probant borné sur le modèle fini corrigé.

## 3. Intégration et gouvernance du dépôt

- Les deux workflows de vérification sont explicitement classés comme propres au niveau méta dans `scripts/check-package-alignment.py` ; ils ne sont pas copiés dans le paquet de modèles destiné aux dépôts adoptants.
- Le noyau Lean et le modèle TLA+ sont inscrits dans `formal/artifacts.json`, avec chaîne d'outils, exécution, commit, résultat, bornes et limites exacts.
- Le prototype est suivi dans la [PR #115](https://github.com/Martin-PB/govcheck/pull/115).
- Le dossier de décision et de recherche initial reste dans la [PR #106](https://github.com/Martin-PB/govcheck/pull/106).

## 4. Lacunes restantes en matière de preuve et de validation

Les résultats actuels n'établissent pas encore :

- la préservation de la provenance, de la révision source, des hypothèses et de la portée des affirmations lors de mappings réels ;
- la composition sûre de mappings ou la conservativité vis-à-vis des ontologies sources ;
- la préservation de l'autorité lors de la traduction d'approbations et de délégations ;
- la couverture sémantique de SACM 2.4 Beta 1 ou l'aller-retour XMI/XML sans perte ;
- la conformité des parseurs, sérialiseurs ou mécanismes d'application aux règles du dépôt au modèle Lean ;
- les propriétés temporelles non bornées au-delà de la configuration TLC finie ;
- la pertinence d'importer des définitions CSLib pour une obligation précise.

La suite consiste à étendre le noyau Lean et les fixtures de la non-promotion épistémique à la préservation de la provenance et de la portée. Il faudra ensuite confronter un mapping concret SACM→GovCheck à la sémantique native de SACM, puis auditer les imports CSLib définition par définition, avec commit exact, dépendances transitives et base de confiance. Il ne faut pas généraliser ce petit succès en affirmant que le métamodèle entier est cohérent.
