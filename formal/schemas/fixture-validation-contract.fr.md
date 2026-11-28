# Contrat de validation des fixtures et des bundles

**Statut :** contrat d'implémentation exécutable. Il clarifie les frontières des validateurs sans rendre normatifs les enregistrements de gouvernance des versions proposés.

## Unités de validation

GovCheck conserve volontairement les deux modes : validation d'un enregistrement unitaire et validation d'un bundle. Les fixtures unitaires ne sont pas converties en bundles uniquement pour satisfaire le validateur inter-enregistrements.

| Unité | Commande | Contrat |
|---|---|---|
| Une instance de schéma / un enregistrement unitaire | `python3 scripts/validate-formal-fixtures.py --root .` | Chaque `*.example.json` est associé à un schéma Draft 2020-12. Tous les identifiants de schéma enregistrés sont disponibles pour résoudre les `$ref` déclarés. |
| Bundle de gouvernance des versions | `python3 scripts/validate-version-governance.py chemin/vers/bundle.json --pretty` | L'entrée est une enveloppe avec `schemaVersion: 1` entier et les tableaux `revisions`, `decisions`, `dependencies`. Le validateur contrôle les identités et relations entre enregistrements. |
| Manifeste de publication | Valider l'instance contre `formal/schemas/release-manifest.schema.json` avec le validateur de schémas unitaires. | Un manifeste est une instance de schéma unitaire, sauf si un bundle spécifié séparément l'intègre explicitement. |
| Références externes | Le validateur unitaire enregistre ensemble les ressources `$id` des schémas du dépôt. | Les références de schéma sont structurelles ; elles ne sont ni des références d'autorité ni des références à des preuves. |

## Résultats et codes de sortie

### Fixtures JSON Schema unitaires

- `valid`, code 0 : les schémas et fixtures associés passent la validation structurelle.
- `invalid`, code 1 : au moins un constat de validation existe.
- Échec de préparation, code 2 : le répertoire, une ressource de schéma ou une association de fixture n'a pas pu être chargé.

### Bundle inter-enregistrements

| État | Code | Signification |
|---|---:|---|
| `valid` | 0 | Aucune contradiction inter-enregistrements détectée ; ce n'est pas une autorisation. |
| `invalid` | 1 | Contradiction structurelle ou entre enregistrements. |
| `unknown` | 2 | Un fait externe relatif à l'autorité reste non résolu. |
| `stale` | 3 | Une dépendance est explicitement non courante. |

Les erreurs priment sur `stale`, qui prime sur `unknown`.

## Invariants et limites

- Un enregistrement unitaire ne doit pas être transmis au validateur de bundles comme s'il s'agissait d'un bundle.
- Une enveloppe de bundle ne doit pas être transmise à un schéma d'enregistrement individuel.
- La validation JSON Schema n'effectue pas les contrôles inter-enregistrements.
- Le validateur de bundles n'effectue pas la validation JSON Schema ; les deux outils sont complémentaires.
- Aucun des deux outils ne prouve la délégation d'autorité, l'existence d'un objet VCS, la compatibilité sémantique, la fraîcheur des preuves, les signatures ou le comportement opérationnel.
- Toutes les fixtures du dépôt sont des exemples synthétiques de conformité aux schémas, pas des preuves.

## Tests de régression

La suite de tests vérifie qu'une fixture unitaire de dépendance est rejetée comme bundle et qu'une enveloppe de bundle est rejetée par le schéma d'arête de dépendance. Elle couvre aussi les cas positifs et négatifs des deux validateurs.

Depuis la racine du dépôt :

```sh
python3 -m unittest discover -s tests -p 'test_formal_fixture_validation.py' -v
python3 -m unittest discover -s tests -p 'test_version_governance_validator.py' -v
```
