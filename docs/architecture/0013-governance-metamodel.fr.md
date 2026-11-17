# 0013 — Métamodèle de gouvernance : objectifs, exigences, normes et assurance

**Statut :** métamodèle conceptuel proposé pour revue ; aucune sérialisation ni implémentation n’est sélectionnée. **English:** [0013](0013-governance-metamodel.md).

## Pourquoi un métamodèle

La gouvernance d’un dépôt dépasse les commandes shell et instructions aux agents. Elle exprime pourquoi le projet existe, ce qu’il doit accomplir, les contraintes applicables, son architecture, les propriétés attendues et les preuves étayant les affirmations sur le résultat.

Le métamodèle préserve les distinctions entre intention, obligation, propriété, implémentation et preuve. Sans cela, le sens d’un contrôle en échec devient ambigu.

## Vocabulaire fondamental

| Concept | Signification | À ne pas confondre avec |
|---|---|---|
| Objectif | Résultat ou valeur recherchée | Contrôle exécutable |
| Exigence | Énoncé à satisfaire par système/processus | Test ou tâche d’implémentation |
| Norme/règle | Directive avec force déontique et périmètre explicites | Conseil informel |
| Propriété | Prédicat sur états, traces, structures ou comportements | Seul texte de l’exigence |
| Contrat | Hypothèses, garanties et obligations à une frontière | Preuve globale |
| Élément d’architecture | Composant, interface, frontière de confiance ou relation | Exigence |
| Modèle | Abstraction avec variables, transitions et hypothèses | Implémentation |
| Artefact d’implémentation | Source, binaire, configuration ou composant déployé | Preuve de sa correction |
| Contrôle/méthode | Procédure examinant une affirmation | Affirmation elle-même |
| Témoin/preuve | Observation, artefact ou dérivation pertinente | Vérité par sa seule existence |
| Affirmation (claim) | Proposition précise sur un sujet et un périmètre | Badge générique |
| Argument | Raisonnement à partir d’affirmations, hypothèses et preuves | Seul rapport de test |
| Décision/autorité | Résolution autorisée, avec provenance et périmètre | Préférence du contributeur |

Une exigence se raffine en sous-exigences et se relie à des propriétés. Les propriétés sont examinées par des méthodes ; les méthodes produisent des preuves ; les affirmations dépendent de preuves et d’hypothèses. Les relations sont explicites, pas déduites de la proximité documentaire ou du nommage.

Les enregistrements de décision doivent rendre leurs éléments de raisonnement inspectables. Le modèle PEAK fournit un cadre utile : Problem (problème), Experience (expérience), Assumptions (hypothèses) et Knowledge (connaissances) sont consignés séparément avant d'enregistrer une Solution et un risque assumé. Ce risque doit être relié aux hypothèses, observations et affirmations pertinentes, avec périmètre, justification, responsable redevable et conditions de réexamen/expiration. Il ne constitue pas en soi une autorisation d'accepter le risque ; l'acceptation reste une décision gouvernée distincte du principal autorisé. PEAK complète les relations typées du métamodèle entre décisions, hypothèses, affirmations et preuves ; ce n'est ni un score de risque ni un argument d'assurance. Les hypothèses restent réfutables et les observations peuvent les remettre en cause. Voir [R-74](../references.fr.md#r-74).

Ne pas fusionner **le risque assumé PEAK**, un **scénario de risque**, une **évaluation du risque**, un **traitement du risque**, le **risque résiduel** et l'**acceptation du risque**. La sortie de risque assumé consigne ce qui pourrait ne pas fonctionner comme prévu ; une évaluation est une analyse distincte liée à une méthode ; un traitement modifie l'exposition ; l'acceptation est une disposition autorisée. Probabilité quantitative, appartenance floue, non-déterminisme, taux de transition, coûts et confiance conservent également des sémantiques distinctes. Voir [R-193](../references.fr.md#r-193) et la [clarification de recherche sur la décision et le risque](../research/decision-and-assumed-risk-crosscutting-2026-11.fr.md).

## Force normative

Distinguer obligation, interdiction, permission explicite, invariant/contrainte, exigence de preuve, exigence de processus/approbation et recommandation non contraignante. L’absence d’interdiction ne vaut pas permission. Une recommandation ne bloque pas l’acceptation. Les règles dérogeables exigent une sémantique explicite de priorité/exception ; conflits et précédences non résolues restent visibles.

La logique déontique peut formaliser des modalités telles que l'obligation, la permission et l'interdiction, mais elle ne fournit pas la sémantique d'autorité, de périmètre, de priorité, de délégation, d'exception, de date d'effet, de preuve ou d'application d'un système de gouvernance. La vérification des modèles/politiques de contrôle d'accès doit examiner séparément cohérence, complétude et propriétés de sûreté avant de tester un évaluateur ou un point d'application. Voir [R-93](../references.fr.md#r-93) et [R-88](../references.fr.md#r-88).

## Périmètre, raffinement et réalisabilité

Chaque objet possède identité stable, historique d’évolution, périmètre, provenance, propriétaire/autorité et relations typées. L’applicabilité peut dépendre du type de changement, des composants affectés, de la menace, du déploiement, des capacités VCS ou du profil projet. Les profils sélectionnent des obligations ; ils ne créent pas de niveaux d’assurance selon la taille du dépôt.

Relations possibles : raffine, dérive-de, satisfait, contraint, entre-en-conflit-avec, remplace, dépend-de, vérifié-par, étayé-par et approuvé-par. Chacune nécessite une sémantique définie.

La cohérence n’est pas la réalisabilité : un ensemble cohérent peut être impossible sous contraintes de ressources, plateforme, temps ou interface. Distinguer contradiction, conflit de périmètre/précédence, raffinement manquant/circulaire, infaisabilité, sous-spécification et sémantique non prise en charge.

Le métamodèle doit accueillir exigences orientées objectifs (dont raffinement KAOS/GORE), logique déontique, temporelle, des prédicats/relationnelle et contrats assume-guarantee. Ce sont des familles conceptuelles, pas un choix d’outil.

## Graphe de traçabilité de l'assurance et décisions transversales

Un **chemin de traçabilité** représentatif (pas un cycle de vie obligatoire ni une séquence de décisions) est :

`Intention/Source → Objectif/Besoin → Exigence/Norme → Propriété/Contrat → Modèle → Implémentation → Contrôle/Méthode → Preuve/Témoin → Affirmation → Argument`

La granularité varie selon le projet et le graphe n'a pas à être globalement acyclique. Liens manquants, sauts injustifiés, contradictions, mappings non pris en charge et soutiens circulaires restent visibles. Les exigences peuvent avoir plusieurs origines ; décisions et éléments probants peuvent être reliés à plusieurs nœuds. Un test sans lien à une affirmation n'établit pas la conformité du projet. Une propriété formelle sans source normative approuvée n'est pas automatiquement une obligation du projet.

**La décision est un objet transversal de premier rang, pas le dernier nœud de ce chemin.** Une décision peut créer, sélectionner, raffiner, justifier, autoriser, rejeter, contraindre, suspendre, remplacer ou révoquer tout nœud ou relation : intention, objectif, exigence, propriété, modèle, implémentation, méthode de vérification, élément probant/affirmation, argument d'assurance, exception, déploiement ou autre décision. Le graphe doit préserver l'autorité, le contexte, la portée, la justification, les alternatives, les conditions, la révision de gouvernance applicable, la provenance, la validité temporelle et les conditions de réexamen/révocation. Une décision d'acceptation est un type particulier de décision qui peut suivre une évaluation d'assurance ; elle ne fait pas de la prise de décision une étape terminale.

Distinguer les éléments probants/l'assurance qui étayent une affirmation, l'autorité habilitée à décider et la décision effectivement prise. Une décision peut accepter une assurance incomplète ou une exposition résiduelle uniquement si les éléments manquants, hypothèses, limites et risques assumés restent explicites. Une telle décision ne transforme pas un témoignage en preuve et ne rend pas impossible un scénario incertain.

Le graphe répond aux questions dans les deux sens : pourquoi un artefact ou une règle existe et quelles décisions l'autorisent ou le contraignent ; quels objectifs une propriété soutient ; quels composants sont affectés ; quelles preuves soutiennent/réfutent une affirmation ; ce qui est inconnu/obsolète/non pris en charge ; et qui a autorisé une exception ou une acceptation de risque, pour quelle portée, sous quelle révision de politique et jusqu'à quand.

## Pipeline d’interprétation

Un futur évaluateur devrait analyser/canonicaliser sans encodage ambigu ni identité dupliquée ; résoudre versions, références et autorité ; déterminer l’applicabilité ; composer règles/profils ; détecter conflits, ambiguïtés et constructions non prises en charge ; dériver obligations/propriétés/preuves requises ; expliquer chaque résultat par les règles sources ; évaluer les affirmations sans traiter l’absence comme un succès ; puis appliquer l’acceptation après satisfaction des conditions et contrôles d’autorité.

C’est une cible de conception, pas un évaluateur implémenté.

## Exigences candidates d’assurance de GovCheck

La discussion a identifié quatre identifiants candidats. Ce sont des propositions, pas des règles approuvées :

- `GOV-ASSURANCE-001` : aucune règle normative n’est perdue silencieusement entre source approuvée, représentation canonique, sémantique évaluateur et projections contrôlées.
- `GOV-ASSURANCE-002` : toute interprétation formelle est traçable à sa source, version, justification et approbation autorisée.
- `GOV-ASSURANCE-003` : les propriétés de correction de GovCheck sont formalisées et vérifiées dans un périmètre et une base de confiance déclarés.
- `GOV-ASSURANCE-004` : chaque résultat de conformité possède un argument d’assurance révisable indépendamment et lié au sujet exact et aux révisions pertinentes.

Les mainteneurs doivent adopter et enregistrer ces identifiants avant qu’ils ne deviennent contraignants.

## Choix ouverts

Vocabulaire ontologique, sérialisation, représentation du graphe, logique, langage de requête, assistant de preuve et algorithme de validation restent ouverts. Prototyper identité stable, relations typées, provenance, périmètre, composition, traces d’explication et échec déterministe avant de choisir une ontologie ou pile de preuve volumineuse.


## Références bibliographiques

- [R-01 — contrôles NIST de sécurité et de confidentialité](../references.fr.md#r-01)
- [R-09 — moteur de décision de politiques Open Policy Agent](../references.fr.md#r-09)
- [R-10 — langage d’autorisation Cedar](../references.fr.md#r-10)
- [R-13 — contrats structurels JSON Schema](../references.fr.md#r-13)
- [R-44 — KAOS et ingénierie des exigences orientée objectifs](../references.fr.md#r-44)
- [R-74 — modèle PEAK de décision de projet](../references.fr.md#r-74)
- [R-193 — modélisation probabiliste, floue et à transitions d'états](../references.fr.md#r-193)
- [R-88 — vérification NIST SP 800-192 des modèles/politiques de contrôle d'accès](../references.fr.md#r-88)
- [R-92 — modélisation des exigences orientée objectifs iStar 2.0](../references.fr.md#r-92)
- [R-93 — logique déontique et modalités normatives](../references.fr.md#r-93)
