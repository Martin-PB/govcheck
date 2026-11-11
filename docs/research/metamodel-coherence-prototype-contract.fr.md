# Contrat du prototype de cohérence du métamodèle — première tranche verticale

**Statut :** contrat d'ingénierie proposé ; ni métamodèle adopté ni développement Lean exécutable.  
**Date :** 2026-11-11.  
**Recherche parente :** [Vérification de la cohérence du métamodèle](metamodel-coherence-verification.fr.md).  
**Version anglaise :** [Metamodel coherence prototype contract](metamodel-coherence-prototype-contract.md).

## 1. Objectif et périmètre

Ce contrat transforme la première expérimentation recommandée en obligations réfutables. Il ne cherche pas à formaliser d'un seul coup l'intégralité de SACM, SEON/ReqON, OWL ou GovCheck. Il vérifie une frontière sémantique critique : **une correspondance d'interopérabilité ne doit pas renforcer le statut épistémique d'un élément probant du seul fait de sa traduction**.

Le prototype est volontairement réparti entre trois artefacts :

1. un petit noyau sémantique Lean définissant les types d'éléments probants, les enregistrements, les contrats de correspondance et les dérivations admissibles ;
2. des fixtures représentant des éléments d'assurance de type SACM et des enregistrements GovCheck, avec identité/révision de la source et provenance explicites ;
3. une abstraction de cycle de vie TLA+ vérifiant quand les éléments probants et rapports de preuve restent applicables après un changement de source, de correspondance, d'hypothèse ou d'autorité.

CSLib est une source candidate de définitions et lemmes réutilisables, uniquement après examen de la pertinence de chaque import. Le prototype doit compiler et prouver son propre noyau sans dépendre de code de traduction CSLib non audité. Une preuve Lean vérifiée par le noyau est la cible des obligations sémantiques statiques ; CSLib n'est pas lui-même le noyau de confiance et ne fournit pas l'ontologie GovCheck.

## 2. Vocabulaire sémantique minimal

Le premier modèle Lean devrait définir au minimum :

- `EvidenceKind` : `Testimony`, `ModelChecking`, `ProgramVerification`, `TheoremProof`, `Inspection`, `Observation` et `Other`. Ce sont des classes distinctes, pas les éléments d'un classement total.
- `EvidenceStatus` : `Passed`, `Failed`, `Inconclusive`, `Unknown`, `Unsupported`, `NotRun` et `Stale`. Le statut n'est pas la classe de méthode.
- `ArtifactRef` : identité stable de l'artefact, révision/empreinte exacte, format natif et profil sémantique déclaré.
- `EvidenceRecord` : sujet, affirmation, classe de méthode, statut, hypothèses, portée, provenance, identité de l'outil/vérificateur, bornes le cas échéant et dépendances d'invalidation.
- `MappingContract` : identités et révisions des modèles source/cible, direction, classe de couverture, hypothèses, constructions prises en charge, pertes explicites, identité de transformation et obligations de préservation déclarées.
- `KernelCheckedDerivation` : dérivation vérifiée par le noyau de preuve déclaré, avec prémisses et conclusion exactes. Ce n'est ni un rapport importé ordinaire ni une chaîne de caractères `proof=true`.

La couverture d'une correspondance doit prendre l'une des valeurs suivantes : `Equivalent`, `SoundDirectional`, `Partial`, `Approximate`, `TraceabilityOnly` ou `Unsupported`. Ces valeurs ne sont pas interchangeables et ne doivent pas être réduites à un booléen.

## 3. Premières obligations de preuve

Le premier développement Lean devrait viser les énoncés suivants. Les noms sont des identifiants de proposition stables, pas des identifiants de règles normatives adoptées.

### VC-EPI-01 — La traduction ne promeut pas le statut épistémique

Une opération de transport/correspondance qui ne fait que réexprimer un enregistrement source préserve son `EvidenceKind`. En particulier, un rapport de test reste un témoignage et un rapport de model checking fini reste un élément probant de model checking.

Un enregistrement cible de type preuve de théorème n'est admissible que si :
- la source est déjà un enregistrement de preuve de théorème et le contrat de correspondance prouve la préservation de son identité de preuve et de ses dépendances ; ou
- une `KernelCheckedDerivation` distincte est fournie, vérifiée sur les prémisses, hypothèses, conclusion et identité du noyau exacts.

La preuve ne doit pas reposer sur un ordre tel que « la preuve de théorème est toujours supérieure au model checking » : ces classes répondent à des questions épistémiques différentes et ne constituent pas une échelle unique.

### VC-EPI-02 — Le statut ne se déduit pas de la classe de méthode

Aucun constructeur ne doit déduire `Passed` de `TheoremProof`, `ModelChecking` de `Passed`, ni `Passed` d'un parsing réussi. La méthode, le statut du résultat et la décision d'acceptation restent des champs séparés. Un théorème peut être faux, une obligation de preuve non démontrée et un vérificateur retourner unknown/error.

### VC-MAP-01 — Préservation de la provenance

Pour toute correspondance prise en charge, l'identité source, la révision/empreinte exacte, l'identifiant natif source, l'identité/version de transformation et la chaîne de provenance sont préservés ou un enregistrement de perte explicite est émis. Un champ de provenance absent ne doit pas être synthétisé silencieusement.

### VC-MAP-02 — Préservation de la portée et des hypothèses

Une affirmation/un élément probant traduit ne peut pas élargir la portée de son sujet, sa validité temporelle, son environnement, ses hypothèses ou ses conditions d'applicabilité. Une correspondance peut restreindre la portée, mais doit déclarer cette restriction. Toute traduction de portée non résolue produit `Unknown` ou `Unsupported`, jamais une réussite implicite.

### VC-MAP-03 — Composition

Si les correspondances A→B et B→C satisfont chacune une classe de préservation déclarée, la correspondance composée A→C ne peut revendiquer que la classe de préservation la plus forte justifiée par une loi de composition prouvée et des hypothèses compatibles. Elle ne peut hériter de `Equivalent` au seul motif que les deux correspondances existent.

### VC-MAP-04 — Aucune perte silencieuse

Toute construction source est classée comme traduite, préservée nativement, explicitement non prise en charge ou explicitement transformée avec déclaration de perte/d'approximation. Les tests aller-retour sont nécessaires mais ne prouvent pas à eux seuls l'équivalence sémantique.

### VC-AUTH-01 — L'autorité n'est pas amplifiée

La correspondance d'une décision, approbation ou délégation ne peut augmenter l'autorité du principal, son domaine, la portée de la cible, ses privilèges, son intervalle d'effet ou sa validité. Toute traduction d'autorité non résolue bloque la transition dépendante.

## 4. Fixtures adversariales

Le premier corpus doit contenir au minimum :

| Fixture | Résultat attendu | Obligation |
|---|---|---|
| Rapport de test unitaire traduit dans un dossier d'assurance | Reste `Testimony`, jamais une preuve de théorème | VC-EPI-01 |
| Rapport d'invariant TLC traduit dans un dossier d'assurance | Reste `ModelChecking`, bornes/configuration conservées | VC-EPI-01 |
| Preuve de théorème avec axiome non enregistré ou objectif admis | Rejet ou limitation explicite du socle de confiance | VC-EPI-01 / VC-EPI-02 |
| Correspondance supprimant la révision source | Échec ou perte explicite, jamais réussite silencieuse | VC-MAP-01 |
| Correspondance élargissant une affirmation d'un composant à tout le dépôt | Échec de l'obligation | VC-MAP-02 |
| Deux correspondances valides isolément avec hypothèses incompatibles | Composition bloquée ou affaiblie | VC-MAP-03 |
| Métaclasse source inconnue omise à l'export | Rapport explicite `Unsupported`/perte | VC-MAP-04 |
| Délégation traduite avec portée plus large ou expiration plus tardive | Échec de l'obligation | VC-AUTH-01 |

Des fixtures positives sont également nécessaires : correspondance sans perte d'un élément probant pris en charge, transfert valide d'une preuve de théorème avec dépendances conservées, et correspondance restreignant la portée sans danger.

## 5. Obligations temporelles : conserver à TLA+ son rôle propre

TLA+ doit modéliser le cycle de vie du paquet de preuve/correspondance, et non remplacer les preuves sémantiques statiques. Les variables d'état candidates comprennent la révision source, la révision de correspondance, la révision des hypothèses, celle du paquet de preuve, le statut, l'intervalle de validité, la révision d'autorité et l'ensemble d'invalidation.

Propriétés temporelles requises :

- Un changement d'une dépendance déclarée rend l'ancien résultat périmé pour les nouvelles décisions d'acceptation jusqu'à réévaluation.
- Les éléments probants historiques restent append-only et consultables.
- Une preuve périmée peut être conservée comme historique mais ne peut autoriser une transition actuelle.
- Une autorité révoquée ou expirée ne peut autoriser une nouvelle adoption de correspondance.
- `Unknown`, `Unsupported` et `Inconclusive` restent bloquants selon la politique d'échec en monde fermé ; aucun résultat manquant ne devient une réussite par défaut.
- Tout nouveau résultat de preuve est lié aux révisions exactes de la source, de la correspondance, des hypothèses et du vérificateur contrôlées.

Les résultats TLC restent des éléments probants de model checking borné pour l'abstraction finie déclarée. La préservation sémantique générale relève des preuves Lean ; la conformité de l'implémentation exige un argument distinct de raffinement/conformité.

## 6. Protocole d'évaluation de CSLib

Ne pas décider que « CSLib est obligatoire » en fonction de sa réputation ou de son ampleur. Pour chaque import candidat :

1. identifier le commit CSLib exact et la chaîne d'outils Lean ;
2. examiner la définition et toutes ses dépendances transitives ;
3. identifier axiomes, `sorry`, `admit`, `unsafe`, frontières natives/oracles et code de traduction généré ;
4. décider si la définition correspond à la sémantique voulue par GovCheck, pas seulement à son nom ;
5. prouver un petit théorème de liaison entre la définition importée et le contrat GovCheck ;
6. enregistrer le socle de confiance et la commande de compilation reproductible.



### Contrainte actuelle de compatibilité CSLib/chaîne d'outils

Le commit `main` de CSLib examiné est `f8acdb37c713b0124ad36b863f50c200a5f1cdba`, qui épingle Lean 4.36.0-rc2 et le commit Mathlib `887bb849a9f64e1c66499fd5ff8523c864e78941`. Ce prototype épingle Lean 4.19.0. Une dépendance directe ne peut donc pas être ajoutée sans changement de chaîne d'outils. La prochaine expérimentation doit soit identifier une révision CSLib compatible avec Lean 4.19, soit isoler un profil CSLib avec sa propre chaîne d'outils épinglée. Ne pas mettre à niveau silencieusement le noyau déjà vérifié.

Si CSLib fournit une formalisation saine et réutilisable d'un concept sémantique requis, le réemploi doit être préféré à une duplication indépendante. Dans le cas contraire, définir le plus petit concept spécifique à GovCheck et prouver sa relation au modèle source pertinent. Ce n'est pas une règle d'optionalité générale : **l'obligation d'assurance est impérative pour les correspondances critiques ; le choix de la bibliothèque repose sur les éléments établis**.

## 7. Critère d'achèvement du prototype

La première tranche n'est achevée que lorsque :

- le projet Lean compile avec une chaîne d'outils épinglée ;
- les théorèmes positifs sont vérifiés par le noyau, sans axiomes/admissions non audités ;
- chaque fixture adversariale est rejetée pour la raison attendue ;
- au moins une correspondance invalide produit un contre-exemple concret ou un échec d'obligation ;
- les révisions source, hypothèses, provenance et dépendances de preuve sont préservées ;
- un modèle TLA+ borné démontre le rejet d'une preuve périmée après changement d'une dépendance ;
- le paquet de preuve enregistre commits, commandes, sorties, limites et socle de confiance exacts ;
- la distinction entre preuve, model checking, validation, témoignage de test et acceptation est exploitable par machine.

Aucune implémentation ne doit prétendre que ce critère est satisfait tant que la compilation Lean, l'exécuteur de fixtures et l'exécution TLC n'ont pas réellement été lancés et leurs sorties enregistrées.

## 8. Décision toujours réservée

Ce contrat est une expérimentation proposée. Il ne sélectionne pas Lean/CSLib comme dépendance universelle des dépôts adoptants, n'adopte pas une ontologie GovCheck, ne remplace pas la sémantique native de SACM et n'autorise aucune dégradation des obligations de preuve. L'autorité devra décider du profil de preuve obligatoire après examen du coût réel, de la couverture et du socle de confiance du prototype.


## Résultats effectifs du prototype

Le noyau Lean 4.19.0 a réussi sa compilation et son audit des axiomes dans [l'exécution 43049890363 de la PR #108](https://github.com/Martin-PB/govcheck/actions/runs/43049890363). Une expérimentation LTS CSLib distincte sous Lean 4.36.0-rc2 a réussi la compilation et l'audit des axiomes dans [l'exécution 43051029627 de la PR #109](https://github.com/Martin-PB/govcheck/actions/runs/43051029627). L'expérimentation CSLib prouve la préservation de la classe de méthode et du type épistémique sur les transitions individuelles et les exécutions LTS finies. Elle reste un modèle abstrait de cycle de vie, pas une preuve de correspondance avec une ontologie externe. Les deux PR restent non fusionnées ; la PR #109 est empilée sur la PR #108.