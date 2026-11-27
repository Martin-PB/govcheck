# Architecture 0038 — Profil d'implémentation du journal canonique local

**Statut :** profil d'implémentation proposé pour l'issue #155. Il ne constitue pas une adoption normative de la Spécification 0007 et ne prétend pas qu'une base locale soit inviolable ou capable de consensus distribué. **English:** [0038](0038-local-canonical-journal-implementation.md).

## 1. Choix à évaluer

Utiliser la liaison SQLite de la bibliothèque standard Python comme premier backend local du journal, avec un fichier de base par périmètre de journal explicite (ou une base contenant plusieurs périmètres explicitement identifiés). Conserver le contrat logique du journal indépendant de ce backend. L'implémentation est une bibliothèque/CLI embarquée ; elle ne démarre aucun service hébergé, serveur MCP ou démon.

Ce choix répond aux exigences du premier incrément : append compare-and-append transactionnel, écrivains sérialisés, recherche d'idempotence, mise à jour atomique de l'événement/reçu/tête, reprise après crash et tests hors ligne. SQLite fournit des transactions et un mode BEGIN IMMEDIATE qui obtient la transaction d'écriture avant de lire/mettre à jour la tête. Le mode WAL permet aux lecteurs et à un écrivain de progresser simultanément, mais les écrivains restent sérialisés et tous les processus doivent utiliser la base sur le même hôte.

## 2. Alternatives de stockage

| Option | Avantages | Coûts/risques |
|---|---|---|
| Journal fichier append-only JSONL | Lisible par un humain ; export simple ; copie facile | Mise à jour atomique de plusieurs enregistrements (événement, tête, reçu) non portable ; verrouillage interprocessus variable selon l'OS ; écritures partielles, ordre fsync, compactage et reprise après crash deviennent du code spécifique. |
| SQLite (bibliothèque standard) | Embarqué, sans serveur/dépendance ; unicité et compare-and-append transactionnels ; reprise gérée par SQLite ; lecteurs simultanés avec un écrivain en mode WAL | Un seul écrivain à la fois ; WAL limité au même hôte et inadapté aux systèmes de fichiers réseau ; durabilité dépendante des PRAGMA, VFS, système de fichiers et matériel ; un administrateur peut toujours remplacer ou réécrire la base. |

Le premier profil choisit SQLite pour éviter d'inventer un protocole portable de verrouillage/transaction de fichiers. Cela ne désigne pas SQLite comme seul backend possible pour tous les déploiements GovCheck.

## 3. Profil opérationnel SQLite

La première implémentation DOIT :
- ouvrir la base sur un chemin de système de fichiers local et rejeter ou documenter clairement les systèmes de fichiers réseau/partagés non pris en charge ;
- utiliser PRAGMA journal_mode=WAL, PRAGMA synchronous=FULL, PRAGMA foreign_keys=ON et un délai d'attente borné pour les verrous ;
- utiliser explicitement BEGIN IMMEDIATE pour l'append afin d'acquérir la réservation d'écriture avant de comparer la tête attendue ;
- mettre à jour l'événement, l'index d'idempotence, le reçu durable et la tête du périmètre dans une seule transaction SQLite ;
- ne retourner un reçu committed qu'après la réussite de COMMIT ;
- si le client perd la réponse après commit, permettre de retrouver le reçu initial par retry avec la même clé d'idempotence et la requête exacte ;
- rejeter la réutilisation d'une clé d'idempotence avec une requête différente en conflict ;
- rendre les lignes d'événements et de reçus immuables par contraintes/triggers, en traitant ces triggers comme des garde-fous et non comme une frontière de sécurité ;
- vérifier la chaîne complète des digests et les reçus indépendamment de la projection mutable de la tête.

Le mode WAL permet aux lecteurs de continuer pendant un écrivain, mais n'autorise pas plusieurs écrivains simultanés. BEGIN IMMEDIATE rend la contention explicite ; les résultats busy/locked ou les E/S ambigus ne doivent jamais être traités comme des succès. La restriction WAL au même hôte est une contrainte de déploiement. synchronous=FULL demande au VFS SQLite de synchroniser les données de commit ; il ne peut compenser un système de fichiers, contrôleur de stockage ou matériel qui ne respecte pas son contrat de durabilité.

## 4. Profil d'événement canonique et de reçu

L'enveloppe initiale est définie par les schémas du package [journal-event-v1](../../govcheck/formal/schemas/journal-event-v1.schema.json) et [journal-receipt-v1](../../govcheck/formal/schemas/journal-receipt-v1.schema.json). Elle contient :
- un identifiant explicite du périmètre de journal ;
- une position monotone (genesis en position 0) ;
- un identifiant d'événement, un type d'événement et une révision de schéma ;
- un payload et son SHA-256 ;
- le digest de l'événement précédent ;
- l'attribution acteur/principal comme donnée (non authentifiée par ce profil) ;
- une clé d'idempotence facultative pour les append ordinaires ;
- un horodatage UTC informatif (jamais une autorité d'ordonnancement) ;
- un digest d'événement calculé sur l'enveloppe canonique sans le champ digest lui-même.

Le reçu lie le périmètre, la position, l'identifiant d'événement, le digest précédent et le digest d'événement. Il est persisté dans la même transaction que l'événement et la tête mise à jour. Le reçu n'est retourné qu'après le point de commit. Sa reconstruction depuis le journal après un résultat client ambigu est idempotente.

Les événements et reçus sérialisés identifient le profil de canonicalisation par govcheck.jcs-safe-integer/v1. Pour le JSON hachable, utiliser un profil restreint compatible RFC 8785 JCS : chaînes Unicode valides, clés d'objet triées selon l'ordre des unités de code UTF-16, tableaux conservant leur ordre, absence de clés d'objet dupliquées, absence de nombres flottants et entiers limités à l'intervalle des entiers sûrs exactement représentables en IEEE-754. Les rationnels exacts, décimaux et grands entiers sont encodés en chaînes ou en enregistrements typés. Ce sous-ensemble évite un canonicaliseur ad hoc non standard tout en restant implémentable avec la bibliothèque standard.

## 5. Sémantique d'append et de reprise

Algorithme d'append :
1. Valider l'enveloppe de requête et calculer son digest canonique.
2. Démarrer BEGIN IMMEDIATE.
3. Chercher la clé d'idempotence. Même clé et même digest de requête : retourner le reçu initial ; même clé et digest différent : retourner conflict.
4. Lire la tête courante du périmètre et comparer position et digest attendus. Un écart retourne stale ou conflict ; aucun rebase automatique n'est permis.
5. Construire l'événement immuable suivant, le reçu et la nouvelle tête.
6. Insérer événement et reçu, mettre à jour la projection de tête et committer atomiquement.
7. Retourner le reçu durable seulement ensuite.

Si le processus crashe avant le commit, la reprise SQLite ne doit exposer aucun élément de la transaction événement/reçu/tête. Si le commit réussit mais que la réponse est perdue, le retry retourne le reçu initial. Si le client ne peut déterminer si le commit a eu lieu et ne peut retrouver un reçu, le résultat est unknown ; il ne doit pas réessayer avec une nouvelle clé d'idempotence.

Le genesis est une opération de bootstrap explicite exigeant le périmètre, l'identité/révision initiale de l'autorité et la révision initiale de gouvernance. Append DOIT échouer fermé si le genesis est absent ou ambigu. Un nom de branche, une URL de dépôt ou une valeur par défaut de forge ne peut créer implicitement un périmètre ou un genesis.

## 6. Intégrité, autorité et limites

Une chaîne SHA-256 détecte modification accidentelle, suppression, réordonnancement et substitution de payload lorsque le vérificateur dispose d'un point de contrôle fiable. Elle n'authentifie pas l'acteur, ne prouve pas l'autorité, n'empêche pas un administrateur de remplacer la base et de recalculer la chaîne, et n'établit pas la correction sémantique. Les triggers SQLite empêchent la mutation accidentelle via l'API ordinaire, mais ne constituent pas une frontière de sécurité contre un adversaire privilégié.

Le premier profil n'implémente ni signatures, ni gestion de clés, ni consensus distribué, ni écrivains multi-hôtes, ni réplication, ni ordre imposé par une forge/VCS. Un reçu authentifié ultérieur pourra être enveloppé par DSSE dans le cadre de l'issue #44 ; cela ne fait pas de la base un fournisseur d'identité de confiance. Les identités Git/Pijul restent des champs de provenance fournis par les adaptateurs et ne déterminent pas l'ordre canonique du journal.

## 7. Références et documents liés

- [R-230 — Transactions, WAL et durabilité SQLite](../references.fr.md#r-230)
- [R-231 — Schéma de canonicalisation JSON RFC 8785](../references.fr.md#r-231)
- [Spécification 0007 — Journal canonique de gouvernance](../specifications/0007-canonical-governance-journal-protocol.fr.md)
- [Architecture 0035 — Modèle de reprise du journal](0035-canonical-journal-recovery-model.fr.md)
- Issue #155 — Implémentation du journal local
- Liés : #45 frontière d'acceptation, #44 attestations détachées, #86 applicabilité de la révision de gouvernance.

**Il s'agit d'un premier profil d'implémentation proposé. Il n'adopte pas SQLite comme backend universel, ne prouve pas l'autorité d'un acteur et ne revendique pas de protection contre un administrateur privilégié de la base.**
