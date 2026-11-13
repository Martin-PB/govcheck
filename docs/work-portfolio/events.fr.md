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

Le journal canonique a enregistré **WP-EVT-000020** : la PR [#122](https://github.com/Martin-PB/govcheck/pull/122) est prête à fusionner après réussite des contrôles d'intégrité des références et d'alignement du package. La PR [#124](https://github.com/Martin-PB/govcheck/pull/124), qui applique le principe de preuve des correspondances au protocole du journal et aux identités VCS, est également déclarée fusionnable ; les contrôles de références, de package, de version et les quatre jobs TLC ont réussi. L'ordre reste impératif : fusionner #122, puis #124. Les anciennes PR #106 et #123 sont fermées sans fusion ; #107 est remplacée par #124.

Le détail et la provenance restent dans le [journal canonique en anglais](events.md#wp-evt-000020).
