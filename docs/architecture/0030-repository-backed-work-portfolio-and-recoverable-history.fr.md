# 0030 — Registre du portefeuille gouverné dans le dépôt et historique révisable/récupérable

**Statut :** proposition d'architecture soumise à la revue du mainteneur ; le registre Markdown initial est créé sur cette branche, mais aucun stockage append-only imposé par machine, service de récupération, synchroniseur de forge ou contrôle d'interception des modifications n'est implémenté.  
**Langue :** l'anglais est la langue par défaut ; voir la [version anglaise](0030-repository-backed-work-portfolio-and-recoverable-history.md).

## 1. Contexte et problème

L'architecture 0028 sépare correctement l'entrée, le backlog candidat et le travail engagé, et traite correctement GitHub Issues/Projects comme un adaptateur opérationnel plutôt que comme l'autorité de gouvernance. Sa lacune était l'absence d'un registre canonique dans le dépôt et d'un contrat suffisamment robuste de révision et de récupération.

Le corps d'une issue est mutable et propre à une forge. L'historique d'activité GitHub constitue une provenance utile, mais pas un modèle canonique portable de révision documentaire, une garantie de conservation intégrale ni un mécanisme indépendant de récupération. Demander aux humains ou aux agents de se souvenir de ne pas écraser le contenu antérieur transfère l'obligation d'intégrité à l'éditeur et contredit la philosophie préventive de GovCheck, où les erreurs doivent être récupérables par défaut.

GovCheck doit permettre à l'éditeur de se tromper sans détruire silencieusement le dernier état de gouvernance accepté. Il doit prévenir les transitions dangereuses lorsqu'il le peut, détecter les contournements lorsque la prévention est hors de sa frontière, préserver les états antérieurs et permettre la récupération.

## 2. Décision d'architecture proposée

Établir un **registre du portefeuille de travaux gouverné, adossé au dépôt**, dans docs/work-portfolio/, comme enregistrement documentaire canonique des éléments de travail GovCheck et de leurs relations. Le registre est indépendant des objets de travail propres aux forges et aux VCS.

Les artefacts initiaux sont :
- README.md / README.fr.md — objet, sémantique, cycle de vie et contrat opératoire ;
- work-items.md — identités stables, résultats attendus, classification et correspondances sources ;
- events.md — journal logique des événements, append-only par politique.

Le registre est un artefact de portefeuille, pas un moteur de règles normatives concurrent. Ses sémantiques sont contraintes par le modèle canonique de gouvernance, la spécification du cycle de vie, la politique d'identité des artefacts et les décisions adoptées.

La représentation Markdown initiale est volontairement provisoire. Cette décision ne choisit ni JSON, ni YAML, ni RDF, ni base de données, ni produit d'event sourcing, ni langage d'expression, ni service de stockage. Un format machine-readable nécessitera une décision distincte après définition du contrat sémantique et tests de migration sans perte.

## 3. Vocabulaire et périmètre

- **Portefeuille de travaux :** ensemble gouverné des travaux à travers leur cycle de vie.
- **Backlog :** étape des candidats uniquement, pas le portefeuille entier.
- **Élément de travail :** unité bornée ayant un résultat attendu et des conditions d'achèvement évaluables indépendamment.
- **Registre :** collection canonique adossée au dépôt, avec métadonnées d'identité et de révision.
- **Adaptateur :** forge, tableau de projet, interface locale ou système de collaboration qui présente/coordonne les objets sans en devenir l'autorité.
- **Événement :** occurrence logique immuable décrivant une transition, décision, correction, autorisation, invalidation ou résultat.

Les états du cycle de vie restent ceux de l'architecture 0028 : Entrée → Backlog candidat → Travail engagé, puis exécution, blocage, validation et résolutions terminales typées. Priorité, assignation, ouverture d'une issue, appartenance à un projet et parenté n'autorisent jamais le travail.

## 4. Identité canonique et correspondance des adaptateurs

Chaque élément logique DOIT avoir un identifiant stable, indépendant du titre, nom de fichier, forge, numéro d'issue et VCS. Les identifiants ne sont jamais réutilisés. Scissions, fusions, doublons, successeurs et remplacements sont des relations typées explicites. Un numéro d'issue n'est conservé que comme correspondance d'adaptateur externe et référence de provenance.

L'enregistrement devrait contenir : résultat, périmètre/exclusions, source/provenance, nature/domaine, état du cycle de vie, priorité et justification, hypothèses/inconnues, risques, exigences, décisions, dépendances, critères d'achèvement, méthode de vérification, acteur responsable, décision d'autorisation pour tout travail engagé, liens vers résultats/preuves, correspondances d'adaptateurs et historique des révisions/événements.

Un regroupement parent est uniquement organisationnel. Il ne transmet ni dépendance, ni priorité, ni autorité, ni engagement, ni acceptation.

## 5. Révisions, événements et récupération

La conception distingue :

1. **Projection courante du registre :** état lisible de chaque élément.
2. **Historique logique des événements :** séquence préservée des changements et décisions ; les corrections ajoutent des événements.
3. **Historique natif du dépôt :** révisions VCS exactes qui préservent les états documentaires acceptés.

Le journal initial adopte une sémantique append-only par politique. Chaque événement devrait identifier : ID d'événement, ID du sujet, type, acteur/provenance, date, révision de base/résultante si disponible, justification, autorité/décision et preuves associées. Correction et rollback sont de nouveaux événements, jamais des modifications d'événements antérieurs.

La révision acceptée du dépôt est le premier point de récupération pratique. Les changements sont préparés sur une branche/un canal dédié et révisés par rapport à une base et un candidat exacts. Une modification non commitée dans l'arbre de travail n'est pas une révision protégée.

**Limite critique :** l'historique Git/Pijul seul ne fournit ni audit inviolable complet ni garantie de sauvegarde indépendante. Un acteur privilégié ou un service d'hébergement compromis peut réécrire ou supprimer l'historique. Un fichier Markdown append-only par politique n'est pas physiquement append-only du seul fait de cette politique. Tant que l'application n'existe pas, l'architecture DOIT le dire et NE DOIT PAS revendiquer l'immutabilité ou la prévention.

Les contrôles futurs doivent évaluer références protégées, réplication indépendante, signatures/attestations, empreintes, snapshots immuables, interception des modifications locales, autorisation, mises à jour concurrentes, récupération et tests de restauration. Le choix technologique doit préserver les sémantiques Git et Pijul et ne pas rendre une forge hébergée obligatoire.

## 6. Propriétés de sécurité et scénarios de menace

Le contrat d'implémentation devra démontrer :

- **Pas de perte silencieuse :** un état accepté antérieur reste récupérable après modification ordinaire, rejet, rollback ou remplacement.
- **Pas de réécriture d'événement :** corrections et révocations sont de nouveaux événements ; les anciens restent adressables.
- **Liaison exacte :** décisions et preuves se rapportent aux révisions exactes de l'élément, de la gouvernance et du candidat.
- **Pas d'autorisation implicite :** éditer un enregistrement, changer une priorité, assigner une issue ou déplacer une carte ne peut engager un travail.
- **Sécurité concurrente :** des modifications concurrentes ne s'écrasent pas silencieusement ; un candidat périmé exige rebase/réévaluation.
- **Adaptateur non autoritaire :** une modification côté forge ne peut remplacer silencieusement le registre canonique.
- **Incertitude visible :** provenance manquante, état inconnu ou historique indisponible bloque ou reste explicitement indéterminé.
- **Récupérabilité :** une procédure de restauration documentée reconstruit un état accepté antérieur et sa traçabilité.

Scénarios : écrasement accidentel, contributeur malveillant, mainteneur/forge compromis, force-push ou réécriture de canal, suppression, modifications concurrentes, synchronisation d'adaptateur périmée, journal corrompu, clé compromise et sauvegarde incomplète. Chaque propriété doit être bornée par un modèle de menace explicite ; aucun mécanisme unique n'est supposé tout résoudre.

## 7. Transition des adaptateurs

Les issues GitHub #40 et #78–#85 restent ouvertes pendant la migration comme vues de navigation et de coordination. Les issues de travail #41–#77 et #86 restent associées par leurs numéros sources. L'issue #33 reste un candidat atomique. Les issues historiques et leurs commentaires sont préservés et liés comme provenance.

La migration est additive :
- aucune issue ni aucun commentaire n'est supprimé ;
- une issue n'est pas clôturée simplement parce que son contenu a été importé ;
- les travaux terminés, doublons ou remplacés reçoivent une disposition explicite et un lien vers leur résultat/successeur ;
- le registre du dépôt est l'autorité ; les modifications d'issues ne sont pas automatiquement autoritaires ;
- la synchronisation est d'abord explicite/manuelle, les dérives étant signalées plutôt que résolues silencieusement.

Un adaptateur opérationnel exige un contrat distinct et des tests aller-retour sur les identifiants, relations, provenance, historique d'événements, états et décisions. Import/export ne doit perdre ni inventer de sémantique.

## 8. Relation avec l'architecture existante

Ce document complète l'architecture 0028 et est contraint par :
- Spécification 0002 — Modèle canonique de gouvernance ;
- Spécification 0003 — Cycle de vie des changements et acceptation ;
- Spécification 0004 — Contrats VCS et collaboration ;
- Architecture 0012 — Autorité normative canonique et conformité documentaire ;
- Architecture 0017 et ADR 0004 — Identité, révision et versionnement des artefacts ;
- Architecture 0018 — Gouvernance des versions, compatibilité et autorité d'approbation.

La spécification 0003 exige déjà des transitions auditables et un historique logique append-only. L'architecture 0017 distingue identité logique, identité de révision immuable, version de contrat et identité d'événement/instance. Ce document applique ces distinctions au portefeuille ; il ne remplace pas ces contrats.

## 9. Base de migration

Le registre initial docs/work-portfolio/work-items.md importe les candidats actifs des issues #41–#77 et #86, ainsi que l'issue atomique #33. Il conserve #40 et #78–#85 comme vues adaptateurs. Les issues historiques #23, #26, #30, #35 et #37 restent des sources de provenance ; #61 est reliée comme prédécesseur doublon de #62. L'issue #46 est enregistrée comme terminée au regard de la PR #39 fusionnée / ADR 0005, sa clôture étant différée jusqu'à acceptation de cette PR de registre. L'issue #75 reste ouverte en attente d'adoption formelle.

L'import capture identité stable, résultat attendu, source, classification et disposition. Il ne copie pas chaque commentaire conversationnel dans le registre canonique ; les discussions sources restent accessibles et ne sont pas élevées silencieusement au rang de décisions adoptées.

## 10. Séquence d'implémentation

1. Réviser et adopter les sémantiques du registre et la base de migration.
2. Définir un contrat machine-readable des éléments/événements sans choisir prématurément une technologie de stockage.
3. Définir application append-only, mises à jour atomiques, concurrence et garanties de récupération.
4. Définir les liaisons de révision natives Git/Pijul et un contrat d'adaptateur neutre.
5. Implémenter contrôles déterministes d'intégrité/dérive et tests négatifs d'écrasement, suppression, mise à jour périmée et transition non autorisée.
6. Ajouter réplication indépendante et exercices de restauration selon le modèle de menace.
7. Migrer ensuite seulement des vues adaptateurs manuelles vers une synchronisation contrôlée.

## 11. Absence de revendications

Cette architecture ne prétend pas que le journal Markdown actuel est inviolable, que les modifications d'issues GitHub sont bloquées, que sauvegardes/signatures/réplication existent, que tous les commentaires historiques ont été importés, ni que le futur moteur de registre est implémenté ou formellement vérifié. La migration initiale constitue une base documentée et révisable, pas encore les garanties visées.
