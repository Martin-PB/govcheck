# 0039 — Source de check GitHub requis pour les reçus d'acceptation authentifiés

**Statut :** tranche d'implémentation dans [#45](https://github.com/Martin-PB/govcheck/issues/45) ; la configuration de confiance et l'adoption du ruleset restent à effectuer.

## 1. Décision

Fournir une source de check GitHub Actions propre au dépôt, nommée **`GovCheck authenticated acceptance receipt`**. Le workflow :

- Crée un check en attente sur le SHA exact de la tête de PR à l'ouverture, synchronisation, réouverture, modification de base ou passage en ready-for-review.
- N'accepte un reçu de journal signé que via un commentaire de PR contenant la commande seule `/govcheck-receipt` et une unique enveloppe JSON DSSE clôturée.
- Exécute le vérificateur depuis `main` de confiance ; il checkout le candidat dans un répertoire séparé avec les credentials désactivés et n'exécute jamais le code candidat.
- Vérifie la signature DSSE avec une trust-policy épinglée et le rôle de signataire requis, puis lie l'événement de gate signé au SHA courant de tête, au SHA courant de base, à la branche cible, au digest de contenu candidat, à l'URI/ID du dépôt, au scope/révision/digest de gouvernance et au digest de politique d'acceptation.
- Exige une décision d'autorité authentifiée avec résultat `pass` ; les résultats avec risque accepté et les tentatives non vérifiées ne satisfont pas ce check.
- Relit la PR avant de terminer le check et échoue si la tête, la base ou l'état a changé pendant la vérification.

Cette source n'est un signal d'enforcement que si l'administrateur du dépôt sélectionne le nom exact du check et la source GitHub Actions de confiance dans le ruleset. GovCheck ne modifie pas le ruleset. La prévention des push directs, les restrictions de bypass et l'option « exiger une branche à jour » restent sous contrôle de l'administrateur. Voir [R-225](../references.md#r-225) et [R-227](../references.md#r-227).

## 2. Frontière de configuration

Le workflow lit des variables publiques du dépôt pour le chemin et le digest de la policy de confiance, le scope du journal, l'URI/ID canonique du dépôt, la révision/digest de gouvernance, le digest de politique d'acceptation, le rôle de signataire requis et la branche protégée. La trust-policy épingle le chemin/digest de l'exécutable OpenSSL et les clés publiques des signataires. Il s'agit de configuration, pas de secrets ; le seul secret est le token GitHub à durée de vie courte du workflow.

Toute valeur absente ou non conforme provoque un échec fermé. Les PR provenant de forks ne sont pas prises en charge par cette première source. Le check est volontairement limité à Git et aux décisions PASS authentifiées.

## 3. Assurance et risques résiduels

Le check vérifie un reçu signé et ses bindings exacts ; une signature ne devient pas une preuve de la justesse de la décision sous-jacente. Le statement de journal signé atteste l'intégrité de chaîne vérifiée au moment de la signature, pas l'immutabilité future de la base. L'arbre candidat est haché par le code GovCheck de confiance mais jamais exécuté.

Le workflow crée un check en attente lors des événements du cycle de vie de la PR. Pour que le déplacement de la branche de base invalide les anciens résultats, le ruleset doit également exiger que la branche de PR soit à jour. Un status check seul ne bloque pas les push directs sans enforcement par le ruleset. Aucun réglage de forge n'est modifié par cette ADR.
