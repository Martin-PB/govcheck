# Comparaison : GovCheck, gittuf, SLSA Source, Gemara, Privateer et Gerrit

**Statut :** comparaison de recherche, pas une décision d'architecture, une adoption ni une affirmation d'implémentation. Elle s'appuie sur les fiches sources ci-dessous et sur les spécifications de conception actuelles de GovCheck.

## 1. Comparaison synthétique

| Système / modèle | Périmètre principal | Apport | Ce qu'il ne remplace pas dans GovCheck |
|---|---|---|---|
| **GovCheck** (conception actuelle) | Gouvernance générale du dépôt : cycle de vie, autorité, acceptation des changements, assurance et adaptateurs VCS | Modèle normatif au niveau du dépôt pour intentions, exigences, règles, propriétés, décisions, affirmations, arguments, preuves, vérifications et risques acceptés | Le projet reste au stade conception/spécification. Le dépôt ne démontre pas encore que l'évaluateur, les adaptateurs ou la frontière d'application sont implémentés ou formellement vérifiés. |
| **gittuf** ([R-112](../references.fr.md#r-112)) | Sécurité des dépôts Git et métadonnées de politique authentifiées | Racine de confiance cryptographique, administrateurs délégués et métadonnées de politique vérifiables sur les changements Git | Gouvernance générale du cycle de vie, sémantiques de dossier d'assurance, artefacts arbitraires du dépôt et sémantiques Pijul |
| **SLSA Source Track** ([R-113](../references.fr.md#r-113)) | Provenance du code source et assurance des contrôles du dépôt source | Vocabulaire et cadre d'assurance sur la création et la protection des révisions sources, avec propriétés attestables | Gouvernance normative du dépôt, modèle d'autorité/délégation couvrant tous les domaines, correction sémantique ou politique d'acceptation des changements |
| **Gemara** ([R-114](../references.fr.md#r-114)) | Modèles de données et schémas de gouvernance, risque et conformité | Catalogues de contrôles, évaluations et vocabulaires de preuves structurés pour l'interopérabilité GRC | Cycle de vie du dépôt, identité de changement indépendante du VCS, modèle d'autorité et distinctions entre tests, model checking et preuve |
| **OpenSSF Privateer** ([R-120](../references.fr.md#r-120)) | Évaluation par plugins de contrôles de sécurité/conformité | Plugins d'évaluation, catalogues de contrôles structurés, contrôles déterministes et revue humaine pour les preuves non résolues | Autorité canonique de gouvernance, cycle de vie du dépôt, acceptation des changements ou preuve de théorème |
| **Exigences de soumission Gerrit** ([R-115](../references.fr.md#r-115)) | Intégration à la revue de code et gating de soumission | Prédicats configurables déterminant si un changement relu peut être soumis | Gouvernance indépendante des forges, sémantiques du cycle de vie multi-VCS, arguments d'assurance et provenance générale des preuves |

## 2. Complémentarité plutôt que remplacement

GovCheck ne devrait pas réimplémenter chaque système adjacent. Son rôle potentiel consiste à définir le modèle normatif de gouvernance et les contrats explicites par lesquels des systèmes spécialisés apportent des preuves ou appliquent une partie des contrôles.

- **Autorité de gouvernance :** GovCheck spécifie quelles affirmations, règles, exigences, autorités et conditions d'acceptation s'appliquent à un dépôt. Périmètre, applicabilité, exceptions, délégation et risques acceptés restent explicites.
- **Intégrité propre à Git :** gittuf peut fournir des métadonnées de politique Git authentifiées et des preuves d'intégrité des changements. Un adaptateur Git peut les consommer ou les recouper sans faire de gittuf l'autorité universelle. Pijul exige ses propres sémantiques et ne peut pas être représenté comme des commits Git.
- **Provenance du code source :** SLSA Source éclaire les attentes et attestations relatives au dépôt source. C'est un profil d'assurance spécialisé, pas un cadre complet de gouvernance du dépôt ; SLSA Build et provenance source restent distincts.
- **Vocabulaire des contrôles :** Gemara peut fournir des concepts GRC et des schémas interopérables. Une correspondance doit préserver autorité, applicabilité, exceptions, identité VCS et sémantiques d'assurance propres à GovCheck.
- **Évaluation des contrôles :** Privateer peut être un évaluateur facultatif de certains contrôles. Conserver identité/version du plugin, révision du catalogue, entrées, sorties, références de preuves, incertitude et état de revue humaine. Une revue assistée par IA n'est pas une preuve.
- **Gating des changements :** exigences de soumission Gerrit, règles d'approbation GitLab, Zuul/Bors et files de fusion natives des forges sont des mécanismes d'intégration. Toute projection du prédicat d'acceptation GovCheck doit déclarer les écarts propres à la plateforme et les hypothèses de contournement.

## 3. Correspondance des preuves et de l'assurance

| Concept GovCheck | Contribution externe candidate | Frontière à préserver |
|---|---|---|
| Identité de source/révision et provenance | gittuf ; SLSA Source ; in-toto/VSA ; Sigstore | Vérifier digest du sujet, identité du signataire/vérificateur, racine de confiance, type de prédicat, périmètre de ressource et fraîcheur. Une signature ou attestation ne prouve ni la vérité de l'affirmation ni la correction du vérificateur. |
| Définition et catégories des contrôles | Gemara ; OSPS Baseline ; Security Insights | Préserver version de la source, identifiants des contrôles, applicabilité et pertes de correspondance. Un catalogue de contrôles n'est pas un résultat d'évaluation. |
| Exécution et évaluation des contrôles | Privateer ; OPA/Rego ; Cedar ; CEL ; Conftest ; Kyverno | Préserver version de l'évaluateur, révision de politique, entrées, résultat déterministe, état non résolu et provenance des preuves. |
| Intégration et acceptation des changements | Gerrit ; règles d'approbation GitLab ; Zuul/Bors ; files de fusion des forges | Évaluer le candidat exact d'intégration ; distinguer approbation, résultat CI, satisfaction de politique et acceptation finale autorisée. |
| Argument d'assurance | SACM ; GSN ; Assurance 2.0 ; argumentation éliminative | Préserver affirmations, contextes, hypothèses, stratégies, preuves, contre-preuves, défaiteurs et justification du niveau de confiance. Un graphe bien formé n'est pas automatiquement valide. |

## 4. Distinctions que GovCheck doit préserver

1. **Un test est un témoignage/élément de preuve, pas une preuve de théorème.** Un test réussi étaye une affirmation bornée sous les hypothèses du test et pour les entrées observées.
2. **Le model checking est une preuve de validation du modèle, pas une preuve de théorème.** Le résultat dépend du modèle, de la spécification, de l'espace d'états exploré et de l'abstraction.
3. **Une preuve vérifiée n'est pas la même chose qu'un modèle vérifié.** Identifier le vérificateur, le noyau, les hypothèses et la frontière de confiance.
4. **Une attestation est une déclaration signée par un producteur/vérificateur identifié.** Elle ne rend ni la déclaration vraie ni le producteur digne de confiance.
5. **Un catalogue de contrôles n'est pas une décision de politique.** Applicabilité, périmètre, exceptions, fraîcheur des preuves et acceptation autorisée du risque doivent être explicites.
6. **Le bouton de fusion d'une forge n'est pas le modèle de gouvernance.** Le même prédicat normatif d'acceptation peut nécessiter des adaptateurs différents pour GitHub, GitLab, Gerrit, Git local, d'autres forges et Pijul.

## 5. Conclusion actuelle

La contribution potentielle de GovCheck se situe au-dessus des outils individuels : une autorité de gouvernance générale résidente dans le dépôt et un modèle de cycle de vie reliant intentions, règles, changements, preuves, arguments d'assurance et décisions d'acceptation entre différents environnements VCS et forges.

Cette contribution reste une hypothèse de conception tant qu'une tranche verticale étroite ne démontre pas qu'une règle réelle de dépôt peut être évaluée de façon déterministe, qu'un résultat échec ou inconnu bloque l'acceptation à la frontière déclarée et que les preuves sont traçables et examinables indépendamment. Cette comparaison ne sélectionne aucune dépendance obligatoire.

## 6. Sources

- [gittuf](../references.fr.md#r-112)
- [SLSA Source Track](../references.fr.md#r-113)
- [Gemara](../references.fr.md#r-114)
- [Exigences de soumission Gerrit](../references.fr.md#r-115)
- [OpenSSF Privateer](../references.fr.md#r-120)
- [OpenSSF Security Insights](../references.fr.md#r-109) et [OSPS Baseline](../references.fr.md#r-110)
- [SLSA Verification Summary Attestation](../references.fr.md#r-121) et [Sigstore](../references.fr.md#r-122)
- [Zuul et Bors](../references.fr.md#r-132)
- [Règles d'approbation GitLab](../references.fr.md#r-131)
- [Argumentation éliminative](../references.fr.md#r-129) et [GSN](../references.fr.md#r-134)