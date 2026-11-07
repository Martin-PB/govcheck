# 0018 — Gouvernance des versions, compatibilité et autorité d'approbation

**Statut :** proposition de gouvernance soumise à la revue des mainteneurs et de l'autorité de gouvernance. Ce document ne désigne pas une autorité absente du modèle canonique, n'adopte pas le document 0017 et ne prétend pas que les contrôles existent déjà.  
**Langue :** l'anglais est la langue par défaut ; voir la [version anglaise](0018-version-governance-and-compatibility-authority.md).

## 1. Objet et relation avec le document 0017

Le document 0017 classe les catégories d'artefacts et définit les cas où MAJOR, MINOR et PATCH ont un sens. Le présent document définit le processus de gouvernance permettant de proposer, évaluer, autoriser et publier ces décisions, y compris l'impact des dépendances et la fraîcheur des preuves. Il opérationnalise le document 0017 sans le remplacer.

Six identités doivent rester distinctes :

- **Révision :** état source exact et immuable.
- **Version de contrat :** promesse de compatibilité faite à des consommateurs déclarés.
- **Version de schéma :** structure et sémantique d'un format d'enregistrement sérialisé.
- **Révision de catalogue :** révision du registre lui-même.
- **Identité de release :** publication liée aux identités exactes des sources et du manifeste.
- **Identité d'instance :** exécution, observation, approbation ou décision particulière.

Aucun de ces nombres ne mesure la maturité, l'assurance, l'approbation ou la correction. Tant qu'ils ne sont pas adoptés selon le processus canonique de gouvernance, les documents 0017 et 0018 restent des propositions. La fusion d'une documentation ne lui confère pas à elle seule une force normative, sauf disposition explicite du modèle canonique et enregistrement de la décision.

## 2. Modèle d'autorité

### 2.1 Trois responsabilités distinctes

1. **Proposant :** identifie l'artefact et le contrat, suggère une classification et fournit le dossier de changement.
2. **Évaluateur de compatibilité :** examine l'impact sur les consommateurs, les différences d'obligations/garanties, les dépendances et la fraîcheur des preuves. Les contrôles automatisés apportent des éléments, pas une autorité sémantique.
3. **Autorité d'approbation :** approuve l'évolution du contrat et sa version publiée selon les règles d'autorité et de délégation du modèle canonique.

Une personne ne peut cumuler plusieurs rôles que si la gouvernance canonique l'autorise. Lorsqu'une revue indépendante est requise, le proposant ne peut pas être l'unique approbateur.

### 2.2 L'autorité dépend du sujet gouverné

| Sujet | Source d'autorité |
|---|---|
| Modèle canonique, règles fondatrices, métamodèle de gouvernance | Autorité désignée par le modèle canonique |
| Paquet de règles ou profil de dépôt | Autorité explicitement déléguée pour ce paquet/profil et son périmètre |
| Schéma public, API, CLI ou protocole | Responsable/mainteneur désigné de l'interface, sous réserve des contraintes supérieures |
| Contrat de modèle/propriété formelle | Autorité du domaine responsable ; les affirmations normatives exigent aussi l'autorité de gouvernance concernée |
| Contrat de release d'un outil/produit | Autorité de publication du produit/dépôt, sans pouvoir sur des contrats normatifs sans rapport |
| Preuve, exécution, approbation ou attestation | Autorité de l'émetteur/de l'approbateur de l'événement ; aucune autorité SemVer n'en découle |

Si le modèle canonique ne désigne pas l'autorité responsable ou sa délégation, l'autorisation est **bloquée**. Un mainteneur peut préparer la proposition, mais ne doit pas combler cette lacune en s'attribuant une autorité normative. L'autorité est délimitée : approuver un paquet, profil, interface ou release n'autorise pas les autres.

Une autorisation lie au minimum l'identité et le fondement de l'autorité, le périmètre, la révision candidate exacte, les versions antérieure et proposée, la décision, sa justification, sa date et sa provenance. Un incrément de version enregistre une décision de compatibilité autorisée ; il n'autorise pas à lui seul le changement sous-jacent.

## 3. Procédure de décision de version

Pour toute modification d'un artefact déclarant une version de contrat :

1. Résoudre l'identité stable de l'artefact, l'identifiant du contrat et la révision/version antérieure exacte.
2. Épingler la révision candidate par identité VCS native et empreinte de contenu si disponible.
3. Identifier le contrat publié, les consommateurs déclarés et le sens de compatibilité.
4. Décrire les changements observables du contrat, pas seulement les différences de fichiers.
5. Comparer les obligations, garanties, entrées/sorties, erreurs, sémantiques et usages pris en charge pertinents.
6. Énumérer les dépendances et les affirmations, tests, preuves, rapports, approbations et releases en aval.
7. Classer selon le document 0017 ; consigner contre-exemples et incertitudes.
8. Obtenir l'évaluation indépendante et l'autorisation requises.
9. Publier une version de contrat immuable liée à la révision exacte/au manifeste de release.
10. Enregistrer migration, dépréciation, support et revalidation des preuves.

Si la compatibilité ne peut pas être établie, le résultat est **indéterminé**, et non PATCH par défaut. Enregistrer une révision ordinaire sans inventer d'incrément de contrat, ou bloquer la publication jusqu'à résolution par revue.

## 4. Décisions de compatibilité

La classification se rapporte au contrat antérieur approuvé et publié, à ses consommateurs déclarés et à ses garanties, et non à la taille apparente du diff.

| Décision | Constat requis | Conséquence |
|---|---|---|
| MAJOR | Un consommateur auparavant conforme doit changer, réévaluer ou migrer ; ou un comportement, une obligation ou une garantie promise est substantiellement modifié/retiré | Plan de migration/dépréciation ; revue des consommateurs et preuves affectés |
| MINOR | Une nouvelle capacité est compatible avec tous les consommateurs existants déclarés et préserve les garanties antérieures | Les consommateurs existants restent valides ; adoption facultative ou périmètre sûr |
| PATCH | Le sens approuvé ne change pas ; un défaut d'implémentation/de représentation est corrigé sans modifier les obligations ni les garanties sur lesquelles les consommateurs s'appuient | Nouvelle révision ; mise à jour des preuves concernées ; aucune migration implicite |
| Aucun incrément de contrat | Aucun changement du contrat : éditorial, métadonnées, projection régénérée ou implémentation hors contrat | Révision ordinaire ; ne pas fabriquer de SemVer |
| Indéterminé / bloqué | Éléments insuffisants/contradictoires ou analyse non prise en charge | Aucune affirmation de compatibilité ; revue humaine compétente |

La publication initiale est un événement d'autorisation distinct, et non un incrément MAJOR/MINOR/PATCH : elle établit la première version de référence approuvée du contrat lorsque les conditions du §2.2 du document 0017 sont satisfaites. Il n'existe alors aucun contrat publié antérieur à comparer, mais l'autorité désignée reste requise. Une décision concluant à l'absence de changement de contrat n'enregistre aucune nouvelle version. Aucun de ces cas ne doit être présenté silencieusement comme un PATCH.

Une correction qui change le sens effectivement reçu par les consommateurs n'est pas automatiquement PATCH parce qu'elle est appelée correction de bug. Une correction de sécurité n'est PATCH que si elle préserve le contrat et ses garanties. Un champ facultatif n'est pas automatiquement MINOR : le comportement face aux champs inconnus doit faire partie du contrat. L'affaiblissement d'une garantie de sécurité ou d'assurance peut être MAJOR même s'il facilite la conformité. Un numéro de version ne légitime pas rétroactivement une modification normative non autorisée.

## 5. Dépendances et fraîcheur des preuves

Compatibilité et fraîcheur des preuves sont deux axes distincts. Un PATCH peut invalider des preuves ; une évolution MAJOR n'invalide pas nécessairement tous les enregistrements historiques.

Utiliser des relations typées, orientées et liées à des révisions :

- **depends-on :** entrée sémantique/structurelle requise ;
- **conforms-to :** conformité revendiquée à un contrat ;
- **refines :** spécialisation ou implémentation d'un contrat abstrait ;
- **derived-from :** génération/dérivation depuis une révision source ;
- **verifies / tests :** une méthode évalue un sujet ou une propriété ;
- **supports / refutes :** une preuve étaye ou réfute une affirmation ;
- **supersedes :** un successeur autorisé remplace un artefact/une décision ;
- **published-with :** artefact inclus dans une release précise.

Chaque dépendance doit identifier la révision/version de contrat amont exacte, et non un simple chemin ou la dernière version. Évaluer les dépendants selon l'un des états suivants :

- **non affecté :** l'analyse établit l'absence de changement pertinent ;
- **revue requise :** impact sémantique inconnu ou jugement métier nécessaire ;
- **obsolète/invalide :** entrée, hypothèse, sujet ou garantie requis modifié ;
- **remplacé :** successeur autorisé ;
- **révoqué :** retrait autorisé d'une approbation, attestation ou déclaration liée à une clé.

Conserver les preuves historiques. Une preuve invalidée reste auditable mais ne peut soutenir une acceptation courante avant revalidation. Un commit Git modifié n'invalide pas à lui seul tous les artefacts ; une SemVer inchangée ne préserve pas à elle seule la validité des preuves.

## 6. Interprétation des champs existants ressemblant à des versions

Le dépôt contient des champs nommés catalogueVersion et schemaVersion. Leur nom ne les transforme pas en SemVer.

| Champ | Interprétation visée | Ne signifie pas |
|---|---|---|
| formal/artifacts.json : catalogueVersion | Marqueur de révision du format du catalogue/registre ; actuellement 1 | Version de chaque artefact, numéro de release ou révision Git |
| formal/lifecycle-transitions.json : schemaVersion | Version de la structure sérialisée du registre de transitions et de son interprétation machine | Version du modèle TLA+, du contrat de cycle de vie ou release des transitions |
| release-manifest.schema.json : schemaVersion | Version du contrat de sérialisation du manifeste de release | Version du produit GovCheck ou d'une instance de manifeste |
| Tag Git et commit de release | Identité de release liée à un commit exact (et au manifeste s'il est publié) | Identité ou version de contrat propre à chaque artefact |
| Commit Git et empreinte de contenu | Identité immuable d'une source/révision | Déclaration de compatibilité sémantique |

La valeur actuelle 1 est un marqueur de format, pas la preuve qu'une politique SemVer a été appliquée. Ne pas renommer ni incrémenter ces champs pour une cohérence cosmétique. Avant toute modification, définir contrat, consommateurs, migration et autorité. Une évolution de format de schéma et une évolution sémantique du modèle peuvent exiger des décisions distinctes.

Ce document ne déclare aucun contractVersion pour le modèle de cycle de vie ou une entrée du catalogue. Ne pas en ajouter avant de satisfaire aux exigences du §2.2 du document 0017.

## 7. Enregistrement minimal d'une décision de version

Chaque décision doit être un événement immuable contenant : identifiant/date ; identifiants d'artefact et de contrat ; identités/empreintes des révisions antérieure et candidate ; version antérieure/proposée ou absence explicite de version ; périmètre du contrat et catégories de consommateurs ; sens/classification de compatibilité ; garanties/obligations/comportements modifiés et justification ; impact des dépendances et preuves affectées ; plan de migration/dépréciation/support ; proposant, évaluateur(s), autorité et fondement ; résultat, conditions et provenance ; lien au tag/commit/manifeste de release le cas échéant.

Une correction crée un événement successeur ; elle n'écrase jamais la décision initiale.

## 8. Limites de l'automatisation

Un futur validateur pourra contrôler complétude structurelle, identifiants uniques, références de révision immuables, syntaxe des versions, dépendances, approbations et liens de manifeste. Il pourra comparer des schémas machine-readable et énumérer les dépendants déclarés.

Il ne doit pas déduire la compatibilité sémantique d'un diff textuel, de tests réussis, d'une étiquette de version ou d'un indicateur saisi manuellement. Sans relation de compatibilité formalisée, le résultat est « revue requise/indéterminé ». L'inconnu bloque l'autorisation et reste un état explicite ; il n'est ni un succès ni un échec technique masqué.

Ce document ne prétend pas que GovCheck implémente un moteur de décision, un graphe de dépendances, un moteur d'invalidation, un validateur de schémas ou un flux d'approbation.

## 9. Adoption et séquence d'implémentation

1. Désigner/confirmer les autorités et délégations dans le modèle canonique.
2. Examiner et adopter ensemble 0017 et 0018, en résolvant explicitement les conflits.
3. Approuver la sémantique des champs existants ; conserver leurs valeurs tant qu'aucun vrai changement de format n'intervient.
4. Définir un enregistrement machine-readable de décision de version et un vocabulaire de dépendances.
5. Étendre catalogue et manifeste dans un changement distinct et revu, avec traitement de compatibilité/migration.
6. Ajouter validateurs et tests négatifs pour autorité absente, compatibilité ambiguë, dépendance orpheline, preuve obsolète et lien de release mutable.
7. Migrer les enregistrements sans inventer de SemVer historique ni d'approbation rétroactive.

## 10. Contrats GovCheck associés et références

- [Architecture 0017 — Identité, révision et politique de versionnement](0017-artifact-identity-revision-and-versioning.fr.md).
- [Spécification 0002 — Modèle canonique de gouvernance](../specifications/0002-canonical-governance-model.fr.md).
- [Spécification 0003 — Cycle de vie et acceptation des changements](../specifications/0003-change-lifecycle.fr.md).
- [Spécification 0005 — Assurance, affirmations et preuves](../specifications/0005-assurance-model.fr.md).
- [Architecture 0012 — Autorité normative canonique](0012-normative-authority-and-documentation.fr.md).
- [Architecture 0013 — Métamodèle de gouvernance](0013-governance-metamodel.fr.md).
- [Semantic Versioning 2.0.0](https://semver.org/lang/fr/spec/v2.0.0.html) ; [W3C PROV-O]([R-24](../references.fr.md#r-24)) ; [DataCite — Versioning]([R-25](../references.fr.md#r-25)) ; [1EdTech Versioning Framework 1.0]([R-23](../references.fr.md#r-23)).

Ces références éclairent la conception ; les règles d'autorité et de compatibilité présentées ici sont des propositions propres à GovCheck, et non des exigences imposées par ces standards.

## Modèle machine-readable

Un premier brouillon non normatif des enregistrements machine-readable est maintenu dans [formal/schemas/README.md](../../formal/schemas/README.md). Il sépare les événements de décision de version des relations de dépendance liées à des révisions précises. Ces schémas restent des propositions : ils ne désignent pas l'autorité, ne prouvent pas la compatibilité et n'implémentent pas l'invalidation.


## Références bibliographiques

Références externes citées dans ce document : [R-14](../references.fr.md#r-14), [R-23](../references.fr.md#r-23), [R-24](../references.fr.md#r-24), [R-25](../references.fr.md#r-25).
