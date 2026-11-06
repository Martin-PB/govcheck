# Spécification 0005 — Assurance, affirmations et preuves

**Statut :** architecture proposée, prête pour revue. **English:** [0005](0005-assurance-model.md).

## Objet et vocabulaire

Indiquer exactement ce qui est établi, par quelle méthode, sur quel sujet/état et sous quelles hypothèses. Ne jamais confondre exécution de tests, model checking, preuve de théorème, conformité de l'implémentation, fidélité normative et acceptation sous un « vérifié » générique.

Chaque dossier distingue affirmation (proposition réfutable et bornée), argument, preuve (résultat d'une méthode/outil), hypothèse, contexte, limite/réfutation possible et décision autorisée. Une affirmation sur un modèle ne porte pas sur le programme sans argument de conformité distinct.

## Classes de méthodes non interchangeables

1. **Exécution empirique :** tests, linters, builds, scans ; résultats observés dans la portée/environnement exécutés.
2. **Model checking :** exploration d'un modèle selon bornes/hypothèses ; ne dit rien automatiquement de l'implémentation.
3. **Preuve de théorème :** vérification d'une dérivation dans une logique/noyau ; consigner axiomes, imports, hypothèses et échappements.
4. **Conformité de l'implémentation :** relation et méthode explicites de raffinement/conformité entre programme et spécification.
5. **Fidélité normative :** traçabilité entre règles approuvées, IDs formels et projections humaines fidèles.
6. **Acceptation :** décision de gouvernance selon laquelle claims/preuves/approbations satisfont le prédicat pour un candidat exact ; elle ne prouve pas toutes les affirmations sous-jacentes.

## Enregistrement des preuves

Lier IDs stables de preuve/claims ; type et identité native immuable du sujet ; dépôt et empreintes exactes base/candidat ; révision/sémantique du paquet de gouvernance ; révision de spécification/modèle ; méthode/portée ; outil/version/configuration/invocation ; environnement, hypothèses, bornes, entrées externes ; résultat brut ou référence protégée ; résultat/date/producteur/provenance ; limites et dépendances d'invalidation. Un code retour seul ne prouve que le résultat de cette invocation.

Les claims déclarent méthodes acceptables, portée, fraîcheur et corroboration. Une preuve soutient, réfute ou laisse indécis. Les contradictions restent visibles. Les arguments décomposent les claims en sous-claims, hypothèses et preuves ; un raisonnement circulaire n'est pas présenté comme preuve.

## Méthodes formelles et socle de confiance

Pour une preuve, consigner logique, noyau/vérificateur et version, axiomes, théorèmes importés, obligations admises, fonctionnalités unsafe, oracles et reproductibilité. Si Lean est choisi, comptabiliser explicitement sorry, axiomes non examinés, unsafe, oracles natifs et confiance dans les dépendances.

Pour le model checking, consigner révision, configuration/constantes, réductions, équité, nombres d'états/transitions, bornes et complétude. Une exploration bornée/partielle n'est jamais dite exhaustive.

Pour la conformité : révisions programme/spécification, relation de raffinement, frontière d'abstraction et méthode. Pour la fidélité normative : approbateurs et traçabilité source-règle-projection.

## Provenance, confiance et fraîcheur

Hashes/signatures peuvent établir intégrité/origine sous hypothèses de clés, pas correction sémantique, autorisation ni vérité externe. Les faits externes exigent source, date de collecte, validité et classification de confiance. Divulguer le TCB : évaluateur, parseur/canonicalisation, adaptateurs VCS, vérificateurs, bibliothèques crypto, runtime et autorités distantes.

Chaque preuve déclare ses dépendances. Modification, compromission d'outil/clé, correction de source ou défaut découvert peuvent l'invalider. Conserver l'historique ; exclure les preuves invalidées des décisions actuelles sauf revalidation.

## Rapports et objectifs de conformité

Rapporter claims, statut, preuves, hypothèses, limites, état lié, provenance, réfutations non résolues et décision exacte. Distinguer non exécuté, non applicable, non pris en charge, incomplet, échoué et réussi ; éviter les scores opaques.

Une implémentation conforme lie les preuves aux états/révisions exacts, expose hypothèses/TCB, conserve contradictions et invalidations, distingue exploration bornée/exhaustive, comptabilise axiomes/noyau et exige des preuves de conformité avant toute affirmation sur le programme. Aucun moteur ni dispositif de preuve n'existe encore.
