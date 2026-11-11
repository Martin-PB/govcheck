# Gouvernance applicable à la frontière du dépôt et préconditions externes des usines logicielles IA

**Statut :** recherche non normative et proposition de classification soumise à la revue du mainteneur. Ce dossier propose une manière de classer les préoccupations ; il n'adopte aucune règle normative, aucun produit, aucune architecture cloud ni aucun workflow obligatoire.
**Préparé le :** 2026-11-11.

## Source et périmètre

Cette revue fait suite à la conférence de Zach Lloyd à AI Engineer, [« How to Build a Software Factory That Improves Itself »](https://youtu.be/nKjPBAw_N_0), cataloguée en [R-162](../references.fr.md#r-162). Elle la confronte à la [présentation officielle de Warp Factories](https://docs.warp.dev/factories/) et à sa [documentation des workflows](https://docs.warp.dev/factories/how-factories-work) ([R-163](../references.fr.md#r-163)), à un essai contrôlé randomisé sur l'assistance IA pour des développeurs expérimentés de projets open source ([R-164](../references.fr.md#r-164)), au profil NIST de gestion des risques de l'IA générative ([R-165](../references.fr.md#r-165)), aux recommandations SSDF déjà référencées ([R-02](../references.fr.md#r-02)), à la référence existante sur l'isolation des agents ([R-79](../references.fr.md#r-79)) et à DORA 2025 ([R-148](../references.fr.md#r-148)).

La conférence recommande de traiter le développement agentique comme un système d'infrastructure et de workflow, plutôt que comme une collection d'agents sollicités individuellement : définir les workflows sous forme de code, isoler les exécutions, conserver de la flexibilité entre modèles et harnesses, enregistrer les exécutions, les évaluer sur des tâches propres au projet, mesurer coût/durée/qualité et utiliser les échecs pour proposer des améliorations. La documentation de Warp explicite une limite importante : les instructions de la factory peuvent définir des points de contrôle humains, mais ce sont les permissions du dépôt et les protections de branche — pas le prompt d'un agent — qui imposent qui peut approuver ou fusionner. Ce sont des observations industrielles utiles, pas une preuve que Warp ou une factory cloud soit nécessaire ou suffisant pour GovCheck.

## 1. La question de conception

GovCheck est un bootstrap de gouvernance généraliste pour dépôts ; il ne doit pas prétendre qu'un exécutable local peut contrôler tous les systèmes qui entourent le dépôt. La question pratique est :

**Pour chaque préoccupation de gouvernance, que peut-on vérifier ou imposer de manière déterministe à la frontière du dépôt ; que peut-on seulement enregistrer ou évaluer comme élément probant ; qu'est-ce qui dépend d'acteurs ou d'infrastructures externes ; et que faut-il conserver comme avertissement, hypothèse ou décision d'acceptation explicite ?**

Cette classification doit porter sur chaque contrôle proposé, pas étiqueter un sujet entier comme « applicable » ou « inapplicable ». Par exemple, un dépôt peut exiger la déclaration d'un profil de sandbox et valider sa configuration, tout en étant incapable de prouver que l'isolation réelle du fournisseur distant fonctionne comme annoncé.

## 2. Classes d'applicabilité candidates

Ces étiquettes sont proposées pour l'audit ; elles ne constituent pas encore le vocabulaire adopté de GovCheck. Leur sémantique doit être confrontée au métamodèle actuel avant d'ajouter de nouveaux concepts.

| Classe | Sens | Réponse appropriée du dépôt |
|---|---|---|
| **E — Imposable localement** | Le dépôt possède les entrées nécessaires et peut décider de la conformité de manière déterministe dans une frontière de confiance définie. | Valider schémas, politiques, signatures, artefacts requis, résultats de tests, transitions d'état permises ou prédicats de release ; échouer de façon fermée si la politique adoptée l'exige. |
| **V — Vérifiable uniquement avec des preuves externes** | L'affirmation ne peut être vérifiée qu'avec une preuve fournie par un acteur/fournisseur de confiance ou une attestation interrogeable. | Lier la preuve à son émetteur, son périmètre, sa date, sa configuration et sa révision ; contrôler format, provenance et validité ; expliciter ce que la preuve n'établit pas. |
| **O — Observable/enregistrable, non imposable par GovCheck seul** | Le sujet peut être mesuré ou déclaré, mais GovCheck ne peut pas faire en sorte que le système concerné se comporte comme annoncé. | Enregistrer mesures, source, méthode, incertitude et responsable ; comparer à un critère explicitement adopté s'il existe ; ne pas présenter un score comme une garantie. |
| **P — Précondition externe** | Le succès dépend d'une infrastructure, de personnes, d'une organisation, de conditions de service, de secrets ou de décisions hors de l'autorité du dépôt. | Déclarer hypothèse/précondition, responsable, méthode de vérification et conséquence d'échec ; exiger une acceptation explicite ou bloquer toute affirmation qui en dépend. |
| **W — Avertissement / heads-up** | Le dépôt peut signaler un risque ou une limite importante, mais ne peut pas y remédier seul, ou aucune politique adoptée n'en fait un motif de rejet. | Émettre un avertissement contextualisé avec justification et action/preuve suggérée ; distinguer avertissement et échec ; permettre une décision de risque autorisée lorsque la gouvernance le permet. |
| **X — Hors du périmètre d'imposition du dépôt** | Le sujet ne peut raisonnablement être contrôlé ou observé de manière fiable à cette frontière. | Déclarer la limite et le risque résiduel ; ne pas revendiquer de couverture. Réexaminer seulement si la frontière du système ou l'autorité disponible change. |

Les classes peuvent se combiner. Par exemple, vérifier localement une configuration de runner déclarée est E ; prouver l'efficacité de l'isolation sous-jacente du fournisseur cloud peut être V ou P ; le risque résiduel d'une compromission du fournisseur peut rester W/P/X. La classification doit identifier l'*affirmation* et la *frontière*, pas seulement le thème.

## 3. Carte initiale des préoccupations

Il s'agit d'hypothèses à vérifier dans le prochain audit GovCheck, et non de l'affirmation que tous ces contrôles existent déjà ou font défaut.

| Préoccupation | Classe probable à la frontière du dépôt | Ce que GovCheck peut raisonnablement faire | Ce qui reste hors de son contrôle direct |
|---|---|---|---|
| Fichiers de gouvernance, schémas, champs requis et liens internes | E | Analyser et valider les déclarations appartenant au dépôt ; rejeter les artefacts mal formés ou incohérents. | La véracité des déclarations. |
| Contrôles requis et preuves liées à un commit/une révision | E/V | Exiger des enregistrements de preuve, vérifier identité des artefacts et métadonnées de fraîcheur, rejeter les preuves absentes ou périmées si la politique l'exige. | La véracité des preuves externes et l'exhaustivité des propriétés contrôlées. |
| Définitions de workflows CI et résultats d'exécution des tests | E/V | Inspecter les workflows versionnés ; consommer des résultats identifiés/signés ; vérifier les jobs attendus et leur rattachement à la révision. | Intégrité des runners, disponibilité de la plateforme, exposition des secrets, ou pertinence des exigences encodées dans les tests. |
| Protections de branches, revues et permissions de fusion de la forge | V/P | Documenter les réglages attendus et, si les API/permissions le permettent, les inspecter ; vérifier leur état avant toute affirmation. | Privilèges administrateur/de contournement, pannes de forge, dérive des politiques et actes des humains autorisés. |
| Workflows d'agents définis dans le dépôt | E | Revoir les changements de configuration, valider les schémas, versionner prompts/rôles/permissions d'outils et tester les prédicats déterministes. | Sémantique réelle d'exécution du fournisseur, valeurs par défaut cachées et non-déterminisme des modèles. |
| Profil de sandbox déclaré comme code | E/V | Vérifier que le profil déclaré respecte la politique locale et que les exécutions identifient ce profil. | Efficacité des contrôles hôte/noyau/cloud, résistance aux évasions, canaux auxiliaires et opérations du fournisseur. |
| Secrets et identifiants | E/V/P | Détecter les secrets interdits dans les fichiers suivis ; déclarer les catégories de secrets requises et les attentes de moindre privilège ; examiner les preuves de permissions disponibles. | Configuration du gestionnaire de secrets, fuites à l'exécution, accès fournisseur, rotation et pratiques humaines sans preuve intégrée. |
| Choix du modèle/harness et reproductibilité | E/O | Enregistrer, lorsque disponible, identifiants et versions du modèle, prompts, configuration d'outils, paramètres d'échantillonnage et contexte de tâche. | Mises à jour cachées des modèles, poids indisponibles, changements côté fournisseur et reproductibilité exacte des services stochastiques. |
| Coût, latence, débit et métriques de qualité | O/V | Définir sémantique, unités, dénominateurs, périmètre, provenance, incertitude et règles de comparaison ; calculer à partir des enregistrements disponibles. | Adéquation des métriques à la valeur métier, événements manquants, exactitude de facturation du fournisseur ou généralisation future. |
| Évaluation par LLM / notation produite par un agent | V/O | Exiger identité/version du juge, grille, jeu de calibration, échantillonnage, analyse des désaccords/erreurs et critères d'escalade humaine. | Fiabilité du juge, angles morts partagés, erreurs corrélées entre évaluateur et générateur et choix subjectifs de la grille. |
| Benchmarks locaux et rejeu de tâches | E/O | Versionner tâches, résultats attendus, environnement, logique de notation et révisions du benchmark ; comparer les configurations sur les mêmes cas. | Représentativité, biais de sélection, fuite de données, évolution des tâches réelles et validité externe. |
| Auto-amélioration de la factory | E/V | Exiger que les changements proposés soient versionnés, revus et contrôlés comme les autres changements du dépôt ; enregistrer l'exécution et les preuves qui motivent chaque proposition. | Transfert d'une amélioration au-delà du benchmark et chemin de déploiement réel de la plateforme externe. |
| Revue humaine, expertise, formation et effectifs | P/O | Spécifier rôles requis, attestations, périmètre de revue, conflits et preuves de réalisation lorsque la politique le permet. | Compétence réelle, attention, incitations organisationnelles, capacité et indépendance effective du reviewer. |
| Propriété des données, confidentialité, résidence et rétention | V/P | Enregistrer hypothèses de flux de données, destinations approuvées, déclarations de politique et attestations fournisseur ; signaler l'absence de conditions/preuves. | Traitement réel par le fournisseur, sous-traitants, interprétation juridique, suppression des sauvegardes, juridiction et exécution contractuelle. |
| Résultats opérationnels après release | O/V | Enregistrer incidents, défauts, rollback, maintenance, reprises et observations ultérieures liés aux révisions livrées. | Télémétrie complète, contexte utilisateur, causes externes et attribution causale. |
| Autorité humaine pour accepter un risque ou fusionner | E/V/P | Encoder les enregistrements d'approbation requis et les protections de dépôt lorsqu'elles existent ; distinguer approbation et preuve technique. | Assurance d'identité, collusion, contournement administrateur, changements hors bande et légitimité du modèle d'autorité lui-même. |

## 4. Ce que les sources disent — et ne disent pas

La recommandation « mesurer sur ses propres tâches » est un bon principe expérimental, pas une garantie. L'essai randomisé de METR portait sur 16 développeurs expérimentés, 246 tâches et des dépôts matures que les participants connaissaient ; il a constaté une augmentation de 19 % du temps de réalisation avec les outils IA du début 2025 dans ce contexte, alors que les participants s'attendaient à un gain. Ce résultat ne se généralise pas à tous les développeurs ni aux outils actuels ; il montre toutefois pourquoi il faut distinguer productivité auto-déclarée, performance sur benchmark et résultats mesurés. Voir [R-164](../references.fr.md#r-164).

La documentation de Warp décrit une implémentation commerciale particulière : définitions de factory versionnées, étapes d'agents, évaluateurs, benchmarks, propositions d'auto-amélioration et points de validation humaine. C'est un exemple industriel concret, pas une norme neutre. En particulier, le score d'un juge LLM est lui-même un élément probant produit par un évaluateur faillible, pas une vérité terrain. Une configuration de factory versionnée dans Git ne prouve pas, à elle seule, que le runtime cloud a exécuté exactement cette configuration ni que les permissions externes ont été appliquées correctement.

Le profil NIST AI RMF pour l'IA générative donne des recommandations de gestion des risques aux organisations ; ce n'est pas un moteur d'application local au dépôt. SSDF et les sources de provenance/chaîne d'approvisionnement informent également les pratiques, mais citer ces références ne prouve pas qu'une implémentation particulière est conforme.

## 5. Fiche de frontière proposée pour chaque exigence ou affirmation

Avant d'implémenter un contrôle, l'audit devrait pouvoir répondre à ces questions :

1. **Affirmation/contrôle :** quelle propriété ou obligation exacte est revendiquée ?
2. **Frontière et sujet :** quel dépôt, quelle révision, quel runner, service, équipe, agent ou organisation est concerné ?
3. **Classe d'applicabilité :** E, V, O, P, W ou X (ou combinaison documentée).
4. **Autorité :** qui peut l'imposer, qui peut l'attester et qui peut accepter le risque résiduel ?
5. **Mécanisme :** contrôle local déterministe, attestation externe, observation, avertissement ou hypothèse explicite ?
6. **Contrat de preuve :** source/émetteur, méthode et version, périmètre, date, rattachement à la révision/configuration, règle de fraîcheur/invalidation et limites connues.
7. **Sémantique d'échec :** rejeter, bloquer une affirmation, demander une preuve, avertir ou autoriser une exception validée ?
8. **Risque résiduel :** qu'est-ce qui reste non vérifié, qui en est responsable et quelle décision est requise ?
9. **Contournement et modèle de menace :** qui peut modifier la règle, supprimer le signal, altérer le runner, falsifier la preuve ou contourner le point d'application ?
10. **Déclencheur de revue :** quel changement ou quelle observation impose une réévaluation ?

Ne pas ajouter un nouvel objet de métamodèle simplement parce que cette liste est utile. Il faut d'abord relier chaque champ aux concepts existants de revendication, exigence, politique, décision, preuve, hypothèse, exception et autorité ; tout véritable manque d'expressivité devra être documenté avant de proposer un changement de schéma.

## 6. Cas adversariaux pour de futurs tests

Ils ne sont ni implémentés ni exécutés par ce changement de recherche. Les confronter aux fixtures existantes sur le cycle de vie, la frontière d'application et la fraîcheur des preuves avant d'en créer de nouvelles.

- **SF-01 — Garde-fou limité au prompt :** le prompt dit « ne jamais fusionner sans approbation », mais le jeton possède le droit de fusion et aucune protection de branche n'est active.
- **SF-02 — Sandbox déclarée, runtime non vérifié :** le dépôt déclare un profil approuvé, mais l'enregistrement d'exécution n'identifie pas la configuration/runtime effectif.
- **SF-03 — Benchmark vert, cible inadéquate :** le benchmark passe alors que ses tâches ne représentent pas les changements à haut risque du dépôt.
- **SF-04 — Juge corrélé au générateur :** la même famille de modèles produit le code et juge sa qualité, sans calibration ni échantillon indépendant.
- **SF-05 — Dénominateur coût/qualité mouvant :** une configuration semble moins chère parce que retries, revue, exécutions échouées ou reprises en aval ont été exclus.
- **SF-06 — Contournement de l'auto-amélioration :** une modification de la définition de factory proposée par un agent est déployée hors du chemin de revue et de CI requis.
- **SF-07 — Attestation fournisseur périmée :** la preuve de sécurité/isolation porte sur une ancienne image de runner, un ancien compte, une région ou une configuration antérieure.
- **SF-08 — Précondition externe absente :** le dépôt affirme que la résidence des données est garantie sans preuve du fournisseur, du contrat ou du runtime.
- **SF-09 — Avertissement présenté comme une contrainte :** la documentation affirme que GovCheck empêche un risque alors qu'il ne fait qu'émettre un avertissement.
- **SF-10 — Contournement autorisé :** un administrateur privilégié contourne les contrôles requis ; le rapport affirme malgré tout que la frontière d'intégration a été imposée sans réserve.

Comportement attendu : déclarer précisément quel prédicat a été contrôlé, sur quelle révision/configuration, par quelle autorité, avec quelles preuves et limites. Une garantie externe manquante ne doit jamais devenir silencieusement un contrôle local réussi.

## 7. Prochaine étape proposée

Utiliser l'audit de gouvernance et d'assurance existant pour classer les exigences et contrôles actuels, en commençant par la frontière d'application du dépôt, la provenance/fraîcheur des preuves, l'autorisation et l'applicabilité aux révisions. Maintenir un registre des écarts avec une ligne par *affirmation/contrôle*, pas une ligne par thème général. Pour chaque ligne, noter : couverture actuelle, classe, mécanisme local, dépendance externe, preuve requise, comportement en cas d'échec, chemin de contournement, responsable du risque résiduel et issue/décision liée.

Ne pas supposer que GovCheck doit exploiter une usine logicielle cloud. Son objectif est de gouverner les dépôts et de rendre explicites les frontières d'assurance entre différents workflows et forges. Un dépôt peut décrire et valider son contrat local, demander ou vérifier des preuves externes lorsque des intégrations existent et refuser des affirmations injustifiées ; il ne peut transformer un fournisseur non fiable, une capacité organisationnelle insuffisante, des mesures peu fiables ou un contournement privilégié en garantie par le seul fait de les documenter.

## 8. Traçabilité

Nouvelles références : [R-162](../references.fr.md#r-162), [R-163](../references.fr.md#r-163), [R-164](../references.fr.md#r-164), [R-165](../references.fr.md#r-165). Références existantes : [R-02](../references.fr.md#r-02), [R-03](../references.fr.md#r-03), [R-79](../references.fr.md#r-79), [R-148](../references.fr.md#r-148). Ce dossier reste non normatif jusqu'à sa revue par le mainteneur habilité.
