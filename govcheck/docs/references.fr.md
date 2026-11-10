# Paquet GovCheck — catalogue des références externes

Ce catalogue accompagne le paquet GovCheck réutilisable. Il ne contient que les sources directement pertinentes pour les contrats génériques d'assurance et de VCS ; les études propres au dépôt restent dans le catalogue méta à la racine du dépôt.

La présence d'une référence est descriptive, pas une adoption. Citer une méthode ou une norme ne signifie pas que GovCheck la sélectionne, l'implémente ou qu'un projet a été évalué avec elle.

<a id="r-05"></a>
## R-05 — TLA+ et TLC
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md), [spécification 0006](specifications/0006-governance-revision-applicability.fr.md), [spécification 0007](specifications/0007-canonical-governance-journal-protocol.fr.md), [README des modèles formels](formal/README.fr.md)

- **Sources primaires :** [Publications TLA de Lamport](https://www.microsoft.com/en-us/research/people/lamport/publications/) · [Projet et documentation TLA+](https://lamport.azurewebsites.net/tla/tla.html) · [DOI de l'article TLA](https://doi.org/10.1145/177492.177726)
- **Utilité :** spécifications par transitions d'états, invariants, propriétés temporelles et model checking.
- **Limite :** les résultats TLC ne valent que pour le modèle, la configuration, les hypothèses et les bornes explorées ; ils ne prouvent ni raffinement de l'implémentation ni fidélité normative.

<a id="r-06"></a>
## R-06 — Intégrité de chaîne logicielle in-toto
- **Cité par :** aucun document du paquet ne cite actuellement cette source.

- **Sources primaires :** [Projet in-toto](https://in-toto.io/) · [Article USENIX Security 2019](https://ssl.engineering.nyu.edu/papers/torres-toto-usenix19.pdf)
- **Utilité :** provenance des étapes de processus, matériaux et produits.
- **Limite :** la provenance n'établit pas qu'une étape enregistrée était sémantiquement correcte ou autorisée.

<a id="r-07"></a>
## R-07 — SLSA
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Source primaire :** [Spécification SLSA](https://slsa.dev/spec/)
- **Utilité :** provenance de build et intégrité de la chaîne logicielle.
- **Limite :** SLSA ne définit ni l'autorité de gouvernance GovCheck, ni le cycle des exceptions, ni un dossier d'assurance complet.

<a id="r-20"></a>
## R-20 — Lean
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Source primaire :** [Référence du langage Lean](https://lean-lang.org/doc/reference/latest/)
- **Utilité :** preuve de théorèmes et vérification de termes de preuve sous définitions, axiomes et hypothèses explicites.
- **Limite :** un théorème ne prouve pas que son prédicat représente la politique approuvée ni qu'un exécutable le raffine.

<a id="r-22"></a>
## R-22 — Sémantiques natives de Git et Pijul
- **Cité par :** [README des modèles formels](formal/README.fr.md), [spécification 0006](specifications/0006-governance-revision-applicability.fr.md), [spécification 0007](specifications/0007-canonical-governance-journal-protocol.fr.md)

- **Sources primaires :** [Documentation Git](https://git-scm.com/docs) · [Théorie Pijul](https://pijul.org/manual/theory) · [Canaux Pijul](https://pijul.org/manual/workflows/channels) · [Conflits Pijul](https://pijul.org/manual/conflicts.html)
- **Utilité :** préserver les sémantiques snapshot/commit de Git et celles de graphe de changements/patches, canaux et conflits de Pijul.
- **Limite :** la documentation ne prouve pas qu'un adaptateur GovCheck est implémenté ; les adaptateurs exigent encore des contrats natifs et des tests de conformité.

<a id="r-35"></a>
## R-35 — Common Criteria / ISO/IEC 15408
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Sources primaires :** [Portail Common Criteria](https://www.commoncriteriaportal.org/) · [Publications CC:2022 et CEM:2022](https://www.commoncriteriaportal.org/cc/index.cfm)
- **Utilité :** contexte pour l'évaluation de sécurité et les niveaux EAL.
- **Limite :** les EAL sont des ensembles d'exigences d'évaluation, pas des grades génériques de maturité logicielle ni des paliers d'assurance GovCheck.

<a id="r-36"></a>
## R-36 — RTCA DO-178C / EUROCAE ED-12C
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Sources primaires :** [FAA AC 20-115D](https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D) · [Présentation RTCA](https://www.rtca.org/do-178/)
- **Utilité :** objectifs de cycle de vie logiciel aéronautique, vérification et preuves de certification.
- **Limite :** norme d'assurance sectorielle dans un contexte de certification de navigabilité, pas réglementation logicielle générale.

<a id="r-37"></a>
## R-37 — Alloy
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Sources primaires :** [Projet et documentation Alloy](https://alloytools.org/) · [Code source de l'analyseur](https://github.com/AlloyTools/org.alloytools.alloy)
- **Utilité :** modélisation relationnelle, analyse bornée et recherche de contre-exemples.
- **Limite :** les résultats dépendent des portées et hypothèses ; ils n'établissent pas la conformité de l'implémentation.

<a id="r-38"></a>
## R-38 — SPIN / Promela
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Source primaire :** [Manuel SPIN](https://spinroot.com/spin/Man/Manual.html)
- **Utilité :** modélisation et vérification de systèmes concurrents/distribués et de propriétés temporelles.
- **Limite :** les résultats portent sur l'abstraction Promela et la configuration de recherche.

<a id="r-39"></a>
## R-39 — Kani
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Source primaire :** [Documentation Kani](https://model-checking.github.io/kani/)
- **Utilité :** model checking borné de programmes Rust et harnesses de preuve.
- **Limite :** fonctionnalités Rust et concurrence prises en charge limitées ; résultats dépendants des harnesses, bornes et toolchain.

<a id="r-40"></a>
## R-40 — Verus
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Source primaire :** [Tutoriel et référence Verus](https://verus-lang.github.io/verus/guide/)
- **Utilité :** vérification statique de correction fonctionnelle pour Rust.
- **Limite :** toutes les fonctionnalités/bibliothèques Rust ne sont pas prises en charge ; le vérificateur et la toolchain compilateur restent dans le socle de confiance.

<a id="r-41"></a>
## R-41 — Dafny
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Source primaire :** [Manuel de référence Dafny](https://dafny.org/dafny/DafnyRef/DafnyRef)
- **Utilité :** spécifications, pré/postconditions, invariants et vérification statique de programmes.
- **Limite :** les affirmations vérifiées dépendent de la spécification Dafny et du vérificateur/backend de confiance.

<a id="r-42"></a>
## R-42 — Coq / Rocq
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Sources primaires :** [Documentation Rocq](https://rocq-prover.org/docs) · [Documentation Coq versionnée](https://docs.rocq-prover.org/)
- **Utilité :** preuve de théorèmes vérifiée par machine en théorie des types dépendants.
- **Limite :** les résultats dépendent des définitions, axiomes, résultats importés et hypothèses du noyau/toolchain.

<a id="r-43"></a>
## R-43 — Isabelle
- **Cité par :** [spécification 0005](specifications/0005-assurance-model.fr.md)

- **Source primaire :** [Documentation Isabelle](https://www.isabelle.in.tum.de/documentation.html)
- **Utilité :** preuve interactive de théorèmes et spécification formelle.
- **Limite :** les résultats dépendent de la logique choisie, des théories importées, axiomes et environnement du prouveur.
