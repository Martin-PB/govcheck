# Audit de provenance des références

**Statut :** document de travail retraçant la provenance des sources issues du PDF initial de 224 pages et des revues ultérieures de GovCheck. Cet audit documentaire ne prétend pas que chaque URL externe a été visitée ni que chaque publication citée a fait l'objet d'une réévaluation indépendante.

## 1. Artefacts sources et périmètre

La source historique principale est **« Évaluer l’intégration des dépôts.pdf »**, datée du 6 novembre 2026 et longue de 224 pages. Elle est conservée dans la bibliothèque du projet plutôt que copiée dans le dépôt. Elle a été créée pour transporter une longue discussion de conception avec ChatGPT vers une nouvelle conversation ; elle constitue donc une archive de discussions, décisions, propositions rejetées, hypothèses et sources externes citées — pas une norme externe ni une autorité normative en elle-même.

Le PDF couvre plusieurs fils de projets avant et parallèlement à la conception propre à GovCheck : Cartocortex, MoriNet et SaussuNet ; une pile d'agent SecOps NixOS ; puis la gouvernance et le bootstrap GovCheck. GovCheck devient explicite vers la page 133. Les contextes antérieurs restent pertinents lorsqu'ils apportent les dépôts, formats, protocoles et références d'interopérabilité qui sous-tendent l'étude initiale.

L'audit prend également en compte les revues critiques externes consignées dans les issues GitHub #23 et #26 ainsi que le suivi consolidé de l'issue #30. Ces revues sont des apports comparatifs ; leurs recommandations ne deviennent pas automatiquement des décisions adoptées par GovCheck.

## 2. Provenance et évolutions du catalogue

- Le catalogue comptait 105 entrées actives au début de cet audit.
- Le catalogue bilingue compte désormais **132 entrées actives**.
- Vingt-huit nouvelles entrées ont été ajoutées ([R-108](references.fr.md#r-108)–[R-135](references.fr.md#r-135)), tandis que le doublon 102 a été retiré et consolidé dans [R-24](references.fr.md#r-24). Les identifiants 12 et 101 étaient déjà retirés. Aucun identifiant retiré n'est réutilisé.
- Neuf entrées comportaient une mention contradictoire d'absence de citation alors qu'elles renvoyaient à l'Architecture 0027. Cette mention a été supprimée pour [R-94](references.fr.md#r-94)–[R-100](references.fr.md#r-100), retired identifier 102 et [R-103](references.fr.md#r-103) ; retired identifier 102 a ensuite été consolidée dans [R-24](references.fr.md#r-24).
- [R-24](references.fr.md#r-24) couvre désormais la famille W3C PROV et conserve les liens vers la recommandation PROV-O et la vue d'ensemble de la famille. retired identifier 102 est retirée.
- Le nom **Privateer** était ambigu. [R-19](references.fr.md#r-19) identifie désormais la distribution de l'agent de programmation Pi privateer-agent/privateer-agent. [R-120](references.fr.md#r-120) identifie séparément l'évaluateur de sécurité/conformité de l'OpenSSF. L'Architecture 0016 distingue et évalue les deux projets.
- Le script de contrôle détecte désormais la contradiction entre une mention d'absence de citation et la présence de renvois inverses. Le guide d'intégrité documente ce contrôle.

## 3. Cartographie des sources

| Domaine de discussion | Couverture du catalogue |
|---|---|
| Cartocortex, MoriNet, SaussuNet, PR examinées et dépôts GovCheck connexes | [R-62](references.fr.md#r-62), [R-68](references.fr.md#r-68), [R-69](references.fr.md#r-69) |
| Sémantiques Git/Pijul/Darcs et théorie des patches | [R-68](references.fr.md#r-68), [R-133](references.fr.md#r-133) |
| Contrôles d'approbation et systèmes de gating de fusion propres aux forges | [R-127](references.fr.md#r-127), [R-131](references.fr.md#r-131)–[R-132](references.fr.md#r-132) |
| Formats de cartes mentales, sérialiseurs, fixtures d'import/export et documentation éditeur | [R-63](references.fr.md#r-63), [R-69](references.fr.md#r-69) |
| CRDT, Yjs/Yrs, Automerge, Loro, WebRTC, ICE/STUN/TURN, WebTorrent, Hyperswarm/HyperDHT | [R-45](references.fr.md#r-45)–[R-50](references.fr.md#r-50), [R-66](references.fr.md#r-66), [R-87](references.fr.md#r-87) |
| OKF, RDF, SKOS, OWL, SHACL, JSON-LD, PROV, Dublin Core, BIBO, DCAT, Web Annotation, ActivityStreams, SIOC, P-Plan et Schema.org | [R-24](references.fr.md#r-24), [R-51](references.fr.md#r-51)–[R-61](references.fr.md#r-61), [R-83](references.fr.md#r-83)–[R-86](references.fr.md#r-86) |
| Dossiers d'assurance, SACM 2.3 et 2.4 Beta 1, Assurance 2.0, PEAK et assurance à l'exécution | [R-33](references.fr.md#r-33)–[R-34](references.fr.md#r-34), [R-70](references.fr.md#r-70)–[R-76](references.fr.md#r-76), [R-129](references.fr.md#r-129), [R-134](references.fr.md#r-134) |
| Model checking, assistants de preuve et méthodes formelles alternatives (TLA+, Lean, Alloy, B, Z, CSP/FDR, iStar, logique déontique) | [R-05](references.fr.md#r-05), [R-20](references.fr.md#r-20), [R-37](references.fr.md#r-37)–[R-43](references.fr.md#r-43), [R-89](references.fr.md#r-89)–[R-93](references.fr.md#r-93) |
| Méthodes de menace/risque, vérification des politiques de contrôle d'accès et conformité structurée | [R-27](references.fr.md#r-27)–[R-36](references.fr.md#r-36), [R-78](references.fr.md#r-78), [R-88](references.fr.md#r-88) |
| Moteurs de politiques, application des règles aux agents/MCP, sandboxing et instructions d'agents | [R-09](references.fr.md#r-09)–[R-10](references.fr.md#r-10), [R-77](references.fr.md#r-77), [R-79](references.fr.md#r-79), [R-104](references.fr.md#r-104)–[R-106](references.fr.md#r-106), [R-128](references.fr.md#r-128), [R-130](references.fr.md#r-130) |
| Provenance de chaîne d'approvisionnement, identité d'artefact, attestations, signatures et assurance des sources/builds | [R-06](references.fr.md#r-06)–[R-08](references.fr.md#r-08), [R-14](references.fr.md#r-14)–[R-15](references.fr.md#r-15), [R-21](references.fr.md#r-21), [R-23](references.fr.md#r-23)–[R-26](references.fr.md#r-26), [R-108](references.fr.md#r-108), [R-112](references.fr.md#r-112)–[R-113](references.fr.md#r-113), [R-121](references.fr.md#r-121)–[R-122](references.fr.md#r-122) |
| Déclarations de sécurité de projets, référentiels, contrôles de dépôts et outils d'évaluation | [R-08](references.fr.md#r-08), [R-109](references.fr.md#r-109)–[R-120](references.fr.md#r-120), [R-127](references.fr.md#r-127) |
| Candidats en sémantique métier, processus, exigences, qualité et ingénierie | [R-74](references.fr.md#r-74), [R-94](references.fr.md#r-94)–[R-100](references.fr.md#r-100), [R-103](references.fr.md#r-103), [R-114](references.fr.md#r-114), [R-123](references.fr.md#r-123)–[R-126](references.fr.md#r-126), [R-128](references.fr.md#r-128) |
| Formats d'instructions d'agents, outils de workflow et emplacement des workflows GitHub Actions | [R-18](references.fr.md#r-18)–[R-19](references.fr.md#r-19), [R-104](references.fr.md#r-104), [R-107](references.fr.md#r-107) |

Le catalogue conserve également les sources ajoutées à partir des revues critiques : gittuf, SLSA Source Track, Gemara, exigences de soumission Gerrit, Minder, Allstar, Conftest, CUE, OpenSSF Privateer, SLSA Verification Summary Attestation (VSA), Sigstore, Symboleo, Catala, Event Calculus, vérification à l'exécution et GitHub CODEOWNERS, CEL, argumentation éliminative, Kyverno, règles d'approbation GitLab, Zuul/Bors, théorie formelle des patches, GSN et NIST SP 800-192 ([R-112](references.fr.md#r-112)–[R-135](references.fr.md#r-135)).


## 4. Repères de pagination du PDF

Les repères suivants relient des passages notables de la discussion au catalogue. Ils facilitent la navigation, mais ne remplacent pas la vérification de l'édition/version exacte de chaque source.

- **Pages 31–49 :** RDF, composition d'ontologies, ingestion de cartes mentales, validation de graphes et vocabulaires du Web sémantique — [R-51](references.fr.md#r-51)–[R-61](references.fr.md#r-61), [R-63](references.fr.md#r-63), [R-83](references.fr.md#r-83)–[R-86](references.fr.md#r-86).
- **Pages 33–34 :** distinction entre le modèle graphe de RDF et la coédition temps réel fondée sur des CRDT — [R-45](references.fr.md#r-45)–[R-50](references.fr.md#r-50), [R-66](references.fr.md#r-66), [R-87](references.fr.md#r-87).
- **Section du projet NixOS SecOps :** isolation d'agents locaux et comparaison de sandboxes/outils, notamment nono, Landlock, Goose, mcp-nixos, SmolVM et Nixi — [R-79](references.fr.md#r-79) couvre les mécanismes transverses de sandboxing et d'agents ; les autres dépendances propres au projet restent une question de périmètre ci-dessous.
- **Page 117 :** NIST SP 800-192 et nécessité de vérifier les modèles de politique, pas seulement d'exécuter les politiques — [R-135](references.fr.md#r-135), avec OPA/Rego [R-09](references.fr.md#r-09), Cedar [R-10](references.fr.md#r-10) et Sentinel [R-77](references.fr.md#r-77).
- **Pages 154–156 :** SLSA, in-toto, GUAC, OpenSSF Scorecard, Best Practices Badge, Security Insights et OSPS Baseline — [R-06](references.fr.md#r-06)–[R-08](references.fr.md#r-08), [R-108](references.fr.md#r-108)–[R-111](references.fr.md#r-111).
- **Page 178 :** Writ et Privateer sont présentés comme outils complémentaires de workflow et d'évaluation de conformité ; Agent Package Manager est nommé sans identité résoluble — [R-18](references.fr.md#r-18), [R-120](references.fr.md#r-120) ; voir les notes sur les identités non résolues ci-dessous.
- **Pages 188–200 :** bootstrap GovCheck, autorité locale au dépôt, frontière d'acceptation, adaptateurs Git/Pijul et forges locales/d'équipe — [R-05](references.fr.md#r-05), [R-20](references.fr.md#r-20), [R-68](references.fr.md#r-68), [R-133](references.fr.md#r-133).
- **Pages 219–220 :** identité des artefacts, chemins stables, releases, tags et politique de versionnement — [R-14](references.fr.md#r-14), [R-15](references.fr.md#r-15), [R-21](references.fr.md#r-21), [R-23](references.fr.md#r-23)–[R-26](references.fr.md#r-26).

## 5. Distinctions sémantiques préservées

- SACM 2.3 est la base formelle consignée en [R-34](references.fr.md#r-34) ; SACM 2.4 Beta 1 est une proposition en cours, enregistrée séparément en [R-73](references.fr.md#r-73). Aucun des deux n'est automatiquement adopté comme métamodèle général de gouvernance du dépôt GovCheck.
- PEAK ([R-74](references.fr.md#r-74)) est un modèle de raisonnement décisionnel autour du problème, de l'expérience, des hypothèses et des connaissances ; ce n'est pas SACM et il ne remplace pas le modèle de dossier d'assurance.
- Tests, observations à l'exécution, model checking, vérification de programmes, preuve de théorème, affirmations de conformité et décisions d'acceptation restent des catégories distinctes.
- Une VSA ou une attestation signée délègue la confiance à un vérificateur ; elle ne prouve pas que le vérificateur est digne de confiance ni que l'affirmation est vraie.
- Les référentiels de sécurité et outils d'évaluation de dépôts sont des candidats pour des contrôles sélectionnables, pas des niveaux universels GovCheck ni des dépendances obligatoires.
- GitHub CODEOWNERS, Allstar et la protection de branche GitHub sont des mécanismes propres à une plateforme ; ils ne définissent pas un modèle d'autorité indépendant des forges.
- Une source évoquée dans la discussion peut être conservée comme contexte historique sans devenir une dépendance adoptée, une exigence normative ou une affirmation d'implémentation.

## 6. Identités de sources et provenances non résolues

Les éléments suivants ne peuvent pas recevoir une fiche source unique et fiable sans information complémentaire :

1. **Tarski** apparaît comme référence possible à un vérificateur/noyau dans la discussion, mais le projet, l'article ou l'outil exact n'est pas identifiable de façon univoque dans le contexte conservé. Aucun URL ni dépendance n'est deviné.
2. **Agent Package Manager** est mentionné dans la discussion précédente sans identité de produit ni URL vérifiée. Il reste volontairement sans lien.
3. **EPIC** apparaît dans le contexte ultérieur du projet comme référence possible de modélisation de décision, mais le framework/la publication exact n'est identifié ni dans le PDF initial ni dans le catalogue actuel. Il ne faut pas le deviner.
4. Le PDF contient aussi des dépendances d'implémentation propres au projet NixOS SecOps : **mcp-nixos, SmolVM, Nixi, nixpkgs, Lanzaboote, microvm.nix et QEMU**. [R-79](references.fr.md#r-79) couvre déjà les références transverses au sandboxing et aux agents nono, Landlock et Goose. Les autres éléments n'ont pas encore reçu d'identifiant GovCheck car ils peuvent être des dépendances de ce projet distinct plutôt que des sources utilisées matériellement par GovCheck.

Ce sont des lacunes de provenance, pas des blocages pour les corrections actuelles du catalogue. Elles ne doivent être résolues que si les concepts correspondants restent pertinents pour GovCheck.

## 7. État des vérifications et travaux restants

Les modifications du dépôt sont enregistrées sur la branche d'audit, mais les contrôles suivants **n'ont pas été exécutés** dans cet environnement :

- python3 scripts/check-reference-integrity.py
- python3 scripts/check-reference-integrity.py --external

Aucun workflow GitHub Actions n'a été déclenché. La première commande doit être exécutée localement pour vérifier la parité bilingue, les identifiants/index, les ancres, les liens Markdown locaux et la traçabilité dans les deux sens. Le mode externe doit ensuite être exécuté séparément pour sonder l'accessibilité des URL. Même un résultat positif ne démontre ni l'autorité de la source, ni sa pertinence sémantique, ni l'exhaustivité ou la correction de son contenu.

L'inventaire des sources du PDF est maintenant largement rapproché du catalogue et des revues critiques, mais une dernière passe page par page sur tout le contexte précédant GovCheck reste nécessaire avant de prétendre à une couverture exhaustive de chaque source mentionnée dans les 224 pages.

## 8. Règle de maintenance

Pour chaque source réellement utilisée par un document GovCheck :
1. maintenir une seule entrée canonique R-XX, avec identité de la source primaire et version/statut ;
2. décrire l'affirmation ou la comparaison précise qu'elle étaye, ainsi que ses limites ;
3. distinguer mention historique, candidat, méthode adoptée, implémentation et résultat vérifié ;
4. lier la source depuis chaque document anglais et français concerné ;
5. maintenir les renvois inverses **Cited by / Cité par** dans les deux catalogues ;
6. ne jamais réutiliser un identifiant retiré ni deviner une identité de source manquante.