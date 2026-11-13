# Journal des événements du portefeuille — index français

Le journal canonique des événements est conservé dans [Portfolio event journal](events.md). Il s'agit d'un registre append-only : cette page française est un point d'accès documentaire, et non une copie parallèle du journal. Les événements, leur ordre et leur historique de correction restent définis par le fichier canonique.

## Références mobilisées

- [R-05 — TLA+ et TLC](../references.fr.md#r-05)
- [R-107 — Emplacement et syntaxe des workflows GitHub Actions](../references.fr.md#r-107) : modèles formels et éléments de model checking mentionnés dans les événements.
- [R-22 — Sémantiques natives des VCS](../references.fr.md#r-22) : distinction entre les sémantiques des systèmes de contrôle de version et l'ordre du journal canonique.
- [R-194 — Linéarisabilité](../references.fr.md#r-194) : point de linéarisation des ajouts concurrents.
- [R-195 — Journalisation anticipée ARIES](../references.fr.md#r-195) : distinction entre commit durable et reprise.
- [R-196 — RFC 9110, idempotence](../references.fr.md#r-196) : nouvelle tentative après perte de réponse.

Pour consulter les entrées, leur provenance et leurs limites, se reporter au [journal canonique](events.md).

## Dernier événement enregistré

Le journal canonique a enregistré **WP-EVT-000021** : la PR [#125](https://github.com/Martin-PB/govcheck/pull/125) présente le premier audit bilingue de couverture sémantique du métamodèle et corrige deux failles de typage dans le prototype Lean. Les correspondances opérationnelles sont désormais limitées aux relations dont l'obligation de preuve est explicite ; les propositions approximatives, limitées à la traçabilité ou non prises en charge restent non opérationnelles. Toute cible de nature preuve de théorème exige un terme de preuve de la proposition cible exacte.

La compilation Lean 4.19.0 et l'audit des axiomes ont réussi (36 déclarations auditées, aucune dépendance hors liste autorisée ; les théorèmes explicitement rapportés ne dépendent d'aucun axiome). Les contrôles d'intégrité des références et d'alignement du package ont également réussi. La PR reste ouverte, non fusionnée et fusionnable. L'issue #73 reste ouverte ; aucun métamodèle complet n'est adopté.

Le détail et la provenance restent dans le [journal canonique en anglais](events.md#wp-evt-000021).


## Dernier événement — WP-EVT-000022

La fusion de la PR #125 a été confirmée directement auprès de GitHub (`merged=true`, le 13/11/2026 à 14:23:44 UTC ; commit de fusion `2ae091f55ab177560f0f603e07b47c847c740480`). Le chantier dépendant a donc commencé.

La première source retenue est le XML normatif lisible par machine du métamodèle OMG SACM 2.4 Beta 1 (fichier `ptc/26-05-28`, chemin daté du 04/05/2026 ; [R-197](../references.fr.md#r-197)). La bêta reste en cours de traitement ; SACM 2.3 demeure formelle.

La branche `work/sacm-native-metamodel-ingestion` ajoute un importateur qui conserve les octets XML exacts et produit un index structurel distinct. Il n'interprète pas encore la sémantique MOF/XMI et n'infère aucune correspondance vers GovCheck. Le digest attendu provient de l'audit indépendant R-128 ; le workflow GovCheck doit encore vérifier ce digest sur le téléchargement officiel réel.

Détail canonique : [journal anglais WP-EVT-000022](events.md#wp-evt-000022).
