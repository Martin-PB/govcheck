# SACM 2.4 Beta 1 — inventaire structurel XMI dérivé de la source

**Statut :** inventaire structurel généré pour une révision exacte du XML de métamodèle OMG, épinglée par digest ; aucune correspondance sémantique vers GovCheck n'est inférée.  
**Source :** [R-197 — XML normatif du métamodèle OMG SACM 2.4 Beta 1](../references.fr.md#r-197).  
**Risque indépendant de divergence entre vues :** [R-128](../references.fr.md#r-128).  
**Générateur :** [`scripts/parse-sacm-xmi.py`](../../scripts/parse-sacm-xmi.py).  
**Synthèse révisable :** [`formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json`](../../formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json).  
**Inventaire complet généré :** publié avec l'artefact du workflow de capture ; il n'est pas dupliqué dans le dépôt sous la forme d'un volumineux fichier généré.

## 1. Entrée exacte et reproductibilité

Le parseur ne consomme que le payload source capturé dont le SHA-256 correspond à la valeur épinglée dans R-197 :

- identifiant de fichier OMG : `ptc/26-05-28` ;
- révision source datée : `2026-05-04` ;
- URL : `https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml` ;
- longueur : `524243` octets ;
- SHA-256 : `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`.

Le document est un XML dont la racine et le vocabulaire du métamodèle utilisent les espaces de noms OMG XMI 20131001 et UML 20131001. Les métadonnées d'export indiquent MagicDraw Clean XMI Exporter 2024x v6. Cela décrit la représentation effective de la source ; cela **ne signifie pas** que SACM 2.4 définit un contrat portable d'échange d'instances XMI.

Le `source.xml` original reste l'autorité et est conservé octet pour octet par le workflow de capture. L'inventaire généré est une vue dérivée, reproductible à partir de ces octets exacts et de la révision du parseur.

## 2. Constat structurel

Le document épinglé par digest contient :

| Construction XMI/UML | Nombre |
|---|---:|
| Éléments XMI identifiés (`xmi:id`) | 1 616 |
| Profils UML | 1 |
| Packages UML | 19 |
| Classes UML | 121 |
| Associations UML | 121 |
| Propriétés UML (attributs possédés et extrémités d'associations) | 355 |
| Généralisations UML | 167 |
| Énumérations UML | 8 |
| Littéraux d'énumération UML | 37 |
| Contraintes UML | 40 |
| Commentaires UML | 157 |
| Types de données UML | 2 |
| Expressions opaques UML | 40 |
| Comportements opaques UML | 3 |

L'arbre des packages comprend les packages principaux `Base`, `Foundation`, `Terminology`, `Packaging`, `Artifact` et `Argument` ; `Mapping` contient les packages `CAE` et `GSN`. Une branche `NonNormative` contient notamment `SACMView`, `DI`, `NamedValueTypes`, `DateTimeDuration`, des constructions liées à l'évaluation et des jointures. L'inventaire conserve les graphies de la source, y compris celles qui peuvent sembler inhabituelles ; il ne les normalise pas silencieusement.

Les huit énumérations et leurs littéraux source sont enregistrés explicitement. On y trouve notamment `AssertionDeclarationKind` (`axiomatic`, `assumed`, `asserted`, `byRule`) et `InferenceTypeKind` (`probable`, `collective`, `necessary`, `sufficient`, `necessaryAndSufficient`, `byRule`). Ce sont des faits propres à la vue XML ; R-128 documente des déclarations PDF contradictoires, dont `needsSupport` à la place de `byRule`.

## 3. Comptabilisation des références et de la contenance

L'inventaire enregistre 1 434 arêtes de référence explicites :

- 1 371 références aboutissent à un `xmi:id` de ce document exact ;
- 63 références sont des références externes `href` et restent volontairement non résolues ;
- aucune référence interne non résolue n'a été observée parmi les attributs de référence reconnus.

Pour chaque élément identifié, la sortie conserve le `xmi:id` stable, le tag XML, le `xmi:type`, le nom, tous les attributs, le propriétaire identifié le plus proche, le chemin de contenance, le texte direct et la structure ordonnée des enfants. Des index séparés recensent l'appartenance aux packages/classificateurs, les extrémités d'associations, les types et multiplicités de propriétés, les cibles de généralisations, les cibles/spécifications de contraintes et les arêtes de référence. Les nœuds sans identifiant (dont la documentation de l'exporteur, les enfants des expressions de contraintes, les données imbriquées des commentaires et les autres nœuds XML non identifiés) sont conservés en ligne ; les déclarations d'espaces de noms sont enregistrées.

Cette comptabilisation est un résultat du parseur pour le fichier épinglé ; elle ne prouve pas que le XML constitue un modèle UML sémantiquement complet ou bien formé.

## 4. Frontière du parseur et comportement défensif

Le parseur utilise uniquement la bibliothèque standard Python `xml.etree.ElementTree`. Il :

- vérifie le SHA-256 exact de la source avant l'analyse ;
- rejette les payloads vides ou trop volumineux, les XML mal formés, les valeurs `xmi:id` dupliquées et les déclarations DTD/entités ;
- distingue les déclarations de métaclasses `xmi:type` des références UML `type` non qualifiées ;
- résout les références internes reconnues par identifiant à partir de l'ensemble complet des identifiants du document ;
- conserve les valeurs `href` externes sans télécharger ni interpréter leurs cibles ;
- conserve génériquement les constructions identifiées inconnues au lieu de les supprimer ou de les convertir.

Il n'exécute pas OCL ni d'autres langages de contraintes, ne résout pas le métamodèle UML externe, ne valide pas la bonne formation UML/MOF, n'interprète pas les extensions fournisseur, ne déduit pas la sémantique d'héritage au-delà de l'enregistrement des références `general` et n'affirme aucune équivalence SACM–GovCheck. Le XML brut reste la source de vérité lorsque la représentation dérivée est incomplète ou ambiguë.

## 5. État des vérifications

La suite contient sept tests synthétiques couvrant l'indexation des constructions, les multiplicités de propriétés, les références d'associations/généralisations/contraintes, la documentation d'exporteur sans identifiant, les identifiants dupliqués, les références non résolues, le digest incorrect, le rejet des DTD/entités, les XML mal formés et la dérivation de la synthèse. Le workflow exécute également le parseur sur le téléchargement officiel réel et compare la synthèse générée à celle versionnée dans le dépôt. L'inventaire complet est publié avec la source brute et le manifeste de capture.

Ces tests établissent le comportement de cette implémentation Python sur les fixtures testées et lors de l'exécution sur la source épinglée. Ils ne constituent **pas** une preuve formelle que le parseur implémente correctement l'intégralité des standards XMI/UML ni que sa sortie est un modèle UML préservant la sémantique. Aucun théorème Lean ne relie actuellement la sortie du parseur Python à l'infoset XML source.

## 6. Non-revendications explicites et travaux suivants

Cet incrément ne :

- résout pas les contradictions PDF/XML connues de SACM 2.4 Beta 1 ;
- n'établit pas une interprétation complète du métamodèle SACM ni la conformité SACM 2.4 ;
- n'importe/exporte pas d'instances de dossiers d'assurance SACM ;
- ne prouve pas le raffinement du parseur vers Lean ou le métamodèle GovCheck ;
- ne génère aucune correspondance sémantique GovCheck opérationnelle ;
- n'adopte pas SACM 2.4 Beta 1 et n'en fait pas la base formelle.

La suite consiste à comparer l'inventaire structurel dérivé de la source à la vue PDF exacte et à la liste des conflits R-128, à classer chaque divergence par construction et portée affectées, puis seulement à définir des obligations de correspondance typées et spécifiques à chaque vue source. Les déclarations Lean Claim/Assertion/inférence existantes restent écrites manuellement ; cet inventaire ne les valide pas. Toute correspondance sémantique utilisée comme prémisse établie dans GovCheck doit être accompagnée d'une preuve de la relation exacte revendiquée.
