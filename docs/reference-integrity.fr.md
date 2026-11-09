# Intégrité du catalogue de références

Le catalogue est un index bilingue de sources et de provenance ; ce n'est ni une liste d'adoption ni une politique normative.

## Sources de référence

- Le [catalogue anglais](references.md) est la présentation par défaut.
- Le [catalogue français](references.fr.md) en est le pendant sémantique.
- Les deux catalogues contiennent 132 entrées actives. Trois identifiants ont été retirés et ne doivent jamais être réutilisés : identifiant 12 retiré (doublon Scorecard consolidé dans [R-08](references.fr.md#r-08)), identifiant 101 retiré (doublon NIST SP 800-218 consolidé dans [R-02](references.fr.md#r-02)) et identifiant 102 retiré (famille W3C PROV consolidée dans [R-24](references.fr.md#r-24)).
- Chaque entrée indique les sources primaires, les concepts pertinents, l'usage précis pour GovCheck et les limites.
- Chaque dossier d'architecture, décision ou spécification renvoie à l'ancre exacte du catalogue qu'il utilise.
- Le champ **Cited by / Cité par** de chaque entrée renvoie vers tous les documents qui la citent. Les sources candidates [R-94](references.fr.md#r-94)–[R-100](references.fr.md#r-100) et [R-103](references.fr.md#r-103) sont discutées dans l'Architecture 0027 sans être adoptées.

## Statut et provenance

Le document initial, **« Évaluer l’intégration des dépôts.pdf »** (6 novembre 2026, 224 pages), est conservé dans la bibliothèque du projet et n'est pas dupliqué dans ce dépôt. Son emplacement et ses limites probatoires sont consignés dans [ADR 0002](decisions/0002-study-placement.md) et [ADR 0002 (français)](decisions/0002-study-placement.fr.md). La cartographie détaillée figure dans l'[audit de provenance des références](reference-provenance-audit.fr.md).

Une référence n'est pas une approbation. Une proposition, un backlog, un prototype de recherche, une spécification bêta, une page produit et une norme formelle ont des statuts probatoires différents. Chaque entrée indique ses limites. La présence d'un protocole ou d'une bibliothèque dans le catalogue n'implique pas que GovCheck, Cartocortex, MoriNet ou SaussuNet l'implémente ou l'adopte.

## Règle de maintenance

Lorsqu'un document utilise une source externe :
1. ajouter ou mettre à jour une seule entrée R-XX, en privilégiant l'éditeur, l'organisme de normalisation ou le dépôt officiel ;
2. préciser le concept et l'affirmation pour lesquels la source est pertinente ;
3. indiquer les limites et distinguer proposition, implémentation, vérification et adoption ;
4. ajouter un lien direct vers l'ancre dans les documents anglais et français qui la citent ;
5. mettre à jour **Cited by / Cité par** dans les deux catalogues ;
6. ne jamais réutiliser un identifiant retiré.

CEL est également conservé comme langage d'expression candidat, sans décision d'adoption. Les revues ont aussi conduit à cataloguer l'argumentation éliminative, Kyverno, les règles d'approbation GitLab, Zuul/Bors, les théories formelles des patches, le standard GSN et NIST SP 800-192.

Les sources candidates qui ne sont pas encore utilisées par un document peuvent rester dans le catalogue si leur statut de source non citée est explicite. Ne jamais faire pointer un champ **Cited by / Cité par** vers un document absent de la branche.

Ne pas ajouter une référence simplement parce qu'un nom de technologie apparaît. L'ajouter lorsque la source étaye matériellement une affirmation, une comparaison, une interface ou une trace documentaire. Inversement, ne pas faire disparaître une source uniquement parce que l'option qu'elle documente n'a pas été retenue.

## Contrôle automatisé

Depuis la racine du dépôt :

~~~sh
python3 scripts/check-reference-integrity.py
~~~

Ce contrôle hors ligne vérifie la parité des entrées EN/FR, les identifiants à deux et trois chiffres, la couverture de l'index thématique, la symétrie des citations, les métadonnées des sources, les ancres, les liens Markdown locaux sous docs/, la traçabilité documentaire/catalogue dans les deux sens et la cohérence entre une mention d'absence de citation et les renvois inverses déclarés. Il signale également les URL externes présentes dans les documents sources mais absentes du catalogue central.

Pour sonder également l'accessibilité des URL externes (réseau requis ; les blocages côté éditeur sont signalés comme avertissements) :

~~~sh
python3 scripts/check-reference-integrity.py --external
~~~

Le contrôle externe est un signal d'accessibilité, pas une garantie d'autorité, d'actualité, d'exhaustivité ou de pertinence sémantique.