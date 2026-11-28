# Prototype de cohérence Lean

**Statut :** première tranche expérimentale ; ce document ne constitue pas un métamodèle GovCheck adopté.

## Périmètre

Ce paquet formalise les premiers invariants de cohérence des preuves et un contrat de correspondance intermodèle porteur de preuve. Il conserve `EvidenceMethodClass`, `EvidenceKind` et `EvidenceStatus` comme trois dimensions distinctes. Le vocabulaire Lean reprend les valeurs `methodClass` du schéma de preuve GovCheck existant et les valeurs de statut de résultat, tout en maintenant explicite et séparée la nature épistémique.

Cette distinction est importante : un enregistrement étiqueté avec la classe de méthode `theorem-proving` et le statut `passed` ne constitue pas, par ces seules étiquettes, une dérivation authentifiée et vérifiée par un noyau. Une exécution de test au statut `passed` demeure un témoignage ; un résultat de model checking demeure un élément de preuve issu du model checking. La fraîcheur et la péremption sont calculées séparément et ne sont pas confondues avec le statut de résultat du schéma source. Le vocabulaire des classes de méthodes du schéma source est représenté directement par `EvidenceMethodClass` ; la nature épistémique constitue une interprétation d'assurance supplémentaire, et non un enum de remplacement.

Le premier module n'importe volontairement aucun module CSLib. Cela isole la proposition et fournit une base de comparaison pour de futures définitions candidates de CSLib. Cela ne signifie ni que CSLib serait inadapté, ni que l'obligation d'assurance portant sur les correspondances critiques serait facultative.

`EvidenceKind` dans Lean est une interprétation sémantique supplémentaire : le `evidence-record.schema.json` actuellement utilisé en production contient `method.methodClass` et `result.status`, mais aucun champ explicite de nature épistémique ni objet typé de dérivation vérifiée par noyau. L'enregistrement Lean n'est donc pas une projection sans perte du schéma JSON actuel. Les fixtures de `fixtures/` sont volontairement des fixtures sémantiques minimales, **et non** des enregistrements de production complets valides au regard du schéma JSON. Le théorème `schema_method_and_status_do_not_determine_epistemic_kind` construit deux interprétations sémantiques ayant la même classe de méthode et le même statut, mais des natures épistémiques différentes ; il constitue un contre-exemple formel à l'inférence de la nature épistémique à partir des seules dimensions du schéma actuel. Voir le contrat bilingue du prototype pour cette lacune de décision identifiée dans les issues #73/#79.

## Chaîne d'outils et commandes

Chaîne d'outils épinglée : Lean 4.19.0.

Depuis ce répertoire :

```sh
lake env lean GovCheckCoherence.lean
lake build
```

## Tranche sémantique SACM 2.4 Beta 1

`GovCheckCoherence.SACM24` préserve les distinctions entre déclarations d'assertions SACM, lie les sujets explicites des Claims aux révisions exactes des modèles et donne un type à la direction des inférences. Le type d'inférence `probable` ne dispose d'aucun pont vers l'implication classique ; `byRule` exige un terme de preuve concret. Les garde-fous relatifs aux vues sources — texte PDF versus XML du métamodèle, notamment `needsSupport`/`byRule` et `gid`/`elementId` — ont passé le même audit des axiomes. Voir le [rapport de risque d'interopérabilité SACM Beta 1](../../docs/research/sacm24-beta1-interoperability-risk.fr.md). Les treize théorèmes publics de correspondance SACM ont passé le build Lean 4.19.0 épinglé et l'audit des axiomes dans [l'exécution 43216879988](https://github.com/Martin-PB/govcheck/actions/runs/43216879988), sans axiome. Voir l'[étude de correspondance SACM 2.4](../../docs/research/sacm24-claim-inference-mapping.fr.md).

## Sémantique des multiplicités UML 2.5

`GovCheckCoherence.UML25Multiplicity` formalise un sous-ensemble volontairement limité des règles UML 2.5 utilisées par la source XMI SACM 2.4 Beta 1. Il démontre le repli à 1 lorsque les spécifications de valeurs inférieures ou supérieures sont absentes ou nulles, la valeur par défaut 0 lorsque `LiteralInteger.value` ou `LiteralUnlimitedNatural.value` est omis, la préservation d'une borne supérieure explicitement illimitée et la non-interprétation des spécifications de valeurs non prises en charge. Les clauses exactes de la source sont répertoriées dans [R-220](../../docs/references.fr.md#r-220).

`GovCheckCoherence.SACM24.SourceFacts` consigne ensuite sept formes de spécifications de valeurs XML transcrites manuellement et démontre que cet interpréteur UML 2.5 produit les intervalles de propriétés SACM correspondants. Cela ne démontre pas que l'analyseur XMI Python a correctement extrait ces formes ; l'obligation de raffinement entre la source et l'analyseur reste ouverte. L'implémentation et le résumé d'inventaire généré sont versionnés en inventaire v2.

## Contrat de correspondance

Le modèle de statuts démontre également que `unknown_status_is_distinct_from_inconclusive` ; les deux statuts sont représentés dans le schéma JSON, tandis que la péremption reste une propriété distincte de fraîcheur.

`GovCheckCoherence.Mapping` lie un identifiant d'assertion source et cible à des propositions Lean. Sa couverture opérationnelle est limitée à `equivalent`, `soundDirectional` et `partialMapping` ; chaque constructeur de `SemanticBridge` porte l'obligation de preuve correspondante. Les candidats approximatifs, limités à la traçabilité ou non pris en charge utilisent le type distinct `MappingProposal`. Une proposition ne possède aucun pont sémantique et ne peut pas habiter `EvidenceMapping` ; elle ne peut donc pas être consommée par l'interface de correspondance typée actuelle comme prémisse sémantique établie.

Une correspondance opérationnelle lie également les révisions exactes des modèles source et cible et exige la préservation de l'identité/révision de la source de preuve, du périmètre exact, de toutes les hypothèses source et de la classe de méthode. Une nature cible de preuve par théorème ne peut être introduite qu'au moyen de `KindMappingRule.deriveTheoremProof`, qui contient un véritable terme de preuve Lean de la proposition cible exacte. Le constructeur de transport générique exclut explicitement `theoremProof` ; même une étiquette source existante de preuve par théorème ne suffit pas à transporter ce statut vers une cible. Le statut de résultat cible demeure indépendant : une nouvelle dérivation de théorème possède son propre résultat, et ne copie pas automatiquement le statut d'un test source.

Le premier profil exige l'égalité exacte des périmètres ; il ne définit pas encore d'ordre partiel sur les périmètres ni de réduction sûre du périmètre. Les champs `premises`, `assumptions`, `kernelIdentity` et `kernelVersion` de `KernelCheckedDerivation` restent des métadonnées de provenance et ne sont pas encore reliés mécaniquement à la fermeture complète des dépendances du terme de preuve. Le contrat exprime une obligation typée ; il ne prouve pas qu'un importateur ou exportateur de production satisfait cette obligation.

## Limites explicites

Il ne s'agit pas encore d'une preuve complète de cohérence du métamodèle. En particulier, ce travail ne démontre pas qu'un importateur/exportateur de production construit des valeurs de correspondance valides, qu'une interprétation SACM/OWL/SEON native à la source est correctement liée aux propositions Lean, que les correspondances se composent de manière conservative, ni qu'une implémentation externe raffine le contrat formel. La fraîcheur et l'autorité temporelle restent régies par les modèles TLA+ du dépôt et exigent un argument de conformité distinct.

Le terme de preuve est vérifié par le noyau Lean épinglé, mais les champs `premises`, `assumptions`, `kernelIdentity` et `kernelVersion` sont des métadonnées de provenance qui ne sont pas encore reliées mécaniquement à la fermeture complète des dépendances du terme de preuve. Les identifiants de Claims sont associés à des propositions Lean dans le sujet de la correspondance, mais aucun analyseur de production n'a encore été démontré comme préservant cette liaison. Les candidats approximatifs, limités à la traçabilité ou non pris en charge sont des valeurs non opérationnelles de type `MappingProposal` ; ils ne portent aucune preuve sémantique.

## Statut de vérification

L'API de correspondance renforcée a été compilée et auditée quant à ses axiomes avec la chaîne Lean 4.19.0 épinglée dans [l'exécution de workflow 43437994055](https://github.com/Martin-PB/govcheck/actions/runs/43437994055), sur la révision source formelle `6580daaeef6c506b0a2da30c790cac43481a15f3`. Le workflow a compilé `GovCheckCoherence`, audité 36 déclarations sous `GovCheckCoherence.Proofs` (toutes dans la liste d'autorisation configurée `propext`, `Classical.choice`, `Quot.sound`) et le rapport explicite `#print axioms` n'a trouvé aucun axiome pour les déclarations de théorèmes répertoriées. Le catalogue des artefacts consigne cette révision exacte vérifiée et cette exécution de workflow.

Le résultat s'applique à la révision exacte de la source formelle indiquée ci-dessus. Les commits documentaires/de portefeuille ultérieurs ne modifient pas les blobs sources Lean vérifiés. Il s'agit d'un résultat relatif à cette petite tranche formelle uniquement : ce n'est ni une preuve de correspondance sémantique avec SACM/OWL/SEON, ni une preuve de fidélité des sources importées, ni une preuve de composition des correspondances, ni une preuve de conformité de l'implémentation. Un commit Git réussi ou une ancienne exécution verte ne constitue pas un résultat de vérification Lean pour une autre révision de la source formelle.


## Fixture adversariale d'audit des axiomes

Le [faux artefact de preuve isolé](GovCheckCoherence/Reproductions/ForbiddenProofArtifact.lean) contient volontairement un théorème utilisant `sorryAx` et un théorème dépendant d'un axiome nommé non autorisé. Il n'est pas importé par la bibliothèque de preuves de production. Le workflow Lean compile cette fixture, capture la sortie de `#print axioms` et exige que l'[auditeur indépendant du rapport](../../scripts/audit-lean-axiom-report.py) rejette les deux dépendances. Les tests Python couvrent la liste d'autorisation, le comportement fail-closed en l'absence de rapport et les deux classes d'axiomes injectés.

Il s'agit d'un test négatif du chemin d'audit des rapports, pas d'une preuve que chaque théorème de production ou dépendance importée est audité à chaque révision. Le manifeste/corpus classe ce test comme adversarial synthétique ; il n'authentifie pas le workflow hébergé et ne remplace ni le noyau Lean épinglé ni l'analyse séparée de sa base de confiance.
