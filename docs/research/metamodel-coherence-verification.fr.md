# Vérifier la cohérence du métamodèle GovCheck : méthodes formelles et outils

**Statut :** proposition de recherche à soumettre à l'autorité ; aucune architecture adoptée. **Date :** 2026-11-11.  
**Version anglaise :** [Verifying GovCheck metamodel coherence](metamodel-coherence-verification.md).  
**Dossier parent :** [Dossier de décision sur le métamodèle](../decisions/metamodel-design-dossier.fr.md).

## 1. Mission et conclusion

L'objectif n'est pas seulement de contrôler la syntaxe des fichiers d'ontologie. GovCheck doit obtenir des éléments d'assurance défendables montrant que (a) chaque modèle source est cohérent selon sa sémantique déclarée, (b) les mappings préservent le sens qu'ils prétendent préserver, (c) l'intégration n'introduit ni contradiction ni conséquence imprévue, et (d) les règles temporelles de gouvernance restent valides lorsque les artefacts, hypothèses, autorités et décisions changent.

**Recommandation :** utiliser une architecture de vérification en couches, avec des contrats formels vérifiés par machine pour les ponts sémantiques critiques comme exigence d'assurance obligatoire, sans imposer un outil monolithique pour tous les contrôles. Lean est le candidat pour le noyau de preuve des théorèmes du pont ; CSLib doit être réutilisé lorsque ses formalismes conviennent, sans présumer qu'il contient toute la théorie GovCheck. Les raisonneurs OWL, SHACL, tests de contrats exécutables, recherche de contre-exemples et model checking temporel complètent la preuve. La chaîne obligatoire précise reste à arbitrer après prototype.

Pour les affirmations critiques d'interopérabilité, les obligations de preuve devraient être obligatoires. L'obligation d'installer Lean dans chaque dépôt adoptant est une décision distincte : un dépôt pourrait consommer un paquet de preuves épinglé, reproductible et vérifiable indépendamment, mais ne doit pas remplacer silencieusement une preuve requise par un test.

## 2. Décomposer la cohérence en obligations explicites

| ID | Propriété | Méthode candidate | Signification du résultat |
|---|---|---|---|
| VC-1 | Artefact source bien formé et préservé | Tests de parsing, schéma et aller-retour natif | Le contenu connu n'est pas perdu silencieusement |
| VC-2 | Ontologie source logiquement cohérente | Raisonneur OWL 2 DL, si applicable | Un modèle existe selon la sémantique déclarée |
| VC-3 | Instances conformes aux contraintes structurelles | SHACL, schémas, EVL, contrôles exécutables | L'instance satisfait les contraintes déclarées, sans théorème général sur son sens |
| VC-4 | Théorie intégrée cohérente | Raisonneurs sources et couche sémantique commune formalisée | Le résultat ne vaut que dans le périmètre et les hypothèses formalisés |
| VC-5 | Préservation du sens par les mappings | Preuve Lean de propriétés de mapping, complétée par des tests | Un théorème de préservation précis tient pour le mapping formalisé |
| VC-6 | Composition cohérente des mappings | Lois de composition en Lean ; recherche de contre-exemples | La composition préserve les propriétés déclarées |
| VC-7 | Extension conservative lorsque requise | Obligations de conservativité/non-interférence | Le noyau GovCheck n'altère pas les conséquences spécifiées dans le vocabulaire source, sauf autorisation |
| VC-8 | Invariants des transitions de gouvernance | Model checking TLA+ ; preuves Lean pour les affirmations générales | Les invariants tiennent dans le modèle vérifié ou les hypothèses formelles |
| VC-9 | Rejet des preuves périmées | Model checking temporel et règles d'invalidation | Décisions, mappings et preuves ne sont utilisés que pendant leur validité |
| VC-10 | Fiabilité et reproductibilité | Entrées/outils épinglés, vérification des preuves, fixtures négatives, rejeu | Le résultat est rattaché aux artefacts et à la base de confiance déclarés |

« Cohérent » ne doit jamais signifier seulement « la commande a réussi ». Chaque résultat enregistre propriété, périmètre, révisions sources, profil sémantique, hypothèses, version du vérificateur, identité du rapport/de la preuve, limites de ressources et statut. Distinguer preuve de théorème, model checking, validation, test, contre-exemple trouvé, indéterminé, non pris en charge, non exécuté et périmé.

## 3. Apports de chaque formalisme

### 3.1 OWL 2 et raisonneurs de logique de description

OWL 2 possède une sémantique formelle fondée sur les modèles. Pour un profil donné, un raisonneur peut vérifier cohérence d'ontologie, satisfiabilité de classes, subsomption et implication logique. C'est approprié pour une ontologie source exprimée dans un profil OWL pris en charge.

Limites : une ontologie cohérente peut être erronée ou incomplète ; plusieurs ontologies cohérentes séparément peuvent devenir incohérentes après intégration ; le monde ouvert d'OWL implique qu'une assertion absente n'est pas automatiquement fausse ; le profil et son expressivité importent ; une équivalence peut être plus forte que prévu et produire des inférences indésirables.

Utiliser les raisonneurs pour les ontologies sources et les mappings exprimés en OWL, pas comme vérificateurs universels de tous les modèles ou de la pertinence des intentions.

Sources : [OWL 2](https://www.w3.org/TR/owl-overview/), [sémantique directe OWL 2](https://www.w3.org/TR/owl2-direct-semantics/), [conformité OWL 2](https://www.w3.org/TR/owl2-conformance/).

### 3.2 SHACL et validation de schémas/contrats

SHACL valide les graphes RDF selon des formes déclarées et produit un rapport. Il convient aux identifiants obligatoires, métadonnées de mapping, statuts autorisés et champs de provenance lorsque ces concepts sont représentés dans le graphe et le langage choisis.

Ce n'est pas un démonstrateur de théorèmes pour des mappings arbitraires. Un rapport positif établit la conformité aux formes, pas la cohérence logique générale ni la préservation sémantique. Les tests doivent aussi couvrir XML/XMI natif, JSON, métadonnées Markdown et autres formats ; ne pas aplatir les artefacts natifs en RDF si cela fait perdre de l'information.

Source : [W3C SHACL](https://www.w3.org/TR/shacl/).

### 3.3 Lean et CSLib : preuve du pont sémantique

Lean permet de définir les domaines sémantiques GovCheck et de prouver des théorèmes sur les mappings. CSLib propose des formalisations réutilisables des fondements de l'informatique, de la sémantique opérationnelle, des systèmes de transition étiquetés, des équivalences et des logiques ; ses intérêts incluent la logique temporelle. Réutiliser ces définitions lorsqu'elles conviennent et formaliser la sémantique GovCheck manquante plutôt que de réimplémenter toutes les ontologies sources.



**Constat concret de compatibilité CSLib (2026-11-11) :** le snapshot `main` de CSLib examiné correspond au commit [`f8acdb37c713b0124ad36b863f50c200a5f1cdba`](https://github.com/leanprover/cslib/commit/f8acdb37c713b0124ad36b863f50c200a5f1cdba). Son fichier `lean-toolchain` épingle Lean **4.36.0-rc2** et son Lake manifest épingle le commit Mathlib `887bb849a9f64e1c66499fd5ff8523c864e78941`. La première tranche GovCheck vérifiée épingle actuellement Lean **4.19.0**. Le snapshot CSLib actuel n'est donc pas directement compatible avec le paquet GovCheck vérifié. Ne pas mettre à niveau le profil de preuve GovCheck uniquement pour importer CSLib. Il faut d'abord soit identifier et tester une révision historique de CSLib compatible avec Lean 4.19, soit isoler un profil de preuve utilisant CSLib avec sa propre chaîne d'outils épinglée. Les modules examinés fournissent bien des fondations utiles pour les LTS, simulations, équivalences de traces et logique temporelle élémentaire ; ils ne fournissent pas d'alignement général d'ontologies ni de métamodèle d'assurance GovCheck.

Le module CSLib de logique temporelle de base (`Cslib.Logics.BTL.Basic`) fournit des modalités futur/passé et une sémantique de satisfaction sur une relation `r`. Sa propre documentation n'impose **aucune propriété d'ordre** à cette relation : la réflexivité détermine si le présent est inclus et la transitivité est nécessaire pour modéliser un écoulement du temps. BTL est donc un langage/sémantique formel réutilisable, pas une déclaration automatique de temps linéaire ni un model checker à exploration d'états. GovCheck doit expliciter les hypothèses de cadre et utiliser TLC (ou un autre model checker) lorsqu'une exploration d'états finis et la génération de contre-exemples sont nécessaires.

Pour chaque formalisme source, définir/importer une interprétation sémantique — ou une abstraction explicitement plus faible — puis un mapping vers le domaine GovCheck. Énoncer notamment les obligations suivantes :

- **Bien-définition :** chaque construction source prise en charge devient une construction cible bien typée.
- **Préservation des contraintes :** une instance valide dans la source satisfait après mapping les contraintes cibles correspondantes.
- **Préservation épistémique :** une preuve issue d'un test ou du model checking ne devient pas une preuve de théorème par mapping.
- **Préservation de l'autorité :** un mapping ne peut augmenter l'autorité, la portée ou la validité d'une décision/délégation.
- **Préservation de la provenance :** identité, révision, origine et historique de transformation sont conservés.
- **Composition :** les mappings composables préservent les propriétés déclarées après composition.
- **Absence de perte silencieuse :** les constructions non prises en charge, supprimées ou approximées sont signalées.
- **Conservativité/non-interférence :** l'ajout du vocabulaire GovCheck n'ajoute pas de conclusions dans le vocabulaire source, sauf conséquences explicitement autorisées.

Ce sont des obligations à définir précisément, pas des théorèmes fournis automatiquement par Lean ou CSLib. Le théorème dépend du type de mapping : exact, sain mais incomplet, partiel, approximatif ou simple traçabilité. « Préserve la sémantique » est trop vague pour être un énoncé de théorème.

La voie Boole/vérification de code de CSLib n'est pas le pont principal pour les ontologies. Son guide précise que les premières traductions peuvent être ad hoc et considérées comme fiables ; les preuves de préservation sémantique sont un objectif à plus long terme. GovCheck ne doit pas faire confiance à un traducteur non prouvé. Épingler CSLib et documenter version de Lean, imports, axiomes, code de confiance, dépendances et instructions de rejeu.

Sources : [CSLib](https://github.com/leanprover/cslib), [organisation](https://github.com/leanprover/cslib/blob/main/ORGANISATION.md), [guide de contribution](https://github.com/leanprover/cslib/blob/main/CONTRIBUTING.md).

### 3.4 Logique temporelle et model checking

TLA+ modélise états et transitions ; il peut vérifier des invariants et propriétés temporelles d'une abstraction à états finis. Il convient à l'adoption/révocation des décisions, validité des délégations, expiration des assurances, changements de versions sources, invalidation des mappings, ordre des approbations et rejet des preuves périmées.

Exemples : une délégation révoquée n'est jamais acceptée pour une nouvelle décision ; une décision ne prend pas effet avant adoption et approbations requises ; un changement de source invalide mappings/preuves dépendants jusqu'à revalidation ; un rapport ne s'applique qu'aux révisions et hypothèses exactes ; aucun résultat de test/model checking n'est promu en preuve de théorème ; un risque accepté expire ou déclenche une revue.

TLC explore le modèle fini spécifié ; le résultat dépend de l'espace d'états, des contraintes et de l'abstraction. TLAPS vérifie mécaniquement des étapes de preuve, mais sa version documentée ne réalise pas le raisonnement temporel général pour tous les constructeurs TLA+. Ne pas tirer un théorème non borné d'un model checking fini.

La logique temporelle complète Lean : Lean pour les définitions sémantiques et théorèmes de préservation ; TLA+/TLC pour l'évolution de la gouvernance ; preuve ou raffinement pour les affirmations générales plus fortes.

Sources : [système de preuve TLA+](https://proofs.tlapl.us/doc/web/content/Home.html), [documentation TLC](https://github.com/tlaplus/tlaplus/blob/master/general/docs/tlcgui.txt).

### 3.5 Vérification de transformations et recherche de contre-exemples

La recherche en ingénierie dirigée par les modèles étudie la vérification par combinaison de règles de transformation, propriétés recherchées et techniques. Epsilon EVL vérifie des contraintes intra- et intermodèles. Alloy cherche des contre-exemples relationnels dans des portées finies. Ces outils sont utiles pour détecter les erreurs tôt, mais une recherche bornée n'est pas une preuve non bornée.

Les utiliser pour produire des contre-exemples et fixtures de régression, puis formaliser les lois de mapping critiques en Lean ou annoncer explicitement les bornes d'un résultat exhaustif.

Sources : [Calegari et Szasz, revue](https://doi.org/10.1016/j.entcs.2013.02.002), [Epsilon EVL](https://eclipse.dev/epsilon/doc/evl/), [analyseur Alloy](https://alloy.readthedocs.io/en/latest/tooling/analyzer.html).

## 4. Chaque mapping doit avoir un contrat sémantique

Déclarer pour chaque mapping :
1. Identifiants, versions, révisions et profils sémantiques source/cible.
2. Direction : source vers cible, inverse, équivalence ou simple traçabilité.
3. Couverture : exacte, équivalente, saine mais incomplète, plus étroite, plus large, partielle, approximative, ambiguë ou non prise en charge.
4. Interprétation des constructions et relations sources dans la cible, y compris les abstractions.
5. Théorème de préservation précis, hypothèses et portée quantifiée.
6. Comportement aller-retour et pertes connues.
7. Contre-exemples et fixtures adversariales.
8. Version, période de validité et conditions d'invalidation.
9. Éléments d'assurance typés : théorème/preuve Lean, rapport de raisonneur, model checking, tests ou combinaison.
10. Base de confiance : parseur, traducteur, vérificateur, axiomes et dépendances externes.

Ne pas exiger une équivalence pour tous les mappings. Une abstraction unidirectionnelle saine peut être la revendication correcte. Sans interprétation sémantique, parler de traçabilité/association, pas d'équivalence sémantique.

## 5. Architecture de vérification proposée

    Artefacts natifs : SACM XML/XMI, OWL/RDF, exigences, cycle de vie, autorité, modèle GovCheck
       ↓
    1. Analyse, empreinte, préservation ; validation des schémas natifs
       ↓
    2. Contrôles sources : raisonneur OWL | SHACL | schéma natif | contraintes exécutables
       ↓
    3. Contrats de mapping typés : versions | couverture | hypothèses | pertes | invalidation
       ↔ recherche de contre-exemples, fixtures et analyse bornée
       ↓
    4. Pont sémantique formel : noyau Lean + réemploi CSLib pertinent
       - bien-définition, préservation, composition, non-interférence
       ↓
    5. Modèle temporel : invariants TLA+/TLC, expiration, révocation, invalidation
       ↓
    6. Registre d'assurance : entrées exactes, chaîne d'outils, périmètre, statut, preuve/rapport, base de confiance

Cette architecture est candidate, non adoptée. Conserver les formats natifs et moteurs sémantiques sources ; ne pas supposer que toute ontologie peut être traduite sans perte vers une représentation unique. Formaliser uniquement la sémantique commune et les mappings dont dépendent les garanties GovCheck.

## 6. Prototype pouvant invalider l'hypothèse

Commencer par trois petites tranches verticales plutôt que formaliser toutes les ontologies.

### Tranche A — Épistémologie de l'assurance

Relier un modèle minimal d'affirmation/preuve GovCheck à SACM et à un modèle de provenance. Formaliser les distinctions entre preuve issue d'un test, model checking et preuve de théorème ; affirmation source et élément qui l'étaye ; révision source et applicabilité de la preuve ; inconnu, non pris en charge, indéterminé, échec et réussite.

Contre-exemple obligatoire : aucun mapping valide ne peut transformer un test ou rapport de model checking en preuve de théorème sans règle d'inférence séparément démontrée et ses hypothèses.

### Tranche B — Mapping intention/exigence/décision

Mapper un petit ensemble d'intention, objectif, exigence, décision et propriété sur SEON/ReqON et un modèle d'exigences pertinent. Déclarer chaque mapping équivalent, directionnel, partiel ou simple traçabilité. Vérifier que GovCheck n'introduit pas d'implications non voulues dans le vocabulaire source.

### Tranche C — Autorité et validité temporelle

Modéliser adoption, délégation, révocation, portée, périodes d'effet et révisions des sources/mappings/preuves. Vérifier les propriétés temporelles avec TLA+ ; formaliser en Lean les théorèmes généraux de préservation de l'autorité une fois la sémantique stabilisée.

### Critères d'acceptation

- Chaque théorème a définitions, hypothèses et portée explicites ; aucun axiome ni traducteur de confiance caché.
- Les fixtures sources volontairement incohérentes sont détectées.
- Les mappings invalides produisent des contre-exemples ou échouent à la preuve.
- Les mappings valides préservent identité et provenance.
- Les constructions non prises en charge et pertes aller-retour sont signalées, jamais supprimées silencieusement.
- Les rapports périmés deviennent inutilisables après changement pertinent d'entrée ou d'hypothèse.
- Les résultats distinguent preuve de théorème, model checking, validation et tests.
- Le rejeu avec entrées épinglées est reproductible.
- Le coût de preuve est mesuré ; une preuve irréalisable ne peut être déclassée qu'avec décision autorisée et lacune résiduelle documentée.

## 7. Recommandation à soumettre à l'autorité

| Question | Recommandation |
|---|---|
| Faut-il assurer la cohérence sémantique critique ? | **Oui.** Exigence d'assurance de premier rang. |
| Chaque contrôle doit-il utiliser Lean ? | Non. Choisir la méthode la plus forte adaptée ; les obligations des mappings critiques doivent être explicites et vérifiées par machine lorsque faisable. |
| CSLib suffit-elle ? | Non. Réutiliser les formalismes pertinents et prouver la sémantique GovCheck manquante. |
| La logique temporelle suffit-elle ? | Non. Elle sert à l'évolution, à la validité temporelle et à l'invalidation, pas au raisonnement statique universel. |
| Remplacer OWL/SHACL par Lean ? | Non. Conserver les vérificateurs natifs et prouver les affirmations critiques du pont. |
| Les tests remplacent-ils une preuve manquante ? | Non. Tout déclassement doit déclarer la lacune et être autorisé. |
| Architecture adoptée ? | Non. Proposition de prototype à examiner. |

L'approche la plus solide est une **vérification hétérogène avec pont formellement spécifié** : raisonneurs/validateurs sources, recherche de contre-exemples et fixtures, preuves Lean/CSLib pour les lois critiques des mappings et model checking temporel pour l'évolution de la gouvernance. Aucun outil seul ne démontre toutes les formes de cohérence.

## 8. Backlog existant et critères de sortie

Pas de nouvel épique :
- **#73 :** contrats sémantiques, classes de mapping, questions de compétence et obligations de preuve.
- **#56 :** évaluation des outils et formalismes sources.
- **#74 :** versionnement des éléments d'assurance, empreintes sources, règles de mapping et dépendances.
- **#79 :** typage des résultats d'assurance et statuts.
- **#81 :** formalisation du cycle de vie et de l'invalidation.
- **#83 :** provenance des références, versions sources et liens retour.

Critères de sortie du premier prototype : trois tranches verticales ; contrôles propres aux sources ; au moins un théorème Lean sur un invariant intermodèle réel ; un contre-exemple délibéré ; contrôles temporels d'invalidation/preuves périmées ; paquet d'assurance reproductible ; base de confiance documentée ; décision sur les obligations de preuve obligatoires.

## 9. Contrat concret de la première tranche

Le contrat d'ingénierie proposé précise désormais la première tranche épistémique, ses obligations de preuve Lean (VC-EPI-01/02, VC-MAP-01–04 et VC-AUTH-01), les fixtures adversariales, les propriétés temporelles d'invalidation, le protocole d'audit des imports CSLib et le critère d'achèvement : [Contrat du prototype de cohérence](metamodel-coherence-prototype-contract.fr.md) / [version anglaise](metamodel-coherence-prototype-contract.md). Il s'agit d'un contrat de conception, pas d'un prototype exécuté ou compilé.

## 10. Références et traçabilité

Catalogue : [R-121 sémantique OWL 2](../references.fr.md#r-121), [R-122 SHACL](../references.fr.md#r-122), [R-123 CSLib](../references.fr.md#r-123), [R-124 TLA+/TLAPS](../references.fr.md#r-124), [R-125 vérification des transformations](../references.fr.md#r-125), [R-126 EVL/Alloy](../references.fr.md#r-126), [R-127 alignement et conservativité](../references.fr.md#r-127).

Documents liés : [dossier de décision](../decisions/metamodel-design-dossier.fr.md), [étude de réemploi](metamodel-ontology-reuse-assessment.fr.md), [Architecture 0013](../architecture/0013-governance-metamodel.md), [Architecture 0027](../architecture/0027-domain-semantic-standards-decisions-and-bootstrap.md), [Spécification 0002](../specifications/0002-canonical-governance-model.md), [Spécification 0005](../specifications/0005-assurance-model.md).


## Éléments probants du prototype (2026-11-11)

La première tranche exécutable a maintenant été compilée et vérifiée dans deux profils épinglés distincts :

- **Noyau Lean :** [PR #108](https://github.com/Martin-PB/govcheck/pull/108), Lean 4.19.0. Les théorèmes de préservation par transport et de non-promotion épistémique compilent ; l'audit des axiomes du module de théorèmes réussit et le rapport explicite ne montre aucun axiome pour les neuf théorèmes. [Exécution 43049890363](https://github.com/Martin-PB/govcheck/actions/runs/43049890363).
- **Pont LTS CSLib :** [PR #109](https://github.com/Martin-PB/govcheck/pull/109), Lean 4.36.0-rc2, commit CSLib `f8acdb37c713b0124ad36b863f50c200a5f1cdba`. Les théorèmes de préservation des transitions LTS et des exécutions finies compilent ; l'audit des axiomes du module de théorèmes réussit et le rapport explicite ne montre aucun axiome pour les douze théorèmes. [Exécution 43051029627](https://github.com/Martin-PB/govcheck/actions/runs/43051029627).

Cela démontre que CSLib peut soutenir des lois formelles de préservation sur des LTS et des exécutions finies avec sa propre chaîne d'outils épinglée. Cela ne démontre **pas** l'alignement d'ontologies, la préservation aller-retour SACM, l'équivalence sémantique entre modèles externes et GovCheck, ni le raffinement de l'implémentation. La PR #109 est empilée sur la PR #108 ; aucune des deux n'est fusionnée.