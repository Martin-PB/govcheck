# Audit de provenance des références

**Statut :** document de travail retraçant la provenance des sources issues du PDF initial de 224 pages et des revues ultérieures de GovCheck. Cet audit documentaire ne prétend pas que chaque URL externe a été visitée ni que chaque publication citée a fait l'objet d'une réévaluation indépendante.

## 1. Artefacts sources et périmètre

La source historique principale est **« Évaluer l’intégration des dépôts.pdf »**, datée du 6 novembre 2026 et longue de 224 pages. Elle est conservée dans la bibliothèque du projet plutôt que copiée dans le dépôt. Elle a été créée pour transporter une longue discussion de conception avec ChatGPT vers une nouvelle conversation ; elle constitue donc une archive de discussions, décisions, propositions rejetées, hypothèses et sources externes citées — pas une norme externe ni une autorité normative en elle-même.

Le PDF couvre d'abord des travaux d'intégration connexes (notamment Cartocortex, MoriNet et SaussuNet), avant la conception et le bootstrap propres à GovCheck. Le contenu spécifiquement consacré à GovCheck devient explicite vers la page 133. Le contexte antérieur reste pertinent lorsqu'il apporte les dépôts, formats, protocoles et références d'interopérabilité qui sous-tendent l'étude initiale.

L'audit prend également en compte les revues critiques externes consignées dans les issues GitHub #23 et #26 ainsi que le suivi consolidé de l'issue #30. Ces revues sont des apports comparatifs ; leurs recommandations ne deviennent pas automatiquement des décisions adoptées par GovCheck.

## 2. Provenance et évolutions du catalogue

- Le catalogue comptait 105 entrées actives au début de cet audit.
- Le catalogue bilingue compte désormais **125 entrées actives**.
- Vingt et une nouvelles entrées ont été ajoutées (R-108–R-128), tandis que le doublon R-102 a été retiré et consolidé dans R-24. Les identifiants R-12 et R-101, déjà retirés, le restent. Aucun identifiant retiré n'est réutilisé.
- Neuf entrées comportaient une mention contradictoire d'absence de citation alors qu'elles renvoyaient à l'Architecture 0027. Cette mention a été supprimée pour R-94–R-100, R-102 et R-103 ; R-102 a ensuite été consolidée dans R-24.
- R-24 couvre désormais la famille W3C PROV et conserve les liens vers la recommandation PROV-O et la vue d'ensemble de la famille. R-102 est retirée.
- Le nom **Privateer** était ambigu. R-19 identifie désormais la distribution de l'agent de programmation Pi privateer-agent/privateer-agent. R-120 identifie séparément l'évaluateur de sécurité/conformité de l'OpenSSF. L'Architecture 0016 distingue et évalue les deux projets.
- Le script de contrôle détecte désormais la contradiction entre une mention d'absence de citation et la présence de renvois inverses. Le guide d'intégrité documente ce contrôle.

## 3. Cartographie des sources

| Domaine de discussion | Couverture du catalogue |
|---|---|
| Cartocortex, MoriNet, SaussuNet, PR examinées et dépôts GovCheck connexes | R-62, R-68, R-69 |
| Formats de cartes mentales, sérialiseurs, fixtures d'import/export et documentation éditeur | R-63, R-69 |
| CRDT, Yjs/Yrs, Automerge, Loro, WebRTC, ICE/STUN/TURN, WebTorrent, Hyperswarm/HyperDHT | R-45–R-50, R-66, R-87 |
| OKF, RDF, SKOS, OWL, SHACL, JSON-LD, PROV, Dublin Core, BIBO, DCAT, Web Annotation, ActivityStreams, SIOC, P-Plan et Schema.org | R-24, R-51–R-61, R-83–R-86 |
| Dossiers d'assurance, SACM 2.3 et 2.4 Beta 1, Assurance 2.0, PEAK et assurance à l'exécution | R-33–R-34, R-70–R-76 |
| Model checking, assistants de preuve et méthodes formelles alternatives (TLA+, Lean, Alloy, B, Z, CSP/FDR, iStar, logique déontique) | R-05, R-20, R-37–R-43, R-89–R-93 |
| Méthodes de menace/risque, vérification des politiques de contrôle d'accès et conformité structurée | R-27–R-36, R-78, R-88 |
| Moteurs de politiques, application des règles aux agents/MCP, sandboxing et instructions d'agents | R-09–R-10, R-77, R-79, R-104–R-106 |
| Provenance de chaîne d'approvisionnement, identité d'artefact, attestations, signatures et assurance des sources/builds | R-06–R-08, R-14–R-15, R-21, R-23–R-26, R-108, R-112–R-113, R-121–R-122 |
| Déclarations de sécurité de projets, référentiels, contrôles de dépôts et outils d'évaluation | R-08, R-109–R-120, R-127 |
| Candidats en sémantique métier, processus, exigences, qualité et ingénierie | R-74, R-94–R-100, R-103, R-114, R-123–R-126 |
| Formats d'instructions d'agents, outils de workflow et emplacement des workflows GitHub Actions | R-18–R-19, R-104, R-107 |

Le catalogue conserve également les sources ajoutées à partir des revues critiques : gittuf, SLSA Source Track, Gemara, exigences de soumission Gerrit, Minder, Allstar, Conftest, CUE, OpenSSF Privateer, SLSA Verification Summary Attestation (VSA), Sigstore, Symboleo, Catala, Event Calculus, vérification à l'exécution et GitHub CODEOWNERS et CEL (R-112–R-128).

## 4. Distinctions sémantiques préservées

- SACM 2.3 est la base formelle consignée en R-34 ; SACM 2.4 Beta 1 est une proposition en cours, enregistrée séparément en R-73. Aucun des deux n'est automatiquement adopté comme métamodèle général de gouvernance du dépôt GovCheck.
- PEAK (R-74) est un modèle de raisonnement décisionnel autour du problème, de l'expérience, des hypothèses et des connaissances ; ce n'est pas SACM et il ne remplace pas le modèle de dossier d'assurance.
- Tests, observations à l'exécution, model checking, vérification de programmes, preuve de théorème, affirmations de conformité et décisions d'acceptation restent des catégories distinctes.
- Une VSA ou une attestation signée délègue la confiance à un vérificateur ; elle ne prouve pas que le vérificateur est digne de confiance ni que l'affirmation est vraie.
- Les référentiels de sécurité et outils d'évaluation de dépôts sont des candidats pour des contrôles sélectionnables, pas des niveaux universels GovCheck ni des dépendances obligatoires.
- GitHub CODEOWNERS, Allstar et la protection de branche GitHub sont des mécanismes propres à une plateforme ; ils ne définissent pas un modèle d'autorité indépendant des forges.
- Une source évoquée dans la discussion peut être conservée comme contexte historique sans devenir une dépendance adoptée, une exigence normative ou une affirmation d'implémentation.

## 5. Identités de sources et provenances non résolues

Les éléments suivants ne peuvent pas recevoir une fiche source unique et fiable sans information complémentaire :

1. **Tarski** apparaît comme référence possible à un vérificateur/noyau dans la discussion, mais le projet, l'article ou l'outil exact n'est pas identifiable de façon univoque dans le contexte conservé. Aucun URL ni dépendance n'est deviné.
2. **Agent Package Manager** est mentionné dans la discussion précédente sans identité de produit ni URL vérifiée. Il reste volontairement sans lien.
3. **EPIC** apparaît dans le contexte ultérieur du projet comme référence possible de modélisation de décision, mais le framework/la publication exact n'est identifié ni dans le PDF initial ni dans le catalogue actuel. Il ne faut pas le deviner.

Ce sont des lacunes de provenance, pas des blocages pour les corrections actuelles du catalogue. Elles ne doivent être résolues que si les concepts correspondants restent pertinents pour GovCheck.

## 6. État des vérifications et travaux restants

Les modifications du dépôt sont enregistrées sur la branche d'audit, mais les contrôles suivants **n'ont pas été exécutés** dans cet environnement :

- python3 scripts/check-reference-integrity.py
- python3 scripts/check-reference-integrity.py --external

Aucun workflow GitHub Actions n'a été déclenché. La première commande doit être exécutée localement pour vérifier la parité bilingue, les identifiants/index, les ancres, les liens Markdown locaux et la traçabilité dans les deux sens. Le mode externe doit ensuite être exécuté séparément pour sonder l'accessibilité des URL. Même un résultat positif ne démontre ni l'autorité de la source, ni sa pertinence sémantique, ni l'exhaustivité ou la correction de son contenu.

L'inventaire des sources du PDF est maintenant largement rapproché du catalogue et des revues critiques, mais une dernière passe page par page sur tout le contexte précédant GovCheck reste nécessaire avant de prétendre à une couverture exhaustive de chaque source mentionnée dans les 224 pages.

## 7. Règle de maintenance

Pour chaque source réellement utilisée par un document GovCheck :
1. maintenir une seule entrée canonique R-XX, avec identité de la source primaire et version/statut ;
2. décrire l'affirmation ou la comparaison précise qu'elle étaye, ainsi que ses limites ;
3. distinguer mention historique, candidat, méthode adoptée, implémentation et résultat vérifié ;
4. lier la source depuis chaque document anglais et français concerné ;
5. maintenir les renvois inverses **Cited by / Cité par** dans les deux catalogues ;
6. ne jamais réutiliser un identifiant retiré ni deviner une identité de source manquante.