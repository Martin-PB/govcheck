# 0011 — Modèle de cycle de vie : lecture de chaque assertion et statut des vérifications

**Statut :** analyse du source de l'artefact actuel. Ce n'est ni un résultat TLC, ni une preuve de théorème, ni un rapport de conformité de l'implémentation. **English:** [0011](0011-lifecycle-model-assertion-audit.md).

## 1. Artefacts présents

La PR #4 a ajouté `formal/tla/GovCheckLifecycle.tla`, sa configuration `formal/tla/GovCheckLifecycle.cfg`, des explications bilingues, `formal/lifecycle-transitions.json`, le diagramme `docs/formal/lifecycle-diagram.mmd`, le script `scripts/render-lifecycle-diagram.py`, `formal/artifacts.json` et le schéma JSON du manifeste de release.

Le module TLA+ est l'autorité sémantique. Le registre JSON et le diagramme Mermaid sont explicatifs. Le script Python contrôle la couverture structurelle et la dérive du fichier généré ; il ne prouve pas l'équivalence sémantique entre registre et TLA+.

## 2. Identité abstraite et état

Le changement est lié au tuple :

`CurrentTuple = <<baseId, candidateId, governanceId, specId>>`

Les identités de base, candidat, gouvernance et spécification influencent ainsi l'évaluation et l'acceptation. Le tuple n'inclut pas encore toutes les identités réelles nécessaires (dépôt, build de l'évaluateur, environnement, dépendances, politique d'approbation, faits externes) : elles restent à raffiner.

Variables :
- `phase` : Proposed, Prepared, Evaluated, Reviewable, Accepted, Applied, Rejected, Withdrawn, Superseded ou Stale ;
- `baseId`, `candidateId`, `governanceId`, `specId` ;
- `evaluatedTuple` ;
- `outcomes` pour un ensemble fini d'obligations ;
- `evidence`, actuellement ensemble d'identifiants d'obligations ;
- `approvals`, actuellement ensemble d'identifiants d'acteurs autorisés ;
- `acceptedTuple` ;
- `appliedCandidateId` ;
- `history`, séquence abstraite de libellés d'événements.

La configuration utilise deux valeurs par dimension d'identité, deux acteurs, deux obligations et `HistoryLimit = 12`. Ce sont des paramètres d'exploration, pas des contraintes de production.

## 3. Actions

- `Prepare` : Proposed → Prepared ; consigne la préparation.
- `PublishEvidence(obligation)` : ajoute un identifiant d'obligation, revient à Prepared et invalide le tuple évalué/résultats.
- `Evaluate` : évalue le tuple courant ; chaque obligation dont l'identifiant est publié devient Pass, sinon Unknown. Si toutes sont présentes : Reviewable ; sinon : Evaluated.
- `Approve(actor)` : ajoute un acteur autorisé si la phase est Reviewable et le tuple évalué courant.
- `Accept` : exige Reviewable, évaluation courante, tous les résultats Pass et assez d'approbations ; enregistre le tuple courant comme accepté.
- `Apply` : exige Accepted et un tuple accepté toujours courant ; enregistre son candidat comme appliqué.
- `ChangeInputs` : change base/candidat/gouvernance/spécification, marque Stale et efface évaluation, preuves, approbations, acceptation et application.
- `Reject`, `Withdraw`, `Supersede` : décisions terminales.
- `Next` : disjonction de ces actions, avec choix existentiels pour obligation, acteur et nouveau tuple.

Les actions qui modifient l'état ajoutent un libellé à `history`, sous réserve de la limite.

## 4. Chaque invariant configuré, précisément

| Nom | Question exacte | Limite importante |
|---|---|---|
| `TypeOK` | Les variables restent-elles dans leurs domaines et l'historique sous sa borne ? | Types/domaines, pas correction métier. |
| `AcceptanceSoundness` | Si Accepted, acceptedTuple=currentTuple, evaluatedTuple=currentTuple, tous les résultats=Pass et le nombre d'approbations atteint le seuil ? | Dépend de la simplification des variables de preuve et d'approbation. |
| `ApplicationSoundness` | Si Applied, appliedCandidateId égale-t-il le candidat du tuple accepté/courant ? | Ne modélise pas un vrai adaptateur ni l'application VCS externe. |
| `NoStaleEvaluation` | En Reviewable/Accepted/Applied, evaluatedTuple est-il courant ? | Seulement les quatre dimensions du tuple. |
| `EvidenceBinding` | En Reviewable, l'évaluation est-elle courante et evidence égale-t-elle les obligations modélisées ? | Pas d'objet probant avec provenance ni liaison individuelle au tuple. |
| `ApprovalBinding` | En Accepted/Applied, les identifiants d'approbation appartiennent-ils à AuthorizedActors ? | Pas de tuple par approbation, signature, rôle, date, motif ou révocation. |
| `NoImplicitApplication` | Hors Applied, appliedCandidateId vaut-il None ? | Ne prouve pas l'application externe. |
| `HistoryNonEmpty` | L'historique contient-il au moins l'événement initial ? | Pas de propriété complète de préfixe/append-only/intégrité. |

## 5. Propriété temporelle et déclarations de théorèmes

`TerminalDiscipline` est configurée sous TLC `PROPERTIES`, pas `INVARIANTS`. Une fois la phase égale à Applied, Rejected, Withdrawn ou Superseded, la phase suivante doit rester identique.

Le module contient aussi des déclarations `THEOREM Spec => []Property`. Elles consignent des obligations de théorème visées. Leur présence ne prouve pas qu'un prouveur les a déchargées. Analyse SANY, contrôles structurels, exploration TLC des invariants/propriétés et preuve de théorème sont des opérations distinctes. Le rapport doit nommer l'opération réellement exécutée.

## 6. Limites visibles dans le source et raffinements requis

1. **Identité des preuves :** `evidence` stocke des noms d'obligations, pas des objets avec sujet, méthode, producteur, outil, résultat, digest, validité, provenance et dépendances.
2. **Vérité/adéquation :** `Evaluate` transforme directement une preuve publiée en Pass. Aucun vérificateur indépendant, argument preuve/affirmation ou niveau de confiance de source n'est modélisé.
3. **Échec :** Fail est déclaré mais aucune action ne le produit. Il faudra distinguer fail, unknown, unsupported, not-run, incomplete, stale et conflict.
4. **Liaison des approbations :** les approbations sont des identifiants d'acteurs, pas des enregistrements signés liés individuellement au candidat, à la gouvernance et à la politique d'approbation.
5. **Invalidation :** ChangeInputs efface les approbations, mais PublishEvidence ne le fait pas. Comme PublishEvidence est possible en Reviewable et revient à Prepared, le raffinement doit décider si une modification de preuve invalide les approbations existantes.
6. **Concurrence :** aucune course entre approbation, publication de preuve, mutation d'entrée, acceptation et application n'est modélisée.
7. **Application :** Apply est une transition abstraite ; elle n'appelle ni ne vérifie un adaptateur Git/Pijul réel, ses capacités, préconditions, échecs partiels ou état effectivement appliqué.
8. **Historique :** les actions ajoutent des libellés, mais HistoryNonEmpty ne prouve ni préfixe, ni authenticité, ni métadonnées acteur/motif, ni résistance à l'altération.
9. **Confiance externe :** pas de clés/signatures/révocation, fraîcheur des sources externes, outil compromis ou adaptateur malveillant.
10. **Sémantique VCS :** état Git dirty/index/sous-modules et patches/canaux/graphe/conflits Pijul sont hors modèle.
11. **Remédiation terminale :** ChangeInputs est désactivée après les états terminaux, y compris Applied. La réouverture après application reste à décider.
12. **Trace finie :** HistoryLimit=12 finit par désactiver les actions qui modifient l'état. C'est une borne d'exploration, pas une règle de rétention.

Ces limites définissent la contribution de l'abstraction ; elles n'annulent pas l'intérêt du premier modèle.

## 7. Ce que la PR #4 a réellement vérifié

La PR #4 rapporte des contrôles structurels :
- le registre de transitions est un JSON valide ;
- les dix actions de `Next` sont représentées ;
- les opérateurs du registre ont des définitions TLA+ de premier niveau ;
- les actions qui modifient l'état contiennent la borne d'historique ;
- le Mermaid commité correspond aux règles de rendu du registre.

La PR ne revendiquait **pas** :
- l'exécution du générateur Python dans un checkout ;
- une validation syntaxique SANY ou un model checking TLC ;
- une preuve par théorème ;
- la conformité de l'implémentation au modèle ;
- une suite locale de tests ou un validateur de schéma ;
- une exécution de CI hébergée.

Un contrôle structurel du source n'est pas du model checking. TLC n'est pas une preuve par théorème. Aucun des deux n'est la conformité de l'implémentation.

## 8. Séquence de vérification à réaliser

1. Épingler versions TLA+ Tools/TLC et Java ; enregistrer les empreintes des binaires/distributions.
2. Exécuter SANY/le parseur et enregistrer commande/sortie exactes.
3. Exécuter TLC avec la configuration commise ; capturer achèvement, nombres d'états/transitions, interblocages et contre-exemples.
4. Examiner chaque contre-exemple et distinguer défaut du modèle et défaut de conception.
5. Raffiner les objets preuve et la fraîcheur des dépendances ; modéliser explicitement Fail/Unknown/Unsupported/NotRun/Incomplete/Conflict.
6. Lier chaque approbation au candidat, à la révision de gouvernance, à la politique, au rôle, à l'acteur et à la révocation.
7. Ajouter modèles de concurrence et courses d'application, si possible séparés et composables.
8. Définir vecteurs de conformité indépendants du langage et relation de raffinement de l'implémentation.
9. Ne rapporter ensuite que les affirmations d'assurance effectivement étayées par les artefacts.

Aucune étape ne doit être déclarée achevée avant que sa preuve d'exécution soit commise ou jointe à la release correspondante.
