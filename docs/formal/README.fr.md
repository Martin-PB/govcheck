# Modèles formels

Les travaux formels de GovCheck sont développés progressivement et restent distincts de toute affirmation relative à l’implémentation.

## Cycle de vie

- [Modèle du cycle de vie v1 — français](lifecycle-model-v1.fr.md)
- [Lifecycle model v1 — anglais](lifecycle-model-v1.md)
- [Module TLA+](../../formal/tla/GovCheckLifecycle.tla)
- [Configuration TLC](../../formal/tla/GovCheckLifecycle.cfg)

Le premier modèle couvre un changement abstrait, l’évaluation liée à un tuple, la publication de preuves, les approbations autorisées, l’acceptation, l’application du candidat exact, la mutation des entrées et les décisions terminales.

**Statut de vérification :** spécification et configuration TLC ajoutées ; aucune exécution TLC ni aucun résultat de preuve ne sont revendiqués. Consulter le document du modèle pour les limites de l’abstraction et les raffinements nécessaires.
