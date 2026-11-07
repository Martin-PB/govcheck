# 0023 — Décision d'amorçage de l'autorité de gouvernance

**Statut :** décision consignée à partir de l'instruction explicite du propriétaire du projet le 07-11-2026 ; proposée à l'adoption par cette pull request. Elle ne prétend pas qu'un registre d'autorité ou un moteur d'application est implémenté.  
**Périmètre :** autorité canonique de gouvernance de GovCheck.

## 1. Décision

Dans le régime de gouvernance actuel, un seul principal détient l'autorité d'adopter, modifier, suspendre et remplacer le modèle canonique de gouvernance et ses politiques normatives.

Ce principal est le propriétaire du projet, identifié dans les enregistrements de gouvernance du dépôt par l'identifiant stable `Martin-PB`. Il s'agit d'une décision explicite du projet, et non d'une déduction fondée sur la propriété du dépôt GitHub, les privilèges d'administration, l'auteur d'un commit, l'état de la CI ou les droits de fusion d'une pull request.

Aucun comité, groupe de mainteneurs, réviseur ou acteur délégué ne partage cette autorité racine dans le régime actuel.

## 2. Auto-amendement

L'autorité unique peut elle-même modifier le modèle d'autorité, notamment pour :

- changer l'identité du détenteur de l'autorité unique ;
- introduire ou supprimer des autorités déléguées ;
- modifier le périmètre ou les pouvoirs permis aux délégataires ;
- introduire ou supprimer une approbation collective ou multipartite ;
- modifier les règles de succession, de suspension ou de révocation.

Un tel changement doit être une décision de gouvernance explicite, attribuable et versionnée. Il prend effet prospectivement à partir de son point d'entrée en vigueur enregistré. Il ne doit pas réécrire silencieusement le fondement d'autorité des décisions antérieures ni valider rétroactivement des décisions qui n'étaient pas autorisées au moment où elles ont été prises.

Une modification du modèle d'autorité n'est pas valide du seul fait qu'elle apparaît dans une pull request fusionnée. L'enregistrement de décision doit identifier le principal approbateur et la révision exacte de gouvernance antérieure en vertu de laquelle ce principal a agi.

## 3. Conséquences opérationnelles

Jusqu'à une décision explicite ultérieure modifiant ce régime :

1. Seul le principal `Martin-PB` peut adopter ou modifier une politique canonique de gouvernance.
2. Les collaborateurs du dépôt peuvent proposer des changements et effectuer des revues techniques, mais ne peuvent pas autoriser l'adoption normative.
3. L'approbation d'une pull request, le droit de fusion, l'administration du dépôt, une CI verte et la propriété de code ne remplacent pas la décision de gouvernance.
4. La délégation est absente par défaut. Aucun délégataire n'a d'autorité sans décision versionnée lui accordant explicitement un ensemble borné de périmètres et d'actions.
5. Si l'enregistrement d'autorité est absent, incohérent, révoqué ou impossible à résoudre, l'autorisation est évaluée à `unknown`/bloquée, jamais implicitement approuvée.
6. Une revue technique peut être demandée comme mesure d'assurance, mais elle ne transfère ni ne partage l'autorité normative finale.

## 4. Séparation des responsabilités

Le régime actuel à autorité unique ne peut pas fournir une autorisation d'adoption par deux personnes : le même principal peut proposer et autoriser une modification de gouvernance.

Il s'agit d'un choix explicite de gouvernance, et non d'une propriété à présenter à tort comme une approbation indépendante. Les contrôles doivent donc distinguer :

- **autorisation normative :** décision de l'autorité unique ;
- **évaluation technique :** validation automatisée et revue indépendante facultative ;
- **exécution :** publication ou application de la révision déjà autorisée.

Lorsque l'autorité unique est également le proposant, le système doit enregistrer cette auto-autorisation conformément au régime. Il ne doit pas déclarer satisfaite une approbation par une personne distincte ou un invariant d'autorisation indépendante.

## 5. Règles d'intégrité et de temporalité

Le futur registre d'autorité et son évaluateur devront imposer :

- des identifiants stables de principaux, et non de simples noms d'affichage ;
- des révisions immuables des décisions et politiques ;
- des points d'entrée en vigueur ou positions de séquence explicites et des liens de remplacement ;
- aucune attribution rétroactive d'autorité ;
- aucune délégation implicite ni élévation de privilèges ;
- un blocage par défaut en cas d'autorité inconnue, absente ou contradictoire ;
- une piste d'audit complète des changements d'autorité.

Une délégation future ne pourra accorder que les actions et périmètres explicitement énumérés ; elle devra avoir une période de validité et pourra être révoquée. Elle ne pourra dépasser l'autorité propre du délégant ni survivre à sa validité.

## 6. Limite de récupération et de compromission

Une autorité racine unique crée un point unique de compromission et de défaillance de disponibilité. La présente décision accepte ce compromis pour le régime initial ; elle ne résout pas la compromission du compte, la perte des clés, l'incapacité ou la succession.

Ces sujets devront faire l'objet d'un amendement explicite et approuvé séparément (par exemple un mécanisme de récupération ou une transition vers une autorité multipartite). Aucun principal de récupération n'est implicitement déduit de l'administration du dépôt ou des contrôles de l'hébergeur.

## 7. Travaux de formalisation

Le modèle de cycle de vie de gouvernance et les tests de conformité devront représenter :

- un principal racine configuré ;
- l'adoption et la modification par ce seul principal ;
- une transition explicite d'auto-amendement du régime d'autorité ;
- un effet prospectif et la préservation de la validité des décisions antérieures ;
- l'absence de délégataires sauf octroi explicite ;
- le blocage par défaut en cas d'autorité inconnue ou révoquée ;
- l'enregistrement explicite du fait que proposant et autorité approbatrice peuvent être le même principal dans ce régime.

Cette décision établit la règle de gouvernance à modéliser. Elle ne prétend pas que ces contrôles sont déjà implémentés ou vérifiés.

## 8. Source

Instruction explicite du propriétaire du projet dans la discussion de gouvernance GovCheck, le 07-11-2026 : « Pour l'instant, moi seul et je pourrai donc moi-même faire évoluer cette autorité. »

