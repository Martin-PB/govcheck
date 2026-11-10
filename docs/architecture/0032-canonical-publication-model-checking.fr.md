# Architecture 0032 — Rapport de model checking du modèle de publication canonique

**Statut :** élément de preuve par model checking enregistré pour un modèle de conception TLA+ borné. Ce rapport n'est ni une décision d'adoption normative, ni une affirmation d'implémentation, ni une preuve du comportement en production.

## 1. Sujet et objectif

Ce rapport consigne la première exécution réussie de SANY et TLC sur [GovCheckCanonicalPublication](../../formal/tla/GovCheckCanonicalPublication.tla), introduit en parallèle des onze choix d'arbitrage enregistrés dans le [compte rendu de séance 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md).

Le modèle isole un protocole de publication logique borné : évaluer un candidat sur une tête canonique capturée ; autoriser uniquement tant que cette base évaluée reste courante ; publier au moyen d'une action distincte d'ajout/effet ; et rejeter une autorisation dont la base est devenue périmée après une autre publication.

## 2. Modèle et configuration exacts

- **Module TLA+ :** `formal/tla/GovCheckCanonicalPublication.tla`
- **Configuration TLC :** `formal/tla/GovCheckCanonicalPublication.cfg`
- **Identifiant d'objet Git blob — module :** `8daef42732223b10142df1c899fc789361ac35ea`
- **Identifiant d'objet Git blob — configuration :** `c535470350360c7e4e54b7026144a23943affb1a`
- **Commit du dépôt vérifié :** `8c77aeac1ef89e2c6dc7463a65af0f9151fa1bb9`
- **PR :** [#96](https://github.com/Martin-PB/govcheck/pull/96)
- **Exécution du workflow :** [42815445104](https://github.com/Martin-PB/govcheck/actions/runs/42815445104)
- **Job TLC :** `canonical-publication / TLC — GovCheckCanonicalPublication` (ID `129827237434`)

La configuration utilise un univers fini de principaux (deux principaux déclarés, dont un principal racine), trois révisions de gouvernance, deux candidats, trois identifiants d'évaluation et trois identifiants d'autorisation. Le journal logique est borné à trois entrées au maximum, genèse comprise. Les identifiants de publication sont finis. Ces bornes appartiennent à l'abstraction vérifiée et ne constituent pas des affirmations sur un fonctionnement de production non borné.

## 3. Chaîne d'outils et exécution

- **SANY :** 2.1
- **TLC :** 2.19 (8 août 2024, révision `5a47802`)
- **tla2tools :** v1.7.4
- **SHA-256 de tla2tools :** `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88` (somme de contrôle du téléchargement vérifiée par le workflow)
- **Java :** Eclipse Temurin 17.0.21+9
- **Recherche :** en largeur d'abord ; quatre workers sur quatre cœurs
- **Résultat :** l'analyse syntaxique et le traitement sémantique SANY ont réussi ; TLC a indiqué « Model checking completed. No error has been found. »
- **Statistiques de l'espace d'états :** 84 307 états générés ; 56 895 états distincts ; aucun état restant ; profondeur du graphe complet : 9.
- **Estimation de collision des empreintes :** probabilité optimiste (8,5 \times 10^{-11}).

## 4. Invariants et propriété temporelle vérifiés

La configuration TLC a vérifié les propriétés suivantes sans contre-exemple :

1. `TypeOK` — les variables restent dans les types d'état finis déclarés.
2. `UniqueRevisions` — deux entrées du journal ne partagent pas la même identité de révision de gouvernance.
3. `ContinuousPredecessors` — chaque entrée autre que la genèse nomme la révision immédiatement précédente.
4. `OnePublicationPerCanonicalPosition` — deux entrées ne sont pas ajoutées sur le même prédécesseur canonique.
5. `AuthorizationBoundToEvaluation` — une autorisation reste liée à l'évaluation et à sa base capturée.
6. `PublicationIsEffectPoint` — l'identifiant de publication de chaque entrée autre que la genèse figure dans l'ensemble des événements publiés.
7. `PublishedOnlyIfAuthorized` — chaque entrée publiée correspond à une autorisation.
8. `NoStalePublication` — la position de base de l'autorisation d'une entrée publiée correspond à la position de son prédécesseur.

La propriété temporelle `AppendOnly` a également été vérifiée : chaque transition autre qu'une transition de piétinement préserve le préfixe existant du journal et ne raccourcit pas celui-ci.

## 5. Interprétation et limites

Il s'agit d'un élément de preuve par model checking pour le module TLA+, la configuration et la chaîne d'outils finis exacts consignés ci-dessus. Il établit que TLC n'a trouvé aucune violation dans l'espace d'états fini exploré. Il ne prouve **ni** la correction du modèle TLA+, **ni** un théorème, **ni** une implémentation, et n'établit pas le comportement d'exécutions distribuées ou non bornées.

Le modèle ne représente pas encore le stockage durable, la reprise après panne, la convergence des répliques, la provenance indépendante des VCS, le remplacement/comparaison d'évaluateurs, la révocation et la requalification historique, les exceptions, la résolution de unknown/conflict, la restauration du contenu lors d'un rollback, ni le raffinement vers du code exécutable. Son action de publication est un ajout logique abstrait ; elle n'établit ni transaction de base de données ni implémentation de compare-and-swap en production.

Le résultat antérieur de l'[Architecture 0031](0031-first-tlc-governance-applicability.fr.md) correspond à une exécution distincte sur le modèle d'applicabilité initial. Aucun des deux rapports n'adopte les onze choix. Leur statut normatif reste en attente de l'événement d'adoption de gouvernance applicable.

## 6. Provenance et reproductibilité

Le workflow a téléversé l'artefact `tlc-report-GovCheckCanonicalPublication` (ID `13763874296`, empreinte SHA-256 `eeb439ae60fa0c251a349d19cb89e65f7bd55aa856be29f86fd379aea3e83981`). Il contient le rapport SANY, le rapport TLC et la somme de contrôle tla2tools. GitHub indique une expiration de l'artefact au 8 février 2027 ; l'exécution et la révision source restent les références principales.

Ce rapport est lié à [R-05 — TLA+ et TLC](../references.fr.md#r-05) et [R-22 — Sémantiques natives de Git et Pijul](../references.fr.md#r-22). Le catalogue central reste l'autorité de référence.
