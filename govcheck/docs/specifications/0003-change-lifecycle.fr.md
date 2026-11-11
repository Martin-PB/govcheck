# Spécification 0003 — Cycle de vie et acceptation des changements

**Statut :** architecture proposée, prête pour revue. **English:** [0003](0003-change-lifecycle.md).

## Principe et identité

GovCheck définit le cycle normatif. Branches/commits/PR Git, canaux/patches Pijul, plateformes de revue, échange de patches et workflows locaux sont des mécanismes, pas le cycle lui-même. Un changement est une proposition identifiée faisant passer le dépôt d'un état de base exact à un candidat exact ; il n'est synonyme d'aucun objet VCS ou forge.

L'enregistrement lie identité du dépôt, descripteurs base/candidat, révision et sémantique de gouvernance, ID et remplacements, ressources touchées, intention/risque, participants/autorités, preuves et évaluation.

## États abstraits

Proposé → Préparé → Évalué → Examinable → Accepté → Appliqué. États terminaux ou exceptionnels : Rejeté, Retiré, Périmé et Remplacé. Des sous-états sont possibles. Accepté et Appliqué sont distincts : le premier est une décision sur un candidat exact ; le second une opération VCS/collaboration.

## Gardes de transition

Chaque transition est un événement auditable avec acteur, date, état d'entrée/sortie, motif et provenance.
- Proposé → Préparé : identités et périmètre résolus.
- Préparé → Évalué : évaluation sur entrées épinglées.
- Évalué → Examinable : aucune invalidité normative non résolue ; preuves et explications disponibles.
- Examinable → Accepté : obligations bloquantes satisfaites, preuves valides, approbations authentiques et autorisées, exceptions valides.
- Accepté → Appliqué : l'adaptateur confirme l'application du candidat exact.
- Tout état avant application → Périmé : entrée pertinente modifiée ou preuve invalidée.
- Rejet, retrait autorisé et remplacement explicite sont enregistrés comme événements.

Aucune transition ne découle d'un nom de branche, label PR, statut CI ou message de chat. L'autorité d'approbation vient de la gouvernance, pas de la forge.

## Applicabilité de la révision de gouvernance

La révision exacte applicable à une évaluation ou une décision est résolue depuis l'historique canonique des événements de gouvernance et ses positions d'effet. Un candidat qui modifie la gouvernance est évalué et autorisé sous la révision antérieure applicable ; sa révision résultante ne peut prendre effet que par un événement ultérieur explicite de publication. Les décisions historiques conservent leur liaison de gouvernance d'origine. Une applicabilité absente, ambiguë, contradictoire ou périmée bloque l'acceptation. Voir la [Spécification 0006 — Applicabilité des révisions de gouvernance et autorisation temporelle](0006-governance-revision-applicability.fr.md) et sa [version anglaise](0006-governance-revision-applicability.md). Le protocole du journal canonique — compare-and-append, commit durable, reprise, nouvelle tentative et adaptateurs VCS — est précisé dans la [Spécification 0007](0007-canonical-governance-journal-protocol.fr.md) proposée ; celle-ci reste une proposition technique, pas une adoption normative ni une affirmation d'implémentation.

## Fraîcheur des preuves

Chaque preuve lie IDs de claims/règles, identité du sujet, empreintes base/candidat, révision/sémantique de gouvernance, révision de spécification, méthode/outil/version/configuration/portée, hypothèses/environnement/entrées externes, résultat/date/provenance et référence d'intégrité. Toute modification d'une dépendance déclarée invalide la preuve. L'historique est conservé ; une revalidation est nécessaire. Une réévaluation n'efface jamais un échec antérieur.

## Prédicat d'acceptation

L'acceptation est dérivée, pas modifiable comme un simple statut. Elle exige identités épinglées, évaluation des règles obligatoires, absence d'échec/conflit/indétermination bloquant, preuves valides et pertinentes, approbations authentiques, exceptions limitées et non expirées, et adaptateur capable d'identifier le candidat et son application.

L'acceptation locale suit le même prédicat mais signale l'absence d'application distante. L'application partagée exige une autorité d'équipe ou une barrière de forge.

## Concurrence, audit et vérification

Évolution de base, rebase et changement de graphe/canal Pijul exigent une analyse de validité par l'adaptateur ; la similarité textuelle ne suffit pas. Les approbations sont liées aux révisions exactes. L'audit logique est append-only ; une correction ajoute un événement.

Les futurs tests/modèles formels couvriront transitions illégales, preuves périmées, mutation après approbation, changement de gouvernance, application exacte, approbations concurrentes, usage local, sûreté et vivacité. Aucun moteur de cycle de vie n'existe encore.

## Références bibliographiques

- [R-05 — modélisation par transitions d'états TLA+ / TLC](../references.fr.md#r-05)
- [R-22 — sémantiques natives Git et Pijul](../references.fr.md#r-22)


## Compte rendu de l'arbitrage sur l'applicabilité de la gouvernance

Les onze résultats sélectionnés par le propriétaire du projet pour l'issue #41 sont consignés, avec leur statut explicite d'adoption en attente, dans le [compte rendu de séance 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md). Ils précisent que le journal canonique du cycle de vie est logique et sérialisé avec contrôle de concurrence ; les objets VCS natifs ne fournissent que transport/provenance ; la publication est l'événement d'effet ; l'ancien évaluateur reste seul faisant autorité pendant la migration d'évaluateur ; révocation et requalification historique sont distinctes ; les exceptions sont bornées et les exigences non dérogeables protégées ; unknown et conflict sont deux états bloquants distincts ; les évaluations périmées sont conservées mais inutilisables pour de nouvelles transitions ; les publications concurrentes sont sérialisées ; un retour arrière crée une nouvelle révision ; enfin, évaluation, autorisation et publication restent trois actes logiques distincts même si l'exécution technique est atomique.

Il s'agit d'un compte rendu de l'orientation d'arbitrage sélectionnée, pas d'une adoption normative ni d'une revendication d'implémentation. Voir la Spécification 0006 et le [compte rendu 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md).
