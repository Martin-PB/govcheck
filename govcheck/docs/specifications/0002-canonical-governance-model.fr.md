# Spécification 0002 — Modèle canonique de gouvernance

**Statut :** architecture proposée, prête pour revue. **Portée normative :** contrat de conception uniquement ; aucun schéma ni évaluateur n'est implémenté. [English](0002-canonical-governance-model.md).

## Objet et invariants

Le modèle canonique versionné est l'unique autorité normative du dépôt. GovCheck l'évalue. Markdown (AGENTS.md, GOVERNANCE.md, SECURITY.md, CONTRIBUTING.md) constitue une projection générée ou vérifiée et une explication, jamais une source concurrente. Le modèle est indépendant du VCS, de l'hébergement, de la forge, de la CI, du langage et du harnais d'agent. Les fondations formelles s'appliquent à tous les dépôts ; les profils peuvent ajouter des exigences, jamais supprimer les fondations.

## Structure conceptuelle

Un paquet contient : identité et version sémantique ; IDs de règles stables ; règles typées ; portées d'applicabilité ; relations explicites (dépendance, raffinement, remplacement, incompatibilité) ; paramètres typés ; exceptions bornées ; profils du dépôt ; métadonnées de projection (document, langue, section, stratégie de génération/vérification). C'est un contrat conceptuel, pas une syntaxe de sérialisation. Le format reste à choisir.

Un ID de règle est immuable et jamais réutilisé. Toute évolution sémantique exige revue et traçabilité. Une règle retirée reste référencée par tombstone ou remplacement.

## Contrats de version du produit et du package

GovCheck possède deux contrats de publication distincts :

- **Produit GovCheck** (**govcheck.product**) : le produit distribuable complet et ses interfaces publiques déclarées, notamment l'exécutable/la CLI et les surfaces d'intégration prises en charge lorsqu'elles seront publiées.
- **Package de gouvernance réutilisable** (**govcheck.governance-package**) : le package consommable indépendamment situé sous **govcheck/**, copié ou installé par bootstrap dans les dépôts gouvernés. Son contrat couvre le modèle de gouvernance, les règles, les profils, le comportement du bootstrap et les interfaces du package prises en charge.

Chaque contrat possède sa propre séquence SemVer, sa propre évaluation de compatibilité, son autorisation et son identité de publication immuable. Une release du produit peut inclure une version donnée du package de gouvernance, mais aucune des deux versions ne se déduit de l'autre. Un tag Git identifie une release du dépôt et son commit ; il n'attribue automatiquement la version d'aucun de ces deux contrats.

Cette spécification n'attribue encore aucune version au produit ni au package. Une première publication est une décision explicite d'initial publication, et non un incrément MAJOR/MINOR/PATCH inventé. Une chaîne SemVer complète comporte trois composantes numériques (par exemple **0.1.0**) ; une abréviation telle que **v0.1** n'est pas une identité de release complète.

Avant 1.0.0, le contrat concerné est explicitement en développement initial : selon SemVer, tout peut évoluer et l'API publique ne doit pas être considérée comme stable. Une modification qui rompt un contrat pré-1.0 déjà déclaré exige néanmoins une évaluation explicite de compatibilité, une note de migration et un incrément MINOR, plutôt qu'un PATCH silencieux. À partir de 1.0.0, les règles normales MAJOR/MINOR/PATCH fondées sur la compatibilité s'appliquent.

Le produit et le package peuvent évoluer à des rythmes différents. Une modification de la CLI GovCheck peut incrémenter le contrat produit sans modifier le package de gouvernance. Une modification d'une règle normative peut incrémenter le contrat du package sans imposer d'incrément produit si les interfaces et garanties du produit restent inchangées. Les marqueurs de format des schémas, révisions d'artefacts, ADR, exécutions, preuves et décisions conservent leurs propres règles d'identité ; ils ne reçoivent pas SemVer du seul fait de leur inclusion dans une release.

## Sémantique des règles

Distinguer au minimum : obligation, interdiction, permission, invariant/contrainte, exigence de preuve, exigence de processus/approbation et conseil. Le conseil est explicitement non normatif. L'absence d'interdiction ne vaut pas permission. Une permission n'annule pas une obligation ou interdiction sans relation de priorité explicite et valide.

## Applicabilité et composition

Le contexte identifie explicitement états du dépôt et candidat, révision de gouvernance, changement, ressources touchées, classe d'acteur et faits d'environnement déclarés. Les fondations obligatoires s'appliquent toujours. Les profils précisent ou ajoutent des contraintes. Une portée étroite ne peut affaiblir silencieusement une règle obligatoire. Les priorités forment une relation partielle explicite, jamais un ordre de fichiers ou un « dernier arrivé ».

Contradictions non résolues, types inconnus, version majeure non prise en charge, portées mal formées, références absentes ou priorité ambiguë constituent une erreur de gouvernance. L'acceptation échoue de manière fermée.

## Exceptions

Une exception identifie les règles et portées exactes, motif, responsable du risque, autorité approbatrice, dates de début/expiration, mesures compensatoires et état exact du dépôt/de la gouvernance. Elle est auditable et révocable. Une exception expirée, non approuvée, hors portée ou liée à un autre état est invalide. Elle ne peut supprimer les fondations formelles, effacer l'historique ni transformer rétroactivement un échec en succès.

## Évaluation

À entrées canoniques et sémantique épinglée identiques, l'évaluation est déterministe. Elle rapporte règles applicables, résultats satisfaits/non satisfaits/indéterminés/en conflit, lacunes de preuves, validité des exceptions, explications et provenance. Résultats agrégés : réussi, échoué, bloqué/indéterminé, gouvernance invalide. Pour accepter, indéterminé ne signifie pas satisfait. Les conseils sont séparés.

## Projections documentaires

Une projection indique révision canonique et version du générateur/vérificateur. GovCheck doit la générer ou vérifier ses énoncés normatifs et détecter les dérives. Les explications libres sont permises si identifiées non normatives. Une projection ne peut inventer de règle, omettre silencieusement une règle obligatoire ou modifier sa force par traduction. L'anglais est la langue par défaut ; le français en préserve le sens. Une divergence est un défaut documentaire, pas une seconde autorité.

## Confiance, choix ouverts et conformité

Le modèle est une donnée, pas du code : aucun script arbitraire du dépôt n'est exécuté. Tout futur langage d'expression sera typé, borné, déterministe et limité en ressources. Les faits externes portent source et fraîcheur ; le modèle ne prouve pas leur vérité. Sérialisation, schéma, langage d'expression, canonicalisation, signatures et distribution restent à décider après comparaison.

Une implémentation devra démontrer IDs stables, composition déterministe, conflits explicites, exceptions bornées, blocage en cas d'indétermination, versions épinglées, détection de dérive et explications reproductibles. Ce sont des objectifs, pas des garanties actuelles.
