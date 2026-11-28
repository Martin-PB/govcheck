# Recherche sur l'enforcement à la frontière d'acceptation du dépôt

**Statut :** synthèse de recherche et proposition de conception pour l'issue [#45](https://github.com/Martin-PB/govcheck/issues/45). Ce document n'est ni une politique adoptée, ni une affirmation d'implémentation, ni une modification de configuration d'une forge.

## Résultat exécutif

L'évaluateur GovCheck peut produire un résultat logique fail-closed, mais un résultat logique n'est pas une frontière effective du dépôt. Une barrière obligatoire n'existe que lorsqu'un adaptateur de confiance intercepte chaque chemin d'écriture pertinent vers la cible gouvernée, vérifie le candidat exact et rejette tout résultat non accepté.

L'Architecture 0015 sépare déjà le noyau de vérification, l'enforcement à la frontière du dépôt et l'intégration propre à chaque forge. Cette recherche précise la frontière opérationnelle sans introduire de service MCP hébergé et sans faire d'une forge l'autorité normative.

**Constat central :** pour Git, le mécanisme natif le plus portable et fort est un hook serveur `pre-receive` sur un dépôt bare contrôlé. Les forges SaaS exposent généralement des barrières de merge propres à leur plateforme (rulesets, branches protégées, checks requis) ; elles ne bloquent pas nécessairement les pushes directs si les branches ne sont pas protégées. Pour Pijul, le hook local documenté s'exécute avant `pijul record` ; le manuel officiel ne documente pas de hook distant obligatoire pre-push/pre-receive. Le Nest autorise les pushes directs des utilisateurs habilités ou l'attachement de changements à une discussion. Une barrière Pijul obligatoire exige donc une intégration du remote/serveur contrôlé, pas seulement un hook local. [R-221](../references.fr.md#r-221), [R-222](../references.fr.md#r-222), [R-223](../references.fr.md#r-223), [R-224](../references.fr.md#r-224), [R-225](../references.fr.md#r-225), [R-226](../references.fr.md#r-226)

## 1. Termes à ne pas confondre

- **Vérification :** GovCheck évalue un candidat selon une révision de gouvernance précise et produit des preuves et un résultat.
- **Attestation :** déclaration de provenance liant le résultat au candidat, à la base, à la politique, au vérificateur, aux entrées et aux preuves.
- **Décision d'acceptation :** décision autorisée permettant ou refusant une opération du dépôt. Elle peut consigner un risque accepté sans modifier le résultat de vérification sous-jacent.
- **Enforcement :** un adaptateur du dépôt/de la forge empêche effectivement la mise à jour d'une référence/d'un canal ou le merge tant que la décision ne l'autorise pas.
- **Observation/rapport :** le résultat est affiché ou stocké sans empêcher la publication. Ce n'est pas de l'enforcement.

Les placements ci-dessous sont des **emplacements et capacités différents, pas des niveaux de maturité**.

## 2. Comparaison des emplacements d'enforcement

| Emplacement | Peut-il bloquer la mise à jour cible ? | Frontière de confiance | Limite principale |
|---|---|---|---|
| CLI locale | Non, à elle seule | Processus contrôlé par l'utilisateur | L'utilisateur peut omettre la commande ou appeler directement le VCS. |
| Hook/wrapper client | Seulement la commande cliente interceptée | Machine et configuration contrôlées par l'utilisateur | Le hook peut être absent, remplacé ou contourné ; il ne contrôle pas les autres clients/transports. |
| Barrière de merge de forge | Oui, pour les merges couverts par les règles de branche/ruleset | Politique de la forge et source de check de confiance | Les pushes directs exigent des restrictions séparées ; les administrateurs et acteurs de bypass restent dans le modèle de menace. |
| Hook Git serveur `pre-receive` | Oui, pour les références reçues par ce dépôt | Hook et vérificateur contrôlés par l'administrateur serveur | N'empêche pas les modifications directes des références/fichiers par l'administrateur ; nécessite le contrôle du serveur Git. |
| Workflow Pijul Nest | Les ACL peuvent limiter les auteurs de push ; les discussions facilitent la revue | Permissions du Nest et propriétaire du dépôt | Le hook local documenté ne s'exécute qu'avant `record` ; aucun hook distant conditionnel n'est documenté. |

### 2.1 GitHub

Les rulesets et branches protégées peuvent imposer des checks de statut et des pull requests. Un check requis peut sélectionner une GitHub App comme source attendue ; c'est important car GitHub indique que toute personne ou intégration disposant du droit d'écriture peut définir un statut. Les checks stricts lient la branche à la dernière base ; les checks souples réduisent les reconstructions mais peuvent devenir obsolètes après un merge. Les permissions de bypass doivent être examinées explicitement. [R-221](../references.fr.md#r-221)

Pour GovCheck, un nom de statut requis ne suffit pas. La source attendue doit être une intégration de vérification de confiance, et le résultat doit lier le candidat et la base exacts. Une définition de workflow ou un évaluateur pris sans contrôle dans la branche candidate n'est pas une racine de confiance. Le candidat de merge/test-merge doit être vérifié comme candidat réellement intégré, ou réévalué après formation du résultat de merge.

### 2.2 GitLab

Les branches protégées régissent les permissions de push et de merge. Les checks externes sont liés au HEAD courant de la merge request ; les réponses obsolètes sont rejetées par HTTP 409 et l'authentification HMAC est prise en charge. Cependant, les checks externes en échec ne bloquent pas le merge par défaut : le projet doit activer **Status checks must succeed**. La capacité de checks externes dépend du niveau d'abonnement (Ultimate). [R-222](../references.fr.md#r-222)

### 2.3 Gitea

Les règles de branches protégées Gitea s'appliquent à HTTP(S), SSH, l'éditeur web, l'API et l'auto-merge en arrière-plan. Le serveur rejette les pushes interdits ; les règles couvrent les pushes directs, force-push, approbations et checks de statut requis. Le comportement des administrateurs doit être configuré délibérément. [R-223](../references.fr.md#r-223)

### 2.4 Forgejo

Le guide de sécurité Forgejo Actions avertit que protéger `main` ne suffit pas à rendre l'exécution des workflows digne de confiance : un utilisateur pouvant pousser sur une branche non protégée peut y ajouter un workflow qui s'exécute. Le périmètre d'enregistrement des runners, la provenance des workflows, les exécutions éphémères et l'isolation sont des contrôles distincts de la protection du merge. [R-224](../references.fr.md#r-224)

### 2.5 Serveurs Git contrôlés et dépôts bare locaux

Le hook serveur Git `pre-receive` s'exécute une fois par opération de réception, reçoit tous les identifiants d'objets anciens/nouveaux et les noms complets des références proposées ; un code non nul rejette les mises à jour proposées. C'est le prototype natif le plus fort de frontière de dépôt pour un serveur Git contrôlé ou un dépôt bare local/d'équipe. Un hook client `pre-push` fournit un retour utile, pas une frontière opposable. [R-225](../references.fr.md#r-225)

Le hook et le vérificateur doivent être installés hors de l'arbre candidat et contrôlés par l'administrateur du dépôt/serveur. Le candidat ne doit pas pouvoir remplacer le vérificateur qui l'évalue. Un administrateur serveur ou un processus disposant d'un accès direct au système de fichiers/aux références peut toujours contourner ou remplacer le hook ; la garantie doit expliciter cette hypothèse.

### 2.6 Pijul et le Nest

Le manuel Pijul documente des hooks de dépôt avant `pijul record` et indique qu'actuellement seul ce hook est pris en charge. Le Nest autorise le push direct aux utilisateurs ayant les permissions du dépôt, ou une voie de contribution qui attache les changements à un canal de discussion. [R-226](../references.fr.md#r-226)

Un hook local de record ou un wrapper ne peut pas imposer l'acceptation distante : un autre client peut pousser directement. Une frontière Pijul obligatoire exige un adaptateur remote/serveur contrôlé qui intercepte la mise à jour du canal ou l'application du patch. Le manuel cité ne documente aucun hook général du Nest. Tant que cela n'existe pas, l'intégration Nest doit être décrite comme support ACL/revue, pas comme enforcement GovCheck.

## 3. Contrat proposé d'enveloppe de décision

Les champs suivants sont une cible de conception, pas un schéma adopté :

| Groupe | Sens requis |
|---|---|
| Sujet | Type de VCS, identité du dépôt, identité native du candidat, digest du contenu/arbre/jeu de changements, référence/canal cible |
| Base | Identité native VCS et digest de contenu de la base utilisée |
| Gouvernance | Paquet/révision/digest exacts de gouvernance et profil applicable |
| Vérificateur | Identité, version, digest exécutable, digest de configuration et fondement de confiance |
| Résultat | `PASS`, `FAIL`, `UNKNOWN`, `CONFLICT` ou `ACCEPTED_WITH_RISK` |
| Preuves | Identités/digests, classe de méthode (test, model checking, proof checking, inspection…), portée, hypothèses et limites |
| Décision | Identifiant stable, identité/provenance de l'autorité, date, portée et expiration |
| Acceptation du risque | Enregistrement séparé : motif, affirmation/exigence touchée, portée, risque résiduel, autorité et expiration ; absent sans autorisation explicite |
| Provenance | Signature ou origine authentifiée équivalente, et racine de confiance utilisée par l'adaptateur |

Les identités Git commit/tree et Pijul canal/jeu de changements doivent rester natives au VCS. Un digest de contenu peut aider à comparer, mais ne doit pas être traité comme une équivalence sémantique entre VCS sans correspondance démontrée. L'enveloppe doit être externe au commit/arbre candidat qu'elle atteste, ou conservée dans un journal de gouvernance append-only, afin d'éviter le défaut d'auto-référence identifié dans l'issue #44.

## 4. Sémantique de décision proposée pour le prototype

1. `PASS` n'est produit que si toutes les règles obligatoires applicables réussissent et si les preuves sont fraîches, correctement cadrées et authentifiées par rapport au vérificateur configuré.
2. `FAIL`, `UNKNOWN` et `CONFLICT` bloquent par défaut. Un vérificateur indisponible, une preuve absente, une base/politique obsolète ou une source de statut non fiable donne `UNKNOWN`, pas `PASS`.
3. Une exception ou acceptation de risque explicitement autorisée peut permettre une opération distincte « acceptée avec risque » si la politique applicable le permet. Elle ne doit jamais réécrire le `FAIL` ou `UNKNOWN` sous-jacent en `PASS`.
4. Toute acceptation lie le candidat exact, la base, la révision de gouvernance, le vérificateur et la référence/le canal cible. Tout changement de ces entrées invalide le résultat antérieur.
5. Un bypass est un événement distinct, attribuable et auditable. Ce n'est pas une vérification réussie.
6. Si l'adaptateur ne peut pas intercepter tous les chemins d'écriture pertinents, son résultat est consultatif et ne doit pas être décrit comme un enforcement effectif.
7. Le résultat de merge lui-même doit être vérifié s'il diffère du HEAD revu. Un check vert obsolète sur un autre candidat n'est pas une preuve transférable.

Il s'agit d'un contrat proposé pour formalisation ; il n'adopte pas un nouveau régime d'autorité et ne décide pas qui peut accorder une exception.

## 5. Déclaration des capacités d'un adaptateur

Chaque adaptateur doit déclarer ses capacités au lieu de les laisser implicites :

- `can_block_merge`
- `can_block_direct_push`
- `can_bind_exact_candidate`
- `can_bind_current_base`
- `can_reject_stale_result`
- `can_pin_trusted_verifier_source`
- `can_record_bypass`
- `can_revalidate_merge_result`
- `can_enforce_all_supported_transports`

Un déploiement qui ne bloque pas les pushes directs doit le dire. Une barrière GitHub de merge n'est pas automatiquement une barrière sur les pushes SSH si les rulesets/protections ne les interdisent pas. Une CLI locale n'est pas une barrière obligatoire. Une discussion Pijul Nest n'est pas un hook de politique côté serveur.

## 6. Séquence d'implémentation candidate

1. Formaliser l'enveloppe et les transitions, y compris preuves obsolètes, exceptions, risque accepté et bypass.
2. Fournir un petit exécutable GovCheck local comme noyau de vérification ; aucun serveur MCP hébergé n'est requis.
3. Prototyper un adaptateur Git `pre-receive` pour un dépôt bare contrôlé. Le hook délègue à un vérificateur de confiance installé par l'administrateur et échoue fermé si le résultat est mal formé, absent, obsolète ou non-PASS. Cette recherche ne l'installe pas sur ce dépôt.
4. Ajouter des adaptateurs de forge séparés : rulesets/source App attendue GitHub, branches protégées + checks externes bloquants GitLab, branches protégées Gitea, branches protégées + configuration de workflows/runners de confiance Forgejo.
5. Traiter l'enforcement remote Pijul comme un projet d'adaptateur distinct ; ne pas prétendre que le Nest le prend en charge avant démonstration d'une intégration serveur contrôlée.
6. Vérifier la configuration effectivement déployée et démontrer un rejet dans un dépôt de test isolé avant de déclarer l'enforcement.

### 6.1 Prototype d'adaptateur implémenté

La branche contient désormais un adaptateur Git pre-receive de référence dans [scripts/govcheck-git-pre-receive](../../scripts/govcheck-git-pre-receive), un installateur dans [scripts/install-govcheck-git-pre-receive.py](../../scripts/install-govcheck-git-pre-receive.py), ainsi que des tests unitaires et end-to-end. L'installateur n'accepte qu'un dépôt Git bare, refuse d'écraser un hook pre-receive existant, exige un fichier d'environnement administrateur hors du dépôt en mode 0600 et installe le hook hors de l'arbre candidat.

Pour les références protégées, le hook exige une seule commande exécutable gate hors du dépôt bare et épingle l'identité du dépôt, le digest du fichier exécutable, l'identité du vérificateur ainsi que la révision et le digest exacts de la politique. La commande doit retourner une enveloppe JSON liée aux identifiants d'objets ancien/nouveau exacts et à la référence. Le hook rejette les enveloppes mal formées ou non concordantes ainsi que FAIL/UNKNOWN/CONFLICT ; accepted-with-risk est désactivé par défaut et exige un paramètre explicite de déploiement et un enregistrement de risque structurellement complet. La commande gate de confiance — et non cet adaptateur — doit vérifier l'autorité, la signature, la portée et l'expiration de l'enregistrement de risque. Le digest du fichier exécutable est épinglé, mais sa fermeture runtime/dépendances reste dans la racine de confiance du serveur.

Le test end-to-end utilise un dépôt bare isolé et un faux exécutable gate : un push avec UNKNOWN est refusé et laisse la référence cible inchangée ; la même mise à jour exacte avec PASS est acceptée. Cela démontre que la frontière Git receive peut rejeter une mise à jour. Cela ne démontre **pas** que l'évaluateur GovCheck actuel est déjà un exécutable gate de confiance. Le hook écrit sur stderr et n'ajoute pas encore de décision durable au journal canonique de gouvernance. La référence protégée initiale est initialisée hors bande dans le test ; le hook rejette la création implicite et la suppression d'une référence protégée. Le hook n'est pas installé sur ce dépôt.

## 7. Menaces et limites résiduelles

- **Workflow/vérificateur contrôlé par le candidat :** une pull request peut modifier son propre workflow ou vérificateur. Utiliser un vérificateur installé/épinglé hors de l'arbre candidat ou une intégration de confiance qui exécute un vérificateur protégé.
- **Usurpation de statut :** exiger une source App/service de confiance lorsque la forge le permet ; ne pas faire confiance au seul nom du contexte.
- **Preuve obsolète / TOCTOU :** lier candidat et base ; rejeter les résultats obsolètes ; réévaluer le résultat de merge réel.
- **Push direct / autre transport :** configurer tous les chemins d'écriture, pas seulement le bouton de merge web.
- **Bypass administrateur :** le consigner et le cadrer ; ne pas prétendre protéger contre l'administrateur qui contrôle le hook/ruleset/serveur.
- **Bypass de hook local :** les hooks clients sont uniquement des contrôles de commodité.
- **Lacune remote Pijul :** le hook local `record` n'intercepte pas `pijul push` ; un remote contrôlé est nécessaire.
- **Disponibilité :** si l'évaluateur de confiance est indisponible, retourner `UNKNOWN` ; toute acceptation d'urgence doit être une décision distincte et autorisée de risque.

## 8. Relation avec les documents GovCheck existants

- [Architecture 0015](../architecture/0015-governance-conformance-and-validation-plan.fr.md) sépare déjà noyau de vérification, enforcement à la frontière du dépôt et intégration forge ; ce sont des responsabilités, pas des niveaux de maturité.
- [Architecture 0022](../architecture/0022-governance-capability-audit.fr.md) consigne la frontière d'enforcement et les limites de contournement.
- [Architecture 0023](../architecture/0023-bootstrap-governance-authority.fr.md) conserve l'autorité racine unique et ses risques résiduels explicites.
- [Specification 0007](../specifications/0007-canonical-governance-journal-protocol.fr.md) fournit le protocole logique de journal proposé ; cette recherche ne choisit pas le stockage physique.
- [Issue #44](https://github.com/Martin-PB/govcheck/issues/44) couvre les attestations interopérables et non circulaires.
- [Issue #45](https://github.com/Martin-PB/govcheck/issues/45) porte l'implémentation et la vérification de la frontière d'acceptation.

**Cette recherche ne modifie aucune protection de branche, aucun ruleset, service hébergé, politique d'autorité ni règle normative d'acceptation.**

## 9. Observation actuelle du ruleset GitHub et audit

Une inspection API en lecture seule le 2026-11-27 a trouvé le ruleset de dépôt `Protection Main` (ID `28251664`) :

- l'application est active et le ruleset cible la branche par défaut ;
- les restrictions de suppression et de non-fast-forward sont activées ;
- aucun acteur de bypass n'est configuré et la réponse API indique `current_user_can_bypass=never` ;
- le ruleset ne contient ni exigence `pull_request`, ni règle `required_status_checks`.

L'endpoint de protection de branche a retourné HTTP 403 `Resource not accessible by integration` ; il s'agit d'une limite de permission API et non d'une preuve d'absence de protection. L'endpoint rulesets était accessible en lecture.

La commande en lecture seule `govcheck/forge.py audit-ruleset` vérifie le scope actif de la branche par défaut, l'exigence de PR, les contextes exacts des checks requis, l'identifiant d'intégration/source GitHub attendu, la fraîcheur stricte, la protection contre suppression/non-fast-forward et les acteurs de bypass. Elle ne rapporte que la conformité de configuration et définit toujours `boundary_demonstrated=false` : un refus réel de mise à jour de référence protégée et la fraîcheur du résultat de merge nécessitent des tests distincts.

L'identifiant source GitHub Actions observé sur les checks GovCheck est `15368`. Les contextes CI actuels sont `govcheck-check`, `package-alignment` et `reference-integrity` ; les workflows filtrés par chemins doivent être rendus disponibles de manière cohérente avant de pouvoir exiger les trois checks.

**Cet audit n'a modifié aucun ruleset ni paramètre de protection de branche.**

## 10. Adaptateur local de gate d'acceptation authentifié

L'adaptateur `govcheck/git_acceptance_gate.py` et le point d'entrée `scripts/govcheck-acceptance-gate` relient maintenant le vérificateur de décision signé `acceptance-decision/v1` au protocole existant de pre-receive Git `govcheck.acceptance-decision/v0`.

Pour chaque mise à jour protégée, le gate :
- clone/checkout le candidat exact depuis le magasin d'objets Git du serveur dans un répertoire temporaire ;
- calcule le snapshot candidat et les bindings complets base/candidat ;
- exécute l'évaluateur GovCheck installé avec les entrées détachées de revue/assurance/identité forge ;
- vérifie la décision d'autorité sur les octets exacts du rapport et les bindings candidat/ref/gouvernance/scope ;
- émet une enveloppe de décision v0 liée au dépôt, à la politique et aux identités/digests du vérificateur épinglés.

Le point d'entrée doit être installé hors du dépôt candidat. Le hook pre-receive épingle le digest du fichier exécutable ; la fermeture Python/runtime reste dans la racine de confiance immuable de l'administrateur du serveur. Toute preuve ou configuration manquante produit UNKNOWN et est rejetée par le hook.

**Ce n'est toujours pas une frontière de forge effective :** le hook local n'a pas encore été installé sur un véritable dépôt bare protégé et testé avec des pushes acceptés/rejetés, et le ruleset GitHub n'exige toujours ni PR ni checks de statut. Les tests unitaires de l'adaptateur vérifient le protocole, pas le rejet démontré d'une mise à jour de référence protégée.

## 11. Résultat de l'intégration sur dépôt bare jetable

Le test d'intégration local `test_real_bare_repo_accepts_scoped_risk_and_rejects_stale_decision` installe le véritable hook pre-receive et le point d'entrée gate dans un dépôt Git bare temporaire.

Il a démontré :
- une mise à jour candidate acceptée uniquement avec une décision `accept_with_risk` DSSE signée, liée au rapport/candidat/base/ref/gouvernance/scope exacts ;
- le rejet d'un second candidat réutilisant la décision du premier candidat ;
- le maintien de la référence protégée `main` sur le premier commit accepté après le rejet de la décision obsolète.

Le test utilise des clés Ed25519 synthétiques et une politique de confiance jetable. Il valide le chemin d'exécution local du hook/gate, y compris la matérialisation des objets Git, mais ne constitue ni une installation sur une forge de production ni un test des règles/bypass GitHub.

## 12. Payload du ruleset GitHub et action externe restante

Les noms et la source des checks de la branche main ont été vérifiés directement dans les check-runs GitHub actuels :

- `govcheck-check`
- `package-alignment`
- `reference-integrity`
- identifiant d'intégration GitHub Actions `15368`

`govcheck/forge.py ruleset-payload` génère un ruleset de branche par défaut avec PR obligatoire, zéro approbation de revue (l'autorité configurée reste la décision GovCheck signée), protection contre suppression/non-fast-forward, les trois checks exacts épinglés à l'intégration `15368`, fraîcheur stricte et aucun bypass. Il n'appelle ni ne modifie GitHub.

Générer le payload :

```sh
python3 govcheck/forge.py ruleset-payload \
  --required-checks govcheck-check,package-alignment,reference-integrity \
  --check-source-id 15368 --required-approvals 0 > govcheck-main-ruleset.json
```

Après examen du JSON généré, un administrateur peut mettre à jour le ruleset existant `28251664` avec GitHub CLI :

```sh
gh api --method PUT /repos/Martin-PB/govcheck/rulesets/28251664 \
  --input govcheck-main-ruleset.json
```

Puis auditer la configuration réelle avec `audit-ruleset`. C'est une action utilisateur/administrateur : l'intégration GitHub actuelle de ChatGPT est en lecture seule et ne l'a pas appliquée.

**Important :** ces trois checks protègent actuellement CI/package/intégrité des références ; `govcheck-check` reste en mode report-only. Les rendre obligatoires ne transforme pas à eux seuls GitHub en gate de décision d'acceptation signée. L'adaptateur local pre-receive est le gate d'acceptation pour les transports Git ; un check d'acceptation GitHub de confiance et la configuration réelle du ruleset restent à faire.

## 13. Signer une décision à partir du rapport exact du gate

Le gate peut maintenant écrire les octets sérialisés exacts du rapport vers un chemin externe avec `GOVCHECK_REPORT_OUTPUT_PATH`. Le digest de sortie est le même `evidence_digest` que celui émis dans le protocole de décision ; il n'est pas recalculé à partir d'un objet JSON parsé puis reformatté.

La commande `sign` construit et signe une décision à partir de ces octets exacts :

```sh
python3 -m govcheck.acceptance_decision sign \
  --report govcheck-report.json \
  --repository-uri https://github.com/Martin-PB/govcheck \
  --repository-id 1447286150 \
  --decision-id decision-<identifiant-unique> \
  --result accept_with_risk \
  --rationale "Risque borné accepté par l'autorité de gouvernance." \
  --risk-acceptance risk-record.json \
  --private-key ~/.config/govcheck/authority-ed25519.pem \
  --key-id govcheck-root-authority \
  --openssl /usr/bin/openssl > acceptance-decision.json
```

Pour `accept`, le signer refuse un rapport dont le résultat global n'est pas PASS. Pour `accept_with_risk`, un dossier de risque complet, borné et expirant est obligatoire. La clé privée reste hors du dépôt.

L'enveloppe signée peut être fournie comme artefact détaché ou autre entrée externe à un adaptateur de forge de confiance. Elle ne doit pas être commitée dans le snapshot candidat dont elle autorise le digest de contenu, car cela créerait une liaison circulaire.


## 14. Reçu durable du journal pour une décision d'acceptation vérifiée

Le gate Git local peut, de manière optionnelle, ajouter un événement de décision d'acceptation à un journal GovCheck SQLite explicitement initialisé. Ce reçu local est distinct d'un check de forge et ne constitue pas un reçu de publication.

L'intégration n'est activée que si les trois paramètres suivants sont fournis au processus du gate :

- `GOVCHECK_JOURNAL_DB` : base SQLite située hors du dépôt bare ;
- `GOVCHECK_JOURNAL_SCOPE_ID` : scope exact, identique à `GOVCHECK_SCOPE_ID` ;
- `GOVCHECK_JOURNAL_AUTHORITY_REVISION` : révision d'autorité épinglée dans le genesis du journal.

Avant l'ajout, l'intégration vérifie le journal complet, compare le principal d'autorité du genesis au signataire DSSE authentifié, contrôle les révisions d'autorité et de gouvernance, puis lie l'événement au dépôt, candidat, base, ref, politique, digest du rapport, résultat et dossier de risque. Elle utilise compare-and-append et une clé d'idempotence déterministe dérivée du payload exact de décision. Le reçu commis peut être récupéré avec la commande `receipt` du journal.

Le gate ne crée jamais le genesis. Celui-ci doit être initialisé explicitement hors du dépôt, avec le principal d'autorité authentifié et les révisions d'autorité/de gouvernance épinglées. Si un paramètre du journal est présent mais que la configuration, le genesis ou l'ajout échoue, le gate retourne UNKNOWN et le pre-receive rejette la mise à jour. Sans aucun paramètre de journal, le comportement antérieur (journal optionnel) est conservé ; un déploiement ne doit pas revendiquer une acceptation journalisée avant installation et audit de ces paramètres.

Cet incrément enregistre les décisions d'acceptation vérifiées, pas les tentatives échouées, bypass ou publications effectives de ref. La chaîne de hachage locale n'authentifie pas les acteurs et ne résiste pas à un administrateur privilégié qui réécrit la base. Ces catégories de reçus et le check/ruleset GitHub réel restent à traiter dans #45/#155.


## 15. Journaliser les résultats du gate, y compris UNKNOWN et le rejet

L'intégration journalise désormais chaque évaluation terminée lorsque le mode journal est configuré, et pas seulement les décisions acceptées. Le type d'événement est `govcheck.acceptance.gate-result/v1` ; il inclut les bindings exacts candidat/base/ref/digest du rapport, l'identifiant et le résultat de décision, les bindings politique/gouvernance/scope, le motif et le dossier de risque.

Lorsqu'un principal d'autorité vérifié est disponible, l'événement lui est attribué uniquement après vérification de son égalité avec le principal épinglé dans le genesis du journal. Si la preuve d'autorité est invalide ou absente, l'acteur enregistré est l'attribution locale fixe `system:govcheck-gate` et le payload indique explicitement `unverified-gate-attempt` ; il ne s'agit pas d'une décision humaine authentifiée. Ces tentatives exigent `GOVCHECK_JOURNAL_AUTHORITY_ID` correspondant à l'autorité du genesis.

Le reçu du journal est écrit avant le retour du hook pre-receive. Il atteste donc le résultat/la tentative du gate, pas la mise à jour ultérieure de la ref Git. Un reçu post-receive sera nécessaire pour établir la publication. Si le journal configuré ne peut pas enregistrer le résultat, le gate retourne UNKNOWN et la mise à jour protégée est rejetée.


La section 15 étend le reçu optionnel de décision acceptée décrit à la section 14 : elle enregistre tous les résultats de gate terminés, en distinguant explicitement l'attribution d'une autorité authentifiée de l'attribution locale non authentifiée d'une tentative du gate.


## 16. Reçu de publication post-receive

Un adaptateur local post-receive distinct, `govcheck.git_publication_receipt`, enregistre la mise à jour réelle de la ref protégée après son exécution par Git. Il recherche dans le journal vérifié le dernier événement de gate correspondant exactement au dépôt, à l'ancienne révision, à la nouvelle révision et à la ref. L'événement de publication ne référence la position et le digest de cet événement de gate que si son résultat est accepté et son attribution d'autorité authentifiée.

Si la ref a été mise à jour sans événement d'acceptation authentifié correspondant (par exemple à la suite d'un bypass administrateur), le hook enregistre tout de même `published-without-verified-acceptance` et émet un avertissement. Il s'agit d'une voie de détection/reçu, pas d'un rollback : le hook Git post-receive intervient après la mise à jour et ne peut pas la rejeter. Un échec d'écriture du reçu est donc un incident nécessitant récupération, et non une preuve que la mise à jour a été bloquée.

Installer le wrapper comme `hooks/post-receive` (le relire et lui donner le droit d'exécution dans le déploiement serveur). Configurer la même base de journal externe et le même scope que pre-receive, ainsi que `GOVCHECK_EXPECTED_REPOSITORY_ID`, `GOVCHECK_JOURNAL_AUTHORITY_ID`, `GOVCHECK_JOURNAL_AUTHORITY_REVISION` et `GOVCHECK_GOVERNANCE_REVISION`. L'adaptateur vérifie ces bindings de genesis et ne surveille que les refs correspondant à `GOVCHECK_PROTECTED_REFS` (par défaut `refs/heads/main`). Aucun genesis n'est créé automatiquement.

Cela complète une séquence locale d'événements—résultat du gate avant mise à jour, reçu de publication après mise à jour—pour Git uniquement. Cela ne configure pas GitHub, ne prouve pas l'impossibilité de contourner le ruleset réel et n'implémente pas de frontière distante/serveur Pijul. Ces critères restent explicitement ouverts dans #45.


## 17. Installation sûre du hook post-receive

`scripts/install-govcheck-git-post-receive.py` installe l'adaptateur de reçu de publication dans un dépôt Git bare contrôlé. Il exige un fichier d'environnement administrateur en mode 0600, situé hors du dépôt bare, et une racine du package GovCheck également située hors du dépôt bare. Il vérifie que la cible est bare, copie le lanceur vers un emplacement contrôlé par le serveur, crée un wrapper qui charge l'environnement externe et épingle le chemin du package, puis donne le mode 0755 aux deux fichiers de hook.

L'installateur refuse d'écraser un `hooks/post-receive` ou un helper existant ; il n'enchaîne pas implicitement des hooks arbitraires. Relire et composer explicitement tout comportement post-receive existant avant installation. La commande prépare uniquement un dépôt serveur local ; elle ne modifie pas ce dépôt GitHub ni son ruleset.

Exemple (remplacer les chemins par des emplacements contrôlés par l'administrateur) :

```sh
python3 scripts/install-govcheck-git-post-receive.py \\
  /srv/git/project.git \\
  /etc/govcheck/project-hook.env \\
  /opt/govcheck
```

Le fichier d'environnement doit épingler la base/scope du journal, l'identité attendue du dépôt, l'identifiant/révision d'autorité du genesis, la révision de gouvernance et les refs protégées. Cet installateur ne crée pas le genesis du journal et ne provisionne pas les clés de confiance.


## 18. Paramètres de provenance requis pour l'acceptation Git avec journal

Le binding de provenance Git typé introduit dans l'implémentation du journal exige `GOVCHECK_REPOSITORY_URI` et `GOVCHECK_GOVERNANCE_DIGEST` en plus des paramètres du journal. Le digest de gouvernance doit identifier le package/révision exact de gouvernance gouverné ; ce n'est pas le digest de trust-policy ou de politique d'acceptation. `GOVCHECK_JOURNAL_AUTHORITY_ID` épingle l'autorité du genesis et est requis pour les reçus de tentatives de gate non authentifiées. Lorsque le mode journal est activé, le gate matérialise aussi le snapshot de base, en plus du candidat, afin de calculer les digests de contenu exacts. Des valeurs manquantes ou une provenance invalide produisent UNKNOWN et rejettent la mise à jour pre-receive.
