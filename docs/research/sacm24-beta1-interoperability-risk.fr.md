# SACM 2.4 Beta 1 — risque d'interopérabilité et de cohérence des sources

**Statut :** audit indépendant d'implémentation enregistré ; garde-fous de sélection de vue source ajoutés à GovCheck ; aucune revendication de conformité SACM 2.4.  
**Date :** 2026-11-12.  
**Catalogue principal :** [R-73 — OMG SACM 2.4 Beta 1](../references.fr.md#r-73).  
**Audit indépendant :** [R-128 — Audit d'impact SACM 2.4 Beta 1 d'Assurance Forge](../references.fr.md#r-128).

## 1. Constat déterminant

SACM 2.4 Beta 1 ne doit pas être traité comme un modèle d'échange unique et stable, prêt à implémenter. La page OMG qualifie la bêta de version en cours/de nature informative et SACM 2.3 reste la spécification formelle. Un audit indépendant d'Assurance Forge indique que la bêta ne fournit pas encore de contrat d'échange natif exploitable (pas de namespace/XSD/Ecore stable, d'implémentation de référence ni de fichiers natifs externes) et que le texte PDF de la spécification contredit le métamodèle XML lisible par machine sur plusieurs points structurels.

Le rapport Assurance Forge ne fait pas autorité pour l'OMG et ses conclusions doivent être vérifiées contre les artefacts OMG épinglés. Il s'agit néanmoins d'un audit d'ingénierie concret, avec script de téléchargement reproductible, empreintes des artefacts, outil de comparaison du modèle et analyse d'impact d'implémentation. C'est un élément suffisant pour **interdire toute revendication selon laquelle GovCheck prend actuellement en charge ou respecte SACM 2.4 Beta 1 comme format cohérent unique**.

## 2. Contradictions texte/modèle rapportées par l'audit indépendant

| Sujet | Texte PDF de la spécification | XML du métamodèle lisible par machine | Conséquence |
|---|---|---|---|
| Identité d'élément | `gid : String[0..1]` | `elementId : UID[1]`, sans `gid` | Impossible de normaliser l'identité sans sélectionner une vue source et enregistrer la transformation |
| Littéraux de déclaration | `axiomatic`, `assumed`, `asserted`, `needsSupport` | `axiomatic`, `assumed`, `asserted`, plus `byRule`, sans `needsSupport` | Le même nom d'énumération possède des ensembles de valeurs incompatibles |
| Multiplicité de `AssertedEvidence.evidence` | `[0..*]` | `[1..*]` | Une collection vide est valide dans une vue et invalide dans l'autre |
| `Claim.value` | `MultiLangString` | `ExpressionLangString` | Texte et expression typée ne sont pas interchangeables |
| Héritage de `BindingPackage` | Les clauses textuelles divergent sur les superclasses | Le XML déclare `ScopedPackage` et `SACMPackageWithBinding` | Le parseur/validateur peut construire une hiérarchie de types différente |
| Multiplicité de `SACMElement.abstraction` | `[0..1]` | `[0..*]` | Une vue autorise au plus une abstraction, l'autre plusieurs |
| Multiplicité de `AssertedRelationship.isCounter` | `Boolean[1]` | `Boolean[0..1]` | Le caractère obligatoire diffère |

L'audit signale aussi des noms obsolètes de SACM 2.3 dans le texte/les annexes de la bêta, des littéraux supprimés encore référencés dans l'annexe C, une ambiguïté sur les points de conformité et un exemple XMI de profil UML propre à un éditeur. Consulter l'audit épinglé complet et son inventaire de défauts lié avant toute implémentation supplémentaire.

## 3. Ce que l'audit dit de l'interopérabilité

L'audit distingue le XML du métamodèle lisible par machine publié par l'OMG d'un format d'instance interopérable :

- La page OMG Beta 1 publie un artefact XML normatif du métamodèle, mais l'audit ne trouve pas de namespace XMI 2.4 stable ni de contrat XSD/Ecore pour l'échange natif d'instances.
- L'exemple XMI de profil UML disponible utilise un namespace MagicDraw spécifique à un éditeur et ne constitue pas un format portable d'instance SACM 2.4.
- Aucun fichier natif 2.4 indépendant ni aucune implémentation de référence n'étaient disponibles pour constituer un corpus d'interopérabilité à la date de l'audit.
- Le script de téléchargement épingle quatre artefacts OMG officiels et leurs empreintes SHA-256 ; l'audit indique que la bêta peut être republiée au même emplacement, ce qui rend les références non épinglées dangereuses.

Il ne s'agit pas d'affirmer que le fichier XML de l'OMG est invalide. Il faut distinguer un artefact de métamodèle lisible par machine d'un contrat de sérialisation stable et portable pour les dossiers d'assurance gouvernés.

## 4. Empreintes des artefacts épinglées par l'audit

Le script de récupération d'Assurance Forge enregistre les empreintes SHA-256 suivantes pour les quatre artefacts OMG Beta 1 officiels téléchargés le 02/10/2026. GovCheck n'a pas encore retéléchargé ces fichiers ni recalculé leurs empreintes de manière indépendante ; il s'agit de valeurs de comparaison, pas d'empreintes vérifiées par GovCheck.

| Artefact OMG | Identifiant de fichier | SHA-256 rapporté par Assurance Forge |
|---|---|---|
| PDF de spécification | ptc/26-06-34 | `25f32d1cd4bf32dfa9c92c7c1840e1a113b1e91c0e97252f6551878c39997ff5` |
| PDF de spécification avec barres de modification | ptc/26-06-35 | `6840a0f67104d07997168d07079c0e168f5ac65ef5fa1779eccb9ebef1fe5f96` |
| XML du métamodèle | ptc/26-05-28 | `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830` |
| XMI du profil UML | ptc/26-05-21 | `9149a0414628e1b70c1f7c2235f5180c64e7a144601eb2ae78d539681918838b` |

## 5. Réponse de GovCheck : mapping qualifié par la vue source

Le module Lean `GovCheckCoherence.SACM24` a été renforcé pour empêcher la fusion silencieuse des deux vues contradictoires :

- `SourceView` distingue `specificationText` de `normativeMetamodelXML`.
- `AssertionDeclarationKind` conserve l'union des deux ensembles de valeurs, dont `needsSupport` et `byRule`.
- `declarationSupportedBySourceView` rejette `byRule` lorsque la vue du texte PDF est sélectionnée et rejette `needsSupport` lorsque la vue du métamodèle XML est sélectionnée.
- `ElementIdentityField` préserve `gid` et `elementId) ; la vue source détermine le champ attendu.
- `SACMClaimInterpretation` exige des preuves que le littéral de déclaration et le champ d'identité sont cohérents avec la vue source sélectionnée, et lie tout sujet explicite à la révision exacte du modèle source.
- `SACMClaimMapping` compose cette interprétation source avec le pont sémantique général `EvidenceMapping` de GovCheck.

Ces garde-fous formalisent les deux conflits pertinents pour la tranche Claim/Assertion actuelle. Ils ne résolvent pas les autres conflits de multiplicité, de type de valeur ou d'héritage et n'établissent pas la conformité à l'une ou l'autre vue source complète.

## 6. Politique de traitement requise

Tant que l'OMG n'a pas publié une version formelle stable de SACM 2.4 ou une bêta dotée d'un contrat de sérialisation cohérent :

1. **Conserver SACM 2.3 comme référence formelle de conformité.** Ne pas modifier les schémas, fixtures, validateurs ou revendications de conformité 2.3 pour les adapter à la bêta.
2. Traiter SACM 2.4 Beta 1 comme une source de recherche uniquement. Ne pas annoncer d'import/export natif 2.4.
3. Épingler chaque artefact source par URL, identifiant de publication/fichier, date de récupération et empreinte cryptographique. Enregistrer si le mapping lit le texte PDF, le métamodèle XML normatif ou le XMI informatif du profil UML.
4. Préserver les champs et valeurs contradictoires dans leur vue source. Toute normalisation doit être une transformation explicite et versionnée, avec pertes déclarées et décision autorisée.
5. Ne pas inventer de namespace XMI, XSD, Ecore ou profil d'échange. Attendre un contrat officiel ou interopérable et de vrais fichiers d'instance externes.
6. Garder le modèle 2.4 et toute future matrice de conformité séparés de 2.3. Une implémentation ultérieure doit être additive et distribuée par version, pas un remplacement silencieux.

## 7. Prochain travail de vérification

- Obtenir et épingler les quatre artefacts OMG Beta 1 avec les URL officielles et comparer leurs empreintes à celles enregistrées par l'audit indépendant.
- Exécuter le diff structurel texte/XML de GovCheck et étendre le modèle Lean source-view aux autres conflits : multiplicité AssertedEvidence, type de Claim.value, héritage BindingPackage, multiplicité abstraction et multiplicité isCounter.
- Construire des fixtures négatives où la vue source et la déclaration/l'identité/multiplicité divergent ; chaque cas doit être rejeté ou explicitement représenté comme conflit.
- Seulement lorsqu'un format d'instance portable et des fichiers d'exemple existeront, construire un corpus de tests aller-retour d'import/export natif.
- Revoir le mapping lorsque l'OMG publiera Beta 2 ou la spécification formelle SACM 2.4.

**Conclusion :** le premier mapping Claim/Assertion SACM est utile précisément parce qu'il expose les contradictions de la bêta au lieu de les masquer. Il formalise une frontière entre vues sources, pas une déclaration de prise en charge de SACM 2.4.
