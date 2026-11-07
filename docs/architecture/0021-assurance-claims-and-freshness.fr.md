# 0021 — Affirmations, arguments et fraîcheur des preuves

**Statut :** proposition de sémantique formelle à examiner ; elle ne devient pas une règle normative approuvée par sa seule présence. Elle raffine la spécification 0005 et le métamodèle 0013. **English:** [0021](0021-assurance-claims-and-freshness.md).

## 1. Objet

Définir le sens calculable d'un dossier d'assurance : quelles affirmations sont étayées, par quels éléments et sous quelles hypothèses ; quand un élément cesse d'être utilisable ; comment cette invalidation remonte dans l'argumentation ; et quand le dossier peut soutenir une décision d'acceptation.

Le modèle ne transforme pas un statut en vérité. Il calcule un statut relatif à un sujet, à des dépendances déclarées, à une méthode, à une provenance et à une autorité de revue. La véracité externe et l'adéquation sémantique restent des questions distinctes.

## 2. Objets et relations

- **Claim / affirmation** : proposition réfutable, identifiée de façon stable, avec sujet, périmètre, source normative, méthode admissible, producteur, réviseur, hypothèses, limites et critères de réfutation.
- **Argument** : décomposition d'une affirmation en sous-affirmations et éléments probants. La composition initiale est conjonctive : toutes les feuilles requises doivent être étayées. Les stratégies alternatives (OR), pondérations et calculs probabilistes sont hors de ce premier modèle.
- **Evidence / élément probant** : résultat d'une méthode, observation, attestation ou dérivation. Son résultat est distinct de son admissibilité, de sa fraîcheur et de son authenticité.
- **Dependency / dépendance** : identité versionnée dont dépend l'élément : candidat/base, gouvernance, spécification, modèle, outil, configuration, environnement, source externe, identité ou clé, selon la méthode.
- **Assumption / hypothèse** : prémisse déclarée, avec source, propriétaire, périmètre, validité et possibilité de réfutation. Une hypothèse n'est pas une preuve. La première machine TLA+ ne calcule pas encore leur justification ; elle la laisse comme limite explicite.
- **Decision / décision** : acte d'une autorité compétente sur un sujet exact et un instant/contexte déterminé.

Relations typées : decomposesInto, supportedBy, refutedBy, dependsOn, assumes, verifiedBy, reviewedBy et supersedes. Elles sont identifiées ; aucune relation n'est inférée du voisinage documentaire.

## 3. Graphe d'argumentation

Le graphe des sous-affirmations doit être acyclique. Une affirmation ne peut se soutenir elle-même, directement ou par un cycle. Chaque affirmation possède une fermeture transitive des éléments probants requis : les éléments directement attachés et ceux de toutes ses sous-affirmations. Cette fermeture peut être calculée par l'implémentation ou fournie par un index vérifié ; elle doit être contrôlée contre les arêtes du graphe.

La composition proposée est prudente :
- toutes les feuilles requises sont présentes ;
- chaque élément requis est courant et porte un résultat favorable ;
- aucune réfutation ou contradiction courante n'est ignorée ;
- les hypothèses requises sont explicites et satisfaites selon une politique approuvée ;
- chaque claim de la fermeture est explicitement revu par l'acteur désigné, habilité et distinct de son producteur. L'action TLA+ ReviewClaim enregistre cette revue ; une modification de preuve, de dépendance ou l'expiration l'invalide.

Un résultat favorable sur une seule feuille ne rend pas l'argument global favorable. Une preuve absente, inconnue, non exécutée, non prise en charge ou incomplète ne devient jamais un succès par défaut.

## 4. Fraîcheur : identité, dépendances et temps

La fraîcheur n'est pas seulement un âge maximal. Pour un élément e, elle dépend au minimum de :

1. **Liaison au sujet** : dépôt, base, candidat, état natif VCS et cible concernés correspondent exactement au sujet évalué.
2. **Liaison aux versions** : pour chaque dépendance déclarée d, la révision observée par e est celle qui est courante.
3. **Validité temporelle** : la fenêtre de validité déclarée n'est pas expirée, selon une horloge et une politique explicites.
4. **Révocation** : ni l'élément, ni l'identité, ni la clé, ni l'autorité pertinente n'a été révoqué.
5. **Intégrité et provenance** : le contenu et la chaîne de production sont vérifiables selon les hypothèses de confiance déclarées.

Dans le modèle borné, les dépendances sont des identifiants versionnés, l'expiration est un entier logique, et la révocation est explicite. Les signatures, la confiance des producteurs, l'horloge réelle et les preuves de liaison au VCS sont hors de ce modèle.

Une preuve peut rester historiquement vraie tout en devenant inutilisable pour une décision actuelle. L'invalidation ne supprime ni l'élément ni son ancien résultat : elle modifie son admissibilité pour l'évaluation présente. La revalidation produit une nouvelle observation liée aux versions courantes ; elle ne réécrit pas silencieusement l'ancienne.

## 5. Propagation de l'invalidation

Une modification de dépendance rend obsolètes les éléments qui la déclarent. La conséquence remonte à toutes les affirmations dont la fermeture transitive contient l'un de ces éléments. Les revues concernées sont également invalidées : elles doivent être renouvelées après republication/revalidation. La propagation est déterministe et transitive ; elle ne dépend pas d'une intervention manuelle ni de l'ordre d'affichage des claims.

Priorité des statuts calculés :
1. Conflict si des éléments courants se contredisent ou si un élément courant déclare explicitement un conflit ;
2. Stale si au moins un élément requis est expiré, révoqué ou lié à une ancienne version ;
3. Refuted si un élément courant réfute l'affirmation ;
4. Incomplete, Unsupported, NotRun ou Unknown si les éléments requis ne permettent pas une conclusion favorable ;
5. Supported seulement si tous les éléments requis sont courants et favorables et si la revue indépendante est valide ;
6. NotIndependentlyReviewed si le contenu paraît favorable mais que l'exigence d'indépendance n'est pas satisfaite.

Une contradiction n'est pas résolue en choisissant arbitrairement la preuve la plus récente ou la plus favorable. La politique de résolution doit être explicitement gouvernée.

Une décision d'acceptation est un instantané. Si une dépendance, un élément probant ou sa validité temporelle change ensuite, la décision courante est invalidée lorsque cela affecte la fermeture du claim racine. L'historique conserve la décision passée et son invalidation ; il ne la réécrit pas.

## 6. Contrat avec le modèle de cycle de vie existant

Le modèle govcheck.lifecycle reste responsable de la phase, du tuple (baseId, candidateId, governanceId, specId), des approbations, de l'acceptation et de l'application du candidat exact. Il efface déjà l'évaluation et les preuves abstraites lors de ChangeInputs, mais ne connaît pas les dépendances individuelles des preuves ni le graphe d'arguments.

Le nouveau modèle govcheck.assurance est volontairement séparé et composable :
- il calcule le statut du claim racine à partir du graphe et de la fraîcheur des éléments ;
- il n'autorise une acceptation d'assurance que si le claim racine est Supported ;
- une modification d'une dépendance pertinente, une révocation, une republication ou une expiration invalide l'instantané d'acceptation ;
- le modèle de cycle de vie doit consommer ce résultat comme précondition de Accept, sans fusionner les identités natives Git/Pijul ni confondre approbation et preuve.

Le pont d'intégration à implémenter ensuite est une relation de raffinement : Lifecycle.Accept est autorisé seulement si Assurance.ClaimStatus(root) = Supported, et l'identité de toutes les dépendances du claim est incluse dans le contexte d'évaluation. Le présent modèle ne prétend pas que ce pont existe déjà dans le module de cycle de vie.

## 7. Assertions du modèle TLA+

Le module formal/tla/GovCheckAssurance.tla et sa configuration bornée vérifient :

| Assertion | Sens |
|---|---|
| TypeOK | Les versions, statuts, horloge, révocations et instantané d'acceptation restent dans leurs domaines. |
| ArgumentGraphWellFormed | Les sous-claims descendent strictement en rang ; la fermeture contient les preuves directes et celles des descendants ; les dépendances correspondent à cette fermeture. |
| ReviewBinding | Chaque revue enregistrée appartient à un réviseur autorisé, distinct du producteur, et porte encore sur des preuves courantes et favorables. |
| ClaimStatusSoundness | Un claim calculé Supported ne contient que des preuves courantes et favorables et toutes les revues requises. |
| AcceptedImpliesSupported | Une acceptation enregistrée implique que le claim racine est encore étayé. |
| AcceptedDependencySnapshotCurrent | Les versions des dépendances pertinentes n'ont pas changé depuis l'acceptation. |
| RevokedEvidenceNotCurrent | Un élément révoqué ne peut être considéré comme courant. |
| AcceptedDiscipline | Propriété temporelle : toute acceptation présente reste étayée dans chaque état atteint. |

La configuration contient un claim racine, un sous-claim, deux éléments probants et deux dépendances. Elle explore les actions ReviewClaim, les modifications de version, la republication/revalidation, la révocation, l'expiration et l'acceptation. La revue du claim racine exige aussi celle de tous ses sous-claims. Cette borne sert à trouver des contre-exemples dans cette abstraction ; elle ne prouve ni la complétude du graphe en production ni la conformité de l'implémentation.

## 8. Limites et décisions non prises

Le modèle ne traite pas encore : la vérité des sources externes ; l'authenticité cryptographique et la révocation des clés ; les hypothèses et dérogations gouvernées ; les stratégies d'argumentation alternatives ; la confiance ou l'indépendance des outils ; les horloges distribuées ; la concurrence entre publication, révocation, acceptation et application ; l'intégrité append-only de l'historique ; la confidentialité/rétention des preuves ; ni le raffinement vers le stockage et l'évaluateur réels.

Il ne choisit ni format canonique, ni ontologie, ni moteur de règles, ni assistant de preuve. Il ne crée pas de niveaux d'assurance selon la taille du dépôt.

## 9. Vérification et statut

Le module et la configuration sont des sources formelles proposées. Ils doivent être analysés par SANY puis explorés par TLC avec une version épinglée. Aucun résultat SANY/TLC n'est revendiqué par cette proposition. Les tests structurels et la revue du source ne remplacent pas l'exécution de TLC. La CI hébergée n'est pas déclenchée dans cette contribution ; les contrôles devront être exécutés selon l'autorisation du mainteneur et les instructions du dépôt.

## Références bibliographiques

- [R-05 — Modélisation par transitions d'états TLA+ / TLC](../references.fr.md#r-05)
- [R-09 — Moteur de décision de politiques Open Policy Agent](../references.fr.md#r-09)
- [R-18 — Évaluation de Writ à partir des sources](../references.fr.md#r-18)
- [R-22 — Sémantiques natives Git et Pijul](../references.fr.md#r-22)
