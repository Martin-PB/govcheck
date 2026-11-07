# ADR 0001 : périmètre produit et architecture du bootstrap

- **Statut :** accepté comme socle initial ; toute évolution exige une ADR qui le remplace explicitement.
- **Date :** 2026-11-05
- **Périmètre :** identité du produit, autorité normative, empreinte d'exécution, VCS/hébergement, assurance et maintenabilité.

## Contexte

GovCheck gouverne les dépôts logiciels et leur cycle de développement. Il n'est pas principalement une sandbox d'agents, une passerelle d'appels d'outils, un plan de contrôle hébergé, un remplacement de CI ou un assemblage d'analyseurs. Ce dépôt est au bootstrap initial : aucun exécutable, moteur canonique, preuve formelle ou mécanisme d'application par une forge n'existe. Cette ADR consigne des décisions de conception, pas des garanties implémentées.

## Décisions

1. **Gouvernance centrée sur le dépôt.** Le dépôt et le cycle de vie de ses changements sont gouvernés. Développeurs et agents sont des contributeurs. GovCheck fournira contexte, exigences applicables, préparation des changements, décisions, dérogations, évaluations, preuves et conditions d'acceptation.
2. **Une seule autorité normative.** Un modèle canonique de gouvernance, versionné et lisible par machine, interprété par GovCheck, sera l'autorité. Markdown (AGENTS.md, GOVERNANCE.md, SECURITY.md, CONTRIBUTING.md) sera une projection contrôlée ou une explication et ne devra pas introduire silencieusement de règles contradictoires. Sa sémantique reste à concevoir.
3. **Fondations formelles pour chaque dépôt.** Les fondations de gouvernance et d'assurance s'appliquent quelle que soit la taille du dépôt. Les exigences et preuves propres au projet varient ; l'existence du modèle formel ne varie pas.
4. **Exécutable local, sans MCP ni service hébergé obligatoire.** Un petit exécutable local est l'interface principale pour les personnes, scripts, CI et agents capables d'exécuter des commandes. Aucun service hébergé, daemon résident ou serveur MCP n'est requis. Une sortie lisible par machine est attendue. Un exécutable portable ne peut empêcher universellement les modifications locales directes ; l'acceptation doit valider indépendamment les preuves.
5. **Séparer VCS, hébergement, collaboration et acceptation.** Git et Pijul sont de première classe et sémantiquement distincts. Usages locaux, serveurs d'équipe, hébergements auto-gérés et publics sont dans le périmètre. Patches, dépendances, canaux et conflits Pijul doivent être représentés nativement, sans les aplatir en commits et branches Git.
6. **Noyau réduit et adaptateurs étroits.** Préférer un noyau de gouvernance/assurance réduit, des profils déclaratifs et des adaptateurs étroits à un système dynamique de plugins. Réutiliser les outils des projets ; ne présumer aucune pile obligatoire importante.
7. **Bootstrap non destructif.** Initialisation et migration suivent inspecter → planifier → appliquer, préservent les fichiers, détectent les conflits et exigent une revue pour les changements destructeurs ou normatifs.
8. **Anglais par défaut, français en parallèle.** L'anglais est la langue d'accueil et de présentation par défaut. Les documents destinés aux utilisateurs et les décisions d'architecture ont des pendants français qui préservent le sens et le statut du texte anglais.
9. **Méthodes formelles fondatrices.** La sémantique de gouvernance et le cycle de vie doivent être conçus pour l'analyse formelle. Lean est candidat pour la logique critique de preuve ; TLA+ ou d'autres méthodes peuvent convenir aux transitions et processus distribués. Aucun langage d'implémentation ni outil formel n'est choisi ici.
10. **Précision des preuves.** Distinguer exécution de contrôles, model checking, vérification de preuves et conformité de l'implémentation. Les preuves identifient sujet, portée, hypothèses, outil/version et état exact du dépôt et de la gouvernance. Un résultat sur un modèle n'est pas automatiquement une affirmation sur l'implémentation.

## Conséquences

- Le cœur ne doit pas coder en dur les concepts GitHub.
- Les adaptateurs VCS préservent les sémantiques natives d'identité et d'état de Git et Pijul.
- L'application par les forges relève des adaptateurs ; l'usage local seul reste complet.
- L'exécutable est l'interface principale ; MCP n'est pas requis.
- Le premier jalon est le contrat canonique de gouvernance et la sémantique du cycle de vie, pas une multitude d'intégrations.
- La politique temporaire reste en vigueur jusqu'à ce que le moteur canonique évalue et applique le modèle.
- La documentation est bilingue, anglais d'abord et par défaut.

## Décisions ouvertes

Langage et distribution ; format des données/règles ; stratégie de formalisation et socle de confiance ; acceptation locale et résistance au contournement ; contrats et empreintes d'état Git/Pijul ; modèle de collaboration/forges ; licence ; contrôles de référence et plateformes.

Toute évolution de ces frontières exige une ADR qui remplace celle-ci. Ne pas réécrire silencieusement cette décision historique.

English: [ADR 0001](0001-bootstrap-boundaries.md).

## Références bibliographiques

- [R-05 — Modélisation par transitions d'états TLA+ / TLC](../references.fr.md#r-05)
- [R-20 — Assistant de preuve Lean](../references.fr.md#r-20)
- [R-22 — Sémantiques natives Git et Pijul](../references.fr.md#r-22)
