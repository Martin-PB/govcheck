# 0010 — Assurance, témoignage, preuve et conformité

**Statut :** approfondissement de la discussion GovCheck des 5–6 novembre 2026. Complète la mémoire 0009 et la spécification 0005 ; ne les remplace pas. **Français :** [0010](0010-assurance-proof-and-conformance.fr.md).

## 1. Le problème fondateur : l'auto-certification ne suffit pas

GovCheck ne doit pas seulement exécuter des contrôles. Il doit empêcher le producteur d'un changement — humain ou agent — d'être la seule autorité qui déclare ce changement conforme.

Un contributeur peut déclarer les exigences qu'il croit applicables, les commandes exécutées, les résultats observés, les tests réussis ou échoués, ses hypothèses et les dérogations demandées. Ces déclarations sont des entrées utiles, mais pas une vérification indépendante par le seul fait d'être affirmées. Un agent ne peut transformer son propre récit, son rapport généré ou son verdict en autorité finale. La même règle vaut pour un humain.

GovCheck évalue indépendamment le contrat de gouvernance et les éléments présentés. Cette indépendance dépend du parseur, de l'évaluateur, des outils, des identités, des sources d'autorité, des adaptateurs et de la frontière d'application. Elle doit être argumentée et documentée, jamais suggérée par une coche verte.

Chaîne de responsabilité : source normative approuvée → interprétation des règles applicables → affirmation circonscrite → éléments probants → argumentation et hypothèses → décision par l'autorité compétente → acceptation du candidat exact → application native du candidat exact. Aucune étape ne peut être remplacée par l'auto-description du contributeur.

## 2. Trois questions d'assurance indépendantes

### 2.1 GovCheck est-il correct par rapport à sa spécification formelle ?

C'est une question de correction de l'implémentation : parseur conforme à la canonicalisation ; composition des règles correcte ; rejet des obligations indéterminées ; gardes de transition respectées ; adaptateur préservant l'identité native du candidat ; implémentation raffinant le modèle.

Éléments possibles : tests, tests fondés sur les propriétés, model checking, preuve d'un composant, compilation vérifiée, preuve de raffinement. Ils ne sont pas équivalents. Une suite de tests ne couvre pas tous les cas ; un modèle vérifié ne prouve pas l'implémentation ; un théorème sur une fonction ne prouve pas l'exécutable entier.

### 2.2 La spécification traduit-elle fidèlement la gouvernance approuvée ?

C'est une question de fidélité normative. Un évaluateur parfaitement vérifié peut implémenter une spécification incomplète, ambiguë ou erronée. Prouver l'implémentation de la spécification ne prouve pas que celle-ci exprime les bonnes règles.

La fidélité exige une chaîne traçable : clause/décision approuvée → identifiant canonique de règle → force normative et applicabilité → prédicat/transition formalisé → propriété/vecteur de test → approbation par l'autorité compétente. Les projections Markdown et traductions préservent le sens. L'assistance sémantique, y compris par IA, peut détecter ambiguïtés, contradictions et lacunes, mais ne devient pas l'autorité normative. Un réviseur habilité approuve l'interprétation. Un agent ne peut approuver sa propre interprétation.

### 2.3 Le projet et le changement exact sont-ils conformes ?

C'est une question de conformité du sujet. Les éléments doivent être liés aux identités exactes du dépôt, de la base, du candidat, de la gouvernance, de la spécification et de l'environnement pertinent. La correction de GovCheck ne prouve pas la conformité du projet. Un build réussi ne couvre pas toutes les obligations. Une signature ne prouve pas la pertinence ou la vérité du contenu. Une approbation ne remplace pas les preuves techniques.

| Question | Sujet | Pont nécessaire | Raccourci invalide |
|---|---|---|---|
| Correction | Implémentation GovCheck | Conformité implémentation-spécification | « Les tests passent, donc le programme est correct. » |
| Fidélité | Interprétation normative | Traçabilité et approbation | « L'évaluateur est prouvé, donc la politique est juste. » |
| Conformité | Candidat exact | Éléments liés au sujet et autorité | « GovCheck est vérifié, donc le changement est conforme. » |

L'effectivité réelle du mécanisme déployé est une quatrième question : un évaluateur local correct peut être contourné ; une barrière peut être désactivée ; un processus peut échouer en exploitation.

## 3. Test, témoignage, élément probant, attestation, preuve

**Test = témoignage d'exécution.** Il indique qu'une invocation déterminée, avec programme, entrées et environnement donnés, a produit une observation. Son enregistrement lie révision exacte, candidat, suite/données, commande/arguments, versions d'outils, environnement, identité et dates d'exécution, sorties/code retour, exécution partielle ou interrompue, provenance et intégrité.

Une suite réussie établit que les cas testés ont produit les observations attendues dans les conditions enregistrées. Elle n'établit pas la correction pour toutes les entrées, l'absence de défaut non testé, la correction de l'oracle, la validité normative de l'exigence, la vérité des faits externes, la conformité d'un autre candidat ni la résistance au contournement. Un échec peut fournir un contre-exemple si le test et l'observation sont fiables. Une réussite est un élément positif circonscrit, pas une preuve universelle. Cela vaut pour tests unitaires, intégration, système, régression, sécurité, fuzzing, propriétés et bout en bout.

**Élément probant** est plus large que test : résultats de build/scan, rapports de model checking, objets/résultats de preuve, attestations, identités VCS/diffs, décisions de revue, mesures opérationnelles, faits externes et dérivations reproductibles. Il peut étayer, réfuter ou laisser une affirmation indéterminée. Les contradictions restent visibles. Un élément n'est pas vrai parce qu'il est stocké, hashé, signé ou étiqueté « vérifié ».

**Attestation** lie une déclaration à un producteur, un sujet et un contexte. Une signature peut établir intégrité et origine sous hypothèses de gestion des clés. Elle n'établit pas seule l'autorité du signataire, son indépendance, l'exécution réelle, l'absence de compromission du runner, l'identité de l'entrée, la pertinence de la sortie ni la vérité d'un fait externe. Authenticité, intégrité, autorité, pertinence et vérité sont distinctes.

**Preuve mathématique** est une dérivation contrôlée relativement à une logique, un noyau, des définitions, axiomes, hypothèses et imports. Le dossier identifie le théorème, la version du noyau, axiomes/imports, hypothèses, obligations admises, fonctionnalités non sûres/oracles et dépendances. Le noyau établit la dérivabilité dans ce système ; il ne prouve pas que l'énoncé représente le besoin réel ou que le programme l'implémente sans pont formel.

## 4. Model checking, preuve et conformité

**Model checking** explore les états atteignables d'un système formel. Une exploration exhaustive terminée établit les propriétés pour tous les états atteignables du modèle configuré. Une exploration bornée/réduite ne vaut que dans ses bornes et hypothèses. Un rapport TLA+/TLC identifie révision/empreinte du modèle, versions TLC/Java, configuration/constantes, symétries/réductions/contraintes, équité, propriétés, nombres d'états/transitions, achèvement, interblocages/contre-exemples et bornes. Un contre-exemple montre un comportement du modèle qui viole la propriété. Une réussite ne prouve pas le programme réel.

**Preuve par théorème** établit la dérivabilité d'une proposition à partir d'axiomes et hypothèses. Prouver les propriétés mathématiques du prédicat d'acceptation ne prouve pas que le programme le calcule correctement. Prouver l'évaluateur conforme à la spécification ne prouve pas la fidélité normative de celle-ci.

**Conformité/raffinement** est le pont entre modèle et exécutable. Il identifie les révisions, l'artefact construit, la frontière d'abstraction, le comportement observable, la relation de raffinement/simulation, les hypothèses et la méthode. Implémentation vérifiée, preuve de raffinement, génération vérifiée, raffinement de traces, tests différentiels et vecteurs de conformité ne sont pas équivalents. Des exemples réussis ne prouvent pas un raffinement complet.

**Fidélité normative** porte sur le passage des règles approuvées au modèle, aux prédicats, tests et documents. Elle exige traçabilité et autorité. Les outils formels contrôlent la cohérence après approbation du sens ; ils ne choisissent pas le sens au nom de l'organisation.

## 5. Les trois dimensions d'assurance

Elles sont complémentaires, pas des niveaux de maturité interchangeables.

- **Mécanique :** schémas/types, canonicalisation, clés dupliquées, identifiants/références, versions, hashes, signatures, empreintes exactes, champs et fraîcheur des preuves, dérive documentaire, enregistrement reproductible, évaluation déterministe, gardes et préconditions d'adaptateurs. Le succès établit le prédicat mécanique déclaré, pas la justesse sémantique, la vérité externe ou l'effectivité.
- **Assistée sémantiquement :** interprétation de la couverture des règles, contradictions de sens, adéquation des tests, fidélité des prédicats, traduction, hypothèses cachées/circulaires et pertinence des éléments. Analyse statique, expertise, argumentation et IA aident à trouver lacunes et ambiguïtés ; ce n'est pas une vérité automatique. Enregistrer réviseur, autorité, raisonnement, sources, incertitude et objections. L'agent ne s'auto-approuve pas.
- **Effectivité opérationnelle :** résistance réelle aux contournements, désactivation de barrières, application d'un autre candidat, preuve obsolète, clé révoquée, courses, scripts malveillants et pannes. Éléments : tests adversariaux, exercices de contournement, audits, incidents, red team, supervision et vérification de la frontière d'intégration. L'effectivité dépend du contexte et du temps ; une preuve de fonction pure ou un test unitaire ne l'établit pas.

## 6. Modes opérationnels

Les modes décrivent l'utilisation, pas une méthode de preuve ni un niveau d'assurance.

- **inspect** : examen en lecture seule ; indique présence, absence, obsolescence, conflit, non-prise en charge ou indétermination ; ne modifie rien et n'accepte rien.
- **audit** : évaluation structurée et traçable d'un état/période ; conserve affirmations, éléments, hypothèses, autorité, dérogations, lacunes et limites. Le rapport atteste qu'un audit a eu lieu, pas que chaque affirmation est vraie, et ne bloque pas automatiquement.
- **enforce** : applique le prédicat à la frontière d'acceptation/intégration ; bloque échec, conflit, indétermination obligatoire, preuve invalide/obsolète, approbation absente/non autorisée ou tuple discordant ; exige une autorité capable d'empêcher l'application et revérifie le candidat exact juste avant celle-ci.

Un exécutable local peut inspecter, auditer et évaluer localement. Il ne peut empêcher seul un utilisateur privilégié de modifier les fichiers ou de contourner l'outil. L'application partagée forte appartient à une frontière d'intégration de confiance. Signaler un échec n'est pas l'appliquer.

## 7. Statuts de preuve

Ne pas réduire les résultats à un booléen. Distinguer **Pass/étayé**, **Fail/réfuté**, **Unknown/indéterminé**, **Not run/non exécuté**, **Not applicable/non applicable**, **Unsupported/non pris en charge**, **Incomplete/incomplet**, **Stale/invalidated/obsolète ou invalidé**, **Conflict/conflit**. Inconnu, non exécuté et non pris en charge ne sont pas des succès. Ils bloquent les obligations obligatoires sauf exception explicite, valide et gouvernée. Une exception ne transforme pas l'inconnu en preuve.

Chaque affirmation possède identifiant, proposition précise, sujet/état cible, source normative, périmètre, méthodes admissibles, éléments, hypothèses/dépendances, limites/réfutations, producteur, vérificateur indépendant, statut et date. L'argumentation décompose en sous-affirmations ; les soutiens circulaires ne sont pas une corroboration indépendante.

## 8. Acceptation : décision de gouvernance

L'obligation formelle retenue est :

`Accepted(change, target_state) ⇒ GovernanceSatisfied(change, target_state)`

C'est une exigence de sûreté du mécanisme d'acceptation, pas l'affirmation que le changement est sans défaut. Le prédicat couvre dépôt/base/candidat exacts, état cible et périmètre, révisions/sémantique de gouvernance et spécification, toutes les exigences obligatoires, éléments admissibles liés au sujet et frais, résultats explicites sans convertir fail/conflit/unknown/unsupported/not-run/incomplete en succès, approbations autorisées liées au changement/candidat/gouvernance exacts, dérogations avec périmètre/autorité/motif/expiration/mesures compensatoires, versions/configurations de l'évaluateur et capacité d'application/limites de contournement.

Un résultat pour un candidat ne se réutilise pas pour un autre candidat, rebase, canal Pijul ou version de gouvernance/spécification sans nouvelle analyse. L'acceptation est dérivée, jamais un booléen fourni par le contributeur. Ce n'est ni test, ni théorème, signature, statut CI, label PR, commentaire ou réaction.

## 9. Outils envisagés

| Famille | Rôle | N'établit pas seule |
|---|---|---|
| Tests unitaires/intégration/propriétés/fuzz/sécurité | Comportement empirique et contre-exemples | Correction universelle |
| TLA+ / TLC | Transitions, concurrence, invariants, temporalité dans une configuration | Conformité de l'implémentation |
| Alloy | Relations et contre-exemples bornés | Théorème non borné |
| Lean / assistant de preuve | Théorèmes, logique critique, raffinement formalisé | Fidélité normative ou exécutable non vérifié |
| OPA / Cedar | Décision exécutable de politique | Justesse normative ou impossibilité de contournement |
| Signatures/attestations/transparence | Intégrité, origine, historique sous hypothèses | Vérité, pertinence ou autorité |

TLA+ a servi au premier modèle car la cible initiale est un système de transitions. Lean a été envisagé pour la logique critique, pas choisi comme dépendance. Alloy pour les contraintes relationnelles et contre-exemples bornés. OPA/Cedar sont des moteurs de politique, pas des prouveurs. Aucun ne remplace les autres ; aucune pile globale n'a été choisie.

## 10. Portée documentaire

Cette restitution développe les distinctions des spécifications 0002–0005 et de l'architecture 0008. Elle complète la mémoire 0009 ; elle ne modifie pas le statut proposé des contrats et ne prétend pas qu'une implémentation existe.


## Références

- [Registre GovCheck des références sur la gouvernance et l'assurance](../references/governance-and-assurance.fr.md) : arguments d'assurance GSN, Lamport/TLA+, provenance in-toto et limites du noyau de preuve de Lean.
- [Version anglaise](../references/governance-and-assurance.md).


## Références bibliographiques

Références externes utilisées dans ce document : [R-04](../references.fr.md#r-04), [R-05](../references.fr.md#r-05), [R-06](../references.fr.md#r-06), [R-20](../references.fr.md#r-20).
