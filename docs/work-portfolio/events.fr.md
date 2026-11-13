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

La branche `work/sacm-native-metamodel-ingestion` ajoute un importateur qui conserve les octets XML exacts et produit un index structurel distinct. Il n'interprète pas encore la sémantique MOF/XMI et n'infère aucune correspondance vers GovCheck. Le digest attendu provient de l'audit indépendant [R-128](../references.fr.md#r-128) ; le workflow GovCheck doit encore vérifier ce digest sur le téléchargement officiel réel.

Détail canonique : [journal anglais WP-EVT-000022](events.md#wp-evt-000022).


## Dernier événement — WP-EVT-000023

Le workflow d'ingestion [43443933268](https://github.com/Martin-PB/govcheck/actions/runs/43443933268) a réussi sur le dernier artefact source officiel : cinq tests unitaires réussis, téléchargement OMG, vérification du digest SHA-256 et publication de l'artefact. Le fichier source fait 524 243 octets et son digest est `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`.

L'artefact [sacm-2.4-beta1-source-capture](https://github.com/Martin-PB/govcheck/actions/runs/43443933268/artifacts/14047167094) (ID `14047167094`, rétention 90 jours) contient les trois fichiers : payload XML exact `source.xml`, manifeste `manifest.json` et index structurel `index.json`. Le workflow a été corrigé après une première exécution qui ne publiait que le manifeste et l'index.

Les correspondances typées Claim/Assertion/inférence déjà présentes dans Lean sont recensées dans les deux documents de recherche. Elles restent écrites manuellement et ne sont pas encore dérivées ni validées par le parseur XML. L'inventaire MOF/XMI, le raffinement du parseur, l'import/export d'instances et la conformité SACM restent ouverts.

Détail canonique : [journal anglais WP-EVT-000023](events.md#wp-evt-000023).


## Dernier événement — WP-EVT-000024

La [PR #126](https://github.com/Martin-PB/govcheck/pull/126) est ouverte, non brouillon et fusionnable ; aucune fusion n'a été effectuée. La tête vérifiée au moment de cet enregistrement est `7f3c68f0c710392fa5de5c7a180661f60b0b0500`.

La source officielle retenue est le XML normatif lisible par machine du métamodèle OMG SACM 2.4 Beta 1, fichier `ptc/26-05-28`, révision source `SACM/20260504/SACM2.4_Metamodel.xml` ([R-197](../references.fr.md#r-197), provenance de comparaison [R-128](../references.fr.md#r-128)). Le workflow [43444799397](https://github.com/Martin-PB/govcheck/actions/runs/43444799397) a réussi cinq tests unitaires, le téléchargement officiel et le contrôle du digest sur 524 243 octets : `0581dfa0b9dfaf17ff0f6c63b74f8e7a8396bea03f315e1334e94f23db110830`.

L'artefact [sacm-2.4-beta1-source-capture](https://github.com/Martin-PB/govcheck/actions/runs/43444799397/artifacts/14046408461), ID `14046408461`, contient le XML exact `source.xml`, le manifeste et l'index structurel. Les contrôles d'intégrité des références [43444799378](https://github.com/Martin-PB/govcheck/actions/runs/43444799378), d'alignement du package [43444799366](https://github.com/Martin-PB/govcheck/actions/runs/43444799366) et le contrôle GovCheck en mode rapport seul [43444799488](https://github.com/Martin-PB/govcheck/actions/runs/43444799488) ont également réussi.

Les correspondances typées Lean existantes sont recensées dans la recherche bilingue, mais elles restent manuellement encodées et non dérivées du parseur XML. L'inventaire MOF/XMI, le raffinement du parseur, l'interchange d'instances et les preuves de correspondances dérivées de la source restent à réaliser. La bêta 2.4 demeure en cours de traitement ; SACM 2.3 reste formelle. L'issue #73 reste ouverte.

Détail canonique : [journal anglais WP-EVT-000024](events.md#wp-evt-000024).


## Dernier événement — WP-EVT-000025

L'incrément suivant la fusion de la PR #126 produit un inventaire structurel XMI lié à la source officielle OMG SACM 2.4 Beta 1 épinglée par digest. Le parseur `scripts/parse-sacm-xmi.py` recense 1 616 identifiants XMI uniques, 19 packages UML et un profil, 121 classes, 121 associations, 355 propriétés, 167 généralisations, 8 énumérations (37 littéraux), 40 contraintes, 157 commentaires, 2 types de données, 40 expressions opaques et 3 comportements opaques.

Il enregistre 1 434 références explicites : 1 371 références internes résolues, 63 références externes `href` conservées sans résolution et aucune référence interne non résolue parmi les attributs reconnus. La synthèse générée est versionnée dans [`metamodel-inventory-summary.json`](../..//formal/sources/sacm-2.4-beta1/metamodel-inventory-summary.json). L'inventaire complet sera publié comme artefact du workflow ; il n'est pas ajouté au dépôt comme volumineux fichier généré.

Sept tests synthétiques du parseur réussissent localement et la synthèse produite depuis le payload officiel récupéré correspond à la synthèse versionnée. Le workflow de PR doit encore répéter ces contrôles sur GitHub. Aucune interprétation UML/MOF/OCL, résolution des références externes, preuve de raffinement, réconciliation PDF/XML ou correspondance sémantique vers GovCheck n'est revendiquée. L'issue #73 reste ouverte.

Détail canonique : [journal anglais WP-EVT-000025](events.md#wp-evt-000025).
