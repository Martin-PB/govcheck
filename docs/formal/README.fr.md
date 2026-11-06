# Modèles formels

Les travaux formels de GovCheck sont développés progressivement et restent distincts de toute affirmation relative à l’implémentation.

## Cycle de vie

- [Modèle du cycle de vie — français](lifecycle-model.fr.md)
- [Lifecycle model — anglais](lifecycle-model.md)
- [Module TLA+](../../formal/tla/GovCheckLifecycle.tla)
- [Configuration TLC](../../formal/tla/GovCheckLifecycle.cfg)
- [Catalogue des artefacts stables](../../formal/artifacts.json)
- [Schéma du manifeste de preuves de release](../../formal/schemas/release-manifest.schema.json)

Le modèle de cycle de vie est un artefact source dont l'identifiant logique stable est `govcheck.lifecycle`. Ses révisions sont suivies dans Git. Un tag de release fige l'arbre source et le commit exacts ; il n'impose pas de créer des copies des fichiers sources portant le nom de chaque release. Les rapports de vérification générés et leur manifeste sont joints à la release GitHub correspondante.

Le premier modèle couvre un changement abstrait, l’évaluation liée à un tuple, la publication de preuves, les approbations autorisées, l’acceptation, l’application du candidat exact, la mutation des entrées et les décisions terminales.

**Statut de vérification :** spécification et configuration TLC ajoutées ; aucune exécution TLC ni aucun résultat de preuve ne sont revendiqués. Consulter le document du modèle pour les limites de l’abstraction et les raffinements nécessaires.
