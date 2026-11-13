# Spécification 0007 — Protocole du journal canonique de gouvernance et des adaptateurs VCS

**Statut :** contrat sémantique proposé à la revue ; il ne constitue ni une adoption normative ni une affirmation d'implémentation. Aucune base de données, sérialisation, suite cryptographique, produit de consensus ou forge n'est sélectionné. **English:** [0007](0007-canonical-governance-journal-protocol.md).

## 1. Objet et périmètre

Cette spécification précise la Spécification 0006 en définissant les obligations de protocole autour du journal logique canonique de gouvernance : ajout, compare-and-append, commit durable, reprise après panne, nouvelle tentative idempotente, observation de répliques et réconciliation des adaptateurs VCS.

Le journal canonique est la seule autorité pour l'ordre normatif des événements dans son périmètre de gouvernance. Git, Pijul et les autres VCS/forges transportent le contenu des candidats et des observations de provenance ; leur ordre natif, topologie de branches, horodatages, ordre de fusion ou état du service d'hébergement n'allouent aucune position normative.

Il s'agit d'un contrat sémantique indépendant des technologies. Le moteur de stockage, le format filaire, l'algorithme de hachage/signature, l'implémentation de consensus, le protocole réseau, le VCS et la forge restent des choix d'implémentation exigeant des éléments de preuve et une analyse de compatibilité séparés.

## 2. Termes et identités

- **Périmètre du journal :** domaine d'autorité dans lequel une séquence canonique unique est ordonnée.
- **Tête du journal :** dernière position commise et son identité d'intégrité (par exemple un condensat ou un jeton immuable équivalent).
- **Événement de journal :** enregistrement immuable commis à une seule position.
- **Requête d'ajout :** événement proposé, accompagné de son prédécesseur/tête attendu et de son identité d'idempotence.
- **Reçu de commit :** élément durable établissant qu'un événement occupe une position canonique donnée.
- **Observation VCS :** révision native Git/Pijul/autre VCS, patch, changement, référence, canal, événement de forge ou objet observé par un adaptateur.
- **Adaptateur :** composant traduisant les observations natives VCS/forge en identités de candidat/provenance ; il ne fait pas autorité sur l'ordre normatif.
- **État matérialisé :** vue dérivée ou projection reconstruite à partir des événements commis du journal.
- **Résultat de commit inconnu :** l'appelant ne peut déterminer si une requête a franchi le point de commit durable.

L'identifiant d'événement, la clé d'idempotence, la position du journal, le condensat du payload, la révision native VCS, l'identité du candidat, l'identifiant d'évaluation, l'identifiant d'autorisation et l'identité de révision de gouvernance sont des champs distincts et MUST NOT être confondus.


Le périmètre du journal MUST posséder une identité stable et non ambiguë. Cette spécification ne décide pas si un périmètre correspond exactement à un dépôt, couvre plusieurs dépôts relevant d'un même domaine d'autorité ou suit une autre frontière de gouvernance. Cette correspondance MUST être explicitement définie avant qu'un déploiement traite un journal comme canonique ; une URL de VCS ou de forge MUST NOT définir implicitement ce périmètre.

## 3. Identité du journal et enveloppe d'événement

Un périmètre de journal MUST posséder une séquence logique canonique unique. Chaque événement commis MUST comporter :
1. un identifiant d'événement stable, unique dans le périmètre ;
2. une position canonique strictement croissante ;
3. la position et l'identité d'intégrité exactes du prédécesseur, sauf pour la genèse ;
4. un type d'événement et une identité/révision de schéma ;
5. une identité/intégrité du contenu liée au payload exact de l'événement ;
6. une attribution d'acteur/principal et de provenance suffisante pour la politique d'autorité applicable ;
7. les identités pertinentes du candidat, de l'évaluation, de l'autorisation, de la publication ou de la révision de gouvernance ;
8. une clé d'idempotence pour les requêtes d'ajout réessayables (les enregistrements de genèse/bootstrap relèvent d'une procédure d'ancrage distincte et n'ont pas à en porter une) ;
9. toute justification, hypothèse, limite et référence aux preuves requises.

Un horodatage mural MAY être enregistré comme métadonnée descriptive. Il MUST NOT allouer les positions, résoudre la concurrence ou déterminer l'applicabilité.

L'encodage, la canonicalisation, le schéma de condensat/signature et le langage de schéma restent des choix d'implémentation. Les choix effectués MUST fournir une identité déterministe de l'enveloppe exacte commise et MUST être documentés avec leurs règles de versionnement et de migration.


L'enregistrement de genèse MUST lier l'identité du périmètre du journal, l'enregistrement/la révision d'autorité initiale, la révision de gouvernance initiale ainsi que les sémantiques initiales des événements et schémas. Sa provenance et son ancre de confiance MUST être explicites et vérifiables indépendamment selon le modèle de confiance déclaré du déploiement. Cette spécification ne sélectionne pas le mécanisme de confiance du bootstrap. Une genèse absente, ambiguë ou invérifiable produit `unknown` et MUST bloquer tout ajout normatif ; elle MUST NOT être reconstruite à partir d'une branche VCS ou d'une valeur par défaut de forge.


Le mécanisme d'intégrité retenu MUST rendre détectable la substitution du payload ou du prédécesseur au regard du modèle de menace documenté. L'identité d'intégrité seule MUST NOT être considérée comme une preuve d'authenticité de l'acteur : l'attribution du principal et de la provenance MUST être validée séparément au regard du mécanisme d'autorité applicable. Un déploiement peut utiliser des engagements cryptographiques, l'intégrité d'un stockage de confiance, des enregistrements authentifiés ou une combinaison de ces mécanismes, mais MUST documenter les garanties et hypothèses de confiance ; aucun algorithme ni aucune suite n'est sélectionné ici.


Une clé d'idempotence MUST être unique dans son périmètre de journal tant que l'événement correspondant peut rester faisant autorité. Elle MUST être liée à l'opération d'ajout exacte, notamment au type d'événement, à l'identifiant d'événement, à la tête attendue et à l'identité du payload. Une réutilisation avec la même enveloppe de requête retourne le reçu initial ; une réutilisation avec toute enveloppe différente produit `conflict`. La compaction, les instantanés et la reconstruction des projections MUST préserver cette garantie de recherche (ou un tombstone équivalent non réutilisable). Les enregistrements de genèse/bootstrap relèvent de la procédure de genèse distincte et sont exemptés des clés d'idempotence ordinaires des ajouts.

## 4. Compare-and-append et sérialisation

Une requête d'ajout MUST nommer la tête attendue du journal par sa position canonique et son identité d'intégrité, ou par un jeton de tête équivalent non ambigu.

Le journal MUST fournir un point de linéarisation unique pour accepter un ajout :
- si la tête attendue correspond à la tête commise courante et que toutes les préconditions applicables sont satisfaites, exactement une position suivante est commise ;
- si la tête attendue est antérieure à la tête courante, la requête est périmée et MUST NOT être rébasée silencieusement ;
- si la position attendue correspond mais que l'identité d'intégrité diffère, le résultat est conflict ou unknown selon que le journal peut établir une incohérence définitive ;
- si le journal ne peut établir la tête courante ou l'état d'autorité requis, l'opération est bloquée en unknown.

Au plus un événement peut être commis à une position canonique donnée. Des requêtes concurrentes visant la même tête ne peuvent pas toutes réussir. Une requête déplacée doit être réévaluée et réautorisée contre la nouvelle tête avant toute nouvelle soumission.

Un ajout réussi retourne un reçu de commit durable liant le périmètre, la position, l'identifiant d'événement, l'identité du prédécesseur et l'identité d'intégrité de l'événement. Une réponse de succès MUST NOT être retournée avant le point de commit durable.

## 5. Frontière entre évaluation, autorisation et publication

L'évaluation, l'autorisation et la publication sont trois actes logiques distincts, avec des identités distinctes et des relations traçables, même si un adaptateur ou une implémentation de persistance les exécute dans une transaction technique atomique.

L'autorisation MUST être liée à l'évaluation exacte, au candidat, à la révision de gouvernance de base et à la tête de journal attendue. La publication MUST revérifier ce lien ainsi que les contrôles applicables d'exception/révocation/péremption immédiatement avant son point de commit.

Une évaluation périmée MUST rester un élément de preuve historique immuable, avec une disposition et un motif de péremption explicites. Elle MUST NOT être réutilisée pour autoriser ou satisfaire une transition ultérieure. Toute nouvelle transition exige une nouvelle évaluation sur les entrées courantes du candidat, de la base, de la gouvernance, de l'évaluateur, de la spécification et des preuves ; l'ancienne évaluation est conservée dans l'historique et n'est pas réécrite.

L'événement de publication est le point d'effet : la révision de gouvernance résultante s'applique prospectivement à partir de la position canonique occupée par cet événement, et non à partir d'un commit Git/Pijul, d'une fusion, d'un tag, d'une mise à jour de branche, de la fin d'une CI, d'une écriture de fichier locale ou d'un horodatage mural.

Une transaction technique peut préparer ou enregistrer l'évaluation et l'autorisation avant la publication, mais MUST NOT exposer la révision résultante comme applicable tant que l'événement de publication n'est pas durablement commis. Une transaction échouée ou abandonnée MUST laisser aucune révision de gouvernance partiellement applicable.

## 6. Durabilité, nouvelles tentatives et reprise après panne

L'ajout durable au journal est le point de commit. Une préparation volatile n'est pas une publication.

- **Panne avant le commit durable :** aucun événement n'a été commis. L'état volatil en attente peut être abandonné. Une nouvelle tentative peut utiliser la même clé d'idempotence et le payload exact.
- **Panne après le commit durable mais avant la réponse :** l'événement reste commis. L'appelant MUST résoudre le résultat en interrogeant la clé d'idempotence/l'identifiant d'événement ou la tête du journal. Il MUST NOT créer un nouvel identifiant d'événement et répéter aveuglément l'opération.
- **Nouvelle tentative dupliquée, même clé et même payload :** retourner le reçu de commit initial sans ajouter un second événement.
- **Même clé, payload différent :** retourner conflict ; ne jamais réinterpréter la clé ni écraser l'événement antérieur.
- **Résultat de commit inconnu :** retourner unknown/bloqué jusqu'à ce qu'une lecture du journal ou une procédure de reprise établisse si l'événement exact a été commis.
- **Événement commis, projection matérialisée manquante :** rejouer depuis une position de journal vérifiée. La reconstruction de projection MUST être idempotente et MUST NOT créer un second événement normatif.
- **Échec d'intégrité du journal, prédécesseur manquant ou enregistrements commis contradictoires :** échouer en mode fermé avec unknown ou conflict ; ne pas deviner, réparer en place ou avancer la tête.

Les instantanés et vues matérialisées MAY accélérer la reprise, mais chacun MUST être ancré à une position exacte du journal et à une identité d'intégrité. Le journal reste l'autorité. Un instantané ne peut effacer, réordonner ou remplacer l'historique commis.

Les effets externes MUST être coordonnés afin que le rejeu ne duplique pas silencieusement une action normative. Les implémentations MUST utiliser un contrat explicite d'idempotence/outbox/réconciliation ou démontrer une propriété équivalente ; cette spécification n'impose aucun mécanisme particulier.

## 7. Contrat des adaptateurs VCS et de provenance

Un adaptateur VCS MAY identifier les révisions natives exactes, patchs/changements, références/canaux et condensats d'objet/contenu ; récupérer, publier ou transporter le contenu d'un candidat ; joindre des métadonnées d'événement forge/VCS comme provenance ; signaler divergence, objets manquants, conflits de fusion et observations de réplication ; et proposer un ajout de candidat au journal canonique.

Un adaptateur VCS MUST NOT allouer ou réordonner les positions du journal canonique ; traiter les horodatages de commit, l'ascendance, l'ordre des branches/canaux, l'ordre de fusion ou l'ordre des événements de forge comme l'ordre normatif de gouvernance ; déduire une autorisation d'un push, d'une fusion, d'un tag, d'un état de branche protégée ou d'une CI verte ; écraser un événement commis ; ou résoudre un conflit de gouvernance en choisissant une branche Git/Pijul ou une valeur par défaut de forge.

Chaque observation VCS SHOULD préserver, lorsqu'elles sont disponibles, le type de VCS, l'identité du dépôt, l'identité de révision/changement/objet natif, le condensat de contenu, la référence/le canal, le(s) parent(s) observé(s), l'identité du distant/de la forge, l'heure d'observation (descriptive uniquement) et la version de l'adaptateur. Une provenance manquante MUST être explicite ; elle MUST NOT être fabriquée à partir d'une position du journal.

Un même candidat logique peut avoir plusieurs représentations natives VCS. Les adaptateurs MUST les lier à une identité de candidat commune uniquement si l'équivalence de contenu et les éléments de preuve de correspondance justifient cette relation. L'identité de révision native et l'identité du journal canonique restent distinctes.

## 8. Réconciliation des répliques

Les répliques se synchronisent par périmètre du journal canonique, position et identité d'intégrité de l'événement, et non en sélectionnant la révision native la plus récente.

- Une réplique en retard sur la tête canonique est périmée et peut rejouer les événements commis manquants.
- Une réplique signalant la même position et la même identité d'intégrité est cohérente pour ce préfixe.
- Une réplique signalant la même position avec une identité d'intégrité différente est en conflict.
- Une position manquante, un prédécesseur invérifiable ou une chaîne d'autorité inaccessible produit unknown.
- Des branches Git ou canaux Pijul divergents sont une divergence de provenance/contenu ; ils ne déterminent pas eux-mêmes quel événement de gouvernance est canonique.
- Un événement VCS sans événement de journal autorisé correspondant est une observation ou un candidat uniquement, pas une publication.

La réconciliation MUST préserver toutes les observations conflictuelles et leur provenance. La résolution exige un événement de journal explicitement autorisé ou un protocole de résolution séparé et documenté. Elle MUST NOT réécrire les événements canoniques antérieurs.

## 9. Vocabulaire des résultats et des échecs

| Résultat | Signification | Effet permis |
|---|---|---|
| committed | Le reçu de l'événement durable est établi | Avancer la tête canonique exactement une fois |
| stale-base | La tête attendue ne correspond plus | Aucun ajout ; réévaluation et réautorisation |
| unknown | Commit/tête/autorité ne peut être établi | Bloquer ; reprendre/interroger ; aucun succès inféré |
| conflict | Identité contradictoire, clé dupliquée avec payload différent ou historique commis incohérent | Bloquer ; résolution explicite et traçable |
| rejected | Une précondition connue de politique/autorisation a échoué | Aucun ajout |
| unavailable | Le service de journal ne peut décider de manière sûre | Aucun ajout ; nouvelle tentative uniquement sous contrat d'idempotence |

Unknown et conflict sont deux états bloquants distincts. Aucun ne peut être converti en Pass, contourné par une exception ou résolu par l'ordre VCS.

## 10. Scénarios de conformité

| ID | Scénario | Résultat requis |
|---|---|---|
| J-01 | Deux requêtes d'ajout utilisent la même tête attendue | Au plus une commit à la position suivante |
| J-02 | Nouvelle tentative après commit durable mais réponse perdue, même clé/payload | Reçu initial retourné ; aucun événement dupliqué |
| J-03 | Même clé d'idempotence avec payload différent | Conflict ; enregistrement initial préservé |
| J-04 | Panne avant commit | Aucun événement dans l'historique durable |
| J-05 | Panne après commit avant mise à jour de projection | La reprise rejoue l'événement commis exactement une fois dans la projection |
| J-06 | Réplique à même position mais identité/condensat d'événement différent | Conflict ; aucun gagnant automatique |
| J-07 | Push/fusion/tag Git/Pijul sans publication au journal | Aucun effet de gouvernance |
| J-08 | Rollback restaurant le contenu d'une ancienne révision | Nouvel événement et nouvelle révision à une position ultérieure |
| J-09 | Tête du journal ou prédécesseur invérifiable | Unknown ; aucun ajout |
| J-10 | Évaluation/autorisation liée à une tête obsolète | Publication bloquée ; réévaluation complète requise |
| J-11 | Évaluation, autorisation et publication exécutées atomiquement | Trois identités/enregistrements logiques restent distincts |
| J-12 | Adaptateur VCS signale des branches/canaux divergents | Préserver les observations ; ne pas en déduire l'ordre normatif |

Ces scénarios sont des cibles de conformité sémantique. Ils ne prétendent pas qu'un journal de production ou un adaptateur existe actuellement.

## 11. Relation formelle et limites

Cette spécification complète la [Spécification 0006](0006-governance-revision-applicability.fr.md), les [Architectures 0032](../architecture/0032-canonical-publication-model-checking.fr.md), [0033](../architecture/0033-governance-evaluator-exception-revocation-model.fr.md) et [0035](../architecture/0035-canonical-journal-recovery-model.fr.md).

Les modèles TLA+ actuels couvrent des tranches bornées distinctes : applicabilité et autorité temporelle ; publication compare-and-append ; contrôles d'évaluateur/exception/révocation ; sûreté du journal face aux pannes/reprises/rollback. Ils constituent des éléments de conception composables, pas un modèle intégré d'implémentation. Le modèle de reprise du journal suppose une autorisation amont et un rédacteur sérialisé ; il ne prouve ni consensus multi-écrivain, ni sémantique durable du système de fichiers, ni reprise éventuelle, ni correction des adaptateurs, ni réconciliation des répliques, ni raffinement de l'implémentation.

Références : [R-05 — TLA+ et TLC](../references.fr.md#r-05), [R-22 — sémantiques natives de Git et Pijul](../references.fr.md#r-22), [R-194 — linéarisabilité](../references.fr.md#r-194), [R-195 — journalisation anticipée et reprise après panne](../references.fr.md#r-195), [R-196 — sémantique des nouvelles tentatives idempotentes](../references.fr.md#r-196).

## 12. Frontière d'autorité

Les onze résultats de la [session d'arbitrage 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md) restent les entrées de conception arrêtées par le propriétaire. Cette spécification en développe les conséquences d'ingénierie sans les rouvrir. Il s'agit uniquement d'une proposition technique. L'adoption normative formelle reste exclusivement réservée à l'autorité racine du dépôt ; elle ne découle ni de ce document, ni d'une revue ou fusion de PR, ni de la CI, ni du model checking.
