# Registre de références GovCheck : gouvernance, assurance et méthodes formelles

**Objet.** Ce registre rassemble les références académiques, normatives, industrielles et les sources de code qui étayent la conception de la gouvernance des dépôts dans GovCheck. C'est une bibliographie de navigation, pas une politique normative ni une décision d'adoption.

**Règle de sélection.** Privilégier les publications primaires, organismes de normalisation, documentations officielles et révisions de code épinglées. Chaque référence n'étaye que le point explicitement indiqué ; elle ne prouve ni que GovCheck implémente la capacité, ni que l'outil cité convient comme dépendance.

## Utilisation rapide

- **Autorité normative et séparation des tâches :** R-01, R-02, R-03.
- **Modèles formels, preuves et arguments d'assurance :** R-04, R-05.
- **Provenance des preuves et chaîne d'approvisionnement logicielle :** R-06, R-07, R-08.
- **Politiques exécutables et autorisation :** R-09, R-10.
- **Posture de sécurité et limites d'application :** R-11, R-12.
- **Schémas canoniques, versionnement et identité des releases :** R-13, R-14, R-15, R-16.
- **Patron externe de catalogue/gouvernance :** R-17.
- **Outils de workflow d'agents évalués, mais non adoptés :** R-18, R-19.
- **Assistant de preuve et contrats d'interface :** R-20, R-21.

## Normes, recommandations publiques et spécifications industrielles

### R-01 — NIST SP 800-53 Rev. 5, contrôles de sécurité et de confidentialité
- **Source primaire :** [Publication NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- **Concepts pertinents :** AC-5 (séparation des tâches), gestion des accès, auditabilité et responsabilité des contrôles.
- **Utilité pour GovCheck :** éclaire la distinction entre autorisation normative, revue technique et exécution, ainsi que les limites d'un régime à autorité unique.
- **Limite :** un catalogue de contrôles n'est pas l'ontologie de GovCheck ; sélectionner un contrôle ne démontre pas son implémentation.

### R-02 — NIST SP 800-218, Secure Software Development Framework (SSDF) 1.1
- **Sources primaires :** [Publication NIST](https://csrc.nist.gov/pubs/sp/800/218/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-218)
- **Concepts pertinents :** exigences et décisions de conception de sécurité documentées, pratiques de développement sécurisé, provenance et releases.
- **Utilité pour GovCheck :** référence pour les obligations traçables de développement et le contexte du cycle de vie où les preuves sont recueillies.
- **Limite :** SSDF est un guide de pratiques, pas un prédicat formel d'acceptation ni une preuve de conformité. NIST a aussi publié un projet de SP 800-218 Rev. 1 / SSDF 1.2 ; respecter le statut de publication invoqué.

### R-03 — Branches protégées et contrôles obligatoires GitHub
- **Source primaire :** [Documentation des branches protégées](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- **Concepts pertinents :** revues obligatoires, contrôles de statut, exceptions de contournement et restrictions de branche.
- **Utilité pour GovCheck :** exemple concret d'un point d'application partagé pour l'acceptation.
- **Limite :** les paramètres de la forge sont des mécanismes d'application, pas l'autorité normative. Les administrateurs et acteurs autorisés à contourner les règles restent dans le modèle de menace.

### R-04 — Goal Structuring Notation (GSN), standard communautaire
- **Source primaire :** [Site officiel du standard GSN](https://scsc.uk/gsn)
- **Concepts pertinents :** structuration des affirmations d'assurance, arguments, stratégies, contexte, hypothèses et preuves.
- **Utilité pour GovCheck :** vocabulaire utile au dossier d'assurance et à la traçabilité des exigences vers les propriétés et les preuves.
- **Limite :** structurer un argument ne rend pas automatiquement ses prémisses vraies et ne remplace pas les prédicats vérifiables.

### R-05 — TLA+ et TLC
- **Sources primaires :** [Publications de Lamport sur TLA](https://www.microsoft.com/en-us/research/people/lamport/publications/) · [Projet et documentation TLA+](https://lamport.azurewebsites.net/tla/tla.html)
- **Référence académique :** Leslie Lamport, « The Temporal Logic of Actions », ACM Transactions on Programming Languages and Systems, 16(3), 1994, p. 872–923. [DOI](https://doi.org/10.1145/177492.177726)
- **Concepts pertinents :** spécifications à transitions d'état, invariants, propriétés temporelles et model checking.
- **Utilité pour GovCheck :** fondement des modèles du cycle de vie, de l'assurance et des transitions d'autorité.
- **Limite :** un TLC terminé établit des propriétés uniquement pour le modèle, la configuration, les hypothèses et les bornes consignées ; il ne prouve ni le raffinement de l'implémentation ni la fidélité normative.

### R-06 — in-toto : intégrité de la chaîne d'approvisionnement logicielle
- **Sources primaires :** [Projet in-toto](https://in-toto.io/) · [Article USENIX Security 2019](https://ssl.engineering.nyu.edu/papers/torres-toto-usenix19.pdf)
- **Référence académique :** Santiago Torres-Arias et al., « in-toto: Providing farm-to-table guarantees for bits and bytes », 28th USENIX Security Symposium, 2019.
- **Concepts pertinents :** enregistrement des étapes, matériaux/produits et provenance d'une chaîne logicielle.
- **Utilité pour GovCheck :** provenance et liaison des enregistrements de contrôle/preuve aux artefacts et étapes qui les ont produits.
- **Limite :** la provenance ne définit pas les règles normatives propres au dépôt et ne prouve pas la correction sémantique d'une étape enregistrée.

### R-07 — SLSA
- **Source primaire :** [Spécification SLSA](https://slsa.dev/spec/)
- **Concepts pertinents :** niveaux de chaîne d'approvisionnement logicielle, provenance et intégrité de construction.
- **Utilité pour GovCheck :** vocabulaire complémentaire pour la provenance des builds et les preuves de release.
- **Limite :** SLSA ne définit ni l'autorité canonique de GovCheck, ni sa politique d'exception, ni son cycle de vie, ni un dossier d'assurance complet.

### R-08 — OpenSSF Scorecard
- **Sources primaires :** [Page OpenSSF](https://openssf.org/projects/scorecard/) · [Dépôt Scorecard](https://github.com/ossf/scorecard)
- **Concepts pertinents :** contrôles automatisés et réutilisables de certaines pratiques de sécurité open source.
- **Utilité pour GovCheck :** source candidate de preuves circonscrites sur la posture de sécurité.
- **Limite :** un score n'est ni une évaluation complète de la gouvernance du dépôt, ni une preuve, ni une décision d'autorisation.

### R-09 — Open Policy Agent (OPA)
- **Source primaire :** [Documentation officielle OPA](https://www.openpolicyagent.org/docs)
- **Concepts pertinents :** séparation entre décision de politique et application ; évaluation d'entrées structurées par rapport à une politique.
- **Utilité pour GovCheck :** éclaire une séparation possible entre évaluateur et point d'application, et une comparaison de politiques déclaratives.
- **Limite :** OPA n'est ni l'autorité normative de GovCheck, ni son moteur d'assurance, ni une preuve de résistance au contournement. Aucune dépendance n'est sélectionnée.

### R-10 — Langage d'autorisation Cedar
- **Sources primaires :** [Référence du langage Cedar](https://docs.cedarpolicy.com/) · [Projet Cedar](https://www.cedarpolicy.com/)
- **Concepts pertinents :** décisions d'autorisation typées portant sur principal/action/ressource/contexte et séparation de la logique d'autorisation de la logique applicative.
- **Utilité pour GovCheck :** référence pour une comparaison future de l'autorisation par périmètre et des sémantiques déterministes de décision.
- **Limite :** Cedar n'est pas un cycle de vie complet, un modèle de fraîcheur des preuves ou un dossier d'assurance. Aucune dépendance n'est sélectionnée.

### R-11 — NIST SSDF : page du projet
- **Source primaire :** [Projet NIST SSDF et publications](https://csrc.nist.gov/projects/ssdf)
- **Concepts pertinents :** pratiques de développement sécurisé et correspondances avec des pratiques établies.
- **Utilité pour GovCheck :** navigation complémentaire sur le statut des publications et profils SSDF.
- **Limite :** utiliser la publication finale datée pour une affirmation portant sur une version précise ; ne pas confondre projet de révision et norme finale.

### R-12 — OpenSSF Scorecard : signaux de posture de sécurité
- **Source primaire :** [Projet Scorecard](https://github.com/ossf/scorecard)
- **Concepts pertinents :** indicateurs de sécurité inspectables indépendamment.
- **Utilité pour GovCheck :** adaptateur de preuve externe facultatif ; conserver le contrôle, la version, le sujet et le résultat brut plutôt que le seul score global.
- **Limite :** les signaux peuvent être incomplets, contextuels ou erronés ; ils ne doivent pas remplacer les règles obligatoires du projet.

### R-13 — JSON Schema Draft 2020-12
- **Source primaire :** [Page officielle de la spécification](https://json-schema.org/draft/2020-12/)
- **Concepts pertinents :** validation structurelle d'enregistrements lisibles par machine.
- **Utilité pour GovCheck :** référence candidate pour les enregistrements de gouvernance et manifestes de preuve si JSON Schema est adopté.
- **Limite :** la validité du schéma n'établit ni autorisation, ni cohérence sémantique, ni vérité, ni adoption d'une politique, ni correction de l'évaluateur. Cette entrée ne le sélectionne pas comme format canonique.

### R-14 — Semantic Versioning 2.0.0
- **Source primaire :** [SemVer 2.0.0](https://semver.org/)
- **Concepts pertinents :** MAJOR/MINOR/PATCH par rapport à une API publique et à un contrat de compatibilité déclarés ; les versions publiées sont immuables.
- **Utilité pour GovCheck :** éclaire la distinction entre identité d'artefact, révision immuable, compatibilité du contrat et identité de release.
- **Limite :** SemVer n'a pas de sens pour tous les artefacts de gouvernance. GovCheck évite de l'appliquer mécaniquement aux modèles, preuves, décisions ou événements.

### R-15 — Tags Git et releases
- **Sources primaires :** [Référence Git : étiquetage](https://git-scm.com/book/en/v2/Git-Basics-Tagging) · [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- **Concepts pertinents :** identification d'une révision source et publication des artefacts associés à une release.
- **Utilité pour GovCheck :** rapports de vérification et manifestes liés à une release, identifiant l'arbre Git, le commit, le modèle, la configuration et les versions des outils.
- **Limite :** un tag ou une release est un mécanisme d'identification/publication, pas la preuve qu'une vérification a été exécutée ou réussie.

### R-16 — OpenAPI et contrats d'interface lisibles par machine
- **Source primaire :** [Spécification OpenAPI](https://spec.openapis.org/oas/latest.html)
- **Concepts pertinents :** contrats d'interface lisibles par machine.
- **Utilité pour GovCheck :** contrats possibles pour le CLI/dossier et documentation des adaptateurs.
- **Limite :** la conformité d'une interface ne prouve ni les sémantiques d'autorisation, ni le comportement d'exécution, ni la correction de l'implémentation.

### R-17 — Google Cloud Knowledge Catalog
- **Source primaire :** [Documentation Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs)
- **Concepts pertinents :** métadonnées typées, entrées de catalogue, relations/traçabilité, métadonnées de gouvernance et découverte de contexte.
- **Utilité pour GovCheck :** le patron transposable est celui des métadonnées obligatoires selon le type d'objet et des relations traçables entre objets gouvernés.
- **Limite :** GovCheck n'est pas un catalogue de données. Ne pas importer l'architecture produit ni supposer que la présence de métadonnées équivaut à une autorité normative ou à une application effective.

## Projets industriels évalués comme complémentaires, non adoptés

### R-18 — Writ (infinri/Writ)
- **Sources primaires :** [Dépôt](https://github.com/infinri/Writ) · [Politique de sécurité à la révision étudiée](https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/SECURITY.md) · [Contrat de session et de barrières](https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/docs/reference/session-and-gates.md)
- **Révision étudiée :** ebdafe5450b201339f81e717ed104e6bcfd3fe3e (revue consignée le 6 novembre 2026).
- **Utilité pour GovCheck :** fixture facultative de test de workflow d'agent et source potentielle de preuves d'exécution circonscrites.
- **Limite :** Writ indique explicitement ne pas être un bac à sable ni une frontière de sécurité ; ses sorties ne sont ni l'autorité normative de GovCheck ni une décision d'acceptation indépendante. Voir l'architecture 0016.

### R-19 — Privateer (privateer-agent/privateer-agent)
- **Sources primaires :** [Dépôt](https://github.com/privateer-agent/privateer-agent) · [Politique de sécurité à la révision étudiée](https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/SECURITY.md) · [README à la révision étudiée](https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/README.md)
- **Révision étudiée :** 181a988e443fa6b6b4138fc349d1260c96408ad4 (revue consignée le 6 novembre 2026).
- **Utilité pour GovCheck :** fixture candidate d'interopérabilité avec un harness d'agent fondé sur Pi.
- **Limite :** une barrière de permission, une fonctionnalité de provenance ou un avertissement de confidentialité ne remplace pas la gouvernance canonique ou une acceptation vérifiée indépendamment. Voir l'architecture 0016.

## Fondements académiques et assistant de preuve

### R-20 — Lean
- **Source primaire :** [Référence du langage Lean](https://lean-lang.org/doc/reference/latest/)
- **Concepts pertinents :** termes de preuve vérifiés par un petit noyau ; démonstration sous définitions, axiomes et hypothèses explicites.
- **Utilité pour GovCheck :** candidat pour des prédicats critiques justifiant une preuve ou la vérification de certificats, si une ADR ultérieure le justifie.
- **Limite :** un théorème sur un prédicat ne prouve ni que le prédicat représente la politique approuvée ni que l'exécutable le raffine. Lean n'est pas sélectionné comme dépendance globale.

### R-21 — Guides de releases et de reproductibilité pour le logiciel de recherche
- **Source primaire :** [Software Sustainability Institute — guides et ressources](https://www.software.ac.uk/resources)
- **Concepts pertinents :** pérennité du logiciel de recherche, citation, releases et reproductibilité.
- **Utilité pour GovCheck :** appuie l'enregistrement des versions exactes des logiciels/outils et du contexte de release nécessaires à l'interprétation des preuves.
- **Limite :** des recommandations générales ne remplacent pas un contrat concret de manifeste de release. Lier un guide précis lorsqu'une recommandation particulière est invoquée.

## Discipline bibliographique et provenance non résolue

1. Privilégier l'organisme normatif, l'éditeur, la documentation officielle ou le dépôt source plutôt que les résumés secondaires.
2. Épingler les analyses de code. Les liens Writ et Privateer identifient les révisions examinées dans l'architecture 0016 ; les actualiser avant toute affirmation sur leur comportement courant.
3. Distinguer les classes de preuve. Une norme, un article scientifique, une documentation produit, du code source, un résultat de test et un rapport de model checking sont des types de preuve différents.
4. Aucune adoption implicite. La présence dans ce registre signifie « pertinent à évaluer », pas « sélectionné », « obligatoire », « compatible » ou « implémenté ».
5. Pas de bibliographie inventée. La discussion précédente mentionnait « Agent Package Manager », mais n'a pas conservé d'URL unique et vérifiée du projet. Il n'est volontairement pas cité comme produit identifié avant établissement de son identité exacte.
6. Garder les liens près des affirmations. Les documents d'architecture doivent lier les sources qui étayent directement leurs affirmations et renvoyer ici pour la bibliographie plus large.

## Documents d'architecture associés

- [0006 — Modèle de menace et de confiance](../architecture/0006-threat-and-trust-model.md) : R-01, R-02, R-06, R-07.
- [0008 — Plan de formalisation et de conformité](../architecture/0008-formalization-and-conformance.md) : R-05, R-13, R-20.
- [0010 — Assurance, témoignage, preuve et conformité](../architecture/0010-assurance-proof-and-conformance.md) : R-04, R-05, R-06, R-20.
- [0013 — Métamodèle de gouvernance](../architecture/0013-governance-metamodel.md) : R-01, R-09, R-10, R-13.
- [0015 — Plan de conformité et validation de la gouvernance](../architecture/0015-governance-conformance-and-validation-plan.md) : R-02, R-06, R-07, R-08, R-09, R-10.
- [0016 — Évaluation de Writ et Privateer](../architecture/0016-writ-privateer-assessment.md) : R-18, R-19.
- [0017–0019 — Identité, versionnement et manifeste de release](../architecture/README.md) : R-14, R-15, R-16.
- [0022 — Audit des capacités de gouvernance](../architecture/0022-governance-capability-audit.md) : R-01, R-02, R-03, R-09, R-10, R-17.
- [0023 — Décision d'amorçage de l'autorité](../architecture/0023-bootstrap-governance-authority.md) : R-01, R-03.


### R-22 — Sémantiques natives de Git et Pijul
- **Sources primaires :** [Documentation Git](https://git-scm.com/docs) · [Manuel Pijul : théorie](https://pijul.org/manual/theory) · [Canaux Pijul](https://pijul.org/manual/workflows/channels) · [Conflits Pijul](https://pijul.org/manual/conflicts.html)
- **Concepts pertinents :** modèle de snapshots/commits et arbres de Git ; graphe de changements/patches, canaux et conflits de première classe de Pijul.
- **Utilité pour GovCheck :** justifie la frontière explicite des adaptateurs VCS et l'obligation de représenter l'identité du candidat, les conflits et l'application selon les sémantiques natives plutôt que de tout forcer dans une abstraction inspirée de Git.
- **Limite :** la documentation des projets décrit leurs sémantiques visées ; GovCheck doit encore fournir contrats d'adaptateur et tests de conformité. Cette référence ne prouve pas qu'un adaptateur est implémenté.

- [0004 — Contrats des adaptateurs VCS et collaboration](../specifications/0004-vcs-collaboration-contracts.fr.md) : R-22.
