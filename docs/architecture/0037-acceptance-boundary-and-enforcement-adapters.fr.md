# 0037 — Frontière d'acceptation du dépôt et adaptateurs d'enforcement

**Statut :** proposition pour l'issue [#45](https://github.com/Martin-PB/govcheck/issues/45). Non adoptée comme politique normative. Ce document ne modifie aucune configuration de forge ni règle de protection de branche.

## 1. Problème

GovCheck peut évaluer un candidat et produire un résultat, mais ce résultat ne bloque pas à lui seul une mise à jour du dépôt. Un workflow report-only, une invocation de CLI locale ou un hook client ne constitue pas une frontière d'acceptation effective si un contributeur peut pousser le même candidat par un autre chemin.

Ce document précise les trois responsabilités déjà distinguées par l'Architecture 0015 :

1. **Noyau de vérification :** évalue les preuves d'un candidat exact selon une révision de gouvernance.
2. **Enforcement à la frontière du dépôt :** empêche une opération protégée du dépôt en l'absence de décision d'acceptation valide.
3. **Intégration forge/VCS :** fait correspondre les identités natives VCS et les capacités propres à chaque plateforme au contrat de frontière.

Ce sont des responsabilités distinctes, pas des niveaux d'assurance ou de maturité. GovCheck reste l'autorité normative de gouvernance ; une forge est un mécanisme d'application, pas la source de la sémantique de gouvernance.

## 2. Contraintes de conception

- Un petit exécutable local reste le noyau de vérification. Aucun serveur MCP hébergé n'est requis.
- La frontière d'enforcement est l'opération de dépôt/dépôt de changement, pas le harnais de l'agent de codage.
- Le contrat logique doit être indépendant du VCS, mais l'identité du candidat reste native au VCS. Les identités commit/tree Git ne doivent pas être confondues avec les identités canal/jeu de changements Pijul sans correspondance sémantique démontrée.
- Un hook local est coopératif tant que toutes les écritures pertinentes ne sont pas interceptées par une frontière de dépôt/serveur contrôlée.
- Les checks de statut de la plateforme sont des signaux d'adaptateur ; le seul nom d'un contexte de statut n'est ni une preuve ni une autorité.
- Les tests, résultats de model checking, résultats de proof checking et inspections conservent leurs classes de méthode distinctes.
- FAIL, UNKNOWN et CONFLICT ne sont pas PASS. Une acceptation autorisée du risque reste une décision distincte et ne doit pas réécrire le résultat sous-jacent.
- Les preuves obsolètes sont invalides lorsque le candidat, la base, la révision de gouvernance, le vérificateur ou les entrées pertinentes changent.
- L'autorité de bypass et ses limites doivent être explicites, attribuables et auditables.
- Cette architecture ne configure pas la protection GitHub du dépôt GovCheck actuel et n'adopte pas de nouveau régime d'autorité.

## 3. Enveloppe proposée de décision d'acceptation

L'adaptateur doit consommer une enveloppe de décision structurée, produite par le vérificateur local ou par une exécution côté serveur de confiance. La sérialisation exacte reste ouverte.

| Groupe | Liaison requise |
|---|---|
| Sujet du dépôt | Identité du dépôt, type de VCS, référence/canal cible |
| Candidat | Identité native du candidat et digest du contenu/arbre/jeu de changements |
| Base | Identité native de la base et digest de contenu utilisés pour l'évaluation |
| Gouvernance | Paquet, révision, digest de gouvernance exacts et profil applicable |
| Vérificateur | Identité, version, digest exécutable, digest de configuration et fondement de confiance |
| Résultat | PASS, FAIL, UNKNOWN, CONFLICT ou ACCEPTED_WITH_RISK |
| Preuves | Identifiants/digests, classe de méthode, portée, hypothèses et limites |
| Décision | Identifiant stable, identité/provenance de l'autorité, date, portée et expiration |
| Acceptation du risque | Enregistrement autorisé distinct, le cas échéant ; jamais inféré d'un PASS |
| Provenance | Origine authentifiée/signature ou frontière d'exécution locale de confiance |

L'attestation ne doit pas être intégrée au commit candidat dont elle prétend attester le hash final. Elle doit être stockée hors bande ou dans un journal append-only gouverné séparément. Cela traite directement le problème d'auto-référence suivi par l'issue #44.

L'identité du candidat dépend de l'adaptateur. Pour Git, l'adaptateur lie l'identifiant complet de l'objet et l'arbre/commit exact évalué. Pour Pijul, il lie l'identité native du canal et du jeu de changements. Un digest de contenu est complémentaire ; il n'établit pas d'équivalence sémantique entre VCS.

## 4. Sémantique d'acceptation

Le contrat par défaut suivant est proposé pour formalisation et tests ; son adoption reste ouverte.

- **PASS :** toutes les règles obligatoires applicables réussissent, les preuves sont fraîches et cadrées sur le candidat/la base/la politique exacts, et la source du vérificateur est fiable.
- **FAIL :** une ou plusieurs affirmations obligatoires sont contredites ou des exigences échouent.
- **UNKNOWN :** les preuves requises sont absentes, obsolètes, indisponibles, non authentifiées ou hors de la compétence du vérificateur.
- **CONFLICT :** des preuves incompatibles ou un état concurrent non résolu empêchent un résultat déterminé.
- **ACCEPTED_WITH_RISK :** une décision autorisée distincte permet une opération bornée malgré un FAIL/UNKNOWN/CONFLICT sous-jacent, avec motif, portée, affirmations touchées, autorité, risque résiduel et expiration consignés.

Comportement par défaut : seul PASS est accepté automatiquement. Les autres résultats bloquent, sauf si une exception/acceptation de risque autorisée par la politique permet une voie distincte « acceptée avec risque ». Cette voie ne doit jamais requalifier UNKNOWN en PASS. Une panne de la barrière est UNKNOWN, pas un succès.

La base d'autorité racine unique de l'Architecture 0023 reste inchangée. Cette proposition n'invente pas un second approbateur et ne prétend pas qu'un nom libre de reviewer prouve une autorité indépendante.

## 5. Adaptateurs d'enforcement

| Adaptateur | Frontière effective | Configuration/confiance requise | Limite résiduelle |
|---|---|---|---|
| CLI locale | Aucune à elle seule | Évaluation du candidat local exact | L'utilisateur peut l'omettre ou appeler directement le VCS. |
| Hook/wrapper client | Intercepte un chemin client | Hook installé et vérificateur fiable | Les autres clients/transports et administrateurs locaux peuvent le contourner. |
| GitHub | Merge vers des références protégées | Ruleset/branche protégée, PR/check requis, source App de confiance, check de base actuelle, bypass examiné | Les pushes directs doivent aussi être bloqués ; confiance App/workflow et bypass administrateur subsistent. |
| GitLab | Merge request vers des références protégées | Branche protégée + « Status checks must succeed » ; check externe lié au HEAD courant et authentifié | Checks externes dépendants du niveau d'abonnement et nécessitant un endpoint de service. |
| Gitea | Push/merge vers références protégées | Règle de branche protégée, contextes requis, comportement administrateur configuré | Propre à la plateforme ; la source fiable du statut doit encore être établie. |
| Forgejo | Push/merge vers références protégées et exécution de workflows de confiance | Protection de branche + accès en écriture contrôlé, périmètre runner, provenance et isolation des workflows | Protéger main seul n'empêche pas l'exécution de workflows arbitraires depuis des branches non protégées. |
| Git pre-receive | Chaque opération de réception mettant à jour des références protégées | Hook serveur et vérificateur installés hors de l'arbre candidat ; décision fail-closed | L'administrateur serveur/accès direct au système de fichiers peut contourner ou remplacer le hook. |
| Remote Pijul | Application du canal/patch | Adaptateur remote/serveur contrôlé interceptant l'opération distante | Le manuel/Nest cité ne documente que des hooks locaux record, pas de hook de politique distante obligatoire. |

Un déploiement doit déclarer ses capacités au lieu de les laisser implicites :

- can_block_merge
- can_block_direct_push
- can_bind_exact_candidate
- can_bind_current_base
- can_reject_stale_result
- can_pin_trusted_verifier_source
- can_record_bypass
- can_revalidate_merge_result
- can_enforce_all_supported_transports

Si un adaptateur ne peut pas intercepter tous les chemins d'écriture pertinents, il ne produit qu'un statut consultatif. Il ne doit pas revendiquer un enforcement effectif.

## 6. Prototype de frontière serveur Git

Le premier adaptateur de référence devrait être un hook Git pre-receive pour un dépôt bare contrôlé :

1. Git fournit chaque tuple old_oid, new_oid et ref_name proposé.
2. Le hook ne traite que les références explicitement protégées ; suppression et création initiale non configurée échouent fermé.
3. Il invoque un exécutable vérificateur installé par l'administrateur. Le vérificateur et la politique sont hors de l'arbre candidat et épinglés par l'opérateur du serveur.
4. Le vérificateur retourne une décision structurée liée aux identifiants d'objets ancien/nouveau exacts, à la référence, à la révision de gouvernance et à l'identité du vérificateur.
5. Le hook valide l'enveloppe et retourne un code non nul si les preuves sont absentes, mal formées ou obsolètes, ou si le résultat est FAIL, UNKNOWN ou CONFLICT.
6. Un résultat ACCEPTED_WITH_RISK n'est accepté que si le déploiement active explicitement cette voie et si l'enveloppe contient un enregistrement autorisé, borné et non expiré d'acceptation du risque. Il reste accepté avec risque, jamais PASS.
7. Le hook journalise l'identifiant de décision et le résultat. Si une mise à jour de référence protégée de l'opération est rejetée, Git rejette l'opération de réception.

Le prototype est implémenté dans scripts/govcheck-git-pre-receive avec l'installateur scripts/install-govcheck-git-pre-receive.py. Il consomme une enveloppe JSON govcheck.acceptance-decision/v0 et exige que l'opérateur serveur épingle hors du dépôt candidat le chemin du seul exécutable gate, son digest SHA-256, l'identité du vérificateur et la révision de politique. Le fichier d'environnement doit être hors du dépôt bare et en mode 0600 ; l'installateur refuse d'écraser un hook pre-receive existant. Le hook rejette les résultats absents/mal formés/non concordants/obsolètes, FAIL, UNKNOWN et CONFLICT. Accepted-with-risk est désactivé par défaut ; s'il est activé, l'exécutable gate de confiance doit lui-même vérifier l'autorité, la signature, la portée et l'expiration de l'enregistrement de risque. Le hook ne vérifie que sa complétude structurelle.

Le test d'intégration crée un dépôt bare isolé, initialise sa référence protégée initiale hors bande, puis démontre qu'un push retournant UNKNOWN est rejeté et qu'un push retournant PASS pour le tuple ancien/nouveau/référence exact est accepté. Le fixture utilise un faux exécutable gate de confiance : il prouve la mécanique de la frontière Git receive, pas la correction sémantique de l'évaluateur GovCheck actuel. Le hook écrit sa décision sur stderr ; ce n'est pas encore un journal de gouvernance canonique append-only. La fermeture de confiance inclut les dépendances de l'exécutable épinglé et le bypass administrateur. Rien n'est installé sur le remote GovCheck.

## 7. Frontière Pijul

Pijul ne doit pas être forcé dans la sémantique des commits Git. Le hook local record documenté n'intercepte pas pijul push ; le Nest propose le push direct via ACL ou l'attachement à une discussion. Par conséquent :

- un wrapper local est consultatif et contournable ;
- la discussion/revue Nest n'est pas équivalente à un hook GovCheck conditionnel côté serveur ;
- l'enforcement obligatoire exige un adaptateur remote/serveur Pijul contrôlé qui valide le canal/jeu de changements natif avant application ;
- tant que cet adaptateur n'existe pas et n'a pas été testé, la déclaration de capacité Pijul doit indiquer can_block_direct_push = false pour le Nest et ne pas revendiquer l'enforcement.

## 8. Hypothèses de confiance et bypass

- Les fichiers de workflow/vérificateur contrôlés par le candidat ne sont pas une racine de confiance. Utiliser un vérificateur épinglé hors de l'arbre candidat ou une intégration de confiance séparée.
- L'usurpation de statut est réduite par l'identité de source attendue lorsque la plateforme le permet.
- Un résultat est invalidé si le candidat, la base, la révision de gouvernance, le vérificateur ou les preuves pertinentes changent.
- Les commits de merge queue/test-merge doivent être évalués comme candidat réel à intégrer.
- Les administrateurs qui contrôlent les règles de branche, hooks, fichiers serveur ou vérificateur restent des acteurs de confiance/capables de bypass. Leurs actions doivent apparaître comme événements de bypass/override, pas comme une vérification réussie.
- L'enforcement local/client ne peut pas être qualifié d'obligatoire si le propriétaire du dépôt peut contourner le client.

## 9. Plan de formalisation et de vérification

Le modèle de frontière d'acceptation doit vérifier :

- aucun PASS à partir de FAIL/UNKNOWN/CONFLICT ;
- liaison exacte candidat/base/gouvernance/vérificateur ;
- invalidation des preuves obsolètes après changement de base ou politique ;
- distinction entre acceptation du risque et PASS ;
- absence de bypass silencieux ;
- publication seulement après décision de barrière valide en mode enforced ;
- le mode advisory peut être contourné, mais la publication résultante est marquée uncontrolled.

L'entrée de confiance du modèle est une hypothèse, pas un théorème sur les identités réelles ou l'intégrité binaire. Un test d'intégration séparé doit exercer l'adaptateur Git pre-receive avec un faux vérificateur : PASS accepté ; FAIL/UNKNOWN/malformé/non concordant/obsolète rejeté ; accepted-with-risk rejeté par défaut et accepté seulement lorsqu'il est explicitement activé avec un enregistrement complet.

## 10. Décisions ouvertes

- Sérialisation exacte de l'enveloppe et schéma de signature/racine de confiance.
- Autorité habilitée à accepter le risque et possibilité ou non de déroger à UNKNOWN pour certaines classes d'affirmations.
- Choix entre GitHub App, workflow réutilisable protégé ou autre fournisseur de statut de confiance.
- Versions et profils de déploiement GitLab/Gitea/Forgejo pris en charge.
- Inclusion d'un adaptateur serveur Pijul contrôlé et mode d'authentification du vérificateur côté serveur.
- Autorisation, expiration et réconciliation du bypass d'urgence dans le journal canonique.

Aucun de ces choix n'est adopté par cette proposition.

## 11. Références et documents liés

Les sources externes des plateformes sont cataloguées dans [R-221–R-226](../references.fr.md#r-221). Documents liés : [Architecture 0015](0015-governance-conformance-and-validation-plan.fr.md), [Architecture 0022](0022-governance-capability-audit.fr.md), [Architecture 0023](0023-bootstrap-governance-authority.fr.md), [Specification 0007](../specifications/0007-canonical-governance-journal-protocol.fr.md), [synthèse de recherche](../research/acceptance-boundary-enforcement-2026-11.fr.md), [issue #45](https://github.com/Martin-PB/govcheck/issues/45).

**Ce document est une proposition. Il n'active aucune protection de branche, n'installe aucun hook, ne choisit aucune forge et n'adopte aucune politique normative d'acceptation.**
