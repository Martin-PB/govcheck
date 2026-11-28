# Matrice candidate de relations typées GovCheck

**Statut :** candidate de recherche, pas un métamodèle ni une règle d'évaluateur adopté. Cet addendum répond au travail de couverture sémantique de l'issue #73. Il propose des relations typées plutôt qu'une chaîne unique du cycle de vie ; il ne déclare pas équivalents des termes d'ontologies externes sur la seule base de leur nom.

## 1. Assertion de relation, pas une simple arête

Une assertion de relation devrait contenir au minimum :

- des références immuables aux artefacts source et cible (identifiant, révision et fragment éventuel) ;
- le type de relation et un profil sémantique versionné ;
- le périmètre et l'intervalle/événement d'applicabilité ;
- la provenance de création de l'assertion ;
- un enregistrement d'autorité si la relation modifie un état normatif ;
- une référence de preuve et un état de fraîcheur si la relation est probatoire ;
- un statut : candidate, active, unknown, conflict, stale, invalidated ou rejected.

L'assertion elle-même est un artefact qui peut être révisé, remplacé ou invalidé. Un lien documentaire n'est pas automatiquement une relation sémantique.

## 2. Familles de relations candidates

Toutes les relations sont orientées et plusieurs-à-plusieurs, sauf si un profil indique une autre cardinalité. Le tableau donne des types source/cible candidats, pas des règles universelles de cardinalité.

| Relation | Source → cible | Sens candidat et garde-fou |
|---|---|---|
| `adopts` | Décision d'autorité → Révision de modèle/spécification | Adoption normative ; exige autorité authentifiée, périmètre et événement de publication. |
| `authorizes` | Grant d'autorité → Action/Publication | Permission dans le périmètre explicite acteur, objet, opération et temps. |
| `obligates` / `prohibits` / `permits` | Norme/Politique → Acteur/Action | Relations déontiques ; jamais inférées d'une preuve descriptive seule. |
| `decomposes` | Objectif/Exigence → Sous-objectif/Sous-exigence | Décomposition structurelle ; la complétude est une affirmation distincte. |
| `derives` | Rationale/Assertion/Exigence → Assertion/Exigence dérivée | Dérivation avec justification ou règle enregistrée. |
| `refines` | Modèle/Exigence → Modèle/Exigence raffinée | Raffinement sémantique ; opérant seulement avec argument de préservation/couverture pour le profil. |
| `allocates` | Exigence/Propriété → Composant/Sous-système | Allocation ; n'établit pas à elle seule la satisfaction. |
| `realizes` | Implémentation/Conception → Modèle/Exigence/Propriété | Assertion de réalisation ; exige trace et contexte de configuration. |
| `satisfies` | Implémentation/Assertion d'assurance → Exigence/Propriété | Assertion de satisfaction ; doit être soutenue par des preuves adaptées à la méthode. |
| `verifies` | Test/Model-check/Preuve → Assertion/Propriété | Vérification qualifiée par méthode, hypothèses, bornes et résultat. |
| `validates` | Besoin/Intention/Assertion stakeholder → Système/Exigence | Validation dans un contexte stakeholder et selon un critère d'acceptation identifié. |
| `supports` / `defeats` | Preuve/Observation → Assertion | Soutien probatoire ou élément réfutant ; inclut provenance, périmètre et fraîcheur. |
| `justifies` | Rationale/Preuve → Décision/Assertion | Relation de justification ; la décision reste un acte autorisé distinct. |
| `assumes` | Modèle/Décision → Hypothèse/Risque | Hypothèse explicite ; liée à un responsable, risque résiduel et revue/expiration. |
| `wasDerivedFrom` | Révision/Activité d'artefact → Révision source/Agent | Provenance, pas équivalence sémantique ni vérité. |
| `supersedes` | Révision/Décision → Révision/Décision précédente | Succession de versions ; ne réécrit pas l'historique. |
| `invalidates` | Changement/Événement de révocation → Assertion/Preuve/Évaluation | Invalidation prospective avec périmètre et événement d'effet. |
| `observes` | Observation/Mesure → État/Assertion | Observation descriptive avec instrument, contexte et date. |
| `contradicts` | Assertion/Preuve → Assertion | Relation de conflit ; le conflit bloque jusqu'à résolution autorisée. |

## 3. Contraintes de types et de cycles

- Aucune exigence de DAG global. Le cycle de vie contient rétroactions, décisions, éléments réfutants et révisions.
- L'acyclicité ne doit être imposée qu'aux familles où elle est pertinente (par exemple `supersedes` et décomposition stricte dans une même révision).
- Un cycle dans `supports`, `justifies` ou `refines` n'est pas automatiquement valide ou invalide ; il nécessite une règle spécifique et ne doit pas bootstrapper sa propre autorité ou preuve.
- `refines`, `realizes` et `satisfies` sont distinctes. Une conception peut raffiner une exigence, une implémentation réaliser une conception et une preuve soutenir une satisfaction ; ces relations ne sont pas interchangeables.
- `verifies` est qualifiée par méthode : test, model checking borné et preuve de théorème donnent des types d'assurance différents. Un test réussi est une preuve empirique, pas une preuve formelle.
- `wasDerivedFrom` enregistre uniquement la provenance. Elle ne doit pas être interprétée comme `sameAs`, entailment logique ou préservation sémantique.

## 4. Correspondance candidate avec les standards existants

- SACM : préserver Claims, Arguments, Evidence et leur structure native ; ne mapper que les types de relations dotés d'un profil explicite.
- GSN : Goal, Strategy, Context, Assumption, Justification et Solution peuvent correspondre à des types d'artefacts candidats, mais un label de lien GSN seul n'établit pas la sémantique GovCheck.
- SysML v2 / ReqIF : exigences, propriétés, comportements et allocations peuvent fournir des artefacts source typés ; la sémantique native des relations doit rester disponible.
- PROV-O : dérivation, activité et agent sont des candidats de provenance, pas de justification normative ou de vérification.
- OSLC : les types de liens peuvent soutenir navigation/interoperabilité, mais un URI n'est pas automatiquement une assertion d'assurance typée.

Aucun standard n'est choisi comme ontologie canonique unique par cette matrice. Le contenu natif des sources doit rester préservable.

## 5. Relations opérantes ou candidates

Une relation reste **candidate** tant que son type, les révisions source/cible, le profil et les preuves/autorités requises ne sont pas résolus. L'évaluateur ne doit pas utiliser une relation candidate pour autoriser une publication ni affirmer une satisfaction.

Pour un mapping sémantique opérant, le profil doit préciser son domaine et son obligation de couverture. Un mapping partiel à domaine vide n'est pas une relation de couverture opérante ; voir l'issue corrective #210. Unknown, conflict et stale restent distincts et bloquants lorsqu'ils affectent l'assertion évaluée.

## 6. Limite de non-adoption

Cette matrice est un artefact de recherche pour l'issue #73. Elle ne met pas à jour le métamodèle canonique, ne modifie pas les sémantiques SACM/GSN/SysML et n'autorise pas de claims d'implémentation. L'adoption nécessite une décision distincte dans #41 après examen du dossier de couverture sémantique et des obligations formelles.


## 7. Correspondance étayée par les sources (versions épinglées, candidate uniquement)

| Base source | Structures/relations natives | Usage GovCheck candidat | Garde-fou de non-équivalence |
|---|---|---|---|
| SACM 2.3 formel ; SACM 2.4 Beta 1 (R-34, R-73) | Claims, argumentation, références d'évidence/artefacts ; la bêta 2.4 ajoute/précise des structures d'assertion et d'inférence. | Sous-graphe d'assurance et mapping typé claim/preuve/argument. | Préserver version et structure native ; 2.4 reste une bêta. Un lien SACM claim/argument n'est pas automatiquement une exigence GovCheck, une preuve ou une autorisation. |
| GSN Community Standard v3 (R-04) | Goals, Strategies, Context, Assumptions, Justifications, Solutions et liens d'argument définis. | Mapping candidat de décomposition d'affirmation, rationale, contexte, hypothèse et référence de preuve. | GSN est une notation/standard d'argument, pas un cycle de vie ni une autorité de gouvernance. Ne pas l'appeler « GSN 3.0 » ; utiliser la source SCSC v3. |
| SysML v2.0 (R-95, R-119) | Langage formel de modélisation des systèmes avec sémantique d'exigences, structure, comportement, analyse et vérification. | Artefacts d'ingénierie typés et relations candidates exigence/propriété/composant. | Ne pas inférer `satisfies`, `realizes` ou `refines` par simple correspondance de labels ; préserver sémantique du modèle et profil de transformation. |
| ReqIF 1.2 (R-95) | Objets d'échange d'exigences, attributs et relations. | Import/export des enregistrements d'exigences et liens natifs. | Les relations du format d'échange ne sont pas automatiquement des assertions d'assurance, d'autorité ou de satisfaction. |
| W3C PROV-O (R-24, R-102) | Entity, Activity, Agent et propriétés de provenance comme dérivation, usage, génération et association. | Assertions de provenance entre artefact/révision/processus/agent. | `wasDerivedFrom` est une provenance, pas un raffinement sémantique, un entailment ni une vérité. |
| OASIS OSLC Core 3.0 et Resource Shape (R-234, R-235) | Interopérabilité des ressources/services Linked Data et contraintes de formes structurelles. | Liens de navigation/interopérabilité et validation structurelle des payloads d'échange. | Les URI et la conformité aux shapes n'établissent ni sémantique d'assurance, ni autorité, ni authenticité/suffisance des preuves. |

## 8. Enregistrement requis du profil de mapping

Avant qu'une relation native devienne opérante, son profil de mapping doit consigner : spécification/version source exacte ; identifiant et domaine/cible de la relation source ; relation candidate GovCheck ; direction et cardinalité ; préservation sémantique ou perte explicite ; constructs non mappés ; conservation du payload natif ; révision et applicabilité ; provenance ; autorité si normative ; et fixtures positives/négatives.

Une correspondance de label n'est pas une preuve de mapping. Un profil incapable de justifier la relation reste candidate/unsupported et ne doit pas alimenter l'évaluateur. Voir le [catalogue de références](../references.fr.md#r-234) et l'[audit de couverture sémantique](metamodel-semantic-coverage-audit.fr.md).
