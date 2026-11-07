# 0014 — Flux de développement gouverné et responsabilités des acteurs

**Statut :** contrat de flux proposé ; aucune orchestration d’agents, aucun modèle de tâche ni contrôle d’approbation n’est réputé exister. **English:** [0014](0014-governed-development-workflow.md).

## Périmètre et dossier

GovCheck gouverne le dépôt et le cycle de vie des changements proposés. Il ne supervise pas chaque appel d’outil d’un agent, ne fournit pas de bac à sable et ne possède pas sa mémoire. Humains et agents sont des contributeurs. Le flux guide l’interprétation de la demande, l’implémentation, la vérification, la revue, l’acceptation et l’application. Il vaut pour tout dépôt ; les obligations varient selon périmètre/profil, pas selon des niveaux fondés sur la taille.

Avant le travail substantiel, résoudre un dossier lié aux identités dépôt/base/candidat (y compris l’état non commité pertinent), aux révisions de gouvernance/spécification, au type de changement, aux objectifs/composants affectés, à l’impact et à l’acteur/autorité initiateur. Le dossier n’est ni branche, commit, patch, PR ni discussion ; ceux-ci sont des objets natifs référencés.

La tâche consigne intention, critères d’acceptation, non-objectifs, périmètre, contraintes, risques, hypothèses, dépendances, décisions requises et preuves attendues. Les entrées manquantes ou contradictoires sont enregistrées, pas inventées.

## Séquence gouvernée

1. **Découvrir la gouvernance :** localiser/valider source canonique, profils, instructions projet et capacités outils ; signaler absence, conflit, non-prise en charge ou obsolescence.
2. **Interpréter la demande :** reformuler intention/critères ; distinguer faits, hypothèses, contraintes et décisions ouvertes.
3. **Analyser l’impact :** tracer objectifs, exigences, normes, propriétés, composants, interfaces, données et frontières de confiance affectés.
4. **Planifier :** identifier obligations, interdictions, permissions, revues, méthodes, preuves et autorités ; planifier avant opérations destructrices/irréversibles.
5. **Concevoir :** mettre à jour architecture/contrats/modèles si nécessaire ; examiner cohérence et faisabilité ; enregistrer décisions.
6. **Implémenter :** réaliser le plus petit changement cohérent en préservant les sémantiques natives dépôt/VCS.
7. **Vérifier :** exécuter les contrôles applicables sous contraintes déclarées ; capturer invocation, entrées, outils, environnement, identité du sujet, sorties et limites.
8. **Examiner l’assurance :** relier affirmations obligatoires aux preuves admissibles ; conserver échecs, inconnues, contradictions et dérogations ; pas d’auto-approbation.
9. **Demander une décision :** soumettre candidat exact et dossier aux réviseurs/autorités habilités.
10. **Accepter/appliquer :** dériver l’acceptation du prédicat ; revérifier les identités exactes avant application ; enregistrer le reçu natif de l’adaptateur.
11. **Clore le dossier :** préserver décisions, références de preuves, dérogations, invalidations et enseignements.

Un autre ordre peut être justifié, mais motif et impact sur l’assurance sont enregistrés. Une tâche ne peut éviter un contrôle obligatoire en se disant documentation ou refactorisation.

## Classes de tâches

| Classe | Questions d’impact | Assurance typique |
|---|---|---|
| Fonctionnalité | Quels objectifs, exigences et interfaces changent ? | Vecteurs d’acceptation, tests, docs, revue architecture |
| Bug | Quel comportement attendu a échoué et quelle portée de régression ? | Reproduction, test de régression, analyse de cause |
| Sécurité | Quels actifs, menaces, frontières et abus changent ? | Analyse de menace, tests adversariaux, revue, provenance |
| Architecture | Quels contrats/composants/attributs qualité changent ? | ADR, cohérence/faisabilité, modèles |
| Dépendance/chaîne outils | Quelles hypothèses confiance/build/licence/reproductibilité changent ? | Version/digest, SBOM ou équivalent, compatibilité/sécurité |
| Modèle/spécification formelle | Quelles clauses approuvées sont formalisées et quelle abstraction est omise ? | Contrôles parseur/modèle, contre-exemples, traçabilité |
| Docs/gouvernance | Le contenu est-il normatif, opérationnel ou explicatif ? | Mapping règles, dérive traduction/projection, approbation |
| Release/application | Quels candidat/artefacts exacts sont publiés/appliqués ? | Manifeste, attestations, fraîcheur, reçu identité |

Ce sont des modèles de flux, pas des niveaux d’assurance.

## Rôles et séparation

Les rôles sont des responsabilités logiques ; une personne peut en cumuler plusieurs, mais les actions incompatibles restent distinguables.

- **Contributeur (humain/agent) :** propose, rapporte et fournit des preuves ; sa déclaration n’est pas autorité par elle-même.
- **Implémenteur/agent :** agit dans le périmètre délégué ; ne peut approuver sa propre exception, certifier son autorité ou être l’unique vérificateur de ses preuves lorsqu’une vérification indépendante est requise.
- **Validateur :** contrôle affirmations/preuves avec méthode et contexte identifiés ; l’indépendance est relative à l’affirmation et déclarée.
- **Réviseur :** examine conception, impact, raisonnement et limites ; un commentaire n’est pas une acceptation sauf autorité explicite liée au candidat.
- **Autorité de gouvernance :** approuve règles, exceptions et acceptation dans un périmètre explicite.
- **Opérateur/administrateur :** exploite l’application locale/partagée ; privilèges et contournements sont déclarés.
- **Adaptateur/service :** rapporte opérations/capacités natives ; n’invente pas d’approbation.

Un agent ne peut être l’unique source de vérité sur une commande ou un test lorsqu’une vérification indépendante est requise. Les cumuls de rôles et revues compensatoires sont enregistrés ; les décisions risquées peuvent exiger une séparation.

## Interopérabilité et qualification des agents

La base obligatoire est une CLI documentée, déterministe et à sortie lisible par machine. Les adaptateurs d’agents peuvent améliorer l’ergonomie mais ne contiennent aucune logique normative. MCP a été discuté comme facultatif lors d’une première itération ; ce n’est pas une dépendance obligatoire. Toute interface future appelle la même sémantique que la CLI et ne crée pas de second évaluateur.

La qualification est une affirmation circonscrite sur version d’agent/harness, configuration, permissions et classe de tâche : l’agent sait-il découvrir la gouvernance, préserver les identités, signaler l’incertitude, éviter les actions interdites, recueillir des preuves admissibles, respecter l’autorité humaine et produire un dossier révisable ? Ce n’est ni badge universel ni garantie de bac à sable. Elle est renouvelée si harness, outils, permissions, gouvernance ou environnement changent.

## Dossier institutionnel

Le dossier/historique préserve décisions, justifications, alternatives acceptées/rejetées, ADR, changements de règles, exceptions, résultats de vérification, invalidations et enseignements. Git conserve les changements de fichiers, pas nécessairement l’autorité, la justification, les preuves ou l’expiration d’une exception. Ce dossier auditable n’est pas une mémoire sémantique d’agent. Protéger accès et confidentialité ; ne pas y copier secrets/données privées.

## Limites et séquencement

Une CLI locale ne peut empêcher un contributeur privilégié de contourner hooks ou modifier les fichiers. L’application partagée exige une frontière de confiance qui empêche l’application et revérifie le candidat exact. Signaler un échec ne bloque pas l’application. Les inconnues obligatoires restent inconnues ; demander clarification ou exception gouvernée, ne jamais l’inventer.

Commencer par contrat CLI et dossier réduits, modèles de tâches et vecteurs de conformité indépendants du langage. Valider sur dépôts représentatifs et plusieurs harness avant adaptateurs/intégration distante. Ne pas attendre chaque preuve formelle, mais préserver identités et traçabilité.

## Références bibliographiques

- [R-02 — pratiques de développement sécurisé NIST SP 800-218](../references.fr.md#r-02)
- [R-03 — application des branches protégées GitHub et limites de contournement](../references.fr.md#r-03)
- [R-06 — provenance de chaîne d'approvisionnement in-toto](../references.fr.md#r-06)
- [R-07 — assurance de chaîne logicielle SLSA](../references.fr.md#r-07)
- [R-18 — évaluation de Writ à partir des sources pour les workflows d'agents](../references.fr.md#r-18)
- [R-19 — évaluation de Privateer à partir des sources pour les workflows d'agents](../references.fr.md#r-19)
- [R-16 — contrats d'interface lisibles par machine OpenAPI](../references.fr.md#r-16)
- [R-22 — sémantiques natives Git et Pijul](../references.fr.md#r-22)
