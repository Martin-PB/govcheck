# Catalogue des références externes de GovCheck

## Index thématique

| Thème | Entrées |
|---|---|
| Autorité de gouvernance, séparation des tâches et développement sécurisé | R-01–R-03, R-11 |
| Évaluation des risques, modélisation des menaces et chemins d'attaque | R-27–R-32 |
| Dossiers d'assurance de sécurité et métamodèles | R-33–R-34 |
| Modèle de décision PEAK | R-74 |
| Surveillance continue et assurance à l'exécution | R-70, R-72, R-75–R-76 |
| Assurance 2.0 et évolution de SACM | R-71, R-73 |
| Régimes d'assurance et exigences orientées objectifs | R-35–R-36, R-44 |
| Model checking et vérification de programmes candidates | R-37–R-43 |
| Provenance des preuves et chaîne d'approvisionnement logicielle | R-06–R-08 |
| Moteurs de politiques et autorisation | R-09–R-10 |
| Schémas et contrats d'interface | R-13, R-16 |
| Identité, versionnement, releases et reproductibilité des artefacts | R-14–R-15, R-21, R-23–R-26 |
| Métadonnées de gouvernance et catalogues | R-17 |
| Systèmes de workflow d'agents évalués comme fixtures | R-18–R-19 |
| Sémantiques de contrôle de version | R-22 |
| CRDT, collaboration temps réel et transport réseau | R-45–R-50, R-66 |
| Représentation des connaissances et interopérabilité | R-51–R-61 |
| Dépôts et études d'intégration | R-62 |
| Protocoles d'intégration et conventions documentaires | R-67 |
| Dépôts adjacents de l'écosystème GovCheck | R-68 |
| Sources du panorama des formats de cartes mentales | R-69 |
| Formats d'échange de cartes mentales et de graphes | R-63 |
| Gouvernance des outils agents et MCP | R-77 |
| Modèles de conformité structurés | R-78 |
| Sandboxing et isolation des agents | R-79 |
| Communication Matrix | R-80 |
| Recherche documentaire | R-81 |
| Extraction de documents | R-82 |
| API de stockage cloud | R-64 |
| Persistance locale navigateur et WebAssembly | R-65 |

## Entrées bibliographiques détaillées

## Registre détaillé des sources

**Objet.** Ce fichier est la bibliographie française unique de GovCheck. Il rassemble les références académiques, normatives, industrielles et les sources de code qui étayent la conception du projet. C'est une bibliographie de navigation, pas une politique normative ni une décision d'adoption.

**Règle de sélection.** Privilégier les publications primaires, organismes de normalisation, documentations officielles et révisions de code épinglées. Chaque référence n'étaye que le point explicitement indiqué ; elle ne prouve ni que GovCheck implémente la capacité, ni que l'outil cité convient comme dépendance.

## Utilisation rapide

- **Autorité normative et séparation des tâches :** R-01, R-02, R-03.
- **Modèles formels, preuves et arguments d'assurance :** R-04, R-05.
- **Provenance des preuves et chaîne d'approvisionnement logicielle :** R-06, R-07, R-08.
- **Politiques exécutables et autorisation :** R-09, R-10.
- **Posture de sécurité et limites d'application :** R-03, R-08, R-18, R-19.
- **Schémas canoniques, versionnement et identité des releases :** R-13, R-14, R-15, R-16.
- **Patron externe de catalogue/gouvernance :** R-17.
- **Outils de workflow d'agents évalués, mais non adoptés :** R-18, R-19.
- **Assistant de preuve et contrats d'interface :** R-20, R-21.
- **Sémantiques natives des VCS et adaptateurs de collaboration :** R-22.
- **Modélisation des menaces, chemins d'attaque et gestion des risques :** R-27 à R-32.
- **Dossiers d'assurance de sécurité et métamodèles :** R-33 à R-34.
- **Modèle de décision PEAK :** R-74.
- **Surveillance continue et assurance à l'exécution :** R-70, R-72, R-75 à R-76.
- **Assurance 2.0 et évolution de SACM :** R-71, R-73.

## Normes, recommandations publiques et spécifications industrielles

<a id="r-01"></a>
### R-01 — NIST SP 800-53 Rev. 5, contrôles de sécurité et de confidentialité
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Publication NIST SP 800-53](https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final)
- **Concepts pertinents :** AC-5 (séparation des tâches), gestion des accès, auditabilité et responsabilité des contrôles.
- **Utilité pour GovCheck :** éclaire la distinction entre autorisation normative, revue technique et exécution, ainsi que les limites d'un régime à autorité unique.
- **Limite :** un catalogue de contrôles n'est pas l'ontologie de GovCheck ; sélectionner un contrôle ne démontre pas son implémentation.

<a id="r-02"></a>

### R-02 — NIST SP 800-218, Secure Software Development Framework (SSDF) 1.1
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Publication NIST](https://csrc.nist.gov/pubs/sp/800/218/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-218)
- **Concepts pertinents :** exigences et décisions de conception de sécurité documentées, pratiques de développement sécurisé, provenance et releases.
- **Utilité pour GovCheck :** référence pour les obligations traçables de développement et le contexte du cycle de vie où les preuves sont recueillies.
- **Limite :** SSDF est un guide de pratiques, pas un prédicat formel d'acceptation ni une preuve de conformité. NIST a aussi publié un projet de SP 800-218 Rev. 1 / SSDF 1.2 ; respecter le statut de publication invoqué.

<a id="r-03"></a>

### R-03 — Branches protégées et contrôles obligatoires GitHub
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Documentation des branches protégées](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches)
- **Concepts pertinents :** revues obligatoires, contrôles de statut, exceptions de contournement et restrictions de branche.
- **Utilité pour GovCheck :** exemple concret d'un point d'application partagé pour l'acceptation.
- **Limite :** les paramètres de la forge sont des mécanismes d'application, pas l'autorité normative. Les administrateurs et acteurs autorisés à contourner les règles restent dans le modèle de menace.

<a id="r-04"></a>

### R-04 — Goal Structuring Notation (GSN), standard communautaire
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Site officiel du standard GSN](https://scsc.uk/gsn)
- **Concepts pertinents :** structuration des affirmations d'assurance, arguments, stratégies, contexte, hypothèses et preuves.
- **Utilité pour GovCheck :** vocabulaire utile au dossier d'assurance et à la traçabilité des exigences vers les propriétés et les preuves.
- **Limite :** structurer un argument ne rend pas automatiquement ses prémisses vraies et ne remplace pas les prédicats vérifiables.

<a id="r-05"></a>

### R-05 — TLA+ et TLC
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Publications de Lamport sur TLA](https://www.microsoft.com/en-us/research/people/lamport/publications/) · [Projet et documentation TLA+](https://lamport.azurewebsites.net/tla/tla.html)
- **Référence académique :** Leslie Lamport, « The Temporal Logic of Actions », ACM Transactions on Programming Languages and Systems, 16(3), 1994, p. 872–923. [DOI](https://doi.org/10.1145/177492.177726)
- **Concepts pertinents :** spécifications à transitions d'état, invariants, propriétés temporelles et model checking.
- **Utilité pour GovCheck :** fondement des modèles du cycle de vie, de l'assurance et des transitions d'autorité.
- **Limite :** un TLC terminé établit des propriétés uniquement pour le modèle, la configuration, les hypothèses et les bornes consignées ; il ne prouve ni le raffinement de l'implémentation ni la fidélité normative.

<a id="r-06"></a>

### R-06 — in-toto : intégrité de la chaîne d'approvisionnement logicielle
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Projet in-toto](https://in-toto.io/) · [Article USENIX Security 2019](https://ssl.engineering.nyu.edu/papers/torres-toto-usenix19.pdf)
- **Référence académique :** Santiago Torres-Arias et al., « in-toto: Providing farm-to-table guarantees for bits and bytes », 28th USENIX Security Symposium, 2019.
- **Concepts pertinents :** enregistrement des étapes, matériaux/produits et provenance d'une chaîne logicielle.
- **Utilité pour GovCheck :** provenance et liaison des enregistrements de contrôle/preuve aux artefacts et étapes qui les ont produits.
- **Limite :** la provenance ne définit pas les règles normatives propres au dépôt et ne prouve pas la correction sémantique d'une étape enregistrée.

<a id="r-07"></a>

### R-07 — SLSA
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Spécification SLSA](https://slsa.dev/spec/)
- **Concepts pertinents :** niveaux de chaîne d'approvisionnement logicielle, provenance et intégrité de construction.
- **Utilité pour GovCheck :** vocabulaire complémentaire pour la provenance des builds et les preuves de release.
- **Limite :** SLSA ne définit ni l'autorité canonique de GovCheck, ni sa politique d'exception, ni son cycle de vie, ni un dossier d'assurance complet.

<a id="r-08"></a>

### R-08 — OpenSSF Scorecard
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Page OpenSSF](https://openssf.org/projects/scorecard/) · [Dépôt Scorecard](https://github.com/ossf/scorecard)
- **Concepts pertinents :** contrôles automatisés et réutilisables de certaines pratiques de sécurité open source.
- **Utilité pour GovCheck :** source candidate de preuves circonscrites sur la posture de sécurité.
- **Limite :** un score n'est ni une évaluation complète de la gouvernance du dépôt, ni une preuve, ni une décision d'autorisation.

<a id="r-09"></a>

### R-09 — Open Policy Agent (OPA)
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Documentation officielle OPA](https://www.openpolicyagent.org/docs)
- **Concepts pertinents :** séparation entre décision de politique et application ; évaluation d'entrées structurées par rapport à une politique.
- **Utilité pour GovCheck :** éclaire une séparation possible entre évaluateur et point d'application, et une comparaison de politiques déclaratives.
- **Limite :** OPA n'est ni l'autorité normative de GovCheck, ni son moteur d'assurance, ni une preuve de résistance au contournement. Aucune dépendance n'est sélectionnée.

<a id="r-10"></a>

### R-10 — Langage d'autorisation Cedar
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Référence du langage Cedar](https://docs.cedarpolicy.com/) · [Projet Cedar](https://www.cedarpolicy.com/)
- **Concepts pertinents :** décisions d'autorisation typées portant sur principal/action/ressource/contexte et séparation de la logique d'autorisation de la logique applicative.
- **Utilité pour GovCheck :** référence pour une comparaison future de l'autorisation par périmètre et des sémantiques déterministes de décision.
- **Limite :** Cedar n'est pas un cycle de vie complet, un modèle de fraîcheur des preuves ou un dossier d'assurance. Aucune dépendance n'est sélectionnée.

<a id="r-11"></a>

### R-11 — NIST SSDF : page du projet
- **Cité par :** [0013](architecture/0013-governance-metamodel.fr.md), [0022](architecture/0022-governance-capability-audit.fr.md)

- **Source primaire :** [Projet NIST SSDF et publications](https://csrc.nist.gov/projects/ssdf)
- **Concepts pertinents :** pratiques de développement sécurisé et correspondances avec des pratiques établies.
- **Utilité pour GovCheck :** navigation complémentaire sur le statut des publications et profils SSDF.
- **Limite :** utiliser la publication finale datée pour une affirmation portant sur une version précise ; ne pas confondre projet de révision et norme finale.

<a id="r-13"></a>

### R-13 — JSON Schema Draft 2020-12
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Page officielle de la spécification](https://json-schema.org/draft/2020-12/)
- **Concepts pertinents :** validation structurelle d'enregistrements lisibles par machine.
- **Utilité pour GovCheck :** référence candidate pour les enregistrements de gouvernance et manifestes de preuve si JSON Schema est adopté.
- **Limite :** la validité du schéma n'établit ni autorisation, ni cohérence sémantique, ni vérité, ni adoption d'une politique, ni correction de l'évaluateur. Cette entrée ne le sélectionne pas comme format canonique.

<a id="r-14"></a>

### R-14 — Semantic Versioning 2.0.0
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [SemVer 2.0.0](https://semver.org/)
- **Concepts pertinents :** MAJOR/MINOR/PATCH par rapport à une API publique et à un contrat de compatibilité déclarés ; les versions publiées sont immuables.
- **Utilité pour GovCheck :** éclaire la distinction entre identité d'artefact, révision immuable, compatibilité du contrat et identité de release.
- **Limite :** SemVer n'a pas de sens pour tous les artefacts de gouvernance. GovCheck évite de l'appliquer mécaniquement aux modèles, preuves, décisions ou événements.

<a id="r-15"></a>

### R-15 — Tags Git et releases
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Référence Git : étiquetage](https://git-scm.com/book/en/v2/Git-Basics-Tagging) · [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
- **Concepts pertinents :** identification d'une révision source et publication des artefacts associés à une release.
- **Utilité pour GovCheck :** rapports de vérification et manifestes liés à une release, identifiant l'arbre Git, le commit, le modèle, la configuration et les versions des outils.
- **Limite :** un tag ou une release est un mécanisme d'identification/publication, pas la preuve qu'une vérification a été exécutée ou réussie.

<a id="r-16"></a>

### R-16 — OpenAPI et contrats d'interface lisibles par machine
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Spécification OpenAPI](https://spec.openapis.org/oas/latest.html)
- **Concepts pertinents :** contrats d'interface lisibles par machine.
- **Utilité pour GovCheck :** contrats possibles pour le CLI/dossier et documentation des adaptateurs.
- **Limite :** la conformité d'une interface ne prouve ni les sémantiques d'autorisation, ni le comportement d'exécution, ni la correction de l'implémentation.

<a id="r-17"></a>

### R-17 — Google Cloud Knowledge Catalog
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Documentation Knowledge Catalog](https://docs.cloud.google.com/knowledge-catalog/docs)
- **Concepts pertinents :** métadonnées typées, entrées de catalogue, relations/traçabilité, métadonnées de gouvernance et découverte de contexte.
- **Utilité pour GovCheck :** le patron transposable est celui des métadonnées obligatoires selon le type d'objet et des relations traçables entre objets gouvernés.
- **Limite :** il s'agit du produit de catalogue de données Google Cloud, et non de l'Open Knowledge Format (OKF), référencé séparément en R-51. GovCheck n'est pas un catalogue de données ; la présence de métadonnées n'équivaut ni à une autorité normative ni à une application effective.

## Projets industriels évalués comme complémentaires, non adoptés

<a id="r-18"></a>
### R-18 — Writ (infinri/Writ)
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Dépôt](https://github.com/infinri/Writ) · [Politique de sécurité à la révision étudiée](https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/SECURITY.md) · [Contrat de session et de barrières](https://github.com/infinri/Writ/blob/ebdafe5450b201339f81e717ed104e6bcfd3fe3e/docs/reference/session-and-gates.md)
- **Révision étudiée :** ebdafe5450b201339f81e717ed104e6bcfd3fe3e (revue consignée le 6 novembre 2026).
- **Utilité pour GovCheck :** fixture facultative de test de workflow d'agent et source potentielle de preuves d'exécution circonscrites.
- **Limite :** Writ indique explicitement ne pas être un bac à sable ni une frontière de sécurité ; ses sorties ne sont ni l'autorité normative de GovCheck ni une décision d'acceptation indépendante. Voir l'architecture 0016.

<a id="r-19"></a>

### R-19 — Privateer (privateer-agent/privateer-agent)
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Dépôt](https://github.com/privateer-agent/privateer-agent) · [Politique de sécurité à la révision étudiée](https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/SECURITY.md) · [README à la révision étudiée](https://github.com/privateer-agent/privateer-agent/blob/181a988e443fa6b6b4138fc349d1260c96408ad4/README.md)
- **Révision étudiée :** 181a988e443fa6b6b4138fc349d1260c96408ad4 (revue consignée le 6 novembre 2026).
- **Utilité pour GovCheck :** fixture candidate d'interopérabilité avec un harness d'agent fondé sur Pi.
- **Limite :** une barrière de permission, une fonctionnalité de provenance ou un avertissement de confidentialité ne remplace pas la gouvernance canonique ou une acceptation vérifiée indépendamment. Voir l'architecture 0016.

<a id="r-20"></a>
### R-20 — Lean
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Référence du langage Lean](https://lean-lang.org/doc/reference/latest/)
- **Concepts pertinents :** termes de preuve vérifiés par un petit noyau ; démonstration sous définitions, axiomes et hypothèses explicites.
- **Utilité pour GovCheck :** candidat pour des prédicats critiques justifiant une preuve ou la vérification de certificats, si une ADR ultérieure le justifie.
- **Limite :** un théorème sur un prédicat ne prouve ni que le prédicat représente la politique approuvée ni que l'exécutable le raffine. Lean n'est pas sélectionné comme dépendance globale.

<a id="r-21"></a>

### R-21 — Guides de releases et de reproductibilité pour le logiciel de recherche
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Software Sustainability Institute — guides et ressources](https://www.software.ac.uk/resources)
- **Concepts pertinents :** pérennité du logiciel de recherche, citation, releases et reproductibilité.
- **Utilité pour GovCheck :** appuie l'enregistrement des versions exactes des logiciels/outils et du contexte de release nécessaires à l'interprétation des preuves.
- **Limite :** des recommandations générales ne remplacent pas un contrat concret de manifeste de release. Lier un guide précis lorsqu'une recommandation particulière est invoquée.

<a id="r-22"></a>

### R-22 — Sémantiques natives de Git et Pijul
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Documentation Git](https://git-scm.com/docs) · [Manuel Pijul : théorie](https://pijul.org/manual/theory) · [Canaux Pijul](https://pijul.org/manual/workflows/channels) · [Conflits Pijul](https://pijul.org/manual/conflicts.html)
- **Concepts pertinents :** modèle de snapshots/commits et arbres de Git ; graphe de changements/patches, canaux et conflits de première classe de Pijul.
- **Utilité pour GovCheck :** justifie la frontière explicite des adaptateurs VCS et l'obligation de représenter l'identité du candidat, les conflits et l'application selon les sémantiques natives plutôt que de tout forcer dans une abstraction inspirée de Git.
- **Limite :** la documentation des projets décrit leurs sémantiques visées ; GovCheck doit encore fournir contrats d'adaptateur et tests de conformité. Cette référence ne prouve pas qu'un adaptateur est implémenté.

- [0004 — Contrats des adaptateurs VCS et collaboration](specifications/0004-vcs-collaboration-contracts.fr.md) : R-22.

## Fondements académiques et assistant de preuve

<a id="r-23"></a>

### R-23 — IMS Global / 1EdTech : spécifications de versionnement
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Spécifications 1EdTech](https://www.imsglobal.org/spec/versioning/v1) (anciennement IMS Global ; consulter la version précise avant d'invoquer une règle particulière).
- **Concepts pertinents :** identifiants de version et conventions de compatibilité pour des artefacts structurés et publiés.
- **Utilité pour GovCheck :** élément comparatif de l'analyse du versionnement par catégorie dans les architectures 0017–0018.
- **Limite :** famille de spécifications propre aux technologies éducatives, pas norme universelle de versionnement des artefacts de gouvernance.

<a id="r-24"></a>

### R-24 — W3C PROV-O
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Recommandation W3C PROV-O](https://www.w3.org/TR/prov-o/).
- **Concepts pertinents :** entités, activités, agents et relations de provenance.
- **Utilité pour GovCheck :** vocabulaire de provenance et relations entre artefacts, activités et agents responsables.
- **Limite :** une ontologie ne fournit à elle seule ni politique de dépôt, ni assurance d'identité, ni mécanisme d'application.

<a id="r-25"></a>

### R-25 — Guide de versionnement DataCite
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Documentation DataCite sur le versionnement](https://support.datacite.org/docs/versioning).
- **Concepts pertinents :** identification et relations entre versions de productions scientifiques citables.
- **Utilité pour GovCheck :** éclaire la distinction entre identité logique persistante d'un artefact et versions identifiées individuellement.
- **Limite :** les recommandations pour les productions scientifiques ne constituent pas une politique générale pour tous les artefacts logiciels et de gouvernance.

<a id="r-26"></a>

### R-26 — Étude sur le versionnement des données scientifiques (2024)
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Article Nature / Scientific Data](https://www.nature.com/articles/s41597-024-03153-y).
- **Concepts pertinents :** pratiques de versionnement et de provenance des données scientifiques.
- **Utilité pour GovCheck :** apport de recherche comparatif à la réflexion sur l'identité et le versionnement des artefacts.
- **Limite :** une recherche propre à un domaine ne définit pas une règle normative de versionnement pour GovCheck.

<a id="r-27"></a>
### R-27 — NIST SP 800-30 Rev. 1, Guide pour la conduite des évaluations des risques
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Publication NIST](https://csrc.nist.gov/pubs/sp/800/30/r1/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-30r1)
- **Concepts pertinents :** sources et événements de menace, vulnérabilités, vraisemblance et impact, évaluation des risques, risque résiduel, hypothèses, justification et incertitude.
- **Utilité pour GovCheck :** étaye une évaluation par scénario qui consigne la manière dont la plausibilité est estimée, les dimensions d'impact considérées, les mesures déjà en place, l'incertitude et la justification du résultat.
- **Limite :** NIST SP 800-30 est un guide d'évaluation des risques, pas une formule quantitative universelle ni une obligation d'utiliser une échelle particulière. GovCheck ne doit pas transformer des échelles illustratives en mesures étalonnées.

<a id="r-28"></a>
### R-28 — NIST SP 800-160 Vol. 1 Rev. 1, Engineering Trustworthy Secure Systems
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Publication NIST](https://csrc.nist.gov/pubs/sp/800/160/v1/r1/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-160v1r1)
- **Concepts pertinents :** ingénierie de la sécurité des systèmes sur l'ensemble du cycle de vie ; besoins de protection des parties prenantes ; exigences, architecture, implémentation, vérification, validation et gestion des risques.
- **Utilité pour GovCheck :** appuie le lien entre besoins de protection, exigences de sécurité, architecture, contrôles, preuves de vérification et décisions de cycle de vie, plutôt qu'une analyse de menaces réduite à un questionnaire ponctuel.
- **Limite :** cette publication est un guide d'ingénierie, pas un schéma de gouvernance de dépôt ni une preuve qu'un système donné satisfait ses exigences de sécurité.

<a id="r-29"></a>
### R-29 — ISO 31000:2018, Management du risque — Lignes directrices
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Page officielle de la norme ISO](https://www.iso.org/standard/31000)
- **Concepts pertinents :** principes et cadre pour identifier, analyser, évaluer, traiter, surveiller, revoir et communiquer les risques.
- **Utilité pour GovCheck :** référence générale de gestion des risques pour maintenir l'évaluation, le traitement, l'acceptation, la surveillance et la revue dans un même processus de gouvernance et de décision.
- **Limite :** ISO 31000 fournit des lignes directrices génériques, pas une taxonomie des menaces cyber ni un algorithme prescrit de calcul du risque. Le texte intégral de la norme n'est pas reproduit ici.

<a id="r-30"></a>
### R-30 — MITRE ATT&CK
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Base de connaissances MITRE ATT&CK](https://attack.mitre.org/) · [Guide de démarrage et d'utilisation](https://attack.mitre.org/resources/)
- **Concepts pertinents :** tactiques et techniques adverses fondées sur des comportements observés ; correspondances entre techniques, plateformes et mesures d'atténuation.
- **Utilité pour GovCheck :** vocabulaire et source de preuves facultatifs pour enrichir les scénarios de menace et l'analyse des chemins d'attaque, et examiner si les contrôles proposés répondent à des comportements adverses connus.
- **Limite :** ATT&CK n'est ni un modèle exhaustif des menaces, ni un estimateur de vraisemblance, ni une base de vulnérabilités, ni une preuve d'exploitabilité. Une correspondance avec une technique ne démontre ni sa faisabilité dans le contexte du projet ni l'efficacité d'une mesure d'atténuation.

<a id="r-31"></a>
### R-31 — Microsoft Security Development Lifecycle : modélisation des menaces
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Guide Microsoft SDL sur la modélisation des menaces](https://www.microsoft.com/en-us/securityengineering/sdl/threatmodeling)
- **Concepts pertinents :** exigences de sécurité, diagrammes de système et de flux de données, identification des menaces, atténuation et validation dans un processus itératif d'ingénierie.
- **Utilité pour GovCheck :** exemple industriel d'un parcours répétable de modélisation des menaces reliant architecture et frontières de confiance aux mesures d'atténuation et à leur validation.
- **Limite :** le processus Microsoft est une méthode pratique, pas une norme complète de gouvernance des risques ou de dossier d'assurance. Ses exemples et son outil ne sont pas des dépendances obligatoires de GovCheck.

<a id="r-32"></a>
### R-32 — Bruce Schneier, « Attack Trees » (1999)
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Article du Dr. Dobb's Journal, archivé par Schneier](https://www.schneier.com/academic/archives/1999/12/attack_trees.html)
- **Référence académique/technique :** Bruce Schneier, « Attack Trees », *Dr. Dobb's Journal*, décembre 1999.
- **Concepts pertinents :** décomposition hiérarchique des objectifs d'un attaquant en sous-objectifs alternatifs ou conjoints ; raisonnement sur la faisabilité et le coût d'une attaque.
- **Utilité pour GovCheck :** technique fondatrice pour représenter les chemins d'attaque et les différentes manières d'atteindre un objectif nuisible, et relier les mesures d'atténuation aux étapes précises d'un chemin.
- **Limite :** les arbres d'attaque sont des modèles dont l'exhaustivité et les estimations de paramètres doivent être justifiées. Les coûts ou probabilités attribués aux nœuds ne doivent pas être considérés comme objectifs sans données étalonnées.

<a id="r-33"></a>
### R-33 — Mohamad, Steghöfer et Scandariato, « Security assurance cases—state of the art of an emerging approach » (2021)
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Article d'Empirical Software Engineering](https://doi.org/10.1007/s10664-021-09971-7)
- **Référence académique :** Mazen Mohamad, Jan-Philipp Steghöfer et Riccardo Scandariato, *Empirical Software Engineering* 26, article 70 (2021).
- **Concepts pertinents :** revue systématique de 51 études sur les dossiers d'assurance de sécurité ; affirmations structurées, argumentation, hypothèses, contexte et preuves ; état de la validation et des outils.
- **Utilité pour GovCheck :** justifie de rendre explicites affirmations, hypothèses, contexte, inférences et preuves, tout en traitant la construction et la maintenance d'un dossier d'assurance comme une activité d'ingénierie qui doit être validée.
- **Limite :** la revue constate un domaine encore immature et des lacunes de validation et de support outillé ; elle ne démontre pas que l'adoption d'une notation de dossier d'assurance produit automatiquement un argument de sécurité valide.

<a id="r-34"></a>
### R-34 — OMG Structured Assurance Case Metamodel (SACM)
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Famille de spécifications OMG SACM](https://www.omg.org/spec/SACM/) · [Version formelle 2.3](https://www.omg.org/spec/SACM/2.3)
- **Concepts pertinents :** représentation exploitable par machine de structures de dossiers d'assurance et relations entre affirmations, argumentation, artefacts et preuves.
- **Utilité pour GovCheck :** métamodèle comparatif possible pour les artefacts d'assurance typés et leur traçabilité, au-delà de documents narratifs libres.
- **Limite :** SACM est un métamodèle, pas une méthode d'évaluation des risques, un oracle de vérité ni une preuve de suffisance des éléments probants. La version 2.4 est actuellement une bêta ; cette entrée renvoie à la version formelle 2.3 et ne recommande pas l'adoption de SACM.

## Sources complémentaires retrouvées dans les discussions sur l'assurance et l'intégration

<a id="r-35"></a>
### R-35 — Common Criteria (ISO/IEC 15408) et méthode commune d'évaluation
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Portail Common Criteria](https://www.commoncriteriaportal.org/) · [Publications CC:2022 et CEM:2022](https://www.commoncriteriaportal.org/cc/index.cfm)
- **Concepts pertinents :** exigences fonctionnelles de sécurité, exigences d'assurance, méthode d'évaluation et niveaux EAL (Evaluation Assurance Levels).
- **Utilité pour GovCheck :** contextualise le vocabulaire d'assurance explicitement distingué des classes de méthodes de GovCheck dans la spécification 0005.
- **Limite :** les EAL sont des ensembles d'exigences d'assurance dans le régime Common Criteria, pas des niveaux génériques de maturité logicielle ni des paliers d'assurance GovCheck. Le périmètre et la cible d'évaluation comptent.

<a id="r-36"></a>
### R-36 — RTCA DO-178C / EUROCAE ED-12C : assurance logicielle aéronautique
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [FAA AC 20-115D](https://www.faa.gov/airports/resources/advisory_circulars/index.cfm/go/document.information/documentNumber/20-115D) · [Présentation RTCA de DO-178C et de ses suppléments](https://www.rtca.org/do-178/)
- **Concepts pertinents :** objectifs du cycle de vie logiciel, vérification, indépendance, preuves de certification et niveaux logiciels A–E ; suppléments associés : DO-330, DO-331, DO-332 et DO-333.
- **Utilité pour GovCheck :** fournit l'exemple aéronautique d'assurance/certification nommé dans la spécification 0005 et distingue les régimes sectoriels des méthodes génériques de test et de preuve.
- **Limite :** DO-178C est une norme d'assurance logicielle aéronautique dans un contexte de certification de navigabilité. La circulaire FAA AC 20-115D décrit un moyen acceptable, pas le seul moyen ni une réglementation logicielle générale. La présentation publique RTCA ne reproduit pas la norme complète.

<a id="r-37"></a>
### R-37 — Langage et analyseur Alloy
- **Cité par :** [0005](specifications/0005-assurance-model.fr.md), [0007](architecture/0007-technology-decision-framework.fr.md), [0009](architecture/0009-govcheck-design-discussion-record.fr.md)

- **Sources primaires :** [Projet Alloy et documentation](https://alloytools.org/) · [Dépôt source de l'analyseur Alloy](https://github.com/AlloyTools/org.alloytools.alloy)
- **Concepts pertinents :** modélisation relationnelle, analyse bornée, recherche d'instances par SAT et recherche de contre-exemples ; Alloy 6 ajoute états mutables et opérateurs temporels.
- **Utilité pour GovCheck :** méthode candidate de modélisation formelle citée dans la spécification 0005 et les architectures 0007/0009.
- **Limite :** les résultats dépendent des portées, bornes et hypothèses déclarées ; l'analyse Alloy ne prouve pas l'implémentation sans argument distinct de raffinement/conformité.

<a id="r-38"></a>
### R-38 — SPIN et Promela
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Manuel SPIN et documentation Promela](https://spinroot.com/spin/Man/Manual.html)
- **Concepts pertinents :** modélisation et vérification de systèmes concurrents/distribués, communication asynchrone, invariants, interblocages et propriétés temporelles.
- **Utilité pour GovCheck :** vérificateur de modèles candidat nommé dans la spécification 0005, distinct de TLA+/TLC et Alloy.
- **Limite :** la vérification porte sur l'abstraction Promela et le mode/options de recherche retenus ; elle n'établit ni conformité de l'implémentation ni fidélité normative.

<a id="r-39"></a>
### R-39 — Vérificateur Rust Kani
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Documentation Kani](https://model-checking.github.io/kani/)
- **Concepts pertinents :** model checking borné de programmes Rust, harnesses de preuve, assertions, détection de comportements indéfinis et contre-exemples.
- **Utilité pour GovCheck :** méthode candidate de vérification de programmes citée dans la spécification 0005.
- **Limite :** les fonctionnalités Rust prises en charge et la couverture de la concurrence sont limitées ; un harness réussi établit seulement les propriétés modélisées avec les bornes et la toolchain configurées.

<a id="r-40"></a>
### R-40 — Vérification Rust avec Verus
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Tutoriel et référence Verus](https://verus-lang.github.io/verus/guide/)
- **Concepts pertinents :** vérification statique de correction fonctionnelle de programmes Rust à l'aide de spécifications et de preuves assistées.
- **Utilité pour GovCheck :** méthode candidate de vérification de programmes citée dans la spécification 0005.
- **Limite :** Verus ne prend pas en charge toutes les fonctionnalités et bibliothèques Rust et ne prétend vérifier ni les compilateurs Rust/LLVM ni lui-même ; les composants de confiance et constructions non prises en charge restent pertinents.

<a id="r-41"></a>
### R-41 — Langage et vérificateur Dafny
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Manuel de référence Dafny](https://dafny.org/dafny/DafnyRef/DafnyRef)
- **Concepts pertinents :** constructions de spécification, pré/postconditions, invariants, métriques de terminaison, conditions de vérification et compilation.
- **Utilité pour GovCheck :** système candidat de vérification de programmes cité dans la spécification 0005.
- **Limite :** les affirmations vérifiées dépendent des spécifications Dafny, du vérificateur et de la toolchain ; elles ne valident pas que la spécification représente la politique approuvée.

<a id="r-42"></a>
### R-42 — Assistant de preuve Coq / Rocq
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Documentation et manuels de référence Rocq](https://rocq-prover.org/docs) · [Archives de documentation Coq versionnée](https://docs.rocq-prover.org/)
- **Concepts pertinents :** théorie des types dépendants, définitions Gallina et termes de preuve vérifiés par machine.
- **Utilité pour GovCheck :** Coq est nommé dans la spécification 0005 ; le projet se nomme désormais Rocq, les noms historique et actuel sont donc conservés.
- **Limite :** une dérivation vérifiée établit un théorème sous ses définitions, axiomes, résultats importés et hypothèses du noyau/toolchain ; elle n'établit pas l'adéquation normative.

<a id="r-43"></a>
### R-43 — Assistant de preuve Isabelle
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Documentation, tutoriels et manuels de référence Isabelle](https://www.isabelle.in.tum.de/documentation.html)
- **Concepts pertinents :** preuve interactive de théorèmes, Isabelle/HOL, spécification formelle et vérification de preuves.
- **Utilité pour GovCheck :** assistant de preuve candidat nommé dans la spécification 0005.
- **Limite :** les résultats dépendent de la logique, des théories importées, des axiomes et de l'environnement de preuve ; aucune intégration Isabelle n'est sélectionnée.

<a id="r-44"></a>
### R-44 — KAOS et ingénierie des exigences orientée objectifs
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Axel van Lamsweerde, Requirements Engineering: From System Goals to UML Models to Software Specifications (2009), notice UCLouvain](https://research.dial.uclouvain.be/entities/publication/ddcd5cbc-c76d-4da2-bd29-509cbf0f9399)
- **Concepts pertinents :** raffinement d'objectifs, obstacles, attribution des responsabilités et dérivation des objectifs système vers exigences et spécifications logicielles.
- **Utilité pour GovCheck :** source de la famille KAOS/GORE explicitement mentionnée dans l'architecture 0013.
- **Limite :** méthode d'ingénierie des exigences et source académique ; ce n'est ni une ontologie GovCheck adoptée ni un langage de politiques exécutable.

<a id="r-45"></a>
### R-45 — Fondements des CRDT
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Shapiro, Preguiça, Baquero et Zawirski, « A comprehensive study of Convergent and Commutative Replicated Data Types » (rapport de recherche INRIA 7506, 2011)](https://dsf.berkeley.edu/cs286/papers/crdt-tr2011.pdf)
- **Concepts pertinents :** types répliqués fondés sur l'état ou les opérations, conditions de convergence, réplication asynchrone et mises à jour concurrentes.
- **Utilité pour GovCheck :** source fondatrice de la discussion CRDT/coédition retrouvée dans l'étude d'intégration Cartocortex.
- **Limite :** la convergence ne préserve pas à elle seule l'intention utilisateur, ne définit ni autorisation, ni transport/persistance, et ne garantit pas la préservation des invariants métier.

<a id="r-46"></a>
### R-46 — Yjs et Yrs
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Documentation Yjs](https://docs.yjs.dev/) · [Dépôt source Yjs](https://github.com/yjs/yjs) · [Port Rust Yrs](https://github.com/y-crdt/y-crdt)
- **Concepts pertinents :** types de données CRDT partagés, mises à jour indépendantes du transport, fournisseurs de synchronisation et édition collaborative.
- **Utilité pour GovCheck :** famille d'implémentations candidate explicitement comparée dans l'étude de transport/backlog de la PR Cartocortex #28.
- **Limite :** le comportement d'une bibliothèque ne choisit ni le modèle de données applicatif ni l'architecture de transport ; les déplacements d'arbres, undo/redo, persistance et migrations propres à Cartocortex exigent des tests distincts.

<a id="r-47"></a>
### R-47 — Automerge
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Documentation Automerge](https://automerge.org/docs/) · [Dépôt source Automerge](https://github.com/automerge/automerge)
- **Concepts pertinents :** documents CRDT local-first, fusion de changements concurrents, historique et synchronisation indépendante du transport.
- **Utilité pour GovCheck :** implémentation candidate explicitement comparée dans l'étude Cartocortex de la PR #28.
- **Limite :** la fusion CRDT ne préserve pas automatiquement l'intention métier ni les permissions ; réseau et stockage doivent être évalués séparément.

<a id="r-48"></a>
### R-48 — CRDT Loro
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Documentation Loro](https://loro.dev/docs) · [Concepts CRDT de Loro](https://www.loro.dev/docs/concepts/crdt) · [Dépôt source Loro](https://github.com/loro-dev/loro)
- **Concepts pertinents :** arbres/listes déplaçables, CRDT de texte enrichi, synchronisation local-first, historique et retour dans le temps.
- **Utilité pour GovCheck :** candidat explicitement mis en avant dans l'étude de la PR #28 parce que ses arbres déplaçables pourraient correspondre aux structures de cartes mentales.
- **Limite :** la matrice de fonctionnalités du projet ne constitue pas une évaluation indépendante d'adéquation ; tester identité, déplacement/suppression, undo/redo et persistance de Cartocortex avant sélection.

<a id="r-49"></a>
### R-49 — Communication temps réel WebRTC
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Recommandation W3C WebRTC 1.0](https://www.w3.org/TR/webrtc/) · [RFC 8835 — Transports pour WebRTC](https://www.rfc-editor.org/rfc/rfc8835.html)
- **Concepts pertinents :** connexions pair-à-pair, canaux de données, sécurité des transports et interaction avec ICE, STUN et TURN.
- **Utilité pour GovCheck :** références protocolaires principales pour l'option de transport pair-à-pair discutée pour la coédition Cartocortex.
- **Limite :** WebRTC ne définit ni signalisation applicative, ni autorisation des salles, ni sémantique CRDT, ni persistance. Pair-à-pair ne signifie pas sans infrastructure ni sans métadonnées.

<a id="r-50"></a>
### R-50 — ICE, STUN, TURN et infrastructure de relais
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [RFC 8445 — ICE](https://www.rfc-editor.org/rfc/rfc8445.html) · [RFC 8489 — STUN](https://www.rfc-editor.org/rfc/rfc8489.html) · [RFC 8656 — TURN](https://www.rfc-editor.org/rfc/rfc8656.html) · [Implémentation de relais coturn](https://github.com/coturn/coturn)
- **Concepts pertinents :** collecte de candidats et vérifications de connectivité, traversée NAT, allocation de relais et repli lorsque les chemins directs échouent.
- **Utilité pour GovCheck :** documente la pile protocolaire précise derrière les mentions STUN/TURN de l'étude Cartocortex.
- **Limite :** STUN seul n'est pas une solution de traversée NAT ; TURN relaie le trafic et introduit disponibilité, coût, confidentialité et contraintes opérationnelles. L'estimation approximative d'usage du relais dans le PDF est une affirmation d'étude, pas une garantie protocolaire.

<a id="r-51"></a>
### R-51 — Open Knowledge Format (OKF) v0.2
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Spécification canonique OKF v0.2](https://github.com/GoogleCloudPlatform/open-knowledge-format/blob/main/SPEC.md) · [Spécification OKF v0.2 dans l'ancien dépôt Knowledge Catalog](https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md)
- **Concepts pertinents :** bundles de connaissances portables fondés sur Markdown, frontmatter YAML, liens et métadonnées de provenance, confiance et cycle de vie.
- **Utilité pour GovCheck :** source de l'étude de stockage OKF et des projections de cartes mentales dans la PR Cartocortex #27 ; c'est le sens précis de « OKF » dans cette discussion.
- **Limite :** OKF est une convention légère de bundle de connaissances, pas une ontologie de graphe, un modèle de disposition de carte mentale, un CRDT, un protocole de transport ou une norme de gouvernance GovCheck. L'ancien chemin Knowledge Catalog est un instantané gelé ; le dépôt dédié est canonique.

<a id="r-52"></a>
### R-52 — Modèle de données RDF 1.1
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [W3C RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf11-concepts/)
- **Concepts pertinents :** modèle de graphes et jeux de données fondé sur des triplets sujet–prédicat–objet et des IRI.
- **Utilité pour GovCheck :** modèle de données fondamental discuté pour une représentation de connaissances partagée entre Cartocortex, MoriNet et SaussuNet.
- **Limite :** RDF est un modèle de données, pas une ontologie métier, un moteur de stockage, un langage de validation ou un protocole de collaboration.

<a id="r-53"></a>
### R-53 — SKOS
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Référence W3C SKOS](https://www.w3.org/TR/skos-reference/)
- **Concepts pertinents :** concepts identifiés par URI, libellés, notations, schémas conceptuels, correspondances et relations sémantiques légères.
- **Utilité pour GovCheck :** vocabulaire envisagé pour taxonomies et organisation des concepts dans l'étude d'intégration.
- **Limite :** SKOS n'est ni un modèle général d'objets applicatifs ni un substitut aux axiomes OWL, contraintes SHACL ou mécanismes de collaboration CRDT.

<a id="r-54"></a>
### R-54 — Langage d'ontologie OWL 2
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [W3C OWL 2 Structural Specification and Functional-Style Syntax](https://www.w3.org/TR/owl-syntax/)
- **Concepts pertinents :** sémantique formellement définie pour classes, propriétés, individus et axiomes d'ontologie.
- **Utilité pour GovCheck :** couche sémantique candidate discutée aux côtés de RDF et SKOS dans l'étude d'intégration.
- **Limite :** le raisonnement OWL ne valide pas toutes les contraintes de données applicatives, ne préserve pas automatiquement toutes les propriétés des sources et ne fournit ni workflow, ni contrôle d'accès, ni synchronisation.

<a id="r-55"></a>
### R-55 — SHACL
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [W3C Shapes Constraint Language (SHACL)](https://www.w3.org/TR/shacl/)
- **Concepts pertinents :** validation de graphes RDF selon des formes et contraintes déclarées.
- **Utilité pour GovCheck :** candidat pour valider structurellement les graphes de connaissances normalisés dans la discussion d'intégration SaussuNet.
- **Limite :** la validation SHACL ne prouve ni vérité sémantique, ni authenticité de provenance, ni autorisation, ni conformité de l'implémentation de transformation.

<a id="r-56"></a>
### R-56 — Termes de métadonnées Dublin Core
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Spécification DCMI Metadata Terms](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/)
- **Concepts pertinents :** propriétés et classes de métadonnées générales pour décrire des ressources.
- **Utilité pour GovCheck :** vocabulaire de métadonnées candidat discuté pour les ressources documentaires du profil de connaissances partagé.
- **Limite :** les termes Dublin Core ne définissent ni modèle métier complet, ni politique d'identité, ni sémantique de contrôle d'accès ou règles de validation.

<a id="r-57"></a>
### R-57 — Ontologie bibliographique BIBO
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Spécification DCMI BIBO](https://www.dublincore.org/specifications/bibo/bibo/)
- **Concepts pertinents :** vocabulaire RDF pour ressources bibliographiques, citations et types de documents.
- **Utilité pour GovCheck :** vocabulaire complémentaire envisagé pour rapports, articles et objets bibliographiques dans l'étude d'intégration.
- **Limite :** BIBO est une spécification communautaire DCMI, pas une recommandation ISO ou W3C ; ne la combiner avec des vocabulaires généraux que si nécessaire.

<a id="r-58"></a>
### R-58 — Vocabulaire de catalogue de données (DCAT) 3
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Recommandation W3C DCAT 3](https://www.w3.org/TR/vocab-dcat-3/)
- **Concepts pertinents :** descriptions interopérables de jeux de données, services de données, distributions et séries de jeux de données dans des catalogues.
- **Utilité pour GovCheck :** vocabulaire candidat pour cataloguer bundles et collections de connaissances dans l'étude d'intégration.
- **Limite :** DCAT décrit des jeux de données/services catalogués ; il ne modélise ni toutes les sémantiques du contenu, ni permissions applicatives, ni édition collaborative.

<a id="r-59"></a>
### R-59 — Modèle de données W3C Web Annotation
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/)
- **Concepts pertinents :** annotations, corps, cibles, sélecteurs et motivations pour annoter une ressource ou un fragment précis.
- **Utilité pour GovCheck :** modèle candidat pour commentaires, questions et annotations attachés à des pages ou passages dans l'étude d'intégration.
- **Limite :** Web Annotation ne définit ni graphe de connaissances complet, ni protocole de coédition temps réel, ni politique d'autorisation.

<a id="r-60"></a>
### R-60 — ActivityStreams 2.0
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [W3C ActivityStreams 2.0 Core](https://www.w3.org/TR/activitystreams-core/)
- **Concepts pertinents :** vocabulaire et syntaxe JSON-LD pour acteurs, objets, activités, collections et interactions sociales.
- **Utilité pour GovCheck :** envisagé pour représenter des activités/événements publiés lorsque le cas d'usage social s'y prête.
- **Limite :** ActivityStreams n'est ni un registre de provenance, ni une garantie d'event sourcing, ni un modèle d'accès, ni un remplacement de PROV-O.

<a id="r-61"></a>
### R-61 — Ontologie P-Plan
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Source primaire :** [Spécification de l'ontologie P-Plan](https://www.opmw.org/model/p-plan/)
- **Concepts pertinents :** représentation de plans abstraits et correspondance avec les traces PROV-O des processus exécutés.
- **Utilité pour GovCheck :** vocabulaire candidat pour décrire des plans d'ingestion/transformation attendus à côté de la provenance observée.
- **Limite :** P-Plan est une ontologie de domaine étendant PROV-O, pas un moteur de workflow général ni une recommandation W3C.

<a id="r-62"></a>
### R-62 — Sources d'intégration Cartocortex, MoriNet et SaussuNet
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Dépôt Cartocortex](https://github.com/complexus-lab/cartocortex) · [Dépôt MoriNet](https://github.com/lejeunecedric/MoriNet) · [Dépôt SaussuNet](https://github.com/lejeunecedric/SaussuNet) · [PR Cartocortex #9 — panorama des formats de cartes mentales](https://github.com/complexus-lab/cartocortex/pull/9) · [PR Cartocortex #27 — étude OKF, stockage et vues graphe](https://github.com/complexus-lab/cartocortex/pull/27) · [PR Cartocortex #28 — backlog CRDT, navigateur et synchronisation cloud](https://github.com/complexus-lab/cartocortex/pull/28)
- **Concepts pertinents :** dépôts sources et artefacts d'étude examinés ; la PR #27 étudie le stockage/projection OKF v0.2, tandis que la PR #28 contient des propositions de travail CRDT et de transport temps réel.
- **Utilité pour GovCheck :** conserve les sources concrètes derrière le PDF initial « Évaluer l’intégration des dépôts » (6 novembre 2026, 224 pages) et la discussion enregistrée par l'ADR 0002.
- **Limite :** la PR #27 est une étude, pas une implémentation exécutée ; la PR #28 est une proposition/backlog et son étude de transport est explicitement non exécutée. Les capacités des dépôts doivent être revérifiées à la révision examinée avant toute affirmation sur leur comportement courant. Le namespace « CKO » du PDF est une proposition, pas une norme externe adoptée.

<a id="r-63"></a>
### R-63 — Formats d'échange de cartes mentales et de graphes
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Documentation Freeplane](https://docs.freeplane.org/) · [Projet FreeMind](https://freemind.sourceforge.io/wiki/index.php/Main_Page) · [XMind](https://xmind.app/) · [Spécification OPML 2.0](https://opml.org/spec2.opml) · [Spécification GraphML](http://graphml.graphdrawing.org/specification.html)
- **Concepts pertinents :** échange de cartes mentales hiérarchiques, plans et graphes généraux, avec métadonnées et dispositions propres aux formats.
- **Utilité pour GovCheck :** conserve les formats FreeMind, Freeplane, XMind, OPML et GraphML explicitement examinés pour l'import/export SaussuNet et la visualisation Cartocortex.
- **Limite :** ces formats ont des capacités expressives et conventions de métadonnées différentes. Un parsing réussi n'est pas une conversion sémantique sans perte ; il faut des fixtures par format et des rapports de perte explicites.

<a id="r-64"></a>
### R-64 — API de stockage cloud et interopérabilité S3
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Documentation et API Amazon S3](https://docs.aws.amazon.com/s3/) · [Interopérabilité Google Cloud Storage](https://docs.cloud.google.com/storage/docs/interoperability) · [Présentation de l'API Google Drive](https://developers.google.com/workspace/drive/api/guides/about-sdk) · [Ressource Drive Microsoft Graph](https://learn.microsoft.com/en-us/graph/api/drive-get?view=graph-rest-1.0) · [Introduction à Azure Blob Storage](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) · [Documentation Hippius](https://docs.hippius.com/) · [Stockage objet compatible S3 Hippius](https://docs.hippius.com/storage/s3/advanced)
- **Concepts pertinents :** API de stockage objet, points de terminaison compatibles S3, API de disques cloud, périmètres OAuth/identifiants, synchronisation côté client et sémantiques propres aux fournisseurs.
- **Utilité pour GovCheck :** conserve les candidats de stockage nommés dans la PR Cartocortex #28 : Amazon S3, interopérabilité Google Cloud Storage, Google Drive, OneDrive/Microsoft Graph, Azure Blob Storage et Hippius.
- **Limite :** « compatible S3 » ne signifie pas sémantiques, cohérence, IAM, versionnement, événements ou multipart identiques. Les API ont des modèles d'authentification et de permission distincts. Il s'agissait de candidats de backlog, pas de fournisseurs sélectionnés ou d'intégrations implémentées.

<a id="r-65"></a>
### R-65 — Accès aux fichiers du navigateur, persistance locale et WebAssembly
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [API File System MDN](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API) · [Origin Private File System (OPFS) MDN](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system) · [Indexed Database API 3.0 W3C](https://www.w3.org/TR/IndexedDB-3/) · [Spécifications WebAssembly](https://webassembly.org/specs/) · [WebAssembly System Interface (WASI)](https://github.com/WebAssembly/WASI)
- **Concepts pertinents :** accès aux fichiers/répertoires avec autorisation utilisateur, stockage navigateur privé à l'origine, persistance IndexedDB et interfaces d'exécution WebAssembly.
- **Utilité pour GovCheck :** conserve les candidats de déploiement et de persistance locaux au navigateur nommés dans la PR Cartocortex #28, notamment File System Access, OPFS, IndexedDB et l'usage conditionnel de WebAssembly/WASI pour réutiliser du code Rust.
- **Limite :** les API navigateur ont des contraintes de prise en charge, permission, contexte sécurisé et quota ; OPFS est privé à l'origine et n'est pas un répertoire visible de l'utilisateur. WASI est une interface système pour runtimes WebAssembly, pas un contournement des permissions du système de fichiers du navigateur. La PR décrit une proposition/backlog, pas un déploiement testé.

<a id="r-66"></a>
### R-66 — Découverte de pairs Hyperswarm et HyperDHT
- **Cité par :** aucune référence actuelle dans les documents de cette branche.

- **Sources primaires :** [Projet Hyperswarm](https://github.com/holepunchto/hyperswarm) · [Implémentation HyperDHT](https://github.com/holepunchto/hyperdht) · [Documentation de découverte de pairs Hyperswarm](https://docs.pears.com/p2p/reference/building-blocks/hyperswarm/)
- **Concepts pertinents :** découverte de pairs par sujets, rendez-vous via table de hachage distribuée, UDP hole punching et connexions chiffrées entre pairs.
- **Utilité pour GovCheck :** conserve l'alternative de découverte de pairs pour application desktop discutée dans la PR Cartocortex #28, à côté de la signalisation WebRTC dans les navigateurs.
- **Limite :** Hyperswarm/HyperDHT est une pile réseau distincte, pas une signalisation WebRTC native au navigateur. Le DHT dépend d'une infrastructure de bootstrap et de la joignabilité réseau ; la découverte de pairs ne définit ni autorisation des salles, ni politique de membres, ni persistance.

<a id="r-67"></a>
### R-67 — WebDAV, Model Context Protocol et conventions de wiki Markdown
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Sources primaires :** [RFC 4918 IETF — WebDAV](https://www.rfc-editor.org/rfc/rfc4918.html) · [Spécification MCP, version 2026-07-28](https://modelcontextprotocol.io/specification/2026-07-28/basic) · [Dépôt de la spécification MCP](https://github.com/modelcontextprotocol/modelcontextprotocol) · [Spécification CommonMark 0.31.2](https://spec.commonmark.org/0.31.2/) · [Documentation de syntaxe Markdown Obsidian](https://obsidian.md/help/syntax) · [Documentation mdBook](https://rust-lang.github.io/mdBook/)
- **Concepts pertinents :** édition distante et verrouillage via HTTP (WebDAV), outils/ressources/prompts via MCP, syntaxe Markdown, extensions propres à Obsidian et publication de bases de connaissances Markdown avec mdBook.
- **Utilité pour GovCheck :** conserve les protocoles externes et conventions documentaires explicitement nommés dans l'évaluation d'intégration pour l'ingestion de sources et l'exposition du wiki SaussuNet/MoriNet.
- **Limite :** WebDAV et MCP sont des protocoles distincts avec des modèles de sécurité et d'autorisation différents. CommonMark est une base, pas le dialecte Obsidian complet. Le PDF décrit des interfaces et une intégration visée ; il ne prouve pas que chaque adaptateur ou chemin serveur est implémenté ou sécurisé.

<a id="r-68"></a>
### R-68 — Dépôts de l'écosystème GovCheck associés et examinés dans l'évaluation
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Sources primaires :** [Pijulation](https://github.com/Martin-PB/Pijulation) · [Passerelle Git–Pijul](https://github.com/Martin-PB/passerelle-Git-Pijul)
- **Concepts pertinents :** projets adjacents servant de contexte pour les sémantiques natives Git/Pijul, l'interopérabilité des graphes de patches, la gouvernance et les pratiques d'assurance formelle.
- **Utilité pour GovCheck :** conserve les sources publiques de dépôts nommées dans l'évaluation initiale.
- **Limite :** l'évaluation examinait aussi des dépôts privés ; leurs noms et URL ne sont volontairement pas reproduits dans ce catalogue public. « Mix », « CCOp Agent » et un dépôt autonome distinct nommé « Nix » n'ont pas été identifiés de façon univoque ; aucun lien supposé n'est fourni. Cette entrée fournit du contexte, elle ne fait pas de ces projets des dépendances de GovCheck.

<a id="r-69"></a>
### R-69 — Inventaire des sources sur les formats de cartes mentales et l'interopérabilité (PR #9)
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Sources primaires du projet :** [PR Cartocortex #9 — panorama des formats de cartes mentales](https://github.com/complexus-lab/cartocortex/pull/9) · [PR Cartocortex #1](https://github.com/complexus-lab/cartocortex/pull/1) · [PR #3](https://github.com/complexus-lab/cartocortex/pull/3) · [PR #4](https://github.com/complexus-lab/cartocortex/pull/4) · [PR #5](https://github.com/complexus-lab/cartocortex/pull/5) · [PR #6](https://github.com/complexus-lab/cartocortex/pull/6) · [PR #8](https://github.com/complexus-lab/cartocortex/pull/8)
- **Implémentations sources et fixtures :** [Code source Freeplane](https://github.com/freeplane/freeplane) · [Sérialiseurs/importeur WiseMapping](https://github.com/wisemapping/wisemapping-frontend) · [Fixture publique de sauvegarde Mindomo](https://github.com/aarontmaher/Lauburu-Monorepo) · [MultiMarkdown 6](https://github.com/fletcher/MultiMarkdown-6) · [Fixture de test SimpleMind](https://github.com/pahund/simple-mind-search) · [Exporteur xmind2smmx](https://github.com/BartRuSec/xmind2smmx) · [Lecteur/écrivain MCP SimpleMind](https://github.com/kharabiner/simplemind-mcp-server)
- **Documentation des éditeurs et produits :** [Guide d'export XMind](https://xmind.com/fr/user-guide/export-new) · [Guide utilisateur MindManager 2017](https://www.mindmanager.com/static/mm/docs/MindManager_2017_User_Guide_EN.pdf) · [Intégrations Microsoft MindManager](https://www.mindmanager.com/en/integrations/microsoft/) · [Démarrage Mindomo](https://help.mindomo.com/getting-started/) · [Import Mindomo](https://help.mindomo.com/basics/import-mind-maps/) · [Export Mindomo](https://help.mindomo.com/basics/export-mind-maps/) · [FAQ compatibilité iThoughts de l'éditeur](https://www.toketaware.com/ithoughts-faq-compatibility) · [Export SimpleMind](https://simplemind.eu/faq/share-export-in-different-formats/) · [Fichiers importables SimpleMind](https://simplemind.eu/faq/what-files-can-simplemind-import/) · [Aide import/export SimpleMind](https://simplemind.eu/faq_group/share-export-and-import/) · [Export MindMeister](https://support.mindmeister.com/hc/en-us/articles/360017447280-Export-Your-Mind-Map) · [Export/Impression MindMeister iOS](https://support.mindmeister.com/hc/en-us/articles/115000807204-Export-or-Print-your-Map-on-iOS) · [Import MindMeister](https://support.mindmeister.com/hc/en-us/articles/360017498199-Import-Text-Files-and-Mind-Maps-into-MindMeister) · [Import Coggle](https://coggle.help/article/34-import-files-into-coggle) · [Article du blog Coggle sur l'import .mm](https://bloggle.coggle.it/post/129486892657/import-other-files-to-coggle) · [Export Coggle](https://coggle.help/article/20-export-options) · [Formats d'export pris en charge par Coggle](https://coggle.help/article/105-supported-export-formats) · [Aide Bubbl.us](https://bubbl.us/help/topics.htm) · [Import iMindMap vers Ayoa](https://support.ayoa.com/opening-imindmap-files-in-ayoa)
- **Références secondaires et non normatives :** [Aide export XMind non vérifiée comme source éditeur](https://xmind-help.github.io/en/export.html) · [FileInfo .mind](https://fileinfo.com/extension/mind) · [FileInfo .imx](https://fileinfo.com/extension/imx) · [File-Extensions .nm5](https://www.file-extensions.org/nm5-file-extension) · [Comparatif d'import/export Mind Mapping Software](https://mindmappingsoftwareblog.com/wp-content/99nc2r/MMS_Import_Export_Comparison.pdf) · [Demande d'export Lucidchart sur le forum communautaire](https://community.lucid.co/ideas/exporting-mind-maps-created-in-lucidchart-to-microsoft-powerpoint-or-word-374) · [Panorama d'export Lucidchart](https://mindmap.guide/post/7-amazing-enterprise-mindmap-tools-with-powerful-export-options/) · [Article sur l'export de tâches MindManager](https://sociamind.com/2015/11/04/exporting-a-simple-task-table-or-to-do-list-from-mindmanager/) · [Présentation de fonctionnalités Bubbl.us](https://edrawmind.wondershare.com/mind-map/bubble-us-mind-map.html)
- **Concepts pertinents :** capacités d'import/export, conteneurs de fichiers, contenu sémantique des cartes, structures d'outline et de graphe, intégrations bureautiques, sérialiseurs au niveau source et fixtures de fichiers réels.
- **Utilité pour GovCheck :** conserve la chaîne complète des sources derrière le panorama des formats cité par l'évaluation initiale de 224 pages, y compris code/fixtures et documentation officielle des éditeurs.
- **Limite :** la PR #9 est une PR documentaire ouverte, pas une implémentation de formats ni une suite de conformité. Le panorama enregistre les preuves disponibles à sa date de revue (2026-10-18). FileInfo, blogs et forums communautaires sont des sources secondaires, pas des spécifications de formats. Une fonctionnalité dans l'interface d'un produit ne prouve pas un échange de fichiers sans perte ; la PR source et les fixtures de chaque format doivent être revérifiées avant toute décision d'implémentation.

<a id="r-70"></a>
### R-70 — Wei et al., « ACCESS: Assurance Case Centric Engineering of Safety-critical Systems » (2024)
- **Cité par :** citation proposée dans [PR #22 — Architecture 0025](https://github.com/Martin-PB/govcheck/pull/22) (document absent de cette branche).
- **Source primaire :** [Article du Journal of Systems and Software](https://doi.org/10.1016/j.jss.2024.112034) · [copie en accès ouvert](https://eprints.whiterose.ac.uk/id/eprint/211554/)
- **Référence bibliographique :** Ran Wei, Simon Foster, Haitao Mei, Fang Yan, Ruizhe Yang, Ibrahim Habli, Colin O’Halloran, Nick Tudor, Tim Kelly et Yakoub Nemouchi, *Journal of Systems and Software* 213 (2024), article 112034.
- **Concepts pertinents :** dossiers d'assurance fondés sur des modèles SACM ; traçabilité vers des artefacts d'ingénierie hétérogènes ; évaluation automatisée, analyse d'impact des changements, preuves de méthodes formelles et évaluation dynamique du dossier d'assurance en production.
- **Utilité pour GovCheck :** démontre une approche étayée par la recherche pour faire évoluer les dossiers d'assurance avec les artefacts d'ingénierie et évaluer leur validité à partir de données d'exécution.
- **Limite :** l'article présente une méthodologie, un prototype et une étude de cas, pas un moteur générique de gouvernance des risques de sécurité prêt pour la production. Il ne faut pas exagérer la portée ni la maturité de ses outils.

<a id="r-71"></a>
### R-71 — Bloomfield et Rushby, « Assurance 2.0: A Manifesto » (2021)
- **Cité par :** citation proposée dans [PR #22 — Architecture 0025](https://github.com/Martin-PB/govcheck/pull/22) (document absent de cette branche).
- **Source primaire :** [Page des auteurs chez SRI et article](https://www.csl.sri.com/users/rushby/abstracts/sss21) · [manuscrit arXiv](https://arxiv.org/abs/2004.10474)
- **Référence bibliographique :** Robin Bloomfield et John Rushby, *Systems and Covid-19: Proceedings of the 29th Safety-Critical Systems Symposium*, 2021, p. 85–108.
- **Concepts pertinents :** examen renforcé du raisonnement et des preuves ; explicitation des éléments réfutants (*defeaters*) et contre-preuves ; évaluation du poids des preuves et de leur capacité à distinguer une affirmation de sa négation.
- **Utilité pour GovCheck :** motive la représentation explicite des contre-affirmations, éléments réfutants, observations contradictoires et évaluations de qualité/force des preuves, plutôt qu'un graphe unilatéral de soutien.
- **Limite :** Assurance 2.0 est une approche/manifeste d'assurance, pas un schéma complet d'événements opérationnels, un modèle d'autorité d'acceptation du risque ou une méthode universelle de score numérique.

<a id="r-72"></a>
### R-72 — Ericsson, « Runtime threat modeling for attack prediction and defense » (2025)
- **Cité par :** citation proposée dans [PR #22 — Architecture 0025](https://github.com/Martin-PB/govcheck/pull/22) (document absent de cette branche).
- **Source primaire :** [Article d'ingénierie Ericsson](https://www.ericsson.com/en/blog/2025/12/runtime-threat-modeling-for-attack-prediction-and-defense)
- **Concepts pertinents :** combinaison de télémétrie, état de configuration et changements d'actifs/contexte avec les connaissances sur les menaces ; hypothèses de menace issues des observations ; évaluation de l'efficacité des contrôles et boucles de retour.
- **Utilité pour GovCheck :** exemple industriel reliant l'observabilité en production à l'évolution du modèle de menace et à l'évaluation des contrôles.
- **Limite :** il s'agit d'un article industriel centré sur les réseaux d'accès radio, pas d'une norme neutre ni d'une preuve que les scores prédictifs sont étalonnés. GovCheck doit préserver provenance, incertitude et décisions humaines gouvernées plutôt que reprendre ses hypothèses de scoring/automatisation.

<a id="r-73"></a>
### R-73 — OMG Structured Assurance Case Metamodel (SACM), version 2.4 Beta 1 (septembre 2026)
- **Cité par :** citation proposée dans [PR #22 — Architecture 0025](https://github.com/Martin-PB/govcheck/pull/22) (document absent de cette branche).
- **Source primaire :** [État de la spécification SACM et documents de la bêta 2.4 chez OMG](https://www.omg.org/spec/SACM)
- **Concepts pertinents :** extensions proposées à SACM 2.3, notamment valeurs structurées/forces typées, constructions liées à l'évaluation, jointures, références à un concept entier, marquage de l'état de développement et révision de la sémantique des packages/relations.
- **Utilité pour GovCheck :** point de comparaison indispensable avant de sélectionner un métamodèle interne ou d'échange. Les résolutions de tickets de la bêta indiquent quelles lacunes de 2.3 la révision tente de combler.
- **Limite :** la version 2.4 est une bêta, pas une spécification formelle adoptée. GovCheck ne doit pas traiter ses constructions provisoires comme des contrats stables ni revendiquer sa conformité. Conserver 2.3 comme base formelle actuelle en attendant l'examen de la version finale 2.4.

<a id="r-74"></a>
### R-74 — Hoover, Rosso-Llopart et Taran, *Evaluating Project Decisions: Case Studies in Software Engineering* (2009/2010)
- **Cité par :** citation proposée dans [PR #22 — Architecture 0025](https://github.com/Martin-PB/govcheck/pull/22) (document absent de cette branche).
- **Source primaire :** [Catalogue de l'éditeur et extrait du chapitre](https://www.informit.com/store/evaluating-project-decisions-case-studies-in-software-9780321544568)
- **Référence bibliographique :** Carol L. Hoover, Mel Rosso-Llopart et Gil Taran, Addison-Wesley Professional, première publication en octobre 2009 (copyright 2010), ISBN 978-0-321-54456-8 ; le chapitre 1, §1.3 présente le modèle de décision PEAK.
- **Concepts pertinents :** Problem, Experience, Assumptions et Knowledge comme entrées de la décision ; un processus de décision produit une solution et un risque assumé.
- **Utilité pour GovCheck :** fournit une grille d'examen des décisions pour rendre explicites et traçables la formulation du problème, l'expérience mobilisée, les hypothèses, les connaissances factuelles, la solution retenue et le risque accepté.
- **Limite :** PEAK est un modèle de décision, pas une taxonomie des menaces, un métamodèle de dossier d'assurance, un algorithme de calcul du risque ou une norme de gouvernance. Il ne prescrit ni sérialisation ni modèle d'autorisation.

<a id="r-75"></a>
### R-75 — NIST SP 800-137, Information Security Continuous Monitoring (2011)
- **Cité par :** citation proposée dans [PR #22 — Architecture 0025](https://github.com/Martin-PB/govcheck/pull/22) (document absent de cette branche).
- **Source primaire :** [Publication NIST](https://csrc.nist.gov/pubs/sp/800/137/final) · [DOI](https://doi.org/10.6028/NIST.SP.800-137)
- **Concepts pertinents :** visibilité continue sur les actifs, menaces, vulnérabilités et efficacité des contrôles déployés ; surveillance alignée sur la tolérance au risque ; réaction lorsque les observations montrent que les contrôles sont insuffisants.
- **Utilité pour GovCheck :** étaye une boucle de retour en production dans laquelle les observations actualisent l'état du système, l'évaluation des contrôles et les décisions de risque, au lieu de figer le modèle de menace à la conception.
- **Limite :** les données de surveillance ne constituent pas automatiquement un incident validé, une menace ou une conclusion d'assurance. Couverture, intégrité de collecte, contexte, incertitude et santé des mécanismes de surveillance doivent être évalués.

<a id="r-76"></a>
### R-76 — Rushby, « Runtime Certification » (RV 2008)
- **Cité par :** citation proposée dans [PR #22 — Architecture 0025](https://github.com/Martin-PB/govcheck/pull/22) (document absent de cette branche).
- **Source primaire :** [Article de l'auteur, présenté au huitième atelier Runtime Verification](https://citeseerx.ist.psu.edu/document?doi=c28045b0a573839028f6042870a3eccd8f9be748&repid=rep1&type=pdf)
- **Référence bibliographique :** John Rushby, « Runtime Certification », article invité à RV 2008, Budapest, avril 2008.
- **Concepts pertinents :** dossiers d'assurance comme affirmations, preuves et arguments ; surveillance en exécution des hypothèses et anomalies ; utilisation de la vérification à l'exécution comme preuve ; détection de la violation d'hypothèses environnementales.
- **Utilité pour GovCheck :** justifie directement de relier les hypothèses déclarées à des conditions surveillables et de permettre aux observations de production de les contester et de déclencher la réévaluation des affirmations d'assurance.
- **Limite :** les moniteurs à l'exécution n'établissent que des propriétés dans leur périmètre formalisé et leur frontière d'observation. Une anomalie ou une hypothèse violée ne constitue pas automatiquement une attaque confirmée ni une preuve de défaillance du système.

<a id="r-77"></a>
### R-77 — Exemples d'application de politiques et de gouvernance des outils MCP
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Sources primaires :** [Documentation HashiCorp Sentinel](https://developer.hashicorp.com/sentinel/docs) · [Documentation Consul MCP Gateway](https://docs.hashicorp.com/consul/docs/agentic-mesh/mcp-gateway) · [Gouvernance des outils agents et blocage des serveurs MCP GitLab](https://docs.gitlab.com/user/ai-governance/tool-governance/) · [Dépôt source Vectimus](https://github.com/vectimus/vectimus)
- **Concepts pertinents :** politiques-as-code, évaluation des politiques aux frontières infrastructure et outils d'agents, autorisation/blocage de serveurs MCP, gouvernance par namespace, preuves d'approbation, événements d'audit et hooks Cedar déterministes.
- **Utilité pour GovCheck :** conserve les systèmes d'application de politiques et de gouvernance MCP comparés dans les discussions élargies du projet, aux côtés d'OPA (R-09) et Cedar (R-10).
- **Limite :** Sentinel est une fonctionnalité HashiCorp Enterprise ; la documentation Consul MCP Gateway indique un statut bêta. Le périmètre de blocage GitLab dépend du produit, de la version et de la surface. Les affirmations de sécurité et de performance de Vectimus ne sont pas établies indépendamment par son README. Ces exemples n'impliquent ni sélection, ni équivalence, ni intégration à GovCheck.

<a id="r-78"></a>
### R-78 — NIST OSCAL et Continuous Compliance Framework (CCF)
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Sources primaires :** [Projet NIST OSCAL](https://pages.nist.gov/OSCAL/) · [Dépôt source OSCAL](https://github.com/usnistgov/OSCAL) · [Documentation Compliance Framework / CCF](https://compliance-framework.github.io/docs/introduction) · [Dépôts Compliance Framework](https://github.com/compliance-framework)
- **Concepts pertinents :** catalogues de contrôles de sécurité lisibles par machine, profils, plans de sécurité système, plans/résultats d'évaluation et preuves structurées en XML, JSON et YAML ; collecte continue de preuves et reporting.
- **Utilité pour GovCheck :** conserve les options OSCAL et CCF discutées pour représenter les contrôles, collecter des preuves et produire des résultats d'évaluation structurés.
- **Limite :** OSCAL est un ensemble de modèles/formats d'information, pas un moteur complet de conformité ni une preuve d'efficacité des contrôles. CCF est une implémentation distincte qui utilise des moteurs de politiques et des collecteurs ; ses affirmations ne constituent ni une norme normative ni une certification indépendante. Un mapping GovCheck exigerait sémantique explicite des contrôles, provenance des preuves et périmètre.

<a id="r-79"></a>
### R-79 — Sandboxing et isolation à l'exécution des agents : nono, Landlock et Docker Sandboxes
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Sources primaires :** [Projet nono et modèle de sécurité](https://github.com/nolabs-ai/nono) · [Site de documentation nono](https://nono.sh/) · [Documentation noyau Linux Landlock](https://docs.kernel.org/userspace-api/landlock.html) · [Documentation Docker Sandboxes](https://docs.docker.com/ai/sandboxes/) · [Projet d'agent IA Goose](https://github.com/aaif-goose/goose)
- **Concepts pertinents :** portée de capacités par outil, restrictions de système de fichiers/réseau, courtage d'identifiants, sandboxing non privilégié imposé par le noyau, isolation microVM et orchestration de runtimes d'agents.
- **Utilité pour GovCheck :** conserve les options d'isolation à l'exécution et d'exécution d'agents discutées dans le contexte élargi de l'architecture sécurité/GovCheck. Goose est inclus comme exemple de harness d'agent, pas comme sandbox.
- **Limite :** le support Landlock et les restrictions disponibles dépendent de la configuration du noyau et de l'ABI ; c'est une couche, pas une frontière VM/conteneur complète. nono et Docker Sandboxes ont leurs propres hypothèses de confiance, politiques et exploitation ; les affirmations des projets/fournisseurs exigent des tests indépendants. Goose est un runtime d'agent, pas une autorité d'autorisation.

<a id="r-80"></a>
### R-80 — Protocole Matrix et client Element X
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Sources primaires :** [Spécification du protocole Matrix](https://spec.matrix.org/latest/) · [Dépôt source de la spécification Matrix](https://github.com/matrix-org/matrix-spec) · [Element X dans l'écosystème Matrix.org](https://matrix.org/ecosystem/clients/element-x/)
- **Concepts pertinents :** communication temps réel fédérée, homeservers, salons, synchronisation d'événements, chiffrement de bout en bout et comportement du client mobile Matrix.
- **Utilité pour GovCheck :** conserve l'option de communication Matrix/Element X discutée pour la collaboration entre agents et humains.
- **Limite :** Matrix est un protocole et un écosystème de communication, pas un modèle de gouvernance ou d'autorisation GovCheck. L'appartenance à un salon et le chiffrement n'établissent pas à eux seuls une politique au niveau projet, le lien d'identité d'agent ou la provenance durable des décisions.

<a id="r-81"></a>
### R-81 — Métamoteur SearXNG
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Source primaire :** [Documentation SearXNG](https://docs.searxng.org/)
- **Concepts pertinents :** agrégation de métamoteur auto-hébergé, moteurs de recherche amont configurables, traitement des requêtes orienté confidentialité et administration.
- **Utilité pour GovCheck :** conserve le service de recherche auto-hébergé discuté comme composant de découverte de sources dans le contexte élargi du projet.
- **Limite :** SearXNG agrège des résultats de moteurs tiers ; il ne valide ni autorité, ni fraîcheur, ni exactitude, ni licence des sources. Les résultats doivent être résolus et vérifiés auprès de sources primaires.

<a id="r-82"></a>
### R-82 — Conversion de documents vers Markdown avec Microsoft MarkItDown
- **Cité par :** [0002](decisions/0002-study-placement.fr.md)
- **Source primaire :** [Dépôt source et documentation Microsoft MarkItDown](https://github.com/microsoft/markitdown)
- **Concepts pertinents :** conversion de PDF, documents Office et autres formats vers Markdown pour indexation et analyse textuelle.
- **Utilité pour GovCheck :** conserve l'utilitaire d'ingestion documentaire discuté pour extraire et examiner des sources telles que PDF et documents bureautiques.
- **Limite :** MarkItDown effectue les E/S avec les privilèges du processus courant. Sa documentation avertit que les entrées non fiables doivent être assainies et que la conversion doit s'exécuter avec les accès les plus restreints nécessaires. La sortie convertie est une extraction, pas une preuve d'exhaustivité ou de fidélité sémantique.


## Discipline bibliographique et provenance non résolue

1. Privilégier l'organisme normatif, l'éditeur, la documentation officielle ou le dépôt source plutôt que les résumés secondaires.
2. L'identifiant R-12 a été retiré lors de la consolidation de son entrée Scorecard en doublon dans R-08 ; ne pas réutiliser cet identifiant retiré.
3. Épingler les analyses de code. Les liens Writ et Privateer identifient les révisions examinées dans l'architecture 0016 ; les actualiser avant toute affirmation sur leur comportement courant.
4. Distinguer les classes de preuve. Une norme, un article scientifique, une documentation produit, du code source, un résultat de test et un rapport de model checking sont des types de preuve différents.
5. Aucune adoption implicite. La présence dans ce registre signifie « pertinent à évaluer », pas « sélectionné », « obligatoire », « compatible » ou « implémenté ».
6. Pas de bibliographie inventée. La discussion précédente mentionnait « Agent Package Manager », mais n'a pas conservé d'URL unique et vérifiée du projet. Il n'est volontairement pas cité comme produit identifié avant établissement de son identité exacte.
7. Garder les liens près des affirmations. Les documents d'architecture doivent lier les sources qui étayent directement leurs affirmations et renvoyer ici pour la bibliographie plus large.
