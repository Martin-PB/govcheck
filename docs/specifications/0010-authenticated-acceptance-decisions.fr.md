# Spécification 0010 — Décisions d'acceptation authentifiées

**Statut :** contrat d'implémentation proposé pour l'issue #45 ; ne crée pas un nouveau régime d'autorité et ne prétend pas que la forge l'applique actuellement. **English:** [0010](0010-authenticated-acceptance-decisions.md).

## 1. Objet

Séparer le résultat d'une évaluation de la décision d'acceptation d'une autorité. Un rapport consigne les éléments probants et conserve son résultat `pass`, `fail`, `unknown` ou `conflict`. Une décision est un acte de gouvernance distinct et authentifié, lié à un candidat et à une évaluation exacts.

Un check CI vert, une évaluation signée ou un reçu de journal local ne constitue pas en soi une décision d'autorité.

## 2. Statement et prédicat

La décision est un Statement in-toto v1 avec le type de prédicat :

`urn:govcheck:attestation:acceptance-decision:v1`

Le schéma JSON strict est `../../govcheck/formal/schemas/acceptance-decision-v1.schema.json`. Le prédicat lie l'identifiant du dépôt, la révision/le digest du contenu candidat, la révision de base, la référence protégée, la révision de gouvernance, le scope, le digest exact du rapport d'évaluation, l'identifiant de décision, l'assertion de date et la justification.

Le signataire de la décision est authentifié par DSSE et associé au rôle requis `governance-authority` dans une politique de confiance épinglée par l'opérateur. Aucun champ libre de principal d'autorité n'est présent ; le principal provient du signataire vérifié.

## 3. Liaison du rapport d'évaluation

`evaluationDigest` est le SHA-256 des octets exacts du fichier de rapport d'évaluation fourni au gate. Le vérificateur doit analyser ces mêmes octets et comparer l'objet rapport analysé à l'objet évalué ; il ne doit pas accepter un objet rapport fourni séparément et différent de l'entrée du digest signé.

La décision lie également la révision candidate complète, le digest de contenu candidat, la révision de base, la référence, la révision de gouvernance et le scope. Toute discordance ou tout rapport obsolète est rejeté.

## 4. Sémantique de décision

- **`accept` :** autorisé uniquement si le résultat global du rapport lié est `pass`.
- **`reject` :** refuse l'acceptation quel que soit le résultat d'évaluation.
- **`accept_with_risk` :** acte d'autorité distinct et scoped pour un rapport dont le résultat n'est pas `pass`. Il exige un enregistrement de risque complet : identifiant, raison, scope, expiration, risque résiduel, claims affectés et digest de l'enregistrement d'autorisation.

L'acceptation du risque doit correspondre au scope candidat et ne doit pas être expirée au moment de la vérification. Elle ne réécrit pas le résultat `fail`, `unknown` ou `conflict` du rapport en `pass`. La décision reste un élément probant historique ; elle n'est ni un test, ni une preuve, ni une revue indépendante.

## 5. Échec et indétermination

Enveloppe, politique de confiance, rôle, association de signataire, octets du rapport ou bindings exacts manquants produisent `unknown` ou `fail`, jamais PASS. Signatures invalides, décisions de rejet, digest de rapport obsolète, candidat/base/ref/politique/scope discordants, enregistrements de risque incomplets ou expirés sont rejetés.

`decidedOn` est une assertion signée, pas une preuve d'horodatage fiable. La validité des clés est vérifiée à l'heure courante du vérificateur ; aucune preuve historique de l'heure de signature n'est fournie.

## 6. Frontière d'enforcement

Ce prédicat est un contrat portable de décision d'autorité. L'adaptateur Git pre-receive local exige toujours un exécutable gate installé séparément et épinglé par digest ; son protocole de sortie v0 est une frontière d'adaptation. L'audit en lecture seule du ruleset GitHub n'applique pas lui-même cette décision.

Une frontière d'acceptation complète exige en plus :
- un exécutable gate de confiance et sa fermeture runtime installés hors de l'arbre candidat ;
- un ruleset de forge exigeant des PR et des checks exacts issus d'une source de confiance ;
- une réévaluation du candidat/base réel de merge ;
- un test réel de mise à jour d'une référence protégée démontrant le rejet de FAIL/UNKNOWN/preuve obsolète ;
- la documentation des limites de bypass administrateur et des transports alternatifs.

Cette spécification ne modifie aucun ruleset de dépôt.

## Références

- [R-06 — in-toto](../references.fr.md#r-06)
- [R-232 — OpenSSL pkeyutl](../references.fr.md#r-232)
- [R-233 — RFC 8032 / EdDSA](../references.fr.md#r-233)
