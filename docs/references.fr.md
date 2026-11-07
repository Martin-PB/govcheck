# Références externes

**Objet.** Cette page est le point d'entrée thématique vers la bibliographie externe de GovCheck. Elle aide à retrouver les sources par question ou domaine de conception, sans dupliquer leur description.

La bibliographie détaillée et numérotée est maintenue dans le [registre gouvernance, assurance et méthodes formelles](references/governance-and-assurance.fr.md) ([English](references/governance-and-assurance.md)). Chaque entrée y consigne la source primaire, les concepts pertinents, l'utilisation dans GovCheck et les limites.

## Parcourir par domaine

| Domaine | Ce que couvrent les références | Entrées détaillées |
|---|---|---|
| Autorité de gouvernance et séparation des tâches | Autorité normative, responsabilités, contrôles d'accès, séparation des tâches et obligations de développement sécurisé | R-01–R-03, R-11 |
| Dossiers d'assurance et arguments de sûreté | Affirmations, arguments, contexte, hypothèses et preuves ; structuration de l'assurance sans la confondre avec une preuve | R-04 |
| Méthodes formelles et preuve | TLA+, TLC, modèles à transitions d'état, invariants, model checking et assistants de preuve | R-05, R-20 |
| Preuves, provenance et chaîne d'approvisionnement logicielle | Attestations in-toto, provenance SLSA, intégrité des builds et éléments circonscrits de posture de sécurité | R-06–R-08 |
| Moteurs de politiques et autorisation | Séparation décision/application des politiques, autorisation typée et limites d'OPA/Cedar | R-09–R-10 |
| Métadonnées de gouvernance et catalogues | Métadonnées typées, relations, traçabilité et patrons de catalogues | R-17 |
| Schémas et contrats d'interface | Validation structurelle avec JSON Schema et interfaces lisibles par machine avec OpenAPI | R-13, R-16 |
| Identité, versionnement et releases des artefacts | Champ d'application de SemVer, révisions immuables, tags Git, releases et contexte de vérification reproductible | R-14–R-15, R-21 |
| Sémantiques des systèmes de gestion de versions et collaboration | Snapshots Git face au graphe de patches de Pijul, canaux, conflits et frontières des adaptateurs | R-22 |
| Systèmes de workflow d'agents évalués comme fixtures | Évaluations de Writ et Privateer épinglées sur leur code source ; aucun n'est adopté comme dépendance ou autorité de GovCheck | R-18–R-19 |

## Règles d'utilisation de la bibliographie

- Partir du domaine pertinent, puis consulter les entrées numérotées correspondantes dans le registre détaillé.
- Utiliser la table de correspondance en fin de registre pour retrouver les documents d'architecture auxquels une source contribue.
- Privilégier les normes et publications primaires, les documentations officielles et les révisions de code épinglées.
- Respecter la classe de preuve de chaque source. Une norme, un article, une documentation produit, un arbre de code, un résultat de test et un rapport de model checking n'étayent pas les mêmes affirmations.
- La présence d'une source signifie qu'elle éclaire le raisonnement documenté ; elle n'implique ni adoption, ni implémentation, ni compatibilité, ni approbation, ni preuve de conformité.
- Conserver les descriptions et limites propres à chaque source dans le registre détaillé ; ne pas maintenir de descriptions bibliographiques en double ici.

## Documentation associée

- [Registre détaillé des références](references/governance-and-assurance.fr.md)
- [Index thématique en anglais](references.md)
- [Enregistrements d'architecture](architecture/README.md)
- [Spécification des adaptateurs VCS et de collaboration](specifications/0004-vcs-collaboration-contracts.fr.md)
