# 0008 — Plan de formalisation et de conformité

**Statut :** proposition d’architecture, prête pour revue. **English:** [0008](0008-formalization-and-conformance.md).

## Objectif

Définir une démarche rigoureuse reliant les contrats normatifs de gouvernance à des modèles formels et à des tests de conformité exécutables. Ce document ne prétend pas que GovCheck dispose déjà d’une implémentation, d’un moteur de cycle de vie vérifié ou d’une preuve achevée.

La première cible formelle est le cycle de vie d’un changement défini dans la spécification 0003, avec la fraîcheur des preuves et l’acceptation liée à un candidat exact. Les sémantiques propres aux VCS restent derrière le contrat d’adaptateur de 0004. Le vocabulaire d’assurance de 0005 s’applique à tous les résultats.

## Frontière du modèle

Le modèle abstrait représente un enregistrement de changement et les identités immuables qui lui sont pertinentes. Il ne modélise ni les mécanismes internes de Git, ni les algorithmes du graphe Pijul, ni une API de forge, ni les primitives cryptographiques, parseurs, systèmes de fichiers ou bases de données concrètes. Ces sujets exigent des contrats ou modèles séparés.

Préserver ces distinctions : un changement n’est ni une branche, ni un commit, patch, canal, PR ou MR ; Accepted (accepté) n’est pas Applied (appliqué) ; une preuve n’est pas une approbation ; une approbation n’est pas l’acceptation ; le model checking ne constitue pas une preuve de conformité de l’implémentation ; le résultat apply d’un adaptateur doit identifier le candidat exact appliqué.

## État abstrait

Variables candidates pour un premier modèle à états finis :

| Variable | Signification |
|---|---|
| phase | Proposed, Prepared, Evaluated, Reviewable, Accepted, Applied, Rejected, Withdrawn, Stale ou Superseded |
| baseId | Identité du descripteur exact de la base |
| candidateId | Identité du descripteur exact du candidat |
| governanceId | Identité de la révision et des sémantiques du paquet de gouvernance |
| specId | Révision de la spécification normative |
| evaluatedTuple | Tuple (base, candidat, gouvernance, spécification) évalué |
| evidence | Ensemble fini de preuves liées à un tuple et à leurs dépendances déclarées |
| approvals | Ensemble fini d’approbations liées aux identités du candidat et de la gouvernance, ainsi qu’à un acteur autorisé |
| requiredApprovals | Seuil et rôles requis, dérivés de la politique pour cette instance |
| blockingObligations | Ensemble fini d’obligations obligatoires et de leurs résultats |
| appliedCandidateId | Identité du candidat déclarée appliquée par l’adaptateur VCS, ou None |
| history | Séquence abstraite d’événements append-only |

Une instance utilise de petits ensembles finis pour les acteurs, preuves, obligations et identités. Ces bornes servent à l’exploration ; elles ne décrivent pas des limites de production.

## Actions à modéliser

1. Prepare : résoudre les identités du dépôt/changement et le périmètre d’impact.
2. Evaluate : évaluer les obligations obligatoires sur un tuple épinglé.
3. PublishEvidence : ajouter une preuve sans écraser l’historique.
4. Approve : enregistrer une approbation autorisée liée au candidat exact et à la révision de gouvernance.
5. Invalidate : rendre une preuve inutilisable lorsqu’une dépendance déclarée change.
6. ChangeInputs : modifier l’identité de la base, du candidat, de la gouvernance ou de la spécification ; rendre l’évaluation obsolète et invalider les preuves/approbations dépendantes selon les règles.
7. Accept : transition autorisée uniquement si le prédicat d’acceptation est satisfait.
8. Apply : transition autorisée uniquement si l’adaptateur confirme l’application du candidat accepté exact.
9. Reject, Withdraw, Supersede : enregistrer explicitement les décisions terminales ou exceptionnelles.
10. Reevaluate : créer une nouvelle évaluation sans effacer les échecs ni les preuves historiques.

Chaque action modifiant l’état ajoute un événement contenant acteur, motif et références avant/après. Le modèle peut abstraire les horodatages et l’authenticité cryptographique, mais doit déclarer explicitement ces abstractions.

## Propriétés de sûreté (invariants)

Le premier modèle doit au minimum vérifier :

- Correction des types : chaque variable reste dans son domaine fini déclaré.
- Justesse de l’acceptation : Accepted implique que le prédicat d’acceptation est satisfait pour le tuple exact courant.
- Justesse de l’application : Applied implique que le candidat appliqué est celui qui a été précédemment accepté.
- Aucune acceptation obsolète : une modification d’une identité pertinente ne peut laisser le changement Accepted ou Applied sans nouvelle décision valide.
- Liaison des preuves : une preuve ne satisfait une obligation que si son tuple sujet et ses dépendances correspondent au tuple courant et qu’elle est valide.
- Liaison des approbations : seules comptent les approbations relatives au candidat et à la révision de gouvernance courants, émises par des acteurs autorisés.
- Aucune approbation implicite : une évaluation réussie, un commentaire, une réaction ou un événement d’application ne crée pas d’approbation.
- Aucune application implicite : l’acceptation seule ne signifie pas que le changement a été appliqué.
- Historique append-only : les actions étendent l’historique ; elles ne réécrivent ni ne suppriment les événements antérieurs.
- Discipline des états terminaux : un changement rejeté, retiré ou supplanté ne peut pas revenir silencieusement dans une phase active.
- L’inconnu n’est pas un succès : une obligation obligatoire non prise en charge ou indéterminée ne peut pas satisfaire l’acceptation.

Ces propriétés appartiennent à l’abstraction. Chacune devra être reliée aux clauses normatives et à des éléments ultérieurs de conformité de l’implémentation.

## Vivacité et équité

La sûreté est prioritaire pour le premier modèle. La vivacité doit être conditionnelle : GovCheck ne peut garantir le progrès si les acteurs n’agissent jamais ou si les adaptateurs externes restent indisponibles.

Propriétés conditionnelles candidates : un changement Reviewable, valide, doté de preuves suffisantes et des approbations requises peut finir par être accepté si l’action reste activable et l’ordonnancement équitable ; un changement accepté peut finir par être appliqué si l’adaptateur reste disponible et confirme le candidat exact ; un changement obsolète peut finir par être réévalué si les entrées se stabilisent et que l’évaluation est planifiée.

Ne pas affirmer de progression inconditionnelle. Les hypothèses d’équité et de disponibilité de l’environnement doivent apparaître dans la configuration et le rapport du modèle.

## Décomposition des modèles

Conserver un premier modèle de cycle de vie réduit. N’ajouter des modèles séparés que si cela se justifie :

- Composition/conflits de règles : priorité, périmètre, héritage, ambiguïtés et règles obligatoires contradictoires.
- État VCS et acceptation : snapshots Git versus état de canal/graphe/patch Pijul ; préserver la sémantique native des conflits.
- Concurrence : approbations simultanées, mutation du candidat, invalidation et courses lors de l’application.
- Scénarios de menace : preuves falsifiées/obsolètes, approbation non autorisée, mensonge d’un adaptateur et retour arrière de gouvernance.

Ne pas réunir toutes les dimensions dans un modèle unique sujet à l’explosion combinatoire. Les composer au moyen de contrats explicites et d’identités abstraites partagées.

## Model checking ou preuve de théorème

Le model checking à états finis (par exemple TLA+/TLC ou un outil équivalent sélectionné par ADR) convient aux systèmes de transitions, à la concurrence, aux invariants de sûreté et à la vivacité conditionnelle sous bornes finies.

La preuve de théorème ne doit être utilisée que lorsqu’une preuve mathématique est justifiée : théorème réutilisable sur un prédicat d’acceptation précisément défini, théorème de raffinement ou transformation vérifiée. Un assistant de preuve ne rend pas normative une modélisation inexacte et n’établit pas la conformité d’une implémentation.

Aucun outil formel n’est sélectionné par ce document. TLA+ est un candidat pour explorer le cycle de vie et la concurrence, pas une dépendance décidée à l’avance.

## Vecteurs de test de conformité

Avant l’implémentation, définir des vecteurs indépendants du langage comprenant : descripteurs initiaux du dépôt/changement et identités de gouvernance/spécification ; séquence d’actions et contexte acteur/autorité ; preuves, dépendances et fraîcheur ; résultat de transition attendu et code de motif ; ajouts attendus à l’historique ; résultat attendu pour l’acceptation et l’application.

Familles minimales de vecteurs :

1. Parcours nominal de Proposed à Applied.
2. Preuve obligatoire manquante.
3. Obligation obligatoire indéterminée ou non prise en charge.
4. Preuve invalidée par mutation du candidat.
5. Approbation invalidée par changement de révision de gouvernance.
6. Approbation d’un acteur non autorisé.
7. Approbation visant un autre candidat.
8. Candidat appliqué différent du candidat accepté.
9. Mutation concurrente entre acceptation et application.
10. Rejet, retrait ou supersession explicite.
11. Acceptation locale seule avec signalement de l’absence d’application distante.
12. État Git avec index/worktree modifiés non réduit à HEAD.
13. Identité de canal/graphe/patch Pijul et conflits non aplatis dans les concepts Git.

Les onze premiers vecteurs de cycle de vie peuvent être partagés entre adaptateurs VCS lorsque pertinent. Les deux derniers sont spécifiques aux adaptateurs et doivent préserver leurs sémantiques natives.

## Discipline des preuves et des affirmations

Une exécution TLC, si cet outil est retenu, doit rapporter la révision du modèle, la configuration, les constantes, les réductions/symétries, l’équité, les nombres d’états/transitions, le statut d’achèvement et les bornes explorées. Une exécution réussie ne soutient que le modèle et la configuration vérifiés.

La conformité exige une relation distincte entre le comportement de l’implémentation et les transitions abstraites, ainsi que des éléments de test. La fidélité normative exige une traçabilité entre les clauses approuvées, les propriétés du modèle et les vecteurs de test. L’acceptation demeure une décision de gouvernance pour un candidat exact du dépôt.

## Décisions volontairement différées

- Outil formel et version.
- Encodage des états et format de configuration.
- Représentation des identités/empreintes.
- Politique de révocation ou d’invalidation des approbations.
- Sémantique exacte de supersession et de réouverture.
- Invalidation des preuves comme état explicite ou validité dérivée.
- Langage du banc de conformité et format d’échange.

Ces décisions seront traitées par des ADR ciblées après revue du présent plan. Aucune ne bloque la revue des frontières d’architecture définies ici.

## Ce que ce document n’affirme pas

Ce document ne fournit ni spécification TLA+, ni résultats TLC, ni preuve de théorème, ni tests exécutables, ni conception cryptographique, ni implémentation, ni assurance que les propriétés listées sont actuellement satisfaites. Il s’agit d’un plan traçable de modélisation et de conception des tests.

## Références bibliographiques

Références externes utilisées dans ce document : [R-05](../references.fr.md#r-05), [R-13](../references.fr.md#r-13), [R-20](../references.fr.md#r-20).
