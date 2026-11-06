# 0012 — Autorité normative canonique et conformité documentaire

**Statut :** contrat d’architecture proposé pour approbation. Aucun moteur, parseur, générateur ou mécanisme d’application n’est réputé implémenté. **English:** [0012](0012-normative-authority-and-documentation.md).

## Principe

Un dépôt ne doit pas acquérir plusieurs autorités normatives concurrentes parce que les humains et agents consultent plusieurs fichiers d’instructions. GovCheck doit interpréter une seule autorité de gouvernance versionnée et lisible par machine. Les documents humains l’expliquent ou la projettent ; ils ne créent pas silencieusement une seconde politique.

Invariant de conception :

`Pour tout document contrôlé d : NormativeContent(d) ⊆ AuthorizedRules(GovCheck)`

C’est une cible, pas l’affirmation que les documents actuels ont déjà été contrôlés.

## Hiérarchie des sources

1. **Source approuvée :** règles canoniques, versionnées, lisibles par machine, avec autorité et provenance.
2. **Sémantique/évaluateur :** interprétation définie des types de règles, périmètres, applicabilité, composition, exceptions et transitions.
3. **Projections humaines contrôlées :** sections générées ou contrôlées mécaniquement dans `AGENTS.md`, `GOVERNANCE.md`, `SECURITY.md`, `CONTRIBUTING.md` et équivalents.
4. **Contenu explicatif :** tutoriels, exemples, justifications, notes d’architecture et discussions. Il explique, mais n’ajoute pas silencieusement d’obligations.

Sérialisation, technologie de schéma, langage d’expression et arborescence restent ouverts. Cet ADR ne choisit ni langage, ni format, ni moteur de politique, ni outil de preuve.

## Classes de contenu documentaire

Chaque section contrôlée est classée comme :
- **Projection normative :** rendu fidèle d’identifiants de règles canoniques, avec métadonnées de traçabilité ou correspondance équivalente.
- **Instruction opérationnelle :** procédure d’usage d’un outil ou d’exécution d’une tâche. Si elle impose un comportement, elle référence une règle autorisée ; sinon elle est explicitement facultative.
- **Contenu explicatif :** justification, exemple, contexte ou conseil ; ce n’est pas une obligation non enregistrée.

Un document peut mélanger ces classes, mais leurs frontières sont explicites. Les sections normatives générées sont distinguables des explications maintenues. Un fichier ne devient pas autorité simplement parce qu’une convention d’agent lui donne une influence pratique.

## Identité et traçabilité

Chaque règle possède un identifiant stable et immuable, un historique d’évolution, une force normative, une applicabilité, des paramètres typés et une provenance vers une décision/source approuvée. Les identifiants ne sont jamais recyclés. Les changements sémantiques créent des révisions, remplacements ou supersessions traçables.

Chaque projection relie les énoncés normatifs aux identifiants de règles. La correspondance inverse indique où chaque règle est projetée, ou qu’elle ne l’est pas. Une traduction projette la même règle ; ce n’est pas une politique indépendante. Une dérive de traduction est un défaut de conformité.

## Contrôles documentaires requis

Un futur outil devrait découvrir le paquet canonique et les documents contrôlés ; valider IDs, références, versions et métadonnées ; détecter les instructions normatives sans référence autorisée ; détecter projections absentes, dupliquées, obsolètes ou divergentes ; comparer anglais/français sans créer de seconde autorité ; signaler sections non classifiées et langage ambigu comme indéterminés ; produire des constats traçables ; et proposer inspection en lecture seule puis plan avant mise à jour.

La recherche textuelle repère des candidats mais ne prouve pas l’équivalence sémantique. La revue sémantique est une activité d’assurance distincte. L’IA ne peut promouvoir silencieusement un texte explicatif en politique obligatoire.

## Protocole de changement

Proposer la modification avec justification et autorité ; valider identité, force, périmètre, références et composition ; obtenir l’approbation de l’autorité désignée ; modifier la source canonique ; régénérer/mettre à jour les projections ; exécuter contrôles mécaniques et revue sémantique requise ; enregistrer la révision exacte et ses preuves.

Modifier d’abord Markdown en laissant la source canonique inchangée n’est pas une modification valide de politique. Une instruction temporaire urgente doit être approuvée, limitée, bornée dans le temps et suivie jusqu’à réconciliation.

## Échecs et limites

Source absente, ID dupliqué, référence non résolue, langage normatif ambigu, projections contradictoires ou sémantique non prise en charge ne sont pas des succès. Les cas obligatoires non résolus sont indéterminés et échouent de manière fermée, sauf exception valide et bornée. Le bootstrap reste non destructif : inspecter → planifier → appliquer, avec diff révisable et retour arrière.

Ouvert : format/encodage/signatures canoniques ; marqueurs Markdown ; sections générées ; langage d’implémentation ; Lean/OPA/Cedar ; classificateur sémantique ; autorité distante. Ces choix exigent des prototypes ciblés.
