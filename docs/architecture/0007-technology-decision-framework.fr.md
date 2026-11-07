# Architecture 0007 — Cadre de décision technologique

**Statut :** cadre de décision, pas sélection de technologies. **English:** [0007](0007-technology-decision-framework.md).

Ce document définit comment choisir sans imposer prématurément une pile. Chaque candidat est évalué selon les mêmes cas d'usage, modèle de menace et tests de conformité. Un score ne décide pas seul : les contraintes éliminatoires sont des portes, et les scores doivent être accompagnés de preuves et inconnues.

## 1. Portes éliminatoires

Écarter ou différer un candidat s'il :
- ne préserve pas les sémantiques Git et Pijul derrière des adaptateurs distincts ;
- exige service hébergé, daemon résident, serveur MCP obligatoire ou plan de contrôle privilégié ;
- relègue l'usage local au second plan ;
- ne fournit pas d'évaluation déterministe et bornée ni d'états indéterminé/erreur explicites ;
- impose l'exécution arbitraire de code de politique du dépôt ;
- empêche des builds/distributions reproductibles sur les plateformes visées ;
- impose dépendances ou contraintes de licence inacceptables ;
- confond tests, model checking, preuves, conformité et acceptation.

## 2. Dimensions à comparer

| Décision | Familles candidates (illustratives, non exhaustives) | Critères |
|---|---|---|
| Langage | Rust, Go, OCaml, Haskell, Kotlin/JVM, Python | Garanties statiques, portabilité, taille/démarrage, écosystème, contributeurs, FFI, chaîne d'approvisionnement, maintenance |
| Sérialisation canonique | JSON + JSON Schema, sous-ensemble YAML, TOML, CBOR, encodage canonique spécifique | Déterminisme, doublons, octets canoniques, évolution du schéma, commentaires/édition, outils, signatures |
| Sémantique | Prédicats typés fixes, DSL restreint, moteur logique/règles | Décidabilité/bornes, explicabilité, composition, sûreté, formalisation, extensibilité |
| Analyse formelle | TLA+, Alloy, PlusCal, Lean, Coq, Isabelle, machines à états exécutables | Claims établissables, TCB, automatisation, compétences, reproductibilité |
| Intégrité des preuves | Hashes, attestations signées, journaux de transparence, formats compatibles in-toto/SLSA | Liaison d'état, identité, révocation, offline, confidentialité, interopérabilité, charge |
| Interface locale | Binaire unique, paquets plateformes, distribution source | Installation, reproductibilité, offline, confiance de mise à jour, plateformes |
| Forge | Adaptateurs GitHub/GitLab/Forgejo/Gitea/Bitbucket ; protocoles génériques | Barrière requise, liaison état exact, contournements, stabilité API, auto-hébergement |
| Pijul | CLI/bibliothèque native et adaptateurs Nest/serveur équipe | Fidélité patches/canaux/graphe/conflits, offline, maturité, maintenance |
| Orchestration des contrôles | Commandes existantes du projet, protocole de preuve standardisé | Moindre privilège, reproductibilité, délais, sortie, absence de toolchain obligatoire |

## 3. Évaluation pondérée après les portes

Pour les candidats admissibles, noter de 0 à 5 avec preuve et confiance : adéquation sémantique (20 %), analysabilité formelle (15 %), sécurité/TCB (15 %), maintenabilité (15 %), portabilité/offline (10 %), écosystème/interopérabilité (10 %), coût opérationnel (10 %), coût de migration/réversibilité (5 %). Pondérations provisoires, à revoir avant notation. Une donnée inconnue reste « inconnue », jamais zéro ni succès supposé. Publier preuves brutes et analyse de sensibilité ; ne pas optimiser aveuglément le score composite.

## 4. Dossier de décision requis

Chaque ADR indique : question et urgence ; contraintes/portes ; alternatives, y compris « différer/sans nouvelle dépendance » ; sources, versions et dates ; preuves de prototypes/tests ; impact sécurité/TCB ; implications Git/Pijul/local ; coût migration/retour arrière ; décision et rejets ; confiance ; déclencheurs de réexamen ; résumé bilingue.

## 5. Ordre suggéré

1. Spécifier invariants sémantiques et hypothèses de menace (propositions rédigées, revue requise).
2. Prototyper sérialisation/canonicalisation et tests différentiels de parseurs.
3. Comparer modèle fixe de règles typées et langages d'expression restreints.
4. Modéliser cycle de vie/concurrence avec TLA+/Alloy ou méthode adaptée ; prouver les propriétés du noyau après clarification des frontières.
5. Comparer les langages via un petit prototype d'évaluateur/parseur.
6. Définir interopérabilité des attestations et cycle de vie des clés.
7. Prototyper séparément les descripteurs d'état Git et Pijul.
8. Choisir ensuite packaging et adaptateurs forge.

Aucun langage, format de sérialisation, noyau formel, format de signature, licence ou dépendance n'est sélectionné ici.

## Références bibliographiques

- [R-05 — Modélisation par transitions d'états TLA+ / TLC](../references.fr.md#r-05)
- [R-06 — Provenance de chaîne logicielle in-toto](../references.fr.md#r-06)
- [R-07 — Assurance de chaîne logicielle SLSA](../references.fr.md#r-07)
- [R-20 — Assistant de preuve Lean](../references.fr.md#r-20)
- [R-22 — Sémantiques natives Git et Pijul](../references.fr.md#r-22)
- [R-35 — Common Criteria / ISO/IEC 15408](../references.fr.md#r-35)
- [R-36 — RTCA DO-178C / EUROCAE ED-12C](../references.fr.md#r-36)
- [R-37 — Alloy](../references.fr.md#r-37)
- [R-38 — SPIN / Promela](../references.fr.md#r-38)
- [R-39 — Kani](../references.fr.md#r-39)
- [R-40 — Verus](../references.fr.md#r-40)
- [R-41 — Dafny](../references.fr.md#r-41)
- [R-42 — Coq / Rocq](../references.fr.md#r-42)
- [R-43 — Isabelle](../references.fr.md#r-43)
