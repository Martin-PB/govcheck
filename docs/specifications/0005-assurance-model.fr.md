# Spécification 0005 — Assurance, affirmations et preuves

**Statut :** architecture proposée, prête pour revue. **English:** [0005](0005-assurance-model.md).

## Objet et vocabulaire

Indiquer exactement ce qui est établi, par quelle méthode, sur quel sujet/état et sous quelles hypothèses. Ne jamais confondre exécution de tests, model checking, preuve de théorème, conformité de l'implémentation, fidélité normative et acceptation sous un « vérifié » générique.

Chaque dossier distingue affirmation (proposition réfutable et bornée), argument, preuve (résultat d'une méthode/outil), hypothèse, contexte, limite/réfutation possible et décision autorisée. Une affirmation sur un modèle ne porte pas sur le programme sans argument de conformité distinct.

## Classes de méthodes non interchangeables

Les classes de méthodes sont l'axe principal ; le mot « niveaux » est réservé au seul sous-ensemble empirique (SLSA, Common Criteria EAL et DO-178C DAL utilisent « levels » sur d'autres axes).

Pour la reconstruction détaillée de ces distinctions (auto-certification vs vérification, témoignage vs preuve, les trois questions d'assurance, statuts des preuves), voir l'enregistrement d'architecture [0010 — Assurance, témoignage, preuve et conformité](../architecture/0010-assurance-proof-and-conformance.fr.md), qui complète cette spécification sans la remplacer.

### Classe 1 — Exécution empirique (sous-niveaux)

| Sous-niveau | Exemples | Établit | N'établit pas |
|---|---|---|---|
| 1a. Tests unitaires | assert_eq!, Vitest | Le comportement attendu sur les cas exécutés | Toute généralité au-delà |
| 1b. Tests d'intégration | plusieurs composants exécutés ensemble | Le chemin fonctionnel testé fonctionne | La composition complète du système |
| 1c. Tests de propriétés | entrées générées, vérification d'invariants | Des propriétés tiennent sur un ensemble élargi d'entrées | Une preuve, même sur le domaine généré |
| 1d. Analyse statique | Clippy, TypeScript strict, linters | Certaines catégories d'erreurs détectées sans exécution | Le comportement réel à l'exécution |

> Une suite de tests, même très complète, n'est pas une preuve formelle.

### Classes formelles et de gouvernance

2. **Model checking :** exploration d'un modèle selon bornes/hypothèses (TLA+/TLC, Alloy, Spin) ; ne dit rien automatiquement de l'implémentation.
3. **Vérification de programmes :** établit des propriétés du programme ou de ses spécifications dans un cadre logique précis (Kani, Verus, Dafny, Lean).
4. **Preuve de théorème :** vérification d'une dérivation dans une logique/noyau (Lean, Coq, Isabelle) ; consigner axiomes, imports, hypothèses et échappements.
5. **Conformité de l'implémentation :** relation et méthode explicites de raffinement/conformité entre programme et spécification.
6. **Fidélité normative :** traçabilité entre règles approuvées, IDs formels et projections humaines fidèles.
7. **Acceptation :** décision de gouvernance pour un candidat exact ; ne prouve pas que toutes les affirmations sont vraies.

## Chaîne de conformité prouvable (langage naturel → formel → implémentation)

La conformité à un texte en langage naturel (ex. AGENTS.md) ne se déduit pas automatiquement d'un programme. Elle s'établit par une chaîne tracée :

    texte normatif → interprétation approuvée (autorité humaine compétente, datée, versionnée)
                   → spécification formelle (règle formelle à ID stable)
                   → implémentation prouvée conforme à cette spécification

- Chaque maillon est consigné dans un registre d'interprétations (ID de règle stable, révision et empreinte du texte source, approbateur, date, spécification formelle référencée).
- Prouver le dernier maillon ne prouve pas les précédents.
- GovCheck ne déclare jamais « conforme » un cas insuffisamment vérifié (l'indéterminé n'est pas un succès).
- La projection vers l'humain est déterministe : générée par script depuis les artefacts formels (diagrammes Mermaid, diagrammes de séquence issus de traces TLC), jamais produite directement par un LLM. La documentation HTML générée servie aux validateurs est un artefact versionné avec contrôle de dérive, comme le diagramme de cycle de vie.

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

## Références bibliographiques

- [R-05 — Modélisation par transitions d'états TLA+ / TLC](../references.fr.md#r-05)
- [R-07 — Niveaux d'assurance de la chaîne logicielle SLSA](../references.fr.md#r-07)
- [R-20 — Assistant de preuve Lean](../references.fr.md#r-20)
- [R-35 — Common Criteria / ISO/IEC 15408 et évaluation EAL](../references.fr.md#r-35)
- [R-36 — Assurance logicielle aéronautique RTCA DO-178C / EUROCAE ED-12C](../references.fr.md#r-36)
- [R-37 — Modélisation relationnelle et analyse Alloy](../references.fr.md#r-37)
- [R-38 — Model checking de systèmes concurrents SPIN / Promela](../references.fr.md#r-38)
- [R-39 — Vérificateur de programmes Rust Kani](../references.fr.md#r-39)
- [R-40 — Vérification Rust Verus](../references.fr.md#r-40)
- [R-41 — Spécification et vérification de programmes Dafny](../references.fr.md#r-41)
- [R-42 — Assistant de preuve Coq / Rocq](../references.fr.md#r-42)
- [R-43 — Assistant de preuve Isabelle](../references.fr.md#r-43)
- [R-89 — spécification/raffinement formels par la méthode B et Atelier B](../references.fr.md#r-89)
- [R-90 — notation de spécification formelle Z (ISO/IEC 13568)](../references.fr.md#r-90)
- [R-91 — Communicating Sequential Processes et vérification de raffinement FDR](../references.fr.md#r-91)
