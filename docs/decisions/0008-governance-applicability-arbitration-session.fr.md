# 0008 — Compte rendu de la séance d'arbitrage sur l'applicabilité de la gouvernance

**Statut du compte rendu :** choix d'arbitrage exprimés par l'utilisateur, en attente de leur intégration et de leur adoption normative formelle selon le processus d'autorité applicable de GovCheck. Ce document n'est pas lui-même un acte d'adoption, ne modifie pas l'Architecture 0023 et ne prétend ni à une implémentation ni à une vérification.
**Autorité/provenance :** choix explicitement sélectionnés par le propriétaire du projet dans la discussion GovCheck du 10-11-2026, en réponse aux onze questions guidées d'arbitrage de l'issue [#41](https://github.com/Martin-PB/govcheck/issues/41).
**Compagnon technique :** [Spécification 0006](../specifications/0006-governance-revision-applicability.fr.md) et [Spécification 0007](../specifications/0007-canonical-governance-journal-protocol.fr.md), proposée ; modèles bornés [GovCheckGovernanceApplicability](../../formal/tla/GovCheckGovernanceApplicability.tla), [GovCheckCanonicalPublication](../../formal/tla/GovCheckCanonicalPublication.tla), [GovCheckGovernanceControls](../../formal/tla/GovCheckGovernanceControls.tla) et [GovCheckJournalRecovery](../../formal/tla/GovCheckJournalRecovery.tla) ; rapports de model checking [Architectures 0031–0034](../architecture/README.fr.md).
**English:** [0008 — governance applicability arbitration session record](0008-governance-applicability-arbitration-session.md).

## 1. Statut et interprétation

Ce document consigne les choix exacts exprimés par l'autorité désignée pendant une séance guidée d'arbitrage. Il en préserve la provenance et les rend examinables. Il **ne transforme pas** la séance en politique normative formellement adoptée du seul fait de son commit ou de sa fusion.

Les choix ci-dessous alimentent la formalisation technique. Avant qu'une exigence normative soit considérée comme adoptée, le processus de gouvernance applicable doit enregistrer l'adoption, son fondement d'autorité, la révision exacte de gouvernance, la position de décision et l'événement explicite de publication avec son point d'effet. Dans l'intervalle, la Spécification 0006 demeure un contrat proposé et l'implémentation ne doit pas présenter ces choix comme une politique déjà adoptée.

L'Architecture 0023 reste la source du régime d'autorité racine actuellement consigné. Rien dans ce compte rendu ne modifie l'identité, le périmètre ou la succession de cette autorité.

## 2. Résultats d'arbitrage retenus

### A-01 — Ordre canonique des événements : journal logique sérialisé avec contrôle de concurrence

**Choix :** B.

GovCheck doit utiliser un journal logique canonique. Les candidats peuvent être préparés en parallèle, mais leur inscription définitive est sérialisée avec validation du prédécesseur et de la base. Un événement dont le prédécesseur attendu n'est plus courant ne peut pas être ajouté comme s'il l'était ; il doit être rejeté comme périmé ou faire l'objet d'une réconciliation explicite et d'une nouvelle évaluation. Ce choix ne sélectionne ni protocole de consensus ni moteur de stockage concret.

### A-02 — Rôle du VCS : adaptateurs de transport et de provenance

**Choix :** B.

Git, Pijul et les autres VCS/forges transportent les artefacts et événements gouvernés et fournissent des références de provenance natives. Leurs graphes natifs de commits/patches ne déterminent pas l'ordre normatif des événements. Les historiques logiques divergents doivent être détectés et résolus explicitement ; une fusion VCS réussie ne constitue pas en elle-même une résolution de gouvernance.

### A-03 — Point d'effet : événement de publication

**Choix :** B.

Le candidat est évalué et sa publication autorisée sous la révision de gouvernance antérieurement applicable. Un événement de publication distinct établit la position d'effet de la révision résultante et constitue le premier événement régi par cette nouvelle révision. L'événement de publication lui-même est autorisé sous la révision antérieure. Aucune règle proposée par le candidat ne peut autoriser sa propre publication.

### A-04 — Transition d'évaluateur : double exécution, ancien évaluateur faisant autorité

**Choix :** C.

L'évaluateur reconnu par la révision de gouvernance antérieurement applicable reste le seul évaluateur faisant autorité pour la transition. Le nouvel évaluateur proposé peut être exécuté en parallèle à des fins de comparaison, d'analyse de migration et de collecte d'éléments, mais son résultat ne peut pas autoriser sa propre adoption. L'identité, la version, la configuration, la sémantique et les dépendances pertinentes de l'évaluateur faisant autorité doivent être liées à l'évaluation. Toute divergence doit être visible et expliquée.

### A-05 — Révocation et décisions historiques

**Choix :** C.

La révocation produit ses effets prospectivement à partir de son événement explicite d'entrée en vigueur. Elle n'efface pas et ne réécrit pas silencieusement les décisions prises sous la révision précédemment applicable. Les décisions historiques peuvent faire l'objet d'une requalification distincte et explicite qui consigne les décisions concernées, le motif, l'autorité, les éléments et le résultat tout en préservant les enregistrements initiaux.

### A-06 — Exceptions

**Choix :** C.

Les exceptions sont explicites, justifiées, délimitées, limitées dans le temps ou par une condition, attribuables, traçables et révocables/soumises à réexamen. Elles consignent la règle et le périmètre du candidat concernés, l'autorité qui les accorde, le motif, le risque résiduel et son acceptation, les mesures compensatoires éventuelles, la date/condition de fin et les conditions de révocation/réexamen. Certaines exigences sont non dérogeables. Une exception est une décision/autorisation distincte, pas une preuve que l'exigence sous-jacente a été satisfaite.

### A-07 — Inconnu et conflit

**Choix :** C.

`unknown` (information insuffisante ou non résolue) et `conflict` (affirmations ou historiques incompatibles) sont deux états distincts et bloquants. Tous deux empêchent une transition normative. Leur résolution doit être explicite, attribuable et traçable. Un conflit ne peut pas être contourné par une exception ni résolu silencieusement par l'ordre de fusion VCS, la préférence de branche ou un défaut d'implémentation.

### A-08 — Évaluations périmées

**Choix :** C.

Une évaluation devenue périmée est conservée comme élément historique indiquant ce qui a été évalué et quand, mais ne peut plus soutenir une nouvelle autorisation/publication. Une nouvelle évaluation est nécessaire sur le candidat, la base, la révision de gouvernance, la chaîne d'autorité, l'évaluateur/la spécification/le profil et les dépendances de preuve pertinentes actuellement applicables. La péremption est distincte d'une évaluation négative et sa cause doit être consignée.

### A-09 — Publications concurrentes

**Choix :** B.

Au plus une publication de gouvernance peut réussir depuis un prédécesseur/une position de base canonique donnés. Les autres candidats préparés ou évalués sur cette base deviennent périmés pour la publication et doivent être réévalués sous la nouvelle révision de gouvernance courante. Ils ne sont pas automatiquement rejetés du seul fait qu'ils ont perdu la course.

### A-10 — Retour arrière

**Choix :** B.

Tout retour arrière crée une nouvelle révision et un nouvel événement de gouvernance. Son contenu peut restaurer celui d'une révision antérieure, mais il possède une nouvelle identité immuable, un nouveau prédécesseur, une nouvelle autorisation, une provenance et une position d'effet propres. Les positions et identités historiques ne sont jamais réutilisées ni rembobinées.

### A-11 — Actes d'évaluation, d'autorisation et de publication

**Choix :** C.

L'évaluation, l'autorisation et la publication sont trois actes logiques distincts, avec des enregistrements et relations identifiables séparément. Un adaptateur peut les exécuter dans une transaction technique atomique, à condition que cette exécution préserve l'identité de chaque acte, sa distinction sémantique, ses entrées, sorties, relations d'ordre/de causalité et sa récupérabilité. Une évaluation n'est pas une autorisation ; une autorisation n'est pas une publication.

## 3. Conséquences transversales pour la formalisation technique

Les choix retenus impliquent que le contrat technique et sa future réalisation exécutable couvrent au minimum :

- identité logique d'événement, identité du prédécesseur et position canonique ordonnée de façon monotone ;
- ajout compare-and-append / publication sérialisée avec rejet des bases périmées ;
- identifiants natifs des VCS comme provenance, pas comme clés d'ordre normatif ;
- liaison de l'évaluation au candidat exact, à la base, à la gouvernance antérieure, à la chaîne d'autorité, à l'évaluateur faisant autorité, à la spécification/au profil et aux dépendances de preuve ;
- résultat distinct de l'évaluateur comparatif, qui ne peut remplacer le résultat faisant autorité ;
- actes distincts d'autorisation et de publication, y compris exécution atomique par adaptateur sans fusion sémantique ;
- positions d'effet prospectives et identités immuables des révisions ;
- événements explicites de révocation et de requalification historique ;
- périmètre des exceptions, exigences non dérogeables, expiration et révocation ;
- résultats fail-closed distincts `unknown` et `conflict` ;
- conservation des évaluations périmées et réévaluation obligatoire ;
- publication à gagnant unique depuis un prédécesseur et sémantique de reprise ;
- retour arrière comme nouvelle révision.

Il s'agit d'exigences de formalisation déduites des choix consignés, pas d'affirmations selon lesquelles le modèle TLA+ borné actuel les couvre déjà.

## 4. Couverture des modèles formels bornés et lacunes explicites

Les artefacts formels sont des **abstractions finies distinctes**, et non un modèle intégré ni une preuve de raffinement :

- **Applicabilité et autorité antérieure — [Architecture 0031](../architecture/0031-first-tlc-governance-applicability.fr.md), PR #90 :** liaison aux positions de décision/d'effet, autorité antérieure applicable et préservation historique bornée ; 20 785 états générés / 18 067 distincts.
- **Publication canonique — [Architecture 0032](../architecture/0032-canonical-publication-model-checking.fr.md), PR #96 :** évaluation sur tête capturée, liaison de l'autorisation, publication comme point d'effet distinct, rejet des autorisations périmées, unicité des révisions/prédécesseurs et une publication par prédécesseur canonique ; 84 307 états générés / 56 895 distincts, huit invariants et `AppendOnly` réussis.
- **Contrôles des évaluateurs, exceptions et révocation — [Architecture 0033](../architecture/0033-governance-evaluator-exception-revocation-model.fr.md), PR #98 :** autorité de l'évaluateur antérieur, résultats comparatifs uniquement pour un remplaçant, états distincts et bloquants `Unknown`/`Conflict`, exceptions bornées/révocables et exigences non dérogeables, révocation prospective, requalification historique distincte et rejet des autorisations périmées ; 2 826 117 états générés / 1 026 484 distincts, neuf invariants et `AppendOnly` réussis.
- **Reprise du journal et rollback — [Architecture 0034](../architecture/0034-canonical-journal-recovery-model.fr.md), PR #99 :** point de commit abstrait d'ajout durable, panne avant/après commit, rejeu jusqu'à la tête, rollback comme nouvel événement/révision restaurant un contenu antérieur et observations passives de répliques Git/Pijul ; 178 549 états générés / 38 434 distincts, six invariants et `AppendOnly` réussis. Le modèle suppose un rédacteur sérialisé et abstrait l'autorisation amont ; son hypothèse d'équité n'est pas un résultat vérifié de vivacité de reprise éventuelle.

La [Spécification 0007](../specifications/0007-canonical-governance-journal-protocol.fr.md) est un contrat sémantique proposé pour compare-and-append, la linéarisabilité, les reçus durables, les nouvelles tentatives idempotentes, le périmètre/la genèse du journal, les adaptateurs VCS limités à la provenance, la réconciliation des répliques et douze scénarios de conformité. Elle n'est pas elle-même vérifiée dans son ensemble par model checking ni implémentée.

**État d'intégration :** les PR #90, #96 et #98 sont fusionnées dans `main`. GitHub a marqué la PR #99 comme fusionnée dans l'ancienne branche de travail de la PR #98, pas dans `main` ; les PR #100 et #104 restent ouvertes et empilées. Le modèle de reprise du journal et la Spécification 0007 ne doivent donc pas être présentés comme déjà intégrés à `main`. Le présent candidat de revue transporte ce travail vers `main`.

### Lacunes restantes

Linéarisabilité et consensus multi-écrivain non bornés/distribués ; durabilité d'un moteur de stockage concret, écritures déchirées et reprise opérationnelle ; correspondances réelles des adaptateurs VCS et résolution de répliques divergentes ; invalidation complète des évaluations périmées selon leurs dépendances et réévaluation ; succession arbitraire d'évaluateurs, identité cryptographique et délégation ; acceptation structurée complète du risque d'exception et expiration temps réel ; workflows explicites de résolution de `unknown`/`conflict` ; exécution atomique concrète préservant les trois actes logiques pendant les interruptions ; séquences multiples de rollback ; tests de conformité exécutables, raffinement de l'implémentation et enforcement en production. La Spécification 0007 décrit des obligations proposées, sans fournir leur implémentation ni leur vérification.

Aucun résultat de model checking fini, aucune modification de spécification ni aucune fusion de PR n'établit la conformité d'une implémentation ou l'adoption normative. Les onze choix restent des entrées de conception sélectionnées par le propriétaire jusqu'à l'enregistrement d'un événement d'adoption distinct sous la révision de gouvernance antérieure applicable.

## 5. Frontière entre adoption et implémentation

- Ce compte rendu enregistre des choix exprimés ; il n'est pas un événement d'adoption normative.
- La Spécification 0006 peut décrire la direction sélectionnée comme une proposition choisie par l'autorité, en attente d'adoption formelle, mais ne doit pas en élever silencieusement le statut.
- Un enregistrement d'adoption ultérieur doit lier le contrat adopté à la révision de gouvernance antérieure et à un événement explicite de décision/publication.
- Une PR fusionnée, une CI verte, un label d'issue ou une permission du dépôt ne constitue pas une adoption normative.
- Ce compte rendu ne revendique aucune implémentation, frontière d'application, consensus distribué, provenance cryptographique ou comportement d'adaptateur VCS.

## 6. Traçabilité

- Issue parente de décision : [#41](https://github.com/Martin-PB/govcheck/issues/41).
- Compagnon technique : [#86](https://github.com/Martin-PB/govcheck/issues/86).
- Régime d'autorité antérieur : [Architecture 0023](../architecture/0023-bootstrap-governance-authority.fr.md).
- Contrat de cycle de vie : [Spécification 0003](../specifications/0003-change-lifecycle.fr.md).
- Contrat d'applicabilité : [Spécification 0006](../specifications/0006-governance-revision-applicability.fr.md).
- Protocole de journal proposé : [Spécification 0007](../specifications/0007-canonical-governance-journal-protocol.fr.md).
- Modèles bornés : [applicabilité](../../formal/tla/GovCheckGovernanceApplicability.tla), [publication canonique](../../formal/tla/GovCheckCanonicalPublication.tla), [contrôles de gouvernance](../../formal/tla/GovCheckGovernanceControls.tla), [reprise du journal](../../formal/tla/GovCheckJournalRecovery.tla).
- Rapports : [Architecture 0031](../architecture/0031-first-tlc-governance-applicability.fr.md), [0032](../architecture/0032-canonical-publication-model-checking.fr.md), [0033](../architecture/0033-governance-evaluator-exception-revocation-model.fr.md) et [0034](../architecture/0034-canonical-journal-recovery-model.fr.md).
- Références : [R-05](../references.fr.md#r-05), [R-22](../references.fr.md#r-22), [R-194](../references.fr.md#r-194), [R-195](../references.fr.md#r-195) et [R-196](../references.fr.md#r-196).

Les références externes éclairent les méthodes techniques ; elles ne déterminent ni n'autorisent la politique de gouvernance choisie par l'utilisateur.
