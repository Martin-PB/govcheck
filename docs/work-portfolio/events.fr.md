# Journal des événements du portefeuille — index français

Le journal canonique des événements est conservé dans [Portfolio event journal](events.md). Il s'agit d'un registre append-only : cette page française est un point d'accès documentaire, et non une copie parallèle du journal. Les événements, leur ordre et leur historique de correction restent définis par le fichier canonique.

## Références mobilisées

- [R-05 — TLA+ et TLC](../references.fr.md#r-05)
- [R-107 — Emplacement et syntaxe des workflows GitHub Actions](../references.fr.md#r-107) : modèles formels et éléments de model checking mentionnés dans les événements.
- [R-22 — Sémantiques natives des VCS](../references.fr.md#r-22) : distinction entre les sémantiques des systèmes de contrôle de version et l'ordre du journal canonique.
- [R-194 — Linéarisabilité](../references.fr.md#r-194) : point de linéarisation des ajouts concurrents.
- [R-195 — Journalisation anticipée ARIES](../references.fr.md#r-195) : distinction entre commit durable et reprise.
- [R-196 — RFC 9110, idempotence](../references.fr.md#r-196) : nouvelle tentative après perte de réponse.

Pour consulter les entrées, leur provenance et leurs limites, se reporter au [journal canonique](events.md).

## Dernier événement enregistré

Le journal canonique a enregistré **WP-EVT-000021** : la PR [#125](https://github.com/Martin-PB/govcheck/pull/125) présente le premier audit bilingue de couverture sémantique du métamodèle et corrige deux failles de typage dans le prototype Lean. Les correspondances opérationnelles sont désormais limitées aux relations dont l'obligation de preuve est explicite ; les propositions approximatives, limitées à la traçabilité ou non prises en charge restent non opérationnelles. Toute cible de nature preuve de théorème exige un terme de preuve de la proposition cible exacte.

La compilation Lean 4.19.0 et l'audit des axiomes ont réussi (36 déclarations auditées, aucune dépendance hors liste autorisée ; les théorèmes explicitement rapportés ne dépendent d'aucun axiome). Les contrôles d'intégrité des références et d'alignement du package ont également réussi. La PR reste ouverte, non fusionnée et fusionnable. L'issue #73 reste ouverte ; aucun métamodèle complet n'est adopté.

Le détail et la provenance restent dans le [journal canonique en anglais](events.md#wp-evt-000021).


## Dernier événement — WP-EVT-000022

La fusion de la PR #125 a été confirmée directement auprès de GitHub (`merged=true`, le 13/11/2026 à 14:23:44 UTC ; commit de fusion `2ae091f55ab177560f0f603e07b47c847c740480`). Le chantier dépendant a donc commencé.

La première source retenue est le XML normatif lisible par machine du métamodèle OMG SACM 2.4 Beta 1 (fichier `ptc/26-05-28`, chemin daté du 04/05/2026 ; [R-197](../references.fr.md#r-197)). La bêta reste en cours de traitement ; SACM 2.3 demeure formelle.

La branche `work/sacm-native-metamodel-ingestion` ajoute un importateur qui conserve les octets XML exacts et produit un index structurel distinct. Il n'interprète pas encore la sémantique MOF/XMI et n'infère aucune correspondance vers GovCheck. Le digest attendu provient de l'audit indépendant [R-128](../references.fr.md#r-128) ; le workflow GovCheck doit encore vérifier ce digest sur le téléchargement officiel réel.

Détail canonique : [journal anglais WP-EVT-000022](events.md#wp-evt-000022).


## Dernier événement — WP-EVT-000023

Le workflow d'ingestion [43443933268](https://github.com/Martin-PB/govcheck/actions/runs/43443933268) a réussi sur le dernier artefact source officiel : cinq tests unitaires réussis, téléchargement OMG, vérification du digest SHA-256 et publication de l'artefact. Le fichier source fait 524 243 octets et son digest est `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`.

L'artefact [sacm-2.4-beta1-source-capture](https://github.com/Martin-PB/govcheck/actions/runs/43443933268/artifacts/14047167094) (ID `14047167094`, rétention 90 jours) contient les trois fichiers : payload XML exact `source.xml`, manifeste `manifest.json` et index structurel `index.json`. Le workflow a été corrigé après une première exécution qui ne publiait que le manifeste et l'index.

Les correspondances typées Claim/Assertion/inférence déjà présentes dans Lean sont recensées dans les deux documents de recherche. Elles restent écrites manuellement et ne sont pas encore dérivées ni validées par le parseur XML. L'inventaire MOF/XMI, le raffinement du parseur, l'import/export d'instances et la conformité SACM restent ouverts.

Détail canonique : [journal anglais WP-EVT-000023](events.md#wp-evt-000023).


## Dernier événement — WP-EVT-000024

La [PR #126](https://github.com/Martin-PB/govcheck/pull/126) est ouverte, non brouillon et fusionnable ; aucune fusion n'a été effectuée. La tête vérifiée au moment de cet enregistrement est `7f3c68f0c710392fa5de5c7a180661f60b0b0500`.

La source officielle retenue est le XML normatif lisible par machine du métamodèle OMG SACM 2.4 Beta 1, fichier `ptc/26-05-28`, révision source `SACM/20260504/SACM2.4_Metamodel.xml` ([R-197](../references.fr.md#r-197), provenance de comparaison [R-128](../references.fr.md#r-128)). Le workflow [43444799397](https://github.com/Martin-PB/govcheck/actions/runs/43444799397) a réussi cinq tests unitaires, le téléchargement officiel et le contrôle du digest sur 524 243 octets : `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`.

L'artefact [sacm-2.4-beta1-source-capture](https://github.com/Martin-PB/govcheck/actions/runs/43444799397/artifacts/14046408461), ID `14046408461`, contient le XML exact `source.xml`, le manifeste et l'index structurel. Les contrôles d'intégrité des références [43444799378](https://github.com/Martin-PB/govcheck/actions/runs/43444799378), d'alignement du package [43444799366](https://github.com/Martin-PB/govcheck/actions/runs/43444799366) et le contrôle GovCheck en mode rapport seul [43444799488](https://github.com/Martin-PB/govcheck/actions/runs/43444799488) ont également réussi.

Les correspondances typées Lean existantes sont recensées dans la recherche bilingue, mais elles restent manuellement encodées et non dérivées du parseur XML. L'inventaire MOF/XMI, le raffinement du parseur, l'interchange d'instances et les preuves de correspondances dérivées de la source restent à réaliser. La bêta 2.4 demeure en cours de traitement ; SACM 2.3 reste formelle. L'issue #73 reste ouverte.

Détail canonique : [journal anglais WP-EVT-000024](events.md#wp-evt-000024).


## Dernier événement — WP-EVT-000025

L'incrément suivant la fusion de la PR #126 produit un inventaire structurel XMI lié à la source officielle OMG SACM 2.4 Beta 1 épinglée par digest. Le parseur `scripts/parse-sacm-xmi.py` recense 1 616 identifiants XMI uniques, 19 packages UML et un profil, 121 classes, 121 associations, 355 propriétés, 167 généralisations, 8 énumérations (37 littéraux), 40 contraintes, 157 commentaires, 2 types de données, 40 expressions opaques et 3 comportements opaques.

Il enregistre 1 434 références explicites : 1 371 références internes résolues, 63 références externes `href` conservées sans résolution et aucune référence interne non résolue parmi les attributs reconnus. La synthèse générée est versionnée dans [`metamodel-inventory-summary.json`](../../formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json). L'inventaire complet sera publié comme artefact du workflow ; il n'est pas ajouté au dépôt comme volumineux fichier généré.

Sept tests synthétiques du parseur réussissent localement et la synthèse produite depuis le payload officiel récupéré correspond à la synthèse versionnée. Le workflow de PR doit encore répéter ces contrôles sur GitHub. Aucune interprétation UML/MOF/OCL, résolution des références externes, preuve de raffinement, réconciliation PDF/XML ou correspondance sémantique vers GovCheck n'est revendiquée. L'issue #73 reste ouverte.

Détail canonique : [journal anglais WP-EVT-000025](events.md#wp-evt-000025).


## Dernier événement — WP-EVT-000026

Le workflow d'ingestion SACM [43451737489](https://github.com/Martin-PB/govcheck/actions/runs/43451737489), vérifié sur le commit `8c0288d5992929089e96596c3f31a8f20ea535f4`, a réussi. Les 12 tests passent : cinq tests de capture source et sept tests d'inventaire XMI. Le téléchargement OMG officiel et le contrôle SHA-256 ont réussi ; l'inventaire complet a été généré et sa synthèse JSON est structurellement égale à la synthèse versionnée.

Résultat : 1 616 éléments XMI identifiés, 121 classes UML, 121 associations, 355 propriétés, 167 généralisations, 8 énumérations (37 littéraux), 40 contraintes, 157 commentaires, 2 types de données, 40 expressions opaques et 3 comportements opaques. Sur 1 434 références, 1 371 sont résolues en interne, 63 références externes `href` sont conservées et aucune référence interne reconnue n'est non résolue.

L'artefact complet [`sacm-2.4-beta1-source-and-xmi-inventory`](https://github.com/Martin-PB/govcheck/actions/runs/43451737489/artifacts/14051746241), ID `14051746241`, digest SHA-256 `01bd32307376baaa0c401b4631d7338bae7f0a999c9d3f94aecc21af5a3c8ae3`, rétention 90 jours, contient la source exacte, le manifeste, l'index d'événements, l'inventaire complet et sa synthèse. Les blobs du parseur, des tests, de la synthèse et du workflow sont identiques à la tête actuelle de PR ; les commits postérieurs ne changent que la documentation et le portefeuille.

La livraison reste structurelle : aucune interprétation UML/MOF/OCL, résolution des références externes, preuve de raffinement du parseur, résolution des conflits PDF/XML, correspondance sémantique vers GovCheck, conformité SACM ou adoption normative n'est revendiquée. L'issue #73 reste ouverte.

Détail canonique : [journal anglais WP-EVT-000026](events.md#wp-evt-000026).


## Derniers événements — WP-EVT-000027 à WP-EVT-000030

## WP-EVT-000027 — Ouverture des chantiers d'audit critique et de recherche décision/risque

Les issues [#130](https://github.com/Martin-PB/govcheck/issues/130) et [#131](https://github.com/Martin-PB/govcheck/issues/131) sont ouvertes. Le chantier réutilise les issues existantes #73, #69, #60, #86/#41, #43/#45/#72 au lieu de créer des doublons. L'addendum bilingue traite la décision comme objet transversal et le risque assumé comme objet de premier rang. Aucune adoption normative ni modification d'autorité n'est impliquée.

Détail canonique : [journal anglais WP-EVT-000027](events.md#wp-evt-000027).

## WP-EVT-000028 — Triage sur sources de la critique externe #129

Un triage bilingue est préparé sur la révision `24760fbfd747fc64f6261b53182f4ed8fdbd4467` nommée par #129. Plusieurs constats sont étayés, d'autres nuancés ; les exécutions Python/TLC/Lean et l'audit d'axiomes restent à reproduire.

Détail canonique : [journal anglais WP-EVT-000028](events.md#wp-evt-000028).

## WP-EVT-000029 — Décision transversale et graphe de traçabilité

L'Architecture 0013 EN/FR remplace la chaîne terminée par une décision d'acceptation par un chemin de traçabilité et une décision transversale de premier rang. Le dossier distingue également les sorties PEAK et les objets candidats d'évaluation/traitement/acceptation du risque. Voir [R-74](../references.fr.md#r-74) et [R-193](../references.fr.md#r-193).

Détail canonique : [journal anglais WP-EVT-000029](events.md#wp-evt-000029).

## WP-EVT-000030 — Distinction du risque assumé PEAK dans l'Architecture 0025

L'Architecture 0025 EN/FR distingue désormais le risque assumé PEAK de l'évaluation, du traitement, du risque résiduel et de l'acceptation autorisée du risque. Voir [R-193](../references.fr.md#r-193).

Détail canonique : [journal anglais WP-EVT-000030](events.md#wp-evt-000030).


## WP-EVT-000031 — Composition Lean d'une chaîne complète de mappings d'éléments probants

Le module Lean de composition des `EvidenceMapping` est exécuté : égalité exacte du modèle intermédiaire, préservation de l'identité/révision de l'artefact, du périmètre, des hypothèses source et de la classe de méthode, composition du pont sémantique, règles épistémiques propres à chaque étape et conservation ordonnée des transformations et pertes déclarées. Le résultat reste une chaîne de deux mappings, sans aplatissement artificiel.

Vérification Lean 4.19.0 et rapport d'axiomes dédié réussis sur la tête de PR #143. Voir [journal anglais WP-EVT-000031](events.md#wp-evt-000031).



## WP-EVT-000032 — Formalisation des sémantiques typées d'incertitude et des objets de risque

Le module Lean distingue les familles de valeurs quantitatives et épistémiques, les états de disponibilité d'une évaluation, les entrées/sorties PEAK et les objets scénario/évaluation/traitement/acceptation du risque. Une acceptation est liée aux révisions exactes du scénario et de l'évaluation et porte autorité, portée, révision de politique et intervalle de validité. Cela ne prouve pas l'autorisation réelle de l'acteur et n'adopte aucun calculateur, score ou politique universelle.

Détail canonique : [journal anglais WP-EVT-000032](events.md#wp-evt-000032).


## WP-EVT-000033 — Vérification du modèle de liaison du contexte des révisions de gouvernance

Le modèle TLA+ lie la révision de politique d'autorité, l'identité/révision de l'évaluateur, l'identité/révision de la spécification et l'identité/révision du profil au contexte de gouvernance capturé pendant l'évaluation et l'autorisation. SANY 2.1 et TLC 2.19 ont réussi : 486 289 états générés/distincts, zéro restant, profondeur 8 ; douze invariants et `AppendOnly` réussis. Il s'agit d'une projection bornée de liaison intermodèle, pas d'une machine à états intégrée ni d'une preuve d'implémentation.

Détail canonique : [journal anglais WP-EVT-000033](events.md#wp-evt-000033).


<a id="wp-evt-000034"></a>
## WP-EVT-000034 — Recherche sur la frontière d'acceptation du dépôt et proposition d'architecture
- **Sujet :** `govcheck.repository.acceptance-boundary-enforcement`.
- **Type d'événement :** `acceptance-boundary-research-proposed`.
- **Enregistré :** 2026-11-17.
- **Artefacts :** [recherche EN](../research/acceptance-boundary-enforcement-2026-11.md) / [FR](../research/acceptance-boundary-enforcement-2026-11.fr.md) ; Architecture 0037 EN/FR ; références [R-221](../references.fr.md#r-221), [R-222](../references.fr.md#r-222), [R-223](../references.fr.md#r-223), [R-224](../references.fr.md#r-224), [R-225](../references.fr.md#r-225), [R-226](../references.fr.md#r-226) ; issue [#45](https://github.com/Martin-PB/govcheck/issues/45).
- **Éléments de preuve plateforme :** rulesets GitHub et source attendue des checks ; branches protégées et checks externes bloquants GitLab ; branches protégées Gitea ; frontières de confiance des workflows/runners Forgejo Actions ; hooks pre-receive Git serveur ; hook local record et voies push direct/discussion du Nest Pijul.
- **Frontière de conception :** noyau de vérification, enforcement à la frontière du dépôt et intégration forge/VCS restent des responsabilités distinctes, pas des niveaux de maturité. La proposition préserve l'exécution par exécutable local, les identités natives VCS, la liaison exacte base/politique/vérificateur, les résultats distincts PASS/FAIL/UNKNOWN/CONFLICT/ACCEPTED_WITH_RISK et les limites explicites de bypass.
- **Limite Pijul :** le manuel cité ne documente qu'un hook local record, pas de hook distant obligatoire de politique. Aucun enforcement Nest n'est revendiqué ; un adaptateur remote/serveur contrôlé est nécessaire.
- **Disposition :** proposition uniquement. Aucune protection de branche, ruleset, service MCP hébergé, régime d'autorité ou politique normative d'acceptation n'a été modifié. Prochain incrément : modèle formel de frontière d'acceptation et prototype isolé de hook Git pre-receive avec tests positifs/négatifs.


<a id="wp-evt-000035"></a>
## WP-EVT-000035 — Proposition de sémantique typée de l'incertitude et du risque assumé terminée
- **Sujet :** `govcheck.decision.assumed-risk.typed-semantics`.
- **Type d'événement :** `typed-risk-specification-candidate-completed`.
- **Date :** 2026-11-27.
- **Issue source :** [#131](https://github.com/Martin-PB/govcheck/issues/131) ; incrément de recherche [PR #142](https://github.com/Martin-PB/govcheck/pull/142) ; incrément Lean typé [PR #150](https://github.com/Martin-PB/govcheck/pull/150), fusionné au commit `3228404631bb565fddd6d0fb5a52f75724fe24dd`.
- **Artefacts :** recherche bilingue `decision-and-assumed-risk-crosscutting-2026-11` ; recherche bilingue `semantic-assurance-and-transition-models-2026-11` ; `formal/lean/GovCheckCoherence/RiskSemantics.lean ; rapport dédié `RiskSemanticsAxiomReport.lean` ; sources de management du risque du catalogue central.
- **Frontières sémantiques :** point/intervalle/distribution probabiliste, appartenance floue, possibilités non déterministes, taux de transition, confiance dans un argument, coût, utilité, priorité et fréquence empirique sont des familles typées distinctes. La disponibilité épistémique préserve NotAssessed, Unknown, NotQuantifiable, NotApplicable, Quantified et Inconclusive.
- **Frontières décision/risque :** les entrées PEAK restent distinctes ; DecisionOutcome conserve Solution et AssumedRisk ; RiskScenario, RiskAssessment, RiskTreatment et RiskAcceptance sont séparés ; l'acceptation lie les révisions exactes du scénario/de l'évaluation et enregistre autorité, portée, révision de politique et intervalle de validité.
- **Éléments probants formels :** 17 théorèmes représentatifs de disjonction des constructeurs et d'intégrité des enregistrements passent sous Lean 4.19.0 ; le rapport dédié ne relève aucune dépendance axiomatique.
- **Limite :** proposition sémantique typée uniquement. Aucun métamodèle normatif, sérialisation canonique, moteur probabiliste/flou, score/calcul universel du risque, politique d'agrégation, optimiseur de traitement ou preuve d'autorité réelle n'est adopté.
- **Disposition :** l'issue #131 est clôturée comme proposition technique terminée. L'adoption normative reste une décision d'autorité distincte ; aucune adoption n'est impliquée ici.


<a id="wp-evt-000036"></a>
## WP-EVT-000036 — Premier incrément du profil d'attestation interopérable fusionné
- **Sujet :** `govcheck.assurance.interoperable-attestation`.
- **Type d'événement :** `in-toto-dsse-profile-increment-merged`.
- **Date :** 2026-11-27.
- **Issue/PR source :** [#44](https://github.com/Martin-PB/govcheck/issues/44), [PR #154](https://github.com/Martin-PB/govcheck/pull/154), fusionnée dans `main` au commit `6556a03d73c8aa2ee4527865b4d12acbc26bc644`.
- **Artefacts :** Spécification 0008 EN/FR ; schéma JSON du prédicat ; `govcheck/attestation.py` standard-library-only ; tests de liaison exacte candidat/base, identités Git/Pijul, résultats à quatre valeurs, structure DSSE PAE/enveloppe et revue indépendante indisponible ; sources de protocole d'attestation du catalogue central.
- **Correction de sécurité :** les JSON de revue intégrés à l'arbre candidat et les noms libres de reviewer ne peuvent plus satisfaire la règle de revue indépendante. La règle reste UNKNOWN tant qu'un vérificateur DSSE détaché et une politique de confiance explicite ne sont pas configurés.
- **Validation :** 143 tests Python, intégrité des références et alignement du paquet passent sur la tête finale de la PR.
- **Limite :** aucune signature/vérification cryptographique, gestion de racines de confiance/clés, association signataire/rôle ou génération du digest canonique du contenu n'est implémentée. Aucune revue indépendante n'est revendiquée ; l'issue #44 reste ouverte.


<a id="wp-evt-000037"></a>
## WP-EVT-000037 — Ouverture du chantier d'implémentation du journal canonique local
- **Sujet :** `govcheck.governance.canonical-journal-local-implementation`.
- **Type d'événement :** `canonical-journal-implementation-work-item-opened`.
- **Date :** 2026-11-27.
- **Issue source :** [#155](https://github.com/Martin-PB/govcheck/issues/155).
- **Fondement :** la Spécification 0007 proposée et le modèle borné de reprise Architecture 0035 sont fusionnés, mais aucune implémentation durable du journal n'existe.
- **Périmètre :** évaluer un stockage embarqué local ; implémenter genesis explicite, append compare-and-append sérialisé, reçus durables, retry idempotent, reprise après crash et vérification de chaîne avec tests hors ligne positifs/négatifs.
- **Frontière :** aucun serveur/MCP hébergé, consensus distribué, cryptographie maison, genesis implicite ou ordre normatif imposé par une forge/VCS. L'intégrité de la chaîne ne prouve ni l'identité d'un acteur ni son autorité.


<a id="wp-evt-000038"></a>
## WP-EVT-000038 — Adaptateur de portefeuille GitHub livré
- **Sujet :** `govcheck.portfolio.forge-native-adapter`.
- **Type d'événement :** `github-forge-adapter-first-backend-completed`.
- **Date :** 2026-11-27.
- **Issue/PR sources :** [#118](https://github.com/Martin-PB/govcheck/issues/118) ; [#119](https://github.com/Martin-PB/govcheck/pull/119), [#120](https://github.com/Martin-PB/govcheck/pull/120), [#121](https://github.com/Martin-PB/govcheck/pull/121), toutes fusionnées.
- **Artefacts :** Architecture 0034 EN/FR ; govcheck/forge.py stdlib-only ; tests de contrat hors ligne ; capacité de bootstrap forge ; README EN/FR.
- **Livré :** IDs de travail stables registry-first, tests d'aller-retour sans perte, inspection read-only des checks/protections, écritures explicites avec token, échecs typés et absence de sémantique d'autorisation par la forge.
- **Limite :** GitHub REST v3 est le seul backend implémenté dans cette issue. GitLab/Gitea/Forgejo, synchronisation bidirectionnelle automatique et écritures Projects v2 restent des chantiers séparés ; l'issue #118 est clôturée pour sa première tranche.


<a id="wp-evt-000039"></a>
## WP-EVT-000039 — Premier backend du journal canonique local fusionné
- **Sujet :** `govcheck.governance.canonical-journal-local-implementation`.
- **Type d'événement :** `local-canonical-journal-first-backend-merged`.
- **Date :** 2026-11-27.
- **Issue/PR source :** [#155](https://github.com/Martin-PB/govcheck/issues/155), [PR #157](https://github.com/Martin-PB/govcheck/pull/157), fusionnée au commit `6ee0b8e64f9f4203a62564b61292b2f4e71e836f`.
- **Artefacts :** Architecture 0038 EN/FR ; bibliothèque/CLI SQLite standard-library ; schémas versionnés d'événement/reçu ; capacités de bootstrap du package ; documentation package EN/FR ; tests hors ligne.
- **Validation :** 167 tests Python, intégrité des références et alignement du package passent sur la tête finale de la PR.
- **Garanties :** genesis explicite, append compare-and-append, reçus durables idempotents, résultats stale/conflict/unknown, reprise transactionnelle SQLite, vérification complète de la chaîne et lectures/appends fail-closed.
- **Limites :** journal local mono-hôte ; aucun consensus distribué, signature, vérification DSSE, authentification d'acteur, preuve d'autorité ou résistance à la réécriture par un administrateur privilégié. Les identités Git/Pijul typées et l'intégration à la frontière d'acceptation restent ouvertes dans #155/#44/#45.


<a id="wp-evt-000040"></a>
## WP-EVT-000040 — Ouverture du chantier de vérification DSSE détachée épinglée
- **Sujet :** `govcheck.assurance.detached-dsse-verifier`.
- **Type d'événement :** `detached-dsse-verifier-work-item-opened`.
- **Date :** 2026-11-27.
- **Issue source :** [#158](https://github.com/Martin-PB/govcheck/issues/158), enfant de #44.
- **Fondement :** la Spécification 0008 définit la structure DSSE/PAE, mais le constructeur n'authentifie pas les signatures. Un vérificateur détaché doit utiliser une politique de confiance épinglée par l'opérateur, hors du contenu contrôlé par le candidat.
- **Périmètre :** fournisseur Ed25519 facultatif délégué à un exécutable OpenSSL épinglé par chemin/digest ; politique et clés publiques épinglées ; association key ID/principal/rôle ; validité/révocation ; liaison exacte candidat/gouvernance ; tests synthétiques positifs/négatifs.
- **Limite :** aucune PKI, horodatage fiable, révocation en ligne, gestionnaire de cycle de vie des clés ou preuve d'identité réelle. Le projet ne dispose toujours que d'un seul contributeur ; aucune revue indépendante n'est fabriquée.
