# Spécification 0006 — Applicabilité des révisions de gouvernance et autorisation temporelle

**Statut :** contrat proposé à la revue du mainteneur ; il n'adopte ni ne modifie la décision d'autorité de l'Architecture 0023 et ne prétend pas décrire une implémentation. **English:** [0006](0006-governance-revision-applicability.md).

## 1. Objet et périmètre

Cette spécification définit comment une évaluation identifie la révision de gouvernance autorisée à évaluer un changement, en particulier lorsque le candidat modifie également la gouvernance, les politiques, les règles, les modèles ou les évaluateurs.

Elle précise la [Spécification 0003](0003-change-lifecycle.fr.md), les [Architectures 0012](../architecture/0012-normative-authority-and-documentation.fr.md), [0017](../architecture/0017-artifact-identity-revision-and-versioning.fr.md), [0018](../architecture/0018-version-governance-and-compatibility-authority.fr.md) et le régime actuel consigné dans l'[Architecture 0023](../architecture/0023-bootstrap-governance-authority.fr.md).

Il s'agit d'un contrat sémantique, pas d'un choix de sérialisation ou d'implémentation. Il n'impose ni horodatage mural, ni ascendance Git, ni base de données, forge, Lean, TLA+ en production ou technologie de signature.

## 2. Termes

- **Révision de gouvernance :** état immuable et identifié de manière unique du paquet normatif applicable, avec les sémantiques d'autorité et de politique nécessaires.
- **Décision de gouvernance :** événement immuable autorisant, rejetant, suspendant, révoquant ou remplaçant un changement déterminé.
- **Candidat :** état exact du dépôt proposé, identifié indépendamment de sa représentation dans une forge.
- **Évaluation :** appréciation enregistrée d'un candidat exact sous une révision de gouvernance, une spécification et un contexte d'évaluateur exacts.
- **Position de décision :** position dans l'ordre canonique des événements à laquelle une décision d'autorité est enregistrée.
- **Position d'effet :** première position à partir de laquelle une révision publiée devient applicable.
- **Révision de base :** révision sous laquelle un changement proposé est évalué et autorisé.
- **Révision résultante :** nouvelle révision proposée par ce changement, le cas échéant.

L'identité logique d'un artefact, son empreinte, sa révision native VCS, sa version de compatibilité, l'identifiant d'évaluation et l'identifiant d'événement restent distincts. SemVer ne remplace pas une révision immuable de gouvernance.

## 3. Contrat normatif proposé

### 3.1 Historique immuable

1. Toute révision publiée DOIT avoir une identité logique stable et une identité de révision immuable.
2. Toute révision autre que la genèse DOIT identifier son prédécesseur, la décision qui l'autorise, le fondement d'autorité et sa position d'effet.
3. L'historique DOIT être append-only au niveau logique. Correction, révocation, retour arrière et remplacement DOIVENT ajouter des événements/révisions ; ils NE DOIVENT PAS réécrire les enregistrements antérieurs.
4. Un retour arrière DOIT publier une nouvelle révision, même si son contenu correspond à un état antérieur. Il NE DOIT PAS faire reculer la position des événements ni effacer l'historique intermédiaire.
5. Les identifiants de révision NE DOIVENT PAS être réutilisés. L'identité du contenu ne démontre pas l'autorité.

### 3.2 Applicabilité déterministe

Pour toute décision ou évaluation à la position canonique *p*, la révision applicable est l'unique révision publiée dont la position d'effet est la plus grande parmi celles inférieures ou égales à *p*.

Le résolveur DOIT retourner la révision unique si la chaîne est valide ; `unknown` si l'historique, l'autorité, le prédécesseur, la position d'effet ou les sémantiques nécessaires manquent/ne peuvent être résolus ; et `conflict` si plusieurs révisions incompatibles revendiquent la même position ou si l'historique est incohérent. `unknown` et `conflict` DOIVENT bloquer l'acceptation normative.

Aucun repli n'est permis vers les règles proposées par le candidat, le contenu de la branche la plus récente, une supposition d'horloge, une valeur par défaut de forge ou une préférence implicite. Les positions DOIVENT être totalement ordonnées dans le domaine d'autorité et allouées atomiquement. Une séquence monotone, un journal fondé sur consensus ou un autre mécanisme justifié peuvent être utilisés. L'horloge murale seule NE DOIT PAS établir l'ordre ou l'applicabilité.

### 3.3 Évaluation et autorisation des candidats qui modifient la gouvernance

Un candidat qui modifie la gouvernance DOIT être évalué selon la révision de base exacte applicable à sa position de décision.

L'évaluation DOIT lier au minimum : dépôt et contexte VCS natif ; identités exactes de base et candidat ; révision de base et identité de sa chaîne d'autorité ; révision résultante proposée ; identités/révisions de spécification et d'évaluateur ; règles/profil et sémantiques résolues ; preuves, hypothèses, limites et résultat ; position de l'événement et provenance.

La décision DOIT lier le même candidat et la même révision de base que l'évaluation. Elle DOIT enregistrer la position, le principal approbateur, le fondement d'autorité, le résultat et la justification.

Un candidat NE DOIT PAS être évalué ou autorisé sous la révision qu'il propose d'introduire. La révision proposée ne devient applicable qu'après un événement explicite de publication autorisé, à une position d'effet strictement ultérieure.

Pour un changement qui modifie simultanément code et gouvernance, la révision antérieure applicable évalue et autorise le candidat complet. La révision résultante ne gouverne que les événements ultérieurs. Une fusion, un push, un tag, une CI verte ou la présence d'un fichier ne constitue pas l'événement d'autorisation.

### 3.4 Validité temporelle et décisions historiques

1. L'applicabilité est déterminée à partir de l'historique canonique, pas en réévaluant les anciennes décisions sous la révision courante.
2. Une décision historique DOIT conserver la révision exacte et le fondement d'autorité applicables à sa position.
3. Un amendement, une révocation ou un retour arrière ultérieur NE DOIT PAS modifier rétroactivement le fondement d'autorité ou l'évaluation de validité d'une décision antérieure.
4. Un événement ultérieur peut consigner qu'une décision est contestée, invalide au titre d'une règle déjà applicable ou affectée par de nouvelles preuves. Il DOIT préserver la décision originale et expliquer le nouvel événement ; il NE DOIT PAS réécrire l'historique.
5. Une révocation prend effet prospectivement à sa position enregistrée, sauf processus distinct, autorisé et justifié consignant explicitement un autre effet. Aucune révocation rétroactive n'est présumée.

### 3.5 Péremption, concurrence et blocage par défaut

Une évaluation ou approbation est périmée si une dépendance liée change : candidat, base, révision de gouvernance, chaîne d'autorité, profil, spécification, sémantique de l'évaluateur ou dépendance déclarée des preuves.

Avant autorisation puis avant publication/application, l'implémentation DOIT confirmer que la base et la révision restent courantes et applicables. Une divergence DOIT invalider l'évaluation/l'approbation en attente et exiger une nouvelle évaluation ; aucun rebasage silencieux n'est permis.

Les changements concurrents DOIVENT être sérialisés à une frontière unique de décision/publication ou résolus par un protocole explicite. Deux changements évalués sur la même base NE DOIVENT PAS être publiés comme successeurs l'un de l'autre. Le candidat perdant devient périmé et doit être réévalué.

Absence d'autorité, historique ambigu, applicabilité inconnue, autorité révoquée, délégation invalide, preuves périmées, événements contradictoires ou sémantiques indisponibles DOIVENT produire `unknown`, `conflict` ou un résultat bloqué/gouvernance invalide. Aucun ne peut être converti en succès.

### 3.6 Autorité et séparation des responsabilités

L'Architecture 0023 consigne actuellement un principal racine unique, le principal racine configuré, et accepte explicitement que ce même principal propose et autorise un changement. Cette spécification ne modifie pas ce régime.

L'implémentation DOIT distinguer proposant/producteur, réviseur/évaluateur technique, autorité normative et publieur/exécutant. Lorsque proposant et autorité sont le même principal, l'enregistrement DOIT le révéler. Il NE DOIT PAS revendiquer une approbation indépendante ou une séparation à deux personnes. Administration du dépôt, droit de fusion et CI ne constituent pas une autorité normative.

Toute délégation future DOIT être explicite, bornée par action et périmètre, temporellement valide, traçable au délégant et révocable prospectivement. Aucune délégation n'est implicite.

## 4. Scénarios de conformité requis

| ID | Scénario | Résultat requis |
|---|---|---|
| GA-01 | Le candidat modifie la politique et tente d'utiliser sa nouvelle politique pour s'évaluer | Blocage ; évaluation sous la révision antérieure |
| GA-02 | Candidat autorisé sous N puis publication de N+1 | N+1 ne s'applique qu'après sa position d'effet ultérieure |
| GA-03 | Décision historique sous N puis publication de N+1 | La décision reste liée à N |
| GA-04 | Révision ou chaîne absente/ambiguë/contradictoire | `unknown` ou `conflict` ; aucune acceptation |
| GA-05 | Évaluation sous N puis publication de N+1 avant autorisation | Évaluation périmée ; nouvelle évaluation obligatoire |
| GA-06 | Deux candidats ciblent simultanément la même base | Au plus un publie depuis cette base ; l'autre devient périmé/en conflit |
| GA-07 | Autorité révoquée avant la position de décision | Blocage sauf autorité valide selon la révision applicable |
| GA-08 | Retour arrière restaurant le contenu d'une ancienne politique | Nouvel événement/révision ; historique intermédiaire préservé |
| GA-09 | Proposant et approbateur sont le même principal | Permis si la politique l'enregistre ; aucune revendication d'indépendance |
| GA-10 | Git/Pijul/forge change sans événement de gouvernance correspondant | Aucune publication ni autorisation implicite |

Ces scénarios sont des objectifs de conformité. Le model checking borné constitue une preuve relative au modèle/configuration déclarés uniquement, pas une preuve de théorème, d'implémentation ou d'application opérationnelle.

## 5. Modèle formel et limites

[GovCheckGovernanceApplicability.tla](../../formal/tla/GovCheckGovernanceApplicability.tla) et sa configuration TLC fournissent un modèle fini couvrant l'évaluation épinglée à la gouvernance courante, l'autorisation par l'autorité applicable à la position de décision, la publication à une position d'effet ultérieure, la préservation des liens historiques, le rejet des évaluations périmées et les historiques append-only.

Le modèle est séparé de `GovCheckAuthority.tla` et `GovCheckLifecycle.tla` : il compose leurs préoccupations sans prétendre que ces modèles définissent déjà l'applicabilité temporelle. Constantes et historiques bornés n'établissent ni correction non bornée, ni authenticité cryptographique, ni consensus distribué, ni raffinement de l'implémentation, ni concurrence complète, ni application par la forge. Délégation, cycle de vie des dérogations, détails de révocation et consensus multi-écrivain restent hors de ce premier modèle.

Le modèle d'applicabilité initial a été analysé par SANY et vérifié par TLC ; son résultat borné exact et ses limites sont consignés dans l'Architecture 0031. Il s'agit d'un élément de preuve par model checking, pas d'une preuve de l'implémentation.

## 6. Arbitrages résolus et obligations d'implémentation restantes

Les onze résultats sélectionnés par l'autorité sont consignés dans le [compte rendu de séance 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md). Ils résolvent les questions de conception auparavant laissées ouvertes : journal logique canonique à ajout sérialisé ; VCS comme transport/provenance et non comme ordre normatif ; publication comme point d'effet ; autorité de l'évaluateur antérieur avec exécution comparative du remplaçant ; révocation prospective et requalification historique distincte ; exceptions structurées avec exigences non dérogeables ; états distincts et bloquants `unknown` et `conflict` ; conservation historique des évaluations périmées sans réutilisation ; une seule publication réussie par prédécesseur canonique ; rollback comme nouvelle révision ; et trois actes logiques distincts même lorsqu'ils sont techniquement atomiques.

Ces choix sont des entrées de conception arrêtées pour le travail technique. Leur adoption normative formelle reste réservée à l'autorité racine du dépôt et ne peut être déduite de cette spécification, d'une PR, d'une fusion ou d'un résultat de vérification. La copie du paquet réutilisable exprime volontairement le rôle d'autorité de manière générique, sans intégrer l'identité d'un principal propre à un dépôt.

Les obligations de formalisation/implémentation restantes sont désormais plus précises : définir le modèle de confiance et de défaillance du journal canonique durable ; spécifier la sérialisation du manifeste de révision et de la chaîne d'autorité ; définir l'ajout atomique résistant aux pannes et la reprise ; préciser la gestion des signatures et clés uniquement dans la mesure requise par le modèle de confiance retenu ; faire correspondre les identités natives Git/Pijul aux événements logiques sans utiliser leur ordre comme ordre normatif ; intégrer les enregistrements d'autorité, de cycle de vie, de décision de version et d'assurance ; fournir un résolveur exécutable, la persistance, la réconciliation des adaptateurs, les tests de conformité et les éléments de preuve relatifs à la frontière d'acceptation. Ce sont des obligations d'ingénierie, et non des questions d'arbitrage encore ouvertes.

## Références

- [R-05 — modélisation des transitions TLA+ et TLC](../references.fr.md#r-05)
- [R-17 — métadonnées de gouvernance typées et relations traçables](../references.fr.md#r-17)
- [R-22 — sémantiques natives Git et Pijul](../references.fr.md#r-22)
- [R-88 — vérification des politiques/modèles NIST SP 800-192](../references.fr.md#r-88)


## 7. Orientation d'arbitrage sélectionnée par l'autorité — adoption formelle en attente

Le propriétaire du projet a sélectionné les onze résultats consignés avec leur provenance dans le [compte rendu de séance 0008](../decisions/0008-governance-applicability-arbitration-session.fr.md). Cette section enregistre leurs conséquences techniques ; elle ne transforme pas la séance en adoption normative. Tant qu'un événement d'adoption distinct n'est pas enregistré sous la révision de gouvernance antérieure applicable, les exigences ci-dessous restent une proposition sélectionnée par l'autorité.

L'orientation retenue est la suivante : (1) journal logique canonique avec ajout sérialisé et contrôle de concurrence ; (2) Git, Pijul et les autres VCS/forges sont des adaptateurs de transport/provenance, pas des autorités d'ordre normatif ; (3) la publication est le premier événement régi par la révision résultante et reste autorisée sous la révision antérieure ; (4) l'évaluateur reconnu par la gouvernance antérieure reste seul faisant autorité, tandis que le remplaçant proposé peut être exécuté à titre comparatif ; (5) révocation prospective avec requalification historique distincte ; (6) exceptions explicites, justifiées, bornées, attribuables, traçables et révocables, certaines exigences étant non dérogeables ; (7) `unknown` et `conflict` sont deux états distincts et bloquants, nécessitant une résolution explicite et ne pouvant être contournés par exception ; (8) les évaluations périmées restent historiques mais ne peuvent plus soutenir une nouvelle transition ; (9) au plus une publication réussit depuis un prédécesseur canonique et les candidats déplacés doivent être réévalués ; (10) un retour arrière crée une nouvelle révision immuable même si son contenu restaure un état antérieur ; (11) évaluation, autorisation et publication sont trois actes logiques distincts, même si un adaptateur les exécute dans une transaction technique atomique.

### 7.1 Couverture des modèles formels bornés et obligations restantes

Le modèle [GovCheckGovernanceApplicability.tla](../../formal/tla/GovCheckGovernanceApplicability.tla), précédemment vérifié, reste limité à son abstraction finie d'applicabilité consignée. Un second modèle de conception borné, [GovCheckCanonicalPublication.tla](../../formal/tla/GovCheckCanonicalPublication.tla), a depuis été ajouté. Il modélise un ensemble fini d'évaluations préparées, une autorisation liée à la tête canonique capturée, une publication distincte comme action d'ajout/effet, le rejet d'une autorisation périmée après l'avancement de la tête, l'unicité des identités de révision, la continuité des prédécesseurs et l'historique append-only. Il est routé vers le workflow TLC comme tâche distincte.

Le modèle de publication canonique a été analysé et vérifié par TLC ; son résultat exact est consigné dans l'Architecture 0032. Le modèle de contrôles de gouvernance décrit en §7.2 et le modèle distinct de reprise du journal décrit en §7.3 complètent cette couverture pour certaines sémantiques A-04 à A-10. La Spécification 0007 propose le contrat de protocole associé. Ces modèles restent des abstractions finies séparées : ils ne constituent ni un modèle intégré ni une preuve de raffinement. La matrice de couverture et les lacunes transversales figurent au §4 du compte rendu 0008.

Les résultats retenus et leur provenance détaillée figurent dans les comptes rendus de séance [anglais](../decisions/0008-governance-applicability-arbitration-session.md) et [français](../decisions/0008-governance-applicability-arbitration-session.fr.md).


### 7.2 Modèle de contrôle des évaluateurs, exceptions et révocation

Le modèle borné distinct [GovCheckGovernanceControls.tla](../../formal/tla/GovCheckGovernanceControls.tla), configuré par [GovCheckGovernanceControls.cfg](../../formal/tla/GovCheckGovernanceControls.cfg), ajoute une couverture par transitions finies des sémantiques retenues A-04 à A-08 :

- seul l'évaluateur reconnu par la révision de gouvernance antérieure peut produire une évaluation faisant autorité ; un remplaçant proposé ne produit que des résultats comparatifs/en parallèle ;
- les évaluations distinguent `Pass`, `Fail`, `Unknown` et `Conflict` ; les deux derniers états ne peuvent pas autoriser ;
- les exceptions sont explicites, justifiées, bornées par une expiration logique, révocables, limitées aux exigences dérogeables et revalidées lors de la publication ; les exigences non dérogeables ne peuvent faire l'objet d'une exception ;
- la révocation de l'autorité est enregistrée à une position logique ultérieure et bloque les publications suivantes sans supprimer les décisions antérieures ;
- la requalification historique ajoute un enregistrement distinct faisant référence à la décision et à la révision de gouvernance d'origine.

Le modèle abstrait volontairement l'autorité sous la forme d'un évaluateur/régime racine antérieur désigné, d'identifiants et d'exigences finis, ainsi que d'un nombre borné d'événements. Il ne modélise ni identité cryptographique, ni délégation, ni horloge temps réel, ni stockage durable, ni reprise après panne, ni répliques distribuées, ni enregistrement exécutable complet de l'acceptation du risque d'une exception. Il ne constitue ni une affirmation d'implémentation ni un acte d'adoption normative. Le modèle et la configuration exacts ont réussi SANY 2.1 et TLC 2.19 : 2 826 117 états générés, 1 026 484 distincts, zéro restant, profondeur 12 ; les neuf invariants et `AppendOnly` ont réussi. Voir [l'Architecture 0033](../architecture/0033-governance-evaluator-exception-revocation-model.fr.md) pour les identités exactes et les limites.

### 7.3 Protocole du journal canonique, reprise et rollback

La [Spécification 0007](0007-canonical-governance-journal-protocol.fr.md) propose le contrat sémantique du journal canonique et des adaptateurs VCS : identité de périmètre, genèse liée à la base d'autorité/gouvernance, compare-and-append avec point de linéarisation unique, commit durable, clé d'idempotence liée à la requête exacte, reprise après panne, projections rejouables et adaptateurs Git/Pijul limités au transport et à la provenance. Elle définit douze scénarios de conformité, mais ne sélectionne aucun moteur de stockage, format de sérialisation, algorithme cryptographique, produit de consensus, VCS ou forge. Elle reste proposée, non adoptée et non implémentée.

Le modèle borné [GovCheckJournalRecovery.tla](../../formal/tla/GovCheckJournalRecovery.tla), configuré par [GovCheckJournalRecovery.cfg](../../formal/tla/GovCheckJournalRecovery.cfg), vérifie une abstraction à rédacteur unique : ajout durable comme point de commit, panne avant/après commit, rejeu jusqu'à la tête, rollback comme nouvel événement/révision restaurant un contenu antérieur et observations passives de répliques VCS. L'exécution SANY 2.1/TLC 2.19 consignée dans l'[Architecture 0034](../architecture/0034-canonical-journal-recovery-model.fr.md) a généré 178 549 états, dont 38 434 distincts, zéro restant ; six invariants et `AppendOnly` ont réussi. L'hypothèse d'équité faible pour `Recover` n'est pas une propriété de vivacité de reprise éventuelle vérifiée.

Ce modèle ne démontre ni la durabilité d'un moteur concret, ni le comportement d'écritures déchirées, ni le consensus multi-écrivain, ni la convergence/réconciliation de répliques divergentes, ni la correction des adaptateurs, ni le raffinement de l'implémentation. Le modèle de reprise de la PR #99 n'était pas sur `main` : GitHub l'a marqué fusionné dans l'ancienne branche de travail de la PR #98 ; les PR #100 et #104 restent ouvertes et empilées. Le présent candidat porte le modèle et la Spécification 0007 vers `main`, sans adoption normative ni affirmation d'implémentation.
