# SACM 2.4 Beta 1 — capture et ingestion source-native du métamodèle

**Statut :** candidat d'implémentation ; les octets source sont épinglés par le workflow d'ingestion, mais ceci ne constitue ni une conformité SACM ni un importateur d'instances SACM.  
**Date :** 13/11/2026.  
**Source officielle :** [page de spécification SACM de l'OMG](https://www.omg.org/spec/SACM), entrée de catalogue [R-197](../references.fr.md#r-197).  
**Tranche formelle liée :** [GovCheckCoherence.SACM24](../../formal/lean/GovCheckCoherence/SACM24.lean).

## 1. Artefact source et statut de version retenus

La première cible d'ingestion source-native est l'artefact du métamodèle lisible par machine et normatif de l'OMG :

| Champ | Valeur épinglée |
|---|---|
| Autorité | Object Management Group (OMG) |
| Spécification | Structured Assurance Case Metamodel (SACM) |
| Version | 2.4 Beta 1 |
| Statut de version | En cours de traitement / bêta informative |
| Référence formelle | SACM 2.3, octobre 2023 |
| Identifiant de fichier OMG | \`ptc/26-05-28\` |
| Chemin de révision source | \`SACM/20260504/SACM2.4_Metamodel.xml\` |
| Format natif | XML |
| Vue source | XML du métamodèle lisible par machine, normatif |
| Valeur SHA-256 de comparaison | \`0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830\` |

Le catalogue OMG identifie ce XML comme un **document normatif lisible par machine** pour la bêta 2.4. Le même catalogue identifie séparément le PDF de spécification comme texte normatif et le XMI du profil UML comme informatif. SACM 2.4 Beta 1 est en cours de traitement ; SACM 2.3 demeure la version formellement adoptée. Ces rôles de source ne doivent pas être confondus.

La valeur SHA-256 ci-dessus est la valeur de comparaison enregistrée par l'audit indépendant Assurance Forge ([R-128](../references.fr.md#r-128)). Le workflow GovCheck télécharge l'URL OMG versionnée et recalcule indépendamment le digest. GovCheck a vérifié indépendamment ce digest sur les octets téléchargés depuis l'URL officielle dans [l'exécution 43444619765](https://github.com/Martin-PB/govcheck/actions/runs/43444619765) : 524 243 octets source, SHA-256 `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`.

## 2. Pourquoi commencer par le XML du métamodèle

Le XML est la description lisible par machine du métamodèle, et non une instance de dossier d'assurance. C'est la bonne première cible d'ingestion parce qu'il fournit une source stable et adressable par version à partir de laquelle dériver l'inventaire des métaclasses, propriétés, associations, multiplicités, énumérations et contraintes.

Il n'établit **pas** un format portable d'échange d'instances. L'audit indépendant [R-128](../references.fr.md#r-128) signale des désaccords entre les vues PDF et XML de la bêta sur plusieurs constructions, et précise que le XMI disponible pour le profil UML est informatif et propre à un fournisseur. Ce travail ne prétend donc pas importer arbitrairement des instances de dossiers d'assurance SACM.

## 3. Contrat d'ingestion implémenté dans cette tranche

Exécution :

\`\`\`bash
curl --fail --location --proto '=https' --tlsv1.2 \\
  --output /tmp/SACM2.4_Metamodel.xml \\
  https://www.omg.org/spec/SACM/20260504/SACM2.4_Metamodel.xml
python scripts/ingest-sacm-metamodel.py \\
  --input /tmp/SACM2.4_Metamodel.xml \\
  --output-dir /tmp/govcheck-sacm-import
\`\`\`

L'importateur :

1. lit la source en octets et vérifie le SHA-256 attendu avant de créer une sortie ;
2. écrit la séquence exacte des octets source dans \`source.xml\`, sans parser puis resérialiser le document ;
3. crée un index XML dérivé des événements : noms qualifiés tels qu'ils apparaissent dans la source, attributs ordonnés, imbrication des éléments, texte, commentaires, instructions de traitement, frontières CDATA, offsets dans le document et positions ligne/colonne ;
4. enregistre l'autorité source, l'identifiant de fichier, l'URL datée, la vue source, le digest, l'heure de récupération, la longueur en octets et le format du parseur/index dans \`manifest.json\` ;
5. n'enregistre aucune correspondance sémantique par défaut.

La copie brute des octets fait autorité pour la fidélité. L'index des événements est un outil de navigation, pas un remplacement canonisé : les distinctions lexicales XML qui ne sont pas représentées dans l'index restent récupérables dans \`source.xml\`. La résolution des DTD/entités externes est désactivée ; l'importateur impose une limite d'entrée de 32 Mio.

Le workflow exécute cinq tests unitaires, télécharge l'artefact OMG exact, vérifie son digest, produit le manifeste et l'index de capture, puis publie le payload exact `source.xml` avec le manifeste et l'index structurel comme artefact de workflow conservé 90 jours. L'artefact de capture réussi est [sacm-2.4-beta1-source-capture](https://github.com/Martin-PB/govcheck/actions/runs/43444619765/artifacts/14046333134) (identifiant `14046333134`). Le payload source n'est pas copié dans l'historique Git : il reste disponible depuis l'URL OMG versionnée officielle.

## 4. Frontière de correspondance sémantique

Cette ingestion n'établit **aucune** correspondance entre une métaclasse SACM et une métaclasse GovCheck. Elle préserve le XML source natif et enregistre un tableau \`semanticMappings\` vide.

| Information source | Traitement actuel | Statut sémantique |
|---|---|---|
| Octets XML, déclaration d'encodage, préfixes, attributs, commentaires, instructions de traitement et texte | Conservés à l'identique dans \`source.xml\` ; événements structurels indexés séparément | Préservation de la source, pas correspondance sémantique |
| Noms des éléments/attributs et containment | Indexés comme événements XML qualifiés par la source | Observation structurelle seulement |
| Sens des métaclasses/propriétés/associations SACM | Non interprété par ce premier importateur | Contenu source non interprété |
| Désaccords PDF/XML | Conservés comme vues sources distinctes dans la recherche SACM et le modèle Lean existants | Conflit explicite ; aucune normalisation |
| Claim/Assertion/inférences SACM vers concepts d'assurance GovCheck | La tranche Lean existante reste un contrat d'interprétation fourni par l'autorité | Correspondance candidate ; non dérivée par cette ingestion XML |
| Autorité, cycle de vie, décisions et exigences GovCheck | Restent des concepts natifs GovCheck | Aucune équivalence automatique SACM |

La tranche Lean SACM 2.4 actuelle est un modèle formel écrit manuellement pour certaines obligations Claim/Assertion/inférences. Elle n'est pas générée à partir de ce XML et ne prouve pas qu'un parseur Python préserve la sémantique MOF/XMI du XML. L'importateur et le modèle Lean restent volontairement distincts tant qu'un inventaire du métamodèle dérivé de la source et une relation de raffinement du parseur n'existent pas.

Toute future correspondance sémantique opérationnelle devra toujours respecter le contrat général de correspondance GovCheck portant des preuves : sens source/cible exacts, révisions source et cible, portée et hypothèses, avec une preuve vérifiée par noyau de la relation précise revendiquée. Un digest XML prouve l'identité des octets relativement à l'hypothèse du hash ; il ne prouve pas une équivalence sémantique.

### 4.1 Correspondances typées existantes et frontière des preuves

Le dépôt contient déjà une tranche de mapping Lean écrite manuellement. Elle fournit des correspondances typées portant des preuves pour certains concepts SACM ; la nouvelle capture XML ne génère ni ne valide encore ces déclarations.

| Type/champ source SACM | Cible Lean GovCheck | Relation encodée | Déclaration vérifiée par noyau |
|---|---|---|---|
| `SACMClaim.identity` | `ClaimSemantics.claimId` | Préservation exacte de l'identifiant | `claim_interpretation_preserves_identity` |
| `SACMClaim.subject` | `SACMClaimInterpretation.mappedSubject` | Préservation exacte du sujet optionnel ; révision du modèle source épinglée | `claim_interpretation_preserves_subject`, `claim_subject_revision_is_pinned` |
| `AssertionDeclarationKind` | `ClaimDisposition` | Mapping injectif préservant les littéraux, contrôlé par la vue source sélectionnée | `mapAssertionDeclaration_injective`, `claim_interpretation_preserves_declaration` |
| `InferenceTypeKind.necessary` | `InferenceBridge` | Implication inverse : conclusion implique prémisse | `necessary_inference_is_reverse_entailment` |
| `InferenceTypeKind.sufficient` | `InferenceBridge` | Implication directe : prémisse implique conclusion | `sufficient_inference_is_forward_entailment` |
| `InferenceTypeKind.collective` | `InferenceBridge` | Équivalence des prémisses conjointes, avec ensemble non vide | `collective_inference_is_joint_equivalence` |
| `InferenceTypeKind.necessaryAndSufficient` | `InferenceBridge` | Équivalence dans les deux directions | Constructeur `InferenceBridge.necessaryAndSufficient` |
| `InferenceTypeKind.byRule` | `InferenceBridge` | Identité explicite de règle et preuve de sa conclusion | Constructeur `InferenceBridge.byRule` |
| `InferenceTypeKind.probable` | Aucun pont classique cible | Non pris en charge tant qu'une sémantique probabiliste n'est pas fournie | `probable_inference_has_no_classical_bridge` |

Ces interprétations sont typées sur le vocabulaire des vues sources transcrit manuellement ; elles ne constituent pas des résultats de conformité dérivés du parseur. L'importateur n'établit pas encore que les déclarations de métaclasses/propriétés du XML épinglé instancient ces types Lean. `Claim.value`, les valeurs/règles d'assertion et les autres packages SACM restent opaques ou non mappés. Les théorèmes prouvent uniquement les relations exactes énoncées dans leurs types ; ils ne prouvent ni la fidélité de l'interprétation d'un Claim en langage naturel, ni le raffinement du métamodèle SACM complet vers GovCheck.

## 5. Vérification et état d'acceptation

Les tests unitaires synthétiques couvrent :
- la préservation exacte des octets ;
- les noms d'éléments et d'attributs qualifiés par préfixe ;
- l'ordre des attributs ;
- les commentaires, instructions de traitement et frontières CDATA ;
- le rejet d'un digest différent avant création des sorties ;
- le rejet d'un XML mal formé ;
- le rejet des DTD externes ;
- l'absence explicite de correspondances sémantiques inférées.

Ces fixtures ne sont pas des exemples d'instances SACM OMG et n'établissent aucune conformité. Le workflow de capture a réussi sur le véritable XML OMG téléchargé pour la tête de PR (exécution 43444619765) ; le digest et la longueur en octets ci-dessus sont vérifiés par GovCheck pour cette URL/révision source exacte.

## 6. Inventaire structurel dérivé de la source

L'incrément d'ingestion suivant a maintenant produit un inventaire structurel XMI/UML lié à une révision précise. Voir le [rapport bilingue d'inventaire structurel](sacm-xmi-structural-inventory.fr.md) et la [synthèse révisable versionnée](../../formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json). Le parseur recense 1 616 identifiants XMI uniques, 121 classes UML, 121 associations, 355 propriétés, 167 généralisations, huit énumérations, 37 littéraux et 40 contraintes. Il comptabilise 1 371 références internes et 63 références externes, sans référence interne non résolue parmi les attributs reconnus. L'inventaire complet est produit dans l'artefact du workflow source. Cela reste une extraction structurelle, pas une interprétation sémantique UML/MOF ni une preuve de raffinement du parseur.

## 7. Non-revendications explicites et étape suivante

Cette tranche ne :
- interprète pas les classes, propriétés, associations, multiplicités, subsets, redefinitions ou contraintes MOF/XMI ;
- ne produit pas une interprétation sémantique complète du métamodèle SACM ;
- n'importe/exporte pas une instance de dossier d'assurance SACM ;
- n'effectue pas de round-trip d'un modèle d'instance ;
- ne mappe pas tous les concepts SACM vers GovCheck ;
- ne prouve pas de théorème de raffinement parseur-vers-Lean ;
- ne revendique ni conformité SACM 2.4 ni adoption normative.

L'incrément suivant consiste à comparer cet inventaire structurel dérivé de la source à la vue PDF exacte et à la liste des conflits R-128, à classer chaque divergence par construction et portée affectées, puis à dériver des obligations de correspondance typées et spécifiques à chaque vue source. Seules les correspondances dont la relation sémantique exacte est formellement démontrée pourront devenir des prémisses établies de GovCheck.
