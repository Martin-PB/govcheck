# SACM 2.4 Beta 1 — alignement des vues sources et registre des conflits

**Statut :** comparaison liée aux révisions de deux vues sources normatives distinctes ; aucune décision de priorité, aucun modèle canonisé, aucune revendication de conformité SACM ni correspondance sémantique GovCheck n'est établi.  
**Élément de travail :** [#73 — conformité des contrats intermodèles](https://github.com/Martin-PB/govcheck/issues/73).  
**Source du métamodèle :** [R-197](../references.fr.md#r-197), [inventaire XMI dérivé de la source](sacm-xmi-structural-inventory.fr.md).  
**Source du texte de spécification :** [R-198](../references.fr.md#r-198).  
**Audit indépendant des divergences :** [R-128](../references.fr.md#r-128).  
**Transcription formalisée :** `formal/lean/GovCheckCoherence/SACM24.lean`, espace de noms `GovCheck.Coherence.SACM24.SourceFacts`.

## 1. Périmètre et identité des sources

Le catalogue OMG répertorie le PDF de la spécification SACM 2.4 Beta 1 comme **document normatif** (identifiant `ptc/26-06-34`) et le XML du métamodèle lisible par machine comme **document normatif lisible par machine** (identifiant `ptc/26-05-28`). Ce sont deux artefacts et deux vues sources distincts, pas deux sérialisations que l'on pourrait fusionner silencieusement. Le catalogue répertorie aussi un XMI informatif du profil UML ([R-199](../references.fr.md#r-199)) ; il est volontairement exclu de cette comparaison normative PDF/XML et constitue une troisième vue source, à traiter séparément.

| Vue source | Identifiant OMG | URL officielle | SHA-256 | État actuel dans GovCheck |
|---|---|---|---|---|
| Texte, figures et annexes de la spécification (PDF) | `ptc/26-06-34` | <https://www.omg.org/spec/SACM/2.4/Beta1/PDF> | `25f32d1cd4bf32dfa9c92c7c1840e1a113b1e91c0e97252f6551878c39997ff5` | Vérifié par GovCheck dans le workflow [43496689208](https://github.com/Martin-PB/govcheck/actions/runs/43496689208) ; 9 019 601 octets ; conservé dans l'artefact [14072371021](https://github.com/Martin-PB/govcheck/actions/runs/43496689208/artifacts/14072371021) |
| Métamodèle lisible par machine (XML) | `ptc/26-05-28` | <https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml> | `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830` | Téléchargement indépendant et digest vérifié par GovCheck ; 524 243 octets |

Le digest PDF rapporté par R-128 a été recalculé indépendamment par GovCheck sur le téléchargement officiel dans le workflow [43496689208](https://github.com/Martin-PB/govcheck/actions/runs/43496689208) : 9 019 601 octets et SHA-256 exact ci-dessus. L'artefact de 90 jours [14072371021](https://github.com/Martin-PB/govcheck/actions/runs/43496689208/artifacts/14072371021) contient le PDF, le XML exact, le manifeste des vues sources et l'inventaire XMI généré. Le workflow n'extrait ni n'interprète automatiquement le texte PDF.

SACM 2.4 Beta 1 reste une version en cours/de nature informative ; SACM 2.3 demeure la version formelle. Le fait que le catalogue OMG classe le PDF et le XML comme artefacts normatifs ne résout pas leurs contradictions.

## 2. Registre des conflits

Le tableau enregistre les affirmations à la granularité réelle de leurs fragments sources. « Non indiqué dans le texte PDF » ne signifie volontairement pas « interdit par le PDF » : des diagrammes, annexes ou autres fragments peuvent apporter cette information.

| Sujet | Fragment source PDF | Vue source XML du métamodèle | Classification | Théorème(s) Lean sur les faits source |
|---|---|---|---|---|
| Identité d'élément | Clause 9.2 : `gid : String[0..1]` ; Figure 9.1 : `elementId` | `elementId : UID[1]`, sans `gid` | **Conflit interne au PDF et entre ses fragments et le XML.** Une règle d'identité globale au PDF n'est pas fondée. | `pdf_identity_fragments_disagree` ; `pdf_clause9_2_uses_gid` ; `pdf_figure9_1_uses_elementId` ; `xml_model_uses_elementId` |
| Littéraux de déclaration d'assertion | Clause 13.6 : `axiomatic`, `assumed`, `asserted`, `needsSupport` ; Annexe G.6 point 6 : trois littéraux ; clause 15.2.1 : `byRule` | `axiomatic`, `assumed`, `asserted`, `byRule` | **Conflit interne au PDF** ; le XML concorde avec la clause 15.2.1 pour `byRule`, mais pas avec la clause 13.6. | `pdf_assertion_declaration_fragments_disagree` ; théorèmes sur les littéraux par fragment |
| `Claim.value` | Figure normative 13.1 (page imprimée 41) : `MultiLangString` ; figure informative 15.1.1 (page imprimée 59) : `ExpressionLangString` | `ExpressionLangString` | **Conflit interne au PDF.** Le XML concorde avec la figure informative et diffère de la figure normative. La valeur `MultiLangString` rapportée par R-128 est confirmée par la figure 13.1 ; son localisateur exact à la clause 13.9 reste à vérifier. | `pdf_normative_figure13_1_vs_informative_figure15_1_1_claim_value_conflict` ; `pdf_normative_figure13_1_vs_xml_claim_value_conflict` ; `claim_value_type_agrees_in_informative_pdf_figure15_1_1_and_xml` ; `r128_reported_claim_value_type_matches_normative_pdf_figure13_1` |
| Multiplicité de `AssertedEvidence.evidence` | Clause 13.13 : `[0..*]` | `[1..*]` | **Conflit de multiplicité.** L'admissibilité d'une collection vide diffère. | `asserted_evidence_multiplicity_conflict` |
| Héritage de `BindingPackage` | Les clauses 10.5 et 11.3 donnent des superclasses différentes | `ScopedPackage` et `SACMPackageWithBinding` | **Conflit interne au PDF** ; le XML concorde avec la clause 10.5, pas avec la clause 11.3. | `binding_package_pdf_fragments_conflict` ; `xml_binding_package_matches_pdf_clause10_5` |
| Multiplicité de `SACMElement.abstraction` | Clause 9.2 : `[0..1]` | `[0..*]` | **Conflit de multiplicité.** | `sacm_element_abstraction_multiplicity_conflict` |
| Multiplicité de `AssertedRelationship.isCounter` | Clause 13.11 : `Boolean[1]` | `Boolean[0..1]` | **Conflit de multiplicité/obligation de présence.** | `asserted_relationship_isCounter_multiplicity_conflict` |
| Héritage de `SACMModel` | Clause 9.10 : `ModelElement` ; l'annexe G.6 point 5 ajoute `Assertion` et `Assessment` | `ModelElement`, `Assertion`, `Assessment` | **Conflit interne au PDF** ; le XML concorde avec le fragment de l'annexe. | `sacm_model_pdf_fragments_differ` ; `xml_sacm_model_matches_pdf_annex_g6` |
| Héritage de `SACMDependency` | Clause 9.11 : `DirectedRelationship` | Le XML déclare également `BaseElement` | **Ajout XML par rapport à la clause PDF citée**, pas preuve que le PDF l'interdit globalement. | `sacm_dependency_xml_adds_base_element` |
| Héritage de `Rule` | Clause 15.2.3 : `BaseElement` | Le XML déclare `ModelElement` et `BaseElement` | **Ajout XML par rapport à la clause PDF citée.** | `rule_xml_adds_model_element` |
| Nom de la propriété de règle d'assertion | Le PDF utilise `assertionRule` | Le XML utilise `assertionDeclarationRule` | **Divergence de nom de propriété.** Un mapping de renommage nécessite un contrat explicite. | `assertion_rule_feature_name_differs` |
| `Claim.subject` et `Claim.whole` | Non indiqués dans la vue textuelle PDF examinée | Le XML déclare des propriétés multivaluées | **Non indiqué versus présent**, pas contradiction établie. L'omission du texte PDF ne prouve pas l'absence dans tous les diagrammes/annexes. | `claim_subject_is_xml_addition_over_pdf_text` ; `claim_whole_is_xml_addition_over_pdf_text` |

Les 12 entrées de comparaison incluent le conflit Claim.value entre les figures normative et informative du PDF et le XML. La figure 13.1 confirme la valeur MultiLangString rapportée par R-128, tandis que le localisateur exact de la clause 13.9 reste à vérifier. Le registre préserve les constats de l'audit R-128 tout en ajoutant les distinctions par fragment déjà représentées dans Lean. Le tableau est un relevé comparatif, pas une décision d'erratum de l'OMG. La transcription exacte des fragments PDF reste une tâche de preuve révisable ; le digest authentifie les octets, pas la justesse d'une transcription humaine.

## 3. Frontière de la formalisation

Le module Lean distingue :
- les valeurs documentaires `SourceView` (texte/PDF de spécification versus XML normatif du métamodèle) ;
- les valeurs `DeclarationSourceFragment` pour la clause PDF 13.6, le point 6 de l'annexe G.6, la clause 15.2.1 et le XML ;
- les valeurs `IdentitySourceFragment` pour la clause PDF 9.2, la figure 9.1 et le XML.

Une `SACMClaimInterpretation` doit rattacher ses fragments de déclaration et d'identité à la vue documentaire sélectionnée, préserver les champs source exacts et conserver la révision du modèle source. Cela empêche de supposer un champ d'identité ou un ensemble de déclarations global au PDF alors que le PDF contient lui-même des fragments incompatibles.

Les théorèmes `SourceFacts` de Lean prouvent que les **constantes transcrites** diffèrent ou concordent comme indiqué. Ils ne prouvent pas que la transcription représente fidèlement le PDF/XML. Le noyau de preuve vérifie les dérivations Lean à partir de ces constantes ; il n'authentifie pas les citations sources. Le rapport d'axiomes mis à jour audite explicitement les théorèmes sur les faits sources, mais cet audit attend encore l'exécution du workflow de la PR.

## 4. Règles de traitement pour l'intégration actuelle

1. Préserver le PDF et le XML comme artefacts sources distincts et identifiés indépendamment.
2. Rattacher chaque affirmation à une clause, figure, point d'annexe ou métaclasse/propriété XML précise, pas seulement à une étiquette documentaire.
3. Représenter les désaccords comme des conflits de première classe avec les deux valeurs source, localisateurs, révisions et provenance.
4. Ne pas choisir une source gagnante, corriger un artefact OMG ni normaliser les valeurs sans décision explicite autorisée.
5. Ne pas traiter l'absence dans un passage textuel comme preuve d'absence dans l'intégralité du PDF.
6. Garder les mappings partiels et qualifiés par vue source. Un mapping dépendant d'un fait contesté ne peut devenir une prémisse établie tant que sa relation sémantique exacte n'est pas prouvée.
7. Conserver SACM 2.3 comme référence formelle de conformité. Ne pas annoncer d'import/export d'instances ni de conformité SACM 2.4 Beta 1.

## 5. Vérification et limites restantes

La capture XML et l'inventaire structurel sont vérifiés indépendamment par workflow (12 tests Python ; digest XML officiel ; inventaire généré comparé à la synthèse versionnée ; source brute et inventaire complet publiés). Le téléchargement PDF et son contrôle SHA-256 par rapport à la valeur épinglée par R-128 ont également réussi ; le manifeste enregistre les deux identités, digests et longueurs, et l'artefact combiné a été publié. Lean 4.19.0 a compilé le modèle de fragments sources dans [l'exécution 43496689323](https://github.com/Martin-PB/govcheck/actions/runs/43496689323) sur le candidat de fusion `af19d63` ; l'audit a couvert 43 déclarations sous GovCheckCoherence.Proofs, toutes dans la liste d'axiomes autorisés (quatre théorèmes wrappers de fragments sources utilisent propext ; aucun axiome non autorisé n'a été signalé). Les théorèmes SourceFacts affichés directement ne dépendent d'aucun axiome.

Ne sont toujours pas démontrés :
- l'exactitude et l'exhaustivité des transcriptions PDF-vers-Lean et XML-vers-Lean ;
- la sémantique UML/MOF complète ou le raffinement du parseur entre l'infoset XML et un modèle source formel ;
- une correspondance sémantique dérivée de la source vers le métamodèle GovCheck ;
- la résolution ou la priorité des conflits sources ;
- l'échange d'instances, le comportement aller-retour ou la conformité SACM 2.4.

Aucune adoption normative n'est proposée par cet incrément de recherche. L'issue #73 reste ouverte.
