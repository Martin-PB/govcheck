# Portefeuille de travaux gouverné

**Statut :** registre initial adossé au dépôt, proposé à la revue du mainteneur. Il établit le point d'ancrage documentaire et la base de migration ; il ne prétend pas qu'un moteur de registre, un event store, un synchroniseur automatique, un stockage immuable ou une frontière d'application soient implémentés.  
**Langue :** l'anglais est la langue par défaut ; voir la [version anglaise](README.md).

## Objet et cycle de vie

Le portefeuille de travaux gouverné est le registre documentaire canonique, indépendant des outils, des travaux proposés et autorisés de GovCheck. Il appartient au dépôt, pas à une issue GitHub, à GitHub Projects ou à un objet propre à une forge.

Il couvre :
- **Entrée (intake) :** signal ou sujet en attente de qualification.
- **Backlog candidat :** travail conservé pour une exécution future éventuelle ; cette conservation ne vaut pas autorisation.
- **Travail engagé :** unité bornée explicitement autorisée par l'autorité compétente.
- **Exécution et clôture :** avancement, preuves, résultats, acceptation, rejet, retrait ou remplacement, avec des sémantiques distinctes.

Le terme *backlog* désigne l'étape des candidats, pas le portefeuille entier. *Élément de travail* désigne une unité bornée. *Portefeuille de travaux* désigne l'ensemble gouverné à tous les stades.

## Autorité et artefacts connexes

Les sémantiques canoniques relèvent du modèle de gouvernance et des spécifications applicables. Le portefeuille enregistre les objets de travail et leurs relations ; il ne crée pas d'autorité normative concurrente.

- Ce répertoire est le registre canonique, dans le dépôt, des éléments de travail GovCheck.
- L'[architecture 0028](../architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md) définit le cycle de vie et la frontière avec les gestionnaires d'issues.
- Les spécifications 0002–0005 définissent les contrats connexes.
- Les décisions/ADR restent l'autorité des décisions adoptées ; les exigences restent dans leurs spécifications ; preuves et résultats gardent leurs identités propres.
- GitHub Issues/Projects, les autres forges et les interfaces locales sont des adaptateurs/projections. Ils coordonnent les échanges mais ne définissent pas l'identité canonique, l'autorité, l'engagement ou l'acceptation.

Un lien vers une issue est une provenance et une correspondance d'adaptateur, pas une délégation d'autorité à cette issue.

## Registre courant

- [Registre des éléments de travail](work-items.md) — import initial des issues #33, #41–#77 et #86, avec identifiants stables, correspondances et dispositions.
- [Journal des événements](events.md) — journal logique append-only.
- [Version anglaise](README.md).

La représentation initiale est en Markdown, lisible par les humains. Aucun format JSON/YAML/RDF, base de données ou langage d'expression n'est choisi. Une représentation machine nécessitera une décision sémantique et technologique distincte et des tests de migration sans perte.

## Identité et révision

Chaque élément logique reçoit un identifiant GovCheck stable (govcheck.work.<slug>), indépendant du titre, chemin, numéro d'issue, forge ou VCS. Les champs descriptifs peuvent évoluer ; les identifiants ne sont jamais réutilisés. Scission, fusion, remplacement et succession sont des relations explicites et peuvent exiger de nouveaux identifiants.

Chaque révision publiée du dépôt est identifiée par l'identité native du VCS et le chemin/contenu exacts. Les identités Git commit/tree/blob et Pijul patch/channel sont complémentaires ; GovCheck ne doit pas fabriquer d'identifiants de type Git pour Pijul. Les empreintes de contenu ne prouvent ni équivalence sémantique, ni vérité, ni autorisation. Voir l'architecture 0017 et l'ADR 0004.

## Sécurité des modifications et historique

L'invariant visé est qu'une modification ordinaire ne puisse pas effacer le dernier état accepté ni réécrire silencieusement une décision. Le processus initial est :

1. Modifier sur une branche/canal dédié, jamais directement dans la base acceptée.
2. Produire un changement révisable, lié à une base et à un candidat exacts.
3. Ajouter une entrée au journal décrivant la transition proposée et sa provenance ; ne jamais modifier ni supprimer une entrée antérieure.
4. Réviser et accepter le candidat exact sous la révision de gouvernance applicable.
5. Préserver la révision acceptée et l'historique VCS natif. Correction, rollback et remplacement sont de nouveaux changements/événements.

**Limite importante :** un historique Git/Pijul ordinaire est un historique de versions, pas un service d'audit inviolable ni une sauvegarde indépendante. Un acteur privilégié ou une forge compromise peut le réécrire. Ce document ne prétend pas empêcher cela. Protection d'intégrité indépendante, références protégées, signatures, réplication, récupération et interception des modifications locales restent à concevoir/implémenter. En attendant, la révision acceptée de la branche principale et son enregistrement de revue/fusion constituent le point de récupération pratique ; les modifications non commitées ne sont pas protégées.

GovCheck doit rendre les opérations dangereuses difficiles ou bloquées, détecter les contournements, préserver les états acceptés antérieurs et permettre la récupération sans dépendre de la discipline de l'éditeur. L'humain ou l'agent qui édite n'est pas le contrôle d'intégrité.

## Sémantique du journal

Le fichier des événements est append-only par politique. Chaque entrée possède un identifiant stable, le sujet, le type d'événement, l'acteur/provenance, la base et la révision résultante si disponibles, la date, la justification, l'autorité/décision et les preuves associées. Une correction est un nouvel événement qui corrige ou remplace explicitement un événement antérieur. Ne jamais modifier silencieusement un ancien événement.

Le journal est actuellement un document du dépôt, pas un stockage append-only dédié et protégé ni un invariant imposé automatiquement. Cette limite reste visible jusqu'à démonstration de contrôles effectifs.

## Contrat d'un élément de travail

Chaque élément doit identifier, selon pertinence : identifiant logique stable et titre ; signal source et provenance ; résultat attendu, périmètre et exclusions ; nature et domaine ; état du cycle de vie ; priorité et justification, distinctes de l'autorité ; hypothèses, inconnues et risques ; exigences, décisions et dépendances ; critères d'achèvement et méthode de vérification ; acteur responsable et décision d'autorisation pour tout travail engagé ; changements, preuves, résultats et acceptations liés ; correspondances d'adaptateurs ; révisions et historique d'événements.

Une information inconnue reste explicitement inconnue. Un champ absent n'est pas implicitement satisfait. Un regroupement parent ne transmet ni priorité, ni dépendance, ni autorité, ni engagement, ni acceptation.

## Adaptateurs et transition

GitHub reste utile pendant la migration :
- les issues restent ouvertes lorsqu'elles coordonnent des candidats actifs ou des discussions ;
- #40 et #78–#85 deviennent des vues de navigation/coordination pointant vers le registre ;
- les numéros d'issues restent des identifiants externes et une provenance historique ;
- aucune issue n'est clôturée uniquement parce que son contenu a été importé ; la clôture exige une résolution et un lien canonique/successeur ;
- la migration est additive : aucune issue, aucun commentaire ni échange source n'est supprimé ;
- la synchronisation est d'abord explicite/manuelle ; les divergences sont signalées, pas réconciliées silencieusement. L'autorité va du registre du dépôt vers la projection adaptateur.

Il ne s'agit pas encore d'une synchronisation opérationnelle. Contrat d'adaptateur, tests aller-retour sans perte et contrôles de dérive restent nécessaires.

## Contrôles futurs

Le registre initial est un document contrôlé, pas un service exécutable. Les travaux futurs doivent spécifier et valider : identités de révision/événement immuables entre Git et Pijul ; mises à jour atomiques et concurrence ; application append-only et détection d'altération ; points de récupération, réplication indépendante et exercices de restauration ; autorisation et applicabilité prospective des révisions de gouvernance ; adaptateurs sans perte ; contrôles déterministes des transitions, provenance, liens, preuves périmées et dérive ; scénarios d'écrasement accidentel, éditeur malveillant, forge compromise, force-push, suppression, concurrence et rollback.

Aucune prévention, immutabilité ou application effective n'est revendiquée tant que des tests et/ou une vérification formelle n'ont pas démontré la propriété dans un modèle de menace déclaré.

## Références GovCheck

- [Architecture 0028](../architecture/0028-governed-work-portfolio-and-issue-tracker-boundary.fr.md).
- [Spécification 0002](../specifications/0002-canonical-governance-model.fr.md).
- [Spécification 0003](../specifications/0003-change-lifecycle.fr.md).
- [Spécification 0004](../specifications/0004-vcs-collaboration-contracts.fr.md).
- [Architecture 0017](../architecture/0017-artifact-identity-revision-and-versioning.fr.md) et [ADR 0004 / Architecture 0018](../architecture/0018-version-governance-and-compatibility-authority.fr.md).
- [Architecture 0012](../architecture/0012-normative-authority-and-documentation.fr.md).
- [Catalogue des références](../references.fr.md), notamment R-24 (vocabulaire de provenance PROV), lorsque pertinent.

Une référence n'implique ni adoption, ni implémentation, ni assurance.
