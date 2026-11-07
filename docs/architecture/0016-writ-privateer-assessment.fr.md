# 0016 — Évaluation de Writ et Privateer fondée sur leurs sources

**Statut :** revue circonscrite des dépôts publics identifiés ci-dessous, dans leur état de branche par défaut au 6 novembre 2026. Ce n’est ni un audit de sécurité, ni une reproduction indépendante, ni une décision d’adoption. **English:** [0016](0016-writ-privateer-assessment.md).

## 1. Périmètre et désambiguïsation

Le nom « Writ » est ambigu. Cette évaluation concerne [`infinri/Writ`]([R-18](../references.fr.md#r-18)), décrit par son dépôt comme un runtime de gouvernance pour Claude Code. Elle n’évalue pas les produits distincts writ.now, withwrit.com ou usewrit.app.

Privateer désigne ici [`privateer-agent/privateer-agent`]([R-19](../references.fr.md#r-19)), une distribution MIT et multi-fournisseurs de l’agent de programmation Pi. Il ne s’agit pas d’autres produits portant le même nom.

Instantanés examinés :
- Writ `main` : `ebdafe5450b201339f81e717ed104e6bcfd3fe3e` (3 novembre 2026).
- Privateer `main` : `181a988e443fa6b6b4138fc349d1260c96408ad4` (3 novembre 2026).

La revue porte sur les descriptions publiques et certains documents d’architecture/sécurité. Elle ne prétend pas avoir construit, installé, exécuté, fuzzé ou audité indépendamment ces projets.

## 2. Writ : ce que décrivent les sources

Writ est un runtime local de gouvernance de flux de travail, spécifique à Claude Code. Le dépôt décrit des hooks Claude Code autour des événements d’outils, un daemon local et une base Neo4j stockant règles et décisions. Il combine récupération de règles/contexte, barrières de flux codées et continuité des décisions.

Les capacités documentées comprennent :
- modes et phases de flux ;
- barrières de plan et de squelette de tests avant les écritures de source en mode travail ;
- approbation humaine représentée par un jeton lié à la barrière et à l’empreinte du plan ;
- contrôles à l’écriture, refus de chemins de credentials et périmètres d’écriture de rôles/projets ;
- récupération de règles, rappel de décisions et dossiers de session ;
- journaux structurés d’événements de barrières sélectionnés.

Ces fonctions concernent le **flux de travail de l’agent et le contrôle de ses actions**. Elles ne remplacent pas le modèle canonique de gouvernance GovCheck, le dossier de changement, les sémantiques natives Git/Pijul, le dossier d’assurance ou le prédicat d’acceptation du candidat exact.

### Frontières de sécurité documentées par Writ lui-même

Le propre fichier `SECURITY.md` de Writ précise que Writ n’est ni bac à sable ni frontière de sécurité, que ses hooks s’exécutent avec les privilèges shell de l’utilisateur et que l’API du daemon est sans authentification, reposant sur une écoute localhost par défaut. Il documente des contournements de l’inspection des écritures shell. Si le daemon ne répond pas et que le repli local ne peut obtenir aucun verdict, l’écriture continue par défaut ; `WRIT_STRICT=1` modifie ce comportement pour le chemin d’écriture.

Ce sont des limites explicites, pas une base pour supposer le confinement d’un agent malveillant. Une API locale sans authentification demande aussi de la prudence sur les hôtes partagés et face aux processus locaux qui peuvent y accéder.

### Rôle potentiel aux côtés de GovCheck

Writ peut être évalué comme **adaptateur facultatif de flux pour agent spécifique** ou source de preuves d’exécution circonscrites. Il ne doit devenir ni l’autorité normative de GovCheck, ni son autorité d’acceptation, ni une dépendance d’exécution obligatoire. Tout événement de barrière doit être traité comme une affirmation issue de l’installation Writ et lié à l’agent/session, au candidat, à la configuration et à la révision Writ. Ce n’est pas une preuve indépendante simplement parce que Writ l’a émise.

Avant intégration, tester :
- l’événement exact émis pour autorisation/refus/approbation et sa liaison au candidat/règles ;
- le comportement fail-open/fail-closed de chaque hook et chemin de panne du daemon ;
- les contournements par formes shell, chemins d’écriture alternatifs et opérations directes filesystem/VCS ;
- identité de session, portée des jetons d’approbation, concurrence et protection des fichiers d’état ;
- contrôle d’accès à l’API du daemon, exposition multi-utilisateur, confidentialité des journaux et mises à jour ;
- barrières bloquantes versus simples alertes.

Ne pas présenter Writ comme un bac à sable adversarial : sa propre politique de sécurité rejette cette interprétation.

## 3. Privateer : ce que décrivent les sources

Privateer est une distribution de l’agent de programmation Pi, pas un moteur de gouvernance de dépôt. Son dépôt annonce des fournisseurs de modèles interchangeables, une barrière de permissions pour commandes shell, modifications de fichiers et actions réseau, des connecteurs MCP, sous-agents, workflows et avertissement de confidentialité avant l’envoi de données personnelles vers un modèle non vérifié. Il propose une CLI/desktop local et des modes facultatifs sans surveillance ou hébergés.

Le `SECURITY.md` du dépôt décrit des contrôles de chaîne d’approvisionnement utiles : absence de scripts d’installation dans le paquet publié, installation recommandée avec scripts npm désactivés, vérifications de provenance/signature, contrôle de somme des bundles et commande `privateer verify` distinguant vérification réussie et résultat indéterminé. Ce sont des affirmations documentées par le projet ; cette revue ne les a pas reproduites indépendamment.

### Frontières de sécurité et d’assurance

La barrière de permissions de Privateer est un contrôle utile **au niveau agent/harness**, mais pas l’autorité de gouvernance GovCheck. Le dépôt documente `--no-quarter` comme option désactivant entièrement la barrière et déconseille son emploi avec du contenu non fiable ou un système contenant des données précieuses. On ne peut donc traiter l’invite de permission locale comme une frontière d’acceptation impossible à contourner.

Ses fonctions de confidentialité sont également distinctes de la conformité du dépôt :
- un avertissement PII local ne prouve pas que chaque secret/donnée privée est détecté ;
- le mode de calcul confidentiel attesté d’un fournisseur ne s’applique que si ce fournisseur/mode est sélectionné et si ses hypothèses d’attestation tiennent ;
- provenance et sommes de contrôle aident à évaluer origine/intégrité d’un artefact, mais ne prouvent pas la justesse de la politique ou la sûreté du code ;
- modes cloud/Harbor facultatifs ont une posture de confiance et de localisation des données différente de la CLI locale.

### Rôle potentiel aux côtés de GovCheck

Privateer est un **candidat de harness pour tester l’interopérabilité**, pas une dépendance ni un moteur de politique GovCheck. Il permet de tester si un agent basé sur Pi peut découvrir et suivre le contrat CLI, et si des preuves peuvent être recueillies sans donner à l’agent l’autorité d’approuver son propre travail. Ses sorties de barrière restent des preuves produites par l’agent, sauf validation séparée.

Avant toute intégration en production, tester défauts et contournements de la barrière, frontières locales/réseau, routage fournisseur et sortie des données, propagation MCP/sous-agents, identité de session/preuve, contrôles provenance/dépendances et distinction exacte entre exécution locale et hébergée.

## 4. Adéquation comparative

| Dimension | Cible GovCheck | Writ (`infinri/Writ`) | Privateer (`privateer-agent/privateer-agent`) |
|---|---|---|---|
| Objet principal | Dépôt et changement proposé exact | Session/flux Claude Code et événements d’outils | Session d’agent et travail de programmation délégué |
| Autorité normative | Source canonique du dépôt (prévue) | Corpus/graphe de règles local pour barrières Writ | Configuration agent, permissions et instructions projet chargées |
| Barrières | Prédicat d’acceptation/application à une frontière déclarée | Barrières d’outils et approbations humaines dans hooks Claude Code | Barrière de permissions par action dans le harness |
| Identité du changement | Tuple exact base/candidat/gouvernance/spécification (prévu) | À vérifier indépendamment avant d’utiliser comme preuve GovCheck | À vérifier indépendamment avant d’utiliser comme preuve GovCheck |
| Sémantiques VCS | Git et Pijul comme adaptateurs natifs distincts (prévu) | Ne remplace pas les contrats VCS natifs | Basé sur Pi ; ne remplace pas le contrat VCS GovCheck |
| Autorité indépendante d’acceptation | Requise pour application partagée | Non établie par les hooks d’agent | Non établie par la barrière de permissions |
| Confinement adversarial | Déclarer frontière réelle et limites | Explicitement pas un bac à sable ; contournements/panne ouverte documentés | Barrière désactivable ; pas une frontière indépendante d’acceptation |
| Hypothèse d’intégration | Cœur gouvernance/dossier | Adaptateur facultatif Claude Code / source de preuves | Fixture d’agent Pi / source de preuves facultative |
| Décision | Produit central | Ne pas adopter comme cœur ni lui attribuer une garantie de bac à sable | Ne pas adopter comme moteur de gouvernance central |

## 5. Recommandation

1. **Conserver la frontière produit GovCheck.** Aucun des deux projets ne remplace modèle canonique, dossier d’assurance ou acceptation du candidat exact.
2. **Les utiliser comme fixtures de test, pas comme dépendances.** Writ teste l’application des règles au moment des outils ; Privateer teste l’interopérabilité d’un agent Pi et sa barrière de permissions.
3. **Définir d’abord un contrat CLI/dossier neutre.** Les intégrations consomment la même sémantique normative, sans décisions de politique concurrentes.
4. **Traiter leurs sorties comme des preuves avec provenance et limites.** Lier révision outil, configuration, session, candidat et invocation ; valider indépendamment si requis.
5. **Exécuter des tests adversariaux avant de se fier aux barrières.** Inclure fail-open, contrôles désactivés, modifications filesystem/VCS directes, approbations obsolètes, confusion de session, exposition d’API locale et sortie de données.
6. **Ne choisir aucun des deux comme dépendance obligatoire à ce stade.** Les éléments actuels justifient une évaluation complémentaire, pas la conclusion que l’un satisfait toutes les exigences GovCheck.

## Sources

Les URL des sources primaires, révisions épinglées et documents examinés sont maintenus dans le [catalogue central des références](../references.fr.md), entrées R-18 et R-19. Ce document renvoie vers ces entrées sans dupliquer les URL externes.

## Références bibliographiques

Références externes citées dans ce document : [R-18](../references.fr.md#r-18), [R-19](../references.fr.md#r-19).
