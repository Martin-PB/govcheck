# Triage sur sources de la critique externe #129

**Statut :** inspection préliminaire des sources ; pas un rapport d'exécution reproduite indépendamment. **Date :** 2026-11-13. **Élément de travail :** [#130](https://github.com/Martin-PB/govcheck/issues/130). **Critique source :** [#129](https://github.com/Martin-PB/govcheck/issues/129).

## 1. Identité de révision et limites de méthode

La comparaison GitHub de `main` avec la branche de travail au moment du triage indiquait que `main` était au commit `24760fbfd747fc64f6261b53182f4ed8fdbd4467`, identique à celui identifié par la critique externe. Les constats ci-dessous concernent donc la même révision source, pas une correction ultérieure de main.

Cette passe a inspecté les fichiers source au moyen de l'intégration au dépôt. Elle n'a **pas** exécuté les tests Python, TLC, les builds Lean, les audits d'axiomes ni le profil de compatibilité CSLib. Il s'agit uniquement d'un triage sur sources. Aucun workflow GitHub Actions n'a été déclenché.

## 2. Constats 6.1–6.7

| Constat de la critique | Qualification sur sources | Éléments actuels et nuances |
|---|---|---|
| 6.1 — absence de modèle canonique/schéma exécutable | **Confirmé** | La Specification 0002 indique explicitement qu'il s'agit d'une architecture proposée/d'un contrat de conception et qu'aucun schéma ni évaluateur n'est implémenté. Markdown reste la représentation pratique du dépôt. |
| 6.2 — circularité d'amorçage/adoption | **Partiellement confirmé ; précisé par une spécification ultérieure** | La Specification 0007 définit désormais un protocole de journal logique indépendant des technologies, des exigences de trust anchor genesis, compare-and-append, commit durable et reprise. Elle reste explicitement proposée et non implémentée. L'affirmation de la critique selon laquelle aucun protocole de journal n'est spécifié est donc incomplète ; le chemin d'adoption/amorçage demeure un problème d'implémentation et d'autorité non résolu. |
| 6.3 — séparation des tâches | **Confirmé comme limite de gouvernance déclarée, pas nécessairement comme incohérence accidentelle** | L'Architecture 0023 indique explicitement que le principal unique actuel peut proposer et autoriser un changement de gouvernance et que le système ne doit pas prétendre à une autorisation à deux personnes. Elle distingue autorisation normative, évaluation technique/revue indépendante facultative et exécution. Le relecteur distinct du modèle d'assurance relève d'une propriété d'évaluation technique distincte, pas de la preuve d'une seconde autorité normative. Le risque résiduel et l'évolution prospective vers plusieurs principaux restent ouverts dans #60/#71. |
| 6.4 — attestation de revue indépendante | **Défaut structurel confirmé par inspection ; exécution encore requise** | `rule_independent_review` lit `docs/attestations/*.json`, exige que `candidate_rev` égale la révision candidate complète et compare une chaîne de caractères de relecteur à la chaîne auteur Git. Le workflow invoque le vérificateur sur `HEAD`. Un fichier commité dans l'arbre candidat ne peut normalement pas contenir le SHA du commit dont l'arbre contient ce fichier sans problème d'autoréférence. Le champ relecteur n'est pas authentifié par ce code. Les tests unitaires inspectés injectent directement un SHA candidat et un auteur synthétiques dans l'évaluateur, puis créent une attestation contenant cette valeur fournie ; ils n'exercent pas un commit réel dont l'arbre contient sa propre attestation. Il faut un contrat d'attestation externe/latéral et une identité authentifiée. |
| 6.5 — échec fermé neutralisé dans la CI | **Confirmé pour le chemin d'enforcement CI actuel** | Le workflow est explicitement nommé report-only ; l'étape GovCheck utilise `continue-on-error: true` et se termine par `|| true`. Les tests unitaires sont une étape bloquante distincte. Ainsi, la sémantique fail-closed de l'évaluateur ne fait pas actuellement du workflow CI une barrière d'acceptation. |
| 6.6 — mapping partiel à couverture vide possible | **Confirmé** | `SemanticBridge.partialMapping` accepte un prédicat de domaine et ne prouve la cible que pour les propositions sources appartenant à ce domaine. Il n'exige pas que le domaine soit habité. Un domaine vide satisfait donc le constructeur sans établir de couverture non vide. Ce n'est pas une preuve de Faux à partir de Vrai ; c'est l'absence d'une garantie de couverture/non-vacuité. |
| 6.7 — journal nécessitant une infrastructure distincte | **Conclusion excessive ; préoccupation sémantique valide, conclusion physique non établie** | La Specification 0007 sépare délibérément l'ordre normatif logique de l'ordre natif du VCS, mais n'impose pas une base de données ou un service physiquement séparé. Elle laisse ouverts le moteur de stockage et les choix de déploiement. Tout support doit néanmoins démontrer les propriétés requises de compare-and-append atomique, commit durable, reprise et idempotence. Une séparation sémantique n'implique pas une séparation physique. |

## 3. Limites formelles et d'implémentation plus profondes

### 3.1 Sûreté et vivacité conditionnelle

Le modèle de cycle de vie contient des invariants de sûreté relatifs à l'acceptation, à la péremption, aux éléments probants et à l'application. Sa condition `NoUnexpectedNonterminalDeadlock` ne garantit pas utilement qu'un candidat légitime atteint finalement `Applied` : le modèle peut conserver des chemins de rejet/retrait. Une propriété de progression pertinente exige des hypothèses explicites sur la disponibilité de l'autorité, la production des éléments probants, l'équité de l'ordonnancement, les dépendances et la possibilité de rejet. Une vivacité inconditionnelle vers l'acceptation serait dangereuse.

### 3.2 Des modèles séparés ne constituent pas une preuve de raffinement

La Specification 0007 qualifie elle-même les modèles TLA+ de tranches bornées séparées et précise qu'ils constituent des éléments de conception composables, pas un modèle intégré de l'implémentation. Aucune relation de raffinement de bout en bout entre modèles de cycle de vie/autorité/journal et vérificateur Python ou implémentation de production n'est établie par cette spécification.

### 3.3 Force des théorèmes Lean

Le code de mapping inspecté comprend des résultats de projection et un théorème dont le témoin est accompagné de l'égalité réflexive `derivation.proof = derivation.proof`. Ce théorème établit l'existence de l'objet dérivation transporté, pas une propriété sémantique supplémentaire du mapping source. Les obligations de preuve au niveau des types peuvent rester utiles, mais les noms et affirmations des théorèmes doivent correspondre à la proposition effectivement établie.

### 3.4 Périmètre exécutable

Les huit règles de `govcheck/check.py` couvrent présence de licence, fichiers de décision bilingues, paires du manifeste, intégrité des références, présence des sources, intégrité du bootstrap, fraîcheur des éléments probants TLA et attestation de revue indépendante. Elles n'implémentent ni cycle de vie canonique, ni registre d'autorité, ni protocole de journal, ni sémantique des décisions/risques, ni contrats d'assurance intermodèles. Cela confirme une lacune importante de conformité de l'implémentation ; cela ne signifie pas que la tranche existante est sans valeur.

## 4. Ce qu'il reste à reproduire

Les travaux suivants restent requis dans #130 :

- exécuter toute la suite de tests unitaires Python sur le commit exact et consigner commande, version de l'interpréteur et résultat ;
- exécuter SANY/TLC pour chaque modèle et configuration versionnés, en consignant digest exact de l'outil, version Java, nombres d'états, bornes, invariants et propriétés temporelles ;
- construire le paquet de cohérence Lean, exécuter son rapport d'axiomes et examiner/construire séparément `formal/cslib-compat` avec son propre toolchain Lean 4.36.0-rc2 (le profil Lean principal épingle 4.19.0) ;
- examiner toutes les configurations des modèles et filtres de chemins CI, et établir quels contrôles sont réellement requis à la frontière d'acceptation ;
- construire des contre-exemples minimaux pour le mapping à domaine vide et le problème d'identité/révision de l'attestation ;
- requalifier chaque constat après exécution : confirmé, réfuté, partiel, dépassé, non reproductible ou nécessitant un arbitrage d'autorité.

Le réseau/l'environnement d'exécution actuel n'a pas permis de cloner le dépôt pour une exécution locale. Les commandes ci-dessus n'ont pas été lancées dans cette passe. Aucun crédit Actions n'a été consommé.

## 5. Disposition

Ce triage précise la critique externe plutôt que de l'accepter en bloc. Les constats 6.1, 6.4, 6.5 et 6.6 sont étayés par l'inspection des sources ; 6.2 et 6.3 nécessitent les nuances indiquées ; la conclusion physique de 6.7 n'est pas soutenue par la Specification 0007. Les préoccupations plus profondes concernant sûreté/vivacité, composition des modèles et conformité de l'implémentation restent importantes.

Ce rapport n'a modifié aucune spécification, aucun modèle Lean/TLA+, aucune règle d'acceptation ni décision d'autorité. Les corrections d'implémentation restent conditionnées par la reproduction exacte et les travaux de conception suivis dans #130 et par les éléments existants applicables.
