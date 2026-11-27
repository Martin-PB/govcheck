# Spécification 0008 — Attestations d'assurance interopérables

**Statut :** profil proposé pour l'issue issue #44 ; il ne constitue pas une adoption normative et ne prétend pas que le runtime actuel vérifie les signatures ou les identités des signataires. **English:** [0008](0008-interoperable-assurance-attestations.md).

## 1. Objet

Définir une représentation portable des éléments d'évaluation GovCheck, transportable et authentifiable au moyen du framework d'attestation in-toto et de DSSE. Le profil lie une évaluation à un sujet candidat immuable, aux identités VCS natives, à la révision exacte de gouvernance, à l'identité du vérificateur, aux entrées, aux méthodes d'assurance, aux limites et au résultat.

Le profil ne transforme pas une attestation en preuve. Il préserve la distinction entre tests (observations/éléments probants), model checking (éléments probants relatifs à un modèle borné), proof checking (preuve acceptée par un noyau donné), inspection/revue et décision d'une autorité.

## 2. Correspondance interopérable

- **in-toto Statement v1** constitue l'énoncé sémantique externe : `_type`, digest du `subject` immuable, `predicateType` et `predicate` typé.
- Le **prédicat GovCheck Assurance Evaluation v1** porte les sémantiques d'évaluation et d'assurance propres à GovCheck. URI : `urn:govcheck:attestation:assurance-evaluation:v1`.
- **DSSE v1** est l'enveloppe authentifiée recommandée. Le type de payload est `application/vnd.in-toto+json` ; les signatures authentifient les octets exacts du payload et son type au moyen de DSSE PAE.
- Le digest du sujet in-toto identifie l'instantané du contenu. Les identités VCS natives Git/Pijul restent des champs supplémentaires ; les identifiants de commit Git et de changement Pijul ne sont pas interchangeables avec un digest de contenu.
- SLSA Verification Summary Attestation (VSA) n'est pas le prédicat générique de GovCheck. Son `verificationResult` est PASSED/FAILED et ses niveaux décrivent des pistes SLSA. Elle peut être émise séparément lorsqu'un niveau SLSA a réellement été évalué, mais ne doit pas encoder UNKNOWN, CONFLICT, le statut d'une preuve ou une décision d'autorité GovCheck.

## 3. Contrat du prédicat

Le schéma JSON complet est `../schemas/govcheck-assurance-evaluation-v1.schema.json`.

Groupes obligatoires :

| Groupe | Sémantique requise |
|---|---|
| `evaluation` | Identifiant stable, date d'évaluation, résultat global `pass`, `fail`, `unknown` ou `conflict`, et résultats par règle. |
| `repository` | URI stable du dépôt et type de VCS. |
| `candidate` | Révision native et identité du contenu/arbre ; pour Git, identifiants commit et tree ; pour Pijul, identités natives du jeu de changements et du canal. |
| `base` | Identité native exacte de la base utilisée pour l'évaluation. |
| `governance` | Périmètre de gouvernance, révision immuable et digest, avec identité/digest du profil facultatifs. |
| `verifier` | URI du vérificateur, version, digest du build/exécutable et digest de configuration. |
| `methods` | Zéro ou plusieurs activités d'assurance typées, avec résultats, portée, entrées/éléments probants, outils, hypothèses et limites. |
| `independentReview` | État explicite : `unavailable`, `not_performed`, `attested` ou `unknown`. Une revue attestée référence un énoncé de revue distinct par digest. |

Les types de méthode sont `test`, `model_check`, `proof_check`, `inspection`, `analysis` et `other`. Leur résultat est typé séparément. Le résultat d'un test n'est pas une preuve ; un résultat TLC est un élément probant relatif au modèle/configuration/bornes exacts ; un résultat de proof checking nomme le noyau et l'identité du théorème et n'établit pas à lui seul un raffinement de l'implémentation.

Le prédicat enregistre des faits et des éléments probants. Il ne décide pas si un résultat est acceptable au regard d'une politique.

## 4. Séparation des décisions et du risque

Une décision d'autorité est un acte de gouvernance distinct, et non un résultat d'évaluation. L'acceptation du risque est également distincte : elle ne réécrit pas `fail`, `unknown` ou `conflict` en `pass`, et doit conserver l'autorité, la justification, la portée, les affirmations concernées, le risque résiduel, les conditions et l'expiration. Ce prédicat peut référencer des décisions/risques distincts par digest immuable, mais ne doit pas les fabriquer à partir du rapport d'évaluation.

Le régime d'autorité actuel dispose d'un seul principal racine. Une décision de cette autorité unique n'est pas une revue par une seconde personne. Lorsqu'aucun second contributeur n'est disponible, `independentReview.status` vaut `unavailable` ; l'évaluateur ne doit ni inférer qu'une revue a eu lieu ni traiter cette absence comme un succès.

## 5. Liaison du sujet et stockage détaché

L'attestation doit être stockée hors de l'arbre candidat qu'elle décrit (par exemple comme artefact CI, artefact attaché à la forge ou objet du journal). Elle ne doit pas être commise dans le même candidat dont elle prétend attester l'identité finale.

Le digest du sujet in-toto identifie un instantané de contenu déterministe. Le prédicat lie en outre :
- l'identité du dépôt ;
- le type de VCS et la révision native du candidat ;
- l'identité de l'arbre/contenu candidat ;
- la révision et l'identité exactes de la base ;
- la révision et le digest de gouvernance ;
- les digests du build et de la configuration du vérificateur.

Tout changement de ces liaisons invalide la réutilisation. Un nouveau candidat, une nouvelle base/politique/vérificateur/entrée exigent une nouvelle évaluation et un nouvel énoncé. L'évaluation reste un élément probant historique et n'est pas réécrite.

## 6. Authentification et confiance

DSSE signe le type de payload et les octets exacts du payload via PAE. Le champ `keyid` est un indice de recherche non authentifié, pas une déclaration d'identité. Les consommateurs doivent vérifier les signatures selon une politique de confiance explicite et associer les clés/certificats acceptés à des identités de principaux stables et à des rôles autorisés.

Une signature DSSE valide authentifie le signataire de l'énoncé ; elle ne fait pas automatiquement de ce signataire un reviewer indépendant, un vérificateur, une autorité de gouvernance ou un approbateur. Les consommateurs doivent contrôler la paire signataire/vérificateur et le rôle selon la politique de confiance applicable. Un champ libre `reviewer` ne suffit jamais.

La première implémentation Python construit et valide le payload Statement in-toto et la structure de l'enveloppe DSSE, et expose les octets DSSE PAE pour une signature externe. Elle **n'implémente pas** la signature cryptographique, la découverte de certificats/clés, la gestion des racines de confiance ou la vérification des signatures. Tant qu'un adaptateur de vérification fiable n'est pas configuré, une enveloppe analysée est structurellement valide mais non authentifiée et ne peut satisfaire une barrière d'attestation. Le runtime du vérificateur et sa politique de confiance appartiennent au TCB.

## 7. Relation avec SLSA VSA

SLSA VSA convient uniquement lorsque GovCheck résume une vérification SLSA réelle d'un artefact selon une piste/un niveau SLSA déclaré. Son vocabulaire PASSED/FAILED ne permet pas une correspondance sans perte avec les quatre résultats de GovCheck et ne représente ni l'autorité, ni les décisions, ni l'acceptation du risque, ni toutes les distinctions entre méthodes d'assurance. Une VSA distincte peut être référencée comme élément probant d'entrée ; GovCheck ne doit pas requalifier son résultat générique en niveau SLSA.

## 8. Conformité et cas négatifs

Un producteur/consommateur conforme doit rejeter ou laisser non authentifiés :
- les digests de sujet in-toto absents ou mal formés ;
- un type Statement ou prédicat non pris en charge ;
- les liaisons candidat, base, gouvernance ou vérificateur manquantes ;
- les codes de résultat d'évaluation/méthode inconnus ;
- un état de revue indépendante `attested` sans référence détachée à l'énoncé de revue ;
- une attestation située dans l'arbre candidat et présentée comme preuve de la révision finale de ce même candidat ;
- une enveloppe sans payload/type/signatures ou avec un base64 invalide ;
- une enveloppe DSSE dont la signature n'a pas été vérifiée par un vérificateur explicitement approuvé ;
- une identité de signataire non associée au rôle requis ;
- des liaisons ou éléments probants obsolètes.

Une signature valide sur un énoncé structurellement valide ne prouve pas que l'évaluation était correcte. Elle authentifie l'auteur de ces octets selon le modèle de confiance. Les méthodes, éléments probants et limites de l'évaluation restent évaluables séparément.

## 9. Limites d'implémentation

La première implémentation fournit un constructeur/validateur standard-library-only du prédicat GovCheck, une sérialisation JSON déterministe, la construction DSSE PAE et des contrôles structurels d'enveloppe. Les opérations cryptographiques sont déléguées délibérément plutôt qu'approximées. Les fixtures utilisent des signatures synthétiques uniquement pour tester la sérialisation ; elles ne prétendent pas démontrer une validité cryptographique.

Le contrôle actuel `independent-review` ne doit pas traiter un enregistrement JSON de l'arbre candidat ou une chaîne libre de reviewer comme une revue authentifiée. Tant qu'un vérificateur d'attestations détachées et authentifiées n'est pas intégré, la revue indépendante reste `unknown` ou `unavailable`.

## 10. Références et documents liés

- [R-227 — DSSE](../references.fr.md#r-227)
- [R-228 — Framework d'attestation in-toto v1](../references.fr.md#r-228)
- [R-229 — SLSA Verification Summary Attestation](../references.fr.md#r-229)
- [R-06 — Projet in-toto](../references.fr.md#r-06) et [R-07 — SLSA](../references.fr.md#r-07)
- [Spécification 0005 — Assurance, affirmations et éléments probants](0005-assurance-model.fr.md)
- [Spécification 0007 — Journal canonique de gouvernance](0007-canonical-governance-journal-protocol.fr.md)
- [Architecture 0023 — Autorité de gouvernance bootstrap](../architecture/0023-bootstrap-governance-authority.fr.md)
- issue #44, issue #60, issue #131

**Cette spécification est proposée. Elle n'adopte aucune racine de confiance, politique de signataire, algorithme cryptographique ou règle obligatoire d'acceptation.**
