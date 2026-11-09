# Spécification 0006 — Applicabilité des révisions de gouvernance et autorisation temporelle

**Statut :** contrat réutilisable proposé à la revue ; il ne prétend pas décrire une implémentation. **English:** [0006](0006-governance-revision-applicability.md).

## 1. Objet et périmètre

Cette spécification définit comment une évaluation identifie la révision de gouvernance autorisée à évaluer un changement, en particulier lorsque le candidat modifie également la gouvernance, les politiques, les règles, les modèles ou les évaluateurs.

Elle précise les [Spécifications 0002](0002-canonical-governance-model.fr.md) et [0003](0003-change-lifecycle.fr.md). Chaque dépôt gouverné définit ses propres principaux autorisés et son régime d'autorité ; ce contrat n'en sélectionne aucun.

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

Le profil de gouvernance applicable au dépôt définit le ou les principaux autorisés et précise si un proposant peut également autoriser. Cette spécification ne sélectionne ni ne modifie ce régime.

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

La configuration TLC est reproductible, mais ne constitue pas une preuve tant que l'exécution et l'enregistrement complet de l'outil, de la configuration et du résultat ne sont pas préservés.

## 6. Décisions ouvertes et obligations d'implémentation

Restent à résoudre : mécanisme d'ordre canonique et modèle de confiance/défaillance ; manifeste de révision et sérialisation de la chaîne d'autorité ; événements séparés ou opération atomique d'évaluation/autorisation ; coordination multi-écrivain et récupération après interruption ; signature, rotation/compromission/révocation des clés ; suspension d'urgence et effets rétroactifs juridiquement requis ; correspondance des identités Git/Pijul ; intégration aux modèles d'autorité, cycle de vie, décision de version et assurance ; résolveur exécutable, persistance, tests et application à la frontière d'acceptation.

Aucun de ces choix n'est adopté implicitement.

## Références

- [R-05 — modélisation des transitions TLA+ et TLC](../references.fr.md#r-05)
- [R-17 — métadonnées de gouvernance typées et relations traçables](../references.fr.md#r-17)
- [R-22 — sémantiques natives Git et Pijul](../references.fr.md#r-22)
- [R-88 — vérification des politiques/modèles NIST SP 800-192](../references.fr.md#r-88)
