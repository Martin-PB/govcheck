# 0029 — Séparation des préoccupations CI et périmètres de vérification formelle

**Statut :** décision d'architecture proposée, mise en œuvre par la modification CI associée, en attente de revue et de fusion.  
**Périmètre :** orchestration de la CI du dépôt et politique de déclenchement des modèles formels GovCheck.  
**Décision :** un contrôle ne s'exécute que lorsqu'un élément de son périmètre de vérification déclaré change. Une modification du vérificateur partagé invalide les exécutions de tous les modèles concernés ; une documentation sans rapport ne les déclenche pas.

## 1. Problème

L'ancien workflow `.github/workflows/tla-check.yml` mélangeait quatre préoccupations indépendantes : vérification TLC, dérive du diagramme de cycle de vie et tests du validateur de gouvernance des versions. Ses filtres de chemins très larges incluaient tous les documents d'architecture et de spécification, tous les schémas et fixtures formels ainsi que plusieurs scripts sans rapport. Une modification d'un document d'architecture indépendant lançait donc tous les modèles TLC et des contrôles annexes.

Ce couplage augmentait le coût de la CI et rendait moins lisible la portée réelle d'un résultat vert.

## 2. Décision et principes

La CI est partitionnée selon la propriété contrôlée, et non selon un répertoire large ou une notion générique de modification du dépôt.

1. **Vérification propre à chaque modèle :** chaque modèle TLA+ possède son propre périmètre de déclenchement : source, configuration TLC et documentation sémantique explicitement associée.
2. **Invalidation du vérificateur partagé :** une modification du runner TLC réutilisable déclenche les workflows de chaque modèle, car elle peut affecter tous leurs résultats.
3. **Contrôles indépendants des artefacts générés :** la cohérence du diagramme du cycle de vie est vérifiée uniquement lorsque son registre de transitions, son générateur, le diagramme généré ou son workflow change.
4. **Contrôles indépendants du validateur :** les tests du validateur de gouvernance des versions ne s'exécutent que si le validateur, ses tests, ses entrées de schéma/catalogue ou son workflow changent.
5. **Aucune inférence par répertoire :** l'emplacement d'un fichier sous `docs/architecture/`, `docs/specifications/` ou `formal/` ne suffit pas à établir une dépendance envers tous les modèles formels.
6. **Dépendance sémantique explicite :** si un document normatif ou explicatif contribue au sens d'un modèle, ce document précis doit figurer dans les chemins de déclenchement du modèle. Cette correspondance est revue lorsque l'abstraction ou les dépendances sémantiques du modèle changent.
7. **Les changements de politique sont vérifiés :** une modification du workflow propre à un modèle ou du runner partagé déclenche les vérifications concernées. Le modèle de routage CI n'est contrôlé que lorsque sa source, sa configuration ou son workflow change.

## 3. Périmètres de vérification

| Préoccupation | Entrées déclenchantes | Contrôle |
|---|---|---|
| Modèle de cycle de vie | `GovCheckLifecycle.tla`, sa configuration `.cfg`, documentation du modèle (EN/FR), workflow dédié, runner TLC partagé | SANY + TLC du seul modèle de cycle de vie |
| Modèle d'assurance | `GovCheckAssurance.tla`, sa configuration `.cfg`, Architecture 0021 (EN/FR), workflow dédié, runner TLC partagé | SANY + TLC du seul modèle d'assurance |
| Modèle d'autorité | `GovCheckAuthority.tla`, sa configuration `.cfg`, Architecture 0023 (EN/FR), workflow dédié, runner TLC partagé | SANY + TLC du seul modèle d'autorité |
| Diagramme du cycle de vie | registre des transitions, générateur, diagramme généré, workflow du diagramme | contrôle déterministe de génération/dérive |
| Gouvernance des versions | validateur, tests du validateur, schémas/catalogue pertinents, workflow du validateur | tests unitaires + compilation Python |
| Politique de routage CI | `CICheckRouting.tla`, sa configuration `.cfg`, workflow du modèle de routage | SANY + TLC de la seule politique de routage |

Le workflow TLC réutilisable épingle TLA+ Tools v1.7.4 et vérifie son SHA-256 avant exécution. Chaque exécution de modèle publie son propre artefact de rapport.

## 4. Propriétés formelles du routage

`formal/tla/CICheckRouting.tla` abstrait l'ensemble des fichiers modifiés en catégories de préoccupations et vérifie que :

- une modification documentaire ou architecturale sans rapport ne déclenche aucun modèle TLC ;
- une entrée propre au cycle de vie déclenche son TLC, mais pas ceux de l'assurance ou de l'autorité ;
- une entrée propre à l'assurance déclenche son TLC, mais pas ceux du cycle de vie ou de l'autorité ;
- une entrée propre à l'autorité déclenche son TLC, mais pas ceux du cycle de vie ou de l'assurance ;
- une modification du runner TLC partagé déclenche les trois vérifications ;
- chaque entrée propre à un modèle déclenche la vérification correspondante.

Le modèle de routage est volontairement distinct des modèles produit de cycle de vie, d'assurance et d'autorité. Il vérifie la politique de dispatch déclarée, pas la correction sémantique de ces modèles ni la fidélité de chaque expression de chemin GitHub Actions. Les listes de chemins des workflows restent la politique exécutable et doivent être confrontées à ce modèle lorsqu'elles changent.

## 5. Invariants et interprétation

Les invariants directeurs sont la **couverture**, l'**isolation**, l'**invalidation par le runner partagé** et la **non-interférence de la documentation sans rapport**. Un modèle ignoré n'est pas présenté comme venant d'être vérifié : cela signifie qu'aucune entrée déclarée dans son périmètre de vérification n'a changé dans la proposition.

Un résultat TLC vert établit uniquement que le modèle fini et sa configuration sélectionnés ont terminé avec les propriétés contrôlées. Il ne prouve ni le raffinement de l'implémentation, ni la fidélité sémantique entre prose et TLA+, ni la correction du moteur de déclenchement GitHub Actions.

## 6. Règle de gestion des changements

Lors de l'ajout ou de la modification d'un modèle formel :

1. identifier sa source, sa configuration, sa documentation sémantique et ses dépendances d'exécution partagées ;
2. mettre à jour les chemins de déclenchement dédiés ;
3. mettre à jour l'abstraction de routage si les catégories de dépendances ou la politique d'isolation changent ;
4. exécuter le modèle de routage lorsque cette politique change ;
5. conserver un rapport propre au modèle et vérifier que les changements sans rapport ne le planifient pas.

Lorsqu'un document modifie le sens d'un modèle, le déclencheur correspondant doit inclure ce document. Les modifications purement éditoriales ou architecturales sans rapport ne doivent pas être ajoutées comme dépendances génériques par joker.

## 7. Conséquences et limites

Cette conception accepte qu'un petit workflow soit dispatché lorsqu'une documentation sémantique propre à un modèle change, tout en évitant les exécutions TLC coûteuses et sans rapport. Elle utilise les filtres de chemins natifs de GitHub Actions et des workflows réutilisables ; elle n'ajoute aucune action tierce de filtrage de chemins ni service externe.

La correspondance des déclencheurs est une déclaration de dépendances explicite et révisable, pas un moteur automatique d'analyse des différences sémantiques. Une dépendance oubliée constitue un défaut de gouvernance ; un joker trop large n'est pas un substitut acceptable à l'analyse des dépendances.
