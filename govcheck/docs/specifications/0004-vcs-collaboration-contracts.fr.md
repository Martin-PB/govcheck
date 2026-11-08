# Spécification 0004 — Contrats des adaptateurs VCS et collaboration

**Statut :** architecture proposée, prête pour revue. **English:** [0004](0004-vcs-collaboration-contracts.md).

## Séparation

Quatre dimensions indépendantes : VCS (Git/Pijul/futur), hébergement (local/équipe/auto-hébergé/public), collaboration (individuel/partagé/revue/patch/demande d'intégration), acceptation/application (locale/équipe/forge/application native). Le cœur possède la sémantique ; les adaptateurs la traduisent. Aucune dépendance du cœur à GitHub, GitLab, Nest ou un transport.

## Contrat VCS

L'adaptateur fournit identité native, descripteurs/empreintes d'état exacts et reproductibles, comparaison base/candidat, ressources touchées, changements/dépendances/conflits natifs, inspection en lecture seule par défaut, application explicite avec préconditions, déclaration de capacités et erreurs précises. Il ne doit ni aplatir les sémantiques ni prétendre que tout VCS possède commits, branches et historique linéaire.

### Git

Identifier dépôt, commit et tree ; expliciter sous-modules, index et worktree. Un commit seul ne décrit pas nécessairement les contenus modifiés/non suivis. Le candidat précise s'il s'agit d'un commit ou instantané index/worktree. Rapporter ancêtres et conflits natifs. Vérifier base et candidat attendus avant mutation.

### Pijul

Préserver identités/dépendances des patches, identité/état des canaux, graphe et conflits natifs. Empreinter le graphe/état pertinent, pas seulement le nom du canal ou un hash isolé. Utiliser les opérations natives ; ne jamais synthétiser des commits Git ni déduire les conflits Pijul d'outils textuels. Une propriété non établie est indéterminée, jamais réussie.

## Hébergement et collaboration

L'hébergement transporte/localise l'état sans redéfinir le VCS. L'usage local seul est complet. Les adaptateurs de collaboration relient participants, revues, décisions, approbations, patches et demandes d'intégration aux IDs de changement et candidats exacts. Une PR/MR est un objet de collaboration, pas le changement.

Déclarer les capacités : lire les revues, authentifier les réviseurs, demander approbation, bloquer intégration, appliquer candidat, observer contournements. Toute lacune est visible. Commentaire/réaction ne vaut pas approbation sans règle explicite et identité vérifiable.

## Limites d'application

Hooks et wrappers locaux sont contournables par qui accède au système de fichiers. Une application partagée forte exige un serveur d'équipe ou une forge imposant une décision liée à l'état exact et à la révision de gouvernance. Une capacité absente est une limite, jamais un succès. Une signature peut établir intégrité/origine sous hypothèses de clés, pas correction ni autorité à elle seule.

## Échecs et conformité

Distinguer absence, non-prise-en-charge, indisponibilité, péremption, conflit, échec d'authentification/autorisation et état mal formé. Toute mutation exige intention et préconditions ; un échec partiel n'est jamais un succès atomique. Les tests couvriront état Git sale/sous-modules, arbres exacts, graphe/patches/conflits Pijul, usage local, capacités, courses, préconditions et lacunes d'application. Aucun adaptateur n'est implémenté.

## Références primaires

- La documentation primaire de Git et Pijul est regroupée sous [R-22 dans le catalogue de références du package](../references.fr.md#r-22).

Ces sources décrivent les sémantiques des VCS sous-jacents ; elles ne démontrent pas que les adaptateurs GovCheck sont implémentés ou conformes.
