# SACM 2.4 Beta 1 — alignement des vues source et inventaire des conflits

**Statut :** comparaison des vues source et modélisation des conflits au niveau des fragments ; aucune règle de priorité ni revendication de conformité SACM 2.4 n'est adoptée.  
**Audit indépendant d'implémentation :** [R-128](../references.fr.md#r-128).  
**XML normatif du métamodèle :** [R-197](../references.fr.md#r-197).  
**PDF normatif :** [R-198](../references.fr.md#r-198).  
**XMI informatif du profil UML :** [R-199](../references.fr.md#r-199).  
**Inventaire structurel :** [rapport d'inventaire XMI](sacm-xmi-structural-inventory.fr.md) et [synthèse versionnée](../../formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json).  
**Modèle formel des fragments source :** [`GovCheckCoherence.SACM24`](../../formal/lean/GovCheckCoherence/SACM24.lean).

## 1. Séparer les artefacts

Le catalogue OMG expose plusieurs artefacts SACM 2.4 Beta 1 distincts. Ils ne sont pas des représentations interchangeables d'un schéma unique déjà résolu :

| Vue source | Identifiant OMG | Chemin source exact | Autorité/statut | Provenance du SHA-256 |
|---|---|---|---|---|
| PDF normatif de spécification | `ptc/26-06-34` | `SACM/20260504/SACM2.4.pdf` | Texte et figures de la spécification normative | `25f32d1cd4bf32dfa9c92c7c1840e1a113b1e91c0e97252f6551878c39997ff5`, rapporté par l'audit indépendant R-128 ; pas encore recalculé indépendamment par GovCheck |
| XML normatif du métamodèle lisible par machine | `ptc/26-05-28` | `SACM/20260504/SACM2.4_Metamodel.xml` | Métamodèle normatif lisible par machine | `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`, vérifié par GovCheck sur 524 243 octets téléchargés |
| XMI informatif du profil UML | `ptc/26-05-21` | `SACM/20260504/SACM2.4_Profile.xmi` | Artefact de profil informatif, distinct du XML normatif du métamodèle | `9149a0414628e1b70c1f7c2235f5180c64e7a144601eb2ae78d539681918838b`, rapporté par R-128 |
| PDF informatif des changements | `ptc/26-06-35` | `SACM/20260504/SACM2.4_Changes.pdf` | Synthèse informative des changements | `6840a0f67104d07997168d07079c0e168f5ac65ef5fa1779eccb9ebef1fe5f96`, rapporté par R-128 |

Les trois derniers digests proviennent du script de téléchargement épinglé de l'audit indépendant. GovCheck n'a vérifié indépendamment que le digest XML. Le PDF compte 161 pages ; R-128 rapporte une couverture d'extraction textuelle d'environ 98 % et avertit que les libellés présents uniquement dans les diagrammes nécessitent une inspection visuelle. Une déclaration absente du texte PDF extrait doit donc être enregistrée comme omission dans cette vue textuelle, pas automatiquement comme preuve qu'aucun diagramme ne la contient.

## 2. Matrice des conflits et omissions

Le tableau conserve la portée de chaque fragment source. « PDF » ne désigne jamais un ensemble unique et cohérent de revendications lorsque le PDF se contredit lui-même.

| Concept / propriété | Déclaration du PDF normatif | Déclaration du métamodèle XML normatif | Classification | Effet sur la tranche Lean actuelle |
|---|---|---|---|---|
| Identité de `SACMElement` | Clause 9.2 : `gid : String[0..1]` ; Figure 9.1 : `elementId : UID[1]` | `elementId : UID[1]` | **Conflit interne au PDF** ; le XML concorde avec la figure, pas avec le texte de la clause | La preuve d'identité doit citer un fragment clause/figure. Une règle PDF globale « gid » est invalide. |
| `Claim.value` | Clause 13.9 : `MultiLangString[0..1]` | `ExpressionLangString[0..1]` | **Conflit direct de type** | Conserver le libellé de type source et le payload brut ; ne convertir aucun des deux en proposition GovCheck ni en simple chaîne. |
| `Claim.subject` | Non indiqué dans la vue de prose PDF extraite | `SACMElement[0..*]` | **Ajout XML / omission du texte PDF** ; pas de contradiction directe | `Option (List ...)` distingue une propriété absente d'une propriété présente vide ou multivaluée. Aucun mapping PDF n'est inféré. |
| `Claim.whole` | Non indiqué dans la vue de prose PDF extraite | `SACMModel[0..*]` | **Ajout XML / omission du texte PDF** | Conserver séparément la propriété XML ; ne fabriquer aucune valeur PDF. |
| `AssertionDeclarationKind` | Clause 13.6 / Figure 13.1 inclut `needsSupport` ; Annexe G.6 point 6 ne liste que `axiomatic`, `assumed`, `asserted` ; la clause 15.2.1 ajoute `byRule` | `axiomatic`, `assumed`, `asserted`, `byRule` | **Conflit interne au PDF entre fragments** ; le XML concorde avec l'extension de la clause 15, pas avec la liste de la clause 13 | Les preuves de déclaration sont liées à un fragment précis clause/annexe/XML. Ni `needsSupport` ni `byRule` n'est rejeté pour l'ensemble du document PDF. |
| Multiplicité de `AssertedEvidence.evidence` | Clause 13.13 : `ArtifactReference[0..*]` | `ArtifactReference[1..*]` | **Conflit direct de multiplicité** | Pas encore représenté dans la tranche Claim actuelle ; nécessite un mapping de relation distinct. |
| Multiplicité de `SACMElement.abstraction` | Clause 9.2 : `SACMElement[0..1]` | `SACMElement[0..*]` | **Conflit direct de multiplicité** | Pas encore mappé. Ne pas réduire une relation XML multivaluée à une référence optionnelle unique. |
| Multiplicité de `AssertedRelationship.isCounter` | Clause 13.11 : `Boolean[1]` | `Boolean[0..1]` | **Conflit direct de multiplicité** | Pas encore mappé ; absence et faux explicite ne doivent pas être confondus. |
| Héritage de `BindingPackage` | Clause 10.5 : `ScopedPackage` et `SACMPackageWithBinding` ; clause 11.3 : `ModelElement` | `ScopedPackage` et `SACMPackageWithBinding` | **Conflit interne au PDF** ; le XML concorde avec la clause 10.5 | Ne pas choisir silencieusement une clause PDF. |
| Héritage de `SACMModel` | Clause 9.10 : `ModelElement` ; l'annexe G.6 point 5 ajoute `Assertion` et `Assessment` | `ModelElement`, `Assertion`, `Assessment` | **Différence entre fragments PDF / extension de l'annexe** ; le XML concorde avec l'annexe G.6 | Conserver la clause et l'annexe comme revendications distinctes ; aucun ensemble de superclasses aplati pour l'instant. |
| Héritage de `SACMDependency` | Clause 9.11 : `DirectedRelationship` | `DirectedRelationship` et `BaseElement` | **Ajout XML par rapport au texte de la clause PDF** | Pas encore mappé. |
| Héritage de `Rule` | Clause 15.2.3 : `BaseElement` | `ModelElement` et `BaseElement` | **Ajout XML par rapport au texte de la clause PDF** | Pas encore mappé. |
| Nom de la propriété de règle d'assertion | Le texte/diagramme PDF utilise `assertionRule` | La propriété XML est `assertionDeclarationRule` | **Divergence de nom de propriété** ; identité sémantique non établie | Conserver les noms et provenances séparés tant que le mapping n'est pas prouvé. |
| `InferenceTypeKind` | Les six littéraux sont décrits dans plusieurs fragments PDF | Le XML contient `probable`, `collective`, `necessary`, `sufficient`, `necessaryAndSufficient`, `byRule` | Aucun conflit d'ensemble de littéraux identifié par l'audit actuel | L'ensemble de littéraux seul ne prouve pas la sémantique d'entailment Lean. |

**Précaution sur les multiplicités :** l'inventaire XMI conserve les nœuds littéraux et leurs attributs XML explicites ; il n'applique pas actuellement les valeurs par défaut UML pour normaliser les attributs `LiteralInteger.value` omis ou l'absence de nœuds de borne supérieure/inférieure. Les cardinalités ci-dessus sont les lectures normalisées consignées par l'audit indépendant R-128. Elles ne sont pas présentées comme mécaniquement prouvées par le parseur Python d'inventaire.

## 3. Correction de la première tranche Lean

La formalisation Claim/Assertion précédente traitait `specificationText` comme une vue PDF cohérente unique et rejetait donc `byRule` pour la vue PDF. C'était trop grossier : le même PDF ajoute `byRule` dans la clause 15.2.1 tandis qu'un autre fragment inclut `needsSupport`. Le PDF donne également des champs d'identité contradictoires entre la clause 9.2 et la figure 9.1.

Le modèle Lean utilise désormais des preuves au niveau des fragments :

- `DeclarationSourceFragment` distingue la clause PDF 13.6, l'annexe G.6 point 6, la clause 15.2.1 et le modèle XML normatif.
- `IdentitySourceFragment` distingue la clause PDF 9.2, la figure PDF 9.1 et le modèle XML.
- Un Claim mappé doit citer les fragments exacts de déclaration et d'identité utilisés ; un simple libellé de document ne suffit pas.
- `SACMClaim.subject` est `Option (List SACMElementRef)` : `none` signifie que la vue source sélectionnée ne déclare pas la propriété ; `some []` signifie que la propriété existe mais ne contient aucune valeur ; une liste non vide préserve plusieurs sujets.
- La présence de la déclaration est optionnelle et sa valeur par défaut effective est modélisée séparément comme `asserted`.
- Une valeur Claim brute conserve un libellé de type source et un payload ; les valeurs d'assertion, références de règles et forces sont conservées comme listes de références opaques.
- Le mapping source vers GovCheck reste partiel : il exige une identité non vide et une preuve de mapping explicite. Ce n'est pas un encodage complet des objets SACM.

Les théorèmes Lean prouvent l'injectivité du mapping déclaration/disposition et les différences entre les **faits transcrits des fragments** (ensembles de déclarations, champs d'identité, multiplicités, listes d'héritage et noms de propriétés). Ils ne prouvent ni l'exactitude de la transcription PDF/XML, ni le raffinement sémantique du parseur Python XMI, ni que le pont d'inférence abstrait exprime la sémantique voulue par SACM.

## 4. Frontière d'autorité et de normalisation

Aucune règle de priorité n'est adoptée entre le PDF normatif et le XML normatif du métamodèle. Les deux artefacts restent disponibles comme revendications versionnées séparément. Un conflit peut être :
- interne à un document (clause PDF contre annexe/figure) ;
- entre le PDF et le XML ;
- un ajout ou une omission plutôt qu'une contradiction directe ;
- une différence de nom dont l'identité sémantique n'est pas établie ;
- non résolu parce qu'un diagramme ou une référence externe n'a pas été interprété.

GovCheck doit préserver ces distinctions, les emplacements source exacts, les révisions source et la relation revendiquée. Une vue normalisée, si elle devient nécessaire, doit être une transformation distincte, versionnée, avec pertes déclarées et décision explicite autorisée. Elle ne doit pas écraser les revendications sources.

## 5. Obligations de preuve et d'implémentation restantes

1. Vérifier le digest du PDF normatif par un téléchargement contrôlé par GovCheck, et pas seulement par l'enregistrement indépendant R-128.
2. Parser et inventorier le XMI informatif du profil UML comme artefact source distinct ; ne pas le fusionner avec le XML normatif du métamodèle.
3. Ajouter une interprétation des valeurs par défaut UML/multiplicités dérivées de la source, avec provenance explicite de la sémantique UML utilisée.
4. Prouver le raffinement du parseur ou vérifier indépendamment les faits structurels générés avant de les traiter comme prémisses formelles.
5. Construire un mapping Claim/Assertion typé et spécifique à chaque vue source, préservant types, multiplicités, valeurs par défaut et provenance ; prouver chaque relation revendiquée.
6. Ajouter des mappings typés distincts pour AssertedEvidence, AssertedRelationship, SACMElement, les packages, l'héritage des modèles et Rule ; conserver les faits non résolus/contradictoires comme propositions non opérationnelles.
7. Conserver SACM 2.3 comme référence formelle de conformité. SACM 2.4 Beta 1 reste une entrée de recherche ; aucune conformité 2.4 ni adoption normative n'est revendiquée.

L'issue #73 reste ouverte. Ce rapport et son modèle Lean de fragments sont un incrément d'ingénierie/recherche, pas une décision d'autorité.
