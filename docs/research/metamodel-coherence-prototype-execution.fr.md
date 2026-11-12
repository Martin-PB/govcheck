# Prototype de cohérence du métamodèle — compte rendu d'intégration

**Statut :** contrat de mapping porté par des preuves ajouté au noyau Lean existant ; compilation Lean et audit des axiomes réussis. Expérimentation de compatibilité CSLib vérifiée séparément.  
**Date :** 2026-11-12.  
**Travaux liés :** issue [#73](https://github.com/Martin-PB/govcheck/issues/73), [recherche sur la cohérence du métamodèle](https://github.com/Martin-PB/govcheck/blob/docs/metamodel-decision-dossier-2026-11/docs/research/metamodel-coherence-verification.fr.md), [proposition d'intégration SACM 2.4](../architecture/0026-sacm-24-conformance-and-govcheck-integration.fr.md).

## 1. Stratégie d'intégration

La première tranche de cohérence des éléments probants a déjà été fusionnée dans `main` par la PR #108. L'expérimentation CSLib LTS a été développée sur sa branche empilée par la PR #109. Ce travail étend le paquet `GovCheckCoherence` existant au lieu d'introduire un noyau Lean concurrent ou une seconde définition de la nature des éléments probants.

Le noyau existant conserve trois dimensions indépendantes :

- `EvidenceMethodClass` : méthode ayant produit l'élément probant ;
- `EvidenceKind` : nature épistémique de l'élément (témoignage, résultat de model checking, preuve de théorème, etc.) ;
- `EvidenceStatus` : résultat de la méthode.

Le schéma de production actuel contient la classe de méthode et le statut du résultat, mais aucun champ explicite de nature épistémique ni objet typé de dérivation. Le type Lean constitue donc une interprétation d'assurance supplémentaire, pas une projection sans perte du schéma JSON actuel. Le théorème existant `schema_method_and_status_do_not_determine_epistemic_kind` formalise cette lacune.

## 2. Contrat de mapping porté par des preuves

La compilation intégrée Lean 4.19.0 et l'audit des axiomes ont réussi dans [l'exécution 43213158225](https://github.com/Martin-PB/govcheck/actions/runs/43213158225), commit contrôlé `abc055ce457b4554500d71d4aa0b73ed8ec722d9`. Le rapport explicite indique que les quatorze déclarations de théorèmes auxiliaires/publics du mapping ainsi que le théorème distinct `unknown`/`inconclusive` ne dépendent d'aucun axiome.

Ajout de `formal/lean/GovCheckCoherence/Mapping.lean`, importé par la bibliothèque `GovCheckCoherence` existante et par le rapport d'axiomes des théorèmes.

Le contrat introduit :

- `ArtifactRef` : identité stable, révision exacte, format natif et profil sémantique ;
- `ClaimSemantics` : identifiant stable d'affirmation lié à une proposition Lean ;
- `MappingSubject` : enregistrement probant, affirmation interprétée, artefact de provenance, révision du modèle sémantique, portée et hypothèses ;
- `MappingCoverage` : équivalent, directionnellement sain, partiel, approximatif, traçabilité seule et non pris en charge ;
- `SemanticBridge` : obligations indexées par la couverture (équivalence, implication directionnelle, préservation sur domaine restreint, relation approximative explicitement déclarée, ou déclaration de traçabilité/non-prise en charge) ;
- `KernelCheckedDerivation` : véritable terme de preuve Lean de la proposition cible exacte, accompagné de métadonnées de provenance ;
- `EvidenceMapping` : liaison aux modèles source/cible exacts, préservation de la classe de méthode, règle typée de nature épistémique, préservation de l'identité/révision de provenance, préservation exacte de la portée et conservation des hypothèses sources.

Une nouvelle nature « preuve de théorème » ne peut pas être obtenue en changeant simplement une étiquette. La règle de mapping transporte une nature déjà « preuve de théorème » ou fournit un `KernelCheckedDerivation` contenant un terme de preuve de l'affirmation cible. Le statut du résultat reste indépendant : un nouveau théorème dérivé possède son propre statut et n'hérite pas automatiquement du statut `passed` d'un test source.

Le premier profil exige volontairement l'égalité exacte des portées. Il ne définit pas encore d'ordre partiel sur les portées et n'autorise pas leur restriction. Les champs `premises`, `assumptions`, `kernelIdentity` et `kernelVersion` d'une dérivation sont actuellement des métadonnées ; le terme de preuve lui-même est vérifié par le noyau, mais ces métadonnées ne sont pas encore reliées mécaniquement à sa fermeture transitive de dépendances.

## 3. Alignement des statuts d'éléments probants

Le schéma d'éléments probants distinguait déjà `unknown` et `inconclusive` dans le modèle TLA d'assurance, mais l'énumération JSON des statuts n'exposait pas `unknown`. Le schéma, sa copie dans le paquet gouverné, la documentation bilingue des statuts et une fixture synthétique incluent désormais `unknown`.

- `unknown` : aucun résultat déterminé n'est disponible à partir des entrées actuelles ;
- `inconclusive` : une méthode a été exécutée, mais n'a établi ni réussite ni échec ;
- `stale` : ce n'est pas un statut de résultat ; il est dérivé séparément des dépendances de révision, de l'expiration et de l'invalidation.

Le type Lean `EvidenceStatus` inclut désormais `unknown`. Une fixture synthétique `evidence-record-unknown.example.json` existe aux niveaux méta et paquet.

## 4. Cycle de vie temporel : réutiliser le modèle existant

Aucun modèle de fraîcheur redondant n'a été ajouté. Le modèle existant `formal/tla/GovCheckAssurance.tla` couvre déjà les résultats `Unknown`, les éléments périmés en raison d'une divergence de révision, l'expiration et la révocation, le statut des affirmations, la revue indépendante, l'acceptation et les instantanés de dépendances acceptées. Ses invariants `AcceptedImpliesSupported` et `AcceptedDependencySnapshotCurrent` constituent la base temporelle existante appropriée.

TLC fournit des éléments de model checking borné pour le modèle fini configuré. Il ne prouve pas la liaison sémantique statique entre deux ontologies ; c'est le rôle du contrat Lean de mapping.

## 5. Résultat de compatibilité CSLib

Un paquet isolé dans `formal/cslib-compat/` a été compilé contre le commit CSLib exact `70e25828d89a3916e41c9d84cfffd7e6093bb1a0`, Lean `4.36.0-rc2` et la révision Mathlib épinglée par CSLib. [L'exécution 43210543930](https://github.com/Martin-PB/govcheck/actions/runs/43210543930) a terminé 1 779 tâches de compilation et contrôlé l'API de modèle/satisfaction BTL ainsi que `Step` et `LeadsTo` sur séquences oméga.

Cela établit uniquement la compatibilité de compilation et d'API dans un paquet isolé. Cela ne prouve pas de raffinement sémantique GovCheck↔CSLib et ne modifie pas la chaîne d'outils Lean 4.19.0 du noyau existant. Voir l'[audit de compatibilité CSLib](cslib-compatibility-audit.fr.md) / [version anglaise](cslib-compatibility-audit.md).

## 6. Tranche sémantique SACM 2.4 Beta 1 qualifiée par la vue source

Une première tranche qualifiée par la vue source est désormais formalisée dans `GovCheckCoherence.SACM24` et documentée dans l'[étude de mapping SACM 2.4](sacm24-claim-inference-mapping.fr.md) / [version anglaise](sacm24-claim-inference-mapping.md). L'audit indépendant Assurance Forge (R-128) identifie des contradictions texte/XML et l'absence d'un contrat stable d'échange d'instances natives ; voir le [rapport sur les risques d'interopérabilité](sacm24-beta1-interoperability-risk.fr.md). Le module Lean distingue désormais les vues texte PDF et métamodèle XML, préserve `needsSupport` et `byRule` sans accepter l'une dans la mauvaise vue, distingue `gid` de `elementId`, ne promeut pas `axiomatic` en preuve de théorème, lie les sujets explicites des Claim aux révisions exactes des modèles et donne des liaisons formelles correctement orientées pour les inférences necessary, sufficient, necessaryAndSufficient et collective. Le type `probable` ne possède aucun constructeur d'implication classique ; `byRule` exige un terme de preuve formel. L'interprétation propositionnelle de la source reste fournie par l'autorité et n'est pas déduite du texte en langage naturel. Les nouveaux théorèmes SACM attendent l'exécution Lean/audit des axiomes en cours.

## 7. Obligations restantes

Le contrat actuel ne prouve pas encore :

- que les sémantiques sources de SACM 2.4 Beta 1, OWL ou SEON/ReqON sont correctement interprétées par les propositions Lean fournies ;
- que de vrais parseurs, sérialiseurs ou adaptateurs d'import/export ne construisent que des valeurs `EvidenceMapping` valides ;
- l'extension conservative/non-interférence pour les ontologies sources ;
- la composition des mappings et la préservation transitive des hypothèses/provenances ;
- la restriction de portée selon un ordre formellement défini ;
- la liaison des métadonnées de dérivation à la fermeture complète des dépendances du terme de preuve ;
- la préservation de l'autorité et des délégations à travers des mappings réels.

La prochaine tranche concrète ne doit pas supposer un import XMI : il faut d'abord épingler et comparer les quatre artefacts OMG Beta 1 officiels, formaliser les autres conflits de multiplicité et d'héritage PDF/XML, puis obtenir un format d'instance portable et des fichiers externes. Seulement ensuite lier des relations `AssertedInference`/`AssertedEvidence` concrètes, en préservant les identités source/cible et les indicateurs de contre-preuve. Il ne faut pas généraliser les petits résultats de compilation Lean et CSLib en affirmant que tout le métamodèle est cohérent.
