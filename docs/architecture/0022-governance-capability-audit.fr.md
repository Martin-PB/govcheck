# 0022 — Audit des capacités de gouvernance et lacunes d'implémentation

**Statut :** audit du dépôt et proposition d'implémentation ; ce document n'est ni une politique normative, ni une décision d'adoption, ni une affirmation d'implémentation.  
**Périmètre :** gouvernance dans GovCheck uniquement. Cet audit porte sur l'état du dépôt après la fusion de la PR #19. **English:** [0022](0022-governance-capability-audit.md).

## 1. Conclusion exécutive

GovCheck contient déjà une conception substantielle de la gouvernance : concept de gouvernance canonique, métamodèle, autorité normative et conformité documentaire, responsabilités des acteurs, procédures de gouvernance des versions, enregistrements structurés de décisions de version et de dépendances, ainsi que modèles TLA+ du cycle de vie et de l'assurance.

La lacune principale n'est pas l'absence d'un catalogue ou d'un nouveau vocabulaire abstrait de gouvernance. C'est l'écart entre ces documents de conception et une autorité de gouvernance adoptée, lisible par machine, dont les règles, périmètres, autorités, dérogations et transitions seraient évalués de manière cohérente.

Le dépôt marque lui-même à plusieurs reprises les documents d'architecture et les schémas concernés comme propositions ou artefacts de conception. En particulier, la spécification 0002 indique qu'aucun schéma canonique de gouvernance ni évaluateur n'est implémenté ; l'architecture 0012 ne revendique aucun moteur, parseur, générateur ou mécanisme d'application ; le README des schémas formels indique que ceux-ci attendent l'adoption de la gouvernance et leur intégration à un validateur. Il faut conserver explicitement ces distinctions.

**Conclusion :** ne pas ajouter un catalogue de gouvernance parallèle. Combler progressivement l'écart entre autorité normative et exécution.

## 2. Éléments examinés

Cet audit repose sur les fichiers et modèles de la branche par défaut, et non sur des déclarations commerciales :

- Spécification 0002 — Modèle canonique de gouvernance.
- Architecture 0012 — Autorité normative canonique et conformité documentaire.
- Architecture 0013 — Métamodèle de gouvernance.
- Architecture 0014 — Flux de développement gouverné et responsabilités des acteurs.
- Architecture 0015 — Outil de conformité de gouvernance et plan de validation.
- Architectures 0017–0019 — identité/versionnement des artefacts, autorité d'approbation et évolution du catalogue/manifeste.
- `formal/schemas/version-decision.schema.json`, `dependency-edge.schema.json`, `version-governance-bundle.schema.json` et le README des schémas.
- `formal/tla/GovCheckLifecycle.tla` et `GovCheckAssurance.tla`, avec leurs configurations TLC.
- PR #19, fusionnée dans le commit `8018cf769b17bd89f86e194e5361c57a9a465936`.

Il s'agit d'un audit des sources. Il ne prétend pas que tous les workflows, validateurs ou chemins CI ont été exécutés pendant cet audit.

## 3. Matrice des capacités

| Capacité de gouvernance | Éléments du dépôt | Évaluation |
|---|---|---|
| Source normative canonique | Spécification 0002 et architecture 0012 définissent une autorité unique et des projections contrôlées | **Conçu ; non implémenté/adopté** |
| Règles typées et force normative | Architecture 0013 distingue obligations, interdictions, permissions, invariants et recommandations | **Conçu ; pas de schéma canonique de règles ni d'évaluateur** |
| Applicabilité et profils | 0002/0013 décrivent périmètres, profils et paramètres typés | **Conçu ; résolution des profils non démontrée** |
| Propriété et autorité | 0013/0018 décrivent responsables, autorités, délégations limitées et blocage si l'autorité est inconnue | **Partiellement représenté ; pas de registre d'autorité adopté ni de résolution des délégations** |
| Workflow d'approbation | 0014/0018 décrivent proposant, évaluateur et autorité ; le schéma de décision de version enregistre rôles et fondement d'autorité | **Partiellement représenté ; enregistrement limité aux décisions de version** |
| Séparation des responsabilités | 0014/0018 et le modèle Assurance exigent une revue indépendante dans certains cas | **Partiellement formalisé ; le modèle Lifecycle ne lie pas l'approbation au proposant et au rôle** |
| Dérogations | 0002/0010/0015 décrivent des dérogations limitées, justifiées, autorisées et temporaires | **Conceptuel uniquement ; pas de schéma dédié ni de modèle de transitions** |
| Cycle de vie des politiques | 0012 décrit proposition, validation, approbation, publication et projection ; 0018 couvre les décisions de version | **Procédure décrite ; pas de modèle général du cycle de vie des politiques** |
| Auditabilité | Le schéma de décision de version porte provenance et supersession ; les modèles TLA conservent un historique/état borné | **Partiel ; pas de contrat général d'événements de gouvernance typés et append-only** |
| Dépendances et impact | Schéma dependency-edge et bundle de gouvernance des versions lient des révisions exactes | **Schéma existant ; évaluation sémantique du graphe et de l'impact incomplète** |
| Fraîcheur des preuves | Le modèle Assurance couvre dérive de version, expiration, révocation et invalidation des revues | **Modélisé formellement dans un fixture borné ; intégration au cycle de vie explicitement en attente** |
| Conformité documentaire | L'architecture 0012 définit les exigences de projection et de détection de dérive | **Conçu ; aucun moteur de conformité revendiqué** |
| Gestion des conflits | 0013/0002 exigent des résultats explicites de conflit/indétermination | **Sémantique proposée ; pas d'évaluateur complet de composition des règles** |
| Application et contournement | 0015 distingue audit local et application opérationnelle, avec limites de contournement | **Exigences documentées ; application en production non établie** |

## 4. Lacunes concrètes dans le périmètre formel actuel

### 4.1 Les approbations du cycle de vie ne constituent pas encore un modèle d'autorité de gouvernance

Dans `GovCheckLifecycle.tla`, `Approve(actor)` vérifie l'appartenance à `AuthorizedActors`, et `Accept` vérifie un seuil cardinal. L'état n'identifie ni proposant, ni rôle d'approbation, ni fondement d'autorité, ni délégation, ni identifiant de décision, ni révocation d'approbation. La configuration TLC actuelle autorise les deux acteurs du fixture et exige une approbation. Ce modèle n'établit donc pas la séparation proposant/approbateur ni une autorité limitée à un périmètre.

Ce n'est pas un défaut au regard de l'abstraction restreinte annoncée pour ce modèle ; c'est une limite qu'il ne faut pas confondre avec une autorisation complète de gouvernance.

### 4.2 L'indépendance dans Assurance est fixée au fixture

`GovCheckAssurance.tla` vérifie que le réviseur désigné est autorisé et distinct du producteur. C'est utile, mais le fixture utilise des constantes producteur/réviseur et un graphe de deux claims. Il ne modélise ni attribution dynamique des rôles, ni chaîne de délégation, ni périmètre d'autorité, ni suspension/révocation d'un réviseur, ni changement de politique modifiant les réviseurs requis.

### 4.3 Les dérogations n'ont pas de cycle de vie de première classe

Les documents de conception exigent que les dérogations soient limitées, justifiées, autorisées, temporaires et révocables. Aucun schéma dédié de dérogation ni modèle TLA+ de ses transitions n'a été trouvé parmi les artefacts de gouvernance examinés. Une dérogation ne doit pas être encodée comme un résultat de contrôle réussi ou un commentaire libre.

### 4.4 Le paquet canonique de gouvernance reste conceptuel

La spécification 0002 décrit identité du paquet, identifiants stables des règles, règles typées, applicabilité, relations, paramètres, dérogations, profils et métadonnées de projection, mais laisse explicitement ouverts la sérialisation et le choix de l'évaluateur. Les schémas JSON existants concernent les décisions de version, les dépendances, les bundles, les preuves ou les manifestes de release ; ils ne constituent pas un schéma canonique de paquet de politiques.

### 4.5 La frontière du validateur est volontairement incomplète

La documentation des schémas précise que la validation structurelle n'établit ni l'autorité ni la correction sémantique, et que les décisions de version autorisées restent `unknown` tant que la délégation ne peut pas être résolue à partir d'un registre d'autorité adopté. C'est une posture correcte de blocage par défaut, mais cela signifie que les enregistrements actuels ne suffisent pas encore à décider opérationnellement une approbation.

## 5. Ce qu'il faut reprendre de Knowledge Catalog — et seulement cela

Le motif transposable utile est celui des **métadonnées de gouvernance obligatoires selon le type d'objet**, pas l'architecture produit de catalogue de données de Google.

Pour GovCheck, appliquer ce principe aux objets de gouvernance eux-mêmes :

- Une **règle** doit identifier son identifiant stable, sa force normative, son périmètre, sa source/autorité, sa révision et son état de cycle de vie.
- Un **profil** doit identifier le sujet gouverné, les règles sélectionnées, les paramètres, les règles de composition et l'autorité qui l'a approuvé.
- Une **autorité/délégation** doit identifier l'émetteur, le délégataire, le périmètre, les actions permises, l'intervalle de validité et la révocation/supersession.
- Une **dérogation** doit identifier le sujet exact et les règles écartées, le motif, les mesures compensatoires, l'approbateur, l'expiration et l'état de révocation.
- Une **décision** doit lier acteur/rôle, fondement d'autorité, révision exacte de la politique, révision exacte du sujet, résultat, justification et décision antérieure en cas de remplacement.
- Un **résultat de contrôle** doit lier la révision exacte de la règle, le sujet, la révision de l'évaluateur/outil, les entrées, le résultat, les limites et les preuves.

Les champs obligatoires doivent dépendre du type d'objet et du résultat de la décision. Ne pas introduire de métadonnées arbitraires définies par l'utilisateur qui pourraient affaiblir les contrôles obligatoires. Toute sémantique obligatoire inconnue doit rester indéterminée/bloquante.

## 6. Séquence d'implémentation recommandée

Il s'agit de lots de travail proposés, pas de changements de politique déjà approuvés.

### G0 — Adopter et identifier l'autorité normative

**Décision initiale désormais consignée dans le document 0023 :** un seul principal, `Martin-PB`, détient actuellement l'autorité normative et peut modifier lui-même le régime d'autorité. Aucun pouvoir n'est déduit de la propriété du dépôt, d'une fusion de PR ou de l'état CI. La décision est versionnée, prospective et peut être amendée explicitement par son détenteur.

Il reste à traduire cette décision en enregistrements canoniques, validation et modèle formel. Le document 0023 distingue aussi autorisation normative, revue technique et exécution, et rend explicite l'absence de séparation des personnes pour l'adoption dans le régime initial.

### G1 — Définir les enregistrements canoniques minimaux

Spécifier et valider un ensemble minimal : paquet de gouvernance, règle, profil, autorité/délégation, dérogation, décision et événement de gouvernance typé. Réutiliser les identités stables et la liaison aux révisions déjà définies en 0017–0019. Conserver un format déclaratif ; aucun script de politique arbitraire.

### G2 — Rendre autorité et dérogations décidables

Ajouter une validation inter-enregistrements du périmètre d'autorité, de la validité des délégations, de la compatibilité acteur/rôle, de la séparation des responsabilités, du périmètre/expiration/révocation des dérogations et de leur supersession. Une autorité absente ou ambiguë doit bloquer l'approbation.

### G3 — Formaliser le cycle de vie de la gouvernance

Un premier modèle borné de la chaîne d'amendement de l'autorité racine unique figure désormais dans `formal/tla/GovCheckAuthority.tla` ; il vérifie l'autorisation par l'autorité précédente, la continuité de la chaîne et la liaison de l'autorité/révision courante à la dernière décision. Il est volontairement plus restreint qu'un cycle de vie complet de gouvernance et figure dans la matrice CI formelle. La prochaine extension portera sur proposer → évaluer → autoriser/rejeter → publier → remplacer/révoquer, avec délégation limitée, revue technique indépendante, dérogations expirables et décisions concurrentes/obsolètes. Ajouter des invariants explicites : pas d'auto-autorisation lorsqu'elle est interdite, pas d'autorisation hors périmètre, pas de dérogation expirée/révoquée, pas de mutation rétroactive d'une politique publiée.

### G4 — Relier gouvernance, assurance et application

Faire consommer à l'acceptation du cycle de vie la révision exacte du paquet/profil de gouvernance adopté et les obligations qui en sont résolues. Revalider les mêmes identités juste avant l'application. Garder l'invalidation des preuves et l'invalidation des politiques distinctes mais composables.

### G5 — Tester la sémantique, pas seulement le schéma

Ajouter des vecteurs de conformité positifs et négatifs indépendants du langage : autorité absente, délégation invalide, auto-approbation, mauvais périmètre, dérogation expirée/révoquée, règles contradictoires, applicabilité inconnue, politique remplacée, mise à jour concurrente et approbation obsolète. Une validation JSON Schema réussie n'est pas une validation de gouvernance.

## 7. Non-objectifs explicites

- Ne pas cloner Google Knowledge Catalog ni construire une plateforme générique de métadonnées.
- Ne pas ajouter un second catalogue à côté de `formal/artifacts.json`.
- Ne pas traiter labels, approbations de PR, CI verte, commentaires ou statut d'administrateur du dépôt comme une autorité normative en soi.
- Ne pas transformer tous les enregistrements de gouvernance en artefacts SemVer.
- Ne pas confondre dérogation et preuve, ni dérogation approuvée et preuve de conformité.
- Ne pas revendiquer une application effective parce qu'une validation locale réussit.

## 8. Conclusion de l'audit

GovCheck a déjà conçu une grande partie du vocabulaire de gouvernance et documenté plusieurs principes de sûreté importants. La prochaine capacité substantielle n'est pas un nouveau métamodèle général : c'est un petit paquet canonique de gouvernance, accompagné d'une sémantique explicite de l'autorité/délégation et des dérogations, validée entre enregistrements et formalisée sur son cycle de vie.

La première décision d'implémentation porte donc sur l'autorité et l'adoption de la gouvernance — pas sur le choix d'une interface de catalogue, d'une plateforme d'ontologie ou d'un moteur générique de workflow.


## Références à l'appui de cet audit

- [R-01](../references.fr.md#r-01) : séparation des tâches et gouvernance des accès.
- [R-02](../references.fr.md#r-02) : pratiques traçables de développement sécurisé.
- [R-03](../references.fr.md#r-03) : point d'application pratique et limites de contournement.
- [R-09](../references.fr.md#r-09) et [R-10](../references.fr.md#r-10) : mécanismes de décision de politique, pas des systèmes complets de gouvernance ou d'assurance.
- [R-17](../references.fr.md#r-17) : inspiration limitée aux métadonnées typées et aux relations traçables.
- Contexte et limites : [registre GovCheck des références](../references.fr.md) et [version anglaise](../references.fr.md).


## Références bibliographiques

Références externes citées dans ce document : [R-01](../references.fr.md#r-01), [R-02](../references.fr.md#r-02), [R-03](../references.fr.md#r-03), [R-09](../references.fr.md#r-09), [R-10](../references.fr.md#r-10), [R-17](../references.fr.md#r-17).
