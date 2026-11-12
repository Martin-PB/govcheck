# ADR 0009 — Document d'intention du dépôt et nomenclature canonique

- **Statut :** adopté par le propriétaire du dépôt le 2026-11-10.
- **Périmètre de la décision :** document d'intention propre au dépôt GovCheck et artefact d'intention canonique attendu dans un dépôt gouverné par GovCheck.
- **Remplace :** aucun.
- **Références :** [R-114](../references.fr.md#r-114), [R-115](../references.fr.md#r-115), [R-116](../references.fr.md#r-116), [R-117](../references.fr.md#r-117), [R-118](../references.fr.md#r-118), [R-119](../references.fr.md#r-119), [R-120](../references.fr.md#r-120), [R-121](../references.fr.md#r-121), [R-122](../references.fr.md#r-122).

## Contexte

GovCheck a besoin d'un document durable, lisible par les humains et les agents, qui exprime la raison d'être du dépôt, ses résultats visés, son contexte opérationnel, ses frontières, contraintes et questions ouvertes. Ce document doit rester distinct des exigences, décisions d'architecture, spécifications, plans d'implémentation et éléments d'évidence d'assurance.

Le nom `product-intent.md` avait été utilisé initialement dans une branche de travail. Le propriétaire du dépôt a demandé une étude des conventions académiques et industrielles existantes avant de retenir un nom canonique. La comparaison a identifié la pratique `intent.md` documentée par Anthropic comme le précédent conceptuel et de nommage le plus proche. Le propriétaire a explicitement validé `intent.md` pour GovCheck le 10 novembre 2026.

## Décision

1. Le nom canonique de l'artefact est **`intent.md`**, en minuscules.
2. Dans l'arborescence documentaire de GovCheck, le fichier canonique anglais est **`docs/intent.md`** et son équivalent français maintenu est **`docs/intent.fr.md`**.
3. Tout dépôt gouverné par GovCheck doit représenter son intention au niveau du dépôt comme un artefact de gouvernance de premier rang. Son nom canonique est `intent.md` ; l'organisation documentaire gouvernée le place dans `docs/intent.md`, sauf contrainte structurelle distincte et consignée justifiant un autre emplacement.
4. Le document d'intention exprime la raison d'être du dépôt, son contexte et ses frontières opérationnelles, ses parties prenantes/utilisateurs ou bénéficiaires, les problèmes ou besoins auxquels il répond, les résultats visés, contraintes, hypothèses et questions ouvertes. Son niveau de détail est proportionné au dépôt, mais son existence et son identité ne sont pas facultatives.
5. GovCheck adopte comme inspiration le **nommage et la pratique conceptuelle générale** documentés dans le AI-native SDLC Playbook d'Anthropic. Cela ne prétend pas qu'Anthropic publie un standard normatif universel de fichier, ni que GovCheck est conforme à un schéma Anthropic.
6. GovCheck **n'adopte pas** le format `INTENT.md` d'IntentDocs et ne revendique aucune compatibilité avec celui-ci. Ce format publié combine présentation produit, personas, releases, stories et critères d'acceptation d'une manière qui fusionnerait des distinctions que GovCheck entend préserver.
7. L'intention est un artefact amont d'orientation de conception, pas une politique normative complète, un ensemble d'exigences adoptées, un modèle de gouvernance exécutable, une décision d'architecture, un contrat d'implémentation ou un dossier d'assurance. Les objectifs, exigences, contraintes, propriétés, décisions, spécifications et obligations d'assurance dérivés conservent leurs propres identités, statuts, autorités et traçabilité.
8. Les relations entre l'intention et les artefacts dérivés ne sont pas entièrement spécifiées par cet ADR. Leur métamodèle, types de relations, cardinalités, sémantiques temporelles, règles de complétude et propriétés de validation nécessitent une recherche et une conception distinctes. Cet ADR n'adopte pas une chaîne linéaire de cycle de vie.

## Conséquences

- Les fichiers de travail actuels sont renommés en `docs/intent.md`, `docs/intent.fr.md`, `docs/intent-impact-analysis.md` et `docs/intent-impact-analysis.fr.md`.
- Les références, index README et index d'architecture utilisent les noms canoniques.
- Le catalogue des références consigne les sources académiques, normatives et industrielles qui éclairent cette décision, avec leur statut et leurs limites.
- Les mécanismes de bootstrap, migration et conformité devront à terme créer, préserver et valider l'artefact d'intention ; cet ADR ne prétend pas que ces mécanismes sont implémentés.
- Une intention concise est valable pour un petit dépôt ; l'absence n'est pas équivalente à un document concis.
- L'analyse d'impact reste un audit de travail et n'adopte pas à elle seule le modèle candidat de relations.

## Alternatives rejetées

- **`product-intent.md` :** restreint inutilement le concept à un produit et introduit une convention composée nouvelle sans nécessité.
- **`INTENT.md` tel que défini par IntentDocs :** format ouvert publié, mais sa structure regroupée ne correspond pas à la séparation sémantique recherchée par GovCheck. GovCheck ne revendique aucune compatibilité.
- **Un nom librement choisi par dépôt :** affaiblit la découvrabilité, la cohérence de l'outillage et l'interopérabilité.
- **Un emplacement exclusivement à la racine :** l'organisation documentaire actuelle de GovCheck utilise `docs/` ; l'emplacement canonique est donc `docs/intent.md`, tout profil de structure différent devant relever d'une règle explicite plutôt que d'un choix ad hoc.

## Réexamen et évolution

Tout changement du nom canonique ou du rôle sémantique nécessite une décision explicite de l'autorité GovCheck compétente. Les changements de l'intention propre à un dépôt sont des changements gouvernés de ce document ; ils ne modifient pas silencieusement les décisions ou exigences existantes.

Le métamodèle des relations est volontairement reporté à un travail distinct d'architecture/spécification fondé sur la recherche.
