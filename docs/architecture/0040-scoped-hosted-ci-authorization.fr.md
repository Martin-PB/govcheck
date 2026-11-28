# 0040 — Autorisation limitée de CI hébergée pour le dépôt GovCheck public

**Statut :** autorisation opérationnelle acceptée, enregistrée le 28-11-2026 à partir de la déclaration explicite du mainteneur du 09-11-2026. Il ne s'agit pas d'une adoption du modèle de gouvernance normatif.

## Contexte

La politique temporaire du bootstrap interdit la CI hébergée sans autorisation explicite. Le mainteneur a explicitement autorisé l'utilisation de GitHub Actions hébergé pour le dépôt public `Martin-PB/govcheck`, en précisant que ces exécutions ne consomment pas son quota personnel de crédits Actions et peuvent être utilisées sans limite.

## Décision et périmètre

Jusqu'à révocation, cette autorisation permet à ChatGPT/aux agents travaillant sur ce dépôt d'exécuter GitHub Actions pour la CI du dépôt, les tests, les vérifications de modèles formels et les workflows de reproduction, y compris les exécutions nécessaires à la validation du travail.

L'autorisation s'applique **uniquement** au dépôt public :

- `Martin-PB/govcheck`

Elle ne s'étend pas aux autres dépôts personnels ou organisationnels.

## Exclusions

Cette autorisation ne permet **pas** :

- de fusionner une PR sans l'approbation applicable du mainteneur ;
- de contourner la protection de branche ou de modifier les rulesets, checks requis, secrets, variables ou permissions du dépôt ;
- de créer, installer ou configurer une GitHub App ou un service externe au nom du mainteneur ;
- d'exposer, créer ou renouveler des clés privées, identifiants ou secrets de signature ;
- d'exécuter des workflows de déploiement, publication de releases ou mutation de comptes externes ;
- de considérer une CI verte comme une adoption normative, une revue indépendante, une preuve formelle de l'implémentation ou un enforcement effectif de la branche protégée.

Seuls les workflows de validation/reproduction sans effet externe et sans modification de l'administration du dépôt sont couverts. Tout workflow introduisant un nouvel effet externe nécessite une autorisation distincte.

## Révocation et réexamen

Le mainteneur peut révoquer ou restreindre cette autorisation à tout moment. Elle doit être réexaminée si le dépôt devient privé, est transféré, change de propriétaire/organisation ou si les paramètres Actions/compte concernés changent substantiellement.

## Source et dossiers associés

- Autorisation explicite du mainteneur enregistrée dans l'issue [#88](https://github.com/Martin-PB/govcheck/issues/88), datée du 09-11-2026.
- Politique temporaire : [BOOTSTRAP_GOVERNANCE.fr.md](../BOOTSTRAP_GOVERNANCE.fr.md).
- Ruleset courant et limites d'acceptation effective : issue [#45](https://github.com/Martin-PB/govcheck/issues/45).

Ce document formalise l'autorisation limitée existante ; il n'autorise aucune autre action ni aucun autre dépôt.
