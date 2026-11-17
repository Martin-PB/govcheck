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
