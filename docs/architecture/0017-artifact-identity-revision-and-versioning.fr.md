# 0017 — Identité, révision et politique de versionnement des artefacts

**Statut :** proposition de politique de gouvernance soumise à la revue des mainteneurs. Elle n'impose pas SemVer à tous les artefacts, ne choisit pas de sérialisation canonique et ne prétend pas que les contrôles de versionnement sont implémentés.  
**Langue :** l'anglais est la langue par défaut ; la version anglaise est [ici](0017-artifact-identity-revision-and-versioning.md).  
**Périmètre :** tous les artefacts et enregistrements gouvernés par GovCheck : artefacts normatifs, architecturaux, formels, d'implémentation, preuves, décisions et publications.

## 1. Objet et principe directeur

GovCheck doit distinguer trois questions souvent confondues :

1. **Identité :** de quel objet logique s'agit-il ?
2. **Identité de révision ou d'instance :** de quel état exact et immuable, ou de quelle occurrence, s'agit-il ?
3. **Version de compatibilité :** quelle promesse de compatibilité cet artefact publié fait-il, le cas échéant, à des consommateurs identifiés ?

Un numéro de version ne répond pas à ces trois questions. Un commit Git, une empreinte de contenu, un `artifactId` stable, une chaîne SemVer, un identifiant d'exécution et un enregistrement de provenance sont des identifiants complémentaires, pas des solutions concurrentes.

**SemVer est un vocabulaire de compatibilité, pas un système universel d'identité ni une mesure d'importance, de maturité, de correction ou d'approbation.** Il ne s'applique que lorsqu'un artefact expose un contrat déclaré à des consommateurs identifiables et que le projet peut définir la compatibilité ascendante de ce contrat. Lorsque ce test échoue, GovCheck doit utiliser une identité logique stable, des révisions/instances immuables et une provenance explicite, plutôt que d'inventer une sémantique MAJOR.MINOR.PATCH.

Ce document est une proposition de politique. Il ne rend pas à lui seul un contrat proposé obligatoire. Son adoption exige une décision de gouvernance prise par l'autorité habilitée et, le cas échéant, une mise à jour de l'autorité canonique de gouvernance.

## 2. Termes et axes d'identité distincts

| Terme | Signification | Représentation typique | Mutabilité |
|---|---|---|---|
| Identité logique d'artefact | Identité continue d'un artefact entre ses révisions et changements de chemin | `artifactId` stable | Stable ; jamais recyclée |
| Identité de révision | État exact du contenu d'un artefact logique | Commit/arbre Git, chemin et empreinte du contenu ; ou identité VCS native | Immuable après publication |
| Version de contrat | Étiquette de compatibilité d'un contrat public déclaré | SemVer `MAJOR.MINOR.PATCH`, uniquement si justifié | Immuable après publication |
| Identité de release | Une publication précise d'un dépôt/paquet | Tag de release, commit/arbre exact et manifeste | Immuable |
| Identité d'instance/événement | Une exécution, observation, approbation, décision ou autre occurrence | ID unique d'événement/exécution/enregistrement, date et lien au sujet | Immuable ; toute correction crée un nouvel événement |
| Provenance | Entités, activités, agents, entrées et dérivations à l'origine d'un artefact/résultat | Relations typées et métadonnées de preuve | Historique append-only ; corrections explicites |

Un artefact logique peut avoir de nombreuses révisions. Un contrat peut avoir plusieurs releases. Une release peut contenir de nombreux artefacts, chacun avec sa propre identité et sa propre révision. Une définition de test peut être versionnée tandis que chaque exécution de test constitue une instance distincte. Un objet de preuve peut être révisé alors que l'énoncé du théorème reste identique. Ces relations ne doivent pas être aplaties dans une seule chaîne de version.

### 2.1 Identifiants stables et révisions immuables

- Tout artefact logique gouverné devrait avoir un identifiant stable, indépendant du nom de fichier, du répertoire, de la branche, du tag ou de l'hébergeur.
- Un identifiant ne doit jamais être réutilisé pour un autre artefact logique. Retrait, remplacement, division ou fusion exigent des relations explicites telles que `supersedes`, `derived-from`, `split-from` ou `merged-from`.
- Toute révision publiée ou tout résultat publié doit être adressable par une identité native immuable et/ou une empreinte de contenu.
- Déplacer ou renommer un fichier ne crée pas, à lui seul, un nouvel artefact logique. Le catalogue est mis à jour dans le même changement et l'identifiant est conservé lorsque la continuité de sens est justifiée.
- Une division, une fusion ou un changement substantiel de sujet peut exiger de nouveaux identifiants logiques, même si le contenu est copié.
- L'historique Git enregistre les changements du dépôt ; un tag de release lie une publication à un commit/arbre exact. Pour Pijul, préserver les identités natives des patches/canaux/graphes au lieu de fabriquer des identifiants de type Git.
- Les empreintes établissent l'identité/intégrité du contenu selon l'algorithme choisi ; elles n'établissent ni équivalence sémantique, ni vérité, ni autorité, ni approbation.

### 2.2 La version de contrat est facultative

Une version de contrat ne doit être attribuée que si tous les éléments suivants sont déclarés :

1. le contrat public de l'artefact et son statut normatif ;
2. ses consommateurs visés et les usages pris en charge ;
3. les obligations, garanties, schémas, API ou sémantiques observables exposés à ces consommateurs ;
4. la relation de compatibilité ascendante et son sens ;
5. les règles d'obsolescence, de retrait, de migration et de support ;
6. l'autorité qui approuve les évolutions du contrat.

Si l'un de ces éléments est inconnu, utiliser une identité de révision et la provenance. Ne pas utiliser un numéro ressemblant à SemVer pour masquer l'absence de politique.

## 3. Le test de compatibilité

Pour un artefact doté d'un contrat déclaré, évaluer la compatibilité par rapport au **contrat publié antérieurement**, et non seulement au diff des fichiers ou à l'étiquette choisie par l'auteur.

Un nouveau contrat n'est rétrocompatible que si tout consommateur conforme à l'ancien contrat peut continuer à l'être sans modifier son usage existant, et si aucune garantie antérieure sur laquelle ces consommateurs s'appuient n'est silencieusement affaiblie. Le test exact doit être spécialisé selon la catégorie d'artefact.

La compatibilité est directionnelle et relative aux consommateurs. Un schéma peut rester syntaxiquement compatible tandis qu'une politique devient normativement incompatible. Un modèle peut préserver une API tout en ajoutant des comportements qui invalident un invariant de sûreté. GovCheck ne doit donc pas déduire la compatibilité d'une syntaxe additive, de noms de fichiers inchangés, de tests réussis ou de l'expression « correction de bug ».

### 3.1 Correspondance SemVer lorsque le test de compatibilité est satisfait

| Incrément | Signification | Interprétation GovCheck |
|---|---|---|
| MAJOR | Évolution du contrat non rétrocompatible | Au moins un consommateur auparavant conforme doit s'adapter, réévaluer ou migrer explicitement ; ou une garantie antérieure est retirée/modifiée |
| MINOR | Capacité ou ajout de contrat rétrocompatible | La nouvelle capacité est facultative/activable ou limitée de telle sorte que les anciens consommateurs et garanties restent valides |
| PATCH | Correction rétrocompatible | Corrige un défaut d'implémentation ou de représentation sans changer le sens voulu du contrat approuvé ni invalider les usages conformes antérieurs |
| Aucun incrément SemVer | Aucun changement de contrat | Évolution éditoriale/explicative, projection régénérée, correction de métadonnées ou révision source sans modification du contrat déclaré ; enregistrer normalement la révision |

Pour un contrat SemVer stable (MAJOR supérieur à zéro), une version publiée doit être immuable. Une version publiée ne doit jamais être écrasée. Une version antérieure à 1.0 peut déclarer une stabilité plus faible, mais `0.y.z` ne doit pas servir de compteur de révisions d'artefact ni éviter de documenter les attentes de compatibilité.

Un « patch » n'est pas synonyme de « petit », « urgent », « correction de bug » ou « éditorial ». Une correction qui modifie le contrat effectivement consommé par les utilisateurs est MAJOR, même si le texte précédent était erroné. Une correction ne peut être PATCH que si la sémantique approuvée attendue était déjà dépourvue d'ambiguïté et que la correction rétablit ce sens sans modifier les obligations des consommateurs ni les garanties sur lesquelles ils s'appuient.

### 3.2 Deux dimensions de compatibilité pour les contrats de gouvernance

Les paquets et profils normatifs exigent deux vérifications :

- **Compatibilité des obligations des consommateurs :** un dépôt auparavant conforme reste-t-il conforme sans changement ?
- **Compatibilité des garanties d'assurance :** toutes les contraintes, protections et garanties de preuve promises antérieurement sont-elles préservées ?

Un changement n'est rétrocompatible que si les deux conditions sont satisfaites. Une nouvelle obligation obligatoire est normalement MAJOR pour un paquet/profil existant. Un assouplissement qui affaiblit une garantie sur laquelle les consommateurs s'appuient peut également être MAJOR, même s'il facilite la conformité. Une nouvelle règle facultative ou limitée à un profil explicitement activé peut être MINOR. La correction d'une source normative qui change l'interprétation effective n'est pas automatiquement PATCH.

La version du format/schéma, celle du métamodèle, celle du paquet de règles et celle du profil de dépôt sont des contrats distincts. Une modification source peut donc être PATCH pour un document explicatif, MAJOR pour un paquet normatif et sans effet sur un schéma de sérialisation.

## 4. Taxonomie des artefacts et régime par défaut

La matrice suivante définit la classification par défaut de GovCheck. « SemVer : oui » signifie uniquement après déclaration du contrat conformément au §2.2 ; cela n'autorise pas à attribuer une version à chaque instance. « Révision » signifie identifiant logique stable et identité de révision immuable. « Instance » signifie enregistrement unique d'une occurrence ou d'un événement. Chaque ligne est une politique de départ, pas l'affirmation que le type d'artefact est déjà implémenté.

| Catégorie d'artefact | Exemples | Régime par défaut | Périmètre SemVer éventuel | Point d'attention pour le changement/la compatibilité |
|---|---|---|---|---|
| Intention produit et objectifs | Finalité, objectifs, non-objectifs | Révision | Contrat d'ensemble d'objectifs publié uniquement | Sens, périmètre, résultats approuvés et raffinements descendants |
| Besoins des parties prenantes | Besoins, résultats utilisateur | Révision | Rarement ; uniquement comme contrat externe stable | Sujet visé et conditions de satisfaction |
| Exigences | Fonctionnelles, qualité, sécurité, processus | Révision | Contrat de jeu/paquet/profil d'exigences | Obligation, applicabilité, satisfaction et consommateurs affectés |
| Critères d'acceptation | Prédicats et scénarios d'acceptation | Révision ; contrat de suite de tests éventuellement versionné | Jeu de critères uniquement s'il est consommé comme contrat | Les résultats auparavant acceptables le restent-ils ? |
| Hypothèses | Environnement, confiance, plateforme, exploitation | Révision | Généralement aucune | Validité des affirmations/preuves dépendantes |
| Exclusions de périmètre | Non-objectifs et frontières explicites | Révision | Contrat de périmètre/profil s'il est consommé en externe | Inclusion/exclusion et obligations affectées |
| Risques et scénarios de menace | Menaces, abus, risques | Révision | Contrat de modèle de menace s'il constitue une frontière stable | Couverture, capacités adverses et affirmations de sécurité |
| Métamodèle normatif | Concepts, relations, typage, interprétation | Révision + version de contrat | Oui, si les sémantiques publiques sont déclarées | Compatibilité structurelle et sémantique ; interprétation |
| Modèle canonique/format de gouvernance | Structure et encodage du paquet canonique | Révision + version distincte de schéma/format | Oui | Parsing, canonicalisation, sens et comportement des consommateurs |
| Paquet de règles normatives | Obligations, interdictions, permissions, invariants | Révision + version de contrat du paquet | Oui, avec double test de compatibilité | Impact sur la conformité et préservation des garanties |
| Règle individuelle | ID stable et révisions | Révision | Normalement pas par règle ; le paquet porte la compatibilité | Identité, force, périmètre, sémantique et remplacement |
| Profil de dépôt | Règles sélectionnées, paramètres, applicabilité | Révision + version de contrat du profil | Oui, s'il est consommé par des dépôts gouvernés | Ensemble effectif d'obligations/garanties et migration |
| Exception/dérogation | Exception bornée, autorisée, limitée dans le temps | Instance/événement avec conditions révisables | Pas de SemVer par exception | Autorité, sujet, périmètre, motif, échéance et révocation |
| Spécification technique/API | CLI, API, contrat d'adaptateur ou protocole | Révision + version de contrat | Oui | Interface observable, erreurs, garanties et migration |
| Sérialisation/schéma | JSON Schema, schéma de rapport, manifeste | Révision + version de schéma | Oui | Parsing producteur/consommateur et interprétation sémantique |
| Décision d'architecture (ADR) | Décision de conception acceptée/rejetée | Révision + événement de décision | Pas de SemVer par ADR | Autorité, périmètre de décision, remplacement et contrats affectés |
| Architecture de référence | Composants, frontières, interfaces | Révision | SemVer uniquement pour un contrat d'architecture publié | Compatibilité des frontières/interfaces/garanties |
| Contrat assume-guarantee | Hypothèses et garanties d'un composant | Révision + version de contrat | Oui | Raffinement, composition et préservation des garanties |
| Propriété/invariant | Prédicat de sûreté, vivacité ou conformité | Révision | Uniquement comme contrat public de jeu de propriétés | Sens du prédicat, domaine, hypothèses et dépendances de preuve |
| Modèle formel | TLA+, Alloy, machine à états, modèle abstrait | Révision ; version de contrat de modèle facultative | Conditionnel | Sémantique des états/comportements, frontière d'abstraction et propriétés |
| Configuration de model checking | Config TLC, constantes, bornes, équité/réductions | Révision liée au modèle | Pas de SemVer par exécution/configuration par défaut | Question exacte explorée et comparabilité |
| Énoncé formel/théorème | Proposition, interface de théorème, axiomes | Révision ; contrat de bibliothèque si exporté | Conditionnel au niveau bibliothèque/interface | Proposition, hypothèses, axiomes et imports |
| Objet/dérivation de preuve | Terme Lean, script, certificat vérifié | Révision | Pas de SemVer par preuve individuelle | Énoncé exact, noyau, dépendances et reproductibilité |
| Définition/suite de tests | Cas de test, harnais, vecteurs d'acceptation | Révision + contrat de suite si consommé | Conditionnel | Oracle, revendication de couverture, fixtures et compatibilité |
| Cas de test individuel | Assertion et fixture | Révision | Généralement aucune | Sujet, oracle, préconditions et résultat attendu |
| Exécution de test | Exécution d'un test ou d'une suite | Instance/événement | Jamais SemVer | Sujet exact, révision du test, invocation, environnement et résultat |
| Outil/compilateur/analyseur | Exécutable GovCheck, TLC, Lean, validateur | Contrat de release propre à l'outil | Oui, pour l'API/CLI publique de l'outil | Compatibilité et identité exacte du build |
| Script/adaptateur de contrôle | Commande, arguments, sortie, contrat de ressources | Révision + contrat d'adaptateur si consommé | Conditionnel | Sémantique CLI/sortie, échecs et frontière de confiance |
| Implémentation/code source | Sources GovCheck et bibliothèques | Révision + contrat de release produit | Oui, pour les interfaces du logiciel publié | Comportement public, CLI/API et garanties prises en charge |
| Binaire/artefact de build | Exécutable, paquet, image conteneur | Instance de build/release immuable | Version héritée de la release produit ; identité du build distincte | Reproductibilité, provenance et identité exacte des sources/outils |
| Configuration de déploiement | Paramètres d'exécution et de politique | Révision ; schéma de config éventuellement versionné | Conditionnel pour une interface stable | Comportement effectif, valeurs par défaut, sécurité et migration |
| Jeu de données/fixture/corpus | Données de test, corpus synthétique, benchmark | Révision ; contrat de dataset éventuellement versionné | Conditionnel, propre au dataset | Schéma, contenu, distribution, labels, partitions et usage visé |
| Contre-exemple/témoin | Trace TLC, entrée fautive, reproducteur minimal | Instance/preuve | Pas de SemVer par témoin | Modèle/test/outil exact et provenance de la trace |
| Élément de preuve/observation | Sortie brute, journal, observation externe | Instance/événement | Pas de SemVer par élément | Lien au sujet, source, date, intégrité et limites |
| Claim/affirmation | Proposition circonscrite relative à un sujet | Révision | Pas de SemVer par affirmation individuelle | Proposition, sujet, périmètre, hypothèses et soutien |
| Argument d'assurance | Décomposition de claims et raisonnement | Révision | Conditionnel pour un cadre/interface d'argument publié | Graphe de soutien, réfutations, hypothèses et dépendances |
| Rapport de vérification/évaluation | Rapport de test, TLC, preuve ou conformité | Instance ; schéma du rapport versionné séparément | Schéma seulement, pas chaque rapport | Exécution exacte, statut, achèvement, hypothèses et preuves |
| Attestation/signature | Déclaration signée relative à un sujet | Instance/événement immuable | Pas de SemVer | Signataire, autorité, clé, sujet, déclaration et révocation |
| Approbation/acceptation/rejet | Décision autorisée sur un candidat exact | Événement immuable | Pas de SemVer | Autorité de l'acteur, tuple candidat, motif et remplacement |
| Manifeste de release | Manifeste d'une release | Instance immuable ; schéma du manifeste versionné | Schéma seulement, pas chaque manifeste | Release exacte, artefacts, empreintes, outils et preuves |
| Documentation normative | Projection humaine des règles | Révision ; contrat normatif porté par le paquet source | Pas de SemVer indépendant | Fidélité à l'autorité canonique et parité de traduction |
| Documentation explicative | Guides, justifications, exemples | Révision | Normalement aucune | Clarté et exactitude ; aucune force normative indépendante |
| Traduction | Version française/anglaise associée à la source | Révision liée à la révision source | Pas de SemVer indépendant | Fidélité sémantique, statut et révision source |
| Diagramme/rapport généré | Mermaid, HTML, vue rendue | Révision/instance dérivée | Générateur ou schéma de sortie éventuellement versionné | Identité du générateur et reproductibilité ; la source reste l'autorité |
| Publication/paquet de release | Bundle publié ou release du dépôt | Identité de release + manifeste immuable | SemVer uniquement pour son contrat consommateur déclaré | Contrat de distribution, contenu, provenance et support |

### 4.1 Lecture de la matrice

- Le régime est attribué à l'**artefact ou à l'enregistrement logique**, pas automatiquement à chaque fichier qui le contient.
- Un paquet peut utiliser SemVer tandis que ses règles individuelles conservent des IDs stables et des révisions ordinaires.
- Un modèle TLA+ peut avoir une identité de révision et éventuellement une version de contrat de modèle ; chaque exécution TLC reste une instance distincte.
- Une bibliothèque de théorèmes peut versionner son interface logique exportée ; un terme de preuve individuel est identifié par sa révision exacte et le contexte de vérification.
- Une suite de tests peut exposer un oracle/contrat de couverture versionné ; les exécutions ne sont jamais des versions de cette suite.
- Un format de rapport peut utiliser SemVer ; un rapport individuel est une instance d'évaluation unique et immuable.
- Un document peut être une projection contrôlée. Sa révision n'est pas une seconde version du paquet normatif.

## 5. Règles de décision propres aux catégories

### 5.1 Paquets et profils normatifs

Avant publication, calculer ou examiner les ensembles effectifs d'obligations et de garanties de chaque profil pris en charge. Pour chaque changement, consigner :

- règles ajoutées, supprimées, dépréciées, renforcées, affaiblies ou dont le périmètre a changé ;
- dépôts/consommateurs nouvellement concernés ou qui ne le sont plus ;
- maintien ou non de la conformité des consommateurs précédemment conformes ;
- préservation ou non des garanties antérieures ;
- besoins de migration, période de transition, exceptions et réévaluations.

Classifications typiques :

| Changement | Classification par défaut |
|---|---|
| Ajouter une obligation obligatoire à un profil existant | MAJOR |
| Ajouter une nouvelle règle facultative non sélectionnée par les profils existants | MINOR |
| Ajouter une règle uniquement à un nouveau profil activable explicitement | MINOR pour la famille paquet/profils ; le nouveau profil a sa propre identité |
| Renforcer une obligation existante ou élargir son applicabilité | MAJOR |
| Affaiblir/supprimer une garantie sur laquelle les consommateurs s'appuient | MAJOR |
| Corriger une faute dans un commentaire sans changer le sens | Aucun incrément de contrat |
| Corriger un défaut d'encodage source alors que le sens approuvé est non ambigu et inchangé | PATCH peut s'appliquer |
| Corriger une formulation/un encodage qui change l'interprétation effective ou les résultats de conformité | MAJOR, même si le changement est appelé correction |
| Modifier une exception individuelle ou son échéance | Nouvelle révision/événement, pas d'incrément SemVer du paquet |

Une modification normative exige l'approbation de l'autorité désignée pour la règle/le paquet. L'incrément SemVer ne peut pas autoriser le changement.

### 5.2 Modèles formels et propriétés

Pour un modèle formel, consigner sa révision, son sujet sémantique, sa frontière d'abstraction, ses variables/actions/relation de transition, ses hypothèses, ses invariants/propriétés temporelles et ses dépendances consommatrices.

Ne pas classer les changements selon leur seule syntaxe :

- Changement de commentaire/formatage sans effet sémantique : révision uniquement, sans incrément de contrat du modèle.
- Ajout d'une variable ou transition démontrée comme conservatrice par observation pour l'interface déclarée et préservant toutes les propriétés promises : éventuellement MINOR.
- Ajout d'un comportement qui invalide une propriété de sûreté/vivacité promise antérieurement : MAJOR.
- Suppression d'un comportement invalide : PATCH uniquement si le contrat approuvé l'excluait déjà et que la correction rétablit exactement ce sens ; sinon MAJOR ou nouveau contrat de modèle.
- Modification de l'énoncé d'une propriété, des hypothèses, de l'équité, des bornes ou de l'abstraction : évaluer comme changement de contrat sémantique ; ne jamais la masquer comme simple patch d'outil/configuration.

Une modification de la configuration TLC crée une nouvelle révision de configuration et une nouvelle identité d'exécution. Elle ne modifie pas rétroactivement les anciens résultats de model checking. Les nombres d'états ne sont comparables que si le modèle, la configuration, l'outil et l'environnement pertinents sont suffisamment alignés.

### 5.3 Preuves, tests et éléments probants

- Réparer une preuve pour la même proposition crée une nouvelle révision de preuve. Cela ne change pas nécessairement le contrat de la bibliothèque de théorèmes.
- Un énoncé de théorème modifié est une autre proposition ; préserver la relation d'identité et ne pas le présenter comme une simple réparation de preuve.
- Corriger l'oracle d'un test crée une révision de définition du test. Si cela modifie le comportement accepté par un contrat publié de suite de tests, évaluer la compatibilité au niveau de la suite.
- Une exécution de test, TLC, de vérification de preuve ou une observation externe est une nouvelle instance. Ne jamais corriger ni écraser son résultat.
- Corriger un rapport produit une nouvelle révision/instance liée à l'enregistrement remplacé, avec motif et autorité. Préserver l'original.
- Invalider une preuve modifie son admissibilité/statut courant, pas son identité historique ni son contenu brut.

### 5.4 Documentation et traductions

Distinguer l'autorité source de sa présentation :

- Les changements de sens normatif dans la source canonique sont gouvernés comme changements de règles/paquets.
- Régénérer une projection seule ne crée pas une nouvelle version SemVer du contrat source.
- Corriger une traduction pour rétablir un sens déjà approuvé crée une révision documentaire ; une traduction qui change l'interprétation effective est un défaut de conformité à corriger avec analyse d'impact.
- Si un document est lui-même explicitement déclaré contrat public, versionner ce contrat séparément des révisions éditoriales, selon le même test de compatibilité.

## 6. Règles d'impact et d'invalidation

La classification de version et la fraîcheur des preuves sont deux décisions distinctes. Tout artefact modifié doit déclencher une analyse de dépendances, même lorsqu'aucun incrément SemVer n'est nécessaire.

Pour chaque claim, preuve, test, rapport, approbation et décision d'acceptation dépendant, déterminer si l'élément modifié fait partie de ses entrées ou hypothèses déclarées. Enregistrer ensuite l'un des états suivants :

- **Non affecté :** l'analyse de dépendances établit l'absence de changement sémantique ou d'identité pertinent.
- **À examiner :** la pertinence ne peut être décidée automatiquement ou l'équivalence sémantique n'est pas établie.
- **Obsolète/invalide :** une entrée, hypothèse, contrat ou sujet requis a changé.
- **Remplacé :** un nouvel artefact/une nouvelle décision autorisée remplace l'ancien.
- **Révoqué :** une autorité ou une clé invalide une attestation/approbation précédemment émise.

Ne pas déduire que tout artefact descendant devient obsolète uniquement parce qu'un commit du dépôt a changé. Inversement, ne pas déduire la fraîcheur d'un SemVer inchangé. Les relations de dépendance et les liens vers les révisions exactes déterminent l'impact.

Au minimum, les changements d'un paquet/profil normatif, d'un modèle, d'une propriété, d'une implémentation, d'un évaluateur, d'une chaîne d'outils, d'une configuration, d'un oracle de test, d'une source externe ou d'une hypothèse de confiance exigent une évaluation d'impact explicite sur les preuves qui en dépendent. Les résultats historiques restent accessibles et sont exclus de l'acceptation courante lorsqu'ils sont invalidés.

## 7. Enregistrement de changement requis pour un contrat versionné

Une proposition de release d'un contrat gouverné par SemVer devrait consigner :

1. l'ID logique de l'artefact et le nom du contrat ;
2. les versions de contrat antérieure et proposée ;
3. les révisions/empreintes exactes antérieure et candidate ;
4. les catégories de consommateurs déclarées et le sens de compatibilité ;
5. l'interface publique/les garanties couvertes par la version ;
6. les changements regroupés en ajouts, modifications, dépréciations, retraits et corrections ;
7. l'analyse de compatibilité, y compris contre-exemples ou cas de migration ;
8. les effets sur les obligations normatives et garanties d'assurance, le cas échéant ;
9. les artefacts/preuves dépendants à examiner ou invalider ;
10. la politique de migration/dépréciation/support ;
11. la décision autorisée et sa provenance ;
12. le tag/commit de release et le manifeste immuable.

L'auteur du changement peut proposer un incrément, mais ne doit pas être l'unique autorité d'une décision de compatibilité normative lorsqu'une approbation indépendante est requise.

## 8. Cas limites illustrés

| Scénario | Traitement correct |
|---|---|
| Ajouter un champ JSON facultatif ; les anciens lecteurs ignorent les champs inconnus comme promis | MINOR pour le contrat de schéma ; nouvelle révision et release du schéma |
| Ajouter un champ facultatif mais les anciens lecteurs rejettent les champs inconnus | Non rétrocompatible ; MAJOR ou format négocié séparément |
| Ajouter une règle de sécurité obligatoire à un profil de dépôt existant | MAJOR pour le profil/paquet, même si le schéma de fichier ne change pas |
| Ajouter un nouveau profil strict activable explicitement | Nouvelle identité de profil ; ajout éventuellement MINOR au catalogue des profils |
| Corriger une faute dans un commentaire TLA+ | Révision du modèle uniquement ; aucun incrément sémantique |
| Ajouter une transition TLA+ qui étend les comportements et viole un invariant de sûreté | Changement MAJOR du contrat de modèle ; réévaluer les claims dépendants |
| Passer la borne TLC de 10 à 12 | Révision de configuration et nouvelle exécution ; pas d'incrément SemVer du modèle en soi |
| Réparer un script de preuve Lean alors que l'énoncé du théorème est identique | Nouvelle révision de preuve ; interface du théorème inchangée |
| Affaiblir les hypothèses ou la conclusion d'un théorème | Nouvelle proposition/interface ; évaluer MAJOR pour la bibliothèque dépendante |
| Corriger la valeur attendue d'un test car le test précédent encodait mal l'exigence approuvée | Révision du test ; évaluer le contrat de suite et les résultats affectés ; réexécuter sans réécrire l'ancienne exécution |
| Relancer la même suite de tests sur un nouveau commit | Nouvelle instance d'exécution, pas un PATCH de l'ancien rapport |
| Corriger la traduction française pour qu'elle corresponde au texte normatif anglais approuvé | Révision de traduction ; aucun SemVer normatif indépendant |
| Modifier la règle approuvée parce que les deux traductions étaient erronées | Changement normatif avec décision d'autorité et analyse de compatibilité |
| Remplacer une clé de signature après compromission | Événement de cycle de vie de clé/attestation et révocation ; pas un PATCH des signatures |
| Reconstruire les mêmes sources avec un autre compilateur | Nouvelle instance de build/provenance ; le SemVer du produit peut rester inchangé |

## 9. Frontière d'automatisation et contrôles de conformité

Une future implémentation GovCheck pourra automatiser les aspects structurels et mécaniques de cette politique. Elle ne doit pas prétendre qu'un changement sémantique est compatible à partir d'un simple diff textuel ou de l'incrément déclaré.

Contrôles candidats :

1. Chaque artefact gouverné possède un ID logique stable et unique lorsque requis.
2. Les révisions/releases publiées sont immuables et se résolvent vers des identités VCS/contenu exactes.
3. Chaque contrat SemVer déclare ses consommateurs, son contrat public et sa politique de compatibilité.
4. Un incrément de version est accompagné d'un enregistrement de changement catégorisé et d'une justification de compatibilité.
5. Les déclarations MAJOR/MINOR/PATCH sont contrôlées par des règles structurelles observables par machine lorsque c'est possible.
6. Les changements de paquets normatifs énumèrent les règles/profils affectés et les deltas effectifs d'obligations/garanties.
7. Les changements de modèles identifient les actions/propriétés/hypothèses modifiées et exigent une analyse d'impact.
8. Les exécutions de rapports/tests/preuves ont des IDs d'instance distincts et lient sujets, définitions, outils, configurations et environnements exacts.
9. Rapports, attestations et décisions ne sont pas écrasés ; corrections/remplacements/révocations sont des événements explicites.
10. Les changements de dépendances produisent un ensemble d'éléments de preuve potentiellement obsolètes à examiner.
11. Les traductions et projections générées identifient la révision de leur source faisant autorité.
12. Toute analyse de compatibilité sémantique non prise en charge reste explicite et exige une revue humaine autorisée ; l'inconnu n'est jamais un succès.

L'automatisation peut valider l'identité, la structure des schémas, les liens, les empreintes, les deltas déclarés et la complétude du processus. Elle ne peut généralement pas prouver qu'un changement normatif préserve le sens attendu, qu'une abstraction de modèle est adéquate ou qu'une correction est sémantiquement rétrocompatible sans relation formalisée et preuve suffisante.

## 10. Adoption et migration

Cette proposition ne doit pas être considérée comme obligatoire avant son approbation par l'autorité GovCheck désignée et son incorporation dans l'autorité canonique de gouvernance selon le cycle de vie normal des changements.

L'adoption doit se faire sans inventer rétroactivement d'historiques SemVer :

1. Inventorier les artefacts logiques existants et préserver les IDs établis, notamment `govcheck.lifecycle`.
2. Lier les artefacts courants à leurs révisions et chemins exacts dans le dépôt.
3. Classer chaque artefact selon le §4 ; enregistrer comme ouvertes les classifications non résolues.
4. Attribuer des versions de contrat uniquement aux artefacts qui satisfont le §2.2. Ne pas fabriquer d'historique MAJOR/MINOR/PATCH antérieur.
5. Préserver la règle de release actuelle : les tags Git identifient les commits exacts ; les preuves générées sont liées à la release par des manifestes immuables.
6. Ajouter progressivement les liens de dépendance et les métadonnées d'invalidation des preuves.
7. Valider la politique sur les cas limites du §8 et des dépôts représentatifs avant d'implémenter son application automatisée.
8. Ne modifier le catalogue des artefacts et le schéma du manifeste de release que dans des changements distincts et revus, une fois les champs et sémantiques nécessaires décidés.

Ce document ne sélectionne aucun format de sérialisation, base de données, gestionnaire de paquets, service de release, assistant de preuve ni dépendance obligatoire supplémentaire.

## 11. Relations avec les contrats GovCheck existants

Cette politique développe, sans les remplacer silencieusement :

- [Spécification 0002 — Modèle canonique de gouvernance](../specifications/0002-canonical-governance-model.fr.md) : identité du paquet canonique, version sémantique et IDs stables des règles.
- [Spécification 0003 — Cycle de vie et acceptation des changements](../specifications/0003-change-lifecycle.fr.md) : identité immuable du candidat, remplacement, fraîcheur des preuves et événements append-only.
- [Spécification 0005 — Assurance, affirmations et preuves](../specifications/0005-assurance-model.fr.md) : lien exact au sujet/à la révision, provenance et invalidation.
- [Architecture 0010 — Assurance, preuve et conformité](0010-assurance-proof-and-conformance.fr.md) : classes de preuve et d'assurance non interchangeables.
- [Architecture 0012 — Autorité normative et documentation](0012-normative-authority-and-documentation.fr.md) : autorité canonique et projections contrôlées.
- [Architecture 0013 — Métamodèle de gouvernance](0013-governance-metamodel.fr.md) : catégories d'artefacts et relations typées.
- [Architecture 0015 — Plan de conformité et de validation](0015-governance-conformance-and-validation-plan.fr.md) : futures responsabilités de validation.

En cas de conflit, l'autorité normative approuvée existante prévaut jusqu'à ce qu'un changement autorisé le résolve. Ce document reste une proposition jusqu'à son adoption.

## 12. Références externes

- [Semantic Versioning 2.0.0](https://semver.org/lang/fr/spec/v2.0.0.html) : exige une API publique déclarée et définit l'immutabilité des versions publiées ainsi que les incréments fondés sur la compatibilité.
- [Cadre de versionnement 1EdTech 1.0]([R-23](../references.fr.md#r-23)) : applique séparément les principes dérivés de SemVer aux spécifications, documents, artefacts de spécification, modèles de données et logiciels.
- [W3C PROV-O]([R-24](../references.fr.md#r-24)) : vocabulaire de provenance pour les entités, activités, agents et dérivations ; il complète le versionnement sans le remplacer.
- [DataCite — Versioning]([R-25](../references.fr.md#r-25)) : distingue versions, identifiants associés et enregistrements conceptuels ; les responsables déterminent ce qui constitue une version majeure/mineure.
- [Scientific Data (2024), cadre de versionnement des jeux de données]([R-26](../references.fr.md#r-26)) : traitement propre au domaine des révisions de jeux de données et de la reproductibilité.

Ces références étayent la distinction entre versionnement de compatibilité, identité de révision et provenance. Elles ne prescrivent pas les classifications d'artefacts de GovCheck : celles-ci sont les propositions spécifiques au projet exposées ci-dessus.


## Références bibliographiques

Références externes citées dans ce document : [R-14](../references.fr.md#r-14), [R-23](../references.fr.md#r-23), [R-24](../references.fr.md#r-24), [R-25](../references.fr.md#r-25), [R-26](../references.fr.md#r-26).
